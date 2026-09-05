# C2 — DR-118 / thresholds, matrix-corpus, G13: what remains after D-293

Measured at HEAD `f3456575071928022a1f0e3a77e531a87157b365` (last COORD heading `## D-294`).
file 08 `e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e`; COORD
`31746810f9be78f697d66eb94d9cd50a95a51218998f97a154596363039fb9b6`;
`DECISIONS-RECOMMENDED.md` `42f27394746d4aac569a09a01da719c0cf318cf114086635e73097a6add97370`;
`DECISION-PACKETS/C1-4-reserved-numbers-security-quality.md` `59497fe6835c3fb3b84dfe757b63daa22b1b4cbdd103fd2d74026a0e192c376c`.

---

## 1. What D-293 already decided — and why nothing remains **now**

**COORD `## D-293`, Decision item 6 (verbatim, COORD lines 16243–16245):**

> `C2 and C3 as agreed (the C2 matrix/corpus,`
> `threshold-approval and G13 sequence; the C3 live-file-08`
> `remasurement with coherent evaluable windows).`

"As agreed" resolves to two documents D-293's **Subject** pins:

- `DECISIONS-RECOMMENDED.md` `42f27394…` §C1–C4, Claude round 3: `- **C2, C3:** unchanged from round 2.`
- `DECISION-PACKETS/C1-4-reserved-numbers-security-quality.claude-recommendation.r2.md`
  `44f51a5d36eb3f03c711112a50119ea67fb01b3a07d255ccbac5d51cc0485627`
  (listed in `DECISION-PACKETS/MANIFEST.sha256` `ecdbb41d…`), C2 bullet, verbatim:

  > `- **C2 DR-118:** preserve D-007's sequence — no thresholds before a measured denominator; after DR-125 closes or is explicitly disposed, author the digest-pinned matrix and corpus, obtain product approval per threshold cell at matrix acceptance, and name G13 before any SATISFIED cycle. Consequence to state plainly: DR-118 cannot reach SATISFIED before that sequence completes.`

- Codex round 3 (`C1-4-…codex-recommendation.r3.json` `0c2550edd4a0edb5489a03f1a7ee1a2b7be1ef27af564907c36c3367075ae5b4`),
  `recommendation`: `Retain the agreed C2 matrix/corpus, threshold-approval, and G13 sequence …`

**Verdict: no further record act now.** D-293's entry is itself the disposition, and **no artifact carries a
RESERVED/UNDECIDED token that D-293 changes**. Measured, field by field, in §2: every reserving token in the
current join, the current contract and the file-08 row states exactly the standing D-293 adopts —
thresholds UNDECIDED until a measured denominator exists, matrix/corpus unauthored, G13 reserved-not-named.
The C2 decision is a *sequence* for future acts, and the first step of that sequence is blocked on a row
(DR-125) that D-293 does not dispose.

---

## 2. Current artifacts, and the tokens that stay as they are

### 2.1 File 08 row (line 300, reserving fragment verbatim)

> `**DECIDED-V1-NOT-INTEGRATED** — role list DECIDED (D-002: TypeScript, sole slice-1 role) and acceptance STRUCTURE decided (D-007 …); **per-row thresholds remain UNDECIDED** (unlike DR-115) — product approvals at matrix acceptance; the matrix/corpus evidence half discharges at DR-G13/G14 qualification`

Owner cell: `Product + language architecture owners`. Status lead label: `**DECIDED-V1-NOT-INTEGRATED**`
(HANDOFF: `DR-118 remains sole `DECIDED-V1-NOT-INTEGRATED`. Do not flatten to OPEN.`)

Gate row **DR-G13** (line 349): harness cell `reserved, not named (blocked on DR-118; D-086; zero C4 progress) …`;
owner `Product + language owners`; status `OPEN`; threshold/waiver cell
`threshold/parity decision per role; semantic degradation has no silent waiver`.

### 2.2 Current DR-118 leftover-join

`docs/coop/artifacts/language-quality-leftover-join.v5.json` — sha256
`e12101736f9a320a06a3311f405981801fad73c42ba9b7537f506e6c4859bd53`; `$.version` = `5`; `$.date` = `"2026-08-24"`;
`$.status` = `"CANDIDATE-NOT-APPLIED"`; `$.registerRow` = `"DR-118"`;
`$.file08StatusToken` = `"DECIDED-V1-NOT-INTEGRATED"`; `$.head` = `"438b2b820ff6c8c683c56c74006973de186f0e69"`;
`$.file08Pin.sha256` = `e503b75b…` (**live**).
Recording heading: **`## D-273 — Record language-quality leftover-join.v5 as DR-118 leftover remasurement`**
(`ADOPTED 2026-08-24`; Stage A Claude ACCEPT `f1dc8c40…` 0/0, Codex ACCEPT `eae8cdc3…` 0/0;
`New cycle after CONTESTED D-272. Not a fourth turn.`).

`$.summary.leftoverDesign` = `["OBL-THRESHOLDS", "OBL-MATRIX-CORPUS", "OBL-G13-RESERVED"]`.

The three obligation objects that must be remeasured **if and when** the sequence advances, verbatim:

```
$.obligations[3] = {"id": "OBL-THRESHOLDS", "leftoverDesign": true, "existingGate": "none",
 "executionObligationOwnerToday": "none", "rideStanding": "not-capable-of-riding",
 "reason": "D-007 item 7 / D-056 / D-113 / file 08: per-row thresholds remain UNDECIDED. Undecided numbers are leftover-design. Parity-or-improvement is a product approval at matrix acceptance. This join does not invent numbers."}

$.obligations[4] = {"id": "OBL-MATRIX-CORPUS", "leftoverDesign": true, "existingGate": "none as authored implementations",
 "executionObligationOwnerToday": "none", "rideStanding": "not-capable-of-riding as execution-only remainder",
 "reason": "D-007: the matrix and corpus are acceptance evidence authored during qualification. D-113 / file 02: no digest-pinned quality corpus or accepted measurement manifest exists. Authoring remains design work (D-056 Decision 5). This join does not author that corpus. Matrix authoring waits on DR-125 closure or disposition (OBL-DR125-ACTIVATION)."}

$.obligations[5] = {"id": "OBL-G13-RESERVED", "leftoverDesign": true, "existingGate": "DR-G13 reserved, not named",
 "namedIdentifiersNotAuthored": [], "executionObligationOwnerToday": "none", "rideStanding": "not-capable-of-riding",
 "reason": "File 08 / D-086: G13 is reserved, not named, blocked on DR-118. Zero C4 progress. Naming G13 into required-now is a later scoped D-002 successor and a D-086 successor in the same act. This join assigns no number and does not invent a harness specification. Live required-now remains 28 without G13."}
```

The gating obligation, verbatim (`$.obligations[9]`, **not** leftover-design):

```
{"id": "OBL-DR125-ACTIVATION", "leftoverDesign": false, "existingGate": "none on DR-118. Activation gate at DR-125.",
 "executionObligationOwnerToday": "none on this row", "rideStanding": "activation-gate-at-DR-125",
 "reason": "v13 matrixShape.dr125ActivationGate: matrix authoring waits on DR-125 closure or its disposition. D-007 OBS-T2-02 routes the manifest/DR-125 dual boundary to those closure acts. DR-125 is OPEN. sdk leftover-join.v6 (D-267) is the current DR-125 ROW leftover-join; leftoverDesign remains OBL-G20-FX-AUTHORING and OBL-SDK-API-RESERVED. …"}
```

`$.proposedLaterWork` (verbatim) already names each future act:
`"A later D-000 cycle may product-approve per-row thresholds at matrix acceptance. This join invents no numbers."`;
`"A later D-000 cycle may author the digest-pinned matrix and corpus only after DR-125 closes or is disposed. This join does not author those bytes and does not apply D-110."`;
`"A later act that names G13 into required-now is a scoped D-002 successor and a D-086 successor in the same act. This join assigns no number."`

### 2.3 The contract that originates the reservation

`docs/coop/artifacts/language-quality-matrix-contract.v13.json` — sha256
`9efffdb3f7ec806bc967db5eff5868aea0a7d11524b1e026993a46505d35c2ae`; `$.status` = `"CANDIDATE-NOT-APPLIED"`,
`$.binds` = `"NOTHING"`; recorded at **`## D-113`**.
`$.thresholds.standing` = `"UNDECIDED / RESERVED"`;
`$.matrixShape.dr125ActivationGate` = `"OPEN. Owner: DR-125. Divergence owner: the DR-125 successor, not this artifact. Matrix authoring waits on that closure or its disposition."`;
`$.corpusDiscipline.standing` = `"No digest-pinned quality corpus or accepted measurement manifest exists in this V2 snapshot (file 02). This artifact does not author one."`;
`$.g13g14.g13` = `"harness.DR-G13 reserved, not named (blocked on DR-118; D-086). Naming here does not author the harness."`
D-113 Decision: `Numeric thresholds remain UNDECIDED (D-007). The matrix/corpus is not authored. … D-056 Class B remains ineligible while thresholds are UNDECIDED.`

**None of these tokens is contradicted by D-293.** D-293 supplies no threshold number, no matrix row list, no
corpus source and no G13 naming.

---

## 3. Precedent (for the acts that come later, when the sequence unblocks)

- **The remasurement form for this lineage:** `## D-273` (above). Its Decision, verbatim, on the point that
  matters here: `leftover-design of OBL-THRESHOLDS, OBL-MATRIX-CORPUS, and OBL-G13-RESERVED remains on
  leftover-join.v5. … Does not invent per-row numeric thresholds. Does not author the matrix or corpus.
  Does not name G13 into required-now.`
- **What its reviewers attacked, one version earlier**
  (`language-quality-leftover-join.v4.review-independent.claude2.json` — **REJECT**, 0 MUST-FIX / 1 SHOULD-FIX,
  **CLAUDE-LQLJ-V4-SF1**): `"Both findingDisposition entries assert 'ACCEPTED. Landed in this lineage at
  leftover-join.v3.' while declaring landedAt: []. The empty array is false against the subject's own bytes …"`;
  and `language-quality-leftover-join.v4.review-independent.codex.json` — **REJECT**, **CODEX-LQLJ-V4-SF1**:
  `"Both historical repairs are attributed to the wrong landing artifact"`. Neither attacked the substance;
  both cost a REJECT.
