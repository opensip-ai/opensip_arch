"""PROBE E — read the frozen proposed disposition maps and measure their populations,
so my disposition MAPS are assessed against actual owning contract sections rather
than generic carry-forward."""
import json, os, re

ROOT = '/tmp/opensip-design-corrections/candidate-subject.v26'
DC = os.path.join(ROOT, 'docs/coop/design-corrections')
R = {}

cx = json.load(open(os.path.join(DC, 'correction-crosswalk.proposed.json'), encoding='utf-8'))
R['crosswalk_standing'] = cx['standing']
R['crosswalk_source'] = cx['source']
rows = {}
for it in cx['items']:
    rows[it['id']] = {k: it.get(k) for k in
                      ('unit', 'contract', 'selector', 'obligation', 'status',
                       'successorCorrection21', 'currentReviewBinding', 'ownerRows')}
R['AR'] = rows

ev = json.load(open(os.path.join(DC, 'evaluation-residual-dispositions.proposed.json'), encoding='utf-8'))
R['evaluation_residuals_standing'] = str(ev['standing'])[:600]
R['evaluation_residuals_count'] = len(ev['items'])
R['evaluation_residual_ids'] = [i.get('id') for i in ev['items']]
R['evaluation_residual_row_keys'] = sorted(ev['items'][0].keys())

qg = json.load(open(os.path.join(DC, 'qualification-gates.proposed.json'), encoding='utf-8'))
R['gates_standing'] = str(qg['standing'])[:600]
R['gates_count'] = len(qg['items'])
R['gate_ids'] = [i.get('id') for i in qg['items']]
R['gate_row_keys'] = sorted(qg['items'][0].keys())
R['gate_status_values'] = sorted({str(i.get('status')) for i in qg['items']})
R['platformFamilies'] = qg.get('platformFamilies')

# FW rows from the current source map
csm = open(os.path.join(DC, 'current-source-map.proposed.md'), encoding='utf-8').read()
fw = re.findall(r'^\| (FW-\d\d) ([^|]*)\| (.*?) \|$', csm, re.M)
R['FW'] = {a: {'title': b.strip(), 'currentContract': c.strip()} for a, b, c in fw}
R['FW_count'] = len(R['FW'])

# DR residual rows
inh = open(os.path.join(DC, 'inherited-residuals.proposed.md'), encoding='utf-8').read()
r16 = re.findall(r'^\| (DR-011-R\d\d) ([^|]*)\| (.*?) \|$', inh, re.M)
R['DR_011_R'] = {a: {'title': b.strip(), 'disposition': c.strip()} for a, b, c in r16}
R['DR_011_R_count'] = len(R['DR_011_R'])
parents = re.findall(r'^\| (DR-0\d\d) \| (.*?) \|$', inh, re.M)
R['DR_parents'] = {a: b.strip() for a, b in parents}
R['DR_parents_count'] = len(R['DR_parents'])

reg = open(os.path.join(ROOT, 'docs/v2/architecture/08-decision-and-readiness-register.md'), encoding='utf-8').read()
five = re.findall(r'^\| (DR-20[1-5]) \| ([^|]*)\| ([^|]*)\| ([^|]*)\|', reg, re.M)
R['DR_201_205'] = {a: {'review': b.strip(), 'finding': c.strip()[:240], 'owner': d.strip()[:160]}
                   for a, b, c, d in five}
R['DR_201_205_count'] = len(R['DR_201_205'])

print(json.dumps({k: v for k, v in R.items() if not isinstance(v, dict) or len(json.dumps(v)) < 2600},
                 indent=1)[:5200])
json.dump(R, open('/tmp/opensip-design-corrections/claude-independent-design.v26/receipts/probeE.json', 'w'), indent=1)
print('\nwrote probeE.json')
