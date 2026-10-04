#!/bin/zsh
# Rerun lanes.sh's drift step alone, after materializing the ignored generator inputs.
set -u
S=/private/tmp/claude-501/-Users-sb-code/8baf40a9-970f-46bc-bd52-a3dde4a615a1/scratchpad
D="$(getconf DARWIN_USER_TEMP_DIR)"; LOCK="${D}opensip-lanes.lock"
cd /Users/sb/code/opensip-ai/opensip-j4a
export PATH=/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:$PATH
export TMPDIR="${D}j4a-tmp/"
PY=/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14
PYAPP=/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/Resources/Python.app/Contents/MacOS/Python
L=$S/j4a-lanes
held=0; give() { if [ "$held" = 1 ]; then rmdir "$LOCK" 2>/dev/null; held=0; fi; }; trap give EXIT INT TERM
until mkdir "$LOCK" 2>/dev/null; do sleep 2; done; held=1
while ps -Ao command | grep -E '[o]pensip-contract-generator|[g]enerate_contracts[.]py' >/dev/null; do sleep 2; done
rm -rf $L/drift; start=$(date +%s)
nice -n 10 $PY -I -B tools/generate_contracts.py --architecture ../opensip_arch --output $L/drift --node $HOME/.nvm/versions/node/v24.16.0/bin/node --generator $HOME/opensip-deps/contracts-generator-rebuild-02/opensip-contract-generator --python $PYAPP > $L/drift.log 2>&1; rc=$?
give
echo "drift (rerun) exit=$rc seconds=$(( $(date +%s) - start ))" >> $L/summary.txt
cat $L/drift.log | tail -3
exit $rc
