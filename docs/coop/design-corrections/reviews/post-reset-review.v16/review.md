# OpenSIP — fresh independent architecture/design/reference review, v16

**Verdict: ACCEPT** — for **source and design only**, bound to the exact frozen bytes
`subjectManifestSha256 = ca5f36d421fb38d264f49fc6b2e1eeffee5bbe8182a7fe25bd50787244042ee9`.

**Zero unresolved MUST issues. Zero unresolved SHOULD issues.** Two new findings are raised and
both are nonblocking advisories. Under the standing rule that *any* unresolved MUST or SHOULD forces
`CHANGES_REQUIRED` regardless of headline acceptance or test counts, there is none here.

I am actual Claude in a fresh independent session. I authored none of these bytes and am not
coauthor `f6955666-0878-461a-a4e1-2ca2c4f5e824`, blind `04af6558-0b64-4a99-9fa4-0ca5ad653a27`, or the
earlier independent `7954d0b3-0895-4506-ad06-08f320d35fe8`. I ran no agents, spawned no subagents,
made no product implementation change, no fix, no commit and no push, and edited no subject byte.
Everything I wrote lives under `/tmp/opensip-design-corrections/post-reset-review.v16`, including both
disposable source copies.

---

## 1. Custody, before and after

The manifest hashes to the declared value. All **6839** declared files verify by digest *and* by
length; **0** missing, **0** hash mismatches, **0** length mismatches, **0** undeclared files on
disk, **0** symlinks, and the observed byte total equals the declared `446,064,505` exactly. I ran
the identical check again after finishing: **identical result**, so the frozen subject is unchanged
by this review.

I made two named disposable full copies:

| Copy | Purpose | Byte-exact vs manifest | In-tree delta after execution |
|---|---|---|---|
| `copy-A-reference-run` | the six recorded reference-check commands | yes, 6839/6839 | 0 modified, 0 added, 0 removed |
| `copy-B-probes` | my probes, plus a second determinism run | yes | 0 modified, 0 added, 0 removed |

The native checker writes its report in-tree and ignores `--help`/`--report`, so it was run only
inside the disposable copies. In both, it reproduced the frozen report **byte-for-byte**.

## 2. Source pins, verified before anything executed

| Pin file | Entries | Valid |
|---|---|---|
| `foundation/source-pins.v1.json` | 1099 | 1099 |
| `native/source-pins.v2.json` | 71 | 71 |
| `security/source-pins.v1.json` | 73 | 73 |
| `workflows/source-pins.v1.json` | 65 | 65 |
| **total** | **1308** | **1308** |

All six reference-check command sources also match their declared `sourceSha256`. **No pin was
rewritten under any circumstance** — a pin failure would have been a finding, not something to repair.

## 3. The six reference checks

I wrote `expected-outcomes.prewritten.json` **before** executing anything, grounding each expectation
in my own pin verification rather than in the candidate's logs. All six reproduced, in **both**
copies, with exits matching, stdout byte-identical to the frozen logs, and in-tree reports
byte-identical to the frozen ones — so the results are deterministic across two independent copies.

I re-derived the headline counts rather than restating them:

- foundation **1679** = 231 + 1331 + 24 + 28 + 65 (summed from the executed component reports)
- identity **1331 passing calls** over **1319 distinct ids**, **12** duplicate extra instances
  (two ids at seven instances each) — confirmed against `identity-report.json` directly
- security **456** passing calls, **10** invariant sweeps
- native **347/347** cases, **66** matrix cells, **0** qualified cells
- workflow surface **1598**, workflows source pins **65**
- integration **365** passed, 0 failed, over declared `syntheticTcbInputs`

These are passing calls, distinct IDs, sweeps and cases **with their recorded scope**. They are not
exhaustive coverage and are never product qualification.

## 4. What actually changed, and what it did to admission

21 files modified, 476 added, **0 removed**. Eleven are normative source; the rest are records, four
refreshed pin files, and generated reports.

