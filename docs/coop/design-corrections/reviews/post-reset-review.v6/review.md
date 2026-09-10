# Fresh independent review — frozen candidate-subject.v6

**Verdict: CHANGES_REQUIRED** (one MUST gap; every prior blind finding resolved)

Reviewer: actual Claude, fresh independent session. I authored none of the subject
bytes. I am not the v5 reviewer (session `52cf468a-…`), not the blind consumer
(`consumer-b.v1`), not the actual-Claude coauthor (session `f360faba-…`) and not
Codex. Everything numeric below was computed by code I wrote, in
`/tmp/opensip-design-corrections/post-reset-review.v6/probes/`, against the frozen
subject only.

This is a **design-reference** review. Nothing here awards readiness, qualifies a
platform, authorizes implementation, or discharges any later gate. Condition 5
remains **NOT MET**.

---

## 1. Manifest and custody

| Check | Result |
|---|---|
| Manifest path | `docs/coop/design-corrections/reviews/candidate-subject.v6.json` |
| Manifest SHA-256 | `cb345532f52980c1cba9d519eacecbe6748885c6693594d0845f0c9b7489a69f` |
| Required SHA-256 | `cb345532f52980c1cba9d519eacecbe6748885c6693594d0845f0c9b7489a69f` — **exact match** |
| Snapshot root | `/tmp/opensip-design-corrections/candidate-subject.v6` |
| Files declared / verified | 1610 / **1610 exact**, before and after review |
| Byte-length total | 19 947 075 declared, 19 947 075 measured |
| Undeclared files on disk | **0** |
| Predecessor manifest | `ccb2311ddbcaea7e8bd540030621c982fa6757792721095a505e4e47652c74cf` (v5) |
| Blind review input custody | `consumer-b.v1/output/blind-review.json` = `112fae48d7476c3763dc7f2ba5b348e088d86619cf03d01dddf38faebbba1422`, matching the value `post-reset-dispositions.v6.proposed.json` cites |
| Historical preservation | 31/31 opening historical files unchanged, 0 changed |

I re-verified every source hash **after** completing all probing; the subject did
not move. I edited nothing in the snapshot or the repository. All work is confined
to `/tmp/opensip-design-corrections/post-reset-review.v6/`, including a disposable
scratch copy used for the suite runs.

The v5 ACCEPT covers only bytes that did not change. I treated the v6 delta as
unreviewed and re-derived each disposition below from current bytes; where a
property was unchanged I still re-measured it rather than inheriting the grade.

---

## 2. Source-pinned suites, workflow surface and integration

Run with `/tmp/opensip-architecture-review-env/bin/python -I -B` from an
independent scratch copy of the frozen tree. Expected counts taken from
`validation-summary.v1.json`, not from historical prompt numbers.

| Suite | Expected | Measured | Pins |
|---|---|---|---|
| foundation (`run-reference-checks.py`) | 424 | **424** (231 + 141 + 28 + 24) | 1092 valid |
| security (`check-security-lifecycle.v1.py`) | 456 + 10 sweeps | **456/456, 10/10 sweeps** | 65 |
| native (`check_native_evidence.v2.py`) | 132, 60 cells, 0 qualified | **132/132, 60 cells, 0 qualified**, 0 open objects | 67 |
| workflows (`run-reference-checks.py`) | 1253, 45 commands, 43 goldens | **1253**, 45 commands, 43 goldens, 13 schemas | 58 valid |
| integration (`check-integration.py`) | 352 | **352 passed, 0 failed** | — |

**Determinism: byte-identical.** Four generated reports reproduce the in-subject
pinned reports exactly:

```
foundation/validation-report.json          56a2a59361a0f20c…  IDENTICAL
workflows/workflows-validation-report.json 9af7734a1a280fc8…  IDENTICAL
security/security-lifecycle-report.v1.json d1ce3f6b5727a94c…  IDENTICAL
integration-report.v1.json                 7472a0fba5ad30c9…  IDENTICAL
```

No delta to investigate. Reproduction from a different absolute path with a clean
interpreter shows the checkers carry no path, clock or environment dependence.

Every suite self-reports `productQualification: false`; the security sweep name
moved from a "bounded pending registration gap" to
`public-domain-details-are-a-closed-fully-registered-set`, consistent with the
registry actually landing.

Passing these suites is design evidence only. It does not prove absence of gaps,
which is why §4 reports one that the suites do not detect.

---

## 3. Blind findings M-1…M-5, S-1…S-6, A-1…A-4 — independently probed

I did not accept the handoff or the Codex review as evidence. Each item below was
attacked with my own code.

### M-1 `subjectScopeCommitment` producing recipe — **RESOLVED**

Probe `p4_m1_subject_scope.py`. I implemented the canonical encoder and the `H`
frame **from the prose alone** and recomputed the commitment independently:

```
my H("subject-scope", D)   bca0e21ac396ea0303c916e4271ac3bad6d8e5d449f4f7dea896dfbecbdabc13
model scopeId              scope2:bca0e21a…bc13
model commitment           sha256:bca0e21a…bc13
recipeReproducesFromProseAlone   true
identicalSuffix                  true
```

The recipe is stated field-by-field in native §4.1a, agrees with identity §3, and
mints one preimage and one digest in two textual spellings. Enumerated-set
semantics hold: input order is irrelevant, a duplicate subject **refuses**
(`SUBJECT_SCOPE_DUPLICATE_SUBJECT`) rather than deduping, and the commitment binds
the snapshot and the enumerator closure, not just the subject list.

