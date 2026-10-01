# X2d r2 — rebase onto 6dd7363, inventory v110 on v109

Rebase-only recheck of the accepted X2d r1 unit. No judgment call from r1 changes. Product worktree `/Users/sb/code/opensip-ai/opensip-x2d` is detached at `6dd736322d58d429d8783fcf09edc7daab7c816b`. `~/Library/Application Support/OpenSIP` is absent.

## Product bytes

The only commit after r1's `0206ce8` is `6dd7363`, X12b. Its diff is `crates/host/Cargo.toml`, `crates/host/src/configuration.rs`, `configuration_tests.rs`, `doctor_ingress.rs`, `lib.rs`, and `design-lock.json`. Nothing under `crates/security` changes.

The six product files match r1's pins, and the first six lines of this review's `hashes.txt` match r1's. `git diff` is byte-identical to r1: 75110 bytes, sha256 `90009b2e2fef312064a496bb7402b195146eebf03132876dd066544ce465bbb6`, 6 files, 1620 insertions, 20 deletions. The uncommitted change is still the four custody edits plus the two intent-to-add lease files.

X12b does not bear on this unit. Host policy-pack admission does not call namespace admission, and it adds no edge from security. The host crate's evaluator dependency is an ordinary dependency in the accepted v109 package graph, which v110 inherits unchanged. Security's edges stay identity, platform, and evaluator. There is still no edge to lifecycle.

## Inventory v110 on v109

Parent v109 is 360591 bytes, sha256 `96df355ac8333940a08402feb21e0065a485cd7fd9f128fd470a83677c639e7c`. Candidate v110 is 364396 bytes, sha256 `4d11a9d9578efa4dc0f6f963ff1d7a6cdc60c571087fadde8faed3438ecad6bc`. Subject manifest is 2135 bytes, sha256 `26f7e3f327e4694f480e2f6a50ab4abaad708da5b9f5891e12cb3ee5977f391d`. Successor record is 20199 bytes, sha256 `1903fc699caa6907325387bace6588b4a6e1767b07e9e4b0123d6bd0132e9a4d`, and its parent pin is v109.

All 786 v109 file rows are equal by value. The only added paths are `namespace_lease.rs` and `namespace_lease_tests.rs`, 788 files in all. `packages`, `pendingDecisions`, and the carried obligations are the parent's. The standing sentence is the v110 header. The sixteen projection rows are rebound by file path to v109.

`build_v110.py` maps both admissible parents: v105 to the X2c successor, and v109 to `policy-pack-x12b-inventory-v109/successor.json`. The two added row texts are the r1 texts. The worktree lock and `/Users/sb/code/opensip-ai/opensip/design-lock.json` are the same 174013 bytes, sha256 `64f447eff3359573900157edee3402b5e2cc4ca3b5a9da7660872040cedb29d0`, and both select v109, which is the verifier anchor. The builder was not rerun, because it writes the candidate and the successor into the architecture tree. README, `verifier-anchor.json`, and the comments in `verify_scratch.py` and `verify_projection.py` name 6dd7363 and v109. Their checks are the same checks.

`verify_projection` against the worktree lock: 16 rows, 83 corruptions refused. `verify_scratch` appending v110 over that lock: passed, 72 inventory successors, 72 contract successors, 16 inheritance rows, v110 selected. `check_package_edges --lane host` against v110 passed. `rustfmt --check --edition 2024` passed on the two new files and on `first_registration.rs`. The workspace suite and workspace clippy were not replayed; the X2d sources are the accepted r1 bytes, and the base commit does not compile into them.

## Verdict

ACCEPT-UNIT. Inventory v110 is ACCEPT on v109. No required findings.
