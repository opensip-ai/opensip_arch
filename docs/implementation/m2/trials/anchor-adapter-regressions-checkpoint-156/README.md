# Conditional anchor adapter regressions — candidate 156

Private, uninstalled, unselected test-only successor to candidate155. Production bytes, dependencies and all36 fixtures are unchanged. This addresses actual Claude150 F1 and documents F2; it is not cumulative approval or proof of filesystem custody.

## Actual adapter coverage

Five additional tests use actual SQLite populations, operational-file codecs and physical captures. They distinguish grant-generation closure from project purge, preserve quarantine markers independently, select the requested generation, join the recorded run, take project identity from the admitted population, and pass the distinct after-read witness and floor slots into assessment. The latter uses the existing private bracket capture phase hook; no production hook or forged admitted capture is added.

Malformed markers are tested in both the queried and a different generation, during both the initial and second physical capture. The retry cases first produce a real malformed witness, then insert the malformed marker between captures. They require the exact population/marker failure, retained unusable raw bytes, expected retry count and successful WAL checkpoint after unwinding.

Nine compiled mutants recreate the nine actual Claude150 survivors: A1/A2 closure cause, A3 marker, A4 generation, A5/A6 after slots, A8 run, A10 project and R6 second-capture error downgrade. Each must fail an assertion in the actual journal-store tests; compilation failures do not count.

## Capture failure is an explicit outcome

The read operation returns a Result. Alongside the conditional assessment states, capture can fail before any successful assessment exists. A malformed marker prevents admission of the complete population, including when its generation is not the requested one. A failure during the second capture returns the error and drops the first owned capture; this API does not return partial assessment evidence on failure. Both transactions must release their WAL readers.

The eventual host must map MarkerUnavailable to unknown custody, never generic busy/retry, not-committed or marker absence. This candidate preserves the existing typed error; it does not implement or claim the public host mapping. The Python reference accepts a supplied projected quarantine flag. That precondition differs from production, which first admits marker bytes and the complete population and may fail at that earlier step.

Downstream consumers must accept the sealed AnchorAssessment and its captured evidence, not a caller-constructible ConditionalStanding enum alone (150 N1). Direct bracket capture retains a SQL reader; read detaches completed captures (150 N2). A covered requested-sequence-above-tail hazard is unreachable under the earlier floor-above-tail guard; this matches the reference law (150 N3).

## Validation and remaining scope

114 security tests and strict workspace/all-target Clippy pass. Nine compiled mutants plus an unmodified baseline pass their expected outcomes. The manifest verifies341 product files,339 byte-identical to155; the only changed files add cfg(test) code. Production-prefix SHA-256 equality is checked against frozen155. No full isolated host repeat is justified for these test-only additions; final155 host98 remains evidence for the identical production sources, not an assertion that host98 ran the new tests.

Location binding, retained ancestor custody/exclusion (124 F1), missing-carrier INIT, ABA exclusion, actual ledger association, current authority, clock/revocation binding, writers, public rendering and formal selection remain open. Historical and migrated admission changes in152/154/155 require their own actual reviews. Frozen bytes and all prior failed evidence are retained.
