# Fresh independent design/reference review — frozen candidate v15

**Verdict: ACCEPT** — 0 unresolved MUST, 0 unresolved SHOULD, 1 new advisory.

`subjectManifestSha256 = 5ec7928426c7a91e323240337dc382c4de32bd4e5f2626eba92c8991067b365f`

I authored none of these bytes. I am not coauthor `77758b10-…`, not prior independent
`46ea25c0-…`, and not blind consumer `878e4b39-…`. This is a design and reference review.
It is not blind reconstructability, not application acceptance, not product qualification,
and not implementation authorization.

**The prior v14 ACCEPT does not cover these bytes.** v15 changes 19 files, seven of them
normative source. I relied on the v14 review only for paths whose owning files I verified
are byte-identical, and there I carry its evidence *with its original limitations* rather
than restating it as fresh.

---

## 1. Custody, before and after

| | Declared | Measured |
|---|---|---|
| Manifest SHA256 | `5ec79284…7b365f` | **matches exactly** |
| Files | 6363 | 6363 |
| Total bytes | 407,813,339 | 407,813,339 |
| Hash mismatches | — | 0 |
| Length mismatches | — | 0 |
| Declared-but-missing | — | 0 |
| Undeclared files | — | 0 |

Verified **before any reading** and again **after all work**, identically
(`custody/verify-PRE.json`, `custody/verify-POST.json`). Every declared file's SHA256 *and*
byte length recomputed, and the tree walked independently for undeclared entries. The frozen
subject and the original repository were never written to; everything I produced, including
two full disposable copies, lives under `post-reset-review.v15/`.

## 2. The exact delta, recomputed rather than read

From the v14 and v15 manifests directly: **316 added, 0 removed, 19 modified**. The declared
`predecessorManifestSha256` matches the real v14 manifest hash. Seven modified files carry
normative source:

| File | Change |
|---|---|
| `native-evidence.md` | availability-route table row widened; §10 pre-Plan order published; V14-ADV-1 sentence |
| `admission-and-qualification.md` | §1.1 availability paragraph rewritten |
| `native_evidence_model.v2.py` | `admit_analysis_spec`, cardinality guard, `scope_refusal_termination`, remedy table |
| `native-evidence.schemas.v2.json` | **exactly one string**: the `operationalCarrier` route |
| `relation-payload-schemas.v2.json` | **exactly one string**: `anchorLaw.enforcedAt` (V14-ADV-2) |
| `check-identity.py` | +49 checks |
| `integration-fixtures.py` | provenance header only; 54 copied declarations, all verified present |

The remaining twelve are the four pin manifests, five generated reports, the crosswalk, the
README and the resume guide. I confirmed by hash that `identity-model.py`,
`identity-schemas.v2.json`, `native-capability-matrix.v2.json`, `common.schema.json`,
`command-envelope.schema.json`, `workflows_model.v1.py`, `public-detail-registry.v1.json`,
`command-inventory.v1.json` and all four proposed-disposition files are **byte-identical to
v14**. That bounds what I had to re-examine, and it is the actual basis for every
`CARRIED-UNCHANGED` below.

For the two clarification files I ran a **key-by-key structural diff**, not just a text diff.
Each changed exactly one string and nothing else.

## 3. Reference commands: reproduced, not accepted

**Pins first.** All **1308** transitive pins verified *before* running anything: 0 stale,
0 missing, and I did not re-pin. The re-seal that V14-ADV-2's digest change forced is a
**pure digest update** — I diffed all four manifests and no pin was added, removed or
repathed; counts stay 1099 / 65 / 71 / 73.

My first attempt exited **127** on all six commands: `zsh` treated my quoted interpreter
variable as one word, so nothing ran. `copy-run1` was byte-identical afterwards, which is what
proves no partial execution. Re-run in a **new** copy, `copy-run2`:

| Command | Exit | Log vs retained | Result |
|---|---|---|---|
| foundation | 0 | identical | 1099 pins, checks executed |
| security | 0 | identical | 456/456 cases, 10 sweeps |
| native | 0 | identical | 347/347 cases, matrix cells 66, 0 qualified |
| workflows | 0 | identical | 65 pins |
| workflow-surface | 0 | identical | 1598/1598 checks |
| integration | 0 | identical | 365 passed, 0 failed |

