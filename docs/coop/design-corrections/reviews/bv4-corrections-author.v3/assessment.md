# bv4-corrections-author.v3 — pre-edit assessment of the two publication joins

Written **before** any edit to `work/`, which is verified byte-identical to
released v2 (4379 files). v1 and v2 are untouched.

Immutable inputs read in full this turn: `codex-assessment.json` (both
`requiredFollowup` items, `supportedCorrections`, `developmentSuiteLimits`),
`complete-codex-note.md` **including the last two sections** — "Follow-through on
the same candidate-only carrier point" and "Same PUBLIC-ROUTE point: exact
inherited host-fault classification" — and
`bv4-public-recheck.v2/{report.json,probe.py}`. I also read the inherited
`d9-exit-contract.v1.14.json` (`nonAnalysisDerivation.rules`,
`scenarioAxesSchema.properties.domainCondition`, `codeMaps`, `causeModel`,
`codeVocabulary`) and the live workflow schemas.

**Position: I agree with both findings without reservation.** Both are correct,
both are my defects, and one of them I made worse by writing a checker that could
not fail. One place needs a design decision the closed taxonomy cannot currently
express; I state the limitation and the smallest successor below rather than
borrowing an unrelated code.

Grounding probe (`probes/p0_carrier_survey.py`, schema admission only, no host
runtime or D9 execution) — results cited throughout.

---

## 1 · CX-BV4-DEFAULT-PUBLIC-CARRIER — agreed

`selection-account-only` names a **Python helper return**. It is not a published
carrier, and root's control is decisive: a valid `AnalysisResult` ADMITs and the
literal insertion of `undeclaredCapabilities` REFUSES, because `AnalysisResult` is
a closed union. My v2 prose said the absence is "machine-readable rather than
implied" — for an in-memory dict that claim is not true of anything a consumer
receives. The gap is real.

**The carriers already exist; nothing needs inventing.** The survey admits all
three:

| Carrier | Probe | What it is |
|---|---|---|
| `DomainDetail{code: native.capability-unavailable, subject, remedy}` | A · ADMIT | `native.capability-unavailable` is **already** a `DomainDetailCode` member, and the registry already aliases `provider-unavailable/capability-missing` → it |
| `DoctorResult.defects[]` (array of `DomainDetail`, `x-opensip-order: sequence`) | B · ADMIT | the installation/environment diagnostic step — `doctor` is an existing `StepKind` and `DoctorResult` an existing `StepDomainResult` member |
| `StepTermination.domainDetail` on a **success** step | C · ADMIT | the success branch forbids `errorCode`/`reasonCodes`/`signal` but **not** `domainDetail`, so an advisory absence rides a successful analysis |

So my correction is to **name and wire these**, not to widen `AnalysisResult`:

- **Fact-producing capabilities** keep the route they already have — the
  `relation@rung` Coverage entry, `provider-unavailable`/`capability-missing`
  under the existing precedence. Unchanged.
- **Candidate-only capabilities** (`clones-near`, `clones-cross-tsjs`, empty
  `relations`) have no Coverage entry, so their public route is the
  `DomainDetail` diagnostic — in `DoctorResult.defects[]` for an environment
  report, and as `StepTermination.domainDetail` for a single operative absence on
  an analysis step. Advisory only: no Control verdict, no repair authority, no
  fabricated clone Candidate, no invented relation, fact or Coverage.
- Deterministic order comes from the existing `x-opensip-order: sequence` on
  `defects`, fed by the selection account's canonical order.
- Honest incompleteness: `defectsFound` may exceed `maxItems: 256`, and the law
  must say the count is authoritative when the list is bounded.

**The blanket-pair residue is real and I will fix all of it.** Root is right that
three places still contradict native §1.4's corrected precedence: admission §1.1,
native §10's `UNSUPPORTED-TYPED` paragraph, and
`unsupportedTypedIsNotOnThisTable` in the native schema. Each still states the
`provider-unavailable` pair as *the* outcome for an unavailable capability, where
§1.4 now says `language-tier-unsupported` wins when the universe cannot serve the
relation at all, and that candidate-only capabilities get no Coverage pair.

## 2 · CX-BV4-PUBLIC-ROUTE-COMPLETE — agreed, and my checker was the worse half

Root reproduced it exactly: **14 of 16** branch targets REFUSE the real
`DomainDetail` schema (probe J confirms `request detail (capability, mode)` is not
a code), and **all 14** internal keys are absent from `internalAliases`. My
`recordsEditOwnedByRoot` sentence claimed "every target is already a member" and
"the edit is mechanical". Both were false.

