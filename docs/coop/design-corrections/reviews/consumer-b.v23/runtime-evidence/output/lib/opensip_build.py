"""Shared constructors for building complete positive Run descriptor graphs.

Every identity here is COMPUTED by opensip_core from the record's own canonical bytes.
Nothing is copied from a kit example. All synthetic repository bytes, toolchain
observations and provider returns are this origin's own SYNTHETIC TRUSTED OBSERVATIONS:
they are assumptions about a future host, never native enforcement proof.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_core as K
import opensip_schema as S
import opensip_store as ST
import opensip_fixture as FX

KIT = S.KIT

IDENTITY_DOC = 'foundation/identity-schemas.v3.json'
RELATION_DOC = 'foundation/relation-payload-schemas.v2.json'
NATIVE_DOC = 'native/native-evidence.schemas.v2.json'
POLICY_V2_DOC = 'workflows/schemas/policy-document.v2.schema.json'
POLICY_V1_DOC = 'workflows/schemas/policy-document.schema.json'
ENUM_PLAN_DOC = 'foundation/enumeration-plan.schema.v1.json'
EMIT_PLAN_DOC = 'foundation/evaluator-emission-plan.schema.v1.json'
SUBJ_INV_DOC = 'foundation/subject-inventory.schema.v1.json'
EXEC_IN_DOC = 'foundation/execution-inputs.schema.v1.json'
IMPORTED_DOC = 'workflows/schemas/imported-evidence.schema.json'
TEST_EXEC_DOC = 'workflows/schemas/test-execution.schema.json'
COMMON_DOC = 'workflows/schemas/common.schema.json'


def doc_sha(name):
    return S.load_doc(name)['sha256']


def doc_bytes(name):
    return S.load_doc(name)['bytes']


class Builder:
    def __init__(self, project_id):
        self.st = ST.Store()
        self.project_id = project_id
        self.admissions = []           # schema-admission results, per record
        self.retained_schema_docs = {}  # kit-relative path -> sha256

    # ------------------------------------------------------------------ helpers
    def retain_schema_doc(self, name):
        d = S.load_doc(name)
        self.st.put_blob(d['bytes'], label='schema:' + d['path'])
        self.retained_schema_docs[d['path']] = d['sha256']
        return d['sha256']

    def admit(self, doc, selector, inst, label):
        r = S.admit(doc, selector, inst, label)
        self.admissions.append(r)
        if not r['admitted']:
            raise RuntimeError('ADMISSION FAILED %s\nstock=%s\nkeywords=%s'
                               % (label, json.dumps(r['stockSchemaErrors'], indent=1)[:2500],
                                  json.dumps(r['publishedKeywordRefusals'], indent=1)[:1200]))
        return r

    def record(self, doc, selector, inst, label):
        """Admit a canonical-record and retain its C bytes; return raw sha256."""
        self.admit(doc, selector, inst, label)
        return self.st.put_record(inst, label=label)

    def framed(self, domain, doc, selector, inst, label):
        """Admit a typed root and retain its exact H preimage frame; return typed id."""
        self.admit(doc, selector, inst, label)
        return self.st.put_framed(domain, inst, label=label)

    def native_framed(self, domain, doc, selector, inst, label):
        """Admit a native record under a native H domain; return bare 64-hex suffix."""
        self.admit(doc, selector, inst, label)
        return self.st.put_native_framed(domain, inst, label=label)

    # ------------------------------------------------------------------ closures
    def component_manifest(self, stable_id, name, version, role, platform, tree_rows):
        """A component manifest BODY under the security metadata profile (S2:
        `opensip-metadata-canonical.1` -- NFC strings, i64 integers). Its raw SHA-256 is
        closure.manifestDigest (identity section 3: "raw SHA256 of the admitted component
        manifest body bytes encoded with the security metadata profile, excluding the
        signature envelope"). Full component-manifest admission (RJ-1..RJ-3, catalog and
        envelope association) is the DELIVERY/SECURITY owner's boundary; this closure
        joins it by digest equality plus the named semanticVersion join."""
        body = {
            'manifestSchemaVersion': 1,
            'kind': 'component',
            'stableId': stable_id,
            'name': name,
            'version': version,
            'role': role,
            # the description is EXPLICIT semantic fixture metadata, pinned in
            # opensip_fixture.py and never derived from the runtime location
            'commands': [{'name': name, 'description': FX.FIXTURE_NAMESPACE,
                          'scope': 'project'}],
            'platforms': [{'os': platform.split('-')[0], 'arch': platform.split('-')[1],
                           'entrypoint': 'bin/' + name,
                           'tree': [{'type': 'file', 'path': r['path'],
                                     'sha256': r['sha256'], 'length': r['bytes'],
                                     'mode': 420} for r in tree_rows]}],
        }
        b = K.Cmeta(body)
        d = self.st.put_blob(b, label='component-manifest:' + name)
        return d, body, b

    def closure(self, kind, semantic_version, protocol_major, platform, files, label):
        """files: list of (path, bytes). Closure tree hashing includes relative path,
        byte length and digest for every selected file; every tree blob is retained."""
        tree = []
        for p, b in sorted(files, key=lambda t: t[0].encode()):
            self.st.put_blob(b, label='closure-file:%s:%s' % (label, p))
            tree.append({'path': p, 'sha256': K.raw_sha256(b), 'bytes': len(b)})
        mdig, body, mbytes = self.component_manifest(
            stable_id=K.raw_sha256(label.encode())[:8] + '-0000-4000-8000-'
                      + K.raw_sha256(label.encode())[:12],
            name=label, version=semantic_version, role='analyzer',
            platform=platform, tree_rows=tree)
        rec = {'schemaVersion': 2, 'kind': kind, 'manifestDigest': mdig, 'tree': tree,
               'semanticVersion': semantic_version, 'protocolMajor': protocol_major,
               'platform': platform}
        tid = self.framed('closure', IDENTITY_DOC, '#/$defs/closure', rec, 'closure:' + label)
        return tid, rec, body

    # ------------------------------------------------------------------ snapshot
    def snapshot(self, files, config, scope_desc, vcs_kind='git', commit_id=None, dirty=False):
        """files: dict path -> bytes. Returns (snapshotId, snapshot record, helpers)."""
        inv = []
        for p in sorted(files, key=lambda s: s.encode()):
            b = files[p]
            self.st.put_blob(b, label='source:' + p)
            inv.append({'path': p, 'sha256': K.raw_sha256(b), 'bytes': len(b)})
        self.admit(IDENTITY_DOC, '#/$defs/source-inventory', inv, 'source-inventory')
        inv_dig = self.st.put_record(inv, label='source-inventory')
        cfg_dig = self.record(IDENTITY_DOC, '#/$defs/semantic-configuration', config,
                              'semantic-configuration')
        scope_dig = self.record(IDENTITY_DOC, '#/$defs/scope-descriptor', scope_desc,
                                'scope-descriptor')
        vcs = {'schemaVersion': 2, 'kind': vcs_kind, 'commitId': commit_id,
               'dirty': dirty, 'sourceInventoryDigest': inv_dig}
        vcs_dig = self.record(IDENTITY_DOC, '#/$defs/vcs-observation', vcs, 'vcs-observation')
        snap = {'schemaVersion': 2, 'projectId': self.project_id, 'sourceInventory': inv,
                'resolvedConfigDigest': cfg_dig, 'scopeDigest': scope_dig,
                'vcsDigest': vcs_dig}
        sid = self.framed('snapshot', IDENTITY_DOC, '#/$defs/snapshot', snap, 'snapshot')
        return sid, snap, {'inventoryDigest': inv_dig, 'configDigest': cfg_dig,
                           'scopeDigest': scope_dig, 'vcsDigest': vcs_dig,
                           'inventory': inv}

    # ------------------------------------------------------------------ facts / scopes
    def fact(self, snapshot_id, relation, resolution, source_u, target_u, producer,
             payload, anchors, confidence, label):
        sel = self.relation_selector(relation)
        self.admit(RELATION_DOC, sel, payload, 'payload:' + label)
        pdig = self.st.put_record(payload, label='payload:' + label)
        rec = {'schemaVersion': 2, 'snapshotId': snapshot_id, 'relation': relation,
               'resolution': resolution, 'sourceUniverse': source_u,
               'targetUniverse': target_u, 'producerClosure': producer,
               'payloadSchemaDigest': doc_sha(RELATION_DOC), 'payloadDigest': pdig,
               'anchors': K.cset(anchors), 'confidenceMillionths': confidence}
        return self.framed('fact', IDENTITY_DOC, '#/$defs/fact', rec, 'fact:' + label)

    @staticmethod
    def relation_selector(relation):
        reg = json.load(open(KIT + '/' + S.doc_path(RELATION_DOC)))['x-opensip-relation-registry']
        return reg['relations'][relation]['selector']

    def scope(self, snapshot_id, relation, resolution, source_u, target_u, enumerator,
              subjects, label):
        rec = {'schemaVersion': 2, 'snapshotId': snapshot_id, 'sourceUniverse': source_u,
               'targetUniverse': target_u, 'relation': relation, 'resolution': resolution,
               'enumeratorClosure': enumerator, 'subjects': K.cset_strings(subjects)}
        return self.framed('subject-scope', IDENTITY_DOC, '#/$defs/subject-scope', rec,
                           'scope:' + label)

    def coverage(self, scope_id, entry, label):
        """Mints coverage2 from the host-owned scope: the subjectScopeCommitment is
        "sha256:" + the 64-hex suffix of the admitted scope2 identity (native 4.1a)."""
        suffix = self.st.suffix(scope_id)
        scope_rec = self.st.objects[scope_id]
        key = {'relation': scope_rec['relation'], 'resolution': scope_rec['resolution'],
               'sourceUniverse': scope_rec['sourceUniverse'],
               'targetUniverse': scope_rec['targetUniverse'],
               'subjectScopeCommitment': 'sha256:' + suffix}
        entry = dict(entry)
        entry['relation'] = scope_rec['relation']
        entry['resolution'] = scope_rec['resolution']
        entry['examinedUniverse'] = {'subjectScopeCommitment': 'sha256:' + suffix,
                                     'subjectCount': len(scope_rec['subjects'])}
        payload = {'schemaVersion': 3, 'key': key, 'entry': entry}
        self.admit(NATIVE_DOC, '#/$defs/CoverageResultV3', payload, 'coverage-payload:' + label)
        pdig = self.st.put_record(payload, label='coverage-payload:' + label)
        rec = {'schemaVersion': 2, 'scopeId': scope_id,
               'payloadSchemaDigest': doc_sha(NATIVE_DOC), 'payloadDigest': pdig}
        return self.framed('coverage', IDENTITY_DOC, '#/$defs/coverage', rec,
                           'coverage:' + label)

    def view(self, plan_id, scope_ids, fact_ids, coverage_ids, producer, schema_digests, label):
        rec = {'schemaVersion': 2, 'planId': plan_id,
               'scopeIds': K.cset_strings(scope_ids), 'facts': K.cset_strings(fact_ids),
               'coverageIds': K.cset_strings(coverage_ids), 'producerClosure': producer,
               'schemaDigests': K.cset_strings(schema_digests)}
        return self.framed('view', IDENTITY_DOC, '#/$defs/view', rec, 'view:' + label)


# ------------------------------------------------------------------ ExecutionInputs derivation
#
# execution-inputs-contract.v1.md sections 4 and 5, implemented ONCE for the HOST side of every
# fixture. Before generation 19 each builder ASSERTED its cell outcome state and its per-relation
# applicability, and two whole classes of defect followed (V18-D8, V19-D3). The contract says the
# outcome "is DERIVED, then joined to the host row", so the host derives it here from its own
# retained evidence and the independent closure re-derives it separately.
PROJECTION_REGISTRY = 'foundation/evaluator-projection-registry.v1.json'
CAPABILITY_MATRIX = 'native/native-capability-matrix.v2.json'


def _reg(rel_path, key=None):
    d = json.load(open(KIT + '/' + S.doc_path(rel_path)))
    return d[key] if key else d


def matrix_pair(capability, mode):
    """section 5 unsupported-typed: "the MATRIX cell deficiency and the cause-registry cause for
    THAT deficiency (not a hardcoded capability-missing for every cell)". Returns (state,
    deficiency, cause) for the CELL's (capabilityId, languageMode) matrix row."""
    rows = [c for c in _reg(CAPABILITY_MATRIX)['cells']
            if c['capability'] == capability and c['mode'] == mode]
    if not rows:
        return None, None, None
    state = rows[0]['state']
    mdef = rows[0].get('deficiency')
    if mdef is None:
        return state, None, None
    reg = (_reg(NATIVE_DOC)['x-opensip-deficiency-cause-registry']['deficiencies'].get(mdef)
           or {})
    allowed = reg.get('allowedCauses') or []
    cause = allowed[0] if (reg.get('nativeCause') == 'required' and len(allowed) == 1) else None
    return state, mdef, cause


