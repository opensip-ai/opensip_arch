"""P05 — substantive execution assessment of the NEW repair closed-world selection owner.

Scope: unit-level execution of the published module's own functions against hand-built retained
views. NOT a full admitted Run and NOT a product bypass claim. I test correctness, conservatism and
completeness of the law itself, not agreement with root or the author.
"""
import importlib.util, json, os, sys

SRC = '/tmp/opensip-design-corrections/candidate-subject.v32'
W = os.path.join(SRC, 'docs/coop/design-corrections/workflows')
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v32/receipts'
spec = importlib.util.spec_from_file_location('rcws32', os.path.join(W, 'repair_closed_world_selection.v1.py'))
M = importlib.util.module_from_spec(spec)
sys.modules['rcws32'] = M
spec.loader.exec_module(M)
R = {'probeScope': ('unit-level execution of the published module over hand-built retained views; '
                    'not a full admitted Run, not a product bypass claim')}
EDIT = 'src/lib/util.ts'


class View:
    def __init__(self, plan=None, scopes=None, coverage=(), snapshot='snap1'):
        self.snapshot_id = snapshot
        self._plan = plan or {'cells': []}
        self._scopes = scopes or {}
        self._cov = coverage

    def enumeration_plan(self):
        return self._plan

    def subject_scopes(self):
        return self._scopes

    def coverage_records(self):
        return self._cov

    def matched_findings(self):
        return []


def binding(universe, paths, kind='symbol', status='selected', ordinal=0, **kw):
    b = {'ordinal': ordinal, 'universe': universe, 'provenance': 'default-unit',
         'enumerator': {'status': status, 'closureId': 'closure:x'},
         'extents': [{'kind': kind, 'paths': list(paths)}]}
    b.update(kw)
    return b


def plan(*bindings, capability='dead-code'):
    return {'cells': [{'capabilityId': capability, 'programBindings': list(bindings)}]}


# ---- 1. RRS-A1: the symbol-extent owner the OLD selector missed is now found ----
p = plan(binding('uA', [EDIT], kind='file', ordinal=0),
         binding('uB', [EDIT], kind='symbol', ordinal=1))
av, unres, owned = M.selected_program_owners(View(plan=p), [EDIT])
R['rrsA1_symbolOwnerFound'] = {'universes': sorted(av), 'unresolved': len(unres),
                               'owned': sorted(owned),
                               'symbolOwnerIncluded': 'uB' in av}
print('1. symbol-extent owner now found :', sorted(av), '| uB included:', 'uB' in av)

# ---- 2. candidateSourcePaths counts as ownership ----
# my first attempt passed `universe` twice (positional and keyword); corrected
p2 = plan(binding('uC', [], kind='file', ordinal=0, candidateSourcePaths=[EDIT]))
p2['cells'][0]['programBindings'][0]['extents'] = []
av2, _, _ = M.selected_program_owners(View(plan=p2), [EDIT])
R['rrsA1_candidatePathsCount'] = {'universes': sorted(av2),
                                  'extentKinds': av2.get('uC', [{}])[0].get('extentKinds')}
print('2. candidateSourcePaths ownership :', sorted(av2), R['rrsA1_candidatePathsCount']['extentKinds'])

# ---- 3. selected UNAVAILABLE binding -> typed unresolved, not dropped ----
p3 = plan(binding('uA', [EDIT], kind='file', ordinal=0),
          binding(None, [EDIT], kind='symbol', ordinal=1,
                  deficiency='provider-unavailable', nativeCause=None))
av3, unres3, _ = M.selected_program_owners(View(plan=p3), [EDIT])
R['unavailableBinding'] = {'availableUniverses': sorted(av3), 'unresolvedRows': len(unres3),
                           'unresolvedVia': [r['via'] for r in unres3],
                           'deficiencyCarried': [r.get('deficiency') for r in unres3]}
print('3. unavailable selected binding   : available=%s unresolved=%d (%s)'
      % (sorted(av3), len(unres3), [r.get('deficiency') for r in unres3]))

# ---- 4. UNSELECTED programs are never inferred ----
p4 = plan(binding('uZ', [EDIT], kind='symbol', ordinal=0, status='unselected'))
av4, unres4, owned4 = M.selected_program_owners(View(plan=p4), [EDIT])
R['unselectedNotInferred'] = {'available': sorted(av4), 'unresolved': len(unres4),
                              'owned': sorted(owned4),
                              'correctlyIgnored': not av4 and not unres4 and not owned4}
print('4. unselected program ignored     :', R['unselectedNotInferred']['correctlyIgnored'])

# ---- 5. file/package/symbol extents stay distinct; no whole-snapshot inference ----
b = binding('uD', ['a.ts'], kind='file', ordinal=0)
b['extents'].append({'kind': 'symbol', 'paths': ['b.ts']})
b['extents'].append({'kind': 'package', 'paths': ['package.json']})
census = M.binding_applicable_paths(b)
R['extentKindsDistinct'] = {k: sorted(v) for k, v in census.items()}
R['noWholeSnapshotInference'] = 'zzz-unrelated.ts' not in census
print('5. per-extent census              :', R['extentKindsDistinct'],
      '| unrelated path absent:', R['noWholeSnapshotInference'])

