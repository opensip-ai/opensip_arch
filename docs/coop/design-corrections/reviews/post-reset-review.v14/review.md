# Fresh independent design/reference review — frozen candidate v14

**Verdict: ACCEPT** — 0 unresolved MUST, 0 unresolved SHOULD, 2 new advisories.

`subjectManifestSha256 = 45b1e128ca51d114895f3c406cc92575e6efe95051bf319023dc1f3180c2f92c`

I authored none of these bytes. I am not coauthor `77758b10-…`, not prior independent
`4e3fe6be-…`, and not blind consumer `878e4b39-…`. This is a design and reference review. It is
not blind reconstructability, not application acceptance, not product qualification, and not
implementation authorization.

---

## 1. Custody, before and after

| | Declared | Measured |
|---|---|---|
| Manifest SHA256 | `45b1e128…0c2f92c` | **matches exactly** |
| Files | 6047 | 6047 |
| Total bytes | 373,681,736 | 373,681,736 |
| Hash mismatches | — | 0 |
| Length mismatches | — | 0 |
| Undeclared files | — | 0 |
| Symlinks / non-regular | — | 0 |

Verified **before** any reading and again **after** all work, with identical results
(`evidence/custody-before.json`, `evidence/custody-after.json`). Every declared file's SHA256 and
byte length was recomputed and the tree walked independently for undeclared entries. The frozen
subject and the original repository were never written to; all work including the full disposable
copy lives under `post-reset-review.v14/`.

## 2. The exact delta, recomputed rather than read

From the v13 and v14 manifests directly: **1668 added, 0 removed, 35 modified**. The 1668 added
files are author and root custody records — before-images, blind-input copies, check logs,
handoffs, probe outputs — not new normative surface. The normative change is confined to **12
files**: the five product contracts, `identity-schemas.v2.json`,
`relation-payload-schemas.v2.json`, `native-evidence.schemas.v2.json`,
`native-capability-matrix.v2.json`, `public-detail-registry.v1.json`, `common.schema.json` and
`command-envelope.schema.json`.

Load-bearing files that are **byte-identical**, which bounds what I had to re-examine:
`d9-exit-contract.v1.14.json` (the historical D9 artifact), `permission-truth-tables.v9.json`,
`security-lifecycle.schemas.v1.json`, `policy-document.schema.json`,
`current-source-map.proposed.md`, `inherited-residuals.proposed.md`,
`qualification-gates.proposed.json`, `evaluation-residual-dispositions.proposed.json`.

## 3. Reference commands: reproduced, not accepted

**Pins first.** I verified all **1308** transitive pins across the four pin files *before* running
anything: 0 stale, 0 missing. I did not re-pin. The v11 stale-pin failure is historical and did
not recur.

All six recorded commands reproduce in a disposable full copy:

| Command | Exit | Log vs retained | Result |
|---|---|---|---|
| foundation | 0 | identical | 1099 pins, checks executed |
| security | 0 | identical | 456/456 cases, 10 invariant sweeps |
| native | 0 | identical | 347/347 cases, **matrix cells 66** |
| workflows | 0 | identical | 65 pins |
| workflow-surface | 0 | identical | 1598/1598 checks |
| integration | 0 | identical | 365 passed, 0 failed |

The regenerated reports were **byte-identical** to the committed ones — the full source-copy delta
after all six commands *and* all my probes is **0 added / 0 removed / 0 modified**. There is
therefore no intended-nondeterministic operational field to report, and nothing was normalized
away.

**Check calls versus unique case IDs.** I recounted the identity report myself: **1282 passing
check calls over 1270 distinct IDs**, the 12 extra instances coming from exactly two IDs at seven
instances each, all passing. The candidate's own `identity-check-counts.v14.json` states the same
three numbers. Neither is exhaustive coverage. Foundation's 1630 is the sum across five components
(231 + 1282 + 24 + 28 + 65), and `validation-summary.v1.json` now carries the corrected
`matrixCells: 66`.

## 4. The four Bv4 required findings

I tested each against **actual Run admission and the actual producer boundary**, not isolated
schema fields, and not by re-running the author's own cases. **212 independently authored probe
cases**, every one bound to the exact frozen source SHA256s, all holding.

### CB4-MUST-1 — anchor cardinality and inventory — **RESOLVED** (48 cases)

A closed `anchorLaw` now sits on **every one of the 13 relations**, in three classes: `source-text`
(nine code relations, **min 1**), `body-identity` (`clones`, **exactly 1**), `inventory`
(`file`/`package`/`vcs-change`, **exactly 0**). It runs *before* the relation's snapshot joins, so
the cardinality fault reports as itself.

