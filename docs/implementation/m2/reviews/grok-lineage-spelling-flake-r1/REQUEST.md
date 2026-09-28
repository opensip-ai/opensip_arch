Grok review: test isolation (F1) and one shared lineage-path spelling (F2). Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-lineage-spelling-flake-r1.

Subject: the uncommitted working-tree changes in /Users/sb/code/opensip-ai/opensip. Pins are in hashes.txt, and the diff is saved as /tmp/opensip-implementation/reviews/grok-lineage-spelling-flake-r1/subject.diff. All six files already exist, so no inventory successor is needed. verify_design passes.

## F1: test isolation (test code only)

- **`installation_observation.rs`:** a test helper `settled(call, changed)` retries a setup call up to 8 times. It retries only on `Root(Descriptor(ChangedDuringRead))` or `Source(Custody(Descriptor(ChangedDuringRead)))`, the same pattern as d9d2779. Two calls use it:
  - `Fixture::fence()`, which is setup for every test that uses the fixture;
  - the `capture_descendant` that must succeed in `native_descendant_earlier_ancestor_changes_during_capture_and_consumption_refuse`.

  Every refusal assertion stays strict and is never retried.
- **`initial_installation.rs`:** `native_actor_is_charged_bound_and_rechecked` used `std::env::temp_dir()` without the scratch lock. It now uses `crate::test_scratch::temp_dir()`.

## F2: one lineage-path spelling

- **identity:** adds `LineageKey::relative_components() -> [String; 5]`, returning `["transitions", "lineage", S, G, "K.node"]`. The crate is `no_std`. A test pins generations 0, 17 and `i64::MAX` and schemas 1 and 2.
- **Callers:** lifecycle `relative_path`, security `node_path` (initial_manifest), and host `installation_lineage` now derive from it. The existing independent spelling test still passes. There is no new crate edge (`check_package_edges --lane host` passes).

## Results

- Workspace: 1075 passed, 0 failed, on two runs.
- clippy `-D warnings` and fmt are clean.

## Decide

Does F1 retry only setup, and never mask a refusal under test? Is F2's spelling byte-identical to the old join chain for every S, G and K, with no change in production behavior? Is anything else wrong?

review.json must contain top-level "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings" and "subjectSha256" (the sha256 of subject.diff). Write REVIEW.md and review.json. Do not commit.
