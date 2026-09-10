"""Which case expectations in the FROZEN corpus depend on each branch of the guard.
- explicitNullRefusal: `"refusal": null` deliberately expects a DETAIL-FREE refusal. The guard must
  keep these PASSING (key present, None == None).
- noRefusalKey: expects success. Under the old code a detail-free refusal here passed silently;
  under the guard it must FAIL. These are the cases the fix protects.
Limit: reads declared expectations; it does not by itself execute them."""
import json, pathlib, sys
CASES = json.loads(pathlib.Path(
 '/tmp/opensip-design-corrections/candidate-subject.v17/docs/coop/design-corrections/workflows/workflow-cases.v1.json'
).read_text())
KEYS = ('refusal', 'recoverRefusal')
out = {'explicitNull': [], 'keyPresentWithValue': 0, 'noRefusalKey': 0, 'groups': {}}

def visit(group, cases):
    g = {'explicitNull': [], 'withValue': 0, 'absent': 0}
    for c in cases:
        if not isinstance(c, dict):
            continue
        exp = c.get('expect', {})
        for k in KEYS:
            if k in exp:
                if exp[k] is None:
                    g['explicitNull'].append({'id': c.get('id'), 'key': k})
                    out['explicitNull'].append({'group': group, 'id': c.get('id'), 'key': k})
                else:
                    g['withValue'] += 1; out['keyPresentWithValue'] += 1
        if not any(k in exp for k in KEYS):
            g['absent'] += 1; out['noRefusalKey'] += 1
        # recoverRefusal may sit outside 'expect' in some shapes
    out['groups'][group] = g

for key, val in CASES.items():
    if isinstance(val, list):
        visit(key, val)
    elif isinstance(val, dict) and isinstance(val.get('cases'), list):
        visit(key, val['cases'])
print(json.dumps({'standing': __doc__, **out}, indent=1))
