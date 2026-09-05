# Blocked on the owner — collected overnight 2026-09-01/02

> **Historical handoff, superseded for current work.** D-367 delegated the remaining design decisions; D-368 replaced the review/recording workflow; D-369 completed the preview design under independent review. The owner-blocking and dual-review instructions below describe their dates. Use [file 08](docs/v2/architecture/08-decision-and-readiness-register.md) and the [accepted reference architecture](docs/coop/completion/reference-architecture.v2.md) for current scope, decisions and next steps.

> **Corrected 2026-09-02 after D-365.** Item 7 as first written was wrong.
> DR-106, DR-108, DR-109, DR-110, DR-113 and DR-116 are **already on D-002's
> deferral limb** and were never on the critical path. Condition 2's
> SATISFIED-requiring set is D-002's affected-row set as amended by D-134 —
> **23 rows, of which 6 are SATISFIED and 17 remain** — not 27 of 32.

Each item below stopped because it needs a decision only you can make. Nothing here
is waiting on orchestrator effort. Ordered by how much they unblock.

---

## 1. The eighteen reserved values — the condition-2 ceiling

**Blocks:** DR-101, DR-103, DR-107, DR-111, DR-112, DR-118, DR-120, DR-121,
DR-124, DR-125, DR-126 — **eleven of the 17 rows condition 2 still needs**.

Each carries at least one obligation measured `leftoverDesign: true` whose own reason
reads *"undecided numbers/values are leftover-design (D-056)"*. In D-314 and D-315 you
adopted the reviewers' agreed recommendation on each, and in eleven cases that
recommendation was **leave it RESERVED**.

| Row | Reserved obligation | D-314/315 item |
|---|---|---|
| DR-111 | `OBL-NUMERIC-WINDOWS` — reader-support windows | Q3 |
| DR-126 | `OBL-RESERVED-TABLES` — per-OS selectors/profiles | Q5 |
| DR-101 | `OBL-D1` core language, `OBL-D2` signing ceremony | Q11–Q13 |
| DR-112 | `OBL-RESERVED-NUMBERS` — OD-112-1/2/4 | Q2 |
| DR-103 | `OBL-OD-1` — manifest caps | Q8 |
| DR-120 | `OBL-ADAPTER-IMPL` | G3-G15 |
| DR-121 | `OBL-CI-ENCODING-RESERVED` | — |
| DR-107 | `OBL-ENCODING-RESERVED` — quarantine format | G3-G18 |
| DR-125 | `OBL-SDK-API-RESERVED` | — |
| DR-118 | `OBL-THRESHOLDS`, `OBL-MATRIX-CORPUS`, `OBL-G13-RESERVED` | — |
| DR-124 | `OBL-GRANT-JOURNAL`, `OBL-INHERIT-BLOCKED`, `OBL-MONOTONIC` | C12 |

**The ask:** not "does the record compel a value" — it doesn't, which is why "reserve
it" won every round. The ask is **which of these you are willing to decide now,
accepting that a decided value can later be superseded**, versus which genuinely must
wait. Each one you supply converts a permanently-blocked row into a grindable one.

---

## 2. §7.1 RunId park — one ruling, one row

**Blocks:** DR-122, which is otherwise one obligation from closing.

`sarif-leftover-join.v14` `OBL-FC-OUTFAIL-FX`: the case
`FC-OUTFAIL.committed-run-preserved` "stays NOT-AUTHORED under the section 7.1 RunId
park." Its sibling `FC-OUTFAIL.no-committed-run` is authored and remasured (D-297,
D-346).

**The ask:** rule the §7.1 RunId park, or authorise authoring the case under a stated
assumption. This is the cheapest single unblock on the board.

---

## 3. Class A openings for DR-131 and DR-133

**Blocks:** two of the three rows file 12 §1 names as the architecture-completion goal,
plus five gate corpora (G24–G28) and DR-133's NT-6 authoring.

Both have accepted design-contract candidates recorded (D-138
`preview-analyze-contract.v2`; D-136 `provider-only-output-contract.v3`) but are "not
eligible in kind today" (D-133). D-314 items 2 and 3 record your agreed sequence:
shared gate-2 entry → fresh application-grade review of the exact final contract bytes
→ **owner-controlled opening**.

