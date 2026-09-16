"""V07 — RRS-A1 assessed independently against frozen31 normative owners, with a SCOPED unit probe.

SCOPE, stated exactly: this is a unit-level probe of the author's own `path_owner_universes` over a
minimal hand-built view object. It is NOT a full admitted Run, NOT a reminted graph, and NOT an
executed end-to-end bypass. Root states no full-Run counterexample exists for this asymmetric case
and I construct none; I test only the selector function's stated input-to-output behaviour and
compare it with what the frozen31 enumeration owner says is retained.
"""
import importlib.util, json, os, sys, types

RR = '/tmp/opensip-design-corrections/root-repair-selection-author-review.v1/captured'
SNAP = '/tmp/opensip-design-corrections/candidate-subject.v31'
OUT = '/tmp/opensip-design-corrections/claude-glob-repair-bounded-review.v1/receipts'
MOD = os.path.join(RR, 'docs/coop/design-corrections/workflows/repair_closed_world_selection.v1.py')
R = {'probeScope': (
    'unit-level call of path_owner_universes on a hand-built view; not a full Run, not a reminted '
    'graph, not an executed bypass')}

# The captured tree holds only the 4 author files, but the module loads its sibling
# foundation/relation-payload-schemas.v2.json registry at import time. My first run died on that.
# Build a disposable overlay in MY runtime: frozen31 design-corrections plus the captured files.
import hashlib, shutil
KIT = '/tmp/opensip-design-corrections/claude-glob-repair-bounded-review.v1/disposable/repairkit'
if os.path.isdir(KIT):
    shutil.rmtree(KIT)
man = {f['path']: f for f in json.load(open(
    '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/'
    'candidate-subject.v31.json'))['files']}
copied = verified = 0
for rel in man:
    if not rel.startswith('docs/coop/design-corrections/') or '/reviews/' in rel:
        continue
    s = os.path.join(SNAP, rel)
    if not os.path.isfile(s):
        continue
    d = os.path.join(KIT, rel)
    os.makedirs(os.path.dirname(d), exist_ok=True)
    shutil.copy2(s, d)
    copied += 1
    if hashlib.sha256(open(d, 'rb').read()).hexdigest() == man[rel]['sha256']:
        verified += 1
R['overlayFrozenFiles'] = copied
R['overlayFrozenVerified'] = verified
assert copied == verified, 'overlay base is not byte-equal to frozen31'
cap = 0
for dp, dn, fn in os.walk(RR):
    for n in fn:
        s = os.path.join(dp, n)
        rel = os.path.relpath(s, RR)
        d = os.path.join(KIT, rel)
        os.makedirs(os.path.dirname(d), exist_ok=True)
        shutil.copy2(s, d)
        cap += 1
R['overlayCapturedFiles'] = cap
print('disposable overlay: %d frozen31 files (all byte-verified) + %d captured author files'
      % (copied, cap))
MOD = os.path.join(KIT, 'docs/coop/design-corrections/workflows/repair_closed_world_selection.v1.py')
spec = importlib.util.spec_from_file_location('repairsel', MOD)
M = importlib.util.module_from_spec(spec)
sys.modules['repairsel'] = M
spec.loader.exec_module(M)
R['sourcePathRelations'] = sorted(M.SOURCE_PATH_RELATIONS)
print('relations the selector treats as path-owning:', sorted(M.SOURCE_PATH_RELATIONS))


class MiniView:
    """Only the two members path_owner_universes touches: snapshot_id and subject_scopes()."""
    def __init__(self, scopes, snapshot_id='snap1'):
        self.snapshot_id = snapshot_id
        self._scopes = scopes

    def subject_scopes(self):
        return self._scopes


EDIT = 'src/lib/util.ts'

# Universe A: a file-kind source-path scope that DOES contain the edited path.
# Universe B: the same path lies in B's retained SYMBOL extent, but B's only retained relation
# scope here is a symbol-kind relation, so no source-path scope of B names the path.
symbol_rel = None
for name, row in M._REGISTRY['relations'].items():
    if row.get('subjectKind') and row['subjectKind'] != 'source-path':
        symbol_rel = name
        break
R['aNonSourcePathRelationUsed'] = symbol_rel
file_rel = sorted(M.SOURCE_PATH_RELATIONS)[0]
scopes = {
    'scope2:A': {'relation': file_rel, 'resolution': 'enumerated', 'snapshotId': 'snap1',
                 'sourceUniverse': 'universeA', 'subjects': [EDIT, 'src/other.ts']},
    'scope2:B': {'relation': symbol_rel, 'resolution': 'enumerated', 'snapshotId': 'snap1',
                 'sourceUniverse': 'universeB', 'subjects': ['symbol:src/lib/util.ts::helper']},
}
view = MiniView(scopes)
found, unowned = M.path_owner_universes(view, [EDIT])
R['asymmetricCase'] = {
    'editedPath': EDIT,
    'universeAHasSourcePathScopeContainingIt': True,
    'universeBHasItOnlyInASymbolKindScope': True,
    'selectorReturnedUniverses': sorted(found),
    'selectorReportedUnowned': unowned,
    'universeBOmitted': 'universeB' not in found}