I diffed the changed documents structurally rather than reading the summaries:

- **All four changed schema/registry JSON documents are prose-only.** Stripping `description`/prose
  keys, `identity-schemas.v2.json`, `capability-manifest-domains.v2.json`,
  `native-evidence.schemas.v2.json` and `repair.schema.json` have **zero** structural diff — no
  `type`, `enum`, `const`, `pattern`, `required`, `additionalProperties`, bound, `$ref` or order
  keyword moved.
- **Registry membership delta is empty in both directions.** No relation, ladder rung, platform id,
  deficiency or coverage state was added or removed.
- **The only structural JSON change in the entire delta** is `workflow-cases.v1.json` gaining exactly
  two `"dynamicDispatch": "not-applicable"` members — a *narrowing*, since the fixture record gains a
  required member (BV5A-NEW-2).
- **Executable lines:** `identity-model.py` +4/−0, `native_evidence_model.v2.py` +26/−3,
  `workflows_model.v1.py` **+0/−0**. Every addition is a new refusal — RC-0 membership, the RC-1
  minting law, the two RC-2 class laws, the mint-time pair check, the retained-scope pair check at
  closure — or the gated fold. The only three removed lines are exactly the three `.lower()` sites
  replaced by `lib_name_fold`.

**No grammar, authority or admission was widened.** The workflows model's CX-BV5-03 corrections are
entirely docstring and comment, which is exactly what a wording-precision finding should produce.

**Digest honesty.** All eleven documents changed bytes, so every derived document digest moved. I
verified structurally *why* this matters: a Coverage `payloadSchemaDigest` **is** the raw SHA-256 of
`native-evidence.schemas.v2.json` (measured equal, `2a5fc493…`), so a description-only edit
necessarily moves every `coverage2` and therefore the reference Run identity. These are truthful
source-bound digest changes, the records describe them as such, and they are **not** identical exact
semantic inputs. My own measured baseline `run2:ca67ad74…` reproduces the coauthor's reported final
baseline independently.

## 5. The four required blind findings

I authored every expected outcome from the published contract text before running, and treated the
shared integration fixture as construction data only — never as a verdict oracle. **594 expectations,
594 agreeing, 0 failing.**

### CB5-MUST-1 — ADM-DOMAIN selection · **corrected and verified**

The selection is **normative**, not a file's self-asserted standing. `identity-and-evidence.md`
states *"The effective registry is selected here, by name."* and names
`native/capability-manifest-domains.v2.json`, superseding `delivery.v4` `valueDomains` **"within its
own declared scope and nowhere else"**; `native-evidence.md` §11 lists the same document
independently, so the selection is stated by both owning contracts.

`RELATION-DOMAIN-V2` carries all **13** relations (12 inherited verbatim + `unresolved-edge`);
`RELATION-LADDER-DOMAIN-V2` publishes the 13 **relation-specific** ladders as a declared mirror of
the single ladder authority. I measured **17** registered `(relation, rung)` pairs: all 17 admit, all
**180** unregistered pairs refuse. A wrong relation or wrong rung still refuses. The four inherited
gates ADM-TYPE / ADM-CLOSED / ADM-DOMAIN / ADM-ORDER are reproduced in inherited order, the CVE1
codec separation is restated, and the inherited `delivery.v4` / `fact-plane.v1` bytes are unchanged.

### CB5-MUST-2 — lib name → declaration component · **corrected and verified**

§2.4 publishes the join as a rule table (Fold, Mapping, Membership, Equality, Order) with
`component(n) = "lib." + fold(n) + ".d.ts"`, a measured discriminator table and version custody. The
same content is carried in the schema descriptions for `libSelection` and `component`.

