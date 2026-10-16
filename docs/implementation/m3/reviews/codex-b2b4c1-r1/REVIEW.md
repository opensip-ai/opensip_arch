# B2-B4C1-r1 review

Verdict: **REQUIRED-FINDINGS**

Subject manifest: 9,952 bytes, SHA-256 `401eaee9f64133703ce631088398cd97a42ceb8b998d1952b076cd2d75b9e65c`. Independently rehashed all 44 members. The three product-map rows match candidate and archive bytes; inherited parent pins match the requested product base. The candidate changes exactly the two mapped existing files and adds only tools/tests/test_discovery_census_blind.py. Main is clean at `d33df45ac0a5422efbebb43eee9c652d17ee742a`; architecture matches `a5b3fc88f7a84bbff40819679bd76172bcb60004`. All six source-authority pins and the unchanged lock pin match.

## Required findings

### B2B4C1-R1-RF-1: Check held-out identities, not only the number of rows, in the Rust margin test

Location: `crates/security/src/custody/discovery_census_tests.rs:620-640,680-721`.

The claimed coverage check counts outstanding/stale/measured/error rows and requires a total of ten, but never checks unique IDs or compares those IDs with the expected held-out manifest set. Ten composed passing rows all carrying the same ID, or a foreign ID replacing one expected entry, still satisfy these checks and yield holds (blind census) with gate=true. The Python receipt composer checks identities correctly, but the separately requested product margin test does not independently verify the composed artifact. The partial-coverage negative tests only the count, not same-count substitutions or duplicates.

Required change: Bind the Rust control to the expected held-out ID set from reviewed manifest evidence, reject duplicates and missing/unknown/substituted IDs, and ensure held-out statuses cannot replace lead-readable rows. Add same-count duplicate-ID and foreign-ID census-record negatives, plus an omitted lead-readable row/status-substitution control. Only exact coverage with all expected successful measurements may meet the gate.

### B2B4C1-R1-RF-2: Close the SystemExit and blind-mode detection gaps in exception redaction

Location: `tools/security/discovery_census.py:884-907,1127-1141`.

blind_row catches Exception, which excludes SystemExit, while __main__ explicitly rethrows SystemExit before the generic blind-mode redaction branch. A verification/model/helper exit such as SystemExit(secret_path) therefore reaches Python termination handling, which prints that string to stderr. In addition, the redaction guard detects only the exact literal --held-out-blind in argv, while argparse permits abbreviated long options by default; an accepted abbreviation enters blind mode without setting this guard. The current CLI canary only exercises an OSError with the full flag and misses both paths. This contradicts the before-run requirement that exceptions, including top-level ones, never disclose content.

Required change: Put the actual parsed blind execution behind a redaction boundary that also sanitizes message-bearing SystemExit, distinguishing intentional parser/help exits before any held-out access. Make dispatch/redaction agree for every accepted flag spelling, for example by disabling abbreviation and dispatching from parsed arguments. Add synthetic/subprocess canaries for SystemExit carrying a planted name/path and for accepted/rejected abbreviated flags; verify stderr/stdout contain only the permitted summary or generic failure, with no exception text.

### B2B4C1-R1-RF-3: Bind or verify the imported population-loader dependency before reusing a receipt

Location: `tools/security/discovery_census.py:868-875,974-999; tools/security/discovery_walk_vectors.py:37-67`.

receipt_bindings covers the census script and Rust cost closure but omits tools/security/discovery_walk_vectors.py, which load_reference imports and executes. That helper selects and loads the reference through ARCH/load, supplies MARKERS to reference_population, and reads the Python generator-closure configuration. Changing that helper can change the population/reference check while leaving every receipt binding unchanged; compose_held_out then continues to accept the old receipt as current. Existing drift controls change only already-bound inputs and do not exercise this executable dependency. The saved result is therefore not bound to all code that performed its population verification.

