# post-reset-review.v7 — fresh independent design/reference review

**Verdict: ACCEPT** (design/reference acceptance of the frozen v7 bytes only).

This grants no readiness grade, no product qualification and no implementation
authorization. Condition 5 remains NOT MET. The fresh blind consumer-B review
and the complete application review are later independent sessions and were not
performed here.

---

## 1. Reviewer and custody

I am actual Claude in a fresh independent session. I authored none of the subject
bytes. I am neither Codex nor actual Claude coauthor session
`5dec928a-6357-4726-9ea8-49a3079fb726`, and neither the v6 reviewer session
`96d049d9-abe2-457b-b05b-1ea5733b0f3e` nor the v5 reviewer.

I wrote only under `/tmp/opensip-design-corrections/post-reset-review.v7`,
including a disposable copy of the subject for suite execution. I made no commit,
push, checkout, reset or clean, and I modified neither the frozen subject nor the
repository.

### Subject verification

| Item | Result |
|---|---|
| Manifest `candidate-subject.v7.json` SHA-256 | `b5cf…65f7b` — **matches required** |
| Declared files | 1743 |
| Files verified by hash **and** length, before review | 1743 / 1743 |
| Files verified by hash **and** length, after review | 1743 / 1743 |
| Hash or length mismatches | 0 |
| Undeclared files on disk | 0 |
| Symlinks / empty directories | 0 / 0 |
| Sum of declared bytes vs `totalBytes` | 28 439 483 = 28 439 483 |
| Duplicate paths in manifest | 0 |
| Declared `predecessorManifestSha256` | `cb345532…` = the v6 manifest, verified by rehashing the embedded copy |

Probe: `probes/verify_subject.py`, outputs `subject-verify.before.json` and
`subject-verify.after.json` (identical).

### One custody observation, outside the subject

Comparing every declared path against the live repository, **1742 of 1743 are
byte-identical**. One diverges:

`docs/coop/design-corrections/reviews/NEXT-REVIEW.md` — declared
`bf1a5baa…` / 50 391 bytes, repository now `3c44beb4…` / 54 122 bytes, mtime
13:10:04, i.e. after the 12:54 freeze and after this session opened. I did not
write it; it is the orchestration's own next-review ledger, not a design or
semantic artifact. **The frozen snapshot copy is intact and is what I reviewed**,
so this does not affect the verdict. I record it because a later application
step that copies from the working tree rather than the frozen snapshot would pick
up bytes this review did not cover.

---

## 2. Delta reviewed

v6 → v7: **133 added, 47 changed, 0 removed, 1563 unchanged**. The substance is
concentrated where the v6 findings were: `identity-and-evidence.md` +20 713 B,
`identity-schemas.v2.json` +34 865 B, `identity-model.py` +30 957 B,
`check-identity.py` +90 420 B, `correction-crosswalk.proposed.json` +16 976 B,
order annotations across every schema document, plus retained coauthor and Codex
custody directories. I did not extend the v5 ACCEPT or any earlier grade to any
changed byte; every finding below rests on my own measurement of v7 bytes.

---

## 3. Prior finding dispositions

### NEW-MUST-1 — RESOLVED

v6 held that the auxiliary-digest law had no closing rule and that five
identity-bearing fields had no producing recipe or defined record.

**The closing rule now exists and is stronger than the array law's.** The array
law closes by naming a default; the digest law closes by admitting *no* default:
an unannotated 64-hex field is inadmissible. I verified that this is real rather
than aspirational, in four independent steps.

**(a) No residue.** Walking the raw schema bytes myself — resolving
`$ref: #/$defs/Hash`, which a naive walker misses, and accounting for the
`(?![\s\S])` anchor this bundle uses instead of `$` — there are **57 bare-64-hex
field sites and all 57 carry `x-opensip-digest`**. Representations used:
`canonical-record` 33, `raw-artifact` 14, `h-identity` 5, `by-domain` 3,
`capability-manifest-id` 2. All four representations and all four retention modes
are within the closed vocabularies. The checker's own coverage assertion
dispatches on pattern/`$ref`, never on a field name. (`probes/p1`, `p2`)

**(b) The recipes are independently constructible.** I implemented `C` and `H`
from the contract prose in section 3 *without reading `canonical.py`*, then:

- my encoder agrees with theirs on 21 adversarial values, including control
  characters, `U+007F`, `U+2028`, a non-BMP scalar, `-2^63`, `2^64-1`, an empty
  key, a slash, and nested arrays — **0 disagreements**;
