#!/bin/zsh
# X4-F1's X9 regression on e093e90 + the X4-F1 diff, serially, with nothing
# else running: release absence, then two run sets of the selected rows
# (storage then host, each with its census), then the comparison with the
# accepted X9-6 evidence.
set -u
S=/private/tmp/claude-501/-Users-sb-code/8baf40a9-970f-46bc-bd52-a3dde4a615a1/scratchpad/x4f1
cd /Users/sb/code/opensip-ai/opensip-x4f1
: > $S/x9.summary
echo "head $(git rev-parse HEAD) diff-sha256 $(git diff e093e90 | shasum -a 256 | cut -d' ' -f1)" >> $S/x9.summary
$S/release.sh; cat $S/release/summary.txt >> $S/x9.summary
for n in 1 2; do
  $S/set.sh x4f1-$n $S/release/release-absence.json; cat $S/x4f1-$n.summary >> $S/x9.summary
done
/opt/homebrew/bin/python3.14 $S/compare.py x4f1-1 x4f1-2 > $S/compare.json; echo "compare exit=$?" >> $S/x9.summary
echo "head-after $(git rev-parse HEAD) diff-sha256 $(git diff e093e90 | shasum -a 256 | cut -d' ' -f1)" >> $S/x9.summary
test ! -e "$HOME/Library/Application Support/OpenSIP" && echo "home absent" >> $S/x9.summary
echo DONE >> $S/x9.summary
