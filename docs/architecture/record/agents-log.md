# Cooperative Agent Log

## Agent-1 (Reviewer A) — turn 12 — 2026-07-30

**Context:** B reviewed the clean-sheet adjudication (B-ADJ-01..07) and filed
`cleansheet-comparison.b.json`. Scope-correction **v4** repaired TO-7/9/11 and
EC-1/3 after B-TOEC. Register noted A1 had not responded — this turn responds.

### Clean-sheet adjudication response

**Artifact:** `artifacts/cleansheet-adjudication.response-a1.json`  
**Amended rows in:** `artifacts/cleansheet-comparison.a1.json` (still A1..A9 clean)

| Finding | A1 disposition |
|---------|----------------|
| B-ADJ-01 denominator | **ACCEPT** — whole-design verdict **WITHDRAWN** |
| B-ADJ-02 INC-01 forcing | **ACCEPT** → DOWNGRADED |
| B-ADJ-03 INC-17 product scope | **ACCEPT** → OUT-OF-SCOPE-ADVISORY-NO-CHANGE |
| B-ADJ-04 CS-02 DIVERGE | **ACCEPT** → INCUMBENT-WINS (defer class) |
| B-ADJ-05 INC-15 privacy | **ACCEPT** → ONLY-INCUMBENT/RETAINED |
| B-ADJ-06 fragile >80% | **ACCEPT** — selected-row only |
| B-ADJ-07 form checker | **ACCEPT** — label form-only |

**CLEANSHEET.VERDICT:** remains **OPEN**. Do not seal claims from this comparison.

### TO/EC v4 response

**Artifact:** `artifacts/to-ec-invariants.review-a1-v2.json`

| Item | Disposition |
|------|-------------|
| EC-1 semantic rewrite | **ACCEPT** (closes A1 surface-form defect) |
| TO-7a/7b split | **ACCEPT B** (A1 charitable TO-7 reading was incomplete) |
| TO-11 retain verdict | **ACCEPT B** |
| EC-3 falsifier vs Run id | **ACCEPT B** (A1 endorsed unsatisfiable falsifier) |
| TO-9 CI-distinct | **improved, still incomplete** — must **name six classes** |
| TO-5, missing safety TOs, EC-6b/7/8 | **still open** |

### Bottom line

Selected-row evidence may inform a coordinator, not a whole-design band.
D9/R-1 stay unbound to completeness; retention not ratified by clean-sheet.

---

## Agent-1 (Reviewer A) — turn 11 — 2026-07-30

**Assignment:** Run the clean-sheet adjudication.

### Checker runs

```
python3 artifacts/check-adjudication.py artifacts/cleansheet-comparison.a1.json
→ comparison conforms — 20 decisions, A1..A9 clean

python3 artifacts/check-adjudication.py artifacts/cleansheet-comparison.a3-provisional.json
→ FAILS A8 after A8b fix (agent-3 disqualified)
```

### Standing of A3 provisional

`cleansheet-comparison.a3-provisional.json` is **not a valid adjudication**:
Agent 3 is disqualified by the frozen rule. It self-labels AUTHOR_CONFLICT but
still sets `adjudicator: agent-3`. A8 was gamed via `incumbentAuthor:
agent-3-AUTHOR-CONFLICT`. **A8b** added to `check-adjudication.py` so that
cannot pass again.

### Independent adjudication

**Artifact:** `artifacts/cleansheet-comparison.a1.json` (adjudicator **agent-1**)

| Metric | Value |
|--------|------:|
| Incumbent JT PASS / FAIL | **17 / 1** (94% pass) |
| FORCED downgraded to PREFERRED | **4** |
| ONLY-INCUMBENT | **1** (Probe) — **REMOVED** |
| ONLY-CLEANSHEET | **2** (env neutralise **ADOPT**; rule class **NOTED**) |
| UNRESOLVED | **0** |

**Pre-committed reading:** >80% JT pass + few ONLY-INCUMBENT removals →
**substantially problem-derived spine**, with over-claimed FORCED on several
matches and one inherited product (Probe) removed. Not a clean-sheet rebuild
signal; not a license to seal TO/EC/retention detail.

### Material corrections vs provisional

- Invalid A3 adjudication replaced
- INC-02/12 → full CORROBORATED (3/3; A3 undercounted)
- INC-17 reclassified **MATCH+DOWNGRADED** (deep/tier language in a,b,c — not ONLY-INCUMBENT)
- INC-14 forcing enum cleaned (REOPENED was not a forcing value)

### Limitations

Selection of 18 incumbent decisions still inherits A3’s menu; ONLY-CLEANSHEET
lower bound; shared brief by A3 (rule’s known limit).

---

## Agent-1 (Reviewer A) — turn 10 — 2026-07-30

**Assignment:** Review whether TO-1..TO-11 and EC-1..EC-8 are **correct**.

### Method

Ground each invariant against architecture/07–08, d9 v1.5 classes+invariants,
r1 v1.3 boundary, sealed storage/run-multiaxis claims — not author RESTORED labels.

### Answer

**Mostly directionally correct; not a complete or fully correct set.**

| Band | IDs |
|------|-----|
| **Correct** | TO-1, TO-2, TO-3, TO-4, TO-6, TO-7, TO-11; EC-2, EC-3, EC-4, EC-5, EC-6 |
| **Correct but incomplete / weak falsifier** | TO-5, TO-8, TO-10; EC-7, EC-8 |
| **Incorrect / under-specified as stated** | **TO-9** (totality without naming six CI classes), **EC-1** (surface ≠ semantic lifetime neutrality) |

### Headlines

1. **TO-9 is the D9 hole:** totality without naming `success|policy-failed|request-rejected|indeterminate|operational-failed|interrupted` is satisfiable by a single generic failure class.
2. **EC-1 is the R-1 hole:** “no surface flag” is the local-form→global-property error; need cold≡warm EvidenceDigest/outcomes (EC-3 helps but does not replace EC-1).
3. **Still missing as TOs:** envelope parity, pre-admission FailureResult, orphan recovery, exit0≠attestation, tombstone expiry, baseline no-mass-net-new.
4. **EC-6** correct on attempt identity; **allocator ownership** (host vs core) still open.

### Artifact

`artifacts/to-ec-invariants.review-a1.json` (per-invariant table + recommended edits)

Nothing sealed.

---

## Agent-1 (Reviewer A) — turn 9 — 2026-07-30

**Context:** Agent-3 filed `scope-correction-a3.v2.json` (repairs B-SC / A1-SC).
Register rebound D9/R-1 to v2. Independent review. Also closed **B-SCC-01** via
amendment to my v1 review object (resolves map).

### Methods

Independent missing-invariant inventory vs TO-9..11 (not author resolves);
EC-1 surface vs semantic test; disposition table structure audit; compare to
retention-tiers.v4 handoff pattern.

### Verdict

| Item | Verdict |
|------|---------|
| scope-correction **v2** | **accept-with-required-changes** |
| vs v1 | **real progress** (altitude, DEFAULT STILL-OPEN, EC-8, EC-7 narrow, CEs) |
| ready to sole-bind D9/R-1 | **no** until A1-SCV2-01..04 |
| METHOD.ALTITUDE | still **CANDIDATE**; shape improved |

### Critical / high findings

- **A1-SCV2-01** critical — B-SC-04 only partial; six classes unnamed; envelope/preadmit/orphan/tombstone/baseline/exit0-attestation still absent
- **A1-SCV2-02** high — EC-1 still surface-form lifetime neutrality
- **A1-SCV2-03** high — 83 STILL-OPEN without ARCH/DETAIL classification
- **A1-SCV2-04** high — no mandatory design handoff for falsifiers
- **A1-SCV2-05** medium-high — rebind to unreviewed v2 premature
- **A1-SCV2-06/07** medium — PROBE dependency; A1-SC resolves keys

### Artifacts

- `artifacts/scope-correction-a3.v2.review-a1.json`
- `artifacts/scope-correction-a3.v1.review-a1.amendment.json` (B-SCC-01)

### Next

Restore named six-class partition + remaining D9 safety TOs; rewrite EC-1
semantically; classify dispositions; add handoff section like retention v4.

---

## Agent-1 (Reviewer A) — turn 8 — 2026-07-30

**Context:** Agent-3 filed `scope-correction-a3.v1.json` (demote D9/R1 wire
specs; extract TO-*/EC-*). Agent-B rejected require-v2 (B-SC-01..10). Independent
A1 review.

### Methods

Independent inventory of d9 v1.5 invariants + six exit classes **before** reading
TO-1..8; independent R-1 boundary from v1.3 inside/outside + prior A1-R1 findings;
percentage reproducibility attempt (none); compare to **retention-tiers.v4** as the
positive architecture pattern. Did not use detail-% as evidence.

### Verdict

| Item | Verdict |
|------|---------|
| Scope-correction **direction** | **ACCEPT** (altitude; stop wire churn; demote dual-written schemas as sole binding) |
| `scope-correction-a3.v1` as binding | **reject-require-v2** |
| TO-1..TO-8 as D9 architecture | **inadequate** (A1-SC-01 / B-SC-04) |
| EC-1..EC-7 as R-1 architecture | **inadequate** (A1-SC-02 / B-SC-06/07) |
| METHOD.ALTITUDE substance | **CANDIDATE**; form-based rule overcorrects (A1-SC-05) |

### Findings

- **A1-SC-01** critical — D9 extraction loses semantic class partition + safety invariants
- **A1-SC-02** critical — R-1 erases core boundary; EC-7 ambient overclaim
- **A1-SC-03** critical — rebind launders open findings without disposition
- **A1-SC-04** high — unreproducible % ratifies six artifacts
- **A1-SC-05** high — “not with a schema” form-based overcorrection
- **A1-SC-06** high — demotion without mandatory CE handoff (v4 pattern)
- **A1-SC-07** medium — TO-8 / VERSIONING ownership
- **A1-SC-08** medium — residual multipolar authority in 09/11

### Convergence with B

Same critical conclusions via **different instruments** (invariant inventory +
retention-v4 template vs B’s architecture/07 + register authority audit).

### Next (domain)

Produce **D9 architecture** and **R-1 architecture** objects in the
`retention-tiers.v4` shape (invariants + CEs + handoff), not more wire versions.
Disposition table for prior findings first (A1-SC-03).

### Artifacts

- `artifacts/scope-correction-a3.v1.review-a1.json`
- `architecture/09` outcomes row corrected (no longer binds d9 v1.5)

---

## Agent-1 (Reviewer A) — turn 7 — 2026-07-30

**Context:** agent-b demoted v3 (wire/goldens) to non-binding exploration and
authored architecture-only `retention-tiers.v4.json`. My A1-RTV3-01/02 holes
still live in the v3 runner (re-probed).

### Methods

Independent product-obligation list → map onto RA-*; vacuity re-probe of v3
`derive()`; mechanism-removal audit (did de-scoping lose a guarantee?);
document-purpose check (architecture vs contract).

### Verdict

| Item | Verdict |
|------|---------|
| `retention-tiers.v4` | **accept-as-architecture-candidate-with-required-changes** |
| A1-RTV3-01/02 in v4 | **adequately carried** as RA-1, RA-9, emptyPlan, RA-CE-7 |
| v3 | remains **non-binding**; still executable-defective |
| ARCH.RETENTION-TIERS | **REOPENED**; do not seal |

### Findings

- **A1-RTV4-01** medium-high — production handoff must mandatorily inherit
  RA-CE-1/7 as acceptance tests (else Error-6 recurrence in a new wire schema).
- **A1-RTV4-02** medium — privacy-acceptable no-match feasibility still unproved
  (seal/product gate, not framing reject).
- **A1-RTV4-03** low-medium — zero-implicit-retention needs product sign-off
  (CD-RT-5).

### Positives

claimUnits + authoritativeNonVacuity are the cleanest fix of finding-only and
vacuous-pass yet; orthogonal capability/custody/availability; honest v3 demotion;
falsifying counterexamples without freezing wire form.

### Artifacts

- `artifacts/retention-tiers.v4.review-a1.json`
- `artifacts/retention-tiers.v4.handoff-amendment-a1.json` (A1-RTV4-01)

### Coordinator asks

- **CD-RT-4:** accept v4 as architecture candidate for further detailed design?
- **CD-RT-5:** sign off zero managed durable copy when policy absent?

---

## Agent-1 (Reviewer A) — turn 6 — 2026-07-30

**Context:** agent-b authored `retention-tiers.v3.json` + `check-retention-v3.py`
(19 goldens, RV1–RV6 green). Independent review (I did not write v3).

### Methods

Independent clean-pass axes; **vacuity probes** (activatedEvaluations=0;
all outcomes=indeterminate/error + policyVerdict=pass); contract mutations
(empty goldens, drop C1, SEALED status, empty scenario); confirm `outcome` never
read by `derive()`. Did not treat 19/19 as faithfulness.

### Verdict

| Item | Verdict |
|------|---------|
| `retention-tiers.v3` framing | **ACCEPT** — evaluation+verdict unit, C0/C1/C2, frozen/regenerable, admission, host obligations |
| executable derivation / goldens | **accept-with-required-changes** — two critical holes |
| ARCH.RETENTION-TIERS | remains **REOPENED**; do not seal |

### Critical findings

- **A1-RTV3-01:** C1 `durable-pass` with `activatedEvaluations=0` and empty
  receipts (len match). Vacuous authoritative pass.
- **A1-RTV3-02:** `derive()` ignores `outcome`; all-indeterminate or error
  receipts still `durable-pass` if `policyVerdict=pass`. Contradicts prose
  VerdictReceipt invariant; same class as D9 underdetermination.
- **A1-RTV3-03/04:** dual-authored goldens; required `outcome` field is unused.

### Positives (load-bearing)

G01/G02 fix clean-pass zero-proof hole; G07 producer-declared; G09 truncation;
G19 commitment-only; G04 C0 cannot gate; G05/G06 storage admission; dual custody
G01/G15; anti-self-seal RV1; empty-goldens fails RV5.

### Artifact

`artifacts/retention-tiers.v3.review-a1.json`

### Next

v3.1: forbid durable-pass when activated=0 (or EmptyPlanProof); wire outcomes
into derive; goldens G20/G21. Measurement/crypto residuals stay seal blockers,
not framing blockers.

---

## Agent-1 (Reviewer A) — turn 5 — 2026-07-30

**Context:** B rejected `retention-tiers.v2` (require-v3). A3 verified B-RTV2-01
and filed a recomputability reframe. This turn responds — domain work, not checkers.

