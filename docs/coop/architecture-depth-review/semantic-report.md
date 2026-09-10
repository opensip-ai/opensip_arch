Verification is complete. I have enough to write the report; no further reads are needed.

**Lens A review of the OpenSIP architecture snapshot after D-371**

Readiness under this lens: NOT_READY for full-design acceptance. That matches the register's own standing, where file 08 records conditions 1, 2, 3 and 5 as NOT MET for the intended product. This review adds four new defects in accepted or applied contracts, three integration gaps that no row currently names, and three hazards where authority documents misstate what is open. Nothing here contradicts the preview-scoped D-369 acceptance, which stays a historical milestone.

Method. I started from the scope chapter, the file 08 full-product section, the reference handoff, the D-369 application manifest and its freeze, and the D-371 act and its prior Claude review. I then followed the actual binding heads named in blueprint §1.1 and freeze §3 rather than the narrative chapters, resolved derivation chains where the head is a delta, and read checker code where the contract delegates to it. The prior Claude acceptance of D-371 was treated as a claim to test; it verified scope arithmetic and custody, not the substance of identity, evidence or coverage contracts, and its own notes say so.

## Findings

**SEM-01, HIGH, newly discovered defect. The baseline detector pivot rests on a precondition that the cited mechanism does not supply.** The versioning contract makes attribution of baseline deltas depend on running the old detector over new code. It states that detector zero "must still be RUNNABLE" and that "that is exactly what the dual-emit window in the custody policy provides", citing the fact-identity custody transition. The fact-identity transition protocol covers only body-hash normalisation level versions, supplies a many-to-many group witness, and says in its own honesty clause that it "does NOT support recomputing an old identity from new inputs". Dual emission of two fingerprint identities is not execution of an older rule pack or provider. The lifecycle chapter's GC roots list locks, active processes, retained evidence, rollback slots and migrations; no root retains a superseded detector closure for baseline use, and the completed lock schema has no multi-version pin. Trigger: any detector major change on a project with a committed baseline. Consequence: the comparison reports INDETERMINATE for every affected detector, which is exit 3 and blocks CI, so the trust failure the pivot exists to prevent reappears as a mass indeterminate instead of mass net-new. Counterevidence considered: the INDETERMINATE fallback is safe, and the cost gate keeps the pivot off ordinary analysis, but chapter 13 §6 instructs the product to "preserve the existing versioned fingerprint and detector-pivot architecture" as settled. Required correction: a contract that either retains superseded detector closures as GC roots with compatibility windows, or ships old algorithm versions inside new components, and a versioning successor that stops attributing the precondition to fact-identity. Owners: the DR-006/111/122/123/130 obligation row, DR-107 and DR-127 for generation retention, DR-011-R13. Confidence: high on the misattribution, medium on the absence of any retention root, which is grep-based.

```
docs/coop/artifacts/versioning-policy.v8.json  $.detectorSemanticDelta.theFix.requires ; $.detectorSemanticDelta.relationToFactIdentity ; $.custodyClasses[USER-CUSTODY].policy.dualEmit (line 60)
docs/coop/artifacts/fact-identity-policy.v2.json  $.custodyTransition.protocol.algorithmChangeToExistingLevel ; $.custodyTransition.protocol.migrationWitness.honesty
docs/v2/architecture/04-lifecycle-delivery-and-operations.md  lines 73-76, 130-137
docs/v2/architecture/13-evidence-workflows-and-product-contracts.md  §6 line 180
```

**SEM-02, HIGH, newly discovered defect. The fact plane cannot express "subject set complete, resolution incomplete for some members", so universal-negative claims over references are unsound under dynamic relationships.** The sufficiency function reads one scalar resolution, one confidence and one coverage value per relation from the view. The provider-side coverage result has a two-value state, complete or unknown, keyed by relation and rung. A TypeScript or Rust universe with computed property access, dynamic import, reflection, macro-generated calls or `any`-typed flow yields references that cannot reach the resolved-binding rung. The provider either reports the relation at resolved-binding with complete coverage, in which case a dead-code or "no consumers" predicate declaring completeness=complete is satisfied while unresolved references exist, or reports the lower rung for the whole relation, refusing every resolution-dependent predicate. The deficiency vocabulary has no member for unresolvable members in scope, and the rung-unavailable reasons are provider-not-installed, language-tier and budget only. Chapter 04 lists "unresolved references, dynamic dispatch" as required coverage machinery and chapter 13 §5 says "no references in the checked scope" is distinct from "no possible consumers", but the binding contract has no representation for that distinction. Counterevidence: known limitation R1-FP-03 defers honesty of coverage=complete to the evidence subject-set commitment; that commitment proves which subjects were evaluated, not that each subject's edges were resolvable. Required correction: a per-relation resolution-completeness dimension or an explicit unresolvable-count coverage state that blocks completeness=complete for universal negatives, plus the corresponding D9 deficiency member. Owners: DR-118 and DR-133, the FACT-PLANE closure items under DR-006 and DR-011-R01, DR-004 and DR-005. Confidence: high.

```
docs/coop/artifacts/check-fact-plane.py  def sufficiency (lines 571-612)
docs/coop/artifacts/fact-plane.v1.json  $.sufficiency ; $.deficiencyVocabulary ; goldenCases name-match-does-not-satisfy-resolved ; knownLimitations[5]
docs/coop/artifacts/delivery.v2.json  CoverageResultV1.coverageState (line 825)
docs/coop/architecture/04-fact-plane.md  line 61 ; docs/v2/architecture/13-... §5 lines 158-161
```

