# G — owner residuals after D-293 through D-313

Evidence packet only. No recommendation lives here. Recommendations go in
`G-owner-residuals.claude-recommendation.md` / `.codex-recommendation.json`
under this directory. Protocol: `DECISION-PACKETS/RECOMMENDATION-PROTOCOL.md`.

Nothing in this file is decided. The owner decides.

Measured at HEAD `a2d004066d2db7ae89de9ea56979bddb210f0786` (last COORD heading `## D-313`).
Date from the clock: 2026-08-29.

| Pin | Path | sha256 |
|---|---|---|
| file 08 | `docs/v2/architecture/08-decision-and-readiness-register.md` | `e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e` |
| COORD | `docs/coop/COORDINATOR-DECISIONS.md` | `fcd95bf67af0ad076b1e3f9e7a784fcda5dbf4632001f844c70782c0a19f7b5c` |
| agreed recs | `DECISIONS-RECOMMENDED.md` | `42f27394746d4aac569a09a01da719c0cf318cf114086635e73097a6add97370` |
| needed §G | `DECISIONS-NEEDED.md` | `9685b1fc2b99096c1bcd584ff761b3da3c1f32dee71950efe24826431faeedf5` |
| C-plan | `DECISION-PACKETS/C-plan/README.md` | `3981ffdcc153b5182814cba25d450f1167b1dbfd574cdfcd6d2494e31c8cb43e` |
| D1-plan | `DECISION-PACKETS/D1-plan/README.md` | `a69a943a2181b90fbe9aeeb3f1c1112375dcbd77d0ebc67472f9971f1843b58f` |
| protocol | `DECISION-PACKETS/RECOMMENDATION-PROTOCOL.md` | (read live) |
| D-293 | COORD `## D-293` | commit `c10319d207cb90e2bf9df4c5e5997cfd35a30193` |

Live readiness (file 08, unmoved since D-236): required-now 28; Condition 2 is **5 of 32**
(DR-102, DR-104, DR-115, DR-119, DR-123). No `docs/v2/implementation/`.

---

## 0. What is already decided (do not re-litigate)

D-293 adopted `DECISIONS-RECOMMENDED.md` A–F. Subsequent COORD headings recorded every unblocked
C-plan act and A3:

| Heading | Act |
|---|---|
| D-295 | `preview-product-boundary-successor.v10` as DR-117 leftover remasurement; Stage A dual ACCEPT 0/0; both grade rulings SUSTAINED FOR APPLICATION |
| D-303 | C3-a compatibility leftover-join remasured to live file 08 |
| D-304 | C7-a(ii) OD-2 final do-not-fold; leftoverDesign of OBL-OD-2 false; bucket `specifiedNotLeftover` |
| D-305..D-308 | C9 a–d: G01/G02/G04 occupancies + distribution-core leftover-join carrying MB = 1e6 bytes; no derived eight-digit constants |
| D-309 | C1-a OD-112-3 carry: "OD-112-3 is the final fail-closed policy" |
| D-310 | C5-a: six `reservedForBlueprint` members classified implementation encodings; leftoverDesign of OBL-CI-ENCODING-RESERVED stays true |
| D-311 | C6-a: seven reserved lifecycle mechanisms classified implementation encodings; leftoverDesign of OBL-ENCODING-RESERVED stays true |
| D-312 | C7-a(i): OD-1 owner = DR-115 Product + release engineering, in reason; existingGate none; executionObligationOwnerToday none; caps remain named open |
| D-313 | A3: identity-namespace leftover-join.v8; consumes G31 occupancy v5; file08StatusToken SATISFIED; does not reopen D-236 |

B1/B2/B3 **programmes** in `DECISIONS-RECOMMENDED.md` are AGREED. G1 below is not a re-vote of those
programmes. It is the remaining **owner-controlled opening-entry content**, remasured to live bytes
(DR-117 leftover is v10 at D-295, not the v9 the B3 text named before that recording).

Protocol rule (verbatim): "no invented identifiers, numbers, lists, verdicts, or fixture bytes; no
edits under docs/; no readiness claims; recommendations may be 'defer with an explicit disposition'
where the record allows it."

