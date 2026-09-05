# G — owner residuals: Claude round 2 (answering Codex's AGREE-WITH-AMENDMENT)

Round 2 under `DECISION-PACKETS/RECOMMENDATION-PROTOCOL.md`. Answers
`DECISION-PACKETS/G-owner-residuals.codex-recommendation.json` (verdict AGREE-WITH-AMENDMENT, confidence high;
six per-question amendments, six top-level refutations). Round 1 is
`DECISION-PACKETS/G-owner-residuals.claude-recommendation.md`. Evidence: `DECISION-PACKETS/G-owner-residuals.md`.

**Nothing here is decided. The owner decides.** This file records no act, edits nothing under `docs/`, edits
neither file 08 nor COORD, makes no readiness claim, opens no D-056 Class A, does not SATISFY DR-117, DR-131 or
DR-133, and is not committed.

Measured at HEAD `a2d004066d2db7ae89de9ea56979bddb210f0786`, last COORD heading `## D-313` (298 `## D-` headings).
Date from the clock: 2026-08-29.

| Pin | Path | sha256 (recomputed at this HEAD) |
|---|---|---|
| file 08 | `docs/v2/architecture/08-decision-and-readiness-register.md` | `e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e` |
| COORD | `docs/coop/COORDINATOR-DECISIONS.md` | `fcd95bf67af0ad076b1e3f9e7a784fcda5dbf4632001f844c70782c0a19f7b5c` |
| agreed recs | `DECISIONS-RECOMMENDED.md` | `42f27394746d4aac569a09a01da719c0cf318cf114086635e73097a6add97370` |
| C1–C4 round 2 | `DECISION-PACKETS/C1-4-reserved-numbers-security-quality.claude-recommendation.r2.md` | `44f51a5d36eb3f03c711112a50119ea67fb01b3a07d255ccbac5d51cc0485627` |

Artifact digests recomputed for this round: `signed-index-trust-contract.v14.json`
`039a570244441709c8a773d2c92944fff7ad1b249718656ab2d87645feec6715`; `component-manifest-schemas.v11.json`
`1c0b8868444a097256aaa7d9caf8ebaa1c6f73fb071dbb4dd712334abb17a005`; `lifecycle-leftover-join.v4.json`
`bcc76ee3d99c88c258496dcc5591682d4ad655e06049b802a383ba03d3f1ddfb`; `anti-lockstep-hostile-goldens.v3.json`
`8be1b6c59515d0e00aff5fe0de584d0ab1aabbdf3091bf878e3258a1c639fd31`; `anti-lockstep-leftover-join.v3.json`
`820d724a10a1e11a2188a323a3425cd13f4c483892bb487fb93f6542103c85e1`; `g21-leftover-join.v13.json`
`058717f51ee62e85fa3094e9a65c207fb78a7f706e57a35a854f1a9a55ecc66e`.

---

## 0. Verdict

**All six Codex amendments are adopted.** Four are adopted as written; two are adopted with the byte citation
corrected or completed in Codex's own direction, not against it. No Codex refutation is rejected.

| id | Codex verdict | Claude round 2 |
|---|---|---|
| Q1 | AGREE-WITH-AMENDMENT | **Adopted as written.** Round 1 limb (a) was wrong and is reversed. |
| Q8 | AGREE-WITH-AMENDMENT | **Adopted as written.** Round 1's three-part triad is withdrawn. |
| G3-G18 | AGREE-WITH-AMENDMENT | **Adopted**, with the citation strengthened from the join to D-311's own Decision. |
| G3-HOSTILE | AGREE-WITH-AMENDMENT | **Adopted**, and round 1's unreconciled count is now reconciled: the seventh class is CC-6. |
| G21-SCHEMA | AGREE-WITH-AMENDMENT | **Adopted as written.** Seven becomes six plus one on a different trigger. |
| G21-NT6 | AGREE-WITH-AMENDMENT | **Adopted as written** on sequencing; the substantive ruling and the guard are kept. |

The other twenty-four ids carried Codex AGREE with empty `refutations` and empty `amendments`. They stand
exactly as round 1 wrote them, except for the two bookkeeping knock-ons recorded at §2 below, neither of which
changes a recommendation.

