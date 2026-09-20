# Independent review — ordinary target planning 287 and conditional completeness 288

**Standing:** bounded native-Rust review of frozen `native-ordinary-targets-checkpoint-287` and `native-ordinary-completion-checkpoint-288`. These are private conditional kernels nested in `role_machine`, not a continuation of the 284–286 Budget joins, not admitted-population producers, and not a T1 ordinary-import gate. They do **not** authenticate observations, write a clock/head/role record, issue a grant, or publish events. Archived 285/286 (`c1e45fcf…97a3`, `ROOT-INTEGRATION.md` `8468b4fa…75cc`) and 284 (`aa610b9a…4dbe`) were not edited. Installed product remains `fa72e50`. Keys are **TEST ONLY**. Prior ROOT-INTEGRATION assessment is **not** implemented here.

Python 3.12.13 `-I -B`. OpenSSL 3.6.3. Rust 1.95.0 `--offline --locked`. Review-local copies only. Frozen fixture/key/result directories were not overwritten. No workspace rerun (284's 529 is predecessor). One **234** security run on the 288 product covers inherited 287 tests; **no separate 233 run** was executed.

---

## Verification

Pins, tar bytes, member counts, and every `subject.json` hash matched **before** extract.

**287** frozen archive: **5756400 B, 517 members, SHA256 `027e03f78fc06757a28ba9d5341b97de6bd0e60b8aba8d78d7ad4b93df1fe1ab`**. Standing: unselected private287 bounded conditional ordinary target planning, no authority. Extract rehashed **517/517**. Product-inputs **434/434**. Nested parent 286 pin `9872efe3…f3c4` equals reviewed 286; live 286 trial tar matches. Nested 215 r14 archive **198136 B / 1445 / `cd338af6…dd9c`**. Product vs 286: **434** files, **431** unchanged; `role_machine.rs` `4a66024a…8ac5` plus `ordinary_targets.rs` `9df87d4b…42aa` and `targets287.ndjson`. Not in `lib.rs`.

**288** frozen archive: **5800624 B, 515 members, SHA256 `a0655354604e2a7f02897cbf65119616b0dde87de9a0d456614c515341801e30`**. Standing: unselected private288 conditional completeness proposals, no authority. Extract rehashed **515/515**. Product-inputs **435/435**. Nested parent 287 pin `027e03f7…e1ab` equals this 287 freeze; live 287 trial tar matches. Product vs 287: **435** files, **433** unchanged; `ordinary_targets.rs` `bab0880a…7e22` plus `completion288.ndjson`. `targets287.ndjson` byte-identical 287→288. `plan()` prefix (lines 1–126) byte-identical. `role_machine.rs` unchanged. Not in `lib.rs`.

Archived 215 r14 `ordinary_batch_model.py` SHA256 `9aa6e56ba6bc5e39bf707e4d901f6dac0c277abef011a3187d34ad256a04d701` (27474 B) matches live draft model and README. Known live OWNER discrepancy: live `/tmp/opensip-implementation/m2-trust-owner-draft-215/OWNER.md` is `780a6dd5…0d60` (50337 B); frozen r14 OWNER is `d8165f14…19fa` (48217 B). Frozen archived OWNER is the source; live historical file was hashed only and left untouched. Initial 287 authoring failure record is retained.

---

## 287 — private T0/T1 planning, no acceptance

`ordinary_targets::plan` is included privately from `role_machine`. It takes six lexical roles (BUNDLE, COMPONENT, CORE, INDEX, PROFILE, REPAIR) plus OLD-subject/below-threshold observations. No authenticated flag, shared-guard, entry-guard, clock, or dispatch. Native returns `Result` where the Python model `assert`s; that is a representation difference, not a second formula.

Never-established TRUSTED/REVOKED refuses (`NeverEstablishedStanding`). RECOVERY requires available restriction evidence; `None` is distinct from `false` (`MissingRecoveryEvidence`). T0 = active U/T/E/S/Q, excluding REVOKED/RECOVERY. Established OLD hits revoke first, including inactive roles; never-established roles are ignored. Then active roles receive quorum observations/stays. T/E/S/R demote to QUORUM-LOST except a Recovery protected by `recovery_revoked == Some(true)`. Below-threshold and OLD-hit roles leave T1. All OLD revocations precede all quorum observations. Owned original/remaining/tentative/ordered facts; at most 12 provisional observations. A plan cannot grant trust.

3040 cases (2016 systematic single-role plus 1024 cross-role): 2656 valid, 384 invalid. Invalid count matches the closed input rules (288 never-established T/V + 96 Recovery-without-bool). Fixtures were traced from actual `ordinary()` locals immediately before completeness at line 53, not an independently copied formula. Independent re-trace of all 3040 rows against archived `ordinary()` matched; property probes held (Recovery/Revoked never T0, T1 ⊆ T0, inactive OLD still revokes, never-established OLD ignored, protected Recovery stays Recovery, unprotected Recovery demotes, OLD before quorum).

**Executed:** inherited by the 288 **234/234** security run (`six_role_tentative_targets_match_exact_frozen_coordination_model` ok). 14/14 r1 compiled controls core-equal frozen `mutation-check-r1` (live baseline cargo skipped; unpatched `ordinary_targets.rs` SHA matched frozen baseline `9df87d4b…42aa`). Frozen mutant dir not overwritten.

**Controls:** 2 invalid planning-input acceptances (`allow-unestablished-trusted-revoked`, `allow-missing-recovery-evidence`). 12 other-first (wrong T0/T1/trace/owned field, not operational exploits): `initial-ignores-active`, `initial-includes-revoked-recovery`, `revoke-never-established`, `skip-inactive-old-subjects`, `keep-old-hit-target`, `quorum-loss-only-trusted`, `forget-protected-recovery`, `lose-recovery-evidence`, `quorum-observe-inactive`, `keep-below-threshold-target`, `reverse-tentative-order`, `drop-stay-quorum-observations`.

**Verdict 287:** bounded match of documented T0/T1/tentative-order arithmetic on externally supplied observations. Conditional context, not an admitted population or import acceptance.

---

## 288 — all-or-nothing completeness proposals

`coordinate` calls the **same** 287 `plan` internally. Completeness = shared guards AND every remaining T1 entry guard. Excluded-role entry guards do not veto. Empty T1 does not waive shared guards. Incomplete: original roles EXACT, all tentative discarded, refused PRESENT for every T0 including healthy siblings and roles already removed from T1. Complete: tentative observations precede accepted PRESENT for T1 only; successful entries become TRUSTED/established with `recovery_revoked = None`. REVOKED/RECOVERY peers cannot gain an ordinary entry from this calculation. No `clock_written`, `metadata_advanced`, record references, grants, dispatch, or persistence. The Python model still sets `clock_written=True` on both complete and incomplete authenticated returns and `metadata_advanced=True` only when complete; native `Proposal` has neither field. That is an intentional bound, not a fixture mismatch.

4768 cases: 4672 valid (892 complete, 3780 incomplete), 96 invalid. Coverage is all 64 T0 subsets × 64 entry-guard subsets + 64 shared-false + 287 cross-role/rejected contexts. Independent re-execution of all 4768 rows against archived `ordinary()` matched. Property probes held (empty T1 still requires shared; excluded false entry does not veto a healthy T1; incomplete refuses every T0 and keeps original roles; complete PRESENT is T1-only; recovery restriction cleared on success).

**Executed:** `cargo clean -p opensip-security` then **234/234** with `Compiling opensip-security` (includes both 287 and 288 tests). Workspace Clippy `-D warnings`, cargo fmt, rustfmt of **seven** include files. Frozen `mutation-check-r1` has **13 report rows including compiled baseline**: 12 variants (11 compiled + 1 compile-failing `retain-tentative-events-on-refusal`). Frozen `mutation-check-r2` compiles that corrected 12th variant. Live cores equal those frozen reports. Frozen dirs not overwritten. Production and fixtures unchanged between r1 and r2.

**Controls:** r1 `retain-tentative-events-on-refusal` failed Rust type inference (`E0283` on `let events = plan…collect()`, `expectedOutcome` false) — compile failure, not a wrong completion. r2 adds `Vec<ProposedEvent>` in the **mutant only**; the compiled variant is a trace/roles difference (tentative observations retained on refusal; `wrongConditionalCompletion` false), not an operational exploit. Two wrong conditional completions: `ignore-shared-guards`, `one-entry-guard-enough`. Other-first (over-refusal / omitted sibling refusals / role or trace): `excluded-role-guard-vetoes`, `omit-healthy-refused-siblings`, `refuse-only-remaining-targets`, `retain-tentative-roles-on-refusal`, `present-original-removed-targets`, `no-target-promotion`, `forget-established-history`, `lose-completed-recovery-projection`, `reverse-success-trace`.

**Verdict 288:** bounded match of documented all-or-nothing completeness, T0 refusal ordering, and recovery-restriction clearing on the 287 plan. Private proposal, not admission, clock write-ahead, or publication.

---

## Combined reproduction table

| Kind | Result |
|---|---|
| 287/288 pins before extract | both match |
| Live `cargo test -p opensip-security` on 288 product | **234/234** after force rebuild (`Compiling opensip-security`) |
| Clippy / fmt / rustfmt 7 includes | pass |
| Independent model re-execution | 3040/3040 and 4768/4768 |
| 287 mutants | 14/14 frozen-equal; 2 invalid-input / 12 other |
| 288 r1 mutants | 13 rows frozen-equal (compiled baseline + 11 compiled variants + 1 type-inference failure); 2 wrong completion / 9 other among compiled variants |
| 288 r2 mutant | 1/1 frozen-equal; compiles the corrected 12th variant; trace difference, not wrong completion |
| Workspace | not rerun (284 529 predecessor) |
| Separate 233 run | **not executed** |

---

## Remaining (do not count closed)

Admitted role/OLD-subject/key-availability/history observations; exact derived T1 / DR-103 vs DR-112 signature integration; current root-chain/shared/time/minimum/identity guards; bound role-record effects and refusal audits; batch interruption/termination, publication, and clock write-ahead custody; policy adoption, artifacts/repair/full commands, fences/census/writers/source selection; M3–M6. These candidates are not shipped behavior, selected registry entries, or cumulative approval.

---

## Verdicts

- [x] **287:** archive/pins verified; T0/T1/tentative-order match of 215 r14 `ordinary()` locals before line 53; 2/12 mutant classification reproduced; inherited by the 234 run.
- [x] **288:** archive/pins verified; same 287 plan; all-or-nothing refusal/ordering/recovery-restriction match; 234/234, Clippy, fmt, 7-file rustfmt; r1 13 rows (11 compiled variants + 1 type-inference failure + compiled baseline) preserved; two wrong completions vs other trace/roles/over-refusals classified; r2 compiles the corrected 12th variant with mutant-only type annotation.
- [ ] **Neither** is current-root authority, complete ordinary import, admitted observation producer, clock/publication, or product installation.
