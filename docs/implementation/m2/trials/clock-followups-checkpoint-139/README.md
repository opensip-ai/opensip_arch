# Rust clock review followups139

Private uninstalled successor136,330productpins325unchanged: two source files and three fixture corpora. No predicate or error mapping changes. Addresses actualClaude134T1/T2/N1; independent review required.

Two genuinely signed recovery epochs straddle the horizon edge in opposite directions within the issue skew: issuedAt one second after edge with wall at edge refuses TIME_RANGE; issuedAt at edge with wall one second later applies. OpenSSL signatures independently verified by reference138 carrier; deterministic keys are public test-only seeds with no authority. Expectations come from the reference, not Rust. Two clock rows (ordinary/report-only) keep continuity exactly at the final calendar second; ordinary plausibility refuses rather than wrongly classifying it as out of range. Existing corpora remain exact byte prefixes: clock1892→1894, recovery871→873, epochs282→284.

A comment explains Input(TIME_RANGE) on checked wall ±1day is unreachable with calendar-admitted observations; Refused(TIME_RANGE) is the reachable derived-horizon result. No new public renderer or typed admitted-record clock adapter is claimed.

80 security tests and strict workspace Clippy pass. Baseline plus two compiled mutants demonstrate the new regressions detect replacing issuedAt with wall and making continuity's maximum exclusive. Fresh host85 final source passes296 workspace+2doc,210sourcepins51archives. Fixture provenance updates exactly three rows; no frozen parent or selected product changed. Pending root/aggregate reviews and production current revocation population binding, typed record adapter/public projection, custody/SQL/history/generation, pin host workflows, selection, M2 and M3–M6 remain open. No cumulative approval.
