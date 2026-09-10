# Blind11 diagnosis — consumer ACCEPT refused

**Standing.** Actual Grok coauthor diagnosis. Not independent design ACCEPT, not NEW blind, not application. Frozen24, live consumer-b.v11, and consumer-b.v11 working files were read only. Blind11 was not contacted or resumed. Private CLI reasoning was not read.

**Verdict: `CONSUMER_CLAIM_REFUSED`.** `ACCEPT-RECONSTRUCTABLE` is false. All five claimed complete Run exports fail frozen `identity-model.v3.open_run_closure` before `close_run` / semantic replay. The root parser is correct. The first refusal is a consumer/helper custody mistake against published law, not a missing product recipe and not an importer error.

## Measured first failure

Root report and this session’s re-run of `check-blind11-exported-graphs.v1.py` on exact copies of the five exports agree:

| Export | Claimed RunId | Owner | Semantic | Reason |
|---|---|---|---|---|
| ts, rust, rust-partial, syntax-code, syntax-data | five distinct `run3:…` | REFUSE | NOT-REACHED | `EVIDENCE_UNAVAILABLE:a87331bca7545468a266d74776d785a9903f93563220ac7f6267b6d749b82257` |

That digest is the raw SHA-256 of kit `native/native-evidence.schemas.v2.json` (230178 bytes). Every export **names** it as Coverage `payloadSchemaDigest` (and ts also via `view.schemaDigests`) and **omits** the bytes from `blobs`. Relation schema `53380a…`, identity-schemas.v3 `b187a21c…`, and (ts) imported-evidence `edce21a3…` are likewise named and omitted. Live retained `reviews/consumer-b.v11/output/exports/ts.store.json` matches the tmp export (`0b3102a2…`).

Parser selfcheck on the author reference fixture **passes** (`positive.json` **contains** `a87331bc…` in blobs). Table-mismatch still refuses `Object table disagrees with retained frame`. The importer is not inventing the first failure.

## Normative selectors (custody law is present)

- `identity-and-evidence.md` §3: `raw-artifact` = exact retained artifact bytes under this digest; default retention `preimage` = store fetch + rehash. `payloadSchemaDigest` is the raw SHA-256 of the exact full schema document the payload-registry row names.
- `identity-schemas.v3.json#/x-opensip-payload-registry` class `coverage` row `"3"`: document `native/native-evidence.schemas.v2.json`, selector `#/$defs/CoverageResultV3`.
- `identity-schemas.v3.json#/$defs/coverage/properties/payloadSchemaDigest`: `x-opensip-digest.representation = raw-artifact`.
- `identity-schemas.v3.json#/$defs/view/properties/schemaDigests/items`: `raw-artifact` + `artifactClass: registered-schema-document`.
- `identity-model.v3.py` `blob()` → `EvidenceUnavailable(digest)` when the promised bytes are absent; `registered_payload` also `blob(schema_digest)`.
- Charter already bound: `R-RETAINED-ARTIFACTS-IN-CLOSURE`, `R-OBJECT-TABLE-FRAMES`, `R-VALIDATE-OWNING-SCHEMA`, `R-ROOT-ADMISSION-EXPORT` (“must not ACCEPT on helper self-consistency”), `stopCondition.acceptForbiddenIf` helper self-consistency.

This is **not** a missing or contradictory product law. Consumer `helpers/graph.py` writes `payloadSchemaDigest: NATIVE_SCHEMA_SHA` from kit file hash; `helpers/store.py` never `put_blob`s those kit document bytes. Helper `close_run` never calls `blob()` / `EvidenceUnavailable`.

## Diagnostic copies (never acceptance; no remint)

Adding **only** the omitted `native-evidence.schemas.v2.json` bytes, then adding all four cited missing kit documents, does **not** mint a new Run. Owner still REFUSE on all five. Next first refusal (same on all five):

`x-opensip-order: canonical-set` on `semantic-configuration.analysis.capabilities` instance `['inventory', 'syntax', 'clones-fact']`.

Canonical order is `clones-fact`, `inventory`, `syntax`. C does not sort. Selectors:

- `identity-and-evidence.md` §3 / `foundation/canonical.py` `x-opensip-order` vocabulary (`canonical-set` = strict ascending canonical item bytes + unique).
- `identity-schemas.v3.json#/$defs/semantic-configuration/properties/analysis/properties/capabilities`.
- Charter `R-VALIDATE-OWNING-SCHEMA` (stock JSON Schema `uniqueItems` does not implement `x-opensip-order`).

We did **not** reorder that array (that would be producer repair / remint). Later M3 refusals therefore remain unreached. Semantic replay, tamper, and proof-bundle comparison through frozen `close_run` were **not** reached on any original export.

## Replay / helper / selected examples (not yet owner-admitted)

These are independent consumer defects visible in helpers; they did not cause the first M3 refusal, and they must not be treated as “coverage already done”:

