#!/bin/zsh
# usage: lead.sh <run-set prefix>
# One X3c-3 lead set (X9 r17 §RC.6; X9-6's recipe): storage's x9_6_matrix
# (403 rows) then host's x9_6_matrix (98 rows), each with its census, under
# ONE hold of the shared lanes lock, unniced. Before each target, no other
# cargo, rustc or test binary may be running (the 5,000 ms timing guard);
# a wait polls every 30 s and is recorded.
set -u
S=/private/tmp/claude-501/-Users-sb-code/8baf40a9-970f-46bc-bd52-a3dde4a615a1/scratchpad/x3c3
P=$1
LOCK="$(getconf DARWIN_USER_TEMP_DIR)opensip-lanes.lock"
mkdir -p $S/x9
waited=0
# The lock is released only if this process's own mkdir took it (HELD=1).
HELD=0
release() { if (( HELD == 1 )); then HELD=0; rmdir "$LOCK" 2>/dev/null; fi }
trap release EXIT
trap 'release; exit 143' INT TERM
until mkdir "$LOCK" 2>/dev/null; do sleep 3; waited=$((waited+3)); done
HELD=1
echo "$(date -u +%FT%TZ) $P lock taken after ${waited}s" >> $S/x9/waits.txt
cd /Users/sb/code/opensip-ai/opensip-x3c3
export PATH=/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:$PATH
export TMPDIR=$(cat $S/tmpdir.txt)/
echo "$P head $(git rev-parse HEAD) diff-sha256 $(git diff d2c00a9 | shasum -a 256 | cut -d' ' -f1)" >> $S/x9/$P.summary
busy() { ps -Ao pid=,command= | grep -E '(^|[ /])(cargo|rustc)( |$)|/deps/[A-Za-z0-9_]+-[0-9a-f]{16}' | grep -v -E 'grep -E' }
for t in storage host; do
  if [[ $t == storage ]]; then pkg=opensip-storage; tgt=commit_tests; else pkg=opensip-host; tgt=commit_matrix_tests; fi
  w=0
  while true; do
    found=$(busy)
    [[ -z $found ]] && break
    echo "$(date -u +%FT%TZ) $P-$t waiting on:" >> $S/x9/waits.txt; echo "$found" | cut -c1-200 >> $S/x9/waits.txt
    sleep 30; w=$(( w + 30 ))
  done
  echo "$(date -u +%FT%TZ) $P-$t load check clear after ${w}s wait" >> $S/x9/waits.txt
  start=$(date +%s)
  env OPENSIP_X9_RUN_SET=$P-$t OPENSIP_X9_RELEASE_ABSENCE=$S/release/release-absence.json nice -n 0 cargo test --locked --offline -p $pkg --features crash-matrix --test $tgt x9_6_matrix -- --exact --test-threads=1 > $S/x9/$P-$t.log 2>&1
  echo "$P-$t exit=$? seconds=$(( $(date +%s) - start )) waited=${w}" >> $S/x9/$P.summary
done
echo "$P head-after $(git rev-parse HEAD) diff-sha256 $(git diff d2c00a9 | shasum -a 256 | cut -d' ' -f1)" >> $S/x9/$P.summary
test ! -e "$HOME/Library/Application Support/OpenSIP" && echo "home absent" >> $S/x9/$P.summary
echo "$P LEAD-DONE" >> $S/x9/$P.summary