- **Closed on both ends.** The minimum is per class; the **maximum** for source-text is the shared
  `fact.anchors` bound — `maxItems: 100000`, `uniqueItems` — which I confirmed is still present and
  which the class explicitly declines to *override* with a per-relation ceiling. An earlier
  revision's "no upper bound at all" is named as wrong and corrected.
- **Positive controls each carry their own fact**: zero-anchor `file`/`package`/`vcs-change` facts
  close a Run; anchored `declares`/`references`/`imports`/`calls`/`types`/`reachability`/
  `unresolved-edge` close; a single-anchor `clones` fact closes.
- **Negatives**: every inventory relation refuses a borrowed anchor *and* a self-consistent anchor
  into its own path; every constructible source-text relation refuses unanchored under TypeScript,
  and separately under Rust and syntax — the cross-universe hole the finding implied; `clones`
  refuses at 0 and at 2. A drifted `bodyIdentityJoin.anchorCardinality` refuses with
  `RELATION_ANCHOR_LAW_DRIFT`; a relation with the law removed refuses with
  `RELATION_ANCHOR_LAW_MISSING` rather than defaulting.
- **Raw bytes.** An empty file and arbitrary non-UTF-8 binary are ordinary inventory, including at
  an extensionless path, with no invented UTF-8 decoding — at zero anchors the
  `ANCHOR_SOURCE`/`ANCHOR_RANGE`/`ANCHOR_UTF8` loop never runs. The *same* non-UTF-8 bytes still
  refuse as a code span. Raw digest, byte length, path and snapshot ownership each still refuse a
  wrong claim.
- **Per-universe totality.** The joined case holds: in one view with two **complete**
  `file@enumerated` scopes over `a.ts` in a TypeScript and a syntax universe, the TypeScript fact
  does **not** discharge the syntax scope
  (`COVERAGE_INVENTORY_TOTALITY_OMITS_PATH:file@enumerated:a.ts`); the Run where each scope carries
  its own fact closes. `package` and `vcs-change` are correctly *not* total.
- **Locations preserved.** Nothing reads `fact.anchors` as a finding location, and `finding`,
  `finding-fingerprint`, `proof-bundle` and `predicate-witness` carry no anchor field, so removing
  inventory anchors removes no route and invents none.

*Limits:* `control-flow` and `literal` are covered at registry level only — the candidate's own
fixture has no payload shape for them. Enforcement is relation-generic (one `anchor_law(row, fact)`
call that runs for every fact), but that is an argument from the code path, not an exhibited Run.
The two universe coordinates are verified *jointly* load-bearing; `universeRule: same-only` makes
their independence unreachable for `file`.

### CB4-MUST-2 — native deficiency causes — **RESOLVED** (24 cases)

A closed `x-opensip-deficiency-cause-registry` names, per deficiency, **which existing structured
carrier** holds the cause. It is **total over `DeficiencyV2`**: 9 rows for 9 members, no gap, no
extra.

- **No enum was widened to make this work.** `NativeCause` is still 14, `DeficiencyV2` 9,
  `UnresolvedEdgeKindV1` 16 — byte-compared against v13, identical. The cause column names precise
  structured/nullable carriers rather than claiming a closed enum.
- **Both boundaries.** At the producer boundary (`admit_coverage_result_v3`): a cause without a
  deficiency, a borrowed scalar cause, a relabelled cause, a wrong or null cause for
  `language-tier-unsupported`, an empty `derivationKinds`, and `external-consumers-unknown` over a
  *closed* world each refuse — each with its **own distinct key**
  (`…-without-deficiency`, `…-carrier-unsupported`, `…-not-for-deficiency`, `…-required`,
  `…-relation-not-in-scope`), not one generic fault. At **retained Run closure** the same faults
  refuse again after I mutated the committed payload and re-closed — the verifier's path.
- **`derivation-policy-unmet` qualifies types only.** Its row carries `relations: ["types"]` and is
  the only row with a relation restriction; a `references` entry declaring it while carrying
  `compiler-inferred` refuses at both boundaries.
- **RC-3 and requirement-relative sufficiency preserved.** I exhibited RC-3 natively rather than
  forging it: a Run with a real admitted `unresolved-edge` fact yields `coverage: complete`,
  `state: incomplete`, `deficiency: null`, and closes. The registry states explicitly that the
  deficiency is not re-derived from the entry alone, because several conditions are
  requirement-relative and RC-3 would otherwise refuse lawful Runs.
