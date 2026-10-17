# C1a4-blind: the blind validation run (run plan, under the C1a4-blind gate)

**Lead record, 2026-10-17. For Codex's pre-run review with C1a4-blind r1; nothing has been run, and no held-out entry has been opened.**

**Authority:**
- the owner's decision of 2026-10-16 (`owner-decisions/2026-10-16/HELD-OUT-T2-MARGIN.md`): the mechanical blind run;
- the C1a plan r6, RF-3 step 3: one gated blind validation run, with a pre-run review, the lead's run and a post-run review. It refreshes the discovery receipt against the final pins and writes the companion snapshot receipt in the closed format;
- the B2-b4 plan r6 §2.5: the receipt, its allowlist and its lifecycle;
- the B3-b3a2 and B3-b3b precedent: one gate reviews the tool and the run together.

**The same method, population and disclosure allowlist** as B2-b4c and B3-b3b. Discovery's blind mode is run unchanged. The companion's is new in this gate.

## Preconditions

1. **Codex accepts C1a4-blind r1** with `runAuthorized: true`.
2. **The gate's code commit is on product main,** with these five tools at exactly the reviewed bytes. The script asserts each, in the run worktree and on main:
   - `tools/security/snapshot_ledger_census.py`: as the gate's `product-map.json` archives it;
   - `tools/security/discovery_census.py`: `06382060…ffef`;
   - `tools/security/discovery_member_model.py`: `582bad12…21f1`;
   - `tools/security/snapshot_ledger_model.py`: `b985d7c8…8214`;
   - `tools/security/discovery_workspace_ledger.py`: `ee1d597a…6940`.

   The last four are main's bytes, which the gate does not change.
3. **A clean detached worktree of main,** `/Users/sb/code/opensip-ai/opensip-c1a4b`, holding no companion receipt yet.
4. **The freeze.** Main is `b753854` plus only this gate's code commit. Nothing else integrates before the run; in particular C1b-0, which changes the generator closure again, integrates only after it. A change to any bound input after the run makes both receipts stale.

## The run (`evidence/run_c1a4_blind.py`), once

**The invocation,** from the committed architecture path:
- `python3.14 -I -B evidence/run_c1a4_blind.py /tmp/opensip-implementation/c1a4b-run`, with its output in `/tmp/opensip-implementation/c1a4b-run.out`;
- then the post-run checks, `run_c1a4b_post_checks.py /tmp/opensip-implementation/c1a4b-post`: the census margin tests, both blind control sets and verify_design, in the run worktree, under the lane;
- then the lead's `RUN-RECORD.md` and the post-run package `c1a4-blind-run-r1/`, for Codex's post-run review.

1. **Under the lane lock,** at nice 10, with a private 0700 TMPDIR and `PATH=/usr/bin:/bin`.
2. **The stale discovery receipt is removed, in the run worktree only.** Then each reviewed blind mode runs exactly once:
   - discovery's `--held-out-blind`;
   - the companion's `--held-out-blind`, only if discovery's succeeded.

   For each, the lead sees only:
   - its one-line summary;
   - its exit code;
   - its stderr, which must be empty;
   - the receipt: ids, verdicts and per-mille margins.
3. **The ordinary modes:**
   - discovery's census, `--write` then `--check`;
   - the workspace ledger, `--check`. Its record binds no receipt, so it stays byte-equal;
   - the companion census, `--write` then `--check`.
4. **The recorded comparison** (`run.json`), against the expectations below.

## The expected bindings: every binding named (B3-b3b's lesson)

**The discovery receipt** has 8 top-level bindings. Against main `b753854`:

| Binding | Expected | Why |
| --- | --- | --- |
| `closure` | **changed, in exactly 2 of its 19 rows:** `crates/platform/src/work_ledger.rs` and `crates/security/src/custody/discovery_rule.rs` | C1a4's census-closure re-pin |
| `reference` | **changed, in exactly 1 of its 6 rows:** `tools/contracts/generator-closure.json` | D2b-0b (contract successor 175) regenerated the generator closure, which the reference-loading code pins |
| `tool` | **changed** | C1a4 re-pinned the two closure rows in `discovery_census.py`'s `CLOSURE` |
| `limits` | unchanged | discovery's caps are untouched |
| `manifest` | unchanged | |
| `memberModel` | unchanged | |
| `rootLengths` | unchanged | |
| `sizes` | unchanged | no size-inventory entry was added since B3-b3b's receipt |

The lead computed this by comparing the committed receipt's bindings with `receipt_bindings` over the inputs at `b753854`, which opens no store. This gate leaves `discovery_census.py` byte-unchanged, and the freeze holds main there, so the table holds at the run. D2b-0b touched none of the companion's bound snapshot sources or tools.

**The companion receipt** is new: all 7 of its bindings are new. They are:
- `discovery`: discovery's own receipt bindings, in full;
- `tools`: the companion tool, the model, discovery's tool and the member model;
- `snapshotSources`;
- `caps`;
- `item5`;
- `maxUnitDepth`;
- `afterWalk`.

## The expected comparison

- **The discovery receipt:**
  - its ids are the old receipt's ten, in order;
  - **every row is equal to the old receipt's row.** C1a4 changed no discovery charge: discovery's `classify_cost`, its walk and its caps are untouched, and (b-prime) is behaviour-preserving. Any difference is a finding;
  - its state stays `holds (blind census)`.
- **The discovery census record:**
  - the changed keys are `entries` (its ten held-out rows) and `heldOutMargin`, with `failingEntries` and `caps` changing only on a failure;
  - every lead-readable row and every workspace row is unchanged.
- **The companion receipt:** ten rows, one per held-out id, each measured, over item 5, or an error.
- **The companion census record:**
  - the changed keys are `heldOutEntries` and `heldOutMargin`, with `failing2x` and `capsStatus` changing only on a failure;
  - its lead-readable and workspace rows are unchanged.
- **The run worktree's changes** are exactly four files:
  - the two receipts, the companion's new;
  - the two census records.

## Outcomes

- **A blind run errors, a row is an error row, or stderr is non-empty.** Nothing is committed. The result goes to Codex and the owner as data, and the held-out margins stay outstanding.
- **Every row is measured or over item 5.** Codex's post-run review of the receipts and the composed records follows. Then:
  - the lead's assent;
  - a product commit of exactly the four files;
  - an inventory successor for the two new paths: the companion receipt and the gate's controls.
- **A companion margin under 2×.** The record shows `fails (blind census)` and `returned-to-law`, and by C1a plan r6 RF-3 step 4 the caps return to the law (an r9 successor). That is data, not a reason to rerun.
- **An over-item-5 held-out entry** claims no margin, as r9 states for lead-readable ones. It counts toward neither the maximum nor a failure.

**The expectation, not a claim.**
- Every lead-readable entry passes at 2^21, 2^24 and 2^33, with the smallest margins 3,960‰ objects, 11,274‰ edges and 39,040‰ bytes (`poly-large-rspack`). Five lead-readable entries are over item 5.
- The held-out set is ten entries, from small to large, for example a large Rust repository. Its sizes are not known to the lead, so no row's outcome is predicted.

## Not claimed

- No held-out content is opened or disclosed beyond the owner's allowlist: ids, verdicts and per-mille margins, and the over-item-5 verdict (LD-C1A4B-2).
- No new method, population or access beyond the companion's blind mode reviewed here.
- No second run.
