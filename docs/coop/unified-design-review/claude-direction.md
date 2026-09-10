All reads are done; nothing further depends on another result. Here is the recommendation.

**Short answer to the user's question:** no. The Fallow-derived constraints in chapter 13 are host-level and language-agnostic. What is TypeScript-specific is the *evidence* Fallow supplied and the per-role native work any second language will need.

## 1. What generalizes, what stays native, and the contract that decides it

**Generalizes across languages (host-owned, written once):**
- §3 sufficiency and visible omissions; §4 candidate/inspect/review handoffs and Control-citation anchoring; §5 repair lifecycle (preview, apply-time content guard, separate verification); §6 delta attribution and schema-aware policy deltas; §8 registry-derived contracts and projections; §9 workflows and bounded review; §10 authoring UX and the direct-call-ban vs transitive-effects distinction; §2's recommendation mechanics (proposal is not intent, strict-resolver acceptance, no writes).

**Native per role (provider and corpus work):**
- §2 discovery conventions: manifests, workspace layouts, convention-loaded entry points differ per ecosystem.
- Which relation rungs exist: `references` at `resolved-binding`, `types` at `checked`, reachability. Only TypeScript and Rust are semantic roles (P-4 in coop 04); everything else is syntax tier.
- Framework abstention classes (FW-03), clone body normalization per language (fact-identity-policy's per-language capability rows), the concrete edit recipes behind a repair action, and §7 runtime/test capture producers and source-map binding per runtime.

**The contract that makes this computable, not hand-listed:** every chapter 13 capability declares its evidence requirements the same way rules do under C-1: relation, minimum rung, completeness, confidence floor. The DR-118 per-role capability matrix declares the highest rung each provider supplies per relation. Availability of a capability for a role is then a host sufficiency computation; an unmet requirement is typed unavailable in every projection (coop 04, "loudly"). Consequence: a syntax-tier language gets discovery, inventory workflows, policy authoring, and delta attribution over syntactic predicates, but never a "no consumers" repair-safety claim. Adding any role costs a DR-118 matrix, DR-119 closure, DR-120 adapter, and a G13-class corpus. That is the whole language roadmap; nothing beyond TypeScript and Rust should be promised.

One correction to chapter 13 §2: "discovery producer" must resolve at scope entry to the role's LanguageProvider inventory facts or host-internal inventory, not a new contribution kind.

`★ Insight ─────────────────────────────────────`
This is why C-1 was worth the fight. Because sufficiency is predicate-relative and per-relation, "does capability X work for language Y" is never a product table someone maintains. It falls out of two declarations that already exist: what the capability needs and what the provider supplies.
`─────────────────────────────────────────────────`

## 2. The new design target and its acceptance condition

**Intended product:** the Control plane of MAP-VS-CONTROL §3 plus chapter 13: authoritative sealed Runs with evidence custody, retention, replay and purge; baselines and ratchets with detector pivot; discovery/recommend; inspect/review; repair preview/apply/verify; runtime, test and history evidence import; workflow profiles; policy authoring; CLI/JSON/SARIF/HTML/agent projections; doctor and purge; independent-release distribution. Roles: TypeScript semantic now, Rust semantic as the retained P-4 substrate, syntax tier for others only if product elects. Map, third-party/WASM/marketplace (DR-116/128), TUI (DR-129), credentials (DR-108), and V1 transition continuity (DR-130) each need an explicit in/out decision recorded in D-371. My default: all OUT except DR-130, which should be decided rather than deferred.

**Design-complete condition:** D-001's five conditions applied to the intended-product row set instead of the D-002 slice.
- **Condition 1 must actually close.** DR-002 through DR-011 are only *preview-disposed*. Authoritative Runs need exactly what D-077/D-078 reduced out: RunId, EvidenceDigest, FactViewId, cache and regeneration keys, `subjectScopeCommitment`, the retention default CD-RT-5, and threat-model V10. These cannot be dispositioned away a second time.
- **Condition 2 over the full set.** The deferral-limb rows that enter scope come off the limb: DR-106, DR-109, DR-113 certainly; DR-110; DR-130 if continuity is elected. Preview-scoped SATISFIED rows need intended-product successors, not regrades: DR-117 (product boundary beyond preview), DR-118 (per-role matrix including Rust), DR-131 (authoritative run contract), DR-122 (SARIF re-entry via G17), DR-124 (activate SC-EVIDENCE and SC-ANALYSIS).
- **New rows only where no owner exists**, at most four: discovery/recommendation contract, advisory inspection/review contract, repair contract, external evidence import contract. Chapter 13 §11 already maps the rest. Contribution-model sign-off (coop 05 CANDIDATE) belongs in the DR-117 successor.
- Conditions 3, 4, 5 unchanged in form; G06/G11/G19 leave HARD-BLOCKED only through their rows.

**Keep the three things separate.** Design complete means independently reviewed contracts with only execution or measurement remaining. The blueprint is condition 5 and `docs/v2/implementation/`. Qualification is the DR-G registry and DR-012. The preview becomes stage 1 of delivery, stage 2 is the authoritative Run and storage, stage 3 the chapter 13 capabilities, later stages the second role.

## 3. Edits now, and where I disagree

**Minimal honest edits:**
1. `COORDINATOR-DECISIONS.md`: append D-371. Quote the user verbatim. Supersede D-001 clause 2's affected-row set (the D-002 slice) with the intended-product row set, supersede the file 12 finish line and the file 08 header as the design target, record the in/out decisions above, name staged delivery with preview as stage 1, and keep D-369 and D-370 as history with their fixed subjects.
2. File 08, the sole register: change the header line to "Preview design COMPLETE (D-369); intended-product design target adopted (D-371), NOT COMPLETE"; append a dated D-371 subsection under "Blueprint-readiness decision" with the row set, a re-measured current-position table for that set (condition 1 NOT MET at 1 of 11), and one table listing each preview-scoped SATISFIED row with its intended-product remainder. Do not rewrite D-369 cells; state the rule that cells carry preview grades and the D-371 table carries remainder until per-row successors land. Add the new rows as OPEN with owners.
3. Record the custody consequence honestly: editing file 08 makes D-369's register and document custody checks DIVERGED by design. D-371 must state the expected D-369 replay failure set (root README plus file 08) and point to the retained after-image in `architecture-publication-before.v1`. Do not repin the application manifest.
4. START-HERE: replace "Current completion state" and the "What was finally accepted?" pointer with the D-371 target and a link to file 08's D-371 section. File 10: retitle the D-370 section to state the new target and staged delivery, keeping the D-370 paragraph. Chapter 13: one added standing line that under D-371 the future-capability constraints are intended-product requirements. Refresh inventory entries the D-370 way.
5. Do not touch file 12, the v2 README, chapters 00 to 04, the reference handoff, or any D-369/D-370 snapshot. No new checklist documents, no schema copies.

**Material disagreements:**
- "Design complete" cannot be declared around condition 1. Identity recipes and CD-RT-5 are the wall for the real product. I will not recommend a wording that calls the design complete while they are disposed rather than closed.
- Stage 1 implementation of the analysis spine should wait for the identity and storage recipes, because the preview's "no durable cache, no stable identity" posture is exactly what a band-aid build would bake in. Distribution and admission work (handoff steps 1 and 2) can proceed now.
- The product must be bounded by explicit in/out decisions in D-371. Without them the register cannot measure completion, and "one complete design" quietly becomes an unbounded roadmap.
- Keep Map out of the Control finish line unless the user elects it; MAP-VS-CONTROL §4.5 already says not to build it before the Control spine works.