- **The selected-scalar limitation is explicit and not overclaimed.** Per carrier:
  `unresolvedEdgeClasses` is a genuine set and loses nothing (I closed a Run carrying two classes at
  once); `closedWorld` and `derivationKinds` are independent; but `input-closure-incomplete`'s
  carrier is a **single scalar** and the retained cause is a **selected** one, not the full set. An
  earlier revision's "loses nothing" generalisation is named as wrong and retracted, and **no
  multi-cause format is introduced** to paper over the limit. I did not find anywhere that a
  cross-relation scalar is claimed to encode every simultaneous deficiency.

### CB4-SHOULD-1 — body language — **RESOLVED** (22 cases)

`languageIdSource` now reads `bodyLanguageByVariant[<variant the closed suffix table selects from
this anchor's path, longest match>]` for `closed-suffix-table` rows and `bodyLanguage` otherwise,
with a companion key stating it is emphatically **not** the domain row's `language` field.

I checked the **committed bytes**, not the sentence: for a `.js` body under
`native.semantic-universe.typescript.v2` the frame the Run actually committed contains `javascript`
and does **not** contain `typescript`; under the grammar-only syntax universe a `.rs` body's
committed frame contains `rust` and never `syntax`. Clone Runs close under all three universes.
Rust uses `selected-compilation-target-edition`, so the selected target dialect — not the engine —
decides. Every derived value is in the unchanged closed `{javascript, rust, typescript}` enum. An
unlisted suffix **refuses** rather than being folded into a neighbour. Level/source/specification/
compiler/normalizer framing and ownership limits are untouched: `recomputableAt` is still
`L0-verbatim` only, and a clones *scope* still closes where no body identity is admissible.

### CB4-SHOULD-2 — capability, default and publication — **RESOLVED** (51 cases)

The matrix `capabilities[].id` is published as **the** closed authority (11 members) with a
`capabilityIdLaw`; cells are exactly the complete product 11 × 6 = **66**; no id contains `@`.

- **The default is fixed by the matrix, not by a release.** This is the substantive half and it
  holds: the default request set is **identical** under a full release registry and a starved
  one-row registry. `UNSUPPORTED-TYPED` cells are requested deliberately and answered; only
  `NOT-SELECTED` cells are excluded, and requesting one is refused as *unsatisfiable*. Explicit
  overrides survive with their own provenance.
- **Release declarations cannot redefine promises.** Unregistered capability, unregistered mode,
  `NOT-SELECTED` cell and duplicate `capabilityId` each refuse with their own key. The earlier "a
  release need not ship everything" sentence is named as wrong and retracted — it had let the
  selected product shrink silently.
- **Candidate-only capabilities fabricate nothing.** `clones-near` and `clones-cross-tsjs` have
  empty matrix `relations`, carry `projection: selection-account-only`, and mint no fact, no
  `relation@rung`, no Coverage and no `Candidate`.
- **Disclosed in the original invocation, with the complete ownership tuple in typed fields** —
  `capabilityId`, `languageMode`, `workspaceRoot` — so two workspaces requesting the same capability
  stay distinguishable, which is exactly what the earlier concatenated subject collapsed.
- **Bounds and honest counts.** A step's notices are bounded at 1024 — exactly the analysis-spec
  request bound, so overflow is **unreachable** — and steps at 64, the invocation's own `StepId`
  0–63 range. Two steps of 1023 compose 2046 notices, the case one flat array refused. Counts are
  exact at the edge; the helpers do not truncate, and a forced oversized step, a 65-step invocation
  and `stepId: 64` are each refused by the schema. A 4000-character `workspaceRoot` survives intact
  as a `UserInputPath` (4096) rather than being folded into a `BoundedText` (1024).
- **All-surface parity.** `capability-availability` is a *declared* parity field of all **five**
  `requestClass: analysis` commands, so it reaches human, SARIF and HTML too.
- **Precedence.** `references` under `syntax-only` keeps `language-tier-unsupported` /
  `capability-missing`, which outranks `provider-unavailable`; it is answered, never rejected merely
  because a provider is missing.
- **No false completes.** I forged the false claim rather than assuming it: the honest answer closes
  a Run and is my positive control, while `coverage: complete` with `deficiency: null` refuses with
  `SYNTAX_CAPABILITY_UNSUPPORTED_SCOPE`, and a relabelling to a weaker deficiency refuses with
  `SYNTAX_CAPABILITY_DEFICIENCY_MISMATCH`.

## 5. Public errors and the publication-shorthand account

The whole route registry was scanned: **every** registered route yields non-empty envelope errors
whose codes are all members of the closed public registry, with a subject and a remedy — even where
`StepTermination.domainDetail` is lawfully **absent**, which is precisely the case the
`kind=failure` envelope's non-empty `errors` requirement would otherwise strand. Vague operational
prose supplies no carrier and is not treated as one.