The D1 plan marks G24–G28 "sequencing only — DR-131 Class A opening", and D-315
G21-NT6 sequences NT-6 authoring after the DR-133 opening. So nothing in either
programme can proceed until the openings land.

**The ask:** the two openings, in the D-316 form. The gate-2 entry and the fresh review
are mine and I will run them once the sequence can start.

---

## 4. OQ-G21-4 — five G21 injections

**Blocks:** `OBL-G21-FX-AUTHORING`, which is the last open obligation on DR-G21.

D-315 G21-SCHEMA left all seven body-bearing CC-5 injections named-open. Two —
truncated bodies and invalid UTF-8 — were ruled unconditionally not schema-blocked and
have since been authored (D-352, D-356). The remaining five (duplicate members, unknown
members, floats, negative integers, over-uint53 integers) are **contingent on
OQ-G21-4**, and D-315 says to "choose neither route and author no bytes here."

**The ask:** rule OQ-G21-4 — either a quoted-type envelope whose body is not validated
because parse-level RF-2 fires first, or a later per-type-schema successor.

---

## 5. OBL-HOSTILE-GOLDENS per-class totals

**Blocks:** `OBL-HOSTILE-GOLDENS` on DR-127.

D-315 G3-HOSTILE: treat the citation-witness floor as authored at D-300, "leave the
seven live v3 within-class universal sets including CC-6 named-open, and supply no
per-class totals." The obligation therefore cannot close by authoring. The same item
records that "the cross-row byte-sharing question remains separate owner work."

**The ask:** either supply per-class totals, or rule that the witness floor discharges
the obligation.

---

## 6. D-032 STILL-ROUTED blockers

**Blocks:** DR-105 and DR-114 — ten obligations between them.

`OBL-BLK-1` through `OBL-BLK-4` and `OBL-FC-C1` sit on both rows' leftover-joins as
D-032 legacy routing that no entry has adjudicated: CA-2 execute-anything, four
tokenless CA-3 effects, host outcome vocabulary versus `doctor-contract.v4`
`effectOutcome`, the grant journal, and the joint-owner FC-C1 recording.

**The ask:** these may be partly mine to propose. I can build a byte-cited packet with a
recommendation per blocker if you want; flagging it because D-032's dispositions are
owner recordings and the routing choice looks preference-laden.

---

## 7. Six deferral-limb rows carry no in-cell disposition — optional hygiene

**Blocks:** nothing. These six are **not** condition-2 work.

DR-106, DR-108, DR-109, DR-110, DR-113 and DR-116 sit on D-002's deferral limb: no
credential-requiring features in slice 1 (DR-108), install is a fresh signed download
(DR-110), no third-party support policy needed yet (DR-116), and DR-106, DR-109 and
DR-113 "each deferred WHOLLY". D-365 records this.

The only loose thread is bookkeeping: their file-08 cells read bare `OPEN` or
`OPEN / inherits hard blockers`, while D-002 requires each deferral to get "its recorded
disposition, never silence". Recording those six in-cell is a separate MF-6 with its own
artifact and commit.

**The ask:** none required. Say the word if you want the in-cell dispositions recorded as
a hygiene act; it needs nothing from you and changes no count.

---

## Not blocked — in progress or queued

- **D-364** — RECORDED 2026-09-01, dual CONSENT 0/0, commit `d4e9372`, pushed. The
  D-294 / D-056 reading convention that unblocked D-363.
- **D-363** — RECORDED 2026-09-01, dual CONSENT 0/0, commit `7c8a1c9`, pushed.
  **DR-117 is SATISFIED**; condition 2 moved for the first time since 2026-08-23.
- **D-365** — RECORDED 2026-09-02, dual CONSENT 0/0, commit `3b4aab2`, pushed.
  Condition 2 now reads **6 of 23 SATISFIED-requiring rows SATISFIED, with 9 of 32 on
  the deferral limb**.
- **`preview-product-boundary-successor.v15`** — discharges the successor D-364 clause 9
  holds owed on the g29 and g30 grounds. Off the critical path; nothing waits on it.
