# Frozen trial review: import-payloads-29

**Reviewer:** Grok. Root remains lead. Not Claude agreement.
**Kind:** Scoped source review of private `inspect_import_payload`. **Not runtime selection. Not layout-23 re-acceptance. Not correspondence, Plan membership, import execution, full walk, or replay.**
**Work tree:** `/tmp/opensip-implementation/m2-grok-import-payloads-review-29/review`. Live, frozen, and history not edited. No commits.

Layout-23 is a separate proposed inventory unit. Live still has **no** `import_payloads.rs`. Eventual runtime composition must use the **current live** lock, not this trial’s inherited 9/15.

Private inherited `product/design-lock.json` is `515f092c1c74429397bf215184ffae24af93c892ca546292c05a717bd47fb523` / 36241 with **9 inventory / 15 contract** successors — **not** live 21/30.

## Subject pin

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `docs/implementation/m2/trials/import-payloads-29/subject.json` | 51895 | `9ea476e42f9fd8047d6608cea18c8e1be11710e3eff476309d1ff59a23d0219a` |
| adjacent `subject.tar.gz` / `archive-pin.json` | 10937672 | `e49408c860834ae97272adaaafb091187b6afdd4cb4856ae418ca56b9d7638ea` |
| adjacent `payloads-result.json` | 702 | `ceedfc5e80742e1e4f438854e4217f9907420a4cac724e5e4726d09daf962ada` |
| export | `/tmp/opensip-implementation/m2-import-payloads-subject-29` | **288/288** members; tar 288; 0 extra; 0 missing |

288 `files[].path` values are unique and string-sorted.

Dependency pins hash-match: import-joins-27 `279a2f93…754e`; identity `7b6750a9…0da2` / 158739; selected totality workflows `60dc11e2…b180` / 142991; totality unit `cdf1afc9…eea5`; inventory-23 subject `29f3027f…a6e4`; archived advisory `6e705a3c…521a`.

Live lock independently **21 inventory / 30 contract** (`471c57d5d647cff9e86649142312b3addb971e3d22072caf97387f519ec8abc9` / 64061). Last inventory candidate is v23; last contract is **import-totality-reference-selection-v1** (`ee921a88…f243` / 2892) — formally selected. Inherited 9/15 is not that base.

## Source delta vs frozen 27

**246** prior product files byte-identical, including identity, identity-policy, `Cargo.lock`, `import_joins.rs`, and prior fixtures. External TCB unchanged (`sha2-const-stable` 0.1.0, `tinyvec` 1.13.3, `unicode-normalization` 0.1.24).

Changed: `lib.rs` export only; additive host `native_owner_tests.rs`. **New:** `import_payloads.rs` (**5836** / `acf9691d780f64a33c037ae3fe2470ff867296a2f80b34b3f876cd4f327c1788`), `import-payload-registry.json` (**2125** / `56636785…8924`), `import-payload-fixtures.json` (**3085386** / `ecd89fcb…2a8a`) under the unchanged 4 MiB per-document cap.

Prior `native-context-fixtures.json` **3736129** and `import-joins-fixtures.json` **1980785** byte-identical to frozen 27.

## Law (two-key row, independently derived drift)

`inspect_import_payload` loads the retained import descriptor (closure roles via existing identity `CLOSURE_FIELD_KIND`), **canonical-decodes** `payloadDigest` bytes, then selects the exact `(kind, payloadDomain)` row from embedded metadata, then compares full schema digest and retained schema artifact, then `registered_record_shape` on that row’s selector.

Kind is the naming-record field; `payloadDomain` is taken from the decoded payload object only (non-object → no domain → `PAYLOAD_IMPORT_UNREGISTERED`). Five closed rows match selected 311c import class **and** selected W `PAYLOAD_REGISTRY` (table byte-identical to predecessor 1d52; only `registry_row` gained the exact-str guard). Metadata `document`/`selector` alias 311c; `ownerDocument`/`ownerSelector` alias W; disagreement is `PAYLOAD_IMPORT_REGISTRY_DRIFT` without Python `repr`. Schema path names map to selected product bytes (`imported-v1` `edce21a3…`, `test-execution-v1` `a6f7c2d8…`, `native-v2` `e5834d37…`).

Compound order independently observed on the 321-row corpus: decode/`invalid` before wrong schema; unregistered domain before wrong schema digest; `PAYLOAD_SCHEMA_NOT_THE_REGISTERED_DOCUMENT` before missing schema artifact; schema artifact before shape. Returns inert JSON. Does not prove correspondence, Plan/import membership, execution, full walk, or replay.

## Reproduction (independent, rustc 1.95.0, `--locked --offline`)

- Frozen payloads actual vs expected: **321/321**, **0 mismatch** (11 checked / 255 refused / 35 invalid / 15 unavailable / 5 limit). Independent rebuilt harness vs frozen actual and expected: **0 mismatch**. Oracle used selected I `7b6750a9` + W `60dc11e2`; two registry `repr` suffixes stripped to named codes only.
- Ten predecessor `TypeError` unhashable list/object domain cases are **separately** recorded (`original-import-phase-exceptions.json` / `host-totality-additions.json`). Current actual is `PAYLOAD_IMPORT_UNREGISTERED`, **not** an old REFUSE relabel.
- Host fixture **316** cases including those ten. `cargo test --locked --offline --workspace`: **121** passed / 0 failed. Identity policy `sourceFilesVerified: 110`. Independent `cargo clippy --locked --offline --workspace --all-targets -- -D warnings` Finished.

Did not re-exec Unicode-15 or 07–12 corpora. Did not treat live 21/30 as this source.

## requiredFindings

None.

## Limits (not required findings)

- This helper does not admit correspondence, selected Plan/import membership, or execute imported claims.
- Host `build_import` concatenation and relation-key lookup remain adjacent open work.
- Live 21/30 does not install these `import_payloads.rs` bytes. Eventual runtime must compose **exact current live**, not inherited 9/15.
- Layout-23 is not accepted here.

## Verdict

No required findings. Private `inspect_import_payload` matches selected I+W phase order on 321 pairs, fail-closes malformed domains as the existing named no-row, and returns inert JSON. Not a live/runtime selection.
