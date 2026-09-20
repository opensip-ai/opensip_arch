# Independent review — target-derived component authority 294

**Standing:** bounded native-Rust review of frozen `native-ordinary-scope-checkpoint-294`. Private `prepare_scoped` composes 293 inventory-body/catalog/shared signatures, 290 availability from the **exact shared finite union**, the unchanged 291 context planner, and actual COMPONENT envelope signatures **only when derived T1 contains TR-COMPONENT**. Body/identity joins always run; shared signatures are never inert. This is not ROOT-chain/current-head/BEGIN proof, host admission, signed time, completeness, grant, or product installation. Installed product remains `fa72e50`. Keys are **TEST ONLY**. Archived 293 was not edited.

Python 3.12.13 `-I -B`. OpenSSL 3.6.3. Rust 1.95.0 `--offline --locked`. Review-local copies only. Frozen fixture/key/result directories were not overwritten. No workspace rerun (284's 529 is predecessor).

---

## Verification

Pins, tar bytes, member counts, and every `subject.json` hash matched **before** extract.

Frozen archive: **8460212 B, 919 members, SHA256 `89e5e903bdea0f5b361898ad34939867a3e8d1923dd4ffa682ede0dbbbe9b050`**. Standing: unselected private294 target-derived component authority; full ROOT/current context pending. Extract rehashed **919/919**. Product-inputs **447/447**. Nested parent 293 pin `7a8555d3…9528` equals reviewed 293; live 293 trial tar matches. Nested 215 r14 `cd338af6…dd9c` / model SHA `9aa6e56b…d701` match. Nested 265 `73c3b3f5…86df` live-matches. Product vs 293: **447** files, **443** unchanged. Changed only `ordinary_targets.rs` `a538a935…2970`. Added: `scope294.ndjson`, `scope294-inputs.ndjson`, `scope294-alternate-root.json`. `plan()` / `coordinate()` / `plan_from_contexts` production text is **byte-identical** to 293. `component_manifest.rs`, `trust_ordinary_metadata.rs`, `trust_ordinary_quorums.rs`, and 293 fixtures are unchanged. `prepare_scoped` is a module-private `fn` (not `pub(super)`). Not in `lib.rs`.

---

## What `prepare_scoped` does

Same Budget: `ordinary_metadata::inventory::prepare` (292 shared BUNDLE/catalog/list + union including the list; 293 catalog 4-tuple / publisher=envelope namespace / body-preimage-envelope digests / hostCore / reserved names; ROOT unresolved; no host admission). Then `role_availability::derive(signing_root, union)` for the C.3 **final-root** outside context (283 binds that document to the captured closure body; whether it is the admitted chain head is **still pending**). Each supplied RECOVERY root is derived with the **same** union. Unchanged `plan_from_contexts` (no caller `active`/`below`/`authenticated` flags). If `remaining()[1]` (lexical TR-COMPONENT in T1), every inventory component envelope is `verify_envelope` + `filter_envelope_revoked(..., union)` and must be `Met`. Excluded COMPONENT: all 293 identity/body joins already done; **no** message quorum required. Relied-on COMPONENT: availability cannot substitute for message quorum.

Dedicated isolation: incoming/retained single-key revocations leave **2** delegated keys available but only **1** surviving actual signer of 2 → `ComponentQuorum` although availability is not short. Incoming one key with 3 signers still meets 2-of-3. Body/catalog/shared failures still refuse; scope cannot waive them.

311 cases, **200/200** positives, over 45 TEST-ONLY signed inputs. Oracle: 265 primary crypto/semantics/key lookup plus 215 r14 `ordinary()` traced before completeness.

**Preserved fixture failures (reference-only, native unchanged):**

1. `fixture-generation-r1.log`: helper `SyntaxError` (`__code__and` missing space) before any execution.
2. `security-integrated-r1`: 240 passed, 1 failed — `valid-full-ordinary-metadata/alternate-BEGIN-root` expected Ok, got `MissingRecoveryEvidence` because later recovery-restriction mutation aliased earlier stored inputs after expected results were computed (251-case corpus). `copy.deepcopy` of record context in the **fixture helper** only. `scope294-before-context-alias-fix.ndjson`, helpers, and failed log retained. Then 45 signed cases added isolated message-quorum rows (r2: 311).

**Executed:** `cargo clean -p opensip-security` then **241/241** with `Compiling opensip-security` (includes 287/288/291/292/293 tests plus new scoped test). Workspace Clippy `-D warnings`, cargo fmt, rustfmt of **nine** include files. 13/13 r1 compiled controls core-equal frozen `mutation-check-r1` (live baseline cargo skipped; unpatched source SHA matched frozen baseline `a538a935…2970`). Frozen mutant dir not overwritten.

**Controls (4 wrong conditional acceptances):** `omit-target-component-authority` (bad COMPONENT signature admitted); `component-authority-omits-incoming-list` / `component-authority-omits-all-revocations` (`incoming-single-key-short-message` admitted); `ignore-protected-recovery`. **9 other-first:** `require-excluded-component-authority` (over-refusal `ComponentQuorum` on excluded); `use-initial-instead-of-remaining-targets`; `use-index-role-for-component-scope`; `outside-availability-omits-incoming-list`; `recovery-uses-outside-root`; `recovery-omits-revocation-union`; `ignore-old-subject-revocation`; `lose-component-proof-path`; `scope-failure-not-latched`. Not operational exploits.

---

## Combined reproduction table

| Kind | Result |
|---|---|
| 294 pins before extract | match |
| Nested 293 / 215 r14 / 265 live tars | match |
| 291 planner / 293 inventory bytes | unchanged |
| Live `cargo test -p opensip-security` | **241/241** after force rebuild |
| Clippy / fmt / rustfmt 9 includes | pass |
| 294 r1 mutants | 13/13 frozen-equal; 4 wrong / 9 other |
| Workspace | not rerun (284 529 predecessor) |

---

## Remaining (do not count closed)

Shared ROOT / accepted-head / bootstrap; exact current vs BEGIN/history/population qualification; signed time / minima / completeness / role-record effects; full host-admission gate; durable custody/fence/census/writers; source selection; M3–M6. 294 is a conditional COMPONENT message gate on derived T1, not complete ordinary import or cumulative approval.

---

## Verdicts

- [x] **294:** archive/pins verified; 293 inventory always; availability from exact shared union; 291 plan unchanged; T1 COMPONENT signatures required and filtered by that union; isolated message-vs-availability cases held; SyntaxError and fixture-aliasing preserved as reference-only; 4/9 mutant classification; 241/241, Clippy, fmt, 9-file rustfmt.
- [ ] **Not** ROOT/current-head/BEGIN proof, host installation, signed time, completeness, grant, or product installation.
