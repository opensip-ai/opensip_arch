"""v9 probe 10 - unit identity recipe, body-identity stability, and the Coverage prerequisite.

Three independent questions:

A. UNIT IDENTITY. Is unitId a DERIVED identity a consumer can rebuild from the published row
   (not an opaque digest)? Does it admit ordinary and `#` marker paths, and stay fixed width at
   the declared field-size bounds? The reviewer recomputes H from the published projection with
   its own code path and compares.

B. STABILITY. Does bodyIdentity stay put when compiler/dialect/source/level inputs are unchanged
   but OWNERSHIP and UNIVERSE identity change? (The coauthor withdrew an assumption that it must
   change; the reviewer measures it rather than accepting either claim.)

C. COVERAGE PREREQUISITE. Can a Run with partial/absent ownership and ZERO clone facts still
   commit a COMPLETE Coverage claim and a determinate seal? Does the honest indeterminate control
   still commit? Is an honest EMPTY finding under a healthy universe still allowed (the rule must
   not over-refuse)? Driven through the owning Run, not by a producer choosing a flag.
"""
import copy, hashlib, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import harness

ns = harness.load()
M, C, N = ns['M'], ns['C'], ns['N']
UID, unit = ns['UID'], ns['unit']
out = {'probe': 'p10_unit_identity_and_coverage',
       'standing': 'independent reviewer probe; synthetic reference store/TCB; not durability or production evidence'}

# ================= A. unit identity =================
def reviewer_unit_id(marker, kind, name):
    """Reviewer's own rebuild of H(native.compilation-unit.v1, UnitIdentityV1)."""
    projection = {'schemaVersion': 1, 'markerPath': marker, 'targetKind': kind, 'targetName': name}
    return 'sha256:' + C.identity('native.compilation-unit.v1', projection)

cases = []
for marker, kind, name, label in [
    ('Cargo.toml', 'lib', 'fixture-root', 'ordinary'),
    ('crates/c#interop/Cargo.toml', 'lib', 'hash-dir', 'marker path containing #'),
    ('crates/c#interop/sub#two/Cargo.toml', 'bin', 'tool', 'two # segments'),
    ('a' * 4096, 'lib', 'x', 'markerPath at declared 4096 maximum'),
    ('Cargo.toml', 'bench', 'n' * 256, 'targetName at declared 256 maximum'),
    ('crates/c#interop/Cargo.toml', 'lib', 'hash-dir-2', 'sibling differing only after #'),
]:
    try:
        model = N.source_unit_id({'markerPath': marker, 'targetKind': kind, 'targetName': name})
        mine = reviewer_unit_id(marker, kind, name)
        cases.append({'label': label, 'markerPathLen': len(marker), 'targetNameLen': len(name),
                      'modelId': model, 'reviewerId': mine, 'agree': model == mine,
                      'identityLength': len(model), 'fixedWidth': len(model) == len('sha256:') + 64})
    except Exception as e:
        cases.append({'label': label, 'refused': str(e), 'exception': type(e).__name__})
ids = [c['modelId'] for c in cases if 'modelId' in c]
out['unitIdentity'] = {
    'cases': cases,
    'allAgreeWithIndependentRebuild': all(c.get('agree') for c in cases if 'modelId' in c),
    'allFixedWidth': all(c.get('fixedWidth') for c in cases if 'modelId' in c),
    'hashMarkerPathsAdmitted': all(c.get('modelId') for c in cases if '#' in c['label']),
    'distinctIdentities': len(set(ids)) == len(ids),
    'noOpaqueDigest': 'preimage record, domain, codec and selector are published; reviewer rebuilt each id independently',
}
# over-bound must refuse
for marker, name, label in [('a' * 4097, 'x', 'markerPath one over maximum'),
                            ('Cargo.toml', 'n' * 257, 'targetName one over maximum')]:
    try:
        N.source_unit_id({'markerPath': marker, 'targetKind': 'lib', 'targetName': name})
        out['unitIdentity'].setdefault('boundEnforcement', []).append({'label': label, 'outcome': 'ADMITTED'})
    except Exception as e:
        out['unitIdentity'].setdefault('boundEnforcement', []).append(
            {'label': label, 'outcome': 'refused', 'cause': str(e)[:140]})

# ================= B. body identity stability =================
def clone_ident(workspace=None, source_path=None, language='rust'):
    r, o, b = ns['build'](has_match=True, relation='clones', universe_language=language,
                          source_path=source_path, workspace=workspace)
    fkey = next(k for k, (d, v) in o.items() if d == 'fact')
    fact = o[fkey][1]
    payload = json.loads(b[fact['payloadDigest']].decode())
    try:
        M.close_run(r, o, b); adm = True
    except Exception as e:
        adm = str(e)
    return {'bodyIdentity': payload['bodyIdentity'], 'sourceUniverse': fact['sourceUniverse'],
            'normalisationVersion': payload['normalisationVersion'], 'admitted': adm}

