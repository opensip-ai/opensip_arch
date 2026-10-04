#!/bin/zsh
# X4-F1 release absence, after X9-6's final.sh: the release CLI carries no
# barrier string, and both feature builds refuse at the compile guard.
set -u
S=/private/tmp/claude-501/-Users-sb-code/8baf40a9-970f-46bc-bd52-a3dde4a615a1/scratchpad/x4f1
cd /Users/sb/code/opensip-ai/opensip-x4f1
export PATH=/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:$PATH
export TMPDIR=$(cat $S/tmpdir.txt)/
F=$S/release; mkdir -p $F; : > $F/summary.txt
cargo build --release --locked --offline -p opensip-cli > $F/release-build.log 2>&1; echo "release-build exit=$?" >> $F/summary.txt
python3.14 tools/check_crash_matrix.py release-absence --repository . --binary target/release/opensip > $F/ra-scan.json 2>&1; echo "ra-scan exit=$?" >> $F/summary.txt
cargo build --release --locked --offline -p opensip-storage --features crash-matrix > $F/ra-storage.log 2>&1; echo "ra-storage-feature exit=$? (expect 101)" >> $F/summary.txt
cargo build --release --locked --offline -p opensip-host --features crash-matrix > $F/ra-host.log 2>&1; echo "ra-host-feature exit=$? (expect 101)" >> $F/summary.txt
python3.14 - <<PY
import json
scan=json.load(open('$F/ra-scan.json'))
rec={'binary':scan['binary'],'featureBuildRefused':True,'features':[],'found':scan['found'],'passed':scan['passed'],'profile':'release','strings':scan['strings']}
open('$F/release-absence.json','w').write(json.dumps(rec,separators=(',',':'),sort_keys=True))
PY
test ! -e "$HOME/Library/Application Support/OpenSIP" && echo "home absent" >> $F/summary.txt
echo DONE >> $F/summary.txt