def owed_relations(capability):
    """The owed (relation, resolution) pairs of one capability, in the AUTHORED array order of
    native-capability-matrix.v2.json#/capabilities[id]/relations.

    Generation 20: this replaces the hand-written rel_for_cap table every fixture carried. The
    order is normative, not cosmetic -- execution-inputs-contract section 4's cross-source order
    names this array as the authority for the account leg and says so explicitly: "the matrix array
    as authored -- NOT lexical. `syntax` is authored declares, literal, control-flow, which is not
    sorted, so nothing may re-sort it."
    """
    for c in _reg(CAPABILITY_MATRIX)['capabilities']:
        if c['id'] == capability:
            return [tuple(r) for r in (c.get('relations') or [])]
    return []


def applicability_first_match(capability, mode, relation, enumerator_status, universe,
                              vcs_kind):
    """execution-inputs-contract section 5 / NativeCoverageAccountV1
    x-opensip-applicability-precedence: a NORMATIVE FIRST-MATCH order, total, exactly one token.

      1 inapplicable-vcs           relation is vcs-change AND the admitted VCS kind is none
      2 unsupported-typed          the matrix cell for (capabilityId, languageMode) is
                                   UNSUPPORTED-TYPED
      3 unavailable-unselected     the binding enumerator status is unselected
      4 unavailable-null-universe  the binding universe is null
      5 supported-available        otherwise

    Row 2 OUTRANKS both unavailable tokens, so an UNSUPPORTED-TYPED cell still discloses its matrix
    deficiency and that deficiency's registered cause even when the enumerator is unselected and U
    is null. Row 3 precedes row 4 deliberately: the enumeration owner refuses a non-null universe
    on an unselected enumerator, so testing the universe first would make unavailable-unselected
    unreachable and collapse two advertised enum members into one.
    """
    if relation == 'vcs-change' and vcs_kind == 'none':
        return 'inapplicable-vcs'
    state, _d, _c = matrix_pair(capability, mode)
    if state == 'UNSUPPORTED-TYPED':
        return 'unsupported-typed'
    if enumerator_status == 'unselected':
        return 'unavailable-unselected'
    if universe is None:
        return 'unavailable-null-universe'
    return 'supported-available'


