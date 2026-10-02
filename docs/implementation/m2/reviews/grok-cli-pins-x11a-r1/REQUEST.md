Grok review r1: X11a, the CLI creator-refusal pins. Law X11 r1 decides that no creator command is live in M2; X11a is its tests-only unit (items 2, 6 and 7). It adds one new test file, `apps/cli/tests/creator_commands_tests.rs`, changes no production byte, and carries inventory v128 (parent v127).

Claude Opus 5.5 leads. You are the single reviewer.

## Rules

- **What you may change.** Make no repository edits, commits, pushes or delegation. Write only under `/tmp/opensip-implementation/reviews/grok-cli-pins-x11a-r1`.
- **Builds and tests.** If you build or test, use a `CARGO_TARGET_DIR` under that directory. Run every test with a private TMPDIR: create a 0700 directory under `$(getconf DARWIN_USER_TEMP_DIR)` (for example `…/grok-x11a-tmp`). Never use the shared `/private/tmp/claude-501` tree, which other runs churn.
- **Git.** Run git read-only, and only against the worktree below.
- **Real home.** Never touch it: `~/Library/Application Support/OpenSIP` must stay absent. The tests read its metadata from the test process only; they never create it.
- **Private fixture.** Never read or print the private 413 UUID fixture.
- **Toolchain.** `PATH=/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:$PATH`. Python is `python3.14`.

## The unit

X11 r1 item 7: "**X11a (M2, tests only, with an inventory successor).** `apps/cli/tests/creator_commands_tests.rs` with item 6's tests. There are no production changes, so the bytes of `apps/cli/src` and `crates/*/src` are unchanged. The inventory successor adds one row for the new file."

Item 1 (lead decision): `opensip`, `analyze`, `fit` and `audit` keep their present refusals byte for byte until M3. Item 2 fixes what each does in M2: the parser refuses before `MetadataHost` builds anything but the metadata envelope, with no attempt, account observation, core, platform, intent, disclosure, gate, pack admission or file access. Its table:

| Input (any order of `--format human\|json` and `--client-correlation-id`) | Diagnostic | Envelope | Exit |
|---|---|---|---|
| `opensip` (no command word) | "Default analysis is not implemented in this development build. Use opensip help." | `kind: failure`, `termination {request-rejected, REQUEST.UNKNOWN_OPTION}`, `errors: []` | 2 |
| `opensip analyze`, `fit`, `audit` (with or without further words) | "Unknown command or arguments. Use opensip help." | the same | 2 |
| any of them with a creator flag: `--allow-backup-custody`, `--ephemeral`, `--project`, `--workspace-root`, `--trust-group`, `--trust-project-owner`, `--baseline`, `--audit-profile`, `--closure-bundle`, `--accept-origin` | "Unknown command option. Use opensip help." | the same | 2 |
| any of them with `--format agent`, `html` or `sarif` | "The selected format is not applicable to this command." | the same, with `errors: [OUTPUT.FORMAT_NOT_APPLICABLE]` | 2 |
| `opensip help analyze` (or `fit`, `audit`, `default`) | "Unknown or unimplemented help topic." | the same | 2 |

"Where several parser failures compete, the existing last-failure-wins rule stands, and X11a's tests pin the resulting bytes rather than restating that rule." Standard error is empty. `help` and `completion` keep the four-row catalogue.

