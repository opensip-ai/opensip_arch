I have what I need. The remaining unread material (security v8 bytes, broker and lifecycle JSON contracts, the claim matrix, checker source) is outside Lens C's journey walk and is listed as not reviewed. Here is the report.

# Lens C review: whole-product completeness and implementer usability

## Standing and what this review tests

The register's own standing is correct and I confirm it: the intended-product design is IN PROGRESS, conditions 1 to 3 and 5 are NOT MET for that target, and D-369's acceptance is preview-scoped history. Nothing below contradicts D-369 within its recorded scope. What I tested is whether the intended product promised in the scope chapter has, for each user journey, either an accepted contract, a named owner with a concrete acceptance case, or a deliberate exclusion. Where it has none of those, I report it. Where it has an owner but the owner's acceptance case does not name the scenario, I say so and give the scenario.

I walked nine journeys against the actual contract text rather than the summaries: bare invocation with no configuration, single-step versus composed invocation, monorepo roots and provenance, baseline to PR delta gate, candidate to inspect to review to repair, projection parity, partial or cancelled invocation, missing provider, and fresh install versus stage upgrade versus legacy coexistence.

## Findings that materially obstruct the intended product

**PROD-01, HIGH. Repair verification by tests has no admission class.** The scope chapter commits to repair "with verification", and chapter 13 §5 says verification runs "through ordinary analysis and any declared, separately authorized tests". The rules chapter defines effects in three classes and places anything that observes the project under execution, which is exactly what a test run is, in the Probe class. Probe is excluded until ARCH.PROBE-CONTRACT selects a restricted runtime, and that contract records runtime denial as unimplementable today. The register's repair obligation row names authorization, revalidation, commit, recovery and verification but never names the Probe contract or the execution-capable grant. An implementer therefore has three incompatible readings: build a test runner as a host effect outside the C-2 overlay, route it through the Rust build-script grant, or wait on ARCH.PROBE-CONTRACT. Chapter 13's disclaimer that it does not authorize a test runner "in the preview" no longer bounds the problem, because D-371 made the full lifecycle a design obligation. Required correction: the DR-117/131 successor must either scope intended-product verification to analysis re-run only, or explicitly classify test execution as a scenario effect owned by ARCH.PROBE-CONTRACT or a new reviewed execution-grant class, and the register row must cite that owner.

**PROD-02, HIGH. JavaScript is promised as selected depth with no owning cell.** The scope chapter selects "TypeScript/JavaScript through the TypeScript role". The accepted DR-118 matrix has twenty provider cells and four host cells, all TypeScript; the capability registry binds five typescript.* capabilities to rungs; neither the matrix nor the product-boundary successor mentions JavaScript at all. The TypeScript universe key is built from a tsconfig graph and compiler options, so a JavaScript project with no tsconfig has no defined universe. For CommonJS projects the imports relation at resolved-target is likely partial, so the flagship zero-configuration journey on such a project ends in Coverage indeterminate, exit code 3, with no cell recording that as the expected outcome. This is not merely "DR-118 is OPEN for the Rust role": it is a scope promise with a foreseeable failure mode that no acceptance case names. Required correction: DR-118/119 must add JavaScript cells naming module systems, the no-tsconfig universe rule, allowJs/checkJs handling, and the expected Coverage outcome of the cycle rule per cell, or the scope chapter must drop JavaScript from selected depth. The assumption that CommonJS resolution is partial under the pinned compiler is untested here.

**PROD-03, HIGH. HTML and agent projections are promised but unowned.** The scope chapter lists "applicable SARIF/HTML and agent projections". The register contains no occurrence of HTML in any row. The V1 projection-parity contract enumerates five surfaces: json, exit-code, human-terminal, sarif and agent-mcp; there is no html surface and therefore no parity fixture, field-mode table or truncation rule for it. The only HTML design is the surfaces chapter's CANDIDATE report section, which states good properties such as strict CSP, vendored assets and visible truncation, but is not tied to any DR row's acceptance evidence. The agent surface is better placed, since agent-mcp has parity field modes, but the register never names it and the V1 slice excludes "full MCP/agent-protocol product parity", so its intended-product standing is silent. Required correction: extend DR-122's full-product obligation text to name HTML and agent projections explicitly and require their parity surfaces in the DR-122 successor, or remove HTML from the scope chapter. No new row is needed.

**PROD-04, HIGH, known open with a missing scenario. Baseline to PR delta gate on ephemeral CI.** The evidence chapter's baseline design is strong: recipe versioned independently of the fact schema, unsupported recipe yields indeterminate with repair instructions, three-way detector pivot, no mass net-new. It also requires the old detector to be runnable for the pivot, and says the pivot's absence yields indeterminate for that detector. The steering document places baselines in the user repository, and the domain model defines a baseline as a pinned Run identity plus fingerprints. On a fresh CI runner there is no run history and only the current release, so after every detector major the gate returns exit 3 until someone runs a baseline upgrade, which itself needs the old detector. The multi-version generation design keeps old generations locally, but nothing says whether a signed closure must carry the previous detector major, whether the baseline artifact must be self-contained, or how a pinned Run identity resolves where no store exists. The register's row 4 owns "baseline and delta contracts", so this is owned, but the acceptance cell does not name the CI-ephemeral case, and it is the case that decides whether the product's highest-leverage CI behavior works. Required correction: the DR-006/111 baseline contract must specify a self-contained baseline artifact, the pivot-availability rule for fresh installs, and the report-scope versus derivation-scope fixture from chapter 13 §6.