Adversarial results at the real producer boundary
(`admit_coverage_result_v3`) — the positive case admits and mints
`coverage2:51cb70f6…`, and:

| Attack | Result |
|---|---|
| Claimant-chosen commitment | REFUSE `native.subject-scope-commitment-mismatch`, `native.examined-universe-commitment-mismatch` |
| Producer examined a narrower partition | REFUSE `native.examined-universe-subject-count-mismatch` |
| Caller-chosen payload schema digest | REFUSE `native.coverage-payload-schema-not-registered` |
| `coverage2` whose scope is outside the view | REFUSE `native.coverage-subject-scope-outside-view` |
| `coverage2` never admitted at the producer boundary | REFUSE `native.coverage-not-admitted-at-producer-boundary` |

**No trusted claimant digest**: the host mints `scope2` from its own enumeration
before reading the payload. **No circular universe authority**: the `subject-scope`
record's eight fields name no scope, coverage, view, evidence or Run, and neither
TypeScript nor Rust universe descriptors reference a scope or coverage. Derivation
order is total and acyclic.

*Incidental positive:* my first fixture claimed `coverage=complete` with a null
`stageTerminal` and was correctly refused by RC-2 — the completeness distinction
the blind consumer praised bites on a real mistake, not only on a designed case.

### M-2 closed TypeScript native context — **RESOLVED**

Probes `p5_m2_ts_context.py`, `p5b`. `TypeScriptNativeContextV2` exists with H
domain `native.context.typescript.v2`;
`toolchain.typescriptStdlibMerkleRoot` exists and mirrors the Rust
`toolchain.rustcDevLlvmDigest` nesting exactly (**A-1** closed).

Input changes each move the identity, and to *different* values:

```
baseline           sha256:d8de0607…e77b   universe sha256:20987096…a655b
compiler changed   sha256:ca98ce73…4a62   universe sha256:c9d0e060…1470a
stdlib changed     sha256:c1573fab…5904   universe sha256:a4768f97…0b1cd
config input changed (honoredOptions.allowJs)  sha256:e4a8fdc5…b0c9
```

Foreign closure and foreign context are rejected in all seven attacks I ran:

| Attack | Refusal |
|---|---|
| stdlib closure omitted from the retained store | `native.native-context-closure-unretained:toolchain.typescriptStdlibMerkleRoot` |
| tool closure omitted | `native.native-context-closure-unretained:toolClosure.closureId` |
| empty closure store | both of the above |
| merkle root naming no retained closure | `…closure-unretained:…` |
| foreign tool closure id substituted | `native.native-context-tool-not-in-closure:runtime` |
| retained tree tampered so it recomputes differently | `native.native-context-closure-identity-mismatch:…` |
| stdlib root pointing at the tool closure | `native.native-context-closure-kind-mismatch:…` |

A Rust descriptor offered as the TypeScript context refuses
`native.native-context-language-mismatch`; a universe bound to a context this host
did not mint refuses `native.universe-context-binding-mismatch`; context bytes that
are not the admitted ones refuse with the `context-bytes-are-not-the-admitted-ones`
subject; and `context` is a **required** positional argument, so the Codex note-7
bypass is structurally closed.

**A-2** identity law verified: one digest, native prefixed form
`sha256:<hex>` and bare `DigestHex` Plan form, `sameDigestTwoForms: true`.
`plan_native_context_digests` deduplicates a genuinely shared context to one member,
keeps two different contexts separate, and emits bare hex only. Context identity is
platform-specific through the signed tool closure, as it must be.

*Correction to my own probe:* my first "foreign closure tree" case admitted. That
was my mislabeling — `tsMacClosureTrees` is a strict **superset** of the base store,
so the named closures were all legitimately retained. It is not a bypass; the
targeted tests above are the real ones.

### M-3 canonical array law — **RESOLVED**

Probes `p1_order_annotations.py`, `p2_m3_policy_order.py`. Identity §3 now states a
**closing default** — "the closing default for any array in a registered payload is
an ordered sequence, including nested arrays and raw token arrays" — plus the
machine-readable `x-opensip-order` annotation with a closed eight-value vocabulary.
`exact_order` in `foundation/canonical.py` is a genuinely enforced validator
keyword, and `sequence` is a true no-op.

The blind consumer's exact counterexample is resolved. With two schema-valid rules
whose canonical-object order is the **reverse** of their `ruleId` order:

```
ruleId order           admits;  policyDigest 7542837281546f28…
canonical-object order REFUSED  "array order ruleId: strict unique order required"
digestsDiffer   true
exactlyOneAdmits true
```

`PolicyDocumentV1.rules` and `RuleProgramV1.rules` both carry
`x-opensip-order: ruleId`; `WaiverSetV1.waivers` carries `waiverId`; reversal
refuses in each case. The generic encoder uses **no** heuristic: `uniqueItems: true`
with no order annotation still admits unsorted; fields literally named `rules` and
`set` get no special treatment; order, repeated tokens and nested arrays are all
preserved byte-exactly; an unregistered annotation refuses rather than silently
passing.

`identity-schemas.v2` carries the annotation on **52 of 52** arrays — the contract's
own explicit claim, verified. See NEW-S1 for the coverage limit elsewhere.

