"""v9 probe 08 - body-language-version bound, version sensitivity, mixed-edition Rust.

Independently measures Codex's counterexample number rather than repeating it: the raw canonical
bytes of a schema-admitted 21-entry Rust edition map, against the inherited u8 (<=255) component
bound. Then checks the FINAL design's fixed-width projection under the same and larger inputs,
tests that compiler/dialect changes actually move the body identity, and exercises mixed-edition
ownership including the same physical file under two explicitly selected target editions.

Trusted synthetic producer observations. No Cargo, compiler, build script or repository runs.
"""
import copy, hashlib, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import harness

ns = harness.load()
M, C, N = ns['M'], ns['C'], ns['N']
UID, unit = ns['UID'], ns['unit']
out = {'probe': 'p08_body_version_and_editions',
       'standing': 'independent reviewer probe; trusted synthetic producer observations; qualifies no enumerator, Cargo or compiler'}

# ---------- 1. The inherited bound, measured ----------
LARGE = {'fixture-root': 2021, **{'ordinary_workspace_crate_%d' % i: 2021 for i in range(20)}}
raw_map = C.canonical(LARGE)
out['inheritedComponentBound'] = {
    'entries': len(LARGE),
    'rawCanonicalEditionMapBytes': len(raw_map),
    'inheritedU8ComponentMaximum': 255,
    'rawMapWouldExceedInheritedBound': len(raw_map) > 255,
    'note': 'This is why a per-crate map cannot BE the languageVersion component.',
}

# ---------- 2. The final projection is fixed width for small AND large admitted inputs ----------
def clone_run(language='rust', source_path=None, workspace=None):
    return ns['build'](has_match=True, relation='clones', universe_language=language,
                       source_path=source_path, workspace=workspace)

def frame_of(r, o, b):
    fkey = next(k for k, (d, v) in o.items() if d == 'fact')
    payload = json.loads(b[o[fkey][1]['payloadDigest']].decode())
    frame = b[payload['bodyIdentity'].split(':', 1)[1]]
    p = 0; comps = []
    for _ in range(5):
        n = frame[p]; p += 1; comps.append(frame[p:p + n]); p += n
    return payload, comps, frame

def measure(label, **kw):
    r, o, b = clone_run(**kw)
    payload, comps, frame = frame_of(r, o, b)
    try:
        rid = M.close_run(r, o, b)
        store = M.EvidenceStore(); ex = 'exec1_' + 'c' * 32
        st = {'prepared': store.prepare(r, o, b, ex, ns['replay']), 'commit': store.commit(ex)}
        cl = {'admitted': True, 'runId': rid}
    except Exception as e:
        cl = {'admitted': False, 'cause': str(e)}; st = None
    return {'case': label, 'bodyIdentity': payload['bodyIdentity'],
            'componentLengths': [len(c) for c in comps],
            'languageVersionBytes': len(comps[4]),
            'allComponentsWithinU8': all(len(c) <= 255 for c in comps),
            'closure': cl, 'store': st}

WS_LARGE = {'edition': LARGE, 'enumeration': 'complete',
            'units': [unit('Cargo.toml', 'lib', 'fixture-root', 'fixture-root')],
            'selectedUnitIds': [UID('Cargo.toml', 'lib', 'fixture-root')],
            'ownership': [{'path': 'src/lib.rs', 'unitId': UID('Cargo.toml', 'lib', 'fixture-root')}]}
small = measure('rust-default-single-crate-map')
large = measure('rust-21-entry-edition-map', workspace=WS_LARGE)
out['fixedWidthUnderLargeInput'] = {
    'small': small, 'large': large,
    'languageVersionStaysRaw32': small['languageVersionBytes'] == large['languageVersionBytes'] == 32,
    'unrelatedCrateGrowthLeavesBodyIdentityUnchanged': small['bodyIdentity'] == large['bodyIdentity'],
    'note': 'The body identity must NOT depend on unrelated crates; the universe identity may still differ.',
}

# ---------- 3. Version sensitivity: a compiler change must move the identity ----------
import types
def with_mutated_context(mutate):
    """Rebuild a Rust clone Run with the native context toolchain mutated at source."""
    orig = ns['rust_inputs']
    def patched(objects, blobs, add, blob, tree, **kw):
        res = orig(objects, blobs, add, blob, tree, **kw)
        return res
    # simpler: mutate the module-level toolchain constants the context is built from
    return None

def rust_ident(mutator=None):
    """Mutate the admitted native context's toolchain fields via the fixture's own source values."""
    saved = {}
    if mutator:
        saved = mutator()
    try:
        r, o, b = clone_run()
        payload, comps, frame = frame_of(r, o, b)
        ok = True
        try:
            M.close_run(r, o, b)
        except Exception as e:
            ok = str(e)
        return payload['bodyIdentity'], comps[4].hex(), ok
    finally:
        for k, v in (saved or {}).items():
            pass

base_ident, base_lv, base_ok = rust_ident()