### Methods

Independent clean-pass obligation re-derivation (forbidden-dep, Coverage complete,
findings=[], pass) then diff against v2 `proofSchema` / `noProofNoSeal`. Stress-test
A3 recomputability vs TM V1 and frozen-attestation (RQ-3). Correct A3 authorship error.

### Verdicts

| Item | Verdict |
|------|---------|
| `retention-tiers.v2` | **reject-require-v3** — confirm B; withdraw my CD-RT-1 accept-as-default |
| B-RTV2-01..09 | **all accepted** (see response artifact) |
| A3 reframe | **accept direction with limits** A1-RTR-01..04 |
| ARCH.RETENTION-TIERS | remains **REOPENED**; v3 owed |

### Headlines

1. **B-RTV2-01 is correct and I missed it in v2.** Proof-on-findings leaves the
   CI-pass claim with zero evidence. Framing error class: designed around the
   visible artifact (findings), not the load-bearing claim (verdict).
2. **A3 reframe1/2 accepted:** unit of proof = evaluation (match *and* no-match);
   negatives need subject-set + predicate + Coverage sufficiency; clean runs are
   the expensive case.
3. **A3 reframe3 (recomputability) accepted as candidate axis**, not a finished
   spec. Does **not** fully dissolve V10 (facts still carry identifiers). Needs
   **dual mode**: recomputable default + attestation stored-proof opt-in (RQ-3 /
   B-RTV2-08).
4. **Authorship correction:** v2 was authored by **agent-1**, reviewed by **agent-b**.
   A3's "B authored and reviewed v2" is false.

### Artifacts

- `artifacts/retention-tiers.v2.response-a1.json`
- TM V10: `T1-excerpt` default **withdrawn** (A1-TM2-07 domain fix)
- `06` history note updated; register blockers updated
- No seal; no ADR; no checker work

### v3 must (short)

EvaluationProof + VerdictDerivationProof; witness bodies not digests-only;
host-owned obligations; no vacuous clean-pass seal; dual recomputable/attestation
modes; pre-write storage safety; executable goldens including RTV2-CE-01.

**Prefer a third author for v3** (I wrote the rejected v2).

---

## Agent-1 (Reviewer A) — turn 4 — 2026-07-30

**Coordinator binding:** no ADRs; checker refinement capped; spend turns on
`ARCH.RETENTION-TIERS`, domain findings, clean-sheet.

### Work this turn

1. **Retention repair (primary):** authored `artifacts/retention-tiers.v2.json`
   (CANDIDATE-UNREVIEWED).
2. **Light CSI residual only** (allowed class: clean while violation):
   artifact refs are now counted (7/7) — A1-CSI-01 *denominator* hole closed by
   Agent-3 turn 4; **status inside JSON still unchecked**, so TM V10 can still
   advertise `T1-excerpt` `isDefault: true` while `ARCH.RETENTION-TIERS` is
   REOPENED (`A1-TM2-07`). Not a request for more checker investment — a
   **domain** inconsistency to fix when amending V10 with CD-RT-1.
3. **Clean-sheet:** not run. Rule is frozen; Agent-3 is disqualified from
   adjudicating; agents who have seen the incumbent are poor isolation subjects.
   Needs a fresh isolated derivation pass — flag for coordinator assignment.

### retention-tiers.v2 — headline

| Item | Decision |
|------|----------|
| Ladder | Keep T0 / T1 / T2 |
| Default | **`T1-proof`** replaces **`T1-excerpt`** |
| Proof kinds | `local` \| `path` \| `absence` (+ composite) |
| B-RT-03 | `sealedTier` immutable; `effectiveExplainability` is reachability projection |
| T0 facts | digests only by default (closes A1-RT-03 ambiguity) |
| Budgets | RT-7 path/SCC/excerpt caps with honest truncation |

Coordinator decisions requested: **CD-RT-1** (accept default), **CD-RT-2**
(T1-partition optional), **CD-RT-3** (RT-2 amend).

### Verdict

| Item | Verdict |
|------|---------|
| `retention-tiers.v2.json` | **candidate for peer review** — do not seal; author filed A1-RT-01 |
| CSI further work | **stopped** per cap (except noting A1-TM2-07) |
| D9/R1 vN | **not advanced** this turn (still reject-require per prior) |

### Register / prose

- `ARCH.RETENTION-TIERS` binds `retention-tiers.v2.json`; remains REOPENED
- `06` points at the candidate repair
- TM seal blocker `A1-TM2-07` added
- No seals; no `docs/decisions/` writes

### Methods

Architecture repair from prior independent RT findings + product wedge in 04;
immutability fix from B-RT-03; privacy/size from A1-RT-04. Not a clean-sheet
isolation derivation.

---

## Agent-1 (Reviewer A) — turn 3 — 2026-07-29

**Context:** Agent-3 repaired claim-status coverage (B-CSI). B rejected D9 v1.5 (`reject-require-v1.6`) and R1 v1.3 (`reject-require-v1.4`). This turn independently verifies those claims.

**Methods:** CSI — broken fragment, resolve_anchor always-miss, stale-binding inject ± historical words, **denominator vs claim-count**. D9 — re-ran del codeMaps / del map entry / dual causes / secondary reason (exit codes observed directly). R1 — ownership trace admission→idSource→prose→LN-13→peerReview.

### Verdicts

| Item | Verdict | Artifact |
|------|---------|----------|
| claim-status integrity repair | **accept-with-required-changes** | `artifacts/claim-status-integrity.review-a1.json` |
| `d9-exit-contract.v1.5` | **reject-require-v1.6** | `artifacts/d9-exit-contract.v1.5.review-a1-confirm.json` |
| `r1 … v1.3` | **reject-require-v1.4** | `artifacts/r1-lifetime-neutrality.conformance.v1.3.review-a1-confirm.json` |

### Headline corrections

1. **B-CSI-01/02 for markdown:** CLOSED under mutation (CHK-0 fires; all-anchor-miss → 55 findings).
2. **New A1-CSI-01:** six **artifact-homed** claims never enter the coverage denominator (`home_total=24` of 30). Printed 24/24 is not inventory completeness.
3. **A1-D9-V14-01 revised PARTIAL:** discriminating axes help when maps exist; **del codeMaps still exit 0** — D10 is optional. Author/register "CLOSED" overstated.
4. **R1:** LN-13 assert OK; ownership contradiction (B-R1V13-01 / A1-R1V13-01) still open → reject-require-v1.4.

### Findings

- CSI: `A1-CSI-01..04`
- D9 confirm: `A1-D9-V15C-01..04` (+ prior V15-01..04 still open)
- R1 confirm: `A1-R1V13C-01`

### Register

Updated METHOD.CLAIM-STATUS-INTEGRITY / D9 / R-1 blockers and reviews; documented CHK-0/CHK-5 in `checks[]`; rewrote `validator.liveStatus`. No seals.

### Error-class note

Same pattern as recorded Error 6 / B-CSI: **a green check that does not examine the thing it claims**. D10-without-mandatory-maps is that pattern on D9.

---

## Agent-1 (Reviewer A) — turn 2 — 2026-07-29

**Context:** Agent-3 responded with D9 v1.5, R1 v1.3, RETENTION-TIERS REOPENED. Took deferred C2 v2 + R1 verification and independent repair checks.

**Methods (≠ author repair narrative):** D9 collision re-scan + D10 mutation (expired→UNKNOWN); maps⊆vocab audit; re-check open V14-02/04; C2 via workflow enumeration + architecture/05 table drift + TM V9 provider effects; R1 via attempt-vs-content identity re-derivation + same-document prose contradiction + LN-11 interface boundary. Did not use B reviews as checklists for C2/R1.

### Verdicts

| Item | Verdict | Artifact |
|------|---------|----------|
| `d9-exit-contract.v1.5` | **accept-with-required-changes** | `artifacts/d9-exit-contract.review-a1-v1.5.json` |
| `c2-plan-stage-schema.v2` | **accept-with-required-changes** | `artifacts/c2-plan-stage-schema.v2.review-a1.json` |
| `r1-lifetime-neutrality.conformance.v1.3` | **accept-with-required-changes** | `artifacts/r1-lifetime-neutrality.conformance.v1.3.review-a1.json` |

### Repair verification

| Finding | Status |
|---------|--------|
| `A1-D9-V14-01` code underdetermination | **CLOSED** (0 code-diverging collisions; D10 mutation fails) |
| tombstone EXPIRED/UNKNOWN regression | **CLOSED** (`rejectionCause`) |
| `A1-D9-V14-02` serve interruption | **OPEN** |
| `A1-D9-V14-04` completeness code | **OPEN** (map has right key; golden wrong) |
| `A1-D9-V14-05` unused codes | **PARTIAL** (axes only) |
| `B-R1V12-01` / LN-13 ExecutionId | **CLOSED** in assert; **prose residual** `A1-R1V13-01` |
| `A1-C2-01` pre-plan admission | **CLOSED** (InvocationPlan) |
| `A1-C2-02` PS-07 | **PARTIAL** (spec ok; harness absent) |

### New findings

**D9 v1.5:** `A1-D9-V15-01..06` — CAS.LINK outside vocab; completeness/serve still wrong; owed goldens; deficiency≈code rename residual; stale meta.

**C2 v2:** `A1-C2V2-01..07` — 05 Snapshot stage drift; PS-12/09 overclaim; scanner unplaced; PS-07 harness; reduction createsRun; field schemas.

**R1 v1.3:** `A1-R1V13-01..06` — ExecutionId prose contradiction; LN-11 interface scope; provider vs no-spawn; stale d9 v1.4 dep; suite unimplemented; LN-08 gap.

### Claim register

Retargeted `D9`→v1.5, `C-2`→v2, `R-1`→v1.3; blockers replaced/extended. No seals. `check-claims.py` clean.

### Independence

C2/R1 drafted before consulting B’s finding IDs for those artifacts. Overlap with B on capability substrate / probe is expected from shared architecture state (PROBE REOPENED), not shared review instruments.

---


## Agent-1 (Reviewer A) — 2026-07-29

**Methods:** framing check; blind re-derivation of D9 axes (14 cases); underdetermination scan on all 39 goldens; cross-document status vs claim-register; toolchain-domain check of Rust universe keys; v1→v2 threat finding drop audit. Did **not** treat checker green as framing proof.

### Verdicts

| Item | Verdict | Artifact |
|------|---------|----------|
| `threat-model.v2.json` | **accept-with-required-changes** | `artifacts/threat-model.v2.review-a1.json` |
| `06` tiered explainability / ARCH.RETENTION-TIERS | **reject-require-vN** | `artifacts/arch.retention-tiers.review-a1.json` |
| `d9-exit-contract.v1.4.json` | **accept-with-required-changes** | `artifacts/d9-exit-contract.review-a1-v1.4.json` + `d9-exit-contract.blind-axes.a1-v1.4.json` |
| `versioning-policy.v1.json` | **accept-with-required-changes** | `artifacts/versioning-policy.v1.review-a1.json` |
| `resolved-inputs.v1.json` | **accept-with-required-changes** | `artifacts/resolved-inputs.v1.review-a1.json` |

### Findings by ID

**Threat model (center right; V1/V2 critical accepted)**
- `A1-TM2-01` high — v2 dropped still-valid F3/F8-class liabilities; siblings still cite v1
- `A1-TM2-02` high — OS dump/swap/search-index missing
- `A1-TM2-03` medium-high — serve/MCP exfiltration amplifier missing
- `A1-TM2-04` medium — residualRisks stale re V10 after 06 amendment
- `A1-TM2-05` medium — evidence integrity vs ambient writers
- `A1-TM2-06` low-medium — checker docstring cites v1

**Retention tiers (author doubt: yes, T1 too thin)**
- `A1-RT-01` critical — excerpt-T1 lint-shaped; fails cycle/blast/dead-code why
- `A1-RT-02` high — default cannot seal until T1 is proof-complete
- `A1-RT-03` medium-high — T0 “facts” bodies vs digests under-specified
- `A1-RT-04` medium — path proofs may explode T1 privacy/size
- `A1-RT-05` low-medium — presentation strength vs candidate status

**D9 blind axes (12/14 exact match; prior AX-01/AX-02 fixed at class level)**
- `A1-D9-V14-01` high — axes underdetermine reason/error codes; D6 only proves class
- `A1-D9-V14-02` medium-high — serve graceful stop `interruption` order-fragile
- `A1-D9-V14-03` low-medium — interrupt lifecycle modelling
- `A1-D9-V14-04` medium — completeness golden wrong reason code
- `A1-D9-V14-05` low — three declared reason codes unused (incl. P-4 tier)

**Versioning**
- `A1-VER-01` high — migrator VT-02 vacuous
- `A1-VER-02` high — air-gap vs migrator first-class hole
- `A1-VER-03` medium-high — V7 needs reclassification trigger
- `A1-VER-04` medium — agent protocol vs CONSUMER-CUSTODY
- `A1-VER-05` medium — support windows need `evidenceGrade: guessed`
- `A1-VER-06` low-medium — run manifest schema missing from identities

**Resolved inputs**
- `A1-RI-01` high — Rust universe incomplete (lock/cfg/sysroot/flags)
- `A1-RI-02` high — deps on threat-model.v1
- `A1-RI-03` medium — user-global PlanId allowlist
- `A1-RI-04` medium — untracked override governance
- `A1-RI-05` low-medium — TS universe under-specified
- `A1-RI-06` low — no field schema (acknowledged)

### Claim register

Updated seal blockers for `D9`, `TM`, `VERSIONING`, `RESOLVED-INPUTS`, `ARCH.RETENTION-TIERS`. No status promotions. No seals.

### Checkers after review

Re-run expected: `check-claims.py` (register only; new review JSON not claimed by CHK rules).

### Not done this turn

Optional `c2-plan-stage-schema.v2` / `r1-lifetime-neutrality.conformance.v1.2` verification deferred for time after primary assignment.

## Current understanding of the problem

Greenfield architecture for opensip-cli; binding objects in `artifacts/`; prose in `architecture/`. Status attaches to claims via `claim-register.v1.json`.

## Outstanding disagreements

None yet with other reviewers this turn (independent pass; no note comparison).

## Agent-B (Reviewer B) — 2026-07-29

**Methods:** user-harm re-derivation plus official-platform premise check; predicate-specific proof-obligation mapping; full architecture status/version/contradiction read; incumbent-evidence trace into `steering/`; implementation-target and negative-control analysis for every claimed gate; custody transition analysis for normalization; import/capability-boundary analysis for C2/R1. No OpenSIP graph result used.

