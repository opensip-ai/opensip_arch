# CLI metadata candidate: independent unit review

**Verdict: CHANGES-REQUIRED**

- **Subject:** `/tmp/opensip-implementation/m1-cli-metadata-subject-01`
- **Manifest:** sha256 `67e7b09fe028f657509537bcdc47312df1f34b46e0ebc43493816f4e62bdd4b1`. It matches, all 97 files match, and nothing is extra or missing. The pins were checked again after the review.

Most of the code is sound. Two findings block acceptance: one new file is outside the design-locked inventory, and human failure output leaves out the termination class and error code. The machine-readable record is in `review.json`.

## Required findings

### RF-1: `crates/platform/src/entropy.rs` is not in the design-locked inventory v3
- Accepted inventory v3 and the module layout list only these platform files: `clock`, `filesystem`, `lib`, `linux`, `locks`, `macos` and `process`.
- Every other new file in the candidate is in the inventory.
- Adding four paths earlier needed the reviewed inventory successor v3.

The inventory has no named owner for the OS CSPRNG draws that REQUEST-ID-V1 requires. This is a real gap in the accepted owners.

**Smallest resolution (either one):**
- **(a)** A scoped inventory successor adds exactly one row: `crates/platform/src/entropy.rs`, package `opensip-platform`, role adapter, description "Provide complete OS CSPRNG draws for operational identifiers; never an input to semantic identity". It is bound through the existing design-lock route.
- **(b)** Move the 10-line function into an existing platform owner.

Neither option changes behavior.

### RF-2: human failure output leaves out termination class and error code
The inventory4 human renderer rule says it "never omits termination-class", and it applies to meta commands. What the binary actually printed:

| Command | Exit | Output |
|---|---|---|
| `opensip --nope` | 2 | `Unknown command option. Use opensip help.` |
| `opensip version --format=sarif` | 2 | `The selected format is not applicable to this command.` (no `OUTPUT.FORMAT_NOT_APPLICABLE`) |
| `opensip version 1</etc/hosts` | 4 | stderr `Required output delivery failed.` (no `operational-failed`, no `DELIVERY.REQUIRED_FAILED`, no RequestId) |

The cause is in `human_renderer.rs:43-50`: for a failure it prints only the diagnostics.

**Fix:**
- For failure envelopes, print the termination class, errorCode and error detail codes with fixed labels, then the diagnostics.
- Printing the RequestId on the stderr delivery-failure path is recommended.
- Add human-rendering tests for request rejection, format-not-applicable and delivery failure.
- The JSON path needs no change.

How the same rule applies to successful help/version output and to completion scripts is left to the owner (A-10).

## Advisories (non-blocking)
- **A-01:** Running with stdout closed (`>&-`) exits 0 and the output is lost. Rust's runtime (`sanitize_standard_fds`) reopens a closed fd 1 as /dev/null before `main`, so the program can't see it. CLI-UNIT should say so. A read-only fd and a broken pipe are both detected correctly.
- **A-02:** The CSPRNG and collision failure paths are not tested through bootstrap. A plain stderr line with exit 4 is lawful: the D9 `pre-admission-host-io-failure` golden applies, and envelope4 can't be built without a valid RequestId. Consider an injectable-draw test, and consider adding `operational-failed/host-io` to that line.
- **A-03:** getrandom's backend is chosen at build time and needs a guard before qualification:
  - A `--cfg getrandom_backend=...` passed through RUSTFLAGS or Cargo config silently changes the trusted code. The build lane must refuse it.
  - On Linux the backend can fall back to reading `/dev/urandom`.
  - libc's build script runs `$RUSTC -vV`.
  - The dependency checker covers only the contracts lane.
  - The r-efi 6.0.0 archive was not cached and is only used for UEFI targets, so its bytes were not checked.
- **A-04:** Parser limits are uneven:
  - Values that follow `--format` or `--client-correlation-id` skip the 1024-argument and 4096-byte limits. The effect is bounded.
  - `version --help` is refused instead of treated as help.
  - The correlation token accepts control characters. That is schema-legal, and metadata review A-01/N-05 is still open.
  - Human-mode refusal text goes to stdout. I found no owner rule on streams.
