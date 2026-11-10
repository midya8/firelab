"""Ordinary, strictly conservative, finite weighted P/T nets."""
import json

def keys(x,expected):
 if type(x)is not dict or set(x)!=set(expected):raise ValueError('unexpected fields')
def integer(x):
 if type(x)is not int:raise ValueError('expected non-boolean integer')
 return x
def parse(p):
 keys(p,['version','places','initial','goal','transitions','counts'])
 if integer(p['version'])!=1:raise ValueError('version must be 1')
 n=integer(p['places'])
 if not 2<=n<=4:raise ValueError('places must be 2..4')
 def vec(v,top=3):
  if type(v)is not list or len(v)!=n or any(not 0<=integer(a)<=top for a in v):raise ValueError('bounded marking/arc vector required')
 vec(p['initial']);vec(p['goal'])
 if sum(p['initial'])>3:raise ValueError('initial total at most 3')
 ts=p['transitions']
 if type(ts)is not list or len(ts)>4:raise ValueError('at most 4 transitions')
 for t in ts:
  keys(t,['pre','post']);vec(t['pre'],2);vec(t['post'],2)
  if sum(t['pre'])!=sum(t['post']):raise ValueError('each transition must conserve total tokens')
 cs=p['counts']
 if type(cs)is not list or len(cs)!=len(ts)or any(not 0<=integer(c)<=3 for c in cs)or sum(cs)>8:raise ValueError('counts 0..3, total at most 8')
 return n,ts

def loads(text):
 def pairs(ps):
  out={}
  for k,v in ps:
   if k in out:raise ValueError('duplicate key')
   out[k]=v
  return out
 def no(_):raise ValueError('JSON decimals/constants forbidden')
 return json.loads(text,object_pairs_hook=pairs,parse_float=no,parse_constant=no)