def source_subject_kind(relation):
    row = _reg(PROJECTION_REGISTRY)['relations'].get(relation) or {}
    return row.get('sourceSubjectKind')


def account_state(applicability, entries, expected_ids=None, covered_ids=None,
                  matrix_deficiency=None, matrix_cause=None):
    """section 5, per account. `entries` are the CoverageResultV3 entries of the matching
    returned partitions; expected/covered are the expected-source-subject join."""
    if applicability == 'supported-available':
        if not entries:
            return ('native-work-incomplete', None, None)    # "Empty -> native-work-incomplete"
        for e in entries:
            if e['coverage'] != 'complete':
                # "Mixed complete+unknown -> not complete"; the PAIR is kept together
                return ('incomplete', e['deficiency'], e['nativeCause'])
        missing = set(expected_ids or ()) - set(covered_ids or ())
        if missing:
            # "every expected source subject ... must be a member of some returned partition ...
            #  Missing expected subjects -> incomplete even if the remaining Coverage is complete"
            return ('incomplete', None, None)
        return ('complete', None, None)
    if applicability == 'unsupported-typed':
        return ('unsupported-typed', matrix_deficiency, matrix_cause)
    if applicability == 'inapplicable-vcs':
        return ('inapplicable', None, None)
    return ('unavailable', None, None)


