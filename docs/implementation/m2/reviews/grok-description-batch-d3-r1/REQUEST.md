Grok review: D3. D3 is the third description-only contract successor. It refreshes the inventory v134 descriptions that integrated units have made stale since D1 and D2. Claude Opus 5.5 leads, and you are the single reviewer.

Do not edit any repository, commit, push or delegate. Write only under `/tmp/opensip-implementation/reviews/grok-description-batch-d3-r1`. If you run anything, use only the two evidence scripts named below or read-only commands, and run git only read-only.

**Machine constraint.** A timing-sensitive crash-matrix run may still be using this machine.
- Run no cargo, no tests and no crash-matrix binary or checker.
- Run the evidence scripts at `nice -n 19`.
- Do not touch `/Users/sb/code/opensip-ai/opensip-x9-6`.
- `~/Library/Application Support/OpenSIP` stays absent; do not read or create it.

## Subject

The pins are in hashes.txt:
- `docs/implementation/m2/description-batch-d3-subject.json`, the subject manifest;
- `docs/implementation/m2/description-batch-d3/`, which holds:
  - `successor.json`;
  - `README.md`;
  - `evidence/descriptions.json`;
  - `evidence/build_d3.py`;
  - `evidence/verify_scratch.py`.

All of these are untracked in arch until acceptance. `description-batch-d3-unit.json` is the lead's draft, marked DRAFT-PENDING-REVIEW. It is not part of the subject.

