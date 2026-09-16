"""PROBE 05 (v31) — source28 item: the ruleResults order correction.

Root says ordered() omitted the explicit ruleIdUTF8 ordering and fell through to generic
canonical-member order, contradicting identity-schemas.v3 and composition 9.3. I do not restate
that. I enumerate EVERY x-opensip-order annotation in identity-schemas.v3 and check whether the
reference ordered() implements each one, so I can say whether ruleResults was the only gap or
whether others remain.
"""
import json, os, re

SRC = '/tmp/opensip-design-corrections/candidate-subject.v31'
F = os.path.join(SRC, 'docs/coop/design-corrections/foundation')
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v31/receipts'
R = {}

sch = json.load(open(os.path.join(F, 'identity-schemas.v3.json')))

# ---- every x-opensip-order annotation, with the property name that carries it ----
ann = {}
def walk(o, prop=None):
    if isinstance(o, dict):
        if 'x-opensip-order' in o and prop:
            ann.setdefault(prop, set()).add(json.dumps(o['x-opensip-order'], sort_keys=True))
        for k, v in o.items():
            walk(v, k if k not in ('properties', '$defs', 'items', 'allOf', 'anyOf', 'oneOf',
                                   'then', 'else', 'if') else prop)
    elif isinstance(o, list):
        for v in o:
            walk(v, prop)
walk(sch)
R['annotatedArrayProperties'] = {k: sorted(v) for k, v in sorted(ann.items())}
byorder = {k: sorted(v) for k, v in ann.items() if any('"by"' in x for x in v)}
setorder = {k: sorted(v) for k, v in ann.items() if not any('"by"' in x for x in v)}
R['explicitByOrders'] = byorder
R['nonByOrders'] = {k: v for k, v in sorted(setorder.items())}
print('properties carrying x-opensip-order : %d' % len(ann))
print('\n--- explicit "by" key orders (%d) ---' % len(byorder))
for k, v in sorted(byorder.items()):
    print('   %-26s %s' % (k, v))
print('\n--- non-"by" orders (%d) ---' % len(setorder))
kinds = {}
for k, v in setorder.items():
    for x in v:
        kinds.setdefault(x, []).append(k)
for x, props in sorted(kinds.items()):
    print('   %-22s %d props: %s' % (x, len(props), sorted(props)[:8]))
R['nonByOrderKinds'] = {x: sorted(p) for x, p in kinds.items()}

# ---- what ordered() actually branches on ----
src = open(os.path.join(F, 'identity-model.v3.py'), encoding='utf-8').read()
m = re.search(r"def ordered\(value,path=\(\)\):(.*?)\nROOT_ORDER_PATH", src, re.S)
body = m.group(1)
R['orderedBody'] = body
names = set()
for mm in re.finditer(r"name==?'([A-Za-z0-9_-]+)'", body):
    names.add(mm.group(1))
for mm in re.finditer(r"name in \[([^\]]+)\]", body):
    for q in re.findall(r"'([^']+)'", mm.group(1)):
        names.add(q)
R['orderedNamedBranches'] = sorted(names)
print('\nordered() named branches (%d): %s' % (len(names), sorted(names)))
R['orderedHasGenericFallback'] = 'else:keys=[C.canonical(v) for v in value]' in body.replace(' ', '')
print('generic canonical fallback present:', R['orderedHasGenericFallback'])

# ---- the gap analysis ----
missing = sorted(k for k in byorder if k not in names)
covered = sorted(k for k in byorder if k in names)
R['explicitByOrdersImplemented'] = covered
R['explicitByOrdersFallingToGenericOrder'] = missing
print('\nexplicit "by" orders IMPLEMENTED by a named branch : %s' % covered)
print('explicit "by" orders left to generic canonical order: %s' % missing)
R['ruleResultsNowImplemented'] = 'ruleResults' in names
R['ruleResultsDeclaredBy'] = byorder.get('ruleResults')
print('\nruleResults implemented:', R['ruleResultsNowImplemented'], R['ruleResultsDeclaredBy'])

# ---- composition 9.3 ----
comp = None
for cand in ('evaluator-composition-contract.v3.md',):
    p = os.path.join(F, cand)
    if os.path.isfile(p):
        comp = p
if comp:
    lines = open(comp, encoding='utf-8').read().splitlines()
    hits = [(i, l) for i, l in enumerate(lines, 1) if 'ruleResults' in l or re.match(r'^#+ *9\.3', l)]
    R['compositionHits'] = [{'line': i, 'text': l.strip()[:260]} for i, l in hits]
    print('\n--- composition contract lines naming ruleResults / 9.3 ---')
    for i, l in hits:
        print('%5d  %s' % (i, l.strip()[:230]))

json.dump(R, open(os.path.join(OUT, 'p05-orderlaw.json'), 'w'), indent=1, default=str)
print('\nwrote p05-orderlaw.json')
