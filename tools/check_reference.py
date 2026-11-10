"""Optional PM4Py2.7.23 semantics reference, not runtime dependency or vendored code."""
import json,sys,importlib.metadata
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'tests')]
from firelab.engine import analyze
from firelab.controls import controls
from test_core import generated
from pm4py.objects.petri_net.obj import PetriNet,Marking
from pm4py.objects.petri_net.utils.petri_utils import add_arc_from_to
from pm4py.objects.petri_net import semantics
assert importlib.metadata.version('pm4py')=='2.7.23'
requests=[c['input']for c in controls()]+list(generated(seed=7301,number=150));state_checks=move_checks=words=0
for p in requests:
 net=PetriNet('reference');ps=[PetriNet.Place(str(i))for i in range(p['places'])];net.places.update(ps);ts=[]
 for j,t in enumerate(p['transitions']):
  tr=PetriNet.Transition(str(j),str(j));net.transitions.add(tr);ts.append(tr)
  for i,w in enumerate(t['pre']):
   if w:add_arc_from_to(ps[i],tr,net,weight=w)
  for i,w in enumerate(t['post']):
   if w:add_arc_from_to(tr,ps[i],net,weight=w)
 def mark(a):return Marking({ps[i]:v for i,v in enumerate(a)if v})
 def vector(m):return[m[x]for x in ps]
 r=analyze(p)
 for row in r['states']:
  state_checks+=1;m=mark(row['marking']);en=semantics.enabled_transitions(net,m)
  assert sorted(ts.index(t)for t in en)==[e['transition']for e in row['moves']if e['successor']is not None]
  for e in row['moves']:
   move_checks+=1;dst=semantics.execute(ts[e['transition']],net,m)
   assert (dst is None)==(e['successor']is None)
   if dst is not None:assert vector(dst)==r['states'][e['successor']]['marking']
 # Exhaust the actual PM4Py reachable graph, with no external timeout/truncation.
 seen={tuple(p['initial']):[]};active=[mark(p['initial'])]
 while active:
  m=active.pop(0);seq=seen[tuple(vector(m))]
  for t in sorted(semantics.enabled_transitions(net,m),key=lambda t:int(t.name)):
   dst=semantics.execute(t,net,m);key=tuple(vector(dst))
   if key not in seen:seen[key]=seq+[int(t.name)];active.append(dst)
 assert sorted(seen)==sorted(tuple(r['states'][i]['marking'])for i in r['summary']['reachable_states'])
 goal=tuple(p['goal']);assert(goal in seen)==r['summary']['goal_reachable']
 if goal in seen:assert len(seen[goal])==r['summary']['goal_distance']
 def schedule(m,cs):
  if not any(cs):return 1
  count=0
  for j,c in enumerate(cs):
   if c:
    nm=semantics.execute(ts[j],net,m)
    if nm is not None:
     rest=cs.copy();rest[j]-=1;count+=schedule(nm,rest)
  return count
 count=schedule(mark(p['initial']),p['counts']);assert count==r['summary']['count_schedule_count'];words+=count
print(json.dumps(dict(reference='PM4Py',version=importlib.metadata.version('pm4py'),requests=len(requests),state_checks=state_checks,transition_checks=move_checks,accepted_count_words=words)))
