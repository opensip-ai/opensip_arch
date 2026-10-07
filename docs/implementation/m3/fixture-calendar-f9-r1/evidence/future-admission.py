from pathlib import Path
b=Path('/tmp/opensip-implementation/f9-authoring');base=Path('/Users/sb/code/opensip-ai/opensip');rel='crates/security/src/trust/current_trust_admission_tests.rs'
s=(base/rel).read_text();start=s.index('#[cfg(target_os = "macos")]\n#[test]\nfn the_native_read_admits');end=s.index('\n}',start)+2
control=s[start:end].replace('fn the_native_read_admits_the_written_store_and_rechecks_state_v1()', 'fn f9_native_fenced_read_admits_a_refreshed_store_after_the_old_calendar_expires()')
control=control.replace('fixture::generate(&Spec::default())', 'fixture::generate_at(&Spec::default(), utc("2028-10-02T00:00:00Z"))')
control=control.replace('let obs = hour_later();', 'let obs = observation(3607, "2028-10-02T01:00:00Z");')
control=control.replace('reread()', 'reread_at(utc("2028-10-02T01:00:00Z"))')
(b/'current_trust_admission_tests.rs').write_text(s+'\n\n// F9: native filesystem/fence with an explicit future observation, not OS clock qualification.\n'+control+'\n')
