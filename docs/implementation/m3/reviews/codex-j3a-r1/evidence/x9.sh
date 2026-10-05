#!/bin/zsh
# J3a's X9 lead-set rerun (J1 r6 item 12; M3-PLAN r10's "J3a, then its lead
# set") on 1d24900 + the J3a diff, serially: source pins, release absence,
# then both lead sets in full, storage then host, each holding the lane lock
# for the whole set and unniced; then the comparison with the accepted X9-6
# evidence.
set -u
S=/private/tmp/claude-501/-Users-sb-code/8baf40a9-970f-46bc-bd52-a3dde4a615a1/scratchpad/j3a
cd /Users/sb/code/opensip-ai/opensip-j3a
mkdir -p $S/x9
diffsha() { (git diff 1d24900; git ls-files --others --exclude-standard | sort | while read f; do echo "=== $f"; cat "$f"; done) | shasum -a 256 | cut -d' ' -f1; }
echo "head $(git rev-parse HEAD) diff-sha256 $(diffsha)" >> $S/x9/x9.summary
$S/pins.sh > $S/x9/source-pins-first.txt 2>&1
$S/locked.sh release $S/release.sh; echo "release exit=$?" >> $S/x9/x9.summary; cat $S/release/summary.txt >> $S/x9/x9.summary
$S/locked.sh leadset-j3a-1-storage $S/leadset.sh j3a-1 storage
$S/locked.sh leadset-j3a-1-host $S/leadset.sh j3a-1 host
/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B $S/compare.py j3a-1 > $S/x9/compare.json; echo "compare exit=$?" >> $S/x9/x9.summary
$S/pins.sh > $S/x9/source-pins.txt 2>&1
echo "head-after $(git rev-parse HEAD) diff-sha256 $(diffsha)" >> $S/x9/x9.summary
test ! -e "$HOME/Library/Application Support/OpenSIP" && echo "home absent" >> $S/x9/x9.summary
echo DONE >> $S/x9/x9.summary
