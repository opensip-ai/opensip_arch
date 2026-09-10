"""v9 probe 09 - exact dialect refusal causes, and real version sensitivity.

p08 measured two things wrongly (reviewer harness errors, NOT product defects):
  (a) it edited the FIRST 'semanticVersion=1.83.0' literal, which is the rust-dev-llvm closure -
      a field the binding deliberately EXCLUDES - so the body identity correctly did not move;
  (b) its refusal cases stopped at the fixture's own FIXTURE_NO_ADMISSIBLE_PAYLOAD guard, which
      masks the underlying cause, so no intended cause was observed.

Here the reviewer captures the real universe/context/ownership records the fixture builds and
calls the MODEL's body_language_version directly, so every refusal reports its own cause; and
version sensitivity is measured on the fields the binding actually names.
"""
import ast, copy, hashlib, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import harness

ns = harness.load()
M, C, N = ns['M'], ns['C'], ns['N']
UID, unit = ns['UID'], ns['unit']
IDS = json.loads((harness.SUBJECT / 'docs/coop/design-corrections/foundation/identity-schemas.v2.json').read_text())
UROWS = IDS['x-opensip-digest-domains']['domainSets']['native-semantic-universe']
out = {'probe': 'p09_dialect_causes',
       'standing': 'independent reviewer probe; trusted synthetic observations; qualifies no enumerator or compiler',
       'harnessCorrections': [
           'p08 edited the rust-dev-llvm closure semanticVersion (an EXCLUDED field), so its negative version result measured nothing. Reviewer error.',
           'p08 refusals were masked by the fixture FIXTURE_NO_ADMISSIBLE_PAYLOAD guard; the model is called directly here.']}

# ---- capture the real records the builder passes to relation_fixture ----
captured = {}
orig = ns['relation_fixture']
def capture(relation, source_path, source_body, source, universe_record, universe_domain, blob,
            context_record=None, ownership=None):
    captured.update(universe=universe_record, context=context_record, domain=universe_domain,
                    ownership=ownership, path=source_path, body=source_body, blobdigest=source)
    return orig(relation, source_path, source_body, source, universe_record, universe_domain, blob,
                context_record, ownership)
ns['relation_fixture'] = capture
ns['build'](has_match=True, relation='clones', universe_language='rust')
ns['relation_fixture'] = orig
UNI = captured['universe']; CTX = captured['context']
ROW = UROWS['native.semantic-universe.rust.v2']
ANCHOR = {'path': 'src/lib.rs', 'blobDigest': captured['blobdigest'], 'startByte': 0,
          'endByte': len(captured['body'])}
BASE_OWN = captured['ownership']['sourceUnitOwnership']
out['capturedOwnership'] = BASE_OWN

def project(label, universe=None, context=None, ownership=None, anchor=None):
    try:
        rec = M.body_language_version(universe or UNI, context or CTX, ROW,
                                      anchor or ANCHOR,
                                      None if ownership == 'ABSENT' else
                                      {'sourceUnitOwnership': ownership if ownership is not None else BASE_OWN})
        return {'case': label, 'record': rec,
                'raw32': hashlib.sha256(C.canonical(rec)).hexdigest()}
    except Exception as e:
        return {'case': label, 'refused': str(e), 'exception': type(e).__name__}

# ---- positive baseline
base = project('baseline-rust')
out['baseline'] = base

# ---- exact refusal causes
def own(**kw):
    o = copy.deepcopy(BASE_OWN); o.update(kw); return o

two_targets = own(
    units=sorted([unit('Cargo.toml', 'lib', 'fixture-root', 'fixture-root', 2021),
                  unit('Cargo.toml', 'bin', 'tool', 'fixture-root', 2015)], key=lambda u: u['unitId'].encode()),
    selectedUnitIds=sorted([UID('Cargo.toml', 'lib', 'fixture-root'), UID('Cargo.toml', 'bin', 'tool')],
                           key=lambda x: x.encode()),
    ownership=sorted([{'path': 'src/lib.rs', 'unitId': UID('Cargo.toml', 'lib', 'fixture-root')},
                      {'path': 'src/lib.rs', 'unitId': UID('Cargo.toml', 'bin', 'tool')}],
                     key=lambda r: (r['path'].encode(), r['unitId'].encode())))
one_selected = copy.deepcopy(two_targets)
one_selected['selectedUnitIds'] = [UID('Cargo.toml', 'bin', 'tool')]
other_selected = copy.deepcopy(two_targets)
other_selected['selectedUnitIds'] = [UID('Cargo.toml', 'lib', 'fixture-root')]

