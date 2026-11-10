"""BFS marking graph and dynamic programming on a firing-count lattice."""
from collections import deque
from itertools import product
from .model import parse

def analyze(p):
 n,ts=parse(p);q=len(ts);total=sum(p['initial']);goal=tuple(p['goal']);start=tuple(p['initial'])
 markings=[a for a in product(range(total+1),repeat=n)if sum(a)==total];index={a:i for i,a in enumerate(markings)}
 matrix=[[t['post'][i]-t['pre'][i]for t in ts]for i in range(n)]
 def decisions(m):
  out=[]
  for j,t in enumerate(ts):
   missing=[[i,t['pre'][i]-m[i]]for i in range(n)if m[i]<t['pre'][i]]
   nxt=None if missing else [m[i]+matrix[i][j]for i in range(n)]
   out.append({'transition':j,'missing':missing,'successor':None if nxt is None else index[tuple(nxt)]})
  return out
 moves=[decisions(m)for m in markings];adj=[[a['successor']for a in ms if a['successor']is not None]for ms in moves];rev=[[]for _ in markings]
 for i,vs in enumerate(adj):
  for v in vs:rev[v].append(i)
 def bfs(roots,edges):
  ds=[None]*len(markings);todo=deque(roots)
  for a in roots:ds[a]=0
  while todo:
   a=todo.popleft()
   for b in edges[a]:
    if ds[b]is None:ds[b]=ds[a]+1;todo.append(b)
  return ds
 si=index[start];gi=index.get(goal);distance=bfs([si],adj);remaining=bfs([]if gi is None else[gi],rev)
 paths=[None]*len(markings);paths[si]=[];ways=[0]*len(markings);ways[si]=1
 for i in sorted(range(len(markings)),key=lambda a:distance[a]if distance[a]is not None else 999):
  if distance[i]is None:continue
  for a in moves[i]:
   j=a['successor']
   if j is not None and distance[j]==distance[i]+1:
    w=paths[i]+[a['transition']];ways[j]+=ways[i]
    if paths[j]is None or w<paths[j]:paths[j]=w
 shortest=[[a['transition']for a in moves[i]if a['successor']is not None and remaining[i]is not None and remaining[i]>0 and remaining[a['successor']]==remaining[i]-1]for i in range(len(markings))]
 states=[{'id':i,'marking':list(m),'distance':distance[i],'shortest_prefix_count':ways[i],'prefix':paths[i],'to_goal':remaining[i],'optimal_next':shortest[i],'deadlock':not adj[i],'moves':moves[i]}for i,m in enumerate(markings)]
 activity=[]
 for j in range(q):
  en=[i for i in range(len(markings))if distance[i]is not None and moves[i][j]['successor']is not None]
  best=min(en,key=lambda i:(distance[i],paths[i],i))if en else None
  activity.append({'transition':j,'enabling_states':en,'dead':not en,'prefix':None if best is None else paths[best]})
 counts=p['counts'];vectors=sorted(product(*(range(c+1)for c in counts)),key=lambda a:(sum(a),a));ix={a:i for i,a in enumerate(vectors)}
 algebra=[[start[i]+sum(matrix[i][j]*k[j]for j in range(q))for i in range(n)]for k in vectors]
 nexts=[]
 for k,m in zip(vectors,algebra):
  valid=all(a>=0 for a in m);row=[]
  for j,t in enumerate(ts):
   if k[j]==counts[j]:continue
   missing=[[i,t['pre'][i]-m[i]]for i in range(n)if m[i]<t['pre'][i]]
   dst=list(k);dst[j]+=1
   row.append({'transition':j,'target':ix[tuple(dst)],'missing':missing,'enabled':valid and not missing})
  nexts.append(row)
 forward=[0]*len(vectors);forward[0]=1;backward=[0]*len(vectors);backward[-1]=int(all(a>=0 for a in algebra[-1]));prefix=[None]*len(vectors);prefix[0]=[];suffix=[None]*len(vectors);suffix[-1]=[]if backward[-1]else None
 for a,row in enumerate(nexts):
  for e in row:
   b=e['target']
   if e['enabled']:
    forward[b]+=forward[a]
    if prefix[a]is not None:
     cand=prefix[a]+[e['transition']]
     if prefix[b]is None or cand<prefix[b]:prefix[b]=cand
 for a in range(len(vectors)-2,-1,-1):
  for e in nexts[a]:
   b=e['target']
   if e['enabled']:
    backward[a]+=backward[b]
    if suffix[b]is not None:
     cand=[e['transition']]+suffix[b]
     if suffix[a]is None or cand<suffix[a]:suffix[a]=cand
 lattice=[{'id':i,'used':list(k),'marking':algebra[i],'nonnegative':all(a>=0 for a in algebra[i]),'prefix_count':forward[i],'suffix_count':backward[i],'prefix':prefix[i],'suffix':suffix[i],'choices':nexts[i]}for i,k in enumerate(vectors)]
 balance=algebra[-1]==list(goal);reachable=gi is not None and distance[gi]is not None
 return {'schema':'firelab-1','input':p,'invariant':{'weights':[1]*n,'total':total,'goal_total':sum(goal),'column_sums':[sum(matrix[i][j]for i in range(n))for j in range(q)]},'incidence':matrix,'states':states,'activity':activity,'count_lattice':lattice,'summary':{'balance':balance,'count_realizable':forward[-1]>0,'count_schedule_count':forward[-1],'count_goal_schedule_count':forward[-1]if balance else 0,'count_witness':prefix[-1],'goal_reachable':reachable,'goal_distance':None if gi is None else distance[gi],'goal_shortest_count':0 if gi is None else ways[gi],'goal_witness':None if gi is None else paths[gi],'reachable_states':[i for i,d in enumerate(distance)if d is not None],'reachable_deadlocks':[i for i,d in enumerate(distance)if d is not None and not adj[i]]}}
