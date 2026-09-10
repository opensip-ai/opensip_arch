I read the OpenSIP orientation and architecture chapters, D-369, the register's decision rows and current position, the Gortex borrow register, the pinned preview contract, and the seven Fallow docs and source files you named. Here is my initial adversarial recommendation.

## Headline

Most of the list is already law in OpenSIP, and in several places OpenSIP is stricter than Fallow. The real risk in this exercise is importing Fallow's *advisory, best-effort, fall-back-to-syntactic* posture into Control. The genuine value is one new guardrail (advisory-over-Control anchoring), four ownership clarifications, and a pinned non-borrow list. Nothing below requires changing preview semantics, and I flag the two items that would.

## 1. Disposition

**Already covered (link, do not redesign)**

| Idea | OpenSIP home | Note |
|---|---|---|
| Deterministic output, stable fingerprints | `06` Baselines and fingerprint recipe (SEALED), FACT-ID-V1 in `04` | OpenSIP is ahead. Fallow's `fallow:fn:` hash of file+name+line is weaker than the host-owned versioned recipe. Preview deliberately has no stable identity (DR-131 `unstableIdentities`). |
| Changed-code gating, baselines | `06` three-way detector pivot (SEALED) | Fallow's `audit --gate new-only` falls back to syntactic key sets when semantic identity mismatches. That is exactly GX-N03. Non-borrow, see below. |
| Exact / normalized / structural / near-clone | `04` L0–L3 body-identity ladder, `clones` relation | Fallow `dupes` maps onto L0–L3. Nothing to add. |
| Discovery, inspect, verdict separation; snapshot-bound review | `05` "Run creation depends on admission mode", `08` QueryService bound to one sealed view selector, `06` acceptance is recorded never inferred | Fallow's fail-closed inspect on `source_sha256` mismatch is the best idea in the corpus and is already OpenSIP's snapshot binding. Worth one clarification row so implementers see the equivalence. |
| Coherent multi-step invocations | `08` one dispatch path, multi-stage WorkflowProfile parent Run | Covered. |
| "Analyze once" projections | `04` central bet | Do not create a row. |
| Completeness only when `completion: complete` | `04` `coverage=unknown` never satisfies `completeness=complete` | Covered as principle. See qualification gap below. |

**Design addition now (settle ownership; no preview change)**