**SEM-03, HIGH, integration gap. Rust dependency crate sources have no sealed path into the sidecar.** The snapshot descriptor seals project-relative files only, with symlinks committed as link targets and never followed. The Rust universe key commits the resolved package set as a Cargo.lock identity and per-project crate roots, but identity is not availability. The sidecar's forbidden list bars a live worktree root, host absolute paths, hidden CAS or digest-only fetch, and network fetch; the prepared-output mechanism covers build-script and proc-macro outputs under grant. Nothing states how registry crate sources or rlib metadata reach the pinned compiler. Trigger: any Rust project with a non-workspace dependency, which is nearly all of them. Consequence: cross-crate trait, type and call resolution is either unavailable, reported as provider-unavailable, or achieved by an implementer inventing an input class the laws forbid. Counterevidence: DR-118/119/120 are OPEN for the full product and could absorb this, but the sealed-read-set law and the forbidden list actively preclude the natural solutions, so this is a contract conflict, not only an unfilled cell. Required correction: a sealed dependency-source input class in the snapshot or universe contract with its own identity and privacy treatment, and a Rust protocol successor. Owners: DR-118/119/120 row, DR-011-R05. Confidence: medium; a mechanism under a name I did not search for is an untested assumption.

```
docs/coop/artifacts/resolved-inputs.v2.json  $.semanticUniverse.perProvider.rust.keyComponents (lines 1681-1694) ; rust-v1 crateRootPaths (line 942-950)
docs/coop/artifacts/rust-provider-protocol.v2.json  $.repositoryExecution.forbidden (lines 249-258) ; $.requestProjection.snapshot (line 262)
docs/coop/architecture/02-domain-model.md  SnapshotId recipe lines 165-173
```

**SEM-04, HIGH, known open contract, sharpened. The RunId recipe is simultaneously parked, refused and applied, and its real dependency chain is misstated.** The binding operability head says no RunId recipe is binding; freeze §7.1 forbids choosing between CSPRNG, descriptor-digest and evidence-digest forms because they have opposite retry-determinism consequences; the applied evidence-identity head refuses to endorse the evidence framing for exactly that reason. Yet the applied evidence head defines a run-identity preimage of schema major, project identity, plan identity, evaluation-authority seal reference, evidence digest and sealed capability, with no execution or attempt identity. That is a content-derived, retry-idempotent RunId, which is the decision §7.1 reserves. The freeze then says the RunId and EvidenceDigest chains "bottom out in capabilityManifestId"; they do not. That identity is now bound by the applied delivery head. The chains actually bottom out in the evaluation-authority seal, owned by an unapplied evaluation-proof artifact whose companion checker mints a wrong plan identity and which pins rejected C-2 bytes, and in the proof-bundle CAS reference, whose canonical-JSON profile exists only as an unapplied recovery with five undetermined rules. Consequence: durable results, baselines, stored views and second-process inspection all wait on a decision nobody has recorded as taken, while an implementer reading the applied head would take it silently. Required correction: an explicit owner decision on attempt versus content identity, then closure of the seal and canonical-JSON dependencies, with the freeze row corrected. Owners: DR-002, DR-006, DR-011-R12 and R15. Confidence: high on the dependency map, medium on whether content-derivation is wrong rather than merely undecided.

```
docs/coop/artifacts/evidence.v10.json  $.canonicalWireGrammar.records.RunIdentityPreimageV1 (lines 959-999), resolved terminus of applied evidence.v15
docs/coop/artifacts/evidence-identity-recipes.v5.json  $.notProposals.RunId (line 896-898) ; line 526-531, 956
docs/coop/IMPLEMENTATION-FREEZE.md  §7.1 rows RunId/EvidenceDigest ; line 1914
docs/coop/artifacts/canonical-json-profile.v1.json  $.status ; $.undeterminedRegister UR-1..5
```

**SEM-05, MEDIUM, documentation hazard. The freeze and register still park two identities that applied heads already bind.** Freeze §7.1, the RESOLVED-INPUTS row in §3, the file 08 "Exact DR-006 park coverage" note and the DR-009 row all record capabilityManifestId and policyOutcome.derivationDigest as fields with no producing rule. The applied delivery head binds CAP-MANIFEST-ID-V1 with a domain separator, admission gates and vectors, and the applied R-1 head carries POLICY-DERIVATION-DIGEST-V1; the blueprint's own correction box says these were "completed by the applied heads on 2026-08-05 and the prose was never updated". Consequence: the register's identity dependency graph is wrong in the direction of overstating what is open, which will misdirect the D-371 identity work and the DR-001 matrix refresh. Required correction: reconcile the three authority documents and the matrix through the DR-001 route. Owners: DR-006, DR-009, DR-011-R15, DR-001. Confidence: high.

```
docs/coop/IMPLEMENTATION-FREEZE.md  lines 1705-1709, 1914 ; §3 RESOLVED-INPUTS row line 381
docs/v2/architecture/08-decision-and-readiness-register.md  lines 63-73 ; DR-009 row line 48
docs/coop/artifacts/delivery.v4.json  $.operations capabilityManifestIdentity (lines 476-531)
docs/coop/IMPLEMENTER-BLUEPRINT.md  §5.1 correction box lines 1455-1471
```