Measured on the exact bytes: the fold **is** the full context-sensitive default lowercase
(`U+0130 → U+0069 U+0307`; final sigma `→ U+03C2`; non-final `→ U+03C3`), is **not** case folding
(sharp s unchanged where `casefold` gives `ss`), and is locale-independent under `tr_TR.UTF-8` and
`lt_LT.UTF-8` — both of which actually applied on this host. The declared **UCD 15.0.0** binding is
**effective, not advertised**: with the declared case data simulated unavailable, `lib_name_fold`
refuses with `ReferenceEnvironmentError`, whose MRO confirms it is **not** an `AdmissionError`, so an
environment fault cannot be laundered into a typed refusal about a caller's `lib` selection. The
portability limit is published in both prose and docstring rather than hidden.

Twelve context-admission controls hold in both directions — a valid selection admits with zero
refusals, and lib-not-retained, honoredOptions set disagreement, a same-case different-*name*
disagreement, duplicate-under-fold, `libSelection` order, incomplete inventory, ambiguous tree
basename, declared duplicate basename, tree digest mismatch, component order, and a
no-implicit-alternate-representation control (declaration-file names placed in `libSelection` are
refused, not silently accepted) each refuse with their exact published typed refusal.

### CB5-SHOULD-1 — RC-1 applicability · **corrected and verified**

RC-1 is now **total** over the registered pairs and decided by rung membership in the closed
five-member resolved set, never by ladder length: five resolved pairs, and twelve not-applicable
pairs enumerated explicitly **including `unresolved-edge@observed`**.
`reachability@from-resolved-calls` is named as the case that shows why a one-rung heuristic is wrong
— its single rung *is* resolved. RC-0 runs **first** and is relation-specific, so an unregistered
pair can never become not-applicable by fallback; the prose says so outright.

I reproduced the refusals at **both** boundaries myself:

| Case | Producer | Retained Run closure |
|---|---|---|
| `unresolved-edge@observed`, valid **(control)** | ADMIT | **ADMIT** — complete Run closes |
| `unresolved-edge@enumerated` | REFUSE (RC-0) | REFUSE (`SUBJECT_SCOPE_RUNG_NOT_IN_RELATION_LADDER`) |
| `observed` + `attempted=true` | REFUSE (RC-1) | REFUSE |
| `observed` + registered class beside count 0 | REFUSE (RC-1) | REFUSE |
| `stageTerminal=budget-exhausted` **(control)** | ADMIT | **ADMIT** |
| `examinedExhaustive=false` **(control)** | ADMIT | **ADMIT** |
| retained scope, **no Coverage wrapper**, `enumerated` | — | REFUSE |
| retained scope, **no Coverage wrapper**, `observed` **(control)** | — | **ADMIT** |

The positive controls are **complete Run admissions** with real `run2:` identities, not schema
fragments. `stageTerminal` and `examinedExhaustive` stay free and independent. RC-2's
attempted/exhaustive/stage/edge laws and the observed-coverage-versus-resolution distinction are
preserved and separately controlled.

**CX-BV5-09** is verified through a complete retained Run on a *resolved* rung: `complete` + count 0 +
`[computed-member-access]` now refuses at producer and closure while the clean control admits; the
analogous `not-attempted` hole is closed with its own control; and `incomplete`/`partial` are
untouched — an honest `incomplete` carrying its classes admits, a class mismatch still refuses,
`incomplete` still needs ≥1 edge, and all three `complete` preconditions still fire.

**CX-BV5-07** is restated honestly as a **determinacy gap**, explicitly *not* a digest collision and
*not* a divergence over byte-identical observations, noting that `complete` and `not-attempted`
necessarily differ in `attempted`. That matches the root limit exactly — no collision is claimed on
identical inputs, and the earlier blind probe's alternatives did change other committed fields.

### CB5-SHOULD-2 — `closedWorld` projection · **corrected and verified**

The projection names its exact five fields, and I measured that the model's projection expression is
byte-equal to the schema's required set. A descriptor built from seven-member evidence carries
exactly five and drops `dynamicDispatch` and `reasons`. A literal seven-member copy, a copy plus
`dynamicDispatch`, a copy plus `reasons`, each of the five single-member drops, and a copied boolean
alone are **all** schema-invalid — so a copied boolean, a dropped field or a detached descriptor
cannot authorize destructive repair.

