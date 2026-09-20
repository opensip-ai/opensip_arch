# Bounded review — frozen incomplete WIP215 revision 13 (closure of my r12 V-1..V-3 model observations)

Reviewer: Claude. Date 2026-09-19. **Scoped model closure only; not protocol approval; no root/product edit, commit or push.** The creator (224) corrections are not discussed.

## 1. Identity and what I ran
- `subject.tar.xz` SHA-256 `fc4171d152614d4598000568640b87c74e04968677b0cc8e392a41957cd7e7f1`, 188,340 bytes, 1,219 members — equals the request; every `subject.json` member rehashed from the tar before extraction; 0 non-regular/unsafe/extra; end pass `re-verified`.
- `beforeimages-r13/OWNER.md` = my r12; OWNER differs from r12 **only in its heading** (diffed). `standing_reset_model.py` is byte-equal to r12 (inherited, not re-run).
- Main model re-run = `ordinary-batch-model-r9.json`, counts unchanged (6272; 4096/1024; 80; 1; 26258 / 1075413 / 12987). `coordination-corpus-r7/baseline.py` = model.
- **Corpus r7 by report name only** (guarded runner; names from `report.json`, generator names asserted absent, sources with `mkdir`/`write_text`/`subprocess` refused, hashes verified, cwd = my directory): **53 named / 50 distinct, 53 rejected, 53/53 exact labels**, baseline passes. *Disclosure:* my adapted runner first failed on its own tuple syntax (a `sed` edit dropped a trailing comma) **before executing any case**; fixed and re-run. No generator or historical script was executed.

## 2. Closure
| r12 | r13 | Status |
|---|---|---|
| **V-1** no path invariant; variants died only on pinned counts | every explored transition now carries whether it was an *accepted COMMIT*, and the loop asserts `pre-BEGIN revocation discharged only by COMMIT` (next state ∈ {RECOVERY, REVOKED} for every revoked-source member otherwise); `closed batch retains no live BEGIN sources` asserted in `check_barrier`. My r12 `x1`/`x2` equivalents (`r13-producer-forgets-protected-source`, `r13-harness-allows-protected-interruption`) now die on the **path invariant**; `x4` (`r13-closed-batch-keeps-sources`) on the no-stale-sources label; `x3` (`r13-BEGIN-forgets-sources`) on the admitted-BEGIN precondition; `x6` on `protected ABORT restores revocation` | **closed** |
| **V-2** `recovery_revoked` defaulted to `False` | `bool|None = None`; `ordinary()` asserts `RECOVERY requires admitted restriction evidence` (exact type `bool`); `abort()` now **requires** `begin_sources` and a lawful source for every RECOVERY member (`ABORT requires admitted BEGIN context`); both refusals have exact-message tests and corpus variants (`…-defaults-false`); the 6272 cells and never-established checks pass explicit `False` | **closed** |
| **V-3** stale assertion label | now `ABORT preserves revoked source, otherwise unbootstrapped` | **closed** |
Excluding my equivalent `x5` from the unsafe counts, and not double-executing the `x6` alias, are both correct.

## 3. Independent variants
Three new ones (`claude-out/probes/model_mutants_r13.py`): a protected below-threshold observation exits to `UNBOOTSTRAPPED` → rejected by `revoked BEGIN source blocks quorum interruption`; a *refused* COMMIT nevertheless resets a protected member → rejected by `protected commit still needs quorum`; `begin` records the BEGIN source only for the first selected member → rejected, but by **`retained exploration coverage`** only. All three rejected.

## 4. Observation (Low; optional)
**W-1 — the path invariant and the protection share one source of truth.** Both the rule (`ordinary`, `abort`, the harness's skip) and the new invariant read `world.begin_sources`, which `begin` itself produces. If `begin` mis-records a source for some members (my `y1`), protection and invariant go blind together and only the pinned counts notice. The harness already knows the pre-BEGIN states at every BEGIN it performs (the seed vector, and the state vector in `check_barrier`'s restart). **[P]:** assert `begin(...)`'s `begin_sources` against that literal vector at both sites (one line each) — then a mis-recording BEGIN dies on a named invariant, and the path invariant's input is independently checked.

## 5. Limits
One conditional model with admitted boolean inputs; I executed the model, the 53 report-named cases and three variants, inside my review directory only. OWNER prose is unchanged from r12 apart from the heading, so nothing new in the logical owner was reviewed. Nothing here approves 215.

## 6. Result
**V-1..V-3 are closed. No finding; one optional Low observation (W-1).**