# Change the rustc version by editing the fixture's toolchain source constant in the namespace.
src = (harness.FOUND / 'check-identity.py').read_text()
out['versionSensitivity'] = {}
def rebuild_with_source_edit(old, new, label):
    """Re-exec the fixture with one literal changed - the only way to move an input the builder
    hard-codes. This edits the reviewer's in-memory copy only; no shipped file is written."""
    assert src.count(old) >= 1, ('literal not found', old)
    import ast
    edited = src.replace(old, new, 1)
    tree = ast.parse(edited)
    last = next(n for n in tree.body if isinstance(n, ast.FunctionDef)
                and n.name == 'graph_with_import').end_lineno
    ns2 = {'__file__': str(harness.FOUND / 'check-identity.py'), '__name__': 'reviewer_v9_variant'}
    exec(compile('\n'.join(edited.split('\n')[:last]), '<variant>', 'exec'), ns2)
    r, o, b = ns2['build'](has_match=True, relation='clones', universe_language='rust')
    fkey = next(k for k, (d, v) in o.items() if d == 'fact')
    payload = json.loads(b[o[fkey][1]['payloadDigest']].decode())
    frame = b[payload['bodyIdentity'].split(':', 1)[1]]
    p = 0; comps = []
    for _ in range(5):
        n = frame[p]; p += 1; comps.append(frame[p:p + n]); p += n
    try:
        ns2['M'].close_run(r, o, b); cl = 'admitted'
    except Exception as e:
        cl = 'refused:' + str(e)
    return {'label': label, 'bodyIdentity': payload['bodyIdentity'],
            'languageVersionHex': comps[4].hex(), 'closure': cl}

v1 = rebuild_with_source_edit("semanticVersion='1.83.0',protocolMajor=3,platform='macos-aarch64')",
                              "semanticVersion='1.84.0',protocolMajor=3,platform='macos-aarch64')",
                              'rust-toolchain-semantic-version-changed')
out['versionSensitivity'] = {
    'baselineBodyIdentity': base_ident, 'baselineLanguageVersionHex': base_lv,
    'variant': v1,
    'compilerChangeMovesBodyIdentity': v1['bodyIdentity'] != base_ident,
    'compilerChangeMovesLanguageVersionComponent': v1['languageVersionHex'] != base_lv,
}

# ---------- 4. Mixed edition: two targets, two editions, ONE package default ----------
MIXED = {'edition': {'fixture-root': 2021, 'legacy-crate': 2015}, 'enumeration': 'complete',
         'units': [unit('Cargo.toml', 'lib', 'fixture-root', 'fixture-root'),
                   unit('legacy/Cargo.toml', 'lib', 'legacy-crate', 'legacy-crate')],
         'selectedUnitIds': [UID('Cargo.toml', 'lib', 'fixture-root'),
                             UID('legacy/Cargo.toml', 'lib', 'legacy-crate')],
         'ownership': [{'path': 'src/lib.rs', 'unitId': UID('Cargo.toml', 'lib', 'fixture-root')}]}
out['mixedEditionWorkspace'] = measure('mixed-edition-workspace-2021-body', workspace=MIXED)

# same physical path, two TARGETS with explicit target editions, selected one at a time
def shared_path_ws(selected_kind, ed_lib, ed_bin):
    units = [unit('Cargo.toml', 'lib', 'fixture-root', 'fixture-root', ed_lib),
             unit('Cargo.toml', 'bin', 'tool', 'fixture-root', ed_bin)]
    sel = [UID('Cargo.toml', selected_kind, 'fixture-root' if selected_kind == 'lib' else 'tool')]
    return {'edition': {'fixture-root': 2021}, 'enumeration': 'complete', 'units': units,
            'selectedUnitIds': sel,
            'ownership': [{'path': 'src/lib.rs', 'unitId': UID('Cargo.toml', 'lib', 'fixture-root')},
                          {'path': 'src/lib.rs', 'unitId': UID('Cargo.toml', 'bin', 'tool')}]}

sel_lib = measure('same-file-selected-lib-target-edition-2021', workspace=shared_path_ws('lib', 2021, 2015))
sel_bin = measure('same-file-selected-bin-target-edition-2015', workspace=shared_path_ws('bin', 2021, 2015))
out['sameFileTwoSelectedTargetEditions'] = {
    'selectedLib': sel_lib, 'selectedBin': sel_bin,
    'bothCommit': bool(sel_lib['store'] and sel_bin['store']),
    'identitiesDiffer': sel_lib['bodyIdentity'] != sel_bin['bodyIdentity'],
    'packageDefaultsAgreeSoMapAloneCouldNotDistinguish': True,
}

# ---------- 5. Refusals: ambiguity, partial enumeration, unselected, absent ownership ----------
def refusal(label, workspace):
    try:
        r, o, b = clone_run(workspace=workspace)
        payload, comps, frame = frame_of(r, o, b)
        try:
            M.close_run(r, o, b)
            return {'case': label, 'outcome': 'ADMITTED', 'bodyIdentity': payload['bodyIdentity']}
        except Exception as e:
            return {'case': label, 'outcome': 'closure-refused', 'cause': str(e)}
    except Exception as e:
        return {'case': label, 'outcome': 'build-refused', 'cause': str(e), 'exception': type(e).__name__}

both_selected = shared_path_ws('lib', 2021, 2015)
both_selected['selectedUnitIds'] = sorted([UID('Cargo.toml', 'lib', 'fixture-root'),
                                           UID('Cargo.toml', 'bin', 'tool')], key=lambda x: x.encode())
partial = copy.deepcopy(MIXED); partial['enumeration'] = 'partial'
unselected = copy.deepcopy(MIXED); unselected['selectedUnitIds'] = [UID('legacy/Cargo.toml', 'lib', 'legacy-crate')]
noowner = copy.deepcopy(MIXED); noowner['ownership'] = []
out['refusals'] = [
    refusal('two-selected-targets-disagree-on-edition', both_selected),
    refusal('enumeration-partial-hides-possible-conflicting-owner', partial),
    refusal('path-owned-only-by-an-unselected-target', unselected),
    refusal('no-owning-row-for-the-path', noowner),
]

print(json.dumps(out, indent=1))