## Findings that need an owner decision before implementation

**PROD-05, MEDIUM, known open. Composed invocations across admission classes have no carrier.** Composition is settled only inside one analysis Plan: the C-2 workflow orders fact, rule, policy and probe stages with dependsOn, and one invocation seals one Run. That covers "audit with several analysis steps". It does not cover a workflow mixing analysis, query and mutation, which is what candidate to inspect to review to repair is. The command envelope is a union of exactly one of run, query, mutation or failure, so a mixed workflow has no envelope, no derived termination, and no parent identity. Chapter 13 §9 defers these to "existing Plan/workflow contracts", which do not have them, and its rule that aggregation cannot hide a failed required step has no carrier. The register's row 2 names host-owned multi-step invocations, so this is owned. Required correction: the DR-117/131 successor must choose between "composed means a profile over analysis stages, everything else is separate commands" and "a host-owned workflow record with per-step envelopes and one derived termination", and the D9 successor must carry the required-step-failure golden.

**PROD-06, MEDIUM, newly identified. Trust-floor continuity across product stages is unowned.** The preview's operational root is fixed at a path ending in preview-v1 with no override, the reference architecture promises no upgrade continuity to an authoritative product, and the distribution contract says cross-major continuity is absent. The lifecycle chapter requires trust roots, revocation observations, expiry floors and anti-rollback counters never to roll back. When stage 2 introduces the evidence state classes and a new state major or root, either the stage-1 trust floors are abandoned, which lets a stage-2 install accept metadata that stage 1 had already refused, or they are migrated by a contract nobody owns. DR-130's acceptance cell is about users of the TypeScript prototype, not stage-to-stage transitions within this product. The scope chapter's rule that milestones must not create incompatible private state models points the right way but has no owner text. Required correction: extend the DR-110/130 obligation to intra-product stage transitions, make SC-TRUST carry-forward mandatory, route state-major migration through DR-107 prepare/commit, and re-scope "no continuity" to analysis results and identities only.

**PROD-07, MEDIUM, documentation hazard with implementation consequence. The missing-provider journey maps to three terminations.** The surfaces chapter says missing signed runtime or provider bytes are the delivery-required fault with exit 4. The D9 golden for that code describes a different situation: a passing Run whose explicitly required export delivery failed. D9's own golden for a required provider that is unavailable is indeterminate, exit 3, with the remedy "install or enable the provider". The host-foundation contract calls an executable lacking its payload layout a required-delivery failure. The install-shape gate says core-only is not the analysis product, which reads as admission refusal, exit 2. A core-only user running analyze could be given any of the three depending on which document the implementer reads, and CI scripts branch on that code. A defensible split exists, namely "not selected in the lock" is Coverage unavailable and "selected but bytes missing" is delivery-required, but it is written nowhere, and the surfaces chapter's citation is to a golden with a different meaning. Required correction: one golden each for "core-only plus analyze" and "selected provider bytes missing" in the DR-131/D9 successor, and a correction or supersession note on the surfaces chapter's cross-reference.

**PROD-08, MEDIUM, known open with a placement gap. Evidence import has no admission form.** Chapter 13 §7 defines the right binding dimensions and explicitly defers artifact admission, freshness, retention and privacy. The gap is placement: an imported coverage or history artifact is neither a producer nor a data-only rule under P-2, and the C-2 contributions descriptor has no input class for it. The register puts adapters under the language rows and richer evidence under the admission rows; no row names the artifact's PlanIntent descriptor, PlanId membership, state class or hostile-input obligations. Required correction: the admission successor must define the artifact as a keyed PlanIntent input with digest, declared adapter and observation window, name its state class, and inherit the hostile-input totality obligations.

**PROD-09, MEDIUM, documentation hazard. Three command vocabularies and two platform lists.** The surfaces chapter carries a CANDIDATE grammar with fifteen verbs, the Map-versus-Control document shows a different illustrative shape, and the reference architecture fixes analyze and doctor for the preview. The product-boundary chapter, marked SEALED, lists Windows as supported and the Rust provider in the v1 spine, both of which the scope chapter now withdraws without annotating those sources. An implementer of the intended product cannot tell which verb set is the design or which SEALED claims still bind. Required correction: the DR-117/131 successor must publish the command and admission-class inventory as one table and mark the older grammars superseded or illustrative, and the platform and role rows in the coop chapters and delivery contract need a D-371 annotation. No new document.

