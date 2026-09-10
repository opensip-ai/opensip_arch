"""Post-reset author (Claude) case additions for native-cases.v2.json (round-trips with indent=1, ensure_ascii=True).
MUST-3 (shared discovery rule, installed dependencies, legal `target` directories, real Cargo target, typed cap, `.`
sentinel), SHOULD-4 regression (confidence floor precedes the former one-rung shortcut). Expectations hand-authored."""
import json
from pathlib import Path
P = Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/native/native-cases.v2.json')
raw = P.read_bytes(); doc = json.loads(raw)
assert (json.dumps(doc, indent=1, ensure_ascii=True) + '\n').encode() == raw
H = lambda ch: ch * 64
fx = doc['fixtures']
fx['markersInstalledMonorepo'] = {
    'Cargo.toml': {'sha256': H('a'), 'isCargoWorkspace': True},
    'crates/core/Cargo.toml': {'sha256': H('d'), 'isCargoWorkspace': False},
    'package.json': {'sha256': H('b')},
    'tsconfig.json': {'sha256': H('c')},
    'packages/web/tsconfig.json': {'sha256': H('e')},
    'packages/target/package.json': {'sha256': H('3')},
    'node_modules/left-pad/package.json': {'sha256': H('1')},
    'node_modules/lodash/package.json': {'sha256': H('1')},
    'node_modules/rusty/Cargo.toml': {'sha256': H('4'), 'isCargoWorkspace': False},
    'packages/web/node_modules/x/package.json': {'sha256': H('5')},
    'target/debug/build/x/package.json': {'sha256': H('2')},
    'crates/core/target/Cargo.toml': {'sha256': H('6'), 'isCargoWorkspace': False},
}
doc['feedbackMap']['PR-MUST-3'] = 'post-reset review MUST-3: one shared discovery rule (../discovery-defaults.py); dependency/VCS/Cargo-output trees pruned by exact segment; installed manifests are never units; typed cap; `.` sentinel normalization shared with security'
doc['feedbackMap']['PR-SHOULD-4'] = 'post-reset review SHOULD-4: sufficiency v2 evaluates the confidence floor for every requirement; no one-rung existential shortcut'
for c in doc['cases']:
    if c['id'] == 'units-nested-monorepo-deepest-within-language-and-workspace-folding':
        c['expect']['$s.scopeDescriptor.excludedPathPrefixes'] = ['.git', 'crates/core/target', 'node_modules', 'packages/cli/.git', 'packages/cli/node_modules',
                                                                  'packages/web/.git', 'packages/web/node_modules', 'target', 'vendor']
        c['note'] = 'Conventional excluded prefixes follow the shared rule: .git/node_modules under every unit root, `target` only under Cargo roots (the workspace root and its folded member crates/core). The tsjs units no longer list a `target` prefix.'
    if c['id'] == 'too-many-units-rejected':
        c['feedback'].append('PR-MUST-3')
        c['steps'].append({'fn': 'discover_units', 'args': {'markers': '$fixtures.markersManyFirstParty'}, 'bind': 'big'})
        c['expect'].update({'$big.units': [], '$big.refused.detail': 'native.too-many-units', '$big.refused.d9.code': 'REQUEST.UNSATISFIABLE',
                            '$big.refused.d9.exitCode': 2, '$big.refused.unitCount': 4200, '$big.refused.limit': 4096})
        c['note'] = '4200 first-party package directories (generated fixture markersManyFirstParty) are a typed REQUEST.UNSATISFIABLE refusal with no truncation and no exception.'
