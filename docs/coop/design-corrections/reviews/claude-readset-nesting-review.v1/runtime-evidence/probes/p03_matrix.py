"""p03 <source|before-model>: independent helper-level matrix and real-Run controls under one identity model.

source        loads the owner stack from work/source (root's corrected identity model)
before-model  loads it from work/hybrid-p03: a regular copy of work/source with ONLY foundation/identity-model.v3.py
              replaced by root's retained before-file
Helper level: identity-model.v3 snapshot_pruned_tree_faults over one-path inventories (Cargo.toml added for Cargo
cases) against a layout listing left-pad, @scope/util and a linked lib (installPath node_modules/lib, realPath
packages/lib), and with no layouts; discovery-defaults classify_path for each path.
Real Runs: the maintained semantic fixture (build_ts_semantic_graph with extra_sources) through close_positive
(seed admission, derive, replay, close_run). Output: receipts/p03-<variant>.json.
"""
import hashlib, importlib.util, json, shutil, sys
from pathlib import Path

BASE = Path('/tmp/opensip-design-corrections/claude-readset-nesting-review.v1')
ROOT = Path('/tmp/opensip-design-corrections/root-source39-readset-nesting.v1')
MODEL = 'docs/coop/design-corrections/foundation/identity-model.v3.py'
variant = sys.argv[1]
out_path = BASE / 'receipts' / ('p03-%s.json' % variant)
if out_path.exists():
    raise SystemExit('refusing to overwrite ' + str(out_path))
tree = BASE / 'work' / 'source'
if variant == 'before-model':
    tree = BASE / 'work' / 'hybrid-p03'
    shutil.copytree(BASE / 'work' / 'source' / 'docs', tree / 'docs', copy_function=shutil.copy2)
    shutil.copy2(ROOT / 'before-files' / MODEL, tree / MODEL)
F = tree / 'docs/coop/design-corrections/foundation'
spec = importlib.util.spec_from_file_location('p03_c24', F / 'check-native-consumer24-corrections.v1.py')
K = importlib.util.module_from_spec(spec)
sys.modules['p03_c24'] = K
spec.loader.exec_module(K)
M, SR = K.M, K.SR
DD = M.native_admission().DD
out = {'variant': variant, 'tree': str(tree), 'modelSha256': hashlib.sha256((tree / MODEL).read_bytes()).hexdigest(),
       'loadedModelFile': str(Path(M.__file__).resolve()), 'loadedDiscoveryFile': str(Path(DD.__file__).resolve())}

LAYOUT = {"schemaVersion": 1, "entries": [
    {"packageName": "@scope/util", "packageVersion": "2.0.1", "installPath": "node_modules/@scope/util", "realPath": "node_modules/@scope/util", "contentSha256": "3" * 64},
    {"packageName": "left-pad", "packageVersion": "1.3.0", "installPath": "node_modules/left-pad", "realPath": "node_modules/left-pad", "contentSha256": "1" * 64},
    {"packageName": "lib", "packageVersion": "0.1.0", "installPath": "node_modules/lib", "realPath": "packages/lib", "contentSha256": "2" * 64}]}
SEGMENTS = list(DD.VCS_TREE_SEGMENTS)
paths = {}
for s in SEGMENTS:
    paths.update({
        'node_modules/left-pad/%s/HEAD' % s: 'nested-vcs-in-listed-package',
        'node_modules/left-pad/lib/deep/%s/x' % s: 'deeper-nested-vcs-in-listed-package',
        'node_modules/left-pad/%s' % s: 'vcs-segment-as-final-file-in-listed-package',
        'node_modules/@scope/util/%s/entries' % s: 'nested-vcs-in-scoped-listed-package',
        'node_modules/lib/%s/x' % s: 'nested-vcs-under-linked-install-path',
        'packages/lib/%s/x' % s: 'vcs-under-linked-real-path',
        '%s/HEAD' % s: 'first-party-vcs-root',
        'sub/%s/x' % s: 'first-party-nested-vcs',
        'sub/%s' % s: 'first-party-vcs-segment-as-file',
        'node_modules/unlisted/%s/x' % s: 'nested-vcs-in-unlisted-package',
        'node_modules/left-pad/node_modules/evil/%s/HEAD' % s: 'vcs-in-unlisted-nested-dependency',
        'target/%s/x' % s: 'vcs-inside-cargo-build-output',
    })
