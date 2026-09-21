# Generated source layout and inventory follow-through

Keep the existing package boundaries and dependency directions. The platform crate owns OS mechanisms, security owns custody and trust interpretation, lifecycle owns installation selection syntax, storage owns marker/ledger mechanics, and host composes those owners. Equal observed fields do not create authority. Inventory entries describe those actual responsibilities, including their limits.

Move exactly these three physical source files into `crates/security/src/generated/`, preserving their bytes and Rust module ancestry through their current private wrappers:

| File | Contents | Handwritten wrapper |
| --- | --- | --- |
| component_manifest_shape.rs | Structural manifest schema predicates | component_manifest.rs |
| trust_record_shape_nodes.rs | Closed trust-record schema predicates | trust_record_shapes.rs |
| trust_record_visit_nodes.rs | Typed reference visits from schema and reference registry | trust_record_reader.rs |

Split the constant data from `metadata_unicode15.rs` and `metadata_casefold15.rs` into `generated/metadata_unicode15_tables.rs` and `generated/metadata_casefold15_tables.rs`. Retain handwritten normalization/folding functions in their existing wrappers. Preserve table contents, Unicode versions, identity gaps and module visibility; no semantic rewrite is intended.

Provide one offline developer command, `tools/generate_security_tables.py --check`, and an explicit write mode. It must verify exact schema/registry/Unicode input pins before generation, generate into an isolated directory, format with the pinned Rust formatter, and compare all five outputs without modifying the repository in check mode. The generator must not run implicitly in Cargo builds or fetch network data. Its helper algorithms and input registry must be accounted for in the inventory and provenance; exporting the reviewed registry must not invent new edge targets or replace shape admission. Keep generator inputs separate from runtime crate sources.

Rust implementation filenames use snake_case; JSON data uses kebab-case. Existing evidence/corpus labels remain traceable to their generating checkpoint. An embedded architecture token such as x86_64 is not a factory naming decision. Any newly introduced factory module must use the agreed subject_factory.rs pattern. No factory rename is currently needed for these213 unlisted paths.

The next inventory successor must account for all213 paths plus the new generator/input/table paths, remove no inherited row without an explicit successor, preserve the20-package dependency DAG, and retain the distinction between fixture, generated data, handwritten validator, OS adapter and public API. Adding rows is not runtime/source-policy acceptance.

The623629-byte trust.rs remains a maintainability concern. Do not mass-split it in the same mechanical generated-file change. Before product materialization, identify and separate its remaining logical owners without widening private visibility, dropping tests or changing full reference/budget behavior. Current extracted trust/ modules are useful boundaries; checkpoint numbers in fixtures are provenance, not a desired module API.

Required next evidence is byte-preserving moves, exact table-content comparison, reproducible generator output, source pin refusal and no-write check behavior, then the affected crate tests and workspace lint. Independent review must assess the actual resulting source, not accept this plan as implementation. Native authority, five-field binding, writers and later product milestones remain separate unfinished work.
