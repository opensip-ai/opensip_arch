# Blind11 diagnosis v2 — corrected coauthor assessment

**Standing.** Actual Grok coauthor. Not independent design ACCEPT, not NEW blind, not application. Source24 acceptance is unchanged. Fresh B and application remain pending. Claude-credit availability is not assumed. v1 under `grok-blind11-diagnosis.v1` is **INTERRUPTED** (`stopReason` cancelled ~25, cause unestablished, not max-60). All v1 bytes are left in place; this directory does not rewrite them.

**Verdict: `CONSUMER_CLAIM_REFUSED`.** Consumer11 `ACCEPT-RECONSTRUCTABLE` remains false. Core v1 facts stand: omitted retained schema bytes, then unsorted `canonical-set` on `analysis.capabilities`. No product-law hole. No root-importer error. v1 **strategy and several helper claims do not stand** and must not be used as-is.

## What v1 got right (reused, not rerun)

Exact five exports fail frozen `open_run_closure` with `EVIDENCE_UNAVAILABLE:a87331bca7545468a266d74776d785a9903f93563220ac7f6267b6d749b82257` = kit `native/native-evidence.schemas.v2.json`, named on Coverage/`schemaDigests` and absent from `blobs`. Also omitted when cited: relation-payload `53380a…`, identity-schemas.v3 `b187a21c…`, ts imported-evidence `edce21a3…`. Parser selfcheck still distinguishes that from importer failure. Diagnostic copies that add those **known kit file bytes** (not remints) next refuse `x-opensip-order: canonical-set` on `semantic-configuration.analysis.capabilities` = `['inventory','syntax','clones-fact']` (canonical-set order `clones-fact`,`inventory`,`syntax`). C does not sort. Selectors remain identity-and-evidence §3 and `identity-schemas.v3.json` (kit texts/schemas), not author Python.

Live `reviews/consumer-b.v11` ts.store.json still matches tmp `0b3102a2…`.

## Correction 1 — kit has procedure/text/schemas, not runnable author models

Normative kit is 80 files, **zero** `.py`. It does **not** include `identity-model.v3.py` or `foundation/canonical.py`. It does include `identity-and-evidence.md`, `identity-schemas.v3.json`, `native-evidence.schemas.v2.json`, atom/composition contracts.

v1 `runnableAdmissionProcedureInProductKit: true` and “gate ACCEPT on frozen `open_run_closure`/`close_run` inside the fresh session” are **wrong**. Putting author models or frozen root outputs **inside** fresh B is an oracle, forbidden by the original charter (“Do NOT access … author Python/TypeScript reference models”).

Operational division:

| Who | Job | Must not |
|---|---|---|
| Fresh consumer | Independently reconstruct C, `x-opensip-*`, digest retention, retained joins, and replay **from kit text/schemas**; export exact object table + blobs | Import author/`identity-model.v3.py`/`canonical.py`; treat root expected graphs as answers |
| Root | After export, admit those **exact** bytes with frozen models | Treat a listed export path as the consumer’s self-ACCEPT |

`R-ROOT-ADMISSION-EXPORT`’s path observable **exposes output for root**. It is not a product-law gap and not something the consumer can honestly mark as “I ran frozen close_run.” Consumer false ACCEPT still violates **its own** stop condition: owning-schema **including published kit keywords**, then independently reconstructed closure joins, then independently reconstructed replay; helper self-consistency is forbidden. That is consumer instruction failure, not “the kit forgot a runnable model.”

v1 cited `identity-model.v3.py blob()` as if it were a kit selector. The **kit** selector is identity-and-evidence §3 (`raw-artifact` / `preimage`: store fetch and rehash) plus the payload-registry row. Root uses the author model to **execute** that law after export.

## Correction 2 — selected rules; do not over-claim helper branches

All five retained replays and the ts `ruleProgramDigest` program select **one** rule:

`file-exists`: `emitWhen = {relation: file, op: exists, minResolution: enumerated, filters: []}`

ts graph also **contains** `clones` and `calls` facts (Run-property material). Those are not selected evaluator predicates. Helper `eval_atom` matching only file/clones, and the unused clones branch, **do not by themselves** prove the required file-exists Run semantically wrong.

`evaluation-subject` records for the four file paths are already in the ts object table. A pure evaluator **may** derive computed subject hashes/records for comparison. v1 calling `put_h("evaluation-subject")` invalid is **withdrawn** unless a selected-graph semantic error is shown. This diagnosis does **not** establish that file-exists matching is false on these four inventoried file subjects (enumerated file facts exist; helper exact-rung equals requested `enumerated` here). Full atom-contract walk (rung ≥ min, occupancy, completeness partitions) was **not** independently re-executed; that limit is stated, not hidden.