- my frame equals theirs, and dropping the `uint64BE` length changes the digest,
  so the length field is load-bearing;
- **all five author literal vectors reproduce under my encoder**;
- **my own five fresh vectors** (different values, different shapes, non-ASCII
  parameter text) produce digests the author's encoder agrees with *and* which
  validate under the registered record selectors, with no collision against the
  author's vectors.

A recipe that were still parked could not be hit independently. (`probes/p3`)

**(c) The five records exist and are closed.** `program-predicate`,
`finding-parameters`, `stage-spec`, `commit-inventory` and `owner-source-set` are
registered `$defs` with every field required. `finding-parameters.parameters` is
an object map with no order annotation — so parameter names are unique by
construction and ordered by the encoder itself; I confirmed a duplicate key is
refused at parse time, before deserialization loses it.

`program-predicate` is an *address* into the admitted `RuleProgramV1`, not a
restatement. I tested the addressing law against a **real three-level nested
predicate** (`and` over an atom, an `or`, and a `not`), validated under the
*actual* workflow `PolicyDocumentV1`/`RuleProgramV1` schemas rather than the
fixture's single atom. My independent implementation of the stated addressing
rule enumerated exactly the same 8 addresses as the model
(`p, p.0, p.1, p.1.0, p.1.1, p.1.1.0, p.2, p.2.0`); child addresses agree; `p.9`
and the leading-zero `p.01` both refuse. All 8 addressed nodes mint distinct
digests, **and the same node at two different addresses mints different digests**,
so the address is load-bearing and a witness cannot name a predicate the admitted
program does not contain. (`probes/p9`)

**(d) `stageSpecDigest` is one record — NEW-ADV-2 closed.** The annotation at
`execution-plan.stages[].stageSpecDigest` and at `cache-key.stageSpecDigest` is
**byte-identical** and names `#/$defs/stage-spec`. `regeneration-key` is literally
`{"$ref": "#/$defs/cache-key"}` — genuinely one schema, two H domains, exactly as
the contract states. `stage-spec.parameters` rows are byte-identical in shape to
the analysis-spec's rows, and the model enforces that each is also an analysis-spec
row, so a stage takes no hidden input.

### Real graph admission — both languages, attacked

I closed **two complete Runs through the actual `close_run`**, each with its own
semantic universe, nonempty facts, Coverage and `nativeContextDigests`:

| | TypeScript | Rust |
|---|---|---|
| Run | `run2:d3ae6d56…` | `run2:6dfd7d9b…` |
| language mode | `ts-tsconfig` | `rust-cargo` |
| fact anchors | `a.ts` | `src/lib.rs` |
| rule subject universe | typescript | rust |
| universe domain | `native.semantic-universe.typescript.v2` | `native.semantic-universe.rust.v2` |
| bound context domain | `native.context.typescript.v2` | `native.context.rust.v2` |
| facts / Coverage / Plan contexts | 1 / 1 / 2 | 1 / 1 / 2 |

The Rust Run is a genuine Rust path, not a Rust context carried inside a TS Run:
the request, the analysed source, the rule's subject universe and the bound
universe are all Rust.

I then ran **26 attacks of my own**, deliberately re-hashing altered payloads
under their *own correct* digests and honestly repointing every referencing field
and re-minting the Plan, so the content-addressed store's re-hash check could not
fire and any refusal had to come from the semantic law. Every one was refused
with an exact typed cause:

