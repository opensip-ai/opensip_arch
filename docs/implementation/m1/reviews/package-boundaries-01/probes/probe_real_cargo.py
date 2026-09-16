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
# Positive, real Cargo, allowed edges in all declaration forms.
case('baseline host', 'pass', nop)
case('baseline provider lane', 'pass', nop, lane='rust-provider', manifest='providers/rust/Cargo.toml')
case('renamed alias host->contracts', 'pass', lambda r: append(r, 'crates/host', '[dependencies]\ndto={package="opensip-contracts",path="../contracts",version="=0.1.0"}\n'))
case('optional feature-gated host->identity', 'pass', lambda r: append(r, 'crates/host', '[dependencies]\nid={package="opensip-identity",path="../identity",optional=true}\n[features]\nx=["dep:id"]\n'))
case('cfg(windows) host->platform', 'pass', lambda r: append(r, 'crates/host', "[target.'cfg(windows)'.dependencies]\nopensip-platform={path=\"../platform\"}\n"))
case('triple target build dep host->reporting', 'pass', lambda r: append(r, 'crates/host', '[target.x86_64-pc-windows-msvc.build-dependencies]\nopensip-reporting={path="../reporting"}\n'))
case('dev dep cli->contracts + normal cli->host', 'pass', lambda r: append(r, 'apps/cli', '[dependencies]\nopensip-host={path="../../crates/host"}\n[dev-dependencies]\nopensip-contracts={path="../../crates/contracts",default-features=false}\n'))
case('same crate normal+dev+build host->contracts', 'pass', lambda r: append(r, 'crates/host', '[dependencies]\nopensip-contracts={path="../contracts"}\n[dev-dependencies]\nopensip-contracts={path="../contracts"}\n[build-dependencies]\nopensip-contracts={path="../contracts"}\n'))
case('filter-platform drops windows resolve edge', 'pass', lambda r: append(r, 'crates/host', "[target.'cfg(windows)'.dependencies]\nopensip-platform={path=\"../platform\"}\n"), extra=('--filter-platform', 'aarch64-apple-darwin'))
case('provider lane provider->contracts,identity', 'pass', lambda r: append(r, 'providers/rust', '[dependencies]\nopensip-contracts={path="../../crates/contracts"}\nopensip-identity={path="../../crates/identity"}\n'), lane='rust-provider', manifest='providers/rust/Cargo.toml')
case('cfg with whitespace normalisation', 'pass', lambda r: append(r, 'crates/host', "[target.'cfg( windows )'.dependencies]\nopensip-platform={path=\"../platform\"}\n"))
case('non-normalized dep path ../host/../contracts', 'pass', lambda r: append(r, 'crates/host', '[dependencies]\nopensip-contracts={path="../host/../contracts"}\n'))

# Negative, fresh real Cargo metadata.
case('contracts->host normal', 'forbidden declared internal edge', lambda r: append(r, 'crates/contracts', '[dependencies]\nopensip-host={path="../host"}\n'))
case('identity->platform triple dev', 'forbidden declared internal edge', lambda r: append(r, 'crates/identity', '[target.aarch64-unknown-linux-gnu.dev-dependencies]\nopensip-platform={path="../platform"}\n'))
case('reporting->host alias spoofed as contracts, optional unused', 'forbidden declared internal edge', lambda r: append(r, 'crates/reporting', '[dependencies]\nopensip-contracts={package="opensip-host",path="../host",optional=true}\n'))
case('platform->host under filtered-out cfg with filter-platform', 'forbidden declared internal edge', lambda r: append(r, 'crates/platform', "[target.'cfg(windows)'.build-dependencies]\nopensip-host={path=\"../host\"}\n"), extra=('--filter-platform', 'aarch64-apple-darwin'))
case('provider->host', 'forbidden declared internal edge', lambda r: append(r, 'providers/rust', '[dependencies]\nopensip-host={path="../../crates/host"}\n'), lane='rust-provider', manifest='providers/rust/Cargo.toml')
case('host->provider path', 'forbidden declared internal edge', lambda r: append(r, 'crates/host', '[dev-dependencies]\nopensip-rust-provider={path="../../providers/rust"}\n'))


def unknown_local(r):
    (r / 'crates/evil/src').mkdir(parents=True)
    (r / 'crates/evil/src/lib.rs').write_text('')
    (r / 'crates/evil/Cargo.toml').write_text(pkg('evil'))
    append(r, 'crates/host', '[dependencies]\nevil={path="../evil"}\n')


