# G-six-amended — Claude round 2

Answers Codex round 1 of *this* cycle
(`DECISION-PACKETS/G-six-amended.codex-recommendation.json`, verdict **AGREE-WITH-AMENDMENT**, confidence high,
five `perQuestion` AGREE plus one AGREE-WITH-AMENDMENT on **G21-SCHEMA**).

Protocol: `DECISION-PACKETS/RECOMMENDATION-PROTOCOL.md` — "Claude answers each refutation/amendment …, adopting
Codex's position where it is better, saying so explicitly." Nothing here decides anything; the owner decides.

Measured at HEAD `f3b05e33479652ede37f0502084b50b590f630f7` (last COORD heading `## D-314`). Date 2026-08-29.

## Pins re-verified at this HEAD

Re-hashed at the start of this round, not copied forward:

| Pin | sha256 (measured) | Matches |
|---|---|---|
| file 08 `docs/v2/architecture/08-decision-and-readiness-register.md` | `e503b75b5599444ee4d7…` | packet — yes |
| COORD `docs/coop/COORDINATOR-DECISIONS.md` | `7cc3d7f07f1313c4fdd8…` | packet — yes |
| `DECISION-PACKETS/G-owner-residuals.md` | `c667cf4f8bf262c5bc19…` | packet — yes |
| Claude r1 (this cycle) | `b8432bc5ee3ac58325175…` | reviewed file |
| Codex r1 (this cycle) | `5d2dd9386ce7b9d427a2b…` | reviewed file |

File 08 and COORD are byte-identical to their packet pins; neither was touched by round 1 or by this round.
Contract and corpus digests re-measured this round: `control-protocol-contract.v2` `c50a79fe…`,
`g21-leftover-join.v13` `058717f5…`, `g21-fixture-corpus.v14` `1012bb02…`,
`anti-lockstep-hostile-goldens.v3` `8be1b6c5…`.

---

## 0. Summary of this round

**Codex's G21-SCHEMA amendment is adopted.** My round-1 six-and-one split was wrong on one member. The
disposition becomes **five-and-two**: five injections stay on the per-type-schema trigger; **`CC-5 invalid
UTF-8` joins `CC-5 truncated bodies` on the `OQ-G21-4` fixture-form/raw-body trigger and is not
schema-blocked.**

**Codex refutation 3 is conceded in full.** My round-1 §0 asserted that none of its corrections changes an
answer. That is false. The invalid-UTF-8 move is a disposition change, and it is the one thing in this cycle
that **replaces** rather than confirms the D-314 text — for the G21-SCHEMA id only.

**The other five ids are held unchanged**, and this round adds the byte that shows the amendment does not reach
them (§2).

Two parts of Codex's *rationale* do not carry the weight put on them, and I say so while adopting the
conclusion (§1.3). The amendment is right; two of its three supports are not the ones that decide it. The
support that does decide it is a case definition neither round cited: `D1-plan/G21.md` item **30**.

| | Round 1 (mine) | Codex r1 | This round |
|---|---|---|---|
| Schema-trigger members | 6 | 5 | **5 — Codex adopted** |
| `OQ-G21-4` fixture-form members | 1 (truncated bodies) | 2 (+ invalid UTF-8) | **2 — Codex adopted** |
| Guard on the fixture-form members | condition on truncated bodies only | none stated | **symmetric, both members (§1.4)** |
| vs D-314 | confirm | replace item 28 | **replace item 28; confirm items 1–27, 29, 30** |

---

## 1. G21-SCHEMA — the amendment, answered

### 1.1 Adopted

**Recommendation — replace D-314 item 28.**

*(i)* **Five** injections stay named-open on the **per-type-schema** trigger: `CC-5 duplicate members`,
`CC-5 unknown members`, `CC-5 floats`, `CC-5 negative integers`, `CC-5 over-uint53 integers`.

*(ii)* **Two** injections stay named-open on the **`OQ-G21-4` fixture-form/raw-body** trigger and are **not**
classified as schema-blocked: `CC-5 truncated bodies` and `CC-5 invalid UTF-8`.

*(iii)* The guard at §1.4 travels with part (ii).

This is Codex's amendment, taken as written on (i) and (ii). I am not defending my round-1 partition.

### 1.2 The byte that decides it

Codex argued the point from the *ordering* of decode versus dispatch. The record settles it more directly, in
the case definition of the member itself. `DECISION-PACKETS/D1-plan/G21.md`, Axis E, item **30**, verbatim:

> 30. `"CC-5 invalid UTF-8"` — body bytes that are not a valid UTF-8 JSON text
>     (`#$.controlFrameEncoding.encoding`: "A frame body is one UTF-8 JSON text (RFC 8259)").

The witness *is defined as* bytes that are not a valid UTF-8 JSON text. Set that against
`control-protocol-contract.v2.json` `c50a79fe…` `$.controlFrameEncoding.messageEnvelope`, re-measured verbatim:

> "Every frame body **object** has exactly these members: type (string, closed vocabulary at
> capabilityEnvelope.messageVocabulary), seq (integer, per framing.sequencing), controlMajor (integer; fixed at
> the negotiated major after hello), **body (object; per-type schema)**."

`messageEnvelope` governs *frame body objects*. A byte sequence that is not a valid UTF-8 JSON text is not an
object, so the four-member requirement — and with it the `body (object; per-type schema)` dependency — never
attaches to an item-30 witness. The same holds for item **29**, verbatim: "`"CC-5 truncated bodies"` — a prefix
`N` with fewer than `N` body bytes delivered." An undelivered body is not an object either.

Neither member is a marginal reading of CC-5. Both are named in the class intent itself —
`$.hostileDualChannelConformance.classes[4].intent`, re-measured verbatim: "Length prefix 0; prefix exactly at,
one over, and far over the operative bound (pre- and post-handshake bounds separately); **truncated bodies;
invalid UTF-8**; duplicate members; unknown members; floats, negative and over-uint53 integers. Each is RF-2
typed…". So moving invalid UTF-8 off the schema trigger does not repeat the inference that got
`g21-fixture-corpus.v3` and `.v4` rejected on `G21FXV3-M1` / `G21FXV4-M1` — that rejection was for filing a
**non-object-top-level RF-2 payload** as a CC-5 member, and invalid UTF-8 is a CC-5 member by name in the class
intent. Codex's third `perQuestion` refutation makes this point and it is correct.