| Attack | Refusal |
|---|---|
| TS context altered to another **schema-valid** `moduleResolutionMode`, re-framed, universe re-bound, Plan re-minted | `NATIVE_CONTEXT_ADMISSION:native.native-context-field-mismatch:moduleResolutionMode` |
| raw canonical payload retained under its own SHA where a frame is required | `H_FRAME_PREFIX` |
| H frame offered where a `canonical-record` is required | parse failure on the framing bytes |
| well-formed **wrong-schema** record under its own correct digest | record validation refusal |
| source bytes altered and honestly re-inventoried | `VCS_INVENTORY_JOIN` reached via closure |
| Plan config diverging from snapshot config | `SNAPSHOT_INPUT_JOIN` |
| Plan naming an unretained context | `EVIDENCE_UNAVAILABLE` |
| Rust dependency file-manifest member bytes tampered | `BLOB_DIGEST` |
| Rust projected `.cargo/config.toml` bytes not retained | `EVIDENCE_UNAVAILABLE` |
| **`configProjectionSha256` replaced by the raw projection-file SHA** | `H_FRAME_PREFIX` |
| Rust `crateRootPaths` naming an uninventoried path | `NATIVE_UNIVERSE_PATH_NOT_INVENTORIED:src/not-in-snapshot.rs` |
| universe binding a context of the other language | `REFERENCE_IDENTITY` |
| snapshot-foreign context (lockfile digest not in snapshot) | `NATIVE_CONTEXT_SOURCE_MISMATCH:package-lock.json` |
| context with uninventoried `configGraphPaths` | `NATIVE_CONTEXT_PATH_NOT_INVENTORIED` |
| **forged ADMIT** — native admission stubbed to return `ADMIT` for everything | `NATIVE_CONTEXT_ADMITTED_IDENTITY` |
| altered stdlib closure reusing the old identity | refused; an honest re-derivation yields a *different* identity |
| foreign scope root spliced into a view | `REFERENCE_IDENTITY` |
| missing preimage for analysis spec / grant / scope | `EVIDENCE_UNAVAILABLE` |

The forged-ADMIT case is the important one: because Run closure re-derives the
context identity from the retained bytes and compares it to the frame digest, a
fabricated `ADMIT` cannot name a different context. A caller-chosen flag buys
nothing. The first case independently reproduces Codex's counterexample, which I
inspected directly rather than inferring: its `final-recheck/custody.json` lists
85 current sources and its `result.final.json` lists 77 captured sources, and I
confirmed **all 162 hash to exactly the frozen v7 bytes**, so its recheck really
was run against these bytes. Its `originalPositiveRun` `run2:88bd8348…` is the
same Run my own unreached-context probe closed. (`probes/p4`, `p5`, `p6`)

**H is never silently a raw payload digest.** Domain separation, frame-vs-payload
non-interchangeability in both directions, and the Rust `CargoConfigProjectionV2`
two-digest distinction (`projectionSha256` = raw SHA-256 of the projected file
bytes; `rust-v2.configProjectionSha256` = H over the whole record) all hold under
substitution attack.

### Cache lookup key vs cache HIT admission

Construction is pure and grants nothing; admission does the work.

- the key is deterministic, and `cache2`/`regen2` differ only by domain;
- a key **constructs successfully for a stage that does not exist** — a miss is
  not a failure — but HIT admission refuses it with
  `CACHE_STAGE_NOT_IN_THE_EXECUTION_PLAN`;
- legitimate cache and regeneration hits admit, and both report
  `grantsEvidenceAuthority: false`;
- the admitted `stageSpec` is byte-equal to the execution plan's own retained
  stage-spec record — the same record, not a parallel one;
- invented output schema → `CACHE_OUTPUT_SCHEMA_JOIN`; swapped producer closure →
  `CACHE_STAGE_SPEC_PRODUCER_JOIN`; cross-Plan key → `CACHE_PLAN_JOIN`; foreign
  scope → `CACHE_SCOPE_SOURCE_JOIN`; a payload-domain reference offered as an
  authoritative root → `CACHE_INPUT_PAYLOAD_REF_NOT_A_ROOT:fact-payload`;
  unselected native context input → refused.

Sealed-output mismatch is typed as `evidence.regeneration-mismatch` with
`HOST.IO_FAILURE`, is a member of the closed public detail registry, and the
suite asserts the sealed Run bytes are preserved unchanged across the mismatch.
(`probes/p5`)

### Remaining-field sweep

Every `x-opensip-digest` annotation resolves: every `canonical-record` selector
exists in the named bundle or document, every `h-identity` `domainSet` is
registered, all 9 domain-set selectors resolve in the native document. All 32
`Ref` domain enum members are registered; `ProofInputRef` (12) and
`FindingEvidenceRef` (5) both exclude `run`, `semantic-evidence`,
`evaluation-seal` and `proof-bundle`, and the proof input vocabulary excludes the
three `*-payload` domains, which are resolvable only through their owning
object's `payloadSchemaDigest`.

**Excluded semantic inputs:** for all 15 prefixed identity domains I checked every
input its contract domain-table row names against the schema's `required` list —
**no domain omits a named semantic input**. Acyclicity holds structurally: the
proof bundle carries no `evidenceId`/`runId`/`evaluationSealId`, evidence may carry
proof, the seal carries both, the Run carries the seal.

