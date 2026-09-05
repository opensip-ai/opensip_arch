# G-six-amended — Claude round 1

Recommendation file. Covers **only** the six ids named in `DECISION-PACKETS/G-six-amended.md`:
Q1, Q8, G3-G18, G3-HOSTILE, G21-SCHEMA, G21-NT6.

Protocol: `DECISION-PACKETS/RECOMMENDATION-PROTOCOL.md`. Nothing here decides anything; the owner decides.

Measured at HEAD `f3b05e33479652ede37f0502084b50b590f630f7` (last COORD heading `## D-314`). Date 2026-08-29.

## Pins re-verified at this HEAD

Every pin in the `G-six-amended.md` table was re-hashed, not copied:

| Pin | sha256 (measured) | Matches packet |
|---|---|---|
| file 08 `docs/v2/architecture/08-decision-and-readiness-register.md` | `e503b75b5599444ee4d7…` | yes |
| COORD `docs/coop/COORDINATOR-DECISIONS.md` | `7cc3d7f07f1313c4fdd8…` | yes |
| `DECISION-PACKETS/G-owner-residuals.md` | `c667cf4f8bf262c5bc19…` | yes |
| Claude r1 | `3025c0729d0154b3bdbf…` | yes |
| Codex r1 | `83cb6d58eec313dd1daf…` | yes |
| Claude r2 | `a96b868e78ae5ed101b3…` | yes |
| Codex r2 | `59802450a098b7a16acf…` | yes |

Artifact digests cited below were also re-measured at this HEAD and all match the round-2 text:
`signed-index-trust-contract.v14` `039a5702…`, `component-manifest-schemas.v11` `1c0b8868…`,
`component-manifest-leftover-join.v15` `f27ffac2…`, `lifecycle-leftover-join.v4` `bcc76ee3…`,
`anti-lockstep-hostile-goldens.v3` `8be1b6c5…`, `anti-lockstep-leftover-join.v3` `820d724a…`,
`g21-leftover-join.v13` `058717f5…`, `g21-fixture-corpus.v11` `13ede110…`,
`g21-fixture-corpus.v14` `1012bb02…`, `control-protocol-contract.v2` `c50a79fe…`,
`provider-only-output-contract.v3` `ef2a7416…`, `d9-exit-contract.v1.14` `8dd33038…`,
`delivery.v2` `47b6cfd1…`, `g18-leftover-join.v6` `f531ba6a…`.

---

## 0. Summary of this round

**All six D-314 dispositions are confirmed. None is changed.** D-314 adopted the round-2 text for these six
(`## D-314` Decision: "Those six are adopted in the round-2 text, not the round-1 text"), and on re-measurement
every one of the six *dispositions* is what the live bytes support.

What this round adds is a **byte-level audit of the reasoning that carries those dispositions**, done against
live bytes rather than against the round-2 file. That audit found **three defective citations and one
unstated condition** in the adopted round-2 text. None of them changes an answer; all four would be legitimate
targets for an adversarial reviewer, and two of them are simply wrong on the bytes. They are corrected here so
that the text a later act cites is the text that survives re-checking.

| # | Where | Defect | Effect on the disposition |
|---|---|---|---|
| 1 | Q1 | Round 2 says `totalDecision` entries `[0] [1] [2] [3] [5]` "all give `alreadyRunning` as bare `refuse`". Measured: `[3]` is a **continue** entry, and `[0]` carries a gloss. | None. The asymmetry it was offered to prove survives; the arithmetic does not. |
| 2 | G21-SCHEMA | Round 2 attributes the ranked reviewer-attack list to `D1-plan/G21.md` §6 and calls vocabulary invention "second-ranked". Measured: the list is in `D1-plan/DR-122-SARIF.md`, where it is **(a)**; G21's own §6 names **(c)** as dominant. | None. Both readings support the disposition. |
| 3 | G3-G18 | Round 2 writes "G18's own `$.doesNot` / `$.failsIf`". Measured: `g18-leftover-join.v6.json` has **no `failsIf` member**; the fields are the occupancy's. Round 1 had the attribution right. | None. Corrected attribution. |
| 4 | G21-SCHEMA | The truncated-body split is stated unconditionally. The record groups truncated bodies **with** the six as body-requiring. The split holds only on a zero-delivered-bytes reading. | None, but the condition must be stated for the disposition to be evaluable. |

Two freshness upgrades are also made: G21-SCHEMA now cites the live latest corpus `g21-fixture-corpus.v14`
(D-302) rather than `v11` (D-301), and Q8 now names `OQ-G15-3`, the recorded qualification of its own
cost-of-deferral claim.

---

## 1. Q1 — OD-112-3 wording after D-309

### Recommendation — **confirm D-314 unchanged**

Keep the existing **preview** refusal as the decided OD-112-3 standing; retain OD-112-3 in
`namedOpenDecisions` with an explicit DECIDED standing rather than removing the entry; do not widen the policy
beyond the preview product stage without a separate owner act.

### Rationale