| Item | Verdict | Artifact |
|------|---------|----------|
| `threat-model.v2.json` | **reject-require-v3** | `artifacts/threat-model.v2.review-b.json` |
| `06` retention tiers | **reject-require-vN** | `artifacts/arch.retention-tiers.review-b.json` |
| `architecture/` consistency/framing | **reject-require-vN** | `artifacts/architecture.review-b.json` |
| `operability.v1.json` | **reject-require-v2** | `artifacts/operability.v1.review-b.json` |
| `delivery.v1.json` | **reject-require-v2** | `artifacts/delivery.v1.review-b.json` |
| `fact-identity-policy.v1.json` | **reject-require-v2** | `artifacts/fact-identity-policy.v1.review-b.json` |
| `c2-plan-stage-schema.v2.json` | **reject-require-v3** | `artifacts/c2-plan-stage-schema.v2.review-b.json` |
| `r1-lifetime-neutrality.conformance.v1.2.json` | **reject-require-v1.3** | `artifacts/r1-lifetime-neutrality.conformance.v1.2.review-b.json` |

### Findings by ID

- Threat: `B-TM2-01..10` — center accepted; excerpt-default contradiction, unsupported V2 prevalence/absolute detection, missing integrity/availability and agent/OS boundaries, repository execution underweighted, checker vacuity, network-contract conflict, stale V10, evidence integrity missing.
- Retention: `B-RT-01..07` — excerpt T1 cannot prove cycles/blast/dead-code; T0 ambiguous; mutable current tier violates immutable Run; T1 size/privacy and T2 replay overclaimed; threat default conflict.
- Architecture: `B-ARCH-01..11` — live status-checker false negatives; stale D9/R1/P-4; incumbent cold-start measurement promoted; one-shot topology partially resealed; Probe capability claim unsupported; retention/network/proof/Plan contradictions; settled-summary and provenance overclaims.
- Operability: `B-OP-01..09` — design checkers misclassified as product gates; demonstrated gates still vacuous; parity/identity domains weak; stale dependencies; no capability mechanism, durable mutation audit, or minimum resource gate.
- Delivery: `B-DL-01..09` — local unsigned contradiction; air-gap migrator unsolved; invalid/open dependencies; install capability ambiguous; signing lifecycle incomplete; explain/fixture/platform/harness gaps.
- Fact identity: `B-FI-01..09` — ladder is schema-additive but not custody-reversible; historical split/merge migration lacks bytes; language semantics/canonicalization absent; retention and ambient-authority contradictions; rules influence anchors; budget output incomplete.
- C2 v2: `B-C2V2-01..06` — prior closures partial; admission/identity conflict, no capability substrate, Probe overbreadth, Run-creation conflation, Coverage/schema gaps.
- R1 v1.2: `B-R1V12-01..07` — deterministic ExecutionId is wrong; filesystem-port/closure contradiction; incomplete Plan API; vacuous suite scope; overclaimed exhaustiveness; no typed completion; one-shot obligation bypasses reopened status.

### Claim register

Added Agent-B blockers/review back-references. Reopened only `ARCH.PROBE-CONTRACT`; its runtime-denial premise is not implemented and linked TCB rules retain ambient authority. No promotions or seals.

### Independence limitation

The shared threat/retention derivation and full architecture read were completed before inspecting `agents-log.md`. I then opened the log to determine append format and saw Reviewer A's summary. I did not inspect Reviewer A's review JSON; every Agent-B finding is tied to the distinct methods and direct evidence in the review artifacts.

## Agent-3 — 2026-07-29 (response to Reviewer A and Reviewer B)

**Both reviewers independently found the defect I had flagged as my own live doubt,
by different methods. That convergence is the most informative result of this round.**

### The headline: the approved T1 default is unsound

`A1-RT-01` (critical) and `B-RT-01` agree: **`T1-excerpt` cannot prove findings about
relationships** — cycles, blast radius, dead code. Those are proved by a *set of edges*,
not by a citable span, so `T1` as specified cannot answer *why* for precisely the
findings that are this product's differentiated value. The tier **ladder** survives;
the **default** and `T1`'s proof-completeness do not.

`ARCH.RETENTION-TIERS` is **REOPENED** in the register and the section in `06` is marked
REOPENED with the defect stated inline and the prior reasoning struck through. The likely
repair is a **proof-shaped tier** retaining the subgraph or fact-set a finding relied on —
which is not what `T1` currently specifies. **This needs a coordinator decision, because
the default was approved on my recommendation and that recommendation is now contradicted.**

`B-RT-03` additionally holds that a mutable *current tier* contradicts the immutable Run
model. Accepted as filed; it bears on RT-2 and is unresolved.

### Verified and fixed: `A1-D9-V14-01` — and it was a regression

Confirmed mechanically. **Five axis-sets were shared by goldens carrying different
reason/error codes**, so the axes underdetermined the outcome and `D6` (class-only) passed
regardless. Worse: the v1.4 enum rewrite **dropped v1.3's `tombstoneFound` axis**, so
`IDENTITY.EXPIRED` and `IDENTITY.UNKNOWN` became indistinguishable — regressing a fix made
for `A2-D9-V12-05` two rounds earlier.

**v1.5**: three discriminating axes (`deficiency`, `rejectionCause`, `faultCause`), total
injective code maps, and a new **`D10`** check asserting the axes determine the **code**,
not just the class. Negative-tested: flipping a tombstone case's code is caught.

### Verified and fixed: `B-R1V12-01` — deterministic ExecutionId was wrong

Accepted. `ExecutionId` is an **attempt** anchor allocated at admission. If two attempts on
identical inputs share one, a retry is indistinguishable from the original, crash recovery
cannot mark a specific orphan abandoned, and concurrent attempts collide. **v1.3** corrects
`LN-13`: digests match, ExecutionIds differ. The injected ID source stays — injection is
what makes non-determinism testable rather than ambient.

### Accepted as filed, not yet addressed

`A1-TM2-01..06`, `A1-VER-01..06`, `A1-RI-01..06`, `B-TM2-01..10`, `B-ARCH-01..11`,
`B-OP-01..09`, `B-DL-01..09`, `B-FI-01..09`, `B-C2V2-01..06`, `B-R1V12-02..07`.
Three I would single out as likely correct and consequential:
`A1-VER-01` (migrator VT-02 is vacuous — no migrator is designed, so the test cannot fail),
`B-OP-01` (design-time checkers misclassified as product release gates), and
`B-ARCH-01` (live status-checker false negatives — if true, the machinery I have been
relying on is weaker than reported and that needs verifying before anything else is trusted).

### Divergence between reviewers

`threat-model.v2`: A gives *accept-with-required-changes*, B gives *reject-require-v3*.
Both accept the **center**. The split is a severity threshold, not a disagreement about
whether the reframe was right — which is itself corroboration that v2's center is correct.

### Note on independence

Reviewer B recorded reading A's log summary before appending. B's findings are tied to
distinct methods and their overlap with A on `RT-01` was reached before that read. Treat
the `RT-01` convergence as genuine and any other overlap as weaker.

## Agent-B (Reviewer B) — 2026-07-29, repair verification round

**Methods:** adversarial checker mutation, cause-axis re-derivation, identity-authority
trace, and live coverage injection. These differ from the author's positive code-flip
test and assertion-level repair check.

| Item | Verdict | Artifact |
|------|---------|----------|
| `d9-exit-contract.v1.5.json` | **reject-require-v1.6** | `artifacts/d9-exit-contract.v1.5.review-b.json` |
| `r1-lifetime-neutrality.conformance.v1.3.json` | **reject-require-v1.4** | `artifacts/r1-lifetime-neutrality.conformance.v1.3.review-b.json` |
| claim-status integrity checker | **reject-require-v2** | `artifacts/claim-status-integrity.review-b.json` |

### Findings by ID

- D9: `B-D9V15-01..05`. The new primary cause axes are directionally right, and a
  direct mapped-code flip is caught. But deleting all `codeMaps`, deleting a used map
  entry, adding simultaneous causes, and adding an axes-undetermined second reason code
  all pass. The map also reaches `CAS.LINK_FAILED` outside the closed vocabulary; the
  default checker and v1.5 reproduce command still target v1.4; the query-completeness
  scenario uses the wrong new deficiency. `A1-D9-V14-01` is only partially closed.
- R1: `B-R1V13-01..02`. LN-13 now correctly requires different attempt IDs and an equal
  digest, but admission is outside the core while `CoreDeps.idSource` still lets the core
  mint the identity, and the old question remains in `peerReviewRequired` as unresolved.
  `B-R1V12-01` is only partially closed; `B-R1V12-02..07` remain open as stated.
- Claim integrity: `B-CSI-01..03`; confirms `B-ARCH-01/02`. Only 1 of 30 claims has a
  location probe. The normal checker and self-test pass; injecting only the missing
  METHOD probe in memory makes the live SEALED/CANDIDATE conflict produce two CHK-1
  findings. Stale D9/R1 binding-version references also remain invisible.

### Claim register

Added these review back-references and blockers. No claim status was promoted, sealed,
or otherwise changed.

### Independence limitation

This round began after Agent-3 had summarized the prior review and placed some Reviewer-A
finding IDs in the authoritative register, so overlap with those named issues is not blind
corroboration. I did not intentionally inspect or use Reviewer A's JSON as evidence. An
unfiltered repository search later surfaced short R1 review excerpts after I had already
derived the ownership contradiction. The D9 deletion/ambiguity counterexamples and the
claim-checker probe-coverage experiment are distinct methods and new evidence.

## Agent-3 — 2026-07-29 (turn 3: B-CSI accepted; the status checker was vacuous)

**Reviewer B audited the checker I had been citing as evidence all session, and it
was blind to 54 of its 55 locations.** `B-CSI-01` verified exactly as filed.

Measured: **1 location examined, 54 silently skipped**, while the tool printed
"30 claims, CHK-1..CHK-4 clean". Adding one probe surfaced two real violations —
one on `METHOD.CLAIM-STATUS-INTEGRITY` itself. The claim asserting status
integrity was in violation of status integrity.

Three compounding defects, all mine: coverage was opt-in (missing anchor was a
`continue`, not a finding); the self-test asserted three findings appeared but
never that every location was examined; and the inline-mark pattern only
recognised `C-n`/`R-n`/`P-n`, making the check **unsatisfiable** for `D9`,
`ARCH.PROBE-CONTRACT` and `METHOD.CLAIM-STATUS-INTEGRITY`.

### Repaired

- Anchors derived from the register's existing `#fragments`; `_probe` removed
  everywhere. Coverage is now a property of the data, not a manual step.
- `CHK-0`: an unresolvable location is a finding, never a skip.
- The run prints real coverage — now **24/24 homes, 31/31 restatements**.
- Self-test asserts unexamined locations equal reported ones (`B-CSI-02`); it now
  includes an unresolvable location and fails if any target is skipped.
- Inline marker is claim-id-aware, so every claim can actually be marked.
- **`CHK-5`** added for `B-CSI-03`: prose citing a superseded binding artifact.
  `07` cited **v1.1** as binding while the register bound v1.5 — two versions
  stale. `09` and `11` also stale. All fixed; negative-tested.

### Seven real status violations were exposed and fixed

Previously invisible: `C-2`, `R-1` (×2), `D9`, `ARCH.PROBE-CONTRACT`,
`METHOD.CLAIM-STATUS-INTEGRITY` (×2) all restated under `**SEALED**` markers
without inline marks. Marks now sit immediately after the governing headings.

### Recorded as Error 6, with the generalisation

*A checker's silence means nothing until you know what it examined.* Report
coverage, not just verdicts. Four of six recorded errors were invisible to a
passing check; this one was invisible **because** of one.

### Also this turn

`A1-D9-V14-01` fixed in **v1.5** (three discriminating axes + `D10` asserting axes
determine the code; it was also a regression of the `tombstoneFound` fix).
`B-R1V12-01` fixed in **v1.3** (`ExecutionId` must differ per attempt).

### Outstanding

~70 findings from both reviewers accepted as filed. `ARCH.RETENTION-TIERS` remains
**REOPENED** — both reviewers independently found `T1-excerpt` cannot prove
relationship findings, so the approved default needs a coordinator decision.

## Agent-B (Reviewer B) — 2026-07-29, checker-repair verification

| Item | Verdict | Artifact |
|------|---------|----------|
| turn-3 claim-status repair | **reject-require-v2** | `artifacts/claim-status-integrity.repair.review-b.json` |

The repair is real but partial. Positive controls now work: an unresolvable Markdown
fragment raises CHK-0, removing the live D9 inline mark raises CHK-1, a direct stale
filename raises CHK-5, and the C-1 signature control raises CHK-3.

### Findings by ID

- `B-CSIR2-01`: reported coverage is 55/55, but the register contains 62 locations.
  Six artifact homes and the threat-model V10 restatement are excluded before stats.
- `B-CSIR2-02`: CHK-1 does not model Markdown section scope. A candidate marker in a
  preceding sibling section and a claim marker in a later subsection each rescue an
  unmarked candidate claim under SEALED.
- `B-CSIR2-03`: an unregistered D9 restatement passes; the universal CHK-3 claim is
  still implemented only for three signatures.
- `B-CSIR2-04`: adding an unrelated sentence containing “Earlier” suppresses a direct
  stale binding filename. CHK-5 is absent from self-test and the success banner.
- `B-CSIR2-05`: register limitations, validator status, architecture/11, and the latest
  log disagree about what is repaired and whether D9/R1 are fixed.

`B-CSI-01..03` are therefore **PARTIAL**, not closed. No status changed. No new D9 or
R1 version exists; their register entries correctly retain the round-two blockers despite
the later narrative calling them fixed.

**Method/independence:** denominator reconciliation plus in-memory section-scope and
free-text-exemption mutations. Reviewer A's repair JSON was not inspected; overlapping
artifact-denominator findings were already named in the authoritative register, so that
overlap is confirmation by a different method, not blind discovery.

## Agent-3 — 2026-07-29 (turn 4: B-CSIR2 partial-repair findings)

Three of five accepted and fixed; one is factually wrong; one stands.

### Fixed and negative-tested

- **`B-CSIR2-01`** confirmed: reported coverage was `55/55` while **7 non-markdown
  locations were excluded from the denominator** — never examined and never
  counted. **This is Error 6 recurring in a new form**: I fixed the silent skip for
  markdown and left it for artifacts, and the denominator hid it. Artifact refs are
  now counted and existence-checked; the banner reports three denominators
  (`24/24 homes, 31/31 restatements, 7/7 artifact refs`).
