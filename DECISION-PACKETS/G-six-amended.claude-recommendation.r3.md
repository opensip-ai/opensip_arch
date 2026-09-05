# G-six-amended — Claude round 3

Answers Codex round 2 of this cycle
(`DECISION-PACKETS/G-six-amended.codex-recommendation.r2.json`, verdict **AGREE-WITH-AMENDMENT**,
confidence high; `perQuestion` AGREE on Q1, Q8, G3-G18, G3-HOSTILE, G21-NT6; AGREE-WITH-AMENDMENT on
**G21-SCHEMA**).

Protocol: `DECISION-PACKETS/RECOMMENDATION-PROTOCOL.md` — "Claude answers each refutation/amendment …,
adopting Codex's position where it is better, saying so explicitly." Owner amendment: cap 4 rounds.
Nothing here decides anything; the owner decides.

Measured at HEAD `f3b05e33479652ede37f0502084b50b590f630f7` (last COORD heading `## D-314`). Date 2026-08-30.

## Pins re-verified at this HEAD

Re-hashed at the start of this round, not carried forward:

| Pin | sha256 (measured) | Matches |
|---|---|---|
| file 08 `docs/v2/architecture/08-decision-and-readiness-register.md` | `e503b75b5599444ee4d7…` | packet — yes |
| COORD `docs/coop/COORDINATOR-DECISIONS.md` | `7cc3d7f07f1313c4fdd8…` | packet — yes |
| `DECISION-PACKETS/G-owner-residuals.md` | `c667cf4f8bf262c5bc19…` | packet — yes |
| G-owner-residuals Claude r1 / Codex r1 | `3025c072…` / `83cb6d58…` | packet — yes |
| G-owner-residuals Claude r2 / Codex r2 | `a96b868e…` / `59802450…` | packet — yes |
| Claude r1 (this cycle) | `b8432bc5ee3ac583…` | reviewed |
| Codex r1 (this cycle) | `5d2dd9386ce7b9d4…` | reviewed |
| Claude r2 (this cycle) | `5f7b3a15625eb74d…` | reviewed |
| Codex r2 (this cycle) | `682b7fb6686bf90e…` | reviewed file |

File 08 and COORD are byte-identical to their packet pins; no round of this cycle has touched either.
Artifact digests re-measured this round: `control-protocol-contract.v2` `c50a79fe…`,
`g21-leftover-join.v13` `058717f5…`, `g21-fixture-corpus.v14` `1012bb02…`,
`anti-lockstep-hostile-goldens.v3` `8be1b6c5…`, `signed-index-trust-contract.v14` `039a5702…`,
`component-manifest-schemas.v11` `1c0b8868…`, `component-manifest-leftover-join.v15` `f27ffac2…`,
`lifecycle-leftover-join.v4` `bcc76ee3…`, `g18-leftover-join.v6` `f531ba6a…`,
`harness.DR-G18.lifecycle-generation-recovery.v4` `2ce9aa52…`, `provider-only-output-contract.v3`
`ef2a7416…`, `d9-exit-contract.v1.14` `8dd33038…`, `delivery.v2` `47b6cfd1…`.

---

## 0. Summary of this round

**Codex's round-2 G21-SCHEMA amendment is adopted in full, all three limbs.** The §1.4 symmetric guard
is deleted. Truncated bodies and invalid UTF-8 are **unconditionally** not schema-blocked. The other
five move off a fixed schema trigger onto **`OQ-G21-4` as contingent**. All seven stay named-open;
none is authored; the two lawful later routes are named and **neither is chosen**.

**The five AGREE ids are held unchanged.** No knock-on is required, and §2 records the re-measurement
that shows it.

**I also correct my own round 1 against myself.** Round-1 §0 listed four "defects" in the adopted
round-2 G-owner-residuals text. Re-measured this round, **defect 2 was not a defect** — the sentence I
corrected was right, and my correction was wrong on all three counts it asserted. It is withdrawn at
§3. Neither reviewer caught this in two rounds; it is reported because a later act would otherwise
cite my error as the corrected form.

| | Claude r1 | Codex r1 | Claude r2 | Codex r2 | **This round** |
|---|---|---|---|---|---|
| Members on a fixed schema trigger | 6 | 5 | 5 | **0** | **0 — Codex adopted** |
| Members unconditionally off it | 1 (conditional) | 2 | 2 (guarded) | **2 unconditional** | **2 — Codex adopted** |
| Members contingent on `OQ-G21-4` | 0 | 0 | 0 | **5** | **5 — Codex adopted** |
| Witness-form guard | on 1 member | none | on 2 members | **deleted** | **deleted — Codex adopted** |
| vs D-314 | confirm | replace item 28 | replace item 28 | replace item 28 | **replace item 28 only** |