for p in ['node_modules/left-pad/.gitignore', 'node_modules/left-pad/.git-like/index.js', 'node_modules/left-pad/.github/workflows/ci.yml',
          'node_modules/left-pad/.hgignore', 'node_modules/left-pad/.svnignore', 'node_modules/left-pad/.jjconfig', 'node_modules/left-pad/git/HEAD',
          'node_modules/left-pad/x.git', 'node_modules/left-pad/.GIT/HEAD', 'node_modules/left-pad/.Git/HEAD', 'node_modules/left-pad/a.git/b']:
    paths[p] = 'lookalike-in-listed-package'
for p in ['.github/workflows/ci.yml', 'src/.gitkeep', 'src/x.hg']:
    paths[p] = 'first-party-lookalike'
for p in ['node_modules/left-pad/index.js', 'node_modules/@scope/util/index.js', 'node_modules/lib/dist/index.d.ts', 'packages/lib/index.ts', 'src/a.ts']:
    paths[p] = 'ordinary'
paths['node_modules/left-pad/node_modules/evil/index.js'] = 'unlisted-nested-dependency-under-listed-parent'
paths['node_modules/unlisted/index.js'] = 'unlisted-package'
paths['target/debug/app.d'] = 'cargo-build-output'

matrix = []
for p, kind in sorted(paths.items()):
    inv = [p] + (['Cargo.toml'] if p.startswith('target/') else [])
    cargo = DD.cargo_roots_from_markers(inv)
    matrix.append({'path': p, 'kind': kind,
                   'faultWithLayout': p in M.snapshot_pruned_tree_faults([{'path': x} for x in inv], [LAYOUT]),
                   'faultWithoutLayout': p in M.snapshot_pruned_tree_faults([{'path': x} for x in inv], []),
                   'discovery': DD.classify_path(p, cargo)})
out['matrix'] = matrix

REAL = {
    'node_modules/left-pad/index.js': b'module.exports = 1;\n',
    'node_modules/left-pad/.github/workflows/ci.yml': b'on: push\n',
    'node_modules/left-pad/.svn/entries': b'12\n',
    'node_modules/left-pad/.jj/repo/store/type': b'git\n',
    'node_modules/@scope/util/.git/HEAD': b'ref: refs/heads/main\n',
    'node_modules/left-pad/.git': b'gitdir: ../../.git/modules/left-pad\n',
    'node_modules/left-pad/node_modules/evil/index.js': b'module.exports = 3;\n',
}
real = []
for p, body in REAL.items():
    row = {'path': p}
    try:
        graph = SR.S.build_ts_semantic_graph(atom=SR.REFS_EXISTS_SRC, has_declares=False, has_references_fact=True, extra_sources={p: body})
        run, objects, blobs, actual = SR.close_positive(graph)
        snap = objects[run['snapshotId']][1]
        row.update(outcome='RETURNED', runId=actual['runId'], closeRunId=M.close_run(run, objects, blobs),
                   inventoryHasPath=any(r['path'] == p for r in snap['sourceInventory']))
    except Exception as exc:
        row.update(outcome='REFUSE', exceptionType=type(exc).__name__, reason=str(exc)[:300])
    real.append(row)
out['realRuns'] = real
out_path.write_text(json.dumps(out, indent=1, default=str) + '\n')
print(json.dumps({'variant': variant, 'modelSha256': out['modelSha256'], 'loadedModelFile': out['loadedModelFile'],
                  'faultsWithLayout': sum(r['faultWithLayout'] for r in matrix), 'cases': len(matrix), 'realRuns': real}, indent=1, default=str))