**The live byte records the residual as an open axis with two limbs, and it names both.**
`docs/coop/artifacts/signed-index-trust-contract.v14.json` `039a5702…`
`$.namedOpenDecisions[2].standing`, verbatim:

> "D-293: OD-112-3 is the final fail-closed policy. Residual axis, named not chosen: whether the
> signed-index-trust-contract.v8 standing token Preview refuse remains, where preview is the product-stage
> scope term of this artifact (roles[].preview, A preview payload), or the standing is fail-closed refuse
> without that stage qualifier; and whether OD-112-3 remains in namedOpenDecisions or leaves it. OD-112-3 is a
> policy, not a number."

That single field carries limb (a) (keep or drop `preview`) *and* limb (b) (stay in or leave the array). The
recommendation answers exactly the two limbs the byte names, and invents no third.

**"preview" is a defined product-stage term in this artifact, not a loose word.** `$.roles` is a five-member
array and every member carries a `preview` field — `TR-CORE`, `TR-INDEX` and `TR-COMPONENT` each
`"in G08 install scope"`, `TR-BUNDLE` `"named; not a required preview shipping surface"`, `TR-REPAIR`
`"DEFERRED with DR-110. Named so the role is not silent."` So the standing byte's own gloss —
"where preview is the product-stage scope term of this artifact (roles[].preview…)" — is checkable, and
dropping the qualifier is a scope widening, not a tidy-up.

**The adopted C1 text preserves the qualifier, and Q0 is what makes that text reach.**
`DECISION-PACKETS/C1-4-reserved-numbers-security-quality.claude-recommendation.r2.md` `44f51a5d…` line 6,
verbatim: "**C1 DR-112:** record OD-112-3 now as a final fail-closed decision (**the existing preview refusal
stands**)." D-314 item 4 confirms the bounded incorporation that makes that content adopted. So limb (a) is
already answered by adopted text; the recommendation records it rather than re-deciding it.

**Limb (b) is supported by the nearest recorded analogue.** D-304 (packet §0) recorded OBL-OD-2 with
`leftoverDesign` false and bucket `specifiedNotLeftover` — a **changed standing**, not a deleted entry. D-314
item 14 confirms that bucket. Retaining OD-112-3 with a DECIDED standing follows the same recorded shape.

### Correction to the adopted round-2 text (defect 1)

Round 2 wrote: "entries `[0]`, `[1]`, `[2]`, `[3]` and `[5]` all give `alreadyRunning` as bare `refuse`; only
`[4]` … carries the stage qualifier." Re-measured, `$.offlineRunningPolicy.totalDecision` has **eight** entries
and that sentence is wrong twice:

- `[3]` (`TR-INDEX` ST-EXPIRED/ST-STALE-REVOCATION with TR-COMPONENT and TR-CORE ST-TRUSTED) is **not** a
  refusal at all — `alreadyRunning` is `"continue already-installed verified component processes"`.
- `[0]` is not bare — `"refuse (do not treat survival as trust)"`.

**Corrected statement, measured:** `alreadyRunning` is a refusal at `[0]`, `[1]`, `[2]`, `[5]` and `[7]`; it is
the bare token `"refuse"` at `[1]`, `[2]`, `[5]` and `[7]`; `[0]` carries a non-stage rationale gloss; `[3]` and
`[6]` are continue entries; `[4]` currently carries the residual-axis paragraph itself rather than an operative
token. **The point the sentence was offered to prove survives intact:** no entry other than `[4]` carries a
*product-stage* qualifier, so once the chosen wording replaces the paragraph, `[4]` becomes the only
stage-qualified refusal in its table.

### What changes if adopted

A `signed-index-trust-contract` successor and its paired signed-index leftover-join successor recording the
chosen wording, through the normal Stage A + Stage B cycle. Both the `$.namedOpenDecisions[2].standing` and the
`$.offlineRunningPolicy.totalDecision[4].alreadyRunning` residual-axis sentences are replaced by the chosen
wording; nothing else in the contract moves. **No file-08 edit.** DR-112 stays `OPEN` (file 08 line 294,
re-measured). No Condition-2 movement.

**Drafting requirement the successor must carry.** The successor must say plainly that the qualifier is the v8
standing token carried forward under the adopted C1 wording, and must **not** silently harmonise `[4]` with the
four bare-refuse entries. A silent harmonisation is the scope widening this recommendation forbids, arriving by
a side door.

### Risk

*If adopted:* `[4]` remains the only stage-qualified refusal in an eight-entry table, and every later reader
will ask why; the successor answers that in words rather than by editing the token.
*If the wider reading were adopted instead:* it would contradict adopted C1 text and extend a security policy's
scope by inference from the single word "final" — against a byte that expressly says D-293 did not choose that
axis.

### Confidence

**High.** The disposition is carried by adopted text plus a live byte that names both limbs. The correction
above is to a supporting sentence, not to the answer.

---

## 2. Q8 — OD-1 four cap values / what "measured caps" measures

### Recommendation — **confirm D-314 unchanged**

Leave the OD-1 numeric limb explicitly open and supply no cap values. Any later value proposal must state an
evaluable measurement method and follow the recorded product-owned D-006 pattern the artifact itself names.
This answer creates **no** gate/corpus/runner prerequisite of its own.

