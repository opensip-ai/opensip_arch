# Packet B1 — DR-131 Class A opening (candidate `preview-analyze-contract.v2`, recorded D-138)

Prepared 2026-08-27 by the Claude orchestrator for the human owner (sole decision authority). Nothing in this packet decides anything. Every factual claim carries a citation; quoted bytes are verbatim. Where the record holds no value, the packet says "not in the record".

**Measurement basis.** HEAD `4abb961aad98525ca8b992a24609a6286964a451` (`git rev-parse HEAD`). File 08 `docs/v2/architecture/08-decision-and-readiness-register.md` sha256 `e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e`; last commit touching it `fc688b15 D-236: record DR-104 SATISFIED under D-056 Class B`; working tree clean for file 08. COORD `docs/coop/COORDINATOR-DECISIONS.md` sha256 `47f7b2011ec719dfadcbccb553a142eb0808e3099f20bf544b4564ab18e28466`; `grep -c '^## D-'` = 277. **Quotation convention:** quoted bytes are verbatim except that hard line-wraps in the sources (COORD, the D-056/D-138 turn-2 drafts, `DECISIONS-NEEDED.md`) are re-flowed to single spaces — whitespace-only normalization; no character other than newline-plus-indent is altered (e.g. `DECISIONS-NEEDED.md` lines 34–35 read `Open Class A` newline four-space-indent `(application-grade acceptance`).

**The question (DECISIONS-NEEDED.md §B, B1, verbatim):** "**DR-131** preview non-authoritative `analyze` — candidate `preview-analyze-contract.v2` (D-138). Open Class A (application-grade acceptance, no express reservation) → then a SATISFIED-GRADE cycle? Or what must change first?" and the parenthetical under B3: "(Grok's standing instruction was "do not SATISFY DR-117/131/133"; I will not open Class A without your word.)"

Grok's handoff instruction, verbatim (`HANDOFF.D-000-orchestrator-live.txt` line 83, under heading "## Do not invent / do not SATISFY"): "Do not SATISFY DR-117 / DR-131 / DR-133 (Class A unopened)."

---

## 1. The DR-131 row of file 08 — every cell, verbatim

Table header (file 08 line 280): `| ID | Decision | Owner / decision authority | Source pin / affected sections | Required acceptance evidence | Status | Blueprint impact |`

Row located by the line beginning `| DR-131 |` (file 08 line 313 at HEAD):

| Cell | Bytes |
|---|---|
| ID | `DR-131` |
| Decision | `Preview non-authoritative `analyze` product contract` |
| Owner / decision authority | `Product + CLI / output` |
| Source pin / affected sections | `[`COORDINATOR-DECISIONS.md`](../../coop/COORDINATOR-DECISIONS.md) D-132 (user-made ADOPTED, commit `d3efe3c…`); D-134 (CONSENT Claude `0b672021…` / Codex `ec305159…`); recorded goal [file 12 §3](12-architecture-completion-goal.md) (file 12 has no authority)` |
| Required acceptance evidence | `Independently reviewed contract that freezes: single first-party bundled declarative pack name/version; sealed facts+Coverage inputs; PlanId membership of the pack; core-evaluated `policyOutcome`; typed-indeterminate on a missing required rung; which preview identities are unstable; upgrade path to a sealed Run; citation of D-077 / D-078. The cell excludes human/machine JSON schema and exit generics already SATISFIED at DR-123 (D-092).` |
| Status | `**OPEN** — accepted design-contract candidate recorded (D-138): [`preview-analyze-contract.v2.json`](../../coop/artifacts/preview-analyze-contract.v2.json) `081ff7fb529b34a3db3ac9f4c7505848e2253be12b5a867d39b49b3a26d56970` — `CANDIDATE-NOT-APPLIED`, binds NOTHING. Not eligible in kind today (D-133). Not SATISFIED.` |
| Blueprint impact | `Hard blocker for preview `analyze`; condition 2 SATISFIED-requiring per D-134` |

The Status cell bytes are exactly the "after (verbatim)" text written by D-141 (`docs/coop/artifacts/coordinator-decisions.D-141.draft.md` lines 57–59); D-141 replaced the prior clause `no contract exists` (same draft, lines 53–55).

Condition-2 snapshot (file 08 line 415, Standing cell, opening bytes): `**5 of 32 `SATISFIED`** — 24 `OPEN`, 1 `DECIDED-V1-NOT-INTEGRATED`, 2 `PROPOSED-CLOSED-FOR-REVIEW`.` … closing bytes: `DR-131 and DR-133 added OPEN by D-135; neither is eligible in kind today (D-133).` Status column: `**NOT MET**`.

---

## 2. The D-138 entry — decision/status text and its reservation

COORD `## D-138 — Record preview-analyze-contract.v2 as DR-131's accepted design-contract candidate` (COORD lines 5836–5891).

- **Status** (verbatim): `**ADOPTED 2026-08-15.** Turn 2 of 3: CONSENT from both independent reviewers, 0 MUST-FIX, 0 SHOULD-FIX.` Claude 2 `artifacts/coordinator-decisions.D-138.review-adversarial.claude2.turn2.json` `31dbf4a513ae3e3e0f526c55d3564dfe3f4f59aa24f8fb6489221ebf91161acd`; Codex `artifacts/coordinator-decisions.D-138.review-adversarial.codex.turn2.json` `b14bb0fe3745a29e9d406e9738273cd689384cb1879d08ea6c94bc496b9596e8`; subject `coordinator-decisions.D-138.turn2.draft.md` `c609de64c295105ce1b2ea6927137ea1455758bfea15bad4265585fba12efa99` (re-measured identical at HEAD).
- **Decision type** (verbatim): `RULE-GOVERNED. Records independent dual ACCEPT of `preview-analyze-contract.v2.json` (0 blockers, 0 SHOULD-FIX from both reviewers). Same no-cell-edit branch as D-116 / D-131 / D-136 / D-137.`
- **Decision** (verbatim, entire paragraph): `Record v2 as DR-131's accepted design-contract candidate. This is coordinator decision D-138, not a register row. DR-131 stays `OPEN`. No `SATISFIED`. The candidate binds NOTHING. D-056 Class A is not opened. Recording v2 does not make DR-131 D-056-eligible in kind on v2 alone: NT-1..NT-8 assign no owner and no existingGate; no DR-G obligation names them. Advisories CLAUDE-PAC-V2-ADV-1 and DR131V1-ADV-1 travel as honesty work. Does not edit file 08. Does not mint a D-096 (A) grant. Does not SATISFY DR-117, DR-133, or any other row. Does not overturn D-136 or D-137. Does not authorize `docs/v2/implementation/`. **Owed later work, not performed here:** on adoption the live DR-131 status-cell clause `no contract exists` becomes stale. A later MF-6 act — its own D-000 cycle and commit — updates that cell to record this accepted candidate while keeping the row OPEN, Class A unopened, and not SATISFIED.`
- **Readiness effect** (verbatim): `Zero. Condition 2 stays 4 of 32. Condition 5 last.`
- **Reversibility** (verbatim): `Total only before the owed MF-6 or another dependent act lands. After one lands, overturn also requires that act's owning-entry supersession or revert and reconciliation of its dependent file-08 record under its own reviewed act. Pre-dependent overturn: C-D138.`

