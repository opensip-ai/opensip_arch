# Independent review — frozen checkpoint 221 (policy-checked marker capture)

Reviewer: Claude (independent; root/Codex is implementation and decision owner). Date 2026-09-19.
Scope: **only** the frozen 221 bytes — `crates/storage/src/store_root.rs` and its evidence. No cumulative, current-authority, OS, target, release or inventory approval. My ordinary-import assistance is unrelated and confers nothing here. No frozen/selected/product file was edited; nothing installed, committed, pushed or delegated; nothing deleted (fresh uniquely named scratch dirs, asserted absent).

## 1. Identity (all recomputed by me)
| Item | Value |
|---|---|
| `subject.tar.xz` | SHA-256 `a160d166d59d8e71465336317c049498148cc38e74637f06ebd8eab742c82dc7`, 4,259,036 bytes — equals request and `archive-pin.json` |
| members | 628, every one hashed **from the tar before extraction** against `subject.json`; 0 non-regular, 0 unsafe paths, 0 mismatches, 0 extras; end-of-review pass `mode: re-verified` |
| `subject.json` / `archive-pin.json` / `README.md` | `2ca45ec8…4eb5e75` / `aa734a52…e3ec230` / `f777fb08…6fa0c96` (full values: `claude-out/pin-verification.json`) |
| product pins | 356 rows; 355 files present and matching; **1 pinned file absent from the archive — finding E-1** |
| exact parent | `parent220/{subject.json,archive-pin.json}` = `b68446d9…c8b7e` / `d7b69e4f…d702a` — byte-equal to the manifest/pin of **my own verified 220 extraction** and to the repo trial copy. Path set equal to 220; against my 220 *bytes* exactly one file differs: `crates/storage/src/store_root.rs` (`db75566f…edf9f`) |
| author patch | `author-final.patch` applied to my 220 bytes reproduces `db75566f…` exactly |
| `reference201` pins | equal to the repo trial copies |
| fixtures | `fixture-provenance.json`: 0 mismatches |
| host receipt 133 | 236 sources, all equal to product pins (the changed file bound at `db75566f…`); 51 deps; 8 commands exit 0; 469 tests recounted from `tests.stdout`; source/lock unchanged; HOME absent |

