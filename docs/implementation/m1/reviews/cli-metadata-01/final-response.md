**Verdict: CHANGES-REQUIRED.** Two findings block acceptance. The rest of the candidate held up under testing. I wrote `review.json` and `review.md` to `/tmp/opensip-implementation/m1-cli-metadata-review-01/`. The frozen subject still matches its pins after the review: manifest `67e7b09f…`, all 97 files, nothing extra or missing.

## Required findings
- **RF-1: `crates/platform/src/entropy.rs` isn't in the design-locked inventory v3.** Every other new file is. The accepted inventory has no named home for the random draws the RequestId law requires, so this is a real owner gap. The smallest fix is either:
  - a scoped inventory successor that adds exactly that one row, bound through the existing design-lock route; or
  - moving the 10-line function into a platform file that's already listed.

  Neither changes behavior.
- **RF-2: human-format failure output leaves out the termination class and error code.** The inventory4 human renderer rule says it "never omits termination-class". What the binary printed:
  - `opensip --nope` printed only `Unknown command option. Use opensip help.`
  - `--format=sarif` printed a sentence but not `OUTPUT.FORMAT_NOT_APPLICABLE`.
  - With stdout on a read-only descriptor, stderr got only `Required output delivery failed.`: no class, no `DELIVERY.REQUIRED_FAILED`, no RequestId.

  JSON output is correct. The fix is to print those fields with fixed labels and add tests. Whether the rule also covers successful help/version output, and how it applies to completion scripts, is a separate owner question (advisory A-10).

## Advisories (non-blocking)
- **Closed stdout isn't detected:** `opensip version >&-` exits 0. Rust's runtime reopens a closed stdout as /dev/null before `main` (I confirmed this in the std source), so the program can't see it. CLI-UNIT should say so. A read-only descriptor and a broken pipe are both caught correctly.
- **getrandom backend needs a build-lane guard:** a `getrandom_backend` cfg passed through RUSTFLAGS silently changes the backend. The dependency checker only covers the contracts lane. The r-efi 6.0.0 archive isn't cached, so its bytes weren't checked; it only builds for UEFI.
- **Still open, not satisfied:** `projection_tests.rs` hasn't been created, and the HostAssetPin channel-agreement check can't run until real asset pins exist. This must not count toward M1.
- **Also recorded:**
  - no bootstrap-level test for a CSPRNG failure;
  - uneven parser limits on flag values;
  - usage text differs from the inventory4 spellings;
  - the process-only host must not be reused at M2;
  - the reference checker is hard-wired to candidate-01;
  - the delivery-failure envelope drops `clientCorrelationId`.

## What held up
- **Request context:** callers can't forge it, and its ID comes only from its own host's registry. The ID is allocated before argument parsing. 600 runs gave 600 distinct IDs, and every attempt to supply a request ID by flag, word or environment variable was refused or ignored.
- **No outside effects:** in a macOS sandbox denying network, all writes, and reads of the project directory, `/Users` and `/private/etc` (each denial checked first), every metadata command gave identical output.
- **Version can't be spoofed:** release-channel environment variables and `--build-channel=release` have no effect.
- **Schema conformance:** 17 author cases, 11 extra probe cases and 5 delivery-failure envelopes all pass the original envelope4 schema.
- **Commands and delivery:** only the 3 implemented commands are advertised, consistently across help, JSON and completions. Read-only descriptor and broken-pipe failures exit 4 with a valid stderr envelope carrying the same RequestId.
- **Dependencies:** library dependencies stay within the allowed table. The getrandom, libc and cfg-if archives match `Cargo.lock` and their extracted sources.
- **Unchanged by this candidate:** the generator's partial status and the 45-command goal.

## What I ran and its limits
- **Build and tests:** in my own copy with a separate target directory, build, test and `clippy -D warnings` (all `--locked --offline`) plus `fmt --check` pass: 5 startup, 2 request-authority, 1 compiled-metadata and 10 identity tests.
- **Other checks:** `verify_design.py` passes. The reference checker, pointed at my build, gives 17 valid cases. I also ran 35 argument probes and the delivery-fault, sandbox and ID-freshness probes.
- **Limits:**
  - Everything ran on macOS arm64 in a debug build; nothing on Linux, no release build, no startup-performance measurement.
  - I couldn't trigger a CSPRNG failure in the real binary.
  - This review doesn't cover the generator or adapter, and doesn't accept integration or M1.
- **Files:** probe outputs are under `work/`. Nothing was committed or pushed, and nothing outside the review directory was changed.
