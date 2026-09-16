"""Read-only reproduction against frozen report08; no parent bytes are changed."""
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
pins = json.loads((HERE/'input-pins.json').read_text())['files']
for row in pins:
    raw = Path(row['path']).read_bytes()
    assert len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256']
root = Path(pins[0]['path']).parent
model = {'__name__':'report08_fit_audit'}
exec(compile((root/'report_model.py').read_bytes(),str(root/'report_model.py'),'exec'),model)
fixtures = json.loads((root/'fixtures.json').read_text())
inventory = json.loads((root/'owner/command-inventory.v5.json').read_text())
command = next(row for row in inventory['commands'] if row['name']=='fit')
rows = []
for golden in fixtures['interruptionGoldens']['scenarios']:
    if golden['command'] != 'fit': continue
    try:
        raw = model['static_parity_text'](golden['envelope'],command,model['document_disclosures']({})).encode()
        observed = {'state':'rendered','bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
    except KeyError as exc:
        observed = {'state':'KeyError','missingMember':exc.args[0]}
    rows.append({'id':golden['id'],'kind':golden['envelope']['kind'],
                 'termination':golden['envelope']['termination'],
                 'queryOutcome':[r['outcome'] for s,r in zip(golden['invocationRecord']['orderedSteps'],golden['invocationRecord']['stepResults']) if s['kind']=='query'],
                 'declaredFormats':golden['formats'],'declaredStatus':golden['status'],
                 'observedStaticParity':observed})
assert len(rows)==3
bad = next(r for r in rows if r['kind']=='run')
assert bad['queryOutcome']==['completed'] and bad['observedStaticParity']=={'state':'KeyError','missingMember':'advisoryReport'}
print(json.dumps({'standing':'Confirmed root counterexample, not a fix or full host/browser test','finding':'Q-FIT-1-STATIC-PARITY','rows':rows,'inputPins':len(pins)},indent=2))