**SEM-06, MEDIUM, integration gap. Imported runtime, test and history evidence has no identity slot.** Freeze law 2 says only declared analysis inputs may affect PlanId. The plan identity recipe has thirteen closed frames; the only plausible carriers are contributions, typed as rule, profile or provider contributions with bundle and artifact digests, and resolved configuration. The snapshot identity covers project-relative files. Chapter 13 §7 requires imported evidence to state source and build correspondence and to enter policy only through a separately admitted artifact and declared predicate, but no artifact defines that admission, no frame carries it, and the D9 code vocabulary has no evidence-import, replay or custody family at all. Trigger: a coverage or trace artifact captured against a different commit, imported for a cold-code predicate. Consequence: either the artifact cannot enter identity and the predicate cannot run, or it enters through an untyped frame and two runs with one PlanId can disagree. Required correction: a versioned plan-identity frame or snapshot descriptor extension for admitted evidence artifacts, with freshness and binding validation and typed refusals. Owners: DR-118/119/120 row for adapters, the DR-002 to DR-009 obligation row for identity joins, DR-007 for D9 vocabulary. Confidence: high on absence.

```
docs/coop/artifacts/resolved-inputs.v2.json  $.planIdContract.requiredInTagOrder (line 811) ; contributions frame (lines 761-764)
docs/coop/artifacts/d9-exit-contract.v1.14.json  $.codeVocabulary (no EVIDENCE./IMPORT./REPLAY./CUSTODY. members)
docs/v2/architecture/13-... §7 lines 219-233
```

**SEM-07, MEDIUM, integration gap. The binding comparison schema cannot express the attribution classes chapter 13 §6 now requires.** The versioning head's comparison result has a closed classification enum of five values and a closed indeterminate-reason enum of three values, all detector-centred. Chapter 13 §6, adopted by D-370, requires separating code changes from detector changes, policy changes, scope changes, waivers and changes in evidence availability, and requires an incompatible-scope refusal when diff scope and comparison base disagree. Every versioning successor from v9 to v17 is rejected or unreviewed. Consequence: a policy-only tightening surfaces as CODE-NET-NEW or as an unexplained indeterminate, which is the misattribution the constraint forbids. Required correction: a versioning successor extending both closed enums and adding policy and scope context identities to the comparison record. Owners: DR-111, the DR-006/111/122/123/130 row, DR-011-R13. Confidence: high.

```
docs/coop/artifacts/versioning-policy.v8.json  $.comparisonSchema.ComparisonResult.classification.values ; .indeterminateReason.values (lines 2997-3016)
docs/v2/architecture/13-... §6 lines 185-198
```

**SEM-08, MEDIUM, integration gap. The applied retention default and the preserved no-write law are unreconciled, and the full product's default request class is unstated.** The product decision CD-RT-5 is binding and not challenged here. Under it, a durable-authoritative request with no policy proceeds and writes with provenance DEFAULTED, and the retention head names CI as "precisely where durable evidence is now written with provenance DEFAULTED and no prospect of the provenance ever becoming CONSENTED". V2 chapter 01 preserves the V1 law that the first useful project interaction remains no-write, and chapter 06 still says persistent custody requires explicit policy and that without one the only safe default is ephemeral operation. For the preview there is no conflict because analyze is non-authoritative. For the intended product, whether the default analyze is a durable-authoritative request decides whether the first run in CI writes fact tuples carrying paths and dirty blobs into runner state under defaulted consent. No row states that decision. Required correction: the full-product analyze contract must name its default request class and the register must record the reconciliation of the preserved law, with chapter 06 updated. Owners: the DR-002 to DR-009 obligation row, DR-008 and DR-113, the DR-010/117/131/133 row, product owner. Confidence: medium.

```
docs/coop/artifacts/retention-tiers.v26.json  $.noAskCasesReDerived[0] (lines 1226-1245), resolved base of applied v28
docs/v2/architecture/01-semantic-model-and-host-authority.md  line 183
docs/coop/architecture/06-evidence-and-persistence.md  lines 319-325, 361-382
```

**SEM-09, LOW, newly discovered defect. Two binding heads assign the wrong remedy class to incomplete input closure.** The delivery head maps missing node_modules or package-resolution entries to Coverage provider-unavailable, and the resolved-inputs head maps an unconstructed universe dimension to the same value. The fact plane defines that deficiency's remedy as "install or enable the provider", and chapter 07 says conflated remedies destroy the agent's next action. Correction: a distinct deficiency for incomplete input closure, or an explicit mapping to required-relation-missing with a widen-inputs remedy. Owners: DR-118, DR-011-R01 and R04. Confidence: high.

```
docs/coop/artifacts/delivery.v2.json  line 1130 ; docs/coop/artifacts/resolved-inputs.v2.json  $.semanticUniverse.completenessRule, .rust.ifIncomplete (lines 1677, 1694)
docs/coop/artifacts/fact-plane.v1.json  $.sufficiency.deficiencyDiscrimination.cases[1]
```

**SEM-10, LOW, documentation hazard. Several narrative and manifest surfaces describe superseded states.** V2 chapter 01 says the evidence head is v10 and unapplied; v15 was applied under D-014. Chapter 06 says the retention head selects no default and that ephemeral operation is admissible "while CD-RT-5 is blocked"; it is decided. Chapter 07's remaining-work item two, the baseline prohibited-effect golden, is already discharged by the D9 head's no-mass-net-new invariant. Chapter 09 names retention v24 as head. The D-369 application manifest self-declares "WORKING-INTEGRATION-NOT-FROZEN-OR-ADOPTED" with applied:false while D-369 binds that exact digest, and its checker's target and deferred row sets are the preview twenty-three plus nine, so a green run says nothing about the twenty-eight-row full-product set. Owners: DR-001 and DR-011 hygiene, documentation custody. Confidence: high.