A colon-suffixed internal key is **not** a standalone public code: `normalize_internal_key` takes
the longest registered key plus the remainder as subject, an unregistered key **refuses** rather
than passing through, and an origin the key cannot have refuses — no origin laundering. The five
conditions stay distinct: user configuration → `CONFIG.INVALID`; external/retained bad input →
`REQUEST.PRECONDITION_FAILED`; impossible requested cell → `REQUEST.UNSATISFIABLE`; producer
protocol fault → `PROVIDER.PROTOCOL_VIOLATION`; host invariant →
`SYSTEM.OUTCOME.ILLEGAL_STATE` + `faultCause: host-invariant`. One key under three origins yields
three different answers. No Run is fabricated before a Plan exists.

**Unicode boundary.** Length and slicing count **code points**; the SHA-256 is over **raw UTF-8
bytes with no added normalization**. I confirmed a fitting non-ASCII subject is *retained* even
though its UTF-8 byte length exceeds 1024; an over-length one elides to exactly 1024 code points
using the declared marker window plus the digest; a composed-versus-decomposed string is **not**
silently normalized (its digest differs from the NFC form's, and the published subject carries the
raw one); distinct long values elide to distinct subjects; and the registered key survives verbatim.

**Root publication-shorthand v14.** The account claims three editorial corrections and the diff
contains exactly three, all substantive and all accurate: naming the already-selected leaf/step
carrier (`release_absence_notices` produces `{noticeCount, notices}`; `stepId` is *added* to form
`CapabilityAvailabilityStepV1` — I confirmed the shapes), all **five** analysis commands rather
than four, and the candidate-only route as the **typed availability notice** rather than a bare
`DomainDetail`. Both root after-images are **byte-identical** to the frozen final bytes, so these
root-owned bytes are covered by this review.

## 6. The selected D9 host-invariant extension

The historical `d9-exit-contract.v1.14.json` is **byte-identical to v13**, and the composition is
published normatively at `#/x-opensip-public-route-registry/hostInvariantSuccessor` rather than
deferred as a mechanical records task. It adds exactly one thing — `faultCause: host-invariant`
mapped to the **existing** `SYSTEM.OUTCOME.ILLEGAL_STATE`.

Common schema, workflow mapper, route registry and owning prose **agree**, and the derived
termination really carries both required fields. Measured: `faultCause` grew by **exactly one**
member and lost none; the fault-cause code mapping shows **0 changed, 1 added**; class and exit
tables are untouched. The subtype is distinct from the already-representable `host-io`,
`ledger-corrupt` and `provider-protocol`, and borrowing `host-io` is refused by contract as a
different remedy. Notably, the registry states that `codeMaps.rule`'s "total and injective" is a
property of the **declared cause domain**, that an errorCode without a preimage was never a
totality violation, and that the earlier claim the maps were non-total **was wrong** — so
mathematical totality is not confused with surjectivity, and the extension does not overclaim: it
says plainly that this *is* a vocabulary extension.

## 7. Advisories

All four Bv4 advisories are addressed **at their original severity**, none upgraded: the stale "60
cells" is replaced by a *derived* count (removing the class of defect, not just the instance); both
prose enumerations now list the syntax domains; the four effect→token mappings are published with
their three scope facts and no confinement claim; and the parameter duplicate-selector limitation is
**accounted rather than lifted**, with re-keying explicitly declined.

The 43 carried advisory dispositions were diffed item by item: **37 → 43, six added, zero removed,
zero changed**, each individually carried with its own limit intact.

I raise **two new advisories**, neither a MUST nor a SHOULD:

- **V14-ADV-1** — §10 ends with the unqualified "No new public code is added and none is needed"
  while §13 of the same document adds four `DomainDetailCode` members (measured: 283 → 287, 0
  removed). Both are true under their own scopes — §10's paragraph is about the deficiency/cause
  *projection* route, and the four additions serve *refusal* branches — but §10's sentence is not
  scoped in its own text, and one addition is named for the very route §10 discusses. Nothing is
  unrepresentable: the registry is unambiguous, records the additions with reasons under an explicit
  `newInThisCorrection` key, and §13 discloses them. This is the same class of prose-versus-registry
  staleness Bv4 itself raised as ADV-1 and ADV-2.
- **V14-ADV-2** — the `anchorLaw`'s `enforcedAt` claims the producer boundary **and** retained Run
  closure, but `anchor_law` is reachable only through `relation_payload_rules` nested inside
  `open_run_closure`, so the reference model exhibits Run-closure enforcement only. The contrast is
  visible inside this same correction: the deficiency-cause registry names *two* call sites and I
  exercised both. The safety-relevant direction is fully demonstrated — a violating fact cannot be
  committed — so this is a scope-of-evidence precision issue in a registry sentence.