fx['markersManyFirstParty'] = {'pkg%04d/package.json' % i: {'sha256': H('1')} for i in range(4200)}
fx['markersManyInstalled'] = dict({'package.json': {'sha256': H('b')}}, **{'node_modules/dep%04d/package.json' % i: {'sha256': H('1')} for i in range(4200)})
doc['cases'].extend([
    {'id': 'units-installed-dependencies-are-pruned-by-segment-and-legal-target-directories-are-program-members',
     'feedback': ['R1', 'R6', 'PR-MUST-3'], 'kind': 'positive',
     'steps': [
         {'fn': 'discover_units', 'args': {'markers': '$fixtures.markersInstalledMonorepo'}, 'bind': 'u'},
         {'fn': 'assign_membership', 'args': {'units': '$u.units', 'files': [
             'index.ts', 'packages/target/index.ts', 'src/target/x.ts', 'packages/web/src/app.ts', 'target/debug/x.rs',
             'crates/core/target/o.rs', 'crates/core/src/target/m.rs', 'node_modules/left-pad/index.js', 'packages/web/node_modules/x/index.js', '.git/hooks/x.js']}, 'bind': 'm'},
         {'fn': 'unit_scope_descriptor', 'args': {'units': '$u.units', 'ignore_paths': [], 'pruned_trees': '$u.prunedTrees'}, 'bind': 's'}],
     'expect': {
         '$u.refused': None,
         '$u.units.0.rootPath': '', '$u.units.0.languageFamily': 'rust', '$u.units.0.memberPackageRoots': ['crates/core'],
         '$u.units.1.rootPath': '', '$u.units.1.languageFamily': 'tsjs',
         '$u.units.2.rootPath': 'packages/target', '$u.units.2.languageMode': 'js-synthesized',
         '$u.units.3.rootPath': 'packages/web', '$u.units.length': 4,
         '$u.prunedTrees': [{'path': 'crates/core/target', 'reason': 'cargo-build-output', 'markerCount': 1},
                            {'path': 'node_modules', 'reason': 'dependency-tree', 'markerCount': 3},
                            {'path': 'packages/web/node_modules', 'reason': 'dependency-tree', 'markerCount': 1},
                            {'path': 'target', 'reason': 'cargo-build-output', 'markerCount': 1}],
         '$m.rows.0.path': '.git/hooks/x.js', '$m.rows.0.reason': 'host-ignore-convention',
         '$m.rows.1.path': 'crates/core/src/target/m.rs', '$m.rows.1.membership': 'program-member', '$m.rows.1.unitOrdinal': 0,
         '$m.rows.2.path': 'crates/core/target/o.rs', '$m.rows.2.reason': 'host-ignore-convention',
         '$m.rows.3.path': 'index.ts', '$m.rows.3.unitOrdinal': 1,
         '$m.rows.4.path': 'node_modules/left-pad/index.js', '$m.rows.4.reason': 'host-ignore-convention',
         '$m.rows.5.path': 'packages/target/index.ts', '$m.rows.5.membership': 'program-member', '$m.rows.5.unitOrdinal': 2,
         '$m.rows.6.path': 'packages/web/node_modules/x/index.js', '$m.rows.6.reason': 'host-ignore-convention',
         '$m.rows.7.path': 'packages/web/src/app.ts', '$m.rows.7.unitOrdinal': 3,
         '$m.rows.8.path': 'src/target/x.ts', '$m.rows.8.membership': 'program-member', '$m.rows.8.unitOrdinal': 1,
         '$m.rows.9.path': 'target/debug/x.rs', '$m.rows.9.reason': 'host-ignore-convention',
         '$m.erasedFiles': [],
         '$s.scopeDescriptor.workspaceRoots': ['.', 'packages/target', 'packages/web'],
         '$s.scopeDescriptor.excludedPathPrefixes': ['.git', 'crates/core/target', 'node_modules', 'packages/target/.git', 'packages/target/node_modules',
                                                     'packages/web/.git', 'packages/web/node_modules', 'target']},
     'note': 'node_modules/*/package.json and node_modules/rusty/Cargo.toml never become units; a Cargo.toml inside node_modules does not create a Cargo root. `target` is pruned only directly under a Cargo root (the workspace root and crates/core); packages/target and src/target are ordinary source. Same rule as security discovery (../discovery-defaults.py).'},
    {'id': 'units-4200-installed-package-manifests-are-one-pruned-tree-not-a-cap-refusal',
     'feedback': ['R6', 'PR-MUST-3'], 'kind': 'positive',
     'steps': [{'fn': 'discover_units', 'args': {'markers': '$fixtures.markersManyInstalled'}, 'bind': 'u'}],
     'expect': {'$u.refused': None, '$u.units.length': 1, '$u.units.0.rootPath': '', '$u.units.0.languageMode': 'js-synthesized',
                '$u.prunedTrees': [{'path': 'node_modules', 'reason': 'dependency-tree', 'markerCount': 4200}]}},
    {'id': 'units-explicit-root-dot-is-the-project-root-under-the-shared-sentinel-normalization',
     'feedback': ['R6', 'PR-MUST-3'], 'kind': 'positive',
     'steps': [{'fn': 'discover_units', 'args': {'markers': '$fixtures.markersInstalledMonorepo', 'explicit_workspace_roots': ['.']}, 'bind': 'u'},
               {'fn': 'discover_units', 'args': {'markers': '$fixtures.markersInstalledMonorepo', 'explicit_workspace_roots': ['packages/web/']}, 'bind': 'w'},
               {'fn': 'discover_units', 'args': {'markers': '$fixtures.markersInstalledMonorepo', 'explicit_workspace_roots': ['packages/./web']}, 'bind': 'g'},
               {'fn': 'discover_units', 'args': {'markers': '$fixtures.markersInstalledMonorepo', 'explicit_workspace_roots': ['node_modules/left-pad']}, 'bind': 'n'}],
     'expect': {'$u.refused': None, '$u.units.length': 2, '$u.units.0.rootPath': '', '$u.units.0.provenance': 'EXPLICIT', '$u.units.1.rootPath': '',
                '$w.units.0.rootPath': 'packages/web', '$w.units.length': 1,
                '$g.refused.detail': 'native.explicit-root-grammar', '$g.refused.d9.code': 'CONFIG.INVALID',
                '$n.refused.detail': 'native.explicit-root-without-marker', '$n.refused.roots': ['node_modules/left-pad'], '$n.refused.d9.code': 'CONFIG.INVALID'},
     'note': 'Config2 `workspaceRoots: ["."]` means the admitted project root in both instruments (security ACCEPT with the root unit; native EXPLICIT root units). An explicit root inside a pruned dependency tree has no first-party marker and refuses typed, as security refuses JOIN_INSIDE_PRUNED_TREE.'},
    {'id': 'sufficiency-v2-confidence-floor-precedes-one-rung-existential-shortcut',
     'feedback': ['F8', 'F12', 'PR-SHOULD-4'], 'kind': 'negative',
     'steps': [{'fn': 'sufficiency_v2', 'args': {'req': {'relation': 'clones', 'minResolution': 'normalized-body-hash', 'completeness': 'partial-ok', 'quantifier': 'existential', 'minConfidenceMillionths': 900000},
                                                'view': {'clones': {'resolution': 'normalized-body-hash', 'coverage': 'complete', 'confidenceMillionths': 100000}, 'declares': {'resolution': 'syntactic', 'coverage': 'complete'}}}, 'bind': 'v2'},
               {'fn': 'sufficiency_v1', 'args': {'req': {'relation': 'clones', 'minResolution': 'normalized-body-hash', 'completeness': 'partial-ok', 'quantifier': 'existential', 'minConfidenceMillionths': 900000},
                                                'view': {'clones': {'resolution': 'normalized-body-hash', 'coverage': 'complete', 'confidenceMillionths': 100000}, 'declares': {'resolution': 'syntactic', 'coverage': 'complete'}}}, 'bind': 'v1'},
               {'fn': 'sufficiency_v2', 'args': {'req': {'relation': 'clones', 'minResolution': 'normalized-body-hash', 'completeness': 'partial-ok', 'quantifier': 'existential', 'minConfidenceMillionths': 900000},
                                                'view': {'clones': {'resolution': 'normalized-body-hash', 'coverage': 'complete', 'confidenceMillionths': 1000000}, 'declares': {'resolution': 'syntactic', 'coverage': 'complete'}}}, 'bind': 'ok'}],
     'expect': {'$v2.satisfied': False, '$v2.deficiency': 'confidence-floor-unmet', '$v2.causes.0': 'confidence-floor-unmet',
                '$v1.satisfied': False, '$v1.deficiency': 'confidence-floor-unmet', '$ok.satisfied': True},
     'note': 'A one-rung relation (clones) under existential/partial-ok with confidence 100000 below floor 900000 is confidence-floor-unmet in v2 exactly as in the retained v1 oracle; the earlier v2 shortcut returned satisfied before step 3.'},
])
P.write_bytes((json.dumps(doc, indent=1, ensure_ascii=True) + '\n').encode())
print('cases', len(doc['cases']))
