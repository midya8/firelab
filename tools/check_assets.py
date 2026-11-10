import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from firelab.controls import controls
assert json.loads((ROOT/'docs/controls.json').read_text())==controls()
for fn,i in [('borrow.json',0),('helpers.json',1)]:assert json.loads((ROOT/'examples'/fn).read_text())==controls()[i]['input']
print('14 control assets and 2 examples match native source')
