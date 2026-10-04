#!/bin/zsh
# X4-F1 lanes on e093e90, after X9-6's lanes.sh. Nothing else may run meanwhile.
set -u
S=/private/tmp/claude-501/-Users-sb-code/8baf40a9-970f-46bc-bd52-a3dde4a615a1/scratchpad/x4f1
cd /Users/sb/code/opensip-ai/opensip-x4f1
export PATH=/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:$PATH
export TMPDIR=$(cat $S/tmpdir.txt)/
L=$S/lanes; mkdir -p $L; : > $L/summary.txt
step() { name=$1; shift; start=$(date +%s); "$@" > $L/$name.log 2>&1; echo "$name exit=$? seconds=$(( $(date +%s) - start ))" >> $L/summary.txt; }
step fmt cargo fmt --all --check
step build-ws cargo build --workspace --all-targets --locked --offline
step build-feature cargo build -p opensip-platform -p opensip-security -p opensip-storage -p opensip-host --features crash-matrix --all-targets --locked --offline
step build-scenario cargo build -p opensip-security -p opensip-storage -p opensip-host --features scenario-fixtures --all-targets --locked --offline
step build-security-feature cargo build -p opensip-security --features opensip-platform/crash-matrix --locked --offline
step clippy-ws cargo clippy --workspace --all-targets --locked --offline -- -D warnings
step clippy-feature cargo clippy -p opensip-platform -p opensip-security -p opensip-storage -p opensip-host --features crash-matrix --all-targets --locked --offline -- -D warnings
step clippy-scenario cargo clippy -p opensip-security -p opensip-storage -p opensip-host --features scenario-fixtures --all-targets --locked --offline -- -D warnings
step new-tests cargo test --locked --offline -p opensip-security --lib -- --test-threads=1 a_reread_fails_closed_once_its_instant_passes_an_expiry the_handoff_clock_advances_by_monotonic_time_only a_rereads_clock_follows_x4b_item_4_and_the_role_machine an_observation_fails_closed_once_its_monotonic_instant_passes_an_expiry a_list_going_stale_during_the_operation_fail_stops_before_any_further_effect an_observation_reads_through_the_retained_handles_with_no_fence_held
step ws1 cargo test --workspace --locked --offline
step ws2 cargo test --workspace --locked --offline
step feature cargo test --locked --offline -p opensip-platform -p opensip-security -p opensip-storage -p opensip-host --features crash-matrix --all-targets
step verify-design python3.14 -I -B tools/verify_design.py --architecture ../opensip_arch --implementation .
cargo metadata --locked --offline --format-version 1 > $L/metadata.json 2>$L/metadata.err
step edges python3.14 tools/check_package_edges.py --repository . --metadata $L/metadata.json --inventory /Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/repository-file-inventory.v134.json --lane host
step checker python3.14 -m unittest tools/tests/test_check_crash_matrix.py
echo "head $(git rev-parse HEAD) diff-sha256 $(git diff e093e90 | shasum -a 256 | cut -d' ' -f1)" >> $L/summary.txt
test ! -e "$HOME/Library/Application Support/OpenSIP" && echo "home absent" >> $L/summary.txt
echo DONE >> $L/summary.txt
