#!/bin/zsh
# usage: locked.sh <name> <cmd...>
# Waits for the shared lane lock (mkdir), runs <cmd> in the J3a worktree with
# the pinned toolchain and the private 0700 TMPDIR, logs to $S/logs/<name>.log,
# and releases the lock straight after, only if this script's own mkdir took it.
set -u
S=/private/tmp/claude-501/-Users-sb-code/8baf40a9-970f-46bc-bd52-a3dde4a615a1/scratchpad/j3a
LOCK="$(getconf DARWIN_USER_TEMP_DIR)opensip-lanes.lock"
mkdir -p $S/logs
cd /Users/sb/code/opensip-ai/opensip-j3a
export PATH=/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:$PATH
export TMPDIR=$(cat $S/tmpdir.txt)/
name=$1; shift
waited=0
taken=0
until mkdir "$LOCK" 2>/dev/null; do sleep 2; waited=$(( waited + 2 )); done
taken=1
trap '[[ $taken == 1 ]] && rmdir "$LOCK" && taken=0' EXIT INT TERM
echo "$(date -u +%FT%TZ) $name lock taken after ${waited}s" >> $S/lock.log
start=$(date +%s)
"$@" > $S/logs/$name.log 2>&1; rc=$?
rmdir "$LOCK"; taken=0
echo "$(date -u +%FT%TZ) $name lock released rc=$rc seconds=$(( $(date +%s) - start ))" >> $S/lock.log
exit $rc