### Rationale

**The artifact declines to mint the numbers and says why, in its own words.**
`component-manifest-schemas.v11.json` `1c0b8868…` `$.namedOpenDecisions[0]`, re-measured:
`standing` = "NO caps are stated in these schemas, and that absence is a NAMED OPEN DECISION, not a default…";
`candidateOwners` names DR-115's numeric-threshold machinery, "which already owns the core's size/startup/memory
numbers, DECIDED at D-006, with the measurement half at qualification", and closes: "This artifact declines to
mint the numbers: a cap is a product threshold, and thresholds in this corpus are **product-owned, measured, and
waiver-formed (the D-006 pattern)**."

**No gate measures the four quantities, and the join says so.**
`component-manifest-leftover-join.v15.json` `f27ffac2…` `$.obligations[9]` (`OBL-OD-1`) records
`leftoverDesign: true`, `existingGate: "none"`, `executionObligationOwnerToday: "none"`,
`rideStanding: "not-capable-of-riding"`, and in `reason`, verbatim: "existingGate stays none; **no gate measures
these four quantities**." The same field names this very question — "**Q8 (what measured caps measures)** and
Q9 … are named, not answered" — so the live byte anticipates the answer being given here rather than there.

**The round-1 triad stays withdrawn, and re-measurement confirms why.** "Named corpus" and "named runner class"
appear nowhere in `$.namedOpenDecisions[0]`. The "named runner/workload" language belongs to a different row:
`control-protocol-contract.v2.json` `c50a79fe…`
`$.transportAndFraming.framing.bounds.constantsStatus`, verbatim — "Operational timeout/deadline VALUES are
deliberately not bound here … because **a numeric threshold without a named runner/workload measures nothing
(the D-006 lesson recorded in D-007's alternatives)**." That is an instructive precedent about *this* framing
clause, and expressly not a DR-103 prerequisite. Choosing the leave-open option while minting a new binding
rule in the same breath is what D-293 Decision 6 exists to prevent.

**The cost of deferring is bounded — and the record itself qualifies that.** C7's precondition bites only on
"oversized-input fixtures" (`DECISIONS-RECOMMENDED.md` C7, quoted at `D1-plan/G15.md` line 647). I re-measured
`$.testCorpusRequirements.classes[3]` (`TC-PATH`) in `schemas.v11`: its thirteen `requires` members carry no
over-length case. I also re-measured the token `oversized` directly in the five G15 governing files named at
`D1-plan/G15.md` §4(d) — `harness.DR-G15.packaging-adapter-conformance.v9.json`,
`at-named-corpus-catalog.v1.json`, `g15-input-corpus.v1.json`, `g15-leftover-join.v6.json`,
`packaging-leftover-join.v4.json` — and the count is **zero in all five**.

### Addition to the adopted round-2 text (precision)

Round 2 presented that boundedness without naming its recorded qualification. **OQ-G15-3** exists precisely to
qualify it, verbatim: the bytes checked "name no over-length manifest, tree, path, or alias case, and the token
`oversized` appears in none of the five G15 governing files. But schemas.v11 `$.namedOpenDecisions[0].consequence`
says 'oversized-input refusal is UNSPECIFIED, not implied - a fixture author must not assume it', which
presupposes that somebody might author one. If a later reading finds one, the dependency is on `OBL-OD-1`, which
is owner-reserved." The honest form of the claim is therefore: **deferring blocks no currently-measured fixture
act, and `OQ-G15-3` records that this is a reading, not a closed proof.**

### What changes if adopted

Nothing recorded; optionally one sentence so later acts can cite the fallback (`DECISIONS-RECOMMENDED.md` §C5–C9,
C7 bullet: "if values are not available, leave the numeric limb open and say so"). `OBL-OD-1` stays
`leftoverDesign: true`; DR-103 stays `OPEN`; Condition 2 unchanged.

### Risk

*If adopted:* the surface stays unbounded in the design, and the owner should see that stated plainly — file 08
line 285, re-measured verbatim: "unbounded-input surface at metadata-only admission; oversized-input refusal
UNSPECIFIED, not implied) remains OPEN with its owner UNASSIGNED between DR-115 and DR-120".
*If numbers were supplied:* `$.namedOpenDecisions[0].consequence` already warns "a fixture author must not
assume it", and no gate exists that could have measured them.

### Confidence

**High.**

---

## 3. G3-G18 — on-disk quarantine format

### Recommendation — **confirm D-314 unchanged**

Leave G18 blocked. Specify no quarantine format now, and do not permit quarantine *fate* without quarantine
*bytes*. The lawful trigger is a **reviewed later implementation successor** that chooses the mechanism and
proves the recorded properties, together with the other recorded type dependencies on this gate.

### Rationale

