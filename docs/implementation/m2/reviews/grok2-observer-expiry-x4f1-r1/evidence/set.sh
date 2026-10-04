#!/bin/zsh
# usage: set.sh <run-set prefix> [release-absence]
# X4-F1's X9 regression: X9-6's run-set entry (`x9_6_matrix`, census then the
# selected rows) limited by OPENSIP_X9_ROWS to the rows rows.py computed.
set -u
S=/private/tmp/claude-501/-Users-sb-code/8baf40a9-970f-46bc-bd52-a3dde4a615a1/scratchpad/x4f1
cd /Users/sb/code/opensip-ai/opensip-x4f1
export PATH=/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:$PATH
export TMPDIR=$(cat $S/tmpdir.txt)/
RA=${2:-}
for t in storage host; do
  if [[ $t == storage ]]; then pkg=opensip-storage; tgt=commit_tests; else pkg=opensip-host; tgt=commit_matrix_tests; fi
  start=$(date +%s)
  env OPENSIP_X9_RUN_SET=$1-$t OPENSIP_X9_ROWS=$(cat $S/rows-$t.txt) ${RA:+OPENSIP_X9_RELEASE_ABSENCE=$RA} cargo test --locked --offline -p $pkg --features crash-matrix --test $tgt x9_6_matrix -- --exact --test-threads=1 > $S/$1-$t.log 2>&1
  echo "$1-$t exit=$? seconds=$(( $(date +%s) - start ))" >> $S/$1.summary
done
test ! -e "$HOME/Library/Application Support/OpenSIP" && echo "home absent" >> $S/$1.summary
