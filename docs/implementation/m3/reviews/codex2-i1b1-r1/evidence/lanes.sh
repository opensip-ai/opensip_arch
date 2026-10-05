#!/bin/zsh
# I1-b1 lanes, run serially from the worktree; each lane takes the shared lane
# lock with mkdir and releases it with rmdir straight after.
set -u
export PATH=/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:$PATH
D="$(getconf DARWIN_USER_TEMP_DIR)"
LOCK="${D}opensip-lanes.lock"
export TMPDIR="${D}i1b1-tmp"
export CARGO_TARGET_DIR=/Users/sb/code/opensip-ai/opensip-i1b1/target
OUT=${1:?output directory}
mkdir -p "$OUT"
PY=/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14
PYAPP=/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/Resources/Python.app/Contents/MacOS/Python
CARGO=/opt/homebrew/Cellar/rust/1.95.0/bin/cargo
AR=$HOME/.cargo/registry/cache/index.crates.io-1949cf8c6b5b557f
INV=../opensip_arch/docs/implementation/m2/repository-file-inventory.v136.json
HELD=0
trap '[ "$HELD" = 1 ] && rmdir "$LOCK"' EXIT
take() { while ! mkdir "$LOCK" 2>/dev/null; do sleep 0.5; done; HELD=1; }
give() { rmdir "$LOCK"; HELD=0; }
cd /Users/sb/code/opensip-ai/opensip-i1b1 || exit 1
home() { [ -e "$HOME/Library/Application Support/OpenSIP" ] && echo present || echo absent; }
echo "home before: $(home)" >> "$OUT/summary.txt"
echo "head: $(git rev-parse HEAD); diff sha256: $(git diff HEAD | shasum -a 256 | cut -d' ' -f1)" >> "$OUT/summary.txt"
lane() {
  local name=$1; shift
  take
  local t0=$(date +%s) s=$(date +%T)
  nice -n 10 "$@" > "$OUT/$name.log" 2>&1
  local rc=$?
  give
  echo "$name rc=$rc start=$s secs=$(( $(date +%s) - t0 ))" >> "$OUT/summary.txt"
}
lane fmt zsh -c 'cargo fmt --all --check && rustfmt --edition 2024 --check crates/evaluator/src/policy_pack_tests.rs'
lane build cargo build --workspace --all-targets --locked --offline
lane clippy-workspace cargo clippy --workspace --all-targets --locked --offline -- -D warnings
lane clippy-crash-matrix cargo clippy -p opensip-platform -p opensip-security -p opensip-storage -p opensip-host --features crash-matrix --all-targets --locked --offline -- -D warnings
lane clippy-scenario-fixtures cargo clippy -p opensip-security -p opensip-storage -p opensip-host --features scenario-fixtures --all-targets --locked --offline -- -D warnings
lane test-1 cargo test --workspace --all-targets --no-fail-fast --locked --offline
lane test-2 cargo test --workspace --all-targets --no-fail-fast --locked --offline
lane doc cargo test --workspace --doc --locked --offline
lane crash-matrix cargo test -p opensip-platform -p opensip-security -p opensip-storage -p opensip-host --features crash-matrix --all-targets --no-fail-fast --locked --offline
GEN=$(ps -axo pid,command | grep -E '[o]pensip-contract-generator|[g]enerate_contracts[.]py')
echo "generator processes before drift: ${GEN:-none}" >> "$OUT/summary.txt"
lane drift zsh -c "$PY -I -B tools/generate_contracts.py --architecture ../opensip_arch --output $OUT/drift-work --node $HOME/.nvm/versions/node/v24.16.0/bin/node --generator $HOME/opensip-deps/contracts-generator-rebuild-02/opensip-contract-generator --python $PYAPP"
lane verify-design $PY -I -B tools/verify_design.py --architecture ../opensip_arch --implementation .
lane edges zsh -c "cargo metadata --locked --offline --format-version 1 > $OUT/host.json && (cd providers/rust && cargo metadata --locked --offline --format-version 1) > $OUT/provider.json && $PY -I -B tools/check_package_edges.py --repository . --metadata $OUT/host.json --inventory $INV --lane host && $PY -I -B tools/check_package_edges.py --repository . --metadata $OUT/provider.json --inventory $INV --lane rust-provider && $PY -I -B tools/tests/test_package_edges.py -v"
lane dependencies zsh -c "$PY -I -B tools/check_dependencies.py --manifest Cargo.toml --target aarch64-apple-darwin --cargo $CARGO --feature-profile security-crypto-workspace && $PY -I -B tools/check_identity_dependencies.py --manifest Cargo.toml --target aarch64-apple-darwin --cargo $CARGO --archives $AR --policy tools/identity/dependency-policy.json && $PY -I -B tools/tests/test_dependency_policy.py --target aarch64-apple-darwin --cargo $CARGO -v && $PY -I -B tools/tests/test_identity_dependencies.py --target aarch64-apple-darwin --cargo $CARGO --archives $AR -v"
echo "home after: $(home)" >> "$OUT/summary.txt"
echo "diff sha256 after: $(git diff HEAD | shasum -a 256 | cut -d' ' -f1)" >> "$OUT/summary.txt"
echo done >> "$OUT/summary.txt"
