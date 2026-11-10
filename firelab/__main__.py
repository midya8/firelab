import argparse,json,sys
from pathlib import Path
from .model import loads

def main():
 p=argparse.ArgumentParser(description='Conservative weighted Petri-net execution evidence');p.add_argument('command',choices=['run','verify','demo']);p.add_argument('file',nargs='?');a=p.parse_args()
 try:
  if a.command=='demo':
   from .controls import controls
   data=controls()[0]['input']
  else:
   if not a.file:raise ValueError('input file required')
   raw=Path(a.file).read_bytes()
   if len(raw)>(8*1024*1024 if a.command=='verify'else 65536):raise ValueError('input size limit')
   data=loads(raw.decode())
  if a.command=='verify':
   from .certificate import verify
   out=verify(data)
   if not out['valid']:raise ValueError(out['error'])
  else:
   from .engine import analyze
   out=analyze(data)
  print(json.dumps(out,sort_keys=True,separators=(',',':'),allow_nan=False))
 except(ValueError,OSError,UnicodeError,RecursionError)as e:print(str(e),file=sys.stderr);return 2
 return 0
if __name__=='__main__':sys.exit(main())
