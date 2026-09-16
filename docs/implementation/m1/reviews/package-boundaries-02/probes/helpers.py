"""Reviewer-owned real-Cargo probes rebound to the v3 inventory. Scratch-only fixtures."""
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

TOOL = Path(os.environ.get('TOOL', Path(__file__).resolve().parents[1] / 'subject-copy/tools/check_package_edges.py'))
INVENTORY = json.loads(Path('/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m1/repository-file-inventory.v3.json').read_bytes())
spec = importlib.util.spec_from_file_location('edges', TOOL)
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)
CARGO = shutil.which('cargo')
HOST = {'opensip-cli': 'apps/cli', 'opensip-contracts': 'crates/contracts', 'opensip-identity': 'crates/identity',
        'opensip-platform': 'crates/platform', 'opensip-reporting': 'crates/reporting', 'opensip-host': 'crates/host'}


def pkg(name, extra='', edition='2024', lib='src/lib.rs'):
    return f'[package]\nname="{name}"\nversion="0.1.0"\nedition="{edition}"\npublish=false\n{extra}'


def fixture():
    root = Path(tempfile.mkdtemp(prefix='fx-')).resolve()
    for name, rel in HOST.items():
        (root / rel / 'src').mkdir(parents=True)
        (root / rel / 'src/lib.rs').write_text('')
        (root / rel / 'Cargo.toml').write_text(pkg(name))
    (root / 'providers/rust/src').mkdir(parents=True)
    (root / 'providers/rust/src/main.rs').write_text('fn main() {}\n')
    (root / 'providers/rust/Cargo.toml').write_text('[workspace]\nmembers=["."]\n\n' + pkg('opensip-rust-provider'))
    members = ','.join(f'"{p}"' for p in HOST.values())
    (root / 'Cargo.toml').write_text(f'[workspace]\nresolver="3"\nmembers=[{members}]\nexclude=["providers/rust"]\n')
    return root


def metadata(root, manifest='Cargo.toml', extra=()):
    run = subprocess.run([CARGO, 'metadata', '--offline', '--format-version', '1', *extra, '--manifest-path', str(root / manifest)],
                         capture_output=True, text=True, env={**os.environ, 'CARGO_TARGET_DIR': str(root / 'target')})
    if run.returncode:
        raise RuntimeError('cargo: ' + run.stderr.strip().splitlines()[-1])
    return json.loads(run.stdout)


def append(root, rel, text):
    with (root / rel / 'Cargo.toml').open('a') as s:
        s.write(text)


results = []


def case(name, expect, build, lane='host', stale=False, manifest='Cargo.toml', extra=(), repo=None):
    """expect: 'pass' or refusal substring. build(root) edits fixture; stale captures metadata before edits."""
    root = fixture()
    outcome = None
    try:
        if stale:
            meta = metadata(root, manifest, extra)
            build(root)
        else:
            build(root)
            meta = metadata(root, manifest, extra)
        r = M.check(repo(root) if repo else root, meta, INVENTORY, lane)
        outcome = 'pass'
    except RuntimeError as exc:
        outcome = str(exc)
    except (M.BoundaryError, OSError, KeyError, TypeError, ValueError) as exc:
        outcome = 'refused: ' + str(exc)
    ok = outcome == 'pass' if expect == 'pass' else (outcome != 'pass' and expect in outcome)
    results.append({'case': name, 'expect': expect, 'outcome': outcome, 'asExpected': ok})
    shutil.rmtree(root)


nop = lambda r: None
DEV_DEP = '[dev-dependencies]\n'
