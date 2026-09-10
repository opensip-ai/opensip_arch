"""P4 (INVOCATION probe). Run the PIN-GATED checkers in a DISPOSABLE repinned clone.

Kind: invocation probe over the two checkers that gate on their own source-pin ledgers
(native/check_native_evidence.v2.py, security/check-security-lifecycle.v1.py) plus, for symmetry,
the workflows launcher.

WHY A CLONE. Those ledgers already disagreed with the delivered bytes BEFORE this correction
(V20-ROOT-1: main changed 10 files and refreshed no pin; root then applied its stage/schema deltas)
and this correction changes more of them. NO PIN IS REFRESHED IN `work`. The repin happens ONLY in
this throwaway tree, and NO PIN MATCH IS CLAIMED for the delivered bytes. Recomputing a digest and
calling it a pin would destroy the evidence root needs to seal the pins itself.

The `before` run uses a repinned clone of the PARENT source, the `after` run a repinned clone of the
corrected source, so the two are compared under identical gating.
"""
import hashlib, json, subprocess, sys
from pathlib import Path

SRC = Path(sys.argv[1])            # a `work` tree
DEST = Path(sys.argv[2])
PY = sys.argv[3]

if DEST.exists():
    subprocess.run(['rm', '-rf', str(DEST)], check=True)
DEST.mkdir(parents=True)
subprocess.run(['cp', '-Rc', str(SRC / 'docs'), str(DEST / 'docs')], check=True)

D = DEST / 'docs/coop/design-corrections'
repinned = {}
for ledger in sorted(D.glob('*/source-pins*.json')):
    man = json.loads(ledger.read_text())
    rows = man.get('files', man.get('pins'))
    assert rows is not None, 'unrecognised pin ledger shape: ' + str(ledger)
    changed = 0
    for item in rows:
        f = DEST / item['path']
        if f.is_file():
            h = hashlib.sha256(f.read_bytes()).hexdigest()
            if h != item['sha256']:
                item['sha256'] = h
                changed += 1
    ledger.write_text(json.dumps(man, indent=2) + '\n')
    repinned[str(ledger.relative_to(D))] = {'rows': len(rows), 'digestsRewritten': changed}

CHECKERS = [('native', 'native/check_native_evidence.v2.py'),
            ('security', 'security/check-security-lifecycle.v1.py'),
            ('workflows-launcher', 'workflows/run-reference-checks.py')]
out = {'kind': 'invocation probe in a DISPOSABLE repinned clone; no pin in `work` was touched',
       'source': str(SRC), 'clone': str(DEST), 'repinnedLedgers': repinned, 'runs': {}}
for name, rel in CHECKERS:
    rep = DEST / ('repinned-%s.json' % name)
    r = subprocess.run([PY, '-I', '-B', str(D / rel), '--report', str(rep)],
                       capture_output=True, text=True, timeout=2400)
    out['runs'][name] = {'exitCode': r.returncode, 'stdout': r.stdout.strip()[-1500:],
                         'stderr': r.stderr.strip()[-1500:]}
print(json.dumps(out, indent=1))
