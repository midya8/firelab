import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'tests'))
from firelab.engine import analyze
from firelab.controls import controls
from test_core import generated
cases=[{'name':c['title'],'input':c['input'],'report':analyze(c['input'])}for c in controls()]
cases.extend({'name':'seed-'+str(i),'input':p,'report':analyze(p)}for i,p in enumerate(generated(number=100)))
Path(sys.argv[1]).write_text(json.dumps(cases,separators=(',',':')))