## 8. Scope dispositions

- **16 AR** — all `CARRIED-UNCHANGED`. I recomputed the crosswalk delta: all 16 rows present in
  both, and every one differs **only** in the four review-provenance fields. No requirement, owner,
  selector or disposition field changed.
- **15 FW** — all `CARRIED-UNCHANGED`. `current-source-map.proposed.md` is byte-identical between
  v13 and v14 and absent from the modified set.
- **27 inherited residuals** (`DR-001`…`DR-011`, `DR-011-R01`…`R16`), individually keyed, all
  `CARRIED-UNCHANGED`; the three owning files are byte-identical. `DR-011-R10` is the row the
  product-v1 contract set sits under; its register entry is still byte-unchanged, and the contract
  changes are graded above as the four Bv4 dispositions rather than as a residual closure.
- **30 evaluation subresiduals** — `CARRIED-UNCHANGED`; the file is byte-identical.
- **5 scoped DR-201…205** — `ROUTING-ASSESSED-ONLY-NOT-APPLIED`, each with its scope and authority
  recorded. Owner routing sits on crosswalk row AR-15, whose only change is provenance pointers.
  Five owner routing assessments do not grant a final application outcome.
- **32 qualification gates** — all `demonstrated: false`, `qualified: false`, over exactly the four
  D-371 machine IDs (`linux-x86_64-gnu`, `linux-aarch64-gnu`, `macos-aarch64`, `macos-x86_64`).
  Nothing in this delta demonstrates or qualifies a gate, and this review does not.

For every inherited unchanged obligation, `CARRIED-UNCHANGED` records **preservation across this
delta only** — with the byte-identity that is its actual basis. It is never a new discharge.

## 9. Preserved safeguards

Probed where the delta's changed paths reach them, and all holding: bool/int distinction and typed
annotation equality; array-order laws; 13 relation selectors and rungs with the registry as single
ladder authority; snapshot-owned file claims (wrong digest, wrong length, path outside snapshot all
refuse); full TS/JS/Rust/syntax closure; raw-32 clone version and Rust target-edition ownership;
unavailable/partial-ownership empty controls; syntax-only representability; ScopeDocument parameter
binding; and D9 fault-cause mappings.

One safeguard was **strengthened** by this delta: `render`'s parity access is now strict, so a
missing declared parity field fails as a required-delivery fault
(`DELIVERY.REQUIRED_FAILED`, `faultCause: delivery-required`) instead of silently vanishing from all
five formats. An earlier `if k in envelope['parity']` guard had weakened this for *every* declared
parity field.

Families whose owning files are outside the 12 normative modified paths — local cycles and
missingness laws, retained ordered/repeated config and `node_modules` layout, imported observation
`evidenceUse`, the cache validated-hit boundary, mutation/repair replay, purge disclosure and the
leased pin ledger — are carried on the reproduced suite and on the v13 independent review's
inherited evidence. I did not regrade unchanged paths by restating them.

## 10. Retained failed attempts

`evidence/probe-attempts.md` retains **every** probe that failed first, with its exact refusal and
an attribution. Sixteen were corrected; three deserve naming because a careless reviewer would have
scored them as candidate defects:

1. My half-matching-universe fact was refused by the **prior** `RELATION_UNIVERSE_RULE:same-only`
   law, not by the totality law I predicted — a correct and stronger outcome from an unreachable
   premise.
2. My hand-forged RC-3 entry was correctly refused by **RC-2** ("incomplete needs ≥1 edge") — the
   candidate rejecting *my* malformed construction. The lawful shape had to be built, not forged.
3. I assumed a syntax-universe empty result *was* the false-complete graph. It is not: the fixture
   emits the honest `unknown` / `language-tier-unsupported` / `capability-missing` answer, so the Run
   closing was **correct**. I had to forge the false claim to test the law at all.

Two ordering refusals also fired on my own malformed release-registry fixtures before I sorted them
— the array-order law working on my input.

## 11. What this review does not claim

Not product qualification, not platform qualification, not implementation authorization, not
application acceptance, not a readiness change, and not blind reconstructability. Native, compiler,
OS, cryptographic, storage and grammar observations remain **synthetic trusted assumptions**, not
measured enforcement. A **new blind review** on these accepted normative bytes and a **separate full
application review** remain distinct gates — and, as scoped, they are not reasons to reject an
otherwise coherent pending design.
