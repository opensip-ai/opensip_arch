I've made all three corrections in the new v2 runtime. Root's three probe cases now refuse or route correctly, the two affected validators pass, and 7 controls that each disable one change fail exactly as intended. This is not acceptance of integrated bytes; all 54 recovery cases (F00–F53) are still not executed.

**1. Execution-plan binding.** Your finding reproduced on the v1 model. The Run record has no execution plan of its own: it comes from the evaluation seal, and `close_run` already ties that plan to the proof and the Run's `planId`. The composition now refuses three mismatches:
- an attempt whose `executionPlanId` isn't that plan (`RUN_TERMINATION_ATTEMPT_EXECUTION_PLAN_MISMATCH`);
- a `stageCount` that isn't the plan's number of stages (`RUN_TERMINATION_ATTEMPT_STAGE_COUNT_MISMATCH`);
- stage progress outside the plan: `stagesCompleted` above `stageCount`, or a `firstFailedStage` that isn't one of its stages (`RUN_TERMINATION_ATTEMPT_STAGE_PROGRESS_MISMATCH`).

It does not require `stagesCompleted` to equal `stageCount`. Completion is runtime progress that no retained record re-derives, and a scheduled stage isn't a completed one. It also doesn't decide whether a completed attempt may carry `firstFailedStage`; both stay with the host attempt owner (workflows §1). The fixtures now use each Run's real plan and stage count. A wrong-plan case that is otherwise admitted refuses, and a partial-progress case is admitted.

**2. Receipt inventory.** Nothing on the composition path already checks this:
- the commit path (`EvidenceStore.commit`) only mints the digest;
- read-only recovery only joins receipt to association.

The composition now requires `receipt.inventoryDigest` to equal `commit_inventory(runId, objects, blobs)` over the Run content it reads (`RUN_TERMINATION_RECEIPT_INVENTORY_MISMATCH`). This assumes that content is the Run's published inventory, not a wider shared store; a wider store fails closed. Namespace, sequence, signer and assurance stay with receipt admission; nothing is authenticated.

All committed-case receipts are now minted by the real reference commit path, and their digest matched `commit_inventory` on two Runs. Controls:
- the minted receipt is admitted;
- your `f*64` digest refuses;
- a digest of the inventory with one published object missing refuses.

**3. Absent carrier on read-only recovery.** When an association names the bound carrier but SQLite holds neither `grant_journal` nor any format 3 object, the result is now the existing `unknown-custody` route (exit 4, `HOST.IO_FAILURE`/`host-io`, no detail). It is never absence, not-committed or success, and the reader never creates or initializes a carrier.
- **Precedence:** `binding-unusable` first, then the format 3 footprint and stability rules, then unmigrated format 1/2 (F46), then this case.
- **Totality:** every dispatch result except `carrierFormat3` now has exactly one read-only standing.
- **Where:** read-only §1 precedence row 4 and the Step 3 sentence, carrier-format §8.1, the S12 unreadable-carrier row, and the dispatch map, route, reader law and phase law.
- **Writer path:** writer fresh-install stays its separate owner.

The controls use real SQLite:
- empty and fallback databases;
- a surviving witness naming either project;
- a binding mismatch;
- a read-only open of a missing file (creates nothing) and of an empty file (bytes unchanged);
- an interrupted fresh install that stays busy.

**Results**

| Check | v1 | v2 |
|---|---|---|
| Semantic replay | 31/31 rows, 37 composition cases | 31/31 rows, 44 composition cases, 0 faults |
| Carrier validator | 384/0 | 406/0 |

Discrimination controls:
- restoring the v1 model fails exactly the 6 new join cases, which reproduces your finding;
- disabling each new join fails exactly its own cases;
- restoring the v1 dispatch JSON fails exactly the 9 absent-carrier checks (391/9);
- restoring the v1 prose fails exactly 2 checks (404/2).

**Diffs**

| Diff | File | SHA-256 | Size |
|---|---|---|---|
| Total vs source38 | `total-edits-vs-source38.diff` | `beaa92e4b9b6e86c43ca088a91f008aa58e54f40b4ba49834576836214cefb4a` | 10 files, 1257 lines |
| Incremental v1 → v2 | `incremental-v1-to-v2.diff` | `870bc958db978852570cd3b25faedb8c854ad754931ce01047e86cd9d0c4c3d4` | 9 files, 534 lines |

`workflows-and-surfaces.md` is unchanged from v1. Full source38/v1/v2 hash maps are in `review.json`. Custody holds: source38, v1 and your assessment are unchanged, and the working copy is regular files.

**Failed attempts, kept**
- My first v2 validator run exited 1 (carrier 405/1). The new totality check wrongly counted the string `'gj_seq_contiguous'`, a condition inside the dispatch function, as a result. It was a checker bug, not a law error; I fixed it to read only returned values and the rerun passes.
- Two looped background launches of the discrimination runs were denied before they started, so each ran individually.

**Binding drift for you to rebind:**
- five source-pin ledgers pin all 10 touched files;
- coverage, normative-inputs and planning-sources pin 6 of them;
- planning sections `security-and-lifecycle:12` and `workflows-and-surfaces:10` changed text, and `workflows-and-surfaces:11`–`13` shift by 4 lines.

I ran only the two affected validators and their controls: no global groups, planning checker or whole-manifest rescan. All commands have finished.

Everything is in `/tmp/opensip-design-corrections/claude-source38-advisory-author.v2`:
- `review.md`
- `review.json`
- `total-edits-vs-source38.diff`
- `incremental-v1-to-v2.diff`