For every question: recommend one of (a) a complete evaluable value now, (b) a lawful deferral
disposition that states it has no Condition-2 / D-056 effect without a separate reviewed act and
successor join, or (c) leave OPEN / named-open. Do not invent a gate so an obligation rides.

---

## 1. G1 — Class A opening entries

`DECISIONS-NEEDED.md` §G1. D-293 Decision 5: programmes authorized; "The D-056 Class A openings
themselves are separate owner-controlled entries; this entry opens none of them." HANDOFF: do not
SATISFY DR-117 / DR-131 / DR-133; openings are the owner's.

### G1-117 — DR-117 opening

Agreed B3 programme (`DECISIONS-RECOMMENDED.md` §B3): Option C with C1 then C2: author a successor
re-citing the twelve current joins and stating relationship to `product-boundary-successor-contract.v8`
(D-116); fresh application-grade dual review bound to that successor's digest; **owner-controlled
opening entry** that lifts D-137's reservation with the owner's word and restates that
successor/contract.v8 relationship; then G29/G30 fixtures; then separate SATISFIED-GRADE + MF-6.
Shared gate-2 entry carries a distinct DR-117 finding.

Live remasurement: C1/C2 leftover limb is recorded at **D-295** as
`preview-product-boundary-successor.v10` (not v9). Grade rulings SUSTAINED FOR APPLICATION. D-137
reservation is still unlifted. File 08 DR-117 status is not SATISFIED.

Recommend: (i) write the opening now vs wait for a shared gate-2 entry first; (ii) the minimum
sentences the opening must contain; (iii) whether it cites v10 or requires another successor; (iv)
whether G29/G30 authoring may start immediately after the opening.

### G1-131 — DR-131 opening

Agreed B1: shared gate-2 entry (common D-056 gate-2 interpretation, then per-row findings; reconcile
D-154 with current gate joins' FX-AUTHORING; do not describe D-249..D-253 as silently overturning
D-154) → fresh application-grade dual review of the exact contract bytes the opening will cite
(`preview-analyze-contract.v2` `081ff7fb…` unless a successor) → T2-02 opening per row citing those
verdicts and the owner's product word → G24–G28 fixtures as conservative sequencing → separate
SATISFIED-GRADE + MF-6.

Recommend: sequencing of shared gate-2 vs the DR-131 opening; whether to author a contract successor
before the opening; minimum sentences of the opening.

### G1-133 — DR-133 opening

Agreed B2: Option 3 → Class A opening → Option 2 pre-SATISFIED sequencing. Fresh review of the
artifact the opening cites (`provider-only-output-contract.v3` `ef2a7416…` or a v4 if three
advisories land). Separate reviewed disposition of the candidate's proposed file-01 preview-role
delta (or remove reliance) before SATISFIED-GRADE. NT-6 authoring as established work; NT-4/NT-7
fixture standing at G20 byte-resolved first. Shared gate-2 entry reconciles D-147 with current
G20/G21 joins, no silent supersession.

Recommend: same shape as G1-131, plus whether NT-6 authoring is in the opening or a later D1 act
(tension with `g21-leftover-join.v13` `$.doesNot[20]` = `"Does not author NT-6."` — see G21-NT6).

---

## 2. G2 — C-plan Q0–Q16

Source: `DECISION-PACKETS/C-plan/README.md` §3. Each *Not stated* sentence is the proof the answer
is not in the record.

### Q0 — Does D-293 reach round-2 recommendation files, or only round-3 text in DECISIONS-RECOMMENDED.md?

Governs C2/C3/C4 content. Round-3 says `All three amendments adopted on top of round 2` and
`- **C2, C3:** unchanged from round 2.` Round-2 text lives in
`DECISION-PACKETS/C1-4-reserved-numbers-security-quality.claude-recommendation.r2.md`
`44f51a5d36eb3f03c711112a50119ea67fb01b3a07d255ccbac5d51cc0485627`. D-293's words never quote it;
they point at `DECISIONS-RECOMMENDED.md` and "the complete file list with digests".

Round-2 C4 already assigns the population packet to `Security + release + platform owners` (the
file-08 DR-126 owner cell). If Q0 = round-3-only, Q4 is still unanswered by D-293's own words.

