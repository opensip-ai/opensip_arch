"""Independent verification of the governance records that carry the AR/FW,
inherited-residual and DR-201..205 dispositions: historical preservation
(DR-204), qualification gates and NEW-ADV-3 (DR-202), evaluation residual
coverage (DR-011-R12), inherited row sources, and the AR/FW row inventories."""
import json, hashlib, re, sys
from pathlib import Path

ROOT = Path('/tmp/opensip-design-corrections/candidate-subject.v7')
DC = ROOT / 'docs/coop/design-corrections'
R = {}

def sha(p):
    p = ROOT / p if not str(p).startswith('/') else Path(p)
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None

# ---------------------------------------------------------- DR-204 historical preservation
hp = json.loads((DC / 'historical-preservation-report.v7.json').read_text())
R['historicalReportKeys'] = list(hp.keys())
rows = None
for k, v in hp.items():
    if isinstance(v, list) and v and isinstance(v[0], dict) and 'sha256' in v[0]:
        rows = v; R['historicalRowsKey'] = k
verified = changed = absent = 0
bad = []
for e in (rows or []):
    p = e.get('path')
    got = sha(p)
    if got is None: absent += 1; bad.append((p, 'ABSENT'))
    elif got == e['sha256']: verified += 1
    else: changed += 1; bad.append((p, 'CHANGED'))
R['historicalFilesDeclared'] = len(rows or [])
R['historicalFilesVerifiedUnchanged'] = verified
R['historicalFilesChanged'] = changed
R['historicalFilesAbsent'] = absent
R['historicalProblems'] = bad
# and the same set must be byte-identical to the v6 subject's copies
V6 = Path('/tmp/opensip-design-corrections/candidate-subject.v6')
if V6.is_dir():
    same = sum(1 for e in (rows or [])
               if (V6 / e['path']).is_file()
               and hashlib.sha256((V6 / e['path']).read_bytes()).hexdigest() == e['sha256'])
    R['historicalAlsoIdenticalInV6Snapshot'] = same
    R['historicalV6SnapshotPresent'] = True
else:
    R['historicalV6SnapshotPresent'] = False

# ---------------------------------------------------------- DR-202 / NEW-ADV-3 qualification gates
qg = json.loads((DC / 'qualification-gates.proposed.json').read_text())
R['qgTopKeys'] = list(qg.keys())
gates = None
for k, v in qg.items():
    if isinstance(v, list) and v and isinstance(v[0], dict) and ('gate' in v[0] or 'id' in v[0]):
        gates = v; R['qgGatesKey'] = k
R['gateCount'] = len(gates or [])
def truthy(g, *names):
    return [g.get(n) for n in names if n in g]
R['gatesQualifiedTrue'] = [g.get('id') or g.get('gate') for g in (gates or []) if g.get('qualified')]
R['gatesDemonstratedTrue'] = [g.get('id') or g.get('gate') for g in (gates or [])
                              if g.get('demonstrated')]
R['gateStatuses'] = sorted({str(g.get('status')) for g in (gates or [])})
R['gateFieldUnion'] = sorted({k for g in (gates or []) for k in g})
fams = set()
for g in (gates or []):
    for k in ('platformFamilies', 'platformFamily', 'machineIds'):
        v = g.get(k)
        if isinstance(v, list): fams |= set(v)
        elif isinstance(v, str): fams.add(v)
blob = json.dumps(qg)
for m in re.findall(r'"(macos|linux)[-a-z0-9]*"', blob): fams.add(m)
R['platformFamiliesSeen'] = sorted(fams)
R['allGatesUnqualifiedAndUndemonstrated'] = (not R['gatesQualifiedTrue']
                                             and not R['gatesDemonstratedTrue'])

# ---------------------------------------------------------- evaluation residuals (DR-011-R12)
er = json.loads((DC / 'evaluation-residual-dispositions.proposed.json').read_text())
R['evalResidualTopKeys'] = list(er.keys())
lists = {k: len(v) for k, v in er.items() if isinstance(v, list)}
R['evalResidualListSizes'] = lists
ids = re.findall(r'"(RES-[0-9A-Za-z\-]+)"', json.dumps(er))
nb = re.findall(r'"(NB-[0-9A-Za-z\-]+)"', json.dumps(er))
esc = re.findall(r'"(ESC[A-Za-z0-9\-]*|escape-[0-9]+)"', json.dumps(er))
R['distinctRES'] = len(set(ids)); R['distinctNB'] = len(set(nb))
R['sampleRES'] = sorted(set(ids))[:25]; R['sampleNB'] = sorted(set(nb))
def dispositions(o, acc):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in ('disposition', 'proposedDisposition', 'status') and isinstance(v, str):
                acc[v] = acc.get(v, 0) + 1
            dispositions(v, acc)
    elif isinstance(o, list):
        for v in o: dispositions(v, acc)
    return acc
R['evalResidualDispositionCounts'] = dispositions(er, {})
R['everyEvalResidualHasADisposition'] = all(
    any(k in item for k in ('disposition', 'proposedDisposition', 'status'))
    for v in er.values() if isinstance(v, list) for item in v if isinstance(item, dict))

# ---------------------------------------------------------- inherited row sources
irs = json.loads((DC / 'inherited-row-sources.proposed.json').read_text())
R['inheritedRowSourcesTopKeys'] = list(irs.keys())
def collect_paths(o, acc):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in ('path', 'source', 'selector') and isinstance(v, str) and v.startswith('docs/'):
                acc.add(v.split('#')[0])
            collect_paths(v, acc)
    elif isinstance(o, list):
        for v in o: collect_paths(v, acc)
    return acc
paths = collect_paths(irs, set())
missing = sorted(p for p in paths if not (ROOT / p).exists())
R['inheritedRowSourcePathsCited'] = len(paths)
R['inheritedRowSourcePathsMissingFromSubject'] = missing

# ---------------------------------------------------------- AR and FW row inventories
cw = json.loads((DC / 'correction-crosswalk.proposed.json').read_text())
R['arRowIds'] = [i['id'] for i in cw['items']]
R['arRowCount'] = len(cw['items'])
sm = (DC / 'current-source-map.proposed.md').read_text()
fw = re.findall(r'\|\s*(FW-\d+)\s', sm)
R['fwRowIds'] = sorted(set(fw), key=lambda x: int(x.split('-')[1]))
R['fwRowCount'] = len(set(fw))
res = re.findall(r'\|\s*(DR-011-R\d+)\s', (DC / 'inherited-residuals.proposed.md').read_text())
R['inheritedResidualIds'] = sorted(set(res), key=lambda x: int(x.split('R')[-1]))
R['inheritedResidualCount'] = len(set(res))
parent = re.findall(r'\|\s*(DR-0\d\d)\s', (DC / 'inherited-residuals.proposed.md').read_text())
R['inheritedParentRows'] = sorted(set(parent))

print(json.dumps(R, indent=1, default=str))
json.dump(R, open(sys.argv[1], 'w'), indent=1, default=str)
