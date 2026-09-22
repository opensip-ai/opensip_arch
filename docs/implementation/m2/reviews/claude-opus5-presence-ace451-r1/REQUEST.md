Actual Claude Opus 5 source review. One reviewer. Grok leads. No repo edits, commits, pushes, or delegation. Write only under /tmp/opensip-implementation/reviews/claude-opus5-presence-ace451-r1. You own the serial native lane until the report is written. Rust is /opt/homebrew/Cellar/rust/1.95.0/bin. Use cargo --locked --offline in /Users/sb/code/opensip-ai/opensip. Do not read the private 413 UUID fixture.

Product HEAD is a11f267. The uncommitted difference is only crates/platform/src/macos.rs (SHA256 edcbaed9494b01995111671cfedfdb78311c8d20103625573d7d49d5a9d1f679, 13601 bytes) and crates/platform/src/filesystem/descriptor_acl_capture.rs (SHA256 7238923b40d614d87da385ec5aa14f1dfdcf890c9e63b17e430856329c749660, 33031 bytes). Confirm with git diff.

macos.rs adds install_non_granting_presence_ace, which replaces the descriptor ACL with one group deny of delete (tag 2, mask 1<<4) for the file's own group id. install_single_ace is the shared writer. set_probe_acl remains test-only and calls that writer. This is a presence marker so a later capture can return Entries rather than NotReturned. It is not creator policy, not an absence proof, and it is not wired to the creator or to private_access.

The new capture test installs that ACE on a fresh 0600 file and expects Entries(1), deny in the low flag nibble, rights exactly 1<<4, and a Group principal. Owner saw 12 acl_capture tests pass.

## What to decide

Read the diff. Replay rustfmt --edition 2024 --check on both paths and cargo test --locked --offline -p opensip-platform --lib acl_capture_. If you accept this source boundary, review.json must contain top-level "verdict": "ACCEPT-UNIT" and requiredFindings []. Do not commit. Say whether replacing the whole ACL with one deny is an acceptable presence marker, or whether that replacement itself is a required finding because it discards other ACEs.