`R-RUN-CLONES-*` remains a complete-Run **property** to exhibit on the graph. It is not the selected replay rule. Do not conflate missing helper relation arms with “the file-exists Run is therefore invalid.” The file-exists exports still fail **owner custody** (schema bytes, then canonical-set) before M3 replay.

## Correction 3 — tamper and recompute: actual code + root counterexample

v1 probe set `recomputeComparesSavedReplayVerdicts: false` by grepping **single-quoted** `replay['claimedVerdict']`. Source uses **double quotes**. That probe boolean is not a measurement PASS.

Actual `recompute.py`: helper `close_run`; then `claimed = replay["claimedVerdict"]`; `recomputed = replay["recomputedVerdict"]`; fail only if helper `close` is not ok, H mismatch, or `claimed != recomputed`. It does not invoke evaluator replay and does not read `proofId` / `ruleResults`.

Root disposable counterexample (`blind11-root-recompute-counterexample.v1/report.json`, originals unchanged):

- original final exports: **exit 0**, `verdict pass pass` all five
- saved replays falsified to `fail`/`fail` with empty `ruleResults` and zero `proofId`, stores unchanged: **exit 0**, `verdict fail fail` all five

That is discriminating evidence that “from-scratch recompute” does not independently replay.

Actual `tamper()` in `reconstruct_rest.py`: deepcopy proof descriptor, flip `proof["verdict"]`, set `replayRefuses` to that inequality. **No replay invocation.** `replayRefuses: true` is tautological, not a tamper control under `R-REPLAY-TAMPER`.

## Completion strategy (current kit only; do not start a new blind here)

Do **not** retry the identical consumer-b recipe. It is likely to false-ACCEPT again (helper graph + listed export + 123 checkboxes).

Do **not** relax independently reconstructed closure/replay. Do **not** change ACCEPT to mean “root will fix it later” or “path listed.”

**Preferred: incremental fresh B, enough turns, honest checkpoints.** Same 80-file kit. First reconstruct C and `x-opensip-order`/`x-opensip-digest` from identity-and-evidence §3 and the schemas (consumer-authored code, not author models). Put **exact kit document bytes** in `blobs` under every named schema digest **before** hashing Coverage/view. Mint **one** small file-exists Run. Independently close and replay **that** export from kit laws. Only if that reconstructed closure/replay holds, widen vectors. Checkpoint after that early gate. If it fails, `CHANGES_REQUIRED` / incomplete — not ACCEPT.

**Team split (peer groups, no author code, no root expected values):** Consistent with the original consumer-B **objective** (one fresh origin reconstructs implementer needs from the kit; no oracle) if and only if:

- every group’s only design input is the same normative 80
- no group receives author models, frozen expected graphs, or root answers
- builder exports are **untrusted** inputs to a validator group that independently reconstructs closure/replay from kit text/schemas
- the integrated consumer verdict is blocked if that validator refuses; ACCEPT is not a builders-only vote
- kinds are not quietly upgraded/dropped

Original **no-subagents** was a **session procedure**, not the consumer-B objective. A coordinated team is not automatically a new origin if it is still one kit, one export set, one verdict. It **is** an oracle if any member is seeded with author code or root expected values. Splitting without an independent kit-only validator just parallelizes the same false-ACCEPT recipe.

Root continues to admit exact exports **after** the consumer; that remains root’s job.

Optional later charter tweak (future kit, not a rewrite of consumer11): keep path listing as the **root-facing** handle; do not tell the consumer to execute frozen models. Consumer stop-condition text is already strong enough if followed.

## Limits

- Original parser not rerun in v2; first-failure and diagnostic next-failure taken from intact v1 measurements plus root’s already-run reports.
- Full M3 semantic replay still not reached on original bytes.
- File-exists helper matching vs full atom-evaluation contract not proven wrong on this graph.
- Query reconstruction not re-executed (no owner-admitted Run).
- Claude-credit question unanswered.
- This session does not launch a new blind.

## Conclusion

Consumer11’s five exports are not reconstructable complete positives. First failure is omitted retained Coverage schema document bytes the kit already names. Next, after diagnostic byte restore only, is unsorted `analysis.capabilities`. Those are consumer reconstruction mistakes against published kit **text/schemas**. The parser is fine. There is no missing product recipe and no importer bug. v1 was wrong to put frozen/author Python inside fresh B, wrong to treat evaluation-subject derivation and unused relation arms as proven invalid, and wrong to treat a failed single-quote probe as a recompute measurement. Tamper is verdict inequality without replay; root’s falsified-replay counterexample shows recompute will PASS a hollow fail/fail. Next fresh B must reconstruct closure/replay from the 80-file kit, retain schema bytes, obey `x-opensip-order`, and fail honestly at an early one-Run gate — or use a kit-only builder/validator team with the same bar. Do not repeat the identical ACCEPT recipe.
