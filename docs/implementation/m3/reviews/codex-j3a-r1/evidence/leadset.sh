#!/bin/zsh
# usage: leadset.sh <run-set prefix> <storage|host>
# One full crash-matrix lead set (X9-6's run-set entry `x9_6_matrix`, census
# then every required run; no OPENSIP_X9_ROWS), run by locked.sh so the lane
# lock is held for the whole set. Unniced (nice -n 0). Before it starts, no
# cargo, rustc or test binary may be running on the machine (the 5000 ms
# timing guard): a wait polls every 30 s and is recorded.
# (X4-F3's leadset.sh, with this unit's paths.)
set -u
S=/private/tmp/claude-501/-Users-sb-code/8baf40a9-970f-46bc-bd52-a3dde4a615a1/scratchpad/j3a
cd /Users/sb/code/opensip-ai/opensip-j3a
set_=$1; t=$2
if [[ $t == storage ]]; then pkg=opensip-storage; tgt=commit_tests; else pkg=opensip-host; tgt=commit_matrix_tests; fi
# Running executables only (`comm`): cargo, rustc, clippy and test binaries.
# Another agent's lane script waiting for the lock is not load.
busy() { ps -Ao pid=,comm= | grep -E '(^|/| )(cargo|rustc|cargo-clippy|clippy-driver)$|/deps/[A-Za-z0-9_]+-[0-9a-f]{16}$' }
waited=0
while true; do
  found=$(busy); [[ -z $found ]] && break
  echo "$(date -u +%FT%TZ) $set_-$t waiting on:" >> $S/x9/waits.txt; echo "$found" | cut -c1-200 >> $S/x9/waits.txt
  sleep 30; waited=$(( waited + 30 ))
done
echo "$(date -u +%FT%TZ) $set_-$t load check clear after ${waited}s wait" >> $S/x9/waits.txt
start=$(date +%s)
env OPENSIP_X9_RUN_SET=$set_-$t OPENSIP_X9_RELEASE_ABSENCE=$S/release/release-absence.json nice -n 0 cargo test --locked --offline -p $pkg --features crash-matrix --test $tgt x9_6_matrix -- --exact --test-threads=1 > $S/x9/$set_-$t.log 2>&1
rc=$?
echo "$set_-$t exit=$rc seconds=$(( $(date +%s) - start )) waited=${waited}" >> $S/x9/x9.summary
test ! -e "$HOME/Library/Application Support/OpenSIP" && echo "home absent" >> $S/x9/x9.summary
exit $rc