# ---- 6. source-path scopes are an ADDITIONAL witness, not the owner source ----
scopes = {'scope2:W': {'relation': 'file', 'resolution': 'enumerated', 'snapshotId': 'snap1',
                       'sourceUniverse': 'uW', 'subjects': [EDIT]}}
wit = M.source_path_scope_witnesses(View(scopes=scopes), [EDIT])
R['witnessUnion'] = {'witnessUniverses': sorted(wit)}
uni, srcs, unowned, paths, ownership = M.relevant_universes(
    View(plan=p, scopes=scopes), [], [{'action': 'delete', 'path': EDIT}])
R['unionOfCensusAndWitness'] = {'relevantUniverses': uni,
                                'includesCensusOwners': {'uA', 'uB'} <= set(uni),
                                'includesWitnessOnlyUniverse': 'uW' in uni}
print('6. union census+witness           :', uni)

# ---- 7. RRS-A2 remedy: two records differing ONLY in targetUniverse/commitment/identity ----
rowA = {'coverageId': 'coverage2:aaa', 'relation': 'file', 'resolution': 'enumerated',
        'sourceUniverse': 'uA', 'targetUniverse': 'uX', 'subjectScopeCommitment': 'c1',
        'closedWorld': {'deadCodeRepairEligible': False, 'reasons': ['nonliteral-loading']}}
rowB = dict(rowA, coverageId='coverage2:bbb', targetUniverse='uY', subjectScopeCommitment='c2')
ca, cb = M.record_coordinates(rowA), M.record_coordinates(rowB)
R['remedyDistinguishes'] = {'coordinatesA': ca, 'coordinatesB': cb, 'distinct': ca != cb}
print('\n7. remedy coordinates distinct    :', ca != cb)
print('   A:', ca)
print('   B:', cb)

# ---- 8. display summary folds ABSENCE ----
sel_closed = [{'closedWorld': {'deadCodeRepairEligible': True, 'exportsClosed': 'closed',
                               'entryPointsRecognized': 'all', 'nonliteralLoading': 'none',
                               'externalConsumers': 'none-declared'}}]
no_absence = M.display_summary(sel_closed, absent=False)
with_absence = M.display_summary(sel_closed, absent=True)
empty = M.display_summary([], absent=False)
R['displaySummary'] = {'closedOnly': no_absence, 'closedPlusAbsence': with_absence,
                       'nothingSelected': empty,
                       'absenceFlipsBoolean': no_absence['deadCodeRepairEligible'] is True
                       and with_absence['deadCodeRepairEligible'] is False,
                       'emptyEqualsSentinel': empty == M.EMPTY_DISPLAY_SUMMARY,
                       'sentinelIsNotAllUnknown': sum(
                           1 for k, v in M.EMPTY_DISPLAY_SUMMARY.items() if v == 'unknown') == 2}
print('\n8. display summary: closed-only=%s' % json.dumps(no_absence))
print('   with absence folded           =%s' % json.dumps(with_absence))
print('   absence flips the boolean     :', R['displaySummary']['absenceFlipsBoolean'])
print('   sentinel has exactly 2 unknown:', R['displaySummary']['sentinelIsNotAllUnknown'])

# ---- 9. selection order is total and byte-based ----
R['selectionOrderKey'] = list(M.SELECTION_ORDER_KEY)
R['orderIncludesIdentityAsSixth'] = M.SELECTION_ORDER_KEY[-1] == 'coverageId'
R['orderHasFiveCoordinatesFirst'] = list(M.SELECTION_ORDER_KEY[:5]) == [
    'relation', 'resolution', 'sourceUniverse', 'targetUniverse', 'subjectScopeCommitment']
print('\n9. SELECTION_ORDER_KEY           :', list(M.SELECTION_ORDER_KEY))

# ---- 10. gate conservatism: unowned path and create-only ----
d_unowned = M.derive(View(plan=plan(), scopes={}), [], [{'action': 'delete', 'path': EDIT}])
d_create = M.derive(View(plan=plan(), scopes={}), [], [{'action': 'create', 'path': 'new.ts'}])
R['gate'] = {'unownedEligible': d_unowned['eligible'],
             'unownedUnmet': len(d_unowned['unmetPreconditions']),
             'createOnlyGateActivated': d_create['gateActivated'],
             'createOnlyEligible': d_create['eligible'],
             'createOnlyDisplayDeterministic': d_create['closedWorld'] == M.EMPTY_DISPLAY_SUMMARY}
print('\n10. unowned delete -> eligible=%s unmet=%d ; create-only -> gate=%s eligible=%s display=sentinel:%s'
      % (d_unowned['eligible'], len(d_unowned['unmetPreconditions']), d_create['gateActivated'],
         d_create['eligible'], R['gate']['createOnlyDisplayDeterministic']))

json.dump(R, open(os.path.join(OUT, 'p05-repairlaw.json'), 'w'), indent=1, default=str)
print('\nwrote p05-repairlaw.json')
