#!/usr/bin/env python3
"""Probe 02: (a) verify disposable copy-A is byte-exact against the frozen
manifest; (b) independently verify ALL transitive source pins declared by the
four source-pins files and the six reference-check command sources, BEFORE any
execution.
"""
import hashlib, json, os, sys

MANIFEST = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v16.json'
OUT = '/tmp/opensip-design-corrections/post-reset-review.v16'
COPY = os.path.join(OUT, 'copy-A-reference-run')

def sha256(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 20), b''):
            h.update(c)
    return h.hexdigest()

m = json.load(open(MANIFEST))
copy_bad, copy_missing = [], []
for rec in m['files']:
    full = os.path.join(COPY, rec['path'])
    if not os.path.isfile(full):
        copy_missing.append(rec['path']); continue
    if os.stat(full).st_size != rec['bytes'] or sha256(full) != rec['sha256']:
        copy_bad.append(rec['path'])
on_disk = set()
for dp, dn, fns in os.walk(COPY):
    for fn in fns:
        on_disk.add(os.path.relpath(os.path.join(dp, fn), COPY))
extra = sorted(on_disk - {r['path'] for r in m['files']})

# --- source pins ---
PINFILES = [
    'docs/coop/design-corrections/foundation/source-pins.v1.json',
    'docs/coop/design-corrections/native/source-pins.v2.json',
    'docs/coop/design-corrections/security/source-pins.v1.json',
    'docs/coop/design-corrections/workflows/source-pins.v1.json',
]
pin_report = []
grand_total = grand_ok = 0
all_mismatch = []
for pf in PINFILES:
    doc = json.load(open(os.path.join(COPY, pf)))
    # discover the pin entries generically: any dict having a path-like key and a sha256
    entries = []
    def walk(o):
        if isinstance(o, dict):
            keys = set(o)
            pathkey = next((k for k in ('path', 'file', 'source', 'relPath') if k in o and isinstance(o[k], str)), None)
            shakey = next((k for k in ('sha256', 'digest', 'sha256Hex') if k in o and isinstance(o[k], str)), None)
            if pathkey and shakey:
                entries.append((o[pathkey], o[shakey]))
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(doc)
    ok = bad = miss = 0
    mism = []
    for path, dig in entries:
        full = os.path.join(COPY, path)
        if not os.path.isfile(full):
            miss += 1; mism.append(('MISSING', path)); continue
        got = sha256(full)
        if got == dig:
            ok += 1
        else:
            bad += 1; mism.append(('MISMATCH', path, dig, got))
    grand_total += len(entries); grand_ok += ok
    all_mismatch.extend((pf,) + t for t in mism)
    pin_report.append({'pinFile': pf, 'pinFileSha256': sha256(os.path.join(COPY, pf)),
                       'entries': len(entries), 'ok': ok, 'mismatch': bad, 'missing': miss,
                       'topKeys': sorted(doc)[:12] if isinstance(doc, dict) else None})

# --- six reference-check command sources ---
rc = json.load(open(os.path.join(
    COPY, 'docs/coop/design-corrections/reviews/codex-post-reset.v1/final-reference.v16/reference-checks.json')))
cmd_report = []
for c in rc['commands']:
    full = os.path.join(COPY, c['source'])
    got = sha256(full) if os.path.isfile(full) else None
    cmd_report.append({'name': c['name'], 'source': c['source'],
                       'declaredSha256': c['sourceSha256'], 'observedSha256': got,
                       'matches': got == c['sourceSha256'],
                       'declaredExit': c['exitCode']})

res = {
    'probe': 'probe-02-verify-copy-and-pins',
    'phase': 'pre-execution',
    'copyName': 'copy-A-reference-run',
    'copyPath': COPY,
    'copyFilesChecked': len(m['files']),
    'copyMissing': copy_missing,
    'copyMismatch': copy_bad,
    'copyExtraFiles': extra,
    'copyByteExact': not (copy_missing or copy_bad or extra),
    'pinFiles': pin_report,
    'pinEntriesTotal': grand_total,
    'pinEntriesOk': grand_ok,
    'pinMismatches': all_mismatch[:50],
    'pinAllValid': grand_ok == grand_total,
    'referenceCheckSources': cmd_report,
    'referenceCheckSourcesAllMatch': all(c['matches'] for c in cmd_report),
    'repinPerformed': False,
    'note': 'No pin was rewritten. Verification is read-only against the frozen bytes.',
}
with open(os.path.join(OUT, 'probe-02-verify-copy-and-pins.json'), 'w') as f:
    json.dump(res, f, indent=2, sort_keys=True)
print(json.dumps({k: v for k, v in res.items() if k not in ('pinMismatches', 'copyExtraFiles')},
                 indent=2, sort_keys=True))