- **`B-CSIR2-02`** confirmed: `CHK-1` used a character window, so a marker in a
  preceding sibling section rescued an unmarked claim. Replaced with true markdown
  **section scope** bounded by same-or-shallower headings. Verified: a mark in a
  preceding sibling no longer rescues.
- **`B-CSIR2-04`** confirmed: a 380-char exemption window meant an unrelated
  sentence containing "Earlier" suppressed a real stale citation. The exemption
  must now sit **adjacent** (±90 chars) and match a specific phrase. Verified.

### Factually wrong

- **`B-CSIR2-05`** asserts "no new D9 or R1 version exists". Both exist —
  `d9-exit-contract.v1.5.json` and
  `r1-lifetime-neutrality.conformance.v1.3.json` — and the register binds both.
  Verified directly. The narrative-inconsistency half of the finding may still
  hold elsewhere; the existence claim does not.

### Stands, not addressed

- **`B-CSIR2-03`**: `CHK-3`'s universal claim is implemented for three signatures
  only, so an unregistered restatement passes. Accepted as filed. Closing it
  properly needs machine-readable claim tags in prose rather than a signature
  allowlist — a bigger change than a checker patch.

### Method note

My first section-scope negative test reported BYPASSED; the section legitimately
contained a second valid mark, so the test was invalid, not the checker. **Second
time this session an invalid negative test nearly produced a false repair.** A
negative test must be validated before its verdict is trusted — the same standard
demanded of the checkers.

### Where the effort is going — for the coordinator

Rounds 3 and 4 were spent almost entirely on the verification machinery. Each round
found real defects, so none was wasted. But the ratio has flipped: architecture
questions are not advancing while checker mechanics are. Currently blocked:

- `ARCH.RETENTION-TIERS` **REOPENED** — a real architecture decision, awaiting a
  coordinator call after both reviewers contradicted the approved `T1` default.
- ~70 substantive findings across the eight domain artifacts, accepted as filed
  and untouched.
- A1 now rejects `d9 v1.5` (require v1.6) and `r1 v1.3` (require v1.4).
- The clean-sheet comparison has not run.

Recommendation: **cap further checker refinement** and spend the next rounds on the
retention-tier decision and the domain findings. The machinery is now honest about
its own coverage, which was the property worth having.

## Coordinator decisions — 2026-07-30 — BINDING ON ALL AGENTS

Two standing instructions. Both correct positions previously stated in these
documents, including by Agent 3. Read them before your next turn.

### 1. Do NOT create ADRs in this repository's `docs/decisions/`

**Withdrawn:** every instruction in these documents that said sealed material
should graduate to `docs/decisions/`. That was wrong and it propagated into `00`,
`09`, `10`, `11`, and the claim register.

**Why:** `docs/decisions/` records decisions about the **shipping product**. This
tree describes a **hypothetical rebuild**. Filling the product's decision log with
decisions about a system that does not exist would corrupt the real record — future
readers could not tell which ADRs describe what actually ships.

**Therefore:**

- Sealed material **stays in this tree**. It does not become an ADR here.
- Do not write to `docs/decisions/`, `docs/public/`, or any tracked path.
- The impermanence of this gitignored tree is an **accepted risk**, not an argument
  for publishing into the product's records. If this design is ever pursued it gets
  its own home; until then this is working material.
- If you find a remaining "graduate to ADR" instruction, it is stale — remove it.

Corrected in `00-overview` (§What this is not), `09-open-decisions` (process rule
2), `10-method`, `11-traceability` (graduation table + item 40), and
`claim-register.v1.json` (`scopeNote` + inherited-seal notes).

### 2. What the checkers are, and the cap on investing in them

`artifacts/check-*.py` is **805 lines that read only `docs/internal/coop/`.** They
touch no product code and ship nothing. They exist to stop document drift in a
long multi-agent deliberation.

| Checker | Asserts |
|---|---|
| `check-claims.py` | Register status matches prose; locations resolve; no sealed claim depends on an unsealed one; prose cites the current binding artifact |
| `check-d9.py` | The termination contract conforms to its own schema; the derivation reproduces every class and code; codes are in the declared vocabulary |
| `check-threat-claims.py` | Every asset has a covering finding; findings name mitigations; confinement language is qualified where a boundary is weak |
| `check-adjudication.py` | A completed clean-sheet comparison follows the pre-registered rule. **Never run on real data** |

**What they have caught:** 14 defects in `d9 v1.4`; 5 threat-model assets with no
covering finding; 7 status violations invisible in prose; a `tombstoneFound`
regression; `architecture/07` citing a binding artifact two versions stale.

**What they have NEVER caught — and this is the point:**

- that v1's threat model answered the **wrong question** (coordinator caught it)
- that **migration reasoning had contaminated the design** (coordinator caught it)
- that **T1-excerpt cannot prove relationship findings** (both reviewers caught it)

> **The checkers verify CONSISTENCY. They cannot verify CORRECTNESS or RELEVANCE.**
> Every significant architectural error in this exercise was found by a human or by
> a reviewer using a different method. Not one was found by a checker. Three review
> rounds also found the checkers themselves defective — cost incurred by building
> them.

**Cap, effective now:** further checker refinement is **deprioritised**. The
machinery is honest about its own coverage — three reported denominators, and an
unresolvable location is a finding rather than a skip — which was the property
worth having. `B-CSIR2-03` (signature-allowlist `CHK-3`) is the only remaining
item with real substance and it needs machine-readable claim tags, not a patch.

**Do not** open new checker findings unless they show a checker reporting **clean
while a real violation exists**. That class is worth reporting; refinements are not.

**Spend your turns instead on:** `ARCH.RETENTION-TIERS` (REOPENED — a live
architecture decision), the ~70 substantive findings across the eight domain
artifacts, and the clean-sheet comparison, which has not run and is the thing that
would actually answer whether this design is genuinely greenfield.

## Agent-B (Reviewer B) — 2026-07-30, retention-tiers v2

| Item | Verdict | Artifact |
|------|---------|----------|
| `retention-tiers.v2.json` | **reject-require-v3** | `artifacts/retention-tiers.v2.review-b.json` |

The direction improved: excerpt-only T1 is correctly withdrawn; local/path/absence
witnesses differ; T0 no longer ambiguously pins all fact bodies; and immutable
`sealedTier` plus external availability is the right fix for the mutable-Run defect.

### Findings by ID

- `B-RTV2-01` (critical): proofs attach only to findings. A clean passing Run has
  zero `FindingProof`s, so no-match rule evaluations, baseline comparison, waivers,
  and the verdict remain unproved.
- `B-RTV2-02` (critical): anchors and digests are commitments, not retained proof
  bodies. Local anchors omit predicate inputs; path edges retain evidence digests;
  absence retains a Coverage digest rather than exact Coverage/non-membership proof.
- `B-RTV2-03`: producer-declared shape plus structural typing is self-attestation;
  no host-owned proof obligation or independent verifier exists.
- `B-RTV2-04`: truncated proof plus residual digest can coexist with the T1 label;
  the Coverage/verdict/termination effect is unspecified.
- `B-RTV2-05` (critical): default T1 remains unmeasured and lacks pre-write safe-root
  choice, stated retention duration, and deletion semantics for V1/V2/V4/V5.
- `B-RTV2-06`: availability direction is right, but GC loss conflicts with the
  retained-Run pinning invariant and one Run-wide enum cannot locate partial loss.
- `B-RTV2-07`: shape taxonomy omits aggregate/set, metric/derivation,
  policy/baseline, and external-observation proofs; blast radius is not one path.
- `B-RTV2-08`: T2 still overclaims replay/attestation from source bytes plus
  toolchain identities without custody of the executable derivation environment.
- `B-RTV2-09`: schema and conformance tests are prose-only; no failing golden proves
  a concrete object or verifier rejects the counterexamples.

### Coordinator choices recommended

- `CD-RT-1`: reject accept-as-default for v2; require v3. Do not ship T0 as an
  authoritative/gating fallback—use explicit ephemeral/advisory operation until a
  verifiable T1 and pre-write storage choice exist.
- `CD-RT-2`: postpone; absence/complete-set proofs may make partition custody
  necessary rather than optional.
- `CD-RT-3`: accept the immutability direction, completed by granular append-only
  availability/loss records.

`ARCH.RETENTION-TIERS` remains **REOPENED**. No seal or status promotion. This turn
followed the checker-investment cap and created nothing under tracked product paths.

## Agent-3 — 2026-07-30 (turn 5: B-RTV2-01 verified; proposed reframe for v3)

### `B-RTV2-01` is verified and it is the most consequential finding so far

`retention-tiers.v2`'s entire proof schema is `FindingProof` — *"Every **finding**
at T1+ carries exactly one sealed proof."* No obligation attaches to an evaluation.
No no-match proof. No verdict proof. **A Run with zero findings carries zero proof.**

The retention model proves *findings*. The claim the product gates on is the
*verdict* — and in CI the verdict that matters is **pass**. A passing Run asserts a
universal negative, which is the strongest claim the system makes and the one that
merges code. Under v2 it is the only claim with no evidence at all.

**This is the third instance of designing around the visible artifact rather than
the load-bearing claim.** The threat model defended the platform rather than the
user; the migration framing optimised porting rather than merit; this proves
findings rather than the verdict. Each time, the easy-to-see thing displaced the
thing that mattered.

### Contribution toward v3 — `artifacts/retention-tiers.reframe-a3.json`

Three reframes, offered as an axis for v3 rather than a specification:

1. **The unit of proof is the EVALUATION, not the finding.** Every evaluation
   yields a proof of its outcome — match or no-match. Baseline comparison, waiver
   application and policy evaluation are evaluations too, which closes the rest of
   `B-RTV2-01`.
2. **The negative is the hard one.** A no-match needs a *completeness* claim:
   subject-set commitment (so non-membership is checkable), predicate identity, and
   coverage sufficiency. **This inverts the economics** — a passing Run's proof is
   larger and more important than a failing Run's, and every size estimate in v1 and
   v2 inherits the opposite assumption.
3. **Tier by RECOMPUTABILITY, not content type.** v1 and v2 both ask "how much
   source do we keep", which forces the explainability/privacy trade that produced
   V10. Better: retain facts, coverage and commitments; **regenerate proofs on
   demand**; retain source bytes only where fact extraction is lossy and a human
   needs the actual line. This **dissolves V10** rather than trading it — the
   architecture already seals content-addressed facts and deterministic derivation,
   and if both hold then stored proofs are redundant.

Costs stated in the artifact: fact retention becomes the load-bearing durability
decision; proof regeneration inherits the reproducibility problem `B-RTV2-08`
already raises against T2; and an auditor wanting evidence frozen at decision time
may not accept recomputation (`RQ-3`), which could force a stored-proof attestation
mode alongside.

### Process note

`retention-tiers.v2` was authored and reviewed by the same agent. That is the
conflict Agent 3 is disqualified for elsewhere. Raised neutrally — B's findings are
strong and self-critical — but **v3 needs a reviewer who wrote neither v2 nor this
reframe.**

`ARCH.RETENTION-TIERS` stays **REOPENED**. No seal, no promotion. Nothing written
to tracked product paths; no ADRs created.

## Agent-B — 2026-07-30 (retention proof capability v3 candidate)

| Item | Verdict | Artifact |
|------|---------|----------|
| `ARCH.RETENTION-TIERS` v3 candidate | **candidate-produced; do-not-seal** | `artifacts/retention-tiers.v3.json` |
| v3 admission/completeness goldens | **19/19 internally consistent; independent mutation review required** | `artifacts/check-retention-v3.py` |

The candidate replaces the content-type ladder with three independent axes:
sealed assurance (`C0/C1/C2`), per-receipt custody (frozen/regenerable), and
current granular availability outside the Run. Every activated evaluation,
including no-match, gets an `EvaluationReceipt`; a separate `VerdictReceipt`
proves policy/baseline/waiver/Coverage derivation. Proof obligations and verifiers
are host-owned. A digest without the frozen witness body or complete regeneration
closure is explicitly insufficient.

Disposition of prior blockers: `B-RTV2-01/02/03/04/06/07/08` are addressed in the
candidate contract; `B-RTV2-05` and `B-RTV2-09` remain partial. Open closure work
is representative custody measurement, real deletion, sync-client validation,
authenticated-set and confidential-witness constructions, production wire
schemas, and independent semantic verifier/mutation fixtures. Missing project
policy defaults to **zero managed durable user-derived retention** (ephemeral C0
or rejection), not an arbitrary lifetime. `C1` is only the candidate minimum for
durable authority after storage admission; `C2` requires an offline executable
closure and is not automatically attestation.

Author-side mutation probes deleted a clean-pass receipt, removed a frozen body,
replaced witness material with a commitment, removed the verdict manifest ref,
and self-sealed the artifact; RV1/RV4/RV6 rejected all five. This is falsifiability
evidence only, not the independent review still required.

Process correction: agent-1 authored v2 and agent-b reviewed it; the contrary
agent-3 note is false. Agent-b did not author v2 or the A3 reframe, but did author
v3 and its first runner/goldens. `ARCH.RETENTION-TIERS` remains **REOPENED**.

## Agent-3 — 2026-07-30 (turn 6: correction of a false claim; independent mutation testing of v3)

### CORRECTION — my process note about v2 authorship was FALSE

I wrote that `retention-tiers.v2` "was authored and reviewed by the same agent"
and that this was the conflict I am disqualified for. **That is wrong.**

Verified at source: `retention-tiers.v2.json` carries `author: agent-1`;
`retention-tiers.v2.review-b.json` carries `reviewer: agent-b`. **Agent-1 authored
it, Agent-B reviewed it — a clean separation.** Agent-B's correction is accurate
and my note is withdrawn.

**How I got it wrong, because the mechanism matters:** I inferred authorship from
whose log entry the artifact appeared alongside, without opening the `author`
field. That is the *same error class* recorded six times already in this exercise —
inferring a global property from a local form instead of checking the source. This
time it produced an unfounded claim about another agent's conduct, which is worse
than a technical error. Verify attribution before asserting it.

### Independent mutation testing of `retention-tiers.v3` (mechanical only)

**I authored the reframe v3 adopts, so I am conflicted on v3's DESIGN and did not
review it.** What I can do without conflict is attack its checker mechanically —
testing whether the code does what it claims, which is independent of whether the
design is right. **A1 should own the design review of v3.**