**Why the five stay.** Items 31–35 each describe a defect *inside a parsed JSON document* — re-measured:
`"duplicate members"` ("duplicate member names anywhere reject the frame (RF-2)"), `"unknown members"`
("unknown members at any level reject (RF-2)"), `"floats"` ("any other numeric form is RF-2"),
`"negative integers"` ("(uint53, non-negative)"), `"over-uint53 integers"` ("exact magnitude at most
9007199254740991"). A witness for any of these must be a frame that is conforming **except** for the injected
defect; otherwise it carries two defects at once and is filed under an identifier it does not cleanly belong
to — recorded rejection pattern **(c)**, "classifying a witness under a closed identifier it does not belong
to", which is the pattern that actually rejected four G21 corpus versions. And a frame that is conforming
except for the injected defect must, per `messageEnvelope`'s "exactly these members", carry `body` — whose
per-type schema `g21-fixture-corpus.v14.json` `1012bb02…` `$.whatIsNotAuthored` records as not authored ("a
ping, pong, hello, helloAck, or **other per-type body schema**"). That is the dependency, and it bites on all
five.

**So the working discriminator is not where the rejection happens. It is whether authoring the witness requires
constructing a conforming frame body object.** Items 31–35: yes. Items 29 and 30: no.

### 1.3 Where Codex's rationale needs tightening — adopting the conclusion, not two of its supports

Two supports in the Codex entry do not discriminate, and an adversarial round 3 would say so. Naming them now
is cheaper than defending them later.

**(a) "Rejected before per-type dispatch" proves too much.** Codex's stated ground is that invalid UTF-8 "fails
before that object and its type/per-type body schema can exist". True of invalid UTF-8 — but as a general test
it moves Codex's own five as well. `$.controlFrameEncoding.encoding`, re-measured verbatim, is a **parse-level**
rule "applied by every receiver":

> "A frame body is one UTF-8 JSON text (RFC 8259) whose top level is a single object. **Parse-level strictness,
> applied by every receiver:** duplicate member names anywhere reject the frame (RF-2); a non-object top level
> rejects; unknown members at any level reject (RF-2) - there is no ignorable-extension mechanism in major 1, so
> nothing can be smuggled through tolerated members; numbers are permitted only as integers with exact magnitude
> at most 9007199254740991 (uint53, non-negative), so every conforming parser holds every permitted value
> exactly and no float admission hazard exists; any other numeric form is RF-2."

Duplicate members, unknown members, floats, negative integers and over-uint53 integers are **all** rejected at
parse level, before any per-type dispatch, by that field's own words. If "rejected before dispatch" were the
test, the schema trigger would empty to zero members — which is not what Codex recommends and not what the
record supports. The authoring test at §1.2 is the one that survives, and it delivers Codex's split exactly.

**(b) RF-2 membership discriminates nothing.** Codex cites
`$.capabilityEnvelope.refusalFamilies.families[1].covers` as naming invalid UTF-8 "independently". Re-measured
verbatim, that field is:

> "length prefix of 0, oversize against the operative bound, truncated body, invalid UTF-8, non-object top
> level, duplicate members, unknown members, non-integer or out-of-range numerics."

One family covers **all ten** remaining injections, naming duplicate members and unknown members exactly as
directly as invalid UTF-8. As a defensive point — invalid UTF-8 is a first-class named violation, not an
inference — it holds. As an affirmative discriminator between the five and the two, it does no work. I adopt
the conclusion without this support.

### 1.4 The strongest counter-evidence, and the guard it requires

The best argument *against* the amendment is `OQ-G21-4` itself, re-measured verbatim:

> "**Seven** of the ten remaining injections (`truncated bodies`, `invalid UTF-8`, `duplicate members`,
> `unknown members`, `floats`, `negative integers`, `over-uint53 integers`) **require a body**, and
> `$.controlFrameEncoding.messageEnvelope` requires that body carry `type`, `seq`, `controlMajor`, and `body` —
> but `g21-fixture-corpus.v8.json#$.whatIsNotAuthored` records "a ping, pong, hello, helloAck, or other per-type
> body schema" as not authored."

`D1-plan/G21.md` semantic-choice **(a)** item 2 groups the same seven, with the caveat "a body needs a `type`
from `capabilityEnvelope.messageVocabulary` and a per-type `body` schema".

**The answer is that the conjunction is unsound for items 29 and 30, and `OQ-G21-4` does not claim otherwise.**
All seven do "require a body" in the sense that distinguishes them from the two authored 4-byte prefix-only
payloads: bytes must follow the prefix. But the second clause — `messageEnvelope` requiring `type`, `seq`,
`controlMajor`, `body` — is scoped by that field to a frame body **object**, and items 29 and 30 define
witnesses that are not objects. `OQ-G21-4` closes "is not settled", so it poses this question rather than
answering it; reading it as an answer is what produced my round-1 error.

**But item 30 admits a second witness form, and that is where the guard is needed.** "Body bytes that are not a
valid UTF-8 JSON text" is also satisfied by a UTF-8-valid envelope containing an invalid-UTF-8 fragment inside
a `body` object — and constructing that requires the unauthored per-type schema. The identical hazard exists at
item 29: a truncated witness whose delivered prefix is drawn from an authored per-type body. My round-1
condition saw this for truncated bodies only. It belongs on both members, symmetrically:

> **Guard on part (ii).** Each witness must be authorable **without constructing a conforming frame body
> object** — for `truncated bodies`, delivered bytes not drawn from a per-type `body`; for `invalid UTF-8`, a
> byte sequence that is not a valid UTF-8 JSON text at the top level rather than an invalid fragment nested
> inside one. If an author elects either object-requiring form, that member re-acquires the schema dependency
> and **both** triggers apply to it.

This is the improvement the amendment needs and did not carry: Codex stated the move unconditionally, and
unconditionally it licenses exactly the object-requiring form that would smuggle the schema dependency back in.
Stated with the guard, the parking disposition is evaluable, which is what D-293 Decision 6 requires of one.

**One consequence worth recording.** In their minimal, guard-compliant form neither part-(ii) witness needs a
`type` token at all. So the invention hazard `OQ-G21-4` names — "whether a body may be constructed by quoting a
`type` token from `capabilityEnvelope.messageVocabulary` without authoring that type's body schema" — **does not
arise** for these two. It continues to bite on all five part-(i) members. The amendment therefore narrows the
open question as well as re-filing two members.

### 1.5 Revised bookkeeping — still exact, no gap and no overlap

`g21-leftover-join.v13.json` `058717f5…` `$.obligations[3].remainingNotAuthored.remainingCc5Injections`,
re-measured this round as **ten** entries in order: `prefix exactly at the operative bound`, `prefix far over
the operative bound`, `truncated bodies`, `invalid UTF-8`, `duplicate members`, `unknown members`, `floats`,
`negative integers`, `over-uint53 integers`, `prefix one over the postHandshake bound`.

| Trigger | Members | n |
|---|---|---|
| **G21-EXACT** (D-314 item 26) | `prefix exactly at the operative bound` | 1 |
| **G21-POST** (D-314 item 27) | `prefix far over the operative bound` (postHandshake half), `prefix one over the postHandshake bound` | 2 |
| **G21-SCHEMA (ii)** — `OQ-G21-4` fixture-form/raw-body | `truncated bodies`, `invalid UTF-8` | 2 |
| **G21-SCHEMA (i)** — per-type schema | `duplicate members`, `unknown members`, `floats`, `negative integers`, `over-uint53 integers` | 5 |

1 + 2 + 2 + 5 = **10**. My round 1 recorded 1 + 2 + 1 + 6 = 10 on the same ten entries; the amendment moves one
member between the third and fourth rows and the partition stays exact.

`OQ-G21-4` still moves part (ii) and G21-POST together, since it asks in one question "whether a postHandshake
fixture needs a session script rather than a payload file" — so the ruling that unblocks the two part-(ii)
members is the same ruling G21-POST waits on. That is unchanged by the amendment and is an argument for taking
`OQ-G21-4` as one piece of owner work rather than three.

### 1.6 What changes if adopted

Nothing authored. Seven of the ten CC-5 entries stay named-open, re-filed under two correctly named triggers,
with the guard at §1.4 attached to part (ii).

**This is the one item in the cycle that supersedes D-314.** `## D-314` item 28, re-measured verbatim:

> "28. **G21-SCHEMA.** Leave **six** per-type-schema-dependent injections named-open on the schema trigger. Keep
> truncated-body authoring separately named-open pending the OQ-G21-4 fixture-form ruling; do not classify it as
> schema-blocked."

Adopting this round replaces "six" with "five" and extends the "do not classify it as schema-blocked" treatment
— already D-314's own language for truncated bodies — to invalid UTF-8. Per the packet's rule, that requires a
**later user-made heading superseding D-314 for the G21-SCHEMA id only**; D-314 items 1–27, 29 and 30 stand as
recorded. No file-08 edit. No COORD edit in this round. No Condition-2 movement. `OBL-G21-FX-AUTHORING` stays
`leftoverDesign: true` on `g21-leftover-join.v13`.

### 1.7 Risk and confidence

*If adopted:* two members are re-filed onto a trigger — `OQ-G21-4` — that is owner work and is not scheduled, so
they do not become authorable today; the gain is that a later per-type-schema successor will not appear to
release two members whose actual blocker is a fixture-form ruling.
*If the guard were omitted:* an author could deliver an object-requiring witness under part (ii) and reintroduce
the schema dependency by a side door — the same shape of error as my round-1 unconditional split, inverted.
*If the amendment were declined:* the six-member framing is refutable on item 30's own definition, and a
per-type schema successor would over-claim.

**Confidence: high** on the five-and-two split, which rests on the case definitions and on `messageEnvelope`'s
own "frame body object" scoping. **High** on the guard. **Medium** on whether `OQ-G21-4` should be answered as
one ruling covering part (ii) and G21-POST together — that is a sequencing observation, not a byte finding, and
the owner may prefer to keep them separate.

---

## 2. The five AGREE ids — held, and the knock-on check that shows they are untouched

Codex is AGREE on **Q1**, **Q8**, **G3-G18**, **G3-HOSTILE** and **G21-NT6**, with no refutations and no
amendments on any of them. I hold all five exactly as written in round 1 and as recorded at D-314 items 5, 12,
the G3-G18 item, the G3-HOSTILE item, and item 29. The round-1 citation corrections stand; Codex re-checked and
confirmed them, and none is load-bearing.

The one thing this round owed the owner is a check that the G21-SCHEMA change does not propagate. It does not,
and for **G3-HOSTILE** the record says so in a field rather than by inference. `anti-lockstep-hostile-goldens.v3`
`8be1b6c5…` `$.classCoverage` is an **object keyed by class id** (11 keys; my round 1 enumerated it structurally
but did not say it was an object — recording that now so a re-checker looks in the right shape). Its `CC-5`
entry, re-measured in full:

```
"CC-5": { "authoredGoldenId": "HG.CC-5",
          "remainingNotAuthored": "within-class universal quantifier is named and not enumerated;
                                   this witness does not exhaust the class",
          "doesNotAuthorG21RemainingCc5Injections": true }
```

That last member is an explicit custody boundary: the hostile-goldens artifact records that it does **not**
author the G21 remaining CC-5 injections. So re-filing two of those ten between G21 triggers cannot move
`OBL-HOSTILE-GOLDENS`. The seven classes carrying `remainingNotAuthored` re-measure as **CC-1, CC-2, CC-4,
CC-5, CC-6, CC-7, CC-9** — unchanged, CC-6 included, agreeing with `$.proposedLaterWork[2]`. `OQ-HG-4`
(whether golden bytes may be shared with `OBL-G21-FX-AUTHORING`) remains separate owner work; the amendment
neither answers it nor changes its shape, since it concerns byte sharing across rows and not which trigger a
G21 member sits on.

The other four are on unrelated axes and no knock-on arises: **Q1** is `signed-index-trust-contract`
OD-112-3 wording; **Q8** is `component-manifest` OD-1 cap values; **G3-G18** is the lifecycle quarantine
format; **G21-NT6** is the DR-133 axis, `$.obligations[3].remainingNotAuthored.dr133` = `["NT-6"]`, disjoint
from `remainingCc5Injections` in the same object. My round-1 confidence marks are unchanged, including
**medium** on the `$.doesNot[20]` self-referential ruling — the `OQ-G21-10` counter-argument is still recorded
and still unresolved in the bytes, and Codex's AGREE expressly preserves that.

---

## 3. Correction to my round 1

Round-1 §0 stated that all four defects it found were non-load-bearing and that "none of them changes an
answer", and §8 item 5 invited exactly this challenge. Codex found the case where it fails. The G21-SCHEMA
entry in the round-1 defect table is withdrawn: defect 4 was not "a condition to be made explicit" on a correct
six-member split — the six-member split was itself wrong, and the correct disposition is five-and-two. The
round-1 §0 summary line "**All six D-314 dispositions are confirmed. None is changed**" is superseded by this
round: **five confirmed, one changed.**

---

## 4. Summary table

| id | Recommendation (≤20 words) | Codex r1 | This round | vs D-314 | Confidence |
|---|---|---|---|---|---|
| Q1 | Keep the `preview` refusal; retain OD-112-3 in `namedOpenDecisions` with DECIDED standing; do not widen scope | AGREE | held unchanged | confirm | high |
| Q8 | Leave the numeric limb open; no cap values; later proposals need an evaluable D-006-pattern method | AGREE | held unchanged | confirm | high |
| G3-G18 | Leave blocked; no format, no fate-without-bytes; trigger is a reviewed implementation successor proving P-1..P-8 | AGREE | held unchanged | confirm | high |
| G3-HOSTILE | Floor authored at D-300; seven classes incl. CC-6 stay named-open; remasurement already delegated | AGREE | held; CC-5 custody boundary added | confirm | high |
| G21-SCHEMA | Five on the schema trigger; truncated bodies and invalid UTF-8 on `OQ-G21-4`, not schema-blocked | AGREE-WITH-AMENDMENT | **Codex adopted**, plus symmetric guard | **replace item 28** | high |
| G21-NT6 | `$.doesNot[20]` self-referential; NT-6 authorable with quoted D9 token; sequenced after the DR-133 opening | AGREE | held unchanged | confirm | medium ruling / high sequencing |

---

## 5. What a round-3 reviewer should attack

1. **The §1.2 authoring test.** Is "requires constructing a conforming frame body object" the right
   discriminator, or does the record support a different one that splits the ten differently? If a different
   test puts `duplicate members` on the raw-body side — a duplicate at envelope level rather than inside
   `body` — the split is four-and-three, not five-and-two, and that would be a further change.
2. **The §1.4 guard.** Is the nested-fragment form of item 30 actually admissible as a CC-5 `invalid UTF-8`
   member, or does the record foreclose it? If foreclosed, the guard is unnecessary on that member (it stays
   necessary on item 29).
3. **§1.3(a).** Verify that `$.controlFrameEncoding.encoding` really does place all five part-(i) defects at
   parse level. If it does not, Codex's ordering ground is stronger than I allow and §1.3(a) should be dropped.
4. **The §2 custody boundary.** `doesNotAuthorG21RemainingCc5Injections` — confirm it means what I read it to
   mean, since it is the whole basis for saying G3-HOSTILE is untouched.

---

## 6. Scope statement

This file recommends. It records nothing. It does not edit file 08 or COORD, does not commit, does not SATISFY
DR-117, DR-131 or DR-133, does not open D-056 Class A, does not invent identifiers, numbers, lists or fixture
bytes, does not mint Rust-as-core, and makes no readiness claim. Every act it names still requires its own
D-000 cycle. If the owner adopts this round: D-314 stands as recorded for Q1, Q8, G3-G18, G3-HOSTILE and
G21-NT6, and a later user-made heading supersedes D-314 **item 28 only**, for the G21-SCHEMA id.
