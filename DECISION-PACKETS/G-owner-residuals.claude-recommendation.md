# G — owner residuals: Claude round-1 recommendation

Round 1 under `DECISION-PACKETS/RECOMMENDATION-PROTOCOL.md`. Evidence: `DECISION-PACKETS/G-owner-residuals.md`
(evidence only; it carries no recommendation). Codex writes `G-owner-residuals.codex-recommendation.json`
independently and adversarially; no Codex file for this item existed when this was written and none was read.

**Nothing here is decided. The owner decides.** This file records no act, edits nothing under `docs/`, makes no
readiness claim, opens no D-056 Class A, and does not SATISFY DR-117, DR-131 or DR-133.

Measured at HEAD `a2d004066d2db7ae89de9ea56979bddb210f0786`, last COORD heading `## D-313`. Date from the clock:
2026-08-29.

| Pin | Path | sha256 (recomputed at this HEAD) |
|---|---|---|
| file 08 | `docs/v2/architecture/08-decision-and-readiness-register.md` | `e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e` |
| COORD | `docs/coop/COORDINATOR-DECISIONS.md` | `fcd95bf67af0ad076b1e3f9e7a784fcda5dbf4632001f844c70782c0a19f7b5c` |
| agreed recs | `DECISIONS-RECOMMENDED.md` | `42f27394746d4aac569a09a01da719c0cf318cf114086635e73097a6add97370` |
| needed §G | `DECISIONS-NEEDED.md` | `9685b1fc2b99096c1bcd584ff761b3da3c1f32dee71950efe24826431faeedf5` |
| C-plan | `DECISION-PACKETS/C-plan/README.md` | `3981ffdcc153b5182814cba25d450f1167b1dbfd574cdfcd6d2494e31c8cb43e` |
| D1-plan | `DECISION-PACKETS/D1-plan/README.md` | `a69a943a2181b90fbe9aeeb3f1c1112375dcbd77d0ebc67472f9971f1843b58f` |

Live readiness as measured in file 08 at this HEAD (recital, not a claim): required-now 28; Condition 2 is
**5 of 32**; Condition 5 `NOT MET`, "Not started; structurally last, and gated on 1, 2 and 4". No
`docs/v2/implementation/`.

---

## 0. Remasurement note — the packet's §0 table is incomplete, and three §3 ids have moved

The packet's §0 table lists D-295 and D-303..D-313. Seven headings between them are absent from it, and all
seven are **D1 fixture-authoring recordings** that bear directly on §3:

| Heading | Act (from COORD at this HEAD) |
|---|---|
| D-296 | `sarif-fc-nonauth-term-golden.v3` as DR-122 FC-NONAUTH-TERM fixture implementations |
| D-297 | `sarif-fc-outfail-golden.v3` `236fdb33…` as DR-122 FC-OUTFAIL **no-committed-run** fixture implementations |
| D-298 | `g20-fixture-corpus.v5` `3d7d8dba…` as DR-G20 fixture implementations |
| D-299 | `g19-fixture-corpus.v2` as DR-G19 fixture implementations |
| D-300 | `anti-lockstep-hostile-goldens.v3` `8be1b6c5…` as DR-127 fixture implementations |
| D-301 | `g21-fixture-corpus.v11` `13ede110…` as G21 CC-5 far-over prefix injection |
| D-302 | `g21-fixture-corpus.v14` `1012bb02…` as per-D-002-platform copies of that injection |

Three consequences, each measured from bytes at this HEAD:

1. **G3-HOSTILE is stale as posed.** The packet asks whether to "author the 16-witness floor now". It is
   already authored and recorded: D-300, dual ACCEPT 0/0, `anti-lockstep-hostile-goldens.v3.json`
   `$.whatIsAuthored` = "Sixteen catalog members. Sixteen UTF-8 .bin citation files … Five join units J-1..J-5
   and eleven class units CC-1..CC-11", `$.summary.authoredMembers` `16`,
   `$.leftoverDesignClosedIfAcceptedAndRecorded` `[]`. The live question is what to do about the per-class
   counts that kept the obligation open, not whether to author the floor.
2. **G3-SARIF-RUNID has been acted on in the record's own conduct.** D-297's Decision reads
   "leftover-design of OBL-FC-OUTFAIL-FX remains on leftover-join.v4 (D-182) because
   FC-OUTFAIL.committed-run-preserved **stays NOT-AUTHORED under the §7.1 RunId park**". The unparked sibling
   was authored; the parked case was left parked.
3. **G21-EXACT and G21-POST have recorded refusals against them.** D-301 and D-302 each carry "Does not pin
   N=65536 as prefix-only RF-2"; D-302 adds "Does not author prefix exactly at the operative bound" and "Does
   not author the postHandshake far-over half"; `g21-fixture-corpus.v11.json` `$.whatIsAuthored` ends
   "No exactly-at member."

A fourth item is stale in `DECISIONS-RECOMMENDED.md` §B2 rather than in the packet: B2 requires "the NT-4/NT-7
fixture standing at G20 byte-resolved before deciding what authoring is required there". D-298 recorded
`g20-fixture-corpus.v5`, whose `$.whatIsAuthored` includes "Two NT cells: closed CoverageV1 plus extra member
policyOutcome (NT-4) or planAdmission (NT-7)". That pre-cycle item is discharged; it is used below at G1-133.

Nothing in this note is a decision. It is a remeasurement, and every recommendation below is written against
the live bytes rather than against the packet's §0 framing.

---

## 1. The standard applied to every id

Three lawful outcomes exist per the packet's §0: a complete evaluable value now; a deferral disposition that
states it has no Condition-2 / D-056 effect without a separate reviewed act and a successor join; or leave
OPEN / named-open. The protocol permits "defer with an explicit disposition"; D-293 Decision 6 requires that
"any later parking disposition names a real trigger".

The test used below, uniformly: **a value is recommended only where the record already contains everything but
the owner's word.** Where a value would be the first appearance of that value in the record, the
recommendation is a named deferral with a trigger, because the alternative is minting — the shape the HANDOFF
and the recurring `does not mint Rust-as-core` guard (`## D-231`, `## D-232`, `## D-287`, four artifacts) exist
to prevent. Where the residual is *procedural* rather than *numeric* — an owner's word, an ordering, a
classification the record's own discriminants settle — the recommendation is to act now, because deferring
those costs the owner a blocker and buys nothing.

Twenty-one of the thirty ids below resolve to a deferral or a named-open with a trigger. That is not caution:
it is what the measurement returns. Nine resolve to act-now, and every one of those nine is procedural.

---

## 2. G1 — Class A opening entries

D-293 Decision 5, verbatim: "The D-056 Class A openings themselves are separate owner-controlled entries; this
entry opens none of them." The three recommendations below concern *when and how* the owner writes those
entries. None of them opens anything.

### G1-117 — DR-117 opening

**Recommendation.** Write the opening now, citing `preview-product-boundary-successor.v10.json`
`8f34c92ef4fb835ce31945bfc73e1442b38dada1d483380231a53d1d93a03483`; do **not** wait for the shared gate-2
entry; do not require a further successor beyond v10; and authorise G29/G30 fixture authoring to begin
immediately once the opening is recorded.

**Rationale.**

- *Steps 1 and 2 of the B3 programme are discharged on the record.* D-293 Decision 5 orders, for DR-117: the
  successor re-citing the twelve current joins and stating its relationship to
  `product-boundary-successor-contract.v8` `52c70f7715fb869bae70bc588043dc5b4d731b73408d2d451e868b8de963f362`
  (D-116); a fresh application-grade dual review bound to that successor's final digest; then the
  owner-controlled opening entry; then G29/G30; then a separate SATISFIED-GRADE + MF-6 cycle. D-295 recorded
  v10 at Stage A Claude ACCEPT 0/0 and Stage A Codex ACCEPT 0/0, and its Status block records for each
  reviewer "grade ruling SUSTAINED FOR APPLICATION", with its Decision adding "Both Stage A reviews answered
  the grade question (D-005 form)". The packet's §0 records the same at D-295. That is the application-grade
  dual review bound to v10's digest.
- *The record itself names the opening as the next step and names its venue.* D-295's Decision, verbatim:
  "Gate 1 Class A remains false under D-137's express reservation; preview-product-boundary-successor.v10 does
  not withdraw that reservation, and this entry does not lift it. **Venue for the lift is the owner-controlled
  opening entry D-293 Decision 5 reserves, which follows this recording.**"
- *The shared gate-2 entry is not a predecessor of DR-117's opening.* D-293 Decision 5's ordered list for
  DR-117 does not contain it. `DECISIONS-RECOMMENDED.md` §B3 mentions it only as a separate sentence — "The
  shared gate-2 entry carries a distinct DR-117 finding" — which is a content requirement on that entry when
  it happens, not an ordering. And DR-117 does not need it: D-295 records "D-056 Eligibility gates 2 and 3
  **continue to hold** for DR-117 (D-159)". Gate 1 is the only false gate on this row, and gate 1 is the
  owner's. This is the point on which G1-117 differs from G1-131 and G1-133 below.
- *v10 is the artifact to cite.* D-295 records v8 as "a historical measurement as of HEAD `df1301a`" and v9 as
  "REJECTED at Stage A by both reviewers and is unrecorded; its findings landed at
  preview-product-boundary-successor.v10". No recorded defect stands against v10. Requiring a further
  successor would re-run D-295's three-turn cost against nothing.
- *G29/G30 may start immediately.* D-293 Decision 5 orders G29/G30 after the opening. `D1-plan/README.md`
  Tier 3 records both as "blocked on sequencing only", sharing
  `product-boundary-successor-contract.v8.json` `52c70f77…`, which is pinned and present.

**Minimum sentences the opening should contain** (proposed content, not recorded text):

1. The owner's word lifting D-137's express reservation, naming D-137 and stating that the lift is the owner's
   act at the venue D-295 names.
2. The artifact cited by digest — `preview-product-boundary-successor.v10.json` `8f34c92e…` — and a restatement
   of its relationship to `product-boundary-successor-contract.v8` `52c70f77…` (D-116), which `DECISIONS-RECOMMENDED.md`
   §B3 requires of both the successor and the opening.
3. That it opens D-056 Class A gate 1 for DR-117 and **does not SATISFY DR-117**; SATISFIED-GRADE + MF-6 is a
   separate later cycle.
4. That gates 2 and 3 continue to hold per D-159 as D-295 measured, and that gates 4 and 5 are not performed.
5. Its readiness recital in the form every entry D-296..D-313 uses (required-now 28; Condition 2 unchanged at
   this entry) and whether it edits file 08 — the recommendation is that it does not, with the register echo
   owed at a later MF-6 (see Q6 and Q9 for the recorded mechanism).
6. That it unblocks G29/G30 fixture authoring under D-293 Decision 5's order.