Eligibility and reasons stay grounded in the **full native evidence**: the guard reads
`run["closedWorld"]["deadCodeRepairEligible"]` *before* any descriptor exists, and the remedy
surfaces that record's `reasons` (`exports-not-closed,entry-points-partial`) which are not in the
projection at all. The guard covers **every** delete and **every** replace, unqualified —
delete-only and replace-only are each gated, a mixed plan is gated, and create-only is not (the
negative control). `dynamicDispatch` is **target-relative**: `present`, `not-applicable`, `absent`
and `unknown` all leave an otherwise eligible unsafe repair applicable, and `present` does not rescue
an ineligible one. The imported-declared origin still denies unsafe repair.

This is **pure reference admission** over synthetic in-memory inputs — no filesystem mutation, no
authorization service, no product host. It is not real host enforcement and I do not claim it is.

## 6. Advisories, all four plus V15-ADV-1

- **CB5-ADV-1** — measured: exactly **four** terminal representations in the `byDomain` registry,
  **five** representation tokens in use, and `by-domain` never a row value. The contract now names it
  *"a selector, not a fifth terminal representation"*.
- **CB5-ADV-2** — three non-equivalent enforcements named, no snapshot join claimed for the
  fingerprint field. Measured: exactly two direct `$ref` sites; the declarative pattern **refuses** a
  300-character segment while imperative `ordered()` **admits** it, so (1) and (3) genuinely differ
  as stated; `ordered()` still refuses dot-dot, backslash and a leading slash; identity and workflow
  `LogicalPath` are byte-identical in constraint. No accepted path set changed.
- **CB5-ADV-3** — both length prefixes stated as present and meant, with the arithmetic and the
  L1–L3 symmetry that decides the reading. I reproduced the worked vector: `a=1\n` gives L0 payload
  `00 00 00 04 61 3d 31 0a` and frame component `00 00 00 08 00 00 00 04 61 3d 31 0a`. The inherited
  `fact-identity-policy.v2` byte grammar is explicitly unchanged — **no historical rewrite**.
- **CB5-ADV-4 / CX-BV5-06** — the inherited eight-member platform vocabulary is kept (not narrowed);
  the four selected product platforms are exactly the matrix `platformFamilies`; the difference is
  exactly the three the blind review measured. The citation is corrected to security **S8**, which I
  confirmed carries all four ids and names Windows among the excluded populations — and
  `admission-and-qualification.md` contains **zero** occurrences of "Windows", so the blind review's
  citation really was wrong. That original citation is retained as explicit history rather than
  deleted, and the registry states that domain membership grants no platform admission or support
  promise.
- **V15-ADV-1 / CX-BV5-02** — the sentence is scoped *"for every input that reaches that step"*, in
  both prose and docstring. 17 ordering expectations agree: a valid spec admits and so does one at
  exactly the 1024 bound; absent/null/boolean/number/string/object and an in-bound malformed array
  all reach the schema step; only an actual over-bound array refuses at step 1; V15-ADV-1's own
  counterexample reproduces (oversized *and* malformed → cardinality) and so does its control (the
  same specs narrowed → schema). Cardinality-first ordering is unchanged, and retained-Run payload
  corruption remains a distinct boundary, stated as *"corruption rather than an oversized request"*.

## 7. Two new findings — both advisory

### V16-ADV-1 — one governance-record digest pin now denotes superseded bytes

`advisory-application-account.v16.proposed.json` `/items[43]` (V14-ADV-1) pins
`native-evidence.md` at `706b7e0f…`, the frozen **v15** digest; the frozen v16 file is `b50c814c…`.

I scanned **825** path+digest cross-references across the v16 governance records: 0 unresolved, and
this is the **only** genuine mismatch. The other 70 differences all sit in `source-copy-accounts.json`
records, which by construction record the state of a *disposable copy* against
`baseManifestSha256` = frozen v15 — correct as written; my first scan mis-scoped them and the
corrected scan is retained.

