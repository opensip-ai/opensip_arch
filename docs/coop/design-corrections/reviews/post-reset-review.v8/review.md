# Fresh independent design/reference review — frozen candidate v8

**Verdict: ACCEPT**, limited to the exact frozen bytes named below.

This is a design and reference review by a fresh Claude session that authored
none of these bytes and is neither of the two current coauthors (Codex, and the
actual Claude session `5dec928a-6357-4726-9ea8-49a3079fb726`). It is **not**
product qualification, **not** application, **not** a readiness grade, and
**not** the fresh blind consumer review. Condition 5 remains **NOT MET**.

ACCEPT here means exactly one thing: after independent reconstruction and
adversarial probing, I found **no unresolved required design gap** in these
bytes. I record two new SHOULD-level gaps and a set of advisories that must be
carried into the pending application accounting, and I state plainly where my
evidence stops.

---

## 1. Subject and custody

| | |
|---|---|
| Frozen subject | `/tmp/opensip-design-corrections/candidate-subject.v8` |
| Manifest | `docs/coop/design-corrections/reviews/candidate-subject.v8.json` |
| Manifest SHA-256 | `cafcd839d44228677c74f5a4baed22d4fa7f384ada542fbbe8c4e74ef3e62d70` — **matches the required value** |
| Declared / verified files | 2024 / **2024** |
| Declared / observed bytes | 44 191 900 / **44 191 900** |
| Hash mismatches, length mismatches, missing | **0, 0, 0** |
| Undeclared files in the snapshot root | **0** |
| Declared standing | `FROZEN CORRECTED CANDIDATE FOR FRESH INDEPENDENT REVIEW; NO ACCEPTANCE` |
| `predecessorManifestSha256` | `b5cfb5d3…65f7b` (the v7 subject) |
| `reviewPending` / `applicationPending` | `true` / `true` |

Custody was verified **before and after** all work by `probes/p00_custody.py`;
the two runs are byte-identical result objects. Every one of the 2024 declared
files was individually re-hashed and re-measured, and the whole tree was walked
for undeclared files. Nothing in the frozen subject or the repository was
modified: `git status` and `HEAD` (`2580a9a8`) are unchanged and there are no
stashes. All of my output, probes and the disposable suite copy live only under
`/tmp/opensip-design-corrections/post-reset-review.v8/`.

The six reference runners were each verified against their declared source
pins in `final-reference.v8/reference-checks.json` before execution.

---

## 2. Reference suites — reproduced in a disposable copy

Run from a throwaway copy of the frozen tree, never the repository.

| Suite | Observed | `validation-summary.v1.json` | Match |
|---|---|---|---|
| foundation | 793 (231 + 445 + 24 + 28 + 65), 1096 pins | 793 (231/445/24/28/65), 1096 | ✅ |
| security | 456 cases + 10 invariant sweeps | 456 + 10 | ✅ |
| native | 150 cases, 60 matrix cells, 0 qualified | 150 / 60 / 0 | ✅ |
| workflows (pins) | 61 pins | 61 | ✅ |
| workflow surface | 1290 / 1290 | 1290 | ✅ |
| integration | 363 | 363 | ✅ |

All nine deterministic reports regenerate **byte-identically** to the frozen
copies (foundation validation/foundation/identity/array-order/quality/
configuration, security, native, integration). Zero deltas.

**Passing these suites is not semantic acceptance**, and I did not treat it as
such. Everything in §4–§6 is my own independent reconstruction.

---

## 3. Independent probes

297 assertions across 15 probe files, all written for this review, all
importing the frozen models read-only. The author check modules run their own
suites and `sys.exit()` at import, so I isolated them (`argv` neutralised,
`SystemExit` swallowed, stdout captured) and none of their output is reported
here as mine.

**284 of 297 passed.** I audited every one of the 13 that did not:

| Non-passing | Cause |
|---|---|
| `p06 RUST-11` | my harness added an unreferenced frame — superseded by `p07 XL-4`, which passes |
| `p08 EXEC-06` | substring search defeated by line wrapping; the prose **is** present (identity §2 ll. 64/68/72) |
| `p08 ENUM-01` | I searched only the `.md` files; the rule is in the normative schema + `closureKinds` registry |
| `p08 BUD-05` | **a genuine finding** — see v8-S1 |
| `p09 G9-10` | a public projection validator cannot detect an omission it has no ground truth for; correctly a host obligation (advisory) |
| `p09 G9-20`, `p10 R2-14 ×2` | my token scan matched *negations inside docstrings* ("does not … authorize it, or implement a mutation ledger") |
| `p12 CW-02/15/18` | locator misses: FW-01…15 live in `current-source-map.proposed.md`, DR-201…205 are AR-15's `ownerRows`, residuals are `DR-011-R01…R16` |
| `p14 COL-01`, `p14 FP-01`, `p15 FP-02` | probe heuristics/wrong join — each re-decided cleanly by `p15`/`p16` |

Exactly one non-passing assertion is a product finding. I say this explicitly
because a probe that refuses for the wrong reason is not evidence about the
rule under test; every negative below asserts its **exact** typed cause.

### Independently reconstructed primitives

I re-implemented `C` and `H` from the prose of identity §3 rather than calling
the model, then compared:

- 10/10 canonical-encoding vectors agree, including non-BMP key ordering by
  UTF-8 bytes, `\b\t\n\f\r` escapes, lowercase `\u00xx`, unescaped U+007F and
  U+2028, unescaped slash, and both integer bounds;
- `C` provably does **not** Unicode-normalize (composed and decomposed spellings
  produce different bytes);
- 12/12 `H(D,X)` vectors agree across six domains; the length field is
  `uint64BE(len(C(X)))`; `cache-key` and `regeneration-key` differ only by
  domain; and `H(D,X) ≠ SHA256(C(X))` for the same payload.

All 32 registered H domains mint 32 distinct identities for one payload, so no
cross-domain identity collision exists by construction.

---

## 4. Bv2 dispositions

The predecessor v7 had an independent ACCEPT; the later fresh blind consumer
Bv2 returned **CHANGES_REQUIRED**. The v7 ACCEPT is limited to v7's bytes and
does not discharge Bv2. I re-decided every Bv2 finding against the v8 bytes.