Regenerated reports were **byte-identical**; the full source-copy delta after all six
commands *and* all my probes is **0 added / 0 removed / 0 modified** in both copies. I
checked mtimes to confirm the reports were genuinely **rewritten** (10:21–10:22, against a
10:19:31 copy time) rather than left untouched — byte-identity only means something if
something was written. No nondeterministic field, nothing normalized away.

The native checker ignores `--report` and writes `REPORT_PATH` relative to its own directory.
Its **actual** report path is
`docs/coop/design-corrections/native/native-evidence-report.v2.json`, and I ran it only in
my disposable copy.

**Counts, honestly.** I recounted the identity report myself: **1331 passing check calls over
1319 distinct ids**, the 12 extra instances from exactly two ids (`closed-closure`,
`exact-version-closure`) at seven each, all passing. Foundation's 1679 = 231 + 1331 + 24 + 28
+ 65. Identity grew by exactly **49 calls and 49 distinct ids** with **zero removed**. The
candidate's own account states the same three numbers. None of these is exhaustive coverage,
and passing calls are not unique cases.

## 4. The two root post-freeze v14 findings

Root found both **after** the v14 freeze; the v14 reviewer did not discover either. They
remain historical findings against v14. **285 independently authored probe cases**, every one
bound to the exact frozen source SHA256s (a mismatch is fatal at import), all holding.

### 4a. The availability carrier — **CORRECTED** (72 cases)

v14 accepted `CommandEnvelope.availability` as the carrier, but admission §1.1 still read
"delivered publicly as a `DomainDetail` … through `DoctorResult.defects[]` or
`StepTermination.domainDetail`", and the native route annotation said the same. That is a real
contradiction and v14 missed it.

Now all seven surfaces agree, and I tested composition rather than prose:

- **The composition really calls the right helper.** `invocation_availability` contains
  `release_absence_notices` and does **not** mention `release_absence_details`.
- **The legacy helper is honestly retired.** It declares itself SUPERSEDED and
  NON-AUTHORITATIVE, names its replacement, and I *executed* it to confirm it genuinely
  discards `workspaceRoot` and collapses two units into fewer records. It cannot substitute.
- **A generic environment note is explicitly not the route.** Both the schema annotation and
  the helper say a `DoctorResult` entry or a `StepTermination.domainDetail` may still carry
  one, but "neither is this route" — singular where an invocation has many, and a doctor
  report is a *different invocation*.
- **No mirror still presents the superseded route.** I swept all six live normative surfaces
  for the three superseded phrasings: **zero remaining**.
- **The tuple survives.** Two units keep **22 distinct notices**, both workspace roots intact,
  in typed fields, never concatenated; `workspaceRoot` is a `UserInputPath` (4096), not a
  `BoundedText` (1024). Removing any one of the three tuple fields refuses; a foreign code
  refuses.
- **Bounds are invocation-versus-step, exactly.** A step's notices are bounded at 1024 —
  *the* analysis-spec request bound, read from the schema, so a step can never truncate — and
  `steps` at 64, the `StepId` range. Two steps of 1023 compose **2046** and still admit: the
  case one flat array refused. Counts are exact; a forced oversized step, a 65-step invocation
  and `stepId: 64` each refuse.
- **Parity.** All **five** `requestClass: analysis` commands declare `capability-availability`;
  no non-analysis command does.
- **Candidate-only capabilities fabricate nothing.** `clones-near` and `clones-cross-tsjs`
  have empty `relations`, no `fact` authority, project `selection-account-only`, name no
  `relation@rung`, and mint no Coverage or Candidate.

### 4b. Pre-Plan selection cardinality — **CORRECTED** (81 + 54 cases)

The arithmetic is real, and I recomputed it **from the matrix** rather than trusting the
prose: 11 selectable capabilities for each of the three TS/JS modes and 10 for each of the
three Rust/syntax modes — the only `NOT-SELECTED` cells are `clones-cross-tsjs` against the
three non-TS modes. So scope roots bounded at 1024 admit **94** units while the matrix-fixed
default produces **1034** requested rows against its own **1024** bound. **93 units = 1023
rows — one row of headroom, not exactly at the bound.**

