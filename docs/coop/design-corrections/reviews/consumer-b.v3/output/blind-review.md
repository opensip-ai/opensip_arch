# Blind consumer-B reconstruction — OpenSIP DR-011-R10

**Verdict: CHANGES_REQUIRED.**

**Reviewer standing.** Fresh blind session. I authored none of this design and had
no prior review context. My only inputs were the 45 files in
`consumer-b.v3/subject`. I read no author reference implementation, no fixture,
golden, report or prior review, and no other `/tmp/opensip-design-corrections`
directory. Where a normative document embedded an example value I treated it as
illustration and computed my own vector instead. Nothing here is a readiness
grade, an acceptance, an implementation authorization, or a claim of product
qualification.

---

## 1. Input custody

All 45 manifest entries verify: exact SHA-256 match and exact byte length for
every file, nothing missing, nothing unlisted present on disk
(`work/verify_manifest.py`, `work/manifest-verification.txt`).

The manifest asserts `parentSubjectSha256 =
fc124cc7d487f7f6fcc97665255574273b03fe1f09e6b70c3246feedf1678beb`. That is a
claim about a parent tree I was not given, so I did not verify it and do not
repeat it as established. What I verified is per-file custody of this subset.
The manifest's own bytes hash to
`7d5ea7a3b74db991ded23504f6f6633d85c2bbd719b9bcc6da2de953a4efb961`.

