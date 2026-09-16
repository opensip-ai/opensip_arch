# Addendum: compiled build-channel agreement (`HostAssetPinV1`)

This is a follow-up after the archived fresh-blind `review.md` / `review.json`. It is not a second claim of pristine blindness and does not replace those files. Frozen subject 185 files and the archived review were not edited. No prior reviewer conclusions were supplied. Root still owns final M1 assent.

**Disposition for this clause: M1 requirement still missing.**  
Not vacuous satisfaction. Not silently deferred to HTML/M6. A reviewed schedule clarification would be required to move only this sentence.

## Selected clause (exact bytes)

Pinned `docs/implementation/m1/source-selection-v2/implementation-coverage.v4.json`  
SHA-256 `e785394993f95ba12e70359bd38181db136a0b849192751f745813d52335c25d`, 393383 bytes (lock candidate pin matches the architecture checkout).

Selector: `/groups/commands/30` `id=version` (array index 30), field `verification.method`.

The method, after the shared help/version envelope sentences, continues:

> M1 is development-only; env/caller release selection and invented closures refuse. BuildMetadataV1.buildChannel and HostAssetPinV1.buildChannel derive from one compiled build selection; disagreement refuses at build time. crates/reporting/tests/projection_tests.rs owns the compiled producer/channel-agreement negatives; apps/cli/tests/startup_tests.rs checks exact CLI package version and absence of caller/environment release switches.

The same sentence already exists in selected `docs/implementation/m1/metadata-v2/implementation-coverage.v2.json` `/groups/commands/30/verification/method`. v4 did not drop it.

`verification.standing` is `not-executed` (planning status). That does not cancel the duty. `moduleFirstMilestone["crates/reporting/src/assets.rs"]` is **M1**. `html_renderer.rs` is **M4**.

## Other selected sources (not the excerpt alone)

**metadata-v2 README (selected unit), lines 89–104**  
`crates/reporting/src/assets.rs` is the compiled metadata producer and the existing `HostAssetPinV1` constant owner. M1 defines **one** compiled development-channel constant there. Both `BuildMetadataV1` and **any fixture** `HostAssetPinV1` take their channel from that constant, never from environment or configuration. `projection_tests.rs` owns producer and channel-agreement negatives; `startup_tests.rs` owns CLI version and caller/environment release-switch refusals. If an explicit asset pin disagrees with the compiled selection, **build admission refuses**. Version uses only compiled constants; it does **not** read assets or their manifest. No new *producer* file is required (the owner is already `assets.rs`). M6 may later replace the development-only constructor after assembly refusals exist.

**report-asset-binding.v1.json** (lock input, SHA-256 `71363c0637d4405d9394782f805f33c294588834990614388a26a2dbd98027a6`)

- `/privateSchemas/HostAssetPinV1`: private, not a wire type; required fields include `buildChannel` enum `release` | `development`; owning module `crates/reporting/src/assets.rs`.
- `/buildTimeValidation`: report then release assembly compile the pin with `buildChannel`; a development build may pin **labelled fixture** assets only with `development`.
- `/loadTimeValidation/precondition`: performed **only when an asset-consuming renderer has been selected**. Absence of assets must not affect human/JSON.

**Build plan**

- Overridden M1 completion (metadata-v2 passage on line 885) requires development metadata, no project/provider/store/network, closure IDs from build-embedded metadata. It does **not** mention `HostAssetPinV1`.
- Lines 767–843 own load-time pin checks, HTML delivery, and assembly of real asset bytes. Those are the HTML/release integration, not a waiver of the version-row channel sentence.

**Inventory v10** still names `crates/reporting/src/assets.rs` (manifest/pin check) and `crates/reporting/tests/projection_tests.rs` (renderer/parity tests). Chapter 14 matches. Inventory is a naming guide for *unrelated* later modules; it does not delete this version-command method.

The short M1 table and the specific `version` verification.method are both selected. The table does not override the method.

## Frozen implementation (185 files)

`crates/reporting/src/assets.rs` defines

```rust
const BUILD_CHANNEL: Metadata1BuildMetadataV1BuildChannel =
    Metadata1BuildMetadataV1BuildChannel::Development;
```

and `development_metadata()` copies that into `BuildMetadataV1`. Unit tests check development + empty closures + SemVer. `lib.rs` exports only `development_metadata`.

`apps/cli/tests/startup_tests.rs` checks `CARGO_PKG_VERSION`, `buildChannel=development`, empty `closureIds`, ignored `OPENSIP_*` spoofs, and `--build-channel=release` as `REQUEST.UNKNOWN_OPTION`.

There is **no** `HostAssetPinV1` identifier, type, or constant in the frozen product sources. `crates/reporting/tests/projection_tests.rs` is absent. No compile-time disagreement refusal exists. The generated contracts expose `Metadata1BuildMetadataV1BuildChannel` only; the pin schema is private and was never handwritten.

No dummy `assetManifestSha256` is present. None should be invented.

## Reconciliation

| Fragment of the method | Status |
|---|---|
| M1 development-only; env/caller release and invented closures refuse | **Satisfied** (`assets.rs` + `startup_tests.rs`) |
| Version does not load assets; CLI package version | **Satisfied** |
| `BuildMetadataV1.buildChannel` and `HostAssetPinV1.buildChannel` from one compiled selection; disagreement refuses at build time | **Missing** |
| `projection_tests.rs` owns those negatives | **Missing** (file absent; no equivalent HostAssetPin disagreement test) |
| Load-time manifest digest / HTML asset use | **Later (M4)** per `loadTimeValidation.precondition` and `html_renderer` milestone |
| Compiling real labelled fixture or release asset bytes into the pin | **Later (report/release assembly, M4/M6)** |

Absence of `HostAssetPinV1` is not compliance. The invariant is that both records’ `buildChannel` fields are the same compiled selection and that a disagreeing pin cannot be admitted at build time. With no second record and no negative, that is unenforced.

“Any fixture HostAssetPinV1” / “if an explicit asset pin disagrees” forbids a **fabricated unused digest**. It does not authorize omitting the private type, the shared `BUILD_CHANNEL`, or the named negatives. A labelled fixture bundle is an assembly input, not a reviewer-made hash.

## What would satisfy this sentence without inventing a pin

Handwritten private `HostAssetPinV1` in `assets.rs` (the selected owner; not a new public schema). `buildChannel` on that type uses the same `BUILD_CHANNEL` constant as `BuildMetadataV1`. `projection_tests.rs` (named owner) holds producer/channel-agreement negatives that refuse a `release` pin against the development selection at **build/test** time. Do not compile a dummy path/digest until labelled fixtures or release assembly exist. Do not read assets on `version`.

Load-time open/read/verify of the manifest remains M4 when HTML is selected.

## Schedule clarification

If root wants the pin *type* and disagreement negatives to wait until the first asset bundle (M4/M6), that needs a **reviewed coverage/schedule successor** changing `/groups/commands/30/verification/method` (and the matching metadata-v2 README sentences). Silent deferral is not available.

## Effect on the archived ACCEPT

The archived `ACCEPT-M1-DEVELOPMENT` did not evaluate this sentence (it treated `projection_tests.rs` only as a naming advisory). **This clause is not covered by that ACCEPT.** Against this clause, M1 is incomplete. This addendum does not rewrite the archived review. Root decides whether overall M1 assent waits on the channel-agreement mechanism or on an accepted schedule successor.
