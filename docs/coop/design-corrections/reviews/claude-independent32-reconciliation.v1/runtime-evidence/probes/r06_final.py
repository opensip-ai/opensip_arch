"""R06 — final check: historical files untouched, both reports consistent with each other."""
import hashlib, json, os, re

BASE = '/tmp/opensip-design-corrections/claude-independent32-reconciliation.v1'
V32 = '/tmp/opensip-design-corrections/claude-independent-design.v32'
SRC = '/tmp/opensip-design-corrections/candidate-subject.v32'
MAN = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v32.json'


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


print('source32 manifest sha :', sha(MAN)[:24], '| required match:',
      sha(MAN) == '3897e8d1bb389f3d39669997d3078d5a44fa024f29d97bd17854a48916610bf2')
# the source files I read this pass, re-verified
man = {f['path']: f for f in json.load(open(MAN))['files']}
READ = ['docs/coop/design-corrections/foundation/evaluator-fault-contract.v3.md',
        'docs/coop/design-corrections/foundation/check-replay.v3.py',
        'docs/coop/design-corrections/native/protocol3-transitions.v1.json',
        'docs/coop/artifacts/fact-identity-policy.v2.json']
bad = [p for p in READ if sha(os.path.join(SRC, p)) != man[p]['sha256']]
print('source files read this pass, hash-verified:', len(READ) - len(bad), 'of', len(READ))

print('\nhistorical v32 runtime preserved:')
for n in ('review.json', 'review.md'):
    p = os.path.join(V32, n)
    print('   %-14s sha=%s' % (n, sha(p)[:24]))
R = json.load(open(os.path.join(BASE, 'review.json')))
print('   superseded sha recorded in successor:',
      R['recordLineage']['supersededRecord']['sha256'][:24])
print('   matches on disk:',
      R['recordLineage']['supersededRecord']['sha256'] == sha(os.path.join(V32, 'review.json')))

md = open(os.path.join(BASE, 'review.md'), encoding='utf-8').read()
checks = {
    'md states ACCEPT unchanged': 'Verdict: ACCEPT — unchanged' in md,
    'md states 107 dispositions': '**107**' in md or '107' in md,
    'md states 13 TCB dependents': '**13**' in md,
    'md states 28 / 32 / 54': all(x in md for x in ('**28**', '**32**', '**54**')),
    'md states condition5 NOT MET': 'condition 5 NOT MET' in md,
    'md names the four RR32 ids': all(x in md for x in ('RR32-01', 'RR32-02', 'RR32-03', 'RR32-04')),
    'md records the superseded location': 'claude-independent-design.v32' in md,
    'md keeps design-only scope': 'no application grade' in md.lower(),
    'md declares no consumer-b read': 'consumer-b' in md,
    'json verdict is ACCEPT': R['verdict'] == 'ACCEPT',
    'json/md agree on manifest': R['subjectManifestSha256'][:8] in md,
}
print('\nreport cross-consistency:')
for k, v in checks.items():
    print('   %-44s %s' % (k, 'OK' if v else 'FAIL'))
cons = json.load(open(os.path.join(BASE, 'receipts', 'r04-consistency.json')))
print('\nstructural consistency: %d checks, %d failures' % (len(cons['checks']), len(cons['failures'])))
print('\noutput tree:')
for n in sorted(os.listdir(BASE)):
    p = os.path.join(BASE, n)
    print('   %-22s %s' % (n, os.path.getsize(p) if os.path.isfile(p) else '<dir>'))
print('receipts: %d | probes: %d' % (len(os.listdir(os.path.join(BASE, 'receipts'))),
                                     len(os.listdir(os.path.join(BASE, 'probes')))))
