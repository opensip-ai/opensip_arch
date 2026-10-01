# Review: project chain X2a with inventory v84

Verdict: REQUIRED-FINDINGS. Two code findings. Inventory v84 is accepted.

Worktree `/Users/sb/code/opensip-ai/opensip-x2a` is HEAD `84a8bfd7b4f28a52fc18bc9e66e02d1f40330d2c`. `product.diff` is `git diff` of that worktree, including the two intent-to-add sources: 36777 bytes, sha256 `c036b0b1f509af459dbbd7e21b2f86514998d622b5e781ef0670c6f19c9d4f81`. The diff is `custody.rs` (the `project_chain` module declaration only) plus `project_chain.rs` and `project_chain_tests.rs`. The real OpenSIP support directory was absent before the verifiers, before the tests, and after the tests.

Law is X2 r5. This unit is the unit-list entry X2a: the scoped premise, the charged birth sample, and the project chain walk (items 1 to 3, the custody half of item 4, and item 9). `ProjectRootAdmission`, selection, the registry, tracking, and public projection are X2b.

## Required findings

RF-1. Recheck treats a change of mtime, ctime, or link count as a birth mismatch.

`ProjectChain::recheck` samples birth again and refuses `Changed` when the new `DirectoryBirthObservation` is not equal to the retained one. That type's equality includes `DescriptorMetadata`, and the metadata includes mode, link count, size, mtime, and ctime. Creating a file in the admitted root changes mtime and ctime. Creating `.opensip` also changes the link count. Device, inode, and native birth stay the same, and the custody judgment still passes. `row()` then reports `PROJECT.ROOT_CUSTODY_REFUSED` subject `name-changed`.

Item 3 rechecks the chain as 468 item 3 does: identity, name, and custody, with this chain added. Identity in that recheck is device and inode. Item 4's root identity adds native birth (and the volume UUID, which is X2b's sample). The birth observation's metadata is the bracket around `fgetattrlist`, so a change during that one call fails the sample. It is not a second identity. The forbidden-substitutes list names mtime and ctime as birth substitutes. Item 6 step 6 rechecks this same chain after creating `.opensip`.

Required: the birth matches when device, inode, birth seconds, and birth nanoseconds match. A real change of those fields still refuses. Mode, owner, and ACL stay in the custody judgment this recheck already reruns. Names stay in the name recheck. Volume stays in the volume check.

RF-2. Placement and the retained spelling allocate outside their charges.

`placement_cost` reserves 0 objects, 1 edge, and the two path lengths in bytes. Inside that reservation, `placement` builds two `Vec<Vec<u8>>` and one `Vec<u8>` per component of H and of the root. The platform's own path cost counts each vector as an object and its buffer as bytes. A ledger with no objects remaining, and with one edge and the path lengths remaining, still runs placement and allocates those vectors.

After the last charge, `walk_project_chain` copies `root.to_path_buf()` into `ProjectChain.spelling` with no reservation. Item 9 charges every step before it runs. The spelling is part of the chain the walk returns.

The 64-level test's ledger total is the charged total only: 577 objects, 10937 edges, 1092854 bytes. The half-cap assertion reads that total. It does not see the vectors or the spelling copy.

Required: reserve the component vectors in `placement_cost` before they are allocated (one object per vector, and bytes for the outer buffers and the copied components), and reserve the retained spelling before the copy. A comparison that does not allocate closes the placement half.

## Judgment calls

1. Acceptable. There is no `InstallationTermination` and no host projection. `row()` names item 8's row and subject for X2b. `ProjectChain` is `pub(crate)`, not `Clone`, and its `Debug` prints no fields.

2. Acceptable. On this host, `open` and `openat` of a symlink with `O_RDONLY | O_DIRECTORY | O_NOFOLLOW | O_CLOEXEC | O_NONBLOCK` return `ENOTDIR` (20). A regular file returns the same errno. `ELOOP` is 62 and is not what this open returns. `ErrorKind::NotADirectory` therefore takes `PROJECT.EXPLICIT_PATH_INVALID`, which is S3's row for a path that is not a directory. Raw 62 still takes subject `symlink`. The walk does not follow the link.