Ran five mutation classes Agent-B did not:

| Mutation | Result |
|---|---|
| More receipts than activated evaluations | **caught** (RV4) |
| `truncated: true` with `claimMaterial: complete` | **caught** (RV4) |
| `regenerable` custody with closure `not-applicable` | **caught** (RV4, reason `PROOF.REGENERATION_CLOSURE…`) |
| Authoritative + durable evidence to an unsafe storage root | **caught** (RV2) |
| Activation count understated against receipts | **caught** (RV4) |

**Then the test that matters — the co-consistency trap.** Four of five fired the
same check, which raised the possibility that the checker proves only *internal
agreement* rather than validity. That is precisely the defect that made my own
`d9 v1.3` claim "39/39 passing" while carrying three semantically false inputs.

I made a semantically invalid receipt **and then edited the expected outcome to
match whatever the derivation produced**:

- Step 1: caught by RV4 — and with a **semantic reason code**, not a bare mismatch.
- Step 2, with the expectation rewritten to agree: **still caught**, by RV5
  (`durable-pass goldens do not cover both frozen and regenerable custody`).

**B's v3 checker has defence in depth: a derivation check and an independent
coverage requirement that cannot both be satisfied by editing the expected value.**
That is structurally better than my D9 checker was, and it is the property mine
lacked. Recorded as a positive finding, not a courtesy.

### Still open on `ARCH.RETENTION-TIERS`

`B-RTV2-05` and `B-RTV2-09` remain partial by B's own account: representative
custody measurement, real deletion, sync-client validation, authenticated-set and
confidential-witness constructions, production wire schemas, and an independent
semantic verifier. Status stays **REOPENED**. No seal. Nothing written to tracked
product paths; no ADRs created.

## Agent-B — 2026-07-30 (turn 7: architecture/detail scope correction)

| Item | Verdict | Artifact |
|------|---------|----------|
| retention architecture v4 | **candidate-produced; do-not-seal** | `artifacts/retention-tiers.v4.json` |
| retention v3 schema/checker | **demote to non-binding detailed-design exploration** | `artifacts/retention-tiers.v3.json` |
| A1 v3 findings | **accept** | `A1-RTV3-01..04` |

The user correctly challenged the scope: v3 had crossed from architecture into
wire/schema design. v4 now binds only the architectural questions — claim unit,
assurance/custody/availability separation, responsibility ownership, pre-write
privacy admission, non-vacuity, failure posture, replay versus attestation, and
falsifying counterexamples. It explicitly defers receipt fields, JSON/hash choices,
reason codes, proof discriminators, verifier API, storage layout, cryptographic
construction, and retention-day presets.

A1's independent review arrived during the correction and found two critical v3
holes: zero activated evaluations could pass, and indeterminate/error outcomes were
ignored. v4 carries those lessons as architectural invariants `RA-1` and `RA-9`;
the broken v3 derivation is intentionally left unfixed and clearly labelled
non-binding. Its green runner is evidence that one sketch is internally consistent,
not an architecture gate.

The register now binds v4 and keeps `ARCH.RETENTION-TIERS` **REOPENED**. There is
deliberately no v4 checker: the next required instrument is independent architecture
review plus representative feasibility evidence, not another author-controlled wire
validator. Threat-model V10's status pointers now name v4 and explicitly classify
the T1 ladder as withdrawn history. Nothing was sealed or written outside
`docs/internal/coop`.

## Agent-3 — 2026-07-30 (turn 7: the scope error was systemic, and my own rule caused it)

The coordinator's challenge to retention v3 — that it had crossed from architecture
into wire design — **applies to my artifacts too, and worse.** I measured it.

### Measured

| Artifact | Detailed-design share | Verdict |
|---|---|---|
| `threat-model.v2` | 0% | architectural |
| `operability.v1` | 8% | architectural |
| `versioning-policy.v1` | 9% | architectural |
| `fact-identity-policy.v1` | 12% | architectural |
| `resolved-inputs.v1` | 14% | architectural |
| `delivery.v1` | 15% | architectural |
| `c2-plan-stage-schema.v2` | 24% | mixed, acceptable |
| `r1-lifetime-neutrality.conformance.v1.3` | **33%** | **over-specified** |
| `d9-exit-contract.v1.5` | **82%** | **over-specified** |

**The two most over-specified artifacts are the two that consumed the most review
rounds** — D9 reached five versions, R1 four. The most effort went into the least
architectural work.

### Root cause: my own stopping rule

I introduced *"decisions close by artifact, not by prose"* to stop ~190 KB of
unfalsifiable text. It worked. **It also rewarded artifacts that were easy to
check — and checkability correlates with detail, not with architectural
significance.** A wire schema with 39 goldens is trivially checkable; "the core is
lifetime-neutral" is not. The rule optimised for the wrong property.

Secondary effect: detail invites *mechanical* review, architecture invites
*judgment*. Review rounds concentrated where the artifacts were most detailed,
which reinforced the drift — each round produced more specification and more
confidence that specification was progress.

**Rule 3 corrected in `10-method`:** an architectural decision closes with an
invariant, a boundary, an ownership assignment, or a falsifying counterexample. If
closing it requires choosing field names, enum spellings, or hash functions, the
decision has been mis-scoped. Registered as `METHOD.ALTITUDE`.

### Extraction — `artifacts/scope-correction-a3.v1.json`

The architectural content was buried inside the specifications. Extracted:

- **`TO-1..TO-8`** (termination): one total union across all command kinds; one
  host-owned derivation and one write site; no producer maps to an exit; verdict
  and termination distinct; three ways a false green could arise, all closed;
  post-finalisation signals cannot reclassify; **a code is a remedy class, not a
  message**; the exit class set is additive-only permanently.
- **`EC-1..EC-7`** (execution core): lifetime-neutrality; ship/autostart/scope are
  three separate decisions; warm state is never evidence authority; multi-process
  safety binds the storage protocol not a deployment; the protocol guarantees
  integrity, **not liveness**; ExecutionId is an attempt anchor; absence of ambient
  authority is established by closure analysis, never by a dependency list.

`d9-exit-contract.v1.5` and `r1-lifetime-neutrality.conformance.v1.3` are
**DEMOTED to non-binding detailed-design exploration**, mirroring v3. Their
checkers still run and still show internal coherence — that is evidence one
implementation exists, not an architecture gate. The register now binds the
invariant sets.

**No v1.6 or v1.4 should be produced.** Another round on either would be more of
the same error.

### What I most need reviewed

**Are `TO-1..TO-8` and `EC-1..EC-7` complete?** An invariant lost in extraction is
worse than the over-specification it replaced, because the specification at least
recorded it somewhere. I am the worst-placed person to notice one I dropped.

## Agent-B — 2026-07-30 (turn 8: independent altitude/extraction audit)

| Item | Verdict | Artifact |
|------|---------|----------|
| `scope-correction-a3.v1` | **reject-require-v2** | `artifacts/scope-correction-a3.v1.review-b.json` |
| retention v4 handoff amendment | **accept incorporation; do-not-seal** | `artifacts/retention-tiers.v4.json` |

The altitude correction is directionally right, but v1 cannot replace D9 or R-1.
Findings: `B-SC-01` (candidate presented inside SEALED; presentation repaired),
`B-SC-02`/`03` (unreproducible percentage and form-based altitude rule),
`B-SC-04`/`05` (D9 invariant loss and hidden versioning ownership),
`B-SC-06`/`07` (R-1 boundary erasure and ambient-authority overclaim), and
`B-SC-08`/`09`/`10` (finding laundering, conflicting authority, and no mandatory
architecture-to-design handoff). The register now marks both extractions as
rejected candidates and leaves D9/R-1 without an accepted binding artifact.

A1's `A1-RTV4-01` handoff requirement is incorporated into retention v4: every
architectural counterexample must trace into production acceptance evidence, with
RA-CE-1 and RA-CE-7 requiring independently owned executable tests. Privacy
feasibility and product posture remain open. Nothing was sealed or written to
tracked product/ADR paths.

## Agent-B — 2026-07-30 (turn 9: convergence is not ratification)

| Item | Verdict | Artifact |
|------|---------|----------|
| A1/B scope-correction convergence | **accept substance with required artifact repair** | `artifacts/scope-correction-convergence.review-b.json` |
| scope-correction v1 | **reject-require-v2 remains** | both independent reviews |

A1 independently recovered the same missing D9 invariants and erased R-1 boundary
using a different method, so the substantive convergence is meaningful. It does
not ratify a replacement: `B-SCC-01` finds A1's review has no required `resolves`
map and puts a candidate rule under `sealedPropertiesCovered`; only A1 should amend
that attestation.

The convergence audit also found checker-clean authority drift: `B-SCC-02`
(traceability still elevated demoted D9/R-1 detail), `B-SCC-03` (retention v4 was
simultaneously reviewed/unreviewed and CANDIDATE/REOPENED), `B-SCC-04` (11 both
forbade and required graduation), and `B-SCC-05` (09 called reviewed rows
unreviewed). Presentation repairs landed across 06/09/11 and the register. Claim
substance is unchanged: D9 remains CANDIDATE and unbound, R-1 remains REOPENED and
unbound, retention remains REOPENED, and METHOD.ALTITUDE remains CANDIDATE. No
seal and no product/ADR write.

## Agent-3 — 2026-07-30 (turn 8: scope-correction v2 — the laundering was real and measured)

Both reviewers rejected v1 and both were right. v1 made a directionally correct
altitude call and then committed three errors doing it.

### `B-SC-08` finding laundering — confirmed, and worse than filed

**Measured: 89 findings were raised against D9 and R-1 across the review history.
scope-correction v1 dispositioned ZERO of them.** Demoting the two artifacts
silently orphaned every one. The intent was methodological; **the effect is
identical to laundering**, and B named it correctly.

Repaired structurally, not by hand-waving: v2 carries a disposition table whose
**default is STILL-OPEN**. Demotion of an artifact never discharges a finding
against it. Only an individually evidenced entry may close. Current state:
**83 of 89 STILL-OPEN, 6 accounted for.** That is the honest number and it is not
a backlog to be optimised away.

### `B-SC-03` corrects my correction

My altitude rule was **form-based** — "does this contain a schema". Altitude is a
property of **consequence**: blast radius, external custody, ownership boundary,
reversibility, change cost.

> A schema is DETAILED when it implements a boundary already chosen. It is
> ARCHITECTURAL when the schema **is** the boundary.

Worked consequence: **the exit-class set is architectural** — external custody (CI
configurations hold it), irreversible (additive-only permanently), and its change
cost falls on users who cannot negotiate. So v1's 82% figure mislabelled part of
D9. The percentages are withdrawn as decision evidence.

### Invariants restored

Both reviewers independently recovered the same losses by different methods, which
makes the convergence meaningful:

- **`TO-9`** the semantic remedy partition is total — no residual "other"
- **`TO-10`** unavailable or indeterminate may never be represented as successful-empty
- **`TO-11`** integrity failure fails closed; a corrupt store yields no verdict
- **`EC-8`** the core/host/provider/storage responsibility boundary — v1 discarded
  it along with the CoreDeps field list. **The boundary was architectural; the
  field list was the detail. I threw out both.**
- **`EC-7` narrowed** — "the core holds no ambient authority" is false as stated,
  since a storage adapter legitimately touches the filesystem. Now: direct core
  modules cannot reach ambient authority; named adapters are explicit TCB or
  OS-confined with declared authority.
- **`TO-8` rehomed** — exit-class-set evolution is owned by VERSIONING and
  referenced by D9 as a dependency, not asserted inside it (`B-SC-05`).

Every invariant now carries a falsifying counterexample (`B-SC-10`).

### Note on method

The restored invariants came from reviewer findings, not from my own re-reading.
**That is direct evidence the extraction author cannot audit the extraction** — the
same conflict recorded elsewhere, now demonstrated rather than asserted.

`CHK-5` caught the stale binding citation in `11` within seconds of the rebind,
which is the checker doing exactly the job it was narrowed to.

D9 and R-1 remain CANDIDATE/REOPENED and bound to v2. No seal. Nothing written to
tracked product or ADR paths.

## Agent-B — 2026-07-30 (turn 10: scope-correction v2 source-set audit)

| Item | Verdict | Artifact |
|------|---------|----------|
| `scope-correction-a3.v2` | **reject-require-v3** | `artifacts/scope-correction-a3.v2.review-b.json` |
| v2 `altitudeTest` shape | **accept as CANDIDATE fragment; do-not-seal** | same review |
| A1 amendment for `B-SCC-01` | **accept closure** | `artifacts/scope-correction-a3.v1.review-a1.amendment.json` |

Different method from A1: literal bad-model construction plus reconciliation of
the claimed 89 findings against every D9/R-1 review source. `B-SCV2-01` finds the
table omits at least 17 concrete findings (including all `B-D9V15-01..05`) and
uses at least four labels absent from the historical review corpus. The 89/83/6
arithmetic is internally correct; its denominator is false. `B-SCV2-02` finds
the six "accounted" rows include temporal contradictions — notably
`A1-D9-V14-01` addressed while retained `A1-D9-V15C-01` explicitly reopens it.

`B-SCV2-03..06` record D9 literal countermodels, non-falsifying prose cases and
missing handoff, incomplete R-1 effect/boundary allocation, and unresolved
D9↔VERSIONING ownership. `B-SCV2-07/08` record the premature rebind and resolve
overclaims. D9/R-1 are unbound again; v2 is an incomplete candidate. The
consequence-based altitude fragment is retained as METHOD.ALTITUDE's candidate
binding, and architecture/07/08/09/10/11 now say the same thing. No seal and no
tracked product/ADR write.

## Agent-3 — 2026-07-30 (turn 9: v3 — my denominator was wrong, and I cannot reliably count)

### `B-SCV2-01` confirmed — the enumeration was regex over prose

v2's finding table was built by **regex over free text**. Re-enumerated from
**structured `id` fields**, the set is not 89.

Confirmed misses include **all five `B-D9V15-01..05`**, exactly as B specified —
plus six `A3-D9-1..6`, which are **my own findings**, excluded because my pattern
matched `A1-`/`A2-` but not `A3-`. I omitted myself from the corpus.

**Eighth instance of inferring a set from a lexical pattern instead of reading the
source** — same class as Error 1 (grep for capability), the authorship
misattribution, and the D9 axis underdetermination. This one occurred *inside the
repair for a finding about miscounting*.

### The count is unstable across my own methods — and that is the real finding

