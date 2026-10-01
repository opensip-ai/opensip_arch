# X2b-1 r3 — rebase re-check

Grok. Worktree `/Users/sb/code/opensip-ai/opensip-x2b` at `7e676a93567bfb5030e01cc11b56de6831f8d19c`. `hashes.txt` recomputed 21/21. The OpenSIP support directory is absent. `product.diff` is `git diff HEAD`: 75293 bytes, sha256 `0359beba4086060307bf45f834ab5239013405364da93a29ddb3e16921583564`, 10 `diff --git` headers, 1680 insertions, 8 deletions. The accepted r2 diff is 75293 bytes, sha256 `141d970e7da08eb422f24e21dc62eaa97091f4e987f827b627ca3a699ae7257c`.

## Rebase

Eight of the ten file diffs are byte-identical to r2: `directory_volume.rs`, `path_binding.rs`, `custody.rs`, `installation_admission.rs`, `installation_read.rs`, `project_admission.rs`, `project_admission_tests.rs`, and `project_chain.rs`. Those eight bases are unchanged from `5b5f04c` to `7e676a9` (the two admission sources are new). The working-tree bytes are the r2 bytes.

`filesystem.rs` and `lib.rs` differ from the r2 diff only in the index line and the hunk offset (`2357` to `2360`, `133` to `134`). Both bases changed between `5b5f04c` and `7e676a9` by X3b-1a's edits above the hunk. X2b-1's hunk in each is the same `directory_volume_observation_cost` re-export. `design-lock.json` at this HEAD selects inventory v91.

## Inventory v93

`repository-file-inventory.v93.json` is 330843 bytes, sha256 `8e3138b1cb15654391aea3d81e493d86bc46828ef56deac25fdb1bfda0c638b8`. Parent v91 is 328245 bytes, sha256 `c36f00e5e72744f56f60ef2cd21a2e6c2b028596463daa43efc94f73583ba1b4`. Successor `project-admission-inventory-v93/successor.json` is 20169 bytes, sha256 `bc2e804e8cb37f388d72ea956fd19b05f991ba059acfa2c616c7ca48080e5d8e`. Subject manifest `project-admission-inventory-v93-subject.json` is 2106 bytes, sha256 `9889a0f00eb9ed1529c1e42ee4ac1110836ac7674be2e88f3dd74c1bcfb4ca97`.

Rows 763 to 765. Added exactly `project_admission.rs` and `project_admission_tests.rs`, each byte-identical to the v88 row. Zero inherited row changes. Paths sorted. Packages and pending decisions unchanged. The standing sentence is this unit's own.

The sixteen projection rows are the same paths and the same effective text as v88. Each `before` equals the v91 description at the same selector, and the candidate row equals that `before`. The projection rule names inventory91. v88 is untouched.

The README still records the proposed `installation_read.rs` sentence, "Captures never walk from the root again; `admit_project_root` alone walks from `/` to the launch or explicit path and the selected project root (law X2 r5, unit X2b-1), charged on the session ledger." The inherited row still carries the older sentence, which an additive successor does not edit. `project_chain.rs` still leaves the configuration-file arm unstated, and no sentence there is false.

## Replay

Reviewer's own, Rust 1.95.0. `opensip-security` lib `project_admission`: 17 passed, 0 failed, 662 filtered out. `opensip-platform` lib `directory_volume`: 4 passed, 0 failed, 213 filtered out. Workspace suite, clippy, fmt, `check_package_edges`, and verify_scratch were not replayed. The cargo target was removed.

## Verdict

ACCEPT-UNIT. Inventory v93 ACCEPT.
