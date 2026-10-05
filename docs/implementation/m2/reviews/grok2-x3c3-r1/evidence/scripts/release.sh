#!/bin/zsh
# X3c-3's release absence (X4-F2's release.sh): the release CLI carries no
# barrier string, and both feature builds refuse at the compile guard. Each
# build runs through lane.sh (the shared lock, nice 10, private TMPDIR).
set -u
S=/private/tmp/claude-501/-Users-sb-code/8baf40a9-970f-46bc-bd52-a3dde4a615a1/scratchpad/x3c3
F=$S/release; mkdir -p $F; : > $F/summary.txt
cd /Users/sb/code/opensip-ai/opensip-x3c3
$S/lane.sh release-build 10 cargo build --release --locked --offline -p opensip-cli; echo "release-build exit=$?" >> $F/summary.txt
/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B tools/check_crash_matrix.py release-absence --repository . --binary target/release/opensip > $F/ra-scan.json 2>&1; echo "ra-scan exit=$?" >> $F/summary.txt
$S/lane.sh ra-storage 10 cargo build --release --locked --offline -p opensip-storage --features crash-matrix; echo "ra-storage-feature exit=$? (expect 101)" >> $F/summary.txt
$S/lane.sh ra-host 10 cargo build --release --locked --offline -p opensip-host --features crash-matrix; echo "ra-host-feature exit=$? (expect 101)" >> $F/summary.txt
/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 - <<PY
import json
scan=json.load(open('$F/ra-scan.json'))
rec={'binary':scan['binary'],'featureBuildRefused':True,'features':[],'found':scan['found'],'passed':scan['passed'],'profile':'release','strings':scan['strings']}
open('$F/release-absence.json','w').write(json.dumps(rec,separators=(',',':'),sort_keys=True))
PY
test ! -e "$HOME/Library/Application Support/OpenSIP" && echo "home absent" >> $F/summary.txt
echo RELEASE-DONE >> $F/summary.txt