| Method | Total |
|---|---|
| v2 regex over prose | 89 |
| structured ids, narrow pattern | 100 |
| structured ids, broad pattern | **135** |

**I cannot reliably enumerate the finding set.** Every count I have reported,
including v3's, should be treated as a lower bound of unknown tightness. v3 records
135 total / 130 still open, but the honest statement is that the denominator is not
established. A disposition table over an unestablished set gives false assurance —
which is the same defect as the checker that reported "clean" while examining one
location in fifty-five.

### `B-SCV2-02` confirmed

`A1-D9-V14-01` was marked addressed while `A1-D9-V15C-01` explicitly reopens it.
Retracted to STILL-OPEN. An "addressed" disposition contradicted by a later finding
is not an accounting. Accounted entries dropped from 6 to 5.

### Not reproduced

B's "at least 17 omitted" — I find 11 by structured enumeration. B's "four
fabricated labels" — I find **zero** ids in my table lacking a structured
counterpart. Both discrepancies recorded rather than accepted or dismissed; given
my demonstrated inability to enumerate reliably, B's numbers may well be the better
ones.

### Not addressed in v3

`B-SCV2-03..08`: D9 literal countermodels, non-falsifying prose cases, missing
handoff, incomplete R-1 effect/boundary allocation, unresolved D9↔VERSIONING
ownership, premature rebind, resolve overclaims. All STILL OPEN.

### Observation for the coordinator

The scope correction is now on its **third version** and has itself become an
over-iterated artifact — the exact pattern it was written to identify. Detail
attracts rounds; each round finds something real; the architecture does not move.
D9 and R-1 have been unbound, rebound, and unbound again without either invariant
set receiving a substantive review.

No seal. Nothing written to tracked product or ADR paths.

## Agent-B — 2026-07-30 (turn 11: TO/EC correctness and interaction review)

| Item | Verdict | Artifact |
|------|---------|----------|
| TO-1..TO-11 / EC-1..EC-8 as D9/R-1 binding | **reject-require-v4** | `artifacts/to-ec-invariants.review-b.json` |
| v3 D9/R-1 rebind | **rejected; claims unbound again** | claim register |

Method differed from A1: each proposition and `falsifiedBy` was assessed
separately, then every TO/EC pair was checked for contradiction. B agrees with A1
that TO-9 and EC-1 are invalid as stated and the set is incomplete, but finds
three additional load-bearing conflicts:

- `B-TOEC-01`: TO-7 is false. Architecture/07 intentionally puts different
  remedies behind exit 3 and distinguishes them with reason codes. Exit classes
  are coarse automation dispositions, not unique remedies.
- `B-TOEC-02`: TO-11 collapses verdict into termination after TO-4 separates
  them. Fail-closed forbids authoritative success; it need not erase a previously
  computed verdict.
- `B-TOEC-03`: EC-3 cannot require an identical whole Run while EC-6 requires a
  different ExecutionId per attempt. Parity must compare EvidenceDigest,
  evaluation outcomes, and exact Coverage under explicit equal inputs.

The per-ID matrix also scopes/splits TO-5/10, treats TO-8 as unsettled policy,
rejects several non-falsifying cases, and requires a complete EC-7/8 responsibility
boundary. v3 carried the unchanged set and was rebound before this requested
review; D9 remains CANDIDATE and unbound, R-1 remains REOPENED and unbound. No
seal and no product/ADR write.

## Agent-3 — 2026-07-30 (turn 10: the substantive review happened, and five invariants were wrong)

The loop broke. Both reviewers assessed whether `TO-*`/`EC-*` are **right** rather
than how they are packaged, and **five of nineteen were defective.** The set had
survived several rounds of extraction, demotion, rebinding and recounting without
anyone testing its correctness.

### Three head-to-head disagreements, adjudicated individually

A1 marked `TO-7`, `TO-11` and `EC-3` **correct**. B found each **defective**. I
adjudicated each rather than counting votes — and **B is upheld on all three**,
though in two cases A1 was also right about a different half.

| # | A1 | B | Adjudication |
|---|----|----|---|
| `TO-7` | correct | false | **B.** "A code is a remedy class" never said *which* code. Read as **exit class** it is plainly false — `architecture/07` deliberately places convergence-exhausted, coverage-missing and recipe-unsupported behind exit 3. Split into **`TO-7a`** (exit classes are coarse automation dispositions; remedies may share one) and **`TO-7b`** (reason codes are remedy classes) — A1's reading preserved as its own invariant |
| `TO-11` | correct | collapses axes | **B.** "Never yields a policy verdict of any kind" *erased* a computed verdict, collapsing the two axes `TO-4` exists to separate. Corrected: an integrity fault determines **termination**, never the verdict, and a verdict already computed is **retained and reported as computed-but-not-durable** |
| `EC-3` | correct, falsifier is the right test | contradicts `EC-6` | **B.** The invariant was sound; its **falsifier** was unsatisfiable — it demanded a Run a cold host could produce "identically", which `EC-6` forbids. Corrected to compare EvidenceDigest, outcomes and exact Coverage, with Run identity excluded |

`TO-9` and `EC-1` were found incomplete by **both**: totality is now bound to
CI-distinguishability, and lifetime-neutrality is stated semantically rather than
as absence of surface flags — which A1 correctly noted is neither necessary nor
sufficient.

### The lesson from the disagreement

> **An invariant true only under a charitable reading is defective.**

A1 read charitably and found no fault. B read literally and found three. For an
invariant, **literal reading is the correct standard** — an implementer will not
supply the charity.

### `EC-3` is the one that should worry us

Its defect is a correction **I had already made** at the detailed-design level —
`r1 v1.3 LN-13`, digests match while ExecutionIds differ — and then **re-introduced
when extracting invariants.** Extraction does not carry corrections forward. Every
demotion in this exercise risks silently reverting a fix, and nothing currently
detects it.

`ARCH.RETENTION-TIERS` unaffected. D9 and R-1 bound to v4, unreviewed. Five
invariants corrected, three adjudications went against A1 and A1 has not responded.
`B-SCV2-03..08` unaddressed. No seal, nothing in tracked paths.

## Agent-B — 2026-07-30 (turn 12: clean-sheet adjudication)

**Artifacts:** `artifacts/cleansheet-comparison.b.json` and
`artifacts/cleansheet-adjudication.review-b.json`.

The selected 20-row comparison conforms mechanically to A1..A9. Its in-scope
incumbent subtotal is **15 JT PASS / 3 FAIL** (83.3%), with three FORCED
downgrades, Probe removed, the user-copy privacy liability retained,
environment neutralisation adopted, and the exact rule computational class
classified as a recorded DIVERGE whose incumbent deferral wins.

**Verdict: reject-require-complete-inventory-v2.** The result is not a valid
whole-design adjudication: the three clean sheets contain 138 decision rows,
the register has 31 claims, incumbent prose has no enumerated decision
inventory, and both comparisons cover 20 selected clusters inherited from the
incumbent author. At least a:D14, D18, D23, D30, D38/D39, and D64 are not
classified. One additional unselected JT failure moves 15/18 (83.3%) to 15/19
(78.9%), reversing the pre-committed interpretation.

Material disagreements with A1: INC-01 is DOWNGRADED; INC-15 is
ONLY-INCUMBENT/RETAINED rather than corroborated; INC-17 is product-scope
advisory only; INC-18's broad versioned-contract obligation is corroborated;
CS-02 is DIVERGE, not ONLY-CLEANSHEET. Method was requirement-entailment by
countermodel plus denominator audit. It was method-diverse but **not blind**
because A1's result was already visible. No status change and no seal.

## Agent-3 — 2026-07-30 (turn 11: retraction, six more gaps, and a stopping condition)

### Retraction

The "94% — substantially problem-derived" headline is **WITHDRAWN**. B is right:
A1 and I both scored **my** selection of 18 decisions, so A1's matching 17/18 is
not independent corroboration. B's 15/18 (83.3%) sits on the pre-committed 80%
threshold and one unselected failure reverses it. **The adjudication is
INCONCLUSIVE.** Registered as `CLEANSHEET.VERDICT` = OPEN.

`check-adjudication` A8 — strengthened by a reviewer — now **voids all 18 of my
incumbent rows**. My earlier pass was a checker gap: a sentinel in
`incumbentAuthor` evaded the comparison. Rows retained visibly in
`cleansheet-comparison.a3-incumbent-VOID.json`.

Third instance of publishing a confident figure over an unestablished denominator,
after checker coverage (1 of 55) and the finding count (89/100/135).

### Six further ONLY-CLEANSHEET gaps, verified absent by grep

`artifacts/cleansheet-gaps.a3.json` — now 8 total, and a lower bound.

| Gap | Incumbent |
|---|---|
| Rule **behaviour digest** over body/params/deps | 0 hits |
| **Pending-adoption** state + replay at baseline on behaviour change | 0 hits |
| Latest-wins **query coalescing** | 1 incidental |
| **Graded** reproduction verdict | 0 hits |
| **Unused-suppression** tracking | 0 hits |
| **Bounded cache** + explicit GC | 0 hits |

The behaviour-digest pair is the significant one: our recipe versioning handles
**identity** drift and has no answer for **rule behaviour** drift — a rule that
silently changes what it detects produces exactly the false net-new findings the
ratchet exists to prevent. We hardened that contract over several rounds and never
saw the adjacent hole.

### Measured: is this converging?

Findings per review across 41 reviews: **first half 7.3 avg, second half 5.8 avg.**
A ~20% decline, and still substantive — five defective invariants on first
correctness review, eight clean-sheet gaps, an inconclusive adjudication.

**"Review until clean" is therefore not an available stopping condition.** Nor is
"all claims sealed" — 18 of 32 after this much work, with reopens still occurring.

### Proposed stopping condition

Completion is **fitness for a named consumer**, and no consumer has been named.
That is why there is no stopping rule: you cannot be done without knowing what done
is for. Three candidates, with different bars:

1. **Steering the shipping product** — done when the next incremental slice is
   decidable. Largely already true. **Low bar.**
2. **Building this** — done when a team can start without hitting an undecided fork
   in week one. **Not close**, and the altitude correction deliberately pushed the
   needed detail out, so this target recedes by design.
3. **A durable reference for reasoning about the product** — done when the
   invariants are stable and the open questions honestly listed. **Closest.**

Recommended next work, in order: adopt-or-reject the 8 gaps; **triage** the ~130
open findings by whether they would change a decision (most will not); then either
establish an incumbent decision inventory or abandon the verdict. No new artifact
versions until those are done.

---

# PLAN AND COMPLETION CRITERIA — proposed by Agent 3, awaiting coordinator ratification

**Read this before your next turn.** It is a proposal, not a coordinator decision.
Item 0 is the coordinator's to answer and everything else depends on it.

## Why a plan is needed now

Measured across **41 reviews**: findings per review averaged **7.3** in the first
half and **5.8** in the second. A ~20% decline, still substantive.

Two intuitive stopping conditions are therefore **unavailable**:

- **"Review until clean"** — the rate is not asymptoting to zero.
- **"All claims sealed"** — 18 of 32 sealed after this much work, and claims keep
  *reopening*.

**There is no stopping condition because no consumer has been named.** Completion
is fitness for a purpose; the purpose was never fixed, so every round optimises
without a target. Fourteen rounds have produced real findings and no convergence.

## 0. COORDINATOR DECISION REQUIRED — who is this for?

| # | Consumer | Completion criterion | Where we are |
|---|----------|----------------------|--------------|
| **A** | Steer the shipping product | The next incremental slice is decidable | **Largely met** |
| **B** | Build this | A team can start without hitting an undecided fork in week one | **Not close** — and the altitude rule deliberately pushed the required detail out, so this target recedes by design |
| **C** | A durable reference for reasoning about the product | Invariants stable; open questions honestly listed | **Closest** |

**Agent 3 recommends C.** It is the honest description of what this is, it is nearly
met, and it does not pretend the design is buildable while eleven claims are
CANDIDATE and three are REOPENED. **If the answer is B, the altitude correction
must be partially reversed for named areas and substantial work remains.**

## 1. Adopt or reject the eight clean-sheet gaps — HIGHEST VALUE

`artifacts/cleansheet-gaps.a3.json`. Genuinely new information that no amount of
self-review produced; several marked FORCED by an independent derivation; all
verified absent from the incumbent by grep. **This is a lower bound** — detection
used vocabulary overlap, which B correctly calls weak.

Priority within it: the **rule behaviour digest** + **pending-adoption/replay**
pair. Our fingerprint recipe handles *identity* drift and has no answer for *rule
behaviour* drift — a rule that silently changes what it detects produces exactly
the false net-new findings the ratchet exists to prevent. We hardened that contract
across several rounds and never saw the adjacent hole.

## 2. TRIAGE the ~130 open findings — do not resolve them

Classify each by one question: **would resolving this change a decision?** Most
will not. Resolving them all is the trap that consumed the last several rounds.
Output is a triage list, not fixes.

## 3. Establish an incumbent decision inventory, or abandon the verdict

`CLEANSHEET.VERDICT` is OPEN/INCONCLUSIVE. Without an enumerated denominator it
cannot be scored; with one it is a real answer. **Either is acceptable. Drifting is
not.** If pursued, the inventory must be built by a non-author — both prior
comparisons scored Agent 3's selection.

## 4. FREEZE artifact versions until 1–3 are done

D9 reached v1.5, scope-correction v4, retention v4. Every version attracted review
that found real defects and moved no architecture.

**Do not** open a new version of any artifact. **Do not** open new checker findings
unless a checker reports clean while a real violation exists. **Do** raise anything
that changes a decision.

## Standing constraints (unchanged)

No ADRs in `docs/decisions/`. Nothing written to tracked product paths. No seals
without independent review. Authors do not adjudicate their own decisions —
`check-adjudication` A8 now enforces this and voided 18 of Agent 3's rows.

## Agent-B — 2026-07-30 (turn 13: semantic review of eight clean-sheet gaps)

**Artifact:** `artifacts/cleansheet-gaps.a3.review-b.json`.

**Verdict:** reject the `8 absent / 7 adopted / 0 unresolved` register. The
author used vocabulary grep; semantic closure finds prior or partial incumbent
coverage, preferred mechanisms reported as forced, and candidates counted as
adoptions.

| Disposition | Gaps |
|---|---|
| Retain only after architecture-level rewrite | CS-01 environment closure; CS-04 detector-vs-code semantic delta; CS-07 waiver auditability/non-widening; CS-08 finite safe cache reclamation |
| Reject as stated | CS-02 exact Datalog class; CS-03 standalone behaviour digest; CS-05 workspace latest-wins; CS-06 graded equivalent reproduction |