- **Both entry paths reach the same owning check.** The complete **default** (94 units) and a
  complete **explicitly supplied** 1034-row spec each refuse with
  `PROJECT.SCOPE_LIMIT`, subject `requestedCapabilities:1034>1024`, `request-rejected` /
  exit 2 / `REQUEST.UNSATISFIABLE` — with a **schema-admitted `StepTermination`** and a
  **schema-admitted full failure envelope** whose non-empty `errors` array is *exactly* the
  termination detail, so the two surfaces cannot disagree. Explicit 1025 refuses; **1024 and
  1023 admit**; one-row and empty selections admit.
- **The fixed default is unchanged.** Its 1023-row array is **identical** under a full and a
  starved release registry — I compared the emitted arrays — and it still overflows at 94
  units under a starved one. The bound is on the *request*, not on availability. Absences are
  disclosed, not dropped.
- **The widened code names all four fields across two families.** `workspaceRoots` (1024),
  `pathPrefixes` and `excludedPathPrefixes` (65536) on the scope descriptor, and
  `requestedCapabilities` (1024) on the analysis spec. Each names itself in the subject, each
  composes an admitted envelope, and each remedy names narrowing and denies truncation — the
  three inherited scope-descriptor remedies are **preserved**, not replaced.
- **Nothing is mistaken for a requested array.** A missing field, `null`, a boolean, an
  integer, a short string, a **1025-character string**, a **1034-key dict**, a nested object,
  a missing or wrong `schemaVersion` and an unknown property each refuse *without ever* being
  a `ScopeRefusal` and without ever publishing `PROJECT.SCOPE_LIMIT`. The decisive case holds:
  a 1025-character string is **never** published as 1025 capabilities. Nothing is coerced.
- **No truncation, no sharding, no raised bound, no host fault.** The full 1034 is reported;
  the bound is still 1024 and read from the schema; the class is never `operational-failed`
  and the code never `SYSTEM.OUTCOME.ILLEGAL_STATE`; no `faultCause: host-invariant` appears.
- **A corrupt retained payload is a genuinely different question.** My first attempt only
  rewrote blob bytes and refused at `BLOB_DIGEST` — correct, but it never reached the schema
  route the claim is about. I forged a **self-consistent** payload (blob re-put, Plan
  re-minted, every digest join holding). Retained Run closure then refuses with a generic
  `ValidationError` of **259,664 characters** — never `PROJECT.SCOPE_LIMIT`, never
  `ANALYSIS_SPEC_CAPABILITY`. Two distinct routes, neither an ordinary request refusal.
  Preflight indexing does not bypass retained schema validation, and
  `admit_analysis_spec` is called **only** from `default_capability_selection`, never from the
  retained path — so the architectural-separation claim is true, not merely asserted.
- **No Plan or Run is minted for the refused step**, while the invocation keeps its ordinary
  attribution and any earlier committed step outcome stands.

## 5. The two v14 advisories — addressed at their original severity

Neither was silently promoted to a required finding, and neither was ignored. I checked each
clarification's *factual claims* myself rather than accepting the assessment.

