from pathlib import Path
import sys,json
sys.path.insert(0,'/tmp/opensip-implementation/measurement-jsonschema-4.25.1')
from jsonschema import Draft202012Validator
from referencing import Registry,Resource
from referencing.jsonschema import DRAFT202012
W=Path('/Users/sb/code/opensip-ai/opensip-host-current-corpus');f=json.loads((W/'crates/host/tests/fixtures/replay-fixtures.current.json').read_bytes());docs=[json.loads(p.read_bytes())for p in (W/'schemas/sources').glob('*.json')];registry=Registry().with_resources((d['$id'],Resource(contents=d,specification=DRAFT202012))for d in docs if '$id'in d);identity=json.loads((W/'schemas/sources/identity-v3.schema.json').read_bytes());bad=[]
for key,row in f['objectPool'].items():
 validator=Draft202012Validator({'$ref':identity['$id']+'#/$defs/'+row['domain']},registry=registry);errors=list(validator.iter_errors(row['descriptor']))
 if errors:bad.append({'poolKey':key,'id':row['id'],'domain':row['domain'],'cases':[c['label']for c in f['cases']if key in c['objects']],'errors':[{'path':list(e.path),'message':e.message}for e in errors[:4]]})
print(json.dumps({'badObjects':len(bad),'details':bad[:6]},indent=2));Path(__file__).with_name('replay-shape-diagnosis.json').write_text(json.dumps(bad,indent=2)+'\n')