| Bv2 | Severity | My disposition | Basis |
|---|---|---|---|
| **G1** payload schema document law | MUST | **CLOSED** | The offending sentence is explicitly **withdrawn** in the contract, and `identity-schemas.v2.json#/x-opensip-payload-registry` replaces it with a closed registry: per class, the exact document whose **full bytes** are hashed, the **selector** that validates, codec `C`, and "a key with no row refuses". My four attacks each refuse with `PAYLOAD_SCHEMA_NOT_THE_REGISTERED_DOCUMENT`: a genuinely *registered* document of the wrong class, a **correct and tight** caller-invented single-record schema (the strongest form — admission is by row, never by document quality), a permissive whole bundle, and a **re-serialization of the right document**. |
| **G2** fact payload encoder | MUST | **CLOSED** | One codec. I re-derived every inherited constraint from `fact-plane.v1.json` itself rather than reading the successor's own `inheritedRequired` labels: all 12 inherited relations preserved with **identical** field sets, required/optional sets and universe rules, plus `unresolved-edge`; the labels are honest. The withdrawn CBOR profile's logical restrictions survive as enforced admission rules — `RELATION_PAYLOAD_NOT_NFC`, `RELATION_PAYLOAD_NEGATIVE_INTEGER`, `UInt64` [0, 2^64−1], no `number` type anywhere. CBOR wire bytes are not a `fact2` preimage. FactRecord1 history is untouched. |
| **G3** `resolvedNodeModulesLayout` | MUST | **CLOSED** | `ResolvedNodeModulesLayoutV1` is a closed record with a stated recipe (raw SHA-256 of `C`), strict ascending unique `installPath`, and both `installPath`/`realPath` for symlink and workspace links. The branch Bv2 said was unconstructible — `nodeModulesInReadSet = true` — is the **positive** path in a complete Run, with a retained two-entry layout that re-hashes to the carried digest. |
| **G4** relocation prose | SHOULD | **CLOSED** | The prose now reads "**Relocated to the context** (§2.4), and therefore *not* fields of the closed…"; no `Retained:` line names the three moved fields. |
| **G5** `tsconfigGraphHash` | MUST | **CLOSED** | `TypeScriptConfigGraphV1`, raw SHA-256 of `C(record)`. My 20 graph probes confirm ordered multiple-base inheritance (later-wins), that swapping two bases **moves** the universe key, that repeated edges are retained (`sequence`, no `uniqueItems`) and are not deduplicated, and that edge-not-a-node, entry-not-a-node, kind-contradicts-basename, cycles and unreachable nodes each refuse with their own typed cause. |
| **G6** capability manifest | SHOULD | **CLOSED** | The inherited 12-relation golden still admits **unchanged** and CVE1 is unchanged (I recomputed `SHA256("opensip.capability-manifest.v1"‖00‖bytes)` for both). The current manifest declares `unresolved-edge@observed` and admits through all four inherited gates. I drove each gate: ADM-TYPE (boolean `schemaVersion`, non-string `profile`/`providerId`, non-list `providers`), ADM-CLOSED (extra/missing key), ADM-DOMAIN (unregistered relation, **a rung from another relation's ladder**, unregistered platform), ADM-ORDER (duplicate and unsorted `platformIds`, duplicate `relationIds`, duplicated provider row). A refused manifest cannot enter a Plan (`CAPABILITY_MANIFEST_ADMISSION`). |
| **G7** ExecutionId | SHOULD | **CLOSED** | The successor is absolutely end-anchored (`(?![\s\S])`) in identity, workflow `common.schema.json` and the commit receipt; the C-2 selector is retained **unchanged** as provenance and would admit a trailing newline; and identity §2 now states the deliberate non-equivalence in the same terms security §S9.1 uses for `RootV1`. RequestId follows the same rule. |
| **G8** `plan.budget` | SHOULD | **RETRACTED — correctly not reinstated** | The original blind reviewer substantively retracted this against the exact frozen bytes. I re-verified the premise myself: `plan.budget` is a closed record (`additionalProperties:false`, both keys required, `unit` const, bounded `limit`) and is **byte-identical** to the resolved configuration's budget. No "schema correction" is claimed anywhere, and the false closed-budget premise is not reinstated. |
| **G9** `evidence.pinned` | SHOULD | **CLOSED** | Registered in the closed public detail registry with an owner; `PinnedPurgeDisclosure` carries the RunId, the **complete** pin inventory sorted uniquely by `pinId` (never a count), and the three consequences as a schema `const` in order. The **actual store** refuses first (`purge → 'pinned'`) with Run and pins intact; only explicit destructive authorization proceeds; the sealed manifest survives and an evidence-requiring query then refuses. Wrong subject, wrong exit code, reordered consequences, an unregistered pin kind and an empty inventory each refuse. |
| **G10** `configOrigin` | SHOULD | **CLOSED** | Derived from the **entry** node's kind, never the node set, and re-checked at binding. A jsconfig entry inheriting a shared `base.json` stays `jsconfig`; a tsconfig entry inheriting a jsconfig base stays `tsconfig`; an explicitly selected custom-named entry derives `tsconfig`; a missing entry raises rather than guessing. A universe contradicting its retained graph refuses `native.universe-context-field-mismatch:configOrigin`. |
| **G11** enumerator closure kind | advisory | **CLOSED** | `x-opensip-digest-domains.closureKinds.byField` pins the kind for **all 14** closure-bearing fields, `subject-scope.enumeratorClosure` → `provider`, restated in the schema description, enforced in the closure, and no new `enumerator` kind is invented. |
| **G12** | confirmation | Acknowledged; no action. |
| **ADV-B1** duplicated budget join | advisory (new, from the clarification) | **PARTLY CLOSED → see v8-S1** | The equality **is** now enforced (`PLAN_BUDGET_CONFIG_JOIN`; my divergent-budget Plan refuses). But it is enforced **only in the reference model**; no sentence in any of the five contracts states it. |

I read the original Bv2 report, its own vectors, and the clarification. The
retraction is sound and the immutable originals are untouched.

---

## 5. NEW-MUST-1 — the identity-bearing digest defect class

I attacked the class rather than the five named instances.

**Every named digest has an explicit, constructible recipe, and I rebuilt each
one independently** (my own `C`, not the model's) and required the Run to carry
exactly my value:

| Field | Recipe | Independently reproduced |
|---|---|---|
| `programPredicateDigest` | raw SHA-256 of `C(program-predicate)` | ✅ `3194a5a5…` |
| `program-predicate.nodeDigest` | raw SHA-256 of `C(addressed node)`, retention `fragment` | ✅ `db380c37…` (I addressed the node myself from the admitted program) |
| `parameterDigest` | raw SHA-256 of `C({schemaVersion,messageCode,parameters})` | ✅ `54335e9b…`, `messageCode` equals the finding's |
| `stageSpecDigest` | raw SHA-256 of `C(stage-spec)` | ✅ `8a8dc7b6…`, `planId` joins the Plan, producer is Plan-selected |
| `outputSchemaDigest` | raw SHA-256 of the exact complete registered document bytes | ✅ preimage retained and re-hashes to itself |
| `inventoryDigest` | raw SHA-256 of `C({schemaVersion,runId,objects,blobDigests})` | ✅ `b332e773…` (18 objects, 57 blobs) |

`stageSpecDigest` is demonstrably **the same record** in the execution plan and
the cache key; `cache-key` and `regeneration-key` share one schema and differ
only by H domain.

**Complete Runs for BOTH languages**, each through actual native compiler/stdlib
closure admission, each with its **own** semantic universe, facts, Coverage and
non-empty `nativeContextDigests`:

- TypeScript `run2:20dceb04…`, universe `15ce9e11…`
- Rust `run2:ed1989fd…`, universe `adefdff5…`

The two universes differ, and each Run's `subject-scope`/`fact` universe is its
**own** language's — so the Rust path is a real Rust path, not a Rust context
carried inside a TypeScript Run. A Rust universe re-pointed at the TypeScript
context refuses at complete-Run closure with
`NATIVE_UNIVERSE_CONTEXT_LANGUAGE:native.context.typescript.v2`, and the mirror
direction refuses too.

**Native producer admission genuinely re-runs at Run closure over retained
bytes — builder-only admission would not catch these.** I re-minted whole Runs
around Coverage records that are internally consistent and hash correctly, and
each is refused by `COVERAGE_PRODUCER_ADMISSION` with a distinct cause:
subject-count contradicting the host-owned scope, a forged key commitment, a
forged examined-universe commitment, complete-with-unresolved-edges,
complete-without-exhaustive-examination, and key relation/rung/universe
disagreeing with the scope.

**The decode may be memoized; the admission may not.** I built two-fact Runs
sharing one canonical payload blob where the second fact owes a *different*
admission. All four refuse for their own reason — unregistered schema, wrong
rung (`RELATION_RUNG_FORBIDDEN_FIELD:resolvedBinding`), wrong relation
(`PAYLOAD_RECORD:#/$defs/CallsPayloadV1`), unregistered relation — so schema,
rung and universe are re-decided on every reference even when the bytes are
cached. This is the exact bypass the root counterexample recorded.

**H identities are never silently raw payload digests.** A raw canonical payload
offered where a frame is required fails `H_FRAME_PREFIX`; a frame offered where a
canonical record is required fails UTF-8 decoding; an unregistered domain fails
`H_FRAME_DOMAIN_UNREGISTERED`. Referenced H preimage frames are distinguished
from arbitrary retained blobs: the literal prefix, the domain-set membership,
the declared length, byte-identity with `C` of its own parse and the registered
record all have to hold.

**Cache key construction vs hit admission** are genuinely two acts. Construction
is pure and deterministic and succeeds with no store access; admission needs the
Run's whole closure — `CACHE_OUTPUT_SCHEMA_JOIN`, `CACHE_STAGE_SPEC_PRODUCER_JOIN`,
`CACHE_INPUT_PAYLOAD_REF_NOT_A_ROOT:fact-payload` (a bare payload-domain
reference is refused as an authoritative root), a foreign scope, an empty store,
and `CACHE_STAGE_NOT_IN_THE_EXECUTION_PLAN` for a spec naming another Plan.
`evidence.regeneration-mismatch` is a named typed refusal.

**Sweeps.** Every bare-64-hex **field site** in `identity-schemas.v2` (57/57) and
in the native bundle (44/44) carries an `x-opensip-digest` annotation once
`items` and nullable `oneOf` branches are followed. The shared types `Hash` and
`DigestHex` correctly carry **no** annotation, which is what stops a field
inheriting a plausible rule. The native bundle declares its own
`x-opensip-digest-law` with an extended retention vocabulary and claims 68
sites; I counted exactly **68** annotations. Non-default retention modes are
closed to the named fields (`fragment` → `nodeDigest`, `derived` →
`capabilityManifestId`, `owner-retained` → `ownerFileManifestSha256`). All 32
`Ref` domain-enum members are registered, and the proof-input vocabulary
excludes the three payload domains.

**Collisions and excluded inputs.** Seven `canonical-record` recipes are shared
across sites; every one is a sameness the contract names (config, scope, policy,
waiver, stage spec, …), and substituting one for another refuses
(`FOREIGN_RECORD:#/$defs/WaiverSetV1`, closed-record violations). Every Plan
field moves PlanId (none is a dead input), and no operational identifier —
RequestId, ExecutionId, timestamps, PIDs, receipts, namespace, sequence, signer —
appears in Run identity.

**The Rust closure specifically.** `CargoConfigProjectionV2` carries two digests
that are provably not interchangeable: `projectionSha256` (raw SHA-256 of the
projected `.cargo/config.toml` **file** bytes, retained) and the 64-hex suffix of
`H("native.cargo-config-projection.v2", record)` — and neither equals the raw
SHA-256 of the canonical record. The dependency source set, its packages'
`fileManifestSha256`, every manifest member's bytes **at exactly the declared
length**, the unified features and the prepared-output set are all retained as
their own frames and joined. `dependencySourceSetId`, `unifiedFeaturesId` and
`preparedOutputSetId` are equal in both the context and the universe.

**Compatibility beyond the small interpreter.** The digests are joined against
the real workflow `PolicyDocumentV1`/`RuleProgramV1`/`Predicate` schemas,
`analysis-spec`/`stage-spec` parameter rows and the workflow payload registry
(re-derived at Run closure and refused on drift), not only the fixture
interpreter. A parameter citing an unregistered document refuses
`PAYLOAD_PARAMETER_UNREGISTERED`; a hidden rule program refuses
`RULE_PROGRAM_POLICY_JOIN`.

**Root counterexample custody.** The `payload-closure-counterexample.v8` and
`capability-admission-counterexample.v8` **final-recheck** source snapshots are
byte-identical to the final frozen bytes for all 19 and all 7 files
respectively; the in-progress originals are stale, as expected for captures of
the defect. I did not infer closure from those assertions — I reconstructed both
attack classes myself against the final source, above.

**Disposition: the NEW-MUST-1 class is closed in these bytes.**

---

## 6. NEW-SHOULD-1 — array order

Complete, and correct on the subtle points.

My own discovery walk (not the author's file list) found 21 JSON-Schema
documents with 272 arrays; **every array declares its order and every
annotation is in the closed vocabulary**. My sweep additionally covers
`native/capability-manifest-domains.v2.json`, which the author's checker does
not list, with no gaps; the author's list covers
`security/security-lifecycle.schemas.v1.json` (60 arrays, 0 missing), which my
`$schema` filter skipped. Combined coverage is complete, and both foundation
`import-source-context` and `product-quality-report` schemas are included.

Verified independently:

- all ten vocabulary terms are named in the contract and **each actually bites**
  on a wrong order; annotations outside the vocabulary refuse rather than pass
  silently (I tried `descending`, `sorted`, `{by:"name"}`, `{by:[]}`,
  `{by:["a","a"]}`, `{by:["a"],descending:true}`, `7`, `null`);
- everything except `sequence` and `canonical-order` requires **unique sort
  keys**; `uniqueItems` alone neither selects nor overrides an order;
- **raw UTF-8 order really differs from canonical escaped-string order**:
  `["\n","!"]` is ascending `utf8` and is refused by `canonical-set`, while
  `["!","\n"]` is the reverse, because `C("\n")` is `"\n"` escaped;
- **tuple field order really differs from canonical object order**: two records
  are ascending by `{by:["name"]}` and descending by canonical bytes, and each
  order refuses under the other annotation;
- `canonical-order` admits measured duplicates and still refuses descending;
  `canonical-set` refuses duplicates — the distinction that lets a G13 FAIL
  report stay truthful;
- **the encoder does not normalize**: `C` preserves `[3,1,2]`, preserves
  duplicates, sorts only object keys, does not NFC-normalize, and validation
  does not mutate the value. Annotations are admission rules, never encoder
  behaviour;
- input configuration layers are **all** `sequence` while the resolved semantic
  record normalizes explicitly, and `allowedScopes` keeps its declared priority
  order;
- token/argv/substitution arrays are ordered sequences that retain repeats and
  position;
- native order violations are reported as **order** faults
  (`native.native-context-field-mismatch:lib-selection-order`,
  `capability.adm-order:platformIds`), not as wrong-language faults.

All earlier blind M1–5 / S1–6 / A1–4 fixes remain intact (the suites that
encode them reproduce exactly and byte-identically).

---

## 7. NEW-SHOULD-2 — the crosswalk

The proposed crosswalk separates the three standings correctly.

All **16 AR** rows are present with no duplicates, and every row carries:
immutable `historicalReviews`; exactly one `latestCompletedReview` pinned to the
v7 review file (`bcf97f11…`, re-hashed and matching) whose
`subjectManifestSha256` is the v8 manifest's own `predecessorManifestSha256`
(`b5cfb5d3…`), with standing text that explicitly refuses to extend to successor
bytes; the later blind Bv2 `CHANGES_REQUIRED` and its clarification, both
re-hashed and matching (`334f8d48…`, `81495d07…`); and a
`currentReviewBinding` whose standing is `PENDING-INDEPENDENT-REVIEW`.

**No self-hash cycle is demanded**: the binding carries no digest of a future
review and states the rule in terms — "A review cannot be hash-embedded in its
own frozen subject." The applied wrapper is correctly described as pinning the
accepted successor review and the exact source row *after* acceptance, and no
applied crosswalk or application record is committed yet. No stale review is
presented as current. **15 FW** rows are enumerated in
`current-source-map.proposed.md`; **DR-201…205** appear as AR-15's `ownerRows`
alongside DR-001/006/009/011; the 16 inherited residual rows are `DR-011-R01…R16`
with 30 nested evaluation-residual items (19 RES + 7 NB + 4 measured escapes).

**NEW-ADV-1 / ADV2 / ADV3.** Pending-versus-accepted standing is unambiguous on
every row. Stage-spec identity is explicit (§5). All **32** qualification gates
carry `qualified: false`, `demonstrated: false`,
`standing: DESIGN-CONTRACT-PENDING-REVIEW` — **no gate is claimed qualified or
demonstrated**, and `readinessChanged` is `false`. Historical v5 non-blocking
advisory evidence and limits are carried forward as evidence and limits, not as
new qualification (§9).

---

## 8. New issues

### `newMustIssues`: none.

### `newShouldIssues`

**v8-S1 — the Plan/configuration budget equality is enforced only in reference
code, and is stated in none of the five contracts.**

*Selectors:* `foundation/identity-model.py` l. 525 (`PLAN_BUDGET_CONFIG_JOIN`);
`identity-schemas.v2.json#/$defs/plan/properties/budget` and
`#/$defs/semantic-configuration/properties/analysis/properties/budget`;
`identity-and-evidence.md` §3 closure list (l. 626, "Snapshot config/scope, Plan
config/scope and native-context source correspondence must agree").

The reference now refuses a Plan whose inline `budget` contradicts its own
committed resolved configuration — I confirmed this (`PLAN_BUDGET_CONFIG_JOIN`),
and it is the right rule. But I grepped all five contracts: the word "budget"
appears only in the domain table, in the configuration-resolution prose and in
unrelated native/security/workflow senses. **No sentence anywhere states that
the two must be equal.** Contract text is the design deliverable and the
reference is explicitly "design evidence, not production code", so an
implementer building from the contracts would not implement this join, would
mint Plans the reference refuses, and two conforming implementations would
disagree on admission. This is the same defect class as Bv2's own findings, and
it is now *asymmetric*: ADV-B1's remedy ("one sentence in identity §3's closure
list") was applied to the code and not to the prose.

SHOULD, not MUST: both values enter PlanId, so identity, replay and determinism
are unaffected — which is exactly why the blind reviewer graded ADV-B1
advisory. *Remedy:* add "and Plan budget" to identity §3's closure list.

**v8-S2 — a `file` relation payload's own content claim is joined to nothing,
while the analogous joins exist everywhere else.**

*Selectors:* `relation-payload-schemas.v2.json#/$defs/FilePayloadV1`
(`path`, `contentSha256`, `byteLength`) and `#/$defs/ClonesPayloadV1/
properties/normalisationVersion`; `identity-model.py`
`relation_payload_rules`; `x-opensip-relation-registry`;
`identity-and-evidence.md` §3 ("every source anchor must name an inventoried
blob") and the closing digest law's scope.

Three facts, each verified: (a) the closing digest law is scoped to
`identity-schemas.v2`, the native bundle extends it to itself via its own
`x-opensip-digest-law`, and `relation-payload-schemas.v2.json` is covered by
**neither** — its two digest-bearing fields carry no representation or retention
annotation; (b) the relation registry declares **no** `snapshotJoins`, unlike
the native context/universe registry rows, which do; (c)
`relation_payload_rules` performs no inventory or snapshot lookup at all, while
fact **anchors** are fully joined (`ANCHOR_SOURCE`, range and UTF-8 boundary
checks). A `file` fact may therefore be admitted claiming a `contentSha256`,
`byteLength` or `path` that contradicts the very snapshot inventory the Run is
bound to, even though the host holds the ground truth.

SHOULD, not MUST: identity, replay and determinism are unaffected (the claim
enters `payloadDigest` and hence `fact2`), the fields are exact reproductions of
the inherited fact-plane payload — which G2 required — and the native provider
admission boundary, not the identity closure, is the declared owner of relation
payload content. *I state the counter-argument plainly:* if a later reviewer
holds that `file` facts are authority-bearing about repository content, this
becomes a MUST, because a rule reasoning over `file` facts would be reasoning
over an unverified provider claim. *Remedy:* one `snapshotJoins` row on the
`file` relation registry entry, mirroring the native rows.

*Limitation on my evidence:* I established v8-S2 at the payload-admission layer
and by source and registry reading. I could **not** drive a complete
`file`-relation Run to a seal, because the fixture Coverage for `file@enumerated`
is refused first as a not-applicable rung carrying a completeness claim
(`RC-1`). A future reviewer with a `file`-shaped Coverage fixture should confirm
the behaviour end to end.

### `newAdvisories`

- **v8-A1** The `evidence.pinned` projection validator cannot detect a
  *truncated* pin inventory — it has no independent ground truth, so a
  one-pin disclosure is schema-valid and internally consistent. The contract's
  "no pin is omitted, truncated or aggregated" is therefore a host obligation
  with no mechanical check. Correctly placed (the host is TCB), but worth
  naming.
- **v8-A2** (Bv2 narrative A2) The Rust component inventory asymmetry is real
  and observable: TypeScript's `standardLibraryComponentDigests` is `minItems:1`
  ordered `{by:["component"]}` with a stated completeness gate, while Rust's is
  `minItems:0`, `sequence`. **It is a representation asymmetry, not
  qualification and not permission to omit closure**: I confirmed that
  unretaining the `rust-dev-llvm` closure, or emptying its retained tree, still
  refuses a complete Rust Run. Carry as advisory until real Rust qualification.
- **v8-A3** (Bv2 narrative A3) The duplicated discovery prose is explanatory.
  Two contracts cite the shared `discovery-defaults.py`; I found no second
  algorithm and no conflicting rule. Advisory only.
- **Carried from v5, still present:** ADV-1 (D-372 l. 80 still attributes the
  declared parity fields to Workflow §9, which §8 owns); ADV-3
  (`check-integration.py` is still covered by none of the four source-pin sets);
  ADV-5 (workflows §8 still does not state that the host projection must be
  *total* over `parityFields`, nor the fault class for a violation).
  **ADV-2 is CLOSED** — `NEXT-REVIEW.md` is now current and correct for v8.
- **Carried from v7, still present:** V7-ADV-1 (the "every 64-hex field"
  sentence is broader than what is enforced — I counted exactly the same **52**
  prefixed identity fields that carry no annotation because their domain is in
  the prefix); V7-ADV-2 (a Plan may select several admitted contexts of one
  language; both my Runs carry two contexts and no contract text requires
  per-language uniqueness); V7-ADV-3 (application must bind the **frozen**
  snapshot bytes, not the working tree).

---

## 9. Limitations — what this review does not establish

1. **Not product qualification.** No OS, compiler, cargo, linker, crypto,
   SQLite, filesystem, clock, lease or end-to-end measurement was performed, and
   none is claimed. Every OS, compiler, crypto, clock, lease and evaluator
   observation in these models is a **synthetic TCB assumption**, never product
   qualification. All 32 gates remain `demonstrated: false`, `qualified: false`.
2. **Not the blind consumer review.** I read the contracts, the schemas, the
   models, the prior reviews and the coauthor assertions. Reconstructability
   from normative bytes alone is a different act; the fresh blind Bv3 is a later
   independent session and is still required.
3. **Not application or readiness.** The application/readiness binding remains
   deliberately unapplied. This document is a review record for later
   application, not an award of readiness. Condition 5 remains NOT MET.
4. **Not implementation authority.** No implementation, source fix, commit,
   push, checkout, reset or clean was performed or is authorized.
5. **The reference evaluator is a small interpreter.** It carries a *real*
   `PolicyDocumentV1`/`RuleProgramV1` in the product DSL, but evaluates a
   single-atom subset. It qualifies neither the declarative language nor a
   native Coverage or relation payload registry.
6. **`admit_cache_entry` is a post-construction conformance check** over an
   admitted Run, as the model itself discloses — not the pre-analysis cache
   scheduling API, and it does not fetch cached output bytes or decide reuse
   policy.
7. **The Rust dependency fixture is one vendored package over a two-package
   lockfile.** Real crate graphs, workspace member enumeration, feature
   unification by an actual `cargo metadata` run and missing-crate Coverage
   remain the native unit's own obligations.
8. **v8-S2's end-to-end behaviour is unconfirmed** for the reason stated in §8.
9. **Historical grades are not extended.** The v7 ACCEPT is limited to v7's
   bytes; the historical 2026-08-13 grades are untouched; Bv2's findings were
   required work and were not discharged by v7.
10. **Coauthor material was treated as assertion, not evidence.** Codex's
    `technical-review.v8.md`, `post-reset-dispositions.v8.proposed.json`, the
    `tsconfig-representation-note.v8.md` and the retained
    `digest-corrections-author.v3` handoff were read as claims to verify. Every
    closure above rests on my own probes. The final native prose/sequence-
    uniqueness/custom-entry corrections are Codex's post-handoff root deltas and
    are **not** attributed to the Claude coauthor; I reviewed them on their
    merits (probes TSG-03/04/05, TSG-09/10) and they hold.

---

## 10. Conclusion

Custody is exact before and after. All six suites reproduce with the declared
counts and byte-identical reports. The four Bv2 MUSTs are closed against
independent reconstruction, not against author vectors. The NEW-MUST-1 digest
defect class is closed: every identity-bearing digest has a constructible
recipe I rebuilt myself, complete TypeScript **and** Rust Runs admit through
real native admission with their own universes and non-empty native contexts,
and altered context, closure, source, config, schema, relation, rung, universe
and payload each refuse with an exact typed cause. NEW-SHOULD-1 and NEW-SHOULD-2
are complete and correct on their subtle points.

Two SHOULD-level gaps remain — one rule that lives in reference code but not in
the design, and one payload content claim joined to nothing — plus the carried
advisories. Neither is an unresolved *required* design gap, so the verdict is
**ACCEPT**, strictly limited to manifest
`cafcd839d44228677c74f5a4baed22d4fa7f384ada542fbbe8c4e74ef3e62d70`.

A fresh blind consumer review and a complete, independently reviewed
application remain required, and are later independent sessions that I have not
performed.
