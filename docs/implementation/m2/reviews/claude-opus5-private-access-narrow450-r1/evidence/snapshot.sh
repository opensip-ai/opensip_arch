#!/bin/bash
# Outside-state snapshot for review claude-opus5-private-access-narrow450-r1 (read-only).
P=/Users/sb/code/opensip-ai/opensip; export GIT_OPTIONAL_LOCKS=0
(cd $P && shasum -a 256 crates/security/src/private_access.rs crates/security/src/lib.rs Cargo.lock design-lock.json)
echo "# product HEAD, status, index:"; git -C $P rev-parse HEAD; git -C $P status --porcelain; shasum -a 256 $P/.git/index
echo "# product target dir (mtime):"; stat -f '%m %N' $P/target $P/target/* 2>/dev/null
echo "# default cargo home global cache:"; stat -f '%m %z %N' ~/.cargo/.global-cache; shasum -a 256 ~/.cargo/.global-cache
