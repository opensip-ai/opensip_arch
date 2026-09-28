# Review: lineage spelling and test isolation

Grok is the single reviewer. Claude Opus 5.5 leads. Review of the uncommitted test-isolation and lineage-path changes. No repository edits.

The six files match `hashes.txt`. `subject.diff` is the git diff of those files, 8375 bytes, sha256 `747ce6c18c72815e40a812c8e09d0ef10a620999eb19c73fad0e6d43d4835caf`. No inventory row is added.

## Verdict

**ACCEPT.**

## F1

`settled` runs the call at most eight times and returns on the first result that is not the named `ChangedDuringRead`. Any other error is returned at once. After eight of those samples it stops rather than succeeding. The only uses are `Fixture::fence()`, which is fixture setup, and the `capture_descendant` that must succeed before `native_descendant_earlier_ancestor_changes_during_capture_and_consumption_refuse` mutates the tree. The refusal assertions in that test, `capture_descendant_with(...).is_err()` and `captured.bytes().is_err()`, are outside `settled`. `native_actor_is_charged_bound_and_rechecked` creates its probe through `test_scratch::temp_dir()`, which takes the scratch lock, and still deletes the probe. Production code is unchanged.

## F2

`LineageKey::relative_components` returns `transitions`, `lineage`, the store string, `generation.to_string()`, and `{schema}.node`. `parse` rejects a negative generation, and schema is only 1 or 2, so those are the same bytes as the old joins. `relative_path`, `node_path`, and the host descendant capture all take that array. The lifecycle test still compares `relative_path` with its own `transitions/lineage/{store}/{g}/{k}.node` literal for generations 0, 1 and `i64::MAX` and schemas 1 and 2. The identity test pins 0, 17 and `i64::MAX`. No `Cargo.toml` changes, so the host lane gains no crate edge. The identity crate builds the strings from `alloc`.
