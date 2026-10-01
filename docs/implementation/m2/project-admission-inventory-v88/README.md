# Project admission inventory88

Adds exactly two sources to inventory87 (unit X4T-0, selected at product 5b5f04c):
- crates/security/src/custody/project_admission.rs
- crates/security/src/custody/project_admission_tests.rs

It keeps all 760 existing rows by value, along with the packages and dependencies, the pending decisions and the carried unresolved obligations, for 762 planned files. No crate or dependency is added. The rows are unit X2b-1, law X2 r5 items 2 to 5: S3 root selection, the item 5 registry capture, `ProjectRootAdmission` and the registry owner's classification. Item 6a's tracking observation is unit X2b-2.

- project_admission.rs (composition) selects the project root by S3, walks its chain (X2a), samples its incarnation and marker, captures the registry once and classifies. The admission grants nothing until tracking exists.
- project_admission_tests.rs (test) checks it on scratch homes and through a real read session on a published scratch installation.

**Numbering and revision.** r2 rebuilds inventory88 on inventory87, the selected predecessor. evidence/build_v88.py refuses to write over any path git already tracks, except this unit's own r1 bytes (built on inventory84 and committed for review), which r2 replaces.

**Changes to existing rows.** No existing row changes by value. These existing sources change, and their descriptions stay true:
- custody.rs gains only the `project_admission` module declaration;
- custody/project_chain.rs generalises its root judgment into `judge_project_object` (S3 directory or config-file custody under the premise) and exposes `open_refusal` and its `Failure` type;
- custody/installation_admission.rs records H's spelling as walked in `Chain` (charged), so the project chain starts from the same H the session walked;
- custody/installation_read.rs gains `ReadSession::admit_project_root` and `ProjectSessionRefusal`. Its inherited description ends "Nothing walks from the root again", which this entry makes false; an inventory successor cannot change an inherited row (verify_design rejects it), so the correction is for a description-only contract successor (as 461b), with the proposed text below;
- platform filesystem/directory_volume.rs publishes `directory_volume_observation_cost` (r2, RF-1), which the volume sample is charged at;
- platform filesystem/path_binding.rs gains `RetainedDirectoryPath::visit_directories_upward` for S3's upward walk.

**Proposed installation_read.rs description sentence** (replacing "Nothing walks from the root again."): "Captures never walk from the root again; `admit_project_root` alone walks from `/` to the launch or explicit path and the selected project root (law X2 r5, unit X2b-1), charged on the session ledger."

project_chain.rs's description still says the root takes S3 directory custody; it does not mention that `.opensip` and the config file now share that judgment. That understatement is for a later description-only successor.

**Projection.** The sixteen effective description overrides bound to inventory87 stay bound by stable file path, with parent inventory87. verify_projection.py is inventory84's helper with only its comment corrected, and runs against the real lock at 5b5f04c, which selects inventory87. evidence/verify_scratch.py appends inventory88 in memory over the real lock, with a synthetic review and assent.