Worse, my control `every-named-public-detail-target-is-already-a-registry-member-or-a-request-detail`
explicitly whitelisted `request detail` / `operational record` prefixes — it was
written so that prose would pass. A test that cannot fail is not evidence, and its
PASS established nothing. I accept that fully.

**What the real route is.** `StepTermination` is the public carrier, not a bare
`DomainDetail`: `class` + `errorCode`/`faultCause`/`reasonCodes`, with
`domainDetail` **optional**. Probes D/E/F admit the three sound branches. So where
no `DomainDetailCode` member fits, `domainDetail` is lawfully **absent** and the
diagnostic lives in the operational record — which is what the existing event law
already permits. Prose placeholders are removed, not re-spelled.

**The four origins, derived through the inherited law.**
`nonAnalysisDerivation.rules` and `axes.domainCondition` settle three of them:

| Origin | Class | Axis | Code |
|---|---|---|---|
| External Config2/CLI configured capability | `request-rejected` (2) | `rejectionCause: config-invalid` | `CONFIG.INVALID` — rule 2, "authored-config errors" |
| Externally supplied / retained spec, origin **known** external | `request-rejected` (2) | `rejectionCause: precondition-failed` | `REQUEST.PRECONDITION_FAILED` |
| Malformed host-supplied **authenticated release registry** | `request-rejected` (2) | `rejectionCause: precondition-failed` | `REQUEST.PRECONDITION_FAILED` |
| Host **bug** minting its own invalid internal layer | **`operational-failed` (4)** | `domainCondition: host-fault` | *see the limitation below* |

I accept root's specific correction that my v2 was wrong to describe every
retained or direct spec as host-generated: the pure helper is not passed an
origin, so the *contract* names the origins and the **host** supplies which one
applies from context it already holds.

### The one thing the closed taxonomy cannot express

`nonAnalysisDerivation` rule 5 puts host failures in `operational-failed`, and
`domainCondition` separates `host-fault` from `precondition-failed`. But:

- `StepTermination` requires `operational-failed` to carry **both** an `errorCode`
  and a non-`none` `faultCause` (probe **H** REFUSES without one).
- `SYSTEM.OUTCOME.ILLEGAL_STATE` is a member of the closed `D9ErrorCode`
  vocabulary in **both** the inherited artifact and the live schema, yet **no**
  `faultCause` and **no** `rejectionCause` maps to it. The survey confirms it is
  the *sole orphan* error code, while `codeMaps.rule` declares the maps "total and
  injective".
- Probe **G** REFUSES `faultCause: host-invariant` (not in the enum), and probe
  **I** shows that borrowing `host-io` **ADMITs** — which is precisely the
  "semantically unrelated existing code" root forbade. An I/O failure and a host
  invariant violation are different remedies.

**Therefore a host-invariant fault is not representable today**, and that is a
genuine gap in the closed vocabulary rather than something I can route around.

**Smallest selected successor.** One `faultCause` member — `host-invariant` —
mapping to the **existing** `SYSTEM.OUTCOME.ILLEGAL_STATE`. It adds no error code,
no D9 class, no exit code and no reason code; it makes an already-published code
derivable and the maps total, which is what `codeMaps.rule` already asserts they
are. I will make this in `workflows/schemas/common.schema.json` and the workflow
model's `FAULT_TO_ERROR` — both in scope — and record the drift explicitly:
**`docs/coop/artifacts/d9-exit-contract.v1.14.json` is historical and its bytes
stay untouched**, so its own `faultCause` enum and `codeMaps` remain as inherited;
the successor D9 artifact is root's to own, and my source will name that exactly
rather than implying the artifact already says it.

If Codex prefers not to add the member at all, the honest alternative is that a
host-invariant fault has **no** representable termination and the contract must
say so — but that leaves §10 asserting a classification nothing can emit, which is
the same class of defect as the prose placeholders. I recommend the member and
will flag it prominently at the checkpoint for exactly this reason.

### What the tests must do differently

Root's criticism applies to my whole approach here: the new tests will
**instantiate and validate real public outputs** through the actual schemas —
`StepTermination`, `DomainDetail`, `DoctorResult` — with valid and invalid
controls, and will assert actor-dependent classification by *deriving* the
termination from an origin, not by comparing strings inside my own proposal. The
prefix whitelist is deleted.

---

## Preserved unchanged

Totality (five-coordinate match), derivation (`types` relation condition), the
raw-byte inventory boundary, RC-3, existential/positive use, the matrix-fixed
default and explicit overrides — all as assented. No new Control or repair
authority, no invented relation/fact/Coverage, no fabricated clone candidate, no
new public `DomainDetailCode`, and no change to historical D9 artifact bytes.

`public-detail-registry.v1.json` is treated as **normative source** this turn: the
14 aliases are a semantic correction I make and defend here, not a mechanical
record edit handed to root.