## 2. What changed (complete file read; 659 lines)
- Production: `observe_marker(root, expected, invoking_uid, authorized_groups)` makes **one** call to `opensip_security::observe_bound_operational_file_with_policy` (directories → read → directories → file sample → directories; reviewed in 210/213/216) and only then runs the unchanged pure decoder on a copy of the ≤128 captured bytes. Result is three-way: `Absent` / `Present{marker, capture}` / `Unavailable(Capture(e) | Marker(e))`. The original `PolicyObservedOperationalFile` (File + bytes + descriptor sample) is retained whole.
- The previous unchecked reader is renamed `observe_unchecked_marker`; it, `CapturedMarker`, `MarkerReadFailure`, `MarkerObservation` and the `opensip_security` read-failure import are `#[cfg(test)]`.
- Decoder, `StoreInstance`, constants: byte-unchanged (diff hunks touch nothing in lines 7–66 besides the cfg'd import).
- Tests: two new macOS tests plus the test-only retry helper `observe_marker_fixture`.
- Doc comments state the limits accurately: sample is after the read; directory samples checked not retained; UID/groups/expected `S` are assertions; nothing is created, repaired or retried.

## 3. Findings

### E-1 (Medium — evidence/freeze defect, **not** a product defect): one pinned product file is missing from the frozen archive
`product-inputs.json` pins 356 files, but the archive carries 355 under `product/`. Missing: `tools/typescript-boundary/tests/fixtures/product/design-lock.json`. Cause, in `scripts/freeze_marker221.py`: the evidence walk prunes `d=='product' and rel.parts` to skip scratch product copies inside `mutation-check-*`/`diagnostic-*`; the same rule prunes this legitimately nested directory **named** `product` inside the real product tree. The freeze script's own pin assertions run against the live tree before the walk, and its post-write check compares the tar only to the rows produced by the same walk, so nothing noticed. 220's archive had all 356.
Consequences: (a) the README/request statement that pinned inputs "and archive members are independently rehashed" holds for 355 of 356 pins; the 356th is verifiable from this archive only by hash reference. (b) the 221 archive is not a self-contained product tree. It does not affect this review's subject: the pin for that file equals 220's, my verified 220 bytes match it (`absentFileMatchesMy220Bytes: true`), it is not among the 236 host sources, and cargo needs it for nothing — all my builds used the archive bytes exactly as frozen, without supplementing it. Do not alter frozen 221; fix the walk in the successor (prune by exact scratch paths, and assert `{product/<pin>} ⊆ archive members`). Evidence: `claude-out/pins-and-parent.json`.

### T-1 (Low): the capture bound passed by the production composition is pinned only from above
Owner mutant `read-bound-widened` (1024) is killed by the 129-byte case. My mutants `m2` (`MARKER_LIMIT - 1`) and `m3` (`72`) **survive all owner tests**: no test sends a 73..128-byte file through `observe_marker`, so the boundary between `Capture(Read(Bound))` and `Marker(NonCanonical)` is unpinned at the composition (the pure decoder's 127/128 cases never reach it). Both outcomes are `Unavailable`, so this is typed-cause fidelity, not admission. My probe `p4` (128 padded bytes → `Marker(NonCanonical)`, 129 → `Read(Bound)`) kills both. `m4` (71) is killed by the owner tests. Evidence: `io/mutation221-report.json`, `io/survivors-vs-my-probes.json`.

### T-2 (Informational, structural): "retains the exact capture" is not distinguishable by test from "bytes of one capture, descriptor of another"
My `m5` performs a second policy capture, decodes the *second's* bytes and retains the *first* capture; it **survives**. With a quiescent fixture both captures are the same inode and bytes, so no deterministic black-box test can separate them; only an injection seam could. I am not asking for one: the property is visible by inspection (one call, `capture` moved into the result, decoder given `capture.captured().bytes()`), and the owner's offset/inode test does pin that the retained File is the read descriptor and not a reopen-by-name. Recorded so the mutation table is not over-read.

No High findings. No production defect found.

## 4. Requested confirmations
**Retry cannot mask other errors — confirmed.** `observe_marker_fixture` loops only on the fully spelled `Unavailable(Capture(Directory(Descriptor(ChangedDuringRead))))`; every other value returns at once and exhaustion panics — it can never turn a refusal into success or absence. Widening it is self-revealing: my `m6` (any `Directory(_)`) and `m7` (any `Unavailable(_)`) are both **killed**, by the helper's exhaustion panic at the first expected refusal (`ForeignOwner`). `File(Descriptor(ChangedDuringRead))` is not retried. Production `observe_marker` contains no loop. What the retry does hide, by design, is a *spurious intermittent* `ChangedDuringRead`; that is the disclosed cause, which I reproduced independently: on a quiet fixture 2000/2000 single attempts were `Present` (`p6`); with one thread creating/removing a **sibling** in the shared account temp directory, 113/2000 single attempts returned exactly that cause and **0** returned anything else — never `Absent`, never another error (`p7`). The mechanism is `DescriptorMetadata` equality across before/during/after including directory `modified`/`changed` times. Observation for the future host owner, not a 221 finding: production is fail-closed single-attempt, so a store root whose ancestors are busy directories will see transient `Unavailable`; whoever consumes this must own that policy rather than treat it as absence or corruption.

**cfg separation — confirmed.** A non-test function referencing `observe_unchecked_marker` fails `cargo check --lib` with `E0425 cannot find function` (the `cargo test --no-run` build fails the same way in its non-test lib unit). Workspace clippy `--all-targets -D warnings` is clean, so nothing test-only leaks into a non-test item. `observe_marker` itself still has no production caller (`#[allow(dead_code)]` on the module): 221 is groundwork, as the README says.

**Causes / composition — confirmed by independent probes through `observe_marker`** (`probes/claude_probes.rs`, 7 tests, all pass on frozen bytes): symlink, dangling symlink, directory and FIFO leaves → `Capture(Read(_))`, never `Absent`/`Present`, no hang; renamed root (missing, then replaced by a directory holding a *valid* marker) → `Capture(Directory(NameChanged))`; invalid bytes **and** mode 0602 → `Capture(File(OthersWrite))` while the same bytes at 0600 → `Marker(Decode)` — policy precedes the decoder; hard link → `HardLinked`, then `Present` once removed; a valid marker under an others-writable **ancestor** → `Directory(Predicate{OthersWrite})`; exact 128/129/empty causes.

**Mutation evidence — sound.** The six owner mutants compile and each dies at a semantic assertion line (561, 591, 585, 598, 550/633, 557/633), none at the retry panic (517) and none by compile error. The baseline hash in `report.json` equals the frozen source. The retained r1 baseline failure (line 519, first `Absent` assertion) is presented as a failure, not a kill; diagnostic-r1 (round 29) and -r2 (round 64, with the one-line `eprintln!` patch) are consistent with the stated cause. My nine: 5 killed, 3 survived (T-1 ×2, T-2), 0 compile failures, baseline passes; source restored from frozen bytes and re-hashed.

**Owner re-runs (fresh scratch, archive bytes, `--offline --locked`, dedicated target):** storage 94/94; workspace clippy clean; `store_root` tests with HOME and TMPDIR unset 7/7.

**Sensitive data.** Owner test/diagnostic/mutation logs: 0 files containing home or per-user temp paths. Three archive files mention home-prefixed paths; all three are unchanged from 220 (two product files, one host script) and none is test output. My archived logs: 0 (per-user temp paths redacted at capture).

## 5. Closure of earlier items
- 202 W-1 (reader returned bytes without descriptor): closed earlier; 221 further retains the whole policy capture in production.
- 202 W-2 (marker leaf duplicated): the new tests spell `"store-instance.v1"` literally on purpose (independent of the constant); `wrong-fixed-leaf` is killed. Fine.
- 216 W-1 (`account_temporary_directory` may create): used only in test setup and commented so.

## 6. Limits
macOS only; no Linux compile or run. No ABA/continuous custody, lease or admission claim exists or was tested. `p7` rates are one machine, one run. I did not re-run host isolation 133 or the full workspace tests; I verified its receipt bindings. I did not review inventory v52 here (proposed, not selected).

## 7. Verdict (bounded)
**The frozen 221 source change is correct within its stated scope: no product finding; the test-only retry is exact and cannot mask other errors.** One evidence defect to fix in the successor's freeze tooling (**E-1**, archive omits one pinned, unchanged file), one low test gap (**T-1**), one structural note (**T-2**). Nothing beyond these bytes is approved.