base = clone_ident()
# same effective edition for the body, but a LARGER units table and an extra unrelated crate:
# ownership record and therefore sourceUniverse must change; body identity must not.
ws_more = {'edition': {'fixture-root': 2021, 'unrelated-crate': 2015}, 'enumeration': 'complete',
           'units': sorted([unit('Cargo.toml', 'lib', 'fixture-root', 'fixture-root'),
                            unit('other/Cargo.toml', 'lib', 'unrelated-crate', 'unrelated-crate')],
                           key=lambda u: u['unitId'].encode()),
           'selectedUnitIds': [UID('Cargo.toml', 'lib', 'fixture-root')],
           'ownership': [{'path': 'src/lib.rs', 'unitId': UID('Cargo.toml', 'lib', 'fixture-root')}]}
more = clone_ident(workspace=ws_more)
# a change to the SELECTED effective edition must move it
ws_ed = copy.deepcopy(ws_more); ws_ed['edition']['fixture-root'] = 2015
moved = clone_ident(workspace=ws_ed)
out['bodyIdentityStability'] = {
    'baseline': base, 'ownershipAndUniverseChanged': more, 'selectedEditionChanged': moved,
    'universeIdentityChanged': base['sourceUniverse'] != more['sourceUniverse'],
    'bodyIdentityUnchangedDespiteOwnershipChange': base['bodyIdentity'] == more['bodyIdentity'],
    'bodyIdentityMovesWhenSelectedDialectMoves': moved['bodyIdentity'] != base['bodyIdentity'],
}

# ================= C. Coverage dialect prerequisite =================
def coverage_case(label, workspace, resolved, has_match=False):
    try:
        r, o, b = ns['build'](has_match=has_match, relation='clones', universe_language='rust',
                              workspace=workspace, resolved=resolved)
    except Exception as e:
        return {'case': label, 'stage': 'build', 'outcome': 'build-refused', 'cause': str(e)}
    ckey = next(k for k, (d, v) in o.items() if d == 'coverage')
    cov = json.loads(b[o[ckey][1]['payloadDigest']].decode())
    view = o[o[r['evidenceId']][1]['viewIds'][0]][1]
    seal = o[r['evaluationSealId']][1]
    rec = {'case': label, 'coverageClaim': cov['entry']['coverage'],
           'deficiency': cov['entry']['deficiency'], 'factCount': len(view['facts']),
           'sealVerdict': seal['verdict']}
    try:
        rid = M.close_run(r, o, b)
        store = M.EvidenceStore(); ex = 'exec1_' + 'c' * 32
        rec['closure'] = {'admitted': True, 'runId': rid}
        try:
            rec['store'] = {'prepared': store.prepare(r, o, b, ex, ns['replay']),
                            'commit': store.commit(ex)}
        except Exception as e:
            rec['store'] = {'refused': str(e)}
    except Exception as e:
        rec['closure'] = {'admitted': False, 'cause': str(e), 'exception': type(e).__name__}
    return rec

healthy = None  # default workspace
partial_ws = {'edition': {'fixture-root': 2021}, 'enumeration': 'partial',
              'units': [unit('Cargo.toml', 'lib', 'fixture-root', 'fixture-root')],
              'selectedUnitIds': [UID('Cargo.toml', 'lib', 'fixture-root')],
              'ownership': [{'path': 'src/lib.rs', 'unitId': UID('Cargo.toml', 'lib', 'fixture-root')}]}
# a universe where the path is simply not owned: per-body refusal, universe still healthy
unowned_ws = {'edition': {'fixture-root': 2021}, 'enumeration': 'complete',
              'units': [unit('Cargo.toml', 'lib', 'fixture-root', 'fixture-root')],
              'selectedUnitIds': [UID('Cargo.toml', 'lib', 'fixture-root')],
              'ownership': [{'path': 'src/other.rs', 'unitId': UID('Cargo.toml', 'lib', 'fixture-root')}]}

out['coveragePrerequisite'] = [
    coverage_case('CONTRADICTORY-partial-ownership-empty-view-claims-complete', partial_ws, True),
    coverage_case('HONEST-partial-ownership-empty-view-claims-unknown', partial_ws, False),
    coverage_case('POSITIVE-healthy-universe-complete-with-a-fact', healthy, True, has_match=True),
    coverage_case('POSITIVE-healthy-universe-honest-empty-view-complete', unowned_ws, True),
    coverage_case('HONEST-healthy-universe-unknown', healthy, False),
]

print(json.dumps(out, indent=1, default=str))
