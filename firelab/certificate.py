"""Separate all-pairs/word-enumeration replay; imports validation, not the engine."""
from itertools import product
from .model import parse

def reconstruct(p):
 n,ts=parse(p);q=len(ts);s=p['initial'];g=p['goal'];total=sum(s)
 # Recursively distribute a fixed token total rather than use generator's product filter.
 def compositions(left,k):
  if k==1:return[[left]]
  return[[v]+rest for v in range(left+1)for rest in compositions(left-v,k-1)]
 ms=compositions(total,n);N=len(ms);root=ms.index(s);goal=ms.index(g)if g in ms else None
 mat=[[t['post'][a]-t['pre'][a]for t in ts]for a in range(n)]
 def step(m,t):
  bag={a:m[a]for a in range(n)}
  for a,w in enumerate(t['pre']):
   if bag[a]<w:return None
  for a,w in enumerate(t['pre']):bag[a]-=w
  for a,w in enumerate(t['post']):bag[a]+=w
  return[bag[a]for a in range(n)]
 moves=[];dist=[[N+1]*N for _ in ms]
 for i,m in enumerate(ms):
  dist[i][i]=0;row=[]
  for j,t in enumerate(ts):
   result=step(m,t);dst=None if result is None else ms.index(result)
   row.append({'transition':j,'missing':[[a,t['pre'][a]-m[a]]for a in range(n)if t['pre'][a]>m[a]],'successor':dst})
   if dst is not None:dist[i][dst]=min(dist[i][dst],1)
  moves.append(row)
 for k in range(N):
  for i in range(N):
   for j in range(N):dist[i][j]=min(dist[i][j],dist[i][k]+dist[k][j])
 def distance(i,j):return None if dist[i][j]>N else dist[i][j]
 # All shortest incoming choices, using a recursion unlike forward BFS.
 memo={root:(1,[])}
 def prefixes(v):
  if v in memo:return memo[v]
  d=distance(root,v)
  if d is None:return(0,None)
  count=0;best=None
  for a in range(N):
   if distance(root,a)!=d-1:continue
   for e in moves[a]:
    if e['successor']==v:
     c,w=prefixes(a);count+=c;cand=w+[e['transition']]
     if best is None or cand<best:best=cand
  memo[v]=(count,best);return memo[v]
 states=[]
 for i,m in enumerate(ms):
  d=distance(root,i);rem=None if goal is None else distance(i,goal);ways,path=prefixes(i)
  opt=[e['transition']for e in moves[i]if e['successor']is not None and rem is not None and rem>0 and distance(e['successor'],goal)==rem-1]
  states.append({'id':i,'marking':m,'distance':d,'shortest_prefix_count':ways,'prefix':path,'to_goal':rem,'optimal_next':opt,'deadlock':all(e['successor']is None for e in moves[i]),'moves':moves[i]})
 activity=[]
 for j in range(q):
  en=[i for i in range(N)if distance(root,i)is not None and step(ms[i],ts[j])is not None]
  best=min(en,key=lambda i:(distance(root,i),prefixes(i)[1],i))if en else None
  activity.append({'transition':j,'enabling_states':en,'dead':not en,'prefix':None if best is None else prefixes(best)[1]})
 cs=p['counts'];vectors=[list(a)for a in product(*(range(c+1)for c in cs))];vectors.sort(key=lambda a:(sum(a),a));rows=[]
 # Enumerate every distinct transition-ID word of a given multiset, testing actual markings.
 # No generator DP or lattice recurrence is used to count schedules.
 def schedules(m,bag):
  if not any(bag):return[[]]if min(m)>=0 else[]
  out=[]
  for j,c in enumerate(bag):
   if c:
    nm=step(m,ts[j])
    if nm is not None:
     b=bag.copy();b[j]-=1
     out.extend([[j]+rest for rest in schedules(nm,b)])
  return out
 for i,k in enumerate(vectors):
  marking=[s[a]+sum(k[j]*(ts[j]['post'][a]-ts[j]['pre'][a])for j in range(q))for a in range(n)]
  pre=schedules(s,k);suf=schedules(marking,[cs[j]-k[j]for j in range(q)])if min(marking)>=0 else[];choices=[]
  for j,c in enumerate(k):
   if c==cs[j]:continue
   dest=k.copy();dest[j]+=1;t=ts[j];missing=[[a,t['pre'][a]-marking[a]]for a in range(n)if marking[a]<t['pre'][a]]
   choices.append({'transition':j,'target':vectors.index(dest),'missing':missing,'enabled':min(marking)>=0 and not missing})
  rows.append({'id':i,'used':k,'marking':marking,'nonnegative':min(marking)>=0,'prefix_count':len(pre),'suffix_count':len(suf),'prefix':min(pre)if pre else None,'suffix':min(suf)if suf else None,'choices':choices})
 balance=rows[-1]['marking']==g;count=rows[-1]['prefix_count'];reachable=goal is not None and distance(root,goal)is not None
 return{'schema':'firelab-1','input':p,'invariant':{'weights':[1]*n,'total':total,'goal_total':sum(g),'column_sums':[sum(mat[a][j]for a in range(n))for j in range(q)]},'incidence':mat,'states':states,'activity':activity,'count_lattice':rows,'summary':{'balance':balance,'count_realizable':count>0,'count_schedule_count':count,'count_goal_schedule_count':count if balance else 0,'count_witness':rows[-1]['prefix'],'goal_reachable':reachable,'goal_distance':None if goal is None else distance(root,goal),'goal_shortest_count':0 if goal is None else prefixes(goal)[0],'goal_witness':None if goal is None else prefixes(goal)[1],'reachable_states':[i for i in range(N)if distance(root,i)is not None],'reachable_deadlocks':[i for i,r in enumerate(states)if r['distance']is not None and r['deadlock']]}}

def same(a,b):
 if type(a)is not type(b):return False
 if type(a)is dict:return a.keys()==b.keys()and all(same(a[k],b[k])for k in a)
 if type(a)is list:return len(a)==len(b)and all(same(x,y)for x,y in zip(a,b))
 return a==b

def verify(report):
 try:
  if type(report)is not dict or 'input'not in report:raise ValueError('report object/input required')
  expected=reconstruct(report['input'])
  if not same(report,expected):raise ValueError('complete report differs from independent replay')
  return{'valid':True,'schema':'firelab-1'}
 except(ValueError,TypeError,KeyError,RecursionError)as e:return{'valid':False,'error':str(e)}