### Q1 — OD-112-3 wording after D-309

D-293: `OD-112-3 is the final fail-closed policy`. D-309 recorded that sentence. Live superseded
sentence (from C-plan C1): `signed-index-trust-contract.v8`
`$.offlineRunningPolicy.totalDecision[4].alreadyRunning` =
`"refuse unless OD-112-3 is later numbered; preview refuse"`.

Still open: does "final fail-closed" drop `preview`? Does OD-112-3 stay in `namedOpenDecisions` with
DECIDED standing, or leave the array?

### Q2 — OD-112-1, OD-112-2, OD-112-4 values

None in the record. D-293: they stay under DR-112 `Security + operations` (1/2) and product/release
(4). Agreed C1: do not invent; leave RESERVED until the authority supplies values or a concrete
owner disposition; parking must name a real trigger and has no eligibility effect without a
separate reviewed act + successor join.

Recommend (a) values, (b) parking disposition with a named trigger, or (c) leave RESERVED.

### Q3 — DR-111 windows (C3(ii))

C3-a (live file-08 remasurement) is recorded (D-303). Limb (ii) remains: one coherent set —
unit (majors? releases? days?), whether four reserved surfaces share one window, and each value.
Round-2: no isolated unit choice; if values are not in hand that is (b) or (c), not a partial
setting. `compatibility-matrices-contract.v5` `numericWindows` = RESERVED; Product/versioning sets
numbers later. File 08 DR-111 owner is Versioning.

### Q4 — DR-126 population-packet owner (C4-b)

D-293 names the sequence "owner assignment, then …" and names no authority. Three artifacts say
choosing the owner is a separate decision (`platform-tcb-contract.v45`
`$.platformProfile.populationPacket`; G22 occupancy `$.filesystems.laterAct`;
`platform-tcb-leftover-join.v9` `$.proposedLaterWork[2]`). File 08 DR-126 owner cell:
`Security + release + platform owners`. Round-2 C4 assigned the packet to that cell (depends on Q0).

### Q5 — DR-126 selectors and per-OS tables (C4-d)

None in the record for any per-OS table row, filesystem selector value, or version/build selector
value. Four stems: macos/arm64, macos/x86_64, linux/x86_64, linux/arm64. Windows D-002 absent.
`mustNot`: `"apfs-or-hfs-plus as a single value"`. Complete profiles, not four isolated selectors.
Ordered after C4-b then C4-c (application-grade TCB successor making grammar governing).

Recommend values, or (c) leave RESERVED until after the grammar successor.

### Q6 — C5/C6 file-08 echo

D-310 and D-311 are COORD-only. D-293: `It does not edit file 08.` Precedents that wrote file 08:
DR-G05 `caps deferred by explicit disposition (D-006)`; DR-130 in-row disposition.

Recommend: COORD-only stands, or a later MF-6 echo (no eligibility effect by itself).

### Q7 — Can implementation-scope leftoverDesign:true ever satisfy D-056 gate 2?

D-293: no eligibility effect without a separate reviewed act and a successor join. Does not say
whether such an act can succeed. C5–C9 packet open question 1: no COORD entry rules on a sub-row
deferral; D-056's only deferral limb is D-002/D-010 row-level.

### Q8 — OD-1 four cap values and what "measured caps" measures

D-312 assigned the owner; invented no numbers. Caps: manifest byte size, tree entry count, path
length, alias count. `component-manifest-schemas.v11` `namedOpenDecisions[0].standing`: NO caps are
stated; absence is a NAMED OPEN DECISION. D-006: numbers are not derivable from any rule. existingGate
none; no gate measures these four quantities. Adopted fallback: if values are not available, leave
the numeric limb open and say so. Oversized-input fixtures wait on measured caps.

Recommend four numbers plus the measurement method, or leave the numeric limb open.

### Q9 — OD-1 assigned to already-SATISFIED DR-115: MF-6 note vs successor citation

Record shows both: D-089 MF-6 for a label; D-102 successor without label change. D-312
`registerEchoAtApplication` remains owed at a later MF-6; live DR-103 cell still reads UNASSIGNED
between DR-115 and DR-120.

### Q10 — OBL-OD-2 summary bucket