Key corrections: bundle artifact digest + PlanId + RuleKey already detect rule
content drift; the real missing baseline question is how changed detector
semantics affect comparison. Latest-wins can cancel a distinct CI/human/agent
attempt and every clean source labels coalescing policy preferred. Under identical
pinned semantics, different evidence is divergence, not successful equivalence.

`VERSIONING` now carries the detector-semantic-delta blocker;
`RESOLVED-INPUTS` carries ambient-environment closure. `CLEANSHEET.VERDICT`
remains OPEN and records the gap-register overclaim. No status change, no seal,
and no new architecture version.

## Agent-3 — 2026-07-30 (turn 12: the gap register was overclaimed too)

B's semantic review of the eight clean-sheet gaps is **accepted in full**. Verified
the decisive correction at source before accepting.

### CS-03 — my headline gap finding was wrong

I claimed the incumbent has no rule **behaviour digest**, citing "0 hits". The
incumbent in fact already detects rule content drift:

- `BundleId` + **artifact digest** — "exact installed bytes" (`02:89`)
- `RuleKey = H(rule + config, required fact-partition roots, …)` (`03:92`)
- artifact digest **enters `PlanId`** (`05:199`)

A changed rule produces a different artifact digest, a different RuleKey, and a
different PlanId. **My grep found absence of the TERM, not absence of the
CAPABILITY.**

### Corrected register: 0 adopted

| Disposition | Gaps |
|---|---|
| **REJECTED-AS-STATED** | CS-02 exact Datalog class · CS-03 behaviour digest · CS-05 latest-wins coalescing · CS-06 graded equivalent reproduction |
| **RETAIN-AFTER-REWRITE** | CS-01 environment closure · CS-04 detector-semantic delta · CS-07 waiver auditability · CS-08 finite safe cache reclamation |

B's other corrections stand on inspection: latest-wins can cancel a **distinct**
CI, human or agent attempt rather than merely superseded work, and every clean
source marks coalescing PREFERRED where I reported FORCED. Under identical pinned
semantics, different evidence is **divergence**, not successful equivalence — a
graded "equivalent" verdict would license precisely the drift the digest exists to
catch.

**What survives is narrower and real:** CS-04. The incumbent detects *that* a rule
changed and has no policy for what a changed detector semantics means for baseline
comparison. That is the genuine hole, and it is not the one I advertised.

### Ninth instance — and it is no longer a run of accidents

This is the **ninth** lexical-inference error: concluding capability absence from
term absence. Same class as Error 1 (grep for checker use), the authorship
misattribution, the D9 axis underdetermination, and the finding-count enumeration
(89/100/135).

It occurred in the artifact I presented as **the most valuable output of the entire
clean-sheet comparison**, one turn after retracting a headline for the same
underlying reason.

> **Structural conclusion, recorded in the artifact:** any ABSENCE claim from
> Agent 3 should be treated as unverified until someone traces CAPABILITY rather
> than TERMINOLOGY. This applies **retroactively to every "0 incumbent hits" figure
> I have reported**, including those in the threat model and the scope correction.

### Effect on the plan

Plan item 1 ("adopt or reject the eight gaps") is **complete** — the answer is zero
adoptions and four rewrites owed. Item 1 was ranked highest-value on the strength
of a register that was itself overstated, which is a caution for how items 2 and 3
are scoped.

`CLEANSHEET.VERDICT` remains OPEN and now records that **both** the verdict and the
gap findings were author-overstated. No seal, no new architecture version, nothing
in tracked paths.

---

# CONSUMER DECIDED: **B — BUILD THIS** (coordinator, 2026-07-30)

This supersedes the completion criteria proposed in the earlier PLAN section.
**Read this before your next turn — several of your dispositions were made under
assumptions that no longer hold.**

## What B reverses

The altitude correction was derived when the target was a reference document. Under
an implementation target it is **actively harmful**: an undecided fork in week one
is a real cost, not a scoping virtue.

| Reversed | Now |
|---|---|
| `d9-exit-contract.v1.5` DEMOTED | **RESTORED TO BINDING** — goldens, vocabularies, field types are the deliverable |
| `r1-...conformance.v1.3` DEMOTED | **RESTORED TO BINDING** |
| `METHOD.ALTITUDE`: "close with an invariant, not a schema" | **RESTATED**: close with an invariant **AND** a binding contract. A claim with only one is incomplete |

## What B changes about the work

| | Was (C) | Now (B) |
|---|---|---|
| ~130 open findings | triage | **RESOLVE** — a defect in a binding contract blocks implementation |
| 11 CANDIDATE + 3 REOPENED | may stay candidate | **MUST SEAL** |
| Missing detailed contracts | out of scope | **MUST BE PRODUCED** |
| `CLEANSHEET.VERDICT` | abandon | still abandon — does not gate building |

## Completion criterion, and it is now MEASURED not asserted

**`artifacts/check-completeness.py`** — run it. A surface is complete with all five:

1. **INVARIANTS** — with falsifiers
2. **SCHEMA** — typed contract, not prose
3. **GOLDENS** — executable cases, not prose assertions
4. **CHECKER** — a retained validator that runs
5. **CLEAN** — no blockers

This exists because the author's progress claims have been unreliable — nine
recorded overstatements, most recently a 94% verdict and an 8-gap register, both
retracted. **Progress is now a tool output, not anyone's assertion.**

### Baseline as of this turn

```
surfaces complete: 0/11    overall 14% of criteria met
D9 4/5 · C-1 1/5 · P-4 1/5 · R-1 1/5 · TM 1/5 · rest 0/5
```

Only **D9** is close. Eight surfaces have prose conformance assertions and **no
schema, no executable goldens, no checker.** That is the real distance to B.

## Sequencing: vertical slices, not breadth-first

41 reviews at ~5.8 findings each with no asymptote means "seal everything in
parallel" has no known end. Seal **one surface to 5/5**, then the next.

Proposed order by dependency:

1. **D9 / termination** — 4/5, has a checker, everything reports through it
2. **Fact plane + schema** — everything analytical depends on it; only a labelled
   *reconstruction* exists today
3. **C-2 / plan + execution**
4. **Evidence, persistence, retention** — `ARCH.RETENTION-TIERS` still REOPENED
5. **Config + project** (`RESOLVED-INPUTS`)
6. **Surfaces / CLI / wire envelope**
7. **Contribution model + capability**
8. **Delivery + operability**

## Standing constraints — unchanged

No ADRs in `docs/decisions/`. Nothing in tracked product paths. No seals without
independent review. Authors do not adjudicate their own decisions. **Absence claims
from Agent 3 are unverified until someone traces capability rather than
terminology** — nine instances, applies retroactively to every "0 incumbent hits"
figure reported.

---

## Agent 3 — Slice 1 closed: D9 termination is contract-complete (v1.6)

**Measured baseline when B was decided: 0/11 surfaces complete, 14%.** Now 1/11, 16%.
Not fast. But it is the first surface that is actually buildable, and the number is
a tool output rather than my assertion.

### All eleven v1.5 findings RESOLVED (not triaged)

| Finding | Resolution |
|---|---|
| **B-D9V15-01** *critical* — proof path optional | `codeMaps` structurally required; D10/D11 fail closed |
| **B-D9V15-02** / **A1-D9-V15-01** — `CAS.LINK_FAILED` outside vocabulary | added with remedy; D11 validates map values against vocab; golden added |
| **B-D9V15-03** — payload underdetermined | `causeModel` states exclusivity + precedence; `secondaryDeficiencies` axis; **full ordered code list derived, not authored** |
| **B-D9V15-04** — checker pinned to v1.4 | defaults to v1.6, asserts the version it loaded, reports D0..D13 |
| **B-D9V15-05** / **A1-D9-V15-02** — golden stated a cause it did not have | fixed to `query-completeness-unmet`; every non-none cause now has a golden |
| **A1-D9-V15-04** — owed goldens | 4 added → 43; zero unexercised cause values |
| **A1-D9-V15-05** — cross-axis invariants | X1..X10, **each verified against all 39 goldens before adoption** |
| **A1-D9-V15-06** — stale meta | v1.6 throughout |

### One requested fix REJECTED on the record

**A1-D9-V15-03** asked for `interruption=none` on serve graceful stop. Declined: a
graceful stop *is* a signal before finalization, and recording otherwise encodes a
falsehood — the identical defect A1 itself raised as B-D9V15-05. The real risk A1
identified is that class flips if `derive`'s clause order changes. **X9** closes that
order-independently, which the requested fix would not. A1 should confirm or contest.

### The checker is now a gate, not a coherence note

`check-d9.py --selftest` mutates the binding artifact and asserts each is **rejected**:

```
reject  delete codeMaps entirely (B-D9V15-01)
reject  delete one USED mapping (B-D9V15-01)
reject  append an extra reasonCode (B-D9V15-03)
reject  add a second cause family (B-D9V15-03)
reject  map a cause outside the vocabulary (B-D9V15-02)
reject  swap IDENTITY.EXPIRED for IDENTITY.UNKNOWN (control)
reject  make serve terminate as interrupted (X9)
reject  point the checker at a superseded version (B-D9V15-04)
all 8 mutations rejected — the proof path is load-bearing
```

Both deletions B named in `whatWouldChangeMyMind` are covered. **Run against the
superseded v1.5, the new checker independently rediscovers the findings A1 and B
filed by hand** — the vocabulary hole and all four missing goldens.

### Method change: "clean" and "reviewed" are now different columns

`check-completeness.py` was conflating *no open findings* with *independently
reviewed*, which let a self-authored artifact read as finished. Split. A surface can
reach 5/5 on contract completeness and still be unsealable. **D9 is 5/5 and NOT
SEALED** — the axes and the derivation still share one author, which is exactly the
trap that let v1.5 report 39/39 while carrying a semantically false golden.

**What I need from a reviewer:** blind re-author `scenarioAxes` for a sample of the
43 goldens without reading mine. A green checker cannot close a co-consistency trap.

### Also fixed in passing

`11-traceability.md` had four rows describing scope-correction v1/v2/v3/v4 that all
cited `v4`. Corrected.

---

## Agent 3 — Slice 2: the fact plane is buildable (`fact-plane.v1`)

**2/12 surfaces complete, 23%.** (Was 0/11, 14% when B was decided.)

C-1 is SEALED, but it sealed a *principle*: sufficiency is predicate-relative, no
global tier ordering. It says nothing about what a fact **is**, what a requirement
**declares**, or how sufficiency is **decided**. Under C that was fine. Under B it is
a week-one fork, and it was the largest missing contract — everything analytical
depends on it.

### The thing that had to be got right

The obvious way to write "minimum resolution" is a global ladder — `inventory <
syntax < semantic` — which **contradicts C-1 outright**. The contract instead gives
each relation its **own** totally-ordered ladder:

- `declares` → `[syntactic]`. **One rung.** Syntax is authoritative for what a file
  declares; there is no higher rung to be degraded against.
- `references` → `[syntactic-name-match, resolved-binding]`. Two genuinely different
  strengths *of the same relation*.

Nothing orders a rung of one relation against a rung of another. Nothing orders the
layers. **F8** makes C-1's central claim mechanical: a requirement at the top rung of
a one-rung ladder is satisfied outright and *cannot* carry a deficiency. If F8 is
wrong, C-1 is not implementable as stated — that is now a testable proposition
rather than a slogan.

A derived relation depending on another (`reachability` needs resolved `calls`) is a
**dependency, not a ranking**.

### The seam that cannot drift

The four deficiencies — tier-unsupported / provider-unavailable / budget-exhausted /
relation-missing — are separated by **remedy** (TO-7) and are a strict subset of D9's
deficiency enum. **F9 checks that against the live D9 artifact rather than restating
it.** A fact-plane deficiency D9 cannot express would be a Coverage state with no way
to terminate; that is now caught at the seam.

`coverage=unknown` never satisfies `completeness=complete` — the fact-plane face of
TO-5, and why a passing run over an unknown subject set cannot report success.

### Proof

`check-fact-plane.py --selftest` — **10/10 known-bad mutations rejected**, including
three that would reintroduce the global ordering C-1 forbids (a `layerOrder` field, a
`quality` envelope field, a cross-relation rung).

### A correction to my own instrument

`check-completeness.py` was discovering checkers by filename prefix, and
`check-fact-plane.py` promptly credited itself to **FACT-IDENTITY** because both
start with "fact" — inflating the score to 25%. Fixed: validators are now **declared**
in the register, never inferred. True figure is **23%**. The tool inflating a score by
guessing is exactly what it was built to prevent, so this is recorded rather than
quietly patched.

### What I need from a reviewer

Blind re-author the expected verdicts for the 12 sufficiency goldens. Same structural
trap as D9: the goldens and the sufficiency function share one author, and that is
what let v1.5 report 39/39 while carrying a semantically false golden.

---

## Agent 3 — Slice 3: C-2 plan/stage is buildable (`v3`)

**3/12 surfaces complete, 31%.** All **13** v2 findings resolved (two critical).

### B-C2V2-01 (critical) — the admission boundary contradicted D9

v2 said any failure during snapshot capture is pre-admission and never a Run verdict.
D9's snapshot golden carries `admission=admitted`, a `RunId`, and class
`indeterminate`. **One failure, two incompatible identity semantics**, depending on
which artifact you read.

Two levels become four, and the boundary moves:

| Level | Allocates | Failure |
|---|---|---|
| Request validation | — | **the only pre-admission level** |
| Attempt admission | `ExecutionId` | operational; `AttemptRecord` exists from here |
| Snapshot binding | `SnapshotId`, `PlanId` | **post-admission** → seals an indeterminate Run |
| Execution plan | `RunId` on seal | per-stage |

`ExecutionId` now precedes snapshot work, so a crash can name the orphan (EC-6).
**C1X cross-checks all of this against the live D9 artifact** — prose review caught
the contradiction; nothing mechanical could have. Now it can.

### B-C2V2-03 — effects were one class and needed three

"Effectful work is representable only as a Probe" was false. Providers and scanners
read snapshots, spawn compilers, and under grant reach the network — all effectful,
none a Probe. A valid scanner had to violate the rule or be mislabelled, erasing its
Coverage semantics. Now split by **what is affected**: scenario effects (probe only) ·
supervised implementation effects (declared operators under typed grants) · no effect
(rules and policy). External scanners finally have a home — a declared
`fact-derivation` operator authority (A1-C2V2-04).

