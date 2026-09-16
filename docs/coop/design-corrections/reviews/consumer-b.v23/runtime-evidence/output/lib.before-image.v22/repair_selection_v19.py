"""S1 CLOSED: the unsafe-repair closed-world SELECTION LAW, reconstructed from published law.

The generation-16 SHOULD V16-S1 said the repair descriptor named "that same Run's ClosedWorldV2"
without saying which Coverage entry owns it when a Run carries several that differ. This kit
publishes the answer in two places that agree, and this module reconstructs it:

  workflows-and-surfaces.md section 6 "A Run holds one ClosedWorldV2 per Coverage entry, not one
  per Run, so the gate states which entries it reads", with its three numbered steps; and
  workflows/schemas/evaluator3/repair.schema.json
  #/$defs/RepairPlanDescriptor/properties/closedWorld, which states the same selection, the same
  reduction and the same authority limit on the descriptor member.

THE LAW, as implemented here:

 1. RELEVANT UNIVERSES -- the union of two published joins, plus one additional witness:
      (a) every universe reached by ALL matching occurrences of EVERY target fingerprint
          (finding3.fingerprint -> finding3.subjectId -> subject3.universe). "All occurrences,
          not a representative", because one fingerprint may lawfully match in two universes.
      (b) every universe that OWNS an unsafe edited path in the RETAINED SELECTED-PROGRAM CENSUS
          of this Run's EnumerationPlanV1: for each binding whose enumerator.status is `selected`,
          its own extents[] per kind plus, on a candidate-only cell, candidateSourcePaths.
            * non-null universe whose census contains the path -> that universe is relevant;
            * SELECTED BUT UNAVAILABLE (universe=null, extents still populated) -> TYPED
              UNRESOLVED OWNERSHIP, which "does not vanish because some other owner of the same
              path is closed";
            * an UNSELECTED binding is never inferred as an owner.
          Each extent kind is read as itself, so a selected program whose own census lacks the
          edit stays UNRELATED, and multiple ownership is preserved.
      (c) retained source-path subject scopes (file, clones, vcs-change) naming the path are an
          ADDITIONAL witness only: they name paths, they do not enumerate owners.
    An unsafe path claimed by no census and no scope is REPAIR.CLOSED_WORLD_NOT_ESTABLISHED
    rather than guessed.
 2. SELECTED RECORDS -- for every relevant universe, EVERY retained native coverage2 of that Run
    whose scope's sourceUniverse is that universe. Independent of evidenceRequirements, so a
    recipe can neither pick a favourable relation/rung nor drop a conflicting record. Dedup by
    coverage2 IDENTITY, ordered on UTF-8 bytes by relation, resolution, sourceUniverse,
    targetUniverse, subjectScopeCommitment, then the coverage2 identity.
 3. THE GATE -- the NON-VACUOUS conjunction of deadCodeRepairEligible over those records, decided
    BEFORE the descriptor is built. A relevant universe with no retained Coverage, an unsafe path
    with no reconstructable owner and an unresolved unavailable-binding ownership are each
    REPAIR.CLOSED_WORLD_NOT_ESTABLISHED: "an empty evidence subset is not truth". Each dissent
    names ALL SIX ordering members unabbreviated plus that record's own `reasons`.
    `dynamicDispatch` is NOT read here and is NOT a global veto.
 4. THE DESCRIPTOR MEMBER -- a five-field DISPLAY SUMMARY, not a copy and not a projection of one
    record: deadCodeRepairEligible is the conjunction (false when none selected), every other
    member takes the LEAST-CLOSED value present, and ABSENCE IS FOLDED IN so the summary cannot
    read as closed while eligibility is refused for absence. With nothing selected the same rule
    yields the five-field least-closed display sentinel. The member carries NO authority -- the
    gate reads the full records, including the two members the summary does not carry.

This module decides nothing about authorization: preview is a Query-class step, recipe trust,
policy consent and the apply-time authorization bound to the exact repairPlanId remain separate
and are not granted here.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_core as K
import opensip_schema as S
import opensip_build as B
import opensip_store as ST
import opensip_closure as CL

OUT = '/tmp/opensip-design-corrections/consumer-b.v22/output'
KIT = S.KIT

LEAST_CLOSED = {
    'exportsClosed': ['closed', 'open', 'unknown'],
    'entryPointsRecognized': ['all', 'partial', 'none'],
    'nonliteralLoading': ['none', 'present'],
    'externalConsumers': ['none-declared', 'possible', 'unknown'],
}
SENTINEL = {'deadCodeRepairEligible': False, 'exportsClosed': 'unknown',
            'entryPointsRecognized': 'none', 'nonliteralLoading': 'present',
            'externalConsumers': 'unknown'}
SOURCE_PATH_RELATIONS = ('file', 'clones', 'vcs-change')
CANDIDATE_ONLY_CAPABILITIES = ('clones-near', 'clones-cross-tsjs')


def enumeration_plan(st, closure):
    ei = json.loads(st.get_blob(st.labels['execution-inputs']).decode())
    dig = ei['enumerationPlanDigest']
    return json.loads(st.get_blob(dig).decode()), ei


def target_universes(st, targets):
    """(a): ALL matching occurrences of EVERY target fingerprint."""
    out, unmatched = {}, []
    findings = {t: r for t, r in st.objects.items() if t.startswith('finding3:')}
    subjects = {t: r for t, r in st.objects.items() if t.startswith('subject3:')}
    for fp in targets:
        occ = [r for r in findings.values() if r.get('fingerprint') == fp]
        if not occ:
            unmatched.append(fp)
            continue
        for f in occ:
            sub = subjects.get(f['subjectId'])
            if sub is None:
                unmatched.append(fp)
                continue
            out.setdefault(sub['universe'], []).append(
                {'fingerprint': fp, 'subjectId': f['subjectId'], 'kind': sub['kind'],
                 'nativeSubjectId': sub['nativeSubjectId']})
    return out, unmatched


def census_owners(plan_param, unsafe_paths):
    """(b): the retained selected-program census. Returns (owners, unresolved, unrelated)."""
    owners, unresolved, considered = {}, [], []
    for ci, cell in enumerate(plan_param['cells']):
        for b in cell['programBindings']:
            status = b['enumerator'].get('status')
            paths = set()
            for ext in (b.get('extents') or []):
                paths |= set(ext['paths'])
            if cell['capabilityId'] in CANDIDATE_ONLY_CAPABILITIES:
                paths |= set(b.get('candidateSourcePaths') or [])
            hit = sorted(paths & set(unsafe_paths))
            considered.append({'cell': cell['capabilityId'], 'program': b['ordinal'],
                              'enumerator': status, 'universe': b.get('universe'),
                              'censusSize': len(paths), 'unsafePathsInThisCensus': hit,
                              'contributes': bool(hit) and status == 'selected'})
            if not hit or status != 'selected':
                continue              # an UNSELECTED binding is never inferred as an owner
            if b.get('universe') is not None:
                for p in hit:
                    owners.setdefault(p, []).append(
                        {'universe': b['universe'], 'cell': cell['capabilityId'],
                         'program': b['ordinal'],
                         'kinds': sorted(e['kind'] for e in (b.get('extents') or []))})
            else:
                unresolved.append(
                    {'paths': hit, 'cell': cell['capabilityId'], 'program': b['ordinal'],
                     'why': ('a SELECTED but UNAVAILABLE binding holds a real retained '
                             'expected-ownership claim with no universe to make eligible and no '
                             'Coverage to establish a closed world, and it does not vanish '
                             'because some other owner of the same path is closed'),
                     'detail': 'REPAIR.CLOSED_WORLD_NOT_ESTABLISHED'})
    return owners, unresolved, considered


def scope_witnesses(st, unsafe_paths):
    """(c): retained source-path subject scopes naming the path -- an ADDITIONAL witness."""
    out = []
    for tid, sc in sorted(st.objects.items()):
        if not tid.startswith('scope2:'):
            continue
        if sc['relation'] not in SOURCE_PATH_RELATIONS:
            continue
        hit = sorted(set(sc['subjects']) & set(unsafe_paths))
        if hit:
            out.append({'scope': tid, 'relation': sc['relation'],
                        'resolution': sc['resolution'],
                        'sourceUniverse': sc['sourceUniverse'], 'paths': hit})
    return out


def selected_records(st, relevant):
    """2: EVERY retained native coverage2 whose scope sourceUniverse is relevant, deduplicated by
    coverage2 identity and ordered on UTF-8 bytes by the six members."""
    rows = []
    for tid, cv in st.objects.items():
        if not tid.startswith('coverage2:'):
            continue
        sc = st.objects.get(cv['scopeId'])
        if sc is None or sc['sourceUniverse'] not in relevant:
            continue
        pay = json.loads(st.get_blob(cv['payloadDigest']).decode())
        key, ent = pay['key'], pay['entry']
        rows.append({
            'coverageId': tid, 'relation': key['relation'], 'resolution': key['resolution'],
            'sourceUniverse': key['sourceUniverse'], 'targetUniverse': key['targetUniverse'],
            'subjectScopeCommitment': key['subjectScopeCommitment'],
            'closedWorld': ent['closedWorld'], 'coverage': ent['coverage'],
            'deficiency': ent['deficiency'], 'nativeCause': ent['nativeCause']})
    seen, dedup = set(), []
    for r in rows:
        if r['coverageId'] in seen:
            continue
        seen.add(r['coverageId'])
        dedup.append(r)
    dedup.sort(key=lambda r: (r['relation'].encode(), r['resolution'].encode(),
                              (r['sourceUniverse'] or '').encode(),
                              (r['targetUniverse'] or '').encode(),
                              r['subjectScopeCommitment'].encode(),
                              r['coverageId'].encode()))
    return dedup


def reduce_summary(records, absence):
    """4: the five-field display summary. Absence is FOLDED IN, not hidden."""
    pool = [r['closedWorld'] for r in records]
    if absence:
        pool = pool + [SENTINEL]
    out = {'deadCodeRepairEligible': bool(records) and all(
        r['closedWorld']['deadCodeRepairEligible'] for r in records) and not absence}
    for field, order in LEAST_CLOSED.items():
        present = [cw[field] for cw in pool if field in cw]
        out[field] = (max(present, key=lambda v: order.index(v)) if present
                      else SENTINEL[field])
    return out


def select(st, targets, edits, label=''):
    plan_param, ei = enumeration_plan(st, None)
    unsafe = sorted({e['path'] for e in edits if e['action'] in ('delete', 'replace')})
    tu, unmatched = target_universes(st, targets)
    owners, unresolved, considered = census_owners(plan_param, unsafe)
    witnesses = scope_witnesses(st, unsafe)
    relevant = set(tu)
    for p, rows in owners.items():
        relevant |= {r['universe'] for r in rows}
    relevant |= {w['sourceUniverse'] for w in witnesses}
    no_owner = [p for p in unsafe
                if p not in owners and not any(p in w['paths'] for w in witnesses)]
    records = selected_records(st, relevant)
    by_universe = {}
    for r in records:
        by_universe.setdefault(r['sourceUniverse'], []).append(r['coverageId'])
    empty_universes = sorted(u for u in relevant if u not in by_universe)

    not_established = []
    for u in empty_universes:
        not_established.append({'detail': 'REPAIR.CLOSED_WORLD_NOT_ESTABLISHED',
                                'because': 'relevant universe retains no native Coverage',
                                'universe': u,
                                'law': 'an empty evidence subset is not truth'})
    for p in no_owner:
        not_established.append({'detail': 'REPAIR.CLOSED_WORLD_NOT_ESTABLISHED',
                                'because': ('unsafe edited path claimed by no selected '
                                            'binding census and no source-path scope'),
                                'path': p})
    for u in unresolved:
        not_established.append(dict(u, because='selected but UNAVAILABLE binding ownership'))

    dissents = []
    for r in records:
        if r['closedWorld']['deadCodeRepairEligible']:
            continue
        dissents.append({
            'detail': 'REPAIR.CLOSED_WORLD_NOT_ESTABLISHED',
            # all SIX ordering members, unabbreviated, plus that record's own reasons
            'relation': r['relation'], 'resolution': r['resolution'],
            'sourceUniverse': r['sourceUniverse'], 'targetUniverse': r['targetUniverse'],
            'subjectScopeCommitment': r['subjectScopeCommitment'],
            'coverageId': r['coverageId'],
            'reasons': r['closedWorld'].get('reasons'),
            'why': ('a destructive edit is a universal negative, so ONE dissenting relevant '
                    'record defeats it')})
    eligible = bool(records) and not dissents and not not_established
    summary = reduce_summary(records, bool(not_established))
    return {
        'label': label, 'unsafeEditedPaths': unsafe, 'targets': list(targets),
        'step1_relevantUniverses': {
            'fromTargetOccurrences': {u: rows for u, rows in sorted(tu.items())},
            'unmatchedTargets': unmatched,
            'fromSelectedProgramCensus': {p: rows for p, rows in sorted(owners.items())},
            'bindingsConsidered': considered,
            'unresolvedOwnership': unresolved,
            'additionalSourcePathScopeWitnesses': witnesses,
            'unsafePathsWithNoReconstructableOwner': no_owner,
            'relevant': sorted(relevant)},
        'step2_selectedRecords': records,
        'step2_selectionStanding': (
            'every retained coverage2 whose scope sourceUniverse is relevant, INDEPENDENT of '
            'evidenceRequirements, deduplicated by identity and totally ordered on the six '
            'published members'),
        'step3_gate': {'eligible': eligible, 'recordCount': len(records),
                       'coverageByUniverse': by_universe,
                       'dissents': dissents, 'notEstablished': not_established,
                       'nonVacuous': bool(records),
                       'dynamicDispatchRead': False,
                       'dynamicDispatchStanding': (
                           'not read by this gate and not a global veto: native 4.5 '
                           'affected_targets and 4.6 sufficiency_v2 keep dynamic-edge effects '
                           'target-relative and per-requirement')},
        'step4_displaySummary': summary,
        'step4_authority': (
            'NONE. No member of this summary is authoritative, the boolean included. The gate '
            'above reads the full selected records including dynamicDispatch and reasons, which '
            'the summary does not carry.'),
    }


def law_branch_controls():
    """The selection branches this origin's five Runs do NOT contain, measured at the law level
    over synthetic EnumerationPlanV1 parameters. They are labelled exactly that: a UNIT
    measurement of the published branch, not a Run and not an admitted record."""
    base = {'schemaVersion': 1, 'cells': []}

    def cell(cap, bindings, kinds=('file',)):
        return {'capabilityId': cap, 'languageMode': 'rust-cargo', 'workspaceRoot': '.',
                'required': True, 'kinds': list(kinds), 'programBindings': bindings}

    def bind(ordinal, universe, status, paths, reason=None):
        b = {'ordinal': ordinal,
             'enumerator': ({'status': 'selected', 'closureId': 'closure2:' + '1' * 64}
                            if status == 'selected'
                            else {'status': 'unselected', 'reason': 'optional-unselected'}),
             'universe': universe,
             'extents': [{'kind': 'file', 'paths': list(paths)}]}
        if reason:
            b['deficiency'] = reason
        return b

    U1, U2 = 'a' * 64, 'b' * 64
    rows = []
    plan = dict(base, cells=[cell('clones-fact', [bind(0, U1, 'selected', ['src/a.rs'])])])
    owners, unresolved, considered = census_owners(plan, ['src/a.rs'])
    rows.append({'branch': 'selected-binding-with-a-non-null-universe-owns-the-path',
                 'owners': owners, 'unresolvedOwnership': unresolved,
                 'expected': 'the universe becomes relevant',
                 'measuredRelevant': sorted({r['universe'] for v in owners.values()
                                             for r in v}),
                 'result': 'PASS' if owners and not unresolved else 'FAIL'})
    plan = dict(base, cells=[cell('clones-fact',
                                  [bind(0, None, 'selected', ['src/a.rs'], 'provider-unavailable'),
                                   bind(1, U2, 'selected', ['src/a.rs'])])])
    owners, unresolved, considered = census_owners(plan, ['src/a.rs'])
    rows.append({'branch': 'selected-but-UNAVAILABLE-binding-contributes-typed-unresolved-'
                           'ownership-that-does-not-vanish-because-another-owner-is-closed',
                 'owners': owners, 'unresolvedOwnership': unresolved,
                 'expected': ('REPAIR.CLOSED_WORLD_NOT_ESTABLISHED survives beside a second '
                              'lawful owner of the same path'),
                 'result': 'PASS' if (unresolved and owners) else 'FAIL'})
    plan = dict(base, cells=[cell('clones-fact', [bind(0, None, 'unselected', ['src/a.rs'])])])
    owners, unresolved, considered = census_owners(plan, ['src/a.rs'])
    rows.append({'branch': 'an-UNSELECTED-binding-is-never-inferred-as-an-owner',
                 'owners': owners, 'unresolvedOwnership': unresolved,
                 'bindingsConsidered': considered,
                 'expected': 'no owner and no unresolved ownership from this binding',
                 'result': 'PASS' if not owners and not unresolved else 'FAIL'})
    plan = dict(base, cells=[cell('clones-fact', [bind(0, U1, 'selected', ['src/other.rs'])])])
    owners, unresolved, considered = census_owners(plan, ['src/a.rs'])
    rows.append({'branch': 'a-selected-program-whose-own-census-lacks-the-edit-stays-UNRELATED',
                 'owners': owners, 'unresolvedOwnership': unresolved,
                 'expected': 'no universe becomes relevant',
                 'result': 'PASS' if not owners and not unresolved else 'FAIL'})
    plan = dict(base, cells=[{'capabilityId': 'clones-near', 'languageMode': 'rust-cargo',
                              'workspaceRoot': '.', 'required': True, 'kinds': [],
                              'programBindings': [
                                  dict(bind(0, U1, 'selected', []),
                                       candidateSourcePaths=['src/a.rs'])]}])
    owners, unresolved, considered = census_owners(plan, ['src/a.rs'])
    rows.append({'branch': 'a-candidate-only-cell-adds-its-candidateSourcePaths-to-the-census',
                 'owners': owners, 'expected': 'the candidate census owns the path',
                 'result': 'PASS' if owners else 'FAIL'})
    # the reduction branches
    rows.append({'branch': 'nothing-selected-yields-the-five-field-least-closed-display-sentinel',
                 'measured': reduce_summary([], False), 'expected': SENTINEL,
                 'result': 'PASS' if reduce_summary([], False) == SENTINEL else 'FAIL'})
    closed = {'closedWorld': {'deadCodeRepairEligible': True, 'exportsClosed': 'closed',
                              'entryPointsRecognized': 'all', 'nonliteralLoading': 'none',
                              'externalConsumers': 'none-declared'}}
    rows.append({'branch': 'absence-is-FOLDED-IN-so-a-closed-record-cannot-hide-it',
                 'measured': reduce_summary([closed], True),
                 'expected': SENTINEL,
                 'result': 'PASS' if reduce_summary([closed], True) == SENTINEL else 'FAIL'})
    mixed = [closed, {'closedWorld': {'deadCodeRepairEligible': True, 'exportsClosed': 'open',
                                      'entryPointsRecognized': 'partial',
                                      'nonliteralLoading': 'present',
                                      'externalConsumers': 'possible'}}]
    want = {'deadCodeRepairEligible': True, 'exportsClosed': 'open',
            'entryPointsRecognized': 'partial', 'nonliteralLoading': 'present',
            'externalConsumers': 'possible'}
    rows.append({'branch': 'every-other-member-takes-the-LEAST-CLOSED-value-present',
                 'measured': reduce_summary(mixed, False), 'expected': want,
                 'result': 'PASS' if reduce_summary(mixed, False) == want else 'FAIL'})
    dissent = [closed, {'closedWorld': dict(closed['closedWorld'],
                                            deadCodeRepairEligible=False)}]
    rows.append({'branch': 'ONE-dissenting-relevant-record-defeats-the-conjunction',
                 'measured': reduce_summary(dissent, False)['deadCodeRepairEligible'],
                 'expected': False,
                 'result': ('PASS' if reduce_summary(dissent, False)['deadCodeRepairEligible']
                            is False else 'FAIL')})
    return rows


def main():
    out = {'standing': __doc__, 'runs': [], 'lawBranchControls': law_branch_controls()}
    for lab in ('typescript', 'rust', 'rust-partial'):
        st, _doc = ST.Store.load(OUT + '/runs/%s.store.json' % lab)
        fps = sorted(t for t in st.objects if t.startswith('finding-key2:'))
        inv = {r['path']: r for t, r in st.objects.items() if t.startswith('snapshot2:')
               for r in r['sourceInventory']}
        # a replace over a real snapshot member, so the unsafe-path join is actually exercised
        victim = sorted(p for p in inv if p.endswith(('.js', '.ts', '.rs')))[0]
        edits = [{'path': victim, 'action': 'replace',
                  'preimageDigest': inv[victim]['sha256'],
                  'postimageDigest': K.raw_sha256(b'repaired\n'), 'postimageBytes': 9}]
        res = select(st, fps[:1], edits, label=lab)
        res['createOnlyContrast'] = {
            'standing': ('a create-only plan activates no gate, but it still READS the selection '
                         'and still BUILDS the member, so the descriptor stays deterministic'),
            'displaySummary': select(st, fps[:1],
                                     [{'path': 'src/new.js', 'action': 'create',
                                       'preimageDigest': None,
                                       'postimageDigest': K.raw_sha256(b'x'),
                                       'postimageBytes': 1}],
                                     label=lab + ':create-only')['step4_displaySummary']}
        out['runs'].append(res)
        g = res['step3_gate']
        print('%-13s universes=%-2d records=%-2d eligible=%-5s dissents=%d notEstablished=%d '
              'summary=%s'
              % (lab, len(res['step1_relevantUniverses']['relevant']), g['recordCount'],
                 g['eligible'], len(g['dissents']), len(g['notEstablished']),
                 json.dumps(res['step4_displaySummary'])))
    bad = [r['branch'] for r in out['lawBranchControls'] if r['result'] != 'PASS']
    print('law-branch controls: %d, failures %s'
          % (len(out['lawBranchControls']), bad))
    for r in out['lawBranchControls']:
        print('   %-6s %s' % (r['result'], r['branch'][:96]))
    with open(OUT + '/vectors/repair-closed-world-selection.json', 'w') as f:
        json.dump(out, f, indent=1)
    assert not bad, bad


if __name__ == '__main__':
    main()