def cross_source_items(binding, inventories, account_triples, candidate=None):
    """The CROSS-SOURCE ORDER of execution-inputs-contract section 4 (normative, generation 20),
    returned as the ordered list of candidate carrier items.

      1 enumerator / binding carrier -- single item, present only when the row is unavailable
        because the enumerator is unselected or the binding universe is null, and placed BEFORE
        this cell's inventories
      2 inventory -- one item per NON-COMPLETE inventory, in this row's inventoryDigests order
        (x-opensip-order canonical-set)
      3 candidate -- at most one
      4 coverage / account -- one group per owed matrix pair, in the AUTHORED matrix relations
        order; inside one account, the section 5 partition order

    `account_triples` must already be in that authored order. Each item is
    {source, pair, carries} where `carries` is True only when the item actually carries a TYPED
    pair, because "an earlier source that carries NO typed pair does not mask a later one that
    does".
    """
    items = []
    unavailable_binding = (binding['enumerator'].get('status') == 'unselected'
                          or binding.get('universe') is None)
    if unavailable_binding:
        pair = (binding.get('deficiency'), binding.get('nativeCause'))
        items.append({'source': 'enumerator-or-binding', 'pair': pair,
                      'carries': pair[0] is not None})
    for d, iv in inventories:                      # already in inventoryDigests order
        if iv['state'] != 'complete':
            pair = (iv.get('deficiency'), iv.get('nativeCause'))
            items.append({'source': 'inventory', 'ref': d, 'pair': pair,
                          'carries': pair[0] is not None})
    if candidate is not None and candidate.get('state') != 'complete':
        pair = (candidate.get('deficiency'), candidate.get('nativeCause'))
        if pair[0] is None:
            # "failing that, the binding's own DECLARED pair" -- and an AvailableProgramBindingV1
            # declares none, so this stays (null, null) rather than manufacturing one
            pair = (binding.get('deficiency'), binding.get('nativeCause'))
        items.append({'source': 'candidate', 'pair': pair, 'carries': pair[0] is not None})
    for t in account_triples:
        if t[0] in ('complete', 'inapplicable'):
            continue
        items.append({'source': 'coverage-or-account', 'pair': (t[1], t[2]),
                      'carries': t[1] is not None})
    return items


