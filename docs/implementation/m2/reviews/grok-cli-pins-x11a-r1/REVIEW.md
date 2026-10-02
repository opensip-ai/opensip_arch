# X11a r1

Claude Opus 5.5 leads. Grok is the single reviewer. Tests-only unit of law X11 r1 items 2, 6, and 7. Git was read-only. `~/Library/Application Support/OpenSIP` is absent.

Verdict: **ACCEPT-UNIT**. Inventory v128: **ACCEPT**. Required findings: none.

| | |
|---|---|
| Worktree | `/Users/sb/code/opensip-ai/opensip-x11a`, detached at `bccb6b4e2879e6dee34c2149182cbb201a00f4ad`. The one new file is intent-to-add. `git diff --quiet bccb6b4 -- apps/cli/src crates` holds. `doctor_tests.rs` and `startup_tests.rs` are unchanged. |
| product.diff | 21621 bytes, sha256 `ca08e21f507e9c9d7bad02be2b303894b822aec7842c55c5b0cd3c8859d98a18`. 1 file, 554 insertions. |
| Law | `cli-enablement-x11/PROPOSAL.md` matches `PROPOSAL-r1.md` except the acceptance sentence “r1 ACCEPTED by Grok on 2026-10-04.” |
| Subject | `cli-pins-x11a-inventory-v128-subject.json`, 2082 bytes, sha256 `2f91855298c4ad46588912896c64d2fcc338f33357278d3755a44a025ca5fb20`. |
| Inventory | v128, 530975 bytes, sha256 `c6bcf2f4818869756b99cec4a4d97c85c48353e2f66035ed92406165550c3ce2`. Parent v127, 529197 bytes, sha256 `ba6133904aa9c92a44aafb4ff73cdc9774c8fe853670bce6a4e417403d8a3fb4`. successor.json, 145147 bytes, sha256 `bdf9da04aa5ad4f45490d1eb9ea9b29f60a925f6b31c6f72a0284f47508b7951`. |

All 22 rows in `hashes.txt` match the worktree and the arch files.

## What the diff does

`apps/cli/tests/creator_commands_tests.rs` runs the real `opensip` with the inherited environment and only `current_dir` set. After every run it compares the account installation, via `symlink_metadata` in the test process, and the whole scratch tree. Refusals require exit 2, empty stderr, a fresh `req1_` plus 32 lowercase hex characters, schema admission of command-envelope v7, and the whole stdout.

The JSON pin is the serializer’s field order on `Envelope7Root`: optional `clientCorrelationId`, then `diagnostics`, `errors`, `exitCode`, `kind`, `requestId`, `schemaFamily`, `schemaMajor`, and `termination` `{class, errorCode}`. The format row’s `errors` entry is `{code, remedy}` for `OUTPUT.FORMAT_NOT_APPLICABLE`. Human output is `Termination`, `Error`, the detail and remedy only on that row, `Request`, and the diagnostic. The correlation id is absent from the human bytes.

Counts: 8 default placements, 96 analyze/fit/audit word forms, 560 creator-flag runs, 120 format runs, 32 help-topic runs, and 5 catalogue runs. That is 821 binary runs. The file finished in 28.91 seconds.

## Items 2, 6, and 7

Every item 2 row is pinned in both formats.

The default diagnostic, the unknown-command diagnostic, the unknown-option diagnostic, and the unknown-help-topic diagnostic are the strings `arguments.rs` and `MetadataHost::execute` emit, with `errors: []`. `analyze`, `fit`, and `audit` are tested alone, with one trailing word, with two trailing words, and after a leading word. `help analyze|fit|audit|default` is included. The ten creator flags are tested on all four command forms, in the eight placements, and also before the command word, as `--flag=x11a`, and as `--flag x11a`. Both value forms stay on the unknown-option row, which is what the parser does: an unknown dash token sets the failure and does not take a value.