**Product.** Main is at 3d2d5b5 (X9-6), read-only. Its lock selects inventory v134, with 75 contract successors, 55 inheritance rows and 4 historical supersessions (D2's, folded). There is no product source, schema, registry, generated-code or inventory change.

**Lead's worktree.** The binding is staged in the uncommitted worktree `/Users/sb/code/opensip-ai/opensip-d3`, detached at 3d2d5b5 (read it if useful). See "Binding" below.

`rationales.json` in this directory is a convenience and is not part of the subject. It has an entry for each of the 122 judged rows: the lead's evidence with file:line, and the product doc comments found stale but not changed.

## What it does

D3 has one record, whose only parent is v134. It covers 62 rows:
- **45 `passageOverrides`** on plain rows (D1's form). Each `before` is the raw v134 description.
- **17 `passageSupersessions`** on inherited rows (law VD1 r1, D2's form). Each `before` is the row's one inheritance entry's `after`, and `supersedes` names the row's chain tail:
  - D1's override on v119, for 15 rows;
  - D2's supersession on v122, for `read_premise.rs` and `installation_session.rs`.

The README tabulates every row, its form and what was stale. The exact text is in `evidence/descriptions.json`, and identically in `successor.json`.

**How the rows were found** (README, "How the rows were found"):
1. Each v134 row's effective description was matched to the lock commit at which it last changed.
2. Each of the 121 rows whose file changed after that point, within 8240856..3d2d5b5, was judged against the file at 3d2d5b5. 8240856 is D1's basis.
3. Added to those were one row found by a scan for time-bound wording, and every row that a README or review since D1 deferred to "the next description-only successor".
4. A second, independent pass checked every drafted claim against the code. It checked units by `git log -S`, law items, counts, and "only" and "never" claims, and its corrections are in the text.

The outcome: 122 rows judged, 62 changed, 60 kept. The README's "Checked and kept" names all 60, with the reason for each kind.

**How the text was edited.** Every sentence that is still true is kept word for word. False text is replaced, and clauses name what the file now does, citing the law item and unit.

## Judgment calls: please rule on each

1. **One record, both forms.** `contract_successor` reads `passageOverrides` and `passageSupersessions` from the same record, and `successor_chain` checks each.
   - A row is superseded if and only if it has an inheritance entry.
   - A direct override of an inherited row would conflict with its projection.
   - An override of D2's two rows would restate a superseded meaning.

   `build_d3.py` asserts that neither occurs. Rejected: splitting into D3a and D3b, which would give two reviews for one purpose.
2. **Pre-D1 omissions are included.** The sweep found seven rows that were already stale by omission before D1: `first_registration.rs`, `installation_doctor_tests.rs`, `installation_root.rs`, `installation_session_tests.rs`, `ordinary_writer_tests.rs`, `current_trust_admission_tests.rs` and `floor_publication_tests.rs`. `floor_publication.rs` also gains X4B-b's `confirmations` beside its X9-1 change. Leaving them out would need a D4 for the same purpose.
3. **Planned rows.**
   - Four plan-era texts gain their M2 content, and the planned sentence is kept wherever it is still the file's purpose: `fact_admission.rs`, `finalization.rs`, `maintenance.rs` and storage's `tests/commit_tests.rs`.
   - `finalization.rs` loses two planned clauses that are not this file: "to lifecycle rollover", and "use outcomes.rs for the retained analysis projection".
   - `tests/commit_tests.rs` loses "API compile-fail fixtures require the selected harness", which names nothing in the file.
   - X6c's README kept `maintenance.rs` as "broader, not contradicted". D3 judges that a text naming none of the file's content is materially incomplete.
   - `commit.rs`, `ledger_store.rs` and `recovery.rs` keep their planned text, because it already covers what they hold.

   Rule on `maintenance.rs` and on the kept three.
4. **"Only under cfg(test)" and X9 barrier points.**
   - These texts are judged contradicted, because X9-1's points exist under the crash-matrix feature outside cfg(test):
     - `carrier_append.rs` ("Crash and fault hooks exist only under cfg(test)");
     - `carrier_rollover.rs`, the same sentence;
     - `project_commit.rs`, crash points and the COMMIT fault hook.

     The new text keeps the file's own hooks under cfg(test) and names the X9 points under the feature.
   - Files whose texts neither list X9 points nor claim cfg(test) only stay true, for example `carrier_start.rs` and `installation_admission.rs`.
   - `commit_session.rs` and `operation_handoff.rs` do list their X9 points, so their scopes are added (x3b.append.*, x2.fence.end).
5. **"Compiled only for tests" under the joint predicate.** `initial_core_tests.rs`, `initial_platform_tests.rs`, `accepted_store_fixture.rs` and its tests' source pin are now compiled under any(test, crash-matrix, scenario-fixtures) (X9-1's shared fixture gates). Their texts now say so.
6. **`clock.rs` (borderline).** Under the test-only crash-matrix feature only, `observe_clock`'s wall reading comes from the scripted clock in a matrix child. It is included because it changes the file's one observation and is a pinned feature site. Rule on whether it is material.
7. **`recovery_route.rs` is kept.** "Library only: no CLI command calls it before X11" reads as if X11 would wire it. Law X11 r1 item 4 rules this wording "stays true", so D3 does not edit it.
8. **X1b is closed.**
   - `read_premise.rs` keeps D2's text (X1b's Write-receipt refresh) word for word. Every sentence is still true at 3d2d5b5, and `opensip doctor` is the one wired CLI path.
   - D3 supersedes D2's link only to add X3d-3's `core_evaluator_closure`.
   - Please confirm that D2's text holds.
9. **Two kept sentences are narrowed because they were literally false.**
   - `post_state.rs`: "Capturing opens, locks, checkpoints and creates nothing under the root." Capture opens and reads every file. The text now matches the code's own claim at `post_state.rs:284`: nothing is opened for writing, locked, checkpointed or created.
   - Host's and storage's `crash_matrix_support.rs`: "Nothing here returns an authority type." Both forward X9-2's three driver entries. Each sentence now begins "Apart from the forwarded driver entries".
10. **Length.**
    - `operation_handoff.rs` is 5073 characters and `commit_session.rs` is 4838. The previous longest was D1's 3989.
    - Ten more texts are over 3000 characters, several of which were near 3000 before.
    - Keeping true text word for word forces the length. Rejected: rewording true text to save space.
11. **Things found but not changed.** These are product doc comments; the README lists them. Examples:
    - `carrier_floor.rs:9-10` and `carrier_operation.rs:52-54` say there is "no other production constructor";
    - `fact_admission.rs:17` says "nothing calls it before X7a";
    - `accepted_store_fixture.rs:1-13`;
    - `driver.rs:3-6`;
    - `commit_session.rs` cites X7 r5 item 6 where X7 r6 records the accessors.

    The lead will route these to a code follow-up.
12. **After selection.** The next inventory successor must:
    - carry all rows by value;
    - project D3's 45 overrides, so `inventoryPassageInheritance` grows from 55 to 100 in canonical order, as D1's 39 did at inventory122;
    - fold the 17 supersessions into their rows' entries, as D2's 4 were folded at inventory123;
    - have its projection helper read both forms.

    If another inventory is selected first, `build_d3.py` rebuilds D3 with no edit, and that needs a new review.

## Binding (lead's worktree; not part of the subject)

`/Users/sb/code/opensip-ai/opensip-d3`'s `design-lock.json` appends D3's `contractSuccessors` entry, as D1's binding did at 7be09a7. The record and subject pins are real. The review and assent pins are SCRATCH-D3 placeholders, which only `verify_scratch.py` serves, in memory. Plain verify_design on that worktree therefore refuses ("missing or escaping regular file: SCRATCH-D3/review.json"), which is correct before review.

At acceptance, the lead will:
1. copy your review.json here;
2. complete `description-batch-d3-unit.json` (ACCEPTED-DESIGN-UNIT, with the review pin);
3. replace the two placeholder pins;
4. run plain verify_design;
5. commit.

## Checks run by the lead

All runs used `PATH=/opt/homebrew/Cellar/python@3.14/3.14.6/bin:/opt/homebrew/bin:/usr/bin:/bin` and `nice -n 19`.

- **Determinism.** `python3.14 -I -B evidence/build_d3.py` produced the same `successor.json` and subject bytes on two runs.
- **Appended mode.** `python3.14 -I -B evidence/verify_scratch.py` ran on main at 3d2d5b5 and appended the binding in memory. The result:
  - passed, with 94 inventory successors and 76 contract successors, and v134 still selected;
  - 55 inheritance rows, unchanged;
  - `inventoryPassageSupersessions` 4 → 21;
  - D3: 45 overrides and 17 supersessions, every `before` the row's current text;
  - 40 generation sources, 48 admission sources and 15 aliases verified.
- **Bound mode.** `python3.14 -I -B evidence/verify_scratch.py /Users/sb/code/opensip-ai/opensip-d3` used the worktree's own entry and gave the same result.
- **Live main.** Plain `tools/verify_design.py --architecture ../opensip_arch --implementation .` on main passes unchanged: 75 contract successors, 55 inheritance rows and 4 supersessions.

## Decide

- Is every new description true of the committed code at 3d2d5b5? Read the files. Is each one a fair, minimal edit of the old effective text?
- Is any sentence that was true now lost or altered?
- Is any v134 row stale at 3d2d5b5 but missing from this batch? Consider especially the 60 kept rows and the rows whose files changed since 8240856.
- Does each supersession name the right link (D1 or D2), and is each plain row's `before` the raw v134 text?
- Rule on judgment calls 1 to 12.
- Is the successor well-formed for selection? Is anything else wrong?

review.json must contain:
- `"verdict"`: `ACCEPT-DESIGN-UNIT` or `REQUIRED-FINDINGS`;
- `"requiredFindings"`;
- `"subjectManifestSha256"`: a single string, the sha256 of `description-batch-d3-subject.json` (lead's value `b31ca109e8a42cd090780d0171e4cc77d91a8c338b3a9aa77bcbe6fccc6403e6`);
- `"successor"`: `{path, bytes, sha256}` of `description-batch-d3/successor.json` (lead's value: 240605 bytes, `b7b4ee2fdc454460c132fee7853b32558fd88cbb389fd6061954144349d99c50`).

This is a contract successor, so it has no `inventoryCandidateAssessment`. If you would change a description's bytes, give the exact replacement string.

Write REVIEW.md and review.json. Do not commit.