**D-311 routes the mechanisms to implementation; it does not forbid the implementation.** `## D-311` Decision,
re-measured verbatim: "`$.mechanismReservation.failureRule` remains the acceptance bar regardless of mechanism:
**a later implementation successor that cannot prove P-1..P-8 fails DR-107, regardless of mechanism choice.**"
An entry that names the acceptance bar for a later implementation successor is contemplating that successor.
D-311 also records, verbatim, that "The lock-file-grammar member is classified as implementation scope; it is
not decided. NO lock is producible until DR-111 closes, so that member **waits on C3(ii)** for any lock-shaped
successor" — which is **Q3**, an owner item.

**The ROW twin records the same route, but does not cover the quarantine member.**
`lifecycle-leftover-join.v4.json` `bcc76ee3…` `$.proposedLaterWork[2]`, verbatim: "A later implementation
successor may choose a journal/lock/lease mechanism. That successor must still prove the live file 04
properties. This join chooses none." Re-measured, `[2]` names **journal/lock/lease** and does not name the
quarantine format — so for the quarantine limb the governing citation is **D-311's own Decision**, which names
all seven members including the on-disk quarantine format. The route is the same; the citation must be the one
that covers the member.

**Fate-without-bytes stays refused, on the twin's own rule.** `$.proposedLaterWork[1]`, verbatim: "A later
leftover-design cycle may author fixture implementations for the three named corpus classes **only where types
are already closed**. This join does not invent those bytes." The quarantine type is not closed: the same
file's `OBL-ENCODING-RESERVED` entry records `leftoverDesign: true`, `existingGate: "none"`, and in `reason`,
verbatim, "Contract v2 reserves the reviewed equivalent of atomic rename and the on-disk quarantine format …
Those mechanisms remain reserved. This join does not invent them … This join does not close it." The occupancy
makes quarantine a required half of EV-2 while reserving its format in the same breath —
`harness.DR-G18.lifecycle-generation-recovery.v4.json` `$.retainedEvidence[1].exactByteIntent`, verbatim:
"**Quarantine is required; on-disk quarantine format is reserved.**"

**Closing the obligation needs successors on both joins.** `g18-leftover-join.v6.json` `f531ba6a…`
`$.obligations[3]` (`OBL-G18-FX-AUTHORING`) is `leftoverDesign: true` with
`existingGate: "none as authored implementations"` and three `namedCorpusNotAuthored` classes; the ROW twin's
"only where types are already closed" rule governs any closure.

### Correction to the adopted round-2 text (defect 3)

Round 2 wrote "G18's own `$.doesNot` / `$.failsIf` offer no `blocked-on-ride`-style placeholder vocabulary
(OQ-G18-3)". Re-measured, `g18-leftover-join.v6.json` **has no `failsIf` member at all** (`failsIf` is absent
from its key set), so as written the citation points at a path that does not exist on the named artifact. The
fields belong to the **occupancy**: `harness.DR-G18.lifecycle-generation-recovery.v4.json` carries both
`$.doesNot` and `$.failsIf`, and the string `blocked-on-ride` occurs **zero** times in it. That is what OQ-G18-3
measures, verbatim: "Occupancy `$.doesNot` and `$.failsIf` supply no lawful placeholder standing for a
reserved-format artifact, unlike G15's `blocked-on-ride` fate vocabulary." Round 1 attributed this correctly;
the round-2 compression introduced the error. **Minting a placeholder standing would be new semantics** — a
named open, not a choice — and that conclusion is unchanged.

### Addition: a drafting requirement the successor pair must carry

`OQ-G18-6` records a live staleness a successor must state rather than inherit: the ROW twin
`lifecycle-leftover-join.v4` names the GATE join as "g18 leftover-join.v5 (D-263)" while the current GATE join
is **v6** (D-276), and the two joins carry different live file-08 tokens (`OPEN` versus
`PROPOSED-CLOSED-FOR-REVIEW`). Any successor pair must say which HEAD it measures at.

### The option the owner still has, and what it is worth

Unchanged and still unmeasured: ask which of the **five** live-cell members have closed types and author only
those under the twin's "only where types are already closed" rule. The five are recorded, not invented —
`harness.DR-G18.lifecycle-generation-recovery.v4.json` `$.liveCellMemberSplit.membersInOrder`, verbatim:
`["old-or-new atomicity", "fail-closed recovery", "dependency/state/permission closure", "leases/refcounts",
"reference-safe retained-evidence/rollback removal"]`. It is named so the owner knows the door exists; it is
not recommended, because it has not been measured.

### What changes if adopted

Nothing. `OBL-G18-FX-AUTHORING` stays `leftoverDesign: true` on both joins; the 40 G18 cases
(`g18-input-corpus.v2` initial states) stay unauthored.

### Risk

*If adopted:* G18 stays blocked on two of the owner's **own** open items — the C6 encoding disposition and Q3's
DR-111 windows — so it is not blocked on anything delegable and will not move on its own.
*If a format were specified outside a reviewed implementation successor:* it bypasses the acceptance bar D-311
names, which is the real defect.

### Confidence

**High.**

---

## 4. G3-HOSTILE — per-class golden counts (OQ-HG-5)

### Recommendation — **confirm D-314 unchanged**

