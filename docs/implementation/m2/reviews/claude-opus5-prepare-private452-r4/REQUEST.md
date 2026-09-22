Actual Claude Opus 5 review of the shape-helper follow-up to accepted preparation 452 r3. Grok leads. No repo edits, commits, pushes, or delegation. Write only under /tmp/opensip-implementation/reviews/claude-opus5-prepare-private452-r4. You own the serial native lane until the report is written. Rust is /opt/homebrew/Cellar/rust/1.95.0/bin. Use cargo --locked --offline in /Users/sb/code/opensip-ai/opensip.

Product HEAD is 137d7e8. The uncommitted difference is only crates/security/src/private_access.rs, SHA256 ccfe2d0d288fb5657181ffd106d61745c4fcec2c11566cb071e34e83524c13d9, 25001 bytes.

private_shape now checks owner, exact mode, and file link count. Both the predicate and prepare_fresh_private_sample use it, so preparation no longer fabricates CapturedAclState::Entries(0). The prepare comment records that a zero-rights allow can remain if a later sample or predicate fails. The security test also prepares a fresh 0700 directory and expects one ACL entry. Owner saw 10 private_access tests pass.

## What to decide

Read the diff against 137d7e8. Replay rustfmt --edition 2024 --check on that path and cargo test --locked --offline -p opensip-security --lib private_access. If you accept, review.json must contain top-level "verdict": "ACCEPT-UNIT" and requiredFindings []. Do not commit.
