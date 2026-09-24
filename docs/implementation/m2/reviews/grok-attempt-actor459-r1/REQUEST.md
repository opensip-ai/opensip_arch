Grok review 459 r1: two subjects in one request, to save your budget. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-attempt-actor459-r1. You own the serial native lane until your report is written. Rust is /opt/homebrew/Cellar/rust/1.95.0/bin. Use cargo --locked --offline in /Users/sb/code/opensip-ai/opensip. Do not read or print the private 413 UUID fixture.

Write three files: REVIEW.md, premise458.json (subject A), and review.json (subject B). A finding in one subject does not block the other.

## Subject A — ACL omission premise, proposal 458 r2 (text)

/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/acl-omission-premise-458/PROPOSAL.md. Your r1 report and its RF-1 are in docs/implementation/m2/reviews/grok-omission-premise458-r1/. r2 requires the matched measured row to carry a signed member `installAclOmission: "no-acl-stored"`, set only after that boot identity passed the fixture set. A type name in `installRootFilesystems` is never enough. `InitialPlatform` takes the per-descriptor `fstatfs` itself. The member needs a profile-set schema successor (plan row 458b); until then omitted ancestors refuse. Decide whether RF-1 is closed and whether anything new is wrong. premise458.json: top-level "verdict" "ACCEPT" or "REQUIRED-FINDINGS", and "requiredFindings" with failure scenarios.

## Subject B — unit 459 source and inventory65

Product HEAD e7bd764. Pins of every changed path are in hashes.txt beside this request. `git status` must show exactly those paths.

1. **Attempt and actor.** New crates/security/src/initial_installation.rs, and `mod initial_installation` in lib.rs. `InitialInstallationAttempt::begin()` allocates one attempt per process (a static flag; a second call refuses even after drop). The attempt owns a `WorkLedger::new()` (the owner's caps) and a 16-byte lineage drawn after a charged entropy cost. `observe_actor` charges `observe_account_accounted`, requires equal real and effective UID, and a home spelling: `/` then nonempty components, no `.`/`..`, no trailing or doubled slash, each at most 255 bytes, and I's full path (home plus the four fixed components) within 4096 bytes and 256 components. `recheck_actor` re-observes and requires the same UID and home bytes. A receipt from another attempt refuses. Any refusal latches the attempt. Nothing opens a path.
2. **Obligations O1 and O6 from the inventory64 assent.** private_access.rs: production judges entries in place through `judge_private_descendant` with an entry lookup (no Vec). The slice form `assess_private_descendant` is `#[cfg(test)]` only. Refusal order is unchanged: state, entry presence, shape, entries.
3. **457 test leak.** Your 457 replay and mine left `opensip-ancestor457-*` directories: a deny-delete fixture cannot be removed by `remove_dir_all`. The scratch guard now runs `/bin/chmod -R -N` first. I removed the leftovers.
4. **Pre-existing full-suite flakiness.** `cargo test -p opensip-security --lib` (all tests) failed 2 of 3 runs at 1b3a3c6 and 3 of 3 at e7bd764 with `ChangedDuringRead`: tests creating temp entries run in parallel with tests whose root walk compares directory metadata. Earlier reviews ran filters. Every security test site now calls `crate::test_scratch::temp_dir()` (31 sites, 23 files), which takes one process-wide lock per test thread and keeps it until the thread exits, after the fixtures drop. The helper is `#[cfg(test)]`, so the non-test build proves every site is test code. Product walks and checks are unchanged. Cost: the full suite takes about 128 s instead of 48 s. Lead results after the change: see RESULTS below.
5. **Lint hygiene.** retained_metadata_index.rs drops a needless borrow. work_ledger.rs allows `new_without_default` with the reason: a `Default` would let `std::mem::take` swap a failed ledger for a fresh one in place. installation_lineage.rs (host test) uses `std::slice::from_ref`.
6. **Inventory65.** docs/implementation/m2/initial-installation-inventory-v65/ (README, successor.json, verification.*, verifier-anchor.json, verify_projection.py) and docs/implementation/m2/repository-file-inventory.v65.json. Subject manifest docs/implementation/m2/initial-installation-inventory-v65-subject.json. It adds exactly the new file at index 233; the two overrides after it move from 509/576 to 510/577. The projection helper is byte-identical to v64's and passed with 28 corruptions refused.

### Decide

- Is the attempt the single owner it claims to be? Can any path reset its ledger, mint an actor without the charged observation, or use a receipt across attempts?
- Is the home spelling rule right against owner §1b and §2 (no normalization; bounds counted on I)?
- Does the O1/O6 refactor keep every private-access refusal and order?
- Is the test lock sound (no deadlock, no silent skip, fixtures dropped under the lock)? Is anything in the product path changed?

### Replay

rustfmt --edition 2024 --check on every changed .rs path. Then `cargo test --locked --offline -p opensip-security --lib` once in full, and the filters initial_installation, external_ancestor, custody, private_access. `cargo test -p opensip-platform --lib work_ledger`, `--doc`. `cargo clippy --locked --offline --workspace --all-targets` (the lead saw zero warnings). Run `python3 -I -B docs/implementation/m2/initial-installation-inventory-v65/verify_projection.py --architecture /Users/sb/code/opensip-ai/opensip_arch --lock /Users/sb/code/opensip-ai/opensip/design-lock.json` from the architecture repository. Afterwards `find "$TMPDIR" -maxdepth 1 -name 'opensip-ancestor457-*'` should print nothing.

review.json must contain top-level "verdict" ("ACCEPT-UNIT" or "REQUIRED-FINDINGS"), "requiredFindings", "subjectManifestSha256" (SHA-256 of initial-installation-inventory-v65-subject.json), and "inventoryCandidateAssessment": {"verdict", "requiredFindings", "path", "bytes", "sha256" of repository-file-inventory.v65.json, "parent": {path, bytes, sha256 of v64}, "successorRecord": {path, bytes, sha256 of successor.json}}. Paths are relative to the architecture repository. Do not commit.

## RESULTS (lead, after the change, before this request)

- Full security lib suite: 10 runs after the lock; 9 passed all 428 (2 ignored), 1 run had one failure whose name was not captured. Before the lock: 1b3a3c6 failed 2 of 3 runs, e7bd764 failed 3 of 3, all with `ChangedDuringRead`. If you see a failure, name it; it is a finding if it is a missed walker or creator.
- Filters: initial_installation 5, external_ancestor 9, private_access 10, custody 55, retained_metadata_index 19, host installation_lineage 4, platform work_ledger 6, platform doc 2. Workspace clippy: 0 warnings. rustfmt check: clean. No `opensip-ancestor457-*` leftovers.
