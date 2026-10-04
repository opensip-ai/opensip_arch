#!/bin/zsh
# X4-F2 lanes on 3f6f9a5 + the X4-F2 diff, after X4-F1's lanes.sh and P0's
# dependency lanes. Serial; nothing else of ours runs meanwhile.
set -u
S=/private/tmp/claude-501/-Users-sb-code/8baf40a9-970f-46bc-bd52-a3dde4a615a1/scratchpad/x4f2
cd /Users/sb/code/opensip-ai/opensip-x4f2
export PATH=/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:$PATH
export TMPDIR=$(cat $S/tmpdir.txt)/
PY=/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14
CARGO=/opt/homebrew/Cellar/rust/1.95.0/bin/cargo
AR=$HOME/.cargo/registry/cache/index.crates.io-1949cf8c6b5b557f
V=/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/repository-file-inventory.v135.json
L=$S/lanes; mkdir -p $L; : > $L/summary.txt
step() { name=$1; shift; start=$(date +%s); nice -n 19 "$@" > $L/$name.log 2>&1; echo "$name exit=$? seconds=$(( $(date +%s) - start ))" >> $L/summary.txt; }
echo "head $(git rev-parse HEAD) diff-sha256 $(git diff 3f6f9a5 | shasum -a 256 | cut -d' ' -f1)" >> $L/summary.txt
test ! -e "$HOME/Library/Application Support/OpenSIP" && echo "home absent (before)" >> $L/summary.txt
step fmt cargo fmt --all --check
step build-ws cargo build --workspace --all-targets --locked --offline
step build-feature cargo build -p opensip-platform -p opensip-security -p opensip-storage -p opensip-host --features crash-matrix --all-targets --locked --offline
step build-scenario cargo build -p opensip-security -p opensip-storage -p opensip-host --features scenario-fixtures --all-targets --locked --offline
step build-security-feature cargo build -p opensip-security --features opensip-platform/crash-matrix --locked --offline
step clippy-ws cargo clippy --workspace --all-targets --locked --offline -- -D warnings
step clippy-feature cargo clippy -p opensip-platform -p opensip-security -p opensip-storage -p opensip-host --features crash-matrix --all-targets --locked --offline -- -D warnings
step clippy-scenario cargo clippy -p opensip-security -p opensip-storage -p opensip-host --features scenario-fixtures --all-targets --locked --offline -- -D warnings
step new-tests cargo test --locked --offline -p opensip-security --lib -- --test-threads=1 a_fenced_read_refuses_a_list_already_stale_at_its_t_eval a_fenced_read_refuses_a_root_already_expired_at_its_t_eval a_catalog_expired_alone_at_the_fenced_read_is_admitted_existing_only the_fenced_reads_clock_is_x4f1s_mapping_and_transition_and_report_only_agrees a_reread_after_a_clocked_fenced_read_clocks_its_own_stored_states a_clocked_refusal_comes_after_its_confirmed_write_ahead_and_is_sticky a_report_only_or_horizon_refused_read_of_an_expired_store_writes_nothing a_list_already_stale_at_the_first_reads_t_eval_refuses_at_the_lease_free_point a_reread_fails_closed_once_its_instant_passes_an_expiry the_handoff_clock_advances_by_monotonic_time_only a_rereads_clock_follows_x4b_item_4_and_the_role_machine an_observation_fails_closed_once_its_monotonic_instant_passes_an_expiry a_list_going_stale_during_the_operation_fail_stops_before_any_further_effect an_unrelated_revocation_update_continues_as_drift_without_the_fence
step ws1 cargo test --workspace --all-targets --no-fail-fast --locked --offline
step ws2 cargo test --workspace --all-targets --no-fail-fast --locked --offline
step ws-doc cargo test --workspace --doc --locked --offline
step feature cargo test --locked --offline -p opensip-platform -p opensip-security -p opensip-storage -p opensip-host --features crash-matrix --all-targets --no-fail-fast
step verify-design $PY -I -B tools/verify_design.py --architecture ../opensip_arch --implementation .
cargo metadata --locked --offline --format-version 1 > $L/host.json 2>$L/metadata.err
(cd providers/rust && cargo metadata --locked --offline --format-version 1) > $L/provider.json 2>>$L/metadata.err
step edges-host $PY -I -B tools/check_package_edges.py --repository . --metadata $L/host.json --inventory $V --lane host
step edges-provider $PY -I -B tools/check_package_edges.py --repository . --metadata $L/provider.json --inventory $V --lane rust-provider
step edges-tests $PY -I -B tools/tests/test_package_edges.py -v
step dependencies $PY -I -B tools/check_dependencies.py --manifest Cargo.toml --target aarch64-apple-darwin --cargo $CARGO --feature-profile security-crypto-workspace
step identity-dependencies $PY -I -B tools/check_identity_dependencies.py --manifest Cargo.toml --target aarch64-apple-darwin --cargo $CARGO --archives $AR --policy tools/identity/dependency-policy.json
step dependency-tests $PY -I -B tools/tests/test_dependency_policy.py --target aarch64-apple-darwin --cargo $CARGO -v
step identity-dependency-tests $PY -I -B tools/tests/test_identity_dependencies.py --target aarch64-apple-darwin --cargo $CARGO --archives $AR -v
step checker $PY -m unittest tools/tests/test_check_crash_matrix.py
echo "head-after $(git rev-parse HEAD) diff-sha256 $(git diff 3f6f9a5 | shasum -a 256 | cut -d' ' -f1)" >> $L/summary.txt
test ! -e "$HOME/Library/Application Support/OpenSIP" && echo "home absent" >> $L/summary.txt
echo DONE >> $L/summary.txt
