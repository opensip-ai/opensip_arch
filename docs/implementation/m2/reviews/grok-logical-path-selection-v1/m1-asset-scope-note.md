# M1 HostAssetPin / buildChannel scope note

This note is **not** a waiver, successor, or fake pin. It states what accepted text already requires, where it conflicts, and what is actually implemented. Root should resolve the reading before a fresh blind consumer.

## What is implemented now

- Live `crates/reporting/src/assets.rs` compiles a single `BUILD_CHANNEL = Development`. Metadata help/version emit `meta.buildChannel: "development"`. Startup tests ignore `OPENSIP_BUILD_CHANNEL=release` and still expect development (`apps/cli/tests/startup_tests.rs`).
- No `HostAssetPin` / `HostAssetPinV1` type or constant exists in the live product (search of `*.rs`/`*.json` under the product tree is empty).
- Metadata-only M1 ingress (`apps/cli/src/bootstrap.rs`) constructs no project, storage, provider, or asset load. Coverage method for metadata commands: “No project/store/component initialization, helper execution, network or **asset loading**.”
- Full report bundle, private asset pin, and selected-projection digest join are unimplemented.

## Accepted texts that pull in different directions

**A. CLI metadata unit** (`docs/implementation/m1/cli-metadata-unit.v1.json`, ACCEPTED-IMPLEMENTATION-UNIT, `integrationApproved: false`) lists remaining integration obligation:

> `HostAssetPinV1 channel agreement`

**B. Coverage verification method** (`docs/implementation/m1/source-selection-v2/implementation-coverage.v4.json` metadata command, standing `not-executed`):

> `BuildMetadataV1.buildChannel` and `HostAssetPinV1.buildChannel` derive from one compiled build selection; disagreement refuses at **build time**. `crates/reporting/tests/projection_tests.rs` owns the compiled producer/channel-agreement negatives.

That file does not exist in live reporting. CLI03 notes already recorded that inline renderer tests “do NOT close HostAssetPin channel test.”

**C. Build plan** (`docs/v2/architecture/implementation-boundaries-and-build-plan.md`):

> Load-time integrity uses a build-embedded `HostAssetPinV1` … of its **private asset manifest**.
> “At load, **and only when an asset-consuming renderer has been selected**, `reporting/assets.rs` resolves the manifest …”
> Assembly “compiles the manifest’s exact length and raw SHA-256 into the host binary as `HostAssetPinV1` with its `buildChannel`.”

**D. Report-assets unit** (`docs/implementation/m1/report-assets-unit.v1.json`) final integration duties include:

> Actual report asset inventory and offline bundle, private compiled HostAssetPinV1 with the sole buildChannel, and the join of VerifiedBundle.projection_sha256 to the compiled selected projection schema digest

That unit is fixture-algorithm acceptance, not product bundle integration. Full report/release is M4/M6 in active-work checkpoints.

**E. Active work / checkpoints** (do not invent an unused fakepin; no asset-consuming runtime yet; do not inflate M1 to full M4/M6; HostAssetPin / shared BUILD_CHANNEL / projection join remain open).

## Ambiguity (for root, not for this reviewer to close)

1. If **A+B** are read as an M1 metadata gate, both compiled values must exist now so a build-time disagreement test can run. There is no selected report-asset manifest to pin, so the only way to satisfy that reading today is a **dummy pin** — which **E** and the user instruction forbid.
2. If **C+D** are read as the owner of the pin, HostAssetPin is a **load-time** check of a real shipped bundle, exercised **only when an asset-consuming renderer is selected**. Metadata help/version never open assets, so the pin is not required to *execute* at metadata-only M1. The **channel agreement** still becomes mandatory at the moment a real pin is compiled: pin.`buildChannel` must be the same sole compiled `BUILD_CHANNEL` already used by metadata.

These two readings are not equivalent. This reviewer does **not** waive A or B, and does **not** invent a unused fake pin to pretend they are closed.

## Recommendation (not an assent)

Keep the live compiled development `BUILD_CHANNEL` as the one metadata-visible selection. Do **not** compile a fake `HostAssetPinV1` for metadata-only M1. Treat private pin + channel-agreement refuse-on-disagreement + projection-schema join as **mandatory before M4 asset-consuming integration** (and as still-open CLI remaining obligation text until that real pin exists). If root wants B’s “build time” clause to bind M1 anyway, that requires a **real** selected manifest to pin, not a dummy — which is a product decision, not a review waiver.
