# Independent review — retained head binding 299

**Standing:** bounded native-Rust review of frozen `native-retained-head-checkpoint-299`. Private `bind_retained_head` takes a 298 `CapsuleClock`, requires retained phase, and binds `heads.root` document/admission to the exact historical root body. This is not current-head proof, historical admission replay, timeEvidence authentication, S4 write-ahead, grant, custody, or product installation. Installed product remains `fa72e50`. Keys are **TEST ONLY**. Archived 294–297 reports were not edited. 298 REVIEW `timeEvidence` type label was corrected separately (beforeimage preserved). Independent 298 `CLOCK-OBSERVATION.md` remains a separate missing-latency note, not 299 scope.

Python 3.12.13 `-I -B`. OpenSSL 3.6.3. Rust 1.95.0 `--offline --locked`. Review-local copies only. Frozen fixture/key/result directories were not overwritten. No workspace rerun (284's 529 is predecessor).

---

## Verification

Pins, tar bytes, member counts, and every `subject.json` hash matched **before** extract.

Frozen archive: **8634200 B, 904 members, SHA256 `4ab31d194d808e346ee9882c090c50e121b887fa25b3bb4c3c4ead16f133e36e`**. Standing: unselected private299 retained root and clock binding; historical/current authority pending. Extract rehashed **904/904**. Product-inputs **452/452**. Nested parent 298 pin `23a84b23…f835` equals reviewed 298; live 298 trial tar matches. Nested 215 r14 `cd338af6…dd9c`. Nested 265 `73c3b3f5…86df`. Live 279 tar `8b081b4f…4e9d` matches. Product vs 298: **452** files, **449** unchanged. Changed: `trust.rs` `d941cff6…361f` (only `binding_matches` visibility `fn` → `pub(super)`; predicate unchanged), `trust_ordinary_roots.rs` `e33af48a…81b7`. Added: `retained-head299.ndjson`. `bind_retained_head` / `RetainedHead` are not in `lib.rs`.

---

## What `bind_retained_head` does

Same Budget, after 298 `capsule_clock`: require `Phase::Retained` (P0/P1 refuse `RetainedPhase`; bootstrap remains separate). Derive `heads.root.document` (DocRef) and `heads.root.admission` (NodeRef) from that capsule. Capture historical body **and** envelope by SHA256 **and** length. Admit the root body (schema/calendar/interval). Reuse existing recovery `binding_matches` on `rootSchema` / `rootVersion` / domain `rootDigest` (not raw SHA). Join `root.expiresAt` to the retained clock projection's `rootExpiresAt`. Root version is already counter-joined by 279.

Historical envelope is integrity-bound opaque bytes. It is **not** reauthenticated under today's keys; opaque/unsigned historical envelopes can still yield this structural view (`historical-envelope-opaque`, `historical-envelope-not-current-authenticated`). Original history admission remains a later owner. Expired historical roots are retained (`valid-expired-root-remains-historical`); no eval-future/expiry decision here.

`RetainedHead` owns the `CapsuleClock`, raw body/envelope, validated root, document DocRef, and admission NodeRef. `authentication_context` borrows that paired root/ref and accepts only `ChainBudget` — no caller-supplied contradictory root/ref, and no wall/evaluation. That is a conditional 297 context, not proof the capsule is current or its history is admitted. Admission NodeRef presence is not target availability (`unavailable-admission-ref-remains-reference`).

34 differential cases, **7/7** positives. Baseline 2 objects / 2 edges / 8736 B; repeat 2/4/8736; 2 captures. Raw whitespace retained while RootBinding uses metadata domain digest (`raw-body-whitespace-not-domain-digest`; `body-sha-is-not-root-binding` refuses). Oracle: 227 r9 capsule joins / full 125 schema, 265 clock/root body and domain digest, existing Budget. Owned facts and exact context getters survive input drop; failure latches Budget.

**Executed:** `cargo clean -p opensip-security` then **246/246** with `Compiling opensip-security`. Workspace Clippy `-D warnings`, cargo fmt, rustfmt of **nine** include files. 9/9 r1 compiled controls core-equal frozen `mutation-check-r1` (live baseline cargo skipped). Frozen mutant dir not overwritten (`report.json` SHA256 `86c53941…b209`). No compile-fail or production correction on 299.

**9 compiled controls: 2 wrong conditional admissions** — `omit-root-binding` (`binding-rootSchema`); `omit-retained-root-expiry-join`. **7 other-first** — `omit-retained-phase` (unwrap on P0 missing heads); `omit-historical-envelope-capture`; `reauthenticate-historical-envelope` (over-refuses opaque historical env with `Envelope`); `substitute-admission-ref-for-document`; `lose-original-root-body-by-reencoding`; `derive-context-from-admission-ref`; `head-binding-failure-not-latched`.

---

## Combined reproduction table

| Kind | Result |
|---|---|
| 299 pins before extract | match |
| Nested 298 / 265 / live 279 tars | match |
| `binding_matches` predicate | unchanged; visibility only |
| Live `cargo test -p opensip-security` | **246/246** after force rebuild |
| Clippy / fmt / rustfmt 9 includes | pass |
| 299 r1 mutants | 9/9 frozen-equal; 2 wrong / 7 other |
| Workspace | not rerun (284 529 predecessor) |

---

## Remaining (do not count closed)

This reduces contradictory supplied 297 root/ref pairs. It does **not** authenticate or select the current capsule, history, or admission target. S4 composition, qualified OS observation, durable write-ahead, post-S4 guards, current/BEGIN/OLD/history/population, active-batch barrier, bootstrap, full host, custody/fence/census/writers, source selection, and M3–M6 remain open. 298 `CLOCK-OBSERVATION.md` still records missing sample-latency/rounding/midpoint law; that is not 299 scope.

---

## Verdicts

- [x] **299:** archive/pins verified; retained-phase only; SHA+len body/envelope; RootBinding + expiry join; historical envelope not reauthenticated; `authentication_context` borrows paired document/root and only `ChainBudget`; 2/7 mutant classification; 246/246, Clippy, fmt, 9-file rustfmt.
- [ ] **Not** current-head proof, historical admission, S4 write-ahead, host installation, completeness, grant, or product installation.
