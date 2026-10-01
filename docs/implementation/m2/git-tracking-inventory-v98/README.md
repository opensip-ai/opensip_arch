# Git tracking inventory98

Adds exactly two sources to inventory96 (unit X4T-a, selected at product fc7dce7):
- crates/security/src/custody/git_tracking.rs
- crates/security/src/custody/git_tracking_tests.rs

It keeps all 770 existing rows by value, along with the packages and dependencies, the pending decisions and the carried unresolved obligations, for 772 planned files. No crate or dependency is added (SHA-1 for the index checksum is implemented in the module). The rows are unit X2b-2, law X2 r7 item 6a and item 1's Git premise scope.

**Order.** This successor replaces inventory95 (parent inventory93, the r5 build) and is rebuilt on the current predecessor. inventory95 is left unchanged. Its two rows differ from inventory95's only where r7 changed the law: the system configuration sources are refusal-only evidence read without custody, and the tests cover that and an ordinary clone admitted with this host's real system sources. evidence/build_v98.py refuses to write over any path git already tracks, and while a lock selects inventory98.

**Changes to existing rows.** No existing row changes by value. These existing sources change, and their descriptions stay true:
- custody.rs gains only the `git_tracking` module declaration;
- custody/project_chain.rs exposes `ProjectChain::path` and `home_index`, and `ProjectChainPolicy::home_filesystem`;
- custody/installation_read.rs gains `ReadSession::observe_project_tracking` (and its `_with` form) and `TrackingSessionRefusal`;
- platform filesystem.rs and lib.rs export `observe_descriptor_metadata`, a status read as a full metadata sample, and `open_fixed_regular_following` (with its cost), which opens a fixed absolute path following links and requires a regular file; it proves no custody and is used only for evidence that can only refuse;
- platform filesystem/path_binding.rs gains `RetainedDirectoryPath::directory_at`.

installation_read.rs's inherited description already understates the session (X2b-1's `admit_project_root`); this entry adds to that, for the same later description-only successor.

**Projection.** The sixteen effective description overrides bound to inventory96 (carried unchanged from inventory94, 93, 91, 87, 84, 83, 82 and 81) stay bound by stable file path, with parent inventory96. verify_projection.py is inventory96's helper with only its comment corrected, and runs against the real lock at fc7dce7, which selects inventory96. evidence/verify_scratch.py appends inventory98 in memory over the real lock, with a synthetic review and assent.
