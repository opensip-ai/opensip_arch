# Advisory: identity-candidate trial 01

Not a design-unit acceptance. Not runtime selection. Not M2 completion. Frozen/live/history unchanged.

Subject `docs/implementation/m2/trials/identity-candidate-01/subject.json` SHA-256 `43b169a35e28bb1a3b3b2787587d82de62887f2ce2f2d336db83e0c10c7e85e8` (3668 bytes, **23/23** files). Archive `dacbb7a34ad84634d3b4e61d9766f57def71c1be0f060a834714f52b02d6acf3` (54832 bytes). Dependency pins for schema-engine-02 subject/archive and exact-schema-profile subject/unit all match.

Private reconstruction under this review dir: copied the trial and **pinned se02** (101 files), rewrote only private `Cargo.toml` paths to those copies. No live `/tmp/.../m2-schema-engine-trial-02` substitution at build time.

## What it is

`IdentityCandidate` is a private struct (`domain`, `shape`, `identifier`). `from_json` admits **selected identity-v3 `$defs/{domain}` shape** via frozen se02 `RegisteredSchemas` (40 documents), then runs an imperative `ordered()` over the admitted value, then `H(domain_name, descriptor)` and prints `{prefix}:{hex}`. Getters expose the readonly descriptor and the **raw schema document sha256**. No Deserialize/Default. Arbitrary domains refuse (`fact2`, `Fact`, `native.context.rust.v2`).

19 closed domains match selected `PREFIX` in `identity_model.proposed.v3.py` (`5ba92896…`). H uses the **name** (`fact`), the printed prefix is **`fact2`**. Independently: `identifier == PREFIX[domain] + ':' + exact_profile_canonical.identity(domain, value)` for the four shape-only extras. That is the selected model’s `identifier()`, not a second hash law.

Oracle: AST extract of `PREFIX` / `ordered` / `identifier` from that model, `SCHEMA` = current identity-v3 (`311c1feb…`), `C` = **accepted** exact-schema-profile `canonical.py` (`ad88e58f…`, the unit this reviewer already accepted). No fabricated Claude agreement.

## Order, path, prefix

Imperative `ordered()` matches the model, not `LogicalPath::parse`:

| Law | Model `ordered()` / this candidate | `LogicalPath` (schema $defs) |
|---|---|---|
| empty / `.` / `..` / `\` / NUL / leading `/` | refuse | refuse |
| per-segment 255 scalars | **not enforced** | enforced on Blob/import-blob `$ref` only |
| final-LF `.` / `..` | **not enforced** | enforced in Rust LogicalPath |
| `a/.\n`, `"x"*256` | **admitted** by helper (focused test says so) | LogicalPath refuses 256 |

identity-v3 **already documents** three non-equivalent path enforcements. Candidate implements the model’s recursive `path`/`logicalPath` check (scopes 2–3), not Blob grammar (1). That is not a silent widening of selected identity-v3.

Order exceptions also match the model: `allowedScopes` = sequence (repeats/order of values not sorted); `sourceInventory`/`tree`/`blobs` = path; `requires` = numeric; `owner-source-set` = by `ownerKey`; `stages` = ordinal 0..n-1 plus backward `requires`; `predicateProofs` / `ruleResults`; **default canonical-set** (unique). `[2,1,1]` ok on `allowedScopes`; `[1,true]` fails `requires`; unnamed `[2,1]` fails canonical-set.

Prefix vs H-domain is separated: `finding` → prefix `finding3`; `fact2` as domain refuses.

## What it is not

The four extras (`import`, `cache-key`, `policy-derivation`, `regeneration-key`) use `0*64` absent closures. They **do** mint candidate IDs (shape+order+H). Labels are `shape-only-absent-references:*`. That is **not** retained-closure or ReplayedRun proof. 2081 finite synthetic/nested/mutation cases are not complete payload/replay law.

Registry is frozen **40** from se02, not root’s separate 48-source registry-03 work.

## Reproduction

Private cargo test (4), clippy `-D warnings`, build: pass. Probe over frozen `requests.ndjson` with private se02 `selected-sources`: **2081 lines byte-identical** to frozen `actual.txt` (133 identifiers, 1948 `E:`). Shape-only Python IDs appear in that output.

## shouldFix (for a later unit, not this trial’s standing)

1. **Budget/JSON negatives:** library takes `budget`; binary always `64MiB`. No focused test for `Limit`, invalid JSON, or unselected `$defs`.
2. **Error collapse:** `From<AdmissionError>` maps `Mismatch` / `Schema` / `SourceSet` / `SourceBytes` all to `Error::Schema(_)`. `E:{e:?}` is explicitly not a public contract; still hides mismatch vs schema-fault vs limit. Schema faults must stay non-invertible (`not`/`anyOf`) — that is se02’s job; candidate should not flatten it if later callers need the distinction.

## requiredFindings

None that contradict “shape + ordered + candidate ID, not closure.” Path/LogicalPath split is selected schema text, not a candidate regression.

## Limits

Did not regenerate the 2081-row oracle from the graph fixture (replayed frozen requests instead). Did not exercise native/compiler. Did not install into product. Advisory only.