Two of the six corrections make round 1 **less** conservative than it was (G3-G18's trigger is a live route,
not a prohibition; G3-HOSTILE's count is resolvable from bytes). Four make it more accurate without changing
what the owner is asked to do. That distribution is worth the owner's notice: the disagreements were about
grounds, not about dispositions, and no disposition moved.

---

## 1. The six amendments

### Q1 — OD-112-3 wording after D-309 — **Codex is right; round 1 limb (a) is reversed**

**Codex's refutation, verbatim:** "Claude's Q0 conclusion reaches the round-2 C1 bytes, but those bytes say
that the existing preview refusal stands. Dropping preview therefore conflicts with Claude's own incorporation
analysis." And: "signed-index-trust-contract.v14 namedOpenDecisions[2].standing and
offlineRunningPolicy.totalDecision[4].alreadyRunning both say D-293 did not choose this residual axis; final
does not itself authorize a wider product-stage scope."

**Answer: adopted in full.** The refutation is correct on the bytes, and it is correct about round 1's internal
inconsistency. `DECISION-PACKETS/C1-4-reserved-numbers-security-quality.claude-recommendation.r2.md`
`44f51a5d36eb3f03c711112a50119ea67fb01b3a07d255ccbac5d51cc0485627` line 6 reads, verbatim: "**C1 DR-112:**
record OD-112-3 now as a final fail-closed decision (**the existing preview refusal stands**). Do not invent
OD-112-1/2/4; …". Round 1's Q0 answer makes exactly that file's C1–C4 content adopted at that digest. Round 1
then recommended dropping the qualifier that same text preserves. Both cannot be held; the adopted text wins,
and my round-1 limb (a) is withdrawn.

The round-3 C1 text carried in `DECISIONS-RECOMMENDED.md` — "OD-112-3 recorded now as the final fail-closed
policy" — does not repeat the parenthetical, but round 3's own words are "All three amendments adopted **on top
of round 2**", so the parenthetical is not displaced. That is the same incorporation route Q0 answers.

**Adopted round-2 recommendation.** **(a) Preserve the `preview` qualifier**: the decided OD-112-3 standing is
the existing `signed-index-trust-contract.v8` preview refusal, recorded as final. Do not widen the policy
beyond the preview product stage without a separate owner act. **(b) Unchanged from round 1** — OD-112-3
**stays** in `namedOpenDecisions` with a DECIDED standing rather than leaving the array; Codex agreed, and the
`OBL-OD-2` analogue (a changed standing, not a deleted entry) still supports it.

**One drafting requirement the successor must carry, and it is reviewer bait.** In
`signed-index-trust-contract.v14.json` `039a5702…` `$.offlineRunningPolicy.totalDecision`, entries `[0]`, `[1]`,
`[2]`, `[3]` and `[5]` all give `alreadyRunning` as bare `refuse`; only `[4]` (TR-COMPONENT ST-REVOKED) carries
the stage qualifier. That asymmetry was round 1's real motive and it survives the amendment. The successor must
say plainly that the qualifier is the v8 standing token carried forward under the adopted C1 wording, and must
not silently harmonise `[4]` with its five siblings — a silent harmonisation is the scope widening Codex's
refutation forbids, arriving by a side door. Both the `namedOpenDecisions[2].standing` and the
`totalDecision[4].alreadyRunning` "Residual axis, named not chosen" sentences are then replaced by the chosen
wording; nothing else in the contract moves.

**What changes if adopted.** A `signed-index-trust-contract` successor and its paired signed-index
leftover-join successor recording the chosen wording, through the normal Stage A + Stage B cycle. No file-08
edit. DR-112 stays `OPEN` (file 08 line 294); no Condition-2 movement — D-293 Decision 6's "no Condition-2 or
D-056 eligibility effect without a separate reviewed act and a successor join" continues to govern.

**Risk.** If adopted: `[4]` remains the one stage-qualified refusal in its table, and every future reader of
that table will ask why; the successor answers it in words rather than by editing the token. If round 1's
widening had been adopted instead: it would have contradicted the adopted C1 text and extended a security
policy's scope by inference from the single word "final".

**Confidence: high** (raised from round 1's medium — the adopted C1 byte removes the judgement call that made
limb (a) medium).

### Q8 — OD-1 cap values and what "measured caps" measures — **Codex is right; the triad is withdrawn**

**Codex's refutation, verbatim:** "The live schemas and component-manifest leftover join establish
product-owned, measured caps and record that no current gate measures the quantities; they do not establish
Claude's new universal named-gate, named-corpus, named-runner triad as a binding prerequisite."

**Answer: adopted in full.** Round 1's disposition (leave the numeric limb open, supply no numbers) is
untouched and Codex agrees with it. What Codex correctly refuses is the sentence round 1 attached to it: "a cap
is settable only with a named measuring gate, a named corpus, and a named runner class." That triad is not in
the bytes. What the bytes carry is a *different* three-part pattern, on a different axis:
`component-manifest-schemas.v11.json` `1c0b8868…` `$.namedOpenDecisions[0].candidateOwners`, verbatim — "a cap
is a product threshold, and thresholds in this corpus are **product-owned, measured, and waiver-formed (the
D-006 pattern)**", with DR-115's machinery described as owning "the core's size/startup/memory numbers, DECIDED
at D-006, **with the measurement half at qualification**". "Named corpus" and "named runner class" appear
nowhere in it; "named runner/workload" comes from `control-protocol-contract.v2.json` `c50a79fe…`
`$.transportAndFraming.framing.bounds.constantsStatus`, which is a DR-102 framing clause, not an OD-1 rule.
Round 1 assembled a prerequisite out of two rows and one analogy and stated it as binding. Choosing the
leave-open option and minting a new rule in the same breath is the shape D-293 Decision 6 and the HANDOFF exist
to prevent; Codex caught it, and it is withdrawn.

**Adopted round-2 recommendation.** Leave the OD-1 numeric limb explicitly open and supply no cap values — the
fallback the adopted C7 text already carries (`DECISIONS-RECOMMENDED.md` §C5–C9, C7 bullet: "if values are not
available, leave the numeric limb open and say so"). **Any later value proposal must state an evaluable
measurement method and follow the recorded D-006 pattern the artifact itself names** — product-owned, measured,
waiver-formed, with the measurement half at qualification. This answer creates no measurement prerequisite of
its own.

**Two recorded observations, offered as what a reviewer will raise, not as rules this answer makes.**
`component-manifest-leftover-join.v15.json` `f27ffac2…` `OBL-OD-1` records `existingGate` `"none"` and, in its
reason, "existingGate stays none; **no gate measures these four quantities**" — so a proposer must expect to be
asked what performed the measurement. And `control-protocol-contract.v2.json`'s `constantsStatus` records, for
its own row, that "a numeric threshold without a named runner/workload measures nothing (the D-006 lesson
recorded in D-007's alternatives)" — an instructive precedent, and expressly not a DR-103 prerequisite here.

**Unchanged from round 1, and still the useful half for the owner.** The cost of deferring is bounded: C7's
precondition bites only on "oversized-input fixtures", and `D1-plan/G15.md` §4(d) measures that
`schemas.v11` `$.testCorpusRequirements.classes[3].requires` names no over-length member and that the token
`oversized` appears in none of the five G15 governing files. Deferring the caps blocks no currently-planned
fixture act. Codex did not contest this and it stands.

**What changes if adopted.** Nothing recorded; optionally one sentence so later acts can cite the fallback.
`OBL-OD-1` stays `leftoverDesign: true`; DR-103 stays `OPEN`; Condition 2 unchanged.

**Risk.** If adopted: the surface file 08 line 285 describes — "an unbounded-input surface at metadata-only
admission; oversized-input refusal UNSPECIFIED, not implied" — stays unbounded in the design, and the owner
should see that stated plainly. If numbers were supplied: `$.namedOpenDecisions[0].consequence` already warns
"a fixture author must not assume it".

**Confidence: high** (unchanged; the confidence was never in the withdrawn sentence).

### G3-G18 — on-disk quarantine format — **Codex is right about the route; round 1's "contradiction" framing is withdrawn**

**Codex's refutation, verbatim:** "D-311 does not prohibit a future format choice. lifecycle-leftover-join.v4
proposedLaterWork[2] expressly allows a later implementation successor to choose a mechanism while proving the
recorded properties. Such a successor would implement the recorded route, not contradict D-311."

**Answer: adopted, and the citation is stronger than Codex's own.** Round 1 wrote "*Specifying a format now
would contradict a decision two headings old.* D-311 is the C6-a act; specifying the quarantine format would
overturn it without reviewing it." That is wrong in kind, and D-311's own text is what shows it. Classifying
the seven reserved mechanisms as **implementation encodings** *routes* them to implementation; it does not
forbid the implementation. `## D-311`'s Decision, verbatim: "`$.mechanismReservation.failureRule` remains the
acceptance bar regardless of mechanism: **a later implementation successor that cannot prove P-1..P-8 fails
DR-107, regardless of mechanism choice.**" An entry that names the acceptance bar for a later implementation
successor is contemplating that successor, not prohibiting it.

Codex's cited byte is real and verified: `lifecycle-leftover-join.v4.json` `bcc76ee3…` `$.proposedLaterWork[2]`,
verbatim — "A later implementation successor may choose a journal/lock/lease mechanism. That successor must
still prove the live file 04 properties. This join chooses none." One byte-level refinement, in Codex's favour
and beyond it: `[2]` names **journal/lock/lease** and does not name the quarantine format, so for the
quarantine limb specifically the governing citation is D-311's Decision — which names all seven members
including "the on-disk quarantine format" — rather than `proposedLaterWork[2]`. The route is the same; the
citation must be the one that actually covers the member.

**Adopted round-2 recommendation.** Leave G18 blocked. Specify no quarantine format now, and do **not** permit
quarantine *fate* without quarantine *bytes*. The lawful trigger is a **reviewed later implementation
successor** that chooses the mechanism and proves the recorded properties (D-311's `P-1..P-8` acceptance bar;
`lifecycle-leftover-join.v4` `$.proposedLaterWork[2]`'s "must still prove the live file 04 properties"),
together with the other recorded type dependencies on this gate: the journal type (OQ-G18-1) and DR-111 for the
lock limb (OQ-G18-2, and **Q3**) — `component-manifest-schemas.v11.json` `$.lockSchema.purpose` reads "NO lock
is producible until DR-111 closes", and D-311's own Decision says the lock-file-grammar member "waits on C3(ii)
for any lock-shaped successor".

**The fate-without-bytes half is unchanged and Codex agrees with it.**
`lifecycle-leftover-join.v4.json` `$.proposedLaterWork[1]`, verbatim: "A later leftover-design cycle may author
fixture implementations for the three named corpus classes **only where types are already closed**. This join
does not invent those bytes." The quarantine type is not closed — `OBL-ENCODING-RESERVED`'s own reason records
that contract v2 "reserves the reviewed equivalent of atomic rename and the on-disk quarantine format", and
D-311 left `leftoverDesign` true. And closing `OBL-G18-FX-AUTHORING` needs successors on **both**
`g18-leftover-join.v6.json` `f531ba6a…` and this ROW twin, so the twin's rule governs any closure. G18's own
`$.doesNot` / `$.failsIf` offer no `blocked-on-ride`-style placeholder vocabulary (OQ-G18-3); minting one would
be new semantics.

**The cheap door round 1 named stays on the table**, unchanged and still unmeasured: ask which of the five
live-cell members have closed types and author only those under the twin's own "only where types are already
closed" rule. It is not recommended here because it has not been measured; it is named so the owner knows it
exists.

**What changes if adopted.** Nothing. `OBL-G18-FX-AUTHORING` stays `leftoverDesign: true` on both joins; the
40 G18 cases stay unauthored.

**Risk.** If adopted: G18 stays blocked on two of the owner's *own* open items — the C6 encoding disposition
and Q3's DR-111 windows — so it is not blocked on anything delegable and will not move on its own. If a format
were specified **outside** a reviewed implementation successor: it would bypass the acceptance bar D-311 names,
which is the real defect — not, as round 1 said, a contradiction of the classification itself.

**Confidence: high** (unchanged; the disposition never depended on the withdrawn framing).

### G3-HOSTILE — per-class golden counts — **Codex is right; and the count round 1 left open is now reconciled**

**Codex's refutations, verbatim:** "The live v3 artifact itself records the current unenumerated-class set in
classCoverage, proposedLaterWork, and remainderAfterThisCorpus. The older D1-plan OQ-HG-5 count is not coequal
current evidence after D-300." And: "D-293 already delegates OBL-HOSTILE-GOLDENS authoring under D-000
constraints, so a purely mechanical post-D-300 join remasurement does not need a newly minted owner
authorization."

**Answer: both adopted, and the first one lets round 1's loose end be tied.** Round 1 reported a discrepancy —
D-300's "seven classes carry unenumerated within-class quantifiers" against `D1-plan/OBL-HOSTILE-GOLDENS.md`
OQ-HG-5's six named classes (CC-1, CC-2, CC-4, CC-5, CC-7, CC-9) — and said "this file does not reconcile them,
and a reviewer should re-check both against the bytes." Codex is right that the live artifact is the current
evidence, and the live artifact resolves it. `anti-lockstep-hostile-goldens.v3.json` `8be1b6c5…`
`$.proposedLaterWork[2]`, verbatim: "Within-class universal quantifiers on **CC-1, CC-2, CC-4, CC-5, CC-6,
CC-7, and CC-9** remain unenumerated. A later corpus may add cases only after those members are named in
governing bytes." `$.classCoverage` carries a `remainingNotAuthored` member on exactly those seven and on no
other — CC-3, CC-8, CC-10 and CC-11 carry `authoredGoldenId` alone. **The seventh class is CC-6**
("handshake downgrade and replay"), which OQ-HG-5's enumeration omits while the same plan, at line 506, records
CC-6 as quantifying over the four handshake steps alongside CC-4. There is no discrepancy in the record; there is a
pre-D-300 plan file with an incomplete list, and it is superseded for measurement purposes. Round 1 should have
gone to the artifact instead of reporting the two counts side by side.

On the second refutation: `## D-293` Decision 8 delegates, verbatim, "the enumerated G15, G16, G18, G19, G20,
G21, G24–G30, `OBL-HOSTILE-GOLDENS` and the two DR-122 SARIF fixture obligations, under the agreed semantic,
coverage, dependency and D-000 constraints." `OBL-HOSTILE-GOLDENS` is inside the delegation and is not in the
reserved list. So a post-D-300 `anti-lockstep-leftover-join` remasurement that adds no semantic choice needs a
D-000 cycle, not a fresh owner grant. Round 1's word "authorise" implied an owner act that D-293 has already
performed; withdrawn.

**Adopted round-2 recommendation.** Treat the citation-witness floor as **already authored** at D-300
(`$.summary.authoredMembers` `16`; `$.whatIsAuthored` "Sixteen catalog members … Five join units J-1..J-5 and
eleven class units CC-1..CC-11"; `$.leftoverDesignClosedIfAcceptedAndRecorded` `[]`). Supply **no** per-class
counts. Record an explicit disposition that the seven classes' within-class universals stay named-open,
**citing the live v3 `classCoverage` / `proposedLaterWork[2]` / `remainderAfterThisCorpus` fields rather than
the pre-D-300 plan framing**, and that `OBL-HOSTILE-GOLDENS` therefore stays `leftoverDesign: true` after
D-300. The `anti-lockstep-leftover-join.v3` `820d724a…` remasurement proceeds as **already-delegated mechanical
work** under D-293 Decision 8 through its normal D-000 cycle — it is not owner content, and it must add no
semantic choice. The **cross-row byte-sharing question stays owner work and stays separate**: `OQ-HG-4` /
`$.proposedLaterWork[3]`, verbatim, "Whether golden bytes may be shared with OBL-G21-FX-AUTHORING is not
decided here" — the same eleven CC classes are measured `leftoverDesign: true` under two ids on two rows
(`OBL-HOSTILE-GOLDENS` on DR-127, `OBL-G21-FX-AUTHORING` on DR-G21), the custody prohibitions run both ways
(D-300 "Does not steal G21 leftover remaining on DR-114"; D-301/D-302 "Does not steal leftover-design of
OBL-HOSTILE-GOLDENS remaining on anti-lockstep-leftover-join.v3"), and nothing says whether one authored byte
set may discharge both. That ruling is worth a sentence because it decides whether the CC work is done once or
twice.

**What changes if adopted.** No fixture act. One disposition sentence from the owner; one OQ-HG-4 ruling; and
one `anti-lockstep-leftover-join` successor recorded as delegated work citing D-300. No Condition-2 movement —
D-300's own readiness recital is "Zero SATISFIED. Condition 2 stays 5 of 32."

**Risk.** If adopted: `OBL-HOSTILE-GOLDENS` does not close, and DR-127 stays a "Hard blocker for
independent-release blueprint" (file 08 line 309). If counts were supplied: a minted coverage set that seven
recorded universal quantifiers contradict.

**Confidence: high.**

### G21-SCHEMA — per-type control-frame body schema — **Codex is right; truncated bodies is split out**

**Codex's refutation, verbatim:** "Claude's own rationale concedes that a truncated body never reaches a
per-type parse and is blocked by delivery representation, not by a per-type body schema. Its recommendation
nevertheless groups truncated bodies with the schema-blocked injections."

**Answer: adopted in full.** The refutation is exactly right, and it is right about an internal inconsistency
in round 1 rather than about a byte. Round 1's own paragraph — "*The one the owner could unblock cheapest*" —
said the truncated-body member "is 'a prefix `N` with fewer than `N` body bytes delivered'
(`D1-plan/G21.md` §2 item 29) — the receiver never completes a parse, so no per-type schema is exercised. What
blocks it is not the schema but the fixture-form question." Round 1 then listed truncated bodies first among
the seven to skip **on the schema ground**. The disposition (skip the member) is the same either way, but the
**trigger** is not, and D-293 Decision 6 requires a parking disposition to name a real trigger. A member parked
against the wrong trigger will not be released when the right one fires.

**Adopted round-2 recommendation, in two parts.**

*(i) Six injections stay named-open on the per-type-schema trigger* — `CC-5 invalid UTF-8`,
`CC-5 duplicate members`, `CC-5 unknown members`, `CC-5 floats`, `CC-5 negative integers`,
`CC-5 over-uint53 integers`. Each needs a complete body object, and
`control-protocol-contract.v2.json` `c50a79fe…` `$.controlFrameEncoding.messageEnvelope` requires that body
carry "type (string, closed vocabulary at capabilityEnvelope.messageVocabulary), seq …, controlMajor …,
**body (object; per-type schema)**", while `g21-fixture-corpus.v8.json` `$.whatIsNotAuthored` — carried forward
verbatim into `g21-fixture-corpus.v11.json` `13ede110…` — lists "a ping, pong, hello, helloAck, or other
per-type body schema" as not authored. Trigger: a successor authoring per-type body schemas for the
`capabilityEnvelope.messageVocabulary` types.

*(ii) `CC-5 truncated bodies` stays named-open on the **fixture-form** trigger* — OQ-G21-4, "whether a
postHandshake fixture needs a session script rather than a payload file" and how "a bare payload file
express[es] … a *truncated body*". Its case definition is satisfied without completing a per-type parse, so the
schema successor is not what releases it. Trigger: the OQ-G21-4 fixture-form ruling — **the same ruling
G21-POST needs**, so one ruling moves both. One guard travels with it: if the author includes leading body
bytes carrying a `type`, that token must be **quoted** from `capabilityEnvelope.messageVocabulary`, never
invented — the lineage's own recorded method (`g21-fixture-corpus.v11.json`'s member `mutation`: "16777216 is
quoted, not invented").

**Bookkeeping the split does not change.** The ten entries of
`g21-leftover-join.v13.json` `058717f5…` `$.obligations[3].remainingNotAuthored.remainingCc5Injections` remain
covered without gap or overlap: one entry under **G21-EXACT**, two postHandshake halves under **G21-POST**
(with the far-over entry's preHandshake half authored at D-301/D-302 and its postHandshake half expressly not —
D-302, verbatim: "Does not author the postHandshake far-over half"), one under this item's part (ii), and six
under part (i).

**What changes if adopted.** Nothing authored; seven of the ten CC-5 entries stay named-open, now under two
correctly named triggers instead of one wrong one.

**Risk.** If adopted: CC-5 remains the largest G21 block. If a schema were authored: it is new protocol
semantics minted inside a fixture corpus — `D1-plan/G21.md` §6 names "inventing a vocabulary the record does
not carry" as the second-ranked recorded reviewer-rejection pattern for this gate. If truncated bodies had
stayed filed under the schema trigger: a later schema successor would appear to release it while the fixture-form
question that actually blocks it was still open.

**Confidence: high.**

### G21-NT6 — author NT-6 at G21 — **Codex is right on sequencing; the ruling and the guard are kept**

**Codex's refutation, verbatim:** "Claude's claim that NT-6 is not behind the opening misreads the agreed B2
programme. DECISIONS-RECOMMENDED.md orders fresh review, then the Class A opening, then Option 2's
pre-SATISFIED-GRADE fixture work; the underlying B2 Option 2 likewise says open Class A now and then sequence
NT-6 before the later cycle."

**Answer: adopted.** `DECISIONS-RECOMMENDED.md` §B2's agreed round-2 text opens "Option 3 → Class A opening →
Option 2's pre-SATISFIED-GRADE sequencing", and lists "NT-6 authoring treated as established work" among the
pre-SATISFIED-GRADE bullets — so NT-6 sits inside the package the arrow places **after** the opening. Codex's
own round-2 B2 AGREE reads the same way: "Choose Option 3, **then the Class A opening**, with Option 2's
pre-SATISFIED-GRADE sequencing. **Before the later per-row cycle**, … author NT-6 …". Round 1 read "before the
later per-row cycle" as an upper bound only and inferred a licence to author earlier. That inference is not in
the adopted text, and where the adopted programme states an order, a recommendation should not quietly
reorder it. Sequencing adopted.

**What is kept from round 1, because Codex kept it too.** The substantive ruling stands: `g21-leftover-join.v13.json`
`058717f5…` `$.doesNot[20]` = "Does not author NT-6." is **self-referential** — it disclaims that join's own
act, not a successor corpus — so NT-6 is authorable at G21 as a delegated D1 act. The same join's
`$.obligations[3].remainingNotAuthored.dr133` = `["NT-6"]` measures NT-6 as remaining work, and a join cannot
coherently measure an item as remaining work and forbid anyone from ever doing it. The no-minting guard stands:
the D9 token must be **quoted** from `d9-exit-contract.v1.14.json` `8dd33038…`, never invented
(`$.doesNot[3]`, "Does not invent a D9 code, exit number, or HostTermination"; OQ-G21-13). The
counter-argument recorded at OQ-G21-10 — that `$.doesNot[20]` lacks the "per-D-002-platform copies of …"
qualifier its two structural siblings carry and sits among substantive prohibitions — is real, is why this is a
ruling rather than an assumption, and should be named in the entry rather than glossed.

**Adopted round-2 recommendation.** Rule `$.doesNot[20]` self-referential; NT-6 is authorable as a delegated D1
act on the G21 join (no ROW twin — `D1-plan/README.md` records G21 has none), with its D9 token quoted, not
invented; **sequence that authoring after the owner's DR-133 Class A opening and before the later per-row
cycle**, per the adopted B2 order. The act authors a DR-133 negative test at the G21 gate and does **not**
SATISFY DR-133, exactly as D-301 and D-302 each recite.

**The counter-evidence the owner should have, since it is the reason round 1 went the other way.** The
sequencing adopted here is a **programme-order** choice, not a lawfulness bar, and two measured facts show it:
NT-1 and NT-2 — DR-133 negative tests on this same join — were authored at `g21-fixture-corpus.v1` (D-241, dual
ACCEPT 0/0) and platform-copied at `g21-fixture-corpus.v2` (D-243) with DR-133's Class A opening unwritten then
and unwritten now; and `D1-plan/G21.md` records at **OQ-G21-12** that NT-6 has no byte dependency on the
opening at all — its product law is fully pinned at `provider-only-output-contract.v3.json` `ef2a7416…`
`$.negativeTests["NT-6"]` and its constructibility warrant is `$.negativeTests.wirePin` (`delivery.v2.json`
`47b6cfd17338fafd407c554afe1951ab23d2896aac99bcfd272fc0894e3cabf3`, "Classes are constructible against these v2
bytes"). So if the DR-133 opening stalls, the owner can lift the sequencing with one sentence and no new rule.
Stating that is not a hedge against the adoption; it is the fact that makes the adoption cheap.

**What changes if adopted.** After the DR-133 opening: one corpus plus a `g21-leftover-join` successor. Before
it: nothing. DR-133 is untouched by the authoring act.

**Risk.** If adopted: NT-6 — the last unauthored DR-133 negative test on the G21 join — inherits the DR-133
opening's queue position, which G1-133 puts behind the shared gate-2 entry and a review cycle. If the
self-referential ruling were declined instead: NT-6 has no route at all, and B2's adopted "author NT-6" is left
without one.

**Confidence: medium** on the `$.doesNot[20]` ruling (the OQ-G21-10 counter-argument is genuine and recorded);
**high** on the sequencing, which is now the adopted text's own order rather than an inference.

---

## 2. Knock-on effects on round-1 AGREE items

Both are bookkeeping. Neither changes a recommendation, and every other AGREE item is untouched.

- **Q0** — recommendation unchanged (D-293 reaches the C1–C4 round-2 content it names, at digest
  `44f51a5d…`, bounded; not a general adoption of `DECISION-PACKETS/`). Its **consequence list grows**: round 1
  listed Q4, Q15 and Q3 as the items Q0 makes operative. **Q1 joins them** — Q0-yes is precisely what makes the
  round-2 C1 parenthetical "(the existing preview refusal stands)" the answer to Q1 limb (a). This strengthens
  Q0 rather than qualifying it: the amendment is a worked example of the incorporation Q0 asserts.
- **G1-133** — recommendation unchanged (shared gate-2 entry → fresh application-grade review of v3
  `ef2a7416…` → the opening; NT-6 is **not** opening content). One sentence sharpens: round 1 said NT-6 becomes
  authorable "subject to G21-NT6"; with G21-NT6 adopted as amended, that now reads **after** the opening rather
  than merely not inside it. The minimum-sentence item — that the file-01 preview-role delta disposition and
  NT-6 authoring are later separate acts the opening does not perform — is unchanged and now more precise.

Round 1 §0's remeasurement of the packet (the seven absent headings D-296..D-302, and the three §3 ids they
move) is unaffected by any amendment and stands. Its one loose end, the D-300 class count, is closed at
G3-HOSTILE above.

---

## 3. Summary table — every id, adopted round-2 text

| id | Adopted round-2 recommendation (≤20 words) | Confidence | vs round 1 |
|---|---|---|---|
| G1-117 | Write the opening now citing v10 `8f34c92e…`; no shared gate-2 wait; G29/G30 immediately after | high | unchanged |
| G1-131 | Keep B1's order: shared gate-2 entry, then fresh review of v2 `081ff7fb…`, then opening | high | unchanged |
| G1-133 | Same order against v3 `ef2a7416…`; NT-6 is a separate act **after** the opening | medium | sharpened |
| Q0 | Yes — D-293 reaches round-2 content it names, at digest `44f51a5d…`; bound the reach | high | consequence list grows |
| Q1 | **Preserve the `preview` qualifier**; keep OD-112-3 in `namedOpenDecisions` with DECIDED standing | high | **limb (a) reversed** |
| Q2 | Leave RESERVED; supply no values and record no parking entry now | high | unchanged |
| Q3 | Leave RESERVED as one coherent set; no isolated unit, no partial surfaces | high | unchanged |
| Q4 | Assign the population packet to file 08's cell `Security + release + platform owners` | high | unchanged |
| Q5 | Leave RESERVED until after C4-c makes the TCB grammar governing | high | unchanged |
| Q6 | COORD-only stands; register echo owed at a later MF-6; no eligibility effect | high | unchanged |
| Q7 | Rule no: a scope label alone never satisfies gate 2 while `leftoverDesign` is true | medium | unchanged |
| Q8 | Leave the numeric limb open; later values need an evaluable method on the D-006 pattern | high | **triad withdrawn** |
| Q9 | Successor citation already done (D-312); echo at a later MF-6 on DR-103, not DR-115 | high | unchanged |
| Q10 | Confirm D-304's `specifiedNotLeftover`; the join's own discriminant selects it | high | unchanged |
| Q11 | Dedicated D-000 successor publishing a candidate set, then choosing; name no language here | medium | unchanged |
| Q12 | Route C — PREFERENCE-LADEN, cheap overturn; no recorded rule determines the language | high | unchanged |
| Q13 | Leave RESERVED pending its own DR-101 ceremony successor; do not merge with DR-112 | high | unchanged |
| Q14 | Keep decimal constants forbidden; occupancies quote `MB = 1e6` as D-305..D-308 did | high | unchanged |
| Q15 | Confirm `Product + release engineering` and `Architecture + release`; rule must cover five dimensions | high | unchanged |
| Q16 | Authorise a new evidence packet now; parking behind Condition 5 is circular | medium | unchanged |
| G3-G15 | Leave the adapter reserved; instead rule OQ-G15-1 (fixture bytes vs execution) | high | unchanged |
| G3-G16 | Leave blocked; a current-declaration enumeration is never authoritative per the contract | high | unchanged |
| G3-G18 | Leave blocked; **trigger is a reviewed implementation successor proving P-1..P-8**, plus DR-111 | high | **framing corrected** |
| G3-HOSTILE | Floor authored at D-300; **seven classes incl. CC-6** stay named-open; remasurement is delegated | high | **count reconciled** |
| G3-SARIF-RUNID | Keep parked; §7.1 says no implementer may close that row; trigger is DR-006 | high | unchanged |
| G21-EXACT | Leave named-open, skip; `N = 65536` is not "greater than 65536", so not RF-2 | high | unchanged |
| G21-POST | Leave named-open, skip both; no negotiated `maxControlFrameBytes` and no fixture form | high | unchanged |
| G21-SCHEMA | Leave named-open, skip **six**; truncated bodies splits to the OQ-G21-4 fixture-form trigger | high | **split adopted** |
| G21-NT6 | `$.doesNot[20]` self-referential; NT-6 authorable, D9 quoted, **sequenced after the opening** | medium ruling / high sequencing | **sequencing adopted** |
| G21-FCNC | Leave named-open, skip; FC-NC is owner-reserved at G12 and the apparatus is shared | high | unchanged |

Thirty ids. Twenty-four unchanged from round 1, five amended on Codex's refutations, one (Q0) unchanged in
substance with a widened consequence list.

---

## 4. What this file does not do

It records nothing and is not committed. It edits nothing under `docs/` — neither file 08 nor COORD. It makes
no readiness claim; live readiness as measured in file 08 at this HEAD is a recital only (required-now 28;
Condition 2 five of 32; Condition 5 `NOT MET`). It does not open D-056 Class A for any row, and it does not
SATISFY DR-117, DR-131 or DR-133. It mints no language and does not treat Rust-as-core as decided — Q11's
route is unchanged, names no language, and keeps round 1's flag that the `slice1Adapter` "TypeScript" token at
`harness.DR-G15.packaging-adapter-conformance.v9.json` `d82fac57…` is an **adapter role** that must not be read
across to the core language. It invents no identifier, number, list, verdict or fixture byte; where round 1
did state a rule the record does not carry — Q8's measurement triad — that sentence is withdrawn rather than
defended. Every digest above was recomputed at HEAD `a2d004066d2db7ae89de9ea56979bddb210f0786`.