The "CANDIDATE-NOT-APPLIED; Class A not opened" reservation, as the record actually spells it, lives in four places:

1. D-138 Decision: `The candidate binds NOTHING. D-056 Class A is not opened.` (above).
2. D-138 pinned turn-2 subject, Decision 2 (`coordinator-decisions.D-138.turn2.draft.md` lines 59–67): `DR-131 stays `OPEN`. No `SATISFIED`. No `QUALIFIED`. The candidate binds NOTHING. D-056 Class A is not opened. This recording is not a SATISFIED re-record. Recording v2 does **not** make DR-131 D-056-eligible in kind on v2 alone: NT-1..NT-8 are specified-classes-not-executed; no DR-G obligation names any of them and no owner is assigned to them, so Eligibility gates 2 and 3 are not established. This artifact assigns no class owners at all. A later SATISFIED cycle must first close and independently review that owner/gate/harness design.`
3. D-141 (the MF-6 that wrote the live cell), Decision (COORD lines 5981–5987): `Replace DR-131's Status-cell clause `no contract exists` with the recorded D-138 candidate in the established form (link, full digest, `CANDIDATE-NOT-APPLIED`, binds NOTHING). DR-131 stays `OPEN`. Not SATISFIED. Class A not opened.`
4. The live cell itself: `` `CANDIDATE-NOT-APPLIED`, binds NOTHING. Not eligible in kind today (D-133). Not SATISFIED.`` (§1).

The owed MF-6 named in D-138 was performed by D-141 (`Performs D-139 H2 only.`, COORD line 5979–5980). Nothing else in D-138 is owed.

---

## 3. The candidate's own fields

`docs/coop/artifacts/preview-analyze-contract.v2.json`, sha256 `081ff7fb529b34a3db3ac9f4c7505848e2253be12b5a867d39b49b3a26d56970` (re-measured at HEAD; matches the D-138 Subject pin and the live cell). Fields verbatim (via `jq`):

- `artifact`: `"preview-analyze-contract.v2"`; `version`: `2`; `date`: `"2026-08-15"`; `documentClass`: `"DESIGN-CONTRACT-CANDIDATE"`; `registerRow`: `"DR-131"`.
- `authorityClaim`: `"This artifact PROPOSES the DR-131 preview non-authoritative analyze product contract. It applies nothing, edits no register row, seals nothing, marks nothing SATISFIED, and does not authorize docs/v2/implementation/. D-056 Class A is not opened. File 12 has no authority."`
- `purpose`: `"Answer every fragment of the live DR-131 acceptance-evidence cell as a stated obligation. Freeze the pack identity and analyze laws. Do not freeze rule IR, evaluation algorithm, packaging, or default numeric constants."`
- `binds`: `"NOTHING"`
- `status`: `"CANDIDATE-NOT-APPLIED"`; `reviewStatus`: `"AWAITING-INDEPENDENT-REVIEW"`; `sealRecommendation`: `"DO-NOT-SEAL"`.
- `doesNot` (array, verbatim): `"Does not SATISFY DR-131."`, `"Does not open D-056 Class A."`, `"Does not invent §7.1 identity recipes."`, `"Does not advertise SARIF."`, `"Does not freeze public rule IR."`, `"Does not rewrite DR-123."`, `"Does not authorize docs/v2/implementation/."`, `"Does not rewrite D-002 commands, platforms, or independent-release machinery."`, `"Does not SATISFY DR-117 or DR-133."`
- `registerRowQuoted.obligationDecomposition`: nine obligations OBL-1..OBL-9, each with a `cellFragmentVerbatim` equal to one fragment of the live Required-acceptance-evidence cell and an `answeredAt` pointer (e.g. OBL-1 `"single first-party bundled declarative pack name/version"` → `["pack"]`; OBL-9 `"The cell excludes human/machine JSON schema and exit generics already SATISFIED at DR-123 (D-092)."` → `["exclusions.dr123"]`). `registerRowQuoted.sourceSha256` is `7585325d73a678739b74309700680e6b7663bf017c6d5a6796eee4cc1441d94e` — the file-08 digest at authoring time (measured: `git show 52ea851:docs/v2/architecture/08-decision-and-readiness-register.md | shasum -a 256` = `7585325d…`; commit `52ea851 D-135: add DR-131 and DR-133 as OPEN in file 08`, 2026-08-15), not the current `e503b75b…`; the quoted acceptance-evidence cell bytes are identical to the live cell in §1.
- `pack`: `name` `"opensip.preview.typescript.pack"`, `version` `1`, `notFrozenHere` `["rule IR","evaluation algorithm","packaging adapters","default numeric constants"]`.
- `negativeTests.status`: `"specified-classes-not-executed"`; classes NT-1 `user-or-third-party-pack-refused`, NT-2 `imperative-rule-refused`, NT-3 `missing-rung-not-success`, NT-4 `component-finding-not-analyze-finding`, NT-5 `sarif-not-advertised`, NT-6 `preview-result-not-sealed-run`, NT-7 `host-must-not-mint-verdict`, NT-8 `host-must-not-mint-d9-or-termination-from-policy`.

Note for gate 1 (below): the reservation is in the artifact's own bytes (`status`, `sealRecommendation`, `authorityClaim`, `doesNot[1]`), not only in the recording entries.

---

## 4. The two independent reviews — paths, digests, verdicts