out['dialectCauses'] = [
    project('ownership-absent', ownership='ABSENT'),
    project('enumeration-partial', ownership=own(enumeration='partial')),
    project('no-owning-row-for-path', ownership=own(ownership=[])),
    project('owned-only-by-unselected-target', ownership=own(selectedUnitIds=['sha256:' + 'e' * 64])),
    project('two-selected-targets-disagree', ownership=two_targets),
    project('POSITIVE-select-bin-target-2015', ownership=one_selected),
    project('POSITIVE-select-lib-target-2021', ownership=other_selected),
    project('empty-edition-map', universe=dict(UNI, edition={})),
    project('unknown-suffix-not-applicable-to-rust', anchor=dict(ANCHOR, path='src/lib.unknownext')),
]
out['partialEnumerationRefusesBeforeReadingRows'] = {
    'partialWithAConflictingOwnerPresent':
        project('partial-with-conflicting-owner', ownership=own(enumeration='partial', **{
            'units': two_targets['units'], 'selectedUnitIds': two_targets['selectedUnitIds'],
            'ownership': two_targets['ownership']})),
    'note': 'partial must refuse at enumeration, never silently select a dialect',
}
out['selectionChangesDialectNotByPath'] = {
    'binSelectedEdition': out['dialectCauses'][5].get('record', {}).get('dialect'),
    'libSelectedEdition': out['dialectCauses'][6].get('record', {}).get('dialect'),
    'differentRaw32': out['dialectCauses'][5].get('raw32') != out['dialectCauses'][6].get('raw32'),
    'noPathCrateOrUnitIdInRecord': all(
        k not in (out['dialectCauses'][6].get('record') or {})
        for k in ('markerPath', 'crateName', 'unitId', 'selectedUnitIds', 'path')),
}

# ---- TypeScript suffix causes
tscap = {}
orig2 = ns['relation_fixture']
def capture2(relation, source_path, source_body, source, universe_record, universe_domain, blob,
             context_record=None, ownership=None):
    tscap.update(universe=universe_record, context=context_record, body=source_body, blobdigest=source)
    return orig2(relation, source_path, source_body, source, universe_record, universe_domain, blob,
                 context_record, ownership)
ns['relation_fixture'] = capture2
ns['build'](has_match=True, relation='clones', universe_language='typescript', source_path='a.ts')
ns['relation_fixture'] = orig2
TSROW = UROWS['native.semantic-universe.typescript.v2']

def ts_project(path):
    a = {'path': path, 'blobDigest': tscap['blobdigest'], 'startByte': 0, 'endByte': len(tscap['body'])}
    try:
        rec = M.body_language_version(tscap['universe'], tscap['context'], TSROW, a, None)
        return {'path': path, 'variant': rec['dialect'], 'languageId': rec['languageId'],
                'raw32': hashlib.sha256(C.canonical(rec)).hexdigest()}
    except Exception as e:
        return {'path': path, 'refused': str(e)}
out['typescriptVariants'] = [ts_project(p) for p in
                             ['a.ts', 'a.tsx', 'a.d.ts', 'a.mts', 'a.cts', 'a.js', 'a.jsx', 'a.mjs',
                              'a.cjs', 'a.vue', 'a', 'a.TS']]

# ---- REAL version sensitivity: mutate exactly the fields the binding names
out['versionSensitivity'] = []
for field, newval in [('rustcVersion', '1.84.0'), ('rustCommitHash', 'c' * 40)]:
    ctx2 = copy.deepcopy(CTX); ctx2['toolchain'][field] = newval
    r = project('rust-context-' + field + '-changed', context=ctx2)
    r['movesRaw32'] = r.get('raw32') != base.get('raw32')
    out['versionSensitivity'].append(r)
for field, newval in [('compilerName', 'not-rustc')]:
    out['versionSensitivity'].append({'case': 'rust-compilerName-is-a-declared-const',
                                      'constInBinding': ROW['languageVersionBinding']['fields']['compilerName']})
# excluded fields must NOT move it
for field, newval in [('targetTriple', 'x86_64-unknown-linux-gnu'), ('cargoVersion', '9.9.9'),
                      ('sysrootDigest', 'd' * 64)]:
    ctx2 = copy.deepcopy(CTX); ctx2['toolchain'][field] = newval
    r = project('EXCLUDED-' + field + '-changed', context=ctx2)
    r['movesRaw32'] = r.get('raw32') != base.get('raw32')
    r['expectation'] = 'must NOT move (declared exclusion)'
    out['versionSensitivity'].append(r)

# ---- the 723 vs 711 measurement, stated exactly
LARGE = {'fixture-root': 2021, **{'ordinary_workspace_crate_%d' % i: 2021 for i in range(20)}}
out['editionMapMeasurement'] = {
    'entries': len(LARGE),
    'bareMapCanonicalBytes': len(C.canonical(LARGE)),
    'wrappedAsEditionMemberCanonicalBytes': len(C.canonical({'edition': LARGE})),
    'inheritedU8Max': 255,
    'note': "Codex reported 723 for this vector; the reviewer measures 711 for the bare map and "
            "723 for it wrapped as an 'edition' member. Both exceed the inherited u8 bound; the "
            "difference is only which value is being canonicalised.",
}

print(json.dumps(out, indent=1, default=str))