```
docs/v2/architecture/01-... lines 16-21 ; docs/coop/architecture/06-... lines 361-382 ; 07-... lines 190-192 ; 09-... row 48
docs/coop/completion/architecture-application.v1.json  $.status ; $.documentationApplication.applied ; $.enactmentPlan.alreadyEnacted
docs/coop/completion/check-architecture-application.v1.py  lines 42-45 ; docs/coop/artifacts/d9-exit-contract.v1.14.json invariant-baseline-no-mass-netnew (line 1369)
```

## Strengths and scenario traces

Substantive strengths worth retaining:

- **Predicate-relative sufficiency is mechanised, not sloganised.** Per-relation ladders, the forbidden global-rank fields, and the rule that a one-rung ladder is never degraded make freeze law 3 checkable. SEM-02 is a gap inside this model, not an argument against it.
- **Termination is a total union with an executable oracle.** Closed cause enums, forty-five goldens, the baseline no-mass-net-new invariant, and the tombstone requirement for IDENTITY.EXPIRED are exactly the axis separations a CI consumer needs.
- **Identity discipline is unusually honest.** Exact-type admission as law 18, namespace minting as law 19, RequestId and ExecutionId excluded from semantic identity, and §7.1 stated as a property rather than a list all survive scrutiny.
- **Provider boundaries are byte-bound.** Sealed VFS transport with manifest, chunk and seal commitments, candidate-only authority until zero exit and EOF, and host-recomputed universe keys are strong.
- **Evidence-first proof attaches to evaluations including no-match, and purge is degradation with tombstones**, with sealed capability immutable and effective capability derived at read time.
- **The three-way detector pivot with INDETERMINATE never blaming code** is the right shape; SEM-01 asks for its precondition to be owned.
- **Derivation resolution and review-binds-bytes-and-environment** are process rules that caught real defects and should not be relaxed.

Scenario traces, each against source bytes:

| Scenario | Result |
|---|---|
| Mixed-language monorepo with dynamic relationships | Unsound universal negatives (SEM-02); Rust dependency sources unsealed (SEM-03); wrong remedy class (SEM-09). Cross-language edges correctly fall to Coverage. |
| Repeat evaluation after evidence loss or tool/policy change | Loss changes only effective capability and typed refusal, never RunId or digest, and IDENTITY.EXPIRED needs a tombstone: sound. Tool change moves PlanId through contributions: sound. Detector pivot precondition unowned (SEM-01); policy-change attribution inexpressible (SEM-07); replay loss result and exit remain the known DR-007/113 gap. |
| Source moves and renames | Root move preserves project identity via registry rebind. File rename correspondence depends on the finding fingerprint recipe, whose ruleId join and ruleMajor rule are open (OPEN-DEP-FI-01..07) and whose stability classes have no recipe. Known open under the DR-006/111/122/123/130 row; no new finding. |
| Cold-code claim under partial coverage | Subject-set completeness is checkable; edge-resolution completeness is not (SEM-02). Runtime observation limits are stated in chapter 13 §7 but have no identity slot (SEM-06). |
| Stale or corrupt evidence import | No admission contract, identity frame or D9 refusal family (SEM-06). |
| Snapshot with mutable compiler inputs | TypeScript: node_modules entries are VFS entries and the universe key binds compiler and stdlib identities: sound. Rust: cfg corpus enters via prepared outputs under grant: sound; dependency sources unsealed (SEM-03). |

## Coverage

Read in full or by cited section: docs/v2/architecture files 00, 01, 04 sections at lines 1-140 and 195-254, 08 lines 36-213 and 297-320 and 376-505, 09, 10, 12 lines 1-80, 13; docs/coop/architecture chapters 02, 03, 04, 05, 06, 07, 09 lines 1-80; IMPLEMENTATION-FREEZE §3 lines 285-700, §6 lines 1405-1580, §7.1 lines 1675-2268; IMPLEMENTER-BLUEPRINT §1.1 lines 121-837 and §5.1 lines 1352-1471; COORDINATOR-DECISIONS D-003, D-014, D-077, D-078, D-369, D-370, D-371; reference-architecture.v2; architecture-application.v1.json lines 1-120 and 8900-9040 and its freeze v6; the dependency supplement lines 1-250 and the named-open-condition entries; check-architecture-application.v1.py lines 1-160; D-371 act, subject and Claude review v2; FALLOW-BORROW-REGISTER lines 43-97. Artifacts read by selector: fact-plane.v1 envelope, registry, requirement, sufficiency, deficiency, profiles, goldens, limitations; check-fact-plane.py sufficiency; fact-identity-policy.v2 custody transition and language capability; resolved-inputs.v2 plan-identity frames, semantic universes, change spec; delivery.v2 snapshot transport and coverage result; delivery.v4 capability-manifest identity; rust-provider-protocol.v2 repository execution and request projection; versioning-policy.v8 custody policy, detector delta, comparison schema; evidence.v10 run-identity preimage, sealed capability, availability differential; evidence-identity-recipes.v5 and v12 selected blocks; retention-tiers.v26 and v28 selected blocks; d9-exit-contract.v1.14 baseline, expired and code selectors; canonical-json-profile.v1 header and undetermined register; product-dispositions CD-RT-5 not-done block; r1 v1.9 open dependencies.

