#!/bin/bash
# Serial native replay for review claude-opus5-private-access-narrow450-r1.
# Every write goes under R: isolated CARGO_HOME copy, CARGO_TARGET_DIR and TMPDIR.
# Usage: replay.sh <name> <cwd> <command...>
R=/tmp/opensip-implementation/reviews/claude-opus5-private-access-narrow450-r1
name=$1; cwd=$2; shift 2
out=$R/evidence/runs; mkdir -p $out
start=$(date -u +%Y-%m-%dT%H:%M:%SZ)
( cd "$cwd" && env -i HOME=/Users/sb PATH=/opt/homebrew/Cellar/rust/1.95.0/bin:/usr/bin:/bin \
  CARGO_HOME=$R/work/cargo-home CARGO_TARGET_DIR=${TARGET:-$R/work/target} TMPDIR=$R/work/tmp/ \
  LANG=C LC_ALL=C TZ=UTC CARGO_INCREMENTAL=0 RUST_TEST_THREADS=1 "$@" ) >$out/$name.stdout 2>$out/$name.stderr
code=$?
end=$(date -u +%Y-%m-%dT%H:%M:%SZ)
python3 -I -B -c 'import json,sys; print(json.dumps({"name":sys.argv[1],"cwd":sys.argv[2],"command":sys.argv[6:],"exitCode":int(sys.argv[3]),"start":sys.argv[4],"end":sys.argv[5]}))' "$name" "$cwd" "$code" "$start" "$end" "$@" > $out/$name.json
echo "$name exit $code"
exit $code
