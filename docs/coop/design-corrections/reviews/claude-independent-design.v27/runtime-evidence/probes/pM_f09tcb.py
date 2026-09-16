"""PROBE M (v27) — two independent checks:
  (a) F-09: is EXECUTION_INPUTS_COVERAGE_DERIVE really raised by the clause the remint prose
      now cites (§5 derived Native Coverage accounts) rather than §3?
  (b) F-13: do EXACTLY the 13 declared rows depend on the TCB-scope move? I classify all 30
      rows myself from their own rationale text and compare against the declared list.
"""
import json, os, re

SRC = '/tmp/opensip-design-corrections/candidate-subject.v27'
F = os.path.join(SRC, 'docs/coop/design-corrections')
PKG = '/tmp/opensip-design-corrections/claude-author-package-successor.v4'
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v27/receipts'
R = {}

# ---------- (a) F-09 ----------
m = os.path.join(F, 'foundation/execution_inputs_model.v1.py')
if not os.path.isfile(m):
    cands = [os.path.join(dp, n) for dp, dn, fn in os.walk(F) for n in fn
             if n.startswith('execution_inputs_model')]
    m = cands[0] if cands else None
print('execution inputs model:', os.path.relpath(m, SRC) if m else 'NOT FOUND')
lines = open(m, encoding='utf-8').read().splitlines()
raises = [i for i, l in enumerate(lines, 1) if 'EXECUTION_INPUTS_COVERAGE_DERIVE' in l]
R['coverageDeriveLines'] = raises
print('EXECUTION_INPUTS_COVERAGE_DERIVE at lines', raises)
for i in raises:
    # nearest preceding section marker or def
    sec = None
    for j in range(i - 1, 0, -1):
        if re.search(r'^\s*(def |class )', lines[j - 1]) and sec is None:
            sec = (j, lines[j - 1].strip())
            break
    print('\n  line %d: %s' % (i, lines[i - 1].strip()[:150]))
    print('     enclosing: %s' % (sec,))
    ctx = [l for l in lines[max(0, i - 26):i] if re.search(r'§|section', l, re.I)]
    print('     nearby section refs:', [c.strip()[:130] for c in ctx][:4])
    R.setdefault('raiseContext', []).append(
        {'line': i, 'text': lines[i - 1].strip(), 'enclosing': sec,
         'nearbySectionRefs': [c.strip() for c in ctx][:4]})

# the contract doc headings
doc = None
for cand in ('docs/coop/design-corrections/foundation/execution-inputs-contract.v1.md',
             'docs/coop/design-corrections/foundation/execution-inputs.v1.md'):
    p = os.path.join(SRC, cand)
    if os.path.isfile(p):
        doc = p
if doc is None:
    for dp, dn, fn in os.walk(F):
        if '/reviews/' in dp:
            continue
        for n in fn:
            if 'execution-inputs' in n and n.endswith('.md'):
                doc = os.path.join(dp, n)
print('\nexecution-inputs contract:', os.path.relpath(doc, SRC) if doc else 'NOT FOUND')
if doc:
    dl = open(doc, encoding='utf-8').read().splitlines()
    heads = [(i, l.strip()) for i, l in enumerate(dl, 1) if re.match(r'^#{1,3} ', l)]
    R['contractHeadings'] = [{'line': i, 'text': t} for i, t in heads]
    for i, t in heads:
        print('  %5d  %s' % (i, t[:120]))
    R['contractPath'] = os.path.relpath(doc, SRC)

# ---------- (b) F-13 independent classification ----------
era = json.load(open(os.path.join(PKG, 'evaluation-residual-author-assessment.json')))
declared = era['sharedReviewDependencies'][0]['dependentResidualIds']
items = era['items']
R['declaredTcbDependents'] = declared
print('\n\ndeclared TCB-SCOPE-01 dependents (%d): %s' % (len(declared), declared))

PAT = re.compile(r'same[- ]process|in[- ]process|outside (the )?(product )?(threat model|TCB)|'
                 r'trust(ed)?[- ]comput|TCB|hostile code|adversarial code|excluded.{0,40}route|'
                 r'selected (authenticated )?code|authenticated code', re.I)
mine, rows = [], []
for it in items:
    txt = json.dumps(it)
    hits = sorted(set(x.group(0) for x in PAT.finditer(txt)))
    dep = bool(hits)
    if dep:
        mine.append(it['id'])
    rows.append({'id': it['id'], 'myTcbDependent': dep, 'signals': hits[:6],
                 'declared': it['id'] in declared})
R['myTcbDependents'] = mine
R['perRow'] = rows
print('\nmy independent classification (%d): %s' % (len(mine), mine))
onlyMine = [x for x in mine if x not in declared]
onlyDeclared = [x for x in declared if x not in mine]
R['dependentOnlyByMyReading'] = onlyMine
R['declaredButNotFlaggedByMe'] = onlyDeclared
R['exactAgreement'] = not onlyMine and not onlyDeclared
print('flagged by me but NOT declared :', onlyMine)
print('declared but NOT flagged by me :', onlyDeclared)
print('exact agreement on the 13      :', R['exactAgreement'])
print('\nrows I flag beyond the declared set, with their signals:')
for r in rows:
    if r['myTcbDependent'] and not r['declared']:
        print('  %-16s %s' % (r['id'], r['signals']))

json.dump(R, open(os.path.join(OUT, 'pM-f09tcb.json'), 'w'), indent=1, default=str)
print('\nwrote pM-f09tcb.json')
