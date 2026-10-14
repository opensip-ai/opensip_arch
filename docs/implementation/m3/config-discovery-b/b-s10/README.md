# B-S10: configuration schema admission materialization

**Design unit, contract successor (materialization form). PROPOSED; arch only until bound.** This is the prerequisite of M3-B unit B1-a that the accepted B1-a plan names (`../b1-a/PLAN-r2.md` §2; Codex `codex-b1a-plan-r2` ACCEPT, with NBO-01). The product validates schemas at runtime only through the admission registry (`SOURCE_PINS`), and `verify_design` binds `schemas/admission-registry.json` to an accepted architecture copy. So the two configuration carriers need a new accepted copy before B1-a can admit them.

## What it selects

- **`admission-registry.json`.** The parent registry (`docs/implementation/m3/native-publication/rust3-identity-materialization-r1/admission-registry.json`) plus two rows, sorted by schema ID:
  - `urn:opensip:product-configuration:2`, which is PCS (`docs/coop/design-corrections/foundation/product-configuration.schema.v2.json`, `591a66e5…`);
  - `urn:opensip:preview-configuration:1`, the preview v1 carrier, through the copy below.
- **`preview-configuration.schema.v1.profiled.json` (lead decision).** The product's exact schema profile (`crates/identity/src/schema.rs`, `opensip-exact-schema-reference-1`) admits no `$comment`. The accepted preview carrier (`docs/coop/completion/preview-configuration.schema.v1.json`, `74b3a3f5…`) has exactly one: a top-level prose note on the paired reader.
  - The copy removes that one member: line 603, and the comma that ended line 602.
  - Every validating keyword is unchanged; the build asserts the two documents are equal once that member is dropped.
  - The parent stays as historical bytes.
  - **Rejected:** widening the schema profile's annotation set. That changes a selected profile for one prose note.
- **`product/`.** Exact copies of every product file the change touches. The product commit copies them byte for byte:
  - **Generation sources.** PCS joins `schemas/registry.json` (owner `crates/host/src/configuration.rs`, major 2), `schemas/source-map.json` and `tools/contracts/options.json`, as namespace `ProductConfiguration2` in module `invocation`, because it is an input carrier.
  - **Admission-only.** The preview v1 carrier joins the admission maps only (B1A-PLAN-R2-NBO-01).
  - **Pins.** Both sources join the identity `SOURCE_PINS` and the host's and storage's identical `SOURCES` lists, which host `admission_tests` requires to be equal; its count assertion and two comments go from 48 to 50. The generator closure gains PCS's row and re-pins `source-map.json` and `options.json`, and the registry recipe is re-pinned.
  - **Regeneration.** The pinned contracts generator regenerated two outputs: `crates/contracts/src/generated/invocation.rs` (the new `ProductConfiguration2Root` carrier) and `apps/report/src/generated/report.ts`.

## Evidence

- **Scripts and records.** `evidence/prepare_b_s10.py`, `run_b_s10_generation.py`, `run_b_s10_checks_r9.py` and their records.
- **Checks r9** (lane held, priority 10, private TMPDIR):
  - rustfmt on the hand-edited files;
  - the identity and contracts test suites pass;
  - Clippy, warnings denied, over identity, contracts, host and storage;
  - host and storage suites run `--no-fail-fast` on the base checkout and on the candidate, with identical failure sets: host 8 and storage 33. These are pre-existing crash-matrix synthetic cases, failing identically at base (`base-admission-tests.log`).
- **Two pre-existing conditions,** recorded and not changed here:
  - the identity dependency policy fails its source census at base and candidate alike (`checks-r9/identity-policy-baseline.json`);
  - neither the host nor the identity crate is rustfmt-clean at base.
- **The report TypeScript lane** runs `verify_design`'s admission preflight, so it can pass only once this successor is accepted. (r2, NBO-01) The scratch verification runs only `verify_design.verify`, with a synthetic appended entry: that admission preflight passes. The actual report lane, and the standard `generate_contracts.py` check, run at integration after real acceptance and assent, with the bound lock in the candidate worktree.
- **(r2, RF-01) Recipe admission.** The registry recipe's `optionsSha256` follows the candidate options bytes, and the generation runner first passes the standard recipe admission (`tools/contracts/admission.py` `registry()`).
- **History.** `evidence/history/attempt0-3`:
  - attempt 0: unsorted generator options;
  - attempt 1: output module changed to `invocation`;
  - attempt 2: `$comment` refused by the profile;
  - attempt 3: storage `SOURCES` missing;
  - attempt 4: the recipe options pin was stale (round 1, Codex B-S10-R1-RF-01), and the new standard recipe admission then refused the unsorted `registry.json` source row.

## Standing

No resolver semantics; those are B1-a's. No law change, and no new consumer of either schema yet. Not bound until Codex's ACCEPT-DESIGN-UNIT, the lead's assent, and its own lock commit.
