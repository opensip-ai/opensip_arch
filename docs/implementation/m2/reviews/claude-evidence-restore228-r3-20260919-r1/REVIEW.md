# Independent scoped review — root-frozen evidence-restore 228 revision 3

Reviewer: Claude. Date 2026-09-19. **Scope: the frozen r3 bytes — `RESTORE.md`, `MUTATION-PUBLICATION.md`, `restore_model.py`, `checkpoint_model.py` and their variant corpora. Not cumulative, implementation or protocol approval.** No product/candidate/architecture edit, commit or push. I supplied source analysis for this owner; I do not infer agreement from that — everything below was checked against the frozen bytes and the pinned sources. Acknowledged owed items (bundle/body/receipt/association/DDL codecs, public detail, adoption, native qualification, durable workflow-ending carrier) are not raised unless the direction blocks them.

## 1. Identity, dependencies, and how I ran things
- Archive pin read first; `subject.tar.xz` SHA-256 `9844908410ec90fb1b828df5970e19c1e0c1b11e198eb58c61257ffdd107ed1b`, 321,496 bytes, **250 members** — equal to the request and pin; exact TAR membership equals `subject.json`; every member's size and SHA verified from the tar before extraction; 0 non-regular/unsafe/extra; end pass `re-verified`.
- Frozen sources are byte-equal to **my own verified reference-201 extraction**: `kernel201.py`, the three product contracts, `source-build-plan.md`, `source-invocation-record.schema.json`, `source-repair.schema.json` (the `evaluator3` copy, `678d8a4f…`). `beforeimages-r1/RESTORE.md` equals the r1 I reviewed.
- **Live paths are not frozen proof.** `restore_model.py` hash-asserts the live 201 kernel (good) but imports `checkpoint_model.py` from the **live draft path `m2-evidence-restore-draft-228/` with no hash assertion**. At review time that file equalled the frozen one; I nevertheless ran a **privately staged copy** whose only change is that import pointing at the frozen file (`claude-out/staged/`, one-line diff retained), and staged every restore variant the same way. Results: restore model = `restore-model-r5.json` (**52**); gate model = `checkpoint-model-r1.json` (**61 guard/inspection cases, 32 interleavings**); **16/16** restore variants (mutants-r4) and **11/11** gate variants rejected with the exact predeclared labels; both baselines pass. Report-named cases only; no generator executed.

## 2. Direction against sources — no contradiction found
Unchanged `MutationReceiptV1` and `receipt2:` recipe; replay key `H("workflow.mutation-intent",{schemaVersion,requestId,stepId,projectId,operation})` with ExecutionId excluded (workflows §1); no GRANT/RA/ICI/ICO/SEAL, no permission token (`permission-truth-tables.v9` closure rule), no `AttemptCustodyV1` widening (identity §2 "exactly"); trust writes under the fence before the lease (S7); final checks → gate as the last admission act → one ledger transaction → barriers under the lock; latch vs durable REV distinguished (S6, F38–F41); body → digest, receipt → receiptId, association last, nothing pointing back; no FAILED/INDETERMINATE receipt from the failing attempt, consistent with `StepResult`'s conditional `required` and the `receiptId:null` purge precedent; stopped session limited to journal cleanup; inspection is a *separate* private owner and "a missing set is unknown". Root's refusal to call the failed attempt "already durably described" is right: the invocation **schema** is not a durable carrier, and the text now says so.

## 3. Findings

### B-0 Blockers to the direction
None.

### M-1 (Medium) — the integrated model never exercises a non-durable native outcome, and mislabels one when it occurs
`restore()` calls `checkpoint.publish(ctx, transaction, latch=latch)` and **never passes `native`**, then returns `'completed' if result['deliveryAllowed'] else 'completed-delivery-failed'`, ignoring `result['outcome']`. Probe (`claude-out/probes/my_probes.py`, frozen gate model, staged restore model, `native` forced):
| native | `restore()` returns | imported records | scope marked completed |
|---|---|---|---|
| `rolled-back` | **`completed-delivery-failed`** | 0 | no |
| `uncertain-absent` | **`completed-delivery-failed`** | 0 | no |
| `uncertain-present` | **`completed-delivery-failed`** | 1 | **yes** |
So (i) a rolled-back or uncertain publication is reported as *completed*, contradicting MUTATION-PUBLICATION ("No uncertain result is changed…", "Native uncertainty remains unknown even if rows are currently visible"); (ii) after `uncertain-present` the scope is treated as COMPLETED, so a same-scope lookup would deliver a replay from a receipt whose durability was never confirmed. The claim "Its final checkpoint invokes checkpoint_model.py … Late latch retains imported completion and reports failed delivery" is true **only for `native='durable'`**; the 32 latch × native combinations live in the gate model alone. **Correction:** plumb `native` through `restore()`, map `outcome` exactly (`completed` / `failed` / `durability-undetermined`), assert the three non-durable rows end-to-end (no completion label, no delivery, scope not replayable on an uncertain outcome, fresh scope required), and add the variant "integration ignores gate outcome".