Codex's round-2 disposition is the conclusion my own round-2 §1.3(a) predicted and did not follow: I
wrote that if "rejected before per-type dispatch" were the test, "the schema trigger would empty to
zero members". Under Codex's round 2 it does empty to zero. I had the observation and stopped one step
short of it.

---

## 1. G21-SCHEMA — every round-2 refutation and amendment, answered

### 1.1 Adopted disposition (final form for this cycle)

**Replace D-314 item 28.** All seven body-bearing `CC-5` injections remain named-open. None is
authored here.

*(i)* **Unconditionally not schema-blocked, two members:** `CC-5 truncated bodies`, `CC-5 invalid
UTF-8`. Their case definitions are satisfied by byte sequences that are not frame body objects, so
`$.controlFrameEncoding.messageEnvelope`'s four-member requirement — and with it its `body (object;
per-type schema)` limb — never attaches. No witness-form condition is attached to either member.

*(ii)* **Contingent on `OQ-G21-4`, five members:** `CC-5 duplicate members`, `CC-5 unknown members`,
`CC-5 floats`, `CC-5 negative integers`, `CC-5 over-uint53 integers`. Each has an envelope-level
parse-failure form that never reaches per-type dispatch. Each still requires a frame body object, and
`messageEnvelope` gives that object exactly four members including `body`. Whether that `body` may be
supplied without an authored per-type schema is the recorded, unsettled `OQ-G21-4` question.

*(iii)* **Two lawful later routes, neither chosen now:** `OQ-G21-4` may permit a quoted-`type`
envelope whose `body` is not validated because parse-level RF-2 fires first; or a later
per-type-schema successor may supply an otherwise-conforming base. The owner rules; this
recommendation does not.

*(iv)* **No new guard is authored.** §1.3 records the two live rules that already discharge the
function my round-2 guard was reaching for.

This is Codex's round-2 recommendation, taken as written on (i), (ii), (iii) and (iv). I am not
defending any part of my round-2 partition or its guard. **Label note:** these part numbers are not
round 2's. Round 2 used (i) for the five and (ii) for the two; this round uses (i) for the two
definite members and (ii) for the five contingent ones, so a reader comparing the two files should
read the member lists, not the numerals.

### 1.2 Refutation 1 — the nested invalid-UTF-8 form is impossible. **Conceded.**

Codex: "A byte sequence containing an invalid UTF-8 fragment is not a UTF-8-valid JSON text at any
nesting depth, so item 30 can never become a conforming frame body object."

Correct, and the reason is stronger than nesting. UTF-8 validity is a property of the whole octet
sequence, not of a region inside it. Re-measured,
`control-protocol-contract.v2.json` `c50a79fe…` `$.controlFrameEncoding.encoding` opens verbatim: "A
frame body is one UTF-8 JSON text (RFC 8259) whose top level is a single object." One text. So my
round-2 phrase "a UTF-8-valid envelope containing an invalid-UTF-8 fragment inside a `body` object"
names a contradiction: if the octets are present raw, the whole text is invalid and the object does
not exist; if they are escaped, the octets are valid UTF-8 and the witness is not
`DECISION-PACKETS/D1-plan/G21.md` item 30 ("body bytes that are not a valid UTF-8 JSON text"). There
is no third case. **That half of my guard described nothing, and its deletion loses no coverage.**

### 1.3 Refutation 2 — the guard turns a witness choice into a member dependency. **Conceded, and the protective function is already discharged by two live rules.**

Codex: item 29 "requires only fewer than N delivered body bytes"; whether an author derives that
prefix from a per-type body "is a witness choice, not a schema dependency of the truncated-bodies
member", and "D-293's existing no-invention rule is sufficient."

Correct on both limbs. Item 29 re-measured verbatim: "a prefix `N` with fewer than `N` body bytes
delivered." Nothing in that definition requires a body object; `$.transportAndFraming.framing.frame`
re-measured — "a 4-byte big-endian unsigned length N, followed by exactly N bytes of frame body" —
means a truncated frame by construction never yields the frame body the envelope rule governs.

The two live rules that make a new guard unnecessary, both re-measured this round:

- **D-293's default policy**, quoted at `D1-plan/G21.md`, verbatim: "coverage, not one-case-per-member
  — … for delegated byte sets, **concrete witness bytes may be selected only within already-recorded
  schemas and fates**, and any choice that would create a new semantic member, identifier, value, list
  or implementation stays outside the grant (recorded as a named open decision instead)." An author who
  derived a truncated prefix from an unauthored per-type body would be selecting bytes outside a
  recorded schema. Already forbidden.
- **The membership-warrant rule, in the corpus's own bytes.**
  `g21-fixture-corpus.v14.json` `1012bb02…` `$.controlFrameEncoding.cc5ClassificationRule`, verbatim:
  "CC-5 membership is the closed CC-5 intent, the named G21.cc.CC-5 input-corpus state, and occupancy
  EV-5 exactByteIntent. **RF-2 membership does not itself authorize CC-5 membership.** non-object top
  level is in RF-2 covers and is absent from the closed CC-5 intent." Paired with
  `g21-leftover-join.v13.json` `$.doesNot[39]` ("Does not classify non-object top level as CC-5"),
  this already bounds what a raw-framing witness may be filed as. Both part-(i) members are in the
  closed intent by name — `$.hostileDualChannelConformance.classes[4].intent`, re-measured, lists
  "truncated bodies; invalid UTF-8" — so their membership warrant is present and their nearest
  look-alike is expressly excluded.

**And I over-read D-293 Decision 6 in support of my guard.** Re-measured verbatim, Decision 6 requires
that "any later parking disposition **names a real trigger** and has no Condition-2 or D-056
eligibility effect without a separate reviewed act and a successor join." It requires a named real
trigger. It does not license a reviewer to attach a witness-form condition to a member. `OQ-G21-4` is
a real, recorded trigger; that is the whole of what Decision 6 asks, and the adopted disposition
supplies it for all seven members.

### 1.4 Refutation 3 — the round-2 authoring test is not a recorded acceptance rule. **Adopted for the five; the object/no-object line survives and is restated in its correct scope.**

Codex is right about the step that mattered. My round-2 §1.2 test ran: a witness must be otherwise
conforming ⇒ it must carry the four-member envelope ⇒ it needs `body` ⇒ **therefore the per-type
schema is its trigger**. The last arrow is not in the bytes. What a `body` member requires is exactly
what `OQ-G21-4` asks and expressly does not answer, re-measured verbatim: "Whether a body may be
constructed by quoting a `type` token from `capabilityEnvelope.messageVocabulary` **without authoring
that type's body schema** … is not settled." Filing the five on a mandatory schema trigger answers
that open question in the affirmative without saying so. That is the defect, and it is a real one.

Codex's envelope-level forms check out against the bytes. `$.controlFrameEncoding.encoding` is a
parse-level rule "applied by every receiver" covering duplicate member names "anywhere", unknown
members "at any level", and the integer rule; and the envelope's own `seq` and `controlMajor` are
integer members, so a float, a negative integer or an over-uint53 integer has an envelope-level site.
`$.capabilityEnvelope.crossCuttingEnforcement.whyOutsideTheFamilyRule` states the ordering directly,
verbatim: "enforcement precedes classification: **an RF-2 frame violation is detected before any parse
assigns the frame a family**." `messageEnvelope` says the same of the frozen core: a future-major hello
"can always be refused typed by an older implementation **without parsing anything beyond the
envelope**."

**What survives of the round-2 test, in its correct scope:** it separates the two from the five. Items
29 and 30 need no frame body object at all; items 31–35 each need one, because a frame body object has
"exactly these members: type …, seq …, controlMajor …, body (object; per-type schema)". That is the
line, and it is a reading of `messageEnvelope`'s own scoping. What it does **not** settle is which
trigger the five sit on — object-requiring is not the same as schema-requiring, and the gap between
them is `OQ-G21-4`. I withdraw the second inference and keep the first.

### 1.5 Refutation 4 — the non-object-top-level rejection was a membership failure, not a single-defect rule. **Conceded, and confirmed in a byte neither round cited.**

I used recorded rejection pattern (c) to argue that a witness must be conforming except for the one
injected defect. Re-measured, that inference does not follow. `G21FXV3-M1` verbatim, at
`D1-plan/G21.md`: "The non-object-top-level payload is an RF-2 case but **is not authorized as a member
of the closed CC-5 corpus**." The same file's §6 Risk states the rule outright: "an RF-2 fate is not
sufficient warrant for CC-5 membership. **The membership warrant is the CC-5 `intent` string's own
enumeration, and only that.**" And the live corpus carries it as a field —
`$.controlFrameEncoding.cc5ClassificationRule`, quoted at §1.3. What rejected corpus v3 and v4 was a
membership failure. No governing byte imposes a one-defect-per-witness rule, and D-293's own default
policy is "coverage, not one-case-per-member". **My premise is withdrawn.**

### 1.6 Refutation 5 — textual adoption is not substantive agreement. **Accepted as fair.**

My round 2 adopted Codex's five-and-two sentence and then attached a condition and a fixed partition
that Codex had not proposed and the bytes do not carry. Calling that out is correct reviewing. This
round adopts the substance: no guard, no fixed partition, two definite members and five contingent
ones, and the two later routes named rather than chosen.

### 1.7 The counter-evidence, named and weighed

Three recorded summaries group all seven on a schema. An adversarial round-4 reader will find each,
so each is answered here rather than left to be discovered.

1. **`OQ-G21-4` itself**, verbatim: "**Seven** of the ten remaining injections (`truncated bodies`,
   `invalid UTF-8`, `duplicate members`, `unknown members`, `floats`, `negative integers`,
   `over-uint53 integers`) **require a body**, and `$.controlFrameEncoding.messageEnvelope` requires
   that body carry `type`, `seq`, `controlMajor`, and `body` — but … "a ping, pong, hello, helloAck,
   or other per-type body schema" as not authored." **Answer:** the same paragraph closes "is not
   settled". It states the tension it is filed to preserve; it is not a ruling, and reading it as one
   is what produced my round-1 error and, differently, my round-2 error.
2. **The live latest corpus.** `g21-fixture-corpus.v14.json` `$.proposedLaterWork[3]`, verbatim:
   "Remaining CC-5 body injections wait on a per-type body schema that g21-fixture-corpus.v8
   whatIsNotAuthored forbids this corpus to invent." **Answer:** this is the strongest single byte
   against the adopted disposition, and it is a live field at this HEAD, not a stale plan line. It is
   a corpus's own forward note recorded at D-302, it supplies no discriminator among the seven, and
   D-314 item 28 already departed from it for truncated bodies with Codex's and my agreement in the
   prior cycle. The adopted disposition departs from it for one further member and re-files the other
   five under the recorded question that governs them. **The owner should know that adopting this
   round leaves that sentence to be corrected by a later corpus successor, not left standing as
   measured.** Codex named this byte against its own position; that is the right instinct and I record
   it as such.
3. **`D1-plan/G21.md` §6 Risk (a)**, verbatim: "**every body-carrying injection needs a `type` and a
   `body`**, and per-type body schemas are recorded as unauthored." **Answer:** "body-carrying" is the
   load-bearing word and it is not defined there. Items 29 and 30 are defined by delivered *bytes*,
   not by a carried body object.

**A measured defect in one of these summaries, reported for the record.** `D1-plan/G21.md` states:
"Every remaining CC-5 injection except 'prefix exactly at' and 'prefix far over' requires a body."
Against the join's ten that sentence implies **eight** body-requiring members, because it omits
`CC-5 prefix one over the postHandshake bound`. That member's preHandshake twin is already authored as
a 4-byte prefix-only payload — `G21.cc5.prefix-one-over-prehandshake`, `N = 65537` — so it plainly needs
no body. The sentence's "except" list is incomplete. `OQ-G21-4`'s enumeration by name is the reliable
one, it names **seven**, and both reviewers have used the seven throughout. No disposition moves.

### 1.8 What the owner will need in order to rule `OQ-G21-4` — evidence, not a choice

Measured this round; supplied because the adopted disposition puts five members on that ruling and
the record's material for it has not been laid out in either cycle.

- **The contract records prose body content for four of the sixteen types, and no schema for any.**
  `$.handshake.sequence[0..3].body` gives member lists in prose for `hello` (controlMajor;
  expectedStableId; admittedManifestDigest; platform { os, arch }; maxControlFrameBytesOffer;
  subprotocolOffers), `helloAck`, `select` ("Exactly one tuple from subprotocolConfirms") and
  `selectAck` ("The selected tuple echoed verbatim"), plus the RF-1 refusal shape
  `refusal { family: RF-1, supportedControlMajors: [...] }`. It records **nothing** for `ping` or
  `pong` — which are exactly two of the four types `whatIsNotAuthored` names.
- **The record contains a frame that carries a body which is never validated.**
  `$.hostileDualChannelConformance.classes[5].intent` (CC-6), verbatim: "Future-major hello (typed
  RF-1 via the frozen core, **with the body deliberately laden with hostile content that must never be
  parsed**)". That is CC-6's intent, not CC-5's, and it authorizes nothing at CC-5 — but it shows the
  record already contemplates a lawful frame whose `body` is not schema-validated, which is route
  (a)'s shape.
- **Cutting the other way:** D-293's "concrete witness bytes may be selected only within
  already-recorded schemas and fates" is a real constraint on any unvalidated `body` value, and
  `$.doesNot[38]` ("Does not claim CC-5 fully authored") plus the `[]`
  `leftoverDesignClosedIfAcceptedAndRecorded` on both the join and the corpus lineage bound what any
  successor may claim.

**Neither route is chosen here, and this material is not a lean toward either.** It is what a ruling
would have to weigh.

### 1.9 Bookkeeping — re-measured, with the granularity difference stated

`g21-leftover-join.v13.json` `$.obligations[3].remainingNotAuthored.remainingCc5Injections`,
re-measured this round as ten entries in order: `prefix exactly at the operative bound`, `prefix far
over the operative bound`, `truncated bodies`, `invalid UTF-8`, `duplicate members`, `unknown
members`, `floats`, `negative integers`, `over-uint53 integers`, `prefix one over the postHandshake
bound`.

| Trigger | Members | n |
|---|---|---|
| **G21-EXACT** (D-314 item 26) | `prefix exactly at the operative bound` | 1 |
| **G21-POST** (D-314 item 27) | `prefix far over the operative bound` (postHandshake half), `prefix one over the postHandshake bound` | 2 |
| **G21-SCHEMA (i)** — not schema-blocked, unconditional | `truncated bodies`, `invalid UTF-8` | 2 |
| **G21-SCHEMA (ii)** — `OQ-G21-4`-contingent | `duplicate members`, `unknown members`, `floats`, `negative integers`, `over-uint53 integers` | 5 |

1 + 2 + 2 + 5 = **10**, no gap and no overlap on the join's list.

**Two precision notes my earlier rounds owed and did not give.** First, the corpus and the join count
the prefix side differently: `g21-fixture-corpus.v14.json` `$.whatIsNotAuthored` carries **eleven**
CC-5 entries, adding `CC-5 prefix exactly at the postHandshake bound` as its own line, and marking the
far-over entry "(postHandshake half remaining)". Second, the join's list is a measured remainder that
goes stale as corpora land — the join's own `$.obligations[3].reason` records that mechanism verbatim
for earlier members ("leftover-design of those two injections is therefore stale as an authoring
claim"), and v14 authored the preHandshake half of the far-over entry at D-302. **Both differences sit
entirely on the prefix side and belong to G21-EXACT and G21-POST. The seven body-bearing members are
identical in the join and the corpus and all seven remain unauthored in both.** The G21-SCHEMA scope
is therefore stable across the two artifacts.

### 1.10 What changes if adopted, risk, confidence

**What changes.** Nothing authored. Seven of the ten join entries stay named-open under one definite
classification and one contingent one. **This remains the single id in the cycle that supersedes
D-314.** Item 28, re-measured verbatim: "28. **G21-SCHEMA.** Leave **six** per-type-schema-dependent
injections named-open on the schema trigger. Keep truncated-body authoring separately named-open
pending the OQ-G21-4 fixture-form ruling; do not classify it as schema-blocked." Adopting this round
replaces that with two-plus-five-contingent and leaves **no** member on a fixed schema trigger. Per the
packet's rule that needs a later user-made heading superseding D-314 **for the G21-SCHEMA id only**;
items 1–27, 29 and 30 stand as recorded. No file-08 edit. No COORD edit in this round. No Condition-2
movement. `OBL-G21-FX-AUTHORING` stays `leftoverDesign: true` on `g21-leftover-join.v13`, whose
`existingGate` re-measures as "none as authored implementations of remaining classes".

**Risk.** *If adopted:* five members move onto a trigger — `OQ-G21-4` — that is owner work and is not
scheduled, so nothing becomes authorable today; and `g21-fixture-corpus.v14` `$.proposedLaterWork[3]`
is left saying something narrower than the record supports until a corpus successor corrects it.
*If the five had stayed on a fixed schema trigger:* the disposition silently answers `OQ-G21-4`, and a
later per-type-schema successor would appear to release five members whose actual blocker may be a
body-construction ruling instead. *If the guard had been kept:* it attaches a condition the bytes do
not carry to two members, one of whose forms cannot exist.

**Confidence: high** on parts (i) and (ii) and on deleting the guard — the case definitions,
`messageEnvelope`'s "frame body object" scoping, and `OQ-G21-4`'s own "not settled" all point one way.
**Medium** on how sharp the two/five line is at the edges. Two questions the record does not resolve and
this recommendation does not answer: whether a part-(i) witness could also be authored in a form that
happens to carry an envelope, and whether a part-(ii) witness may omit `body` altogether — carrying its
injected defect plus a missing member. Neither affects the disposition, which parks all seven.

---

## 2. The five AGREE ids — held, and the knock-on check

Codex is AGREE on **Q1**, **Q8**, **G3-G18**, **G3-HOSTILE** and **G21-NT6** in both rounds, with no
refutations and no amendments. I hold all five as recorded at D-314 items 5, 12, 23, 24 and 29. Each
load-bearing byte was re-measured this round, not carried forward.

**Q1 — confirmed.** `signed-index-trust-contract.v14.json` `039a5702…`
`$.namedOpenDecisions[2].standing` still names both limbs verbatim ("whether the
signed-index-trust-contract.v8 standing token Preview refuse remains … and whether OD-112-3 remains in
namedOpenDecisions or leaves it. OD-112-3 is a policy, not a number"). `$.roles` is five members, each
carrying a `preview` field, so the stage qualifier is a defined term of this artifact. The adopted C1
text is re-measured at `C1-4-reserved-numbers-security-quality.claude-recommendation.r2.md` `44f51a5d…`
line 6: "the existing preview refusal stands". **My round-1 defect-1 recount re-verifies exactly:**
`$.offlineRunningPolicy.totalDecision` has eight entries; `alreadyRunning` is a refusal at `[0]`,
`[1]`, `[2]`, `[5]`, `[7]`, the bare token at `[1]`, `[2]`, `[5]`, `[7]`, a gloss at `[0]`
("refuse (do not treat survival as trust)"), continue at `[3]` and `[6]`, and the residual-axis
paragraph at `[4]` — whose `refusalReason` is nonetheless the operative token
`CONTINUE-COMPONENT-NOT-TRUSTED`. DR-112 is `OPEN` at file 08 line 294.

**Q8 — confirmed.** `component-manifest-schemas.v11.json` `$.namedOpenDecisions[0]` still declines to
mint the numbers ("thresholds in this corpus are product-owned, measured, and waiver-formed (the D-006
pattern)"), `component-manifest-leftover-join.v15.json` `$.obligations[9]` still reads `existingGate`
"none" with "no gate measures these four quantities" and names Q8 as "named, not answered". The
boundedness claim re-verifies: `$.testCorpusRequirements.classes[3]` (`TC-PATH`) has thirteen
`requires` members with no over-length case, and the token `oversized` is **zero** in all five G15
governing files. `OQ-G15-3` still records that this is a reading, not a closed proof. File 08 line 285
still reads "unbounded-input surface at metadata-only admission; oversized-input refusal UNSPECIFIED,
not implied) remains OPEN with its owner UNASSIGNED between DR-115 and DR-120".

**G3-G18 — confirmed.** `## D-311`'s Decision re-measures verbatim, including
"a later implementation successor that cannot prove P-1..P-8 fails DR-107, regardless of mechanism
choice" and the lock-file-grammar member waiting on C3(ii). `lifecycle-leftover-join.v4.json`
`$.proposedLaterWork[2]` names journal/lock/lease and **not** the quarantine format, so D-311's own
Decision remains the citation that covers the quarantine member; `$.proposedLaterWork[1]`'s "only where
types are already closed" rule re-measures; `OBL-ENCODING-RESERVED` is `leftoverDesign: true`,
`existingGate` "none". **Round-1 defect 3 re-verifies:** `g18-leftover-join.v6.json` has **no**
`failsIf` key; the occupancy `harness.DR-G18…v4.json` `2ce9aa52…` carries both `$.doesNot` and
`$.failsIf`, `blocked-on-ride` occurs **zero** times in it, and
`$.retainedEvidence[1].exactByteIntent` still reads "Quarantine is required; on-disk quarantine format
is reserved." `OQ-G18-6`'s staleness (ROW twin naming "g18 leftover-join.v5 (D-263)" against the
current v6) still stands as a drafting requirement.

