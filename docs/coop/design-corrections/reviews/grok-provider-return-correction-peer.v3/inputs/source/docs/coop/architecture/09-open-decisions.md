# 09 — Open decisions

**Status:** the register of what is *not* settled in the greenfield design.

Migration sequencing, feature-parity coverage, and compatibility questions are
**not** here — they belong to `../steering/` and must not constrain anything in
this tree.

---

## Reopened by the greenfield re-derivation

| # | Decision | Why it reopened |
|---|----------|-----------------|
| **R-1** | **Execution topology** | **V1 CLOSED BY SCOPE / SEAL-WITH-CHANGES recommendation:** one-shot orchestration host plus pure data-only core. Resident host, autostart/default, and per-project/multi-project residency are parked outside v1 behind measurement and product scope change. Runtime denial remains NOT DISCHARGED; dependent authority modes are excluded. The original reopening history remains in [08](08-surfaces-and-topology.md). |
| **R-2** | **How much of the rule surface is declaratively expressible** | Any figure derived from an existing corpus measures that corpus's constraints. Richer facts expand the declarative surface, so the split must be measured **against a real fact schema on real rules** — not predicted from an existing implementation. |

## Decisions that need a product owner, not another reviewer

| # | Question | Why it matters | Standing lean |
|---|----------|----------------|---------------|
| **P-1** | Is a **third-party rule ecosystem** a real goal? | Determines whether the fact-query and rule IR become supported public contracts with all the freeze cost that implies, and whether signing, admission, and a marketplace are required | Design the **boundary** as if yes; build **depth** only on explicit commitment |
| **P-2** | **Contribution ontology:** narrow producers and data-only profiles, vs full third-party lifecycle parity | The largest remaining fork. Narrow contributions are the recommendation; parity would reopen the extension ABI, command grammar, and substrate packaging | Narrow + the policy boundary in [05](05-rules-and-extensions.md) |
| ~~**P-4a**~~ | ~~Which **Rust semantic substrate**?~~ | **DECIDED:** bundled exactly pinned `rustc_driver` sidecar, one supervised process per Rust semantic universe. Compiler/toolchain/sysroot/provider identities and offline assets enter the signed manifest and PlanId; repository build execution is denied by default and requires a per-project grant | Closed by `delivery.v4.json#rustSemanticSubstrate`; instability is contained behind the provider protocol |
| **P-3** | How much **cross-language rule portability** is required? | Sets fact-schema richness. Deep-single-language with breadth-as-checkbox needs far looser normalization than true portability | Normalize at the syntax and reference layers; provider namespaces above |
| ~~**P-4**~~ | ~~Which languages get semantic providers?~~ | **DECIDED by product owner: TypeScript and Rust**, with the capability tier surfaced loudly. Recorded in `../artifacts/claim-register.v1.json`; consequences in [04](04-fact-plane.md#provider-coverage-and-the-capability-tier) | Closed — a third provider requires a fresh disposition under the same evidence gate |

---

## Design questions still open

| Area | Open question | Status |
|------|---------------|--------|
| Fact schema | Body-hash normalization policy | **SEAL-WITH-CHANGES recommendation** — `../artifacts/fact-identity-policy.v2.json` plus `fact-identity-policy.freeze-closure-coordinator.v1.json`. Ladder, L1 default, framed byte grammar, capability matrix, and many-to-many transition protocol are fixed. Corpora remain implementation evidence; third-party imperative authority remains excluded |
| Fact schema | Language-specific namespaces vs the normalized core | **CANDIDATE** — `../artifacts/fact-plane.v1.json` relation registry: a `language-namespace` layer with per-relation ladders. Membership is illustrative; the SHAPE is the contract |
| Storage | When a columnar or vectorised engine earns its complexity | Deferred behind a benchmark |
| Rules | Imperative escape hatch contract and budget model | **EXCLUDED FROM INITIAL PRODUCT** — `../artifacts/fact-identity-policy.v2.json` and `delivery.v4.json`. The no-ambient-authority claim is retracted; an imperative contribution cannot be admitted until a restricted runtime exists |
| Rule/Probe authority | Whether effectful work is truly unrepresentable as a Rule, and which runtime enforces the boundary | **REOPENED (ARCH.PROBE-CONTRACT)** — interface labels do not confine linked TCB code; see `../artifacts/architecture.review-b.json` |
| Probe | Whether the effectful stage ships in a first release | **DECIDED: NO** — Probe, scenario-effectful, untrusted, and network-granted analysis modes are rejected until ARCH.PROBE-CONTRACT supplies a tested capability mechanism |
| Outcomes | Termination architecture | **CANDIDATE, independently reviewed, not applied** — `../artifacts/d9-exit-contract.v1.14.json`, validated by `check-d9-v1.14.py`. Independent pre-freeze review of exactly those bytes: PASS, 0 blocking, 2 advisories tabled as verifier residuals. 45 goldens. The review blocker is closed; what is open is that the total axes-to-class function lives in the checker's `referenceDerivation`, not the JSON, and that two consumers still pin the prior version v1.13 |
| Config + project model | Precedence, provenance, scope, change detection, path policy, **ambient-input closure** | **CANDIDATE, contract-complete** — `../artifacts/resolved-inputs.v2.json`. A1-RI-04 (untracked overrides that can flip CI) needs a **product** owner; TM owes an F8-class secret-value finding |
| Security | Threat model | **CANDIDATE** — `../artifacts/threat-model.v3.json`. Reviewer defects are repaired, but **V10 is `UNRESOLVED` in the artifact's own bytes** and its `requiredResolution` is open. An earlier revision of this row claimed V10 was RESOLVED-BY-DISPOSITION against the superseded `retention-tiers.v5` plus `evidence.v1`; v5 was independently **REJECTED** and `evidence.v1` was never independently accepted, so that disposition never existed. All privacy/offline publication remains **BLOCKED**: no R1-R18 property is DEMONSTRATED |
| Observability | Phase-aware events, typed projections, volume budgets, **host-audit plane** | **SEAL-WITH-CHANGES candidate** — `../artifacts/operability.v10.json`, independently reviewed PASS at 0 blocking findings and self-declared `CANDIDATE-NOT-APPLIED`. Architecture buildable, product evidence absent. The six parked identity recipes it records are **blocking**, not residual |
| Validation | Release gates | **SEAL-WITH-CHANGES (architecture), RELEASE BLOCKED (product)** — 19 exact gates map a closed 25-property registry. G9 blocks missing capability runtime and G19 blocks unresolved durable-authoritative retention; the twelve design checkers discharge no product property; 0/25 properties are DEMONSTRATED |
| Versioning | Compatibility policy per contract | **CANDIDATE, independently reviewed, not applied** — `../artifacts/versioning-policy.v8.json`; its independent cold stored-read rejoin review of exactly those bytes is PASS with an empty findings list, and v8 self-declares `CANDIDATE-NOT-APPLIED`. Baseline comparison uses a **three-way detector pivot**; support windows are GUESSED and that property is NOT DISCHARGED |
| Distribution | Artifact set, platforms, signing, air-gap | **SEAL-WITH-CHANGES** — `../artifacts/delivery.v4.json`. Full TypeScript+Rust is default on Linux x86_64/aarch64 GNU, macOS arm64/x86_64 13+, and Windows x86_64 MSVC 10 22H2/Server 2022. Signed manifests and current-plus-two offline compatibility are binding; release evidence is not demonstrated |
| Authoring | Local loop, fact explorer, rule explainability | **SEAL-WITH-CHANGES** — local provenance is non-blocking; blocking promotion is separately verified and audited |
| Explainability retention | Tiered vs absolute | **ARCH.RETENTION-TIERS — CANDIDATE**, and the V10 fork is **not** closed. The head is `../artifacts/retention-tiers.v24.json` — independently reviewed PASS on **both parts** at 0 blockers, but `CANDIDATE-NOT-APPLIED`: it is not the Phase-1A insertion, it selects no retention default, it does not close `CD-RT-5` and it does not unblock G19. Its own `integrationState` records V10 `UNRESOLVED`, `CD-RT-5` `BLOCKED_ON_PHASE_1A` and G19 `BLOCKED`. It retains the shape (sealed capability immutable, effective capability derived at read time, terminal loss append-only, authority withdrawn below `verifiable`) and adds the **V10 item-3 discharge** — purge semantics, verified by execution rather than asserted. **That discharge narrows the fork; it does not close it, and it is not a signature.** `CD-RT-5`'s `unblocksWhen` names four preconditions, and whether they are satisfied is the product authority's determination, not any architecture artifact's. **`CD-RT-5` is not signed.** The binding product packet holds it at `BLOCKED_ON_PHASE_1A` with `ruleWhilePending`: *no implementer may choose a retention default and no freeze may claim V10 resolved*; the freeze signature block carries `Product signer (scope + CD-RT-5): [UNSET]`. Zero implicit durable retention is a **proposed posture awaiting that disposition**, not a product decision — an earlier revision of this row recorded it as signed, sourced only from the independently **REJECTED** `retention-tiers.v5`. Open: the Phase-1A proof/custody packet, then `CD-RT-5`; behind those, A1-RTV4-02 measurement and dedup/backup deletion — [06](06-evidence-and-persistence.md) |

Rows above have **mixed review states**: some are unreviewed; others have completed
reviews with unresolved blockers. The authoritative per-claim status and linked
review artifacts are in `../artifacts/claim-register.v1.json`, validated within
the checker's documented limits by `check-claims.py`.

---

## Do not re-deliberate without new evidence

Evidence-compiler center; graph as substrate; host-owned Run, timing, and policy;
snapshot integrity and read-set model; provenance-complete derivation keys;
multi-axis Run outcome; Coverage-conditional determinism; Coverage as a
content-addressed artifact; independently versioned fingerprint recipe;
`RepairPlan` as first-class; extensions own detection while the project owns
policy; predicate-based rule classification; **predicate-relative fact
sufficiency (C-1)**; and the confinement-honesty limits.

### Reopening conditions

| Trigger | Reopens |
|---------|---------|
| The declarative/imperative split, measured against a real schema, comes out badly | Declarative-first as the default rule representation (R-2) |
| Large-corpus latency shows changed-scope capture is unachievable cold | Execution topology (R-1), and possibly the whole cold-path model |
| A stable native compiler API ships for the deep language | Semantic provider packaging, and possibly the host language |
| Product commits to a public extension marketplace | P-1, P-2, capability matrix, threat model, and versioning together |
| Team composition data arrives | Host language — the runner-up remains one good decision away |

---

## Process rules

**SEALED.**

1. **Decisions close by artifact, not by prose agreement.**
2. **Sealed material does NOT graduate into this repository's `docs/decisions/`.**
   That log records decisions about the shipping product; ~~this tree describes a
   hypothetical rebuild. Mixing them would corrupt the real record with decisions
   about a system that does not exist. The impermanence of this tree is an accepted
   risk, not a reason to publish here.~~ *(Corrected: earlier revisions of these
   documents instructed the opposite.)*

   **Correction 2026-08-04 — the struck rationale is withdrawn; the rule above is
   not.** This tree is neither hypothetical nor impermanent: it is tracked at
   `opensip/docs/coop` and is the greenfield design being implemented. The rule
   still holds for a narrower reason than the struck text gave — the product's ADR
   log records decisions about the shipping TypeScript codebase, and this corpus
   records decisions about a different subject. Separate subjects, separate logs,
   however durable either one becomes.
3. **Every artifact carries a back-reference** listing the sealed properties it
   must encode, and review checks that list. Internal consistency is not
   conformance.
4. **Inherited constraints are re-tested, not carried forward.** See
   [10-method](10-method.md), rule 6 — this rule exists because a migration
   constraint silently shaped four design decisions before anyone noticed.