Not reviewed: threat-model.v3 body, operability.v10 body, trusted-request-context.v3, c2-plan-stage-schema.v4 body, evaluation-proof.v8 body, lifecycle-generation-contract.v2 body, all security, broker, host-effect and doctor completion artifacts, the D-370 fallow-review subject bytes, the quality and protocol corpora, and every checker other than the two named. Untested assumptions: that no Rust dependency-source mechanism exists under a name outside my search terms; that no lock or lifecycle artifact retains superseded detector closures; that the resolved evidence.v15 value preserves the v10 run-identity preimage unchanged, which D-014 states but I did not resolve myself; SHA-256 values were not recomputed.

```json
{
  "reviewer": "Claude (Anthropic), model claude-fable-5-1, independent Lens A review",
  "lens": "A — semantic correctness, evidence and analysis",
  "readiness": "NOT_READY",
  "findings": [
    {
      "id": "SEM-01",
      "severity": "HIGH",
      "classification": "newly_discovered_defect",
      "title": "Detector-pivot precondition misattributed to fact-identity dual-emit; no lifecycle root keeps detector0 runnable",
      "source": [
        "docs/coop/artifacts/versioning-policy.v8.json#$.detectorSemanticDelta.theFix.requires",
        "docs/coop/artifacts/versioning-policy.v8.json#$.detectorSemanticDelta.relationToFactIdentity",
        "docs/coop/artifacts/versioning-policy.v8.json line 60 ($.custodyClasses USER-CUSTODY policy.dualEmit)",
        "docs/coop/artifacts/fact-identity-policy.v2.json#$.custodyTransition.protocol.migrationWitness.honesty",
        "docs/v2/architecture/04-lifecycle-delivery-and-operations.md lines 73-76, 130-137",
        "docs/v2/architecture/13-evidence-workflows-and-product-contracts.md line 180"
      ],
      "trigger": "Detector major changes on a project holding a committed baseline; gate-compare requested.",
      "consequence": "Pivot cannot run because detector0 is neither retained by lifecycle GC roots nor reproducible by identity dual-emit; every affected detector reports INDETERMINATE (exit 3), blocking CI on each detector-major crossing.",
      "counterevidence_considered": "INDETERMINATE fallback is safe by design; VER-PIVOT-COST-GATE keeps pivot off ordinary analysis; chapter 13 §6 nonetheless treats the pivot architecture as preserved and settled.",
      "required_correction": "Own the precondition: retain superseded detector closures as GC roots with compatibility windows or ship prior algorithm versions inside components; VERSIONING successor must stop citing fact-identity as the supplier.",
      "register_owner": "DR-006/111/122/123/130 obligation row; DR-107, DR-127; DR-011-R13",
      "confidence": "high on misattribution; medium on absence of any retention root (grep-based)"
    },
    {
      "id": "SEM-02",
      "severity": "HIGH",
      "classification": "newly_discovered_defect",
      "title": "Fact-plane sufficiency cannot represent resolution-incomplete views; universal-negative predicates over references are unsound under dynamic relationships",
      "source": [
        "docs/coop/artifacts/check-fact-plane.py lines 571-612 (def sufficiency)",
        "docs/coop/artifacts/fact-plane.v1.json#$.sufficiency, $.deficiencyVocabulary, goldenCases[name-match-does-not-satisfy-resolved], knownLimitations[5]",
        "docs/coop/artifacts/delivery.v2.json line 825 (CoverageResultV1.coverageState enum complete|unknown)",
        "docs/coop/architecture/04-fact-plane.md line 61",
        "docs/v2/architecture/13-evidence-workflows-and-product-contracts.md lines 158-161"
      ],
      "trigger": "Dead-code or no-consumers predicate requiring references@resolved-binding with completeness=complete over a universe containing computed access, dynamic import, reflection or macro-generated references.",
      "consequence": "Provider must report one scalar rung per relation; reporting resolved-binding with coverage complete yields a satisfied universal negative while unresolvable references exist; reporting the lower rung refuses all resolution predicates. False cold-code findings and unsafe repair preconditions.",
      "counterevidence_considered": "R1-FP-03 defers coverage=complete honesty to the EVIDENCE subject-set commitment, which proves subject membership, not per-subject edge resolvability.",
      "required_correction": "Add a resolution-completeness dimension or unresolvable-count coverage state per relation that blocks completeness=complete for universal negatives; add matching deficiency and D9 member.",
      "register_owner": "DR-118, DR-133; FACT-PLANE closure under DR-006 and DR-011-R01; DR-004/DR-005",
      "confidence": "high"
    },
    {
      "id": "SEM-03",
      "severity": "HIGH",
      "classification": "integration_gap",
      "title": "Rust dependency crate sources have no sealed input path",
      "source": [
        "docs/coop/artifacts/resolved-inputs.v2.json lines 1681-1694 ($.semanticUniverse.perProvider.rust.keyComponents), lines 942-950 (rust-v1 crateRootPaths)",
        "docs/coop/artifacts/rust-provider-protocol.v2.json lines 244-258 ($.repositoryExecution.forbidden), line 262 ($.requestProjection.snapshot)",
        "docs/coop/architecture/02-domain-model.md lines 165-173 (SNAPSHOT-ID-V1 descriptor)"
      ],
      "trigger": "Any Rust project with a non-workspace dependency.",
      "consequence": "Cross-crate resolution is unavailable or requires an implementer to invent an input class the sealed-read-set law and forbidden list preclude; Rust native depth promised by D-371 is unreachable as contracted.",
      "counterevidence_considered": "DR-118/119/120 are OPEN for full product; prepared outputs cover build-script/proc-macro cfg. Neither supplies dependency sources.",
      "required_correction": "Define a sealed dependency-source input class with identity and privacy treatment in the snapshot or universe contract; RUST-PROVIDER-PROTOCOL successor.",
      "register_owner": "DR-118/119/120 row; DR-011-R05",
      "confidence": "medium (untested: a mechanism under a name outside search terms)"
    },
    {
      "id": "SEM-04",
      "severity": "HIGH",
      "classification": "known_open_contract",
      "title": "RunId recipe is parked, refused and applied at once; dependency chain misstated as bottoming out in capabilityManifestId",
      "source": [
        "docs/coop/artifacts/evidence.v10.json lines 959-999 ($.canonicalWireGrammar.records.RunIdentityPreimageV1; terminus of applied evidence.v15)",
        "docs/coop/artifacts/evidence-identity-recipes.v5.json lines 896-898 ($.notProposals.RunId), 526-531, 956",
        "docs/coop/IMPLEMENTATION-FREEZE.md §7.1 RunId row and line 1914",
        "docs/coop/artifacts/canonical-json-profile.v1.json $.status, $.undeterminedRegister UR-1..5",
        "docs/coop/artifacts/operability.v10.json $.requestIdContract.fixtures[8].parked (as quoted by freeze)"
      ],
      "trigger": "Any attempt to seal an authoritative Run, serve a stored view, or retry an attempt.",
      "consequence": "Applied head implies content-derived retry-idempotent RunId with no attempt identity, the decision §7.1 reserves; true blockers are the evaluation-authority seal (unapplied EP8 with defective checker, pinning rejected C-2 v3) and the proof-bundle CAS ref's canonical-JSON profile with five undetermined rules, not capabilityManifestId.",
      "counterevidence_considered": "D-014 applied v15 while stating no recipe is unparked; evidence-first design may intend content-addressed Runs with separate AttemptRecords.",
      "required_correction": "Record an explicit owner decision on attempt-vs-content Run identity; close EP seal and canonical-JSON dependencies; correct freeze §7.1 dependency statement.",
      "register_owner": "DR-002, DR-006, DR-011-R12, DR-011-R15",
      "confidence": "high on dependency map; medium on whether content-derivation is wrong rather than undecided"
    },
    {
      "id": "SEM-05",
      "severity": "MEDIUM",
      "classification": "documentation_hazard",
      "title": "Freeze §7.1, §3 and file 08 still park capabilityManifestId and policyOutcome.derivationDigest although applied heads bind them",
      "source": [
        "docs/coop/IMPLEMENTATION-FREEZE.md lines 1705-1709, 1914; §3 RESOLVED-INPUTS row line 381",
        "docs/v2/architecture/08-decision-and-readiness-register.md lines 63-73 (Exact DR-006 park coverage); DR-009 row line 48",
        "docs/coop/artifacts/delivery.v4.json lines 476-531 (capabilityManifestIdentity, CAP-MANIFEST-ID-V1)",
        "docs/coop/artifacts/r1-lifetime-neutrality.conformance.v1.6.json line 1831 (POLICY-DERIVATION-DIGEST-V1)",
        "docs/coop/IMPLEMENTER-BLUEPRINT.md lines 1455-1471"
      ],
      "trigger": "D-371 identity-contract work or DR-001 matrix refresh reads the register's park list.",
      "consequence": "Open-identity set overstated; effort misdirected; the RunId/EvidenceDigest blocker misidentified.",
      "counterevidence_considered": "Blueprint §5.1 correction box already discloses the staleness; the register may retain history deliberately, but the park-coverage note is presented as current boundary.",
      "required_correction": "Reconcile freeze §3/§7.1, file 08 DR-006 note and DR-009 row, and the claim matrix via the DR-001 route.",
      "register_owner": "DR-006, DR-009, DR-011-R15, DR-001",
      "confidence": "high"
    },
    {
      "id": "SEM-06",
      "severity": "MEDIUM",
      "classification": "integration_gap",
      "title": "Imported runtime/test/history evidence has no identity slot and no typed refusal family",
      "source": [
        "docs/coop/artifacts/resolved-inputs.v2.json line 811 ($.planIdContract.requiredInTagOrder), lines 761-764 (contributions frame)",
        "docs/coop/artifacts/d9-exit-contract.v1.14.json $.codeVocabulary (no EVIDENCE./IMPORT./REPLAY./CUSTODY. members)",
        "docs/coop/IMPLEMENTATION-FREEZE.md §6 law 2",
        "docs/v2/architecture/13-evidence-workflows-and-product-contracts.md lines 215-239"
      ],
      "trigger": "Coverage or trace artifact captured against a different build imported for a cold-code predicate; stale or corrupt artifact.",
      "consequence": "Artifact cannot lawfully affect PlanId, or enters through an untyped frame so equal PlanIds diverge; no typed stale/corrupt refusal.",
      "counterevidence_considered": "Chapter 13 §7 correctly states binding dimensions and observation limits; DR-118/119/120 mention adapters and source mapping; PLAN-ID-V1 is versioned and extensible.",
      "required_correction": "Versioned plan-identity frame or snapshot-descriptor extension for admitted evidence artifacts with freshness and binding validation; D9 refusal family via DR-007 successor.",
      "register_owner": "DR-118/119/120 row; DR-002–009 row; DR-007",
      "confidence": "high on absence"
    },
    {
      "id": "SEM-07",
      "severity": "MEDIUM",
      "classification": "integration_gap",
      "title": "VERSIONING comparison enums cannot express chapter 13 §6 attribution classes",
      "source": [
        "docs/coop/artifacts/versioning-policy.v8.json lines 2997-3016 ($.comparisonSchema.ComparisonResult.classification.values; .indeterminateReason.values)",
        "docs/v2/architecture/13-evidence-workflows-and-product-contracts.md lines 185-198",
        "docs/v2/architecture/08-decision-and-readiness-register.md DR-011-R13 row (line 94)"
      ],
      "trigger": "Policy-only tightening, scope change, waiver change, or evidence-availability change between baseline and current.",
      "consequence": "Result must be CODE-NET-NEW, DETECTION-DELTA, CODE-FIXED, UNCHANGED or INDETERMINATE with a detector-only reason; policy and scope deltas are misattributed or unexplained.",
      "counterevidence_considered": "D-370 declared no preview contract change; for the full product a successor is nonetheless mandatory and v9–v17 are all rejected or unreviewed.",
      "required_correction": "VERSIONING successor extending both closed enums and adding policy/scope/evidence-availability context identities to ComparisonResult.",
      "register_owner": "DR-111; DR-006/111/122/123/130 row; DR-011-R13",
      "confidence": "high"
    },
    {
      "id": "SEM-08",
      "severity": "MEDIUM",
      "classification": "integration_gap",
      "title": "Applied implicit durable retention unreconciled with preserved no-write first interaction; full-product default request class unstated",
      "source": [
        "docs/coop/artifacts/retention-tiers.v26.json lines 1226-1245 ($.noAskCasesReDerived[0]; resolved base of applied v28)",
        "docs/v2/architecture/01-semantic-model-and-host-authority.md line 183",
        "docs/coop/architecture/06-evidence-and-persistence.md lines 319-325, 361-382",
        "docs/v2/architecture/08-decision-and-readiness-register.md line 405 (DR-002–009 obligation row)"
      ],
      "trigger": "First authoritative analyze on a project with no retention policy, especially in CI.",
      "consequence": "Either durable user-derived evidence (paths, dirty blobs) is written under DEFAULTED consent on the first run, or the product's default run is ephemeral and durable results are not produced by default; the design does not say which.",
      "counterevidence_considered": "CD-RT-5 is a binding product decision and is not challenged; v28 keeps first-run disclosure and never persists a defaulted policy; the preview is non-authoritative so no preview conflict exists.",
      "required_correction": "Full-product analyze contract states its default request class; register records reconciliation of the preserved no-write law; chapter 06 updated.",
      "register_owner": "DR-002–009 row; DR-008, DR-113; DR-010/011-R16/117/131/133 row; product owner",
      "confidence": "medium"
    },
    {
      "id": "SEM-09",
      "severity": "LOW",
      "classification": "newly_discovered_defect",
      "title": "Incomplete input closure mapped to provider-unavailable, whose remedy is wrong",
      "source": [
        "docs/coop/artifacts/delivery.v2.json line 1130 ($.typescriptSemanticSubstrate...snapshotTransport.packageResolution)",
        "docs/coop/artifacts/resolved-inputs.v2.json lines 1677, 1694 ($.semanticUniverse.completenessRule; .rust.ifIncomplete)",
        "docs/coop/artifacts/fact-plane.v1.json $.sufficiency.deficiencyDiscrimination.cases[1]",
        "docs/coop/architecture/07-outcomes-and-failure.md lines 167-175"
      ],
      "trigger": "Missing node_modules entry or unconstructed cfg dimension with the provider installed.",
      "consequence": "Consumer is told to install or enable a provider that is present; agent remediation misdirected.",
      "counterevidence_considered": "Remedy order is declared a judgment in fact-plane knownLimitations[2]; the misuse is still cross-artifact vocabulary drift.",
      "required_correction": "Distinct input-closure deficiency or explicit mapping to required-relation-missing with widen-inputs remedy.",
      "register_owner": "DR-118; DR-011-R01, DR-011-R04",
      "confidence": "high"
    },
    {
      "id": "SEM-10",
      "severity": "LOW",
      "classification": "documentation_hazard",
      "title": "Stale narrative and manifest self-status after applications and D-369/D-371",
      "source": [
        "docs/v2/architecture/01-semantic-model-and-host-authority.md lines 16-21",
        "docs/coop/architecture/06-evidence-and-persistence.md lines 361-382; 07-outcomes-and-failure.md lines 190-192; 09-open-decisions.md row 48",
        "docs/coop/completion/architecture-application.v1.json $.status, $.documentationApplication.applied, $.enactmentPlan.alreadyEnacted",
        "docs/coop/completion/check-architecture-application.v1.py lines 42-45",
        "docs/coop/artifacts/d9-exit-contract.v1.14.json line 1369 (invariant-baseline-no-mass-netnew)"
      ],
      "trigger": "Reader resolves current heads from narrative chapters or trusts a green application checker for full-product standing.",
      "consequence": "Wrong head selection or a preview-scoped checker read as full-product evidence.",
      "counterevidence_considered": "Chapters carry preview-application banners and blueprint reading rule 2 covers self-declarations; hazard remains for chapter 06/07/09 statements with no banner.",
      "required_correction": "Narrative refresh under the DR-001 matrix route; manifest self-status annotation or enactment note.",
      "register_owner": "DR-001, DR-011; documentation custody",
      "confidence": "high"
    }
  ],
  "strengths": [
    "Predicate-relative sufficiency mechanised: per-relation ladders, forbidden global-rank fields, one-rung ladders never degraded (fact-plane.v1 F8; freeze law 3).",
    "Total termination union with executable oracle, closed cause enums, baseline no-mass-net-new invariant and tombstone-gated IDENTITY.EXPIRED (d9 v1.14).",
    "Identity discipline: exact-type admission (law 18), namespace minting by owner (law 19), RequestId/ExecutionId exclusion, §7.1 stated as a property.",
    "Byte-bound provider boundary: sealed VFS transport with manifest/chunk/seal commitments, candidate-only authority until zero exit and EOF, host-recomputed universe keys.",
    "Evidence-first proof per evaluation including no-match; PURGED as degradation with tombstones; sealed capability immutable, effective capability derived at read time.",
    "Three-way detector pivot with INDETERMINATE never attributing delta to code (needs its precondition owned, SEM-01).",
    "Derivation-resolution discipline and review-binds-bytes-and-environment rule; chapter 13's separation of observed facts, product defaults and project decisions."
  ],
  "coverage": {
    "read_in_full_or_by_section": [
      "docs/v2/architecture/00-status-and-authority.md lines 1-70",
      "docs/v2/architecture/01-semantic-model-and-host-authority.md (full)",
      "docs/v2/architecture/04-lifecycle-delivery-and-operations.md lines 1-140, 195-254",
      "docs/v2/architecture/08-decision-and-readiness-register.md lines 36-213, 297-320, 376-505",
      "docs/v2/architecture/09-v1-to-v2-claim-matrix.md (full)",
      "docs/v2/architecture/10-mvp-and-future-scope.md (full)",
      "docs/v2/architecture/12-architecture-completion-goal.md lines 1-80",
      "docs/v2/architecture/13-evidence-workflows-and-product-contracts.md (full)",
      "docs/coop/architecture/02,03,04,05,06,07 (full); 09 lines 1-80",
      "docs/coop/IMPLEMENTATION-FREEZE.md §3 lines 285-700, §6 lines 1405-1580, §7.1 lines 1675-2268",
      "docs/coop/IMPLEMENTER-BLUEPRINT.md §1.1 lines 121-837, §5.1 lines 1352-1471",
      "docs/coop/COORDINATOR-DECISIONS.md D-003, D-014, D-077, D-078, D-369, D-370, D-371",
      "docs/coop/completion/reference-architecture.v2.md (full); architecture-application.v1.json lines 1-120, 8900-9040; architecture-application-freeze.v6.json; architecture-incorporated-dependency-supplement.v1.json lines 1-250 and named-open-condition entries; check-architecture-application.v1.py lines 1-160",
      "docs/coop/unified-design-review/D-371-design-target.v1.md, claude-review.v2.md",
      "docs/coop/FALLOW-BORROW-REGISTER.md lines 43-97"
    ],
    "artifacts_read_by_selector": [
      "fact-plane.v1.json (envelope, relationRegistry, requirementSchema, sufficiency, deficiencyVocabulary, profiles, goldenCases, conformanceClaims, knownLimitations); check-fact-plane.py sufficiency",
      "fact-identity-policy.v2.json (custodyTransition, languageCapability, anchorValidation head)",
      "resolved-inputs.v2.json (planIdContract frames, semanticUniverse, changeSpec, rust-v1 canonicalization)",
      "delivery.v2.json (snapshotTransport, CoverageResultV1, TypeScriptSemanticUniverse schemas); delivery.v4.json (capabilityManifestIdentity)",
      "rust-provider-protocol.v2.json (repositoryExecution, requestProjection, snapshot limits); rust-provider-protocol.v4.json top-level keys",
      "versioning-policy.v8.json (custody policy, detectorSemanticDelta, comparisonSchema)",
      "evidence.v10.json (RunIdentityPreimageV1, sealedCapabilityContract, availabilityDifferential); evidence.v15.json header; evidence-identity-recipes.v5/v12 selected blocks",
      "retention-tiers.v26.json (noAskCasesReDerived, consent selectors); retention-tiers.v28.json header",
      "d9-exit-contract.v1.14.json (baseline, expired goldens; invariants; code vocabulary greps)",
      "canonical-json-profile.v1.json (header, undeterminedRegister); product-dispositions.v1.json (CD-RT-5 not-done block); r1 v1.9 open dependencies"
    ],
    "scenarios_traced": [
      "mixed-language monorepo with dynamic relationships",
      "repeat evaluation with evidence loss and with tool/policy version change",
      "source moves and renames with stable finding matching",
      "cold-code claim under partial coverage",
      "stale or corrupt evidence import",
      "snapshot capture with mutable compiler inputs (TypeScript node_modules, Rust cfg and dependencies)"
    ],
    "untested_assumptions": [
      "No Rust dependency-source sealing mechanism exists under a name outside the searched terms (registry, vendor, cargo, rlib, rmeta, extern, dependenc).",
      "No lock or lifecycle artifact retains superseded detector closures for baseline pivot.",
      "The resolved evidence.v15 value preserves v10's RunIdentityPreimageV1 unchanged (stated by D-014; not resolved independently).",
      "SHA-256 values and checker executions were not recomputed."
    ]
  },
  "not_reviewed": [
    "threat-model.v3.json body and storage-namespace derivation body",
    "operability.v10.json and trusted-request-context.v3.json bodies",
    "c2-plan-stage-schema.v4/v9/v10/v11 bodies",
    "evaluation-proof.v8 and v13 bodies",
    "lifecycle-generation-contract.v2, leftover-join, DR-G18 harness bodies",
    "all security, broker, host-effect, doctor, CI-carrier and compatibility completion artifacts",
    "D-370 fallow-review subject bytes; quality and protocol corpora",
    "every retained checker other than check-fact-plane.py and check-architecture-application.v1.py",
    "docs/v2/architecture chapters 02, 03, 05, 07, 11 and the prototype evidence reference"
  ]
}
```