3. Acceptable. A relative path, `.`, `..`, an empty component, a missing path, and a non-directory are `PROJECT.EXPLICIT_PATH_INVALID`. S3's explicit-path cases use that code for an absent path and for a file. A root that is H, above H, beside H, or inside `Library/Application Support/OpenSIP` (ASCII case-insensitive, including the directory itself and descendants) is `outside-home`, and that check runs before any open.

4. Acceptable. Every directory from H through the root is checked with the borrowed H-filesystem predicate, including directories whose ACL is present so the premise is not consulted. Ancestors above H stay on the 468 step 0 judgment, which is item 3's rule for `/` through H.

5. Acceptable. X2a samples native birth with `RetainedDirectory::observe_birth`, charged before the call (`BIRTH_COST`: 0 objects, 3 edges, 1536 bytes). `std::fs::Metadata` on this host is 144 bytes, so 512 bytes per bracketed read covers the status buffers. Unsupported or unreliable birth is `birth-unsupported`. There is no mtime or ctime fallback. Device and inode are inside the birth observation's metadata. `DirectoryVolumeObservation` is a separate sampler on the retained descriptor. The unit list gives `ProjectRootAdmission`, which is where item 4 stores the APFS volume UUID, to X2b.

6. Acceptable. Against `84a8bfd`, `custody.rs` gains only the module declaration. The two new files are the rest of the diff. This does not edit the store-endpoint walk from X3a-1.

## What matches the law

Placement is lexical and first. The root must extend H by exact component bytes. The installation suffix is refused in any ASCII case, and a sibling of `OpenSIP` is not refused for placement. The open uses `open_project_root` at 256 components. Ancestors through the parent of the root use `judge_ancestor` and the borrowed premise. The root uses S3 directory custody: the shared `check` with the trust groups, then each ACL entry. A write allow must name the invoking user, root, or a trusted group. Read-only allows and denies pass. Unknown flags or a missing entry are `acl-unreadable`. An omitted ACL is an empty ACL only when `AclOmissionPremise::admits` accepts that descriptor. Trust groups do not waive the ancestor predicate. The premise is borrowed, not built. Nothing is created.

`row()` uses item 8's subjects for custody (`outside-home`, `foreign-owner`, `mode`, `acl-unreadable`, `acl-write`, `symlink`, `not-a-directory`, `custody`, `name-changed`, `volume-unsupported`, `birth-unsupported`), `PROJECT.EXPLICIT_PATH_INVALID` for a bad path, and the host I/O row for I/O. Budget failures stay `WorkFailure::Budget`.

## Inventory v84

v84 is v83 plus the two new source rows. All 756 v83 rows match by value, including descriptions. Packages, dependencies, and pending decisions match. `custody.rs` keeps its description. Parent pin: `repository-file-inventory.v83.json`, 320110 bytes, sha256 `4e32a2c7263b6ddcd938f42885b9e567fb13f759ba6871bf2c713b109894781a`. Candidate: 322464 bytes, sha256 `99b80dc4eb4790b380223c7eb575f9259f6fac69e0f33922ea7df1ab45653c2b`. Successor record: `project-chain-inventory-v84/successor.json`, 20152 bytes, sha256 `61ecb9224f30b7401862e1ff6dd55e127b1d7d0742b109de0d1bdc1097a581ae`. Subject manifest sha256 `e6cf13fefccc40e1a7303601e2efcba1e2130fb825e0f1716e038291d8ac89a6`.

`verify_projection.py` against a scratch lock that selects v83: PASS, 16 rows, 83 corruptions refused. `verify_scratch.py` on this worktree: passed, and the selected inventory is v84. The verifier anchor matches `verify_design.py` and `design-lock.json` at this HEAD. v83 stays the parent under review with X3a-1. These bytes are the parent this candidate claims, and this candidate does not edit them.

## Replay

rustc 1.95.0 (Homebrew). `cargo test --locked --offline -p opensip-security --lib project_chain`, `CARGO_TARGET_DIR` under this review directory: 14 passed, 0 failed. The 64-level ledger line is the total quoted under RF-2. Workspace suite, clippy, fmt, and `check_package_edges` were not replayed. The passing tests do not close RF-1 or RF-2: the recheck test renames and replaces the directory, and the budget test reads the charged total.
