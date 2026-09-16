"""S03 — every non-review candidate36 file that carries the frozen36 sha256 (hex, or sha256:-prefixed) of any file the proposed
successor patch changes. These are the digest-bearing owners a successor must update beyond the five pin ledgers (the rehearsal
found one: check-identity v20-native-view-fixture-declares-current-registered-schemas). Read-only on frozen36."""
import hashlib, json, os, re

S36 = '/tmp/opensip-design-corrections/candidate-subject.v36'
V1 = '/tmp/opensip-design-corrections/claude-consumer23-gap-assessment.v1'
OUT = '/tmp/opensip-design-corrections/claude-consumer23-gap-assessment.v2/receipts'
MAN = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v36.json'
man = {f['path']: f['sha256'] for f in json.load(open(MAN))['files']}
patch = open(os.path.join(V1, 'successor-patch/successor-v23-gaps.patch'), encoding='utf-8').read()
changed = sorted(set(re.findall(r'^\+\+\+ b/(\S+)', patch, re.M)))
LEDGERS = {'docs/coop/design-corrections/foundation/source-pins.v1.json', 'docs/coop/design-corrections/foundation/evaluator3-source-pins.v1.json',
           'docs/coop/design-corrections/native/source-pins.v2.json', 'docs/coop/design-corrections/security/source-pins.v1.json',
           'docs/coop/design-corrections/workflows/source-pins.v1.json'}
old = {p: man[p] for p in changed}
kit = {p: hashlib.sha256(open(os.path.join(V1, 'disposable/kit36-successor', p), 'rb').read()).hexdigest() for p in changed}
hits = {p: [] for p in changed}
for rel in man:
    if not rel.startswith('docs/') or '/reviews/' in rel:
        continue
    try:
        t = open(os.path.join(S36, rel), 'rb').read().decode('utf-8')
    except Exception:  # noqa: BLE001
        continue
    for p, h in old.items():
        if h in t:
            hits[p].append({'file': rel, 'occurrences': t.count(h), 'isPinLedger': rel in LEDGERS})
R = {'changedFiles': changed, 'frozen36Digest': old, 'rehearsedDigest': kit,
     'bearers': hits, 'nonLedgerBearers': {p: [h for h in v if not h['isPinLedger']] for p, v in hits.items()}}
for p in changed:
    print('%-80s ledgers=%d nonLedger=%s' % (p, sum(1 for h in hits[p] if h['isPinLedger']), [h['file'] for h in hits[p] if not h['isPinLedger']]))
json.dump(R, open(os.path.join(OUT, 's03-digest-bearers.json'), 'w'), indent=1)
print('wrote s03-digest-bearers.json')
