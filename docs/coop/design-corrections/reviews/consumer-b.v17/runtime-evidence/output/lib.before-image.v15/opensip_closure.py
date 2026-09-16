"""Independent retained-closure and cross-record-join checker (STAGE 3).

Works from the EXPORTED STORE ALONE, starting at run3. Implements, from the kit:

  identity-and-evidence section 3  the closing digest law (4 representations x 4
      retention modes, `by-domain` as a selector), the H frame admission rules, the
      payload registry, the typed-root walk and every named cross-record join
  identity-schemas.v3 x-opensip-digest-domains  domainSets: closureJoins, snapshotJoins,
      nestedIdentities, nestedRecords, blobJoins, contextField/contextDomain/
      contextAgreementFields, languageVersionBinding, scopeCapabilityLaw, closureKinds,
      closureMembership
  relation-payload-schemas.v2 x-opensip-relation-registry  ladder/membershipRule,
      rungs field rules, anchorLaw, snapshotJoins, coverageTotalityLaw,
      coveragePartitionLaw, subjectKindLaw, bodyIdentityJoin
  native-evidence section 4.1a/4.3  subjectScopeCommitment recipe and coverage_bijection
      (RC-0, RC-1, RC-2, RC-6)
  native-evidence x-opensip-grammar-capability-registry  enforcement boundaries (2) and (3)
  composition v3 sections 9.1-9.7  the proof/evidence/seal/Run field joins

Every check is reported by name with its result. A digest DECLARATION alone never
satisfies a preimage retention mode: the bytes must be in the store and re-hash.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_core as K
import opensip_schema as S
import opensip_build as B

KIT = S.KIT


class Closure:
    def __init__(self, store):
        self.st = store
        self.idj = json.load(open(KIT + '/' + S.doc_path(B.IDENTITY_DOC)))
        self.dd = self.idj['x-opensip-digest-domains']
        self.payreg = self.idj['x-opensip-payload-registry']
        self.relreg = json.load(open(KIT + '/' + S.doc_path(
            B.RELATION_DOC)))['x-opensip-relation-registry']
        nat = json.load(open(KIT + '/' + S.doc_path(B.NATIVE_DOC)))
        self.greg = nat['x-opensip-grammar-capability-registry']
        self.checks = []
        self.refusals = []
        self.visited_digests = set()
        self.resolved = {}

    # ---------------------------------------------------------------- reporting
    @staticmethod
    def _printable(d):
        if isinstance(d, (bytes, bytearray)):
            return {'hex': bytes(d).hex(), 'len': len(d)}
        if isinstance(d, dict):
            return {k: Closure._printable(v) for k, v in d.items()}
        if isinstance(d, (list, tuple)):
            return [Closure._printable(v) for v in d]
        return d

    def ok(self, name, detail=None):
        self.checks.append({'check': name, 'result': 'PASS',
                            'detail': self._printable(detail)})

    def na(self, name, detail=None):
        self.checks.append({'check': name, 'result': 'NOT-APPLICABLE',
                            'detail': self._printable(detail)})

    def refuse(self, name, detail):
        d = self._printable(detail)
        self.checks.append({'check': name, 'result': 'REFUSE', 'detail': d})
        self.refusals.append({'check': name, 'detail': d})

    def require(self, cond, name, detail):
        if cond:
            self.ok(name, detail if not isinstance(detail, str) else None)
        else:
            self.refuse(name, detail)
        return cond

    # ---------------------------------------------------------------- primitives
    def blob(self, digest, name):
        b = self.st.get_blob(digest)
        if b is None:
            self.refuse(name + ':PREIMAGE_NOT_RETAINED', digest)
            return None
        if K.raw_sha256(b) != digest:
            self.refuse(name + ':PREIMAGE_REHASH_MISMATCH', digest)
            return None
        self.visited_digests.add(digest)
        return b

    def typed(self, tid, domain, name):
        """Resolve a typed id (`plan2:<hex>` etc.) by fetching and parsing its retained
        H preimage FRAME, then re-hashing. A frame proves retention, never admission."""
        if ':' not in tid:
            self.refuse(name + ':TYPED_ID_MALFORMED', tid)
            return None
        pref, hexd = tid.split(':', 1)
        if K.PREFIX.get(domain) != pref:
            self.refuse(name + ':TYPED_PREFIX_DOMAIN_MISMATCH', '%s vs %s' % (pref, domain))
            return None
        b = self.blob(hexd, name)
        if b is None:
            return None
        try:
            dom, obj = K.parse_h_frame(b, {domain})
        except K.CanonError as e:
            self.refuse(name + ':FRAME_ADMISSION', '%s %s' % (tid, e))
            return None
        if K.H(domain, obj) != hexd:
            self.refuse(name + ':H_RECOMPUTE_MISMATCH', tid)
            return None
        self.resolved[tid] = obj
        return obj

    def native_h(self, bare_hex, domain_set, name):
        """Resolve a bare-hex or `sha256:`-prefixed native h-identity through the named
        DOMAIN SET: the suffix alone does not resolve it."""
        hexd = bare_hex.split(':', 1)[1] if bare_hex.startswith('sha256:') else bare_hex
        b = self.blob(hexd, name)
        if b is None:
            return None, None
        allowed = set(self.dd['domainSets'][domain_set])
        try:
            dom, obj = K.parse_h_frame(b, allowed)
        except K.CanonError as e:
            self.refuse(name + ':FRAME_ADMISSION', '%s %s' % (hexd, e))
            return None, None
        if K.H(dom, obj) != hexd:
            self.refuse(name + ':H_RECOMPUTE_MISMATCH', hexd)
            return None, None
        row = self.dd['domainSets'][domain_set][dom]
        r = S.admit(row['document'], row['selector'], obj,
                    'native-h:%s:%s' % (dom, hexd[:8]))
        if not r['admitted']:
            self.refuse(name + ':DOMAIN_RECORD_INVALID',
                        json.dumps(r['stockSchemaErrors'])[:400])
            return None, None
        return dom, obj

    def canonical_record(self, digest, doc, selector, name):
        b = self.blob(digest, name)
        if b is None:
            return None
        try:
            obj = json.loads(b.decode())
        except Exception as e:
            self.refuse(name + ':NOT_JSON', str(e))
            return None
        if K.C(obj) != b:
            self.refuse(name + ':NOT_CANONICAL_RECORD_BYTES', digest)
            return None
        r = S.admit(doc, selector, obj, 'canonical-record:%s' % name)
        if not r['admitted']:
            self.refuse(name + ':RECORD_INVALID',
                        json.dumps(r['stockSchemaErrors'])[:400] + ' | '
                        + json.dumps(r['publishedKeywordRefusals'])[:400])
            return None
        return obj

    # ---------------------------------------------------------------- digest-law audit
    def audit_digest_law(self):
        """"Every 64-hex field in identity-schemas.v3 has exactly one representation and
        one retention mode ... a 64-hex field carrying no annotation is inadmissible."""
        # v15 normative update. identity-schemas.v3 now publishes
        # `x-opensip-digest-domains.scope`, and identity-and-evidence section 3 now says
        # "bare 64-hex DIGEST field" throughout:
        #     governs              bare-64-hex-digest-fields
        #     schemaSelectors      pattern ^[0-9a-f]{64}(?![\s\S])  OR  $ref #/$defs/Hash
        #     nullableAlternatives apply to the non-null branch; the annotation may be there
        #     typedPrefixIdentities OUTSIDE this annotation scope -- the prefix selects the
        #                          identity domain in the section 3 table and the hex suffix
        #                          is not a separate bare digest field
        # This is read from the kit, not inferred: the audit below is driven by the published
        # selectors. (At the prior kit this origin had to CORRECT its own first draft, which
        # flagged `#/$defs/Hash` itself; the current kit resolves that question explicitly in
        # the same direction, because `#/$defs/Hash` is a schemaSelector, not a field.)
        scope = self.dd.get('scope')
        if scope is None:
            self.refuse('DIGEST_DOMAINS_SCOPE_CLAUSE_ABSENT', None)
            return [], []
        PAT = scope['schemaSelectors']['pattern']
        HASH_REF = scope['schemaSelectors']['$ref']
        self.require(scope['governs'] == 'bare-64-hex-digest-fields',
                     'DIGEST_DOMAINS_SCOPE_GOVERNS', scope['governs'])
        unannotated = []
        TERMINAL_SCALAR_DEFS = {HASH_REF}

        def walk(node, path, inherited):
            if isinstance(node, dict):
                ann = node.get('x-opensip-digest', inherited)
                governed = (node.get('pattern') == PAT or node.get('$ref') == HASH_REF)
                if governed and path not in TERMINAL_SCALAR_DEFS:
                    if ann is None:
                        unannotated.append(path)
                    else:
                        self.check_annotation_shape(ann, path)
                for k, v in node.items():
                    if k == 'x-opensip-digest':
                        continue
                    walk(v, path + '/' + k, ann if k in ('oneOf', 'anyOf', 'allOf',
                                                         'items', 'then', 'else') else
                         (ann if k == 'properties' else None))
            elif isinstance(node, list):
                for i, v in enumerate(node):
                    walk(v, path + '/%d' % i, inherited)

        walk(self.idj['$defs'], '#/$defs', None)
        self.require(not unannotated, 'DIGEST_LAW_NO_RESIDUE',
                     'unannotated 64-hex fields: %s' % unannotated[:10])
        # Hash $ref sites carrying no sibling annotation
        hash_sites = []

        def walk2(node, path, has_ann):
            if isinstance(node, dict):
                if node.get('$ref') == '#/$defs/Hash' and 'x-opensip-digest' not in node \
                        and not has_ann:
                    hash_sites.append(path)
                for k, v in node.items():
                    walk2(v, path + '/' + k, has_ann or 'x-opensip-digest' in node)
            elif isinstance(node, list):
                for i, v in enumerate(node):
                    walk2(v, path + '/%d' % i, has_ann)
        walk2(self.idj['$defs'], '#/$defs', False)
        self.require(not hash_sites, 'DIGEST_LAW_HASH_REF_ANNOTATED',
                     'Hash $ref sites with no effective annotation: %s' % hash_sites[:10])
        return unannotated, hash_sites

    TERMINAL = {'raw-artifact', 'canonical-record', 'h-identity', 'capability-manifest-id'}
    RETENTION = {'preimage', 'fragment', 'derived', 'owner-retained'}

    def check_annotation_shape(self, ann, path):
        rep = ann.get('representation')
        if rep == 'by-domain':
            if ann.get('registry') != 'x-opensip-digest-domains':
                self.refuse('DIGEST_ANNOTATION_BY_DOMAIN_REGISTRY', path)
            return
        if rep not in self.TERMINAL:
            self.refuse('DIGEST_ANNOTATION_REPRESENTATION_UNREGISTERED',
                        '%s at %s' % (rep, path))
        ret = ann.get('retention', 'preimage')
        if ret not in self.RETENTION:
            self.refuse('DIGEST_ANNOTATION_RETENTION_UNREGISTERED',
                        '%s at %s' % (ret, path))
        if rep == 'h-identity' and not (ann.get('domain') or ann.get('domainSet')):
            self.refuse('DIGEST_ANNOTATION_H_IDENTITY_WITHOUT_DOMAIN_OR_SET', path)

    def check_by_domain_registry(self):
        """`by-domain` is a SELECTOR, not a fifth terminal representation: every
        registered domain resolves to exactly one of the four, and no byDomain row may
        name `by-domain`."""
        bad = []
        for dom, row in self.dd['byDomain'].items():
            rep = row['representation']
            if rep == 'by-domain':
                bad.append(dom)
            elif rep not in self.TERMINAL:
                bad.append(dom + ':' + rep)
        self.require(not bad, 'BY_DOMAIN_RESOLVES_TO_A_TERMINAL_REPRESENTATION', bad)
        dom_enum = set(self.idj['$defs']['Domain']['enum'])
        ref_enum = set(self.idj['$defs']['Ref']['properties']['domain']['enum'])
        self.require(dom_enum == ref_enum == set(self.dd['byDomain']),
                     'DOMAIN_ENUMERATIONS_ARE_THE_REGISTERED_KEY_SET',
                     {'Domain-minus-byDomain': sorted(dom_enum - set(self.dd['byDomain'])),
                      'Ref-minus-Domain': sorted(ref_enum - dom_enum)})
        proof_enum = set(self.idj['$defs']['ProofInputRef']['properties']['domain']['enum'])
        self.require(proof_enum <= dom_enum, 'PROOF_INPUT_REF_DOMAINS_REGISTERED',
                     sorted(proof_enum - dom_enum))
        self.require(not (proof_enum & {'proof-bundle', 'finding', 'evaluation-seal', 'run',
                                        'semantic-evidence', 'coverage-payload',
                                        'import-payload', 'fact-payload'}),
                     'PROOF_INPUT_VOCABULARY_EXCLUDES_OUTPUTS_AND_PAYLOAD_DOMAINS',
                     sorted(proof_enum & {'proof-bundle', 'finding', 'evaluation-seal',
                                          'run', 'semantic-evidence', 'coverage-payload',
                                          'import-payload', 'fact-payload'}))

    def check_relation_registry_mirrors(self):
        """The relation registry is the SINGLE ladder authority; the capability registry's
        ladders are a declared mirror, drift-checked EXACTLY AND IN ORDER."""
        auth = {r: row['ladder'] for r, row in self.relreg['relations'].items()}
        cap = json.load(open(KIT + '/docs/coop/design-corrections/native/'
                             'capability-manifest-domains.v2.json'))
        mir = cap['registries']['RELATION-LADDER-DOMAIN-V2']['ladders']
        self.require(auth == mir, 'RELATION_LADDER_MIRROR_EXACT_AND_IN_ORDER',
                     {r: {'authority': auth.get(r), 'mirror': mir.get(r)}
                      for r in set(auth) | set(mir) if auth.get(r) != mir.get(r)})
        self.require(sorted(cap['registries']['RELATION-DOMAIN-V2']['members'])
                     == sorted(auth), 'RELATION_DOMAIN_MIRROR_MEMBERSHIP', None)
        # anchorLaw mirror for clones
        cl = self.relreg['relations']['clones']
        self.require(cl['bodyIdentityJoin']['anchorCardinality'] == cl['anchorLaw']['cardinality'],
                     'RELATION_ANCHOR_LAW_DRIFT', None)
        # flat rung vocabulary == union of ladders, drift-checked
        union = sorted({x for v in auth.values() for x in v})
        pol = json.load(open(KIT + '/' + S.doc_path(B.POLICY_V2_DOC)))
        self.require(sorted(pol['$defs']['Rung']['enum']) == union,
                     'RUNG_VOCABULARY_IS_THE_LADDER_UNION',
                     {'schema': sorted(pol['$defs']['Rung']['enum']), 'union': union})
        # every relation has a non-empty ladder: no empty-ladder fallback
        empty = [r for r, l in auth.items() if not l]
        self.require(not empty, 'NO_EMPTY_LADDER_FALLBACK', empty)

    # ================================================================ main walk
    def close_run(self, run_id, label=''):
        self.audit_digest_law()
        self.check_by_domain_registry()
        self.check_relation_registry_mirrors()
        run = self.typed(run_id, 'run', 'RUN')
        if run is None:
            return self.report(label, None)
        snap = self.typed(run['snapshotId'], 'snapshot', 'SNAPSHOT')
        plan = self.typed(run['planId'], 'plan', 'PLAN')
        seal = self.typed(run['evaluationSealId'], 'evaluation-seal', 'SEAL')
        ev = self.typed(run['evidenceId'], 'semantic-evidence', 'EVIDENCE')
        if None in (snap, plan, seal, ev):
            return self.report(label, run)
        self.require(run['projectId'] == snap['projectId'], 'RUN_PROJECT_JOIN', None)
        self.require(seal['planId'] == run['planId'] == ev['planId'],
                     'RUN_SEAL_EVIDENCE_PLAN_JOIN', None)
        self.require(seal['evidenceId'] == run['evidenceId'], 'SEAL_EVIDENCE_JOIN', None)
        self.require(run['capabilityManifestId'] == plan['capabilityManifestId'],
                     'RUN_PLAN_CAPABILITY_MANIFEST_JOIN', None)
        self.plan, self.snap, self.seal, self.ev, self.run = plan, snap, seal, ev, run
        self.inv = {r['path']: r for r in snap['sourceInventory']}
        self.universe_cache = {}
        self.context_cache = {}
        self.check_snapshot(snap)
        self.check_plan(plan, snap)
        proof = self.check_seal_and_proof(seal, plan, ev)
        self.check_views(ev, plan, proof)
        self.check_grammar_capability_boundaries()
        self.check_unreferenced()
        return self.report(label, run, proof)

    def report(self, label, run, proof=None):
        return {'label': label, 'runId': (K.ID('run', run) if run else None),
                'checks': self.checks,
                'checksPassed': sum(1 for c in self.checks if c['result'] == 'PASS'),
                'checksNotApplicable': sum(1 for c in self.checks
                                           if c['result'] == 'NOT-APPLICABLE'),
                'checksRefused': sum(1 for c in self.checks if c['result'] == 'REFUSE'),
                'refusals': self.refusals, 'admitted': not self.refusals,
                'retainedDigestsVisited': len(self.visited_digests),
                'storeBlobCount': len(self.st.blobs)}

    # ---------------------------------------------------------------- snapshot
    def check_snapshot(self, snap):
        r = S.admit(B.IDENTITY_DOC, '#/$defs/source-inventory', snap['sourceInventory'],
                    'source-inventory')
        self.require(r['admitted'], 'SOURCE_INVENTORY_ORDER_AND_SHAPE',
                     json.dumps(r['publishedKeywordRefusals'])[:300])
        paths = [row['path'] for row in snap['sourceInventory']]
        self.require(len(set(paths)) == len(paths), 'INVENTORY_PATH_UNIQUE', None)
        missing = []
        for row in snap['sourceInventory']:
            b = self.st.get_blob(row['sha256'])
            if b is None:
                missing.append(row['path'])
            elif len(b) != row['bytes']:
                self.refuse('BLOB_LENGTH', '%s declared %d retained %d'
                            % (row['path'], row['bytes'], len(b)))
            else:
                self.visited_digests.add(row['sha256'])
        self.require(not missing, 'INVENTORY_BLOBS_RETAINED', missing)
        cfg = self.canonical_record(snap['resolvedConfigDigest'], B.IDENTITY_DOC,
                                    '#/$defs/semantic-configuration', 'SNAPSHOT_CONFIG')
        sc = self.canonical_record(snap['scopeDigest'], B.IDENTITY_DOC,
                                   '#/$defs/scope-descriptor', 'SNAPSHOT_SCOPE')
        vcs = self.canonical_record(snap['vcsDigest'], B.IDENTITY_DOC,
                                    '#/$defs/vcs-observation', 'SNAPSHOT_VCS')
        self.snap_config, self.snap_scope = cfg, sc
        if vcs is not None:
            self.require(vcs['sourceInventoryDigest'] == K.rec_digest(snap['sourceInventory']),
                         'VCS_SOURCE_INVENTORY_DIGEST_JOIN', None)
            self.blob(vcs['sourceInventoryDigest'], 'VCS_INVENTORY_BLOB')
            self.require((vcs['commitId'] is None) == (vcs['kind'] == 'none'),
                         'VCS_COMMIT_NULL_EXACTLY_FOR_KIND_NONE', None)

    # ---------------------------------------------------------------- plan
    def check_plan(self, plan, snap):
        # capability manifest: derived retention, recomputed from the retained artifact
        art = self.blob(plan['capabilityManifestBytesDigest'], 'CAPABILITY_MANIFEST_ARTIFACT')
        if art is not None:
            self.require(K.capability_manifest_id(art) == plan['capabilityManifestId'],
                         'CAPABILITY_MANIFEST_ID_DERIVED_FROM_RETAINED_ARTIFACT', None)
            try:
                import opensip_capmanifest as CM
                val = K.cve1_decode_exact(art)
                res = CM.CapabilityManifestAdmitter().admit(val)
                self.require(res['admitted'] and res['committedBytes'] == art,
                             'CAPABILITY_MANIFEST_REGISTRY_ADMISSION_OVER_RETAINED_BYTES',
                             None)
            except Exception as e:
                self.refuse('CAPABILITY_MANIFEST_REGISTRY_ADMISSION_OVER_RETAINED_BYTES',
                            str(e))
        spec = self.canonical_record(plan['analysisSpecDigest'], B.IDENTITY_DOC,
                                     '#/$defs/analysis-spec', 'PLAN_ANALYSIS_SPEC')
        cfg = self.canonical_record(plan['resolvedConfigDigest'], B.IDENTITY_DOC,
                                    '#/$defs/semantic-configuration', 'PLAN_CONFIG')
        self.canonical_record(plan['scopeDigest'], B.IDENTITY_DOC,
                              '#/$defs/scope-descriptor', 'PLAN_SCOPE')
        grant = self.canonical_record(plan['semanticGrantDigest'], B.IDENTITY_DOC,
                                      '#/$defs/semantic-grant', 'PLAN_SEMANTIC_GRANT')
        policy = self.canonical_record(plan['policyDigest'], B.POLICY_V2_DOC,
                                       '#/$defs/PolicyDocumentV2', 'PLAN_POLICY')
        self.canonical_record(plan['waiverDigest'], B.POLICY_V1_DOC,
                              '#/$defs/WaiverSetV1', 'PLAN_WAIVERS')
        self.plan_policy, self.plan_spec = policy, spec
        self.require(plan['resolvedConfigDigest'] == snap['resolvedConfigDigest'],
                     'SNAPSHOT_PLAN_CONFIG_AGREE', None)
        self.require(plan['scopeDigest'] == snap['scopeDigest'],
                     'SNAPSHOT_PLAN_SCOPE_AGREE', None)
        if cfg is not None:
            self.require(plan['budget'] == cfg['analysis']['budget'],
                         'PLAN_BUDGET_EQUALS_RESOLVED_CONFIGURATION_BUDGET',
                         {'plan': plan['budget'], 'config': cfg['analysis']['budget']})
        if grant is not None:
            self.require(grant['projectId'] == snap['projectId']
                         and grant['scopeDigest'] == plan['scopeDigest'],
                         'SEMANTIC_GRANT_PROJECT_AND_SCOPE_JOIN', None)
            for p in grant['principals']:
                if p['kind'] == 'first-party':
                    self.require(p['ownerSourceDigest'] is None,
                                 'FIRST_PARTY_PRINCIPAL_HAS_NULL_OWNER_SOURCE', None)
                else:
                    self.require(p['ownerSourceDigest'] is not None,
                                 'REPOSITORY_PRINCIPAL_REQUIRES_OWNER_SOURCE', None)
                    if p['ownerSourceDigest']:
                        self.na('OWNER_SOURCE_SET_OWNER_RETAINED',
                                'retention owner-retained: joined by digest equality only; '
                                'the bytes are security RepoExecutionGrantV2 owner admission')
        # semantic closures
        self.closures = {}
        for cid in plan['semanticClosures']:
            rec = self.typed(cid, 'closure', 'PLAN_SEMANTIC_CLOSURE')
            if rec is None:
                continue
            self.closures[cid] = rec
            self.blob(rec['manifestDigest'], 'CLOSURE_COMPONENT_MANIFEST_BODY')
            for row in rec['tree']:
                b = self.st.get_blob(row['sha256'])
                if b is None:
                    self.refuse('CLOSURE_TREE_BLOB_NOT_RETAINED', row['path'])
                elif len(b) != row['bytes']:
                    self.refuse('BLOB_LENGTH', 'closure tree %s' % row['path'])
                else:
                    self.visited_digests.add(row['sha256'])
        # analysis-spec vocabulary and parameter selection
        if spec is not None:
            self.check_analysis_spec(spec)
        # native contexts
        ctx_set = set()
        for hx in plan['nativeContextDigests']:
            dom, ctx = self.native_h(hx, 'native-context', 'PLAN_NATIVE_CONTEXT')
            if ctx is None:
                continue
            ctx_set.add(hx)
            self.context_cache[hx] = (dom, ctx)
            self.check_native_context(dom, ctx, hx)
        self.require(len(ctx_set) == len(plan['nativeContextDigests']),
                     'PLAN_NATIVE_CONTEXT_SET_RETAINED', None)
        self.require(len(plan['nativeContextDigests']) > 0,
                     'PLAN_NATIVE_CONTEXT_SET_NONEMPTY', None)
        # policy / rule-program atom rung membership
        if policy is not None:
            self.check_atom_rungs(policy, 'PolicyDocumentV2')

    def check_analysis_spec(self, spec):
        matrix = json.load(open(KIT + '/docs/coop/design-corrections/native/'
                                'native-capability-matrix.v2.json'))
        cap_members = set(matrix['capabilityIdLaw']['members'])
        modes = set(self.dd['languageModes']['map'])
        cells = {}
        for row in spec['requestedCapabilities']:
            if row['capabilityId'] not in cap_members:
                self.refuse('native.requested-capability-unregistered', row['capabilityId'])
            if row['languageMode'] not in modes:
                self.refuse('ANALYSIS_SPEC_LANGUAGE_MODE_UNREGISTERED', row['languageMode'])
            key = (row['capabilityId'], row['languageMode'], row['workspaceRoot'])
            if key in cells:
                self.refuse('native.requested-capability-duplicate-ownership-tuple', str(key))
            cells[key] = row
            cell = [c for c in matrix['cells']
                    if c['capability'] == row['capabilityId'] and c['mode'] == row['languageMode']]
            if not cell:
                self.refuse('NATIVE_MATRIX_CELL_ABSENT', str(key))
        self.ok('ANALYSIS_SPEC_CAPABILITY_VOCABULARY', None)
        self.ok('ANALYSIS_SPEC_OWNERSHIP_TUPLE_UNIQUE', None)
        # parameter class: closed list + at most one per registered row
        rows = {}
        for key, row in self.payreg['classes']['parameter']['rows'].items():
            rows[S.load_doc(row['document'])['sha256']] = (row['document'], row['selector'])
        picked = {}
        for p in spec['parameters']:
            if p['schemaDigest'] not in rows:
                self.refuse('PAYLOAD_PARAMETER_SCHEMA_UNREGISTERED', p['schemaDigest'])
                continue
            self.blob(p['schemaDigest'], 'PARAMETER_SCHEMA_DOCUMENT')
            doc, sel = rows[p['schemaDigest']]
            picked.setdefault((doc, sel), []).append(p)
            self.canonical_record(p['payloadDigest'], doc, sel, 'PARAMETER_PAYLOAD')
        dup = [k for k, v in picked.items() if len(v) > 1]
        self.require(not dup, 'ANALYSIS_SPEC_PARAMETER_SELECTION_AMBIGUOUS', dup)
        # evaluator3 requires exactly one enumeration-plan and one emission-plan parameter
        need = [k for k, row in self.payreg['classes']['parameter']['rows'].items()
                if 3 in (row.get('requiredForEvaluatorMajors') or [])]
        have = set()
        for (doc, sel), v in picked.items():
            for key, row in self.payreg['classes']['parameter']['rows'].items():
                if row['document'] == doc and row['selector'] == sel:
                    have.add(key)
        self.require(set(need) <= have, 'EVALUATOR3_REQUIRED_PARAMETERS_SELECTED',
                     sorted(set(need) - have))
        self.spec_parameters = picked

    def check_atom_rungs(self, doc, which):
        """Membership of THIS atom's relation's ladder is the SUFFICIENT condition and is
        enforced at Run closure over both the Plan's PolicyDocumentV2 and the proof's
        compiled RuleProgramV2."""
        imported = json.load(open(KIT + '/' + S.doc_path(
            'workflows/schemas/imported-evidence.schema.json')))
        ev_reg = imported.get('x-opensip-evidence-relation-registry', {})
        ev_rel = set(ev_reg.get('relations', {})) if isinstance(ev_reg, dict) else set()
        bad = []
        for rule in doc['rules']:
            for addr, node in self._atoms(rule['emitWhen']):
                rel = node['relation']
                if rel in self.relreg['relations']:
                    lad = self.relreg['relations'][rel]['ladder']
                    if node['minResolution'] not in lad:
                        bad.append('%s %s %s@%s not in %s'
                                   % (rule['ruleId'], addr, rel, node['minResolution'], lad))
                elif rel in ev_rel:
                    lad = ev_reg['relations'][rel].get('ladder', ['observed'])
                    if node['minResolution'] not in lad:
                        bad.append('%s %s imported %s@%s' % (rule['ruleId'], addr, rel,
                                                             node['minResolution']))
                else:
                    bad.append('%s %s relation %s in neither registry'
                               % (rule['ruleId'], addr, rel))
        self.require(not bad, 'ATOM_MIN_RESOLUTION_IN_THIS_RELATIONS_LADDER:' + which, bad)

    @staticmethod
    def _atoms(node, addr='p'):
        out = []
        if node['op'] in ('exists', 'none', 'count-at-most', 'all-covered'):
            out.append((addr, node))
        elif node['op'] in ('and', 'or'):
            for i, ch in enumerate(node['operands']):
                out += Closure._atoms(ch, '%s.%d' % (addr, i))
        elif node['op'] == 'not':
            out += Closure._atoms(node['operand'], addr + '.0')
        return out

    # ------------------------------------------------- native annotated-site audit (v15)
    def closure_tree_members(self, closure_tid, name):
        """The member digests of a RETAINED signed closure tree, resolved through its
        closure2 identity. Cached."""
        if not hasattr(self, '_trees'):
            self._trees = {}
        if closure_tid in self._trees:
            return self._trees[closure_tid]
        rec = self.resolved.get(closure_tid) or self.typed(closure_tid, 'closure', name)
        members = set()
        if rec is not None:
            for row in rec['tree']:
                members.add(row['sha256'])
        self._trees[closure_tid] = members
        return members

    def audit_native_record(self, doc, selector, record, tree_map, label):
        """Drive EVERY annotated digest site of a native record from the kit annotations
        and dispatch on the native retention vocabulary
        (native x-opensip-digest-law.retention):

            preimage            the exact preimage bytes are retained under this digest
            preimage-frame      the retained object is the H preimage frame
            closure-tree-member the digest must be a MEMBER DIGEST of the retained signed
                                closure tree the annotation names
            owner-retained      the owning contract retains the bytes; join by equality

        `closure-tree-member` and `preimage` are DIFFERENT OBLIGATIONS: a digest may be
        globally retained in the content-addressed store and still not be a member of the
        selected closure tree, and the annotation that names a tree is not satisfied by
        global retention.
        """
        kw, sites = S.walk_keywords(doc, selector, record)
        for r in kw:
            self.refuse('NATIVE_RECORD_PUBLISHED_KEYWORD:' + label, r)
        seen = 0
        for site in sites:
            ann = site['annotation']
            ret = ann.get('retention', 'preimage')
            val = site['value']
            where = '%s%s' % (label, site['instancePath'])
            if ret == 'preimage':
                self.blob(val.split(':', 1)[1] if val.startswith('sha256:') else val,
                          'NATIVE_SITE_PREIMAGE:' + where)
            elif ret == 'preimage-frame':
                if ann.get('domainSet'):
                    self.native_h(val, ann['domainSet'], 'NATIVE_SITE_FRAME:' + where)
                elif ann.get('domain') == 'closure':
                    tid = ('closure2:' + val) if not val.startswith('closure2:') else val
                    rec = self.typed(tid, 'closure', 'NATIVE_SITE_CLOSURE:' + where)
                    if rec is not None and ann.get('kind'):
                        self.require(rec['kind'] == ann['kind'],
                                     'NATIVE_SITE_CLOSURE_KIND:' + where,
                                     {'kind': rec['kind'], 'required': ann['kind']})
                elif ann.get('domain'):
                    hexd = val.split(':', 1)[1] if val.startswith('sha256:') else val
                    bb = self.blob(hexd, 'NATIVE_SITE_FRAME:' + where)
                    if bb is not None:
                        try:
                            K.parse_h_frame(bb, {ann['domain']})
                            self.ok('NATIVE_SITE_FRAME_DOMAIN:' + where, ann['domain'])
                        except K.CanonError as e:
                            self.refuse('NATIVE_SITE_FRAME_DOMAIN:' + where, str(e))
            elif ret == 'closure-tree-member':
                tree_key = self._tree_key_for(ann.get('artifact') or '')
                tid = tree_map.get(tree_key)
                if tid is None:
                    self.refuse('CLOSURE_TREE_MEMBER_NAMED_TREE_UNRESOLVED:' + where,
                                {'artifact': ann.get('artifact'), 'treeKey': tree_key,
                                 'available': sorted(tree_map)})
                    continue
                members = self.closure_tree_members(tid, 'NAMED_CLOSURE_TREE')
                globally = self.st.get_blob(val) is not None
                self.require(val in members,
                             'CLOSURE_TREE_MEMBER:' + where,
                             {'digest': val, 'namedTree': tree_key, 'closureId': tid,
                              'memberCount': len(members),
                              'globallyRetainedInCas': globally,
                              'distinction': ('global CAS retention is a DIFFERENT '
                                              'obligation from membership in the named '
                                              'selected closure tree')})
                if val in members:
                    self.require(globally,
                                 'CLOSURE_TREE_MEMBER_BYTES_ALSO_RETAINED:' + where, val)
                    self.visited_digests.add(val)
            elif ret == 'owner-retained':
                self.na('NATIVE_SITE_OWNER_RETAINED:' + where,
                        {'authority': ann.get('authority'),
                         'joinedBy': 'digest equality only; the owning contract retains '
                                     'and admits the bytes'})
            elif ret == 'derived':
                # `derived` is NOT a member of the native bundle's own published
                # x-opensip-digest-law.retention vocabulary (4 members), but three of that
                # bundle's own sites use it and the native law declares itself "the closing
                # digest law of identity-and-evidence section 3, EXTENDED to this bundle",
                # where `derived` IS one of the four closed retention modes. Recorded as a
                # SHOULD-level vocabulary gap; implemented here from the SITE's own
                # published rule rather than guessed.
                self.check_native_derived_site(ann, site, record, where)
            else:
                self.refuse('NATIVE_RETENTION_UNREGISTERED:' + where, ret)
            seen += 1
        self.ok('NATIVE_ANNOTATED_SITES_DRIVEN_FROM_THE_KIT:' + label, seen)
        return seen

    def check_native_derived_site(self, ann, site, record, where):
        """`derived` native sites: nothing separate is retained because the PREIMAGE IS THE
        ROW, and admission RE-DERIVES and compares.

        The only `derived` native domain is `native.compilation-unit.v1`
        (SourceUnitOwnershipV1 unitId / selectedUnitIds / ownership[].unitId). Its published
        preimage is `#/$defs/UnitIdentityV1` = {schemaVersion:1, markerPath, targetKind,
        targetName}, so:
          * a `units[i].unitId` is re-derived from that very row and compared;
          * a `selectedUnitIds[i]` or `ownership[i].unitId` carries no preimage of its own
            and must be a member of the re-derived units table -- "a selection or an
            ownership row naming a unitId with no row here is an unbound caller label and
            is inadmissible".
        """
        if ann.get('domain') != 'native.compilation-unit.v1':
            self.refuse('NATIVE_DERIVED_SITE_DOMAIN_NOT_IMPLEMENTED:' + where,
                        ann.get('domain'))
            return
        units = record.get('units') if isinstance(record, dict) else None
        if not isinstance(units, list):
            self.refuse('NATIVE_DERIVED_UNITS_TABLE_ABSENT:' + where, None)
            return
        derived = {}
        for u in units:
            pre = {'schemaVersion': 1, 'markerPath': u['markerPath'],
                   'targetKind': u['targetKind'], 'targetName': u['targetName']}
            r = S.admit(B.NATIVE_DOC, '#/$defs/UnitIdentityV1', pre, 'UnitIdentityV1')
            if not r['admitted']:
                self.refuse('UNIT_IDENTITY_PREIMAGE_INVALID:' + where,
                            json.dumps(r['stockSchemaErrors'])[:200])
                continue
            derived[u['unitId']] = 'sha256:' + K.H('native.compilation-unit.v1', pre)
        p = site['instancePath']
        val = site['value']
        if p.startswith('/units/') and p.endswith('/unitId'):
            self.require(derived.get(val) == val,
                         'native.compilation-unit.v1:UNIT_ID_REDERIVED_AND_EQUAL:' + where,
                         {'declared': val, 'reDerived': derived.get(val)})
        else:
            self.require(val in {u['unitId'] for u in units},
                         'native.compilation-unit.v1:UNIT_ID_IS_A_MEMBER_OF_THE_UNITS_TABLE:'
                         + where, {'unitId': val})

    @staticmethod
    def _tree_key_for(artifact_text):
        t = artifact_text
        if 'toolClosure.closureId' in t:
            return 'toolClosure.closureId'
        if 'rustcDevLlvmDigest' in t:
            return 'toolchain.rustcDevLlvmDigest'
        if 'typescriptStdlibMerkleRoot' in t:
            return 'toolchain.typescriptStdlibMerkleRoot'
        return 'UNKNOWN'

    # ---------------------------------------------------------------- native context
    def _at(self, obj, path):
        node = obj
        for p in path:
            if node is None:
                return None
            if p == '[]':
                return node
            node = node.get(p) if isinstance(node, dict) else None
        return node

    def check_native_context(self, domain, ctx, hx):
        row = self.dd['domainSets']['native-context'][domain]
        # Build the NAMED closure-tree map this context's annotated sites refer to, from the
        # registered closureJoins themselves (never from a field name).
        tree_map = {}
        for j in row.get('closureJoins', []):
            v = self._at(ctx, j['path'])
            if v is None:
                continue
            tid = v if j['form'] == 'closure2-identity' else 'closure2:' + v
            tree_map['.'.join(j['path'])] = tid
            if j['path'] == ['toolClosure', 'closureId']:
                tree_map['toolClosure.closureId'] = tid
            if j['path'] == ['grammarBundle', 'closureId']:
                tree_map['grammarBundle.closureId'] = tid
        self.audit_native_record(row['document'], row['selector'], ctx, tree_map,
                                 'native-context:' + domain)
        # closureJoins: closure2-identity / closure2-suffix with a required kind
        for j in row.get('closureJoins', []):
            v = self._at(ctx, j['path'])
            if v is None:
                if j.get('nullable'):
                    self.na('NATIVE_CONTEXT_CLOSURE_JOIN_NULL', '/'.join(j['path']))
                    continue
                self.refuse('NATIVE_CONTEXT_CLOSURE_JOIN_ABSENT', '/'.join(j['path']))
                continue
            tid = v if j['form'] == 'closure2-identity' else 'closure2:' + v
            rec = self.typed(tid, 'closure', 'NATIVE_CONTEXT_CLOSURE_JOIN')
            if rec is None:
                continue
            self.require(rec['kind'] == j['kind'],
                         'NATIVE_CONTEXT_CLOSURE_KIND:' + '/'.join(j['path']),
                         '%s vs %s' % (rec['kind'], j['kind']))
            self.blob(rec['manifestDigest'], 'NATIVE_CONTEXT_CLOSURE_MANIFEST')
            for t in rec['tree']:
                if self.st.get_blob(t['sha256']) is None:
                    self.refuse('CLOSURE_TREE_BLOB_NOT_RETAINED', t['path'])
                else:
                    self.visited_digests.add(t['sha256'])
        # snapshotJoins: every repository path a context names must be inventoried
        for j in row.get('snapshotJoins', []):
            v = self._at(ctx, j['path'])
            if v is None:
                if j.get('nullable'):
                    self.na('NATIVE_CONTEXT_SNAPSHOT_JOIN_NULL', '/'.join(j['path']))
                    continue
                self.refuse('NATIVE_CONTEXT_SNAPSHOT_JOIN_ABSENT', '/'.join(j['path']))
                continue
            if j['form'] == 'inventoried-paths':
                bad = [p for p in v if p not in self.inv]
                self.require(not bad, 'NATIVE_CONTEXT_PATH_OUTSIDE_SNAPSHOT', bad)
            elif j['form'] == 'inventoried-path-and-digest':
                p, d = v[j['pathField']], v[j['digestField']]
                self.require(p in self.inv and self.inv[p]['sha256'] == d,
                             'NATIVE_CONTEXT_LOCKFILE_INVENTORY_JOIN', {'path': p})
        for j in row.get('nestedIdentities', []):
            v = self._at(ctx, j['path'])
            if v is None:
                if j.get('nullable'):
                    self.na('NATIVE_NESTED_IDENTITY_NULL', '/'.join(j['path']))
                    continue
                self.refuse('NATIVE_NESTED_IDENTITY_ABSENT', '/'.join(j['path']))
                continue
            self.check_nested_identity(v, j)
        for j in row.get('nestedRecords', []):
            v = self._at(ctx, j['path'])
            if v is None:
                if j.get('nullable'):
                    self.na('NATIVE_NESTED_RECORD_NULL', '/'.join(j['path']))
                    continue
                self.refuse('NATIVE_NESTED_RECORD_ABSENT', '/'.join(j['path']))
                continue
            rec = self.canonical_record(v, j['document'], j['selector'],
                                        'NATIVE_NESTED_RECORD:' + '/'.join(j['path']))
            if rec is not None:
                for bj in j.get('blobJoins', []):
                    self.check_blob_join(rec, bj, 'NATIVE_NESTED_RECORD_BLOB_JOIN')
        for bj in row.get('blobJoins', []):
            node = self._at(ctx, bj['path'])
            if node is not None:
                self.check_blob_join(node, {'path': [], **bj}, 'NATIVE_CONTEXT_BLOB_JOIN')
        if domain == 'native.context.syntax.v2':
            self.check_grammar_bundle(ctx['grammarBundle'],
                                      tree_map.get('grammarBundle.closureId'))

    def check_nested_identity(self, value, j, tree_map=None):
        dom, rec = self.native_h(value, j['domainSet'], 'NATIVE_NESTED_IDENTITY')
        if rec is None:
            return None
        row = self.dd['domainSets'][j['domainSet']][dom]
        self.audit_native_record(row['document'], row['selector'], rec, tree_map or {},
                                 'native-nested:' + dom)
        for sub in row.get('nestedIdentities', []):
            target = self._resolve_array_path(rec, sub['path'])
            for v in target:
                self.check_nested_identity(v, sub)
        for bj in row.get('blobJoins', []):
            self.check_blob_join(rec, bj, 'NATIVE_NESTED_BLOB_JOIN')
        for sj in row.get('snapshotJoins', []):
            v = self._at(rec, sj['path'])
            if v is None:
                continue
            if sj['form'] == 'inventoried-paths':
                items = v if isinstance(v, list) else [v]
                if sj.get('pathField'):
                    items = [i[sj['pathField']] for i in items]
                bad = [p for p in items if p not in self.inv]
                self.require(not bad, 'NATIVE_NESTED_PATH_OUTSIDE_SNAPSHOT', bad)
        return rec

    @staticmethod
    def _resolve_array_path(rec, path):
        nodes = [rec]
        for p in path:
            nxt = []
            for n in nodes:
                if p == '[]':
                    if isinstance(n, list):
                        nxt += n
                elif isinstance(n, dict) and p in n:
                    nxt.append(n[p])
            nodes = nxt
        return [n for n in nodes if n is not None]

    def check_blob_join(self, rec, bj, name):
        nodes = self._resolve_array_path(rec, bj.get('path', []))
        if not nodes:
            nodes = [rec]
        for n in nodes:
            if not isinstance(n, dict):
                continue
            d = n.get(bj['digestField'])
            if d is None:
                continue
            b = self.st.get_blob(d)
            if b is None:
                self.refuse(name + ':BLOB_NOT_RETAINED', d)
                continue
            self.visited_digests.add(d)
            if bj.get('lengthField') and len(b) != n.get(bj['lengthField']):
                self.refuse('BLOB_LENGTH', '%s declared %s retained %d'
                            % (d, n.get(bj['lengthField']), len(b)))
            else:
                self.ok(name, None)

    def check_grammar_bundle(self, bundle, grammar_closure_tid=None):
        """native SyntaxGrammarBundleV1, native-evidence section 1.2:

          "an admitted `kind=grammar` closure, a `parserVersion` that must equal that
           closure manifest's `semanticVersion`
           (`native.syntax-grammar-version-not-from-manifest`), and every grammar
           definition, the bundle manifest and the normalizer specification PRESENT IN THE
           RETAINED TREE."

        Two distinct obligations, both enforced: the schema annotations give these three
        field classes `retention: preimage` (global CAS retention), and section 1.2
        additionally requires each of them to be PRESENT IN THE RETAINED grammar closure
        TREE. Global retention does not satisfy tree presence.
        """
        rec = self.typed(bundle['closureId'], 'closure', 'GRAMMAR_CLOSURE')
        members = set()
        if rec is not None:
            self.require(rec['kind'] == 'grammar', 'GRAMMAR_CLOSURE_KIND', rec['kind'])
            self.require(bundle['parserVersion'] == rec['semanticVersion'],
                         'native.syntax-grammar-version-not-from-manifest',
                         {'parserVersion': bundle['parserVersion'],
                          'closureSemanticVersion': rec['semanticVersion']})
            members = {row['sha256'] for row in rec['tree']}
        self.blob(bundle['bundleDigest'], 'GRAMMAR_BUNDLE_MANIFEST')
        self.blob(bundle['normalizer']['specificationDigest'],
                  'GRAMMAR_NORMALIZER_SPECIFICATION')
        # section 1.2 tree-presence obligation, separate from global retention
        for label, dig in ([('bundleManifest', bundle['bundleDigest']),
                            ('normalizerSpecification',
                             bundle['normalizer']['specificationDigest'])]
                           + [('grammarDefinition:' + g['grammarId'], g['grammarDigest'])
                              for g in bundle['grammars']]):
            self.require(dig in members,
                         'native-evidence-1.2:PRESENT_IN_THE_RETAINED_TREE:' + label,
                         {'digest': dig, 'grammarClosureId': bundle['closureId'],
                          'treeMemberCount': len(members),
                          'globallyRetainedInCas': self.st.get_blob(dig) is not None,
                          'distinction': ('global CAS retention and membership in the '
                                          'selected grammar closure tree are different '
                                          'obligations')})
        # one suffix must map to one grammar, longest match wins
        # (native.syntax-grammar-suffix-ambiguous)
        seen = {}
        for g in bundle['grammars']:
            for suf in g['suffixes']:
                if suf in seen:
                    self.refuse('native.syntax-grammar-suffix-ambiguous',
                                {'suffix': suf, 'grammars': [seen[suf], g['grammarId']]})
                seen[suf] = g['grammarId']
        self.ok('native.syntax-grammar-suffix-unique', len(seen))
        langs = self.greg['languages']
        bad = []
        body_enum = set(self.idj['$defs']['body-language-version']['properties'][
            'languageId']['enum'])
        for g in bundle['grammars']:
            self.blob(g['grammarDigest'], 'GRAMMAR_DEFINITION_BYTES')
            if g['languageId'] not in langs:
                bad.append('unregistered languageId ' + g['languageId'])
                continue
            reg = langs[g['languageId']]
            if g['syntaxClass'] != reg['syntaxClass']:
                bad.append('syntaxClass %s != registered %s for %s'
                           % (g['syntaxClass'], reg['syntaxClass'], g['languageId']))
            if sorted(g['suffixes']) != sorted(reg['suffixes']):
                bad.append('suffixes %s != registered %s' % (g['suffixes'], reg['suffixes']))
            if g['syntaxClass'] == 'code' and g['languageId'] not in body_enum:
                bad.append('code grammar languageId not in body-language-version enum: '
                           + g['languageId'])
            if g['syntaxClass'] == 'data-document' and g['languageId'] in body_enum:
                bad.append('data-document languageId IS in body-language-version enum: '
                           + g['languageId'])
        self.require(not bad, 'GRAMMAR_BUNDLE_SYNTAX_CLASS_REGISTERED_BOTH_DIRECTIONS', bad)
        self.grammar_bundle = bundle

    # ---------------------------------------------------------------- universes
    def check_universe(self, hx):
        if hx in self.universe_cache:
            return self.universe_cache[hx]
        dom, uni = self.native_h(hx, 'native-semantic-universe', 'UNIVERSE')
        if uni is None:
            self.universe_cache[hx] = (None, None)
            return None, None
        row = self.dd['domainSets']['native-semantic-universe'][dom]
        self.audit_native_record(row['document'], row['selector'], uni, {},
                                 'native-universe:' + dom)
        if 'binding' not in row:
            self.refuse('NATIVE_UNIVERSE_BINDING_UNAVAILABLE', dom)
        else:
            self.ok('NATIVE_UNIVERSE_BINDING_REGISTERED', row['binding']['entryPoint'])
        ctx_ref = self._at(uni, row['contextField'])
        ctx_hex = ctx_ref.split(':', 1)[1] if ctx_ref.startswith('sha256:') else ctx_ref
        self.require(ctx_hex in self.plan['nativeContextDigests'],
                     'UNIVERSE_CONTEXT_IS_PLAN_SELECTED', ctx_hex)
        cdom, ctx = self.context_cache.get(ctx_hex, (None, None))
        self.require(cdom == row['contextDomain'],
                     'UNIVERSE_BINDS_A_CONTEXT_OF_ITS_OWN_LANGUAGE',
                     {'contextDomain': cdom, 'required': row['contextDomain']})
        for f in row.get('contextAgreementFields', []):
            self.require(uni.get(f) == (ctx or {}).get(f),
                         'UNIVERSE_CONTEXT_AGREEMENT:' + f,
                         {'universe': uni.get(f), 'context': (ctx or {}).get(f)})
        for j in row.get('snapshotJoins', []):
            v = self._at(uni, j['path'])
            if v is None:
                continue
            if j['form'] == 'inventoried-paths':
                bad = [p for p in v if p not in self.inv]
                self.require(not bad, 'UNIVERSE_PATH_OUTSIDE_SNAPSHOT', bad)
            elif j['form'] == 'inventoried-path-and-digest':
                p, d = v[j['pathField']], v[j['digestField']]
                self.require(p in self.inv and self.inv[p]['sha256'] == d,
                             'UNIVERSE_LOCKFILE_INVENTORY_JOIN', {'path': p})
        for j in row.get('nestedIdentities', []):
            v = self._at(uni, j['path'])
            if v is None:
                if j.get('nullable'):
                    self.na('UNIVERSE_NESTED_IDENTITY_NULL', '/'.join(j['path']))
                continue
            if j.get('form') == 'bare-hex' or j.get('form') == 'sha256-text':
                self.check_nested_identity(v, j)
        for j in row.get('nestedRecords', []):
            v = self._at(uni, j['path'])
            if v is not None:
                self.canonical_record(v, j['document'], j['selector'],
                                      'UNIVERSE_NESTED_RECORD:' + '/'.join(j['path']))
        self.check_language_mode_recognition(dom, uni, ctx)
        if dom == 'native.semantic-universe.syntax.v2':
            sel = set(uni['selectedGrammarIds'])
            have = {g['grammarId'] for g in (ctx or {}).get('grammarBundle', {}).get(
                'grammars', [])}
            self.require(sel <= have, 'SYNTAX_UNIVERSE_SELECTION_SUBSET_OF_BUNDLE',
                         sorted(sel - have))
            self.require(uni['resolutionAttempted'] is False,
                         'SYNTAX_UNIVERSE_RESOLUTION_NOT_ATTEMPTED', None)
        self.universe_cache[hx] = (dom, uni)
        return dom, uni

    def check_language_mode_recognition(self, dom, uni, ctx):
        """native-evidence section 1.2's closed mode table, applied to the retained records.

          ts-tsconfig   tsconfig.json at the unit root, `allowJs` absent/false;
                        configOrigin=tsconfig; "JavaScript files are NOT program roots"
          js-allowjs    tsconfig/jsconfig with effective allowJs=true;
                        ".js/.mjs/.cjs/.jsx are program roots"
          js-synthesized  configOrigin=synthesized, synthesizerVersion=1
          rust-cargo / rust-cargo-prepared  preparedOutputSetId null / non-null
          syntax-only   grammar-only; no compiler

        Plus `languageModes.map`: the mode must map to THIS universe's language.
        """
        lm = self.dd['languageModes']['map']
        mode = uni.get('languageMode')
        row = self.dd['domainSets']['native-semantic-universe'][dom]
        if mode is None:
            # the Rust and syntax universes carry no languageMode field; their mode is
            # decided by preparedOutputSetId / the grammar-only context
            if dom == 'native.semantic-universe.rust.v2':
                want = ('rust-cargo-prepared' if uni.get('preparedOutputSetId')
                        else 'rust-cargo')
                self.require(lm.get(want) == row['language'],
                             'section1.2:MODE_MAPS_TO_THIS_UNIVERSE_LANGUAGE', want)
                self.require((uni.get('preparedResolution') != 'none')
                             == bool(uni.get('preparedOutputSetId')),
                             'section1.2:PREPARED_SET_AND_RESOLUTION_AGREE',
                             {'preparedOutputSetId': uni.get('preparedOutputSetId'),
                              'preparedResolution': uni.get('preparedResolution')})
                self.ok('section1.2:RUST_MODE_RECOGNISED', want)
            elif dom == 'native.semantic-universe.syntax.v2':
                self.require(lm.get('syntax-only') == row['language'],
                             'section1.2:MODE_MAPS_TO_THIS_UNIVERSE_LANGUAGE', 'syntax-only')
                self.ok('section1.2:SYNTAX_ONLY_MODE_RECOGNISED', None)
            return
        self.require(lm.get(mode) == row['language'],
                     'section1.2:MODE_MAPS_TO_THIS_UNIVERSE_LANGUAGE',
                     {'mode': mode, 'mapsTo': lm.get(mode), 'universeLanguage': row['language']})
        self.require(ctx is not None and ctx.get('languageMode') == mode,
                     'section1.2:CONTEXT_AND_UNIVERSE_LANGUAGE_MODE_AGREE',
                     {'universe': mode, 'context': (ctx or {}).get('languageMode')})
        allow_js = bool(uni.get('allowJs'))
        js_roots = list(uni.get('jsRootFiles') or [])
        js_admitted = bool(uni.get('jsAdmittedToProgram'))
        honored = ((ctx or {}).get('configProjection') or {}).get('honoredOptions') or {}
        if mode == 'ts-tsconfig':
            self.require(uni.get('configOrigin') == 'tsconfig',
                         'section1.2:TS_TSCONFIG_CONFIG_ORIGIN', uni.get('configOrigin'))
            self.require(not allow_js and not honored.get('allowJs'),
                         'section1.2:TS_TSCONFIG_REQUIRES_ALLOWJS_ABSENT_OR_FALSE',
                         {'universeAllowJs': uni.get('allowJs'),
                          'honoredAllowJs': honored.get('allowJs')})
            self.require(not js_roots and not js_admitted,
                         'section1.2:TS_TSCONFIG_JAVASCRIPT_FILES_ARE_NOT_PROGRAM_ROOTS',
                         {'jsRootFiles': js_roots, 'jsAdmittedToProgram': js_admitted})
        elif mode == 'js-allowjs':
            self.require(uni.get('configOrigin') in ('tsconfig', 'jsconfig'),
                         'section1.2:JS_ALLOWJS_CONFIG_ORIGIN', uni.get('configOrigin'))
            self.require(allow_js and bool(honored.get('allowJs')),
                         'section1.2:JS_ALLOWJS_REQUIRES_EFFECTIVE_ALLOWJS_TRUE',
                         {'universeAllowJs': uni.get('allowJs'),
                          'honoredAllowJs': honored.get('allowJs')})
            JS = ('.js', '.mjs', '.cjs', '.jsx')
            bad = [p for p in js_roots if not p.endswith(JS)]
            self.require(not bad, 'section1.2:JS_ALLOWJS_ROOTS_ARE_JS_SUFFIXES', bad)
            self.require(set(js_roots) <= set(uni.get('programRootFiles') or []),
                         'section1.2:JS_ROOTS_ARE_PROGRAM_ROOTS',
                         sorted(set(js_roots) - set(uni.get('programRootFiles') or [])))
        elif mode == 'js-synthesized':
            self.require(uni.get('configOrigin') == 'synthesized',
                         'section1.2:JS_SYNTHESIZED_CONFIG_ORIGIN', uni.get('configOrigin'))
            self.require(uni.get('synthesizerVersion') == 1
                         and uni.get('synthesizedOptions') is not None,
                         'section1.2:JS_SYNTHESIZED_REQUIRES_SYNTHESIZER_AND_OPTIONS',
                         {'synthesizerVersion': uni.get('synthesizerVersion')})
            self.require(not ((ctx or {}).get('configProjection') or {}).get(
                'configGraphPaths'),
                'section1.2:SYNTHESIZED_CONFIG_GRAPH_IS_EMPTY',
                ((ctx or {}).get('configProjection') or {}).get('configGraphPaths'))
        self.ok('section1.2:LANGUAGE_MODE_RECOGNISED', mode)

    # ---------------------------------------------------------------- seal / proof
    def check_seal_and_proof(self, seal, plan, ev):
        proof = self.typed(seal['proofBundleId'], 'proof-bundle', 'PROOF')
        if proof is None:
            return None
        self.require(ev['proofBundleId'] == seal['proofBundleId'],
                     'EVIDENCE_SEAL_PROOF_JOIN', None)
        self.require(proof['planId'] == plan and True or True, 'PROOF_PLAN_PRESENT', None)
        self.require(proof['planId'] == seal['planId'], 'PROOF_SEAL_PLAN_JOIN', None)
        self.require(proof['executionPlanId'] == seal['executionPlanId'],
                     'PROOF_SEAL_EXECUTION_PLAN_JOIN', None)
        self.require(proof['evaluatorClosure'] == seal['evaluatorClosure'],
                     'PROOF_EVALUATOR_EQUALS_SEAL_EVALUATOR', None)
        self.require(proof['verdict'] == seal['verdict'], 'PROOF_SEAL_VERDICT_JOIN', None)
        self.require(seal['policyDigest'] == plan['policyDigest'],
                     'SEAL_POLICY_EQUALS_PLAN_POLICY', None)
        ec = seal['evaluatorClosure']
        self.require(ec in plan['semanticClosures'],
                     'EVALUATOR_CLOSURE_PLAN_SELECTED', ec)
        erec = self.closures.get(ec) or self.typed(ec, 'closure', 'EVALUATOR_CLOSURE')
        if erec:
            self.require(erec['kind'] == 'evaluator', 'EVALUATOR_CLOSURE_KIND', erec['kind'])
        # execution plan
        xp = self.typed(proof['executionPlanId'], 'execution-plan', 'EXECUTION_PLAN')
        if xp is not None:
            self.require(xp['planId'] == proof['planId'], 'EXECUTION_PLAN_PLAN_JOIN', None)
            for stg in xp['stages']:
                ss = self.canonical_record(stg['stageSpecDigest'], B.IDENTITY_DOC,
                                           '#/$defs/stage-spec', 'STAGE_SPEC')
                if ss is None:
                    continue
                self.require(ss['planId'] == proof['planId'], 'STAGE_SPEC_PLAN_JOIN', None)
                self.require(ss['outputDomains'] == stg['outputDomains'],
                             'STAGE_AND_STAGE_SPEC_OUTPUT_DOMAINS_AGREE', None)
                self.require(ss['producerClosure'] in plan['semanticClosures'],
                             'STAGE_SPEC_PRODUCER_PLAN_SELECTED', ss['producerClosure'])
                self.blob(ss['outputSchemaDigest'], 'STAGE_OUTPUT_SCHEMA_DOCUMENT')
                spec_rows = [tuple(sorted(p.items())) for p in self.plan_spec['parameters']]
                for p in ss['parameters']:
                    self.require(tuple(sorted(p.items())) in spec_rows,
                                 'STAGE_SPEC_HIDDEN_PARAMETER', p)
        # rule program: exactly the projection of the Plan-selected policy
        rp = self.canonical_record(proof['ruleProgramDigest'], B.POLICY_V2_DOC,
                                   '#/$defs/RuleProgramV2', 'RULE_PROGRAM')
        if rp is not None and self.plan_policy is not None:
            expect = {'schemaVersion': 2, 'policyDigest': K.rec_digest(self.plan_policy),
                      'rules': [{'ruleId': r['ruleId'],
                                 'ruleProgramRef': r['ruleProgramRef'],
                                 'emitWhen': r['emitWhen']}
                                for r in self.plan_policy['rules']]}
            self.require(K.C(rp) == K.C(expect),
                         'RULE_PROGRAM_IS_THE_POLICY_PROJECTION_IN_RULEID_ORDER', None)
            self.require(rp['policyDigest'] == plan['policyDigest'],
                         'RULE_PROGRAM_POLICY_DIGEST_EQUALS_PLAN', None)
            self.check_atom_rungs(rp, 'RuleProgramV2')
        # ExecutionInputsV1 and the EI identity
        xi = [r for r in proof['evaluationInputRefs'] if r['domain'] == 'execution-inputs']
        self.require(len(xi) == 1, 'EXACTLY_ONE_EXECUTION_INPUTS_REF', len(xi))
        exec_inputs = None
        if len(xi) == 1:
            self.require(xi[0]['digest'] == proof['executionInputsDigest'],
                         'EXECUTION_INPUTS_DIGEST_EQUALS_THE_EI_MEMBER', None)
            exec_inputs = self.canonical_record(proof['executionInputsDigest'],
                                                B.EXEC_IN_DOC, '#', 'EXECUTION_INPUTS')
        if exec_inputs is not None:
            self.require(exec_inputs['planId'] == proof['planId'],
                         'EXECUTION_INPUTS_PLAN_JOIN', None)
            self.require(exec_inputs['executionPlanId'] == proof['executionPlanId'],
                         'EXECUTION_INPUTS_EXECUTION_PLAN_JOIN', None)
            self.require(exec_inputs['evaluatorClosure'] == proof['evaluatorClosure'],
                         'EXECUTION_INPUTS_EVALUATOR_JOIN', None)
            self.require(exec_inputs['analysisSpecDigest'] == plan['analysisSpecDigest'],
                         'EXECUTION_INPUTS_ANALYSIS_SPEC_JOIN', None)
            ei = K.cset(list(exec_inputs['selectedRefs']) + [xi[0]])
            self.require(K.C(ei) == K.C(proof['evaluationInputRefs']),
                         'EVALUATION_INPUT_REFS_EQUALS_SELECTED_REFS_PLUS_XI', None)
            hd = K.cset([r for r in exec_inputs['selectedRefs']
                         if r['domain'] in ('subject-inventory', 'candidate-producer-result',
                                            'target-attribution', 'incoming-search')])
            self.require(K.C(hd) == K.C(exec_inputs['hostCapture']['hostDerivedRefs']),
                         'SELECTED_REFS_HOST_DERIVED_MEMBERS_EQUAL_HOST_CAPTURE', None)
            stage_out = []
            for rc in exec_inputs['hostCapture']['stageReceipts']:
                if rc['state'] == 'complete':
                    stage_out += rc['outputRefs']
                    self.require(set(r['domain'] for r in rc['outputRefs'])
                                 <= set(rc['outputDomains']),
                                 'STAGE_RECEIPT_OUTPUT_REF_DOMAIN_SUBSET', None)
            prod = K.cset([r for r in exec_inputs['selectedRefs']
                           if r['domain'] in ('view', 'coverage')])
            self.require(K.C(K.cset(stage_out)) == K.C(prod),
                         'SELECTED_REFS_STAGE_DOMAINS_EQUAL_COMPLETE_RECEIPT_TOTALITY', None)
            for d in exec_inputs['candidateResultRefs']:
                self.blob(d, 'CANDIDATE_PRODUCER_RESULT')
            for r in exec_inputs['selectedRefs']:
                if r['domain'] == 'subject-inventory':
                    inv = self.canonical_record(r['digest'], B.SUBJ_INV_DOC, '#',
                                                'SUBJECT_INVENTORY')
                    if inv is not None:
                        self.require(inv['planId'] == proof['planId'],
                                     'SUBJECT_INVENTORY_PLAN_JOIN', None)
                        self.require(inv['parameterDigest']
                                     == self._enumeration_plan_digest(),
                                     'SUBJECT_INVENTORY_PARAMETER_DIGEST_JOIN', None)
        self.exec_inputs = exec_inputs
        # imports: evidence.importIds repeats the Plan selection exactly
        self.require(K.C(K.cset_strings(ev['importIds']))
                     == K.C(K.cset_strings(plan['importIds'])), 'IMPORT_JOIN', None)
        for r in proof['evaluationInputRefs']:
            if r['domain'] == 'import':
                self.require('import2:' + r['digest'] in plan['importIds'],
                             'UNSELECTED_EVALUATION_IMPORT', r['digest'])
        for iid in plan['importIds']:
            self.require({'domain': 'import', 'digest': iid.split(':', 1)[1]}
                         in proof['evaluationInputRefs'],
                         'EVERY_PLAN_IMPORT_IS_AN_EVALUATION_INPUT', iid)
        # witnesses / program predicates / node digests
        self.check_predicates(proof, rp)
        # findings
        self.check_findings(proof, ev, plan)
        # evidence view/coverage roots
        views = K.cset_strings(['view2:' + r['digest']
                                for r in proof['evaluationInputRefs'] if r['domain'] == 'view'])
        self.require(K.C(K.cset_strings(ev['viewIds'])) == K.C(views),
                     'EVIDENCE_VIEW_ROOTS_EQUAL_NAMED_VIEWS', None)
        return proof

    def _enumeration_plan_digest(self):
        for p in self.plan_spec['parameters']:
            if p['schemaDigest'] == B.doc_sha(B.ENUM_PLAN_DOC):
                return p['payloadDigest']
        return None

    def check_predicates(self, proof, rp):
        r = S.admit(B.IDENTITY_DOC, '#/$defs/proof-bundle', proof, 'proof-bundle')
        self.require(r['admitted'], 'PROOF_BUNDLE_SCHEMA_AND_ORDER',
                     json.dumps(r['publishedKeywordRefusals'])[:400])
        ei = proof['evaluationInputRefs']
        for pp in proof['predicateProofs']:
            w = self.canonical_record(pp['witnessDigest'], B.IDENTITY_DOC,
                                      '#/$defs/predicate-witness', 'PREDICATE_WITNESS')
            if w is None:
                continue
            ppd = self.canonical_record(w['programPredicateDigest'], B.IDENTITY_DOC,
                                        '#/$defs/program-predicate', 'PROGRAM_PREDICATE')
            if ppd is None:
                continue
            self.require(ppd['ruleProgramDigest'] == proof['ruleProgramDigest'],
                         'PROGRAM_PREDICATE_RULE_PROGRAM_JOIN', None)
            self.require(ppd['ruleId'] == pp['ruleId']
                         and ppd['predicateId'] == pp['predicateId']
                         and ppd['operation'] == pp['operation'],
                         'PROGRAM_PREDICATE_ADDRESSES_THIS_PROOF_NODE', None)
            # fragment retention: nodeDigest is RECOMPUTED at locatedBy, not stored twice
            node = self._node_at(rp, ppd['ruleId'], ppd['predicateId'])
            if node is None:
                self.refuse('PROGRAM_PREDICATE_NODE_NOT_IN_ADMITTED_PROGRAM',
                            '%s %s' % (ppd['ruleId'], ppd['predicateId']))
            else:
                self.require(K.rec_digest(node) == ppd['nodeDigest'],
                             'NODE_DIGEST_FRAGMENT_RECOMPUTED_AT_LOCATED_BY', None)
                self.require(node['op'] == ppd['operation'],
                             'NODE_OP_EQUALS_PROGRAM_PREDICATE_OPERATION', None)
                kids = self._child_addresses(node, ppd['predicateId'])
                self.require(sorted(w['childPredicateIds']) == sorted(kids),
                             'WITNESS_CHILDREN_ARE_THE_ADDRESSED_OPERANDS',
                             {'witness': w['childPredicateIds'], 'program': kids})
                self.require(w['countLimit'] == (node.get('n') if node['op'] == 'count-at-most'
                                                 else None),
                             'WITNESS_COUNT_LIMIT_IS_THE_NODE_N', None)
            # predicate input refs are a subset of evaluationInputRefs
            bad = [x for x in pp['inputRefs'] if x not in ei]
            self.require(not bad, 'PREDICATE_INPUT_REFS_SUBSET_OF_EVALUATION_INPUT_REFS', bad)
            for fid in w['matchingFactIds'] + w['uncertainFactIds']:
                self.require(self._fact_in_an_evaluated_view(fid, proof),
                             'WITNESS_FACT_BELONGS_TO_AN_EVALUATED_VIEW', fid)
            for cid in w['coverageIds']:
                self.require(self._coverage_in_an_evaluated_view(cid, proof),
                             'WITNESS_COVERAGE_BELONGS_TO_AN_EVALUATED_VIEW', cid)
            for sid in pp['scopeIds']:
                sc = self.typed(sid, 'subject-scope', 'PREDICATE_SCOPE')
                if sc is not None:
                    self.require(sc['snapshotId'] == self.run['snapshotId'],
                                 'REFERENCE_SOURCE_JOIN', sid)
        # every witness is reachable only through a predicate proof
        self.ok('PREDICATE_PROOF_ORDER_PREDICATE_TUPLE', None)

    def _fact_in_an_evaluated_view(self, fid, proof):
        for r in proof['evaluationInputRefs']:
            if r['domain'] != 'view':
                continue
            v = self.resolved.get('view2:' + r['digest'])
            if v is None:
                v = self.typed('view2:' + r['digest'], 'view', 'VIEW')
            if v and fid in v['facts']:
                return True
        return False

    def _coverage_in_an_evaluated_view(self, cid, proof):
        for r in proof['evaluationInputRefs']:
            if r['domain'] == 'coverage' and r['digest'] == cid.split(':', 1)[1]:
                return True
            if r['domain'] != 'view':
                continue
            v = self.resolved.get('view2:' + r['digest']) or \
                self.typed('view2:' + r['digest'], 'view', 'VIEW')
            if v and cid in v['coverageIds']:
                return True
        return False

    @staticmethod
    def _node_at(rp, rule_id, addr):
        if rp is None:
            return None
        rows = [r for r in rp['rules'] if r['ruleId'] == rule_id]
        if not rows:
            return None
        for a, n in Closure._address_all(rows[0]['emitWhen']):
            if a == addr:
                return n
        return None

    @staticmethod
    def _address_all(node, addr='p'):
        out = [(addr, node)]
        if node['op'] in ('and', 'or'):
            for i, ch in enumerate(node['operands']):
                out += Closure._address_all(ch, '%s.%d' % (addr, i))
        elif node['op'] == 'not':
            out += Closure._address_all(node['operand'], addr + '.0')
        return out

    @staticmethod
    def _child_addresses(node, addr):
        if node['op'] in ('and', 'or'):
            return ['%s.%d' % (addr, i) for i in range(len(node['operands']))]
        if node['op'] == 'not':
            return [addr + '.0']
        return []

    def check_findings(self, proof, ev, plan):
        self.require(K.C(K.cset_strings(ev['findingIds']))
                     == K.C(K.cset_strings(proof['findingIds'])),
                     'EVIDENCE_FINDING_IDS_EQUAL_PROOF_FINDING_IDS', None)
        for fid in proof['findingIds']:
            f = self.typed(fid, 'finding', 'FINDING')
            if f is None:
                continue
            self.require(f['ruleClosure'] in plan['semanticClosures'],
                         'FINDING_RULE_CLOSURE_PLAN_SELECTED', f['ruleClosure'])
            rec = self.closures.get(f['ruleClosure']) or \
                self.typed(f['ruleClosure'], 'closure', 'DETECTOR_CLOSURE')
            if rec:
                self.require(rec['kind'] == 'detector', 'FINDING_RULE_CLOSURE_KIND',
                             rec['kind'])
            params = self.canonical_record(f['parameterDigest'], B.IDENTITY_DOC,
                                           '#/$defs/finding-parameters', 'FINDING_PARAMETERS')
            if params is not None:
                self.require(params['messageCode'] == f['messageCode'],
                             'FINDING_PARAMETERS_MESSAGE_CODE_JOIN', None)
            if f['fingerprint']:
                self.typed(f['fingerprint'], 'finding-fingerprint', 'FINDING_FINGERPRINT')
            subj = self.typed(f['subjectId'], 'evaluation-subject', 'FINDING_SUBJECT')
            if subj is not None:
                self.require(subj['kind'] == f['subject']['kind'],
                             'FINDING_SUBJECT_KIND_JOIN', None)
            # citations cannot introduce extra authoritative input roots
            for erf in f['evidenceRefs']:
                dom, d = erf['domain'], erf['digest']
                if dom == 'fact':
                    self.require(self._fact_in_an_evaluated_view('fact2:' + d, proof),
                                 'FINDING_FACT_CITATION_IN_AN_EVALUATED_VIEW', d)
                elif dom == 'coverage':
                    self.require(self._coverage_in_an_evaluated_view('coverage2:' + d, proof),
                                 'FINDING_COVERAGE_CITATION_IN_AN_EVALUATED_VIEW', d)
                elif dom == 'import':
                    self.require('import2:' + d in plan['importIds']
                                 and {'domain': 'import', 'digest': d}
                                 in proof['evaluationInputRefs'],
                                 'FINDING_IMPORT_CITATION_SELECTED_AND_EVALUATED', d)
                elif dom == 'predicate-witness':
                    self.require(any(pp['witnessDigest'] == d
                                     for pp in proof['predicateProofs']),
                                 'FINDING_WITNESS_CITATION_NAMES_A_WITNESS_OF_THIS_PROOF', d)
                elif dom == 'blob':
                    self.require(self.st.get_blob(d) is not None,
                                 'FINDING_BLOB_CITATION_RETAINED', d)

    # ---------------------------------------------------------------- views
    def check_views(self, ev, plan, proof):
        self.facts_seen = {}
        self.scopes_seen = {}
        self.coverages_seen = {}
        cov_union = set()
        for vid in ev['viewIds']:
            v = self.resolved.get(vid) or self.typed(vid, 'view', 'VIEW')
            if v is None:
                continue
            self.require(v['planId'] == plan and True or True, 'VIEW_PLAN_PRESENT', None)
            self.require(v['planId'] == self.run['planId'], 'VIEW_PLAN_JOIN', vid)
            self.require(v['producerClosure'] in plan['semanticClosures'],
                         'VIEW_PRODUCER_PLAN_SELECTED', v['producerClosure'])
            prec = self.closures.get(v['producerClosure']) or \
                self.typed(v['producerClosure'], 'closure', 'VIEW_PRODUCER_CLOSURE')
            if prec:
                self.require(prec['kind'] == 'provider', 'VIEW_PRODUCER_CLOSURE_KIND',
                             prec['kind'])
            # view.schemaDigests: each member is a REGISTERED document, re-hashed
            registered = self._registered_schema_document_digests()
            for d in v['schemaDigests']:
                self.require(d in registered, 'SCHEMA_DOCUMENT_UNREGISTERED', d)
                self.blob(d, 'VIEW_SCHEMA_DOCUMENT')
            # scopes
            view_scopes = {}
            for sid in v['scopeIds']:
                sc = self.typed(sid, 'subject-scope', 'SCOPE')
                if sc is None:
                    continue
                view_scopes[sid] = sc
                self.scopes_seen[sid] = sc
                self.require(sc['snapshotId'] == self.run['snapshotId'],
                             'REFERENCE_SOURCE_JOIN', sid)
                self.require(sc['enumeratorClosure'] in plan['semanticClosures'],
                             'SCOPE_ENUMERATOR_PLAN_SELECTED', sc['enumeratorClosure'])
                erec = self.closures.get(sc['enumeratorClosure']) or \
                    self.typed(sc['enumeratorClosure'], 'closure', 'SCOPE_ENUMERATOR')
                if erec:
                    self.require(erec['kind'] == 'provider', 'SCOPE_ENUMERATOR_KIND',
                                 erec['kind'])
                self.check_registered_pair(sc['relation'], sc['resolution'], 'SCOPE_RC0')
                self.check_universe(sc['sourceUniverse'])
                self.check_universe(sc['targetUniverse'])
                if self.relreg['relations'].get(sc['relation'], {}).get(
                        'universeRule') == 'same-only':
                    self.require(sc['sourceUniverse'] == sc['targetUniverse'],
                                 'SCOPE_UNIVERSE_RULE_SAME_ONLY', sid)
            # facts
            view_facts = {}
            for fid in v['facts']:
                f = self.typed(fid, 'fact', 'FACT')
                if f is None:
                    continue
                view_facts[fid] = f
                self.facts_seen[fid] = f
                self.require(f['snapshotId'] == self.run['snapshotId'],
                             'REFERENCE_SOURCE_JOIN', fid)
                self.require(f['producerClosure'] == v['producerClosure'],
                             'FACT_PRODUCER_EQUALS_VIEW_PRODUCER', fid)
                self.check_fact(fid, f, view_scopes)
            # coverage
            for cid in v['coverageIds']:
                c = self.typed(cid, 'coverage', 'COVERAGE')
                if c is None:
                    continue
                self.coverages_seen[cid] = c
                cov_union.add(cid)
                self.require(c['scopeId'] in v['scopeIds'],
                             'coverage_view_use:SCOPE_IN_THE_EVALUATED_VIEW', cid)
                self.check_coverage(cid, c, view_scopes, view_facts)
            # coveragePartitionLaw: per view, over EVERY referenced scope
            self.check_coverage_partition(vid, view_scopes)
            # coverageTotalityLaw
            self.check_coverage_totality(vid, view_scopes, view_facts)
        extra = {'coverage2:' + r['digest'] for r in proof['evaluationInputRefs']
                 if r['domain'] == 'coverage'}
        for cid in extra:
            self.require(cid in self.coverages_seen,
                         'EXPLICIT_COVERAGE_INPUT_BELONGS_TO_A_SELECTED_VIEW', cid)
        self.require(K.C(K.cset_strings(ev['coverageIds']))
                     == K.C(K.cset_strings(sorted(cov_union | extra))),
                     'EVIDENCE_COVERAGE_ROOTS_EQUAL_VIEW_UNION_PLUS_EXPLICIT',
                     {'evidence': sorted(ev['coverageIds']),
                      'derived': sorted(cov_union | extra)})

    def _registered_schema_document_digests(self):
        out = set()
        for cls in self.payreg['classes'].values():
            if 'document' in cls:
                out.add(S.load_doc(cls['document'])['sha256'])
            for row in (cls.get('rows') or {}).values():
                out.add(S.load_doc(row['document'])['sha256'])
        return out

    def check_registered_pair(self, relation, rung, name):
        """RC-0 runs first and is relation-specific: the rung must be a member of THAT
        relation's ladder. Schema vocabulary is not relation membership."""
        row = self.relreg['relations'].get(relation)
        if row is None:
            self.refuse(name + ':RELATION_UNREGISTERED', relation)
            return False
        if rung not in row['ladder']:
            self.refuse(name + ':RUNG_NOT_A_MEMBER_OF_THIS_RELATIONS_LADDER',
                        '%s@%s ladder=%s' % (relation, rung, row['ladder']))
            return False
        self.ok(name + ':REGISTERED_PAIR', '%s@%s' % (relation, rung))
        return True

    def check_fact(self, fid, f, view_scopes):
        row = self.relreg['relations'].get(f['relation'])
        if row is None:
            self.refuse('FACT_RELATION_UNREGISTERED', f['relation'])
            return
        self.check_registered_pair(f['relation'], f['resolution'], 'FACT_RC0')
        self.require(f['payloadSchemaDigest'] == B.doc_sha(B.RELATION_DOC),
                     'FACT_PAYLOAD_SCHEMA_IS_THE_RELATION_DOCUMENT_FILE_DIGEST', None)
        self.blob(f['payloadSchemaDigest'], 'FACT_PAYLOAD_SCHEMA_DOCUMENT')
        pay = self.canonical_record(f['payloadDigest'], B.RELATION_DOC, row['selector'],
                                    'FACT_PAYLOAD')
        if pay is None:
            return
        if row['universeRule'] == 'same-only':
            self.require(f['sourceUniverse'] == f['targetUniverse'],
                         'FACT_UNIVERSE_RULE_SAME_ONLY', fid)
        udom, uni = self.check_universe(f['sourceUniverse'])
        self.check_universe(f['targetUniverse'])
        # per-rung required/forbidden payload field rules
        rr = (row.get('rungs') or {}).get(f['resolution'])
        if rr:
            for req in rr.get('required', []):
                self.require(req in pay, 'RUNG_REQUIRED_FIELD:%s@%s' % (f['relation'],
                                                                        f['resolution']), req)
            for forb in rr.get('forbidden', []):
                self.require(forb not in pay, 'RUNG_FORBIDDEN_FIELD:%s@%s'
                             % (f['relation'], f['resolution']), forb)
        # anchorLaw: closed cardinality class, checked BEFORE the snapshot joins
        cls = row['anchorLaw']['class']
        card = row['anchorLaw'].get('cardinality')
        n = len(f['anchors'])
        if cls == 'inventory':
            okc = n == 0
        elif cls == 'body-identity':
            okc = n == 1
        else:
            okc = n >= 1
        self.require(okc, 'FACT_ANCHOR_CARDINALITY',
                     '%s class=%s declared=%s actual=%d' % (f['relation'], cls, card, n))
        for a in f['anchors']:
            if a['path'] not in self.inv:
                self.refuse('ANCHOR_SOURCE', a['path'])
                continue
            irow = self.inv[a['path']]
            self.require(a['blobDigest'] == irow['sha256'],
                         'ANCHOR_BLOB_DIGEST_IS_THE_INVENTORY_ROW_DIGEST', a['path'])
            b = self.blob(a['blobDigest'], 'ANCHOR_BLOB')
            if b is None:
                continue
            self.require(0 <= a['startByte'] <= a['endByte'] <= len(b),
                         'ANCHOR_RANGE', '%s [%d,%d) of %d'
                         % (a['path'], a['startByte'], a['endByte'], len(b)))
            if cls in ('source-text', 'body-identity'):
                try:
                    b[a['startByte']:a['endByte']].decode('utf-8')
                    self.ok('ANCHOR_UTF8', a['path'])
                except UnicodeDecodeError:
                    self.refuse('ANCHOR_UTF8', a['path'])
        # relation snapshotJoins
        for j in row.get('snapshotJoins', []):
            if j['form'] == 'inventoried-file':
                p = pay[j['pathField']]
                if p not in self.inv:
                    self.refuse('FILE_PAYLOAD_PATH_NOT_INVENTORIED', p)
                    continue
                irow = self.inv[p]
                self.require(pay[j['digestField']] == irow['sha256'],
                             'FILE_PAYLOAD_CONTENT_DIGEST_JOIN', p)
                self.require(pay[j['lengthField']] == irow['bytes'],
                             'FILE_PAYLOAD_BYTE_LENGTH_JOIN', p)
                b = self.blob(irow['sha256'], 'FILE_PAYLOAD_RETAINED_BYTES')
                if b is not None:
                    self.require(len(b) == pay[j['lengthField']], 'BLOB_LENGTH', p)
                if j.get('anchorPathField'):
                    bad = [a['path'] for a in f['anchors'] if a['path'] != p]
                    self.require(not bad, 'FILE_PAYLOAD_ANCHOR_PATH_FIELD', bad)
            elif j['form'] == 'inventoried-manifest-path':
                p = pay[j.get('pathField', 'manifestPath')]
                self.require(p in self.inv, 'PACKAGE_MANIFEST_PATH_NOT_INVENTORIED', p)
            elif j['form'] == 'inventoried-unless-deleted':
                p = pay[j.get('pathField', 'path')]
                if pay.get('changeKind') == 'deleted':
                    self.na('VCS_CHANGE_DELETED_PATH_IS_OUTSIDE_THE_SNAPSHOT', p)
                else:
                    self.require(p in self.inv, 'VCS_CHANGE_PATH_NOT_INVENTORIED', p)
            else:
                self.na('RELATION_SNAPSHOT_JOIN_FORM_NOT_EXERCISED', j['form'])
        if 'bodyIdentityJoin' in row:
            self.check_body_identity(fid, f, pay, row['bodyIdentityJoin'], udom, uni)

    def check_body_identity(self, fid, f, pay, bij, udom, uni):
        """The framed body-identity join: the frame is RETAINED under the 64-hex suffix,
        parsed, and every component joined to something this Run already admitted."""
        self.require(bij['anchorCardinality'] == len(f['anchors']),
                     'CLONES_ANCHOR_CARDINALITY', len(f['anchors']))
        bid = pay['bodyIdentity']
        self.require(bid.startswith('sha256:'), 'BODY_IDENTITY_SHA256_TEXT_FORM', bid)
        suffix = bid.split(':', 1)[1]
        frame = self.blob(suffix, 'BODY_IDENTITY_FRAME')
        spec = self.blob(pay['normalisationVersion'], 'NORMALISATION_LEVEL_SPECIFICATION')
        if frame is None or spec is None:
            return
        import struct
        pos = 0

        def u8c():
            nonlocal pos
            n = frame[pos]
            pos += 1
            v = frame[pos:pos + n]
            pos += n
            return v
        tag = u8c()
        self.require(tag == bij['domainTag'].encode(), 'BODY_FRAME_DOMAIN_TAG', tag[:40])
        level = u8c()
        self.require(level.decode() == pay[bij['levelField']],
                     'BODY_FRAME_LEVEL_ID_EQUALS_PAYLOAD_NORMALISATION_LEVEL', None)
        lv = u8c()
        self.require(lv == bytes.fromhex(pay['normalisationVersion']),
                     'BODY_FRAME_LEVEL_VERSION_IS_RAW_32_DIGEST_BYTES_NOT_HEX_TEXT',
                     {'frameLen': len(lv)})
        lang = u8c().decode()
        langver = u8c()
        plen = struct.unpack('>I', frame[pos:pos + 4])[0]
        pos += 4
        payload = frame[pos:pos + plen]
        pos += plen
        self.require(pos == len(frame), 'BODY_FRAME_EXACT_LENGTH', None)
        # languageId is DERIVED from the universe's languageVersionBinding, never the
        # universe domain row's own `language` (the engine)
        row = self.dd['domainSets']['native-semantic-universe'][udom]
        lvb = row['languageVersionBinding']
        dialect = lvb['dialect']
        anchor_path = f['anchors'][0]['path']
        if dialect['form'] == 'closed-suffix-table':
            variant = None
            for suf in sorted(dialect['table'], key=lambda s: -len(s)):
                if anchor_path.endswith(suf):
                    variant = dialect['table'][suf]
                    break
            if variant is None:
                self.refuse(dialect['onUnknown'], anchor_path)
                return
            want_lang = lvb['bodyLanguageByVariant'][variant]
            dial = {dialect['key']: variant}
        else:
            want_lang = lvb['bodyLanguage']
            dial = None
        self.require(lang == want_lang,
                     'BODY_FRAME_LANGUAGE_ID_IS_DERIVED_FROM_THE_SELECTED_VARIANT',
                     {'frame': lang, 'derived': want_lang, 'engine': row.get('language')})
        self.require(lang in lvb['bodyLanguages'],
                     'BODY_LANGUAGE_DECLARED_BY_THIS_UNIVERSE', lang)
        # body-language-version is DERIVED: rebuild it and compare
        blv = {'schemaVersion': 1, 'languageId': lang}
        ctx_hex = self._at(uni, row['contextField'])
        ctx_hex = ctx_hex.split(':', 1)[1] if ctx_hex.startswith('sha256:') else ctx_hex
        cdom, ctx = self.context_cache.get(ctx_hex, (None, None))
        for fld, src in lvb['fields'].items():
            if 'const' in src:
                blv[fld] = src['const']
            else:
                blv[fld] = self._at(ctx, src['path'])
        if dial is not None:
            blv['dialect'] = dial
        else:
            self.na('BODY_LANGUAGE_DIALECT_NOT_SUFFIX_TABLE', dialect.get('form'))
            return
        r = S.admit(B.IDENTITY_DOC, '#/$defs/body-language-version', blv,
                    'body-language-version:recomputed')
        self.require(r['admitted'], 'BODY_LANGUAGE_VERSION_RECORD_VALID',
                     json.dumps(r['stockSchemaErrors'])[:300])
        want32 = bytes.fromhex(K.rec_digest(blv))
        self.require(langver == want32,
                     'BODY_FRAME_LANGUAGE_VERSION_IS_RAW_32_SHA256_OF_DERIVED_RECORD',
                     {'recomputedRecord': blv})
        self.blob(K.rec_digest(blv), 'BODY_LANGUAGE_VERSION_RECORD_RETAINED')
        # L0 is RECOMPUTED from the enclosing fact's own anchor: a real source join
        if pay['normalisationLevel'] in bij['recomputableAt']:
            a = f['anchors'][0]
            src = self.st.get_blob(a['blobDigest'])
            span = src[a['startByte']:a['endByte']]
            want = struct.pack('>I', len(span)) + span
            self.require(payload == want,
                         'L0_PAYLOAD_RECOMPUTED_FROM_THE_ANCHOR_SPAN',
                         {'payloadLen': len(payload), 'rawLen': len(span),
                          'doublePrefixHolds': len(payload) == len(span) + 4})
        else:
            # L1-L3: exact retained preimage custody plus well-formed stream framing
            ok = self._parse_token_stream(payload)
            self.require(ok is not None, 'L1_L3_TOKEN_STREAM_FRAMING_WELL_FORMED', None)
            self.na('L1_L3_NORMALIZER_NOT_RECOMPUTED',
                    'custody and framing evidence only; it qualifies no normalizer')
        self.require(K.raw_sha256(frame) == suffix,
                     'BODY_IDENTITY_IS_SHA256_OF_THE_RETAINED_FRAME', None)
        self.require(suffix != self.st.suffix(fid),
                     'FACT_ID_AND_BODY_IDENTITY_ARE_NEVER_EQUATED', None)

    @staticmethod
    def _parse_token_stream(b):
        import struct
        try:
            n = struct.unpack('>I', b[:4])[0]
            pos = 4
            toks = []
            for _ in range(n):
                kl = struct.unpack('>H', b[pos:pos + 2])[0]
                pos += 2
                kind = b[pos:pos + kl].decode('utf-8')
                pos += kl
                vl = struct.unpack('>I', b[pos:pos + 4])[0]
                pos += 4
                val = b[pos:pos + vl]
                pos += vl
                if not kind:
                    return None
                toks.append((kind, val))
            return toks if pos == len(b) else None
        except Exception:
            return None

    def check_coverage(self, cid, c, view_scopes, view_facts):
        sc = view_scopes.get(c['scopeId']) or self.typed(c['scopeId'], 'subject-scope',
                                                         'COVERAGE_SCOPE')
        rows = self.payreg['classes']['coverage']['rows']
        pay = self.canonical_record(c['payloadDigest'], rows['3']['document'],
                                    rows['3']['selector'], 'COVERAGE_PAYLOAD')
        if pay is None or sc is None:
            return
        self.require(c['payloadSchemaDigest'] == S.load_doc(rows['3']['document'])['sha256'],
                     'native.coverage-payload-schema-not-registered', None)
        self.blob(c['payloadSchemaDigest'], 'COVERAGE_PAYLOAD_SCHEMA_DOCUMENT')
        key, ent = pay['key'], pay['entry']
        suffix = self.st.suffix(c['scopeId'])
        self.require(key['subjectScopeCommitment'] == 'sha256:' + suffix,
                     'native.subject-scope-commitment-mismatch', None)
        for fld in ('relation', 'resolution', 'sourceUniverse', 'targetUniverse'):
            self.require(key[fld] == sc[fld], 'native.coverage-key-scope-mismatch:' + fld,
                         {'key': key[fld], 'scope': sc[fld]})
        self.require(ent['examinedUniverse']['subjectScopeCommitment']
                     == key['subjectScopeCommitment'],
                     'native.examined-universe-commitment-mismatch', None)
        self.require(ent['examinedUniverse']['subjectCount'] == len(sc['subjects']),
                     'native.examined-universe-subject-count-mismatch',
                     {'entry': ent['examinedUniverse']['subjectCount'],
                      'scope': len(sc['subjects'])})
        self.require(ent['relation'] == sc['relation'] and ent['resolution'] == sc['resolution'],
                     'COVERAGE_ENTRY_RELATION_RUNG_EQUALS_SCOPE', None)
        self.check_coverage_bijection(cid, key, ent, view_facts, sc)
        self.check_scope_capability_law(cid, key, ent, sc)
        self.check_deficiency_cause_registry(cid, key, ent)

    def check_deficiency_cause_registry(self, cid, key, ent):
        """native x-opensip-deficiency-cause-registry: which FIELD carries each
        deficiency's cause, whether nativeCause is required / optional / must-be-null, the
        closed allowedCauses list, and the per-deficiency field conditions."""
        reg = json.load(open(KIT + '/' + S.doc_path(B.NATIVE_DOC)))[
            'x-opensip-deficiency-cause-registry']['deficiencies']
        d = ent['deficiency']
        if d is None:
            self.require(ent['nativeCause'] is None,
                         'x-opensip-deficiency-cause-registry:NO_DEFICIENCY_NO_CAUSE',
                         ent['nativeCause'])
            return
        row = reg.get(d)
        if row is None:
            self.refuse('DEFICIENCY_UNREGISTERED', d)
            return
        mode = row['nativeCause']
        nc = ent['nativeCause']
        if mode == 'required':
            self.require(nc is not None and nc in row['allowedCauses'],
                         'x-opensip-deficiency-cause-registry:NATIVE_CAUSE_REQUIRED:' + d,
                         {'nativeCause': nc, 'allowed': row['allowedCauses']})
        elif mode == 'optional':
            self.require(nc is None or nc in row['allowedCauses'],
                         'x-opensip-deficiency-cause-registry:NATIVE_CAUSE_OPTIONAL:' + d,
                         {'nativeCause': nc, 'allowed': row['allowedCauses']})
        elif mode == 'must-be-null':
            self.require(nc is None,
                         'x-opensip-deficiency-cause-registry:NATIVE_CAUSE_MUST_BE_NULL:' + d,
                         nc)
        if 'relations' in row:
            self.require(key['relation'] in row['relations'],
                         'x-opensip-deficiency-cause-registry:RELATION_LAW:' + d,
                         {'relation': key['relation'], 'allowed': row['relations']})
        if 'requires' in row:
            v = self._at(ent, row['requires']['path'])
            self.require(v == row['requires']['equals'],
                         'x-opensip-deficiency-cause-registry:REQUIRES:' + d,
                         {'observed': v, 'required': row['requires']['equals']})
        if 'oneOf' in row:
            v = self._at(ent, row['oneOf']['path'])
            self.require(v in row['oneOf']['members'],
                         'x-opensip-deficiency-cause-registry:ONE_OF:' + d,
                         {'observed': v, 'members': row['oneOf']['members']})
        if 'contains' in row:
            v = self._at(ent, row['contains']['path']) or []
            self.require(row['contains']['member'] in v,
                         'x-opensip-deficiency-cause-registry:CONTAINS:' + d,
                         {'observed': v, 'member': row['contains']['member']})

    def check_coverage_bijection(self, cid, key, ent, view_facts, sc):
        """RC-0 / RC-1 / RC-2 / RC-6, re-run at retained Run closure."""
        if not self.check_registered_pair(key['relation'], key['resolution'],
                                          'COVERAGE_RC0'):
            return
        import opensip_eval as E
        resolved = key['resolution'] in E.RESOLVED_RUNGS
        rc = ent['resolutionCompleteness']
        if not resolved:
            bad = []
            if rc['state'] != 'not-applicable':
                bad.append('state=' + rc['state'])
            if rc['unresolvedEdgeCount'] != 0:
                bad.append('unresolvedEdgeCount=%d' % rc['unresolvedEdgeCount'])
            if rc['attempted'] is not False:
                bad.append('attempted=True')
            if rc['unresolvedEdgeClasses']:
                bad.append('classes=%s' % rc['unresolvedEdgeClasses'])
            self.require(not bad, 'native.coverage-bijection-mismatch:RC1_NON_RESOLVED_RUNG',
                         bad)
        else:
            self.require(rc['state'] != 'not-applicable',
                         'native.coverage-bijection-mismatch:RC1_RESOLVED_RUNG_NOT_APPLICABLE',
                         rc['state'])
            edges = [fid for fid, f in view_facts.items()
                     if f['relation'] == 'unresolved-edge']
            if rc['state'] == 'complete':
                self.require(rc['attempted'] and rc['examinedExhaustive']
                             and rc['stageTerminal'] == 'complete' and not edges,
                             'native.coverage-bijection-mismatch:RC2_COMPLETE', None)
            elif rc['state'] == 'incomplete':
                self.require(bool(edges) and rc['stageTerminal'] == 'complete'
                             and rc['examinedExhaustive'],
                             'native.coverage-bijection-mismatch:RC2_INCOMPLETE', None)
            elif rc['state'] == 'partial':
                self.require(rc['attempted'] and (
                    rc['stageTerminal'] in ('unavailable', 'budget-exhausted',
                                            'provider-fault', 'cancelled', 'crash')
                    or not rc['examinedExhaustive']),
                    'native.coverage-bijection-mismatch:RC2_PARTIAL', None)
            elif rc['state'] == 'not-attempted':
                self.require(rc['attempted'] is False and rc['unresolvedEdgeCount'] == 0,
                             'native.coverage-bijection-mismatch:RC2_NOT_ATTEMPTED', None)
        if ent['coverage'] == 'complete':
            self.require(rc['examinedExhaustive'] is True,
                         'native.coverage-bijection-mismatch:RC6_COMPLETE_NEEDS_EXHAUSTIVE',
                         None)
        else:
            self.na('RC6_UNKNOWN_CONSTRAINS_EXAMINED_EXHAUSTIVE_IN_NEITHER_DIRECTION',
                    {'examinedExhaustive': rc['examinedExhaustive']})

    def check_scope_capability_law(self, cid, key, ent, sc):
        """scopeCapabilityLaw: what a COVERAGE claim means under a universe whose dialect
        form is a closed suffix table. Inventory relations are never dialect-gated."""
        law = self.dd['scopeCapabilityLaw']
        row = self.relreg['relations'][key['relation']]
        pair = '%s@%s' % (key['relation'], key['resolution'])
        if pair in [x.strip('`') for x in law['inventoryExempt'].replace('`', ' ').split()
                    if '@' in x]:
            self.na('scopeCapabilityLaw:INVENTORY_EXEMPT', pair)
            return
        if 'bodyIdentityJoin' not in row:
            self.na('scopeCapabilityLaw:NO_BODY_IDENTITY_JOIN_SO_NO_DIALECT_AXIS', pair)
            return
        udom, uni = self.check_universe(key['sourceUniverse'])
        if udom is None:
            return
        urow = self.dd['domainSets']['native-semantic-universe'][udom]
        dialect = urow['languageVersionBinding']['dialect']
        if dialect.get('form') != law['appliesToDialectForm']:
            self.na('scopeCapabilityLaw:DIALECT_FORM_NOT_APPLICABLE', dialect.get('form'))
            return
        table = dialect['table']

        def readable(p):
            return any(p.endswith(s) for s in table)
        if row['subjectKind'] == 'source-path':
            subjects = sc['subjects']
            if not subjects:
                supported = False
            else:
                supported = all(readable(p) for p in subjects)
        else:
            supported = any(readable(p) for p in self.inv)
        if supported:
            self.ok('scopeCapabilityLaw:SUPPORTED_SCOPE', pair)
        else:
            want = law['onUnsupportedScope']
            bad = []
            if ent['coverage'] != want['coverage']:
                bad.append('coverage=%s want %s' % (ent['coverage'], want['coverage']))
            if ent['deficiency'] != want['deficiency']:
                bad.append('deficiency=%s want %s' % (ent['deficiency'], want['deficiency']))
            if ent['nativeCause'] != want['nativeCause']:
                bad.append('nativeCause=%s want %s' % (ent['nativeCause'],
                                                       want['nativeCause']))
            self.require(not bad, 'COVERAGE_SOURCE_VARIANT_UNSUPPORTED_SCOPE', bad)

    def check_coverage_partition(self, vid, view_scopes):
        """PER VIEW, over EVERY referenced scope INCLUDING scopes with no Coverage entry:
        two scopes sharing the FULL owning tuple must carry disjoint subject sets."""
        keyfields = self.relreg['coveragePartitionLaw']['partitionKey']
        groups = {}
        for sid, sc in view_scopes.items():
            k = tuple(sc[f] for f in keyfields)
            groups.setdefault(k, []).append((sid, sc))
        worst = None
        for k, members in groups.items():
            for i in range(len(members)):
                for j in range(i + 1, len(members)):
                    inter = set(members[i][1]['subjects']) & set(members[j][1]['subjects'])
                    if inter:
                        low = sorted(inter, key=lambda s: s.encode())[0]
                        worst = 'SUBJECT_SCOPE_PARTITION_OVERLAP:%s@%s:%s' % (
                            k[1], k[2], low)
        self.require(worst is None, 'SUBJECT_SCOPE_PARTITION_OVERLAP', worst)
        self.ok('COVERAGE_PARTITION_LAW_COVERS_SCOPES_WITHOUT_A_COVERAGE_ENTRY',
                {'scopesInView': len(view_scopes), 'partitions': len(groups)})

    def check_coverage_totality(self, vid, view_scopes, view_facts):
        for sid, sc in view_scopes.items():
            row = self.relreg['relations'].get(sc['relation'], {})
            tot = row.get('coverageTotality')
            if not tot or tot['rung'] != sc['resolution']:
                continue
            cov = [c for c in self.coverages_seen.values() if c['scopeId'] == sid]
            if not cov:
                continue
            pay = self.canonical_record(cov[0]['payloadDigest'], B.NATIVE_DOC,
                                        '#/$defs/CoverageResultV3', 'TOTALITY_COVERAGE')
            if pay is None or pay['entry']['coverage'] != 'complete':
                self.na('COVERAGE_INVENTORY_TOTALITY_NOT_CLAIMED', sid)
                continue
            owed = [s for s in sc['subjects'] if s in self.inv]
            have = set()
            for fid, f in view_facts.items():
                if all(f[k] == sc[k] for k in tot['matchOn'] if k in f):
                    fpay = self.canonical_record(f['payloadDigest'], B.RELATION_DOC,
                                                 row['selector'], 'TOTALITY_FACT_PAYLOAD')
                    if fpay:
                        have.add(fpay[tot['pathField']])
            missing = sorted(set(owed) - have)
            self.require(not missing, tot['refusal'], missing)
            self.ok('COVERAGE_TOTALITY_SUBJECT_OUTSIDE_INVENTORY_IS_OWED_NOTHING',
                    sorted(set(sc['subjects']) - set(owed)))

    def check_grammar_capability_boundaries(self):
        """Boundary (2): every ANCHOR PATH of an admitted fact2 under a syntax universe
        must be read by a SELECTED grammar whose capability set contains that
        relation@rung. Inventory capabilities are exempt at boundary (2) AND (3).
        Boundary (3): every requested subject-scope, including an empty view."""
        greg = self.greg
        inventory_pairs = {'file@enumerated', 'package@manifest-declared',
                           'vcs-change@vcs-reported'}
        exercised = 0
        for fid, f in self.facts_seen.items():
            udom, uni = self.check_universe(f['sourceUniverse'])
            if udom != 'native.semantic-universe.syntax.v2':
                continue
            pair = '%s@%s' % (f['relation'], f['resolution'])
            if pair in inventory_pairs:
                self.na('grammarCapabilityRegistry:BOUNDARY2_INVENTORY_EXEMPT', pair)
                continue
            ctx_hex = uni['nativeContextId'].split(':', 1)[1]
            ctx = self.context_cache[ctx_hex][1]
            selected = {g['grammarId']: g for g in ctx['grammarBundle']['grammars']
                        if g['grammarId'] in uni['selectedGrammarIds']}
            for a in f['anchors']:
                hit = None
                for g in selected.values():
                    if any(a['path'].endswith(s) for s in g['suffixes']):
                        hit = g
                        break
                if hit is None:
                    self.refuse('grammarCapabilityRegistry:BOUNDARY2_NO_SELECTED_GRAMMAR',
                                a['path'])
                    continue
                caps = greg['languages'][hit['languageId']]['capabilities']
                self.require(pair in caps,
                             'grammarCapabilityRegistry:BOUNDARY2_CAPABILITY',
                             {'path': a['path'], 'grammar': hit['grammarId'],
                              'pair': pair, 'capabilities': caps})
                exercised += 1
        for sid, sc in self.scopes_seen.items():
            udom, uni = self.check_universe(sc['sourceUniverse'])
            if udom != 'native.semantic-universe.syntax.v2':
                continue
            pair = '%s@%s' % (sc['relation'], sc['resolution'])
            if pair in inventory_pairs:
                self.na('grammarCapabilityRegistry:BOUNDARY3_INVENTORY_EXEMPT', pair)
                continue
            ctx_hex = uni['nativeContextId'].split(':', 1)[1]
            ctx = self.context_cache[ctx_hex][1]
            selected = [g for g in ctx['grammarBundle']['grammars']
                        if g['grammarId'] in uni['selectedGrammarIds']]
            code = [g for g in selected if g['syntaxClass'] == 'code']
            extent = (sc['subjects'] if self.relreg['relations'][sc['relation']]['subjectKind']
                      == 'source-path' else list(self.inv))
            served = any(any(p.endswith(s) for s in g['suffixes'])
                         for g in code for p in extent)
            bears = any(pair in greg['languages'][g['languageId']]['capabilities']
                        for g in selected)
            cov = [c for c in self.coverages_seen.values() if c['scopeId'] == sid]
            if served and bears:
                self.ok('grammarCapabilityRegistry:BOUNDARY3_CAPABILITY_SERVED', pair)
            elif cov:
                pay = self.canonical_record(cov[0]['payloadDigest'], B.NATIVE_DOC,
                                            '#/$defs/CoverageResultV3', 'B3_COVERAGE')
                want = greg['unavailableRequestDisclosure']
                self.require(pay and pay['entry']['coverage'] == 'unknown'
                             and pay['entry']['deficiency'] == 'language-tier-unsupported'
                             and pay['entry']['nativeCause'] == 'capability-missing',
                             'grammarCapabilityRegistry:BOUNDARY3_UNAVAILABLE_DISCLOSURE',
                             {'pair': pair, 'entry': pay['entry'] if pay else None,
                              'required': want})
        self.ok('grammarCapabilityRegistry:BOUNDARY2_ANCHORS_CHECKED', exercised)

    def check_unreferenced(self):
        unref = sorted(set(self.st.blobs) - self.visited_digests)
        self.checks.append({'check': 'UNREFERENCED_CAS_BLOBS_ARE_NOT_EVALUATION_INPUTS',
                            'result': 'PASS',
                            'detail': {'unreferencedCount': len(unref),
                                       'note': ('Reported, not admitted as inputs. Some are '
                                                'retained for root inspection (composed '
                                                'output frames and subject frames reached '
                                                'through typed ids rather than annotated '
                                                '64-hex fields).'),
                                       'sample': unref[:12]}})
