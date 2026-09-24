Grok source review 460 r1: the read half of owner step 5, the creator-side observation of I's parent chain. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-parent-observation460-r1. You own the serial native lane until your report is written. Rust is /opt/homebrew/Cellar/rust/1.95.0/bin. Use cargo --locked --offline in /Users/sb/code/opensip-ai/opensip. Do not read or print the private 413 UUID fixture.

Product HEAD is 9c53c94. Pins of the seven changed paths are in hashes.txt beside this request; `git status` must show exactly those. No new file, so no inventory successor. Owner text: /Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/initial-root-binding-owner-selection-v1/owner.md §1a step 5, §1b, §2 (budget) and §3. Accepted premise law: docs/implementation/m2/acl-omission-premise-458/PROPOSAL.md.

## The unit

Platform (charged mechanisms, no policy):
- `retained_path_open_cost(path)` counts components from the raw bytes (one per slash) before any parse, allocation or open, and covers the root handle, one handle per component, the component and edge vectors, the NUL-terminated names and the closing recheck. `RetainedDirectoryPath::open_accounted` charges it first. `component_count`, `visit_directories` (root-to-leaf, no descriptor escapes), `recheck_exact_names_cost` and `recheck_exact_names_accounted`.
- `RetainedDirectory::open_child_directory_if_present_accounted` returns `None` for NotFound without failing the work scope (a `run` error latches the ledger, so an expected "missing" must not travel as an error). Other errors, including a symlink (ELOOP) or a file (ENOTDIR), fail the scope.
- `RetainedDirectory::observe_child_absent` uses `fstatat(..., AT_SYMLINK_NOFOLLOW)`: only ENOENT is absence; any entry, including a dangling symlink, is presence; other errors are returned. Charged wrapper too.
- `descriptor_filesystem_observation_cost` and `observe_filesystem_accounted`.

Security:
- initial_installation.rs: the attempt gains `run` (charged work for other owners on its one ledger; refused once latched; any failure latches), `lineage`, `require_lineage` (a mismatch latches), `InitialActor::lineage`, and a `#[cfg(test)]` `for_tests` constructor. `begin_with`/`begin_on` stay private, so production still has only `begin`. The row text for this file (it opens no path) stays true.
- custody/installation_root.rs (row: "resolve the fixed installation root from the actual account database and retain its existing or missing-path evidence") gains `observe_installation_parent(attempt, actor, premise)`: retain root-to-H with the charged open; capture and judge every component with `check_external_ancestor`; an omitted ACL is `AncestorAclOmitted` unless an `AclOmissionPremise` admits that descriptor's own filesystem sample (local, not union, qualified type name); then `Library` and `Application Support` as external ancestors and `OpenSIP` with `observe_private_directory`; each child's native name must match; the outcome is the first missing fixed ancestor, `preview-v1` positively absent through the retained `OpenSIP` handle, or `preview-v1` present; then a second name check on every retained child, `recheck_exact_names` on the chain, and `recheck_actor`. `AclOmissionPremise` has only a `#[cfg(test)]` constructor (plan unit 462 mints the real one from a signed row), so in production every omitted ancestor refuses. On a stock Mac this observation therefore refuses at `/`.
- The existing read-only `RootObservation` walk and its legacy writer-list chain are unchanged.

## Decide

1. Is the charge taken before every open, capture, name sample and filesystem sample? Is any work uncounted, or any allocation made before its reservation?
2. Can the walk admit an ancestor it should refuse: an omitted ACL without a premise, a premise for another attempt, a symlink component, a renamed component, a non-private `OpenSIP`, a group-writable H?
3. Is `preview-v1` absence positive and through the retained parent? Is any entry at that name, including a dangling symlink, reported as present?
4. Does `run` or `require_lineage` open a way to reset the ledger, avoid the latch, or begin a second attempt?
5. Does anything read as creation permission, a barrier receipt, or Evidence B being available?

## Lead results

rustfmt check clean; workspace clippy 0 warnings; `cargo test -p opensip-platform --lib` 162 passed; `cargo test -p opensip-security --lib` 433 passed, 2 ignored; focused filters `initial_installation creator_parent installation_root` 19 passed; no `opensip-parent460-*` or `opensip-ancestor457-*` leftovers. Replay at least: rustfmt check, the platform lib suite, the security filters `creator_parent`, `initial_installation`, `installation_root`, platform filters `accounted child_absence`, and workspace clippy. The full security suite takes about 130 s; run it if your budget allows.

review.json: top-level "verdict" "ACCEPT-UNIT" or "REQUIRED-FINDINGS", and "requiredFindings" (each with a failure scenario). Write REVIEW.md and review.json. Do not commit.
