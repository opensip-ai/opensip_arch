#!/bin/zsh
# Base test files over I1-c's product bytes: which existing tests flip.
set -u
export PATH=/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:$PATH
D="$(getconf DARWIN_USER_TEMP_DIR)"; LOCK="${D}opensip-lanes.lock"; export TMPDIR="${D}i1c-tmp"
S=/private/tmp/claude-501/-Users-sb-code/8baf40a9-970f-46bc-bd52-a3dde4a615a1/scratchpad/i1c-flipcheck
export CARGO_TARGET_DIR=$S/target
HELD=0; trap '[ "$HELD" = 1 ] && rmdir "$LOCK"' EXIT
while ! mkdir "$LOCK" 2>/dev/null; do sleep 2; done; HELD=1
cd $S/tree
nice -n 10 cargo test -p opensip-evaluator --lib --locked --offline -- pack_tests > $S/evaluator.log 2>&1; echo "evaluator rc=$?" >> $S/summary.txt
nice -n 10 cargo test -p opensip-host --lib --locked --offline -- configuration::tests > $S/host.log 2>&1; echo "host rc=$?" >> $S/summary.txt
rmdir "$LOCK"; HELD=0
