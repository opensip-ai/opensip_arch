#!/bin/zsh
# usage: set.sh <run-set prefix> [release-absence]
# X4-F2's X9 regression (law X4T r12 item 13): X9-6's run-set entry
# (`x9_6_matrix`, census then the selected rows), storage then host, limited
# by OPENSIP_X9_ROWS to the law's selection (x9-rows.py): 54 storage F00
# rows; for host a prefix that matches no row, so its census runs alone.
# Before each target's run, no cargo, rustc or test binary may be running:
# the 5 s timing guard must not run under load. A wait polls every 60 s and
# is recorded.
set -u
S=/private/tmp/claude-501/-Users-sb-code/8baf40a9-970f-46bc-bd52-a3dde4a615a1/scratchpad/x4f2
cd /Users/sb/code/opensip-ai/opensip-x4f2
export PATH=/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:$PATH
export TMPDIR=$(cat $S/tmpdir.txt)/
RA=${2:-}
busy() { ps -Ao pid=,command= | grep -E '(^|[ /])(cargo|rustc)( |$)|/deps/[A-Za-z0-9_]+-[0-9a-f]{16}' | grep -v -E 'grep -E' }
for t in storage host; do
  if [[ $t == storage ]]; then pkg=opensip-storage; tgt=commit_tests; else pkg=opensip-host; tgt=commit_matrix_tests; fi
  waited=0
  while true; do
    found=$(busy)
    [[ -z $found ]] && break
    echo "$(date -u +%FT%TZ) $1-$t waiting on:" >> $S/x9/waits.txt; echo "$found" | cut -c1-200 >> $S/x9/waits.txt
    sleep 60; waited=$(( waited + 60 ))
  done
  echo "$(date -u +%FT%TZ) $1-$t load check clear after ${waited}s wait" >> $S/x9/waits.txt
  start=$(date +%s)
  env OPENSIP_X9_RUN_SET=$1-$t OPENSIP_X9_ROWS=$(cat $S/x9/rows-$t.txt) ${RA:+OPENSIP_X9_RELEASE_ABSENCE=$RA} nice -n 0 cargo test --locked --offline -p $pkg --features crash-matrix --test $tgt x9_6_matrix -- --exact --test-threads=1 > $S/x9/$1-$t.log 2>&1
  echo "$1-$t exit=$? seconds=$(( $(date +%s) - start )) waited=${waited}" >> $S/x9/$1.summary
done
test ! -e "$HOME/Library/Application Support/OpenSIP" && echo "home absent" >> $S/x9/$1.summary
