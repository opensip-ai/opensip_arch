# Independent Grok review: admission-runtime-selection v1

**Reviewer:** Grok (explicitly authorized). Root remains lead. Not Claude agreement.
**Verdict: ACCEPT-DESIGN-UNIT**
**subjectManifestSha256:** `239574c80fa6c24a2eceb534fd747029190d77017489f69c7bd358c73230f64a`
**requiredFindings:** none

Bounded composed unit: 48-source private interpreter, 15 current aliases, 19-domain `IdentityCandidate` (shape/order/path/H, not closure), host compile-time embedding, design-binding admission guard. Not complete M2, native analysis, report profile 6, M6, historical readers, or publication.

## Custody

| Manifest | Bytes | SHA-256 | Members |
| --- | ---: | --- | ---: |
| Selection `admission-runtime-selection-v1-subject.json` | 17287 | `239574c8…f64a` | **76/76** |
| Implementation trial `trials/admission-runtime-01/subject.json` | 43776 | `37c21ff8…062e` | **244/244** |
| Implementation archive | 1426608 | `b8d9c989…0101` | pin match |

Successor parents (sorted) pin: combined-corrections `219a9277…b65e`, source-selection-v3 `e638c55c…4ae4`, exact-schema-profile `fe1ebd49…1940`, inventory v11 `0ae9d439…1f62`. Successor candidates **75** = subject files minus `successor.json` itself; SHA-equal; sorted. Materialization map **22/22** match selection product and implementation product.

Live lock before this unit: **9 inventory / 12 contract**. Inventory v11 is already live (15 new paths). This unit is the topological **13th contract** append. Generation `registry.json` / `source-map.json` in the candidate **byte-equal live 40**.

Work stayed under `/tmp/opensip-implementation/m2-grok-admission-runtime-selection-v1-review/review`. Frozen/live/history not edited. Isolation receipts keep original `/tmp/...-candidate-01` paths; reproduction used a private product copy.

## Code (not packaging)

Identity remains `#![no_std]` + `sha2-const-stable` only. `Program` lives in a private `schema` module and is **not** re-exported. Public surface: `RegisteredSchemas`, `SchemaHandle`, `ShapeValue`, `SourcePin`, `SchemaAdmissionError`, plus `IdentityDomain` / `IdentityCandidate`.

`from_sources` checks count, positional length, SHA-256, `$id`, then owned preflight. `record_schema` binds logical document → current `$id` then **refuses non-current digest** (`SourceBytes`). Report-projection empty selector is `UnsupportedCodec` **before** `admit_json`. Defs such as `/$defs/ReportViewId` remain C-shaped. `include_bytes!` order in host `schema_sources.rs` **equals** `SOURCE_PINS` (48/48). Host `embedded_schema_registry()` is the explicit constructor; CLI `help`/`version` still only `MetadataHost` (no registry).

`IdentityDomain` is exactly 19 names; all exist as identity-v3 `$defs` keys (`fact`, not `Fact`). `IdentityCandidate::from_json` admits shape, runs imperative `ordered()` (path/LF, array laws, stage DAG), then domain-separated H. Missing joins still yield a candidate; it is not a `ReplayedRun`. Nested `CandidateError::Schema(Mismatch|Json|Limit)` is preserved in host tests (`{}` mismatch vs budget 0 Limit vs `-0` Json).

Admission registry: 48 sources sorted by `$id`, 15 unique sorted aliases. `verify_design.admission_sources` compares the **entire** registry (and aliases) to **accepted architecture pins**; implementation bytes must equal those pins. A local rehash cannot authorize. On the current 9/12 lock, `verify_design --implementation` reports `generationSources: 40` and **does not** emit `admissionSources` — the 48-source guard activates only when `schemas/admission-registry.json` is among selected contract-successor inputs. That is the intended post-selection switch, not a map bypass.

Host Cargo.toml adds only `opensip-identity` (inventory v11 already lists that edge). Contracts stay a leaf. No new crates or external packages.

## Reproduction (private copy)

| Check | Result |
| --- | --- |
| `cargo fmt --all --check` | 0 |
| `clippy --workspace --all-targets -D warnings` | 0 |
| `cargo test --workspace --all-targets` | **61/61** |
| `test_design_binding.py` | **64/64** |
| `check_dependencies` / `check_package_edges` (inventory v11, host lane) | passed; host→identity present |
| `verify_design` on candidate product + live 9/12 lock | passed; 40 generation; no admissionSources |
| External `use opensip_identity::Program` | **E0432** |
| External `IdentityCandidate { … }` | **E0451** |

Did not re-run 2081/26570 oracle corpora or host/provider isolation exports (receipts remain original tmp paths). Those remain finite development evidence as stated.

## Limits (not waived)

Not complete M2, native analysis, report codec profile 6 (27 829 365 / depth 39), M6 resource qualification, historical retained readers, or signed release. Interpreter work budgets stay explicit and unselected as product law. After lock selection, the 48-source guard must run; do not treat generation-40 preflight as admission-registry coverage.

## requiredFindings

[]