Item 6 fixes the tests: refusal bytes for every row in both formats (exit 2; JSON valid against the selected command-envelope v7 source schema, as `doctor_tests.rs`'s `schema_valid` does, with `kind`, the exact termination, `errors` and diagnostic; the exact human lines apart from the request id; empty stderr; a fresh well-formed `req1_` id per run); zero effects on the real installation (existence and, when present, device, inode, mode and modification time, read from the test process only) and on a scratch working directory with invalid `.opensip/config.json` and `package.json` (bytes unchanged); the catalogue; the source pin; and no new feature, `cfg`, environment variable or argument.

## Law

All paths are under arch `docs/implementation/m2/` unless named otherwise. All are accepted.
- `cli-enablement-x11/PROPOSAL.md` r1 (equal to `PROPOSAL-r1.md` apart from its acceptance note): items 1, 2, 6 and 7, "Forbidden substitutes" and "Not claimed". This is the law of this unit.
- Your law review, `reviews/grok-cli-enablement-x11-r1/REVIEW.md`.
- Precedent: X10a's `apps/cli/tests/doctor_tests.rs` (product), which runs the real binary with no override and holds X10's source pin. X11a widens that pin in its own file and does not edit `doctor_tests.rs`.

## Subject

Pins are in hashes.txt.

- **Product.**
  - **Worktree.** `/Users/sb/code/opensip-ai/opensip-x11a`, detached at `bccb6b4` (main, with X6c integrated; the lock selects v127).
  - **The diff.** Save `git -C <worktree> diff` as product.diff and report its sha256. The one new file is intent-to-add.
  - **Lead's value.** `ca08e21f507e9c9d7bad02be2b303894b822aec7842c55c5b0cd3c8859d98a18`, 21621 bytes. 1 file changed, 554 insertions(+). `git diff --quiet bccb6b4 -- apps/cli/src crates` holds.
- **Arch.** These files are all untracked:
  - `repository-file-inventory.v128.json` (parent v127);
  - `cli-pins-x11a-inventory-v128-subject.json`;
  - `cli-pins-x11a-inventory-v128/`.

## What was built

### `apps/cli/tests/creator_commands_tests.rs` (7 tests)

**Harness.**
- `Runs` owns one scratch working directory per test under `std::env::temp_dir()`, holding `.opensip/config.json` ("not valid configuration") and `package.json` ("not valid package data"), as `startup_tests.rs` builds them. It snapshots the directory's whole tree (every entry and every file's bytes) and the real installation's state when the test begins.
- `run` starts `env!("CARGO_BIN_EXE_opensip")` with the inherited environment and only `current_dir` set: no `env_clear`, no variable, no argument beyond the input (call 7). After **every** run it asserts that the real installation's state and the scratch tree equal their snapshots.
- `refused(args, expect, diagnostic, not_applicable)` asserts exit 2 and empty stderr, then:
  - **JSON:** `schema_valid` against `urn:opensip:product-v1:workflows:evaluator3:command-envelope:7` (the same registry call as `doctor_tests.rs`), `kind`, the whole `termination`, `diagnostics == [diagnostic]`, and the **whole stdout byte for byte** against the v7 empty-errors branch with the run's id substituted: `{["clientCorrelationId":…,]"diagnostics":[…],"errors":[],"exitCode":2,"kind":"failure","requestId":…,"schemaFamily":"opensip.product.envelope","schemaMajor":7,"termination":{"class":"request-rejected","errorCode":"REQUEST.UNKNOWN_OPTION"}}\n`. The not-applicable row's `errors` is its one registered error `{"code":"OUTPUT.FORMAT_NOT_APPLICABLE","remedy":"Choose an applicable output format."}`.
  - **Human:** the whole stdout equals `Termination: request-rejected\nError: REQUEST.UNKNOWN_OPTION\n[Detail: OUTPUT.FORMAT_NOT_APPLICABLE\nRemedy: Choose an applicable output format.\n]Request: <id>\n<diagnostic>\n`. The correlation id is never rendered in human output.
  - **The id** is 37 bytes, `req1_` plus 32 lowercase hex, and new to the test's set. Each test ends by asserting its set's exact size, so every run had a distinct id.
- `placements(words)` gives eight orders of one input: plain; `--format human` first; correlation first and `--format=human` last; `--format=json` last; `--format json` first; `--format=json` between the first word and the rest; `--client-correlation-id=…` then `--format json` last; and `--format=json` first with `--client-correlation-id …` last. Three are human and five JSON; three carry `clientCorrelationId`.

**The tests.**
1. `the_default_analysis_keeps_its_refusal_in_both_formats`: row 1, eight placements of no command word.
2. `analyze_fit_and_audit_keep_their_refusal_with_or_without_further_words`: row 2 for each word alone, with one and two further words, and after a leading word, in all eight placements (96 runs).
3. `every_creator_flag_is_an_unknown_option_on_every_creator_command`: row 3 for each of the four command forms (none, `analyze`, `fit`, `audit`) and each of the ten creator flags. Each pair runs in all eight placements, and also with the flag before the command word, as `--flag=x11a`, and as `--flag x11a` (where the value parses as a word), each in human and JSON (560 runs).
4. `agent_html_and_sarif_are_not_applicable_to_every_creator_command`: row 4 for each command form and each of `agent`, `html` and `sarif` (120 runs):
   - human: `--format F` after, `--format=F` before, and with a correlation id;
   - JSON: `--format=json` before the inapplicable format, with and without a correlation id (call 1);
   - competing failures, pinned at their bytes (call 2): `F` then `--format=json` gives "Output format was specified more than once." in JSON with `errors: []`; `--ephemeral` then `F` gives the not-applicable row; `F` then `--ephemeral` gives the unknown-option row; the same two orders with `--baseline` under `--format=json` first.
