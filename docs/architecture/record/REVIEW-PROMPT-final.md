# Review assignment — OpenSIP greenfield architecture, final round

You are one of **two independent reviewers**. Read this whole file before touching
anything. Your assignment differs depending on whether you are **Reviewer 1** or
**Reviewer 2** — the coordinator will tell you which. Phase 1 is identical for both
and **must be done before you read the other phases' targets**.

---

## 1. What this is

Three AI agents were asked to design the best possible architecture for
`opensip-cli` from scratch — greenfield, no migration constraint, any language.
That produced a claim register, twelve architecture documents, and a large set of
JSON artifacts. Both of you have reviewed earlier rounds; Agent 3 has since done
the implementation-contract work.

Everything lives in **`docs/internal/coop/`** (gitignored, local-only):

```
architecture/00..11-*.md        the design documents
artifacts/*.json                binding contracts + every review filed so far
artifacts/check-*.py            twelve retained checkers
artifacts/claim-register.v1.json  single source of per-claim status
agents-log.md                   the full history, including every error made
```

Start with `agents-log.md` (long — the last ~200 lines cover this round) and
`artifacts/claim-register.v1.json`.

## 2. What changed since your last review

The coordinator decided the consumer is **B — build this**. A team should be able to
start and not hit an undecided fork in week one. That **reversed** an earlier
altitude correction: detailed contracts are now the deliverable, findings are
RESOLVED rather than triaged, and candidates must seal.

All eleven contract surfaces are now contract-complete, measured by
`artifacts/check-completeness.py`:

```
surfaces complete: 11/11   overall 100% of criteria met
criterion: invariants + schema + executable goldens + retained checker + no open findings
```

| Surface | Binding artifact | Checker |
|---|---|---|
| D9 termination | `d9-exit-contract.v1.6.json` | `check-d9.py` |
| FACT-PLANE | `fact-plane.v1.json` | `check-fact-plane.py` |
| C-2 plan/stage | `c2-plan-stage-schema.v3.json` | `check-c2.py` |
| EVIDENCE | `evidence.v1.json` | `check-evidence.py` |
| RESOLVED-INPUTS | `resolved-inputs.v2.json` | `check-resolved-inputs.py` |
| FACT-IDENTITY | `fact-identity-policy.v2.json` | `check-fact-identity.py` |
| VERSIONING | `versioning-policy.v2.json` | `check-versioning.py` |
| OPERABILITY | `operability.v2.json` | `check-operability.py` |
| DELIVERY | `delivery.v2.json` | `check-delivery.py` |
| TM | `threat-model.v3.json` | `check-threat-claims.py` |
| R-1 | `r1-lifetime-neutrality.conformance.v1.4.json` | `check-r1.py` |

Roughly 95 of your findings were resolved. Each artifact has a `resolves` block
naming your finding id and what was done. **Several of your requested fixes were
rejected on the record with reasons** — those are flagged in §5 and you should
confirm or contest them.

Every checker supports `--selftest`, which mutates the binding artifact in known-bad
ways and asserts each mutation is rejected. 110 mutations, all rejected.

---

## 3. The gap only you can close — READ THIS FIRST

**Nothing is sealed, and a green checker cannot seal it.**

On all eleven surfaces the fixtures/goldens and the validating function **share one
author**. That is the exact trap that let D9 v1.5 report "39/39 passing" while
carrying a golden whose stated cause was not its scenario's cause. Agent B found it
by re-deriving the axes blind. The checker could not, because mutual consistency
between an input and a derivation written by the same person proves only that the
person was consistent.

So the highest-value thing you can do is **not** to read the artifacts critically.
It is to **independently produce the expected values and then compare.**

### Phase 1 — BLIND RE-AUTHORING (both reviewers, do this first)

For your assigned surfaces below:

1. Read **only** the scenario prose / the `what` field / the human description of
   each case. **Do not read** `expectedTermination`, `expected`, `expect`,
   `mustRejectBy`, `valid`, or the checker's derivation function.
