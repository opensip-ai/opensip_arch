# Independent Grok review: CLI metadata03

**Reviewer:** Grok (explicitly authorized). Codex remains lead. Not Claude agreement.
**Subject:** `/tmp/opensip-implementation/m1-cli-metadata-subject-03`
**Manifest:** `/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m1/trials/cli-metadata-03/subject.json`
**Manifest SHA-256:** `d4cbfc02e6c7ada77dceec5928daa93a6aa996ff4c7ddefe210aca27403323a3`
**Members:** 231
**Archive:** `7cbda39d1d3ba19b5aeaad1961e9c4791f528cffdf67a6bdba8038fc76f247aa` / 1317508 bytes
**Verdict:** **ACCEPT-UNIT**

This accepts only the frozen CLI metadata03 bytes: help/version/completion/parser refusal, process-only RequestContext before parse, OS-CSPRNG draw, bounded envelope7 JSON staging, and selected L02 output-failure behavior. It does not accept generator/bootstrap, HostAssetPin channel agreement, getrandom backend/build-lane policy, assets, fresh blind consumer B, M1, or product release. The 45-command product goal is unchanged; this CLI advertises three implemented commands. No-args analysis is honestly unimplemented. CLI02’s actual Claude ACCEPT-UNIT (`9180e2a8…0e4c44`) is a predecessor on different bytes and is not current agreement for this unit.

## Custody

231/231 listed files and the adjacent `status.json` archive digest match before and after. Frozen subject was not executed against. Private exact copy of listed files only under `review/copy`. Product and architecture trees were not edited.

## Predecessor CLI02 (read-only) and L02

CLI02 closed RF-1 (getrandom wrapper in inventoried `crates/platform/src/lib.rs`) and RF-2 (human Termination/Error/Detail/Remedy/Request). Advisory **B-01** (Detail/Remedy labels not pinned) is **closed here**: the old drop-labels mutant now fails `human_failure_and_success_display_termination_and_registered_details` (5 other startup tests still pass). **B-02** remains: fish is not installed; no fish execution is claimed. **A-02** (no bootstrap entropy/collision injection in the binary), **A-03** (getrandom backend / `r-efi` still in the lock), **A-06** (HostAssetPin), and **A-07** (do not reuse this process-only host for M2) stay open and are not completed by this unit.

Selected L02 (source-selection-v2 `reference/L02-policy-selection.json`, semantic members inherited unchanged by selected v3) is complete-output-or-operational-failure. CLI03 matches that for this metadata process: serialization/write/flush failure is `OUTPUT.SERIALIZATION_FAILED` exit 4, fixed caller-free stderr, no second envelope after possibly visible normal bytes. Projection construction failure before output is distinct (`MetadataError::Projection` → delivery envelope or `DELIVERY.REQUIRED_FAILED`). This does not close RP-OBL-L02 source binding or final integration.

## Changed source versus CLI02

Material implementation deltas (not the extra freeze evidence/logs/schemas):

- Generated interfaces: `Envelope4` → `Envelope7Root`. Host `serde_json::from_value` is construction of a generated carrier, not semantic admission.
- `MetadataError::{Projection, Serialization}` split; JSON `render_json` maps capacity/IO encode failure to Serialization; human `render_human` `?` maps to Projection.
- `bootstrap.rs`: write/flush/`Serialization` → `output_failure()` only. CLI02 appended a delivery envelope on stdout failure; that second-envelope branch is gone.
- Parser: `take_value` increments the 1024-argument counter and applies the 4096-byte cap to option values.
- `json_renderer.rs`: inclusive 4MiB complete-emission bound including the newline delimiter; fallible `try_reserve_exact`; escaped UTF-8 byte counts. Direct `serde` dependency is declared. Three inline serializer stress tests use scalar values, not admitted envelopes.
- Human tests now pin `Detail:` / `Remedy:` / exact remedy text / line adjacency to `Request:` for format-not-applicable.

## Reproduction (private copy)

Rustc/cargo 1.95.0 (Homebrew). Node v24.16.0. TypeScript 6.0.3 from `/tmp/opensip-implementation/m1-joint-generation-candidate-03/tools/contracts/node_modules/typescript/bin/tsc`.

