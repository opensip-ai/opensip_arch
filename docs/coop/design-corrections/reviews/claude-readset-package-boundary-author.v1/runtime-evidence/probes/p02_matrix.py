"""p02 <edited|baseline>: helper-level matrix of identity-model.v3 snapshot_pruned_tree_faults under one model, in its
own process. Explicitly scoped: this calls the owner join directly over synthetic layouts; it is not a Run.

edited    loads work/source (explicit nested package custody)
baseline  loads work/hybrid-baseline-model: a regular copy of work/source with ONLY identity-model.v3.py restored to
          the baseline bytes (the prior captured review source)
Output: receipts/p02-<variant>.json.
"""
import hashlib, importlib.util, json, shutil, sys
from pathlib import Path

BASE = Path('/tmp/opensip-design-corrections/claude-readset-package-boundary-author.v1')
PRIOR = Path('/tmp/opensip-design-corrections/claude-readset-nesting-review.v1/work/source')
MODEL = 'docs/coop/design-corrections/foundation/identity-model.v3.py'
variant = sys.argv[1]
out_path = BASE / 'receipts' / ('p02-%s.json' % variant)
if out_path.exists():
    raise SystemExit('refusing to overwrite ' + str(out_path))
tree = BASE / 'work' / 'source'
if variant == 'baseline':
    tree = BASE / 'work' / 'hybrid-baseline-model'
    shutil.copytree(BASE / 'work' / 'source' / 'docs', tree / 'docs', copy_function=shutil.copy2)
    shutil.copy2(PRIOR / MODEL, tree / MODEL)
spec = importlib.util.spec_from_file_location('p02_identity', tree / MODEL)
M = importlib.util.module_from_spec(spec)
sys.modules['p02_identity'] = M
spec.loader.exec_module(M)
DD = M.native_admission().DD


def entry(name, install, real):
    return {"packageName": name, "packageVersion": "1.0.0", "installPath": install, "realPath": real, "contentSha256": "5" * 64}


EVIL = 'node_modules/left-pad/node_modules/evil'
INNER = 'node_modules/@scope/util/node_modules/@inner/pkg'
STORE = 'node_modules/.pnpm/store-pkg@1.0.0/node_modules/store-pkg'
BASE_ROWS = [entry('left-pad', 'node_modules/left-pad', 'node_modules/left-pad'), entry('@scope/util', 'node_modules/@scope/util', 'node_modules/@scope/util'),
             entry('lib', 'node_modules/lib', 'packages/lib'), entry('store-pkg', 'node_modules/store-pkg', STORE), entry('store-pkg', STORE, STORE)]
LAYOUTS = {
    'none': [],
    'base': [{'schemaVersion': 1, 'entries': BASE_ROWS}],
    'base+nested': [{'schemaVersion': 1, 'entries': BASE_ROWS + [entry('evil', EVIL, EVIL), entry('@inner/pkg', INNER, INNER),
                                                                 entry('dep', STORE + '/node_modules/dep', STORE + '/node_modules/dep'),
                                                                 entry('x', 'packages/lib/node_modules/x', 'packages/lib/node_modules/x')]}],
}
PATHS = {
    'node_modules/left-pad/index.js': 'ordinary', 'node_modules/left-pad/dist/index.d.ts': 'ordinary',
    'node_modules/@scope/util/index.js': 'ordinary', 'node_modules/lib/dist/index.d.ts': 'ordinary',
    STORE + '/index.js': 'ordinary-store', 'node_modules/store-pkg/lib/x.js': 'ordinary',
    'packages/lib/src/index.ts': 'first-party', 'src/a.ts': 'first-party',
    EVIL + '/index.js': 'nested', EVIL + '/package.json': 'nested', INNER + '/index.js': 'nested',
    STORE + '/node_modules/dep/index.js': 'nested', 'packages/lib/node_modules/x/index.js': 'nested',
    EVIL + '/node_modules/deeper/index.js': 'nested-deeper', 'node_modules/left-pad/node_modules/other/index.js': 'nested-unlisted-sibling',
    'node_modules/.pnpm/store-pkg@1.0.0/node_modules/dep/index.js': 'unlisted-store-sibling',
    'node_modules/left-pad/node_modules': 'nested-boundary-as-file',
    'node_modules/left-pad/node_modules-like/index.js': 'lookalike', 'node_modules/left-pad/Node_modules/x/index.js': 'lookalike',
    'node_modules/left-pad/my_node_modules/index.js': 'lookalike', 'node_modules/left-pad/node_modules.bak/index.js': 'lookalike',
    EVIL + '/.git/HEAD': 'vcs', 'node_modules/left-pad/.hg/x': 'vcs', STORE + '/.svn/entries': 'vcs', '.git/HEAD': 'vcs',
    'node_modules/unlisted/index.js': 'unlisted', 'target/debug/app.d': 'cargo',
}
rows = []
for p, kind in sorted(PATHS.items()):
    inv = [p] + (['Cargo.toml'] if p.startswith('target/') else [])
    r = {'path': p, 'kind': kind, 'discovery': DD.classify_path(p, DD.cargo_roots_from_markers(inv))}
    for name, layouts in LAYOUTS.items():
        r['fault:' + name] = p in M.snapshot_pruned_tree_faults([{'path': x} for x in inv], layouts)
    rows.append(r)
out = {'variant': variant, 'modelSha256': hashlib.sha256((tree / MODEL).read_bytes()).hexdigest(),
       'loadedModelFile': str(Path(M.__file__).resolve()), 'rows': rows}
out_path.write_text(json.dumps(out, indent=1) + '\n')
print(json.dumps(out, indent=1)[:12000])
