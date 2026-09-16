#!/bin/sh
# Reproduces the M1 TypeScript package-edge comparison. Provisioning contacts the
# npm registry explicitly; this is not an offline or hermetic build claim.
set -eu
here=$(cd "$(dirname "$0")" && pwd)
NODE=/Users/sb/.nvm/versions/node/v24.16.0/bin/node
NPM=/Users/sb/.nvm/versions/node/v24.16.0/bin/npm
cd "$here"

# 1. Trial-owned tool closure from the pinned lockfile (network provision).
if [ "${SKIP_INSTALL:-0}" != 1 ]; then
  PATH=/Users/sb/.nvm/versions/node/v24.16.0/bin:/usr/bin:/bin "$NPM" ci --ignore-scripts --no-audit --no-fund --registry=https://registry.npmjs.org/
fi
"$NODE" -e 'const l=require("./package-lock.json").packages; for (const [p,v] of [["node_modules/dependency-cruiser","sha512-NUGjObRSbUJTo9FFQixtTfV/3ozbtpivPKJoWP5g7JbKdFjBrQ4TsbmpcOrUcErK+q9n2l+Y4ZS2xVjGGtzm8g=="],["node_modules/typescript","sha512-y2TvuxSZPDyQakkFRPZHKFm+KKVqIisdg9/CZwm9ftvKXLP8NRWj38/ODjNbr43SsoXqNuAisEf1GdCxqWcdBw=="]]) if (l[p].integrity!==v) throw new Error("lock pin drift "+p)'

# 2. Reference copy baseline (byte-identical copy; the root reference is not executed).
OPENSIP_TEST_TYPESCRIPT=/tmp/opensip-implementation/m1-control-generation-candidate-02/tools/contracts/node_modules/typescript \
  "$NODE" --test ../reference-copy/test-typescript-edges.cjs

# 3. Same-payload matrix for dependency-cruiser alone, the candidate and the reference copy.
"$NODE" harness/run-matrix.mjs

# 4. Candidate test suite, then each mutant must fail its targeted tests.
"$NODE" --test candidate/test-check-lane.mjs
rm -rf work/mutants
"$NODE" -e '
const fs=require("fs"),path=require("path");
const mutants={"no-bust":["check-lane.mjs","{ bustTheCache: true }","{}"],"no-cwd":["check-lane.mjs","process.chdir(path.dirname(tsconfigPath));","process.chdir(root);"],
 "no-loader-guard":["supplement.mjs","...loaderFindings(program, root, lane), ",""],"no-census":["supplement.mjs",", ...censusFindings(lane, modules)",""],
 "single-type-conditions":["check-lane.mjs","conditions: [\x27types\x27, ...g.conditions]","conditions: lane.typeConditions"]};
for (const [name,[file,from,to]] of Object.entries(mutants)) {
  const dir=path.join("work/mutants",name); fs.mkdirSync(dir,{recursive:true});
  for (const f of ["check-lane.mjs","supplement.mjs"]) fs.copyFileSync(path.join("candidate",f),path.join(dir,f));
  const p=path.join(dir,file),text=fs.readFileSync(p,"utf8");
  if (text.split(from).length!==2) throw new Error(name+": mutation site not unique");
  fs.writeFileSync(p,text.replace(from,to));
}'
for m in no-bust no-cwd no-loader-guard no-census single-type-conditions; do
  if OPENSIP_TRIAL_CHECKER="$here/work/mutants/$m/check-lane.mjs" "$NODE" --test --test-reporter=tap candidate/test-check-lane.mjs > "work/mutants/$m.tap" 2>&1; then
    echo "mutant $m survived: tests are not meaningful" >&2; exit 1
  fi
  echo "== $m"; grep '^not ok' "work/mutants/$m.tap" | sed -E 's/^not ok [0-9]+ - //'
done