Treat the citation-witness floor as **already authored** at D-300. Supply **no** per-class counts. Record an
explicit disposition that the **seven** classes' within-class universals stay named-open, citing the live v3
fields rather than the pre-D-300 plan framing. The `anti-lockstep-leftover-join` remasurement proceeds as
**already-delegated mechanical work** under D-293 Decision 8 if it adds no semantic choice. The cross-row
byte-sharing question stays **separate owner work**.

### Rationale

**The floor is authored, and the artifact says so.** `anti-lockstep-hostile-goldens.v3.json` `8be1b6c5…`
re-measured: `$.summary.authoredMembers` = `16`, `$.summary.authoredFiles` = `16`,
`$.summary.caseCountInvented` = `false`, `$.summary.dr127Satisfied` = `false`;
`$.whatIsAuthored`, verbatim: "Sixteen catalog members. Sixteen UTF-8 .bin citation files … **Five join units
J-1..J-5 and eleven class units CC-1..CC-11.**"; `$.leftoverDesignClosedIfAcceptedAndRecorded` = `[]`.

**The seven-class set is measurable from the live artifact, and CC-6 is the seventh.** I enumerated
`$.classCoverage` directly: exactly **seven** entries carry a `remainingNotAuthored` member —
**CC-1, CC-2, CC-4, CC-5, CC-6, CC-7, CC-9** — and CC-3, CC-8, CC-10, CC-11 carry none.
`$.proposedLaterWork[2]`, verbatim: "Within-class universal quantifiers on **CC-1, CC-2, CC-4, CC-5, CC-6,
CC-7, and CC-9** remain unenumerated. A later corpus may add cases only after those members are named in
governing bytes." `$.remainderAfterThisCorpus`, verbatim: "…because **seven classes** carry unenumerated
within-class quantifiers; sixteen citation witnesses do not exhaust those universals."

**The apparent discrepancy is a superseded plan file, not a conflict in the record.**
`D1-plan/OBL-HOSTILE-GOLDENS.md` **OQ-HG-5** names **six** classes — "Six of the eleven classes carry universal
quantifiers with no member list: CC-1 …, CC-2 …, CC-4 …, CC-5 …, CC-7 …, CC-9 …" — omitting CC-6. The same plan
file, at its `$.handshake.sequence[0..3]` bullet, records those as "the four handshake steps **CC-4 and CC-6**
quantify over". So CC-6 is a quantifying class in the plan's own bytes; OQ-HG-5's enumeration is simply
incomplete, and it is pre-D-300. The live artifact is the current evidence and it resolves the count.

**The remasurement needs no new owner grant.** `## D-293` Decision 8, re-measured verbatim: "**D1 (fixture
authoring).** Delegated to the orchestrator under D-000 review for the enumerated G15, G16, G18, G19, G20, G21,
G24–G30, `OBL-HOSTILE-GOLDENS` and the two DR-122 SARIF fixture obligations, under the agreed semantic,
coverage, dependency and D-000 constraints." The reserved list that follows — G07, G08, G09, G12, G14, G22 with
same-id ROW twins, plus `OBL-WINDOWS-PATH`, `OBL-ENVELOPE-MISMATCH`, `OBL-UNICODE-NORM`,
`OBL-JOIN-FX-AUTHORING`, `OBL-R10-AUTHORING`, `OBL-R6-AUTHORING`, and the G09/DR-105 envelope — does **not**
contain `OBL-HOSTILE-GOLDENS`. So a post-D-300 remasurement that adds no semantic choice needs a D-000 cycle,
not a fresh owner act.

**The byte-sharing question is genuinely separate, and it decides whether the CC work is done once or twice.**
`$.proposedLaterWork[3]`, verbatim: "Whether golden bytes may be shared with OBL-G21-FX-AUTHORING is not decided
here." The same eleven CC classes are measured under two ids on two rows — `OBL-HOSTILE-GOLDENS` on
`anti-lockstep-leftover-join.v3` `820d724a…`, `OBL-G21-FX-AUTHORING` on `g21-leftover-join.v13` `058717f5…`,
whose `$.obligations[3].remainingNotAuthored.dr102` lists `CC-1`…`CC-11`. The custody prohibitions run both
ways and are re-measured: D-300 Decision, "leftover-design of OBL-G21-FX-AUTHORING remains on g21
leftover-join.v13 (D-292)"; D-301 and D-302 each, verbatim, "Does not steal leftover-design of
OBL-HOSTILE-GOLDENS remaining on anti-lockstep-leftover-join.v3." Nothing says whether one authored byte set
may discharge both. That ruling is worth a sentence.

### What changes if adopted

No fixture act. One disposition sentence from the owner; one OQ-HG-4 ruling; one `anti-lockstep-leftover-join`
successor recorded as delegated work citing D-300. No Condition-2 movement — D-300's own recital, re-measured:
"**Readiness effect:** Zero SATISFIED. Condition 2 stays 5 of 32."

### Risk

*If adopted:* `OBL-HOSTILE-GOLDENS` does not close, and DR-127 stays a hard blocker — file 08 line 309,
re-measured, ends "| OPEN | **Hard blocker for independent-release blueprint** |".
*If counts were supplied:* a minted coverage set that seven recorded universal quantifiers contradict, against
an artifact that records `caseCountInvented: false`.

