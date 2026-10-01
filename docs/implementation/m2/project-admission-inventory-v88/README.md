# Project admission inventory88

Adds exactly two sources to inventory84 (unit X2a, selected at product 8bfc78a):
- crates/security/src/custody/project_admission.rs
- crates/security/src/custody/project_admission_tests.rs

It keeps all 758 existing rows by value, along with the packages and dependencies, the pending decisions and the carried unresolved obligations, for 760 planned files. No crate or dependency is added. The rows are unit X2b-1, law X2 r5 items 2 to 5: S3 root selection, the item 5 registry capture, `ProjectRootAdmission` and the registry owner's classification. Item 6a's tracking observation is unit X2b-2.

- project_admission.rs (composition) selects the project root by S3, walks its chain (X2a), samples its incarnation and marker, captures the registry once and classifies. The admission grants nothing until tracking exists.
- project_admission_tests.rs (test) checks it on scratch homes and through a real read session on a published scratch installation.

**Numbering.** v85 (X3b-1a) and v87 (X4T-0) are committed in arch on parent v84 but not selected; v86 is reserved. This unit is numbered v88 and built on v84. It is rebuilt and renumbered on the real predecessor at integration; evidence/build_v88.py is parameterised by its constants and refuses to write over any path git already tracks.

**Changes to existing rows.** No existing row changes by value. These existing sources change, and their descriptions stay true:
- custody.rs gains only the `project_admission` module declaration;
- custody/project_chain.rs generalises its root judgment into `judge_project_object` (S3 directory or config-file custody under the premise) and exposes `open_refusal` and its `Failure` type;
- custody/installation_admission.rs records H's spelling as walked in `Chain` (charged), so the project chain starts from the same H the session walked;
- custody/installation_read.rs gains `ReadSession::admit_project_root` and `ProjectSessionRefusal`;
- platform filesystem/path_binding.rs gains `RetainedDirectoryPath::visit_directories_upward` for S3's upward walk.

project_chain.rs's description still says the root takes S3 directory custody; it does not mention that `.opensip` and the config file now share that judgment. That understatement is for a later description-only successor.

**Projection.** The sixteen effective description overrides bound to inventory84 stay bound by stable file path, with parent inventory84. verify_projection.py is inventory84's helper with only its comment corrected, and runs against the real lock at 8bfc78a, which selects inventory84. evidence/verify_scratch.py appends inventory88 in memory over the real lock, with a synthetic review and assent.
