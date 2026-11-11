# OpenSIP final-product design: independent assessment

2026-11-10. Independent read-only assessor (Claude Fable 5.2). Architecture commit `e47ebabedd4c77e3d009e91c6ca7d91a23625b73`.

Saved by the lead from the assessor's returned text, unedited. The assessor could not write files itself.

## Judgement

None of the three earlier findings justifies a change to the accepted product contracts as the change was proposed. Each finding quotes the text accurately. But the first aims its remedy at the wrong clause, the second is better fixed by a successor the project has already planned, and the third is largely covered by two adopted plans that the earlier summary does not mention.

The earlier conclusion that the design "addresses all four goals substantially" is too generous in two places.

- **Usability where a person or agent meets a finding.** A finding as contracted today is a rule, a file path, a symbol name, a severity and a message code. It has no line position, no related locations and no explanation, and the SARIF output is not allowed to carry a line. The project's accepted quality plan says this itself and proposes the fix, but the contract successor is not written.
- **Speed.** The only measurement taken so far missed your approved budgets on most medium repositories, and the replay the design requires before every sealed result grew faster than linearly. You decided on 2026-10-14 to wait for the reference-runner measurement. That is reasonable, but speed is unproven, not addressed.

Finding quality and verified improvement are well supported, by the evidence design and by the targets you approved on 2026-10-03.

Three things are worth doing now. All three are already named in accepted plans, so this is a recommendation about priority, not new scope.

