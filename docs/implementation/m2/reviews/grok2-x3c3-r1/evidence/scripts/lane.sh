#!/bin/zsh
# usage: lane.sh <log name> <nice level> <command...>
# Takes the shared lanes lock (waiting in the background if held), runs the
# command in the X3c-3 worktree with the pinned toolchain and the private
# 0700 TMPDIR, releases the lock straight after.
set -u
S=/private/tmp/claude-501/-Users-sb-code/8baf40a9-970f-46bc-bd52-a3dde4a615a1/scratchpad/x3c3
name=$1; level=$2; shift 2
LOCK="$(getconf DARWIN_USER_TEMP_DIR)opensip-lanes.lock"
waited=0
# The lock is released only if this process's own mkdir took it (HELD=1).
HELD=0
release() { if (( HELD == 1 )); then HELD=0; rmdir "$LOCK" 2>/dev/null; fi }
trap release EXIT
trap 'release; exit 143' INT TERM
until mkdir "$LOCK" 2>/dev/null; do sleep 3; waited=$((waited+3)); done
HELD=1
cd /Users/sb/code/opensip-ai/opensip-x3c3
export PATH=/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:$PATH
export TMPDIR=$(cat $S/tmpdir.txt)/
start=$(date +%s)
nice -n $level "$@" > $S/logs/$name.log 2>&1
rc=$?
echo "$name exit=$rc seconds=$(( $(date +%s) - start )) waited=${waited} at=$(date -u +%FT%TZ)" | tee -a $S/logs/summary.txt
exit $rc
