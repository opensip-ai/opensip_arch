#!/bin/sh
# Offline full check for author-03, using only frozen inputs in this directory
# plus the pinned runtime below. No install, no network. All writes stay under
# this directory (TMPDIR is redirected); results/ is regenerated, so run it in a
# copy when the frozen results must be preserved.
set -eu
here=$(cd "$(dirname "$0")" && pwd)
NODE=/Users/sb/.nvm/versions/node/v24.16.0/bin/node
cd "$here"
mkdir -p work/tmp
TMPDIR="$here/work/tmp"
export TMPDIR

"$NODE" -e 'if (process.version !== "v24.16.0") { console.error("pinned runtime is Node v24.16.0, got " + process.version); process.exit(1); }'

echo "== 1. frozen tree matches freeze-manifest.json (results/ excluded)"
"$NODE" harness/freeze-manifest.mjs --verify

echo "== 2. archive custody: acquired archives vs lock integrity and materialized trees"
"$NODE" provenance/verify-archives.mjs

echo "== 3. reviewer probe module regenerates byte-identically from the copied review-02 script"
cp harness/reviewer-probes.generated.mjs work/tmp/reviewer-probes.frozen.mjs
"$NODE" harness/derive-reviewer-probes.mjs
cmp harness/reviewer-probes.generated.mjs work/tmp/reviewer-probes.frozen.mjs

echo "== 4. case comparison: author02 matrix, review-02 probes, author-03 regressions; both candidates; Node oracles"
"$NODE" harness/run-cases.mjs

echo "== 5. checker test suite (all cases + real CLI invocations)"
"$NODE" --test checker/test/boundary.test.mjs

echo "== 6. real CLI invocations: realpath, /tmp alias, .bin symlink"
"$NODE" harness/cli-invocation.mjs

echo "== 7. real lanes: staged tools/contracts with pnpm materialization; provider/report missing-lane fixtures; baseline"
"$NODE" harness/real-lanes/run-real-lanes.mjs

echo "== 8. mutants: each must fail the test suite"
"$NODE" harness/mutants.mjs
"$NODE" harness/summarize-mutants.mjs
