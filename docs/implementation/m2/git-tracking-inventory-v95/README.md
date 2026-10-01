# Git tracking inventory95

Adds exactly two sources to inventory93 (unit X2b-1, selected at product 8452ab9):
- crates/security/src/custody/git_tracking.rs
- crates/security/src/custody/git_tracking_tests.rs

It keeps all 765 existing rows by value, along with the packages and dependencies, the pending decisions and the carried unresolved obligations, for 767 planned files. No crate or dependency is added (SHA-1 for the index checksum is implemented in the module). The rows are unit X2b-2, law X2 r5 item 6a and item 1's Git premise scope.

**Numbering.** v94 (ledger creation) and v96 (current trust) are in flight on other parents. This unit is v95 on v93, rebuilt on its real predecessor before integration if needed. evidence/build_v95.py refuses to write over any path git already tracks.

**Changes to existing rows.** No existing row changes by value. These existing sources change, and their descriptions stay true:
- custody.rs gains only the `git_tracking` module declaration;
- custody/project_chain.rs exposes `ProjectChain::path` and `home_index`, and `ProjectChainPolicy::premise` and `home_filesystem`;
- custody/installation_read.rs gains `ReadSession::observe_project_tracking` (and its `_with` form) and `TrackingSessionRefusal`;
- platform filesystem.rs and lib.rs export `observe_descriptor_metadata`, a status read as a full metadata sample;
- platform filesystem/path_binding.rs gains `RetainedDirectoryPath::directory_at`.

installation_read.rs's inherited description already understates the session (X2b-1's `admit_project_root`); this entry adds to that, for the same later description-only successor.

**Known law gap (reported).** Item 1's custody rule for the system configuration sources meets stock macOS at `/`: the root directory is on the sealed system volume (not H's), omits its ACL, and so refuses under "an object not on H's volume must carry a readable ACL". `/etc` is a symbolic link, so `/etc/gitconfig` cannot be walked no-follow, and `/opt/homebrew/etc` is user-owned and group-writable. The code follows the law as written, so the production entry refuses every repository on a stock Mac until the law is amended.

**Projection.** The sixteen effective description overrides bound to inventory93 stay bound by stable file path, with parent inventory93. verify_projection.py runs against the real lock at 8452ab9, which selects inventory93. evidence/verify_scratch.py appends inventory95 in memory over the real lock, with a synthetic review and assent.