1. **`recompute.py`** loads `helpers.closure.close_run` (join subset, `ok: not faults`) and compares `replay.claimedVerdict` to `replay.recomputedVerdict` written by the same helper. That is not `identity-model.v3.close_run` and not byte/identity comparison of a recomputed proof bundle (`R-REPLAY-COMPARE-BUNDLE`, `R-REPLAY-NO-CALLER-TRUTH`, `R-FROM-SCRATCH-COMMAND`).
2. **`helpers/evaluator.py` `eval_atom`** matches **file** (exact rung only) and **clones** (anchor path). Other claimed relations are not matched. Missing Coverage with no match is partially three-valued, but this is not the published native atom/rung/universe walk. Do not read “file+clones helper” as selected complete example coverage for TS/Rust/syntax Runs.
3. Replay **mints** `evaluation-subject` with `store.put_h` when missing — caller-authored identity during supposed replay.
4. Tamper vector (`vectors/replay-tamper.json`) asserts helper `replayRefuses` while preserving listed ids; it never ran against frozen `close_run`.
5. `R-ROOT-ADMISSION-EXPORT` is marked `executed` with artifact `exports/ts.store.json`. The **requirement text** demands independent root admission of exact bytes; the **observable** only asks for a listed export path. Consumer satisfied the weak observable and violated the text and `stopCondition`.

## Classification

| Failure | Class | Not |
|---|---|---|
| Coverage/view schema digests named, bytes absent (`a87331bc…` first) | **Consumer/helper mistake** against published custody/registry law | Missing product law; root importer error |
| Unsorted `analysis.capabilities` (diagnostic, after schema bytes restored) | **Consumer/helper mistake** against `x-opensip-order` / C-does-not-sort | Design gap |
| Helper `close_run` + saved-verdict compare offered as replay | **Consumer/helper mistake** against charter stopCondition and R-REPLAY-* | Root importer |
| Native match only file/clones; remint subjects in replay | **Consumer/helper incomplete reconstruction** of selected examples | Proof those Runs would admit |
| Charter observable for R-ROOT-ADMISSION-EXPORT is path listing | **Charter sequencing/procedure underspecified** relative to its own requirement text | Product-law hole; do not weaken reconstruction |

No valid Run remint. No author-oracle repair of consumer11 bytes. Independent24 / frozen24 grades are not reopened.

## Why repeated fresh consumers ACCEPT

The product admission procedure (`open_run_closure` then `close_run` on retained object table + blobs) is already in the kit. The charter **names** it (`stopCondition`, R-ROOT-ADMISSION-EXPORT text, R-VALIDATE-OWNING-SCHEMA) but the **listed observable** for root admission is “export path present.” Consumers implement a parallel helper graph, mark 123 IDs executed, and ACCEPT. That is false relative to the kit’s own owner. Fix the **procedure used at ACCEPT**, not the reconstruction bar.

## Completion strategy (next fresh origin, current kit only)

Do not expand original requirement kinds into extra Runs. Do not hand the consumer expected graphs.

1. Before hashing Coverage/view/fact records, `put_blob` the **exact kit file bytes** for every `payloadSchemaDigest` and every `view.schemaDigests` member (native-evidence.schemas.v2, relation-payload-schemas.v2, identity-schemas.v3, and any other named registry document).
2. Build every `x-opensip-order` array with `foundation/canonical.py` (or equivalent kit keyword implementation). C must see already-ordered unique items. Stock jsonschema is not admission.
3. Export object table + all blobs. Then, as an accept-blocking gate **inside that same fresh session**, run frozen `identity-model.v3.open_run_closure` and `close_run` on the **exact export bytes** (the root parser is the model). Helper `close_run` is not that gate.
4. Only after owner ADMIT + semantic ADMIT: independently replay from retained program/views/facts/Coverage/scopes; compare recomputed proof-bundle identities/bytes to the retained claim; tamper by changing logical result with identities preserved. No `put_h` of missing subjects during replay.
5. Native matching must follow the published atom law for **each relation actually claimed complete**. File+clones-only helper support does not cover a TS/Rust/syntax complete Run if other relations are claimed.
6. If M3 refuses: record first refusal, `CHANGES_REQUIRED` or incomplete — never ACCEPT. Preserve the failing export.

Charter for a **later** kit may tighten R-ROOT-ADMISSION-EXPORT’s observable to “frozen close_run ADMIT on listed exact bytes.” That is procedure, not a new reconstruction demand. It must not be used to rewrite consumer11 after the fact.

## Read scope and limits

**Read:** consumer-b.v11 prompt, requirements.json (kinds, stopCondition, phase 5/9/11 IDs), blind-review.json/md, five store exports + ts.replay + replay-tamper + design-gaps + requirement-status, helpers store/graph/closure/evaluator/kit_const/recompute; root parser, selfcheck assessment+positive fixture, final admission report/claims; frozen identity-model.v3 (blob/registered_payload/coverage/open_run_closure), identity-schemas.v3 coverage/view/registry/semantic-configuration, identity-and-evidence §3, native-evidence.schemas.v2 digest; live ts.store.json hash.

**Not read:** private `response.raw.json` / session updates; consumer-b.v11 kit was not mutated; not every one of the 80 subject files in full; not every helper branch; not full M3 replay (owner refused first); diagnostic copies were not sorted/repaired.

**Limits:** After schema-byte restoration, only the next first refusal is known (`canonical-set` on `analysis.capabilities`). Further M3/native/replay defects may exist; they are not hidden as “probably fine.” Query reconstruction was not re-executed because no Run is owner-admitted.

## Conclusion

Consumer11’s five exports are not reconstructable complete positives under the kit they were given. First failure is omitted retained Coverage schema document `native/native-evidence.schemas.v2.json` (`a87331bc…`), which `open_run_closure` lawfully refuses as `EVIDENCE_UNAVAILABLE`. The parser is proven. The product law is not missing. ACCEPT-RECONSTRUCTABLE must be refused. The efficient next-consumer path is: retain named schema bytes, obey `x-opensip-order`, gate ACCEPT on frozen `close_run` of exact exports, then replay. Do not weaken reconstruction and do not repair these bytes into a valid Run.
