import copy,itertools,json,random,subprocess,sys,tempfile,unittest
from pathlib import Path
from firelab.engine import analyze
from firelab.certificate import verify,reconstruct
from firelab.model import loads,parse
from firelab.controls import controls

def generated(seed=1927,number=120):
 rng=random.Random(seed)
 for _ in range(number):
  n=rng.randrange(2,5);total=rng.randrange(4);s=[0]*n;g=[0]*n
  for i in range(total):s[rng.randrange(n)]+=1;g[rng.randrange(n)]+=1
  ts=[]
  for j in range(rng.randrange(5)):
   w=rng.randrange(3);a=[0]*n;b=[0]*n
   for k in range(w):a[rng.randrange(n)]+=1;b[rng.randrange(n)]+=1
   ts.append({'pre':a,'post':b})
  cs=[rng.randrange(3)for t in ts]
  yield{'version':1,'places':n,'initial':s,'goal':g,'transitions':ts,'counts':cs}

def leaves(x,path=()):
 if type(x)is dict:
  for k,v in x.items():
   if path==()and k=='input':continue
   yield from leaves(v,path+(k,))
 elif type(x)is list:
  for i,v in enumerate(x):yield from leaves(v,path+(i,))
 else:yield path,x

def altered(r,path,val):
 z=copy.deepcopy(r);a=z
 for k in path[:-1]:a=a[k]
 a[path[-1]]=val;return z

class Core(unittest.TestCase):
 def test_controls(self):
  for c in controls():self.assertTrue(verify(analyze(c['input']))['valid'],c['title'])
 def test_helper_distinction(self):
  r=analyze(controls()[0]['input']);s=r['summary'];self.assertTrue(s['balance']);self.assertFalse(s['count_realizable']);self.assertEqual(s['goal_witness'],[1,0,2]);self.assertEqual(s['goal_distance'],3)
 def test_helper_counts(self):
  s=analyze(controls()[1]['input'])['summary'];self.assertEqual(s['count_witness'],[1,0,2]);self.assertEqual(s['count_schedule_count'],1)
 def test_global_impossible(self):
  s=analyze(controls()[2]['input'])['summary'];self.assertTrue(s['balance']);self.assertFalse(s['goal_reachable']);self.assertEqual(s['reachable_deadlocks'],s['reachable_states'])
 def test_self_loop_guard(self):
  r=analyze(controls()[2]['input']);self.assertEqual(r['incidence'][0],[0]);self.assertEqual(r['states'][0]['moves'][0]['missing'],[[0,1]])
 def test_order_count(self):self.assertEqual(analyze(controls()[4]['input'])['summary']['count_schedule_count'],2)
 def test_duplicate_ids(self):self.assertEqual(analyze(controls()[5]['input'])['summary']['goal_shortest_count'],2)
 def test_not_liveness(self):
  r=analyze(controls()[9]['input']);self.assertFalse(r['summary']['goal_reachable']);self.assertEqual(r['summary']['reachable_deadlocks'],[])
 def test_empty_and_vacuum(self):
  self.assertEqual(analyze(controls()[10]['input'])['summary']['count_schedule_count'],1);self.assertTrue(analyze(controls()[11]['input'])['summary']['count_realizable'])
 def test_multiset_boundary(self):self.assertEqual(analyze(controls()[12]['input'])['summary']['count_schedule_count'],2520)
 def test_negative_rows(self):self.assertTrue(any(not r['nonnegative']for r in analyze(controls()[13]['input'])['count_lattice']))
 def test_seeded(self):
  for p in generated(number=350):self.assertEqual(analyze(p),reconstruct(p))
 def test_exhaustive(self):
  vs=[list(v)for v in itertools.product(range(3),repeat=2)if sum(v)<=2];ts=[{'pre':a,'post':b}for a in vs for b in vs if sum(a)==sum(b)];count=0
  for a,b in itertools.product(ts,repeat=2):
   for s in vs:
    for cs in itertools.product(range(2),repeat=2):
     p={'version':1,'places':2,'initial':s,'goal':list(reversed(s)),'transitions':[a,b],'counts':list(cs)};self.assertEqual(analyze(p),reconstruct(p));count+=1
  self.assertEqual(count,4704)
 def test_every_primitive_forgery(self):
  r=analyze(controls()[0]['input']);count=0
  for path,val in leaves(r):
   v=(not val)if type(val)is bool else val+1 if type(val)is int else 'wrong'if type(val)is str else 0
   self.assertFalse(verify(altered(r,path,v))['valid'],str(path));count+=1
  self.assertEqual(count,197)
 def test_strict_types(self):
  p=controls()[0]['input']
  for key,val in [('places',True),('version',1.0),('counts',[True,0,0]),('initial',[0,0,4]),('extra',0)]:
   z=copy.deepcopy(p);z[key]=val
   with self.assertRaises(ValueError):parse(z)
  z=copy.deepcopy(p);z['transitions'][0]['post']=[2,1,0]
  with self.assertRaises(ValueError):parse(z)
 def test_strict_json(self):
  for t in ['{"a":1,"a":2}','{"a":1.0}','NaN','Infinity']:
   with self.assertRaises(ValueError):loads(t)
 def test_exact_report_schema(self):
  r=analyze(controls()[0]['input']);r['extra']=1;self.assertFalse(verify(r)['valid']);r.pop('extra');r['summary']['count_schedule_count']=False;self.assertFalse(verify(r)['valid'])
 def test_cli_atomic(self):
  with tempfile.TemporaryDirectory()as d:
   f=Path(d)/'x.json';f.write_text('{"version":1,"version":1}');out=subprocess.run([sys.executable,'-m','firelab','run',str(f)],capture_output=True,text=True);self.assertEqual(out.returncode,2);self.assertFalse(out.stdout)
if __name__=='__main__':unittest.main()