**Collisions:** four field spellings carry more than one annotation object. None
is a collision. `items` is my walker's JSON-Schema keyword leaf, not a field name.
`payloadSchemaDigest` is `raw-artifact` at all three sites, differing only in
prose description. `payloadDigest` is `canonical-record` at all three, registered
by the sibling schema digest (imports additionally through the workflow
`PayloadRegistryV1` keyed by `kind` + `payloadDomain`), which is the correct
semantic difference. `outputSchemaDigest` is the same `raw-artifact` at both
sites, and the model enforces their equality. This is exactly the behaviour the
contract mandates — dispatch is per site, never per name. (`probes/p12`)

### NEW-SHOULD-1 — RESOLVED

Coverage is now **complete, not partial**. Walking every schema document myself:
**329 arrays, 329 annotated, 0 vocabulary violations, across 20 documents** —
including the two the v6 finding did not enumerate,
`foundation/import-source-context.schema.json` (1/1) and
`foundation/product-quality-report.schema.v3.json` (4/4). The three documents v6
measured at zero are now complete: native 85/85, security 60/60 (the 61st is my
walker matching a property literally *named* `items`), product-configuration
10/10. Workflow schemas are complete across all 13. (`probes/p7`)

Enforcement is real, not documentation: `x-opensip-order` is registered in
`ExactValidator.VALIDATORS` via `validators.extend`. An annotation outside the
closed vocabulary refuses; malformed `{"by": …}` forms refuse.

The distinctions the scope names all hold under my own adversarial cases:

- **the encoder never normalizes** — `["z","a","z"]` and `["a","a"]` survive
  encoding intact; only object keys are sorted;
