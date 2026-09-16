# Decisions forced during reconstruction and design-gap CANDIDATES (to be adjudicated in phase 10)

Each entry records: selector, what is missing/conflicting, what this reconstruction chose, and whether
the choice is algorithm freedom or a public/semantic contract gap. Candidates are re-verified before
they become issues.

1. stage-spec.outputSchemaDigest registry (identity-schemas.v3 #/$defs/stage-spec, cache-key; identity s3
   "exact complete registered stage output schema document bytes"). No closed list of stage OUTPUT schema
   documents is named (x-opensip-payload-registry lists payload/parameter documents only). Two hosts could
   pin different documents for the same view-producing stage -> different stageSpecDigest -> exec-plan2 ->
   proof/seal. CHOICE: native/native-evidence.schemas.v2.json for native view stages. Candidate SHOULD.

2. Clone level-specification custody join. SyntaxGrammarBundleV1.normalizer.specificationDigest is singular,
   while FACT-IDENTITY BH-1 versions each level separately and identity s3 joins frame levelVersion "to the
   retained specification" without naming which record carries per-level specification digests; TS/Rust
   contexts carry no normalizer record at all. CHOICE: require normalisationVersion bytes retained and (syntax
   universe) present as a member digest of the admitted grammar closure tree. Candidate SHOULD.

3. Zero-config syntax-only unit recognition. enumeration-contract s1 says U-1 yields "one tsjs/rust/syntax-only
   unit per directory by marker precedence"; native s1.2/U-1 name markers only for tsjs/rust and say syntax-only
   files have unitOrdinal null. No recognizer/marker/workspaceRoot rule mints the syntax-only cell for a
   repository with no compilation unit under the default profile. CHOICE: explicit analysis selection
   (workspaceRoot ".", provenance explicit-plan-selection). Candidate SHOULD (zero-config path undetermined).

4. Unannotated bare 64-hex digest fields in foundation/execution-inputs.schema.v1.json (16 positions) and
   foundation/incoming-search.schema.v1.json (3 positions), measured by ref/schemas.py unannotated_hex_fields.
   identity s3's closing digest law scopes identity-schemas.v3 (native/relation bundles extend it to themselves);
   the closure checker "refuses a 64-hex field the schema does not annotate" while walking. Whether the law
   reaches these registered canonical-record input documents is not stated. Candidate advisory/SHOULD.