*On the earlier probe defect:* the blind F2 illustration used an invalid workflow
`minResolution` spelling. My regression above does not reuse it — both rules
validate under the real `Rule` schema, and the divergence is demonstrated on
`ruleId`-versus-canonical-object order. The original ambiguity was real and is now
closed on its merits, not dismissed on the strength of that spelling error.

### M-4 resolved configuration shape — **RESOLVED**

Probes `p3_m4_resolved_config.py`, `p3b`. Driven through the **actual resolver**
(`product-configuration-model.resolve`) and the **actual Run graph**, not the schema
alone.

All five sections are now `required` at the top level, and the resolver emits all
five unconditionally (`semantics = {k: resolved.get(k, {}) for k in [...]}`), so an
omitted input section and an explicitly-empty one converge to one spelling:

```
omitted sections        {"analysis":{…},"components":{},"discovery":{},"evidence":{},"policy":{}}
explicitly empty        identical bytes
digest (both)           05204503bb04fad41878cf47d2024d7164db0a1d7ed84c3c63c26f478030d3c6
convergeToOneSpelling   true
```

Propagation confirmed: both spellings converge at `snapshot2:a0371b83…` and
`plan2:959a31a6…`.

Post-resolution requiredness is enforced by the resolver, not just prose: an empty
`analysis` refuses `CONFIG_PROFILE_MISSING`; missing `capabilities` or `budget`
refuses `CONFIG_DEFAULTS_INCOMPLETE`.

**Absent vs explicitly empty `entryPoints` stays distinct**, as it should — absent
means "discover", `[]` means "none" — and the distinction survives at every level
(`config`, `snapshot2`, `plan2` all differ). Operations/presentation are excluded:
`ui` and `retention` leave the digest unchanged and never enter the semantic value,
and top-level `operations`/`presentation` keys are refused by
`additionalProperties: false`.

### M-5 public typed security details — **RESOLVED**

Probe `p6.json`. `public-detail-registry.v1.json` and
`common.schema.json#/$defs/DomainDetailCode` are **exactly equal at 282 members**,
both sorted, no duplicates. `PROFILE_SET.*` went 0 → 6, `ENVELOPE.*` 0 → 3,
`ROOT.*` 38 → 40: the 11 records the handoff specified all landed.

All eleven emit as valid typed terminations through the **real** host boundary
(`integration-host-model.public_termination`), with the D9 branches the handoff
specified — including `PROFILE_SET.NO_TR_PROFILE_ROLE` carrying
`REQUEST.SCHEMA_MAJOR_UNSUPPORTED` while the rest carry
`EXTENSION.ADMISSION_REJECTED`. A host can now emit the refusals S8/S9.1 mandate.

The vocabulary stays **closed, with no wildcard**: `PROFILE_SET.ANYTHING_GOES`,
`ENVELOPE.MADE_UP` and `ROOT.NOT_A_REAL_CODE` are each refused as
`unregistered public domain detail`. Subject-only sub-details are correctly *not*
codes — `PROFILE_SET_KEY_NOT_MACHINE_ID`, `CHALLENGE_EXPIRED` and `COUNTER_MISMATCH`
all refuse as codes, preserving the single public vocabulary. The internal alias
table (7 entries) normalizes `RF-6:AUTHORIZATION.GRANT_NOT_CURRENT` →
`TRUST.COMPONENT_REVOKED_DURING_OPERATION` at the boundary, and the alias rule
states that an unknown internal key is refused.

### S-1 D9 `hostTerminationUnion` — **RESOLVED**

Workflows §0 now carries an explicit disposition row naming
`$.hostTerminationUnion`: **superseded for product envelope major 2** by
`StepTermination`, whose closed field set includes `authority`, `domainDetail` and
`faultCause`; optional fields remain **absent rather than explicitly null**; and
§8's renderer parity `run-id` is named as a *separate closed projection* that may be
null and is never `termination.runId`. Both readings the blind consumer identified
are now adjudicated rather than left to the implementer.

### S-2 two schema-1 root documents — **RESOLVED**

Probe `p7.json`. Security S9.1 names **one** admission boundary:
`security/security-lifecycle.schemas.v1.json $.schemas.RootV1` (and `RootV2`),
reached only through `admit_root_document`. The v8 document is named the immutable
historical *rule source*, not a second gate. Measured: v8 carries 18 patterns, all
18 ending in a bare `$`, and **admits** a trailing-newline `indexOrigin.url`;
`RootV1` uses `(?![\s\S])` and **refuses** it. The successor bundle carries 38
patterns with **0** bare `$`. Two regressions exercise this through the host gate,
and the author records a mutation test proving they bite.

### S-3 inventory tie-break — **RESOLVED**