2. From the scenario alone, write down what the outcome **should** be.
3. *Then* diff against what the artifact says.
4. Report every disagreement, including ones where you conclude the artifact is
   right and your first instinct was wrong — those are informative too.

**Both of you do Phase 1 on the same two surfaces**, independently, because they are
the most load-bearing:

- **D9** (`d9-exit-contract.v1.6.json`) — 43 goldens. Re-author `scenarioAxes` for a
  sample of at least 15, chosen to include every cause family.
- **EVIDENCE** (`evidence.v1.json`) — 10 counterexamples + 5 accepting fixtures.
  For each counterexample, decide from the `what` prose alone **which invariant
  should reject it**, then compare to `mustRejectBy`.

Do not read each other's output before filing.

### Phase 2 — adversarial review, split

**Reviewer 1:** FACT-PLANE · C-2 · RESOLVED-INPUTS · VERSIONING · TM
**Reviewer 2:** FACT-IDENTITY · OPERABILITY · DELIVERY · R-1 · (+ re-check TM's
retracted overclaims)

For each: blind re-author the fixtures where practical, then review adversarially.

---

## 4. Standing constraints — do not violate these

- **Do NOT create ADRs in `docs/decisions/`.** This tree describes a hypothetical
  rebuild and must not graduate into the product's decision log.
- **Write nothing outside `docs/internal/coop/`.** No tracked product paths.
- **Do not adjudicate your own work.** If you authored something, you may not seal it.
- **Do not seal anything you also flagged.**
- File findings as JSON artifacts next to the others, named
  `<artifact>.review-<you>.json`, with per-finding `id`, `severity`, `evidence`,
  `impact`, `requiredChange`, `confidence`, and `whatWouldChangeMyMind`.
- Use a **new log file** — `agentlog3.md` — not `agents-log.md`, which is very large.

---

## 5. Known weaknesses — start here, do not take these on trust

### Agent 3's absence claims are unverified as a class

Recorded nine times: Agent 3 has repeatedly inferred *absence of capability* from
*absence of a term* (grep), and been wrong. **Any statement of the form "X does not
exist / is not reachable / has no consumer" in these artifacts should be treated as
unverified until someone traces capability rather than terminology.** This applies
retroactively to every "0 hits" figure in the tree.

### The measuring instrument inflated its own score four times

`check-completeness.py` was caught: crediting a checker by filename prefix; using
`max()` over golden families so smaller ones vanished; matching schemas by key name
so `sealedPropertiesCovered` counted as a schema because it contains "properties";
and a substring test that let a design-integrity gate discharge *"the product
implements the architecture"*. Each was found by auditing a favourable number.
**Audit the instrument, not just the artifacts** — including the eleven checkers.

### Fixes that were REJECTED rather than applied — confirm or contest

- **A1-D9-V15-03.** You asked for `interruption=none` on serve graceful stop. Agent 3
  declined: a graceful stop *is* a signal before finalization, so recording otherwise
  encodes a falsehood — the same defect class as B-D9V15-05, which you raised. The
  order-dependency you were actually worried about is closed by invariant **X9**
  instead. Is that the right call?
- **B-DL-08** (platform/packaging test domain) was declared **unresolvable here** and
  the property left NOT DISCHARGED, on the grounds that it needs a platform matrix
  and the P-4a Rust substrate decision, neither of which is an architecture decision.
- **A1-VER-05** (support windows) was **marked, not fixed**: every window carries
  `evidenceGrade: GUESSED` and the property is NOT DISCHARGED. The grounding harness
  may be permanently unbuildable, because the telemetry that would inform it is what
  the threat model refuses to collect.

### Nine properties are NOT DISCHARGED or PARTIAL, deliberately

