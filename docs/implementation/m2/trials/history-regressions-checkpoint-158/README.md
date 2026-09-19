# Historical decoder regressions — candidate158

Private, uninstalled, unselected test-only successor157. Addresses actual Claude152 T1, N2 and N5 without changing production decoder bytes. One fixture appends exactly three canonical schema-refused rows: recordSchema3 on a schema1 shape, recordType SEAL on that shape, and lowercase z in wallClockData. Prior1624 fixture bytes remain identical. Total1627 cases:214 admitted,1413 refused,14 historical kinds. The only Rust edit changes the fixture-count assertion.

An owner check adapted from Claude's independent structural extractor compares closed kind sets, required/properties fields, enum vocabularies, scope and residual bounds to the SHA-256-pinned frozen schema. It exits nonzero on mismatch or an unrecognized extraction shape. Other numeric/string constraints are printed for inspection; this is not a proof of all Rust control flow. Three compiled vocabulary-extension mutants (effect class, revocation reason and terminal cause) must fail this structural check even though no sampled fixture contains those invented words. Three separately compiled behavioral mutants must fail the Rust fixture test. The original reviewer script's hash and the adaptation are preserved.

The cumulative fixture provenance now records all1627 rows, schema/canonicalizer pins, Python/UCD versions and exact prior-byte preservation. The original152 provenance and followup-r2 record remain historical evidence; they are not rewritten.

## Limits confirmed by152

The platform_historical_alias accessor communicates historical meaning; document() also exposes the immutable whole document, so the accessor name does not enforce exclusive access or prevent a caller from trying the current parser. Every admitted fixture must still be refused by JournalRecord::parse. Future consumers must preserve historical labeling.

The historical decoder enforces canonical input itself. The existing terminal_body helper canonicalizes and relies on its caller's canonical gate; do not lose that gate in a unified reader. Free strings can contain escaped controls, DEL, U+2028 and other schema-permitted code points. They remain opaque historical data; rendering and logging need their own admission/escaping. No vocabulary extension, normalization policy or type-level authority claim is added here.

## Validation

114 security tests, strict workspace/all-target Clippy, three compiled behavioral mutants and three compiled structural mutants plus baselines pass.342 product pins,340 unchanged157; two changed files are fixture and test assertion. Production prefix equality is checked against157. No isolated host repeat for this test-only delta;157 host99 is evidence for identical production sources, not a claim that it ran the new fixture rows. Actual review remains required. All previously listed custody, host composition, production authority, migration, selection and M2–M6 obligations remain open.
