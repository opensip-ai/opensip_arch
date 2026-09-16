# M1 startup refinements

The [actual Claude plan review](reviews/plan-01/review.md) identified five required
refinements. These concern the implementation approach; the accepted base remains
pinned and unchanged. This file is the current correction account, not acceptance.

| Finding | Current disposition and required evidence |
|---|---|
| RF-01 metadata carrier | Root confirms envelope3 has no typed help/version payload. Before JSON metadata delivery, define and review the typed payload, parity selectors, release/development metadata and compatibility successor. Do not smuggle data through diagnostics or claim M1 complete. Check the host self-identity/signing cycle explicitly. |
| RF-02 TS integers | Select `bigint` for every schema integer, including small integer constants/enums, in the initial TS carriers. This uniform policy avoids ambiguous number/bigint admission; ordinary browser view coordinates may remain numbers outside wire carriers. Lossless lexing precedes shape validation and output emits bare decimal tokens. Trial acceptance still requires exact boundary/negative vectors. |
| RF-03 generation | Trial complete source closure through an explicit URN ID map; unknown/remote refs refuse. Compare Typify0.8.0, json-schema-to-typescript16.0.0 and Ajv8.20.0 on the actual selected sources before selecting a combined recipe. Test all eight outputs including report shape validation. Define and measure the exact generator closure; versions/lockfiles alone are not executable closure proof. TypeScript7.0.2 is the current registry trial candidate, not yet selected provider compiler. |
| RF-04 inventory successors | Inventory v3 adds four initial developer provenance/test files while preserving all198 original file entries by value and20 packages. Actual Claude review03 and root canonical-unit.v1 acceptance cover this exact scoped successor. The product lock2 now binds it; actual Claude successor review02 and root design-binding-unit.v1 accept that bounded additive profile. Each later tool-specific addition or changed responsibility needs a scoped reviewed successor; status prose is not a replacement inventory. Original frozen bytes remain intact; product lock may select a successor only with its own actual review/assent binding. |
| RF-05 provider lock | Select path dependencies to the one shared pure-source owner as the authoritative lock source mode. Build isolation copies exact hashed provider/shared sources preserving the same relative paths, with root host workspace absent, and uses the checked-in provider lock unchanged with `--locked --offline`. There is no alternate registry/vendor source mode or lock rewriting to pass an isolation test. Manifest/lock and actual proof are not authored yet. |

TS lock policy remains a candidate until the isolated-install trial: separate
provider/report roots and per-lane pnpm locks, no root workspace or root install.
Node24.16.0/pnpm11.10.0 are installed development tools, not signed provider closures.
No TS package configuration or generated product carrier has been created.

The initial root Cargo workspace uses explicit members and excludes the Rust
provider. Pure shared package fields are explicit. The first snapshot used RustCrypto sha2 without default features. The live successor
selects sha2-const-stable0.1.0 to remove the cpufeatures/libc chain across targets;
[source inspection and boundary evidence](trials/software-hash-01/README.md) support
the exact selection accepted by actual Claude review02/03. `no_std` and a passing dependency graph
do not by themselves establish the complete purity claim.

The digest source name is `digests.rs` as already specified by the accepted file
inventory. The first frozen code-review subject retains its initial singular
spelling as evidence; the live correction was accepted in successor review03.

Actual code review01 is scoped to lexical/canonical/hash primitives and the
developer binding tool. Full schema ordering, registered descriptor admission,
provider/build/generation proofs, CLI metadata and all later milestones remain
separate required work. Qualification remains32 unperformed gates and54 planned
recovery cases.

The first [generator probes](trials/generator-probes-01/README.md) confirm that
losslessness is required when loading schema bounds too: native JSON parsing
rounds the schema's u64 maximum before Ajv compiles it. An adapter must preserve
exact schema constants/bounds as well as instance integers. Typify0.8.0 uses
`regress` for the tested lookahead, not Rust regex; its generated LazyLock/runtime
and full constraint coverage still need review. The [reference closure probe](trials/schema-closure-01/README.md)
refuses an undefined filter target in a historical-looking Atom definition. Resolve
entry-point ownership or a reviewed successor before judging RF-03 complete.

The [current unit record](canonical-unit.v1.json) owns acceptance of the first
foundation and inventoryv3. It does not close RF-01/02/03/05 or the remaining
successor-binding work under RF-04. Package-lane trial04 now passes a bounded
explicit frozen-install/build sequence and exact BigInt output after the earlier
failed settings attempts; final policy and full isolation remain pending.