**PROD-10, MEDIUM, newly identified. Closure accounting for chapter 13 contracts is not measurable.** D-371 chose not to add rows for the repair, review, discovery and import contracts and relies on the register's obligation table, whose rows list up to eight owner rows each. Condition 2 is measured per row SATISFIED. Each of eight rows can close on its own subject while the repair contract is never authored, and the measurement cannot see it. The D-371 review noted that unowned contracts must get a row, but nothing forces the check. Required correction: for each obligation row, name the single primary row whose SATISFIED cell must cite the contract digest. This is a table edit, not a new row or checklist.

**PROD-11, LOW, documentation hazard. Gate registry not annotated for D-371.** The register says condition 4 is REASSESS, but the G17 row still reads "dropped / inapplicable, not required-now" and G06/G11 read "NOT slice-1-required" with no full-product note, while the scope chapter puts SARIF and durable evidence in scope. Required correction: annotate those rows at the next refresh.

**PROD-12, MEDIUM, integration gap. Monorepo root and workspace discovery diverge between the preview contract and the V1 rule.** The V1 resolved-inputs rule orders explicit path, nearest project configuration, then VCS root, and makes a candidate above an intervening project marker a typed ambiguity. The preview host-foundation rule walks up to the nearest tracked configuration, drops the VCS-root step and the ambiguity clause, and selects the current directory with defaults on no match. Workspace units exist in the V1 scope model as parallelism over one parent Run, but the preview configuration carrier has no workspace field and chapter 13's "workspace layout" discovery has no contract for entering scope. Required correction: the discovery successor must define the project marker for the TypeScript role, restore or explicitly supersede the ambiguity rule, and define how discovered workspace units enter scope with provenance. The exact marker definition in resolved-inputs was not read and is an assumption.

## D-370 and D-371 challenged

D-371 is a scope act and was reviewed as one; its acceptance did not claim any contract complete, and the register text is truthful about that. My challenges are PROD-10 above and the observation that "one complete design implemented in stages" is only measurable if stage transitions are themselves designed, which PROD-06 shows they are not. Chapter 13's Fallow constraints are not slogans: §3, §4, §5 and §6 state falsifiable negatives and name the acceptance obligations, and §4's separation of candidate, equivalence and refactor safety is genuinely load-bearing. Two of them are under-placed in the ontology, which is PROD-01 and PROD-08. §2's recommendation surface and §10's authoring surface are constraints without schemas, and both say so.

On complexity: the identity set is large, with thirteen named identities of which five are parked, and there are three canonical encodings an implementer must build, CVE1 for identities, deterministic CBOR for the TypeScript wire, and the security metadata profile for control and lock bytes. Each has a stated reason and the wire ones are applied V1 contracts, so I do not recommend a change; I record it as the main implementer cost, not as overengineering. The five-state-class model with three active, and the broker design with zero handles in the preview profile, are justified by the full product's repair path.

## Strengths worth retaining

- **Per-relation ladders with a closed deficiency vocabulary joined to D9.** "Installed, applicable, executed, sufficient" are mechanically distinct, each deficiency has a remedy, and a Coverage state cannot arise that has no termination.
- **D9 as one total union with goldens for the hard cases.** Interrupt before and after finalization, verdict distinct from termination, durability failure never reports success, and the no-mass-net-new baseline invariant are goldens, not prose.
- **RequestId allocated before parsing and excluded from every semantic identity**, with a retained checker joining the exclusion to the closed inputs.
- **Host-owned fingerprint recipe versioned independently of the fact schema**, with unsupported recipe yielding indeterminate plus repair instructions.
- **Provider-only output law with a negative corpus, and a capability registry with fixed relation and rung bindings**, refusing unknown capabilities rather than treating them as extensions.
- **Host foundation discipline**: account home from the OS record, no environment override, deny-by-absence permission policy, CI never opening the local layer, unsupported project filesystems refused rather than degraded.
- **Scope rides with re-entry triggers** as the pattern for deferring without silence.
- **The register's honest condition table** and the separation of preview grades from full-product remainders.

## Readiness

NOT_READY for full-design acceptance under this lens, which matches the register. None of the findings is a proven break in an accepted preview contract; PROD-01, PROD-02 and PROD-03 are scope promises with no owning acceptance case, PROD-04 through PROD-08 and PROD-12 are owned obligations whose acceptance cells omit the deciding scenario, and the rest are hazards that will mislead an implementer.