`sourceInventory` carries `x-opensip-order: path`. Two rows sharing a `path` with
different digests are now **refused** (`array order path: strict unique order
required`), as are unsorted rows; distinct sorted paths admit. Path uniqueness is
enforced, so no tie-break is needed — the option the blind consumer preferred.
Identity §3 states this in prose too ("there is no tie-break, and duplicate paths
refuse before an identity is minted").

### S-4 `regeneration-mismatch` — **RESOLVED**

Registered as `evidence.regeneration-mismatch` (identity now owns 5 of 282 records).
Prose, model and registry agree on the spelling. The termination is fully typed and
emits through the real host boundary: `operational-failed` / `HOST.IO_FAILURE` /
`faultCause: host-io` / exit 4. **Sealed-Run preservation** holds structurally — in
`EvidenceStore.restore`, `RegenerationMismatch` is raised *before* any
`self.objects.update(...)` or availability change, and the contract states "It cannot
replace the sealed Run."

### S-5 by-reference dependencies — **RESOLVED**

Probe `p8_s5_cve1.py`. (a) Identity §3 now declares CVE1 a **normative dependency**
that "must be provided to a release-builder or blind consumer", and
`resolved-inputs.v2.json` — which **is** in the frozen subject — states all eight
closed types with exact tags and lengths. I proved this is now *constructible*, not
merely verifiable: I implemented a CVE1 decoder **and encoder** from that document
alone and round-tripped all seven published vectors **byte-identically**,
reproducing all 7 `capabilityManifestId` values, all 7 `committedBytesSha256`, and
re-deriving each id from my own re-encoding of the decoded value.

(b) The contract index now states the governance distinction explicitly: the
correction crosswalk and readiness register "grant standing; they are not additional
semantic recipes and are omitted from blind reconstruction inputs to avoid
disclosing prior verdicts." The next blind kit must therefore include
`resolved-inputs.v2.json` and continue to exclude the two governance records.

### S-6 stale author obligations — **RESOLVED**

Zero occurrences of `(obligation, Codex)` or `Integration obligation` remain in
`security-and-lifecycle.md` or `native-evidence.md`. The handoff records all six as
verified-discharged against current bytes with the implementing function and
asserting check named, and E20's `CoreTransitionIntentV1` case (11 required fields,
5 operations including `store-migrate`/`store-rollback`) confirms the specific
example the blind consumer raised.

### A-1 nesting — **RESOLVED**
Identity §3 and native §2.3/§2.4/§14 cite the exact nesting:
`TypeScriptNativeContextV2.toolchain.typescriptStdlibMerkleRoot` and
`NativeContextV2.toolchain.rustcDevLlvmDigest` (inside `ToolchainIdentityV1`).
Verified present in the schema at those paths.

### A-2 prefixed identity law — **RESOLVED**
Native §11 tabulates one digest in three admitted textual forms (foundation typed
prefix / native `Sha256Text` / bare `DigestHex` suffix) with the rule for which is
required where. Verified mechanically in M-2.

### A-3 cache/regeneration shared schema — **RESOLVED**
`regeneration-key` is now `{"$ref": "#/$defs/cache-key"}` — a genuinely shared
schema that cannot drift — while the two stay separated **only** by `H` domain. On
one identical descriptor: `cache2:bfebd6ca…` vs `regen2:24a9481a…`.

### A-4 grammar token ordering — **RESOLVED**
Identity §3 now reads "`discriminator` is raw SHA256 of their canonical JSON
**ordered** string array (grammar order, repeated tokens retained)", and the array
law separately states that declaration-signature tokens preserve grammar order
including repeated tokens. The encoder preserves repeated tokens (verified).

---

## 4. New findings

### NEW-MUST-1 — the auxiliary-digest law has no closing rule, and three identity-bearing fields fall outside it

*Probes `p9_recipe_sweep.py`, `p10_digest_recipe_gap.py`.*

v6 closed the **array** ambiguity with an explicit closing default. The
**auxiliary digest** law was not given the same treatment: identity §3 has an
enumeration ("Auxiliary raw digests have producing rules, not caller-defined
meanings: `resolvedConfigDigest` …, `scopeDigest` …, `analysisSpecDigest` …,
`semanticGrantDigest` …, `vcsDigest` …") plus class rules ("Import
mapping/observation, policy, rule-program, waiver-set and witness digests are raw
SHA256 of canonical bytes under their specifically registered schema"; blobs and
inventories raw SHA256; schema digests over complete document bytes) — but **no
closing default** for anything outside both.

Five required 64-hex fields in `identity-schemas.v2` fall outside both, are named in
**none** of the five product contracts, and carry **no** schema `description`:

| Field | Record | Reaches | Class |
|---|---|---|---|
| `programPredicateDigest` | `predicate-witness` | `witnessDigest` → `proof2` → `evidence2` → `seal2` → `run2` | **semantic** |
| `parameterDigest` | `finding` | `finding2` → `evidence2` → `seal2` → `run2` | **semantic** |
| `stageSpecDigest` | `execution-plan.stages`, `cache-key` | `exec-plan2`, `cache2`/`regen2` | **semantic** |
| `outputSchemaDigest` | `cache-key` | `cache2` / `regen2` | operational |
| `inventoryDigest` | `commit-receipt` | receipt only | operational |

Control: all five *enumerated* fields (`resolvedConfigDigest`, `scopeDigest`,
`analysisSpecDigest`, `semanticGrantDigest`, `vcsDigest`) **are** named in the
contracts. The sweep is `allFiveUnnamed: true` / `allControlsNamed: true`, so this
is a real omission, not a matching artefact.

The class rule does not rescue them. The proof bundle carries a **separate**
`ruleProgramDigest` field — that is the "rule-program digest" the class rule names.
`programPredicateDigest` is a different field, digesting the individual predicate,
and there is **no registered predicate-program, stage-spec or parameter-payload
record anywhere in the schema bundle** (`$defs` contains no `stage*`, `param*` or
`predicate*` definition other than `predicate-witness` itself). So the implementer
must invent both the record shape and the digest recipe.

