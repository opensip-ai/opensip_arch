# Review: project chain X2a r2

Verdict: ACCEPT-UNIT.

Worktree `/Users/sb/code/opensip-ai/opensip-x2a` is at `99f1c35b50ddd7a3a2724d9acadf9c72f27ce7da`. Every pin in hashes.txt matches. `git diff` is 40876 bytes, sha256 `fec621e35496daa27d9f6c9a8e8c7c4478a24d03616dca8e3548363f59a60890`: the `project_chain` module declaration in `custody.rs`, plus `project_chain.rs` and `project_chain_tests.rs`. `store_endpoint` stays. The real OpenSIP support directory is absent.

## r1 RF-1

Closed. `same_birth` compares device, inode, birth seconds, and birth nanoseconds. `DirectoryBirthObservation`'s other metadata is not part of that comparison. `recheck` still reruns names, the three-band custody judgment, and the volume checks, then samples the birth again through `observe_birth`. A file created in the root, and `.opensip` created there, both pass. A renamed root and a different directory at the same name refuse `Changed`. A mode change on an ancestor still refuses through the ancestor custody row.

## r1 RF-2

Closed. `placement` compares borrowed path components and allocates no vector. `placement_cost` is 0 objects, 1 edge, and the two path lengths. The test records 0 objects for that charge. `spelling_cost` reserves 1 object and the root's byte length, and `WorkScope::run` charges it before `to_path_buf`. A ledger one object short of the completed walk refuses `WorkBudgetError::Objects`.

The 64-level walk charged `Cost { objects: 578, edges: 10937, bytes: 1093206 }`.

## Replay

Rust 1.95.0. `cargo test --locked --offline -p opensip-security --lib -- project_chain`: 17 passed, 0 failed, 618 filtered out. Workspace, clippy, fmt, `check_package_edges`, and `verify_scratch` were not replayed.

## Inventory

v84 is the r1 candidate, unchanged: 322464 bytes, sha256 `99b80dc4eb4790b380223c7eb575f9259f6fac69e0f33922ea7df1ab45653c2b`. Parent v83 is 320110 bytes, sha256 `4e32a2c7263b6ddcd938f42885b9e567fb13f759ba6871bf2c713b109894781a`. The successor record is 20152 bytes, sha256 `61ecb9224f30b7401862e1ff6dd55e127b1d7d0742b109de0d1bdc1097a581ae`. Verdict ACCEPT.
