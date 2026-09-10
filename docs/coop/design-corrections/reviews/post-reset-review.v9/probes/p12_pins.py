"""v9 probe 12 - transitive artifact pins: present in all four suites, and actually AUTHENTICATED.

The v9 correction claims delivery.v4.json, fact-plane.v1.json, fact-identity-policy.v2.json and
resolved-inputs.v2.json appear in all four consuming pin sets. Presence in a manifest is not
authentication, so this probe also (a) confirms each consuming runner verifies its pin set before
running, and (b) tampers with each artifact in a throwaway copy and checks the runner refuses.
"""
import hashlib, json, shutil, subprocess, sys, tempfile
from pathlib import Path

SUB = Path('/tmp/opensip-design-corrections/candidate-subject.v9')
DC = SUB / 'docs/coop/design-corrections'
PY = '/tmp/opensip-architecture-review-env/bin/python'
WANTED = ['delivery.v4.json', 'fact-plane.v1.json', 'fact-identity-policy.v2.json', 'resolved-inputs.v2.json']
SUITES = {
    'foundation': 'foundation/source-pins.v1.json',
    'security': 'security/source-pins.v1.json',
    'native': 'native/source-pins.v2.json',
    'workflows': 'workflows/source-pins.v1.json',
}
out = {'probe': 'p12_pins', 'standing': 'independent reviewer probe; design/reference only'}

# ---- (1) presence and counts
pinsets = {}
for name, rel in SUITES.items():
    d = json.loads((DC / rel).read_text())
    files = d.get('files') or d.get('pins') or d.get('sources') or []
    if isinstance(files, dict):
        entries = [{'path': k, **(v if isinstance(v, dict) else {'sha256': v})} for k, v in files.items()]
    else:
        entries = files
    paths = [e.get('path') for e in entries]
    pinsets[name] = {'count': len(entries), 'keys': sorted(d.keys()),
                     'wantedPresent': {w: any(w in (p or '') for p in paths) for w in WANTED},
                     'wantedPaths': {w: [p for p in paths if w in (p or '')] for w in WANTED}}
out['pinSets'] = pinsets
out['allFourArtifactsInAllFourSuites'] = all(
    all(v['wantedPresent'].values()) for v in pinsets.values())

# ---- (2) do the pinned digests match the actual bytes?
mismatch = []
for name, rel in SUITES.items():
    d = json.loads((DC / rel).read_text())
    files = d.get('files') or d.get('pins') or d.get('sources') or []
    entries = files if isinstance(files, list) else [{'path': k, **(v if isinstance(v, dict) else {'sha256': v})}
                                                     for k, v in files.items()]
    for e in entries:
        p = e.get('path'); h = e.get('sha256')
        if not p or not h:
            continue
        f = SUB / p if (SUB / p).exists() else DC / p
        if not f.exists():
            mismatch.append({'suite': name, 'path': p, 'issue': 'pinned file absent'}); continue
        if hashlib.sha256(f.read_bytes()).hexdigest() != h:
            mismatch.append({'suite': name, 'path': p, 'issue': 'digest mismatch'})
out['pinDigestMismatches'] = mismatch

# ---- (3) tamper test: does each consuming runner REFUSE on a tampered transitive artifact?
RUNNERS = {
    'foundation': ('foundation/run-reference-checks.py', []),
    'security': ('security/check-security-lifecycle.v1.py', []),
    'native': ('native/check_native_evidence.v2.py', []),
    'workflows': ('workflows/run-reference-checks.py', []),
}
tamper = []
for suite, (rel, args) in RUNNERS.items():
    for artifact in WANTED:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / 'copy'
            shutil.copytree(SUB, root)
            target = next((p for p in (root / 'docs/coop/artifacts').glob('*') if p.name == artifact), None)
            if target is None:
                tamper.append({'suite': suite, 'artifact': artifact, 'result': 'artifact not in docs/coop/artifacts'})
                continue
            b = target.read_bytes()
            target.write_bytes(b.replace(b'{', b'{ ', 1))  # semantically inert, byte-changing
            r = subprocess.run([PY, '-I', '-B', str(root / 'docs/coop/design-corrections' / rel)] + args,
                               cwd=root, capture_output=True, text=True, timeout=300)
            blob = (r.stdout + r.stderr)
            tamper.append({'suite': suite, 'artifact': artifact, 'exitCode': r.returncode,
                           'refused': r.returncode != 0,
                           'mentionsPin': 'PIN' in blob.upper() or 'pin' in blob,
                           'tail': blob.strip()[-200:]})
out['tamperTests'] = tamper
out['everySuiteRefusesEveryTamperedTransitiveArtifact'] = all(
    t.get('refused') for t in tamper if 'exitCode' in t)
print(json.dumps(out, indent=1))