- **A-05:** Usage strings in the catalogue differ from the inventory4 `cli` spellings. This is lawful because the catalogue is build-selected, but a later check should pick one source.
- **A-06:** `crates/reporting/tests/projection_tests.rs` has not been created, and the HostAssetPinV1 channel-agreement check can't run yet (no pin carrier or real assets). This is still open. It is not satisfied and must not count toward M1.
- **A-07:** The process-only host lets one context be used repeatedly. That is fine inside a single invocation. M2 durable ingress must replace this host for analyses and mutations. Delivery handling will later move to the inventoried `host/src/delivery.rs`.
- **A-08:** The reference checker has a fixed root path (candidate-01), so its frozen results came from that tree's binary. I pointed a copy at my own build and got the same 17 valid results.
- **A-09:** The delivery-failure envelope drops `clientCorrelationId`. That is schema-legal.
- **A-10 (proposed owner clarification):** Does "never omits termination-class" apply to successful help/version human output? Completion scripts should be exempt, since their stdout must stay valid shell code and the exit status carries the result.

## What holds up
- **Request context can't be forged.**
  - Callers can't construct a context, and it can't be serialized, cloned or copied.
  - An ID is read only by exact object identity inside its own host's registry.
  - Contexts from another host or never reserved return nothing (unit test).
  - Reservations live as long as the host.
- **Allocation happens before parsing.**
  - The ID is 16 CSPRNG bytes, rendered as `req1_` plus 32 lowercase hex.
  - At most 8 candidates are drawn on collision, and nothing is replaced.
  - 600 runs gave 600 distinct IDs.
- **Request IDs can't be spoofed.** `--request-id` in both forms, `requestId=` words and `OPENSIP_REQUEST_ID` are all refused or ignored, and every refusal gets a fresh ID.
- **Metadata commands touch nothing outside the process.** Under a sandbox denying network, all writes, and reads of the cwd fixture, `/Users` and `/private/etc` (all controls confirmed denied), every metadata path produced identical output.
- **Version can't be spoofed.**
  - The channel is a compiled development constant, `hostRelease` comes from `env!(CARGO_PKG_VERSION)` with SemVer validation, and closures are empty.
  - Release variables in the environment, a `CARGO_PKG_VERSION` environment variable and `--build-channel=release` have no effect.
- **Envelope4 conformance (ExactValidator).**
  - The 17 author cases pass.
  - 11 more parser/format probes pass.
  - 5 delivery-failure envelopes pass: read-only fd ×4 and EPIPE.
- **Refusals are lawful, and help matches the implemented commands.**
  - `errors=[]` appears only with UNKNOWN_OPTION, exit 2 and a nonempty diagnostic.
  - A known but unimplemented topic is refused.
  - Help, JSON and completions list the same three commands.
- **Required delivery failures are reported.**
  - A read-only fd or a broken pipe gives exit 4 and a valid stderr failure envelope with the same RequestId.
  - Rust's convenience Stdout treats EBADF as success (confirmed in the std source).
- **Library edges** are all within the module-layout table.
- **Generator status and the 45-command goal are untouched.**
  - Generator status stays partial, and the bindings were not re-reviewed here.
  - The full 45-command inventory4 goal is unchanged, and the CLI advertises only its 3 implemented commands.

## What I ran
All in a private copy with its own target directory:

- **Build and lint:** `cargo build`, `cargo test` and `cargo clippy -D warnings`, all `--locked --offline`, plus `cargo fmt --check`, all pass. Tests: 5 startup, 2 authority, 1 metadata, 10 identity.
- **Design verifier:** `verify_design.py` passes (46 inputs).
- **Owner pins:** the metadata-v2 and trusted-request-context.v3 hashes match their accepted pins.
- **Reference checks:**
  - A copy of the reference checker pointed at my build: 17 cases, 0 invalid.
  - 16 additional outputs validated with the same ExactValidator.
- **Probes:** 35 argv probes, delivery-fault probes, a sandbox run with working controls, and 600 invocations for ID freshness.
- **Dependency archives:**
  - The getrandom, libc and cfg-if `.crate` hashes match the lock, and each archive is identical to its extracted source.
  - The per-target dependency tree and the backend and build-script sources were inspected.
- **Outputs:** saved under `work/probes/` and `work/build-test.log`.

## Scope and limits
- This is a review of the concrete unit only. It does not review the generator or adapter, and it does not accept integration, design-lock binding or M1.
- Everything ran on macOS aarch64 in a debug build. Linux backends, other targets, release builds, startup performance (DR-G03), size and memory, and firewall qualification were not run.
- The sandbox evidence comes from denial controls, not a syscall trace.
- A CSPRNG failure could not be triggered in the real binary.
- The r-efi archive was not available offline.
- Nothing was committed or pushed, and no frozen, product or architecture files were changed. Everything I wrote is inside this review directory.

Once RF-1 and RF-2 are resolved and a new frozen subject is re-verified, the unit is expected to be acceptable. That acceptance would cover this unit only.