| Reviewer | Path | sha256 (re-measured at HEAD; matches D-138 Verdicts) | `verdict` | blockers / SHOULD-FIX / advisories |
|---|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/preview-analyze-contract.v2.review-independent.claude2.json` | `22a0d892f3051fd007cd7dc26a215e7aa3004f296f99a67aea83bd3035bfd903` | `"ACCEPT"` | `counts`: `blockers` `0`, `shouldFix` `0`, `advisories` `1` (`CLAUDE-PAC-V2-ADV-1`) |
| Codex | `docs/coop/artifacts/preview-analyze-contract.v2.review-independent.codex.json` | `e48cb59253f0fe789e5c448ff197d74d3aea745f7eb9f8fbc394077a993a0db1` | `"ACCEPT"` | `blockerCount` `0`, `shouldFixCount` `0`, `advisoryCount` `1` (`DR131V1-ADV-1`) |

Both reviews measured the subject at `081ff7fb…` start and end (Claude `subject.sha256Start`/`subject.sha256End`; Codex `subjectSha256AtStart`/`subjectSha256AtEnd`). Moved/edited flags, by each file's own keys: Claude `subject.movedDuringReview: false`, `subject.editedByReviewer: false` (top-level `.movedDuringReview` absent); Codex `subjectMovedDuringReview: false`, `authorityOfThisVerdict.editsSubject: false` (Codex has no key named `movedDuringReview` or `editedByReviewer`).

Grade language — the bytes that matter for gate 1:

- Claude `acceptanceGrade` (verbatim): `"ACCEPT as an independently reviewed DR-131 design-contract candidate. This verdict does not apply the artifact, does not mark DR-131 SATISFIED, and does not open D-056 Class A. The artifact's own status fields govern: CANDIDATE-NOT-APPLIED, DO-NOT-SEAL, binds NOTHING."`
- Claude `whatThisAcceptanceDoesNotDo` (verbatim, five items): `"Does not apply the artifact. It remains CANDIDATE-NOT-APPLIED and binds NOTHING."`, `"Does not mark DR-131 SATISFIED. Its live cell still reads OPEN with blueprint impact 'Hard blocker for preview analyze'."`, `"Does not open D-056 Class A."`, `"Does not execute any of the eight classes. All remain specified-classes-not-executed."`, `"Does not authorize docs/v2/implementation/."`
- Codex `authorityOfThisVerdict` (verbatim keys/values): `marksDR131Satisfied: false`, `marksAnyRegisterRowSatisfied: false`, `opensD056ClassA: false`, `mintsD096Grant: false`, `authorizesImplementation: false`, `qualifiesOrDemonstratesAnything: false`, `appliesOrSealsCandidate: false`, `inventsIdentityRecipe: false`, `inventsD9Code: false`, `editsSubject: false`, `editsFile08: false`, `editsCoordinatorDecisions: false`, `commits: false`; `note`: `"This ACCEPT verdict is independent review evidence on the v2 candidate bytes only. DR-131 remains OPEN; a later recording and any owed MF-6 update require their own authorized reviewed acts."`
- Codex `reviewScope` (verbatim): `"preview-analyze-contract.v2 only. This review does not mark DR-131 SATISFIED, apply or seal the candidate, open D-056 Class A, mint a D-096 grant, authorize docs/v2/implementation/, edit file 08 or COORD, commit, or modify the subject or the other review target."`

Advisories (non-blocking, travelling as "honesty work" per D-138):
- `CLAUDE-PAC-V2-ADV-1` (severity `ADVISORY`): NT-7 and NT-8 open their pass condition with `'Refused.'` for properties whose actor is the host itself; suggestion is to restate in NT-6's idiom or scope the inputs to a request/configuration. `whyNotShouldFix`: the substantive clauses `"state a correct and testable conformance property"`.
- `DR131V1-ADV-1` (severity `ADVISORY`, standing `CONTINUES-NON-GATING-AND-ACKNOWLEDGED`, sites `/policy/result`, `/findingDisposition/3`): DR-009/D-079 `policyOutcome.derivationDigest` traceability; suggestion: `"A later traceability-only successor may cite D-079 / route-b.DR-009.preview-disposition.v2 without adding a recipe or changing policy semantics."`

---

## 5. D-056's five eligibility gates, verbatim, and the byte evidence for DR-131 today

D-133 (COORD lines 5641–5645, Decision type) fixes where the gates are defined: `D-056's pinned turn-2 subject `dfb0c2af…` already states eligibility as a property; its five gates govern.` That subject is `docs/coop/artifacts/coordinator-decisions.D-056.turn2.draft.md`, sha256 `dfb0c2af39ff31df9bf3609c131f03ee2d87a585dcd684abd633d47ffb11ed82` (re-measured at HEAD; matches the COORD D-056 Status pin). Section `## Eligibility (narrow)` (lines 95–124), verbatim:

> A later SATISFIED re-record of a slice-affecting architecture row may use this amendment only when **all** of the following are true of that row at the moment of that later cycle:
>
> 1. One of:
>    - **Class A.** An independently accepted design contract exists at 0 blockers with application-grade acceptance and no express reservation (D-001 T2-02), recorded by a D-000 entry; the row's lead label is `OPEN`.
>    - **Class B.** The lead label is `DECIDED-V1-NOT-INTEGRATED` because a D-000 entry already recorded the product/architecture decision (D-006, D-008, D-009, or a later sibling of that form).
> 2. Every remaining acceptance-evidence member is **only** harness *execution*, fixture *execution*, or qualification *measurement*. Authoring of fixtures, schemas, successors, actor-joins, missing design, or still-UNDECIDED numbers is **not** a remainder this amendment may split.
> 3. Each such remainder is already named as a condition-4 / DR-G* obligation with an owner. Naming a harness identifier is not itself SATISFIED.
> 4. A dedicated later D-000 cycle plus independent SATISFIED-GRADE review of *that row* accepts the split and records SATISFIED under this amendment.
> 5. An MF-6 file-08 cell edit records SATISFIED and removes the cell's conflicting "until executed" / "until measured" SATISFIED-bar. This entry is not that edit.

The same subject's Decision clause 5 (lines 186–190), which the G24–G28 joins cite: `**Authoring fixtures and harness *specifications* remains lawful design work now.** Execution remains qualification. DR-103's own schema already places fixture generation under DR-120 / DR-G15. That authoring must exist and be independently reviewed before DR-103 can become eligible.`

The T2-02 property the Class A limb points at — D-001 (heading `## D-001 — Definition of "completed" for the V2 design` at COORD line 60; the T2-02 bullet is lines 181–190, line 191 begins the next bullet `- **DR-006**`), verbatim: `**Standing route-A acceptance property (T2-02),** stated once and referenced wherever a candidate's applicability is at issue: a candidate is applicable when its independent review returns **0 blockers AND grants application-grade acceptance with no express reservation** — no candidate-only limitation, no EXPRESSLY-NOT-FOR-APPLICATION language, no named apply-condition left undischarged on the record — and the coordinator then applies per route A. "0 blockers" alone is measured insufficient by three corpus precedents (EIR v6: accepted as CANDIDATE only; delivery.v5: expressly not for application; r1 v1.9: apply-condition chain), so the weaker phrase is struck everywhere.`

### Gate-by-gate evidence for DR-131 at HEAD `4abb961`

**Gate 1 (Class A) — does NOT hold today.**
- Holds: "independently accepted design contract exists at 0 blockers" — both reviews `ACCEPT` at 0/0 (§4); "recorded by a D-000 entry" — D-138 (§2); "lead label is `OPEN`" — live cell (§1).
- Fails: "application-grade acceptance and no express reservation". The reviews grant candidate-grade acceptance in terms (Claude `acceptanceGrade`: `"ACCEPT as an independently reviewed DR-131 design-contract candidate … does not open D-056 Class A"`; Codex `opensD056ClassA: false`, `appliesOrSealsCandidate: false`). The artifact carries a candidate-only limitation in its own bytes (`status` `"CANDIDATE-NOT-APPLIED"`, `sealRecommendation` `"DO-NOT-SEAL"`, `doesNot` `"Does not open D-056 Class A."`). D-138 and D-141 both say `Class A is not opened` / `Class A not opened`. D-001 T2-02 names exactly this shape as insufficient: `EIR v6: accepted as CANDIDATE only`.
- Contrast, the one Class A precedent: D-015 recorded `**Route-A acceptance property:** MET. Reservation-language sweep of the VERDICT clean — … zero acceptance reservations. The subject carries 9, likewise none an acceptance reservation. No apply-conditions.` (COORD lines 1211–1214) and DR-102 was later SATISFIED at D-085 under Class A. For DR-131 no entry records the Route-A acceptance property as MET. Not in the record: any D-000 entry lifting the D-138 reservation.
- Venue for a lift (stated for the sibling DR-117 chain: D-168, heading COORD line 7061, quoted passage lines 7092–7095 (Venue sentence 7094–7095); D-207, heading line 9062, quoted passage lines 9096–9099 (Venue sentence 9098–9099); verbatim): `Gate 1 Class A remains false under D-137's express reservation. … Venue for any later lift is a reviewed coordinator act, not an artifact.` No DR-131 entry states the venue; the DR-117 statements are the only venue bytes in the record.

