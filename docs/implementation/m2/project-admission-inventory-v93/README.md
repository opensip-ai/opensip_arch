# Project admission inventory93

Adds exactly two sources to inventory91 (unit X3b-1a, selected at product 7e676a9):
- crates/security/src/custody/project_admission.rs
- crates/security/src/custody/project_admission_tests.rs

It keeps all 763 existing rows by value, along with the packages and dependencies, the pending decisions and the carried unresolved obligations, for 765 planned files. No crate or dependency is added. The rows are unit X2b-1, law X2 r5 items 2 to 5: S3 root selection, the item 5 registry capture, `ProjectRootAdmission` and the registry owner's classification. Item 6a's tracking observation is unit X2b-2.

- project_admission.rs (composition) selects the project root by S3, walks its chain (X2a), samples its incarnation and marker, captures the registry once and classifies. The admission grants nothing until tracking exists.
- project_admission_tests.rs (test) checks it on scratch homes and through a real read session on a published scratch installation.

**Numbering and revision.** Grok accepted unit X2b-1 with inventory88 (r2, parent inventory87). verify_design needs a linear chain, and inventory91 (X3b-1a) was selected meanwhile, so inventory93 carries the same two added rows, byte for byte, on parent inventory91. inventory88 stays as reviewed. evidence/build_v93.py refuses to write over any path git already tracks.

**Changes to existing rows.** No existing row changes by value. These existing sources change, and their descriptions stay true:
- custody.rs gains only the `project_admission` module declaration;
- custody/project_chain.rs generalises its root judgment into `judge_project_object` (S3 directory or config-file custody under the premise) and exposes `open_refusal` and its `Failure` type;
- custody/installation_admission.rs records H's spelling as walked in `Chain` (charged), so the project chain starts from the same H the session walked;
- custody/installation_read.rs gains `ReadSession::admit_project_root` and `ProjectSessionRefusal`. Its inherited description ends "Nothing walks from the root again", which this entry makes false; an inventory successor cannot change an inherited row (verify_design rejects it), so the correction is for a description-only contract successor (as 461b), with the proposed text below;
- platform filesystem/directory_volume.rs publishes `directory_volume_observation_cost` (r2, RF-1), which the volume sample is charged at;
- platform filesystem/path_binding.rs gains `RetainedDirectoryPath::visit_directories_upward` for S3's upward walk.

**Proposed installation_read.rs description sentence** (replacing "Nothing walks from the root again."): "Captures never walk from the root again; `admit_project_root` alone walks from `/` to the launch or explicit path and the selected project root (law X2 r5, unit X2b-1), charged on the session ledger."

project_chain.rs's description still says the root takes S3 directory custody; it does not mention that `.opensip` and the config file now share that judgment. That understatement is for a later description-only successor.

**Projection.** The sixteen effective description overrides bound to inventory91 stay bound by stable file path, with parent inventory91. verify_projection.py is inventory84's helper with only its comment corrected, and runs against the real lock at 7e676a9, which selects inventory91. evidence/verify_scratch.py appends inventory93 in memory over the real lock, with a synthetic review and assent.
