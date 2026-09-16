"""P5: all accounts across the five runs, plus the outcome/carrier fault sites."""
import base64, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT32 = '/tmp/opensip-design-corrections/candidate-subject.v32'
RB = '/tmp/opensip-design-corrections/root-blind19-final-source32.v1'
MODEL = os.path.join(ROOT32, 'docs/coop/design-corrections/foundation/execution_inputs_model.v1.py')

src = open(MODEL).read().split('\n')
print('=== owner lines 1400-1440 (OUTCOME_DERIVE / CAUSE_CARRIER sites)')
for i in range(1399, 1440):
    print(i + 1, src[i][:180])

print('\n=== derive_outcome partial/complete branches')
import re
txt = open(MODEL).read()
m = re.search(r'^def derive_outcome', txt, re.M)
ln = txt[:m.start()].count('\n') + 1
for i in range(ln + 35, ln + 90):
    if i - 1 < len(src):
        print(i, src[i - 1][:180])


def blobs_of(export):
    out = {}
    for d, b in export['blobs'].items():
        try:
            out[d] = base64.b64decode(b) if isinstance(b, str) else bytes(b)
        except Exception:
            pass
    return out


def jload(raw):
    try:
        return json.loads(raw)
    except Exception:
        return None


rows = []
print('\n=== every nativeCoverageAccount across the five runs')
for name in ('syntax-code', 'typescript', 'rust', 'rust-partial', 'syntax-data'):
    ex = json.load(open(os.path.join(RB, name, 'exact-export.json')))
    bl = blobs_of(ex)
    ei = None
    for d, raw in bl.items():
        doc = jload(raw)
        if isinstance(doc, dict) and 'nativeCoverageAccounts' in doc and 'cellOutcomes' in doc:
            ei = doc
    print('---', name)
    for a in ei['nativeCoverageAccounts']:
        rows.append({'run': name, **a})
        print('   c%s/p%s %-16s@%-22s app=%-24s srcU=%-9s tgtU=%-9s cov=%d' % (
            a['cellOrdinal'], a['programOrdinal'], a['relation'], a['resolution'],
            a['applicability'],
            (str(a['sourceUniverse'])[:8] if a['sourceUniverse'] else 'null'),
            (str(a['targetUniverse'])[:8] if a['targetUniverse'] else 'null'),
            len(a['coverageIds'])))

# What is the consumer's own rule? Tabulate applicability -> (sourceUniverse null?)
rule = {}
for r in rows:
    rule.setdefault(r['applicability'], set()).add(r['sourceUniverse'] is None)
print('\n=== consumer rule: applicability -> {sourceUniverse is null}')
for k, v in sorted(rule.items()):
    print('   %-26s -> %s' % (k, sorted(v)))

json.dump({'accounts': rows,
           'consumerRuleApplicabilityToNullUniverse': {k: sorted(v) for k, v in rule.items()}},
          open(os.path.join(HERE, 'p5-outcomes.json'), 'w'), indent=2)
print('\nWROTE p5-outcomes.json')