1. Write the finding-explanation successor (the quality plan's D8) before M4 renderer work starts, and make it carry a display position and related locations.
2. Measure replay on the first real admitted graph instead of waiting for M6, with a stated threshold at which the replay implementation gets attention.
3. Note now, for M5 planning, that `repair preview` shows no diff.

Everything else should wait for measurements.

## Sources and short names

All paths are under `/Users/sb/code/opensip-ai/opensip_arch/`.

| Short name | File | Standing |
|---|---|---|
| WS | `docs/v2/contracts/product-v1/workflows-and-surfaces.md` | Accepted contract (D-372) |
| NE | `docs/v2/contracts/product-v1/native-evidence.md` | Accepted contract |
| IE | `docs/v2/contracts/product-v1/identity-and-evidence.md` | Accepted contract |
| AQ | `docs/v2/contracts/product-v1/admission-and-qualification.md` | Accepted contract |
| SEC | `docs/v2/contracts/product-v1/security-and-lifecycle.md` | Accepted contract |
| SMAP | `docs/coop/design-corrections/current-source-map.proposed.md` | Applied by D-372 despite the filename |
| QG | `docs/coop/design-corrections/qualification-gates.applied.v1.json` | Applied gate map; nothing qualified |
| CH10, CH13 | `docs/v2/architecture/10-mvp-and-future-scope.md`, `13-evidence-workflows-and-product-contracts.md` | CH13 §§5–7 and 9 are replaced by WS §§1–7 (WS:66) |
| BP | `docs/v2/architecture/implementation-boundaries-and-build-plan.md` | Milestone and command routing |
| AQP | `docs/implementation/m3/analysis-quality/PLAN.md` | Accepted plan r6, 2026-10-03; a plan, not a contract (AQP:9) |
| M3P | `docs/implementation/m3/M3-PLAN-r10.md` | Accepted M3 plan |
| AGI | `docs/implementation/agent-interface/` (`README.md`, `GUIDANCE.md`, `EVALUATION.md`) | Reviewed delivery guidance; selects no release gate (README:3-7) |
| SMR | `docs/implementation/m3/s-m-report/S-M-REPORT.md` | Preliminary measurement, lead's macOS host (SMR:3) |
| schemas | `docs/coop/design-corrections/workflows/schemas/evaluator3/*.schema.json` | Owning output schemas (SMAP:40-44) |

Implementation standing: M3 is not complete (`docs/implementation/m3/IMPLEMENTATION-STATUS.md:3`). The first usable `analyze` is M4. Review, repair and `agent serve` are M5. Qualification is M6 (BP:887-890, 949-997). All three earlier findings concern M5 or M6 surfaces, so none blocks current work.

## The three earlier findings

### 1. Repair prerequisites: partly agree

**The text is as described.** The gate "covers **every `delete` and every `replace` edit** in the plan … without qualification" (WS:724-727), and eligibility is "the **conjunction** of `deadCodeRepairEligible` over every selected record" (WS:815-816).

**The diagnosis is wrong in one important way.** Repair edits are whole-file: the edit record is a path, an action and two digests (`repair.schema.json:309`, `FileEdit`). Removing one unused function from a file is therefore a `replace`. Covering every replace is not an over-generalisation of a deletion rule. It is how in-file dead-code removal is expressed.

**The reachable scope today is dead-code removal only.** The only recipe identifier I found in the workflow reference cases is `remove-unused-export` (`docs/coop/design-corrections/workflows/workflow-cases.v1.json:3824`). CH10:45 scopes repair to a deterministic lifecycle with "no implicit mutation or model-driven autonomous maintenance loop". The "replacement-based refactors" the earlier agent worried about are not in the design, so splitting prerequisites by repair type would change nothing today.

**The real narrowness is in the eligibility ingredients, which the earlier finding did not trace.** `deadCodeRepairEligible` needs `exportsClosed=closed` (NE:2237-2239). That needs a manifest that "publishes nothing" (NE:2216-2218). The reference model marks any `package.json` with `main`, `exports`, `module`, `types`, `bin`, `browser` or `files` as open, and any Cargo package with a lib or proc-macro target as open (`docs/coop/design-corrections/native/native_evidence_model.v2.py:1655-1667`). A user declaration cannot override this. One non-literal `import()` anywhere in the universe also disables repair for the whole universe (NE:2221-2222, 2238-2239), although findings treat dynamic edges per target (NE:2230-2235). In practice OpenSIP's own repair will apply to leaf applications and binary-only crates. It will not apply to internal monorepo packages or to any Rust library crate.

**Scenario.** A pnpm monorepo has `packages/ui` with `private: true` and a `main` field. The advisory rule reports an export nothing in the workspace references. `opensip repair preview` returns the plan with `applicable=false` and `REPAIR.CLOSED_WORLD_NOT_ESTABLISHED`; unmet preconditions are plan data, not a failure (WS:915-919, 1272-1273). The developer or agent deletes the export by hand and runs `opensip audit`, which classifies the entry `CODE-FIXED` (WS:352-354). The cost is one manual edit. Finding and verification are unaffected, because the gate restricts only OpenSIP writing to the tree.

**Classification.** Deliberate scope limitation; WS:827-830 says "The conservatism is deliberate". There is one wording inconsistency: WS:716-717 scopes the requirement to "Destructive unused-code recipes" and SMAP:63 calls it "Recipe-specific", while WS:724-727 applies it to every plan. That matters only if a second recipe class is added. The plausible one is removing an unused dependency from a library crate's manifest, which this gate would refuse for a reason unrelated to that edit.

**Smallest response.** No change now. When the first real-repository results exist, count how many dead-code findings are repair-eligible. If the share is small, you have a real choice: accept that agents and people make the edits and OpenSIP verifies them, or add an explicit declared route for private internal packages. Do not relax the gate without that count.

### 2. Review briefs: partly agree

**The record is as described.** `ReviewBrief` requires `runId`, `candidates`, `producer`, `advisory` and `truncated`, and `candidates` is up to 1,000 candidate identifiers (`review.schema.json:334-367`).

**What other records already provide:**

| Wanted | Provided? | Where |
|---|---|---|
| Evidence references | Yes, as identifiers | `InspectionBundle.facts`, `coverageIds`, `importIds` (`review.schema.json:186-210`) |
| Limitations | Yes | `InspectionBundle.limitations` (`review.schema.json:211-218`); context coverage and truncation (WS:686-689) |
| Reasons for attention | Partly | `Candidate.kind`, `evidenceLevel`, `controlBearing`, `ruleId` (`review.schema.json:58-129`). Nothing says why one candidate is ordered before another |
| Next steps | No | `agentHints` is up to 64 free-text strings with no required content (`command-envelope.schema.json:150-158`) |

**Two things the earlier finding missed.**

- The adopted Fallow constraint required more than the successor kept. CH13:287-288 says "Deterministic selection records its version, inputs, reasons, scope, limits, and omissions." WS:66 replaces that prose, and what replaced it is "an advisory, bounded (≤ 1000) ordering labelled with its producer" (WS:696-697; SMAP:65). The reasons, inputs and version were dropped in consolidation. I could not tell whether that was deliberate.
- The better place to fix it is already planned. AQP:417-432 proposes explanation fields on every finding (reason, evidence path, scope statement, suggested action, limitations), and AQP:549 lists the contract successor as D8, status "proposed", for M4. `AGI/EVALUATION.md:72-89` separately scopes a context-pack experiment and warns "Do not assume that `InspectionBundle` or `ReviewBrief` already defines token budgeting."

**Scenario.** An agent is asked what to look at first in a pull request. `review brief` returns up to 1,000 `candidate2:` hashes. The agent calls `candidates` to learn each kind and path, `inspect` to get `fact2:` hashes, and `fact.list` or `artifact.get` to resolve them (`AGI/GUIDANCE.md:18-24`). That gives byte offsets, and only then does it read source. That is four operation types and one round trip per candidate before the first actionable sentence. A plain agent with grep may be faster on simple cases, which is the comparison `AGI/EVALUATION.md:15-21` requires.

**Classification.** Usability refinement, and partly a constraint lost in consolidation. Not a defect in authority or correctness.

**Smallest response.** Do not build a separate "compact brief". Put the explanation on the finding and candidate through D8, make sure that successor covers the advisory candidate kinds as well as findings, and have the brief successor record the producer version and a reason code per entry. The ranking itself should wait: CH13:290-292 says "User research and measurements should choose the list size".

### 3. End-to-end usefulness in acceptance criteria: partly agree

**The gate-map observation is correct.** I read the acceptance, evidence and threshold text of all 32 gates in QG. None names a completed human or agent task. DR-G13 (QG:263-275) asks for per-cell exact observations, performance, and real repository shapes with "manual-correction counts".

**Most of the proposed obligations already exist in adopted plans.**

| Proposed measure | Already present | Where |
|---|---|---|
| Useful versus rejected recommendations | Yes, reported without a target | Precision ≥ 0.99 gating and ≥ 0.90 advisory at 95% confidence (AQP:148); accepted versus dismissed counts (AQP:162) |
| Time and manual corrections | Yes | Zero manual corrections for conventional shapes (AQP:154); triage time and time to first trustworthy result (AQP:161-162) |
| Agent tool-call and context cost | Yes | Paired plain-agent versus OpenSIP study; adoption, outcome, tokens and elapsed time kept separate (`AGI/EVALUATION.md:11-52`) |
| Full analysis and edit/recheck performance | Yes | Three workflows including a preparation-invalidating edit (AQP:361-364); budgets (AQP:374-378); single-file edit ≤ 2 s (AQP:385) |
| Verified improvements and regressions on complete tasks | No | The agent study lists investigation tasks only (`AGI/EVALUATION.md:23-24`). Q7 is a rubric on whether a developer "could act" (AQP:429) |

**Their standing is weaker than a gate, by explicit decision.** The Q2–Q8 targets are owner-approved (AQP:544) but "Until it is accepted, Q2–Q8 are reported at M6 but are not qualification evidence" (AQP:450). They wait on a DR-G13 successor. The agent study is required only before claiming benefit, "without adding a delivery prerequisite" (`AGI/review/AUTHOR-ASSENT.md:5-7`).

**Scenario.** An agent is told to clear the unused-export findings in one package. OpenSIP passes every fact oracle and the precision target. The agent removes an export that a test helper loads dynamically. Only a task that ends with a re-check and the project's tests would catch it. No current instrument scores that.

**Classification.** A qualification detail already scheduled to be selected later, plus one missing task type. Not an architectural omission.

**Smallest response.** No gate-map change now. When the DR-G13 successor and the agent study plan are written, add a small set of closed-loop tasks: finding, edit, re-check, with a pass defined as the target `CODE-FIXED` and nothing `CODE-NET-NEW`. The product already computes those classes (WS:352-354) and the `repair verify` outcome (WS:1039-1040), so this needs no new infrastructure. Whether an agent-use result becomes a release prerequisite is your decision, and it is best taken at M5.

## Additional concerns, by likely effect

### A. A finding does not say where or why (highest effect)

- `FindingSurface` carries `subjectPath`, an optional `qualifiedName`, `severity` and `messageCode`, plus a digest of the parameters, not the parameters (`common.schema.json:1635`).
- "A finding locates through `finding-fingerprint.subjectKey.logicalPath` … `finding`, `finding-fingerprint`, `proof-bundle` and `predicate-witness` carry no anchor field at all" (IE:1027-1031).
- A SARIF result has one location containing only a file URI, and the schema forbids anything else (`sarif-adapter.schema.json:243-275`).
- Message parameters are a fixed seven: rule, path, name, kind, language and two counts (`docs/coop/design-corrections/foundation/evaluator-composition-contract.v3.md:44`).

**Scenario.** A boundary rule fires in CI. The pull-request annotation lands at the top of `src/ui/button.ts` and says the rule matched two facts. It does not say which import, on which line, or what it reached. An agent can recover that with follow-up queries. A person reading a pull request cannot.

Keeping line offsets out of the fingerprint is correct and should stay (IE:200-202). A display position does not need to enter identity.

The accepted quality plan already records the gap: "O5. No explanation fields" (AQP:128) and "Without these, OpenSIP produces correct facts but not findings a developer can act on" (AQP:519). The gap is known and planned, but the contract successor does not exist. **Worth doing now:** write D8 before M4 renderer work, and require a display position, related locations and a SARIF region in it.

### B. Speed is unproven, and the one measurement is unfavourable

- The design requires complete replay before sealing: "independently reconstruct every subject, enumeration result, predicate descriptor and witness" (IE:1580-1584), and retaining every predicate node for every rule and subject (IE:1526-1537).
- In the measurement, replay over a synthetic graph took 28.5 s, 44.5 s, 62.5 s and 16.5 s on four medium TypeScript repositories (SMR:35-38), against a warm budget of 8 s and an edit target of 2 s (AQP:377, 385). "71 sources take 0.452 s and 1381 sources take 62.509 s" (SMR:120).
- The graph was one fact and one finding per source file (SMR:15). Real graphs will hold far more per file.
- Four of fourteen rows also exceeded the warm budget without replay, from analysis time alone (`docs/implementation/m3/s-m-delta-round/O3-O4-PROPOSAL-r1.md:27-36`).

You chose to keep the budgets and staging and re-test on the reference runner (`docs/implementation/m3/owner-decisions/2026-10-14/README.md:7-8`). I agree with not restaging on preliminary numbers. Changed-scope reuse is an M4 decision (M3P:741).

**Worth doing now:** measure replay on the first real admitted graph and state the threshold at which the replay implementation is reworked. If real-volume replay stays superlinear after an implementation fix, that becomes a design question about IE §4. Not before.

I could not find whether `--ephemeral` analysis skips replay (WS:242-248 does not say). It matters, because ephemeral is the natural edit-loop mode.

### C. The contracts alone do not define what OpenSIP finds

"O2. No first-party rule catalog" (AQP:125). The catalog draft is done as plan material (M3P:300), and the product pack is M5 (AQP:503). This is a sequencing fact, not a defect. The consequence is that finding quality first becomes observable at the M3 internal-harness dogfood checkpoint (AQP:500; M3P:316). That checkpoint is the one to protect from slipping.

### D. How often results will be determinate is unmeasured

- Nine framework recognizers exist (NE:2758-2760). Anything else gives `entryPoints.state=none`, and reachability negatives become indeterminate (NE:2768-2771).
- Computed member access and `any`-typed calls count against completeness in TypeScript as well as JavaScript (NE:603-610).

The posture is honest and the right default. The risk is a tool that is correct and frequently silent. The plan reports yield beside precision but sets no target (AQP:158-160). Set one at the planned target revisit, once exploratory numbers exist.

### E. `repair preview` does not show the change

The preview record carries paths, digests and a byte count per file (`repair.schema.json:309`; WS:712-714). Its parity fields are plan id, snapshot id, `applicable` and unmet preconditions (`docs/coop/design-corrections/workflows/command-inventory.v3.json:854`). I found no contracted surface that returns the new content or a diff. A person asked for interactive consent to apply (SEC S10.1) sees hashes.

This is a design omission in a closed schema, in an M5 feature. Fix it in the repair successor before M5. It is small.

### F. Watch at dogfood; no action now

- `recommend` can propose only workspace roots: "`recommendations` carries zero rows" (WS:1275-1279), against the fuller intent at CH13:67-72.
- After an OpenSIP upgrade, a baseline whose prior detector closure is unavailable makes `audit` indeterminate, exit 3 (WS:295-298, 314-316).
- A first run on a backup-managed storage root needs an explicit choice, and CI refuses without it (SEC:317-331).
- Default retention is durable and unbounded (IE:1633-1636). Store growth per run is not among the planned measurements.

## Strengths verified

- **Honest results.** Three-valued evaluation; a missing rung is indeterminate, never a silent fallback (WS:600-604; QG DR-G25). "Zero emitted findings never establish complete analysis" (WS:466-467).
- **Delta attribution suited to pull-request gating.** Code, detector, policy, scope and waiver changes are separated (WS:346-358). A bug hidden by disabling its rule still gates (WS:460-463). A removed detector cannot hide a new bug (WS:434-438).
- **Stable finding identity** that excludes line offsets and messages (IE:200-202).
- **Advisory work cannot become a verdict or a repair authorization** (WS:690-693).
- **Safe mutation.** Journaled apply with rollback (WS:1010-1022), and verification on a fresh snapshot (WS:1036-1042).
- **One typed envelope for people and agents**, with declared parity fields and bounded queries (WS:1108-1113, 1163-1172).
- **Quantified, owner-approved targets** with a confidence rule (AQP:145-154), and a real-repository corpus of 49 repositories with ten held-out families (`docs/implementation/m3/owner-decisions/2026-10-09/README.md:13`).
- **Policy can be tested before it is enforced** (WS:631-652).

## Now versus later

| When | Item |
|---|---|
| Now | Write D8 with display position, related locations and SARIF region, before M4 renderers (concern A) |
| Now | Measure replay on the first real graph; set a rework threshold (concern B) |
| Note now, fix at M5 | Repair preview shows no diff (concern E) |
| Wait for measurement | Repair eligibility share and any declared route for internal packages (finding 1) |
| Wait for measurement | Brief ranking and reason vocabulary (finding 2) |
| Wait for measurement | Yield target and recognizer breadth (concern D) |
| Wait for measurement | Budgets and staging, already decided 2026-10-14 (concern B) |
| Decide at M5 | Closed-loop tasks in the DR-G13 successor and agent study; whether agent-use results gate release (finding 3) |
| No change | The three earlier proposals as framed |

## Coverage and confidence

**Bootstrap.** Architecture `main` is at `e47ebabedd4c77e3d009e91c6ca7d91a23625b73`, the working tree is clean, and it is two local commits ahead of `origin/main` (OD-LEAD-1 and OD-PACE-1, process only). The route preflight printed `ROUTE-OK R3-FRONTIER claude claude-fable-5-2/high`. The product checkout is at `15690f3d`; I read only its README.

**Read in full.** START-HERE; CH10; CH13; the product-v1 README; SMAP; AQ; WS (all 1,699 lines); `review.schema.json`; the workflow projection contract; the three agent-interface documents; the O3/O4 proposal and both owner-decision READMEs.

**Read in part.**
- NE: §1.3, §4.4–4.8 and §6–8, of 4,282 lines.
- IE: parts of §3, all of §4, the start of §5.
- SEC: S3.1 and S10.1 only.
- QG: every row's acceptance, evidence, threshold and expansion text.
- AQP: §§1–3, 5–7 and 9–11; not the corpus method in §4.
- SMR: §§1–4.
- BP: the milestone and command tables.
- M3P and the M3 status board: keyword search only.
- Other schemas and three reference-model functions: targeted extraction.

**Not read.** The live control directory, by instruction. Any sibling worktree. The decision register beyond the readiness table. Product source. The earlier agent's full assessment; I had only the owner's summary. I ran no product code, benchmark or test.

**Confidence.**
- High on what the schemas and contract lines say.
- Medium on the absence claims: no surface returns a diff; no record carries ordering reasons; ephemeral replay is unspecified. Those rest on searches of the contracts and schemas.
- Lower on the current state of the D2 and D8 successors. The status board's evidence cut-off is 2026-10-22 and it does not mention them. The control directory may record progress I did not see.

**Stale labels that did not affect conclusions.**
- The register still says implementation is "NOT MET" (`docs/v2/architecture/08-decision-and-readiness-register.md:402`) while implementation proceeds.
- QG:268 says "cold/warm p95" where AQ:268-270 specifies median and maximum (AQP:132 records this).
- CH13's body still uses "future" for capabilities now in scope; its header explains this.