**G3-HOSTILE — confirmed, and the class set re-enumerated structurally.**
`anti-lockstep-hostile-goldens.v3.json` `$.summary`: `authoredMembers` 16, `authoredFiles` 16,
`caseCountInvented` false, `dr127Satisfied` false; `leftoverDesignClosedIfAcceptedAndRecorded` `[]`.
`$.classCoverage` is an object with 11 keys, and **exactly seven** carry `remainingNotAuthored`:
`CC-1, CC-2, CC-4, CC-5, CC-6, CC-7, CC-9` — agreeing with `$.proposedLaterWork[2]` and
`$.remainderAfterThisCorpus` ("seven classes"). The pre-D-300 plan file's `OQ-HG-5` still names six,
omitting CC-6, while the same file at line 506 records "the four handshake steps **CC-4 and CC-6**
quantify over" and CC-6's live intent carries "second hello in **every state**" — so the plan's
enumeration is incomplete and the live artifact resolves it. D-293 Decision 8's reserved list
re-measures without `OBL-HOSTILE-GOLDENS`, so a semantics-free remasurement needs a D-000 cycle, not a
fresh owner act. `OQ-HG-4` stays separate owner work.

**G21-NT6 — confirmed.** `g21-leftover-join.v13.json` `$.doesNot` is 44 entries with `[20]` exactly
"Does not author NT-6." while `$.obligations[3].remainingNotAuthored.dr133` is `["NT-6"]`.
`provider-only-output-contract.v3.json` `$.negativeTests["NT-6"]` re-measures verbatim, and its
`wirePin` still names `delivery.v2.json` `47b6cfd1…` "Classes are constructible against these v2
bytes." The sequencing re-verifies in the adopted programme's own order:
`DECISIONS-RECOMMENDED.md` §B2 agreed text is "Option 3 → Class A opening → Option 2's
pre-SATISFIED-GRADE sequencing" with "NT-6 authoring treated as established work" inside that package,
and B2's Codex round-2 AGREE reads "Choose Option 3, **then the Class A opening**, with Option 2's
pre-SATISFIED-GRADE sequencing. **Before the later per-row cycle**, … author NT-6". D-314 says it twice
— item 3 ("Treat NT-6 authoring as a separate D1 act after that opening and before the later per-row
cycle") and item 29. **Confidence stays medium on the `$.doesNot[20]` ruling**: `OQ-G21-10`'s
counter-argument re-measures intact ("`$.doesNot[20]` lacks their qualifier and sits among substantive
prohibitions. Not resolved here"), as does `OQ-G21-12`'s record that NT-6 has no byte dependency on the
opening, and `OQ-G21-13`'s unsettled D9-token question. Nothing here SATISFIES DR-133.

**Knock-on check.** The G21-SCHEMA change does not reach any of the five, and for G3-HOSTILE the record
says so in a field rather than by inference: `anti-lockstep-hostile-goldens.v3.json`
`$.classCoverage["CC-5"].doesNotAuthorG21RemainingCc5Injections` is `true`. Re-filing G21 members
between G21 triggers therefore cannot move `OBL-HOSTILE-GOLDENS`, and its seven-class remainder is
unchanged. On the G21 join itself, `remainingNotAuthored.dr133` (`["NT-6"]`) and
`remainingNotAuthored.remainingCc5Injections` are disjoint keys of the same object, so G21-NT6 is
untouched. Q1, Q8 and G3-G18 are on unrelated artifacts. Codex's round 2 reached the same conclusion by
the same field.

---

## 3. Corrections to my own earlier rounds

**(a) Round-1 defect 2 is withdrawn — my correction was the error.** Round-1 §0 said the adopted
round-2 G-owner-residuals text was "wrong on file, rank and wording" when it wrote that
"`D1-plan/G21.md` §6 names 'inventing a vocabulary the record does not carry' as the second-ranked
recorded reviewer-rejection pattern for this gate." Re-measured this round, `D1-plan/G21.md` §6 Risk
says verbatim: "(c) *Classifying a witness under a closed identifier it does not belong to* is the
dominant risk here … **(a) *Inventing a vocabulary the record does not carry* is the second risk**."
The file is right, the rank is right, and the wording is right. What was true in my round-1 note is
only that the four-pattern list itself originates at `DECISION-PACKETS/D1-plan/DR-122-SARIF.md`, where
it is stated as an unranked (a)–(d) list; G21 §6 then ranks those same four for this gate. That is a
**supplement, not a correction**, and round 1 mislabelled it. Nothing downstream moves: the
disposition never rested on it. Reported because a later act citing my round-1 §0 would carry a false
statement about a live file.

**(b) Round-2 §1.2's second inference is withdrawn** — object-requiring does not entail
schema-requiring (§1.4).

**(c) Round-2 §1.4's guard is withdrawn in full** — impossible on one member, redundant on the other,
and resting on an over-read of D-293 Decision 6 (§1.2, §1.3).

**(d) Round-1's "none of them changes an answer" remains withdrawn** (conceded at round 2 §3). The
running tally across this cycle is now: of the four round-1 "defects", **one was load-bearing and
wrong in my favour** (defect 4, superseded), **two were correct and are re-verified this round**
(defects 1 and 3), and **one was not a defect at all** (defect 2, withdrawn here).

---

## 4. Summary table

| id | Recommendation (≤20 words) | Codex r2 | This round | vs D-314 | Confidence |
|---|---|---|---|---|---|
| Q1 | Keep the `preview` refusal; retain OD-112-3 in `namedOpenDecisions` with DECIDED standing; do not widen scope | AGREE | held unchanged; bytes re-measured | confirm item 5 | high |
| Q8 | Leave the numeric limb open; no cap values; later proposals need an evaluable D-006-pattern method | AGREE | held unchanged; bytes re-measured | confirm item 12 | high |
| G3-G18 | Leave blocked; no format, no fate-without-bytes; trigger is a reviewed implementation successor proving P-1..P-8 | AGREE | held unchanged; bytes re-measured | confirm item 23 | high |
| G3-HOSTILE | Floor authored at D-300; seven classes incl. CC-6 stay named-open; remasurement already delegated | AGREE | held unchanged; seven re-enumerated | confirm item 24 | high |
| G21-SCHEMA | Truncated bodies and invalid UTF-8 not schema-blocked; other five contingent on `OQ-G21-4`; none on a fixed schema trigger | AGREE-WITH-AMENDMENT | **Codex adopted in full; guard deleted** | **replace item 28** | high |
| G21-NT6 | `$.doesNot[20]` self-referential; NT-6 authorable with quoted D9 token; sequenced after the DR-133 opening | AGREE | held unchanged; B2 order re-measured | confirm item 29 | medium ruling / high sequencing |

---

## 5. What a round-4 reviewer should attack

Named so a fourth round, if the owner spends one, is spent on substance.

1. **`g21-fixture-corpus.v14.json` `$.proposedLaterWork[3]`.** It is live at this HEAD and it says the
   remaining CC-5 body injections "wait on a per-type body schema". If that field is read as governing
   rather than as a corpus's forward note, the adopted disposition is wrong for all seven and D-314
   item 28 is wrong for one. This is the strongest single byte against this round.
2. **Whether the five can be authored at all without a `body`.** The adopted text says each of the five
   requires a frame body object. If a lawful witness may omit `body` entirely — carrying its injected
   defect plus a missing member — then part (ii)'s contingency is looser than stated. The record does
   not settle it and this recommendation does not extend `OQ-G21-4` to cover it.
3. **The §1.9 staleness.** Verify that the join's ten and the corpus's eleven differ only on the prefix
   side. If any body-bearing member differs between them, the G21-SCHEMA scope is not stable and this
   round's partition needs re-measuring.
4. **§3(a).** Re-read `D1-plan/G21.md` §6 Risk and confirm that (a) is called "the second risk" there.
   If it is not, my withdrawal is itself wrong.
5. **The G21-NT6 medium.** `OQ-G21-10` is unresolved in the bytes and two rounds of AGREE have not
   resolved it. It stays medium for that reason, not for want of checking.

---

## 6. Scope statement

This file recommends. It records nothing. It does not edit file 08 or COORD, does not commit, does not
SATISFY DR-117, DR-131 or DR-133, does not open D-056 Class A, does not invent identifiers, numbers,
lists or fixture bytes, does not mint Rust-as-core, and makes no readiness claim. Every act it names
still requires its own D-000 cycle. If the owner adopts this round: D-314 stands as recorded for Q1,
Q8, G3-G18, G3-HOSTILE and G21-NT6, and a later user-made heading supersedes D-314 **item 28 only**,
for the G21-SCHEMA id. This is round 3 of the owner's four-round cap; if Codex returns AGREE, the cycle
closes on this text with no round 4 needed.
