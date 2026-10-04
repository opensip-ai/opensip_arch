#!/bin/zsh
# J4a lanes on d2c00a9 + the J4a diff, after X4-F2's lanes.sh. Serial. Each
# cargo or tool step takes the shared lane lock (mkdir) and releases it at once.
set -u
S=/private/tmp/claude-501/-Users-sb-code/8baf40a9-970f-46bc-bd52-a3dde4a615a1/scratchpad
D="$(getconf DARWIN_USER_TEMP_DIR)"
LOCK="${D}opensip-lanes.lock"
cd /Users/sb/code/opensip-ai/opensip-j4a
export PATH=/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:$PATH
export TMPDIR="${D}j4a-tmp/"
PY=/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14
# The generator's selected child interpreter (not the launcher alias).
PYAPP=/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/Resources/Python.app/Contents/MacOS/Python
# The drift check needs the git-ignored generator inputs: tools/contracts/
# node_modules and python-packages, copied from the main checkout at d2c00a9
# (the generator admits each by its pinned sha256).
CARGO=/opt/homebrew/Cellar/rust/1.95.0/bin/cargo
NODE=$HOME/.nvm/versions/node/v24.16.0/bin/node
GEN=$HOME/opensip-deps/contracts-generator-rebuild-02/opensip-contract-generator
AR=$HOME/.cargo/registry/cache/index.crates.io-1949cf8c6b5b557f
V=/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/repository-file-inventory.v136.json
L=$S/j4a-lanes; mkdir -p $L; : > $L/summary.txt
held=0
take() { until mkdir "$LOCK" 2>/dev/null; do sleep 2; done; held=1; }
give() { if [ "$held" = 1 ]; then rmdir "$LOCK" 2>/dev/null; held=0; fi; }
trap give EXIT INT TERM
step() {
  name=$1; shift
  take; start=$(date +%s)
  nice -n 10 "$@" > $L/$name.log 2>&1; rc=$?
  end=$(date +%s); give
  echo "$name exit=$rc seconds=$(( end - start ))" >> $L/summary.txt
}
echo "head $(git rev-parse HEAD) diff-sha256 $(git diff d2c00a9 | shasum -a 256 | cut -d' ' -f1)" >> $L/summary.txt
test ! -e "$HOME/Library/Application Support/OpenSIP" && echo "home absent (before)" >> $L/summary.txt
step fmt cargo fmt --all --check
step build-ws cargo build --workspace --all-targets --locked --offline
step clippy-ws cargo clippy --workspace --all-targets --locked --offline -- -D warnings
step clippy-feature cargo clippy -p opensip-platform -p opensip-security -p opensip-storage -p opensip-host --features crash-matrix --all-targets --locked --offline -- -D warnings
step clippy-scenario cargo clippy -p opensip-security -p opensip-storage -p opensip-host --features scenario-fixtures --all-targets --locked --offline -- -D warnings
step ws1 cargo test --workspace --all-targets --no-fail-fast --locked --offline
step ws2 cargo test --workspace --all-targets --no-fail-fast --locked --offline
step ws-doc cargo test --workspace --doc --locked --offline
step feature cargo test -p opensip-platform -p opensip-security -p opensip-storage -p opensip-host --features crash-matrix --all-targets --no-fail-fast --locked --offline
rm -rf $L/drift; step drift $PY -I -B tools/generate_contracts.py --architecture ../opensip_arch --output $L/drift --node $NODE --generator $GEN --python $PYAPP
step verify-design $PY -I -B tools/verify_design.py --architecture ../opensip_arch --implementation .
take; cargo metadata --locked --offline --format-version 1 > $L/host.json 2>$L/metadata.err
(cd providers/rust && cargo metadata --locked --offline --format-version 1) > $L/provider.json 2>>$L/metadata.err; give
step edges-host $PY -I -B tools/check_package_edges.py --repository . --metadata $L/host.json --inventory $V --lane host
step edges-provider $PY -I -B tools/check_package_edges.py --repository . --metadata $L/provider.json --inventory $V --lane rust-provider
step edges-tests $PY -I -B tools/tests/test_package_edges.py -v
step dependencies $PY -I -B tools/check_dependencies.py --manifest Cargo.toml --target aarch64-apple-darwin --cargo $CARGO --feature-profile security-crypto-workspace
step identity-dependencies $PY -I -B tools/check_identity_dependencies.py --manifest Cargo.toml --target aarch64-apple-darwin --cargo $CARGO --archives $AR --policy tools/identity/dependency-policy.json
step dependency-tests $PY -I -B tools/tests/test_dependency_policy.py --target aarch64-apple-darwin --cargo $CARGO -v
step identity-dependency-tests $PY -I -B tools/tests/test_identity_dependencies.py --target aarch64-apple-darwin --cargo $CARGO --archives $AR -v
echo "head-after $(git rev-parse HEAD) diff-sha256 $(git diff d2c00a9 | shasum -a 256 | cut -d' ' -f1)" >> $L/summary.txt
test ! -e "$HOME/Library/Application Support/OpenSIP" && echo "home absent" >> $L/summary.txt
echo DONE >> $L/summary.txt