- **raw UTF-8 order ≠ canonical escaped-string order**: `["\n","!"]` is admitted
  by `utf8` and refused by `canonical-set`, and the reverse order is admitted by
  `canonical-set` and refused by `utf8` — the two orders genuinely disagree,
  because escaping moves `\n` from `0x0A` to `\` `n`;
- **tuple field order ≠ canonical object order**: `[{"a":"z","b":"1"},
  {"a":"a","b":"2"}]` is admitted by `{"by":["b"]}` and refused by
  `canonical-set`, and the reverse holds for the reversed rows;
- **`canonical-order` admits measured duplicates; `canonical-set` refuses them** —
  and the single `canonical-order` site in the bundle is exactly
  `g13-result-schema.v5.json …/fixtureResults/items/properties/actualObservations`,
  the measured observations of a truthful G13 FAIL report. Both still refuse a
  descending order;
- every selector holds positively and negatively, and a missing or wrong-typed
  sort key refuses rather than passing.

Annotations match the owning prose. Ordered sequences stay sequences: `argv`
("exact argument vector; no shell, no interpolation, no PATH search"),
declaration-signature and clone `excludedTokens`, TypeScript `paths[].substitutions`,
configuration `allowedScopes`, `orderedSteps`, `stepResults` and repair `targets`
are all `sequence`; resolved semantic sets (`scopeIds`, `facts`, `coverageIds`)
are `canonical-set`. Input configuration layers preserve sequence while resolved
semantic sets normalize explicitly, exactly as section 3 states.

Native order violations keep their own typed cause and are **not** misclassified
as a language error: reversing `libSelection` yields
`native.native-context-field-mismatch:lib-selection-order` and reversing
`configGraphPaths` yields
`native.native-context-field-mismatch:array-order:configProjection/configGraphPaths`.
Neither mentions a language. (`probes/p8`, `p9`)

All earlier blind M1–M5, S1–S6 and A1–A4 fixes remain intact: the foundation
identity suite that carries them passes 354/354 unchanged, and the array-encoder,
policy-order, resolved-config, subject-scope, TS-context and CVE-1 checks that
v6 verified are still present and passing in the same suite.

### NEW-SHOULD-2 — RESOLVED

All **16/16** crosswalk rows now carry the three-way separation, and I verified
each one rather than reading the shape:

- `latestCompletedReview` pins `post-reset-review.v6/review.json`; I rehashed the
  file and got `269c1622…`, matching the declared value, for all 16 rows;
- its declared `subjectManifestSha256` `cb345532…` equals the review's own
  `subject.manifestSha256` **and** equals v7's declared
  `predecessorManifestSha256` **and** equals the hash of the v6 manifest embedded
  in this subject — so the pinned predecessor is the actual one;
- every row's `selector` (e.g. `/arDispositions/AR-01`) **resolves inside the v6
  review document**, and every declared `overallVerdict` matches it;
- all 16 `historicalReviews` files exist and are labelled immutable;
- all 16 `currentReviewBinding` blocks are `PENDING-INDEPENDENT-REVIEW` and
  assert **no** hash, verdict or subject manifest — no self-hash cycle is
  demanded, and the v7 manifest hash appears nowhere in the crosswalk;
- `post-reset-review.v1` now appears **only** as a historical entry, never as
  `latestCompletedReview` or as a current binding.

This is the correct resolution: it neither demands that a future review be
hash-embedded in its own frozen subject nor presents a stale review as current.
(`probes/p10`)

### Advisories

- **NEW-ADV-1 — addressed.** `post-reset-dispositions.v7.proposed.json` carries an
  explicit `statusVocabulary` distinguishing in-progress work, claimed author
  corrections pending independent review, and pending application binding, and the
  crosswalk uses the matching `status` values. Earlier frozen vocabulary is
  retained historically rather than rewritten.
- **NEW-ADV-2 — closed.** See above: one byte-identical annotation, one record.
- **NEW-ADV-3 — correctly preserved, still undemonstrated.** All **32** gates
  `DR-G01…DR-G32` carry `standing: DESIGN-CONTRACT-PENDING-REVIEW`,
  `qualified: false`, `demonstrated: false` and `implementationHarnessAuthored:
  false`; **not one** is true anywhere. `platformFamilies` is exactly the four
  D-371 machine IDs: `linux-x86_64-gnu`, `linux-aarch64-gnu`, `macos-aarch64`,
  `macos-x86_64`. `DR-G17` is present and unqualified, consistent with D-372
  reactivating SARIF rather than claiming it measured.

---

## 4. Suite execution

Run in a disposable copy at
`post-reset-review.v7/work`, with `/tmp/opensip-architecture-review-env/bin/python -I -B`.

| Suite | Expected (`validation-summary.v1.json`) | Measured | Δ |
|---|---|---|---|
| foundation total | 697 | **697** | 0 |
| — check-foundation | 231 | 231 | 0 |
| — check-identity | 354 | 354 | 0 |
| — product-quality | 24 | 24 | 0 |
| — product-configuration | 28 | 28 | 0 |
| — array-order | 60 | 60 | 0 |
| foundation source pins | 1094 | 1094 | 0 |
| security cases | 456 | **456** | 0 |
| security invariant sweeps | 10 | 10 | 0 |
| native cases | 132 | **132** | 0 |
| native matrix cells / qualified | 60 / 0 | 60 / 0 | 0 |
| workflows checks | 1253 | **1253** | 0 |
| integration checks | 360 | **360** | 0 |

**Zero failures, zero count deltas.** All eleven deterministic reports regenerate
**byte-identically** to the frozen copies (foundation, identity, product-quality,
product-configuration, array-order, validation, security-lifecycle,
native-evidence, workflows ×2, integration). Independently of the suites I
verified **all four source-pin manifests: 1288/1288 rows hash-exact, 0 bad, 0
absent** (foundation 1094, native 68, security 67, workflows 59).

Passing tests are not semantic acceptance, and I did not treat them as such —
every disposition above rests on probes I wrote, and the one MUST-class finding
v6 raised was found by sweeping for a defect class, not by running suites.

---

## 5. Dispositions

### AR-01…AR-16 — all ACCEPT

Each row's `contract`, `selector`, `evidence` paths and unit resolve in the
subject; each carries the verified three-way review separation of §3; each is
`AUTHOR-CORRECTED-PENDING-INDEPENDENT-REVIEW` or
`PROPOSED-SOURCE-MAP-PENDING-REVIEW-AND-APPLICATION`, i.e. none claims an award.
The five units cited (foundation, native, security, workflows, integration) all
execute at their declared counts with byte-identical reports. **I accept these as
review records, not as an award of readiness**; the applied wrapper still has to
bind an accepted successor review and the exact source row.

### FW-01…FW-15 — all ACCEPT

All 15 rows are present in `current-source-map.proposed.md` with a current
contract and a preserved boundary. The honesty of the boundaries is the basis:
FW-02 keeps semantic-similarity advisory with no bundled model or repair
authority; FW-11 keeps metric redistribution out of "behavioural improvement";
FW-14 states plainly that no digest-pinned corpus exists and that synthetic design
cases are not that corpus; FW-15's closed DSL is the one I exercised against the
real `PolicyDocumentV1`/`RuleProgramV1` schemas. The prior FUTURE/preview wording
is correctly recorded as no longer a reason to omit the design.

### Inherited residuals — all ACCEPT as scoped dispositions

All 16 `DR-011-R01…R16` rows and all 11 parent rows `DR-001…DR-011` carry an
individual product-successor disposition with its preserved limitation. Three I
checked in substance:

- **R06 EVIDENCE** — identity-and-evidence is now genuinely the owning Phase-1A
  packet: proof/evidence/seal closure, retained regeneration closure, custody,
  the immutable-assurance vs current-availability split and typed D9 joins are
  all present and exercised.
- **R12 EVALUATION PROOF** — `evaluation-residual-dispositions.proposed.json`
  carries **30 items with 30 dispositions**: 19 `RES-EP13-01…19` as
  "prospective-product-replacement; historical limitation preserved", 7 as
  "…historical observation preserved", 4 as "historical measured escape
  preserved; mechanism not in product authority". The count matches the required
  19 RES + 7 NB + 4 escapes exactly, and no escape is reclassified as fixed.
- **R10 blind consumer-B** — correctly states it *cannot* be closed by the
  proposed table and needs a fresh implementer litmus after final integration.
  I accept the disposition; the litmus itself is not mine to perform.

`DR-003`'s prospective pre-blueprint split is explicit, scoped, and expressly not
a SATISFIED/DEMONSTRATED claim, leaving DR-G09/G18/G19/G21/G22 and DR-012 as
mandatory pre-release measurements.

### Scoped review owners DR-201…DR-205

| Row | Disposition | Basis |
|---|---|---|
| **DR-201** Semantic correctness | **ACCEPT** | The v6 CHANGES_REQUIRED rested entirely on parked recipes. Nothing is parked now: 57/57 bare-hex sites annotated with no default, five closed records, all five recipes independently reconstructed from prose, and the divergence v6 demonstrated (`proof2:edba615b…` vs `proof2:67d4359b…`) can no longer arise because the representation is declared per site and a payload offered where a frame is required fails on the prefix. Happy-path vs pre-admission, Run vs command finalization and post-commit output failure remain unblurred. |
| **DR-202** Delivery/operations | **ACCEPT** | Verified in these bytes, not carried over: `evidence.regeneration-mismatch` is typed `HOST.IO_FAILURE`, is in the closed 282-entry public detail registry, and the sealed Run bytes survive the mismatch unchanged; `evidence.missing` is likewise typed as custody loss rather than a false predicate; commit ordering and the availability/assurance split are explicit; 32/32 gates `qualified:false`. |
| **DR-203** Prototype lessons | **ACCEPT (partial, on the honesty of the split)** | FW-14 and the g13 note still state plainly that no digest-pinned corpus, matrix or thresholds exist, that the g13 platform aliases are labels within an old corpus and not machine IDs accepted by product grants, and that historical preview evidence never qualifies a native product cell. Acceptance is of the disclosure, not of completeness; DR-118/DR-G13 stay blocking. |
| **DR-204** V1/coop invariant coverage | **ACCEPT** | Independently re-measured: manifest hash exact, 1743/1743 files, 0 undeclared, 1288/1288 source pins, byte-identical regeneration of all 11 reports, and **31/31 historical files verified unchanged against the live repository** with the report's own `openingSha256` = `currentSha256`. NEW-SHOULD-2 is carried and resolved. No newest-head heuristic or baseline-only standing; `readinessChanged:false`. The one repository divergence in §1 is a coordination file outside the design surface and is recorded rather than absorbed. |
| **DR-205** Small-core/components | **ACCEPT** | Core/TCB/product boundaries, storage, packaging and fault containment are stated; component selection is explicitly first-party bounded and opens no third-party plugin or untrusted-runtime ecosystem (consistent with the scope's "no untrusted ecosystem / implicit repository execution"); P-1/P-2/G3 implications are carried explicitly in D-372 §"Explicit product and output re-entry acts"; DR-128 remains post-MVP. |

Accounting: **5 of 5 ACCEPT**. Condition 3's review-owner requirement is
discharged *on the current scope for these frozen bytes*. That is one input to
the central register's condition set; it is not itself a readiness grade, and
conditions 4 and 5 are untouched by this review.

---

## 6. New findings

**newMustIssues: none.** I found no unresolved required design gap.

**newShouldIssues: none.**

**New advisories:**

- **V7-ADV-1 — "every 64-hex field" is wider than the rule's enforced scope.**
  The closing-digest-law paragraph says *"Every 64-hex field in
  identity-schemas.v2 has exactly one representation … a 64-hex field carrying no
  annotation is inadmissible."* Enforcement — correctly — covers **bare**
  64-hex fields: 52 prefixed identity fields (`^plan2:[0-9a-f]{64}…`,
  `^closure2:…`, `prj1-…`) carry no annotation, because their domain is carried by
  the prefix and defined by the section 3 domain table. The design is closed
  either way; only the sentence is broader than what it enforces. A blind
  implementer could read it as requiring annotations on prefixed identities too.
  Saying "every **bare** 64-hex field" would remove the ambiguity. Not a gap.

- **V7-ADV-2 — a Plan may select several admitted contexts of one language.**
  Adding a second, fully well-formed TypeScript context to
  `plan.nativeContextDigests` closes a Run. I characterised this before judging
  it, and it is **not** an identity or trust break: the extra context is genuinely
  re-admitted (removing its closures or its frame bytes refuses), a
  snapshot-foreign context is refused with an exact typed cause, no universe binds
  it so no evidence is attributed to it, and Plan and Run identities both change,
  so nothing is silently equal. Nothing in the contract requires per-language
  uniqueness, so this is consistent with the design as written. The advisory is
  presentational: a consumer that reads `plan.nativeContextDigests` as *the*
  toolchain for a language would be reading a set as a scalar. The authoritative
  per-fact answer is the fact's `sourceUniverse`.

- **V7-ADV-3 — application must copy from the frozen snapshot.** Per §1, one
  declared path already differs in the working tree. The application step should
  bind snapshot bytes, not working-tree bytes.

---

## 7. Limitations

These bound the verdict and must not be read as qualification.

1. **Synthetic TCB inputs.** Every compiler, cargo, stdlib, LLVM, sysroot,
   lockfile, dependency-acquisition, OS, crypto, clock, lease and evaluator
   observation is an explicit synthetic trusted assumption. No compiler, cargo,
   build script, proc macro, OS durability or repository code was executed and no
   real toolchain was measured. This is TCB assumption, never product
   qualification.
2. **The fixture interpreter is small.** It evaluates a single-atom subset. I
   mitigated this by exercising the record shapes, digests and addressing law
   against a real three-level predicate under the *actual* workflow policy and
   rule-program schemas, but the declarative language itself is not qualified by
   this review, and neither is a native Coverage or relation payload registry.
3. **The Rust corpus is one vendored registry package** over a two-package
   `Cargo.lock`. Real crate graphs, workspace member enumeration, feature
   unification by an actual `cargo metadata` run and missing-crate Coverage remain
   the native unit's own cases and later qualification.
4. **`admit_cache_entry` is not a cache subsystem.** It is a post-construction
   conformance check over a lookup key and its consumed input closure; it does not
   fetch or validate cached output bytes or decide reuse policy.
5. **I reused the subject's fixture builders** to obtain valid graphs. Every
   attack, mutation and assertion in `probes/p4`–`p6`, `p9` is mine, and the
   digest reconstruction in `probes/p3` uses an encoder I wrote from the contract
   prose alone. Where I reused an author fixture I say so; I did not treat any
   self-consistent author vector as independent reconstruction.
6. **Not performed here, by design:** the fresh blind consumer-B review
   reconstructing both TypeScript and Rust paths from normative inputs alone, and
   the complete independently reviewed application. Both are later independent
   sessions.
7. **No platform qualification.** All 32 gates remain undemonstrated on the four
   D-371 machine IDs. Real product qualification is a later release obligation and
   its absence is **not** a missing design-implementation prerequisite.

---

## 8. What this verdict is

ACCEPT means: on the exact frozen bytes of manifest
`b5cfb5d316eb0101950476a37a2095ed0d9c5d51263408d3462f105d63165f7b`, I found **no
unresolved required design gap**. The v6 MUST and both SHOULDs are genuinely
resolved and independently verified rather than asserted, and the three advisories
are addressed or correctly preserved.

This is an exact review record for later application. It awards no readiness, no
product qualification and no implementation authorization. Condition 5 remains
NOT MET. Current application and readiness remain deliberately unapplied pending
the blind and application reviews that follow.
