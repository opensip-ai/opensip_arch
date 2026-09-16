# source39.v3 — completion of the source39.v2 self-audit

**Standing**
- This is the same origin, `9d3dfb70-b2d3-498c-a3c1-f8de9e488514`, and a bounded completion continuation.
- Runtime source39.v2 stopped after reporting status: its final chain, checkpoints 4–11 and review were incomplete.
- This runtime started with an exact copy of v2's `output/` and the unchanged kit.
- A copied result is prior measured work. It is reused here only where the ledger below says so, and never counted as a v3 execution.
- Fresh-origin independence is not claimed anew.

## Inputs and custody

- **Read:**
  - `charter.md` and `requirements.json`, which equal v2's after runtime-path rebinding;
  - the kit;
  - own v2 `final-response.md` and the copied runtime logs;
  - own historical outputs.
- **Not read:** harness files beside the charter, LIVE, author sources/models/fixtures, root artifacts, other agents' work, private logs, the web.
- **Kit.** `consumer-input-manifest.json` SHA-256 is `c2f2f88d2e3bebfa8fa1b521cb76d2584483eb922973d6e555fe05a15da4ad80`, parent `f71a59928d1b6aa84eed81b8cb49fd1fba91c65dd6599c58f99efcdc42569009`.
  - All 104 members verify, with no unlisted files (`vectors/phase0-custody.json`, `logs/v3-p0.0.phase0_custody.log`).
  - Re-verified at the end in `runs/final-custody.json`.

## Preservation and path rebinding

1. `tools/v3_preserve_and_rebind.py`.
   - **Manifest.** `preserved/v2-copied-output.manifest.json` hashes all 1,365 files. Every file equals the same path in the read-only v2 runtime, except the one v3-authored tool present at manifest time.
   - **Copy.** Every non-store file (reports, logs, checkpoints, notes, helper code) was copied to `preserved/v2-copied-state/` before any v3 step rewrote it.
   - **Rebind.** The v2 root was replaced with the v3 root in 50 helper files, including `preserved/pre-hc33/` (`port-manifest-v3.json`: before and after SHA-256).
2. **Tool defect, recorded.** The rebind tool lives in `tools/`, so it rewrote its own `V2` constants after executing.
   - The executed bytes were restored from its pre-rebind copy, which is kept at `preserved/v3-authored/v3_preserve_and_rebind.executed.py`.
   - The port-manifest entry is annotated.
3. **Label edits** (deliberate, not bulk):
   - `vectors/phase0_custody.py`: runtime label, continuation text, and prior custody rows taken from the preserved v2 copy;
   - checkpoint tools p456/p7/p8/p9: log labels and what was measured where;
   - `tools/finalize_review.py`: runtime label, standing, limitations and advisories;
   - `tools/v1_v2_provenance.py`: scrubs the v3 label.
   - HC-33..HC-36 docstrings keep "source39.v2" because those corrections were made there.
4. **First v3 pass preserved.** `preserved/v3-pre-hc37/`: 82 files produced by the first v3 pass, before HC-37/HC-38.

## What the copied v2 state contained

**Complete, all after the last change to ref/builders** (`ref/retained_graph.py` HC-36, 02:52:50 in v2):
- store builds (`logs/v2-build2.*`);
- replay-all;
- tamper;
- pre/post matrix;
- phases 4–7;
- run termination;
- phase 8 envelopes and compare;
- graph query;
- from-scratch (`logs/v2-final-chain.1`);
- admission log (`logs/v2-final-chain.2`, 27 positives, 0 failures).

**Never executed in v2:**
- replay export (`logs/v2-final-chain.3` absent; no `runs/*.replay-export.json`);
- the final run-termination repeat;
- the retention-negatives rerun with the fixed remint (`vectors/retention-negatives.json` was the pre-fix attempt, `allPass` false);
- v1-v2 provenance;
- final custody;
- checkpoints 4–11;
- `notes/11`;
- both review files.

`requirement-status.json` had 26 executed, 105 unexecuted and 3 future-qualification rows.

## v3 execution sequence

1. **`v3-p0`: phase 0 custody.** PASS, 11 phase-0 IDs executed.
2. **`v3-final` (first v3 pass, preserved in `preserved/v3-pre-hc37/`).**
   - Replay export: 27/27 exported; fresh `close_run` ADMIT; retained closure ADMIT with reachable-set equality; C(proof) byte-equal.
   - Run termination: 28 Runs, 0 failures.
   - Retention negatives: 32/32 constructed and passing.
   - Provenance, and final custody PASS.
3. **Walker gaps found.** The first negatives pass showed two builder input mutations refused only by owner admission, while the independent walker admitted them:
   - `ts-pass~hidden-import`: plan `importIds` is `[]`, but the proof's evaluation inputs name `import2:68dec80d…`;
   - `rust-mixed~unit-id-not-derived`.

   These were corrected from the kit as **HC-37** (selected-import membership for by-domain import references) and **HC-38** (execute the published SourceUnitOwnershipV1 `unitId` derivation).
   - Fresh-process smoke check (`scratch/v3-hc37/`): the walker now refuses the first with `JOIN UNSELECTED_EVALUATION_IMPORT` and the second with `JOIN DERIVED_UNBOUND`.
   - `ts-pass` and `rust-mixed` still ADMIT with 0 faults.
