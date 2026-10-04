#!/bin/zsh
# X4-F3 lanes on d2c00a9 + the X4-F3 diff, serially. Each lane takes the
# shared lane lock (locked.sh) and releases it straight after; every lane runs
# at nice -n 10 with the private 0700 TMPDIR and --locked --offline.
set -u
S=/private/tmp/claude-501/-Users-sb-code/8baf40a9-970f-46bc-bd52-a3dde4a615a1/scratchpad/x4f3
W=/Users/sb/code/opensip-ai/opensip-x4f3
cd $W
export PATH=/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:$PATH
PY=/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14
CARGO=/opt/homebrew/Cellar/rust/1.95.0/bin/cargo
AR=$HOME/.cargo/registry/cache/index.crates.io-1949cf8c6b5b557f
V=/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/repository-file-inventory.v136.json
L=$S/lanes; mkdir -p $L; : > $L/summary.txt
step() { name=$1; shift; start=$(date +%s); $S/locked.sh lane-$name nice -n 10 "$@"; rc=$?; cp $S/logs/lane-$name.log $L/$name.log; echo "$name exit=$rc seconds=$(( $(date +%s) - start ))" >> $L/summary.txt; }
echo "head $(git rev-parse HEAD) diff-sha256 $(git diff d2c00a9 | shasum -a 256 | cut -d' ' -f1)" >> $L/summary.txt
test ! -e "$HOME/Library/Application Support/OpenSIP" && echo "home absent (before)" >> $L/summary.txt
step fmt cargo fmt --all --check
step build-ws cargo build --workspace --all-targets --locked --offline
step build-feature cargo build -p opensip-platform -p opensip-security -p opensip-storage -p opensip-host --features crash-matrix --all-targets --locked --offline
step build-scenario cargo build -p opensip-security -p opensip-storage -p opensip-host --features scenario-fixtures --all-targets --locked --offline
step build-security-feature cargo build -p opensip-security --features opensip-platform/crash-matrix --locked --offline
step clippy-ws cargo clippy --workspace --all-targets --locked --offline -- -D warnings
step clippy-feature cargo clippy -p opensip-platform -p opensip-security -p opensip-storage -p opensip-host --features crash-matrix --all-targets --locked --offline -- -D warnings
step clippy-scenario cargo clippy -p opensip-security -p opensip-storage -p opensip-host --features scenario-fixtures --all-targets --locked --offline -- -D warnings
step new-tests cargo test --locked --offline -p opensip-security --lib -- --test-threads=1 a_certain_refusal_is_the_invariant_row a_successful_lease_free_read_during_unrelated_unwinding_gets_no_guard the_same_read_after_the_guards_entry_records_its_fail_stop a_bare_latch_on_any_lease_free_handle_before_the_entry_gets_no_guard every_ordered_pair_of_sources_keeps_the_first_stops_cause the_stop_transition_is_the_only_latch_after_the_guards_entry a_first_read_succeeding_during_unrelated_unwinding_is_refused_at_the_guards_entry a_certain_refusal_completes_while_an_observation_holds_the_monitor a_successful_admission_takes_no_stop_cause_lock a_certain_refusal_then_an_observer_tick_keeps_operation_stopped a_stale_guard_held_after_its_section_keeps_its_row_and_stale_guard an_observer_revocation_then_a_certain_refusal_keeps_trust_revoked
step ws1 cargo test --workspace --all-targets --no-fail-fast --locked --offline
step ws2 cargo test --workspace --all-targets --no-fail-fast --locked --offline
step ws-doc cargo test --workspace --doc --locked --offline
step feature cargo test --locked --offline -p opensip-platform -p opensip-security -p opensip-storage -p opensip-host --features crash-matrix --all-targets --no-fail-fast
rm -rf $S/contracts-drift; mkdir -m 700 $S/contracts-drift
step contracts-drift $PY -I -B tools/generate_contracts.py --architecture ../opensip_arch --output $S/contracts-drift/work --node $HOME/.nvm/versions/node/v24.16.0/bin/node --generator $HOME/opensip-deps/contracts-generator-rebuild-02/opensip-contract-generator --python /opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/Resources/Python.app/Contents/MacOS/Python
step verify-design $PY -I -B tools/verify_design.py --architecture ../opensip_arch --implementation .
$S/locked.sh metadata zsh -c "cargo metadata --locked --offline --format-version 1 > $L/host.json && (cd providers/rust && cargo metadata --locked --offline --format-version 1) > $L/provider.json"
step edges-host $PY -I -B tools/check_package_edges.py --repository . --metadata $L/host.json --inventory $V --lane host
step edges-provider $PY -I -B tools/check_package_edges.py --repository . --metadata $L/provider.json --inventory $V --lane rust-provider
step edges-tests $PY -I -B tools/tests/test_package_edges.py -v
step dependencies $PY -I -B tools/check_dependencies.py --manifest Cargo.toml --target aarch64-apple-darwin --cargo $CARGO --feature-profile security-crypto-workspace
step identity-dependencies $PY -I -B tools/check_identity_dependencies.py --manifest Cargo.toml --target aarch64-apple-darwin --cargo $CARGO --archives $AR --policy tools/identity/dependency-policy.json
step dependency-tests $PY -I -B tools/tests/test_dependency_policy.py --target aarch64-apple-darwin --cargo $CARGO -v
step identity-dependency-tests $PY -I -B tools/tests/test_identity_dependencies.py --target aarch64-apple-darwin --cargo $CARGO --archives $AR -v
step checker $PY -m unittest tools/tests/test_check_crash_matrix.py
echo "head-after $(git rev-parse HEAD) diff-sha256 $(git diff d2c00a9 | shasum -a 256 | cut -d' ' -f1)" >> $L/summary.txt
test ! -e "$HOME/Library/Application Support/OpenSIP" && echo "home absent" >> $L/summary.txt
echo DONE >> $L/summary.txt