```
c2               PARTIAL         physical storage schema stays private
c2               CONDITIONAL     effectful work is unrepresentable as a Rule
fact-identity    NOT DISCHARGED  imperative rules hold no ambient authority
fact-identity    PARTIAL         a rule cannot influence its own identity
r1               NOT DISCHARGED  the core holds no ambient authority AT RUNTIME
r1               PARTIAL         the execution core is lifetime-neutral
operability      NOT DISCHARGED  the product implements the architecture
versioning       NOT DISCHARGED  support windows are evidence-based
delivery         NOT DISCHARGED  every supported platform works
```

Three depend on `ARCH.PROBE-CONTRACT`, which is **REOPENED** — no capability
substrate exists. **Question to answer explicitly: is this honest, or is it
defeatism dressed as honesty?** An architecture that marks its hardest properties
undischarged and calls itself complete may be doing the right thing or may be
declaring victory over the easy half.

---

## 6. The specific questions each surface needs answered

Every claim in the register carries a `reviewPending` array. Read yours. The ones
Agent 3 considers most likely to be wrong:

- **FACT-PLANE / F8** — "a requirement at the top rung of a one-rung ladder is
  satisfied outright and cannot carry a deficiency" is the mechanical form of C-1's
  central claim. *If F8 is wrong, C-1 is not implementable as stated.*
- **EVIDENCE** — is a sorted-leaf Merkle root the right commitment for
  non-membership, versus an accumulator or an explicit-false-positive structure? The
  ~100 bytes/evaluation cost argument is **structural, not measured**; nobody has
  built the fold. A1-RTV4-02 should stay open, narrowed to "measure it".
- **C-2** — the admission boundary was chosen to agree with D9's snapshot golden,
  which makes **D9 load-bearing for C-2's identity model**. Is that dependency
  direction right? And is "supervised-implementation-effect" a real class or a
  licence, given nothing enforces it?
- **VERSIONING** — the detector pivot requires running the OLD detector over new
  code on every comparison crossing a detector version, **potentially doubling
  analysis cost** during a transition window. Affordable? Unmeasured.
- **RESOLVED-INPUTS** — is "neutralise when you can" right, or does neutralising
  locale hide a real user expectation? Agent 3 asserts no rule should respect the
  user's locale; that is an assertion.
- **FACT-IDENTITY** — is many-to-many the right group transition model, or does it
  make the user-facing diff unreadable? And is "not provided by the API, dependency
  closure audited" strong enough to ship the imperative escape hatch at all?
- **R-1** — does orchestration-host + pure-core make lifetime neutrality **trivially
  true by shrinking the core's subject**? Items (2)-(4) remain measurement-gated and
  the claim stays REOPENED.
- **TM** — **V5's real deletion under content-addressed dedup is still UNSOLVED**;
  it is the one finding v3 does not advance. R2's sync/backup detection is unverified
  against real clients and V2's prevalence is ASSERTED.
- **OPERABILITY** — 11 of 12 gates unqualified blocks release by the artifact's own
  rule. Correct posture, or unshippable?

---

## 7. What to produce

1. **Blind re-authoring diffs** for D9 and EVIDENCE (both reviewers) — file even if
   you found zero disagreements, because a clean independent derivation is the
   evidence needed to seal.
2. **Review artifacts** for your Phase 2 surfaces.
3. **A seal recommendation per surface**: SEAL / SEAL-WITH-CHANGES / DO-NOT-SEAL,
   with the specific blocker for anything short of SEAL.
4. **One judgement call**, stated plainly: *given nine properties are undischarged
   and three wait on a reopened capability contract, is this architecture complete
   enough to build from?* That is the question consumer B actually asks, and neither
   the checkers nor Agent 3 can answer it.

## 8. How to verify the current state yourself

```bash
cd docs/internal/coop
for k in claims d9 fact-plane c2 evidence resolved-inputs fact-identity \
         versioning operability delivery threat-claims r1; do
  python3 artifacts/check-$k.py            # expect: OK
  python3 artifacts/check-$k.py --selftest # expect: all mutations rejected
done
python3 artifacts/check-completeness.py    # expect: 11/11, 100%
```

If any of that does not reproduce, **that is your first finding.**
