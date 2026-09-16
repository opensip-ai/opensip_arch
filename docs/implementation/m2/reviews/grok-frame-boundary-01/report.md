# Advisory: H-frame / native-domain admission boundary

Not an acceptance. Not fresh-consumer identity. Not full closure from shape. Root’s annotation walker is parallel; this does not implement it. Product/frozen/history not edited.

Live product 9/13 (`opensip` design-lock: inventory v11 + admission-runtime). Native document current alias: logical `native/native-evidence.schemas.v2.json` → `schemas/sources/native-v2.schema.json` SHA-256 `e5834d37aebd96d77d352975878da349033f8633ecbd83322ad0fbea461f7773` (280357 bytes), `$id` `urn:opensip:product-v1:native:evidence-schemas:v2`. Identity-v3 live = selected `311c1feb…`.

Prior boundary report (`grok-retained-closure-boundaries-01`): identity graph ≠ `open_run_closure`; native admission cannot live in `opensip-identity` (DAG: identity → contracts only). This note is the **next increment**: `parse_h_frame` / `admit_frame` / `domainSets`.

## Frame law (identity-separable)

`h_preimage_frame` / `parse_h_frame` (model 231–268):

```
frame = b"opensip.product.v1\0" || ASCII(D) || 0x00 || uint64BE(len(C(X))) || C(X)
digest = SHA256(frame)   // this digest is what plan.nativeContextDigests stores (bare hex)
```

`D` must match `[a-z0-9.-]+` and be a **key of** `x-opensip-digest-domains.domainSets[domainSet]`, not a 19-domain `PREFIX` name. Native H domains are e.g. `native.context.typescript.v2`, **not** `fact2:`.

Identity may, given explicit blob bytes and a `domainSet`:

1. Missing blob → unavailable; wrong SHA → `BLOB_DIGEST`
2. Bytes not starting with the frame prefix (including putting **`C(X)` here**) → `H_FRAME_PREFIX`
3. Domain NUL / non-ASCII / empty → `H_FRAME_DOMAIN`
4. `D` not in that domainSet → `H_FRAME_DOMAIN_UNREGISTERED:D`
5. Declared length ≠ payload → `H_FRAME_LENGTH`
6. `parse` fail or `C(value)≠payload` → `H_FRAME_NONCANONICAL` / lexical
7. `identity(D,value)≠SHA256(frame)` → `H_FRAME_IDENTITY` (`SHA256(C(X))` is never H)
8. **Shape only:** ExactValidator of the row’s `document`+`selector` on the **current alias bytes** (or **exact retained bytes** for a historical Run). Live current: native-v2 `#/$defs/TypeScriptNativeContextV2` | `NativeContextV2` | `SyntaxNativeContextV2` | universe `*ResolvedInputs`

`retain_h_identity` / `native_context_frame` / `native_universe_frame` only **write** the frame into the blob map after domainSet membership. They do not call `admit_native_context`.

That is still **not** an admitted native context.

## Must stay native / evaluator (admit_frame after parse)

`admit_frame` (1577–1631) **after** `parse_h_frame`:

| Step | Owner |
|---|---|
| `snapshotJoins` inventoried-paths / path+digest vs **this Run’s snapshot** | evaluator/host (needs snapshot object) |
| `blobJoins` member length (layout `contentSha256`, rust `projectionSha256`) | identity **blob()** if maps supplied; not native semantics |
| `nestedRecords` (e.g. `ResolvedNodeModulesLayoutV1`) + their blobJoins | identity canonical-record **shape** + blob; **not** resolver/read-set law |
| `nestedIdentities` (`sha256:` + recursive `admit_frame` into `native-nested`) | identity frame recursion **shape**; nested owner admission still native |
| `closureJoins` (toolchain / stdlib / rust-dev-llvm / grammar kinds on retained `closure2`) | identity role check **if** objects map present; kinds from domainSet rows |
| `native_admission().admit_native_context` (refusals, `planNativeContextDigest`, domain) | **native/components** — “a frame proves retention, never admission” |
| `bind_typescript_universe` / rust/syntax bind (section 11) | **native** |
| capability ADM-DOMAIN, syntax capability, coverage dialect | native + evaluator |
| public `open_run_closure` / ReplayedRun | not this increment |

Identity crate still must not depend on native/evaluator.

## Current vs retained

Admission registry lists native-v2 **once as a source** and **once as** `logicalDocument: native/native-evidence.schemas.v2.json` with the **same** sha256. Current alias is that implementation path. Historical Runs bind **exact retained document bytes**, not `$id`/major fallback. Do not validate a retained frame against a newer native-v2 if the Run committed another digest.

## Domain registry (identity-v3 `domainSets`)

- **native-context:** `native.context.{typescript,rust,syntax}.v2` — each names selector, `closureJoins`, `language`, `admission.entryPoint=admit_native_context`
- **native-semantic-universe:** `native.semantic-universe.{typescript,rust,syntax}.v2` — `bind_*_universe`, `contextDomain` must match the bound context domain
- **native-nested:** dependency-source-set, file-manifest, unified-features, prepared-output-set, cargo-config-projection, source-unit-ownership

Cross-language mix (TS universe + rust context domain) is a **native bind** refusal, not a frame-parse error.

## Test vectors (identity increment only)

Construct frames with exact-profile `canonical` + `identity(D,X)` (accepted exact-profile canonical). Do **not** treat pass as `admit_native_context`.

1. Happy path: minimal **schema-valid** TS context object (only required JSON Schema fields), domain `native.context.typescript.v2`, frame stored under SHA256(frame); `parse_h_frame` ok. Assert **no** native ADMIT flag.
2. Payload `C(X)` stored under SHA256(C(X)) used as nativeContextDigest → `H_FRAME_PREFIX`
3. Frame with wrong u64 length / truncated / trailing extra after payload
4. Noncanonical inner JSON (`{ }`, `1.0`, duplicate keys)
5. Domain `native.context.typescript.v1` or `fact` in `native-context` set → unregistered
6. TS descriptor parsed with rust row selector (or rust domain + TS body) → `H_FRAME_RECORD` / schema fail
7. Mutate one payload byte after framing → `H_FRAME_IDENTITY`
8. Syntax context that includes `toolClosure` (schema should fail if additionalProperties/required forbid it)
9. `sha256:` missing on rust `dependencySourceSetId` — **not** in parse_h_frame; belongs to `nestedIdentities` (later)
10. Snapshot path not inventoried — **not** identity-only; skip until snapshot map exists

## Limits

Did not execute native compiler/stdlib joins. Did not implement code. Shape-valid frame ≠ admitted context ≠ selected Plan universe ≠ ClosedRun.