- **The G13-naming form, when it comes:** `a scoped D-002 successor and a D-086 successor in the same act`
  (join `$.obligations[5].reason`, verbatim) — the same shape as `## D-147 — Add DR-G23 as required-now
  well-formed admission obligation` and `## D-167 — Add DR-G31 as required-now identity-namespace negative-test
  execution obligation`. That act **changes required-now from 28**, so it is a file-08 register-content act
  with its own cycle, not a leftover remasurement.

---

## 4. Successor diff — none required now

There is no successor to author for C2 at this HEAD. When the sequence advances, the minimal diffs are:

| Trigger | Successor | Which obligation moves |
|---|---|---|
| DR-125 closes or is expressly disposed | `language-quality-leftover-join.v6` | `OBL-DR125-ACTIVATION` reason refreshed; `OBL-MATRIX-CORPUS` **stays** `leftoverDesign: true` (the corpus is still unauthored) |
| Digest-pinned matrix + corpus authored and recorded | `language-quality-matrix-contract.v14` + join successor | `OBL-MATRIX-CORPUS` → `leftoverDesign: false`, by the D-174 pattern (obligation stays in `obligations[]`, moves out of `summary.leftoverDesign`) |
| Product approval of per-row thresholds at matrix acceptance | a `Product + language architecture owners` act | `OBL-THRESHOLDS` → `leftoverDesign: false` |
| G13 named into required-now | scoped D-002 successor **and** D-086 successor in one act | `OBL-G13-RESERVED`; required-now moves off 28 |

**Anything D-293 leaves open must remain an explicit named open decision in any such successor**: the per-row
threshold values, the matrix row vocabulary beyond `$.matrixShape.illustrativeFloor` (which the contract itself
labels `an ILLUSTRATIVE FLOOR, not a closed vocabulary`), and the corpus source. None is in the record; the
record's own reason is quoted at D-007: `no measured denominator exists pre-blueprint`.

---

## 5. Prohibitions

From **D-293**: `This entry marks nothing `SATISFIED`. It does not edit file 08. It does not open D-056 Class A.`

From **D-273** (verbatim): `Does not pin QUALIFIED. Does not invent per-row numeric thresholds. Does not author
the matrix or corpus. Does not steal OBL-SDK-API-RESERVED. Does not name G13 into required-now. Does not
SATISFY DR-118. Does not SATISFY DR-125. … Gate 1 Class A is not opened. Not SATISFIED. Required-now stays 28.
Condition-4 effect is zero. … Does not treat D-272 as adopted. Does not edit file 08. Does not authorize
`docs/v2/implementation/`.`

From **D-113**: `D-056 Class B remains ineligible while thresholds are UNDECIDED.`

From HANDOFF (`b926489d…`): `COORD live remasurement must not flatten DR-118 `DECIDED-V1-NOT-INTEGRATED` to
OPEN`; `Do not steal OBL-THRESHOLDS / OBL-MATRIX-CORPUS / OBL-G13-RESERVED`.

From **D-293 Decision 5**, on the parked A2 headings: **D-272 is CONTESTED and stays parked**; any C2 act must
not treat it as adopted (D-273 is the live recording).

---

## 6. Dependencies and ordering

- **Blocked on DR-125.** `matrixShape.dr125ActivationGate` = `OPEN`; the join routes matrix authoring behind
  `OBL-DR125-ACTIVATION`. DR-125's current ROW leftover-join is `sdk-leftover-join.v6`
  (`e91d6e926830833d563bb89f3693d65328173af6f0d42275ad5339ef73880341`, recorded `## D-267`), whose
  `leftoverDesign` is `["OBL-G20-FX-AUTHORING", "OBL-SDK-API-RESERVED"]`. **D-293 does not dispose DR-125.**
  DECISIONS-NEEDED lists no DR-125 item; `STATUS.2026-08-26.md` §3.C groups DR-125 SDK APIs with the
  "after Condition 5" reservations, which the C5–C9 packet §0 measured as record-backed for DR-125 (via
  `sdk-leftover-join.v6` `proposedLaterWork`: `A later implementation successor after condition 5 may choose an
  SDK language, framework, or API surface. This join chooses none.`).
- **Then blocked on a measured denominator** (D-007's rejected alternative THRESHOLDS-NOW:
  `no measured denominator exists pre-blueprint, and inventing numbers would repeat the class D-006's reviewer
  struck (a threshold whose runner/workload is unnamed measures nothing)`).
- **Independent of C1, C3, C4.** Nothing in C2 waits on them, and nothing waits on C2.

---

## 7. Act shape

**No further act.** Nothing to dispatch at this HEAD.

The next C2-shaped act is a **DR-125 closure or disposition** — an item D-293 does not decide and this plan does
not scope. If the owner wants the C2 sequence started, the first act is that DR-125 disposition, not a DR-118 act.

**Estimated acts for C2 now: 0.**
