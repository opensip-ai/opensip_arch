#!/bin/zsh
# J3a's new and changed tests, by name, each package's lib or test target.
set -u
rc=0
cargo test --locked --offline -p opensip-platform --lib -- reservation_tests || rc=1
cargo test --locked --offline -p opensip-host --lib -- request::tests || rc=1
cargo test --locked --offline -p opensip-security --lib -- installation_routing:: mint_intent_records_the_lent_request_id intent_is_bound_charged_and_consumed_once open_reserves_its_execution_id || rc=1
cargo test --locked --offline -p opensip-host --test admission_tests -- --exact opaque_api_misuse_fails_for_the_intended_reason || rc=1
exit $rc