### M-2 (Low–Medium) — the adoption/bundle request needs a named immutable binding; `inputDescriptorDigest` is the inherited home
The replay key deliberately excludes inputs, and `MutationParams.target` is a `UserInputPath` that "never enters identity". MUTATION-PUBLICATION says "Retained immutable invocation parameters and dependency results bind the actual bundle/adoption request before lookup" without saying **where**. **[E]** `MutationParams` (closed) has `inputDescriptorDigest`: "Retained closed operation-specific input: CoreTransitionIntentV1 for installation operations; RepairRecoveryIntentV1 for repair-recover", required by `allOf` for six operations. Project-adoption consent (`origin ProjectId`, target) is exactly such an input; without it, the only request data in the step is a path. **Correction:** state that evidence-restore carries a closed restore-intent descriptor via `inputDescriptorDigest` (and joins the `required` list), and that the association's "exact replay scope" also records that digest. Not doing so does not block the direction, but it is the one place the text could be completed wrongly (consent carried as an unbound flag).

### M-3 (Low–Medium) — unpinned live dependency in the evidence chain
See §1: the restore model's gate dependency is a mutable draft path without a hash check, unlike the kernel. Anyone re-running the frozen model later may silently test a different gate. Pin it like the kernel, or import the sibling file.

### L-1 (Low) — "barriers while retaining the checkpoint lock" is not asserted
My variant moving `after-barrier` to after the unlock **survives**: the trace assertion checks only `lock < admit < consume < unlock`. Add `after-barrier` (and the transaction) inside that ordering.

### L-2 (Low) — step 3's journal transaction
"Prepare the existing carrier transactions … (journal before ledger) … this does not authorize a new journal effect." Under α nothing is appended, so a journal **write** transaction only adds busy-refusal modes; the "no prior durable REV" read is already stable under the in-process level-4 lock. Say whether the journal is opened for read or write, and why.

### L-3 (Low) — export's publication path is unstated
MUTATION-PUBLICATION covers restore only. Export also writes (backup-export pins plus its receipt). State whether it uses the same final checkpoint/one-transaction shape or only the ordinary generic-mutation path; today it is neither claimed nor excluded.

### L-4 (Low) — `attempted_scopes`
"Incomplete scopes do not retry" is enforced by an in-memory set (my variant removing it is rejected by label). That models *in-invocation* state, which is correct — a fresh process necessarily has a fresh RequestId and scope — but the limits string should say so, so it is not read as durable attempt evidence, which α deliberately does not have.

Not a finding: my variant "guard refusal does not latch the gate" survives; the prose does not require a latch on refusal, so nothing is owed.

## 4. Claims versus test scope
Counts reproduce (52; 61 + 32; 16 + 11 exact labels). Accurate limit statements: observations and native outcomes are asserted, no real concurrency, no codec. One claim needs narrowing (M-1). The gate model's `recover('absent', all-admitted) → 'no-completion-observed'` correctly avoids a negative.

## 5. Limits
Prose, two conditional models and frozen source copies; I executed the staged models, the 27 report-named variants and four variants/one probe of my own, all inside my review directory. Nothing native, no codec, no registry integration exists to review. This is a scoped review of r3, not approval of 228 or of anything it depends on.

## 6. Result
**Direction faithful to the pinned sources; no blocker. One Medium model defect (M-1: non-durable native outcomes are unexercised end-to-end and mislabelled as completed), two Low–Medium completions (M-2 input binding, M-3 unpinned dependency), four Low observations.**
