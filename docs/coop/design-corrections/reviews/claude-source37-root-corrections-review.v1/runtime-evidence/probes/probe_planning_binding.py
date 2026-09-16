"""Enumerate every planning/pin binding in the verified overlay copy that still records a pre-overlay SHA-256 of an
overlay file (the planning checker stops at its first failure). No regeneration, no write outside receipts."""
import hashlib, json, os

RT = '/private/tmp/opensip-design-corrections/claude-source37-root-corrections-review.v1'
OV = RT + '/work/source37-overlay'
ov = json.load(open(RT + '/subject-manifest.json'))['files']
before = {f['beforeSha256']: f['path'] for f in ov}
after = {f['sha256']: f['path'] for f in ov}
TARGETS = [
    'docs/v2/architecture/implementation-normative-inputs.v5.json',
    'docs/v2/architecture/implementation-coverage.v1.json',
    'docs/v2/architecture/implementation-planning-sources.v1.json',
    'docs/coop/design-corrections/foundation/evaluator3-source-pins.v1.json',
    'docs/coop/design-corrections/foundation/source-pins.v1.json',
    'docs/coop/design-corrections/native/source-pins.v2.json',
    'docs/coop/design-corrections/security/source-pins.v1.json',
    'docs/coop/design-corrections/workflows/source-pins.v1.json',
    'docs/coop/design-corrections/workflows/workflows-report.v1.json',
]
res = {'standing': 'binding consequence enumeration only; no pin regeneration', 'targets': {}}
for t in TARGETS:
    raw = open(os.path.join(OV, t), 'rb').read()
    text = raw.decode('utf-8')
    stale = sorted({p for h, p in before.items() if h in text})
    current = sorted({p for h, p in after.items() if h in text})
    res['targets'][t] = {'sha256': hashlib.sha256(raw).hexdigest(), 'staleOverlayPaths': stale, 'alreadyUpdatedOverlayPaths': current}
cov = json.load(open(os.path.join(OV, 'docs/v2/architecture/implementation-coverage.v1.json')))
res['coverageSourcesStale'] = sorted(k for k, v in cov['sources'].items() if v.get('path') in {f['path'] for f in ov} and v['sha256'] != hashlib.sha256(open(os.path.join(OV, v['path']), 'rb').read()).hexdigest())
ni = json.load(open(os.path.join(OV, 'docs/v2/architecture/implementation-normative-inputs.v5.json')))
res['normativeInputsV5Stale'] = sorted(r['path'] for r in ni['files'] if r['sha256'] != hashlib.sha256(open(os.path.join(OV, r['path']), 'rb').read()).hexdigest())
res['coverageSubjectManifestSha256StillMatchesV5Bytes'] = cov['subjectManifestSha256'] == hashlib.sha256(open(os.path.join(OV, cov['subjectManifest']), 'rb').read()).hexdigest()
json.dump(res, open(RT + '/receipts/probe-planning-binding.json', 'w'), indent=1)
print(json.dumps(res, indent=1))