Required change: Include the imported helper and relevant reference/loading dependency pins in the receipt binding, or enforce their fixed accepted hashes before either a blind run or ordinary receipt reuse. Account for the configuration/closure inputs selecting executed reference dependencies. Use only public code/input pins, preserving the disclosure limit. Add a synthetic helper/reference-loader drift control showing that an old receipt becomes stale or is refused before composition, without opening a held-out store.

These findings are based on source inspection. No additional Rust execution or unpermitted synthetic command was used to demonstrate them.

## Other assessment

The blind row uses the same verified_tree, model, reference population and code caps as the ordinary census. Integrity failures and ordinary measurement exceptions are reduced to the stated classes; population differences disclose no paths or counts. Measured margins use integer floor division and a 2,000 threshold, which is equivalent to fitting twice for positive costs. The receipt generator emits the two planned row shapes and fixed public metadata. Its write target is only the receipt, followed by one outcome-count summary. RF-2 concerns bypasses around that intended error boundary.

The dedicated join requires the private mode token and heldOut is True. The existing store_path still requires heldOut is False. The ordinary census uses compose_held_out before its lead-readable loop, and skips held-out stores. No held-out workspace is admitted to the blind mode. The provided synthetic access spy and join controls support the separation.

Python receipt validation checks closed row keys, integer nonnegative margins excluding booleans, true integrity/population, passes2x consistency, unique IDs and a derived state. Exact manifest coverage is checked before current receipts compose. Treating manifest drift as stale before comparing current ID coverage is sound: the receipt no longer claims to describe the changed manifest, and cannot close the gate. This does not excuse missing identity validation of the composed record in Rust (RF-1).

Ordinary generation deterministically composes current receipts, preserves absent/stale outstanding states, and includes measured failures in failingEntries with caps returned to law. Mixed error/failure receipts remain incomplete while known measured failures still return the caps. Lead-readable and workspace computations remain unchanged. Workspace full-ledger margins stay outstanding. The Rust test correctly classifies measured margins and derives the aggregate state/cap result, but its ten-row arithmetic is not exact identity coverage.

The code preserves the existing census model and costs; the lead-readable generated census and vector files remain byte-identical to base because there is no real receipt. No production caller, environment read, law change or qualification is added. Inventory remains v198 with 164 contract successors. The new synthetic-test path requires the declared v199 successor, including the earlier description corrections; the eventual real receipt requires its separate follow-up. B2-b4c2 and the all-entry margin remain future work. This review does not authorize running the real blind census.

## Verification

Independently executed only the permitted candidate commands:

- Operability source census: 114 rows, passed with no findings.
- Existing census controls: 18 tests passed.
- New blind controls: 17 tests passed, using temporary synthetic stores/receipts only.
- Ordinary census --check over lead-readable stores/overlays: both generated records verified. No receipt existed.

Candidate map hashes remain exact after these checks, and the real receipt remains absent.

Assessed supplied Rust/lane evidence without running Rust or the lane. All 17 current check rows pass. The security comparison preserves the identical 14 baseline failures and 1,128 passes at base and candidate; this is not a full-suite pass. Recorded all-targets Clippy for host/security runs with warnings denied and completes successfully. The edited Rust test file has base-clean and candidate-clean formatting classifications.

All 18 recorded controls match their logs: seven Python guard mutations and eleven Rust census-record controls (four valid records accepted, seven invalid records rejected). The coverage-unchecked Python mutation is caught as an unexpected unittest error rather than an assertion failure; it is still a nonzero test outcome. None of those controls covers same-count Rust ID substitution, message-bearing SystemExit or imported-loader drift. Existing passing controls therefore do not resolve RF-1 through RF-3.

## Boundaries

No Cargo, rustc, Rust tests, builds, lane or network was run. No other panes or delegation were used. No T2 held-out store or overlay was opened, and --held-out-blind was never run against the T2 cache. No private fixture, installation directory, signing keys or held trees were accessed. No real receipt was written. Neither repository, the candidate worktree, the stage nor control files was edited. Only REVIEW.md and review.json in the requested directory were written.