5. `help_for_the_analysis_commands_is_an_unknown_topic`: row 5 for `help analyze`, `fit`, `audit` and `default` in all eight placements (32 runs).
6. `help_and_completion_keep_the_four_row_catalogue`: exit 0 and empty stderr for each; `help` human byte for byte (it carries no request id); `help --format=json` schema-valid, `kind: meta`, `topic: null`, a fresh id, and `meta.commands` exactly the four rows (`completion`, `doctor`, `help`, `version`, with their usage and summary); `completion bash`, `zsh` and `fish` byte for byte (each lists exactly `completion doctor help version`, then `# Termination: success`).
7. `no_creator_gate_writer_pack_or_commit_symbol_reaches_the_binary_or_the_ingress`: over the production text (call 4) of every `.rs` under `apps/cli/src` and of `crates/host/src/outcomes.rs`, `doctor_ingress.rs`, `request.rs` and `lib.rs`, none of `run_initial_creator`, `create_initial_installation`, `mint_intent`, `CreationIntent`, `admit_ordinary_writer`, `produce_write_platform`, `DurableWriteGate`, `admit_policy_selection`, `finalize` or `route_recovery` appears. `apps/cli/src` does not name `installation_entry`. In `crates/security/src`, `fn run_initial_creator(` and `fn admit_ordinary_writer(` are each defined in exactly one production text, their owners `custody/installation_routing.rs` and `custody/ordinary_writer.rs`, once each and as `pub(crate) fn`, and `lib.rs` names neither (call 5).

That is 821 binary runs in all, about 29 seconds for the file.

**Mutation checks (lead, reverted).** Each was made in the worktree, observed to fail its test, and reverted with `git checkout`:
- the default diagnostic shortened in `arguments.rs` fails test 1;
- a `finalize` identifier added to `bootstrap.rs` fails test 7;
- `run_initial_creator` made `pub fn` fails test 7.

## Judgment calls: please rule

