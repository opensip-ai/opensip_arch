#!/bin/zsh
# J3a lanes on 1d24900 + the J3a diff (with the staged lock), serially, in
# six groups. Each group takes the shared lane lock (locked.sh, which removes
# it only if its own mkdir took it) for that group's lanes only and releases
# it straight after. Every lane runs at nice -n 10 with the private 0700
# TMPDIR and --locked --offline, and is logged and summarized on its own.
# Usage: lanes.sh (all groups) | lanes.sh run <group> (inside the lock).
set -u
S=/private/tmp/claude-501/-Users-sb-code/8baf40a9-970f-46bc-bd52-a3dde4a615a1/scratchpad/j3a
W=/Users/sb/code/opensip-ai/opensip-j3a
cd $W
export PATH=/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:$PATH
PY=/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14
CARGO=/opt/homebrew/Cellar/rust/1.95.0/bin/cargo
AR=$HOME/.cargo/registry/cache/index.crates.io-1949cf8c6b5b557f
U=/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/durable-entry-j3a-inventory-v139
V=/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/repository-file-inventory.v139.json
L=$S/lanes; mkdir -p $L
step() { name=$1; shift; start=$(date +%s); nice -n 10 "$@" > $L/$name.log 2>&1; rc=$?; echo "$name exit=$rc seconds=$(( $(date +%s) - start ))" >> $L/summary.txt; }
diffsha() { (git diff 1d24900; git ls-files --others --exclude-standard | sort | while read f; do echo "=== $f"; cat "$f"; done) | shasum -a 256 | cut -d' ' -f1; }
if [[ ${1:-} == run ]]; then
  case $2 in
    build)
      step fmt cargo fmt --all --check
      step build-ws cargo build --workspace --all-targets --locked --offline
      step build-feature cargo build -p opensip-platform -p opensip-security -p opensip-storage -p opensip-host --features crash-matrix --all-targets --locked --offline
      step build-scenario cargo build -p opensip-security -p opensip-storage -p opensip-host --features scenario-fixtures --all-targets --locked --offline
      step build-security-feature cargo build -p opensip-security --features opensip-platform/crash-matrix --locked --offline
      step clippy-ws cargo clippy --workspace --all-targets --locked --offline -- -D warnings
      step clippy-feature cargo clippy -p opensip-platform -p opensip-security -p opensip-storage -p opensip-host --features crash-matrix --all-targets --locked --offline -- -D warnings
      step clippy-scenario cargo clippy -p opensip-security -p opensip-storage -p opensip-host --features scenario-fixtures --all-targets --locked --offline -- -D warnings
      step new-tests $S/newtests.sh ;;
    ws1)
      step ws1 cargo test --workspace --all-targets --no-fail-fast --locked --offline ;;
    ws2)
      step ws2 cargo test --workspace --all-targets --no-fail-fast --locked --offline
      step ws-doc cargo test --workspace --doc --locked --offline ;;
    feature)
      step feature cargo test --locked --offline -p opensip-platform -p opensip-security -p opensip-storage -p opensip-host --features crash-matrix --all-targets --no-fail-fast ;;
    checks)
      rm -rf $S/contracts-drift; mkdir -m 700 $S/contracts-drift
      step contracts-drift $PY -I -B $U/evidence/drift_scratch_j3a.py . $S/contracts-drift/work
      step verify-scratch $PY -I -B $U/evidence/verify_scratch.py .
      step verify-design-staged $PY -I -B tools/verify_design.py --architecture ../opensip_arch --implementation .
      git show HEAD:design-lock.json > $L/head-lock.json
      step verify-design-head $PY -I -B tools/verify_design.py --architecture ../opensip_arch --lock $L/head-lock.json --implementation .
      step verify-projection $PY -I -B $U/verify_projection.py --architecture ../opensip_arch --lock $L/head-lock.json
      step metadata zsh -c "cargo metadata --locked --offline --format-version 1 > $L/host.json && (cd providers/rust && cargo metadata --locked --offline --format-version 1) > $L/provider.json"
      step edges-host $PY -I -B tools/check_package_edges.py --repository . --metadata $L/host.json --inventory $V --lane host
      step edges-provider $PY -I -B tools/check_package_edges.py --repository . --metadata $L/provider.json --inventory $V --lane rust-provider
      step edges-tests $PY -I -B tools/tests/test_package_edges.py -v
      step dependencies $PY -I -B tools/check_dependencies.py --manifest Cargo.toml --target aarch64-apple-darwin --cargo $CARGO --feature-profile security-crypto-workspace
      step identity-dependencies $PY -I -B tools/check_identity_dependencies.py --manifest Cargo.toml --target aarch64-apple-darwin --cargo $CARGO --archives $AR --policy tools/identity/dependency-policy.json
      step dependency-tests $PY -I -B tools/tests/test_dependency_policy.py --target aarch64-apple-darwin --cargo $CARGO -v
      step identity-dependency-tests $PY -I -B tools/tests/test_identity_dependencies.py --target aarch64-apple-darwin --cargo $CARGO --archives $AR -v
      step checker $PY -m unittest tools/tests/test_check_crash_matrix.py ;;
  esac
  exit 0
fi
: > $L/summary.txt
echo "head $(git rev-parse HEAD) diff-sha256 $(diffsha)" >> $L/summary.txt
test ! -e "$HOME/Library/Application Support/OpenSIP" && echo "home absent (before)" >> $L/summary.txt
for g in build ws1 ws2 feature checks; do
  $S/locked.sh group-$g $S/lanes.sh run $g
  echo "group $g done $(date -u +%FT%TZ)" >> $L/summary.txt
done
echo "head-after $(git rev-parse HEAD) diff-sha256 $(diffsha)" >> $L/summary.txt
test ! -e "$HOME/Library/Application Support/OpenSIP" && echo "home absent" >> $L/summary.txt
echo DONE >> $L/summary.txt