5. enumeration-plan.schema.v1 / subject-inventory.schema.v1 annotations and descriptions name
   foundation/identity-schemas.v2.json (#/$defs/scope-descriptor, LogicalPath) while the selected identity owner
   is identity-schemas.v3. Byte-identical constraints in both; advisory drift.

6. program-predicate.nodeDigest record names workflows/schemas/policy-document.schema.json#/$defs/Predicate
   (policy1 owner) while RuleProgramV2/PolicyDocumentV2 use policy-document.v2.schema.json#/$defs/Predicate
   (Atom with endpoint/evidence/v2 filters). If v1 Predicate does not admit v2 atoms, the nodeDigest record
   selector refuses every v2 node. MEASURED (jsonschema 4.25.1, ref/schemas.py admit): atom
   {op:exists, relation:clones, minResolution:normalized-body-hash, filters:[], endpoint:source} is REFUSED by
   policy-document.schema.json#/$defs/Predicate and ADMITTED by policy-document.v2.schema.json#/$defs/Predicate;
   the same atom without endpoint and an evidence atom pass both. A closure checker obeying the nodeDigest
   x-opensip-digest record selector (retention fragment: "recomputes it there" under the named record) refuses any
   RuleProgramV2 node that carries `endpoint` -- i.e. every incoming (endpoint=target) atom and every explicitly
   spelled source endpoint. Owner-document drift in an identity-bearing digest annotation. Candidate SHOULD.

7. Charter prose "101 kit files" vs manifest 102 files (process advisory, not design).

8. UnitMembershipV1 order. units[] and rows[] are x-opensip-order sequence and unitOrdinal assignment order is not
   published (native s1.4 names discover_units/assign_membership in excluded author code), yet C(UnitMembershipV1)
   is EnumerationPlanV1.membershipDigest -> analysisSpecDigest -> PlanId. Two hosts can mint different PlanIds for
   one repository. CHOICE: units by (rootPath bytes, languageFamily); rows by path bytes. Candidate SHOULD.

9. Pruned-tree files in the snapshot inventory. ResolvedNodeModulesLayoutV1 description: node_modules rows "could
   not exist" as inventory rows; U-4 assigns host-ignore-convention to inventoried files inside pruned trees and
   identity s5 snapshot capture removes only nested-repository/nested-project/custody-excluded paths. Whether
   node_modules/target bytes are captured into snapshot.sourceInventory is not decided in one place. CHOICE:
   node_modules not inventoried (read-set via layout record); no target/ files in the synthetic repositories.

10. Syntax-only repository scope descriptor: unit_scope_descriptor emits workspaceRoots from unit roots; with zero
    units workspaceRoots would be empty (nothing in scope under the import/scope membership law), and an explicit
    "." root without a language marker refuses native.explicit-root-without-marker. CHOICE: workspaceRoots ["."].
    Joins candidate 3.

11. TypeScript universe jsAdmittedToProgram/jsDiagnosticsEnabled: checked "against the context" but the derivation
    from honored allowJs/checkJs is not written. CHOICE: jsAdmittedToProgram=allowJs, jsDiagnosticsEnabled=allowJs AND checkJs.
    Candidate advisory.

12. NativeCoverageAccountV1.targetUniverse value. execution-inputs s5 publishes the sourceUniverse join and says
    targetUniverse is "deliberately not joined", but does not say what value an account carries (U? the Coverage key
    target? null for no Coverage?) nor whether an admitted-target relation owes one account per target universe.
    The field is inside C(ExecutionInputsV1) -> executionInputsDigest -> proof3. CHOICE: targetUniverse = binding U,
    one account per binding x matrix pair (all Runs here are same-universe). Candidate SHOULD (cross-universe hosts diverge).

13. Rule outcome when a REQUIRED evidenceUse kind has no Plan-selected wrapper but no root is indeterminate because of
    it (e.g. the atom using it sits under a branch another child decides). composition s5 says required import
    obligations "are assessed according to declared evidenceUse independently of a boolean branch", but the outcome
    sentence lists only population and root-blocking causes. CHOICE: a gating enabled rule with a rule-level required
    `evidence-kind-unavailable` is indeterminate. Candidate advisory (gate result differs between readings).

14. Correspondence reason with several simultaneous conditions (symbol with empty tokens AND incomplete population):
    s9.5 emits one deficiency per condition, finding.correspondence.reason holds one value. CHOICE: every applicable
    deficiency emitted; reason = first in s9.5 table order (projection-unavailable, population-incomplete,
    signature-ambiguous). Collision population = all rows of the rule's relevant inventories (pre-glob). Candidate advisory.

16. Required clones-fact census over non-code files (TO MEASURE in the pilot Runs). native s1.4 line ~789: the default
    profile requests every registered capability per unit with required=true. enumeration x-opensip-kind-derivation:
    clones-fact kinds [file]; x-opensip-file-membership-extent-law.fileKind: every scoped first-party path "including
    data-document, unsupported-file, extensionless ... Inventory is not grammar-gated". execution-inputs s5: every expected
    source subject of a source-path relation must be in some returned partition, else incomplete; a partition over a
    data/unsupported path must disclose language-tier-unsupported/capability-missing (native s1.2 grammar law, and the
    scopeCapabilityLaw for TS). Hence a required clones-fact account over any unit containing README/package.json/
    tsconfig.json is incomplete in EVERY admissible construction -> requiredCellDeficiencies -> proof
    executionDeficiencies nonempty -> sealed verdict >= indeterminate, while native s1.2 (lines 443-445) promises
    "No syntax Run is made blanket-indeterminate ... a code-grammar declares/clones Run ... close[s] with a genuine
    complete and no deficiency". Candidate MUST if measured (default-profile Runs could never pass).
    MEASURED (syntax universe, explicit analysis selection, fresh-process closure+replay, runs/syntax-*.replay.json):
      syntax-code (code files only): ADMIT, verdict pass, clones-fact cell complete.
      syntax-mixed-disclosed (+README.md, data/config.json, LICENSE; clones partition over data paths coverage unknown,
        language-tier-unsupported/capability-missing): ADMIT, every rule outcome pass, verdict INDETERMINATE,
        executionDeficiencies [language-tier-unsupported/capability-missing, required-cell-unsatisfied/null].
      syntax-mixed-omitted (data paths in no clones partition): ADMIT, verdict INDETERMINATE [required-cell-unsatisfied].
      syntax-mixed-falsecomplete (complete clones Coverage over data paths): REFUSE SYNTAX_CAPABILITY_UNSUPPORTED_SCOPE.
    No admissible construction of a required clones-fact cell over a unit containing a non-code file seals pass.
    TypeScript universe MEASURED (runs/ts-*.replay.json, default-unit binding of a tsconfig unit): the unit file extent
    always contains package.json, package-lock.json, tsconfig.json, tsconfig.base.json (and README.md here); the TS
    scopeCapabilityLaw forces their clones partition to disclose language-tier-unsupported/capability-missing.
      ts-pass (clones-fact optional): ADMIT, pass; clones-fact cell partial with the disclosed pair, no required row.
      ts-clones-required (clones-fact required, as the default profile requests): ADMIT, every rule pass, sealed
        INDETERMINATE [language-tier-unsupported/capability-missing, required-cell-unsatisfied/null].
    A tsconfig unit cannot exist without such files, so under native s1.4's default (every capability, required=true)
    no TypeScript Run can seal pass. Upgraded to MUST candidate.
    Rust universe MEASURED (runs/rust-mixed-clones-required.replay.json): the same required clones-fact census over
    Cargo.toml/Cargo.lock is satisfied by ONE complete clones partition over every file (no disclosure owed: the
    scopeCapabilityLaw gates only closed-suffix-table dialect forms, and native s10 ownership guards test only
    partial/ambiguous ownership) -> ADMIT, sealed PASS. So identical repository shapes (a unit containing its own
    manifest) are forced indeterminate under TypeScript/syntax universes and pass under Rust: the obligation is not
    uniformly defined, which strengthens the candidate (inconsistent census law across universes).

MEASURED CLOSURE CONSEQUENCES (runs/syntax-matrix.summary.json; fresh-process close_run):
 - Candidate 1: syntax-code~stage-output-schema-relation-doc (stage-spec.outputSchemaDigest = relation-payload doc
   instead of native-evidence doc; both registered payload documents) -> same planId, DIFFERENT executionPlanId,
   BOTH ADMIT with complete replay. Two conforming hosts mint different exec-plan2/proof3/seal3/run3 for one Plan.
 - Candidate 2: syntax-code~clone-level-spec-not-in-grammar (L0 level spec retained but not a grammar closure tree
   member) -> refused ONLY by this reconstruction's own cb24.CLONE_LEVEL_SPEC_NOT_IN_GRAMMAR_CLOSURE; no published
   refusal names the join, so a literal kit reader admits it.
 - Candidate 6: syntax-code~explicit-endpoint-source (atom spells endpoint:"source") -> REFUSE
   DIGEST_FRAGMENT_RECORD_REFUSED:$.nodeDigest:policy-document.schema.json#/$defs/Predicate reached through
   proof.predicateProofs[0].witnessDigest -> programPredicateDigest -> nodeDigest. The same policy without the
   optional default spelling ADMITs. A v2-only construct makes an otherwise valid Run unclosable.
 - Candidate 8: syntax-code~membership-reordered (UnitMembershipV1.rows reversed; schema order "sequence" admits it)
   -> refused only by re-derivation under this reconstruction's chosen order (cb24.UNIT_MEMBERSHIP_DERIVATION).

17. Abbreviated refusal keys (advisory). native-evidence.md s1.2 lines 440-443 name the scope refusals as
    `SYNTAX_CAPABILITY_UNSUPPORTED_SCOPE`, `…_CAUSE_MISMATCH`, `…_DEFICIENCY_MISMATCH`; a kit-wide search finds no complete
    spelling of the two abbreviated keys (only COVERAGE_DIALECT_* spells both, s10 lines 3300-3302), and no key at all for
    an unsupported source-path scope answered `coverage: unknown` with a null deficiency. Readers can expand "…" as
    SYNTAX_CAPABILITY_UNSUPPORTED_SCOPE_CAUSE_MISMATCH or SYNTAX_CAPABILITY_CAUSE_MISMATCH. Internal keys, so advisory.
    HELPER CORRECTION HC-KEYNAMES (preserved: vectors/unsupported-grammar.attempt1.json, sha256 73a4faf1...): ref/native_facts.py
    had emitted SYNTAX_CAPABILITY_{DEFICIENCY,CAUSE}_MISMATCH / *_UNSUPPORTED_UNDISCLOSED as if published; corrected from the
    kit (grep of every SYNTAX_CAPABILITY_/COVERAGE_* token) to emit only the published complete keys and to prefix every
    reconstructed name with cb24.

HELPER CORRECTIONS LOG (original failure preserved -> kit selector -> correction):
 HC-1 syntax-code replay attempt1 (runs/syntax-code.replay.attempt1.json): DIGEST_PREIMAGE_MISSING vcs-observation.sourceInventoryDigest
      (builder omitted the source-inventory record; identity #/$defs/vcs-observation canonical-record) and
      DIGEST_REPRESENTATION_UNREGISTERED framed-body-identity (relation-payload-schemas.v2 #/x-opensip-digest-law/representations).
 HC-2 phase4 attempt1 (vectors/phase4-tables.attempt1.json): vector expectation wrongly added not-for-deficiency for a budget row
      with no allowedCauses (native #/x-opensip-deficiency-cause-registry/deficiencies/budget-exhausted).
 HC-3 rust runs first pass: inventory rows sorted by (path,id) against subject-inventory rows order {"by":["nativeSubjectId","path"]};
      digest law demanded preimages for h-identity retention "derived" (identity #/x-opensip-digest-domains/retention/derived).
 HC-4 closure crash on unbound universe (checker defect, not kit): guarded, internal errors now reported as cb24.CLOSURE_INTERNAL_ERROR.
 HC-5 digest law did not descend into resolved records (candidate 6 not reached): transitive execution added (identity s3 closing law).
 HC-KEYNAMES above.

15. Per-binding returned views: CellProgramOutcomeV1.viewDigests is treated as a host OBSERVATION input (like
    stageOrdinal) validated by s3 joins (planId, producer = enumerator closure, every scope sourceUniverse = U,
    views on the named complete receipt), not as a derived field. s4 lists it among host row fields without saying
    which. Advisory only: a host omitting a returned view still cannot close an account (census + selectedRefs totality).