**Caveat the owner should decide explicitly.** This recommendation reads B3 step 2 ("a fresh application-grade
dual review bound to that successor's digest") as discharged by D-295's two Stage A ACCEPTs, because both were
bound to the frozen v10 digest and both answered the grade question in D-005 form. If the owner reads step 2
as requiring a review cycle *separate from* the recording's Stage A, then that cycle runs first and everything
else in this recommendation is unchanged. This is the one limb of G1-117 on which the record admits two
readings.

**What changes if adopted.** One new COORD heading (the owner's Class A opening entry). No file-08 edit at the
opening. `g29-leftover-join.v4` and `g30-leftover-join.v4` become authorable against their pinned occupancies.
No Condition-2 movement at the opening itself — SATISFIED-GRADE is a later separate cycle, and the HANDOFF's
"do not SATISFY DR-117" continues to bind until the owner says otherwise.

**Risk.** If adopted: the opening is an owner-controlled Class A act, and if the later shared gate-2 entry
reaches a different common interpretation of D-056 gate 2, the DR-117 finding may need restating — exposure is
small because D-295 already measured gates 2 and 3 as holding under D-159. If deferred: seventeen G29/G30
fixture cases (D1-plan: G30 7, G29 10) stay blocked on an owner sentence, and the D-295 grade rulings age
against a HEAD that keeps moving.

**Confidence: high.**

### G1-131 — DR-131 opening

**Recommendation.** Keep B1's order exactly: (1) the shared gate-2 entry first, (2) then the fresh
application-grade dual review of `preview-analyze-contract.v2.json`
`081ff7fb529b34a3db3ac9f4c7505848e2253be12b5a867d39b49b3a26d56970`, (3) then the T2-02 opening. Do **not**
author a contract successor before the opening; author one only if the fresh review returns MUST-FIX findings,
in which case the review re-binds to the successor's digest and the opening cites that.

**Rationale.**

- *The order is the adopted one.* `DECISIONS-RECOMMENDED.md` §B1 round 2, items 1–4, adopted at D-293 Decision
  5, numbers the shared gate-2 entry first and the opening third. Codex's round-2 AGREE restates the same
  order.
- *Unlike DR-117, DR-131 needs the gate-2 entry first.* No COORD heading records DR-131's gate 2 as holding;
  the packet §1 records the open reconciliation work the shared entry must do (D-154 against the current gate
  joins' FX-AUTHORING flags, without describing D-249..D-253 as silently overturning D-154). Writing the
  opening before that entry would have the opening rely on a gate-2 reading that no reviewed act carries. The
  asymmetry with G1-117 is byte-grounded, not stylistic: D-295 says gates 2 and 3 "continue to hold" for
  DR-117; nothing says that for DR-131.
- *No successor is required before the opening.* B1 names v2 "unless a successor is authored" — a conditional,
  not a requirement — and file 08 line 313 records v2 `081ff7fb…` as the accepted design-contract candidate
  (D-138), `CANDIDATE-NOT-APPLIED`, "binds NOTHING". No recorded defect stands against v2. Authoring a
  successor pre-emptively would bind the fresh review to bytes chosen before the review that would justify
  them.
- *Nothing on this path has moved since D-293.* COORD headings D-294..D-313 contain no shared gate-2 entry, no
  `preview-analyze-contract` review, and no DR-131 opening.

**Minimum sentences the opening should contain** (proposed content, not recorded text):

1. The owner's product word opening D-056 Class A gate 1 for DR-131.
2. The exact contract bytes cited by digest, and what the opening does — and does not do — to file 08 line
   313's two recitals, `CANDIDATE-NOT-APPLIED` / "binds NOTHING" and "Not eligible in kind today (D-133)". The
   opening must say which of those it changes; leaving either unaddressed is the defect a reviewer will find.
3. The two fresh application-grade verdicts, cited by digest.
4. The gate-2 finding it relies on, by reference to the shared entry's **distinct DR-131 finding** (B1 item 1,
   and Codex's round-2 "separately evidenced findings").
5. That it **does not SATISFY DR-131**; SATISFIED-GRADE + MF-6 is a later separate cycle, with G24–G28 fixture
   authoring between them as conservative sequencing (B1 item 4's exact characterisation — "not as a
   precedent-proven automatic reopening of gate 2").
6. Its readiness recital and whether it edits file 08 (recommendation: it does not; echo at MF-6).

**What changes if adopted.** Two COORD headings before the opening (the shared gate-2 entry, then the review
cycle), then the opening. `DECISION-PACKETS/D1-plan/` Tier 2 — G25 (2 payloads), G26 (3), G27 (3), G24 (4),
G28 (4) — becomes recordable after the opening. No file-08 edit. No Condition-2 movement at the opening.

**Risk.** If adopted: the shared gate-2 entry is the most expensive single act in the G1 set, because it must
state a common D-056 gate-2 interpretation and declare whether it interprets D-056 or is a scoped successor
amendment (B1 item 1) — that is a rule act with D-000 clause 5 overturn cost. If deferred: sixteen G24–G28
fixture cases stay blocked, and DR-131 stays a hard blocker at file 08 line 313.

**Confidence: high** on the sequencing and the no-successor limb; the minimum-sentence list is a proposal.

### G1-133 — DR-133 opening

**Recommendation.** Same shape as G1-131 — shared gate-2 entry, then the fresh application-grade review, then
the opening — with the review dispatched against `provider-only-output-contract.v3.json`
`ef2a7416700cc8197486c6e29450673c60e3b94512be3ad278d1995f7d281309` and a v4 authored only if that review
returns MUST-FIX findings. **NT-6 authoring is not content of the opening**; it is a separate D1 act, and the
`$.doesNot[20]` tension is resolved by the separate one-sentence ruling recommended at **G21-NT6**, not inside
the opening.

**Rationale.**

- *The order and the review target are the adopted ones.* `DECISIONS-RECOMMENDED.md` §B2 round 2: Option 3 →
  Class A opening → Option 2's pre-SATISFIED sequencing, with "the fresh application-grade dual review
  targeting whichever artifact the opening entry cites (v3 `ef2a7416…`, or a v4 successor if the three
  advisories are landed)". Landing the advisories is offered as a condition, not required; dispatching against
  v3 and re-binding on MUST-FIX is the reading that keeps the review bound to final bytes without pre-judging
  it. File 08 line 314 records v3 `ef2a7416…` as `CANDIDATE-NOT-APPLIED`, "binds NOTHING".
- *One of B2's four pre-cycle items is now discharged.* B2 requires "the NT-4/NT-7 fixture standing at G20
  byte-resolved before deciding what authoring is required there". D-298 recorded `g20-fixture-corpus.v5`
  `3d7d8dba…`, whose `$.whatIsAuthored` includes "Two NT cells: closed CoverageV1 plus extra member
  policyOutcome (NT-4) or planAdmission (NT-7)". The other three items stand: the file-01 preview-role delta
  disposition (or removal of reliance), NT-6 authoring, and the D-147 reconciliation in the shared gate-2
  entry.
- *NT-6 does not belong in the opening.* An opening is a D-056 gate-1 record. Every fixture authoring in this
  record is its own (corpus, join-successor) act — D-241, D-243, D-245, D-247, and now D-296..D-302 — and
  `g21-leftover-join.v13.json` `058717f5…` `$.obligations[3].remainingNotAuthored.dr133` = `["NT-6"]` measures
  NT-6 as remaining fixture work on the G21 join, not as opening content. Putting it in the opening would mix
  a gate act with an authoring act and would inherit the `$.doesNot[20]` tension into a Class A entry.
- *The file-01 delta is the item to watch.* B2 requires "a separate reviewed disposition of the candidate's
  proposed file-01 preview-role delta … or removal of reliance on that delta, **before the SATISFIED-GRADE
  cycle**" — before that cycle, not before the opening. So it does not gate the opening, and the opening
  should say so rather than leave it ambiguous.

**Minimum sentences the opening should contain.** As G1-131 items 1–6, substituting DR-133, v3's digest, the
distinct DR-133 gate-2 finding reconciling D-147 with the current G20/G21 joins (B2, "rather than any 'silent
supersession' language"), plus one sentence stating that the file-01 preview-role delta disposition and NT-6
authoring are later separate acts that the opening does not perform.

**What changes if adopted.** The shared gate-2 entry is shared with G1-131 and G1-117, so it is one act, not
three. Then a review cycle and the opening. NT-6 becomes authorable as a delegated D1 act on the G21 join
subject to G21-NT6. No file-08 edit; no Condition-2 movement at the opening.

**Risk.** If adopted: the DR-133 opening depends on the same shared gate-2 entry as DR-131, so a defect there
delays both. If deferred: DR-133 stays a hard blocker at file 08 line 314, and NT-6 — the last unauthored
DR-133 negative test on the G21 join — stays parked behind an ambiguity that costs one sentence to resolve.

**Confidence: medium.** The sequencing is high-confidence; the NT-6 placement depends on G21-NT6, which is
itself medium.

---

## 3. G2 — C-plan Q0–Q16

### Q0 — Does D-293 reach the round-2 recommendation files, or only the round-3 text?

**Recommendation.** **Yes — it reaches them**, bounded: D-293 adopts the round-2 content that the adopted
round-3 text and D-293's own Decision incorporate by name, at the pinned digest
`44f51a5d36eb3f03c711112a50119ea67fb01b3a07d255ccbac5d51cc0485627` for C1–C4. It is not a general adoption of
everything in `DECISION-PACKETS/`.

**Rationale.**

- *The round-3 text is self-referentially incomplete without round 2.* `DECISIONS-RECOMMENDED.md` §C1–C4
  carries only round 3, which reads "All three amendments adopted **on top of round 2**" and "- **C2, C3:**
  unchanged from round 2." Those two sentences have no content unless round 2 is reached.
- *D-293's own words already reach past the round-3 text.* D-293 Decision 6, verbatim: "C2 and C3 as agreed
  (**the C2 matrix/corpus, threshold-approval and G13 sequence**; the C3 live-file-08 remasurement with
  coherent evaluable windows)." That C2 content appears nowhere in §C1–C4's round-3 text. D-293 therefore
  demonstrably recites round-2 content, which settles the question on D-293's own bytes rather than on an
  inference about its Subject pointer.
- *The bounding matters.* §B1, §B2, §B3 and §C5–C9 carry their round-2 text in full inside
  `DECISIONS-RECOMMENDED.md`; the only gap is §C1–C4's round-2 file. Reading Q0 broadly ("every packet file is
  adopted") would sweep in evidence packets that were never recommendations, so the answer should name the one
  file and the digest.

**What changes if adopted.** No artifact edit. One sentence in the owner's answer fixes C2's, C3's and C4's
content. It makes the round-2 C4 owner assignment operative (see **Q4**), makes the round-2 C9 authorities
operative (see **Q15**), and makes round-2's "no isolated unit choice" rule operative (see **Q3**).

**Risk.** If adopted: a later act could over-read it into a general adoption; the bounding sentence is what
prevents that, so it must be in the answer, not implied. If deferred: Q4 has no adopted owner, Q15's "named
authorities" has no referent, and C4-b — the first of three sequenced C4 acts — cannot start.

**Confidence: high.**

### Q1 — OD-112-3 wording after D-309

**Recommendation.** Two limbs. (a) Drop the `preview` stage qualifier: the standing is fail-closed `refuse`
without it. (b) OD-112-3 **stays** in `namedOpenDecisions` with a DECIDED standing rather than leaving the
array.

**Rationale.**

- *The record expressly leaves both limbs unchosen, so this is squarely the owner's.* The D-309 carry,
  `signed-index-trust-contract.v14.json` `039a5702…`, `$.namedOpenDecisions[2].standing`, verbatim: "D-293:
  OD-112-3 is the final fail-closed policy. Residual axis, named not chosen: whether the
  signed-index-trust-contract.v8 standing token Preview refuse remains, where preview is the product-stage
  scope term of this artifact (roles[].preview, A preview payload), or the standing is fail-closed refuse
  without that stage qualifier; and whether OD-112-3 remains in namedOpenDecisions or leaves it." The same
  residual is restated at `$.offlineRunningPolicy.totalDecision[4].alreadyRunning`.
- *For (a): the qualifier was doing provisionality work that "final" removes.* The superseded v8 sentence was
  `"refuse unless OD-112-3 is later numbered; preview refuse"` — the stage qualifier scoped a refusal that was
  awaiting a number. D-293's word is "OD-112-3 is the **final** fail-closed policy". Keeping a product-stage
  qualifier on a policy declared final would leave the post-preview stage unstated, which reintroduces exactly
  the open axis the word "final" closes.
- *For (b): the record's practice is to change a standing, not to delete an entry.* The nearest recorded
  analogue is `OBL-OD-2`, which left the leftoverDesign partition at D-304 by a changed flag and a changed
  bucket while remaining a named obligation on `component-manifest-leftover-join.v15.json` `f27ffac2…`.
  Removing OD-112-3 from the array would leave the contract with no site carrying its DECIDED standing — D-293
  is COORD, not the contract — and would make the array a record of *undecided* items only, which none of its
  four entries' wording supports.

**The alternative the owner should weigh on (a).** Dropping `preview` widens the refusal beyond the preview
product stage. That is a substantive scope extension. If the owner does not intend it, the lawful alternative
is to keep the qualifier and record that the policy is final *within* the preview stage, with the
post-preview stage named open and a trigger. Either is lawful; (a) is recommended because "final" reads
against a stage-scoped standing.

**What changes if adopted.** A `signed-index-trust-contract` successor and its paired signed-index
leftover-join successor recording the chosen wording, through the normal Stage A + Stage B cycle. No file-08
edit. DR-112 stays `OPEN` (file 08 line 294); no Condition-2 movement — D-293 Decision 6's "no Condition-2 or
D-056 eligibility effect without a separate reviewed act and a successor join" continues to govern.

**Risk.** If adopted: this lineage's recent REJECTs were custody and self-description defects (C-plan §2 names
the pattern), so the successor's own self-description is the hazard, not the wording choice. If deferred: the
live contract carries a self-described unchosen axis in a security row, and any reviewer reading it will find
it.

**Confidence: medium.** Limb (b) is well supported; limb (a) is a scope call the record expressly declines to
make, and the alternative is stated for that reason.

### Q2 — OD-112-1, OD-112-2, OD-112-4 values

**Recommendation.** **(c) Leave RESERVED.** Supply no values, and record no parking disposition at this time.

**Rationale.**

- *There is nothing to confirm and everything to mint.* `signed-index-trust-contract.v14.json`
  `$.namedOpenDecisions[0].standing` and `[1].standing` both read "RESERVED. Named. Not minted."; `[3].standing`
  reads "RESERVED to product/release. Named as an expiry-bearing waiver, not a number." The C1–C4 packet §1.4
  measured "**None in the record.**"
- *The three quantities are the kind D-006 says cannot be derived.* A quorum/threshold cardinality without a
  named root-key population, or a clock-skew floor without a named clock source, would repeat the defect the
  record already names: `control-protocol-contract.v2.json` `c50a79fe…`
  `$.transportAndFraming.framing.bounds.constantsStatus`, verbatim — "a numeric threshold without a named
  runner/workload measures nothing (the D-006 lesson recorded in D-007's alternatives)."
- *A parking entry would cost an act and buy the standing the bytes already carry.* D-293 Decision 6 already
  states that any later parking "has no Condition-2 or D-056 eligibility effect without a separate reviewed
  act and a successor join". The authority limbs need no act either: C-plan §1 records that file 08 line 294
  already reads `Security + operations` for OD-112-1/2, and that `$.namedOpenDecisions[3].standing` and
  `$.auditAndWaiver.waiverExpiry` already route OD-112-4 and its duration to product/release.

**What changes if adopted.** Nothing. No artifact, no COORD heading, no file-08 edit. DR-112 stays `OPEN`;
Condition 2 unchanged.

**Risk.** If adopted: three of C1's five limbs stay open indefinitely and DR-112 cannot move. If values were
supplied instead: a minted quorum cardinality is a substantive security decision taken without the named
authority's input, and it is precisely the invention the HANDOFF forbids.

**Confidence: high.**

### Q3 — DR-111 windows (C3(ii))

**Recommendation.** **(c) Leave RESERVED as one coherent set.** Do not set the unit alone, and do not set a
subset of the four reserved surfaces.

**Rationale.**

- *The adopted text forbids a partial setting.* Reached through **Q0**: "if the values are not in hand, that
  is choice (b) or (c) above, **not a partial setting**" (C-plan §3 Q3, quoting the adopted round-2 text).
- *The live contract reserves the numbers to the very authority being asked.*
  `compatibility-matrices-contract.v5.json` `d0386cee…` `$.numericWindows`, verbatim: "RESERVED. This artifact
  does not mint how long a reader is supported. Product/versioning sets numbers later. Alias-window numbers
  are D-012's, not this row's." File 08 line 293 names the DR-111 owner as `Versioning authority`.
- *The unit itself is not in the record.* C1–C4 packet §3.5: "Unit of a 'window' (majors? releases? days?) is
  **not in the record**." Choosing the unit alone would bind all four reserved surfaces to a unit before it is
  known whether they share one window — the packet's own second sub-question.
- *The unblocked limb is already done.* C3-a, the live-file-08 remasurement, was recorded at D-303; only
  owner content remains.

**What changes if adopted.** Nothing recorded. No `compatibility-matrices-contract.v6` /
`compatibility-leftover-join.v4` pair. DR-111 stays `OPEN`.

**Risk.** If adopted: DR-111 stays a hard blocker, and two downstream items stay parked on it — the C6 lock
limb (C-plan §1, C6 row: "the lock limb additionally waits on **C3(ii)**") and G18's `conflicting-project-locks`
class, where `component-manifest-schemas.v11.json` `1c0b8868…` `$.lockSchema.purpose` reads "NO lock is
producible until DR-111 closes" (see **G3-G18**). If a unit were set alone: the adopted text forbids it and a
reviewer would reject on that sentence.

**Confidence: high.**

### Q4 — DR-126 population-packet owner (C4-b)

**Recommendation.** Assign the population packet to file 08's own DR-126 owner cell — **`Security + release +
platform owners`** (line 308) — which is the round-2 C4 assignment.

**Rationale.**

- *It invents no authority.* The cell already names that authority for DR-126; the assignment states that the
  packet belongs to the row's own owner rather than to a new body.
- *The three "separate decision" sentences say the decision is separate, not that it must land elsewhere.*
  `platform-tcb-contract.v45.json` `da87bdb4…` `$.platformProfile.populationPacket`: "A later packet that
  supplies these selectors is a different artifact. … **Choosing its owner is a separate decision.** Windows
  remains D-002 absent."; the same sentence at `harness.DR-G22.platform-abi-loader.v2` `$.filesystems.laterAct`;
  and `platform-tcb-leftover-join.v9` `$.proposedLaterWork[2]` "… and does not choose that packet's owner."
  This answer *is* that separate decision.
- *Q0 supplies the adoption route.* With Q0 answered yes, the round-2 C4 assignment to that cell is adopted
  content rather than a fresh proposal. If Q0 is answered no, the recommendation is unchanged, because that
  cell is the only authority the register names for DR-126.

**What changes if adopted.** C4-b becomes runnable — a COORD-only act, optionally with
`platform-tcb-leftover-join.v10` (C-plan §1, C4 row). That unblocks C4-c (an application-grade TCB successor
making the grammar governing), which in turn precedes C4-d (which additionally needs **Q5**). G22 remains
reserved: D-293 Decision 8 says "G22 stays reserved until C4 resolves", and C4 is not resolved until C4-d.

**Risk.** If adopted: none material; it is the row's own owner cell. If deferred: three sequenced C4 acts stay
blocked, G22's reservation has no release condition it can reach, and DR-126 stays a "Hard blocker for
platform qualification" (file 08 line 308).

**Confidence: high.**

### Q5 — DR-126 selectors and per-OS tables (C4-d)

**Recommendation.** **(c) Leave RESERVED** until after C4-c — the application-grade TCB successor that makes
the grammar governing.

**Rationale.**

- *Nothing is in the record to confirm.* C1–C4 packet §4.4: "**None in the record** for any per-OS table row,
  filesystem selector value, or version/build selector value."
- *D-293's own order puts population last.* Decision 6, verbatim: "owner assignment, then an application-grade
  TCB successor that makes the grammar governing, then complete profile population." Populating before the
  grammar is governing runs the adopted order backwards.
- *The grammar constrains what a value may be, so values written first may be rejected by it.*
  `platform-tcb-contract.v45.json` `$.platformProfile.slice1ProfileStems[0].filesystemWhereItAffectsResolution.mustNot`,
  verbatim: "apfs-or-hfs-plus as a single value". And the same contract is `CANDIDATE-NOT-APPLIED` binding
  `NOTHING` (C-plan §1), so values authored against it today would be authored against a grammar that binds
  nothing.
- *Profiles must be complete.* The packet §2 Q5 records "Complete profiles, not four isolated selectors" —
  the same defect Q3 identifies as a partial setting.

**What changes if adopted.** Nothing now; C4-d stays queued behind C4-b and C4-c.

**Risk.** If adopted: DR-126 stays a hard blocker and G22 stays reserved. If values were set now: they would be
the first per-OS table rows in the record, authored against a non-governing grammar, in a row whose subject is
the platform TCB.

**Confidence: high.**

### Q6 — C5/C6 file-08 echo

**Recommendation.** **COORD-only stands.** The register echo rides a later MF-6, and the owner records that
disposition explicitly, including the sentence that the echo has no eligibility effect by itself.

**Rationale.**

- *D-293 and both acts already say so.* D-293's Decision closes "It does not edit file 08." D-310 and D-311
  each carry "Does not edit file 08", and D-310's Decision names the question rather than answering it,
  verbatim: "Q6 is named, not answered: whether this classification is echoed in file 08, as DR-G05's
  caps-deferred cell and DR-130's in-row disposition were, or lives only in COORD. D-293 closes with It does
  not edit file 08; this act does not edit file 08."
- *The two precedents are register-cell edits, i.e. MF-6-class acts.* DR-G05's "caps deferred by explicit
  disposition (D-006)" and DR-130's in-row disposition both write cells. The whole D-170..D-313 branch is a
  no-cell-edit branch (each entry recites it), so an echo cannot ride an ordinary recording act.
- *The record already carries the mechanism for an owed echo.*
  `component-manifest-leftover-join.v15.json` `f27ffac2…` records, for both `OBL-OD-1` and `OBL-OD-2`,
  "registerEchoAtApplication remains owed at a later MF-6". Applying the same form to the C5/C6 classifications
  keeps them visible and costs no act now.
- *The disposition must state its own limits.* D-293 Decision 7 requires "an express scope/eligibility
  successor and a successor-join remeasurement" before any concrete encoding becomes post-Condition-5 work,
  and D-310 records that "The classification has no Condition-2 or D-056 eligibility effect without" them. The
  echo changes none of that and should say so.

**What changes if adopted.** No act now. One sentence in the owner's answer, and two lines in whichever MF-6
next touches DR-121 and DR-107. No Condition-2 movement.

**Risk.** If adopted: the classifications live only in COORD until an MF-6 lands, so a reader of file 08 alone
does not see them — the exact gap the two precedents closed. If a file-08 edit were made now: it would
contradict D-293's closing sentence and would be a cell edit outside the branch D-170..D-313 runs on.

**Confidence: high.**

### Q7 — Can implementation-scope `leftoverDesign: true` ever satisfy D-056 gate 2?

**Recommendation.** **Rule no**, narrowly: a scope classification alone never satisfies D-056 gate 2 while the
obligation is measured `leftoverDesign: true`. The route to gate 2 is the flip of the measured flag on a
successor join, not a scope label. Record the ruling rather than leaving it open.

**Rationale.**

- *D-056 has no sub-row deferral limb.* C5–C9 packet, open question 1, verbatim: "No COORD entry or artifact
  rules on a sub-row deferral; the only deferral limb D-056 names is the D-002/D-010 row-level limb." Reading
  one in would be a D-056 amendment, and D-293's Decision closes "It does not amend D-000 or D-056."
- *The record has run both experiments, and they separate cleanly.* D-310 and D-311 classified the six CI
  `reservedForBlueprint` members and the seven reserved lifecycle mechanisms as implementation encodings and
  each expressly left `leftoverDesign` **true** — D-310: "leftover-design of OBL-CI-ENCODING-RESERVED remains
  true on monorepo leftover-join.v4: existingGate none, executionObligationOwnerToday none, rideStanding
  not-capable-of-riding." By contrast `OBL-OD-2` *did* leave the partition, at D-304, by a **changed flag**:
  `component-manifest-leftover-join.v15.json` `f27ffac2…` records `OBL-OD-2` with `leftoverDesign: false`,
  `rideStanding: "specified-not-leftover"`, and its own reason calls it "the first recorded leftoverDesign flip
  of a RESERVED/UNDECIDED-value obligation". Classification did not move the flag; disposition did. That is the
  answer, already demonstrated twice.
- *D-293 answered the half it could.* "no eligibility effect without a separate reviewed act and a successor
  join" — the recommendation adds only that a scope label is not that act.

**What the ruling does not decide.** It does not decide whether a future express scope/eligibility successor
could succeed. It decides that a scope label alone never does. That narrowness is deliberate: the broader
ruling is not supported by the bytes.

**What changes if adopted.** One RULE-GOVERNED COORD entry, no file-08 edit. It makes the residual path for
DR-121 and DR-107 explicit — each needs the express scope/eligibility successor and successor-join
remeasurement D-293 Decision 7 already requires. No Condition-2 movement.

**Risk.** If adopted: D-000 clause 5 overturn cost attaches, and it forecloses a cheaper path a later act might
have wanted. If deferred: D-310 and D-311 each carry the question unanswered in their own Decision text, and
every later encoding act inherits it — the question does not get cheaper by waiting.

**Confidence: medium.** The bytes support the reading strongly but no artifact states it; this is a rule the
owner is being asked to make.

### Q8 — OD-1 four cap values, and what "measured caps" measures

**Recommendation.** **Leave the numeric limb open, explicitly** — the fallback the adopted C7 text already
carries. Supply no numbers. State, for any later act, that a cap is settable only with a named measuring gate,
a named corpus, and a named runner class.

**Rationale.**

- *The absence is a recorded decision, not a gap to fill in.* `component-manifest-schemas.v11.json`
  `1c0b8868…` `$.namedOpenDecisions[0].standing`, verbatim: "NO caps are stated in these schemas, and that
  absence is a NAMED OPEN DECISION, not a default."; the same object's `candidateOwners`: "… a cap is a product
  threshold …"; `## D-006` Decision type: "Numbers are not derivable from any rule."
- *There is nothing to measure with.* `component-manifest-leftover-join.v15.json` `f27ffac2…` `OBL-OD-1`:
  `existingGate` `"none"`, and its reason "existingGate stays none; **no gate measures these four
  quantities**". A cap "measured" against no gate and no corpus would repeat the defect
  `control-protocol-contract.v2.json` names — a threshold without a named runner measures nothing.
- *The adopted text supplies this exact fallback.* `DECISIONS-RECOMMENDED.md` §C5–C9, C7 bullet: "if values
  are not available, leave the numeric limb open and say so."
- *The cost of deferring is bounded, and that is worth telling the owner.* C7's precondition bites only on
  "oversized-input fixtures", and G15's coverage set contains none: `D1-plan/G15.md` §4(d) measures that
  `schemas.v11` `$.testCorpusRequirements.classes[3].requires` names no over-length member and that the token
  `oversized` appears in none of the five G15 governing files. So deferring the caps blocks no
  currently-planned fixture act.

**What changes if adopted.** Nothing recorded; optionally one sentence so later acts can cite the fallback.
`OBL-OD-1` stays `leftoverDesign: true`; DR-103 stays `OPEN`; Condition 2 unchanged.

**Risk.** If adopted: the surface file 08 line 285 describes — "an unbounded-input surface at metadata-only
admission; oversized-input refusal UNSPECIFIED, not implied" — stays unbounded in the design. That is a real
residual and the owner should see it stated plainly. If numbers were supplied: they would be minted, not
measured, against no gate and no corpus, and `schemas.v11` `$.namedOpenDecisions[0].consequence` already warns
"a fixture author must not assume it".

**Confidence: high.**

### Q9 — OD-1 on the already-`SATISFIED` DR-115 row: MF-6 note or successor citation?

**Recommendation.** **Both, in the order the record has already taken them**: the successor citation is done
(D-312), and the register echo rides a later MF-6 **on the DR-103 row**, not on DR-115. Do not put an MF-6 note
on the DR-115 row and do not change DR-115's `SATISFIED` label.

**Rationale.**

- *The stale cell is DR-103's, not DR-115's.* File 08 line 285 reads that OD-1 "remains OPEN with its owner
  UNASSIGNED between DR-115 and DR-120, and choosing that owner is a separate decision", and
  `component-manifest-leftover-join.v15.json` `f27ffac2…` `OBL-OD-1` says exactly that: "registerEchoAtApplication
  remains owed at a later MF-6: the live DR-103 row still reads that OD-1 remains OPEN with its owner
  UNASSIGNED between DR-115 and DR-120, and this join does not edit file 08."
- *The successor mechanism was already used, without a label change.* D-312 assigned the owner by successor
  join — the D-102 shape the C5–C9 packet's open question 2 names — and file 08 was untouched.
- *The D-089 precedent is about a status label, which this is not.* D-312 assigned OD-1 to DR-115's *authority*
  (an owner-cell reference); it added no DR-115 acceptance-evidence element. Opening a `SATISFIED` row for a
  change that is not one of its acceptance-evidence elements is a heavier act than the record needs.
- *One MF-6 covers both echoes.* `OBL-OD-2`'s reason on the same join: "registerEchoAtApplication remains owed
  at a later MF-6: the live DR-103 row must name OD-2 alongside OD-1." C-plan §1 records the same limb as
  already anticipated at `component-manifest-leftover-join.v9` `$.proposedLaterWork[0]`.

**What changes if adopted.** No act now. One later MF-6 on the DR-103 row carrying both echoes: OD-1's owner
and OD-2's naming. No Condition-2 movement — D-312 already recorded the assignment; the echo is bookkeeping.

**Risk.** If adopted: file 08's DR-103 row stays stale on the owner sentence until that MF-6 lands, and file 08
is the register a reader trusts. If an MF-6 were put on DR-115 instead: a `SATISFIED` row is reopened for a
change that does not belong to it.

**Confidence: high.**

### Q10 — `OBL-OD-2` summary bucket

**Recommendation.** **Confirm D-304's `specifiedNotLeftover`.** Do not overturn to `dischargedOrDeferred`.

**Rationale.**

- *That is the live bucket and it is current at this HEAD.* `component-manifest-leftover-join.v15.json`
  `f27ffac2…` `$.summary.specifiedNotLeftover` = `["OBL-SCHEMA","OBL-FIXTURE-51","OBL-V2-A1",
  "OBL-G15-HARNESS-SPEC","OBL-WINDOWS-PATH-NAMED","OBL-OD-2"]`.
- *The join states the discriminant itself, and it selects `specifiedNotLeftover`.* `OBL-OD-2`'s reason,
  verbatim in part: "summary bucket is specifiedNotLeftover: the class-specific DR-111 statements already
  specify the rule, matching OBL-SCHEMA, rather than discharging the obligation to another row
  (dischargedOrDeferred holds OBL-SIG-CEREMONY and OBL-LOCK) and rather than leaving a named-gate execution
  remainder (OBL-G15-HARNESS-SPEC)." OD-2 is not discharged to another row — `existingGate` is "none.
  Specified by D-293 Decision 7 as final do-not-fold." and `executionObligationOwnerToday` is "none on this
  row" — so the record's own three-way test lands on `specifiedNotLeftover`.
- *Overturning costs an act in a defect-prone lineage for a relabel with no readiness effect.*
  `component-manifest-leftover-join` v7 and v8 were both burned on custody/self-description defects (C-plan
  §2).

**What changes if adopted.** Nothing. One confirming sentence.

**Risk.** If adopted: the C-plan's noted "closer reading" is set aside; if a later act needs
`dischargedOrDeferred` semantics it needs a successor. If overturned: a successor act with no readiness effect
in the lineage that has already lost two versions to wording defects.

**Confidence: high.**

### Q11 — OD-101-1 language and candidate set

**Recommendation.** **(ii) A dedicated D-000 successor that first publishes the candidate set and then
chooses** — not a direct owner statement now, and not indefinite RESERVED. **This recommendation names no
language.**

**Rationale.**

- *Both routes are lawful; the record says so and says nothing more.* D-293 Decision 7 C8: "OD-101-1 is
  resolved before the core-implementation blueprint under `Architecture + release engineering` (a dedicated
  D-000 successor, or the owner's direct statement)."
- *No candidate list exists anywhere.* Packet §2 Q11; C5–C9 packet §C8: "OD-101-1: **none in the record** as a
  decision." A direct statement naming a language would be that language's first appearance as a choice, with
  no recorded comparison — which is the shape the recurring guard `does not mint Rust-as-core` (`## D-231`,
  `## D-232`, `## D-287`, four artifacts) exists to prevent. A successor that publishes the candidate set
  first creates the comparison the guard presupposes, and the comparison is what makes the choice reviewable.
- *The constraints to compare against are already recorded, so the successor invents nothing to run the
  comparison.* From `distribution-core-inventory-contract.v16` and file 08 DR-101/DR-115 (packet §2 Q11): small
  native executable; default install excludes language runtimes; platforms macos/arm64, macos/x86_64,
  linux/x86_64, linux/arm64 with Windows D-002 absent; the D-006 envelope with MB = 1e6 bytes (core ≤ 25 MB
  compressed / ≤ 80 MB installed; RSS 40/50 help-version, 60/100 doctor). And `DR-118 does not mandate
  implementation language`.
- *Route (iii) is self-defeating.* File 08 line 283 names DR-101 a "Hard blocker for core implementation
  blueprint", and the blueprint is Condition 5's subject, which file 08's conditions table records as "gated on
  1, 2 and 4". Leaving OD-101-1 RESERVED indefinitely leaves DR-101 `OPEN`, which keeps Condition 2 short,
  which keeps Condition 5 unreachable.

**Two guards the successor must carry.** First, naming a candidate inside that successor is a **proposal**, not
a recording, until the successor is adopted; the successor must say so. Second, the slice-1 adapter role token
"TypeScript" at `harness.DR-G15.packaging-adapter-conformance.v9.json` `d82fac57…` `$.slice1Adapter` is the
*adapter* role and must not be read across to the core language — the same field's next sentences are "This
specification does not add a Rust adapter and does not mint Rust-as-core."

**What changes if adopted.** A `distribution-core-inventory-contract.v17` and/or
`distribution-core-leftover-join.v11` carrying the candidate set and the choice, through Stage A + Stage B dual
review (C-plan §1, C8 row). `OBL-D1` stays `leftoverDesign: true` on `distribution-core-leftover-join.v10.json`
`1de52b76…` until that successor lands and a join remeasurement follows. DR-101 stays `OPEN` at the successor;
no Condition-2 movement from the successor alone.

**Risk.** If adopted: the choice is PREFERENCE-LADEN with cheap overturn (**Q12**), so a later owner may
reverse it and every citing act inherits the reversal; and the act is a two-artifact sequence in a lineage
where `distribution-core-leftover-join.v8` was REJECTED on custody defects (`CLAUDE-DCLJ-V8-SF1`,
`CLAUDE-DCLJ-V8-SF2`; C-plan §2). If deferred: the core-implementation blueprint and Condition 5 stay
structurally blocked, and C8-a and C8-b stay queued.

**Confidence: medium.** The route is well supported; whether the owner prefers to state a language directly is
a preference the record expressly leaves to them.

### Q12 — OD-101-1 Route C (preference) vs rule-governed

**Recommendation.** **Route C — PREFERENCE-LADEN, cheap overturn.**

**Rationale.**

- *It is already the adopted characterisation.* `DECISIONS-RECOMMENDED.md` §C5–C9, C8 bullet: "recorded under
  `Architecture + release engineering` (PREFERENCE-LADEN, cheap overturn)", adopted at D-293 Decision 7.
- *The contract offers the disjunction and declines to resolve it.*
  `distribution-core-inventory-contract.v16` `$.namedOpenDecisions[0].owner`: "A later Route-C or rule-governed
  successor, not this extraction."
- *The substance: no recorded rule determines the language.* `DR-118 does not mandate implementation language`,
  and DR-101's recorded constraints (small native executable, no runtimes in the default install, the four
  D-002 platforms, the D-006 envelope) are **filters**, not a decision procedure — more than one language
  passes them, so the residue is preference. `## D-001`'s classing of DR-101 as "Rule-governed architecture
  authoring with review" describes the **row's authoring discipline**; a row can be rule-governed while a named
  open decision inside it is preference-laden, which is exactly what the contract's own disjunction
  contemplates.

**Tension stated honestly.** `## D-001`'s classification is the counter-argument, and choosing Route C lowers
the overturn cost under D-000 clause 5. That is the practical consequence the owner is choosing.

**What changes if adopted.** It sets the overturn cost for the Q11 successor and can be recorded in that same
successor or as a one-sentence ruling. No readiness effect.

**Risk.** If adopted: cheap overturn means the language choice can be reversed by a later preference statement,
and every downstream artifact citing it inherits churn. If rule-governed were chosen: the successor would have
to exhibit a rule that determines the language, and no such rule is in the record — so the act would likely
fail review on its own terms.

**Confidence: high.**

### Q13 — OD-101-2 signing-ceremony content

**Recommendation.** **Leave RESERVED** pending its own DR-101 ceremony successor. Do not merge with DR-112, and
do not treat any OD-112 act as closing `OBL-D2`.

**Rationale.**

- *Nothing is in the record to confirm.* C5–C9 packet §C8: "OD-101-2: **none in the record.** Signing ROLES
  exist … no ceremony, threshold, or notarization procedure is named."
- *The live join already records the separation D-293 requires.*
  `distribution-core-leftover-join.v10.json` `1de52b76…` `OBL-D2` (alias `OD-101-2`): `leftoverDesign: true`,
  `existingGate: "none"`, `rideStanding: "not-capable-of-riding"`, reason verbatim —
  "distribution-core-inventory-contract.v16 extracts signing ROLES and reserves ceremony/thresholds/notarization.
  G01-G05 do not own OS notarization or code-signing ceremony. DR-112 recovery ceremony and DR-110 repair-media
  trust remain adjacent, not owners."
- *The content is not derivable, and the nearest thresholds are themselves reserved.* A ceremony is a threshold
  plus custody plus a notarization procedure; the parallel DR-112 threshold (OD-112-1, quorum/threshold
  cardinality) is "RESERVED. Named. Not minted." per **Q2**. Authoring an OD-101-2 ceremony now would either
  mint thresholds or borrow DR-112's — the merge D-293 Decision 7 C8 forbids.
- *The adopted text pre-empts the shortcut.* "a deferral to C1 does not close `OBL-D2`."

**What changes if adopted.** Nothing now. `OBL-D2` stays `leftoverDesign: true`; DR-101 stays `OPEN`; C8-b
stays queued behind C8-a.

**Risk.** If adopted: core code-signing and OS notarization stay undesigned, and they are named in DR-101's own
subject at file 08 line 283 ("signing/notarization") — for a product whose core is a *signed* distribution
core, that is the residual worth naming out loud. If merged with DR-112: it contradicts D-293 Decision 7 C8 and
the join's own reason string.

**Confidence: high.**

### Q14 — Derived MB byte constants in C9 occupancies

**Recommendation.** **Keep them forbidden.** Occupancies quote the rule (`MB = 1e6`) and never write the
derived decimal constants.

**Rationale.**

- *D-293 stated a rule, not constants.* Decision 7 C9: "MB means 1e6 bytes for the D-006 G01/G02/G04
  quantities."
- *The four adopted C9 acts already took this form, verified at this HEAD.*
  `harness.DR-G01.core-download.v11.json` `f95f0178…`, `harness.DR-G02.core-installed.v6.json` `e05bbaa4…` and
  `harness.DR-G04.core-memory.v5.json` `5a646c98…` each carry the token `MB = 1e6`, and none of
  25000000 / 80000000 / 40000000 / 50000000 / 60000000 / 100000000 occurs in any of the three. The D-305
  reviewer measured the same: `coordinator-decisions.D-305.review-adversarial.claude2.json` records "25000000
  is absent from the subject."
- *The occupancies already refuse the binary analogues by name*, per packet §2 Q14 — "Does not invent a D-006
  unit or authorize 26214400 as the bound." / "… 83886080 …" / "… a binary-MB byte constant." Admitting decimal
  literals would create the mirror hazard: a reader seeing `25000000` cannot tell whether it was derived under
  D-293's rule or minted, whereas "≤ 25 MB, MB = 1e6 bytes per D-293" carries its own derivation.
- *The record has a general property that points the same way.* `docs/coop/IMPLEMENTATION-FREEZE.md`
  `e809d439…` §7.1, line 1731: "A value that appears only as a literal in a vector, fixture, golden or example
  is not a rule." A bare constant would add no rule while risking being read as one.

**What changes if adopted.** Nothing — it confirms the form D-305..D-308 already used. Optionally one sentence
so later occupancies can cite it rather than re-deriving the discipline.

**Risk.** If adopted: every consumer does the arithmetic itself, so an arithmetic slip in a later act is
possible — the mitigation is that the rule travels with every quotation. If permitted: six numeric tokens enter
the record that no artifact states as authorized, and the C9 lineage's own refusals become internally
inconsistent.

**Confidence: high.**

### Q15 — G02 installed-tree accounting authorities

**Recommendation.** **Confirm the two the round-2 text names** — `Product + release engineering` (file 08
line 297, the DR-115 owner cell) and `Architecture + release` (file 08 line 338, the DR-G02 owner cell) — and
require that the rule they record cover **all five** recorded dimensions.

**Rationale.**

- *D-293's sentence names none.* "G02 installed-tree accounting stays open until the named authorities record a
  complete rule" — so the referent must come from the adopted round-2 text, which names those two. **Q0**
  supplies the adoption route; if Q0 were answered no, the recommendation is unchanged, because those two cells
  are the only authorities the register names for the two rows involved.
- *Both are the register's own owner cells*, so naming them invents no authority.
- *"Complete" must mean all five dimensions.* The recorded set is logical lengths, allocated blocks,
  metadata/xattrs, links, deduplicated inventory nodes (packet §2 Q15; the adopted C9 bullet names the same
  five). A rule silent on one leaves the comparison unscorable, which is exactly the residue the live join
  records: `distribution-core-leftover-join.v10.json` `1de52b76…` `OBL-2` reason — "Remainder is (a) G02
  tree-accounting UNDECIDED, so G02 size comparison cannot be scored, and (b) G01-G05 execution, which remains
  qualification (D-056)."

**What changes if adopted.** No act now; it fixes the referent so a later G02 accounting act knows who must
sign it. The rule itself stays open; `OBL-2` stays `leftoverDesign: true`.

**Risk.** If adopted: it relies on Q0 for the adoption route, though not for the substance. If deferred: "the
named authorities" has no referent, so no one can start the rule, and the record stays in the asymmetric state
`OBL-2` describes — G01 and G04 specified scorable on the new occupancies while G02 is not.

**Confidence: high.**

### Q16 — C10, C11, C12

**Recommendation.** **Authorise a new byte-cited evidence packet under `DECISION-PACKETS/` covering C10, C11
and C12 now**, and take the decisions after it exists — sequenced after the C4 and C8 chains. Do **not** park
them behind the seal or Condition 5.

**Rationale.**

- *Parking behind Condition 5 is circular.* File 08's conditions table records Condition 5 as "Not started;
  structurally last, **and gated on 1, 2 and 4**", and Condition 2 as "Every slice-affecting V2 row
  `SATISFIED`". C11 and C12 name rows that Condition 2 measures — DR-105 (line 287), DR-114 (line 296), DR-124
  (line 306), DR-127 (line 309) — and DECISIONS-NEEDED §C's own heading says each item "keeps a row OPEN until
  decided". An item that keeps a Condition-2 row open cannot lawfully wait for a condition that Condition 2
  gates.
- *They are genuinely undecided and unplanned.* C-plan §3's closing note: "`DECISIONS-RECOMMENDED.md`'s Summary
  table covers `C1–C4` and `C5–C9` only, and D-293's Decision items 6 and 7 name no C10/C11/C12 disposition.
  **They remain undecided and unplanned.**"
- *A packet costs no record act.* C-plan and D1-plan are both planning-only ("Planning only. Nothing here is
  recorded"; "It authors no fixture byte, records no successor artifact, proposes no COORD entry, and decides
  nothing"). Authorising the packet buys the owner a byte-cited basis without spending a review cycle.
- *Sequencing.* C10's G07 is owner-reserved under D-293 Decision 8, so it is owner work regardless; C12's
  DR-127 execution routes touch the anti-lockstep lineage D-300 has just written into, so measuring after
  D-300 rather than before is cheaper.

**What changes if adopted.** A new evidence packet under `DECISION-PACKETS/` (named by the owner; no name is
minted here). No record act, no file-08 edit, no Condition movement.

**Risk.** If adopted: more owner queue, at a point where five C-items already wait on owner sentences. If
parked: three items that keep Condition-2 rows open sit behind a condition that cannot be reached while they
are open.

**Confidence: medium.** The circularity argument is strong; whether to spend the effort now rather than after
the current C queue is the owner's call.

---

## 4. G3 — D1 byte blockers and named fixture opens

D-293 Decision 8 delegates the authoring shape; `D1-plan/README.md` records that "new semantic
members/values/lists/implementations are named open decisions, never a choice". Every recommendation below
respects that: where a choice would create semantics, the recommendation is a named open with a trigger, and
the trigger is named because D-293 Decision 6 requires one.

### G3-G15 — adapter implementation (`OBL-ADAPTER-IMPL`)

**Recommendation.** **Leave reserved. Name no adapter.** Record the reservation with its trigger: a DR-120
successor that lifts D-108's reservation, itself downstream of OD-101-1 (**Q11**). Separately — and this is the
lever that actually moves G15 — rule on **OQ-G15-1**, whether AT fixture *bytes* depend on the adapter or only
AT *execution* does.

**Rationale.**

- *The reservation is recorded and current.* `g15-leftover-join.v6.json` `4b2ac34c…` (D-290) stands
  `BLOCKED-ON-OBL-ADAPTER-IMPL`; `harness.DR-G15.packaging-adapter-conformance.v9.json` `d82fac57…`
  `$.slice1Adapter`, verbatim: "TypeScript. This specification does not add a Rust adapter and does not mint
  Rust-as-core. Adapter implementation remains reserved (D-108)." `## D-108` (COORD L4271) records "Adapter
  implementations remain reserved."
- *This is not an unowned choice; it is a reserved implementation.* The slice-1 adapter **role** is already
  recorded as TypeScript. What is reserved is the **implementation**. So the lawful lift is a successor that
  addresses D-108, not a fresh naming — and naming one now would mint a build or packaging tool that appears
  nowhere in the record, or mint Rust-as-core.
- *The real lever is OQ-G15-1, and it is cheap.* `D1-plan/G15.md` OQ-G15-1 records the two byte sets that make
  it ambiguous: `packaging-leftover-join.v4.json` `03251cc8…` `$.obligations[4].reason` ("The 51 D-106 fixtures
  are FG-3 hand-authored DR-103 admission-class evidence, not adapter-run AT fixtures.") against occupancy
  `$.at8.identityCase` ("two adapter RUNS") and three `matrixCells.*.passProperty` strings whose subject is
  "the adapter". A reviewed ruling that AT fixture bytes are authorable while AT execution waits would move
  most of the 324 AT cells without naming an adapter.

**Honest limit on that lever.** Even a favourable OQ-G15-1 ruling leaves `AT-8` short:
`$.at8.standing` says the seventeen AT-ARCHIVE-* keys admit no lawful fate but `produced`, and `produced` for
`AT-ARCHIVE-IDENTITY` is defined as two adapter runs (OQ-G15-4). So the identity case stays blocked on the
adapter regardless.

**What changes if adopted.** Nothing on the reservation. If the owner also rules on OQ-G15-1 favourably: a G15
corpus, plus successors on **both** joins — `g15-leftover-join.v6` and the ROW twin `packaging-leftover-join.v4`
`03251cc8…` (D-266) — since `D1-plan/README.md` records that closing a twinned obligation "requires a successor
on both".

**Risk.** If adopted: 324 AT cells stay unauthored and G15 stays Tier 4. If an adapter were named: it is an
implementation decision taken before OD-101-1 and before Condition 5, and D-108's reservation would be
overturned by an act that never reviewed it.

**Confidence: high.**

### G3-G16 — comparison-basis component axis

**Recommendation.** **Leave blocked. Do not enumerate the set.** Record the trigger: an application-grade
successor that applies `monorepo-ci-contract.v16` (or its successor) together with an authored ownership record
supplying the comparison-basis union.

**Rationale.**

- *The governing contract pre-emptively refuses the list the owner would write today.*
  `monorepo-ci-contract.v16.json` `$.selector.closedLaneUniverse.componentLanes`, verbatim: "Exactly one
  component lane per component identity in the comparison-basis union. **A current-declaration-only enumeration
  is never authoritative.**" Anything enumerable today is a current declaration, so enumerating cannot produce
  the authority G16 needs — it would produce a list the governing contract disclaims.
- *The gap is measured, not assumed.* `g16-leftover-join.v5.json` `7ce75ea5…` (D-278) stands
  `BLOCKED-ON-UNENUMERATED-COMPARISON-BASIS-COMPONENT-AXIS`. OQ-G16-1: occupancy
  `$.namedCorpusClasses[0].exactByteIntent` requires "one cell per declared comparison-basis component
  identity"; `$.componentAxis.source` = "Comparison-basis identities are not invented here";
  `.catalogAuthoredHere` = `false`; v16 is not applied; live file 02 lines 123–152 enumerate no component
  identities.
- *The route the record does name is the ownership record, and it is itself unmeasured.*
  `$.selector.ownershipRecord.standing` = "AUTHORITATIVE committed design record. Not CI YAML. Not a
  path-filter table as authority.", and D-310's Decision confirms "The ownership record stays the only impact
  authority". But OQ-G16-2 records that neither `g16-leftover-join.v5` nor `monorepo-leftover-join.v4`
  `03d4478c…` carries an `OBL-OWNERSHIP-RECORD`-shaped measurement, so whether authoring it falls inside
  `OBL-G16-FX-AUTHORING` or is a separate act is unsettled — the owner may want to settle that in the same
  breath.
- *Even after the axis lands, 24 is a floor.* `D1-plan/G16.md`: the 24 class-level cells are "a floor and not a
  closed total".

**What changes if adopted.** Nothing. `OBL-G16-FX-AUTHORING` stays `leftoverDesign: true` on
`g16-leftover-join.v5` and its ROW twin `monorepo-leftover-join.v4` `03d4478c…` (D-277).

**Risk.** If adopted: G16 stays Tier 4 indefinitely; DR-121 and DR-G16 stay `OPEN`. If enumerated: the list is
disclaimed as authority by the very contract that requires it, and the corpus built on it inherits the defect.

**Confidence: high.**

### G3-G18 — on-disk quarantine format

**Recommendation.** **Leave blocked.** Do not specify a format, and do **not** rule that a corpus may record
quarantine *fate* without quarantine *bytes*. Record the trigger as the pair the record actually names: closure
of `OBL-ENCODING-RESERVED` (the quarantine and journal format types) plus DR-111 (**Q3**) for the lock class.

**Rationale.**

- *The ROW twin states a positive rule that the fate-without-bytes reading would have to carve an exception
  to.* `lifecycle-leftover-join.v4.json` `bcc76ee3…` `$.proposedLaterWork[1]`, verbatim: "A later
  leftover-design cycle may author fixture implementations for the three named corpus classes **only where
  types are already closed**. This join does not invent those bytes." The quarantine type is not closed —
  D-311 classified the seven reserved lifecycle mechanisms as implementation encodings and left
  `OBL-ENCODING-RESERVED` `leftoverDesign: true`. And closing `OBL-G18-FX-AUTHORING` requires successors on
  **both** `g18-leftover-join.v6.json` `f531ba6a…` and this ROW twin, so the twin's rule governs any closure.
- *Specifying a format now would contradict a decision two headings old.* D-311 is the C6-a act; specifying the
  quarantine format would overturn it without reviewing it.
- *The block is wider than quarantine, which is why a single fate ruling would not unblock G18 anyway.*
  `D1-plan/G18.md` §4 records three separate unclosed types: quarantine format (OQ-G18-3, occupancy
  `$.retainedEvidence[1].exactByteIntent` — "Quarantine is required; on-disk quarantine format is reserved");
  the journal type (OQ-G18-1); and lock producibility (OQ-G18-2), where
  `component-manifest-schemas.v11.json` `1c0b8868…` `$.lockSchema.purpose` reads "NO lock is producible until
  DR-111 closes".
- *The occupancy supplies no lawful placeholder fate.* OQ-G18-3 measures that G18's `$.doesNot` and `$.failsIf`
  offer nothing like G15's `blocked-on-ride` vocabulary. Minting one would be new semantics — a named open, not
  a choice.

**The option the owner has if they want motion.** Ask which of the five live-cell members have closed types, and
author only those under the ROW twin's own "only where types are already closed" rule. That is a scoped
question the record's rule already licenses, unlike a fate placeholder. It is not recommended here because it
has not been measured; it is named so the owner knows the cheap door exists.

**What changes if adopted.** Nothing. `OBL-G18-FX-AUTHORING` stays `leftoverDesign: true` on both joins; the
40 G18 cases stay unauthored.

**Risk.** If adopted: G18 stays blocked on two of the owner's *own* open items — the C6 encoding disposition and
Q3's DR-111 windows — so it is not blocked on anything delegable, and it will not move on its own. If a format
were specified: it contradicts D-311. If fate-without-bytes were allowed: it carves an exception into the ROW
twin's stated rule, in the lineage whose closure requires that twin's successor.

**Confidence: high.**

### G3-HOSTILE — per-class golden counts (OQ-HG-5)

**Recommendation.** The 16-witness floor is **already authored and recorded** (D-300 — see §0). Supply **no**
per-class counts; record an explicit disposition that the universally-quantified classes' case counts stay
named-open, and that `OBL-HOSTILE-GOLDENS` therefore stays `leftoverDesign: true` after D-300. Two cheap
follow-ons are recommended alongside: rule on **OQ-HG-4**, and authorise the `anti-lockstep-leftover-join`
remasurement that D-300 expressly did not perform.

**Rationale.**

- *The floor exists.* `anti-lockstep-hostile-goldens.v3.json` `8be1b6c5…` (D-300, dual ACCEPT 0/0):
  `$.whatIsAuthored` = "Sixteen catalog members. Sixteen UTF-8 .bin citation files under
  docs/coop/artifacts/fixtures/anti-lockstep-goldens.v1/ with no platform subdirectory. Five join units J-1..J-5
  and eleven class units CC-1..CC-11 …"; `$.summary.authoredMembers` `16`;
  `$.leftoverDesignClosedIfAcceptedAndRecorded` `[]`.
- *D-300 gives the reason the obligation stayed open, verbatim*: "leftover-design of OBL-HOSTILE-GOLDENS
  remains on anti-lockstep-leftover-join.v3 (D-186) because leftover-join remasurement is not this entry,
  because **seven classes carry unenumerated within-class quantifiers**, and because closing that obligation
  needs a successor on anti-lockstep leftover-join alone (no same-id GATE twin)." (`D1-plan/OBL-HOSTILE-GOLDENS.md`
  OQ-HG-5 names six such classes by name — CC-1, CC-2, CC-4, CC-5, CC-7, CC-9. The two counts are reported as
  measured; this file does not reconcile them, and a reviewer should re-check both against the bytes.)
- *Counts cannot be supplied without inventing the coverage set.* `$.whatIsNotAuthored` on the same artifact
  lists "an enumerated CC-1 reachable-ordering list"; the plan's §2 arithmetic records "Golden *cases* per
  class: **not enumerable from the record**", the quantifiers being universals ("Every pairwise and every
  reachable total ordering", "every byte offset", "EVERY channel state", "every handshake step boundary")
  with no member list. For CC-11 the contract bounds its own claim: "these fixtures show serialization
  indifference on the exercised vectors and nothing more - a finite fixture set cannot prove the universal
  negative."
- *OQ-HG-4 is worth a sentence because it decides whether the CC work is done once or twice.* The same eleven
  CC classes are measured `leftoverDesign: true` under two ids on two rows — `OBL-HOSTILE-GOLDENS` on DR-127
  and `OBL-G21-FX-AUTHORING` on DR-G21. The custody rules are explicit both ways (D-300: "Does not steal G21
  leftover remaining on DR-114"; D-301/D-302: "Does not steal leftover-design of OBL-HOSTILE-GOLDENS remaining
  on anti-lockstep-leftover-join.v3"), but nothing says whether one authored byte set may discharge both.
- *The remasurement is unblocked and cheap.* `anti-lockstep-leftover-join.v3.json` `820d724a…` is still current
  and still predates D-300, which expressly "Does not remasure anti-lockstep-leftover-join.v3."

**What changes if adopted.** No fixture act. One disposition sentence; optionally one OQ-HG-4 ruling; and one
`anti-lockstep-leftover-join` successor citing D-300. No Condition-2 movement — D-300's own readiness recital
is "Zero SATISFIED. Condition 2 stays 5 of 32."

**Risk.** If adopted: `OBL-HOSTILE-GOLDENS` does not close, and DR-127 stays a "Hard blocker for
independent-release blueprint" (file 08 line 309). If counts were supplied: a minted coverage set that six or
seven recorded universal quantifiers contradict — the single largest sizing risk the plan names.

**Confidence: high.**

### G3-SARIF-RUNID — `FC-OUTFAIL.committed-run-preserved`

**Recommendation.** **Keep it parked.** Do not author an opaque pinned literal RunId. Name the trigger: closure
of the DR-006 canonical RunId / Finding fingerprint recipes (ID-DEP-S1).

**Rationale.**

- *The park is not this row's to lift.* `docs/coop/IMPLEMENTATION-FREEZE.md` `e809d439…` §7.1, line 1711,
  verbatim: "Every row above must be closed by a binding artifact before signature. **None may be closed by
  this record, by the blueprint, by a checker, or by an implementer.**" The RunId derivation row's implementer
  rule (column 4) is "Escalate. Do **not** choose CSPRNG bytes, a `RunDescriptor` digest, or an evidence-bundle
  digest — they have opposite retry-determinism consequences."
- *The case's own pass property resolves the two readings.* `sarif-fc-outfail-golden-bind.v1.json`
  `$.namedCases[0].intentVerbatim` requires the fixture to "preserve its identity and sealed termination" for
  an already-committed Run. A literal that no recipe produced cannot be *preserved* — there is nothing it is
  the preservation of. §7.1's "A value that appears only as a literal … is not a rule" (line 1731) shows a
  literal mints no recipe; it does not show a literal can carry identity continuity, which is what this case
  asserts.
- *The prohibitions are on the row itself.* `sarif-leftover-join.v4.json` `a2ab59d7…` `$.doesNot[8]` and
  `sarif-projection-contract.v15.json` `$.whatThisDoesNotDo[3]`, both "Does not mint RunId/Finding recipes",
  with `$.identityDependencies.dependencies[0]` (ID-DEP-S1) recording the ride on DR-006.
- *The record has already taken the available half and left this one, one heading apart.* D-297 recorded
  `sarif-fc-outfail-golden.v3.json` `236fdb33…` for `FC-OUTFAIL.no-committed-run`, whose shape needs no
  derivation (`d9-exit-contract.v1.14.json` `8dd33038…` `$.hostTerminationUnion.nullabilityPolicy`: "a
  pre-admission failure omits runId entirely rather than carrying null"), and its Decision states
  `committed-run-preserved` "stays NOT-AUTHORED under the §7.1 RunId park". Confirming the park makes an
  existing conduct explicit rather than creating a new standing.

**What changes if adopted.** Nothing. `OBL-FC-OUTFAIL-FX` stays `leftoverDesign: true` on
`sarif-leftover-join.v4` `a2ab59d7…` (D-182); DR-122 stays `PROPOSED-CLOSED-FOR-REVIEW`.

**Risk.** If adopted: DR-122's FC-OUTFAIL obligation cannot close until DR-006 does, so DR-122 carries one
unauthored case indefinitely. If a literal were pinned: it would be the first RunId value in the record, and
§7.1 line 1711 says no implementer may close that row.

**Confidence: high.**

### G21 named opens

For each: recommend a value, or "leave named-open and skip those members". Four of the five are leave-and-skip;
one is a ruling.

#### G21-EXACT — exactly-at vs the preHandshake `N > 65536` bound

**Recommendation.** **Leave named-open and skip the member.** Do not author "CC-5 prefix exactly at the
operative bound". Trigger: a `control-protocol-contract` successor that states what "exactly at the operative
bound" refuses.

**Rationale.** This is a byte contradiction, not a preference.

- *The framing clause does not refuse `N = 65536`.* `control-protocol-contract.v2.json` `c50a79fe…`
  `$.transportAndFraming.framing.bounds.preHandshake`, verbatim: "Until helloAck is accepted, **N greater than
  65536** or N equal to 0 is refusal family RF-2, detected from the prefix alone". 65536 is not greater than
  65536.
- *The class intent requires an RF-2 fate for that member.*
  `$.hostileDualChannelConformance.classes[4].intent` lists "prefix exactly at, one over, and far over the
  operative bound (pre- and post-handshake bounds separately)" and states "**Each is RF-2 typed**". So
  authoring `N = 65536` as a CC-5 member asserts a fate the framing clause does not produce — a semantic claim
  against the contract, not a witness selection.
- *The postHandshake half does not rescue it.* `$…bounds.postHandshake`: "A frame **exceeding** the negotiated
  bound is RF-2" — exactly-at is again not refused; and it additionally needs a negotiated value (see
  **G21-POST**).
- *The record has already refused this twice, at the two most recent G21 headings.* D-301 and D-302 both carry
  "Does not pin N=65536 as prefix-only RF-2"; D-302 adds "Does not author prefix exactly at the operative
  bound"; `g21-fixture-corpus.v11.json` `13ede110…` `$.whatIsAuthored` ends "No exactly-at member." and
  `$.remainderAfterThisCorpus` records "CC-5 prefix exactly at the operative bound remains unauthored,
  including its postHandshake half; N=65536 is not pinned as RF-2."

**What changes if adopted.** Nothing authored. `OBL-G21-FX-AUTHORING` cannot close while this member is
unauthored, and any successor corpus must keep `$.leftoverDesignClosedIfAcceptedAndRecorded` empty and keep
carrying "Does not claim CC-5 fully authored" (`D1-plan/G21.md` §6 risk (d)).

**Risk.** If adopted: CC-5 stays permanently short of its own closed intent until a contract successor lands,
so DR-G21's fixture obligation cannot close. If authored anyway: the fixture asserts RF-2 where the contract's
predicate does not, which is precisely the class of defect that rejected `g21-fixture-corpus.v3` and `.v4`
(`G21FXV3-M1` / `G21FXV4-M1`, a witness filed under a closed identifier it does not belong to).

**Confidence: high.**

#### G21-POST — the postHandshake bound

**Recommendation.** **Leave named-open and skip both postHandshake members** — "far over the operative bound
(postHandshake half)" and "prefix one over the postHandshake bound". Trigger: a successor that pins a
negotiated `maxControlFrameBytes` for fixtures **and** states the fixture form for postHandshake session state.

**Rationale.**

- *A fixture must pick one negotiated value and the record pins none.*
  `$.transportAndFraming.framing.bounds.postHandshake`: "the operative bound is the negotiated
  maxControlFrameBytes (handshake field): the component may accept less than the host offer but never less than
  65536; the ceiling either side may offer or accept is 16777216." `$.handshake.sequence[1]` bounds it ("at
  most the offer, at least 65536") without pinning it. Minting one is `D1-plan/G21.md` §6(b) item 4 —
  "Record as a named open decision, do not choose."
- *Both quotable constants are unusable here.* `g21-fixture-corpus.v8.json` `$.whatIsNotAuthored` lists "65536
  or 16777216 as newly invented bounds" and "26214400". If the assumed bound were 65536, "one over" is 65537 —
  byte-identical to the already-authored `G21.cc5.prefix-one-over-prehandshake` (`76cc5805…`), so the two
  injections would be distinguishable only by session state, not by payload bytes (OQ-G21-3). If it were
  16777216, `g21-fixture-corpus.v11.json` already warns in its own member `mutation`: "These bytes coincide with
  the postHandshake ceiling; a later prefix-exactly-at-postHandshake fixture must not reuse these bytes."
- *The fixture form is unsettled too.* Both authored CC-5 payloads are 4-byte prefix-only files; OQ-G21-4
  records that whether a postHandshake fixture needs a session script rather than a payload file is not
  settled. Choosing that form is a new fixture semantics, not a witness selection.
- *D-302 already recorded the refusal*: "Does not author the postHandshake far-over half."

**What changes if adopted.** Nothing authored; two of the ten remaining CC-5 injections stay named-open, with
the same closure consequence as G21-EXACT.

**Risk.** If adopted: CC-5 stays short by two more members. If a value were minted: it enters the record as a
protocol constant that `constantsStatus` expressly says is not a measurement, and it collides with the already
authored far-over payload's bytes.

**Confidence: high.**

#### G21-SCHEMA — per-type control-frame body schema

**Recommendation.** **Leave named-open and skip the seven body-carrying CC-5 injections** — truncated bodies,
invalid UTF-8, duplicate members, unknown members, floats, negative integers, over-uint53 integers. Trigger: a
successor authoring per-type body schemas for the `capabilityEnvelope.messageVocabulary` types.

**Rationale.**

- *Every body needs a per-type schema, and none is authored.*
  `$.controlFrameEncoding.messageEnvelope`, verbatim: "Every frame body object has exactly these members: type
  (string, closed vocabulary at capabilityEnvelope.messageVocabulary), seq (integer, per framing.sequencing),
  controlMajor (integer; fixed at the negotiated major after hello), **body (object; per-type schema)**." And
  `g21-fixture-corpus.v8.json` `$.whatIsNotAuthored`, carried forward verbatim into `g21-fixture-corpus.v11.json`,
  lists "a ping, pong, hello, helloAck, or other per-type body schema" as not authored.
- *The plan calls this out as the binding constraint.* `D1-plan/G21.md` §6(b) item 6: "**Record as a named open
  decision, do not choose.** This is what stops seven of the ten remaining CC-5 injections from being
  straightforward."
- *Quoting a `type` token is not obviously enough.* OQ-G21-4 leaves open whether a body may be constructed by
  quoting a vocabulary member without authoring that type's body schema.

**The one the owner could unblock cheapest.** `"CC-5 truncated bodies"` is "a prefix `N` with fewer than `N`
body bytes delivered" (`D1-plan/G21.md` §2 item 29) — the receiver never completes a parse, so no per-type
schema is exercised. What blocks it is not the schema but the fixture-form question: whether a payload *file*
can express "fewer than N bytes delivered", which is a delivery property. That is the same OQ-G21-4 ruling
G21-POST needs, so one fixture-form ruling would move both.

**What changes if adopted.** Nothing authored; seven of the ten remaining CC-5 injections stay named-open.

**Risk.** If adopted: CC-5 is the largest remaining G21 block and it stays blocked. If a schema were authored:
it is new protocol semantics minted inside a fixture corpus — `D1-plan/G21.md` §6 names "inventing a vocabulary
the record does not carry" as the second-ranked recorded reviewer-rejection pattern for this gate.

**Confidence: high.**

#### G21-NT6 — author NT-6 at G21 despite `$.doesNot[20]`

**Recommendation.** **Choose.** Rule that `g21-leftover-join.v13.json` `058717f5…` `$.doesNot[20]` = "Does not
author NT-6." is **self-referential** — it disclaims that join's own act, not a successor corpus — so NT-6 is
authorable at G21 as a delegated D1 act. Its D9 token must be **quoted** from `d9-exit-contract.v1.14.json`
`8dd33038…`, never invented.

**Rationale.**

- *The same join lists NT-6 as remaining work.* `$.obligations[3].remainingNotAuthored.dr133` = `["NT-6"]`. A
  join cannot coherently measure an item as remaining work and simultaneously forbid anyone from ever doing it;
  the two readings are reconciled only by the self-referential one.
- *The parallel entries have the self-referential shape.* OQ-G21-10 records that `$.doesNot[24]` / `$.doesNot[32]`
  ("Does not author per-D-002-platform copies of the NT-1/NT-2 payloads" / "… of the two CC-5 payloads")
  disclaim acts that `authoredImplementations` records as already done by other artifacts. The
  counter-argument OQ-G21-10 also records — that `$.doesNot[20]` lacks their qualifier and sits among
  substantive prohibitions — is real, and is why this is a ruling rather than an assumption.
- *The record's own recent practice is per-entry disclaimer.* D-301 and D-302 each carry "Does not author
  NT-6" as a statement about that entry, which is exactly the self-referential form.
- *The adopted B2 stands on the other side of the tension and should not be left unresolved.*
  `DECISIONS-RECOMMENDED.md` §B2, adopted at D-293 Decision 5: NT-6 authoring "treated as established work";
  Codex's round-2 AGREE: "author NT-6".
- *Sequencing: not behind the DR-133 opening.* Codex's B2 round-2 AGREE places NT-6 authoring "Before the later
  per-row cycle", and `D1-plan/G21.md` §4 records the standing as NOT BLOCKED on that basis, NT-6 being fully
  defined at `provider-only-output-contract.v3.json` `ef2a7416…` `$.negativeTests["NT-6"]` and constructible
  against the pinned wire.
- *The D9 limb resolves by quotation, which is the lineage's own recorded method.* OQ-G21-13 asks whether a
  hostile-input D9 token counts as an invention against `$.doesNot[3]` ("Does not invent a D9 code, exit
  number, or HostTermination"). The lineage already distinguishes quoting from minting: `g21-fixture-corpus.v11.json`'s
  member `mutation` states "16777216 is quoted, not invented", and `G21.cc5.prefix-one-over-prehandshake`
  quoted 65536 to derive 65537. `d9-exit-contract.v1.14.json` `8dd33038…` is present and pinned, so a quoted
  class token is available without minting one.

**What changes if adopted.** NT-6 becomes authorable as a delegated act: one corpus plus a
`g21-leftover-join` successor (no ROW twin — `D1-plan/README.md` records G21 has none). DR-133 is untouched:
the act authors a DR-133 negative test at the G21 gate and does not SATISFY DR-133, exactly as D-301 and D-302
each recite.

**Risk.** If adopted: the ruling reads a prohibition narrowly, and a reviewer may read `$.doesNot[20]`
substantively — the counter-argument is recorded and the owner is overriding it, which should be said in the
entry rather than glossed. If left named-open: the last unauthored DR-133 negative test on the G21 join stays
parked behind an ambiguity that one sentence resolves, and B2's adopted "author NT-6" has no route.

**Confidence: medium.**

#### G21-FCNC — FC-NC default-posture / process-tree vs the G12 owner reservation

**Recommendation.** **Leave named-open and skip the member.** Do not author `FC-NC-CA1-PROCESS-TREE` at G21.
Trigger: an owner ruling on the FC-NC **reservation** — whether the CA-1 apparatus is released at G21 while the
default-posture half stays reserved at G12.

**Rationale.**

- *The subject split is recorded, so the temptation is real.* `harness.DR-G21.component-failure-containment.v4.json`
  `$.basedOn.doctorV4.role`: "FC-NC consented CA-1 process-tree containment is this gate, not G12"; and
  `$.retainedEvidence[1].passProperty`: "that half remains G12".
- *But FC-NC as a whole is owner-reserved on two joins.* `g12-leftover-join.v5.json`
  `$.obligations[3].namedCorpusNotAuthored` and `doctor-actor-leftover-join.v12.json`
  `$.obligations[10].namedClassesNotAuthored`; D-293 Decision 8 reserves "the gate obligations at G07, G08,
  G09, G12, G14 and G22 (with every current same-id ROW twin)".
- *A partial release is not actually partial, because the apparatus is shared.* OQ-G21-11 records that both
  halves are witnessed against one `doctor-contract.v4` class with one `exactByteIntent` and one
  `passProperty` covering both postures, and that the CA-1 half needs the same apparatus — process/module
  trace, sentinel-writing component fixture, doctor report. Authoring the CA-1 half at G21 would build the
  reserved G12 apparatus under a delegated id.
- *The delegated orchestrator has already honoured the reservation*: D-301 and D-302 each carry "Does not
  author FC-NC-CA1-PROCESS-TREE."
- *Also blocked by G21's own prohibitions.* `D1-plan/G21.md` §6(b) item 11 records that authoring the FC-NC
  default-posture half violates `$.doesNot[5]` ("Does not take over G12 …") and `$.doesNot[6]`.

**What changes if adopted.** Nothing authored; the member stays outside every G21 corpus, as the two most
recent G21 entries already recite.

**Risk.** If adopted: one G21 live-cell member stays unauthored, contributing to the same non-closure as
G21-EXACT / G21-POST / G21-SCHEMA. If released half-way: the owner's G12 reservation is effectively spent by a
delegated act, on a security-adjacent gate, without the G12 obligation itself being decided.

**Confidence: high.**

---

## 5. Summary table

| id | Recommendation (≤20 words) | Confidence |
|---|---|---|
| G1-117 | Write the opening now citing v10 `8f34c92e…`; no shared gate-2 wait; G29/G30 immediately after | high |
| G1-131 | Keep B1's order: shared gate-2 entry, then fresh review of v2 `081ff7fb…`, then opening | high |
| G1-133 | Same order against v3 `ef2a7416…`; NT-6 is a separate later act, not opening content | medium |
| Q0 | Yes — D-293 reaches round-2 content it names, at digest `44f51a5d…`; bound the reach | high |
| Q1 | Drop the `preview` qualifier; keep OD-112-3 in `namedOpenDecisions` with DECIDED standing | medium |
| Q2 | Leave RESERVED; supply no values and record no parking entry now | high |
| Q3 | Leave RESERVED as one coherent set; no isolated unit, no partial surfaces | high |
| Q4 | Assign the population packet to file 08's cell `Security + release + platform owners` | high |
| Q5 | Leave RESERVED until after C4-c makes the TCB grammar governing | high |
| Q6 | COORD-only stands; register echo owed at a later MF-6; no eligibility effect | high |
| Q7 | Rule no: a scope label alone never satisfies gate 2 while `leftoverDesign` is true | medium |
| Q8 | Leave the numeric limb open; any later cap needs named gate, corpus, runner | high |
| Q9 | Successor citation already done (D-312); echo at a later MF-6 on DR-103, not DR-115 | high |
| Q10 | Confirm D-304's `specifiedNotLeftover`; the join's own discriminant selects it | high |
| Q11 | Dedicated D-000 successor publishing a candidate set, then choosing; name no language here | medium |
| Q12 | Route C — PREFERENCE-LADEN, cheap overturn; no recorded rule determines the language | high |
| Q13 | Leave RESERVED pending its own DR-101 ceremony successor; do not merge with DR-112 | high |
| Q14 | Keep decimal constants forbidden; occupancies quote `MB = 1e6` as D-305..D-308 did | high |
| Q15 | Confirm `Product + release engineering` and `Architecture + release`; rule must cover five dimensions | high |
| Q16 | Authorise a new evidence packet now; parking behind Condition 5 is circular | medium |
| G3-G15 | Leave the adapter reserved; instead rule OQ-G15-1 (fixture bytes vs execution) | high |
| G3-G16 | Leave blocked; a current-declaration enumeration is never authoritative per the contract | high |
| G3-G18 | Leave blocked; no format, and no fate-without-bytes against the ROW twin's rule | high |
| G3-HOSTILE | Floor authored at D-300; counts stay named-open; rule OQ-HG-4; remasure the join | high |
| G3-SARIF-RUNID | Keep parked; §7.1 says no implementer may close that row; trigger is DR-006 | high |
| G21-EXACT | Leave named-open, skip; `N = 65536` is not "greater than 65536", so not RF-2 | high |
| G21-POST | Leave named-open, skip both; no negotiated `maxControlFrameBytes` and no fixture form | high |
| G21-SCHEMA | Leave named-open, skip seven; no per-type body schema is authored | high |
| G21-NT6 | Choose: `$.doesNot[20]` is self-referential; NT-6 authorable, D9 token quoted not invented | medium |
| G21-FCNC | Leave named-open, skip; FC-NC is owner-reserved at G12 and the apparatus is shared | high |

---

## 6. What this file does not do

It records nothing. It edits nothing under `docs/`. It makes no readiness claim. It does not open D-056 Class A
for any row, and it does not SATISFY DR-117, DR-131 or DR-133. It does not edit file 08 or COORD, and nothing
here is committed. It mints no language and does not treat Rust-as-core as decided — Q11 recommends a route,
names no language, and expressly flags the `slice1Adapter` "TypeScript" token as an adapter role that must not
be read across to the core. It invents no identifier, number, list, verdict or fixture byte, and where a value
would be new it recommends a named deferral with a trigger instead. Every digest above was recomputed at HEAD
`a2d004066d2db7ae89de9ea56979bddb210f0786`; §0's remasurement corrects the packet from bytes rather than
inheriting its framing, and the one count discrepancy found (D-300's "seven classes" against OQ-HG-5's six
named classes) is reported as measured rather than reconciled.