```json
{
  "reviewer": "Claude (Anthropic), model claude-fable-5-1, independent read-only review of the post-D-371 docs snapshot",
  "lens": "C — whole-product completeness and implementer usability",
  "readiness": "NOT_READY",
  "findings": [
    {
      "id": "PROD-01",
      "severity": "HIGH",
      "classification": "integration_gap",
      "title": "Repair verification by tests has no admission class in the accepted ontology",
      "sources": [
        "docs/v2/architecture/10-mvp-and-future-scope.md:43 (Repair row) and :45 (Exclusions row)",
        "docs/v2/architecture/13-evidence-workflows-and-product-contracts.md:170-176",
        "docs/coop/architecture/05-rules-and-extensions.md:73-82, 265-287",
        "docs/coop/architecture/09-open-decisions.md:38-39",
        "docs/v2/architecture/08-decision-and-readiness-register.md:410 (row 6)"
      ],
      "trigger": "Implementer builds the intended-product repair lifecycle and reaches verify; chapter 13 permits declared, separately authorized tests.",
      "consequence": "Test execution is a scenario effect, which the rules chapter reserves to the Probe stage; Probe is excluded pending ARCH.PROBE-CONTRACT. Three incompatible build paths exist (host effect outside the C-2 overlay, Rust build-script grant, wait on Probe). Register row 6 names verification but not its enforcing contract.",
      "counterevidence_considered": "Chapter 13 §5 says it does not authorize a test runner in the preview; that disclaimer is preview-scoped and D-371 made the full lifecycle a design obligation. The v1-slice execution-capable grant exists but is bound to Rust build scripts and sealed inputs, not project tests.",
      "required_correction": "DR-117/131 successor must either scope intended-product verification to analysis re-run only, or classify test execution as a Probe/scenario effect (or a new reviewed execution-grant class) and cite ARCH.PROBE-CONTRACT in register row 6.",
      "register_owner": "DR-105, DR-117, DR-131; V1 ARCH.PROBE-CONTRACT",
      "confidence": "high"
    },
    {
      "id": "PROD-02",
      "severity": "HIGH",
      "classification": "newly_discovered_defect",
      "title": "JavaScript is promised as selected native depth with no owning DR-118 cell, corpus or universe rule",
      "sources": [
        "docs/v2/architecture/10-mvp-and-future-scope.md:39",
        "docs/coop/completion/analysis-quality-completion.v2.md:84-115, 256-262",
        "docs/coop/completion/language-quality-matrix.completed.v2.json (grep for javascript/allowJs/CommonJS: no matches)",
        "docs/coop/artifacts/preview-product-boundary-successor.v10.json (grep for javascript: no matches)",
        "docs/coop/artifacts/resolved-inputs.v2.json:1696-1709 (TypeScript universe key requires tsconfig graph)"
      ],
      "trigger": "User runs zero-config analyze on a JavaScript project with no tsconfig or with CommonJS requires.",
      "consequence": "No defined semantic universe; imports at resolved-target likely partial; cycle rule returns Coverage indeterminate (exit 3) and no cell records this as expected. The zero-config 'useful analysis' promise is unevidenced for the promised language.",
      "counterevidence_considered": "File 10 states DR-118/119 must still settle each cell and register row 5 is OPEN; that covers Rust, but JavaScript is nowhere named as a cell, corpus or limitation.",
      "required_correction": "Add JavaScript cells to DR-118/119 naming module systems, the no-tsconfig universe rule, allowJs/checkJs handling and expected cycle-rule Coverage per cell; or remove JavaScript from selected depth in file 10.",
      "register_owner": "DR-118, DR-119; product owner for scope",
      "confidence": "high for the gap; medium for the exact runtime consequence (CommonJS resolution behavior under the pinned compiler untested)"
    },
    {
      "id": "PROD-03",
      "severity": "HIGH",
      "classification": "integration_gap",
      "title": "HTML and agent projections promised by the scope chapter have no owning row or parity surface",
      "sources": [
        "docs/v2/architecture/10-mvp-and-future-scope.md:41",
        "docs/v2/architecture/08-decision-and-readiness-register.md (grep HTML: no matches; row 4 at :408 names only 'machine projection parity')",
        "docs/coop/artifacts/operability.v10.json $.projectionParity.surfaces (json, exit-code, human-terminal, sarif, agent-mcp; no html)",
        "docs/coop/architecture/08-surfaces-and-topology.md:371-384 (HTML report CANDIDATE)",
        "docs/coop/v1-slice.md:172-173 (excludes full MCP/agent parity)"
      ],
      "trigger": "Implementer builds the HTML report or agent surface for the intended product.",
      "consequence": "No parity fixtures, field modes, truncation rule, gate or acceptance cell for HTML; agent surface has parity modes but no register standing under D-371.",
      "counterevidence_considered": "DR-122's cell says 'explicit per-command/capability applicability', which could be read to cover any projection; but the cell and operability surfaces never name HTML.",
      "required_correction": "Extend DR-122's full-product obligation to name HTML and agent projections and require their parity surfaces in the DR-122 successor; or remove HTML from file 10. No new row.",
      "register_owner": "DR-122, DR-123",
      "confidence": "high"
    },
    {
      "id": "PROD-04",
      "severity": "HIGH",
      "classification": "known_open_contract",
      "title": "Baseline to PR delta gate on ephemeral CI is unaddressed by the owned baseline contract",
      "sources": [
        "docs/coop/architecture/06-evidence-and-persistence.md:499-593",
        "docs/coop/architecture/07-outcomes-and-failure.md:126",
        "docs/coop/steering/03-compatibility-and-parity.md:62-73",
        "docs/v2/architecture/13-evidence-workflows-and-product-contracts.md:178-198",
        "docs/v2/architecture/08-decision-and-readiness-register.md:408 (row 4)"
      ],
      "trigger": "PR gate on a fresh CI runner after a detector major bump, or with a baseline referencing a Run not in the runner's store.",
      "consequence": "Pivot needs the old detector; fresh install has none; every comparison returns indeterminate (exit 3) until a baseline upgrade that itself needs the old detector. Whether closures ship N-1 detector majors or baselines must be self-contained is undecided.",
      "counterevidence_considered": "Dual-emit windows, published compatibility policy and the multi-version generation model supply ingredients; none names the ephemeral-CI case or the store-less resolution of a pinned Run identity.",
      "required_correction": "DR-006/111 baseline contract must specify a self-contained baseline artifact (fingerprints, recipe version, detector identity), a pivot-availability rule for fresh installs, and the report-scope vs derivation-scope fixture.",
      "register_owner": "DR-006, DR-111, DR-123 (row 4)",
      "confidence": "high that it is unaddressed; medium-high that it materially obstructs"
    },
    {
      "id": "PROD-05",
      "severity": "MEDIUM",
      "classification": "known_open_contract",
      "title": "Composed invocations across admission classes have no envelope, aggregation rule or parent identity",
      "sources": [
        "docs/v2/architecture/10-mvp-and-future-scope.md:19",
        "docs/v2/architecture/13-evidence-workflows-and-product-contracts.md:274-280",
        "docs/coop/artifacts/c2-plan-stage-schema.v4.json:565-571",
        "docs/coop/architecture/07-outcomes-and-failure.md:64-70",
        "docs/coop/architecture/08-surfaces-and-topology.md:269-271, 297-304",
        "docs/v2/architecture/08-decision-and-readiness-register.md:406 (row 2)"
      ],
      "trigger": "A named workflow chaining analysis, inspect (query) and repair preview (mutation) in one invocation.",
      "consequence": "CommandEnvelope is a union of exactly one kind; C-2 composes only analysis stages inside one Run; the 'aggregation cannot hide a failed required step' rule has no carrier; no parent/child identity exists.",
      "counterevidence_considered": "'audit' with several analysis steps is fully covered by the multi-stage ExecutionPlan; the gap is cross-class composition only.",
      "required_correction": "DR-117/131 successor must choose 'composed = profile over analysis stages; other operations are separate commands' or 'host-owned workflow record with per-step envelopes and one derived termination'; D9 successor carries the required-step-failure golden.",
      "register_owner": "DR-117, DR-131, DR-007",
      "confidence": "high"
    },
    {
      "id": "PROD-06",
      "severity": "MEDIUM",
      "classification": "integration_gap",
      "title": "Stage-to-stage state continuity, especially monotonic trust floors, is unowned",
      "sources": [
        "docs/coop/completion/reference-architecture.v2.md:27-28",
        "docs/coop/completion/host-foundation-completion.v2.md:35-40, 106-107",
        "docs/coop/completion/distribution-runtime-completion.v2.md:168-177, 349-350",
        "docs/v2/architecture/04-lifecycle-delivery-and-operations.md:80-81",
        "docs/v2/architecture/10-mvp-and-future-scope.md:95-96",
        "docs/v2/architecture/08-decision-and-readiness-register.md:318 (DR-130 cell), :411 (row 7)"
      ],
      "trigger": "Stage 2 introduces SC-EVIDENCE/SC-ANALYSIS and a new state major or operational root replacing preview-v1.",
      "consequence": "Stage-1 trust high-water and revocation floors are either abandoned (anti-rollback weakened) or migrated by a contract nobody owns; DR-130 covers TypeScript-prototype users, not intra-product stages.",
      "counterevidence_considered": "Same-major root reuse is stated; DR-107 prepare/commit covers schema majors generically; 'trust floors never restored from a lifecycle rollback' addresses rollback, not root/major transition.",
      "required_correction": "Extend the DR-110/130 obligation to intra-product stage transitions: SC-TRUST carry-forward mandatory, state-major migration via DR-107, and re-scope 'no continuity' to analysis results and identities.",
      "register_owner": "DR-107, DR-112, DR-124, DR-130",
      "confidence": "medium-high"
    },
    {
      "id": "PROD-07",
      "severity": "MEDIUM",
      "classification": "documentation_hazard",
      "title": "Missing-provider journey maps to exit 2, 3 or 4 depending on the document read",
      "sources": [
        "docs/coop/architecture/08-surfaces-and-topology.md:211-212",
        "docs/coop/artifacts/d9-exit-contract.v1.14.json:2279-2308 (required-delivery-failed is an export-delivery scenario) and :1550-1575 (analysis-required-provider-unavailable, exit 3)",
        "docs/coop/completion/host-foundation-completion.v2.md:15-16",
        "docs/v2/architecture/02-distribution-and-components.md:236-239",
        "docs/v2/architecture/08-decision-and-readiness-register.md:372 (DR-G30)"
      ],
      "trigger": "Core-only install runs analyze; or the lock selects a provider whose bytes are missing.",
      "consequence": "Surfaces chapter cites DELIVERY.REQUIRED_FAILED for missing provider bytes, but that golden's scenario is a different failure; D9's provider-unavailable golden says exit 3; the install-shape gate implies admission refusal. CI and agents branch on this code.",
      "counterevidence_considered": "A defensible split ('not selected' → Coverage unavailable; 'selected but missing' → delivery-required) exists but is written nowhere.",
      "required_correction": "Add goldens for 'core-only + analyze' and 'selected provider bytes missing' in the DR-131/D9 successor; correct or supersede the surfaces chapter cross-reference.",
      "register_owner": "DR-007, DR-114, DR-131, DR-G30",
      "confidence": "high"
    },
    {
      "id": "PROD-08",
      "severity": "MEDIUM",
      "classification": "known_open_contract",
      "title": "Runtime/test/history evidence import has no admission form in the C-2/P-2 ontology",
      "sources": [
        "docs/v2/architecture/13-evidence-workflows-and-product-contracts.md:215-239",
        "docs/v2/architecture/02-distribution-and-components.md:277-282 (P-2)",
        "docs/coop/artifacts/c2-plan-stage-schema.v4.json (contributions/capabilityGrants descriptor; no evidence-artifact input class)",
        "docs/v2/architecture/08-decision-and-readiness-register.md:406 (row 2), :409 (row 5)"
      ],
      "trigger": "User imports a V8/Istanbul coverage file or CI history for advisory priority or a future predicate.",
      "consequence": "The artifact is neither a producer nor a data-only rule; its PlanIntent descriptor, PlanId membership, state class and hostile-input obligations are unnamed; ownership is split across language rows and admission rows.",
      "counterevidence_considered": "Chapter 13 §7 explicitly defers artifact admission and the register table names adapters; the deferral is honest but the placement gap is real.",
      "required_correction": "Admission successor defines a keyed PlanIntent input class for evidence artifacts (digest, adapter, observation window), names its state class and inherits hostile-input totality obligations; cross-reference from rows 2 and 5.",
      "register_owner": "DR-117, DR-131, DR-124, DR-118",
      "confidence": "high"
    },
    {
      "id": "PROD-09",
      "severity": "MEDIUM",
      "classification": "documentation_hazard",
      "title": "Three command vocabularies and two platform/role lists face the implementer",
      "sources": [
        "docs/coop/architecture/08-surfaces-and-topology.md:243-263",
        "docs/MAP-VS-CONTROL.md:130-151",
        "docs/coop/completion/reference-architecture.v2.md:10",
        "docs/coop/architecture/01-product-boundary.md:50-51 (SEALED; Windows and Rust in v1 spine)",
        "docs/v2/architecture/10-mvp-and-future-scope.md:39-40"
      ],
      "trigger": "Implementer selects the intended-product command surface or supported platforms.",
      "consequence": "No document states which verb set is the design; SEALED coop claims about Windows and the Rust spine are withdrawn by file 10 without annotation at source.",
      "counterevidence_considered": "File 10 says exact admission contracts come next at DR-117/118/119; v1-slice says command names are a later implementer concern. Neither resolves which grammar is authoritative today.",
      "required_correction": "DR-117/131 successor publishes one command/admission-class inventory and marks older grammars superseded or illustrative; annotate coop 01 and delivery platform/role rows with D-371 scope. No new document.",
      "register_owner": "DR-117, DR-131, DR-119, DR-126",
      "confidence": "high"
    },
    {
      "id": "PROD-10",
      "severity": "MEDIUM",
      "classification": "documentation_hazard",
      "title": "Chapter 13 contract closure is not measurable under per-row SATISFIED accounting",
      "sources": [
        "docs/v2/architecture/08-decision-and-readiness-register.md:403-420 (obligation table; row 6 lists eight owner rows)",
        "docs/coop/unified-design-review/D-371-design-target.v1.md:94-97",
        "docs/coop/unified-design-review/claude-direction.md:30"
      ],
      "trigger": "Condition 2 is re-measured after several owner rows close on their own subjects.",
      "consequence": "The repair, review, discovery or import contract can remain unauthored while every listed owner row reads SATISFIED; the measurement cannot detect it.",
      "counterevidence_considered": "D-371 states an unowned contract must receive a row before acceptance; nothing forces that check at measurement time.",
      "required_correction": "For each obligation row, name the single primary row whose SATISFIED cell must cite the contract digest. Table edit only; no new rows or checklist.",
      "register_owner": "Register editor; D-371 successor",
      "confidence": "high"
    },
    {
      "id": "PROD-11",
      "severity": "LOW",
      "classification": "documentation_hazard",
      "title": "Gate registry rows G17, G06, G11 carry preview-era 'dropped/not required' text with no D-371 annotation",
      "sources": [
        "docs/v2/architecture/08-decision-and-readiness-register.md:348, 353, 359, 433"
      ],
      "trigger": "Reader consults the gate registry for SARIF or durable-evidence qualification.",
      "consequence": "Reads SARIF as dropped from the product although file 10 puts it in scope; condition 4 says REASSESS but no row reflects it.",
      "counterevidence_considered": "Row 4 text says authoritative projections cannot inherit preview exclusions; the gate rows do not.",
      "required_correction": "Annotate G17/G06/G11 with full-product standing at the next register refresh.",
      "register_owner": "DR-122, DR-106, DR-109; register editor",
      "confidence": "high"
    },
    {
      "id": "PROD-12",
      "severity": "MEDIUM",
      "classification": "integration_gap",
      "title": "Monorepo root resolution and workspace discovery diverge between the preview contract and the V1 rule",
      "sources": [
        "docs/coop/artifacts/resolved-inputs.v2.json:1659-1673",
        "docs/coop/completion/host-foundation-completion.v2.md:113-116, 162-169",
        "docs/v2/architecture/13-evidence-workflows-and-product-contracts.md:49-63",
        "docs/v2/architecture/08-decision-and-readiness-register.md:407 (row 3)"
      ],
      "trigger": "Zero-config analyze from a package directory inside a monorepo, with or without a root opensip.json.",
      "consequence": "Preview rule drops the VCS-root step and the 'candidate above an intervening marker is a typed ambiguity' clause; no definition of the TypeScript project marker; workspace units exist in V1 scope but the preview carrier has no field and chapter 13 discovery has no entry contract.",
      "counterevidence_considered": "Preview scope may lawfully narrow the V1 rule; but the narrowing is not recorded as a supersession and the full product re-inherits the V1 rule.",
      "required_correction": "Discovery successor defines the TypeScript-role project marker, restores or explicitly supersedes the ambiguity rule, and defines how discovered workspace units enter scope with provenance.",
      "register_owner": "DR-103, DR-104, DR-125 (row 3); V1 RESOLVED-INPUTS owner",
      "confidence": "medium (resolved-inputs project-marker definition not read; assumption marked)"
    }
  ],
  "strengths": [
    "Per-relation sufficiency ladders with a closed deficiency vocabulary checked against D9 (docs/coop/architecture/04-fact-plane.md:175-207; d9-exit-contract.v1.14.json:954-992).",
    "D9 as one total termination union with goldens for interrupt before/after finalization, verdict≠termination, durability failure, and no-mass-net-new baseline (d9-exit-contract.v1.14.json:1369, 2202-2248, 2279-2308).",
    "RequestId allocated before parsing and excluded from every semantic identity with a retained checker (docs/coop/architecture/02-domain-model.md:87-128).",
    "Host-owned fingerprint recipe versioned independently of the fact schema; unsupported recipe yields indeterminate with repair instructions (docs/coop/architecture/06-evidence-and-persistence.md:522-541).",
    "Provider-only output law with negative corpus and a capability registry with fixed relation/rung bindings that refuses unknown capabilities (analysis-quality-completion.v2.md:84-107).",
    "Host foundation discipline: OS-account home, no environment override, deny-by-absence policy carrier, CI never opens layer 4, unsupported project filesystems refused (host-foundation-completion.v2.md §1-§4).",
    "Chapter 13's separation of candidate/equivalence/refactor-safety questions and Control-citation validation (13-evidence-workflows-and-product-contracts.md:111-152).",
    "Scope rides SD-1..SD-8 with explicit re-entry triggers as the deferral pattern (scope-rides-completion.v2.md).",
    "Register condition table truthfully NOT MET / REASSESS with preview grades preserved as history (08-decision-and-readiness-register.md:376-434).",
    "Publication sequence with one SQLite selection transaction and no mutable 'current' symlink (distribution-runtime-completion.v2.md:326-350)."
  ],
  "coverage": {
    "files_read_in_full": [
      "docs/v2/architecture/10-mvp-and-future-scope.md",
      "docs/v2/architecture/README.md",
      "docs/v2/architecture/00-status-and-authority.md",
      "docs/v2/architecture/01-semantic-model-and-host-authority.md",
      "docs/v2/architecture/02-distribution-and-components.md",
      "docs/v2/architecture/03-configuration-and-security.md",
      "docs/v2/architecture/04-lifecycle-delivery-and-operations.md",
      "docs/v2/architecture/05-v1-to-v2-relationship.md",
      "docs/v2/architecture/12-architecture-completion-goal.md",
      "docs/v2/architecture/13-evidence-workflows-and-product-contracts.md",
      "docs/coop/completion/reference-architecture.v2.md",
      "docs/coop/completion/scope-rides-completion.v2.md",
      "docs/coop/completion/analysis-quality-completion.v2.md",
      "docs/coop/completion/distribution-runtime-completion.v2.md",
      "docs/coop/completion/host-foundation-completion.v2.md",
      "docs/coop/completion/D-368-workflow-proposal.v3.md",
      "docs/MAP-VS-CONTROL.md",
      "docs/START-HERE.md",
      "docs/coop/FALLOW-BORROW-REGISTER.md",
      "docs/coop/v1-slice.md",
      "docs/coop/architecture/01-product-boundary.md",
      "docs/coop/architecture/02-domain-model.md",
      "docs/coop/architecture/03-execution-model.md",
      "docs/coop/architecture/04-fact-plane.md",
      "docs/coop/architecture/05-rules-and-extensions.md",
      "docs/coop/architecture/06-evidence-and-persistence.md",
      "docs/coop/architecture/07-outcomes-and-failure.md",
      "docs/coop/architecture/08-surfaces-and-topology.md",
      "docs/coop/architecture/09-open-decisions.md",
      "docs/coop/steering/03-compatibility-and-parity.md",
      "docs/coop/unified-design-review/D-371-design-target.v1.md",
      "docs/coop/unified-design-review/claude-direction.md",
      "docs/coop/unified-design-review/claude-review.v2.md",
      "docs/coop/unified-design-review/README.md",
      "docs/coop/fallow-review/claude-review.v2.md"
    ],
    "files_read_in_part": [
      "docs/v2/architecture/08-decision-and-readiness-register.md (lines 1-506 in three reads; all sections)",
      "docs/coop/completion/architecture-application.v1.json (lines 1-560 units; 8990-9040 supplement pointer and enactment plan)",
      "docs/coop/completion/architecture-incorporated-dependency-supplement.v1.json (top-level keys only)",
      "docs/coop/COORDINATOR-DECISIONS.md (D-002, D-009, D-010, D-077, D-078, D-370, D-371)",
      "docs/coop/IMPLEMENTER-BLUEPRINT.md (lines 100-340, §1.1 normative byte set and note N-1)",
      "docs/coop/artifacts/d9-exit-contract.v1.14.json (golden id inventory; goldens at 1550-1605, 2202-2308; code vocabulary 954-992)",
      "docs/coop/artifacts/operability.v10.json ($.projectionParity 1210-1360)",
      "docs/coop/artifacts/resolved-inputs.v2.json (1650-1710 projectModel)",
      "docs/coop/artifacts/c2-plan-stage-schema.v4.json (556-596 workflow/budgets)",
      "docs/coop/artifacts/preview-analyze-contract.v2.json (top-level keys; 98-192)",
      "docs/coop/completion/language-quality-matrix.completed.v2.json and preview-product-boundary-successor.v10.json (grep only)"
    ],
    "scenarios_traced": [
      "Bare `opensip analyze` with no configuration: host-foundation §2-§3 root walk and layer defaults; DR-131 pack/policy; D9 pass/indeterminate goldens.",
      "One-step vs multi-step: C-2 workflow stages with dependsOn inside one ExecutionPlan; CommandEnvelope union; admission classes table.",
      "Monorepo roots/workspaces/provenance: resolved-inputs projectModel vs host-foundation §2; six-layer precedence and CI layer-4 exclusion.",
      "Baseline → PR delta gate: evidence chapter baseline properties and detector pivot; D9 baseline-compare-unsupported-recipe golden; steering baselines.",
      "Candidate → inspect → review → repair preview/apply/verify: chapter 13 §4-§5; rules chapter effect classes; D9 repair goldens; broker SDK effects (readProject/writeHostState only).",
      "CLI/JSON/SARIF/HTML/agent parity: operability projectionParity surfaces; DR-122 scope ride SD-5; surfaces chapter report section.",
      "Partial/cancelled invocation: D9 user-interrupt-finite and post-finalization goldens; convergence-exhausted indeterminate; orphan recovery invariant.",
      "No provider installed: D9 provider-unavailable vs required-delivery-failed; surfaces chapter mapping; host-foundation payload rule; DR-G30.",
      "Fresh install / update / legacy coexistence: host-foundation roots; distribution-runtime §3/§5; DR-110/130 cells; file 05 migration constraints."
    ],
    "untested_assumptions": [
      "That the pinned TypeScript compiler leaves CommonJS require edges partially resolved without tsconfig (PROD-02).",
      "That resolved-inputs.v2's 'intervening project marker' has no TypeScript-role definition (PROD-12; the marker section was not read).",
      "All SHA-256 pins and checker execution counts; no checker was executed or read as source."
    ]
  },
  "not_reviewed": [
    "Security completion v8 contract bytes, permission truth tables and fixtures (docs/coop/completion/security-*).",
    "Broker bootstrap/SDK courier contracts and broker-sdk-api.v1.ts.",
    "lifecycle-carrier.contract.v2.json, control-completion v5, protocol fixtures, compatibility matrices and selection models.",
    "docs/v2/architecture/09-v1-to-v2-claim-matrix.md, 07-review-record.md, 11-three-reviewer-direction-synthesis.md, prototype-evidence-reference.md.",
    "IMPLEMENTATION-FREEZE.md §3/§7 bytes; claim-register.v1.json; product-dispositions.v1.json.",
    "Full contents of the incorporated dependency supplement (only its key list).",
    "state-class-contract.v11, sarif-projection-contract.v15, provider-only-output-contract.v3, preview-product-boundary-successor.v10 (grep only).",
    "The quality corpus files and G13 result schema.",
    "docs/coop/agents-log*, agentlog*, p.md, TREE-ENDSTATE, ORGANIZATION-PLAN, operations tooling."
  ]
}
```