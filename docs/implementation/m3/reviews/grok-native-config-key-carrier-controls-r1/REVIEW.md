# Native configuration key carrier boundary controls

ACCEPT.

These are supporting schema-shape controls for the existing `CargoConfigProjectionV2` key arrays. A fresh unchanged first-party identity build loads the complete current registered source set, and 24 supplied records enter the actual `admit_json` selector. Inventory stays at v184 with 144 successors. Contract successors stay at 161. Product code, the design lock, and accepted law stay unchanged.

## Subject and cutoff

Subject manifest `docs/implementation/m3/native-profile/config-key-carrier-controls-r1-subject.json` is 2886 bytes, SHA-256 `d0a2146f4b11dcbe5dfbdf9d8ad0a405c21a65b093656d8f42896702340efb0e`, with one trailing newline. Its 12 members are unique, sorted, and byte-identical to the named files.

Live product HEAD `d4b7ce130406875e1ccf4647254bc457c3fb766e` is clean. Its subject is “Bind reviewed NCA-1 configuration association and key records.” It parents `e35fc24009e7be34ff1707b087379cc1b7d4811b`. The only change at that commit is `design-lock.json`. Live architecture HEAD `097fc1e8c503bca80d22d0982e97c83181c83d7b` matches the cutoff. Its subject is “Select conditional native config association and complete key records.” Its parent is `35630f75be3e33a19d0bb511831bd5776fc02b95`. The only untracked architecture path is `docs/implementation/m3/syntax-e/e2s/`, outside this packet. This control directory is absent from both heads.

`design-lock.json` is 627281 bytes, SHA-256 `7798b8d47964e4e91a82e7dff6eb5efd965f6ab90c60dca67e01b8f29d2cd465`. It holds 144 inventory successors ending at v184, 161 contract successors, 103 inventory passage rows, and 46 inputs. The contract tail is the bound NCA-1 successor. `source.json` records the same product head, architecture head, lock blob, inventory 184, and 161 contract successors. Its NCA-1 subject, unit, and review pins match the architecture head: subject `717ba5e28778418e6cda0669ceeca1a977ba47d4c935d45789491f59445866e3`, unit `c5cb25cbeef3fd78feb5001e20ca78b74d4502a4b8dd34ad30762ff0d9d90812`, and review `ba8103cecb6051065c4a4e0d86790b57967dcca9713b0a10d3a132ca6c1edb4e`.

## Current source registry

`schemas/sources/native-v2.schema.json` is 294866 bytes, SHA-256 `81d57d6d68bd1c310d632148fe3c4c3b9b23e224603465e1a9f43062cc8f0712`. `RegisteredSchemas::source_requirements` lists 48 documents. Each pinned length and SHA-256 matches the product tree, including that native document at `urn:opensip:product-v1:native:evidence-schemas:v2`. `from_sources` refuses a different count and any byte or digest mismatch before it compiles the registry. The shape driver reads every requirement from the product root and selects `/$defs/CargoConfigProjectionV2` on that native id.

The authority document `docs/coop/design-corrections/native/native-evidence.schemas.v2.json` remains 277967 bytes, SHA-256 `2d37b810bd9ffed741d74241fc8a11051606862d8af2f152eed16b92bdc66043`. Its `CargoConfigProjectionV2` object equals the current definition: both key arrays keep `maxItems` 64, item `minLength` 1, item `maxLength` 256, and `uniqueItems`. The two schema files differ in size. The Python reference and the first-party decoder both evaluate the current native document. The authority file is the equality witness for this definition.

`admit_json` counts string length with `chars().count()`, which is Unicode scalar length for these records. The separate canonical bound in `canonical.rs` remains `MAX_BYTES` at 4 MiB. The largest stored record is 872 bytes of compact JSON. Whole-document canonical saturation stays untested.

## Twenty-four shape results

`cases.json` is 25224 bytes, SHA-256 `104439b30d42928a5e8eb8137aca7e33a25ef443c54893de5cfc4ba1de867120`. It holds 24 records. The captured stdout has the same 24 `PASS` lines in that order, and `controls.stderr` is empty. An independent Draft 2020-12 evaluation of the current `CargoConfigProjectionV2` definition agrees with every stored `expectedValid` flag.

The fixed carrier base is schema version 2, empty replacement paths, an empty rustflags projection, `ancestorCarrierVerified` true, `cargoHome` `private-empty`, `environmentProjection` `none`, `claimsCargoSwitch` false, and a 64-hex projection digest. Empty honored and stripped arrays pass. Each array accepts 64 distinct keys and refuses 65 at `maxItems`. A repeated `a` refuses at `uniqueItems`. A raw empty string refuses at `minLength`.

The encoded boundary strings match the accepted canonical string rule. Bare ASCII `a` repeated 256 times passes and 257 times refuses. Quoted `é` repeated 254 times is 256 Unicode scalars and 510 UTF-8 bytes, and it passes. One more `é` is 257 scalars and 512 UTF-8 bytes, and it refuses. Forty-two NUL escapes plus `aa`, written as `\u0000`, is 256 scalars and passes. One more ASCII character is 257 scalars and refuses. The empty named-segment spelling is the two-character encoding `""`, and it passes. The same seven strings are applied to both `honoredKeys` and `strippedKeys`. Scalar length and UTF-8 length differ on the quoted Unicode pair. These controls select no 256-byte cap.

The overlap record places `a` in both arrays. Both checkers accept it. Structural schema validation has no cross-array constraint. Complete semantic disjointness remains the accepted NCA-1 rule. `crossPopulationDisjointnessImplemented` stays false.

The encodings come from the closed NCA-1 notation binary recorded at 563408 bytes, SHA-256 `6d625773e717bf07c83b13be7d8a64ca6a29ce761f44a333e58a742c43944cc9`. This review reconstructed those seven strings from the canonical encoder and compared them with the stored cases. It did not rerun that binary.

## Build attestation

The identity build log is 457 bytes, SHA-256 `b68f343f0ae6364b`. It compiles `opensip-identity` from the product crate and finishes the dev profile in 1.48s. The bridge log is empty. The driver uses niceness 10, `cargo build -p opensip-identity --locked --offline`, an isolated target directory, explicit `cc` and `SDKROOT`, a mode-0700 private temporary directory for the build, and the shared lane taken and released around the build. HOME stays the inherited environment value. The fresh rlib and the shape program are authoring outputs. Their recorded digests are `b4c594925d2253dc20632853edd3c2893729a9b9e6938d7c0990b660042f5717` and `c8ab6be61047336cde4687a27f4c6049dc77593cc42820f663c993ade5d64b19`.

The before-and-after pin lists 21 identity Rust sources plus `Cargo.lock` and `crates/identity/Cargo.toml`. All 23 match the product head, and the Rust list is the complete `crates/identity/src` set. `shape_controls.rs` remains evidence. It is absent from the product tree. This review did not rerun Cargo or `rustc`.

The controls supply shape admission of supplied records. They leave original traversal, honor and strip classification, include capture, snapshot and cwd and read provenance, public failure routes, signed Tool, profile, owner, worker, full C2a and C3a, S-M, effective L, and qualification open. All six full native publication duties remain open.

This review did not run `verify_design.py`. Under the standing ML5 rule, this acceptance grants no dependent gate. An architecture-only support commit follows this acceptance, recorded root assent, and a current `verify_design`. There is no lock commit. Nothing is pushed.

Required findings: none.