### Confidence

**High.** This is the best-evidenced of the six: the class set was enumerated from `$.classCoverage` directly,
not read off a summary.

---

## 5. G21-SCHEMA — per-type control-frame body schema

### Recommendation — **confirm D-314's split, with one condition made explicit**

*(i)* Six injections stay named-open on the **per-type-schema** trigger: `CC-5 invalid UTF-8`,
`CC-5 duplicate members`, `CC-5 unknown members`, `CC-5 floats`, `CC-5 negative integers`,
`CC-5 over-uint53 integers`.
*(ii)* `CC-5 truncated bodies` stays named-open on the **fixture-form** trigger, `OQ-G21-4` — **conditional on
the witness delivering no body bytes that would require a per-type schema.** If the author elects to deliver
partial body bytes carrying a `type`, the member re-acquires the schema dependency and both triggers apply.

### Rationale

**The schema is recorded as required and recorded as not authored.**
`control-protocol-contract.v2.json` `c50a79fe…` `$.controlFrameEncoding.messageEnvelope`, verbatim: "Every
frame body object has exactly these members: type (string, closed vocabulary at
capabilityEnvelope.messageVocabulary), seq …, controlMajor …, **body (object; per-type schema)**." And
`$.capabilityEnvelope.messageVocabulary` is a closed sixteen-member array (re-measured: `hello`, `helloAck`,
`select`, `selectAck`, `refusal`, `ping`, `pong`, `cancel`, `health`, `healthReport`, `resourceReport`, `fault`,
`effectRequest`, `effectResult`, `shutdown`, `shutdownAck`). The corpus records the schema as unauthored:
`$.whatIsNotAuthored` carries "a ping, pong, hello, helloAck, or **other per-type body schema**".

**Freshness upgrade over round 2.** Round 2 cited `g21-fixture-corpus.v11` `13ede110…` (recorded at D-301). The
live latest recorded corpus is **`g21-fixture-corpus.v14`** `1012bb02…` (D-302). I diffed the two
`whatIsNotAuthored` arrays: v14 drops "per-platform copies of these bytes" and adds "mutation of
fixtures/g21.v11/", and **every CC-5 entry and the per-type-body-schema entry are identical in both**. So the
disposition is unaffected, but the current citation should be v14.

**The bookkeeping partitions exactly, with no gap and no overlap.** `g21-leftover-join.v13.json` `058717f5…`
`$.obligations[3].remainingNotAuthored.remainingCc5Injections` has **ten** entries. Re-measured against the
four owner items: one under **G21-EXACT** (`prefix exactly at the operative bound`); two under **G21-POST**
(`prefix far over the operative bound` — postHandshake half, D-302 verbatim "Does not author the postHandshake
far-over half" — and `prefix one over the postHandshake bound`); one under part (ii); six under part (i).
1 + 2 + 1 + 6 = 10.

**One ruling moves both (ii) and G21-POST.** `OQ-G21-4` asks, in one question, "whether a postHandshake fixture
needs a session script rather than a payload file" — the same fixture-form ruling G21-POST waits on.

### The condition, and the counter-evidence that makes it necessary (defect 4)

Round 2 stated the split unconditionally, resting on the case definition: `D1-plan/G21.md` §2 item 29,
verbatim — "`"CC-5 truncated bodies"` — a prefix `N` with fewer than `N` body bytes delivered." Since `N`
body bytes may be **zero** delivered, no per-type parse is completed and no schema is exercised. That reading is
sound and it carries the split.

But the record groups truncated bodies **with** the six, twice, and an adversarial reviewer will find both:

- `OQ-G21-4`, verbatim: "**Seven** of the ten remaining injections (`truncated bodies`, `invalid UTF-8`,
  `duplicate members`, `unknown members`, `floats`, `negative integers`, `over-uint53 integers`) **require a
  body**".
- `D1-plan/G21.md` semantic-choice item 2 lists the same seven — truncated bodies first — as needing "body
  bytes … drawn from the closed envelope at `#$.controlFrameEncoding.messageEnvelope`", with the **caveat** "a
  body needs a `type` from `capabilityEnvelope.messageVocabulary` and a per-type `body` schema".

So the split is right **only under the zero-delivered-bytes reading**, and stating it unconditionally leaves it
refutable. Making the condition explicit is what makes the parking disposition evaluable, which is what D-293
Decision 6 requires of a parking disposition. The guard travels with it unchanged: if leading body bytes carry
a `type`, that token must be **quoted** from `capabilityEnvelope.messageVocabulary`, never invented.

### Correction to the adopted round-2 text (defect 2)

