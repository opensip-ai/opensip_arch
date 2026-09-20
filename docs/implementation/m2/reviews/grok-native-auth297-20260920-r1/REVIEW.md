# Independent review — pre-time root authentication 297

**Standing:** bounded native-Rust review of frozen `native-ordinary-auth-checkpoint-297` against the independent 296 `ORDERING.md` split. Distinct `RootChainAuthentication` authenticates without wall/evaluation; full `RootChainEvidence` still owns `ExpiredNoChain` / `FinalExpired` / `FinalFuture`. `prepare_authenticated_times` runs 294 scoped inventory then this auth phase, then the shared 296 source projection. This is not current-head admission, S4 write-ahead, durable clock proof, host admission, grant, or product installation. Installed product remains `fa72e50`. Keys are **TEST ONLY**. Archived 294/295/296 reports were not edited except the 296 TIME-PRODUCER hash-label correction (beforeimage preserved).

Python 3.12.13 `-I -B`. OpenSSL 3.6.3. Rust 1.95.0 `--offline --locked`. Review-local copies only. Frozen fixture/key/result directories were not overwritten. No workspace rerun (284's 529 is predecessor).

---

## Verification

Pins, tar bytes, member counts, and every `subject.json` hash matched **before** extract.

Frozen archive: **8676588 B, 964 members, SHA256 `f0d7c35de1c6752c1e024bd65e670fb954d0546b8a0bea274731de72dec945df`**. Standing: unselected private297 pre-time authentication; current context, S4 write-ahead and operational authority pending. Extract rehashed **964/964**. Product-inputs **450/450**. Nested parent 296 pin `7de5863c…cdfe` equals reviewed 296; live 296 trial tar matches. Nested 215 r14 `cd338af6…dd9c`, 225 r2 `84e48e36…c413` / `TIME-PRODUCER.md` `804134cd…0843`, 265 `73c3b3f5…86df` live-match. Product vs 296: **450** files, **446** unchanged. Changed: `trust.rs` `d1d09966…5d6c`, `trust_ordinary_roots.rs` `dbc1f8dd…bc37`, `trust/ordinary_targets.rs` `f7b911df…5016`. Added: `auth297.ndjson`. `prepare_authenticated_times`, `authenticate_shared`, `RootChainAuthentication`, and `AuthenticationProof` are not in `lib.rs`.

---

## Ordering against 296 `ORDERING.md`

The requested 297 plan matches the frozen source:

- Private `RootChainFacts` kernel owns reader, aggregate byte/link budget, accepted-version identity, `+1`/previous, nondecreasing issue, actual old/new quorums, and finite-union filters. `admit()` still refuses intrinsic `issuedAt >= expiresAt` (`Error::Expiry`) and unparseable calendars.
- Full `verify_root_chain` always passes `Some((evaluation, wall))`. Distinct `authenticate_root_chain` always passes `None`. The `Option` lives only on module-private `verify_chain_inner`. There is **no** conversion or accessor from `RootChainAuthentication` into `RootChainEvidence`.
- `AuthenticationContext` has no wall/evaluation fields. `authenticate_shared` / `prepare_authenticated_times` accept none.
- Full `prepare` still does admit_original → Full `Q::prepare` → kernel. `verify_shared` / `authenticate_shared` take already-constructed typed `SharedEvidence` and only admit_original then kernel. The 295 `prepare_rooted` / 297 `prepare_authenticated_times` wrappers build scoped/shared proof first, then original capture. Historical envelope remains SHA+length only.
- 296 `prepare_times` still uses `prepare_rooted` (eval/wall). New `prepare_authenticated_times` is 294 `prepare_scoped` then `authenticate_shared` then the same `project_times` helper (three-source max excludes root; presented root is closure last).
- Eval-expiry and `FinalFuture` stay out of the pre-time type. Reintroducing clocks on `authenticate_root_chain` over-refuses `expired-authentic-same-head` with `ExpiredNoChain` (other-first). Stripping clocks from the full wrapper wrongly admits eval-expiry cases.

This closes the **pre-time expiry/future split only**. S4 future/range/horizon, write-ahead, and `tEval` root/list validity remain unimplemented.

---

## What the tests show

68 TEST-ONLY signed cases, **28/28** positives. Every case also runs untouched `prepare_times` on its own Budget with original wall/evaluation. Asserted **7** auth-success / full-refusal pairs: `same-head-expired`, `final-expired`, `future-successor`, `clock-inputs-are-not-authentication-inputs`, `expired-authentic-same-head`, `expired-authentic-final-root`, `future-authentic-final-root`. `future-authentic-same-head` authenticates and the full empty-chain path also succeeds (no `FinalFuture` on same-head); S4's presented-root future guard remains mandatory. Intrinsic `intrinsic-intermediate-interval-invalid`, `intrinsic-intermediate-calendar-invalid`, and `expired-and-invalid-signature-still-refuses` still fail both phases. Direct `authenticate_root_chain` checks: unsupported reader, accepted-version mismatch, anchor byte budget. Baseline 11/30/18839; repeat 11/60/18839; 11 captures.

Oracle: new AST projection of exact 265 `verify_root_chain` (`phase-projection.json`). Removed **exactly five** clock-dependent nodes (two input timestamp conversions; `ROOT.EXPIRED_NO_CHAIN`, `ROOT.FINAL_EXPIRED`, `ROOT.FINAL_FUTURE`). Passes `None` clocks; does not invent favorable times. Not an unchanged full-chain oracle. Separate full comparator uses an untouched model instance. 294/215 r14 scope and 225 r2 producer remain.

**Preserved authoring (production algorithm unchanged except documented Clippy style):**

1. `author-r1.log`: trailing blank line failed exact suffix assertion before writing `ordinary_targets.rs`; helper beforeimage retained; resume that phase only.
2. Clippy-r1: two `collapsible_if` on the time-gated expiry/future blocks; `trust-before-clippy-collapse.rs` retained. Collapse is control-flow style; predicates unchanged. Final Clippy-r3 passes.
3. Mutant r1: three filter-removal variants did not compile (`SignatureEvidence` ≠ `QuorumReport`). Retained. r2 uses `filter_revoked(..., &BTreeSet::new())` / `filter_envelope_revoked(..., &BTreeSet::new())` only; production unchanged.

**Executed:** `cargo clean -p opensip-security` then **244/244** with `Compiling opensip-security`. Workspace Clippy `-D warnings`, cargo fmt, rustfmt of **nine** include files. r1 16 variants + baseline and r2 3 compiled filters core-equal frozen `mutation-check-r1` / `mutation-check-r2` (live baseline cargo skipped). Frozen mutant dirs not overwritten (`report.json` SHA256 `1a38ce96…2bfe` / `ca151805…cb1d`).

**16 compiled controls: 10 wrong conditional admissions** — `remove-existing-full-time-guards`; `omit-chain-gap`; `omit-chain-backdated`; `omit-old-root-threshold`; `omit-new-root-threshold`; r2 `omit-successor-old-key-filter` / `omit-successor-new-key-filter` / `omit-presented-first-key-filter`; `omit-presented-first-threshold`; `calendar-failure-becomes-zero`. **6 other-first** — `reintroduce-authentication-clock-guard`; `omit-anchor-reader`; `omit-anchor-budget`; `omit-accepted-version`; `project-original-ref-after-rotation`; `auth-time-failure-not-latched`. r1 three filter omissions remain compile-fail, not counted as detections.

---

## Combined reproduction table

| Kind | Result |
|---|---|
| 297 pins before extract | match |
| Nested 296 / 215 r14 / 225 r2 / 265 live tars | match |
| Full 289/295 `prepare` / `verify_shared` | retained |
| Auth path wall/eval inputs | none |
| Live `cargo test -p opensip-security` | **244/244** after force rebuild |
| Clippy / fmt / rustfmt 9 includes | pass |
| 297 r1+r2 mutants | 16 compiled frozen-equal; 10 wrong / 6 other; 3 r1 compile-fail preserved |
| Workspace | not rerun (284 529 predecessor) |

---

## Remaining (do not count closed)

S4 observation, future/range/horizon, write-ahead and original time-evidence codecs; `tEval` root/list validity, anti-rollback, minima, completeness, role-record effects; current vs BEGIN/OLD/history/population; bootstrap; active-batch head barrier; full host admission; custody/fence/census/writers; source selection; M3–M6. 297 is a distinct pre-time authentication type plus 296 candidate projection, not complete ordinary import or cumulative approval.

---

## Verdicts

- [x] **297:** archive/pins verified; private kernel split matches 296 ORDERING (eval-expiry/`FinalFuture` only on the full wrapper; no wall/eval on auth; no conversion); 7 auth-success/full-refusal pairs; intrinsic interval/calendar/bad-sig still refuse; 296 projection reused after auth; 10/6 mutant classification with r1 compile-fails preserved; 244/244, Clippy, fmt, 9-file rustfmt.
- [ ] **Not** S4 write-ahead, current-head/BEGIN proof, host installation, completeness, grant, or product installation.
