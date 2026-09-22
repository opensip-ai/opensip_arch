#!/bin/bash
# Outside-state snapshot for review claude-opus5-capture-gaps449-r1 (read-only).
W=/tmp/opensip-implementation/capture-gaps449; WT=/Users/sb/code/opensip-ai/opensip/.git/worktrees/capture-gaps449
export GIT_OPTIONAL_LOCKS=0
(cd $W && shasum -a 256 crates/platform/src/filesystem/descriptor_acl_capture.rs Cargo.lock Cargo.toml crates/platform/Cargo.toml)
echo "# worktree HEAD/status:"; git -C $W rev-parse HEAD; git -C $W status --porcelain
echo "# worktree admin index/HEAD:"; shasum -a 256 $WT/index $WT/HEAD
echo "# worktree target dir (mtime):"; stat -f '%m %N' $W/target $W/target/* 2>/dev/null
echo "# default cargo home global cache:"; stat -f '%m %z %N' ~/.cargo/.global-cache; shasum -a 256 ~/.cargo/.global-cache