| Idea | Addition |
|---|---|
| Advisory bounded decision review (`decision_surface.rs`) | The trust mechanism is the borrow, not the UX. Fallow rejects any agent-proposed decision whose `signal_id` was not emitted deterministically. OpenSIP should state the same law for every advisory or agent surface over Control: items must reference Control-emitted identities from a named sealed view; unanchored items are rejected; output is never a Run or gate. This closes the door before MCP and Map open it. Cap size, blast × reversibility ranking, and question phrasing are product UX. |
| Zero-config / recommend (`onboarding.rs`) | Model as a host-owned read-only projection over project inventory. Constraints to settle: proposal is not applied intent; it must round-trip the strict resolver (Fallow's own test: schema-valid is not loader-accepted); it never writes; it never touches private permission policy (`03`: repository settings cannot grant). The auto/default/taste split with no recommended answer on taste questions is a good product shape, not architecture. |
| Stronger remediation preconditions | Grammar has `repair preview\|apply` but no precondition law. Add one: apply requires complete Coverage for the justifying predicate, a fresh content-digest guard against the sealed Snapshot at apply time, and a mutation artifact linked to the Run. Abstention is Coverage-typed via the four deficiencies, not a new outcome ladder. Repair stays DENIED in the v1 overlay. |
| Generated contract registry (`issue_meta.rs`, `contract-surfaces.mjs`) | `08` already says specs carry host handlers only and parity is a typed contract. Add: rule and predicate public identity (id, config key, explain anchor, projection label) is registry-derived by the host, never hand-duplicated per projection, and parity tests consume the registry. Drift gate becomes a qualification obligation once more than one rule exists. |
| Policy weakening vs code improvement | Fallow's `audit_weakening.rs` is token counting over diffs. OpenSIP has a stronger claim by construction: effective-policy digest and pack identity enter PlanId, so a base-vs-head comparison across differing policy digests without a recorded acceptance transition is refused or INDETERMINATE, never silently compared. Record as a clarification of existing `05`/`06` law, not an edit to the SEALED table. |

**Later implementation (ontology covered, keep out of preview)**

- **Rich language-specific evidence.** Fallow's abstention classes (decorators, DI, dynamic import, overloads) are a good deficiency vocabulary for the TypeScript provider corpus under DR-118/G13. Adaptation required: Fallow's sidecar decides `confirmed-used`; in OpenSIP the provider emits facts and Coverage and the host rule decides (DR-133).
- **Runtime, test, history evidence.** Later relation families entering as admitted producers. Name identity dimensions now as a list, not a recipe: observation window, deployment set, source-map identity. Fallow's cloud source and license watermark are commercial, exclude.
- **Semantic similarity via embeddings.** Fallow keeps it offline, unverified, never gating, and consent-gated. That is compatible only on the Map plane or as a parked advisory capability. Explicit non-borrow for Control.
- **Zero-config learning from real-world corpus.** A maintainer method, not product architecture. Adopt as a corpus-sourcing method for G13 with Fallow's public-only privacy boundary.
- **Declarative policy authoring and test UX.** Fallow's seven-row fixture matrix is a strong RulePack acceptance template. Ties to the `05` contribution model, which still needs product sign-off.

**Reject adaptation (explicit non-borrows)**

- Syntactic fallback when semantic identity mismatches, and `best-effort` timeouts reporting syntactic findings as the result. `05`: elapsed time cannot manufacture semantic BudgetExhausted.
- Global confidence ladder (`very_high` to `none`) and `actionable` flag on findings. C-1 forbids `quality`, `tier`, `degraded`, `rank`.
- Protocol adapters applying "surface-specific exit policy" (Fallow architecture invariants). D9 owns termination.
- Remote `$schema` URL fallback in generated config. Offline law.
- Text-heuristic weakening detection as a gate. Fine as a syntactic rule later; it has the silent false-negative mode `05` documents.
- Fallow-shaped stable IDs replacing the host recipe.

`★ Insight ─────────────────────────────────────`
Fallow and OpenSIP make opposite default bets. Fallow is syntactic-first with an opt-in semantic pass that *refines* findings and abstains conservatively. OpenSIP is predicate-relative: a rule declares the rung it needs and gets Coverage-indeterminate if unmet. Fallow's five outcomes (`confirmed-used`, `retained-abstained`, etc.) are provider verdicts. Under DR-133 those must become host-side sufficiency results over provider facts. Same information, inverted authority.
`─────────────────────────────────────────────────`

## 2. Contracts to settle now

1. **Advisory anchoring law.** Owner: Product + agent-surface/operability. Home: MAP-VS-CONTROL §5 and `08` agent surface.
2. **Recommendation as read-only projection.** Owner: Product/CLI + configuration. If implemented, it fits the doctor project-mode resource envelope (DR-114) rather than a new admission class.
3. **Repair precondition law.** Owner: Semantic + product. Home: `05` capability matrix or `08` admission classes.
4. **Registry-derived public identity.** Owner: Output/operability + CLI. Home: `08` command grammar bullet on spec-driven registry.
5. **Observation relation families as declared extension points** of the closed v1 relation registry, dimension list only. Owner: Semantic.

None of these introduce a universal evidence ranking or a model in Control.

## 3. Minimum safe doc strategy

**Create one new file** `docs/coop/FALLOW-BORROW-REGISTER.md` mirroring the Gortex register's form exactly: pinned commit `23bb9a7e…`, non-authoritative status, `FW-01..` accepted/parked rows with disposition vocabulary (`ARCHITECTURE-CLARIFICATION`, `POST-V1-PARKED`, `PHASE-5-MEASURE`), `FW-N01..` non-borrows, maintenance rule. A new file strands no pin.

**Link from** README's table (next to the Gortex row), START-HERE's directory list, and MAP-VS-CONTROL §8 competitive adjacency plus its change log. MAP-VS-CONTROL is guidance with its own change log and is not cited by any register row I found.

**Do not edit** `04`, `05`, `06`, `08` in `docs/coop/architecture`. They are SEALED or CANDIDATE with review pins. The register's "OpenSIP home" column links to them.

**File 08 acknowledgement.** Every edit strands whole-document pins (the register documents this defect itself). D-369's recording preconditions cite "the resulting file-08 digest". Codex must check whether `architecture-application.v1.json` pins file 08 before touching it. My recommendation: no row edits at all. If the user wants 08 to acknowledge, one appended dated note under "How to use the register" stating the supplement is non-authoritative, changes no row, gate, or preview scope, and naming the rows it would touch on re-entry (DR-114 for recommend, DR-128/117 for third-party advisory surfaces, G25 for omission fixtures). That note needs a pin-move record with property verification in the established form. Otherwise put the acknowledgement in file 10's deferred-directions table, which is explicitly non-binding.

**Preview semantics and qualification.** Nothing above changes analyze, doctor, or help. Two items would if made binding, and I recommend neither now:

- A preview fixture asserting the human summary lists unrun predicates and extraction skips. `04` seals the principle, but DR-131 excludes output schema (owned by DR-123) and the pinned contract covers only the indeterminate outcome. Binding it means adding to the G25 corpus, which is a qualification criteria change requiring gate-owner recording.
- A `recommend` command. D-002 fixes the command surface; adding one needs a scoped D-002 successor.

## 4. Gaps and disagreements

- **"Deterministic output/fingerprints" should come off the adopt list.** It reads as if Fallow has something OpenSIP lacks. The reverse is true.
- **"Zero-config" hides two ideas.** Detection-derived proposal is fine. "Strong defaults so no config is valid" is already the preview: one bundled pack.
- **Missing from the list:** fail-closed inspect on source digest, consent boundary where project config and MCP cannot authorize a download (matches grants living only in private host state), and the contract-surface drift gate. Include the first two as confirmation rows.
- **Branching conservation** (`audit_branching.rs`) is a good essay on metric honesty but is a health metric. Exclude from Control; at most a rule-authoring caution that per-unit ceilings constrain partition, not quantity.
- **Exclude entirely:** cloud runtime source, license watermark, telemetry, decision cap numbers, AskUserQuestion payload shapes, token lists.

I will review the concrete Codex patch next against this list, in particular the file-08 pin question and that no row disposition or grade is asserted.
