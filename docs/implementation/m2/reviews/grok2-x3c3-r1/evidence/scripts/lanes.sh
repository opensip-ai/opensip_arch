#!/bin/zsh
# X3c-3's lanes on d2c00a9 + the X3c-3 diff, serially, each under the shared
# lanes lock (lane.sh takes and releases it per step), at nice 10, with the
# private 0700 TMPDIR, --locked --offline. Modelled on X4-F2's lanes.sh.
set -u
S=/private/tmp/claude-501/-Users-sb-code/8baf40a9-970f-46bc-bd52-a3dde4a615a1/scratchpad/x3c3
L=$S/lane.sh
W=/Users/sb/code/opensip-ai/opensip-x3c3
PY=/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14
CARGO=/opt/homebrew/Cellar/rust/1.95.0/bin/cargo
AR=$HOME/.cargo/registry/cache/index.crates.io-1949cf8c6b5b557f
V=/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/repository-file-inventory.v136.json
F=--locked; O=--offline
cd $W
echo "lanes-begin head $(git rev-parse HEAD) diff-sha256 $(git diff d2c00a9 | shasum -a 256 | cut -d' ' -f1)" >> $S/logs/summary.txt
test ! -e "$HOME/Library/Application Support/OpenSIP" && echo "home absent (before)" >> $S/logs/summary.txt
$L fmt 10 cargo fmt --all --check
$L build-ws 10 cargo build --workspace --all-targets $F $O
$L build-feature 10 cargo build -p opensip-platform -p opensip-security -p opensip-storage -p opensip-host --features crash-matrix --all-targets $F $O
$L build-scenario 10 cargo build -p opensip-security -p opensip-storage -p opensip-host --features scenario-fixtures --all-targets $F $O
$L clippy-ws 10 cargo clippy --workspace --all-targets $F $O -- -D warnings
$L clippy-feature 10 cargo clippy -p opensip-platform -p opensip-security -p opensip-storage -p opensip-host --features crash-matrix --all-targets $F $O -- -D warnings
$L clippy-scenario 10 cargo clippy -p opensip-security -p opensip-storage -p opensip-host --features scenario-fixtures --all-targets $F $O -- -D warnings
$L ws1 10 cargo test --workspace --all-targets --no-fail-fast $F $O
$L ws2 10 cargo test --workspace --all-targets --no-fail-fast $F $O
$L ws-doc 10 cargo test --workspace --doc $F $O
$L feature 10 cargo test $F $O -p opensip-platform -p opensip-security -p opensip-storage -p opensip-host --features crash-matrix --all-targets --no-fail-fast
rm -rf $S/contracts-drift
$L contracts-drift 10 $PY -I -B tools/generate_contracts.py --root . --architecture ../opensip_arch --output $S/contracts-drift --node /Users/sb/.nvm/versions/node/v24.16.0/bin/node --generator /Users/sb/opensip-deps/contracts-generator-rebuild-02/opensip-contract-generator --python /opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/Resources/Python.app/Contents/MacOS/Python
$L verify-design 10 $PY -I -B tools/verify_design.py --architecture ../opensip_arch --implementation .
$L metadata 10 zsh -c "cargo metadata $F $O --format-version 1 > $S/logs/host-metadata.json && (cd providers/rust && cargo metadata $F $O --format-version 1) > $S/logs/provider-metadata.json"
$L edges-host 10 $PY -I -B tools/check_package_edges.py --repository . --metadata $S/logs/host-metadata.json --inventory $V --lane host
$L edges-provider 10 $PY -I -B tools/check_package_edges.py --repository . --metadata $S/logs/provider-metadata.json --inventory $V --lane rust-provider
$L edges-tests 10 $PY -I -B tools/tests/test_package_edges.py -v
$L dependencies 10 $PY -I -B tools/check_dependencies.py --manifest Cargo.toml --target aarch64-apple-darwin --cargo $CARGO --feature-profile security-crypto-workspace
$L identity-dependencies 10 $PY -I -B tools/check_identity_dependencies.py --manifest Cargo.toml --target aarch64-apple-darwin --cargo $CARGO --archives $AR --policy tools/identity/dependency-policy.json
$L dependency-tests 10 $PY -I -B tools/tests/test_dependency_policy.py --target aarch64-apple-darwin --cargo $CARGO -v
$L identity-dependency-tests 10 $PY -I -B tools/tests/test_identity_dependencies.py --target aarch64-apple-darwin --cargo $CARGO --archives $AR -v
$L checker 10 $PY -m unittest tools/tests/test_check_crash_matrix.py
echo "lanes-end head $(git rev-parse HEAD) diff-sha256 $(git diff d2c00a9 | shasum -a 256 | cut -d' ' -f1)" >> $S/logs/summary.txt
test ! -e "$HOME/Library/Application Support/OpenSIP" && echo "home absent (after)" >> $S/logs/summary.txt
echo LANES-DONE >> $S/logs/summary.txt