def primary_pair(items):
    """"the FIRST retained source record that ACTUALLY CARRIES a typed pair" -- and explicitly
    (null, null) when none does (pure missing work). Never unzipped across records."""
    for it in items:
        if it['carries']:
            return it['pair']
    return (None, None)


def derive_cell_outcome(binding, inventories, account_triples, candidate=None):
    """section 4 outcome table, row by row, with the generation-20 carrier rule.

    `inventories` are this (cell, program)'s retained (digest, SubjectInventoryV1) pairs in
    inventoryDigests order; `account_triples` are the derived per-account triples in the AUTHORED
    matrix relations order. The state ladder is unchanged; what changed is the carrier: it is the
    first source that actually carries a typed pair in the published cross-source order, and
    (null, null) for pure missing work rather than a manufactured provider-unavailable.
    """
    items = cross_source_items(binding, inventories, account_triples, candidate)
    pair = primary_pair(items)
    if (binding['enumerator'].get('status') == 'unselected'
            or binding.get('universe') is None):
        return ('unavailable',) + pair
    inv_states = [iv['state'] for _d, iv in inventories]
    returned_work = any(t[0] == 'complete' for t in account_triples)
    typed_unavailable = ('unavailable' in inv_states
                         or (candidate is not None and candidate['state'] == 'unavailable'))
    if typed_unavailable and not returned_work:
        return ('unavailable',) + pair
    not_complete = [t for t in account_triples
                    if t[0] in ('incomplete', 'native-work-incomplete')]
    if 'partial' in inv_states or not_complete:
        return ('partial',) + pair
    if candidate is not None and candidate['state'] != 'complete':
        return ('partial',) + pair
    # "every account complete/inapplicable/UNSUPPORTED" -- an unsupported account is an ANSWERED
    # account and does not hold the row open (section 5, generation 20)
    return ('complete', None, None)


