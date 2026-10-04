#!/bin/zsh
# X4-F3's mutation checks, run by locked.sh: each mutation is applied to
# operation_guard.rs, the new tests run, and the file is restored from its
# backup (its sha256 is checked before and after).
set -u
S=/private/tmp/claude-501/-Users-sb-code/8baf40a9-970f-46bc-bd52-a3dde4a615a1/scratchpad/x4f3
cd /Users/sb/code/opensip-ai/opensip-x4f3
F=crates/security/src/custody/operation_guard.rs
cp $F $S/mutations/operation_guard.rs.orig
before=$(shasum -a 256 $F | cut -d' ' -f1)
TESTS=(a_certain_refusal_is_the_invariant_row a_successful_lease_free_read_during_unrelated_unwinding_gets_no_guard the_same_read_after_the_guards_entry_records_its_fail_stop a_bare_latch_on_any_lease_free_handle_before_the_entry_gets_no_guard every_ordered_pair_of_sources_keeps_the_first_stops_cause the_stop_transition_is_the_only_latch_after_the_guards_entry a_first_read_succeeding_during_unrelated_unwinding_is_refused_at_the_guards_entry a_certain_refusal_completes_while_an_observation_holds_the_monitor a_successful_admission_takes_no_stop_cause_lock a_certain_refusal_then_an_observer_tick_keeps_operation_stopped a_stale_guard_held_after_its_section_keeps_its_row_and_stale_guard an_observer_revocation_then_a_certain_refusal_keeps_trust_revoked)
: > $S/mutations/summary.txt
for m in r7-records no-entry-check bare-unwind; do
  cp $S/mutations/operation_guard.rs.orig $F
  python3 $S/mutate.py $m || { echo "$m: mutation failed to apply" >> $S/mutations/summary.txt; continue; }
  nice -n 10 cargo test --locked --offline -p opensip-security --lib -- --test-threads=4 $TESTS > $S/mutations/$m.log 2>&1
  echo "$m exit=$?" >> $S/mutations/summary.txt
  grep -E "^test .* \.\.\. FAILED" $S/mutations/$m.log | sed 's/^/  /' >> $S/mutations/summary.txt
  grep -E "^test result" $S/mutations/$m.log | sed 's/^/  /' >> $S/mutations/summary.txt
done
cp $S/mutations/operation_guard.rs.orig $F
after=$(shasum -a 256 $F | cut -d' ' -f1)
echo "restored: $([[ $before == $after ]] && echo identical || echo DIFFERENT) $after" >> $S/mutations/summary.txt
