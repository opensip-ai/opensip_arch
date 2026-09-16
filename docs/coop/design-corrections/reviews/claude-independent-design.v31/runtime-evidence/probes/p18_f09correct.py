"""PROBE 18 (v31) — RR27-01: correct my v27 F-09 evidence claim.

v27 said EXECUTION_INPUTS_COVERAGE_DERIVE is raised ONLY inside load_coverage and
partitions_in_cell. That came from a probe that walked backwards to the nearest `def` line, which
cannot tell a nested body from code that merely follows a function. Here I decide enclosure by
INDENTATION and block extent, which is the right test, and report where each raise actually sits.
The §5 conclusion is re-checked independently of the function question.
"""
import json, os, re

SRC = '/tmp/opensip-design-corrections/candidate-subject.v31'
F = os.path.join(SRC, 'docs/coop/design-corrections/foundation')
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v31/receipts'
R = {'corrects': 'v27 F-09 function-exclusivity claim'}

p = os.path.join(F, 'execution_inputs_model.v1.py')
lines = open(p, encoding='utf-8').read().splitlines()
R['fileUnchangedSince27'] = 'docs/coop/design-corrections/foundation/execution_inputs_model.v1.py' \
    not in [c['path'] for c in json.load(open(os.path.join(OUT, 'p01-delta.json')))['cumulative']['changed']]

# every top-level def with its block extent
defs = []
for i, l in enumerate(lines, 1):
    m = re.match(r'^(\s*)def (\w+)\s*\(', l)
    if m:
        defs.append({'line': i, 'name': m.group(2), 'indent': len(m.group(1))})
for d in defs:
    end = len(lines)
    for j in range(d['line'], len(lines)):
        l = lines[j]
        if l.strip() and (len(l) - len(l.lstrip())) <= d['indent'] and not l.lstrip().startswith('#'):
            end = j
            break
    d['endLine'] = end

TOK = 'EXECUTION_INPUTS_COVERAGE_DERIVE'
raises = [i for i, l in enumerate(lines, 1) if TOK in l]
R['tokenLines'] = raises
rows = []
for i in raises:
    encl = [d for d in defs if d['line'] < i <= d['endLine']]
    innermost = max(encl, key=lambda d: d['indent']) if encl else None
    txt = lines[i - 1]
    rows.append({'line': i, 'text': txt.strip()[:120],
                 'indent': len(txt) - len(txt.lstrip()),
                 'enclosingFunctions': [d['name'] for d in encl],
                 'innermostFunction': innermost['name'] if innermost else '<module level>'})
R['raiseSites'] = rows
print('%-6s %-6s %-34s %s' % ('line', 'indent', 'innermost function', 'text'))
for x in rows:
    print('%-6d %-6d %-34s %s' % (x['line'], x['indent'], x['innermostFunction'], x['text'][:70]))

fns = sorted({x['innermostFunction'] for x in rows if x['line'] != raises[0]})
R['distinctEnclosingFunctions'] = fns
R['v27ClaimWasOnlyTwoFunctions'] = ['load_coverage', 'partitions_in_cell']
R['v27ClaimIsCorrect'] = set(fns) <= {'load_coverage', 'partitions_in_cell'}
print('\ndistinct enclosing functions for the raise sites:', fns)
print('v27 "only load_coverage / partitions_in_cell" claim holds:', R['v27ClaimIsCorrect'])

# where does the coverage-account loop live?
for x in rows:
    if x['innermostFunction'] not in ('load_coverage', 'partitions_in_cell'):
        lo = max(0, x['line'] - 14)
        print('\n--- context for line %d (innermost: %s) ---' % (x['line'], x['innermostFunction']))
        for j in range(lo, min(len(lines), x['line'] + 2)):
            print('%5d  %s' % (j + 1, lines[j][:130]))
        break

# the section-5 conclusion, re-checked on its own terms
doc = os.path.join(F, 'execution-inputs-contract.v1.md')
dl = open(doc, encoding='utf-8').read().splitlines()
heads = [(i, l.strip()) for i, l in enumerate(dl, 1) if re.match(r'^#{1,3} ', l)]
R['contractHeadings'] = [{'line': i, 'text': t} for i, t in heads]
sec5 = next((t for i, t in heads if re.match(r'^## 5', t)), None)
sec3 = next((t for i, t in heads if re.match(r'^## 3', t)), None)
R['section5'] = sec5
R['section3'] = sec3
print('\ncontract §3 =', sec3)
print('contract §5 =', sec5)
R['section5IsCoverageAccounts'] = bool(sec5 and 'Coverage account' in sec5)
R['sectionConclusionStands'] = R['section5IsCoverageAccounts']
print('§5 is the derived Native Coverage accounts clause, so the v27 §5 conclusion stands:',
      R['sectionConclusionStands'])

json.dump(R, open(os.path.join(OUT, 'p18-f09correct.json'), 'w'), indent=1, default=str)
print('\nwrote p18-f09correct.json')
