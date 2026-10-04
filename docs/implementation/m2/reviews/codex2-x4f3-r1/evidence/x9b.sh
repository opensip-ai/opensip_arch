#!/bin/zsh
# X4-F3's X9 lead sets, after x9.sh's pins and release absence (done at
# 19:57Z): both lead sets in full, storage then host, each holding the lane
# lock for the whole set and unniced; then the comparison with the accepted
# X9-6 evidence and the pins again.
set -u
S=/private/tmp/claude-501/-Users-sb-code/8baf40a9-970f-46bc-bd52-a3dde4a615a1/scratchpad/x4f3
cd /Users/sb/code/opensip-ai/opensip-x4f3
echo "restart $(date -u +%FT%TZ) head $(git rev-parse HEAD) diff-sha256 $(git diff d2c00a9 | shasum -a 256 | cut -d' ' -f1)" >> $S/x9/x9.summary
$S/locked.sh leadset-x4f3-1-storage $S/leadset.sh x4f3-1 storage
$S/locked.sh leadset-x4f3-1-host $S/leadset.sh x4f3-1 host
/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B $S/compare.py x4f3-1 > $S/x9/compare.json; echo "compare exit=$?" >> $S/x9/x9.summary
$S/pins.sh > $S/x9/source-pins.txt 2>&1
echo "head-after $(git rev-parse HEAD) diff-sha256 $(git diff d2c00a9 | shasum -a 256 | cut -d' ' -f1)" >> $S/x9/x9.summary
test ! -e "$HOME/Library/Application Support/OpenSIP" && echo "home absent" >> $S/x9/x9.summary
echo DONE >> $S/x9/x9.summary
