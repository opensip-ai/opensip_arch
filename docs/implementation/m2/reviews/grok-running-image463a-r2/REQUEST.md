Grok re-review 463a r2 after your r1 RF-1. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-running-image463a-r2. You own the serial native lane until your report is written. Rust is /opt/homebrew/Cellar/rust/1.95.0/bin. Use cargo --locked --offline in /Users/sb/code/opensip-ai/opensip. Do not read or print the private 413 UUID fixture.

Product HEAD cd48f87; the r1 bytes were not committed. Pins of the four paths are in hashes.txt beside this request. lib.rs and macos_loader.rs are the r1 bytes. Inventory67 and its subject manifest are unchanged from r1, where you accepted the layout.

## Changes

- filesystem.rs: new `RetainedDirectory::open_regular_cost(relative)`, next to `open_regular`: one parent `dup`, and per component a NUL-terminated name, one `openat` and one kind-check status read with its buffer. Nothing else in filesystem.rs changed.
- macos_image.rs: the leaf open is charged `open_regular_cost(leaf)` plus the caller's status read; `recheck` is charged `open_regular_cost(leaf)` plus the reopened and held status reads; `kernel_path` now splits the path and makes both leaf copies inside the charged path step, whose reservation covers four 4096-byte buffers; the file-read cost no longer double-counts the open. A test pins the counts: `open_regular` of one leaf is 3 objects and 3 edges, the leaf step 4 edges, the recheck 5 edges, with the name, NUL and status buffers.

## Decide

Is RF-1 closed? Is any status read, copy or allocation still outside its reservation? Anything new wrong? Replay at least rustfmt, the platform lib suite and workspace clippy.

review.json must contain top-level "verdict", "requiredFindings", "subjectManifestSha256" (SHA-256 of running-image-inventory-v67-subject.json, unchanged) and "inventoryCandidateAssessment" as in r1. Write REVIEW.md and review.json. Do not commit.