`--format agent|html|sarif` alone stays human, because the initial format is `Human` and that arm does not assign a format. The JSON form of the not-applicable row is `--format=json` first and the inapplicable format second: the second format overwrites “Output format was specified more than once.” with `format-not-applicable` and leaves `format` as `Json`. The tests pin that stdout. The opposite order, inapplicable format then `--format=json`, is pinned as the twice-format diagnostic in JSON with `errors: []`. `--ephemeral` or `--baseline` before the inapplicable format is the not-applicable row; after it, the unknown-option row. Those are the bytes last-failure-wins emits. No helper restates the rule.

`schema_valid` is the same `embedded_schema_registry` call as `doctor_tests.rs`, on `urn:opensip:product-v1:workflows:evaluator3:command-envelope:7`. Refusal tests assert the set size, so each run’s id is new. Human help and the three completion scripts carry no request id and are pinned whole, including `# Termination: success` and exactly `completion doctor help version`. JSON help is schema-valid, `kind: meta`, `topic: null`, one fresh id, and `meta.commands` exactly the four catalogue rows with their usage and summary.

Zero effects run inside `Runs::run`, so they cover the refusal runs and the catalogue runs. The installation comparison is absence, or device, inode, mode, and modification seconds and nanoseconds, without following a symlink. The scratch directory holds `.opensip/config.json` (“not valid configuration”) and `package.json` (“not valid package data”), and the snapshot is every relative entry and every file’s bytes. On this host the installation was absent before and after the replay.

The source pin copies `doctor_tests.rs`’s `production` reader verbatim: cut at `#[cfg(test)]\nmod tests`, then drop lines whose trim starts with `//`. It scans every `.rs` file under `apps/cli/src` (four files: `arguments.rs`, `bootstrap.rs`, `main.rs`, `terminal.rs`) and `host/src/outcomes.rs`, `doctor_ingress.rs`, `request.rs`, and `lib.rs`. None of the ten forbidden names appears. `apps/cli/src` does not name `installation_entry`. Under `crates/security/src`, `fn run_initial_creator(` and `fn admit_ordinary_writer(` each occur in exactly one production text, `custody/installation_routing.rs` and `custody/ordinary_writer.rs`, once each, as `pub(crate) fn`. `lib.rs` names neither. The test passed, so that is the tree at `bccb6b4`.

No production byte changes. No new feature, `cfg`, environment variable, or argument. `doctor_tests.rs` is untouched, so X10’s environment and `cfg` pin stays on X10’s files.

Item 7 is this file and one inventory row. There is no contract successor.

## Judgment calls