def build_accounts_and_outcomes(st, cells, rel_for_cap, inventories, cov_by, coverage_payloads,
                                view_of_universe, provider, stage_ordinal=0, vcs_kind='none'):
    """The HOST side of ExecutionInputsV1 `nativeCoverageAccounts` + `cellOutcomes`, derived.

    cov_by             {(relation, resolution, universe): typed coverage2 id}
    coverage_payloads  {typed coverage2 id: CoverageResultV3}
    view_of_universe   {universe: typed view2 id}  (a single-universe Run passes one entry)
    inventories        [(digest, SubjectInventoryV1)]
    rel_for_cap        RETAINED for call compatibility and no longer read: generation 20 derives
                       the owed relations and their ORDER from the matrix itself

    Generation 20 reconciliation against the newly frozen clauses:
      * applicability is the published FIRST-MATCH precedence, keyed on the CELL's
        (capabilityId, languageMode) matrix state -- not on whether this Run happened to return a
        partition, and not on availability first;
      * `sourceUniverse` is the binding's universe coordinate for EVERY applicability, which is an
        EXTERNAL join the schema cannot state;
      * the owed accounts are the matrix `capabilities[id].relations` array AS AUTHORED, which is
        also the cross-source order authority for the row carrier;
      * the row carrier is the first source ACTUALLY CARRYING a typed pair, and explicitly
        (null, null) for pure missing work.
    """
    accounts, outcomes = [], []
    for ci, c in enumerate(cells):
        for bind in c['programBindings']:
            po = bind['ordinal']
            U = bind.get('universe')
            status = bind['enumerator'].get('status')
            selected = status == 'selected' and U is not None
            invs = [(d, iv) for d, iv in inventories
                    if iv['cellOrdinal'] == ci and iv['programOrdinal'] == po]
            # the row's inventoryDigests order IS the cross-source order for the inventory leg
            invs.sort(key=lambda t: K.C(t[0]))
            triples = []
            # the owed accounts, in the AUTHORED matrix relations order (generation 20)
            for rel, rung in owed_relations(c['capabilityId']):
                appl = applicability_first_match(c['capabilityId'], c['languageMode'], rel,
                                                 status, U, vcs_kind)
                cid = cov_by.get((rel, rung, U)) if U else None
                # only supported-available names envelopes. An UNSUPPORTED-TYPED cell that
                # lawfully returned an unknown CoverageResultV3 still names NOTHING here: that
                # Coverage stays in its view, in the stage capture and in selectedRefs.
                ids = [st.suffix(cid)] if (appl == 'supported-available' and cid) else []
                acc = {'cellOrdinal': ci, 'programOrdinal': po, 'relation': rel,
                       'resolution': rung,
                       # EXTERNAL JOIN: sourceUniverse IS the binding's universe coordinate for
                       # EVERY applicability; carrying no Coverage does not erase it, and a null
                       # binding universe stays null. NOT "null whenever coverageIds is empty".
                       'sourceUniverse': U,
                       # deliberately NOT joined by section 5
                       'targetUniverse': U if ids else None,
                       'applicability': appl, 'coverageIds': ids}
                accounts.append(acc)
                entries, covered = [], set()
                for tid in ([cid] if ids else []):
                    entries.append(coverage_payloads[tid]['entry'])
                    sc = st.objects[st.objects[tid]['scopeId']]
                    covered |= set(sc['subjects'])
                kind = source_subject_kind(rel)
                expected = set()
                for _d, iv in invs:
                    if iv['kind'] == kind:
                        expected |= {r['nativeSubjectId'] for r in iv['rows']}
                mdef = mcause = None
                if appl == 'unsupported-typed':
                    _s, mdef, mcause = matrix_pair(c['capabilityId'], c['languageMode'])
                triples.append(account_state(appl, entries, expected, covered, mdef, mcause))
            state, dfc, cause = derive_cell_outcome(bind, invs, triples)
            null_reason = None
            if not selected:
                null_reason = ('optional-unselected'
                               if bind['enumerator'].get('status') == 'unselected'
                               else 'unavailable-binding')
            outcomes.append({
                'ordinal': len(outcomes), 'cellOrdinal': ci, 'programOrdinal': po,
                'capabilityId': c['capabilityId'], 'languageMode': c['languageMode'],
                'workspaceRoot': c['workspaceRoot'], 'required': c['required'],
                'kinds': c['kinds'], 'universe': U,
                'enumeratorStatus': bind['enumerator'].get('status'),
                'enumeratorClosure': provider if selected else None,
                'state': state, 'deficiency': dfc, 'nativeCause': cause,
                'stageOrdinal': stage_ordinal if selected else None,
                'stageOrdinalNullReason': null_reason,
                'inventoryDigests': sorted([d for d, _ in invs]),
                'viewDigests': ([st.suffix(view_of_universe[U])]
                                if selected and U in view_of_universe else []),
                'candidateResultDigest': None})
    return outcomes, accounts