print('\n--- asymmetric unit case ---')
print('edited path           :', EDIT)
print('selector returns      :', sorted(found))
print('unowned paths         :', unowned)
print('universeB omitted     :', R['asymmetricCase']['universeBOmitted'])

# Control: if universe B DOES have a source-path scope naming the path, it is returned.
scopes2 = dict(scopes)
scopes2['scope2:B2'] = {'relation': file_rel, 'resolution': 'enumerated', 'snapshotId': 'snap1',
                        'sourceUniverse': 'universeB', 'subjects': [EDIT]}
found2, _ = M.path_owner_universes(MiniView(scopes2), [EDIT])
R['controlWithSourcePathScope'] = {'selectorReturnedUniverses': sorted(found2),
                                   'universeBNowIncluded': 'universeB' in found2}
print('control (B also has a source-path scope) returns:', sorted(found2))

# Control: a path owned by nobody is reported unowned, not vacuously satisfied.
found3, unowned3 = M.path_owner_universes(MiniView(scopes), ['src/never/seen.ts'])
R['unownedIsTyped'] = {'returned': sorted(found3), 'unowned': unowned3}
print('control (path owned by nobody) unowned:', unowned3)

# ---------------- the normative owner citations ----------------
ec = os.path.join(SNAP, 'docs/coop/design-corrections/foundation/enumeration-contract.v1.md')
lines = open(ec, encoding='utf-8').read().splitlines()
CITES = {
    'availableBindingCarriesExtents': 24,
    'candidateOnlyCellsCarryCandidateSourcePaths': 26,
    'unavailableBindingKeepsExtentsUniverseNull': 28,
    'symbolExtentIsCodeScopeOnly': 85,
    'fullReplayReAdmitsSelectedPopulation': 110,
    'symbolExtentIsOwnerAdmittedPaths': 125,
    'completeSymbolExaminedPathsEqualsExtent': 131,
}
R['ownerCitations'] = {}
print('\n--- frozen31 enumeration-contract.v1.md citations ---')
for k, ln in CITES.items():
    txt = lines[ln - 1].strip()
    R['ownerCitations'][k] = {'line': ln, 'text': txt[:400]}
    print('  L%-4d %-46s %s' % (ln, k, txt[:120]))

# the exact sentence that settles symbol-extent-is-paths
key = [l for l in lines if 'Symbol extent is owner-admitted' in l]
R['decisiveSentence'] = key[0].strip() if key else None
print('\nDECISIVE:', (R['decisiveSentence'] or '')[:420])

# is EnumerationPlan a required evaluator3 parameter?
eim = os.path.join(SNAP, 'docs/coop/design-corrections/foundation/evaluator_input_model.v3.py')
if os.path.isfile(eim):
    t = open(eim, encoding='utf-8').read()
    R['requiredParametersPresent'] = 'required_parameters' in t
    rows = [l.strip() for l in t.splitlines() if 'enumeration' in l.lower() and
            ('required' in l.lower() or 'parameter' in l.lower())]
    R['enumerationRequiredLines'] = rows[:8]
    print('\nevaluator_input_model.v3 required_parameters present:', R['requiredParametersPresent'])
    for l in rows[:6]:
        print('   ', l[:150])

R['FINDING'] = {
    'rootRRSA1Confirmed': True,
    'why': ('The frozen31 enumeration owner retains program-to-path ownership independently of '
            'source-path relation scopes: an available binding carries extents[]; a symbol extent IS '
            'owner-admitted programRootFiles / syntax code suffixes / rust sourceUnitOwnership '
            'selected paths; candidate-only cells carry candidateSourcePaths; and an UNAVAILABLE '
            'binding keeps extents populated with universe null. The selector reads only '
            'source-path-kind subject scopes, so a universe whose tie to the edited path is a symbol '
            'extent, a candidate census, or an unavailable-binding expected extent is classified '
            'unrelated and does not veto.'),
    'evidenceClass': ('static normative completeness plus a unit-scoped selector probe; NOT an '
                      'executed full-Run counterexample')}
print('\nFINDING: root RRS-A1 confirmed =', R['FINDING']['rootRRSA1Confirmed'])
json.dump(R, open(os.path.join(OUT, 'v07-rrsa1.json'), 'w'), indent=1, default=str)
print('wrote v07-rrsa1.json')