Round 2 wrote: "`D1-plan/G21.md` §6 names 'inventing a vocabulary the record does not carry' as the
**second-ranked** recorded reviewer-rejection pattern for this gate." Re-measured, that is wrong on file, rank
and wording. The ranked list lives in **`DECISION-PACKETS/D1-plan/DR-122-SARIF.md`**, §Risk, verbatim: "The
reviewer-attack pattern on the two recorded corpus lineages was **(a) inventing a vocabulary or encoding the
record does not carry**, (b) collapsing two classes the occupancy keeps separate, (c) classifying a witness
under a closed identifier it does not belong to, (d) over-claiming closure." Vocabulary invention is **(a)**,
not second. And `D1-plan/G21.md` §6's own Risk paragraph ranks differently *for G21*: "(c) *Classifying a
witness under a closed identifier it does not belong to* **is the dominant risk here**: `g21-fixture-corpus.v3`
and `.v4` were REJECTED on `G21FXV3-M1` / `G21FXV4-M1` for filing a non-object-top-level RF-2 payload as a CC-5
member." **Corrected statement:** authoring a per-type body schema inside a fixture corpus is the **(a)** shape
in the recorded four-pattern list; for G21 specifically the recorded dominant risk is (c), and G21 is the gate
where that pattern is not hypothetical — it rejected four corpus versions.

### What changes if adopted

Nothing authored. Seven of the ten CC-5 entries stay named-open under two correctly named triggers, with the
truncated-body trigger now carrying its operative condition.

### Risk

*If adopted:* CC-5 remains the largest G21 block.
*If a schema were authored:* new protocol semantics minted inside a fixture corpus — pattern (a).
*If truncated bodies had stayed filed under the schema trigger:* a later schema successor would appear to
release a member whose actual blocker is still open.
*If the split were left unconditional:* it is refutable on OQ-G21-4's own grouping, and a later author could
read it as licence to deliver partial body bytes without quoting a vocabulary token.

### Confidence

**High** on the six-and-one split; **high** on the condition, which is what the record's own grouping requires.

---

## 6. G21-NT6 — author NT-6 at G21

### Recommendation — **confirm D-314 unchanged**

Rule `g21-leftover-join.v13` `$.doesNot[20]` **self-referential**: NT-6 is authorable as a delegated D1 act on
the G21 join, with its D9 token **quoted**, never invented. **Sequence that authoring after the owner's DR-133
Class A opening and before the later per-row cycle**, per the adopted B2 order. The act authors a DR-133
negative test at the G21 gate and does **not** SATISFY DR-133.

### Rationale

**The join measures NT-6 as remaining work in the same breath as disclaiming it.** Re-measured:
`g21-leftover-join.v13.json` `058717f5…` `$.doesNot` is a 44-entry array whose `[20]` is exactly
`"Does not author NT-6."`, while `$.obligations[3].remainingNotAuthored.dr133` = `["NT-6"]`. A join cannot
coherently measure an item as remaining work and forbid anyone from ever doing it.