# ------------------------------------------------------------------ not-applicable RC entry
def rc_not_applicable(stage_terminal='complete'):
    """RC-1: every non-resolved registered rung is `not-applicable`, minted with
    attempted=false, unresolvedEdgeCount=0 and unresolvedEdgeClasses=[]. stageTerminal
    stays free."""
    return {'state': 'not-applicable', 'attempted': False, 'examinedExhaustive': True,
            'stageTerminal': stage_terminal, 'unresolvedEdgeCount': 0,
            'unresolvedEdgeClasses': []}


def closed_world_open(reasons=None):
    return {'exportsClosed': 'unknown', 'entryPointsRecognized': 'none',
            'nonliteralLoading': 'none', 'externalConsumers': 'unknown',
            'dynamicDispatch': 'not-applicable',
            'reasons': list(reasons or []), 'deadCodeRepairEligible': False}


def entry(coverage, closed_world, deficiency=None, native_cause=None,
          rc=None, derivation_kinds=None, confidence=1000000):
    return {'coverage': coverage,
            'resolutionCompleteness': rc or rc_not_applicable(),
            'closedWorld': closed_world,
            'derivationKinds': sorted(derivation_kinds or []),
            'confidenceMillionths': confidence,
            'deficiency': deficiency, 'nativeCause': native_cause}


# ------------------------------------------------------------------ clone body identity
def body_identity_frame(level_id, level_version_hex, language_id, language_version_raw32,
                        payload_bytes):
    """fact-identity-policy.v2 canonicalisationSchema.byteGrammar.domainSeparatedPreimage:
         u8 len||domainTag, u8 len||levelId, u8 len||levelVersion (RAW 32 bytes),
         u8 len||languageId, u8 len||languageVersion, u32be len||payload
    Unframed concatenation is FORBIDDEN."""
    import struct
    def u8(b):
        if len(b) > 255:
            raise ValueError('u8 component overflow: %d bytes' % len(b))
        return bytes([len(b)]) + b
    lv = bytes.fromhex(level_version_hex)
    assert len(lv) == 32
    assert len(language_version_raw32) == 32
    out = b''
    out += u8(b'opensip.fact-identity.v1')
    out += u8(level_id.encode('ascii'))
    out += u8(lv)
    out += u8(language_id.encode('ascii'))
    out += u8(language_version_raw32)
    out += struct.pack('>I', len(payload_bytes)) + payload_bytes
    return out


def l0_payload(span_bytes):
    """L0-verbatim: u32be raw_byte_len || exact body-span bytes. The outer frame adds its
    own u32be payload_len, so payload_len == raw_byte_len + 4 (identity section 3)."""
    import struct
    return struct.pack('>I', len(span_bytes)) + span_bytes


def token_stream(tokens):
    """L1-L3 framedTokenStream: u32be token_count || token*,
    token = u16be kind_id_len || kind_id || u32be value_len || value."""
    import struct
    out = struct.pack('>I', len(tokens))
    for kind, val in tokens:
        kb = kind.encode('utf-8')
        vb = val.encode('utf-8') if isinstance(val, str) else val
        out += struct.pack('>H', len(kb)) + kb + struct.pack('>I', len(vb)) + vb
    return out
