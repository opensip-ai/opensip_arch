# Package-parser inventory v26 — additive layout review

**Verdict: `ACCEPT-UNIT`**

Layout packaging only. Not SOURCE38, not safety38, not TOML dependency/profile acceptance, not parser implementation acceptance, not full enumeration, not runtime/replay. Frozen/live/history not edited. Safety38 advisory bytes were not modified. Root remains lead. Not Claude agreement.

Live `inventory_successor` (`opensip/tools/verify_design.py` 86–142) admits additive layout only when independent review `verdict` is **`ACCEPT-UNIT`**, `requiredFindings` is `[]`, and `inventoryCandidateAssessment.verdict` is `ACCEPT`. That is the token used here. `ACCEPT-DESIGN-UNIT` is the runtime/reference contract token and would be refused at inventory activation.

**subjectManifestSha256** `8e167a9332852630ecc08629e8a3f9af6b3dd08c6cdff337eb765b740956b32e`  
`docs/implementation/m2/package-parser-inventory-v26-subject.json` **631** bytes, **3** members, paths sorted unique, **0** pin mismatches.

| Member | Bytes | SHA-256 |
| --- | ---: | --- |
| `package-parser-inventory-v26/README.md` | 928 | `0d94688813099a9d4e00de8fd85b01b74ac2c848f8d608d24d1296549942e8c5` |
| `package-parser-inventory-v26/successor.json` | 702 | `bd6bdd086ccd332b610dec008c9d81f8898a866ba8062186823ce68fe1aff4ce` |
| `repository-file-inventory.v26.json` | 147952 | `1a861b0cd3bc6dcbb952e2b136299bd7e3a4492f2eb488039e90e89ac740a324` |

## Checker (`inventory_successor` 85–143)

Successor record declares **both** required true flags: `parentArtifactBytesUnchanged`, `inheritedRowsEqualByValue`. Parent pin is the live inventory **candidate** v25, not the v25 successor **record**. Candidate pin matches disk. `same_reference` on this assessment uses candidate path+bytes+sha256, parent path+bytes+sha256, and successor-record path+sha256.

Parent vs candidate: same keys except `standing` and `files`; `packages` (20) and `pendingDecisions` (9) identical. Sorted unique additions; inherited rows equal by value (0 mutated, 0 removed).

## Parent is live inventory **candidate** 25

Live lock independently **23 inventory / 34 contract** (`69967` / `1dcc5db9325f1e4f12db2ee55a4863c8a128f1beb40ac562fa95758a17912951`). Last inventory **candidate**:

`docs/implementation/m2/repository-file-inventory.v25.json` **146522** / `414a83c71206aff15eaf9001d4d16f192b2abac3931565a41a8a95a9c629ae3e`

That is `successor.parent`. Last contracts: runtime **v17** (`d41ff9c87ae12162b92b22f04f16c4889d3639941cd67ef8c1250d826bbb4853` / 11769) then enumeration-totality **v1** (`342afdbd53bb6cfafee63596cf8459a4f5c74e792edde4932c07a40acdff0b69` / 2610). Live tree has **no** `toml.rs`, `package-fixtures.json`, or `test_identity_dependencies.py`. Identity `Cargo.toml` still pins only `sha2-const-stable=0.1.0` and `unicode-normalization=0.1.24` `default-features=false`. Evaluator still depends on contracts+identity; identity depends only on contracts (no reverse edge).

## Candidate assessment: **ACCEPT**

| Claim | Check |
| --- | --- |
| 393 inherited rows | v25 393 unique sorted paths; all present in v26; **0 mutated** |
| 3 new files | `toml.rs`, host `package-fixtures.json`, `test_identity_dependencies.py`; none removed |
| 396 total | 393+3 |
| 20 packages / DAG | `packages` and `pendingDecisions` identical; no new package/edge |
| v25 path order | subsequence of v26 (insertions at host fixtures **119**, identity `src/` **136**, tools tests **348**) |
| packaging flags | both required true flags present |
| row shape | `{path, package, role, description, generated, standing}` |

New rows (`generated: false`, `standing: proposed`):

- `opensip-identity` `crates/identity/src/toml.rs` **source** (snake_case). Parse complete retained TOML bytes into an inert borrowed table view; syntax vs local resource errors distinct; numeric literals preserved; no package or Run admission authority. Sole inventory `role: source`; identity still owns parse. Layout README expressly does **not** accept the external TOML graph or parser profile.
- `opensip-host` `crates/host/tests/fixtures/package-fixtures.json` **fixture** (kebab, sibling of `enumeration-fixtures.json`). Package-manifest projection cases; fixture success does not establish full enumeration or replay.
- `tooling` `tools/tests/test_identity_dependencies.py` **test** (sibling of `test_dependency_policy.py` / `test_package_edges.py`). Exact identity source/dependency census with real Cargo controls; no sandbox or memory-safety proof.

Ownership split named in README matches the three rows: identity parses retained bytes, evaluator classifies packages, host supplies bytes. Internal dependency directions unchanged.

## Inherited description overrides

Live `inventoryPassageInheritance` has **4** entries, all parented at **v25**. v26 copies **before-text** on those rows. `successor_chain` (312–346) projects by **stable filepath** after additive inserts.

| v25 pointer | Stable path | v26 index |
| --- | --- | ---: |
| `/files/7/description` | `apps/cli/src/bootstrap.rs` | **7** |
| `/files/13/description` | `apps/report/package.json` | **13** |
| `/files/200/description` | `package.json` | **202** |
| `/files/267/description` | `schemas/sources/imported-v1.schema.json` | **269** |

No override dropped. Private activation must rewrite the lock inheritance parent to this candidate and project **all four** pointers by filepath (7, 13, 202, 269).

## requiredFindings

None.

## Scope / limits

No product files created in this layout unit. Does not accept safety38, SOURCE38, the five-crate TOML pin, winnow unsafe accounting, or a tomllib profile. Does not install a live identity dependency. Complete enumeration, reconstruction, replay, and custody remain open. Root assent and private activation of **this** record remain pending.
