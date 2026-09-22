Actual Claude Opus 5 re-review after required findings on presence ACE 451. Grok leads. No repo edits, commits, pushes, or delegation. Write only under /tmp/opensip-implementation/reviews/claude-opus5-presence-ace451-r2. You own the serial native lane until the report is written. Rust is /opt/homebrew/Cellar/rust/1.95.0/bin. Use cargo --locked --offline in /Users/sb/code/opensip-ai/opensip. Do not read the private 413 UUID fixture.

The rejected marker is not in this diff. Product HEAD is a11f267. The uncommitted difference is test-only code in crates/platform/src/macos.rs (SHA256 21cf25969e36d8b5c4086f58e0e58be9a07b822f72e24cb10ee512a67f6da2f6, 14807 bytes) and crates/platform/src/filesystem/descriptor_acl_capture.rs (SHA256 4792507382b33f5b3f67a34ab302dc8646c983c1f225e577be0c6aff02227d1e, 33848 bytes).

RF-1: the group deny-delete marker is gone. The new helper appends one zero-rights allow for the file owner.
RF-2: it reads the existing extended ACL with acl_get_fd_np and appends. The test first installs an allow of right 2, then appends, and expects both rights 0 and 2. Owner unlink and rename-over succeed after the parent directory is chowned to the process gid.
RF-3: both helpers are cfg(test). cargo check -p opensip-platform --lib is warning-free. There is no production caller and no generic production writer.

The two leaked scratch directories named in the 451 review were removed after chmod -RN.

Owner saw 12 acl_capture tests pass. This is still not creator policy.

## What to decide

Read the diff against a11f267. Replay rustfmt --edition 2024 --check on both paths, cargo test --locked --offline -p opensip-platform --lib acl_capture_, and cargo check --locked --offline -p opensip-platform --lib. If you accept, review.json must contain top-level "verdict": "ACCEPT-UNIT" and requiredFindings []. Do not commit.