**V14-ADV-1.** The frozen bytes are `706b7e0f…` — the exact alternative the coauthor supplied,
not root's originally proposed wording. The replacement preserves **all four** refusal-code
additions ("The refusal branches later in this section separately add four public detail
codes; those additions do not change this projection"), and the four members are named at
lines 2376–2384 with all four still present in the **unchanged** 287-code registry. I
independently confirmed the geometry the fix depends on: §10 spans **2140–2537**, the
four-codes paragraph sits at **2376 inside §10**, and §13 begins at **2750**. So "later in
this section" is accurate, and root was right to reject its own "section 13" wording.

*A correction to the prior review's own text:* v14's V14-ADV-1 **title** says "section 13 of
the same document" while its **own selector** cites 2376–2385, which is section 10. The
selector is right and the title is wrong. Root preserved the frozen artifact verbatim and
recorded the qualification separately rather than editing it — the correct handling. I record
it so a successor does not inherit it as fact.

**V14-ADV-2.** `anchorLaw.enforcedAt` now (i) **preserves the producer obligation** as a modal
MUST with "on every owning fact" attached to the obligation, (ii) preserves the verifier
obligation at retained closure, (iii) **accurately limits the exhibited reference evidence** —
"it does not exhibit a separate producer-boundary call site" — and (iv) **claims no producer
implementation**, naming no function, call site or boundary: "Producer enforcement remains an
implementation conformance obligation." I re-derived the call-site fact myself in the
byte-identical model: `anchor_law` is defined at 840 with **exactly one** call site at 939
(the 1081 occurrence is a comment), inside `relation_payload_rules` (923–1003), whose own
single call site is 755, inside `open_run_closure` (566). The ordering clause survives and is
true — 939 precedes the `relation_source_joins` call at 957.

The change strengthens the statement rather than weakening the law: the old text asserted as
*fact* something the reference model does not exhibit.

## 6. The four Bv4 findings do not regress

**CB4-MUST-1** — the anchor law is still closed over all 13 relations in three classes
(source-text 9 / min 1 / no per-relation maximum; `clones` exactly 1; `file`/`package`/
`vcs-change` exactly 0), the classes partition the 13 without overlap, every class carries a
rule, and the shared `fact.anchors` `maxItems: 100000` / `uniqueItems` bound is present and
not overridden. The owning file's only change is the `enforcedAt` string.

**CB4-MUST-2** — the deficiency-cause registry is still **total over `DeficiencyV2`**, 9 rows
for 9 members, recomputed, no gap and no extra. No enum widened: `DeficiencyV2` 9,
`NativeCause` 14, `UnresolvedEdgeKindV1` 16. The owning file's only change is the
`operationalCarrier` string.

**CB4-SHOULD-1** — owning files byte-identical. Complete Runs still close under the
TypeScript, Rust and grammar-only syntax universes in my own positive controls. The
body-language evidence itself is **carried**, not re-graded.

**CB4-SHOULD-2** — 11 capability ids, none containing `@`; cells the complete 11 × 6 = **66**;
`capabilityIdLaw` published; `platformQualified` still false. An unregistered capability, an
unregistered mode, a `NOT-SELECTED` cell and a duplicate id each still refuse with their own
key, and requesting a `NOT-SELECTED` cell is refused as *unsatisfiable*. This is where §4a
belongs: v14's resolution was **incomplete at the admission mirror**, and v15 completes it.

Established laws probed where this delta reaches them, all holding: typed canonical equality
and bool/int distinction; canonical-set array order on the requested set; 13 relations with
the registry as single ladder authority; the availability bound tied to the request bound
rather than restated; and **required-output failure after a committed Run** — `render`'s
parity access is still strict, tested *behaviourally* after my first string-match attempt
falsely tripped on the comment documenting the removed guard.

## 7. One new advisory

**V15-ADV-1** — the published pre-Plan ordering paragraph says, unqualified, that "everything
a schema is genuinely better at — an unknown property, a wrong type, a missing field, a
missing `schemaVersion` — still refuses at the schema step exactly as before"
(`native-evidence.md:2906`, repeated in the `admit_analysis_spec` docstring). That holds only
while the array is within its bound. A spec with **1034 valid rows and** a missing
`schemaVersion`, a wrong `schemaVersion`, an unknown property or a missing `policyPackIds`
refuses with `PROJECT.SCOPE_LIMIT`, not with the schema fault; the same four at 10 rows refuse
with a `ValidationError`, which is my control.

**Not a MUST or a SHOULD.** Nothing is unrepresentable and no admission outcome is wrong: the
refusal that fires states a *true* fact about the instance, the malformed spec is refused
either way, both routes are `request-rejected` / exit 2, no Plan or Run is minted, and
narrowing the selection then reveals the underlying schema fault — the diagnostic is deferred
across two round trips, never lost. The same paragraph *does* state the implemented order
precisely ("bounded selection cardinality first"; "conditional on the field actually being a
JSON array in an object"), so an implementer building from the published order reaches the
right result. This is the same class as V14-ADV-1, at the same severity. Repair: scope the
sentence to specs whose array is within its bound.

## 8. Scope dispositions

- **16 AR** — all `CARRIED-UNCHANGED`, individually keyed. I recomputed the crosswalk delta:
  all 16 rows present in both, and every one differs **only** in the two review-provenance
  fields `historicalReviews` and `latestCompletedReview`. No obligation, selector, owner,
  unit, contract, evidence, `ownerRows` or status field changed.
- **15 FW** — all `CARRIED-UNCHANGED`; `current-source-map.proposed.md` is byte-identical and
  absent from the 19 modified paths.
- **27 inherited residuals** (`DR-001`…`DR-011`, `DR-011-R01`…`R16`), individually keyed, all
  `CARRIED-UNCHANGED`; both owning files byte-identical. `DR-011-R10` is the row the
  product-v1 contracts sit under; its entry is byte-unchanged, and the contract edits are
  graded in §4 and §5, not as a residual closure. (`DR-012` appears in that file only as prose
  — "remains release qualification" — and is not one of the 27 rows.)
- **30 evaluation subresiduals** — `CARRIED-UNCHANGED`; the file is byte-identical.
- **5 scoped `DR-201`…`DR-205`** — `ROUTING-ASSESSED-ONLY-NOT-APPLIED`, each with scope and
  authority. I read their owner routing directly from crosswalk row **AR-15**, whose only v15
  change is the two provenance pointers. Five owner routing assessments do not grant a final
  application outcome.
- **32 qualification gates** — all `demonstrated: false`, `qualified: false`, over exactly the
  four D-371 machine ids (`linux-x86_64-gnu`, `linux-aarch64-gnu`, `macos-aarch64`,
  `macos-x86_64`). Nothing in this delta demonstrates or qualifies a gate, and neither does
  this review.
- **45 carried advisories** — diffed item by item against v14: **43 → 45**, two added
  (V14-ADV-1, V14-ADV-2), **zero removed, zero changed**, each at its original advisory
  severity and bound by sha to both the v14 review and the source correction. My V15-ADV-1 is
  **not** in that account and must be accounted separately by any future application.
- **D-372 unapplied; condition 5 NOT MET**; readiness register unchanged — read from the
  frozen bytes, not from a summary.

For every inherited unchanged obligation, `CARRIED-UNCHANGED` records **preservation across
this delta only**, with byte-identity as its actual basis. It is never a new discharge, and
routing-only is not a grade.

## 9. Retained failed attempts

`evidence/probe-attempts.md` retains **all eight**, with exact refusals and attribution.
**None was a candidate defect.** Three deserve naming:

1. My "full" release registry declared every capability for every mode, including the
   `NOT-SELECTED` `clones-cross-tsjs` × `rust-cargo` cell. It was refused with
   `native.release-capability-mode-not-selected` — **the v14 CB4-SHOULD-2 safeguard firing on
   my input**, so the failure is evidence the law holds.
2. Two array-order refusals (`utf8` on `languageModes`, `canonical-set` on the registry rows
   and on `requestedCapabilities`) fired on my own unsorted fixtures.
3. My strict-parity check string-matched `render`'s source and hit the **comment** documenting
   the guard the v14 delta *removed* — a false negative entirely of my own making, which would
   have been a false accusation had I reported it. Replaced with a behavioural test.

I also over-asserted that every analysis command declares all four of human/json/sarif/html.
`fit` declares no SARIF and `repair-verify` no HTML; the published rule is that a *declared*
format must be applicable, not the converse. My expectation was wrong; both declarations are
unchanged from v14 and lawful.

## 10. What this review does not claim

Not product qualification, not platform qualification, not implementation authorization, not
application acceptance, not a readiness change, and not blind reconstructability. Native,
compiler, OS, cryptographic, storage and grammar observations remain **synthetic trusted
assumptions**. There is **no real host, CLI or renderer execution** to infer from: "reaches
every renderer" is a *declared* parity field plus a strict render selection, not observed
output. No AR, FW, residual, subresidual, owner row or gate is graded or closed here.

A **NEW blind consumer review** on these bytes and a **separate full independent
application/readiness review** remain distinct required acts — and, as scoped, they are not
reasons to reject an otherwise coherent pending design.
