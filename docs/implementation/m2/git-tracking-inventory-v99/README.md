# Git tracking inventory99

Adds exactly two sources to inventory97 (unit X3b-1b, selected at product 46b1d60):
- crates/security/src/custody/git_tracking.rs
- crates/security/src/custody/git_tracking_tests.rs

It keeps all 772 existing rows by value, along with the packages and dependencies, the pending decisions and the carried unresolved obligations, for 774 planned files. No crate or dependency is added (SHA-1 for the index checksum is implemented in the module). The rows are unit X2b-2, law X2 r8 item 6a and item 1's Git premise scope.

**Order.** This successor supersedes inventory98 (parent inventory96, the r7 build, committed but never reviewed) and inventory95 (parent inventory93, the r5 build). Both are left unchanged. Its two rows differ from inventory98's only in naming law X2 r8, which changed item 1's wording but not item 6a, so the code is unchanged. evidence/build_v99.py refuses to write over any path git already tracks, and while a lock selects inventory99.

**Changes to existing rows.** No existing row changes by value. These existing sources change, and their descriptions stay true:
- custody.rs gains only the `git_tracking` module declaration;
- custody/project_chain.rs exposes `ProjectChain::path` and `home_index`, and `ProjectChainPolicy::home_filesystem`;
- custody/installation_read.rs gains `ReadSession::observe_project_tracking` (and its `_with` form) and `TrackingSessionRefusal`;
- platform filesystem.rs and lib.rs export `observe_descriptor_metadata`, a status read as a full metadata sample, and `open_fixed_regular_following` (with its cost), which opens a fixed absolute path following links and requires a regular file; it proves no custody and is used only for evidence that can only refuse;
- platform filesystem/path_binding.rs gains `RetainedDirectoryPath::directory_at`.

installation_read.rs's inherited description already understates the session (X2b-1's `admit_project_root`); this entry adds to that, for the same later description-only successor.

**Projection.** The sixteen effective description overrides bound to inventory97 (carried unchanged from inventory96 back to inventory81) stay bound by stable file path, with parent inventory97. verify_projection.py is inventory97's helper with only its comment corrected, and runs against the real lock at 46b1d60, which selects inventory97. evidence/verify_scratch.py appends inventory99 in memory over the real lock, with a synthetic review and assent.
