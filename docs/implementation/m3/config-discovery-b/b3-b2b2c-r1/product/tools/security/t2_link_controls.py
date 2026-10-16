"""The T2 link-map controls' reconstructions (M3-B r9 item 20's first control; unit B3-b2b2c, B3-b plan r2 section 3 and
amendment A3).

Developer tool, run by the check lane before the security crate's T2 link-map tests (which it never replaces). For each
lead-readable T2 workspace whose ecosystem has a D15 reader (Cargo and npm; Python has none at M3, law item 20), it:
  * re-verifies every member store against its pinned gitTree and QD-22 treeDigest, no-follow, through the census tool's
    own `verified_tree` and `store_path` (a held-out entry is refused before any filesystem call), and the workspace
    overlay record through the census's `verified_workspace`: canonical, its SHA-256 the manifest's `overlayDigest`, and
    equal to the cache's and the archived acquisition copy;
  * reconstructs a minimal `vcs: none` tree: each overlay link's provider manifest (`Cargo.toml` or `package.json`) at
    `<mount>/<package directory>/`, with its exact verified bytes, and the reader carrier rendered from the overlay as
    FETCH-SPEC section 6 (`.cargo/config.toml`, one `[patch.crates-io]` line per link sorted by package name, the name a
    quoted key; it must equal the cache's rendered file byte for byte) and law item 20 (`package.json` `{"private": true, "workspaces": [<link directories,
    sorted>]}`) state;
  * writes `<out>/<workspace id>/w/` (the tree) and `<out>/<workspace id>/expected.json` (the canonical overlay record,
    its digest, the ecosystem, the member mounts and the link map).
The manifest must be the one the bound T2 census was taken over (its SHA-256 in discovery_census.json). No corpus byte is
written into any repository: `--out` must lie outside both checkouts (the lane gives its private temporary directory).
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import os
import shutil
import sys

CENSUS_TOOL = 'tools/security/discovery_census.py'
CENSUS_RECORD = 'crates/security/src/custody/discovery_census.json'
RENDERED = ('cargo', 'npm')
MANIFEST_NAME = {'cargo': 'Cargo.toml', 'npm': 'package.json'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def carrier(ecosystem, links):
    """The reader carrier rendered from the overlay's link map."""
    if ecosystem == 'cargo':
        # FETCH-SPEC section 6, with each package name a quoted key, as the acquisition rendered the cache's file.
        body = '[patch.crates-io]\n' + ''.join('"%s" = { path = "%s" }\n' % (name, links[name]) for name in sorted(links))
        return '.cargo/config.toml', body.encode()
    doc = {'private': True, 'workspaces': sorted(links.values(), key=lambda s: s.encode())}
    return 'package.json', (json.dumps(doc, indent=2) + '\n').encode()


def write(path, raw, mode):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(raw)
    os.chmod(path, mode)


def reconstruct(product, arch, cache, out):
    census = load('discovery_census', product / CENSUS_TOOL)
    manifest_raw = (arch / census.MANIFEST).read_bytes()
    pinned = json.loads((product / CENSUS_RECORD).read_bytes())['manifest']
    require(hashlib.sha256(manifest_raw).hexdigest() == pinned['sha256'] and len(manifest_raw) == pinned['bytes'],
            'the T2 manifest is not the one the bound census was taken over')
    manifest = json.loads(manifest_raw)
    store = os.path.join(cache, 'store')
    by_id = {e['id']: e for e in manifest['repositories']}
    done = []
    for ws in manifest['workspaces']:
        ecosystem = ws['ecosystem']
        if ws['heldOut'] is not False or ecosystem not in RENDERED:
            continue
        trees = {}
        for entry_id in ws['memberIds']:
            entry = by_id[entry_id]
            trees[entry_id] = census.verified_tree(census.store_path(store, entry), entry)
        _, members, overlay_raw = census.verified_workspace(cache, arch, store, ws, manifest, trees)
        overlay = ws['overlay']
        require(overlay_raw == census.canonical(overlay) and hashlib.sha256(overlay_raw).hexdigest() == ws['overlayDigest'],
                'overlay digest: ' + ws['id'])
        links = overlay['links'][ecosystem]
        mounts = {m['mount']: by_id[m['entry']] for m in overlay['members']}
        root = out / ws['id']
        require(not root.exists(), 'the reconstruction exists already: ' + str(root))
        w = root / 'w'
        for mount in sorted(mounts):
            (w / mount).mkdir(parents=True)
        for name in sorted(links):
            # `<mount>` or `<mount>/<package directory>`: a member may provide a package at its root.
            mount, _, rel = links[name].partition('/')
            require(mount in mounts, 'a link outside the overlay members: ' + links[name])
            inner = (rel + '/' if rel else '') + MANIFEST_NAME[ecosystem]
            require(trees[mounts[mount]['id']].nodes.get(inner, {}).get('kind') == 'file',
                    'a provider manifest is not a verified regular file: ' + links[name])
            with open(os.path.join(census.store_path(store, mounts[mount]), inner), 'rb') as fh:
                raw = fh.read()
            write(w / mount / inner, raw, 0o644)
        path, raw = carrier(ecosystem, links)
        if ecosystem == 'cargo':
            # FETCH-SPEC section 6's own rendering, as the cache wrote it.
            with open(os.path.join(cache, 'workspaces', ws['id'], '.cargo', 'config.toml'), 'rb') as fh:
                require(fh.read() == raw, 'the Cargo carrier differs from the cache rendering: ' + ws['id'])
        write(w / path, raw, 0o644)
        for d in [w] + sorted(p for p in w.rglob('*') if p.is_dir()):
            os.chmod(d, 0o755)
        write(root / 'expected.json', json.dumps(dict(id=ws['id'], ecosystem=ecosystem, overlayDigest=ws['overlayDigest'],
                                                      overlay=overlay_raw.decode(), members=sorted(mounts), links=links),
                                                 indent=2, sort_keys=True).encode() + b'\n', 0o644)
        done.append(dict(id=ws['id'], ecosystem=ecosystem, members=len(mounts), links=len(links), overlayDigest=ws['overlayDigest']))
    return done


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--architecture', type=Path, required=True)
    parser.add_argument('--t2-cache', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True, help='a new directory outside both checkouts')
    args = parser.parse_args()
    product = Path(__file__).resolve().parent.parent.parent
    arch = args.architecture.resolve(strict=True)
    out = args.out.resolve()
    for checkout in (product, arch):
        require(out != checkout and checkout not in out.parents, 'the reconstruction must lie outside the checkouts')
    require(not out.exists(), 'the output directory exists already: ' + str(out))
    out.mkdir(mode=0o700)
    try:
        done = reconstruct(product, arch, str(args.t2_cache.resolve(strict=True)), out)
    except BaseException:
        shutil.rmtree(out)
        raise
    print(json.dumps(dict(reconstructed=done), indent=2))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, TypeError, OSError) as error:
        print(f'T2 link-control reconstruction failed: {error}', file=sys.stderr)
        raise SystemExit(1)