Demonstrated divergence, through the real identity model, for identical source and
an identical compiled predicate:

```
reading: raw SHA256 of canonical record   ppd e9570bdc…  witness c7634190…  proof2:edba615bfce73f04…
reading: H("rule-program", record)        ppd ea6c6006…  witness e86e3c1f…  proof2:67d4359b0337c754…
```

Two conforming implementations mint different `proof2`, hence different `evidence2`,
`seal2` and `run2`, for the same source — precisely what FW-06 and identity §3 exist
to prevent, and precisely the standard by which M-1 was accepted as a MUST and
fixed. The reference suites do not detect this because a single implementation is
self-consistent.

**Required.** Either (a) name each of the five fields in identity §3's
auxiliary-digest enumeration with its producing rule and its registered record, or
(b) add a closing default for digests mirroring the one now given for arrays (e.g.
"a `*Digest` field not otherwise specified is raw SHA256 of `C` of the closed record
named by its schema"), *and* add the missing closed records for the predicate
program, the stage spec and the finding parameter payload — since a closing default
cannot bind to a record that does not exist.

### NEW-SHOULD-1 — `x-opensip-order` is applied only to `identity-schemas.v2`

*Probe `p1_order_annotations.py`.* Coverage of the contract's own machine-readable
mechanism:

| Bundle | Arrays | Annotated |
|---|---|---|
| `identity-schemas.v2` | 52 | **52** |
| `native-evidence.schemas.v2` | 85 | **0** |
| `security-lifecycle.schemas.v1` | 61 | **0** |
| `product-configuration.schema.v2` | 10 | **0** |
| workflow schemas (13 documents) | ~114 | **3** (policy-document only) |

This is *not* an ambiguity — the closing default makes an unannotated array a
`sequence`, and the native contract declares its stricter orders in prose
(`libSelection` "strictly sorted by UTF-8 name bytes";
`standardLibraryComponentDigests` "sorted by `component`" / "strictly unique
component keys in UTF-8 order"; `crateRootPaths`; `configGraphPaths`), which the
native model enforces (`native.native-context-field-mismatch:lib-selection-order`,
`:stdlib-component-order`). A producer following prose is correct, and a wrong order
refuses rather than diverging.

But the annotation is the contract's stated mechanism for exactly this, and where a
schema is silent while a model enforces a strict order, the schema/model agreement
is not machine-checkable. Annotate the native, security, product-configuration and
remaining workflow arrays — at minimum every array whose owning contract declares a
stricter order — so the drift check that exists for `identity-schemas.v2` extends to
the rest.

### NEW-SHOULD-2 — crosswalk review provenance is stale

Every one of the 16 `correction-crosswalk.proposed.json` items still carries
`review.path = reviews/post-reset-review.v1/review.json` with
`subjectManifestSha256 = e7403b70…`, four subjects behind. The accompanying
`currentBytesStanding` ("Corrections in progress; changed bytes require a new
independent review") keeps this **honest** — no acceptance is claimed — so this is
metadata hygiene, not a false grade. Repoint each row at the accepted successor
review when one exists.

### Advisories

- **NEW-ADV-1.** `post-reset-dispositions.v6.proposed.json` items use
  `proposedDisposition` while the crosswalk uses `status` and the residual tables use
  prose. A single vocabulary would make the pending-versus-awarded distinction
  harder to misread at application time.
- **NEW-ADV-2.** `cache-key` reuses `stageSpecDigest` under the same field name as
  `execution-plan.stages`. If NEW-MUST-1 is fixed by naming records, state
  explicitly that both are the same digest of the same record, so a reader does not
  infer two recipes from one spelling — the same trap A-2 addressed for identities.
- **NEW-ADV-3.** The four `platformFamilies` in `qualification-gates.proposed.json`
  (`linux-x86_64-gnu`, `linux-aarch64-gnu`, `macos-aarch64`, `macos-x86_64`) match
  the D-371 four-machine scope exactly; all 32 gates are
  `DESIGN-CONTRACT-PENDING-REVIEW` with `qualified: false` and `demonstrated: false`.
  Correct, and worth keeping explicit in the application so no gate is read as
  measured.

---

## 5. AR-01…AR-16 disposition

Scope: design-reference correctness only, against the frozen bytes.
`ACCEPT (scoped)` means I found no gap forcing implementer invention within that
row's obligation; it awards no readiness.

| Row | Unit | Obligation | Disposition | Basis |
|---|---|---|---|---|
| AR-01 | foundation | Exact integer admission | **ACCEPT (scoped)** | foundation 424/424; exact `const`/`enum`/integer typing verified in `canonical.py`; `1.0`/`true`/boundary controls hold |
| AR-02 | foundation | Authenticated qualification subject and independent oracles | **ACCEPT (scoped)** | product-quality 24, product-configuration 28; oracles report `productQualification: false` |
| AR-03 | security | Repository/config custody and discovery | **ACCEPT (scoped)** | security 456 + sweep `admitted-boundary-inventory-joins-security-discovery-and-native-unit-discovery`; S-6 join discharged |
| AR-04 | security | Forward clock excursion and poisoned-floor recovery | **ACCEPT (scoped)** | sweeps `clock-floor-monotone-no-clamp-report-only-writes-nothing`, `recovery-epoch-applies-once-…` |
| AR-05 | security | Expired root continuity and live revocation | **ACCEPT (scoped)** | S-2 boundary named and regressed; `root-schema-reader-sets-typed-unsupported-never-corruption` |
| AR-06 | security | Support population and multiple platform profiles | **ACCEPT (scoped)** | `one-machine-platform-vocabulary-joins-…`; four machine IDs match D-371 |
| AR-07 | native | Sealed Rust dependencies and authorized preparation | **ACCEPT (scoped)** | native 132/132, 60 cells; not separately re-probed (recorded limitation §7) |
| AR-08 | workflows | Invocation/attempt/step/Run and action lifecycle | **ACCEPT (scoped)** | workflows 1253, 45 commands, 43 goldens |
| AR-09 | foundation | Identity/proof/custody/retention closure | **CHANGES_REQUIRED** | **NEW-MUST-1**: `programPredicateDigest`, `parameterDigest`, `stageSpecDigest` have no producing recipe and no closed record; `proof2` diverges. Selectors: `identity-and-evidence.md` §3 auxiliary-digest paragraph; `identity-schemas.v2.json#/$defs/predicate-witness`, `#/$defs/finding`, `#/$defs/execution-plan` |
| AR-10 | workflows | Runnable prior detector and portable baseline custody | **ACCEPT (scoped)** | workflows suite; blind E1–E4 comparison properties re-read as unchanged |
| AR-11 | workflows | Typed delta attribution and admitted imported evidence | **ACCEPT (scoped)** | workflows suite; conservative evidence axis retained |
| AR-12 | native | Resolution-complete authoritative negative predicates | **ACCEPT (scoped)** | RC-2 verified adversarially (it refused my own invalid `complete` claim) |
| AR-13 | native | TS/JS/Rust native cells, monorepos and output parity | **ACCEPT (scoped)** | M-2 probes; 60 matrix cells, 0 qualified |
| AR-14 | security | Core/state/trust migration and concurrent operations | **ACCEPT (scoped)** | `lease-mode-compatibility-matrix`; `CoreTransitionIntentV1` 11 fields / 5 operations |
| AR-15 | integration | One effective current narrative and obligation crosswalk | **ACCEPT (scoped)**, with NEW-SHOULD-2 | index states the governance-only distinction; crosswalk review provenance stale but honestly labelled |
| AR-16 | workflows | Provenance-specific remedies and exact outcome goldens | **ACCEPT (scoped)** | S-1 disposition row; registry 282 = enum 282; 11 codes emit through the real host boundary |

---

## 6. FW-01…FW-15 disposition

| Row | Disposition | Note |
|---|---|---|
| FW-01 zero-config/recommend | **ACCEPT (scoped)** | M-4 convergence verified through the real resolver; no implicit config write |
| FW-02 clones | **ACCEPT (scoped)** | advisory boundary retained; not separately re-probed |
| FW-03 native semantics | **ACCEPT (scoped)** | M-2; versioned wire contracts, protocol major 3 |
| FW-04 richer evidence | **ACCEPT (scoped)** | import2 registry; runtime/test/history do not become static Coverage |
| FW-05 delta gate | **ACCEPT (scoped)** | separate audit gate participation retained |
| **FW-06 determinism** | **CHANGES_REQUIRED** | NEW-MUST-1 — two conforming implementations mint different `proof2`/`run2` for identical source; this row is the exact property violated |
| FW-07 coherent workflow | **ACCEPT (scoped)** | bounded step DAG and disjoint derivation DAG retained |
| FW-08 omissions | **ACCEPT (scoped)** | examined-vs-resolution completeness enforced by RC-2, not asserted |
| FW-09 candidate→inspect→review | **ACCEPT (scoped)** | closed advisory artifacts; stale-reference refusal |
| FW-10 repair evidence | **ACCEPT (scoped)** | separate apply consent; guarded journals |
| FW-11 weakened safeguards/metric redistribution | **ACCEPT (scoped)** | architecture 13 §6 restrictions remain binding |
| FW-12 bounded review | **ACCEPT (scoped)** | explicit truncation/membership; no completeness claim |
| FW-13 common registry | **ACCEPT (scoped)** | registry/enum exact equality; unknown records refuse |
| FW-14 real configuration corpus | **ACCEPT (scoped)** | correctly still an implementation-harness obligation; synthetic cases explicitly disclaimed as not that corpus |
| FW-15 policy authoring/test | **ACCEPT (scoped)** | closed DSL; deterministic suites; M-3 ordering now closed |

---

## 7. Inherited residual disposition (DR-011-R01…R16, DR-001…011)

`inherited-residuals.proposed.md` and `inherited-row-sources.proposed.json` describe
**prospective** successors. They award nothing, and I did not treat any as
discharged.

| Residual | Disposition |
|---|---|
| R01 FACT-PLANE | **ACCEPT (scoped)** — product view/fact/Coverage joins supply the declared surface; old D9-v1.6 checker not elevated |
| R02 FACT-IDENTITY | **ACCEPT (scoped)** — `fact2`/`finding-key2` wrappers current; no plugin ecosystem inferred |
| R03 C2 | **ACCEPT (scoped)** — the C-2 `subjectScopeCommitment` deferral is now genuinely picked up (M-1); the retained artifact and its "SHAPE ONLY" note are untouched and remain a non-recipe |
| R04 DELIVERY | **ACCEPT (scoped)** — CVE1 constructible (7/7 vectors); historical OBS-1/version skew retains original standing |
| R05 Rust PC-7 | **ACCEPT (scoped)** — protocol major 3; rejected base-v2 remains rejected |
| R06 EVIDENCE | **CHANGES_REQUIRED** — identity-and-evidence is the Phase-1A owning packet, and NEW-MUST-1 lands inside its proof/witness closure |
| R07 RETENTION | **ACCEPT (scoped)** — CD-RT-5 and applied v28 posture preserved; old unreviewed checker still unreviewed |
| R08 D9 | **ACCEPT (scoped)** — S-1 row plus closed `StepTermination`; branch contract verified |
| R09 R-1 | **ACCEPT (scoped)** — semantic IDs exclude RequestId/ExecutionId/receipts/paths |
| R10 blind consumer-B | **OPEN — not closable here.** The row requires a fresh implementer litmus after the final decisions. `consumer-b.v1` ran against the v5-era kit and returned CHANGES_REQUIRED; a **new** blind consumer on an accepted successor is required, with `resolved-inputs.v2.json` included and the two governance records excluded |
| R11 OPERABILITY G19 | **ACCEPT (scoped)** — real fsync/process-death/storage measurements correctly remain release gates, not design prerequisites |
| R12 EVALUATION PROOF | **CHANGES_REQUIRED** — `evaluation-residual-dispositions.proposed.json` disposes each RES/NB/escape individually, but the proof closure itself carries NEW-MUST-1 |
| R13 VERSIONING | **ACCEPT (scoped)** — old v14/v15/v16 rejection and v17 unreviewed standing unchanged |
| R14 CFG-6/TM | **ACCEPT (scoped)** — restored CFG-6 root preserved; not reopened on the stale v2 note |
| R15 trusted request context | **ACCEPT (scoped)** — hash equality grants no permission; verified in the claimant-digest attacks (M-1) |
| R16 product authority | **ACCEPT (scoped)** — D-367/D-370/D-371 scope preserved; no third-party ecosystem opened; CD-RT-5 binding |

Parent rows DR-001…DR-011: their product successor obligations are stated and
consistent with the bytes I measured. **DR-002/DR-004/DR-006** inherit
CHANGES_REQUIRED through R06/R12 (identity/proof closure). The remainder are
**ACCEPT (scoped)** as prospective dispositions only — none is discharged by this
review, and DR-012 remains release qualification.

---

## 8. Scoped review-owner dispositions DR-201…DR-205 (new, current scope)

These rows were `ACCEPTED` on 2026-08-13 at old digests. The register itself records
them as reopened for the current scope ("The 28 affected V2 rows and DR-201–205 …
OPEN for full-product integration; historical acceptance is retained, not counted as
review of changed scope"). I award **no** blanket extension; each disposition below
is new and scoped to the v6 bytes.

| Row | New scoped disposition | Selectors and reasons |
|---|---|---|
| **DR-201** semantic correctness | **CHANGES_REQUIRED** | Its scope expressly includes *parked recipes*. `identity-and-evidence.md` §3 auxiliary-digest paragraph parks the producing rules for `identity-schemas.v2.json#/$defs/predicate-witness/properties/programPredicateDigest`, `#/$defs/finding/properties/parameterDigest` and `#/$defs/execution-plan/properties/stages/items/stageSpecDigest`, and no closed record exists for the predicate program, the finding parameter payload or the stage spec. Demonstrated: `proof2:edba615b…` vs `proof2:67d4359b…` for identical inputs. Other axes (happy-path/pre-admission branches, Run-versus-command finalization, post-commit output failure) are unblurred in these bytes |
| **DR-202** delivery/operations | **ACCEPT (scoped)** | Generation coexistence, mandatory storage, recovery, repair, permissions, state classes and loader TCB are stated in `identity-and-evidence.md` §5 and `security-and-lifecycle.md`; `evidence.regeneration-mismatch` is registered and typed with sealed-Run preservation (S-4); commit ordering and the availability/assurance split are explicit. Gate evidence is carried in `qualification-gates.proposed.json` with all 32 rows `qualified: false` — correctly undemonstrated rather than overclaimed |
| **DR-203** prototype lessons | **ACCEPT (scoped, partial — the split remains honest)** | `prototype-evidence-reference.md` and `05-v1-to-v2-relationship.md` are in the subject; FW-14 continues to state plainly that no digest-pinned corpus, matrix or thresholds exist and that synthetic design cases are **not** that corpus. Language-quality claims stay blocked by DR-118/DR-G13 by design. No new gap; the honesty of the split is the acceptance basis, not a claim of completeness |
| **DR-204** V1/coop invariant coverage | **ACCEPT (scoped)** | Exact-selector/digest posture holds under my own re-measurement: manifest `cb345532…` exact, 1610/1610 files, 0 undeclared, 31/31 historical files unchanged, byte-identical report regeneration. No newest-head heuristic or baseline-only standing appears in the v6 records; `readinessChanged: false` and every gate/disposition is explicitly pending. Carries **NEW-SHOULD-2** (crosswalk `review` blocks still cite the v1 manifest `e7403b70…`) — stale provenance, but honestly labelled and promoting nothing |
| **DR-205** small-core/components | **ACCEPT (scoped)** | `02-distribution-and-components.md` and `10-mvp-and-future-scope.md` are in the subject; core/TCB/product boundaries, storage, packaging and fault containment are stated; the component selection is explicitly first-party bounded and opens no third-party plugin ecosystem (R16); P-1/P-2/G3 implications are carried in D-372. DR-128 remains post-MVP. No new gap in this row's scope |

**Condition 3 accounting:** 4 of 5 `ACCEPT (scoped)`, DR-201 `CHANGES_REQUIRED`.
Condition 3 does **not** re-discharge on the current scope until DR-201 clears.

---

## 9. Scope, limitations and what this review does not do

- Every custody, signature, clock, lease, provider-protocol, OS and filesystem
  observation in the subject and in my probes is a **synthetic TCB assumption**, not
  native enforcement proof and not product qualification. Real compiler, OS, crypto,
  SQLite, fsync, process-death and end-to-end measurements remain mandatory
  **release gates**; they are correctly *not* pre-implementation design
  prerequisites, and I did not treat any as a design gap.
- Passing 424 + 456 + 132 + 1253 + 352 source-pinned checks does **not** prove the
  absence of gaps. NEW-MUST-1 is invisible to all of them because one
  implementation is self-consistent with itself. I found it by sweeping for the M-1
  *defect class* rather than re-running the suites.
- I did not exercise: the provider wire protocol (native §9), clone equivalence
  modes (§6), framework recognition (§8), the Rust dependency-source/prepared-output
  paths (§3), the security trust-time and lease/migration state machines beyond
  their sweeps, the G13 report gate, or HTML/agent rendering. I read them for
  ownership and consistency only, and my AR-07/FW-02 dispositions rest on the suites
  rather than on independent probes.
- My probes are one reading of the contracts. Where I chose, I disclosed. Retained
  sources and results are listed in §10.
- Scope held constant: D-371 remains **one complete intended product implemented in
  stages** — common host/evidence/workflows, TS/JS/Rust, four macOS/Linux machine
  IDs, no untrusted ecosystem and no implicit repository execution. I found nothing
  in v6 that widens or narrows it.
- The central, navigation and application drafts are **deliberately unapplied**
  pending design + blind + complete final-application review. I read them as pending
  acts and awarded no grade on their behalf. `readinessChanged: false`;
  **condition 5 NOT MET**.
- This review is not acceptance of any successor. A fresh blind consumer on an
  accepted successor, and a separate complete final-application review, remain
  **later acts not performed by me**.

---

## 10. Verdict

**CHANGES_REQUIRED.**

The v6 delta is genuine and, on the evidence I gathered, unusually well made. All
five blind MUSTs and all six SHOULDs are resolved, and the four advisories are
addressed rather than deflected. The strongest evidence is not that the suites pass
— they do, byte-identically, at every expected count — but that the corrections
survive attacks the subject's own cases do not run: I reproduced the M-1 commitment
from prose alone with an independent encoder and `H` frame; I broke the TypeScript
context seven different ways and got seven precise typed refusals; I built CVE1 from
its specification and round-tripped all seven published vectors byte-identically,
turning a verify-only recipe into a constructible one; the M-3 counterexample now
admits in exactly one order; and the M-4 resolver converges two input spellings to
one digest while keeping absent and empty `entryPoints` properly distinct. The
public detail vocabulary is closed at 282 = 282 with no wildcard and no sub-detail
leakage. Custody is exact before and after.

It is not yet complete. The same defect class the blind consumer found in M-1 — a
required, identity-bearing field whose producing recipe exists nowhere — is still
present in three more places. `programPredicateDigest`, `parameterDigest` and
`stageSpecDigest` are required fields that reach `proof2`, `finding2` and
`exec-plan2`, and the records they digest are not defined anywhere in the schema
bundle. I demonstrated two conforming readings producing different `proof2` for
identical source. v6 gave the array-ordering law an explicit closing default and did
not give the digest law the same treatment; that asymmetry is the whole finding, and
the fix is the one v6 already proved it knows how to write.

That is a narrow, mechanical gap in an otherwise closing design — a missing
paragraph and three missing record definitions, not a rethink. But it is a required
gap that would force implementer invention and diverge a committed identity, so the
verdict is CHANGES_REQUIRED rather than ACCEPT. I would expect a corrected successor
to clear a re-review.

Nothing here awards readiness, qualifies a platform, or authorizes implementation.

---

### Retained artifacts

```
probes/p1_order_annotations.py   x-opensip-order coverage across all 17 schema bundles
probes/p2_m3_policy_order.py     M-3 schema-valid two-rule divergence + encoder heuristic controls
probes/p3_m4_resolved_config.py  M-4 via the real resolver
probes/p3b.json                  M-4 propagation into snapshot2/plan2
probes/p4_m1_subject_scope.py    M-1 prose-only oracle + boundary attacks + acyclicity
probes/p5_m2_ts_context.py       M-2 mutations, A-1/A-2, Plan digest set semantics
probes/p5b.json                  M-2 seven foreign-closure attacks
probes/p6.json                   M-5 typed host emission, alias, wildcard and sub-detail controls
probes/p7.json, p7b.json         S-2 pattern discipline; S-3 inventory duplicate refusal
probes/p8_s5_cve1.py             S-5 CVE1 decoder+encoder, 7/7 vectors byte-identical
probes/p9_recipe_sweep.py        digest-field recipe sweep (54 fields, with controls)
probes/p10_digest_recipe_gap.py  NEW-MUST-1 divergence counterexample
runs/{foundation,security,workflows,integration}.json   re-run reports (byte-identical to pinned)
review.json                      machine-readable verdict and dispositions
```
