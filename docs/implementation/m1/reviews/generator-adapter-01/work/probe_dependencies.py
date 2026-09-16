"""Reviewer negatives for tools/check_dependencies.py on clones of the subject workspace."""
import json, shutil, subprocess, os
from pathlib import Path

R = Path('/tmp/opensip-implementation/m1-generator-adapter-review-01')
BASE = R / 'work/dep'
CARGO = '/opt/homebrew/bin/cargo'
SHA2 = '/Users/sb/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/sha2-const-stable-0.1.0'
results = []


def clone(name):
    d = R / 'work/d' / name
    if d.exists(): shutil.rmtree(d)
    d.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(['cp', '-cR', str(BASE), str(d)], check=True)
    return d


def run(name, root, expect, target='aarch64-apple-darwin', policy=None, relock=True):
    env = dict(os.environ, CARGO_TARGET_DIR=str(R / 'tmp/cargo-target'))
    lock = ''
    if relock:
        p = subprocess.run([CARGO, 'metadata', '--offline', '--format-version', '1', '--manifest-path', str(root / 'crates/contracts/Cargo.toml')],
                           capture_output=True, text=True, env=env)
        lock = '' if p.returncode == 0 else 'relock failed: ' + p.stderr.strip().splitlines()[-1]
    argv = ['python3', '-I', '-B', str(root / 'tools/check_dependencies.py'), '--manifest', str(root / 'crates/contracts/Cargo.toml'),
            '--target', target, '--cargo', CARGO] + (['--policy', str(policy)] if policy else [])
    p = subprocess.run(argv, capture_output=True, text=True, env=env)
    row = {'probe': name, 'target': target, 'exit': p.returncode, 'expect': expect,
           'matchesExpectation': (p.returncode == 0) == (expect == 'accept'),
           'tail': (p.stdout.strip() or p.stderr.strip()).splitlines()[-1][:300], 'relock': lock}
    results.append(row); print(json.dumps(row))


def edit(root, old, new):
    f = root / 'crates/contracts/Cargo.toml'; t = f.read_text(); assert old in t, old; f.write_text(t.replace(old, new))


def main():
    run('D00 baseline', clone('d00'), 'accept', relock=False)
    r = clone('d01'); edit(r, 'features = ["derive"]', 'features = ["derive", "rc"]'); run('D01 extra serde feature', r, 'refuse')
    r = clone('d02'); edit(r, 'serde_json = "=1.0.151"', 'serde_json = "=1.0.151"\nsha2-const-stable = "=0.1.0"'); run('D02 undeclared normal dependency', r, 'refuse')
    r = clone('d03'); (r / 'crates/contracts/Cargo.toml').write_text((r / 'crates/contracts/Cargo.toml').read_text() + '\n[dev-dependencies]\nsha2-const-stable = "=0.1.0"\n')
    run('D03 undeclared dev-dependency', r, 'refuse')
    r = clone('d04'); (r / 'crates/contracts/Cargo.toml').write_text((r / 'crates/contracts/Cargo.toml').read_text() + '\n[build-dependencies]\nsha2-const-stable = "=0.1.0"\n')
    run('D04 undeclared build-dependency', r, 'refuse')
    r = clone('d05'); (r / 'crates/contracts/Cargo.toml').write_text((r / 'crates/contracts/Cargo.toml').read_text() + "\n[target.'cfg(windows)'.dependencies]\nsha2-const-stable = \"=0.1.0\"\n")
    run('D05 windows-only undeclared dependency, darwin filter', r, 'refuse')
    run('D05b same, windows filter', r, 'refuse', target='x86_64-pc-windows-msvc', relock=False)
    r = clone('d06'); (r / 'crates/contracts/Cargo.toml').write_text((r / 'crates/contracts/Cargo.toml').read_text() + "\n[target.'cfg(any())'.dependencies]\nsha2-const-stable = \"=0.1.0\"\n")
    run('D06 cfg(any()) edge (never compiled)', r, 'accept')
    r = clone('d07'); (r / 'crates/contracts/build.rs').write_text('fn main(){}\n'); run('D07 root build script', r, 'refuse', relock=False)
    r = clone('d08'); (r / 'crates/contracts/src/bin').mkdir(parents=True); (r / 'crates/contracts/src/bin/x.rs').write_text('fn main(){}\n')
    edit(r, 'autobins = false', 'autobins = true'); run('D08 extra binary target', r, 'refuse', relock=False)
    r = clone('d09'); edit(r, 'serde_json = "=1.0.151"', 'serde_json = "=1.0.151"\nsha2-const-stable = { version = "=0.1.0", optional = true }\n[features]\ndefault = ["sha2-const-stable"]')
    run('D09 optional dependency enabled by default feature', r, 'refuse')
    r = clone('d10'); edit(r, 'serde_json = "=1.0.151"', 'serde_json = "=1.0.151"\nsha2-const-stable = { path = "%s" }' % SHA2); run('D10 path dependency to local source', r, 'refuse')
    r = clone('d11'); pol = json.loads((r / 'tools/contracts/dependency-policy.json').read_text()); pol['dependencies'][0]['checksum'] = '0' * 64
    (r / 'pol.json').write_text(json.dumps(pol)); run('D11 policy checksum mismatch', r, 'refuse', policy=r / 'pol.json', relock=False)
    r = clone('d12'); pol = json.loads((r / 'tools/contracts/dependency-policy.json').read_text()); del pol['resolvedFeatures']['memchr']
    (r / 'pol.json').write_text(json.dumps(pol)); run('D12 policy lacks feature row', r, 'refuse', policy=r / 'pol.json', relock=False)
    r = clone('d13'); edit(r, 'publish = false', 'publish = false\nbuild = false'); edit(r, '[dependencies]', '[features]\nunsafe-extra = []\ndefault = ["unsafe-extra"]\n\n[dependencies]')
    run('D13 root-crate own feature added (no dependency effect)', r, 'refuse', relock=False)
    (R / 'logs/dependency-probes.json').write_text(json.dumps(results, indent=2) + '\n')


main()
