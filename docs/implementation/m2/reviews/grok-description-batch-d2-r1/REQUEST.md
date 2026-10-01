Grok review: D2. It is a description-only contract successor. It uses law VD1 r1's `passageSupersessions` to refresh the four inherited inventory rows that D1 deferred. Claude Opus 5.5 leads. You are the single reviewer.

Do not edit any repository, commit, push or delegate. Write only under `/tmp/opensip-implementation/reviews/grok-description-batch-d2-r1`. If you run anything, use only the two evidence scripts named below or read-only commands, and run git only read-only. Run no product cargo.

## Subject

The pins are in hashes.txt:
- `docs/implementation/m2/description-batch-d2-subject.json`, the subject manifest;
- `docs/implementation/m2/description-batch-d2/`, which holds `successor.json`, `README.md`, `evidence/descriptions.json`, `evidence/build_d2.py` and `evidence/verify_scratch.py`.

All of these are untracked in arch until acceptance.

The product is main at 96dd114, read-only. Its verify_design is VD1-a (accepted in `reviews/grok-verify-design-vd1-r1`). Its lock selects inventory v122, with 73 contract successors (D1 included) and 55 inheritance rows. There is no product, schema, registry, generated-code or inventory change, so no worktree and no inventory successor are needed.

## What it does

There are four supersessions on v122, its only parent. Each one replaces an effective description that no longer describes the file at 96dd114. `passageOverrides` is empty. The README gives each row's target and what was stale in it. The exact before and after text is in `evidence/descriptions.json`, and identically in `successor.json`.

| v122 | File | `supersedes` (record, parent and selector) |
|---|---|---|
| 273 | `crates/identity/src/store_lineage.rs` | 468a's `successor.json`, v74 `/files/158/description` |
| 372 | `crates/security/src/custody/installation_session.rs` | 461b's `successor.json`, v80 `/files/247/description` |
| 388 | `crates/security/src/custody/read_premise.rs` | 461b's `successor.json`, v80 `/files/250/description` |
| 398 | `crates/security/src/initial_installation.rs` | 468a's `successor.json`, v74 `/files/242/description` |

Each `before` equals the row's one `inventoryPassageInheritance` entry's `after`, which is the named override's `after`.

**Is there a D1-era link? No.** D1 made only direct overrides of plain rows, and `build_d1.py` refused inherited rows. Inventory122's projection grew from 16 to 55 entries with D1's 39 meanings, but none of them is one of these four files. Each of the four rows still has exactly one inheritance entry, from 468a or 461b, and no row has an earlier supersession. So the correct link to supersede is the root override in each case. `build_d2.py` derives the target from the lock rather than hard-coding it. It would take the chain tail if a supersession existed, and it asserts that there is exactly one inheritance entry per row.

## Evidence for the new text (file:line at 96dd114)

**`read_premise.rs`**
- The purpose types and `produce_write_platform` (302).
- The invariant row for a foreign receipt (353).
- The write-receipt lendings: `bootstrap_source` 168, `charge` 176, `charge_guarded` 191, `reserve_end_path_settlement` 209, `settle_end_path` 218.
- `selected_core` (117).
- Consumers: `ordinary_writer.rs` 23/40 and `operation_handoff.rs` 62/348.
- The CLI: `apps/cli/src/bootstrap.rs` 34 calls `host.doctor`, which calls `observe_installation_for_doctor` (`doctor_ingress.rs` 39), which reaches `produce_read_platform` (`installation_doctor.rs` 57). No CLI path reaches `produce_write_platform`.

**`installation_session.rs`**
- The core finding (664).
- The current record under `CURRENT_STATE_CAP` (680), with the over-cap, decode and `current_matches` outcomes all `IncompleteRefusal::CurrentStore` (`installation_admission.rs` 456–472).
- The node limit: `lineage_limit(true)` is the budget row, and the generation bound is the `Chain` finding (760–762; `installation_admission.rs` 395–414).
- The receipt rechecks at 357 and again at 392.
- The endpoint values (393, 451–465).
- `retain` (277).

**`store_lineage.rs`**
- `into_nodes` (194), used by `installation_admission.rs` 1449 and `installation_session.rs` 755.

**`initial_installation.rs`**
- `recheck_actor_in` (284, also used by `ReceiptGuard::recheck_in`), `recheck_storage_in` (299) and `recheck_handoff_storage` (660).
- `reserve_end_path_settlement` (170) and `settle_end_path` (183). These are the only non-test callers of `WorkLedger::reserve_settlement` and `settle`; `ordinary_writer.rs`'s `settle` is its own method.

## Judgment calls: please rule on each

1. **The one edited true sentence.** In `read_premise.rs`, "The receipt is private …" becomes "The read receipt is private …". With two purposes, "the receipt" is ambiguous, and the lending that sentence names is the read receipt's only. Every other sentence of each old text is kept word for word.
2. **The "Library only" sentences are replaced, not qualified.** In `read_premise.rs` and `installation_session.rs` they are false since X10a wired `opensip doctor`. The replacement names doctor as the one wired CLI path. `read_premise.rs` also says no CLI command reaches a write receipt.
3. **`initial_installation.rs` keeps "the initial creator's pre-installation attempt" and "the only work ledger for the whole act".** Both are still true of the creator. A new sentence says the same attempt also stands behind the read and write receipts.
4. **Scope.** Only the four rows that D1 and VD1 named. Is any other inherited row (the other 12 of the original 16) now stale? If so, it can join D2 by name.
5. **After selection.** The next inventory successor must:
   - carry these four rows by value;
   - fold each supersession into its row's inheritance entry (law VD1 item 3): `before` stays the raw text, `after` becomes D2's;
   - keep its projection helper's count at 55. The helper must now also read `passageSupersessions`.

## Checks run by the lead

All runs used `PATH=/opt/homebrew/bin:/usr/bin:/bin` and a private 0700 TMPDIR under `$(getconf DARWIN_USER_TEMP_DIR)`.

- **`python3.14 -I -B evidence/build_d2.py` (deterministic).** Two runs produced identical bytes.
- **`python3.14 -I -B evidence/verify_scratch.py`** ran the real verify_design at 96dd114 over the real lock with D2 appended, with the review and assent held in memory. The result:
  - passed, with 74 contract successors and v122 still selected;
  - `inventoryPassageSupersessions` 4;
  - 55 inheritance rows, unchanged;
  - every `before` equals its row's current meaning;
  - 40 generation sources, 48 admission sources and 15 aliases verified.
- **Live `verify_design --architecture ../opensip_arch --implementation .` at 96dd114** passes unchanged: 73 contract successors, 55 inheritance rows and 0 supersessions.

## Decide

- Is every new description true of the committed code at 96dd114? Read the files. Is each a fair, minimal edit of the old effective text?
- Is any changed sentence that was true now lost?
- Does each supersession name the right link?
- Rule on judgment calls 1 to 5.
- Is the successor well-formed for selection? Is anything else wrong?

review.json must contain:
- `"verdict"`: `ACCEPT-DESIGN-UNIT` or `REQUIRED-FINDINGS`;
- `"requiredFindings"`;
- `"subjectManifestSha256"`: a single string, the sha256 of `description-batch-d2-subject.json`;
- `"successor"`: `{path, bytes, sha256}` of `description-batch-d2/successor.json`.

This is a contract successor, so it has no `inventoryCandidateAssessment`. If you would change a description's bytes, give the exact replacement string.

Write REVIEW.md and review.json. Do not commit.
