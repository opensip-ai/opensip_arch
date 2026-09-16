# Advisory: retained-input resolver trial 01

Not formal acceptance. Not runtime selection. Not M2 complete. Frozen/live/history not edited. Did not demand the full graph walker from the prior boundary advisory.

Subject `docs/implementation/m2/trials/retained-input-01/subject.json` SHA-256 `fb8de2b0de9541c905efbfa4c96cd752e10ec8ef3b72b8ed3fd6128f39f58e8f` (3184 bytes, **20/20** files). Archive `29840b4d8c009703245fa39b65ed5605b83a016f2cb0330e18847df83b9b9e89` (70098 bytes).

Runtime dependency pins match accepted `admission-runtime-selection-v1` (live **9/13** lock last contract successor). Private copy of frozen `admission-runtime-01` product (203 `product/` files) used for Cargo; **no** live subject-01 path at build time. Library depends only on that identity crate; host is test/harness only.

## What it is

`RetainedInputs` borrows immutable object and blob maps. `object(key, domain, budget)` recomputes expected-domain `IdentityCandidate` (shape/order/H) and, for the **nine** selected `closureKinds.byField` rows whose owner is in the 19-domain `PREFIX` table, looks up the named closure and checks `kind`. Regeneration uses the cache-key rows. `blob` distinguishes missing vs SHA mismatch; `require_length` and `canonical_record` (`parse` + `C(X)==bytes`) are separate.

Independently: those nine rows equal `{k:v in byField if k.split('.')[0] in PREFIX}`. Stage-spec and native toolchain/grammar rows are **not** here (later owners). No `open_run_closure`, `ClosedRun`, `ReplayedRun`, or `close_run`.

`object` returning a candidate after a valid role check **does not** claim payload blobs exist (focused test: success then `MissingBlob([0;32])`).

Budget: the same per-descriptor limit is **reused** for the object plus at most two role `from_json` calls (import producer+adapter). Not a graph work bound.

## Missing vs invalid / hash / domain / key / role

Aligned with AST-extracted model `get` / `blob` / `canonical_bytes` / `admit_closure_field_kinds` + `EvidenceUnavailable`:

| Condition | Rust | Oracle class |
|---|---|---|
| absent object/blob | `MissingObject` / `MissingBlob` | unavailable |
| SHA-256 ≠ claimed digest | `BlobDigest` | invalid |
| length | `BlobLength` | invalid |
| `C(X)` ≠ stored blob bytes | `NoncanonicalRecord` | invalid |
| lexical parse fail | `Canonical` | invalid |
| claimed domain ≠ stored | `ObjectDomain` | invalid |
| stored value’s identifier ≠ key | `ObjectIdentity` | invalid |
| closure `kind` ≠ published role | `ClosureRole` | invalid |
| missing/non-string role field | `InvalidRoleField` | invalid |

Harness stdout is only `ok` / `unavailable` / `invalid`. That **is not** a public wire/error profile.

## Object value vs blob canon

Object path: in-memory descriptor → `canonical_bytes` → candidate. It does **not** require a CAS blob of `C(descriptor)`. Blob path: stored bytes must hash to the key **and**, for `canonical_record`, equal `C(parse(bytes))`. `{ }` hashes as itself but is noncanonical. `1.0` is a canonical error. That split matches the selected model and the README.

## Lifetime / immutability

Maps are borrowed. `IdentityCandidate<'a>` is tied to the **registry**, not to a mutable `ObjectInput`. Tests mutate a descriptor only after dropping the previous `RetainedInputs`. No I/O, fallback, or cache.

## Reproduction

Private cargo test (3), clippy `-D warnings`, harness over frozen `requests.ndjson`: **2442 lines byte-identical** to `expected.txt` / `actual.txt` (`ok=151`, `unavailable=112`, `invalid=2179`).

## requiredFindings

None against the stated incomplete prototype.

## shouldFix

Reuse of the same budget across role lookups is documented; a later annotation walk must not treat it as spent graph work.

## Limits

Did not regenerate the 2442 queries from identity-candidate requests (replayed frozen ndjson). Did not implement native/H-frame/payload-registry/Plan joins. Root’s next annotation walk remains next work.
