"""P16: does the frozen owner implement the §5 'missing expected subjects -> incomplete' rule
that the consumer applied to its clones-fact cells?"""
import importlib.util, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT32 = '/tmp/opensip-design-corrections/candidate-subject.v32'
FOUND = os.path.join(ROOT32, 'docs/coop/design-corrections/foundation')
MODEL = os.path.join(FOUND, 'execution_inputs_model.v1.py')
CONTRACT = os.path.join(FOUND, 'execution-inputs-contract.v1.md')

out = {}
src = open(MODEL).read()
lines = src.split('\n')

print('=== owner references to an expected-subject census')
pat = re.compile(r'(censusMissing|expected.?subject|expectedSubjects|subject.?census)', re.I)
hits = []
for m in pat.finditer(src):
    ln = src[:m.start()].count('\n') + 1
    hits.append({'line': ln, 'text': lines[ln - 1].strip()[:200]})
for h in hits:
    print('  %d  %s' % (h['line'], h['text']))
out['ownerCensusReferences'] = hits

# what feeds censusMissing?
print('\n=== censusMissing assignments in the owner')
for m in re.finditer(r'censusMissing', src):
    ln = src[:m.start()].count('\n') + 1
    lo = max(0, ln - 8)
    print('  --- line %d' % ln)
    for i in range(lo, min(len(lines), ln + 4)):
        print('    %d %s' % (i + 1, lines[i][:170]))
    break

M = importlib.util.module_from_spec(importlib.util.spec_from_file_location('owner', MODEL))
importlib.util.spec_from_file_location('owner', MODEL).loader.exec_module(M)
print('\n=== does derive_summary take an expected-subject argument?')
import inspect
for fn in ('derive_summary', 'derive_account_summary', 'summarize_account'):
    f = getattr(M, fn, None)
    if f:
        print('  %s%s' % (fn, inspect.signature(f)))
        out['summaryFnSignature'] = '%s%s' % (fn, inspect.signature(f))

print('\n=== contract section 5 sentences on expected subjects')
ct = open(CONTRACT, encoding='utf-8', errors='ignore').read()
sent = []
for m in re.finditer(r'[^.|]*expected (source )?subject[^.|]*\.', ct, re.I):
    s = ' '.join(m.group(0).split())
    sent.append(s)
    print('   *', s[:400])
out['contractExpectedSubjectSentences'] = sent

print('\n=== contract sentence exempting this unit from the census')
for m in re.finditer(r'[^.|]*does not invent that census[^.|]*\.', ct, re.I):
    s = ' '.join(m.group(0).split())
    print('   *', s[:400])
    out['contractCensusExemption'] = s

# consumer's own stated rationale
HC = '/tmp/opensip-design-corrections/consumer-b.v19/output/helper-corrections.json'
hc = json.load(open(HC))
found = []
txt = json.dumps(hc)
for m in re.finditer(r'MISSING_EXPECTED_SOURCE_SUBJECTS[A-Z_]*', txt):
    found.append(m.group(0))
print('\n=== consumer cites the clause token:', sorted(set(found)))
out['consumerCitedClause'] = sorted(set(found))

json.dump(out, open(os.path.join(HERE, 'p16-census.json'), 'w'), indent=2, default=str)
print('\nWROTE p16-census.json')