**Gate 2 (remainder is only execution / measurement) — the record carries two readings; not reconciled in bytes.**
- Reading (a), gate 2 holds: D-154 Decision (COORD lines 6467–6470), verbatim: `NT-7 and NT-8 leftover-design closes: remainder is G28 execution. After this act, D-056 Eligibility gates 2 and 3 hold for DR-131's eight NT classes. Class A is not opened. Gate 4 reserves eligibility to a later SATISFIED-GRADE cycle. Not eligible in kind. Not SATISFIED.` This is the only COORD line at or after D-154 that states gate 2 for DR-131 (measured: no line after COORD 6469 contains both "ate 2" and "DR-131").
- Reading (b), gate 2 does not hold: each current G24–G28 leftover-join carries one obligation with `leftoverDesign: true` — `OBL-G24-FX-AUTHORING`, `OBL-G25-FX-AUTHORING`, `OBL-G26-FX-AUTHORING`, `OBL-G27-FX-AUTHORING`, `OBL-G28-FX-AUTHORING` (§7) — each with `rideStanding` `"not-capable-of-riding as execution-only remainder"` and `executionObligationOwnerToday` `"none"`, and each `reason` citing `D-056 Decision clause 5: authoring fixtures remains design work`. Those joins were recorded as current by D-249..D-253 (2026-08-23), each stating e.g. `leftover-design of OBL-G24-FX-AUTHORING remains on leftover-join.v4.` (D-250, COORD 12249–12250). STATUS.2026-08-26.md §2 item 2 reads: `D-056 clause 5: authoring fixtures is design work, so a row with unauthored fixtures is ineligible.` (that sentence is the orchestrator's gloss: measured 0 occurrences in COORD and 0 in file 08).
- Both readings are ADOPTED bytes. D-249..D-253 do not restate gate 2 for DR-131; D-154 does not mention FX-AUTHORING. Which reading governs is an open question (§10, Q2).

**Gate 3 (each remainder named at a DR-G* obligation with an owner) — holds for the eight NT classes per D-150..D-154; partially "owner: none" at the FX-AUTHORING layer.**
- NT-1, NT-2 → `DR-G24` (D-150, `It owns DR-131 NT-1 and NT-2 only.`), file 08 line 360 owner cell `Product + CLI / output`.
- NT-3 → `DR-G25` (D-151, `It owns DR-131 NT-3 only.`), file 08 line 361 owner `Product + CLI / output + semantic owners`.
- NT-5 → `DR-G26` (D-152, `It owns DR-131 NT-5 only.`), file 08 line 362 owner `Output/operability + CLI/product owners`.
- NT-6 → `DR-G27` (D-153, `It owns DR-131 NT-6 only.`), file 08 line 363 owner `Product + CLI / output`.
- NT-7, NT-8 → `DR-G28` (D-154, `It owns DR-131 NT-7 and NT-8 only.`), file 08 line 364 owner `Product + CLI / output`.
- NT-4 → per D-148 (COORD 6220–6223): `NT-4 is not leftover-design: its pass is already named as DR-133 execution at G21 (D-145) and G23 (D-147). This entry does not name DR-131 NT-4 at those gates.` Measured: the current G21 join `g21-leftover-join.v13.json` (`058717f5…`, D-292) and G23 join `g23-leftover-join.v8.json` (`498324e5…`, D-240) contain the string `DR-131` zero times each.
- All five gate rows carry `PROPOSED; not QUALIFIED` and harness identifiers `not authored; not QUALIFIED` (file 08 lines 360–364).
- Within the joins, the execution obligations (`OBL-G2x-EXECUTION`, `OBL-G2x-HARNESS-SPEC`) carry named owners; the five `OBL-G2x-FX-AUTHORING` obligations carry `executionObligationOwnerToday: "none"` (§7).

**Gate 4 (dedicated D-000 cycle plus independent SATISFIED-GRADE review of that row) — not performed.** No COORD heading records a SATISFIED-GRADE cycle for DR-131. Every DR-131-adjacent recording states the negative: D-154 `Gate 4 reserves eligibility to a later SATISFIED-GRADE cycle.`; D-249..D-253 each `Not a three-limb act. Not SATISFIED-GRADE.`

**Gate 5 (MF-6 cell edit records SATISFIED and removes the "until executed" bar) — not performed.** The live DR-131 Status cell (§1) carries no "until executed" / "until measured" sentence; its bar is the three clauses `` `CANDIDATE-NOT-APPLIED`, binds NOTHING. Not eligible in kind today (D-133). Not SATISFIED.`` and the Blueprint-impact `Hard blocker for preview `analyze``.

Summary table:

| Gate | Holds for DR-131 today? | Governing bytes |
|---|---|---|
| 1 Class A | No | reviews' candidate-grade wording; artifact `status`/`doesNot`; D-138, D-141 "Class A not opened" |
| 2 execution-only remainder | Contested in bytes: D-154 "hold" vs five `OBL-G2x-FX-AUTHORING` `leftoverDesign: true` on the current joins | D-154; g24 v4 / g25 v5 / g26 v4 / g27 v4 / g28 v4; D-249..D-253 |
| 3 named at DR-G* with owner | Yes for NT-1..NT-8 (G24–G28; NT-4 via G21/G23 per D-148); FX-AUTHORING owner `"none"` | D-148, D-150..D-154; file 08 lines 360–364 |
| 4 SATISFIED-GRADE cycle | Not performed | D-154; D-249..D-253 |
| 5 MF-6 SATISFIED cell edit | Not performed | live cell |

---

## 6. What a "T2-02 application-grade, no-express-reservation acceptance" entry would have to say

Derived strictly from the gate-1 wording (§5), the T2-02 property (D-001), the D-015 precedent form, and the DR-117 venue bytes. This section describes; Appendix A pre-drafts.

**It would have to say (minimum content):**
1. Subject: `docs/coop/artifacts/preview-analyze-contract.v2.json` at `081ff7fb…` — the same bytes D-138 recorded; no v3 (an artifact cannot lift the reservation: D-168/D-207 `Venue for any later lift is a reviewed coordinator act, not an artifact.`).
2. The gate-1 finding in D-001 T2-02's own terms: that the independent review returns 0 blockers (measured: both 0/0) AND grants application-grade acceptance with no express reservation — i.e. the entry must state that the "candidate-only limitation" is lifted, that no `EXPRESSLY-NOT-FOR-APPLICATION` language stands, and that no named apply-condition is left undischarged. Following D-015's form: a reservation-language sweep of the verdicts and the subject, recorded in the entry.
3. Which review evidence satisfies "grants application-grade acceptance". Two byte-supported shapes exist; the entry must pick one (this is the owner's choice, §9 Q1):
   - (i) the two existing 0/0 ACCEPT verdicts are read as application-grade by the reviewed coordinator act, with their self-limiting grade sentences (`"ACCEPT as an independently reviewed DR-131 design-contract candidate"`, `opensD056ClassA: false`) treated as reservations of the *recording*, not of the *contract*, and lifted by the act; or
   - (ii) a fresh dual independent review of the same bytes, dispatched with a prompt asking for an application-grade verdict, whose verdict files are then cited.
4. The user's authority: gate 1 is a product-boundary lift on a row owned by `Product + CLI / output`; DECISIONS-NEEDED §B says the openings are "product/architecture authority". The entry must record the user's word (D-132 form: "Made directly by the user in conversation … recorded verbatim").
5. Express negatives: does not SATISFY DR-131; does not perform gates 4 or 5; does not close `OBL-G24..G28-FX-AUTHORING`; does not execute NT-1..NT-8; does not edit file 08 (or names the owed MF-6); does not open Class A for DR-117 or DR-133; does not mint a D-096 (A) grant; does not authorize `docs/v2/implementation/`.
6. Its position on gate 2 (see §10 Q2): either it states which reading governs, or it expressly leaves gate 2 to the SATISFIED-GRADE cycle.
7. Readiness effect: `Zero SATISFIED. Condition 2 stays 5 of 32.`
8. Reversibility: total before a dependent SATISFIED-GRADE cycle or MF-6; overturn restores the D-138/D-141 "Class A not opened" standing.

**What it would change in file 08 — the exact cell.** Only the Status cell of the row beginning `| DR-131 |` (file 08 line 313, column 6). Its current bytes are in §1. The clause that becomes stale on adoption is `` — `CANDIDATE-NOT-APPLIED`, binds NOTHING. Not eligible in kind today (D-133).`` (the D-138 form). Per the D-138 → D-141 precedent, that rewrite is a separate MF-6 act (its own D-000 cycle and commit), not the opening entry itself. The lead label `**OPEN**`, the clause `Not SATISFIED.`, the Blueprint-impact cell, and the condition-2 snapshot (line 415, `5 of 32`) would not change at the opening. The exact replacement text is not in the record; a form consistent with D-141 would replace the stale clause with a citation of the opening entry (Appendix A gives DRAFT bytes).

**What it would NOT do.**
- Not SATISFY DR-131 — gates 4 and 5 remain their own acts (D-056 turn-2 subject, Decision 2: `Each later SATISFIED re-record is its own D-000 cycle.`).
- Not change Condition 2 arithmetic (stays `5 of 32`, `NOT MET`).
- Not close any `leftoverDesign: true` obligation (§7) and not author any fixture bytes (D-056 clause 5).
- Not touch DR-G24..G28 rows (`PROPOSED; not QUALIFIED`) or any harness identifier.
- Not open Class A for DR-117 (D-137/D-207) or DR-133 (D-136/D-140) — separate packets B3/B2.
- Not authorize `docs/v2/implementation/` (Condition 5, reserved to the user by D-001).
- Not supersede D-138 or D-141 (it builds on them; overturn of it restores their standing).

---

## 7. Every leftover-design obligation measured on DR-131's current leftover-join(s)

**Naming precision.** There is no `<lineage>-leftover-join.vN.json` whose lineage is DR-131 (measured: `ls docs/coop/artifacts | grep leftover-join` lists 38 lineages; none is `preview-analyze-…-leftover-join`; the only non-review leftover-join JSONs containing the string `DR-131` are the g24–g28, g30 and sarif GATE joins). DR-131's leftover-design is measured on:

- **Row-level measurement:** `docs/coop/artifacts/preview-analyze-nt-gate-join.v2.json` (`4081c7400b3b9eae61089bb807140b4f75f5dd512b664c1f6657553a7da03813`, recorded D-148 as "DR-131 leftover-design measurement") and `docs/coop/artifacts/preview-analyze-admission-leftover.v1.json` (`1222501032917790832a3ffa8f3953ceb7a73907942a5ea30442346bf59935a5`, recorded D-149 as "DR-131 leftover grouping"). Measured at the same path the gate-join table below uses: `preview-analyze-nt-gate-join.v2.json` `summary.leftoverDesign` = `["NT-1","NT-2","NT-3","NT-5","NT-6","NT-7","NT-8"]` (top-level `.leftoverDesign` absent; per-class `classes[].leftoverDesign` is `true` for those seven and `false` for NT-4; `summary.dischargedByNamedDR133Classes` = `["NT-4"]`; `summary.requiredNowUnchanged` = `19`). `preview-analyze-admission-leftover.v1.json` carries neither a top-level `leftoverDesign` nor a `summary` key (both measured `null`). The v2 bytes still flag those seven classes: they are frozen at the D-148 measurement (`NT-1, NT-2, NT-3, NT-5, NT-6, NT-7, and NT-8 remain leftover-design.` … `Gates 2 and 3 do not hold.`, COORD lines 6219–6224), and D-148 itself named the closing route (`a later D-000 cycle may close the seven leftover classes by naming them at one or more condition-4 / DR-G* obligations.`, lines 6225–6228). That closing was recorded class-by-class by later entries, not by a new artifact version: D-150 (`NT-1 and NT-2 leftover-design closes: remainder is G24 execution.`, lines 6304–6305), D-151 (NT-3), D-152 (NT-5), D-153 (NT-6), D-154 (`NT-7 and NT-8 leftover-design closes: remainder is G28 execution.`, lines 6467–6468). So the v2 artifact's seven-class flag is superseded in COORD but not in its own bytes; no later version of either artifact is recorded (COORD names only v2 / v1).
- **Gate-level current joins (the ones whose `leftoverDesign` flags are current in the record, per D-249..D-253):** the five DR-131 gate joins below. "Current" per the recording entry named in each row; no later version file exists for any of the five (`ls` shows g24 ≤ v4, g25 ≤ v5, g26 ≤ v4, g27 ≤ v4, g28 ≤ v4).

| Join file (current) | sha256 (re-measured; matches recording entry) | Recorded by | `registerRow` | DR-131 classes named | `summary.leftoverDesign` |
|---|---|---|---|---|---|
| `g24-leftover-join.v4.json` | `c451f7ce20e93442172322ff2fd29a029a9a0ca209538ece7c590d32c72e43d7` | D-250 | `DR-G24` | `["NT-1","NT-2"]` | `["OBL-G24-FX-AUTHORING"]` |
| `g25-leftover-join.v5.json` | `9f2b137fe0b01830b4113ef26c8283214a75982f588f164391d61c5510f67aa3` | D-249 | `DR-G25` | `["NT-3"]` | `["OBL-G25-FX-AUTHORING"]` |
| `g26-leftover-join.v4.json` | `aba91c5a43f77ccb9244977c746ca8238b54a4e3af5f431b37b74ce6e5e68591` | D-251 | `DR-G26` | `["NT-5"]` | `["OBL-G26-FX-AUTHORING"]` |
| `g27-leftover-join.v4.json` | `630b226a852e2d6479513559cb0773fad67f80271d4814e726fc69c3aa943a5f` | D-252 | `DR-G27` | `["NT-6"]` | `["OBL-G27-FX-AUTHORING"]` |
| `g28-leftover-join.v4.json` | `604dc98dfc4fd6ec2df1c22f2169b5ec921f2f43ab43ef7e0c98b48750dee085` | D-253 | `DR-G28` | `["NT-7","NT-8"]` | `["OBL-G28-FX-AUTHORING"]` |

All five: `status` `"CANDIDATE-NOT-APPLIED"`, `binds` `"NOTHING"`, `file08StatusToken` `"OPEN"`, `summary.classAOpened` `false`, `summary.dr131Satisfied` `false`, `summary.requiredNowUnchanged` `28`.

Every obligation on those five joins, with its `leftoverDesign` flag (31 obligation objects; 5 flagged `true`):

| Join | `id` | `leftoverDesign` | `rideStanding` | `executionObligationOwnerToday` |
|---|---|---|---|---|
| g24 v4 | `OBL-G24-HARNESS-SPEC` | `false` | `qualification-at-named-gate` | `Product + CLI / output` |
| g24 v4 | `OBL-G24-NAMED-CORPUS` | `false` | `specified-not-leftover` | `Product + CLI / output` |
| g24 v4 | `OBL-G24-INPUT-CORPUS` | `false` | `specified-not-leftover` | `Product + CLI / output` |
| g24 v4 | **`OBL-G24-FX-AUTHORING`** | **`true`** | `not-capable-of-riding as execution-only remainder` | `none` |
| g24 v4 | `OBL-G24-EXECUTION` | `false` | `qualification-at-named-gate` | `Product + CLI / output` |
| g24 v4 | `OBL-NT12-UNNAMED-REMAINDER-CLOSED` | `false` | `specified-not-leftover` | `none as leftover-design` |
| g25 v5 | `OBL-G25-HARNESS-SPEC` | `false` | `qualification-at-named-gate` | `Product + CLI / output + semantic owners` |
| g25 v5 | `OBL-G25-NAMED-CORPUS` | `false` | `specified-not-leftover` | `Product + CLI / output + semantic owners` |
| g25 v5 | `OBL-G25-INPUT-CORPUS` | `false` | `specified-not-leftover` | `Product + CLI / output + semantic owners` |
| g25 v5 | **`OBL-G25-FX-AUTHORING`** | **`true`** | `not-capable-of-riding as execution-only remainder` | `none` |
| g25 v5 | `OBL-G25-EXECUTION` | `false` | `qualification-at-named-gate` | `Product + CLI / output + semantic owners` |
| g25 v5 | `OBL-NT3-UNNAMED-REMAINDER-CLOSED` | `false` | `specified-not-leftover` | `none as leftover-design` |
| g26 v4 | `OBL-G26-HARNESS-SPEC` | `false` | `qualification-at-named-gate` | `Output/operability + CLI/product owners` |
| g26 v4 | `OBL-G26-NAMED-CORPUS` | `false` | `specified-not-leftover` | `Output/operability + CLI/product owners` |
| g26 v4 | `OBL-G26-INPUT-CORPUS` | `false` | `specified-not-leftover` | `Output/operability + CLI/product owners` |
| g26 v4 | **`OBL-G26-FX-AUTHORING`** | **`true`** | `not-capable-of-riding as execution-only remainder` | `none` |
| g26 v4 | `OBL-G26-EXECUTION` | `false` | `qualification-at-named-gate` | `Output/operability + CLI/product owners` |
| g26 v4 | `OBL-NT5-UNNAMED-REMAINDER-CLOSED` | `false` | `specified-not-leftover` | `none as leftover-design` |
| g26 v4 | `OBL-G17-REMAINS-INAPPLICABLE` | `false` | `specified-not-leftover` | `none` |
| g27 v4 | `OBL-G27-HARNESS-SPEC` | `false` | `qualification-at-named-gate` | `Product + CLI / output` |
| g27 v4 | `OBL-G27-NAMED-CORPUS` | `false` | `specified-not-leftover` | `Product + CLI / output` |
| g27 v4 | `OBL-G27-INPUT-CORPUS` | `false` | `specified-not-leftover` | `Product + CLI / output` |
| g27 v4 | **`OBL-G27-FX-AUTHORING`** | **`true`** | `not-capable-of-riding as execution-only remainder` | `none` |
| g27 v4 | `OBL-G27-EXECUTION` | `false` | `qualification-at-named-gate` | `Product + CLI / output` |
| g27 v4 | `OBL-NT6-UNNAMED-REMAINDER-CLOSED` | `false` | `specified-not-leftover` | `none as leftover-design` |
| g28 v4 | `OBL-G28-HARNESS-SPEC` | `false` | `qualification-at-named-gate` | `Product + CLI / output` |
| g28 v4 | `OBL-G28-NAMED-CORPUS` | `false` | `specified-not-leftover` | `Product + CLI / output` |
| g28 v4 | `OBL-G28-INPUT-CORPUS` | `false` | `specified-not-leftover` | `Product + CLI / output` |
| g28 v4 | **`OBL-G28-FX-AUTHORING`** | **`true`** | `not-capable-of-riding as execution-only remainder` | `none` |
| g28 v4 | `OBL-G28-EXECUTION` | `false` | `qualification-at-named-gate` | `Product + CLI / output` |
| g28 v4 | `OBL-NT78-UNNAMED-REMAINDER-CLOSED` | `false` | `specified-not-leftover` | `none as leftover-design` |

The five `true` obligations name the unauthored corpora verbatim (`namedCorpusNotAuthored`): `hostile-but-well-formed admission corpus (DR-131 NT-1, NT-2)`; `missing-required-rung corpus (DR-131 NT-3)` (with `namedNt3Readings` `["NT-3.missing-required-rung","NT-3.universe-unconstructible"]`); `refuse-or-not-offer corpus (DR-131 NT-5)`; `no-silent-promotion corpus (DR-131 NT-6)`; `host-must-not-mint corpus (DR-131 NT-7, NT-8)`. Each `reason` states the join `does not invent fixture bytes`.

NT-4's execution home is G21/G23 (D-148). Current `g21-leftover-join.v13.json` `summary.leftoverDesign` = `["OBL-G21-FX-AUTHORING"]`; current `g23-leftover-join.v8.json` `leftoverDesign` = `[]`. Neither names DR-131 by string; whether G21's FX-AUTHORING leftover bears on DR-131 NT-4 is not stated in the record.

---

## 8. Options, with consequences for Condition 2

Condition 2 today: `**5 of 32 `SATISFIED`**`, `**NOT MET**` (file 08 line 415). DR-131 is in the SATISFIED-requiring set (D-134: `the 21 rows D-002 named plus **DR-131** and **DR-133** (cardinality 23)`).

**Option 1 — Open Class A now (a T2-02 acceptance entry on v2 at `081ff7fb…`).**
- Immediate Condition-2 effect: none. `5 of 32` unchanged; gate 1 only. Requires an owed MF-6 to the Status cell (D-138→D-141 precedent) — also zero readiness effect.
- Unlocks: a dedicated SATISFIED-GRADE cycle (gate 4) on DR-131 may be drafted. If that cycle accepts and its MF-6 (gate 5) lands, Condition 2 becomes 6 of 32 (5 + 1), still `NOT MET`.
- Risk carried into that cycle: gate 2 is contested in bytes (§5). If the SATISFIED-GRADE reviewers read the five `OBL-G2x-FX-AUTHORING` `leftoverDesign: true` flags as design remainder under D-056 clause 5, the cycle fails on gate 2 regardless of the opening; the opening entry would then stand alone with no dependent act. If they read D-154 as governing, the cycle can proceed. Not in the record: any reviewer verdict on this question for DR-131.
- Sub-choice (§6 item 3): (i) coordinator act reads the existing 0/0 verdicts as application-grade, or (ii) fresh dual application-grade review first. (ii) costs one more review round on unchanged bytes; (i) risks a reviewer OBJECT that the verdicts' own grade sentences are "express reservations" that a coordinator act cannot re-read (the D-001 T2-02 EIR-v6 precedent: `accepted as CANDIDATE only`).
- Product consequence: the pack identity `opensip.preview.typescript.pack` version `1` and the eight NT laws become the accepted product law for preview `analyze` at design level (still `binds NOTHING` until applied per route A; application is a further act).

**Option 2 — Do not open Class A.**
- Condition 2 stays `5 of 32`; DR-131 stays `OPEN`, Blueprint impact `Hard blocker for preview `analyze``. Grok's standing instruction (`Do not SATISFY DR-117 / DR-131 / DR-133 (Class A unopened).`) continues to describe the state.
- Nothing mechanical remains on DR-131 (STATUS §3.A is complete); the row cannot move without this decision.
- The handoff's five-item completion bar (STATUS §1: `DR-131, DR-133, DR-117 SATISFIED; Condition 2 MET; identity cited via D-077/D-078`) stays at `all five NOT MET`.

**Option 3 — Open conditionally.** Byte-supported conditions the owner could attach (each is a "what must change first" answer to B1):
- (a) *Gate-2 ruling first*: a D-000 entry stating whether `OBL-G24..G28-FX-AUTHORING` `leftoverDesign: true` blocks gate 2 for DR-131 (i.e. whether D-154's "hold" governs or the joins' clause-5 reading governs). Consequence: if the ruling is "blocks", then fixture authoring for five corpora (DECISIONS-NEEDED §D delegation question) must precede any SATISFIED-GRADE cycle; the opening alone still has zero Condition-2 effect. If "does not block", Option 1 proceeds cleanly.
- (b) *Fresh application-grade dual review first* (§6 item 3(ii)), then the opening entry cites those verdicts. Consequence: one additional review round; removes the "candidate-only limitation" argument at gate 1.
- (c) *Advisory landing first*: a v3 successor landing `CLAUDE-PAC-V2-ADV-1` (NT-7/NT-8 `'Refused.'` idiom) and `DR131V1-ADV-1` (D-079 traceability). Consequence: new bytes, new dual review, new recording (D-138 successor) before any opening; both advisories are recorded as non-blocking "honesty work", so this is optional under the record.
- (d) *Open together with DR-133 and DR-117* (packets B2/B3). Consequence: the candidate's `joins.dr133` pins `provider-only-output-contract.v3.json` `ef2a7416…` (D-136) and `joins.dr117` pins `preview-product-boundary-successor.v5.json` `5face6a9…` (D-137) — v5, not the current v8 (D-207). Opening DR-131 alone leaves those pins at candidate grade; whether a Class A contract may pin sibling candidates is not addressed in the record.

**Orchestrator recommendation:** Option 3(a) then Option 1 — obtain a byte-recorded gate-2 ruling for DR-131 (one D-000 cycle, zero readiness effect) before spending the opening, because the opening's only value is the SATISFIED-GRADE cycle it unlocks and that cycle's outcome currently turns on an unreconciled pair of ADOPTED bytes (D-154 vs. D-249..D-253). If the owner prefers a single act, Option 1 with sub-choice (ii) (fresh application-grade review) is the shape least exposed to a reviewer OBJECT at gate 1.

---

## 9. Open questions the bytes do not resolve

- **Q1 (gate 1 evidence).** D-001 T2-02 says the *independent review* "grants application-grade acceptance". Both existing DR-131 verdicts grant candidate grade in terms. Can a reviewed coordinator act (the venue D-168/D-207 name for the sibling row) supply the application grade the verdicts withheld, or must new verdicts be obtained? Not in the record.
- **Q2 (gate 2 reading).** D-154 (ADOPTED 2026-08-15): `After this act, D-056 Eligibility gates 2 and 3 hold for DR-131's eight NT classes.` D-249..D-253 (ADOPTED 2026-08-23) record joins carrying `OBL-G2x-FX-AUTHORING` `leftoverDesign: true` whose `reason` cites D-056 clause 5, without restating gate 2 for DR-131. Which governs at a later SATISFIED-GRADE cycle? Not in the record.
- **Q3 (artifact bytes vs. act).** After an opening act, the artifact at `081ff7fb…` still reads `status: "CANDIDATE-NOT-APPLIED"`, `sealRecommendation: "DO-NOT-SEAL"`, `doesNot: "Does not open D-056 Class A."`. The record (D-168/D-207) says the artifact is not the venue; it does not say whether a frozen artifact whose own bytes deny Class A can nevertheless stand as the Class A contract. Not in the record.
- **Q4 (NT-4 home).** D-148 places NT-4 at G21/G23 as DR-133 execution and expressly does not name DR-131 NT-4 there. Current G21 join carries `OBL-G21-FX-AUTHORING` leftover-design. Whether that bears on DR-131's gate 2 is not stated.
- **Q5 (sibling pins).** The candidate pins DR-117 at v5 (D-137) while v8 (D-207) is current. Whether a Class A opening on DR-131 requires re-pinning is not in the record.
- **Q6 (post-opening cell text).** The exact Status-cell bytes after an opening are not in the record; Appendix A offers DRAFT bytes only.

---

## Appendix A — DRAFT (not proposed, not dispatched, not reviewed) of a T2-02 application-grade acceptance entry

> **DRAFT — for the owner's inspection only. Entry number to be assigned at recording (next unused after D-292). Every bracketed item is a choice the owner must make; nothing here is adopted.**
>
> `## D-NNN — Open D-056 Class A for DR-131: record preview-analyze-contract.v2 at application grade with no express reservation`
>
> - **Date:** [date of recording]
> - **Status:** [dual CONSENT record: reviewer paths + sha256, turn number, subject draft sha256 — filled at recording]
> - **Decision type:** PREFERENCE-LADEN (product-boundary lift on a row owned by `Product + CLI / output`), made by the user and recorded verbatim in the D-132 form; the recording act itself is RULE-GOVERNED under D-000. Gate-1-only act. Not a SATISFIED re-record. Not an MF-6.
> - **Subject:** `docs/coop/artifacts/preview-analyze-contract.v2.json` `081ff7fb529b34a3db3ac9f4c7505848e2253be12b5a867d39b49b3a26d56970` (unchanged since D-138; re-measured at HEAD [hash]).
> - **User words, recorded verbatim:** [the owner's exact words opening Class A for DR-131].
> - **Verdicts relied on for "application-grade acceptance":** [EITHER (i) `preview-analyze-contract.v2.review-independent.claude2.json` `22a0d892…` ACCEPT 0/0 and `preview-analyze-contract.v2.review-independent.codex.json` `e48cb592…` ACCEPT 0/0, read at application grade by this reviewed act; OR (ii) new verdict paths + sha256 from a fresh dual application-grade review of the same bytes].
> - **Route-A acceptance property (D-001 T2-02):** [MET / NOT MET — must be measured in the entry]. Reservation-language sweep of the verdict(s) and the subject: [list every `reserv`/`candidate`/`not for application`/`apply-condition` hit and its disposition, in the D-015 form]. Named apply-conditions left undischarged: [none / list].
> - **Decision:** D-056 Eligibility gate 1 (Class A) is opened for DR-131 on `preview-analyze-contract.v2` at `081ff7fb…`: an independently accepted design contract exists at 0 blockers with application-grade acceptance and no express reservation, recorded by this D-000 entry; the row's lead label is `OPEN`. The D-138 / D-141 reservation `Class A not opened` is lifted for DR-131 only. The artifact's own `status`, `sealRecommendation`, and `doesNot` fields are frozen bytes of a recorded candidate and are not the venue for this lift (D-168 / D-207). Gate 2 standing: [EITHER "D-154 governs: gates 2 and 3 hold for DR-131's eight NT classes; `OBL-G24..G28-FX-AUTHORING` remain leftover-design at their gates as condition-4 work" OR "not ruled here; reserved to the SATISFIED-GRADE cycle"]. Gate 3: NT-1/2 at DR-G24 (D-150), NT-3 at DR-G25 (D-151), NT-5 at DR-G26 (D-152), NT-6 at DR-G27 (D-153), NT-7/8 at DR-G28 (D-154), NT-4 at G21/G23 as DR-133 execution (D-148). Gates 4 and 5 are not performed. DR-131 stays `OPEN`. Not SATISFIED. Not eligible-in-kind is superseded for DR-131 only to the extent of gate 1. Does not close `OBL-G24-FX-AUTHORING`, `OBL-G25-FX-AUTHORING`, `OBL-G26-FX-AUTHORING`, `OBL-G27-FX-AUTHORING`, or `OBL-G28-FX-AUTHORING`. Does not author fixture bytes. Does not execute NT-1..NT-8. Does not apply the candidate per route A. Does not open Class A for DR-117 or DR-133. Does not mint a D-096 (A) grant. Does not change required-now 28. Does not edit file 08. Does not authorize `docs/v2/implementation/`. Advisories CLAUDE-PAC-V2-ADV-1 and DR131V1-ADV-1 continue as honesty work. **Owed later work, not performed here:** (1) an MF-6 act updating the DR-131 Status cell (DRAFT after-bytes below); (2) a dedicated SATISFIED-GRADE D-000 cycle for DR-131 (gate 4) and its MF-6 (gate 5), each its own act.
> - **Readiness effect:** Zero SATISFIED. Condition 2 stays 5 of 32. Condition 4 stays MET on the naming half (28 of 28). Condition 5 last.
> - **Reversibility:** Total before the owed MF-6 or a dependent SATISFIED-GRADE cycle lands. Overturn restores the D-138 / D-141 standing `Class A not opened` for DR-131. Does not unwrite D-138, D-141, D-148..D-154, or D-249..D-253. Overturn: C-D-NNN.
> - **Commit:** C-D-NNN.
>
> **DRAFT after-bytes for the owed MF-6 (Status cell of the row beginning `| DR-131 |` only; D-141 form):**
>
> `**OPEN** — accepted design contract (D-138; D-056 Class A opened D-NNN): [`preview-analyze-contract.v2.json`](../../coop/artifacts/preview-analyze-contract.v2.json) `081ff7fb529b34a3db3ac9f4c7505848e2253be12b5a867d39b49b3a26d56970` — binds NOTHING until applied. Gates 4–5 not performed. Not SATISFIED.`
>
> (Removes only `` `CANDIDATE-NOT-APPLIED`, binds NOTHING. Not eligible in kind today (D-133).``; keeps `**OPEN**` and `Not SATISFIED.`; Blueprint-impact cell unchanged; snapshot stays 5 of 32.)

---

## Appendix B — Citations relied on

File 08 (`docs/v2/architecture/08-decision-and-readiness-register.md`, `e503b75b…`): line 280 (table header); line 284 (DR-102 row, Class A precedent form); line 313 (DR-131 row, all seven cells); lines 360–364 (DR-G24..DR-G28 rows); line 415 (condition-2 snapshot row).

COORD (`docs/coop/COORDINATOR-DECISIONS.md`, `47f7b201…`): D-001 (heading line 60; T2-02 bullet lines 181–190); D-015 lines 1201–1216 (Route-A acceptance property MET; DR-102 precedent); D-056 lines 3343–3396 (Status pin `dfb0c2af…`; Decision incl. D-133 forward pointer); D-085 lines 3508–3541 (DR-102 SATISFIED under Class A); D-132 lines 5554–5617 (user grant; clause 5); D-133 lines 5621–5670 (gates are a property; "does not name DR-131 or DR-133 as eligible today"); D-134 lines 5674–5707; D-135 line 5711 heading; D-137 Decision..Commit lines 5809–5832 (heading 5779); D-138 lines 5836–5891; D-139 lines 5892–5932; D-141 lines 5967–5994; D-148 lines 6198–6238; D-149 lines 6240–6278; D-150 lines 6280–6320; D-151 lines 6322–6360; D-152 lines 6362–6401; D-153 lines 6403–6441; D-154 lines 6443–6483 (esp. 6467–6472); D-168 (heading line 7061; venue sentence lines 7094–7095) and D-207 (heading line 9062; venue sentence lines 9098–9099); D-249 lines 12127–12206; D-250 lines 12208–12293; D-251 lines 12295–12362; D-252 lines 12364–12430; D-253 lines 12432–12498; D-292 (heading line 16035; line 16105 "Gate 1 Class A is not opened.").

Artifacts (`docs/coop/artifacts/`, sha256 re-measured at HEAD): `preview-analyze-contract.v2.json` `081ff7fb…`; `preview-analyze-contract.v2.review-independent.claude2.json` `22a0d892…`; `preview-analyze-contract.v2.review-independent.codex.json` `e48cb592…`; `coordinator-decisions.D-056.turn2.draft.md` `dfb0c2af…` (lines 95–124 Eligibility; 186–190 Decision clause 5; 170–174 Decision clause 2); `coordinator-decisions.D-138.turn2.draft.md` `c609de64…` (lines 55–83); `coordinator-decisions.D-141.draft.md` (lines 49–62, before/after cell bytes); `preview-analyze-nt-gate-join.v2.json` `4081c740…`; `preview-analyze-admission-leftover.v1.json` `12225010…`; `g24-leftover-join.v4.json` `c451f7ce…`; `g25-leftover-join.v5.json` `9f2b137f…`; `g26-leftover-join.v4.json` `aba91c5a…`; `g27-leftover-join.v4.json` `630b226a…`; `g28-leftover-join.v4.json` `604dc98d…`; `g21-leftover-join.v13.json` `058717f5…`; `g23-leftover-join.v8.json` `498324e5…`.

Working documents: `DECISIONS-NEEDED.md` §B (B1, B3 parenthetical); `STATUS.2026-08-26.md` §1 table, §2 items 1–2, §3.A; `HANDOFF.D-000-orchestrator-live.txt` line 83.