case('non-inventory local crate', 'unknown or relocated local package', unknown_local)


def provider_member(r):
    (r / 'providers/rust/Cargo.toml').write_text(pkg('opensip-rust-provider'))
    text = (r / 'Cargo.toml').read_text().replace('"crates/host"]', '"crates/host","providers/rust"]').replace('exclude=["providers/rust"]\n', '')
    (r / 'Cargo.toml').write_text(text)


case('host workspace includes provider', 'workspace crosses host/provider boundary', provider_member)
case('lib path escapes into another package', 'target crosses package source boundary', lambda r: (r / 'crates/host/Cargo.toml').write_text(pkg('opensip-host', '[lib]\npath="../contracts/src/lib.rs"\n')))
case('build script escapes', 'target crosses package source boundary', lambda r: ((r / 'crates/build.rs').write_text('fn main(){}\n'), (r / 'crates/host/Cargo.toml').write_text(pkg('opensip-host', 'build="../build.rs"\n'))))


def symlink_src(r):
    (r / 'crates/host/src/lib.rs').unlink()
    (r / 'crates/host/src/lib.rs').symlink_to(r / 'crates/contracts/src/lib.rs')


case('symlinked lib.rs escapes', 'target crosses package source boundary', symlink_src)


def ws_inherit(r):
    (r / 'Cargo.toml').write_text((r / 'Cargo.toml').read_text() + '[workspace.package]\nversion="0.1.0"\n')
    (r / 'crates/host/Cargo.toml').write_text('[package]\nname="opensip-host"\nversion.workspace=true\nedition="2024"\n')


case('version.workspace inheritance', 'must not inherit workspace values', ws_inherit)


def ws_dep(r):
    (r / 'Cargo.toml').write_text((r / 'Cargo.toml').read_text() + '[workspace.dependencies]\nopensip-contracts={path="crates/contracts"}\n')
    append(r, 'crates/host', '[dependencies]\nopensip-contracts={workspace=true}\n')


case('workspace-inherited internal dependency', 'must not inherit workspace values', ws_dep)
case('host metadata under provider lane', 'workspace crosses host/provider boundary', nop, lane='rust-provider')
case('repository argument is a parent dir', 'unknown or relocated local package', nop, repo=lambda r: r.parent)

# Stale metadata (captured before the edit).
case('stale: inactive cfg(windows) build dep contracts->host', 'forbidden manifest internal edge', lambda r: append(r, 'crates/contracts', "[target.'cfg(windows)'.build-dependencies]\nopensip-host={path=\"../host\"}\n"), stale=True)
case('stale: optional alias reporting->host', 'forbidden manifest internal edge', lambda r: append(r, 'crates/reporting', '[dependencies]\nx={package="opensip-host",path="../host",optional=true}\n'), stale=True)
case('stale: allowed host->contracts added', 'metadata internal declarations differ', lambda r: append(r, 'crates/host', '[dependencies]\nopensip-contracts={path="../contracts"}\n'), stale=True)
case('stale: edition2021 underscore dev_dependencies contracts->host', 'refused', lambda r: (r / 'crates/contracts/Cargo.toml').write_text(pkg('opensip-contracts', '[dev_dependencies]\nopensip-host={path="../host"}\n', edition='2021')), stale=True)
case('fresh: edition2021 underscore dev_dependencies contracts->host', 'forbidden declared internal edge', lambda r: (r / 'crates/contracts/Cargo.toml').write_text(pkg('opensip-contracts', '[dev_dependencies]\nopensip-host={path="../host"}\n', edition='2021')))
case('fresh: edition2021 underscore allowed host->contracts', 'pass', lambda r: (r / 'crates/host/Cargo.toml').write_text(pkg('opensip-host', '[build_dependencies]\nopensip-contracts={path="../contracts"}\n', edition='2021')))
case('stale: lib path escape added', 'refused', lambda r: (r / 'crates/host/Cargo.toml').write_text(pkg('opensip-host', '[lib]\npath="../contracts/src/lib.rs"\n')), stale=True)
case('stale: provider added to host workspace', 'refused', provider_member, stale=True)
case('stale: package renamed in manifest', 'metadata package differs from manifest', lambda r: (r / 'crates/host/Cargo.toml').write_text(pkg('opensip-hostx')), stale=True)

print(json.dumps({'tool': str(TOOL), 'cargo': subprocess.run([CARGO, '--version'], capture_output=True, text=True).stdout.strip(), 'results': results}, indent=1))
sys.exit(0)