The index is explicit that readiness and correction records are governance
standing, not semantic recipes, and are deliberately excluded. I confirmed that
by reconstruction rather than by assertion: I never needed a verdict, a grade or
a review narrative to build a Run. Historical review prose inside inherited
normative documents (the `native-evidence.md` standing block, the security
`Joint correction provenance` section, `delivery.v4`'s objection registers) is
provenance only; I did not follow a single link out of the kit.

---

## 2. What I built

I wrote my own canonicalizer and identity helper directly from prose —
identity-and-evidence §§2–3 for `C` and `H`, admission-and-qualification §1 for
lexical and numeric admission, `resolved-inputs.v2#planIdContract.canonicalValueEncoding`
for CVE1, `delivery.v4` operation 17 for the capability-manifest gates and
recipe, and `fact-identity-policy.v2#canonicalisationSchema` for the framed body
preimage. Then I built five complete Run descriptor graphs and 143 vectors, and
validated 214 descriptors against the kit's own closed schemas through a pinned
local registry with no network.

**Results: 143 vectors, 0 failing. 214 schema checks, 0 invalid. 5 complete
Run graphs. 89 retained blobs, 108 retained H preimage frames, 70 retained
canonical records.** Ten of the vectors are *findings* — vectors whose purpose
was to record a design gap — and they are counted separately from failures.

| Graph | run2 | Verdict | What it exercises |
|---|---|---|---|
| `RUN-TS` | `665153ac…a52eb1` | pass | four TypeScript contexts under one Plan |
| `RUN-RUST-2021` | `fdeafd4a…3a63ca` | fail | mixed-edition workspace, lib target selected |
| `RUN-RUST-2015` | `64834bd0…8a6272` | fail | same file, test target at an overriding edition |
| `RUN-RUST-2021-NARROW` | `8856505f…858373` | fail | selection changes, dialect does not |
| `RUN-RUST-PARTIAL` | `a0533553…f33b51` | indeterminate | partial ownership, empty clone view |

### 2.1 The chain, and where each decision lives

Zero-config discovery is security's, not native's. Security S3 walks upward from
the launch directory over `O_NOFOLLOW` lstat/ACL custody, selects the root by
`config > vcs-default > cwd-default` (a nested `opensip.json` is a deliberate
boundary that wins for launches inside it), and exports a closed
`AdmittedBoundaryInventoryV1`. Native §1.4 U-8 consumes that record unchanged —
it never re-derives a boundary from caller input — and produces per-language,
per-program `WorkspaceUnitV2` units that may share a root. Both instruments
consume the one shared pruning rule, by exact path segment. That separation is
clean and I could reconstruct it without guessing: security owns *authority*,
native owns *language unit existence*, and the two are allowed to disagree about
the same directory (an explicit root without a language marker is admitted for
custody with a warning and refused by the language layer as `CONFIG.INVALID`).

Typed configuration is admission §1.1's: compiled authenticated defaults, then
global, project, interactive local and flags, arrays replacing atomically and
records merging by named field. The resolved semantic record always carries all
five sections, with `{}` for an empty one, and always a complete
`analysis.budget`. `resolvedConfigDigest` is raw SHA-256 of its canonical bytes.
The distinction that matters and that the contract gets right: absent
`entryPoints` means automatic recognition, explicit `[]` means deliberate empty
intent, and `[]` for `workspaceRoots` is refused rather than silently read as
either.

Then `snapshot2` over ProjectId, sorted inventory, config, scope and VCS digests;
the invocation/step/attempt lifecycle in operational identities that never enter
a content identity; native contexts and universes bound before PlanId and
re-admitted at Run closure over retained bytes alone; `plan2`; facts, Coverage
and `view2`; the pure evaluator and `proof2`; `evidence2`, `seal2`, `run2`; the
four-step commit order; and the separate monotonic availability generation.

The semantic/operational split is the strongest thing in this design and I
verified it rather than accepting it. Two attempts with different RequestId,
ExecutionId, wall clock and PID mint the same `run2` (vector B-6); changing one
semantic field of the Run moves it (B-7); every semantic field of the snapshot
moves `snapshot2` (B-5). Operational *authority* is likewise outside identity:
`RepoExecutionGrantV2` and `RepairApplyAuthorizationV1` are referenced
operationally and only their semantic projection — principal kind, closure,
owner-source digest, operation set, scope — enters the Plan. And the
mutation/analysis split is enforced by the step kind: only `analysis` and
`verify` seal or link a `run2`; `comparison`, `query`, `render`, `import`,
`repair-preview`, `repair-apply`, `test-execution`, `native-preparation`,
`mutation`, `export-delivery` and `doctor` mint none.

### 2.2 Exact admission and the two encoders

The lexical gate is where most of the value is, and it is well specified.
`1.0`, `1e0`, `-0`, `NaN`, out-of-range integers, duplicate keys and lone
surrogates all refuse *before* deserialization loses the evidence (A-2…A-9).
`true` and `1` encode differently (A-7). `C` preserves array order and repeats
and never sorts (A-14). Keys sort by UTF-8 bytes with non-BMP keys last (A-12).
The escaping law reproduces exactly: quote and backslash escaped, the five short
escapes, lowercase `\u00xx` for the other C0 controls, slash unescaped, and
U+007F and U+2028 left as raw scalars (A-10). No Unicode normalization, so NFC
and NFD spellings are two identities (A-11). Container depth counts containers
only, so a 32-deep array admits and a 33-deep one refuses (A-13).

The `x-opensip-order` vocabulary is genuinely closed and I implemented it as an
*admission* check rather than a sort: an unknown annotation refuses (A-15), a
`canonical-set` array that is unsorted or has a duplicate refuses before hashing
(A-15b/c), `canonical-order` admits equal neighbours (A-15d), and `sequence`
retains grammar order including repeated tokens (A-15e). That last one is not
decoration — the repeated `extends` base in my custom TypeScript config and the
declaration-signature discriminator both depend on it.

The two encoders are correctly kept apart. `C` admits a non-NFC string; CVE1
refuses it (C-8, C-8b). CVE1 is total on `true` and on `"1"`, which is exactly
why ADM-TYPE has to be a gate *before* encoding rather than a property of the
encoder — I reproduced both halves (C-4, C-4b, C-4c). All four capability-manifest
gates fire: closure on the two nested records (C-5), a platform-id case variant
and a rung borrowed from another relation (C-6, C-6b), and a committed manifest
out of declared order, rejected and never sorted into shape (C-7, C-7b). My own
manifest yields `capabilityManifestId =
d129952fec589bdc3197f8671567351dc87d4224a8cc2abe53d7ae0fa05989f6` over 1020
committed CVE1 bytes, computed twice by two independently spelled paths, and the
raw artifact digest of those same bytes is a different value (C-3) — which is the
`derived` retention working as designed.

### 2.3 The digest law

The four-representation, four-retention closing law is the best-engineered part
of the identity contract, and it survives adversarial probing. A raw canonical
payload offered where a frame is required fails the prefix (B-3b, E-20); a frame
with a tampered declared length fails parsing (B-4); a well-formed frame
round-trips and re-canonicalizes to itself (B-4b); `SHA256(C(X))` is never
`H(D,X)` (B-3, E-21); and the same descriptor under two domains gives two
identities (B-2). An unregistered H domain in an otherwise well-formed frame
refuses (E-22).

The `CargoConfigProjectionV2` triple is the sharpest instance and I built all
three values to show they are three distinct things: the raw digest of the
projected `.cargo/config.toml` *file*
(`fff0d3dc…4520b`), the 64-hex suffix of
`H("native.cargo-config-projection.v2", record)` (`e20db99d…7f8fc7`), and the raw
SHA-256 of the canonical *record*, which is neither (`81b713fc…75da58`). The
contract explicitly says the third is not the answer, and a reader who assumed
"digest of the record" would have produced it (D-22).

### 2.4 The TypeScript configuration graph

I built four contexts under one Plan, which the contract says is ordinary rather
than exceptional, and the closure requirement held: the retained context frame
set equals `plan.nativeContextDigests` exactly, and every universe's own
`nativeContextId` is `sha256:` plus a Plan member (D-1, D-3).

`configOrigin` is *derived* from the retained `TypeScriptConfigGraphV1`, never
asserted, and my four universes cover all three derived values (D-4). The
explicitly selected custom-named config is a node of kind `other` whose
`extendsResolved` is `["custom/config/base.x.json", "custom/config/base.y.json",
"custom/config/base.x.json"]` — three ordered edges with the first base repeated
last, retained because that array is a `sequence` and later entries win. It
derives `configOrigin: tsconfig` (D-5). The jsconfig project inherits
`jsproj/shared/common-base.json`, a differently named shared base of kind
`other`, and still derives `configOrigin: jsconfig` (D-6). That the entry node's
kind alone decides, and not the node set, is stated and is what makes both cases
representable.

The `node_modules` case is the one an earlier draft could not express, and
`ResolvedNodeModulesLayoutV1` fixes it properly. My layout has three rows
including a pnpm-style store link whose `realPath` is itself an `installPath` of
the same layout — a constraint I checked rather than assumed — and none of the
three is a snapshot inventory row, because the shared discovery rule prunes
`node_modules` by segment (D-7). `nodeModulesInReadSet` is exactly
`nodeModulesLayoutDigest is not null`, and the synthesized project takes the
other branch with every bare specifier unresolved (D-8).

### 2.5 Clone body identity

This is the part I probed hardest, because it is where the design does the most
work.

`languageVersion` is the raw 32 bytes of `SHA-256(C(body-language-version))`, and
`body-language-version` has `derived` retention: no free fields, every field
copied from a named path in an already-admitted retained record, recomputed at
closure. I rebuilt it for both languages from the universe's own
`nativeContextId` and confirmed the fixed-width argument independently: my
21-crate edition map canonicalizes to 391 bytes against a `u8` component maximum
of 255, so a map-valued component genuinely is not representable (D-16). The
contract's own illustration says 723 bytes for 21 crates; my number differs
because crate names differ, which is why I computed mine rather than quoting
theirs. The conclusion holds either way.

**Body language is not provider identity.** I put byte-identical 19-byte bodies
in `app/src/one.ts` and `app/src/legacy.js`, read them through *one* TypeScript
engine universe, and got two identities:
`sha256:8b45c222…420a493` (typescript, `{sourceVariant: "ts"}`) and
`sha256:75ebe15b…4d0d3b` (javascript, `{sourceVariant: "js"}`) (D-9, D-10). The
`.d.ts`-is-never-`.ts` longest-suffix rule holds and an unlisted suffix refuses
rather than folding into a neighbour (E-6, E-6b).

**The Rust dialect law is correct and I could not break it.** The mixed-edition
workspace has `cb-core` at package default 2021 with a `test` target declaring
2015, `cb-legacy` at 2015 under a marker directory containing `#`, and `cb-tools`
at 2024. `crates/core/src/shared.rs` is owned by both `cb-core` targets. Under
the selection naming the lib target the effective edition is 2021
(`sha256:423c20c1…d1cdb8`); under the selection naming the test target it is 2015
(`sha256:fbc211a3…1250ff`); the two are different `sourceUniverse` values and
therefore two analyses, not two readings of one (D-13, D-14). Narrowing the
selection from three units to two without touching the owning target leaves the
body identity byte-identical while `sourceUniverse` and `run2` both move (D-15) —
which is precisely the stability property the design claims. The `#` marker
directory closes a complete Run and `unitId` re-derives from the published
four-field preimage (D-17), so the withdrawal of the delimiter-joined label was
the right call.

The refusals are total and each has its own cause, in the fixed order: no
committed ownership (E-3), `partial` enumeration refusing before any row is read
(E-2), no row for the path (E-4), a path owned only by unselected targets (E-5),
and selected owners whose effective editions disagree (E-1). A `clones` fact with
two anchors refuses (E-15) — zero would leave the claim unattached and several
would make the L0 recomputation a choice.

At L0 the payload is genuinely recomputable: I retained the frame under its
64-hex suffix, re-hashed it to the claimed `bodyIdentity`, and confirmed the
frame ends in `u32be len || the exact anchor span bytes` taken from the retained
blob (D-11, D-12). That is a real source join, not a custody claim. At L1 what
the design asks for is exact retained preimage custody plus framed-stream
parsing, and it says so — it grades no tokenisation, and I did not pretend
otherwise.

### 2.6 Coverage, subjectScopeCommitment, and the empty clone view

`subjectScopeCommitment` is the identical digest to the `coverage2` scope, in a
different textual spelling, with `subjectCount` equal to the inventory length. I
verified all three equalities for every Coverage record in the TypeScript and
Rust graphs (D-20), and the two provider-lies refuse at the producer boundary: a
narrower examined partition (E-18) and a claimant-chosen commitment (E-19). This
is the one check that catches a worker that examined less than the host
enumerated, and it works because the host builds the scope from its own
enumeration and the provider's value is never an input.

The partial-ownership Run is the case the contract is most careful about and it
reconstructs correctly in shape: no body identity is minted, the clone view is
empty, Coverage reports `coverage: unknown` rather than claiming completeness,
and the seal is `indeterminate` rather than a false pass (D-18). Enumeration
completeness and resolution completeness stay distinct: the one-rung `clones`
relation reports `not-applicable`, which is explicitly not `complete` (D-19). I
did not invent a resolved rung for file facts.

But this is also where the design runs out of vocabulary — see MUST-5.

### 2.7 Imports, mutation keys, terminations

The dependency `import2` is a real registered payload: `DependencySourcePayloadV1`
under `native.import-payload.dependency-source.v1`, validated through the
registry selector, wrapped with six auxiliary raw canonical-record digests and
one H identity (`import2:df766981…c7fab1`). I checked that
`payloadDigest` is raw SHA-256 of the canonical payload and that `importId` alone
is `H("import", wrapper)` (D-24), and my Plan projects `read-import` because it
selects an import — a join I enforced before minting PlanId.

The two mutation keys are genuinely different recipes and I built both: the
generic replay key is the bare 64-hex `H("workflow.mutation-intent", {schemaVersion,
requestId, stepId, projectId, operation})` = `e01c7dd9…c12330`, scoped to one
host-minted request so a different fresh request never deduplicates it; the
repair-apply key is the raw SHA-256 of `C({operation, projectId, repairPlanId,
baseSnapshotId})` = `fe142613…efc4b6`, content-derived and explicitly not an H
identity. Neither equals the other under either recipe.

I wrote sixteen public terminations from the schemas rather than from the
goldens table, and all validate against the closed `StepTermination` branch
contract, including the pinned-purge refusal with its complete three-pin
inventory sorted by `pinId` and the three ordered consequences. The
distinctions the contract insists on are real and schema-enforced: `evidence.purged`
before evaluation is `request-rejected`/exit 2, `evidence.missing` during a
selected operation is `operational-failed`/`HOST.IO_FAILURE`/exit 4, and
successfully admitted partial native inputs are an *authoritative* indeterminate
Run at exit 3 carrying its `coverageId`. A required renderer failing after commit
is `DELIVERY.REQUIRED_FAILED` with the RunId retained and no rewrite of the Run.
Ephemeral `policy-failed` carries `authority: ephemeral` and the schema forbids
it from also carrying a `runId`.

For the audit path I built three comparison results: an empty-result comparison
whose verdict is `indeterminate` purely from a gating rule deficiency with zero
entries (missing evaluation can hide a finding that appears in neither set);
`required-evidence-unavailable`, which gates as `indeterminate-gating-rule`; and
`evidence-availability-changed` on a non-gating rule. All three validate. The
explicit test, preparation and repair authorizations each validate as their own
closed parameter record, with the test step's four effect values copied from the
security truth table.

---

## 3. Required findings

Five MUST issues. Each is a place where two conforming implementations would
disagree on admission, or where a mandated public output has no expressible
value. None is a matter of taste and none is algorithm freedom.

### MUST-1 — the rung ladder is not in the registry that identity §3 names

`identity-and-evidence.md` §3 says `relation-payload-schemas.v2.json`'s
`x-opensip-relation-registry` "carries each relation's selector, universe rule
and rung ladder", and Run closure requires `resolution` to be "a rung of that
relation's ladder". That registry has no `ladder` key. Its `rungs` member is a
per-rung *field-rule* table and is `{}` for eight of thirteen relations: `file`,
`package`, `vcs-change`, `declares`, `literal`, `control-flow`, `reachability`
and `clones`. Read literally, no `file` fact and no `clones` fact can ever close
a Run — which would void the entire product.

The values do exist in the kit, and they are unambiguous:
`native/capability-manifest-domains.v2.json#/registries/RELATION-LADDER-DOMAIN-V2/ladders`
publishes all thirteen and they match the inherited `fact-plane.v1` ladders
exactly (F-4b). But that registry declares its `boundPositions` as
`ProviderCapability.relations value` only, so it is bound to the capability
manifest, not to `fact2.resolution`. The contract's own rule applies: an
unresolved overlap is a design defect, never reviewer discretion.

I proceeded under the stated assumption that the ladder is that value. Without
it none of my five graphs is constructible.

### MUST-2 — `minResolution` has two closed vocabularies and no mapping

`PolicyDocumentV1`'s `Atom.minResolution` is a `Resolution`:
`syntax | resolved | type | external`. `RequirementV2.minResolution` is a `Rung`,
and `fact2.resolution` is a ladder rung. The two enums share zero members, and
nothing in the kit maps one onto the other.

The evaluator must decide whether an admitted fact meets an atom's minimum
resolution. Whether `resolved` is satisfied by `resolved-target`, by
`resolved-binding`, by `checked`, or by all of them is a public semantic decision
that changes which findings a policy emits and therefore which verdicts a gate
produces. Two conforming implementations disagree on the same Plan. I avoided the
problem by using `syntax` everywhere, where all candidate readings agree; a
policy needing `resolved` or `type` is not reconstructible.

### MUST-3 — `syntax-only` has supported fact cells and no admissible universe

`native-capability-matrix.v2.json` gives mode `syntax-only` `SUPPORTED-DESIGN`
for capability `syntax` (declares/literal/control-flow at `syntactic`) and for
`clones-fact` (clones at `normalized-body-hash`). §1.2 gives that mode
`Universe: none`. But `fact2.sourceUniverse`, `fact2.targetUniverse` and both
`subject-scope` universe fields are **required, non-nullable** h-identities of the
`native-semantic-universe` domain set, which registers exactly two members —
TypeScript and Rust. There is no null branch and no third domain.

So an advertised capability is unrepresentable in the identity graph. The same
gap reaches `file` facts in any repository with no TypeScript or Rust unit at
all, since `file`, `package` and `vcs-change` have no capability row either
(ADV-3). I did not build this shape, because doing so would require inventing a
domain or a null branch on a required field.

### MUST-4 — `ScopeDocumentV1` must be an analysis-spec parameter that the closed registry forbids

`comparison-result.schema.json#/$defs/EvaluationContext` states that its
`scopeDigest` is the raw SHA-256 of `ScopeDocumentV1`, "the workflow glob
scope-policy document, **bound as an analysis-spec parameter**". The identity
payload registry's `parameter` class has exactly one row —
`foundation/import-source-context.schema.json` — and the registry law says a key
with no row refuses, with no default and no caller-selected schema.

So such a parameter refuses at Plan admission, and the comparison contract's own
scope axis (E2→E3) cannot be populated. One contract requires a binding a sibling
contract's closed registry forbids.

### MUST-5 — the partial-ownership disclosure has no publishable typed cause

Both the identity contract and native §11 mandate a specific public behaviour:
under partial ownership the clones scope mints no body identity, "its Coverage
reports the incompleteness", and the predicate and seal are indeterminate. Three
refusable states are named — ownership absent, enumeration partial, owners
ambiguous — and none of them has a `NativeCause` member. The §10 row that would
carry them enumerates nine causes, all about dependency sources, generated files,
lockfiles, program units, `node_modules` and stripped flags.

The contract mandates a disclosure the closed vocabulary cannot express. I used
`deficiency: input-closure-incomplete` with `nativeCause: null` — schema-valid,
because `nativeCause` is nullable, but the disclosure then carries no cause at
all, and every implementer would invent a different pairing, which would then
differ across the CLI/JSON/SARIF/HTML/agent parity fields.

---

## 4. SHOULD issues

**SHOULD-1 — mirrors declare different owning orders for the same digest
preimage.** `identity#/$defs/import.omissions` declares `canonical-set`; the
workflow `ImportWrapperV2.omissions`, whose description claims to be an exact
mirror, declares `sequence`. Same for every array of the foundation
`scope-descriptor` versus `ImportScopeDescriptor`. Under `canonical-set` the
array must be strictly ascending; under `sequence` any order is admitted. So the
same bytes are admissible in one unit and refused in the other, while both
records name the same digest preimage — and the byte-identical-wrapper claim in
workflows §12 fails for exactly those inputs. Identity §3's "No caller may elect
a different order for one schema" is the rule being broken, by the schemas
themselves.

**SHOULD-2 — `import.blobs` cardinality diverges.** The foundation record has no
`minItems` and `maxItems 100000`; the workflow mirror has `minItems 1` and
`maxItems 4096`. An import with zero blobs, or with 5000, is admissible in one
unit only.

**SHOULD-3 — `ResolvedNodeModulesLayoutV1.contentSha256` is described twice,
oppositely.** The schema says "as inventoried in the snapshot"; native §2.2 says
the rows "are not snapshot inventory rows and must not be", because the shared
rule prunes `node_modules` by segment. The machine-readable registry resolves it
toward the prose (a `blobJoin`, not a `snapshotJoin`), and that is what I built —
but an implementer reading only the schema would add `node_modules` paths to the
snapshot inventory and contradict the discovery rule.

---

## 5. Non-blocking advisories

- **ADV-1** A schema-valid strict *subset* of the pin inventory validates against
  `PinnedPurgeDisclosure`. Completeness is a host obligation observed under the
  exclusive purge lease. The contract says this itself; recorded as a limitation
  of the closed schema, not a defect.
- **ADV-2** `EnforcementValue` admits `ENFORCED-AT-HOST-BROKER` for a test step's
  network effect; `TEST.CONFINEMENT_CLAIM_REFUSED` is a host-side join against
  `permission-truth-tables.v9`. Correct by design — but schema validity must not
  be read as an enforcement claim.
- **ADV-3** `file`, `package` and `vcs-change` appear in the relation registry and
  in the capability-manifest relation domain but in no matrix capability row, so
  the matrix does not say which component produces them.
- **ADV-4** The "723 bytes for twenty-one crates" illustration is not reproducible
  from the published grammar (my own 21-crate map is 391 canonical bytes). The
  design conclusion holds under my measurement; the number should not be read as
  an oracle.

---

## 6. What required invention, and what did not

Two things required a stated assumption and one required an invention:

- The **ladder** for the eight one-rung relations: *assumed*, not invented — the
  values are in the kit and agree with the inherited registry (MUST-1).
- The **`examinedExhaustive` reading** under partial ownership: *chosen*, because
  `ViewEntryV3` has no other field in which a clones scope can say its ownership
  enumeration did not finish (MUST-5).
- The **deficiency/cause pairing** for that same case: *invented*, because no
  admissible pairing exists (MUST-5).

Two things I refused to invent and reported instead: a `syntax-only` universe
(MUST-3) and a `Resolution`-to-rung mapping (MUST-2).

Against that, several things that *look* like gaps are correctly-scoped
implementation freedom and I want to say so explicitly, because a reviewer
counting open questions would otherwise miscount them:

- Query planning is explicitly an optimization that must agree with a retained
  full scan. Freedom, with a stated oracle.
- The L1–L3 normalizer: the contract requires retained preimage custody plus the
  framed-identity check, and explicitly declines to grade tokenisation.
  `normalisationVersion` pins whatever specification bytes are used, so two
  levels are two facts and never one fact computed differently. The absence of
  level specifications from this kit is a scoped deferral to FACT-IDENTITY, not a
  missing public contract.
- Near-clone grouping, cache eviction, provider process management: all
  implementation.
- SQLite WAL settings, fsync ordering, process-death and ACL race handling: named
  as qualification obligations, not design alternatives. Correctly placed.

---

## 7. Substantive assessment

This is a strong design and the reconstruction was mostly a pleasure rather than
a fight. The parts that usually rot — canonical encoding, digest representation,
what is semantic versus operational — are closed here in a way I could not
subvert. The closing digest law is the standout: by admitting *no* default it
makes an unannotated 64-hex field refuse rather than silently inherit a plausible
rule, which is genuinely stronger than the array law it is modelled on, and it
held against every confusion I tried in both directions. The
`subjectScopeCommitment` recipe is the right shape — one preimage, one digest,
two spellings — and the producer-boundary check catches the one lie (a narrower
examined partition) that nothing else would catch. The Rust dialect law is the
most careful piece of work in the kit: putting the selection *inside* the record
whose identity the universe names is what makes "one file at two editions" a pair
of honest analyses instead of an ambiguity, and the distinction it draws between
selected scope and incomplete enumeration — a selection leaves a trace in the
identity, an omission does not — is exactly right and is the kind of thing that
is usually blurred.

The five MUST issues are not of that quality, and none is a deep design problem.
Four are *closure* failures at seams between documents that individually get
their own side right: a registry that says it carries a ladder and does not; a
field name reused across two closed vocabularies with no bridge; a language mode
the matrix advertises and the identity graph cannot represent; a document one
contract requires as a parameter and another's closed list excludes. The fifth is
a vocabulary that ran one enum member short of the behaviour its own prose
mandates. All five are the same failure mode as the defects this revision already
fixed by hand — `M-1`/`M-2` on `subjectScopeCommitment` and the TypeScript
context, the withdrawn payload-schema rule, the withdrawn delimiter label — which
suggests the closure discipline is working but has not yet been run mechanically
across *every* cross-document reference. Each of the five is a small, local,
mechanical edit; none needs a redesign.

That is why the verdict is CHANGES_REQUIRED rather than anything sharper. The
design is reconstructable end to end by a blind implementer — I did it, five
times, with 143 vectors and 214 schema validations and no author oracle — but not
*without* an assumption on MUST-1 and an invention on MUST-5, and not at all for
the shapes blocked by MUST-2, MUST-3 and MUST-4. An implementer who hit any of
those five would have to choose, and two implementers choosing independently
would produce different public output from the same inputs. That is the exact
condition these contracts say must not survive review.

---

## 8. Limitations

Every OS, compiler, provider, cryptographic and SQLite observation in this
reconstruction is a synthetic assumption, stated as such in the code. Nothing
here measures a real toolchain, proves confinement, or qualifies a platform, a
normalizer, an enumerator or a storage carrier. Synthetic TCB observations are
assumptions, never native enforcement proof — and real measurement is future
qualification work, which I am not treating as a defect of a design document.

I built descriptor graphs and admission logic, not a product. Passing my own
reconstruction shows the design is constructible under *my* reading; it does not
show my reading is the author's. Schema validation establishes shape conformance
only — the joins the prose requires (snapshot joins, closure joins, frame
re-admission, citation closure, budget agreement, universe binding) I implemented
myself from prose, and that implementation is my reading too.

I did not verify the claimed parent subject hash, which was not derivable from
this kit. I did not construct a `syntax-only` Run and I avoided any policy
requiring a resolved or type minimum resolution; both omissions are reported
above rather than worked around.

This review grants no readiness grade, no acceptance, no implementation
authorization, and makes no claim of product qualification.

---

## 9. Artifacts

| File | Contents |
|---|---|
| `blind-review.md` | this review |
| `blind-review.json` | structured verdict, `newMustIssues`, `newShouldIssues`, advisories, custody, results |
| `cb-vectors.json` | all 143 vectors, 214 schema checks, five Run graphs, terminations and keys |
| `work/cb_canonical.py` | `C`, exact admission, `H`, order vocabulary, CVE1, manifest gates, body frame, dialect selection — authored from prose |
| `work/cb_vectors.py` | admission, identity-movement and capability-manifest vectors |
| `work/cb_graph.py` | the five Run graph builders and the reconstructed admission joins |
| `work/cb_validate.py` | pinned local schema registry and validator |
| `work/cb_report.py` | driver: graph vectors, negatives, mirror probes, terminations, comparison and authorization instances |
| `work/verify_manifest.py`, `work/manifest-verification.txt` | input custody verification and its output |