Not a MUST or SHOULD: nothing normative is affected, and the **substance** of V14-ADV-1 survives
verbatim in the current bytes. The cost is verification friction — a reader checking the account
finds one pin that does not resolve, with no field marking it as an as-of-v15 historical pin, which
is inconsistent with sibling item V14-ADV-2 whose pin resolves only because its file happened not to
change. *Repair:* refresh the pin, or label it explicitly as historical.

### V16-ADV-2 — the Unicode gate reads a same-build proxy

`lib_name_fold` gates on `unicodedata.unidata_version` and then returns `name.lower()`. In CPython
both derive from the same UCD generation step, so on any stock build they cannot disagree and the
gate is exactly as effective as the contract claims — which is what I measured. The precision point
is that the gate reads a *different module's* declared version rather than the case table the fold
itself consults, and the §2.4 custody paragraph presents `unicode_case_data_agreement()` as reporting
"the running version" without naming the proxy relationship.

Not a MUST or SHOULD: no admission outcome changes on any conforming build, nothing is
unrepresentable, and everything CX-BV5-01 asked for is delivered and verified. *Repair:* one clause
noting the proxy, and that a host sourcing the two independently owes its own equivalent binding.

## 8. Preserved prior corrections

All twelve explicitly named prior corrections have live anchors in the frozen bytes and a governing
suite that executed and passed on those exact bytes: capability/default/availability composition;
body-language and compiler-dialect ownership; anchor cardinality and file totality; digest
annotations with no default and no residue; typed canonical equality; relation/rung scope; imported
observation and ScopeDocument binding; the runtime evidence boundary; cache admission; repair replay;
purge disclosure; and required-output failure after a committed Run. Combined with the zero
structural schema change, the empty registry delta and the narrowing-only executable delta, nothing
was weakened. This is preservation evidence, not a first-principles re-derivation of each.

## 9. Registers — preservation, not grades

- **16 AR rows** — CARRIED-UNCHANGED. Measured field by field against the v15 crosswalk before-image
  (whose digest I verified equals the frozen v15 manifest entry): the *only* differing fields on
  every row are `historicalReviews` and `latestCompletedReview`, review-provenance pointers. No
  obligation, selector, owner, unit, contract, evidence, ownerRows or status field moved.
- **15 FW rows** — CARRIED-UNCHANGED. `current-source-map.proposed.md` is byte-identical across the
  delta and absent from the modified paths.
- **27 inherited residuals** (DR-001…DR-011 plus DR-011-R01…R16) — CARRIED-UNCHANGED. Both owning
  documents are byte-identical; all sixteen R-rows present.
- **5 scoped review owners** (DR-201…205) — ROUTING-ASSESSED-ONLY-NOT-APPLIED.
- **30 evaluation subresiduals** — CARRIED-UNCHANGED; owning file byte-identical.
- **32 qualification gates** — all `demonstrated:false`, `qualified:false` over the four selected
  machine ids. Unperformed, and this review performs none.
- **Carried advisory account** 45 → 50: five added (CB5-ADV-1..4, V15-ADV-1), zero removed, zero
  severity changed. All 45 pre-existing items differ in exactly one added field,
  `currentAssentStanding`, which states the item is carried at its exact original severity and that
  the assent does not turn carried or routing-only dispositions into new application grades.

**CARRIED-UNCHANGED and ROUTING-ONLY are not grades and not final application outcomes.** Nothing
here is discharged, closed or graded. My own V16-ADV-1 and V16-ADV-2 are not in that account and any
future application must account for them separately.

## 10. Failed attempts — all eight are mine