| Command | Result |
| --- | --- |
| `cargo test --locked --offline --workspace --all-targets` | exit 0; **22/22** (6 startup, 2 request-authority, 4 reporting, 10 identity) |
| `cargo clippy --locked --offline --workspace --all-targets -- -D warnings` | exit 0 |
| `cargo fmt --all -- --check` | exit 0 |
| `tsc` of `apps/report/src/generated/report.ts` | exit 0; emit byte-identical to freeze `compiled-report/report.js` `253031a9…82b3` / 1857983 bytes |
| Private `check-current-metadata.mjs` writing `metadata-independent-current/` (copied `metadata-current04/` not overwritten) | **29/29** envelope7 exact-reader admits, fresh request IDs, expected exits, empty stderr |
| Independent Python probes | **24/24** |
| B-01 drop-labels mutant | **killed** (exit 101) |

## Independent probes (24/24)

Environment `OPENSIP_BUILD_CHANNEL=release` / `OPENSIP_HOST_RELEASE=99.99.99` ignored (compiled `0.1.0` / `development` / empty closures). Host-minted `req1_` request IDs. Caller `--request-id` and `--build-channel=release` refused and not used. No-args: “Default analysis is not implemented…”. 1025 tokens: too many arguments. Option values count toward 1024 (1025th value → invalid correlation, not a successful unknown-command parse). 4097-byte option values refused and not echoed. Oversize correlation omits the field. 128-scalar unicode correlation accepted and distinct from request id. Non-unicode arguments refused. Escape topic never appears in human output. Human `Detail:`/`Remedy:` labels and registered remedy text for format-not-applicable; unknown-option path has empty errors and no Detail line. Read-only stdout JSON and human: exit 4, exact `OUTPUT.SERIALIZATION_FAILED: required output emission failed.\n`, no envelope on stderr. Real EPIPE (read end closed) for JSON, human, and completion: same exit 4 and same one-line diagnostic. No home/store/provider/config side effects. Completion+JSON is format-not-applicable. `--` not selected. Duplicate `--format` refused. Advertised catalogue is exactly `completion`, `help`, `version`.

Request-context foreign/unreserved projection and collision budget (8 draws, no replace, entropy error does not publish) reproduced as the two host unit tests.

Bounded JSON: escaped NUL bytes counted; UTF-8 character ≠ byte; inclusive 4MiB including newline; oversize returns error with no partial buffer — reproduced as the three reporting serializer tests.

Completion: `bash -n` and sourcing registers `complete -W 'completion help version' opensip`. `zsh -n`; `compinit` binds `_comps[opensip]=_opensip`; `#compdef` is first line. Fish text is `complete -c opensip -f -a 'completion help version'` plus `# Termination: success` **by inspection only**.

## Must-fix / should-fix

None in this metadata scope.

## Advisories (non-blocking)

- **C-01:** When an *option value* is the 1025th token, the diagnostic is “Invalid client correlation ID.” or “Expected --format…” rather than “Too many command arguments.” The bound is still enforced. Non-Unicode option values similarly collapse to the missing-value diagnostic, not the Unicode diagnostic.
- **C-02:** `delivery_failure` still omits `clientCorrelationId` (schema-legal). Write/serialization failure no longer emits that envelope at all.
- **C-03:** Generated `Envelope7Root` comments still describe “Joint unaccepted successor7”. That is generated commentary, not this unit’s admission claim. Shape match is not semantic catalogue/build admission.

## Preserved earlier failures

Freeze retains `test03` (stale envelope4 expectation), `test04` (oversized diagnostics vs generated field bounds), `test05` (`--locked` before regenerating the offline lock), `clippy03`, and `metadata-current03` as the prior parser run. They are not substituted for `test08` / `clippy04` / `metadata-current04`.

## Remaining (not completed)

HostAssetPin channel agreement; getrandom backend and full dependency-lane policy (lock still carries `r-efi`); generator/bootstrap; fresh blind consumer B; assets/CSP; M1 and release qualification. macOS aarch64 debug only. A CSPRNG failure was not induced in the binary. Sandbox evidence here is empty-cwd/env-clear plus no created paths, not a syscall trace.