D-304 recorded `specifiedNotLeftover` with an explicit reason (class-specific DR-111 statements
already specify the rule). C-plan noted `dischargedOrDeferred` as the closer reading of a
disposition-closed design decision. Recommend: confirm D-304's bucket, or overturn to
`dischargedOrDeferred` via a successor.

### Q11 — OD-101-1 language and candidate set

D-293 supplies route and authority only: resolve before the core-implementation blueprint under
`Architecture + release engineering` (dedicated D-000 successor, or the owner's direct statement).
Both lawful. PREFERENCE-LADEN, cheap overturn. **No candidate language list exists anywhere.**
HANDOFF: do not invent reserved lists. Recurring guard: `does not mint Rust-as-core`
(D-231, D-232, D-287, four artifacts).

Constraints any language must meet (from `distribution-core-inventory-contract.v16` and file 08
DR-101 / DR-115): small native executable; default install excludes language runtimes; platforms
macos/arm64, macos/x86_64, linux/x86_64, linux/arm64 (Windows D-002 absent); D-006 envelope with
MB = 1e6 bytes (core ≤ 25 MB compressed / ≤ 80 MB installed; RSS 40/50 help-version, 60/100 doctor).
DR-118 `does not mandate implementation language`.

Recommend: (i) owner states the language directly now; (ii) dedicated successor that first publishes
a candidate set then chooses; (iii) leave RESERVED (DR-101 stays OPEN; Condition 2 stays NOT MET on
this row). If (i) or (ii) names a language, it must not pretend the list was already in the record.

### Q12 — OD-101-1 Route C (preference) vs rule-governed

Sets D-000 clause 5 overturn cost. D-001 classes DR-101 as `Rule-governed architecture authoring
with review`. Contract `namedOpenDecisions[0].owner` = `A later Route-C or rule-governed successor,
not this extraction.` Adopted C8 rec already says PREFERENCE-LADEN. D-293 does not resolve the
disjunction. Recommend one.

### Q13 — OD-101-2 ceremony content

Signing ROLES exist. No ceremony, threshold, or notarization procedure is named. D-293: own DR-101
successor owned separately from DR-112. A deferral to C1 does not close OBL-D2. Recommend content,
or leave RESERVED pending that successor (do not merge with DR-112).

### Q14 — Derived MB byte constants in C9 occupancies

D-305..D-308 recorded `≤ 25 MB, MB = 1e6 bytes per D-293` form and refused binary-MB literals.
None of 25000000 / 80000000 / 40000000 / 50000000 / 60000000 / 100000000 appears in the record.
Recommend: occupancies may write the decimal constants later, or they stay forbidden (quote MB only).

### Q15 — G02 installed-tree accounting authorities

D-293: stays open until "the named authorities" record a complete rule. That sentence names none.
Round-2 C9 names `Product + release engineering` and `Architecture + release` (DR-115 and DR-G02
owner cells). Dimensions: logical lengths, allocated blocks, metadata/xattrs, links, deduplicated
inventory nodes. Recommend confirm those two authorities, or name others.

### Q16 — C10, C11, C12

Outside D-293. Summary table covers C1–C9 only.

- **C10** G07 filesystem coverage list (`filesystems.standing` UNPOPULATED).
- **C11** DR-105/DR-114 FC-C1 joint-owner recording; BLK-1..4 routing (D-032 "still-routed").
- **C12** DR-124 grant-journal assignment (owner concurrence); DR-127 AL-1/2/5 and AL-3 execution routes.

Recommend: park until after seal / Condition 5; or open a new decisions packet now.

---

## 3. G3 — D1 byte blockers and named fixture opens

D-293 Decision 8 delegated 16 obligations with a reserved list (G07, G08, G09, G12, G14, G22 and
named twins). Authoring shape is delegated; **new semantic members/values/lists/implementations are
named open decisions, never a choice** (D1-plan).

### G3-G15 — adapter implementation (OBL-ADAPTER-IMPL)

`g15-leftover-join.v6` standing BLOCKED-ON-OBL-ADAPTER-IMPL. D-108: adapter implementations remain
reserved. Occupancy: "Adapter implementation remains reserved (D-108)." Does not invent cargo, npm,
esbuild, webpack, a Dockerfile, a CLI, or a Rust adapter; does not mint Rust-as-core. 324 AT cells
wait on an adapter.

Recommend: name an adapter, or leave reserved until after Condition 5 / language (Q11).

### G3-G16 — comparison-basis component axis

Standing BLOCKED-ON-UNENUMERATED-COMPARISON-BASIS-COMPONENT-AXIS. OQ-G16-1: declared comparison-basis
component identity set is not in the record. 24 is a floor, not a closed total.

Recommend: enumerate the set, or leave blocked.

### G3-G18 — on-disk quarantine format

Standing BLOCKED-ON-OBL-ENCODING-RESERVED. Quarantine is required; format is reserved. D-311
classified encodings as implementation-scope; leftoverDesign of OBL-ENCODING-RESERVED stays true.
OQ-G18-3: whether a corpus may record quarantine *fate* without quarantine *bytes* is not stated.

Recommend: specify a format; allow fate-without-bytes; or leave blocked.

### G3-HOSTILE — per-class golden counts (OQ-HG-5)

Authorable floor is 16 witnesses, one per named specification unit (J-1..J-5 + CC-1..CC-11). Case
count is not enumerable. First-authoring is NOT blocked on a closed count (Axis E remainingNotAuthored).

Recommend: author the 16-witness floor now; or wait for per-class counts.

### G3-SARIF-RUNID — FC-OUTFAIL.committed-run-preserved

§7.1 parks RunId derivation (`"No exact RunId derivation recipe is binding yet."`).
`FC-OUTFAIL.no-committed-run` is not blocked. OQ-SARIF-8: may committed-run-preserved carry a
literal RunId matching `^run1:[0-9a-f]{64}$` as an opaque pin, or must it wait for the recipe?

Recommend: opaque pinned literal now, or keep parked.

### G21 named opens (do not invent; recommend choose vs leave named-open)

From `DECISION-PACKETS/D1-plan/G21.md` §(b). Remaining G21 fixture authoring is otherwise delegated.

| ID | Choice |
|---|---|
| G21-EXACT | exactly-at vs preHandshake `N>65536` bound |
| G21-POST | postHandshake bound |
| G21-SCHEMA | per-type control-frame body schema (ping/pong/hello/…) |
| G21-NT6 | author NT-6 at G21 despite `$.doesNot[20]` vs B2 "author NT-6" |
| G21-FCNC | FC-NC default-posture / process-tree vs G12 owner reservation |

For each: recommend a value, or "leave named-open and skip those members".

---

## 4. Required recommendation shape

Claude writes `DECISION-PACKETS/G-owner-residuals.claude-recommendation.md` covering **every** id
in §1–§3. Per id:

- **Recommendation** (one sentence, then any required wording).
- **Rationale** — each factual claim cites this packet section or a path/JSON path/COORD heading.
- **What changes** if the owner adopts (file 08 / COORD / leftover-join / occupancy / nothing).
- **Risk** if adopted / if deferred.
- **Confidence** low | medium | high.

Then a summary table: id | recommendation (≤20 words) | confidence.

Do not SATISFY DR-117/131/133 in the recommendation text as if already opened. Do not edit file 08
or COORD. Do not invent fixture bytes. Do not mint Rust-as-core as if it were already decided;
naming it as a *candidate* in Q11 is a recommendation, not a recording.

Codex, independently and adversarially, writes
`DECISION-PACKETS/G-owner-residuals.codex-recommendation.json`:

```json
{
  "item": "G-owner-residuals",
  "reviewOf": "DECISION-PACKETS/G-owner-residuals.claude-recommendation.md",
  "verdict": "AGREE | DISAGREE | AGREE-WITH-AMENDMENT",
  "confidence": "low|medium|high",
  "perQuestion": [
    {
      "id": "G1-117",
      "verdict": "AGREE|DISAGREE|AGREE-WITH-AMENDMENT",
      "recommendation": "...",
      "refutations": [],
      "amendments": []
    }
  ],
  "rationale": "...",
  "refutations": [],
  "amendments": []
}
```

Codex must try to refute Claude before agreeing, and must re-check packet claims against bytes.
`perQuestion` must include every id Claude recommended.
)