4. **`v3-closure`.** Because the walker changed, every closure-dependent step was re-executed:
   - replay-all `--no-build`, from-scratch, tamper ×3;
   - replay export, admission log, retention negatives, pre/post matrix;
   - phase 5 vectors, phase 7 vectors, phase 8 envelopes, graph query, run termination;
   - provenance, final custody.

## Reuse ledger (v2 results not re-executed in v3)

Each row below was produced in v2 after the last modification of the code it uses (v2 runtime mtimes), and none of that code calls
`close_run`, so HC-37/HC-38 cannot affect it.

| Result | v2 log | Why reuse is exact |
|---|---|---|
| store bytes of all Runs and input mutations | `logs/v2-build2.*`, `logs/v2-replay-all.0` (builds) | evaluator/builders unchanged since HC-35 (02:42) |
| phases 1–3 vectors | `logs/v2-p0to3.*` | canonical/CVE1/protocol helpers unchanged since port |
| phase 4 tables, phase 6 vectors, prepared-mode vector | `logs/v2-p456.0`, `.2`, `logs/v2-disc-mode.1` | no `close_run` call (grep); code unchanged since 02:44 |
| discovery/membership vectors (s39-M1 measurement) | `logs/v2-disc-mode.0` | no closure; document equal to v1 |
| phase 8 compare | `logs/v2-final-chain.0` | `admit_graph` only; code unchanged since 02:44 |
| pre-correction self-check of v1 bytes | `selfcheck/pre-summary.json` | intentionally pre-correction code |
| reference census | `vectors/reference-census.json` | kit-only; re-run in v3 (`logs/v3-neg2.0`) only to add its `classification: explanatory` label |

## Final measured results (v3)

- **Custody.**
  - Phase 0 PASS (`logs/v3-p0.0`).
  - Final custody PASS (`logs/v3-closure.15`, `runs/final-custody.json`): manifest and parent as expected, 104 members, rows identical to phase 0.
  - The charter and requirements SHA-256 are recorded there.
- **Replay-all** (`logs/v3-closure.0`): 62 stores, all with results; 29 ADMIT and 33 REFUSE at owner graph admission. The retained closure refuses 10 of those 33; the other 23 are owner-semantic laws the walker delegates.
- **From-scratch** (`logs/v3-closure.1`): 27/27 claimed positives ADMIT through owner admission, retained closure, replay and reachable-set equality. The designed negative refuses.
- **Tamper** (`logs/v3-closure.2-4`): all constructed semantic controls are refused by replay after both earlier stages admit, and all identity controls refuse.
- **Replay export** (`logs/v3-closure.5`): 27/27. Each has a fresh `close_run` ADMIT and retained closure ADMIT, with reachable set equal. Proof, evidence, seal and Run are byte- or identity-equal, and all 520 witnesses are byte-equal.
- **Admission log** (`logs/v3-closure.6`): 27 positives, 0 failures.
- **Retention negatives** (`logs/v3-closure.7`, re-run with labels as `logs/v3-neg2.1`, identical outcomes): 32/32 constructed and passing. The builder rows `hidden-import` and `unit-id-not-derived` are now refused by the walker.
- **Pre/post matrix** (`logs/v3-closure.8`), counts of the 27 positives:
  - pre code: v1 bytes 27 ADMIT; v2 bytes 27 ADMIT;
  - post code: v1 bytes 26 REFUSE; v2 bytes 27 ADMIT;
  - identities unchanged; only subject descriptors added.
- **Phase vectors.**
  - Phase 5, phase 7 and phase 8 envelopes: 0 failures (`logs/v3-closure.9-11`).
  - Graph query: 53 vectors, 0 failures (`logs/v3-closure.12`).
  - Run termination: 28 Runs, 9 candidate checks, 30 compositions, 0 failures (`logs/v3-closure.13`).
- **Provenance** (`selfcheck/v1-v2-provenance.json`, `logs/v3-neg2.2`).
  - 56 re-executed report documents equal their v1 counterparts after removing process fields. They include phases 1–4 and 6–8 vectors, the s39-M1 discovery vector, envelopes, traces, graph query and run termination.
  - The closure reports differ because of the new stage fields, and 62 stores differ because of the added subject frames. `cmp-empty` is the one store that is equal.
- **Checkpoints.**
  - The first write of checkpoint 9 (`logs/v3-record.3`) marked R-NEGATIVE-FIRST-REFUSAL and R-VALID-VS-INVALID-VS-EXPLANATORY failed. The new negatives and census files lacked a top-level `firstRefusal` / `masksLater` and classification labels.
  - Both files were re-emitted with those fields (`preserved/v3-pre-labels/` keeps the earlier bytes), and checkpoint 9 was rewritten with no unexecuted or failed ID (`logs/v3-record2.0`).
