# Independent review — retained ordinary S4 proposal 301

**Standing:** bounded native-Rust review of frozen `native-ordinary-s4-checkpoint-301`. `prepare_clock_input` runs 299 retained-head then 297 authenticated times on one Budget; `evaluate_retained_ordinary` feeds those typed sources plus a **recorded** Anchor into unchanged `assess_kernel`. This does **not** adopt proposed 300 sampling, qualify an OS clock, persist a write-ahead, authenticate `timeEvidence` provenance, or dispatch roles. Installed product remains `fa72e50`. Keys are **TEST ONLY**. Prior 298–300 reports were not edited.

Python 3.12.13 `-I -B`. OpenSSL 3.6.3. Rust 1.95.0 `--offline --locked`. Review-local copies only. Frozen fixture/key/result directories were not overwritten. No workspace rerun (284's 529 is predecessor).

---

## Verification

Pins, tar bytes, member counts, and every `subject.json` hash matched **before** extract.

Frozen archive: **8748720 B, 926 members, SHA256 `b6db23ad9b2c9e73e1f42b2c7a949c6afdd577a7c8bc9ee18be5312d9e95906b`**. Standing: unselected private301 retained ordinary authentication to unchanged S4; provenance and publication pending. Extract rehashed **926/926**. Product-inputs **453/453**. Nested parent 299 pin `4ab31d19…e36e` equals reviewed 299. Nested 215 r14 `cd338af6…dd9c`, 225 r2 `84e48e36…c413`, 265 `73c3b3f5…86df`. Live 297 tar `f0d7c35d…45df` matches. Included `kernel201.py` SHA256 `df45c9c5…2299`. Product vs 299: **453** files, **449** unchanged. Changed: `trust.rs` `8d566f6c…098f` (private reexport of `OrdinaryClockInput` only), `trust/ordinary_targets.rs` `8e4ba22c…1c7c`, `trust_time.rs` `1b845612…34f1`. Added: `ordinary-s4301.ndjson`. `prepare_clock_input` / `evaluate_retained_ordinary` / `RecordedObservation` are not in `lib.rs`.

`assess_kernel` production text is **byte-identical** to 299 (5145 B). New `RecordedObservation` / `evaluate_retained_ordinary` wrap it; they do not retune DAY/HORIZON/calendar constants.

---

## What the composition does

Same Budget: 298 `capsule_clock` then 299 `bind_retained_head` (P2 only; P0/P1 `RetainedPhase`) then 297 `prepare_authenticated_times` using `head.authentication_context` with **fixed** `ChainBudget { max_links: 131072, max_stored_bytes: 268435456 }`. Fixture `linkLimit` is ignored at this boundary (deliberate): 297 `zero-link-budget-refuses-successor` therefore **proposes** here. Role/OLD/R contexts and revoked-key population remain **supplied** premises from the 297 fixture, not derived current authority.

`OrdinaryClockInput` is opaque: newest = authenticated manifest/catalog/list maximum; `root_issued` separate; list issue = `issued[2]`; catalog/root expiry from 296 projection. Callers cannot inject arbitrary time scalars into `evaluate_retained_ordinary`.

`RecordedObservation::admit` checks closed `{wall, mono, bootId}` (exactly 3 keys), calendar wall, nonnegative i64 mono, boot 1..=256 **Unicode characters**. No UUID grammar and no `observe_clock()`. Comment and code: not proposed 300.

S4 order in `assess_kernel` (unchanged): payload/root **future** (no-write `PayloadFuture`) → range representability → fresh/horizon → in-session continuity → beyond-horizon. Expired presented roots still **propose** floor writes (`same-head-expired`, `final-expired`, `expired-authentic-*`, `post-s4-expiry-still-proposes-floor`); later `states` mark expiry at `tEval` and do **not** clear `floor_write`. Future roots/manifests vs the **recorded** wall are `NoWrite` (`future-authentic-final-root`, `payload-future-no-write`, `root-future-distinct-from-newest`). Horizon/continuity refusals are `NoWrite`. Report-only sets `ReportOnly` and `NoWrite`. Poisoned floor / malformed continuity / boot-change cases still `NewRequired` when L would advance.

`ProofRetention`: `NoWrite` if no `floor_write`; `NewRequired` iff `last_write`; else `Keep` of the exact retained T **NodeRef**. That is a requirement, not a fabricated proof, receipt, or I/O. Observation admission failure does **not** latch the Budget (`failed=false` on 14 observation rows); metadata/head failures do.

99 cases from pinned 68 TEST-ONLY 297 fixtures by `authIndex`: **44** input-refused / **14** observation-refused / **41** proposals (**30** NewRequired / **4** Keep / **7** NoWrite). Same Budget both rounds: baseline 11/32/18839; repeat 11/64/18839; 11 captures. Test counts `[88, 28, 82]` = doubled outcomes.

**Executed:** `cargo clean -p opensip-security` then **247/247** with `Compiling opensip-security`. Workspace Clippy `-D warnings`, cargo fmt, rustfmt of **nine** include files. 12/12 r1 compiled controls core-equal frozen `mutation-check-r1` (live baseline cargo skipped). Frozen mutant dir not overwritten (`report.json` SHA256 `35a9a699…a1ca`). No compile-fail or production correction.

**12 compiled controls (all caught):** `omit-observation-closed-shape`; `boot-byte-count-instead-of-characters` (Unicode vs bytes); `omit-current-root-future-input` (`future-authentic-final-root` becomes `Advance` instead of `PayloadFuture`); `newest-from-root-only`; `revocation-time-from-newest`; `omit-presented-catalog-expiry`; `omit-presented-root-expiry`; `ignore-report-only`; `replace-proof-without-last-write`; `preserve-proof-despite-new-last`; `expiry-erases-write-ahead-requirement` (`expired-authentic-same-head` wrongly `NoWrite`); `substitute-observation-for-original-proof`.

---

## Combined reproduction table

| Kind | Result |
|---|---|
| 301 pins before extract | match |
| Nested 299 / 297 / 265 / kernel201 | match |
| `assess_kernel` vs 299 | byte-identical |
| Proposed 300 sampling | **not used** |
| Live `cargo test -p opensip-security` | **247/247** after force rebuild |
| Clippy / fmt / rustfmt 9 includes | pass |
| 301 r1 mutants | 12/12 frozen-equal |
| Workspace | not rerun (284 529 predecessor) |

---

## Remaining (do not count closed)

Recorded observation is not OS provenance; 300's 1 s/midpoint/public-mapping issues are out of this freeze. `timeEvidence` NodeRef is still not authenticated original-history proof. Role/OLD/revocation population, current/BEGIN, bootstrap/active-batch, durable write-ahead/receipt, post-S4 minima/completeness/role effects, full host/custody/fence/census/writers, source selection, and M3–M6 remain open. This adapter cannot dispatch a role or publish anything.

---

## Verdicts

- [x] **301:** archive/pins verified; 299 then 297 on one Budget with paired root/ref; recorded closed Anchor only (no 300 UUID/OS producer); S4 kernel unchanged; future/horizon/continuity no-write vs expired-root still proposes; ProofRetention is a requirement not a receipt; 12/12 mutants; 247/247, Clippy, fmt, 9-file rustfmt.
- [ ] **Not** OS qualification, current-head/history proof, durable S4 publication, host installation, completeness, grant, or product installation.