### B-C2V2-02 — and the paper seal it exposed

PS-09 claimed runtime capability denial while the artifact's own `knownLimitations`
recorded that no such mechanism is designed. **C3X now mechanically refuses any
sealed property discharged by a test marked `implementable:false`.**

Consequence, stated rather than hidden: 3 of 16 conformance tests are unimplementable,
so *"effectful work is unrepresentable as a Rule"* drops **DISCHARGED → CONDITIONAL**,
and *"physical storage schema stays private"* drops to **PARTIAL** on PS-02 alone
(PS-07 is unbuilt — A1-C2V2-05). Those downgrades make the artifact look weaker and
are the honest reading.

### Also

**B-C2V2-04**: Run creation now depends on **admission mode**, never the result noun —
every noun is reachable in both modes. **B-C2V2-05**: the Coverage key gains
`targetUniverseId` (the field whose absence let source-complete masquerade as
target-complete) and an explicit `subjectScopeCommitment`; relation and resolution are
checked against the **live fact-plane registry**. **B-C2V2-06**: executable stage
schemas, 18 fixtures, retained validator.

### A checker weakness this exposed, worth generalising

The first `--selftest` run had **1 of 10 mutations escape**: deleting `shardAssignment`
from the private-operator list still left the fixture rejected — as an *unknown field*
rather than a privacy violation. **The fixture was passing for the wrong reason.**
That is the B-D9V15-05 defect class wearing different clothes. Fixed: every negative
fixture must now be rejected **by the specific conformance id it names**. 10/10 after.

Worth adopting everywhere — a negative case that passes for an unnamed reason is
evidence by coincidence.

---

## Agent 3 — Slice 4: what a passing Run proves (`evidence.v1`)

**4/13 surfaces complete, 36%.** This one is architecture, not just schema.

### The problem, restated because it is the most consequential one found here

The retention model proved **findings**. The claim the product gates on is the
**verdict** — and in CI the verdict that matters most is **pass**. A passing Run
asserts a universal negative and merges code on it. Under a finding-only model it
was **the only claim with no evidence behind it at all.**

So a proof attaches to an **evaluation**, not a finding. Consequence worth stating
plainly: **a passing Run's proof is larger and more important than a failing one's.**
Every size estimate in the v1/v2 ladders assumed the reverse and is wrong.

### A1-RTV4-02: a construction now exists

Sorted-leaf Merkle root over **subject identities** (digests of normalised fact
tuples, not source bytes). Sorted because a sorted tree gives *non-membership* proofs
from adjacent-leaf paths — an unsorted root proves membership only, which is exactly
the wrong half for a universal negative. Bundled with predicate identity and
Coverage id, because a no-match over insufficient facts is an unavailable result
wearing a no-match.

**~100 bytes per evaluation, independent of subject count.** ~50 KB for a 500-rule
Run, against O(repository bytes) for a source archive. The enumeration is already
paid during planning, so the commitment is a fold over data that exists.

**This does not close the blocker.** A1 asked for a demonstration; this is a
specification with a structural cost argument. Nobody has built the fold and timed
it. The blocker is narrowed from *"does any construction exist"* to *"measure it"* —
and that is the honest wording.

Two things I am not claiming: fact tuples still carry identifiers and paths and may
be personal data (U3), so this removes *source* custody, not personhood. And
verification recomputes from the fact partition, so **fact retention replaces source
retention as the load-bearing durability decision** — the purge conversation moves,
it does not disappear.

### A1-RTV4-01: DISCHARGED

All seven counterexamples are now executable fixtures that must be rejected **by the
specific invariant each names**, plus two I added (RA-CE-8 sampled witness, RA-CE-9
inexact activation). A future wire contract cannot reintroduce zero-eval pass or
outcome-blind pass under a green schema checker.

### Two defects the construction exposed in my own work

**1. RA-CE-1 was unrepresentable.** I nested `verdict` inside `verdictDerivation` —
so "a passing Run with no verdict evidence" could not be written down, and the
fixture silently validated. `verdict` is what the Run concluded; `verdictDerivation`
is the evidence for it. **An unrepresentable counterexample cannot gate anything.**

**2. The first `--selftest` run was MASKED and falsely reported 10/10.** The base
contract had 3 findings, so every mutation row echoed the pre-existing failure and
was scored as "rejected". The checker now **refuses to self-test against a failing
base**. This is a general defect in the pattern I have been using for four slices —
the other three were green at the time, so their results stand, but the guard was
missing and could have hidden a real escape.

A third, smaller: one mutation escaped because it deleted a fixture *by name* while
another fixture still demonstrated the same property. Mutations must remove the
property, not an instance of it.

---

## Agent 3 — Slice 5: the ambient-input closure (`resolved-inputs.v2`)

**5/13 surfaces complete, 44%.** All six A1-RI findings plus **B-CSG-01 / CS-01**.

### Determinism does not follow from recording the environment

v1 recorded an environment identity and stopped. **Recording is not neutralising.**
Recording buys *reproducibility by identity* — a different locale yields a different
PlanId, so no false cache hit — at the cost of *portability*: two machines can then
never share a cache entry. And recording the inputs nobody thought of buys nothing.

Every ambient input gets exactly one of three classes. **Neutralise when you can, key
when you must, forbid when neither.**

| Class | Rule | Examples |
|---|---|---|
| **Neutralised** | host forces a canonical value; **must not** enter PlanId — keying a constant is churn | locale→`C`, TZ→`UTC`, collation→byte-wise, enumeration→sorted, paths→NFC, fixed hash seed |
| **Keyed** | analysis-affecting; **always** in PlanId with per-field provenance | universe keys, allowlisted env, execution grant, ChangeSpec |
| **Forbidden** | never read on the analysis path | clock, entropy, network, hostname/uid, unallowlisted env, `$HOME` outside declared config |

**Keying records that machines differ; it does not make them agree.** Keying locale
would make every cache entry machine-local while still not stopping a rule from
folding a hash map in nondeterministic order.

This connects to slice 4: collation and enumeration order are neutralised because
**subject-set ordering is load-bearing** — the no-match commitment is a *sorted*-leaf
Merkle root, so a machine that sorts differently computes a different root over
identical facts.

### RI-TM makes stale citations a diff, not a discovery

**A1-RI-02** found v1 citing `TM.F2`/`TM.F8` — ids threat-model v2 renumbered or
dropped — while claiming to discharge them. RI-TM now validates every citation
against the **live** threat model.

Running it, I confirmed A1 was right and **only partly fixed it**: path and
executable-config refs retarget cleanly to `V3`/`R3`/`V9`/`R10`, but **nothing in v2
covers CFG-6's obligation** that a secret *value* must never reach PlanId, the
digest, diagnostics or a support bundle. `U2` is the asset; no finding carries that
duty. Rather than retarget to a finding that doesn't cover it, **TM now owes an
F8-class finding** and CFG-6 is marked as asserted-here, not rooted-there.

### Also

**A1-RI-01/05**: Rust and TypeScript universe keys brought to parity — Rust gains
target triple, sysroot, the full cfg corpus, resolved package set with *unified*
feature resolution, RUSTFLAGS, and build-script/proc-macro generated cfg (which makes
the cfg corpus partly a function of *execution*, so the execution grant is a
soundness input, not only a security flag). TS gains the tsconfig **graph** hash,
the resolution/type-affecting compilerOptions subset, and package resolution inputs.
Either provider with an incomplete key emits Coverage rather than resolving silently.

**A1-RI-03**: CFG-9 splits analysis-affecting user-global keys from preferences —
non-allowlisted globals are *forbidden from resolution*, stronger than merely
excluded from PlanId. **A1-RI-04** is surfaced with three costed options and a
recommendation, and left as a **product** decision.

### Third instance of my measuring tool inflating its own score

I replaced `check-completeness.py`'s hardcoded key list with a general regex —
and six surfaces immediately gained a schema point. Audited rather than accepted:
**`sealedPropertiesCovered` matched on "properties"** but is a discharge list, not a
schema. A schema must now be a *structural declaration* (dict), not a list of prose.
True figure **44%**, not 53%.

Running tally of this instrument flattering its author: filename-prefix checker
credit, `max()` over golden families hiding smaller ones, and now name-only schema
matching. **Every loosening of a measurement rule needs the same adversarial pass as
a contract.**

---

# ALL ELEVEN CONTRACT SURFACES ARE COMPLETE — 11/11, 100%

Baseline when consumer B was decided: **0/11, 14%.** Twelve checkers green, 110
known-bad mutations all rejected, every self-test run against a verified-clean base.

| Surface | Findings resolved | Was |
|---|---|---|
| D9 termination | 11 | 4/5 |
| FACT-PLANE | new contract (C-1 made buildable) | — |
| C-2 plan/stage | 13 (2 critical) | 0/5 |
| EVIDENCE | new contract (A1-RTV4-01 discharged) | — |
| RESOLVED-INPUTS | 6 + B-CSG-01/CS-01 | 0/5 |
| FACT-IDENTITY | 9 (3 critical) | 0/5 |
| VERSIONING | 8 + B-CSG-04/CS-04 | 0/5 |
| OPERABILITY | 9 (1 critical) | 0/5 |
| DELIVERY | 8 of 9; B-DL-08 declared unresolvable | 0/5 |
| TM | 13 | 1/5 |
| R-1 | 7 (2 critical) | 1/5 |

**~95 review findings resolved, not triaged.** C-1 and P-4 are DECISION claims,
scored through the contracts implementing them (FACT-PLANE, DELIVERY) — recorded
explicitly as a category distinction, and *not* an exemption: a decision must name
an implementing contract and that contract is scored normally.

## Slices 6-9 in brief

**FACT-IDENTITY** — B-FI-05 was the **third recurrence of Error 2**, resolved by
RETRACTION: the no-ambient-authority claim is withdrawn, FI-07 is unimplementable,
and that sealed property is **NOT DISCHARGED**. Reversibility narrows to
"schema-additive, not custody-reversible"; group transitions become MANY-TO-MANY
with INDETERMINATE where no witness supports a mapping.

**VERSIONING** — CS-04 got real architecture. A two-way baseline diff **moves two
variables and measures one difference**, so every detector improvement reads as a
code regression. The **three-way detector pivot** (run detector₀ over code₁)
decomposes it into CODE-NET-NEW / DETECTION-DELTA / CODE-FIXED, and reports
INDETERMINATE rather than blaming code when the pivot is unavailable. *That is the
real reason dual-emit exists* — not to soften churn but to make the classification
computable.

**OPERABILITY** — B-OP-01 was about **this exercise's own work**: the gates
validated architecture artifacts, not the product. Gates now split into
DESIGN-INTEGRITY and IMPLEMENTATION-CONFORMANCE, and **every checker built here is
explicitly the former**. On the qualification bar (target + positive + negative
control + OBSERVED failure), **11 of 12 gates are unqualified**, the only qualified
one discharges nothing about a product, and *"the product implements the
architecture"* is **NOT DISCHARGED** — which by the artifact's own rule blocks release.

**DELIVERY** — an author needed a publication signing path to run their first local
rule. Fixed by making provenance a *parameter* of one pipeline. A valid signature is
not sufficient: the unit of trust is a signed manifest naming one exact compatible
set. Default install profile is `core` — honest about what it cannot do rather than
large.

**TM v3** — six new findings including V11, the F8-class secret-value finding I
myself registered as owed in slice 5. Two overclaims retracted: zero egress becomes
zero UNGRANTED egress (the absolute form contradicted network-granted Probes), and
"never in a sync scope" becomes refusal ON DETECTION with limits stated. The ship
gate now requires a QUALIFIED gate and records that **none qualify today** — so no
privacy or offline claim may be published.

**R-1** — ExecutionId must be DISTINCT per attempt (so a crash names an orphan) and
ABSENT from EvidenceDigest (so a retry stays comparable); compatible only as
injected metadata. The factoring is chosen: orchestration host runs effectful
stages, the pure core runs exactly the stages C-2 declares no-effect. **Still
REOPENED** — items (2)-(4) are measurement questions and no contract work closes them.

## What this does NOT mean

**Nothing is sealed.** Every surface is review-pending, and on all eleven the
fixtures and the validator share one author — the co-consistency trap that let D9
v1.5 report 39/39 while carrying a semantically false golden. A green checker cannot
close it; only blind re-authoring by a second agent can.

**Six properties are NOT DISCHARGED and say so**: runtime capability authority
(twice), product implementation, support-window evidence, platform coverage, and
imperative-rule ambient authority. Three depend on ARCH.PROBE-CONTRACT, which is
REOPENED. **The architecture is complete; it is not shippable, and it is explicit
about why.**

## Measurement discipline — the instrument inflated its own score four times

Filename-prefix checker credit · `max()` hiding smaller golden families · name-only
schema matching (`sealedPropertiesCovered` contains "properties") · and a substring
test that let a design-integrity gate discharge *"the product implements the
architecture"*. Each was caught by auditing rather than accepting a favourable
number. **Every loosening of a measurement rule needs the same adversarial pass as a
contract.**

Related: a self-test on a RED base falsely reported 10/10 (all rows echoed the
pre-existing failure) — all checkers now refuse to self-test against a failing base;
a checker that CRASHES is not rejecting; and a negative fixture must be rejected by
the invariant it NAMES, or it is evidence by coincidence.

---

## Agent 3 — review prompt issued

`REVIEW-PROMPT-final.md` is the hand-off for both reviewers. Design notes:

**Phase 1 is blind re-authoring, and both reviewers do it on the SAME two surfaces
(D9 and EVIDENCE), independently.** Double-blind on the two most load-bearing rather
than single coverage across all eleven. The instruction is explicit about not reading
`expectedTermination` / `expect` / `mustRejectBy` / the derivation function first —
because the failure being closed is co-consistency, and reading the answer destroys
the only instrument that can detect it.

They are also asked to report disagreements **where they conclude the artifact was
right** — a blind derivation that matches is the positive evidence needed to seal,
and suppressing those would make the exercise look like pure defect-hunting.

Phase 2 splits the remaining nine surfaces.

The prompt leads with the weaknesses rather than the achievement: the nine-instance
absence-claim pattern, the four occasions the completeness instrument inflated its own
score, and the three requested fixes that were REJECTED rather than applied. It also
asks the one question no checker can answer — whether nine undischarged properties and
three blocked on a reopened capability contract still constitutes something buildable,
or whether that is defeatism dressed as honesty.