I preserved every failed attempt with its corrected successor. Six were harness or fixture defects
(a wrong `snapshot2:` prefix; an evidence snapshot taken before a view rekey; a closure record
missing `schemaVersion`; an analysis-spec with the wrong `schemaVersion` and an incomplete capability
row; an unsorted canonical-set array; a resolver that missed record-relative custody paths) and two
were **wrong expectations of my own** — I expected an order refusal where `ES2022 < dom < es2022`
really *is* ascending by raw UTF-8 bytes, and I expected a tree-ambiguity refusal where my own
declared inventory had duplicated the basename first. **Not one was a design failure**, and in every
case the correctly-constructed controls in the same run already agreed.

## 11. What this does not claim

Source/design acceptance coexists with a **pending**, independently reviewed application. This
review invents no grade authority. **D-372 is unapplied, condition 5 is NOT MET, the readiness
register is unchanged and no implementation is authorized** — I verified the v16 README change is
purely additive (an eight-line header, zero deleted lines, before-image equal to the frozen v15
README, and line 144 still reads *"D-372 has not been applied and the central readiness register is
unchanged"*).

I claim no blind reconstructability. A **new blind consumer v6** over these accepted bytes is a
separate act, still required, and this review cannot supply it. I preserve the root blind
qualifications as written: the reported **58** negative-labelled rows are a labelled *aggregation*,
not 58 demonstrated refusals — they include schema-valid cases and omit the separately named flat
ts-negatives (18) and rust-negatives (14) maps; the **8** closed graphs are correct while the 11
scanned runIds include 3 synthetic public-envelope placeholders; and the blanket
"no filesystem or cryptographic primitive" wording means no *product* filesystem or TCB
qualification — actual Python file IO and `hashlib` SHA-256 executed there, as they did here.

No product, platform, compiler, storage or cryptographic qualification is claimed or implied. No
implicit repository execution, untrusted ecosystem, full Map application or model dependency is
inferred. Everything measured is reference admission over synthetic inputs: no compiler, Cargo,
provider, repository, renderer, ledger or operating system executed. The intended product remains one
complete design implemented in stages, over native TypeScript/JavaScript/Rust plus bounded bundled
grammar modes and four selected macOS/Linux machine ids.

## 12. Required next acts

1. A **new blind consumer v6** reconstruction over these accepted normative bytes.
2. A complete, **independently reviewed application and readiness reconciliation**.
3. Optionally, the two nonblocking clarifications V16-ADV-1 and V16-ADV-2, at their stated severity.

**On the final pin seal.** The disposition record's `finalPinSeal` text — *"Separate final
AFTER-ALL-RECORDING live and copied pin checks remain mandatory"* — was written **before** recording
and states the obligation, not its outcome. The live guide records it as executed
(*"All 1308 live AND copied pins passed final seal after recording"*), and independently of both I
verified all 1308 transitive pins against the frozen bytes myself before executing anything, with
zero mismatches. I therefore treat the seal as **satisfied for the bytes under review**, not
outstanding.

**One live-tree observation, for completeness.** The in-repository
`reviews/NEXT-REVIEW.md` was written at 12:48:24, one minute after the freeze, by the orchestration
harness recording this review session. It is the one file the freeze record explicitly permits to
change (*"except explicitly allowed mutable NEXT guide in live tree"*), it is **not** mine, and it
has no effect on the frozen subject — whose 6839 files verified identically before and after.

---

**Verdict, bound to the exact frozen bytes.** Against
`ca5f36d421fb38d264f49fc6b2e1eeffee5bbe8182a7fe25bd50787244042ee9`, whose 6839 files I verified by
digest and length before and after, the four required blind findings and all nine root CX-BV5 points
are corrected **in the admission**, not merely in prose — and I reproduced each refusal at both the
producer boundary and complete retained Run closure, while every positive control still closes a
complete Run. The delta widens no grammar, no authority and no admission: four changed schema
documents are prose-only, registry membership is untouched, and every executable change is a new
refusal. The two findings I raise are advisory and change nothing at admission. **ACCEPT**, for
source and design only, with blind reconstruction, application and readiness all still open.
