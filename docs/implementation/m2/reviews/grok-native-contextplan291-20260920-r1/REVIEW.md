# Independent review — context-to-plan composition 291

**Standing:** bounded native-Rust review of frozen `native-context-planning-checkpoint-291`. Private `plan_from_contexts` derives 287 planner inputs from 290 `Evidence` plus retained-state/OLD-hit premises. It does **not** prove current vs BEGIN provenance, authenticate population/history, grant trust, or implement the T1 DR-103/DR-112 gate. Installed product remains `fa72e50`. Keys are **TEST ONLY**. Archived 290 and `INERT-ROUTING.md` were not edited. A separate planning note is in `INERT-IDENTITY.md`; it is **not** this bounded verdict.

Python 3.12.13 `-I -B`. OpenSSL 3.6.3. Rust 1.95.0 `--offline --locked`. Review-local copies only. Frozen fixture/key/result directories were not overwritten. No workspace rerun (284's 529 is predecessor).

---

## Verification

Pins, tar bytes, member counts, and every `subject.json` hash matched **before** extract.

Frozen archive: **6109896 B, 526 members, SHA256 `36147214715a344241ac70ca72981fa9221a11b52bd5f5ae54053410b22c818c`**. Standing: unselected private291 conditional context-to-plan derivation, no authority. Extract rehashed **526/526**. Product-inputs **441/441**. Nested parent 290 pin `f3012512…9b80` equals reviewed 290; live 290 trial tar matches. Nested 215 r14 `cd338af6…dd9c` / model SHA `9aa6e56b…d701` (27474 B) match. Nested 265 live tar `73c3b3f5…86df` matches. Frozen OWNER `d8165f14…19fa` (48217 B) differs from live `/tmp/opensip-implementation/m2-trust-owner-draft-215/OWNER.md` `780a6dd5…0d60` (50337 B); frozen OWNER is source, live untouched.

Product vs 290: **441** files, **436** unchanged. Changed: `trust.rs` `d0c63bba…040b` (include relocation), `role_machine.rs` `481b1eb5…47b9` (`State` `pub(super)`, ordinary_targets include removed), `ordinary_targets.rs` `e4a35a36…a6cd`. Added: `context291.ndjson`, `context291-roots.ndjson`. `trust_role_availability.rs` byte-identical to 290 (`bdec1efd…78df`). 287 `targets287.ndjson` and 288 `completion288.ndjson` byte-identical to reviewed 288. `plan()` + `coordinate()` production prefix is **byte-identical** to 288. Not in `lib.rs`.

`ordinary_targets` include moved from `role_machine` to `root_payload` (`include!("trust/ordinary_targets.rs")` with `use super::super::role_machine::State`). Same `State` enum; visibility widened only to the private trust parent.

---

## What `plan_from_contexts` does

Inputs: six retained `{state, established, recovery_revoked}` premises, OLD-subject hits, one outside 290 `Evidence`, and optional per-role recovery `Evidence`. **No** caller `active`/`below` flags. Non-RECOVERY roles use outside; RECOVERY requires a supplied context (`MissingRecoveryRoot`); extra recovery context on a non-RECOVERY role refuses (`UnexpectedRecoveryRoot`); RECOVERY whose selected role is `Absent` refuses (`InactiveRecoveryRoot`) rather than fabricating an active BEGIN. Then `active = keys.is_some()`, `below_threshold` from that role's 290 `below_threshold()` (`None` → false), and the **unchanged** 287 `plan`. Owned `Source` records which root digest and optional `(available keys, threshold)` were used after all typed contexts drop.

290 `derive` remains a full-document shape/identity factory plus supplied revocations, **not** current-head authority. Exact current/BEGIN relationship and population/OLD/restriction provenance stay external. 277 restriction joins are not invoked here.

1284 cases, 938 distinct root/population contexts: 1128 valid, 156 invalid. Oracle: 265 primary `root_keys_for_role` / `role_threshold` on the **source context roots**, then 215 r14 `ordinary()` traced at line 53 — not 290 expected-output fields and not a copied native formula. Tests compare T0/T1, tentative roles, ordered trace, and source identity/keys after drop. Inherited 3040 planner and 4768 completeness tests still run.

**4MiB framing (inspected):** initial test parsed the grouped 938-root fixture as one product JSON value and hit `ByteLimit` (`security-initial-r1`: 236 passed, 1 failed unwrap `Err(ByteLimit)`). Fixture changed to independent NDJSON rows; production 4MiB limit and planner algorithm unchanged. `context291-roots-before-row-framing.json` (7515461 B), `contextplan291_tests-before-row-framing.rs`, and the failed log are retained.

**Executed:** `cargo clean -p opensip-security` then **237/237** with `Compiling opensip-security` (includes 287, 288, and 291 tests). Workspace Clippy `-D warnings`, cargo fmt, rustfmt of **nine** include files. 13/13 r1 compiled controls core-equal frozen `mutation-check-r1` (live baseline cargo skipped; unpatched source SHA matched frozen baseline `e4a35a36…a6cd`). Frozen mutant dir not overwritten.

**Controls (7 invalid-context acceptance):** `missing-recovery-uses-outside`, `recovery-always-uses-outside`, `ignore-unexpected-recovery-context`, `allow-inactive-recovery-context`, `use-bundle-availability-for-all`, `forget-recovery-protection` (MissingRecoveryEvidence becomes Ok), `fabricate-established-history`. **6 other-first** (wrong derived T0/T1/source facts, still valid contexts): `all-roles-active`, `ignore-derived-key-loss`, `ignore-old-subject-hits`, `lose-source-identity`, `mislabel-recovery-root`, `lose-source-key-facts`. Not operational exploits.

---

## Combined reproduction table

| Kind | Result |
|---|---|
| 291 pins before extract | match |
| Nested 290 / 215 r14 / 265 live tars | match |
| 287/288 algorithms and fixtures | unchanged vs reviewed 288 |
| Live `cargo test -p opensip-security` | **237/237** after force rebuild |
| Clippy / fmt / rustfmt 9 includes | pass |
| 291 r1 mutants | 13/13 frozen-equal; 7 invalid-context / 6 other |
| Workspace | not rerun (284 529 predecessor) |

---

## Remaining (do not count closed)

Authenticated BEFORE state/history/OLD subjects; exact BEGIN/current context qualification and retained revocation population; T1 DR-103/DR-112 (see `INERT-IDENTITY.md`); shared/minimum/time/role-record effects; batch cleanup; durable custody/fence/census/writers/source selection; M3–M6. 291 is not shipped behavior or cumulative approval.

---

## Verdicts

- [x] **291:** archive/pins verified; context-to-plan derivation matches 215 r14 locals plus 265 key lookup; 287/288 kernels unchanged; 7/6 mutant classification reproduced; 237/237, Clippy, fmt, 9-file rustfmt.
- [ ] **Not** current-root/BEGIN proof, T1 signature gate, clock/publication, or product installation.