**The counter-argument is real, recorded, and is why this is a ruling rather than an assumption.**
`OQ-G21-10`, verbatim: the parallel `$.doesNot[24]`/`$.doesNot[32]` entries ("Does not author per-D-002-platform
copies of the NT-1/NT-2 payloads" / "… of the two CC-5 payloads") "disclaim acts that `authoredImplementations`
records as *already done by other artifacts*, which supports the self-referential reading — but `$.doesNot[20]`
**lacks their qualifier and sits among substantive prohibitions**. Not resolved here." That sentence should be
named in the entry, not glossed.

**NT-6 is fully defined and constructible today.** `provider-only-output-contract.v3.json` `ef2a7416…`
`$.negativeTests["NT-6"]`, re-measured verbatim: `name` "d9-exit-hosttermination-refused"; `input` "A
constructible extra member or out-of-vocabulary frame carrying a D9 class, exit number, or HostTermination";
`pass` "Rejected before admission. No D9 minted from the component. Mapping remains DR-007 / v1.14 host-owned."
Its constructibility warrant is `$.negativeTests.wirePin`, re-measured: `path` `docs/coop/artifacts/delivery.v2.json`,
`sha256` `47b6cfd17338fafd407c554afe1951ab23d2896aac99bcfd272fc0894e3cabf3`, `note` "Classes are constructible
against these v2 bytes."

**The sequencing is the adopted programme's own order, not an inference.** `DECISIONS-RECOMMENDED.md` §B2,
re-measured: the agreed recommendation is "**Option 3 → Class A opening → Option 2's pre-SATISFIED-GRADE
sequencing**", with "NT-6 authoring treated as established work" among the pre-SATISFIED-GRADE bullets, and the
operative sentence "Choose Option 3, **then the Class A opening**, with Option 2's pre-SATISFIED-GRADE
sequencing. **Before the later per-row cycle** … author NT-6". NT-6 therefore sits inside the package placed
after the opening. Where the adopted programme states an order, a recommendation should not quietly reorder it.

**The no-minting guard.** The D9 token must be quoted from `d9-exit-contract.v1.14.json` `8dd33038…`, never
invented — `$.doesNot[3]`, "Does not invent a D9 code, exit number, or HostTermination"; `OQ-G21-13` records
that whether a *hostile-input* token the fixture asserts is refused counts as an invention "is not settled by
the record", and calls itself "the concrete byte-level form of OQ-G21-10". The authoring act must resolve that
in its own D-000 cycle.

**No ROW twin.** `DECISION-PACKETS/D1-plan/README.md`, re-measured: "G21, G24–G30, `OBL-HOSTILE-GOLDENS` and the
two DR-122 obligations have **no same-id ROW twin**." So closure runs through the G21 join alone.

### The counter-evidence the owner should have

The sequencing is a **programme-order** choice, not a lawfulness bar, and two measured facts show it. First,
NT-1 and NT-2 — DR-133 negative tests on this same join — were authored at `g21-fixture-corpus.v1` (D-241, dual
ACCEPT 0/0) and platform-copied at `g21-fixture-corpus.v2` (D-243, dual ACCEPT 0/0) with DR-133's Class A
opening unwritten then and unwritten now. Second, `OQ-G21-12` records that NT-6 has **no byte dependency** on
the opening: "NT-6 is fully defined at `provider-only-output-contract.v3.json#$.negativeTests["NT-6"]` and
constructible against the pinned `delivery.v2.json` wire. Section 4 records the standing as NOT BLOCKED on that
basis; the sequencing question is not resolved here." **So if the DR-133 opening stalls, the owner can lift the
sequencing with one sentence and no new rule.** That is not a hedge against the adoption; it is the fact that
makes the adoption cheap.

### What changes if adopted

After the DR-133 opening: one corpus plus a `g21-leftover-join` successor. Before it: nothing. DR-133 is
untouched by the authoring act — as D-301 and D-302 each recite verbatim, "Does not SATISFY DR-133. Does not
author NT-6."

### Risk

*If adopted:* NT-6 — the last unauthored DR-133 negative test on this join — inherits the DR-133 opening's queue
position, which G1-133 puts behind the shared gate-2 entry and a review cycle.
*If the self-referential ruling were declined:* NT-6 has no route at all, and B2's adopted "author NT-6" is left
without one.

### Confidence

**Medium** on the `$.doesNot[20]` ruling — the OQ-G21-10 counter-argument is genuine, recorded, and unresolved
in the bytes. **High** on the sequencing, which is the adopted text's own order.

---

## 7. Summary table

| id | Recommendation (≤20 words) | vs D-314 | Confidence |
|---|---|---|---|
| Q1 | Keep the `preview` refusal; retain OD-112-3 in `namedOpenDecisions` with DECIDED standing; do not widen scope | confirmed; one citation corrected | high |
| Q8 | Leave the numeric limb open; no cap values; later proposals need an evaluable D-006-pattern method | confirmed; OQ-G15-3 qualification added | high |
| G3-G18 | Leave blocked; no format, no fate-without-bytes; trigger is a reviewed implementation successor proving P-1..P-8 | confirmed; occupancy attribution corrected | high |
| G3-HOSTILE | Floor authored at D-300; seven classes incl. CC-6 stay named-open; remasurement already delegated | confirmed; class set re-enumerated from bytes | high |
| G21-SCHEMA | Six named-open on the schema trigger; truncated bodies on OQ-G21-4, conditional on zero body bytes | confirmed; condition made explicit, citation corrected | high |
| G21-NT6 | `$.doesNot[20]` self-referential; NT-6 authorable with quoted D9 token; sequenced after the DR-133 opening | confirmed unchanged | medium ruling / high sequencing |

---

## 8. What an adversarial reviewer should attack first

Named so the next round is spent on substance, not on discovery:

1. **The Q1 recount.** `$.offlineRunningPolicy.totalDecision` has eight entries; re-derive the refusal/continue
   split independently. If my recount is wrong, the corrected sentence is wrong, not the disposition.
2. **The G21-SCHEMA condition.** Is a zero-delivered-body truncated-body witness actually admissible as a CC-5
   member, or does `OQ-G21-4`'s "require a body" grouping foreclose it? If it forecloses it, part (ii) collapses
   back into part (i) and the split should be withdrawn — that would be a real change, not a citation fix.
3. **The G3-HOSTILE class enumeration.** I read `$.classCoverage` structurally rather than trusting
   `$.proposedLaterWork[2]`; the two agree at seven. Re-check both.
4. **The G3-G18 quarantine citation.** I moved the governing citation from `proposedLaterWork[2]` to D-311's
   Decision because `[2]` names journal/lock/lease and not the quarantine format. Verify that reading.
5. **Whether any of these corrections is load-bearing.** My position is that none is: all six dispositions stand
   on other bytes. If a correction *does* change an answer, say so — that is the case for replacing the D-314
   text rather than confirming it.

---

## 9. Scope statement

This file recommends. It records nothing. It does not edit file 08 or COORD, does not commit, does not SATISFY
DR-117, DR-131 or DR-133, does not open D-056 Class A, does not invent identifiers, numbers, lists or fixture
bytes, does not mint Rust-as-core, and makes no readiness claim. Every act it names still requires its own
D-000 cycle. If the owner adopts this round unchanged, D-314 stands as recorded for all six ids and no
superseding heading is needed; the corrections in §0 are to reasoning a later act would cite, and a later act
should cite them in this form.