1. **Right.** A single inapplicable format stays human. Its JSON bytes exist only when JSON was selected first and the second format overwrites the twice-format failure. Pinning that pair is what “both formats” requires for row 4.
2. **Right.** Five competing orders per command and format assert the stdout the parser emits. The expected diagnostics match `arguments.rs`: a later failure replaces `failure`, and the `html|sarif|agent` arm replaces the twice-format failure while the `json` arm does not.
3. **Right.** Kind, termination, errors, and diagnostic are checked, and the whole stdout is compared. The hand-built JSON matches `Envelope7Root` and `Common4DomainDetail` field order. The replay accepted those bytes. That is item 1’s byte-for-byte refusal.
4. **Right.** Each `tests/*.rs` file is its own crate. A shared `tests/common` module would be a second inventory row and an edit to `doctor_tests.rs`. The copied reader’s body matches `doctor_tests.rs` lines 109–119, and its doc comment names that source.
5. **Right.** Walking every security `.rs` file, requiring one definition in the known owner as `pub(crate) fn`, and requiring `lib.rs` not to name the function, fails a second public wrapper. Both modules are `pub(crate) mod` in `custody.rs`. The function’s own visibility is the fact the law states.
6. **Right.** Item 6 adds `lib.rs` to the symbol scan. X10’s `cfg(test)` ban stays in `doctor_tests.rs`. `host/src/lib.rs` contains `#[cfg(test)] mod native_owner_tests`, which this reader does not cut, because the cutter looks for `mod tests`. Extending that ban would fail on a file the law does not put under it. The unit adds no production byte, which is item 6’s seam rule.
7. **Right.** `Command` sets `current_dir` and no environment. `doctor_tests.rs` does the same. `startup_tests.rs` clears the environment and plants release variables; that is an override, and these tests do not follow it. `HOME` is read only by `real_installation` in the test process.
8. **Right.** The snapshot is taken when the test starts, and every `run` requires equality. A new file anywhere under the scratch directory fails the tree compare. The comparison holds when the installation exists; here it was absent.
9. **Right.** “With or without further words” is the word alone, one trailing word, two trailing words, and a leading word. Each reaches the parser’s catch-all. `help … default` is in the table and in the test.
10. **Right.** M2 gives these flags no values. `--project=x11a` is one unknown dash token. `--project x11a` sets the same failure and then records `x11a` as a word, which the failure discards. Both are pinned on every command form, in human and JSON.
11. **Right.** Human help and `completion bash|zsh|fish` are pinned whole, so a catalogue edit fails them. JSON help pins the four rows’ name, usage, and summary. The rendered help and completion text matches `human_renderer.rs` and the four-row `catalogue()`.
12. **Right.** Eight placements put `--format` before, between, and after the words, and put the correlation id before and after, in both formats. For a one-word command, “between the first word and the rest” is the same argv as `--format=json` last; both runs still execute and take distinct ids. The file’s 821 runs completed in 28.91 seconds.

## Inventory v128

v128 adds exactly `apps/cli/tests/creator_commands_tests.rs` (`opensip-cli`, test, `generated: false`, `standing: proposed`). 948 v127 rows are equal by value. `packages`, `pendingDecisions`, and every top-level field other than `files` and `standing` are unchanged. `doctor_tests.rs` and `startup_tests.rs` rows are equal, including the startup description that begins “Exercise help/version with unavailable…”.

The worktree lock and the main checkout lock are the same document. The selected candidate is v127’s pin. The successor’s parent is that pin, its candidate is v128’s pin, `addedFiles` is the one path, and the four unchanged-graph flags are true. Carried obligations equal the v127 record.

The 55 projection rows are the same paths, `before` texts, and effective descriptions as v127’s projection. Each parent selector matches the lock’s inheritance row for v127. Each candidate selector is `/files/<new index>/description`, and the index is the old index plus one only for paths that sort after the inserted file. No passage supersession is bound to v127, so none is folded. D2’s four `after` texts are still the effective descriptions. The count stays 55.

Rebuilding the candidate in memory with `json.dumps(..., indent=2)` reproduces v128 byte for byte (`c6bcf2f4…`). `build_v128.py` was not executed against the arch tree.

`verify_projection.py` against the worktree lock: 55 rows, 278 corruptions refused. `verify_scratch.py` on the worktree: passed, 88 inventory successors, 74 contract successors, 55 inheritance rows, v128 selected. `check_package_edges --lane host` passes on v127 and on v128, 20 declared and 20 resolved edges.

## Replay

Private `TMPDIR` mode 0700 under `DARWIN_USER_TEMP_DIR`. `CARGO_TARGET_DIR` under this review directory, removed after the runs.

- `cargo test --locked --offline -p opensip-cli --test creator_commands_tests`: 7 passed, 0 failed, 28.91 seconds.
- `cargo clippy --locked --offline -p opensip-cli --all-targets -- -D warnings`: clean.
- `cargo fmt --all -- --check`: clean.

The workspace suite of 1688 tests and a workspace-wide clippy were not replayed. The product diff is this test file only, and that package’s tests, clippy, and rustfmt were run. The real OpenSIP home was absent before and after. Nothing was written in either repository.
