#!/bin/zsh
# X4-F2's X9 regression on 3f6f9a5 + the X4-F2 diff, serially: release
# absence, then two run sets of the law's selection (storage then host, each
# with its census), then the comparison with the accepted X9-6 evidence.
set -u
S=/private/tmp/claude-501/-Users-sb-code/8baf40a9-970f-46bc-bd52-a3dde4a615a1/scratchpad/x4f2
cd /Users/sb/code/opensip-ai/opensip-x4f2
: > $S/x9/x9.summary
echo "head $(git rev-parse HEAD) diff-sha256 $(git diff 3f6f9a5 | shasum -a 256 | cut -d' ' -f1)" >> $S/x9/x9.summary
busy() { ps -Ao pid=,command= | grep -E '(^|[ /])(cargo|rustc)( |$)|/deps/[A-Za-z0-9_]+-[0-9a-f]{16}' | grep -v -E 'grep -E' }
waited=0
while true; do
  found=$(busy); [[ -z $found ]] && break
  echo "$(date -u +%FT%TZ) release waiting on:" >> $S/x9/waits.txt; echo "$found" | cut -c1-200 >> $S/x9/waits.txt
  sleep 60; waited=$(( waited + 60 ))
done
echo "$(date -u +%FT%TZ) release load check clear after ${waited}s wait" >> $S/x9/waits.txt
$S/release.sh; cat $S/release/summary.txt >> $S/x9/x9.summary
for n in 1 2; do
  $S/set.sh x4f2-$n $S/release/release-absence.json; cat $S/x9/x4f2-$n.summary >> $S/x9/x9.summary
done
/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B $S/compare.py x4f2-1 x4f2-2 > $S/x9/compare.json; echo "compare exit=$?" >> $S/x9/x9.summary
echo "head-after $(git rev-parse HEAD) diff-sha256 $(git diff 3f6f9a5 | shasum -a 256 | cut -d' ' -f1)" >> $S/x9/x9.summary
test ! -e "$HOME/Library/Application Support/OpenSIP" && echo "home absent" >> $S/x9/x9.summary
echo DONE >> $S/x9/x9.summary