1. **The JSON branch of row 4.** A single `--format agent|html|sarif` is the only format argument, so the output stays human; the not-applicable row is then human. Its JSON form is reachable only when `--format=json` comes first and the inapplicable format second, where the parser's second-format failure is overwritten by the not-applicable failure. "In both formats" is met that way, and the tests pin both. **Rejected:** treating row 4 as human-only, which would leave its JSON bytes unpinned.
2. **Competing failures are pinned, not restated.** Item 2 says the tests "pin the resulting bytes rather than restating that rule". The tests run five competing orders per command and format (call 1's pair, format twice, a creator flag before and after the format, with and without JSON first) and assert the bytes the parser emits. No helper encodes the rule.
3. **Every placement is a full exact-bytes check.** Item 6's field list (kind, termination, errors, diagnostic) is asserted, and the whole stdout is also compared byte for byte, in JSON and in human. This is stronger than the item's list and is what item 1's "byte for byte" asks.
4. **The production reader is copied, not shared.** Item 6: "The pin reuses `doctor_tests.rs`'s `production` reader." Each `tests/*.rs` file is its own crate, so sharing needs a `tests/common` module, which is a second new inventory row and an edit to `doctor_tests.rs`. The reader is copied verbatim, with its doc comment naming its source. **Rejected:** a shared module.
5. **The security pin is by definition, not by grep of one file.** It walks every `.rs` under `crates/security/src`, requires each function to be defined in exactly one production text, its known owner, once and as `pub(crate) fn`, and requires `lib.rs` to name neither. A public wrapper of the same name elsewhere would fail it. Both modules are `pub(crate) mod` in `custody.rs`; the function's own visibility is the binding fact.
6. **X10's seam pin is not widened to `host/src/lib.rs`.** Item 6's source pin lists symbols; it adds `lib.rs` to the files for those symbols. X10's environment and `cfg` pin (in `doctor_tests.rs`, unchanged) cannot extend to `lib.rs`, which legitimately carries `#[cfg(test)]` modules and macOS `cfg`s. Item 6's "No test seam" is met by the unit itself: no production byte changes.
7. **"No override" means the inherited environment.** Item 6: "They run the real built `opensip` with no override, as X10 r4 item 5's binary tests do." `doctor_tests.rs` sets only the working directory; these tests do the same. `startup_tests.rs`'s `env_clear` plus fake release variables is not followed, because that is an override.
8. **Zero effects is the comparison, checked after every run.** The real installation's state is captured when each test begins (absent, or (device, inode, mode, mtime seconds and nanoseconds) from `symlink_metadata`, so a symlink is not followed). Every run must leave it equal. So the test holds on a machine where the installation exists; on this host it is absent before and after. The scratch comparison covers the whole tree, so a new file anywhere under the working directory (for example a lock under `.opensip/`) fails it, not just a change to the two files.
9. **"With or without further words"** covers one and two trailing words and a leading word (`src analyze`): every such input reaches the parser's catch-all. **"`help … default`"** is included as item 2 lists it.
10. **Creator flags that take values.** In M2 no flag takes a value, so `--project x11a` parses `x11a` as a word. Both that form and `--project=x11a` are pinned; each gives the unknown-option row.
11. **The catalogue is pinned byte for byte.** Item 6 asks that `help` and `completion` "list exactly" the four commands. The human help and the three completion scripts carry no request id, so their whole bytes are pinned; JSON help pins the four rows exactly. This also enforces "Forbidden substitutes": no change to the catalogue in M2.
12. **Test cost.** 821 runs, each followed by a tree snapshot, take about 29 seconds in the file and run in parallel with the workspace. **Rejected:** fewer placements, which would weaken "any order".

## Inventory v128

- Adds exactly one row, `apps/cli/tests/creator_commands_tests.rs` (`opensip-cli`, test). 948 v127 rows are equal by value, for 949 files. Packages, dependencies, pending decisions and carried obligations are unchanged.
- **No existing row changes**, because no other byte changes. `startup_tests.rs`'s and `doctor_tests.rs`'s rows stay true (the reason for item 6's placement).
- **Projection.** The 55 rows the lock binds to v127 are carried by stable file path (16 from inventory81 onward, D1's 39 with D2's four `after` texts checked). None is folded on v127. The count stays 55.
- `evidence/build_v128.py` reads the parent from the lock, refuses tracked paths and a lock selecting v128, and reproduces the same bytes on rerun.

## Checks

These ran at bccb6b4 plus this diff, with a private 0700 TMPDIR (`…/x11a-tmp`).
- **Workspace runs.** `cargo test --locked --offline --workspace --all-targets` twice: each 1688 passed, 0 failed and 3 ignored, across 18 test binaries. That is X6c's 1681 at bccb6b4 plus these 7.
- **Lints.** `cargo clippy --locked --offline --workspace --all-targets -- -D warnings` is clean.
- **Formatting.** `cargo fmt --all -- --check` is clean.
- **`check_package_edges --lane host`** (worktree `cargo metadata`): passes against v127 and v128, with 20 declared and 20 resolved edges.
- **`verify_projection.py`** against the real lock at bccb6b4: 55 rows, 278 corruptions refused.
- **`evidence/verify_scratch.py`** (v128 appended in memory to the worktree's lock, with the record's 55 rows): passes, with 88 inventory successors, 74 contract successors and 55 inheritance rows. v128 is selected.
- **`build_v128.py`** reruns produce the same bytes: 949 files, 948 v127 rows equal by value, one added, 55 projection rows.
- **Home.** `~/Library/Application Support/OpenSIP` is absent before and after.

## Decide

- Does X11a meet X11 r1 items 2, 6 and 7? In particular:
  - **Refusal bytes:** every row of item 2, both formats, several orders, exact bytes, schema validity, empty stderr, fresh ids;
  - **Zero effects:** the real installation and the scratch working directory, after every run;
  - **Catalogue:** exactly the four rows in `help` and the three completions;
  - **Source pin:** item 6's symbols over item 6's files, `installation_entry` out of the CLI, and both security functions `pub(crate)` and not re-exported;
  - **No seam and no production change.**
- Are calls 1 to 12 right?
- Is v128 right on v127, with the one added row's text and the carried 55-row projection?
- Is anything else wrong?

## Output

Write REVIEW.md and review.json to `/tmp/opensip-implementation/reviews/grok-cli-pins-x11a-r1`. Do not commit.

review.json must contain:
- `"verdict"`: `ACCEPT-UNIT` or `REQUIRED-FINDINGS`;
- `"requiredFindings"`;
- `"subjectManifestSha256"`: the sha256 of `cli-pins-x11a-inventory-v128-subject.json`, as a single string. The lead's value is `2f91855298c4ad46588912896c64d2fcc338f33357278d3755a44a025ca5fb20` (2082 bytes).
- `"inventoryCandidateAssessment"`, with:
  - `verdict` and `requiredFindings`;
  - `path`, `bytes` and `sha256` of `repository-file-inventory.v128.json` (lead: 530975 bytes, `c6bcf2f4818869756b99cec4a4d97c85c48353e2f66035ed92406165550c3ce2`);
  - `parent`: the v127 pin (529197 bytes, `ba6133904aa9c92a44aafb4ff73cdc9774c8fe853670bce6a4e417403d8a3fb4`);
  - `successorRecord`: the pin of `cli-pins-x11a-inventory-v128/successor.json` (lead: 145147 bytes, `bdf9da04aa5ad4f45490d1eb9ea9b29f60a925f6b31c6f72a0284f47508b7951`).
