import os, hashlib, json, sys

ROOT = '/tmp/opensip-design-corrections/candidate-subject.v26'
NAMES = [
    'foundation/enumeration-contract.v1.md',
    'foundation/atom-evaluation-contract.v1.md',
    'foundation/execution-inputs-contract.v1.md',
    'foundation/evaluator-composition-contract.v3.md',
    'foundation/evaluator-fault-contract.v3.md',
    'workflows/query-projection-contract.v3.md',
    'workflows/workflow-projection-contract.v3.md',
    'foundation/target-attribution.schema.v2.json',
    'native/fact-batch.schema.v3.json',
    'native/occupancy-companion.schema.v1.json',
    'native/dispatch-binding.schema.v1.json',
]
base = os.path.join(ROOT, 'docs/coop/design-corrections')
for n in NAMES:
    p = os.path.join(base, n)
    if os.path.isfile(p):
        b = open(p, 'rb').read()
        txt = b.decode('utf-8', 'replace')
        print('%-52s bytes=%-8d lines=%-5d %s' % (n, len(b), txt.count('\n') + 1, hashlib.sha256(b).hexdigest()))
    else:
        print('%-52s MISSING at %s' % (n, p))

print('\n--- search by basename ---')
want = set(os.path.basename(n) for n in NAMES) | {
    'hydradb-dispositions.proposed.md', 'correction-crosswalk.json',
    'inherited-residual-dispositions.proposed.json', 'commit-recovery-plan.md',
    'implementation-boundaries-and-build-plan.md', 'implementation-coverage.md',
    'carrier-format.v3.md', 'carrier-dispatch.v3.json', 'carrier-migration.v1.md',
    'grant-journal.carrier.v3.sql', 'commit-recovery-readonly.v3.md',
}
hits = {}
for dp, dn, fn in os.walk(ROOT):
    for f in fn:
        if f in want:
            hits.setdefault(f, []).append(os.path.relpath(os.path.join(dp, f), ROOT))
for k in sorted(want):
    for v in hits.get(k, ['<<NOT FOUND>>']):
        print('%-46s %s' % (k, v))
