# OBL-HOSTILE-GOLDENS — OBL-HOSTILE-GOLDENS — D1 fixture-authoring plan record

Recorded at HEAD `8bc9963f68784842de643d5dbb1269bd4cf4411a`. This is an inventory of already-recorded
bytes. It authors no fixture byte, records no successor, and decides nothing.

## 1. Governing bytes

### 1.1 GATE leftover-join

This obligation is **ROW-only**: it lives on an architecture-row leftover-join (DR-127), not on a
`DR-G*` gate join. `DECISION-PACKETS/D1-fixture-authoring-delegation.md`
sha256 `bc8484cc7159af26a142b97a55b1095049f7ea2ac10c283cd1e2428ba2569ea9` places it in
`### 3.3 ROW-only fixture obligations (8 measurements, 8 distinct ids)`, not in §3.1's GATE-side
table.

- Path: `docs/coop/artifacts/anti-lockstep-leftover-join.v3.json`
- sha256: `820d724a10a1e11a2188a323a3425cd13f4c483892bb487fb93f6542103c85e1`
- `$.artifact` = `"anti-lockstep-leftover-join.v3"`
- `$.version` = `3`
- `$.date` = `"2026-08-21"`
- `$.documentClass` = `"DESIGN-CONTRACT-CANDIDATE"`
- `$.registerRow` = `"DR-127"`
- `$.status` = `"CANDIDATE-NOT-APPLIED"`
- `$.reviewStatus` = `"AWAITING-INDEPENDENT-REVIEW"`
- `$.sealRecommendation` = `"DO-NOT-SEAL"`
- `$.binds` = `"NOTHING"`
- `$.head` = `"a11a0412ba30fc454deb6cbe03a6716e88469e3e"`
- `$.requiredNowUnchanged` = `28`
- `$.file08StatusToken` = `"OPEN"`

COORD heading that recorded it (`docs/coop/COORDINATOR-DECISIONS.md`
`1ee9def72c44acd96f36da3392d4980d0e06afb731b0a4003b5bde73247e136c`, line 7990), verbatim:

> `## D-186 — Record anti-lockstep-leftover-join.v3 as DR-127 leftover remasurement`

**`$.file08Pin` is stale against live file 08.** The join carries:

```json
{
  "path": "docs/v2/architecture/08-decision-and-readiness-register.md",
  "sha256": "f909ddff7f3a8e9be864259808c4a2320170181001bdb746814b07393dd9d5e1"
}
```

Live file 08 at HEAD hashes to `e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e`.
The join's own `$.remeasurementClause` addresses this:

> "If a cited file moves in a way that is not append-only COORD growth or COORD heading hygiene,
> with file 08, leftover-join v1, leftover-join v2, and this draft unmoved, re-measure before
> recording. recordedInputs.HEAD must equal the top-level head. This join does not unwrite D-167
> through D-185. Frozen v2 remains a historical measurement as of HEAD a11a041. Frozen v1 remains a
> historical measurement as of HEAD 5d5d778."

The DR-127 row text itself is unchanged between the pinned and live digests — the cell quoted in
§1.3 below re-extracts byte-identically from live file 08 line 309. But the digest mismatch is on
the record and a successor must handle it. See OQ-HG-1.

`$.leftoverDesignOpenStanding`, verbatim:

> "The live DR-127 token is OPEN. leftover-design of an unauthored v7 contract is stale as an
> authoring claim. leftover-design of hostile dual-channel goldens, uncovered AL-1/AL-2/AL-5
> execution, and AL-3 core-release-byte rollback remains."

`$.summary.leftoverDesign` = `["OBL-HOSTILE-GOLDENS","OBL-AL3-CORE-ROLLBACK","OBL-AL1-AL2-AL5"]`;
`$.summary.goldensAuthored` = `false`; `$.summary.fixturesExecuted` = `false`;
`$.summary.classAOpened` = `false`; `$.summary.requiredNowUnchanged` = `28`.

`$.liveGateOwners` = `{"DR-G21": "Supervisor + protocol + operability"}` — note this names the *G21*
gate owner, not DR-127's own owner cell. DR-127's owner is at file 08 line 309 column 3:
`Protocol + versioning + release owners`.

`$.doesNotCloseLeftoverAlone`, verbatim:

> "This candidate does not make DR-127 D-056-eligible. OBL-HOSTILE-GOLDENS, OBL-AL3-CORE-ROLLBACK,
> and OBL-AL1-AL2-AL5 remain leftover-design. Gates 2 and 3 do not hold. Class A is not opened. The
> file 08 token stays OPEN. Not SATISFIED."

### 1.2 The obligation object (verbatim)

JSON path: `$.obligations[1]` of `docs/coop/artifacts/anti-lockstep-leftover-join.v3.json` (verified:
the `obligations` array is `[OBL-CONTRACT-V7, OBL-HOSTILE-GOLDENS, OBL-CC-EXECUTION,
OBL-AL3-COMPONENT, OBL-AL4, OBL-AL3-CORE-ROLLBACK, OBL-AL1-AL2-AL5, OBL-WINDOWS,
OBL-ADVISORY-HONESTY]`).

```json
{
  "id": "OBL-HOSTILE-GOLDENS",
  "leftoverDesign": true,
  "existingGate": "none as authored implementations",
  "namedNotAuthored": "hostile dual-channel race/fault/EOF/duplicate/teardown goldens with byte-opaque provider frames",
  "executionObligationOwnerToday": "none",
  "rideStanding": "not-capable-of-riding as execution-only remainder",
  "reason": "D-111 records hostile dual-channel goldens remain named, not authored here. File 08 acceptance-evidence cell names those goldens. v7 raceCatalogByReference consumes J-1..J-5 and CC-1..CC-11 of control-protocol-contract.v2 and does not copy them. D-056 Decision clause 5: authoring fixtures remains design work. This join does not invent those golden bytes."
}
```

Field-by-field:

- `$.obligations[1].reason` — quoted in full above. Four sentences, each naming a different governing
  byte: D-111 (COORD), the file 08 acceptance-evidence cell, `anti-lockstep-contract.v7`'s
  `raceCatalogByReference`, and D-056 Decision clause 5.
- `$.obligations[1].namedNotAuthored` — a **string**, not an array (unlike the GATE joins'
  `namedCorpusNotAuthored` arrays). Its value is the tail of file 08 line 309 column 5, byte-exact.
- `$.obligations[1].existingGate` = `"none as authored implementations"`.
- `$.obligations[1].rideStanding` = `"not-capable-of-riding as execution-only remainder"`.
- `$.obligations[1].executionObligationOwnerToday` = `"none"`.
- `namedCorpusNotAuthored`, `remainingNotAuthored`, `namedCases` — **absent** on this obligation
  object. `namedNotAuthored` is the only naming field.

**The sibling obligation that carries the CC execution half**, `$.obligations[2]`, quoted because it
is what makes OBL-HOSTILE-GOLDENS' scope readable:

```json
{
  "id": "OBL-CC-EXECUTION",
  "leftoverDesign": false,
  "existingGate": "DR-G21",
  "executionObligationOwnerToday": "Supervisor + protocol + operability",
  "rideStanding": "qualification-at-named-gate",
  "reason": "v7 executionRoutes.CC-1-to-CC-11 is DR-G21 / condition 4. D-015: DR-127 gains no design-level SATISFIED supplier from CC-1..CC-11 existing. G21 v3 leftoverDesignClosedIfAcceptedAndRecorded names OBL-G21-HARNESS-SPEC on DR-114. This join does not steal G21 leftover remaining on DR-114, does not execute CC-1..CC-11, and does not claim QUALIFIED."
}
```

So the record splits the CC surface in two on this row: **execution** of CC-1..CC-11 rides DR-G21
(`OBL-CC-EXECUTION`, leftoverDesign false), while **authoring the golden bytes** stays on DR-127
(`OBL-HOSTILE-GOLDENS`, leftoverDesign true, not-capable-of-riding). See §2 and OQ-HG-4 for the
overlap with G21's own FX obligation.

### 1.3 The cell that plays the occupancy role

**There is no `harness.DR-G*` occupancy artifact for this obligation.** Confirmed three ways:

1. `$.registerRow` is `"DR-127"`, an architecture row, not a `DR-G*` gate row.
2. `$.basedOn` (6 entries: `contractV7`, `g21v3`, `g16v2`, `d056`, `predecessorV1`, `predecessorV2`)
   contains no `occupancy*` key. The two harness files it does name are cited for a different
   purpose: `$.basedOn.g21v3.role` = "Cited only as the already-named G21 runner.
   leftoverDesignClosedIfAcceptedAndRecorded names OBL-G21-HARNESS-SPEC on DR-114. This join does
   not steal G21 leftover remaining on DR-114 and does not treat CC execution as SATISFIED
   evidence."; and `$.basedOn.g16v2.role` = "Cited only. v7 executionRoutes allow AL-1/AL-2/AL-5 to
   ride a reviewed owning gate such as G16 only for the exact cases that accepted contract covers.
   G16 v2 does not apply v16 IR-1..IR-4 / G16-12 and states hostile dual-channel goldens ride
   DR-127 / G21. Uncovered AL-1/AL-2/AL-5 remain on this row."
3. `$.obligations[1].existingGate` = `"none as authored implementations"` and
   `$.obligations[1].rideStanding` = `"not-capable-of-riding as execution-only remainder"`.

**What plays the occupancy role instead is the file 08 acceptance-evidence cell**, exactly as
`$.obligations[1].reason` says: "File 08 acceptance-evidence cell names those goldens."

- File: `docs/v2/architecture/08-decision-and-readiness-register.md`
- sha256: `e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e`
- Table header, **line 280**, verbatim:

> `| ID | Decision | Owner / decision authority | Source pin / affected sections | Required acceptance evidence | Status | Blueprint impact |`

- The DR-127 row is **line 309**. Column 5 of that header is `Required acceptance evidence`.
  **Column 5 of line 309, verbatim** (this is the cell that plays the occupancy role):

> ` Bidirectional N/N+1 skew, independent rollback/coexistence, no bundle promotion gate; hostile dual-channel race/fault/EOF/duplicate/teardown goldens with byte-opaque provider frames `

The other cells of line 309, for the record:

| col | header | value verbatim |
|---|---|---|
| 1 | ID | ` DR-127 ` |
| 2 | Decision | ` Anti-lockstep compatibility and host-owned control/data race precedence ` |
| 3 | Owner / decision authority | ` Protocol + versioning + release owners ` |
| 4 | Source pin / affected sections | ` [Control demarcation](02-distribution-and-components.md#exact-controldata-plane-demarcation); [compatibility](04-lifecycle-delivery-and-operations.md#separate-compatibility-matrices) ` |
| 5 | Required acceptance evidence | ` Bidirectional N/N+1 skew, independent rollback/coexistence, no bundle promotion gate; hostile dual-channel race/fault/EOF/duplicate/teardown goldens with byte-opaque provider frames ` |
| 6 | Status | ` OPEN ` |
| 7 | Blueprint impact | ` Hard blocker for independent-release blueprint ` |

The cell's semicolon splits it into two limbs. The **second** limb — "hostile dual-channel
race/fault/EOF/duplicate/teardown goldens with byte-opaque provider frames" — is byte-identical to
`$.obligations[1].namedNotAuthored` and is the whole of OBL-HOSTILE-GOLDENS. The **first** limb —
"Bidirectional N/N+1 skew, independent rollback/coexistence, no bundle promotion gate" — is the
AL-1..AL-5 pass-property surface, which the join splits across `OBL-AL1-AL2-AL5`,
`OBL-AL3-COMPONENT`, `OBL-AL3-CORE-ROLLBACK` and `OBL-AL4`, not this obligation.

**What this cell does *not* give that a `harness.DR-G*` occupancy would.** There is no
`exactByteIntent` string anywhere in the DR-127 lineage — no `retainedEvidence[]`, no
`namedCorpusClasses[]`, no `passProperty`, no `failsIf`, no `platforms`, no `windowsStanding`, no
`liveHarnessCellVerbatim`. The five gate-style fields the brief asks for at §1.3 are all absent
here. Their function is taken over by the two contracts in §1.5: `anti-lockstep-contract.v7`
supplies the consumption rule and `control-protocol-contract.v2` supplies the class definitions with
their `intent` strings. That substitution is what
`$.obligations[1].reason` sentence 3 records: "v7 raceCatalogByReference consumes J-1..J-5 and
CC-1..CC-11 of control-protocol-contract.v2 and does not copy them."

The join's `$.executionRoutesVerbatim` is the closest thing to a fate table this row carries:

```json
{
  "CC-1-to-CC-11": "DR-G21 / condition 4, and DR-012 qualification where that row applies. Specifications consumed, not SATISFIED evidence.",
  "AL-3-component-or-generation-selection-rollback": "Accepted D-107 lifecycle-generation-contract.v2 and DR-G18. Not G21. Not a core-release-byte rollback.",
  "AL-3-core-release-byte-rollback": "Reviewed DR-110 owning contract and its applicable named gates, or remains this row until that contract exists. D-107/DR-G18 expressly exclude core-release-byte rollback.",
  "AL-4": "Consume lifecycle-generation-contract.v2 recorded at D-107. Remaining execution is DR-G18 / condition 4. Not G21.",
  "AL-1-AL-2-AL-5": "Selection/qualification evidence rides a reviewed owning gate such as DR-G16 only for the exact cases that accepted contract covers. Uncovered AL-1/AL-2/AL-5 execution remains at DR-127. It is not a D-056 condition-4 remainder pending a reviewed owning-gate contract. Not G21."
}
```

### 1.4 ROW twin join (or: none)

**None, and the direction is inverted from the GATE cases.** This obligation is ROW-only:
`DECISION-PACKETS/D1-fixture-authoring-delegation.md`
sha256 `bc8484cc7159af26a142b97a55b1095049f7ea2ac10c283cd1e2428ba2569ea9` lists it under
`### 3.3 ROW-only fixture obligations (8 measurements, 8 distinct ids)` with the row:

> `| `anti-lockstep-leftover-join.v3` / `OBL-HOSTILE-GOLDENS` | DR-127 `Protocol + versioning + release owners` | `namedNotAuthored`: "hostile dual-channel race/fault/EOF/duplicate/teardown goldens with byte-opaque provider frames" | "D-111 records hostile dual-channel goldens remain named, not authored here." | byte-set (goldens) | "v7 raceCatalogByReference consumes J-1..J-5 and CC-1..CC-11 of control-protocol-contract.v2 and does not copy them." |`

There is no GATE-side join carrying the id `OBL-HOSTILE-GOLDENS`. The §3.2 cross-custody rule —

> "Closing a fixture obligation would require a successor on *both* the GATE join and its ROW twin,
> since the same id is measured true on both."

— is therefore **inapplicable**: closing `OBL-HOSTILE-GOLDENS` needs a successor on
`anti-lockstep-leftover-join` alone.

The nearest thing to a twin is a *different id on a different row* covering overlapping bytes:
`g21-leftover-join.v13.json` sha256 `058717f51ee62e85fa3094e9a65c207fb78a7f706e57a35a854f1a9a55ecc66e`,
`$.obligations[3]` = `OBL-G21-FX-AUTHORING`, whose
`$.obligations[3].remainingNotAuthored.dr102` = `["CC-1","CC-2","CC-3","CC-4","remaining CC-5
injections","CC-6","CC-7","CC-8","CC-9","CC-10","CC-11"]`. Different id, different row, overlapping
byte set. That overlap is §2's last subsection and OQ-HG-4. The record explicitly forbids treating
them as one custody: `anti-lockstep-leftover-join.v3.json#$.doesNot[8]` — "Does not steal G21
leftover remaining on DR-114."

Another id on this same join is also recorded as being on the same subject and expressly separate:
`OBL-CONTRACT-V7` (`$.obligations[0]`, leftoverDesign false) — the contract exists; the goldens do
not.

### 1.5 Governing contract/spec the join pins

Two artifacts, in a chain: the join pins v7; v7 pins control-protocol-contract.v2.

#### (a) `anti-lockstep-contract.v7` — the "v7" of the obligation reason

**What "v7" refers to, pinned.** The obligation reason's phrase "v7 raceCatalogByReference" resolves
to `anti-lockstep-contract.v7`, on four independent bytes:

1. `$.basedOn.contractV7.path` = `"docs/coop/artifacts/anti-lockstep-contract.v7.json"`,
   `$.basedOn.contractV7.sha256` =
   `"8c41bddd7c351abc3a0b4b721f9302df29ba7d053352cb950ec8b23e4afdd671"`.
2. That file's `$.raceCatalogByReference` exists and its content matches the reason's claim
   (quoted below); no other artifact in `docs/coop/artifacts/` carries that key name.
3. COORD line 4411, verbatim:
   > `## D-111 — Record anti-lockstep-contract.v7 as DR-127's accepted design-contract successor candidate`
4. `$.obligations[0].reason` (OBL-CONTRACT-V7): "D-111 recorded anti-lockstep-contract.v7 as
   DR-127's accepted design-contract successor candidate at dual ACCEPT 0/0."

The lineage is `anti-lockstep-contract.v1` through `.v7`; v7 is the head on disk and the recorded
one. It is **not** `sarif-projection-contract.v7`, `g21-fixture-corpus.v7`, or any other v7.

- Path: `docs/coop/artifacts/anti-lockstep-contract.v7.json`
- sha256: `8c41bddd7c351abc3a0b4b721f9302df29ba7d053352cb950ec8b23e4afdd671` (re-hashed at HEAD)
- `$.artifact` = `"anti-lockstep-contract.v7"`, `$.version` = `7`, `$.date` = `"2026-08-15"`,
  `$.registerRow` = `"DR-127"`, `$.status` = `"CANDIDATE-NOT-APPLIED"`,
  `$.reviewStatus` = `"AWAITING-INDEPENDENT-REVIEW"`, `$.binds` = `"NOTHING"`.
- Verdicts (`$.basedOn.contractV7.reviews` of the join): Claude
  `anti-lockstep-contract.v7.review-independent.claude2.json`
  `73fb7bde942b1b393faa928c4db3538fb7dfa58faee6bb8f4ad66368d2a67235` ACCEPT 0/0; Codex
  `anti-lockstep-contract.v7.review-independent.codex.json`
  `9f1adab71c6231a0e72a37f301f5e253453f2a76f1545739e27f40eba30d9663` ACCEPT 0/0. **Dual ACCEPT.**

`$.raceCatalogByReference`, verbatim and complete — this is the consumption rule the obligation
reason cites:

```json
{
  "joins": "J-1..J-5 of control-protocol-contract.v2",
  "classes": "CC-1..CC-11 of control-protocol-contract.v2",
  "rule": "This row CONSUMES those joins and classes. It does not copy them. Execution remains DR-G21 / condition 4 and DR-012 qualification where that row applies. D-015: DR-127 gains no design-level SATISFIED supplier from CC-1..CC-11 existing.",
  "byteOpacity": "Provider semantic frames are compared byte-for-byte. The control plane may decide supervision/fate only under the owning contract."
}
```

`$.recordedInputs.governingSources[2]` of v7 pins the consumed contract:

```json
{"path":"docs/coop/artifacts/control-protocol-contract.v2.json","sha256":"c50a79fef566ecccbd8913a3d309b0cf7332f7d77f892474a548ef3d7b4ebdca","role":"J-1..J-5 and CC-1..CC-11 are the race catalog. D-015: those classes are specifications, not this row's executed SATISFIED evidence."}
```

v7's `$.authorityClaim`, verbatim (the sentence naming the consumption):

> "This artifact PROPOSES the DR-127 anti-lockstep and host-owned dual-channel precedence design
> contract: the five independent-release pass properties, the bundle-is-not-a-hidden-gate rule,
> preview-required N/N+1 pairs, and the consumption of DR-102 joins J-1..J-5 / CC-1..CC-11 as the
> race catalog. It applies nothing, does not fork the control protocol, does not treat CC-1..CC-11
> execution as this row's SATISFIED evidence, does not adopt file 11's cost warning as a D-000, and
> does not authorize docs/v2/implementation/. The DR-127 row remains OPEN until coordinator
> disposition after independent review."

**Note the citation gap.** `anti-lockstep-leftover-join.v3.json#$.recordedInputs` (15 entries) does
**not** list `control-protocol-contract.v2.json`. The join reaches the contract only transitively,
through `$.basedOn.contractV7` → v7's own `$.recordedInputs.governingSources[2]`. See OQ-HG-2.

#### (b) `control-protocol-contract.v2` — where J-1..J-5 and CC-1..CC-11 are defined

- Path: `docs/coop/artifacts/control-protocol-contract.v2.json`
- sha256: `c50a79fef566ecccbd8913a3d309b0cf7332f7d77f892474a548ef3d7b4ebdca` (re-hashed at HEAD;
  matches v7's pin)
- `$.artifact` = `"control-protocol-contract.v2"`, `$.version` = `2`, `$.date` = `"2026-08-13"`,
  `$.registerRow` = `"DR-102"` (a **different row** from DR-127),
  `$.status` = `"CANDIDATE-NOT-APPLIED"`, `$.reviewStatus` = `"AWAITING-INDEPENDENT-REVIEW"`,
  `$.sealRecommendation` = `"DO-NOT-SEAL"`, `$.binds` = `"NOTHING"`.

**J-1..J-5 — `$.joinPrecedenceTable.joins[0..4]`.** The goldens must exercise these; each is quoted
in full.

`$.joinPrecedenceTable.mechanism` (the frame the five joins sit in):

> "The host maintains ONE host-owned merged event order per supervised child: an append-only total
> order over control-plane events (frame accepted, refusal, cancel issued, shutdown issued, deadline
> expiry) and data-plane boundary events (first byte, EOF, process death, and the owning
> participant's fault report per J-2 - boundary events and boundary reports only, never content).
> Each event is appended at host observation with its channel and kind. Determinism claim, bounded:
> given the same observed event sequence per channel and the tie rules below, the merged order is a
> pure function of those observations - the joins bind ORDERING. What any ordering MEANS - fates,
> D9, exits, Coverage - is decided under the OWNING contract and is DR-007-open; no code value
> appears in this table (identityDependencies ID-DEP-2)."

`$.joinPrecedenceTable.joins[0]` — **J-1**, race `"cancellation versus result"`:

> "cancel-issued is appended when the host writes the cancel frame; a provider result is represented
> by its final-octet arrival within the data-plane stream (content invisible; the owning participant
> reports 'stream position P complete' as a boundary fact). If the final octet was read before
> cancel was written, the result precedes the cancel in the merged order; otherwise cancel precedes.
> Same-observation-instant tie: the data-plane event is appended first (a byte that has arrived is
> history; the host's own control action never retroactively outranks received bytes). The owning
> contract then decides what a result-after-cancel or cancel-after-result IS."

`$.joinPrecedenceTable.joins[1]` — **J-2**, race `"control fault versus provider fault"`:

> "A control-plane fault (any RF family) and a provider-plane fault (as defined by the owning
> contract, surfaced to the host as a boundary event, e.g. EOF-mid-stream or the owning
> participant's fault report) are both appended at observation. The earlier event drives the
> supervision transition (which ladder step starts); the later one is still appended and delivered -
> never coalesced, never dropped. Same-instant tie: the control-plane fault is appended first,
> because supervision is this plane's own authority while the provider fault's meaning belongs to
> the owning contract; ordering first does not let the control fault redefine the provider fault."

`$.joinPrecedenceTable.joins[2]` — **J-3**, race `"EOF/process death"`:

> "EOF is per-channel (fd1, fd4 observed separately); process death (reaped exit status) is a
> distinct event. All channels are drained to EOF - every octet read and delivered - before the
> death event is appended, under a bounded host drain deadline whose expiry is itself a typed
> appended event (drain-deadline-expired) that precedes the death event when it fires. Death is
> therefore always the LAST event of a child's merged order, and no octet that arrived before death
> can be lost behind it."

`$.joinPrecedenceTable.joins[3]` — **J-4**, race `"duplicate or late frames"`:

> "Duplicate/out-of-order CONTROL frames: seq discipline makes them RF-7 at the receiver - typed,
> appended, never silently dropped, never reordered-to-fit. Late CONTROL frames after shutdownAck:
> RF-7, appended after the shutdown event they violate. Late PROVIDER data after cancel or teardown
> initiation: delivered unmodified per the no-suppression rule, appended in arrival order; the
> owning contract alone assigns its meaning. The control plane has no concept of a provider
> duplicate: recognizing one would require reading content."

`$.joinPrecedenceTable.joins[4]` — **J-5**, race `"teardown"`:

> "The teardown ladder is deterministic and one-way: T-1 shutdown frame (or cancel, when teardown
> begins as cancellation) -> T-2 bounded wait for shutdownAck and voluntary exit -> T-3 data-plane
> and control-plane EOF observation with J-3 draining -> T-4 kill of the full process tree -> T-5
> reap and final death event. Each transition is an appended event; expiry of each bounded wait is
> an appended typed event; the ladder never skips backward and teardown never truncates or rewrites
> the merged order retroactively."

`$.joinPrecedenceTable.deadlineDiscipline` — the clause that bounds what a golden may fix:

> "Every 'bounded wait' above MUST exist, MUST be finite, and its expiry MUST be a typed appended
> event - that is bound HERE. The numeric values are host operational configuration bound at
> blueprint/qualification, NOT here: a duration constant without a named runner and workload would
> be a threshold that measures nothing, and the containment harness (DR-G21) is where expiry
> behavior gets its goldens (identityDependencies ID-DEP-3)."

**CC-1..CC-11 — `$.hostileDualChannelConformance.classes[0..10]`.**

`$.hostileDualChannelConformance.discipline` (the framing sentence, and the source of the
"byte-opaque provider frames" property):

> "Fixture CLASSES with exact-byte intent - what is injected, what must hold, and how equality is
> judged - not implementations. Every class that touches the data plane judges provider semantic
> frames BYTE-FOR-BYTE against the injected reference stream: equality means equal octet sequences
> per frame after boundary recovery under the owning contract's own framing, and equal frame order.
> The harness that executes these classes is DR-G21/blueprint work (identityDependencies ID-DEP-3);
> acceptance for DR-102 is 'contract proving no TS/Rust frame translation plus hostile conformance',
> and these classes are the hostile half's specification."

That sentence — "Fixture CLASSES with exact-byte intent - what is injected, what must hold, and how
equality is judged - not implementations" — is this lineage's equivalent of a gate occupancy's
`exactByteIntent` field, and the eleven `intent` strings below are the exact-byte intents.

`$.hostileDualChannelConformance.classes[0]` — **CC-1**, `"race-ordering matrix"`:

> "Every pairwise and every reachable total ordering of {cancel-issued, provider-final-octet,
> control-fault, provider-fault-report, provider-EOF, process-death, teardown-initiated} is
> exercised with scripted channel actors. provider-fault-report is the owning participant's fault
> report surfaced to the host as a boundary event - J-2's second provider-fault constituent -
> injected by the scripted owning-side actor as a boundary report whose content the control plane
> never reads. For each ordering the merged event order must match the J-1..J-5 rules exactly,
> including every J-2 variant in which the provider fault is the fault report rather than an EOF and
> the same-observation-instant tie J-2 resolves control-fault-first, and the provider byte stream
> delivered to the owning participant must equal the injected stream byte-for-byte in every ordering
> - a race may change WHAT the order says, never one provider octet."

`$.hostileDualChannelConformance.classes[1]` — **CC-2**, `"mid-frame interleave"`:

> "Control frames (ping, cancel, health, shutdown) delivered while a provider frame is partially
> transmitted on the data plane - including split at every byte offset of the provider frame's
> length prefix and at chunk sizes of 1 byte. The provider frame must arrive byte-identical with
> boundaries intact; the control frames must be processed normally; no cross-channel buffering
> artifact may reorder either plane's own events."

`$.hostileDualChannelConformance.classes[2]` — **CC-3**, `"duplicate/late/reordered control frames"`:

> "seq repeats, gaps, decreases; frames replayed after their state window; frames after shutdownAck.
> Each is RF-7 typed at first violation; the provider stream in flight remains byte-identical; the
> violation event lands in the merged order exactly once."

`$.hostileDualChannelConformance.classes[3]` — **CC-4**, `"EOF at every state"`:

> "fd3/fd4/fd1 EOF and process death injected at EVERY channel state (AWAIT-HELLO through TEARDOWN)
> and at every handshake step boundary. Every case yields the typed J-3 ordering (drain, then death
> last); no state yields a partial-parse acceptance, a hang without a bounded-wait expiry event, or
> a fabricated success."

`$.hostileDualChannelConformance.classes[4]` — **CC-5**, `"oversized and malformed framing"`:

> "Length prefix 0; prefix exactly at, one over, and far over the operative bound (pre- and
> post-handshake bounds separately); truncated bodies; invalid UTF-8; duplicate members; unknown
> members; floats, negative and over-uint53 integers. Each is RF-2 typed; the fixture's pass
> property includes the observable memory bound - the receiver refuses oversize from the prefix
> alone without buffering the body."

`$.hostileDualChannelConformance.classes[5]` — **CC-6**, `"handshake downgrade and replay"`:

> "Future-major hello (typed RF-1 via the frozen core, with the body deliberately laden with hostile
> content that must never be parsed); second hello in every state (RF-8); helloAck proposing a
> different controlMajor than offered (RF-8); re-select attempts after selectAck (RF-8). No
> downgrade path exists to find: pass means every attempt ends in the typed refusal plus teardown
> ladder, never a lower-version session."

`$.hostileDualChannelConformance.classes[6]` — **CC-7**,
`"subprotocol-name spoofing versus manifest declarations"`:

> "Offers and confirms carrying tokens outside the admitted manifest's capabilities[] declarations:
> case variants, NFC/NFKC-equal-but-code-point-different variants, homoglyphs, trailing/leading
> whitespace, zero-width insertions, same string declared by a DIFFERENT stableId's manifest, and
> subprotocolVersion off-by-one. Every one is RF-4 under exact code-point/integer equality against
> THIS component's admitted declarations; nothing normalizes, nothing fuzzy-matches, no
> cross-component custody leak."

`$.hostileDualChannelConformance.classes[7]` — **CC-8**, `"fate-assignment smuggling"`:

> "Control frames attempting to carry provider meaning: members named or valued after
> fates/verdicts/D9/Coverage/frame types, an effectRequest asking the host to 'retry the analysis',
> a fault report embedding a claimed provider verdict, a cancel scoped to 'discard the last result'.
> Each is RF-5 (or RF-2 where the member is unknown) and the fixture proves the provider stream and
> the owning contract's view of it are bit-identical to the no-smuggling run - the attempt must be
> inert, not merely refused."

`$.hostileDualChannelConformance.classes[8]` — **CC-9**, `"pass-through byte identity under stress"`:

> "Chunk-boundary fuzzing on the data plane: 1-byte writes, maximum-size writes, pathological flush
> patterns, interleavings with heavy control traffic, cancellation mid-stream. Reassembled provider
> octet sequence identical to injected in every run; frame-boundary recovery under the owning
> contract's own in-band framing yields byte-for-byte equal frames in equal order. No fixture
> declares a subprotocol sensitive to carrier write boundaries: the pipe transport preserves none
> (nonTranslationObligation.octetIdentityProperty), so such a subprotocol is untransportable here by
> contract - a fixture-design error, not a conformance dimension."

`$.hostileDualChannelConformance.classes[9]` — **CC-10**, `"identity-binding mismatch"`:

> "helloAck echoing a wrong stableId, wrong digest, digest in wrong case or truncated; hello sent
> with a stableId/digest for a different admitted component. Each is RF-3 typed from either side; no
> session reaches select; the mismatch event is recorded once in the merged order."

`$.hostileDualChannelConformance.classes[10]` — **CC-11**,
`"non-canonical encoding indifference"`:

> "Semantically identical control messages serialized with different member orders, whitespace, and
> string escapes drive byte-different frames through identical protocol behavior: identical state
> transitions, identical merged event order, identical responses. The bound is the claim: these
> fixtures show serialization indifference on the exercised vectors and nothing more - a finite
> fixture set cannot prove the universal negative that no receiver anywhere compares control frames
> by bytes. That universal rule remains a specified obligation at
> controlFrameEncoding.nonCanonicalByConstruction; CC-11 is its testable witness, and any receiver
> whose behavior differs across these byte-different serializations fails."

**Supporting enumerations the classes reference** (needed to know what a golden must instantiate):

- `$.capabilityEnvelope.refusalFamilies.families[0..7]` — **RF-1..RF-8**, ids and names verbatim:
  RF-1 `control-version-unsupported`; RF-2 `frame-violation`; RF-3 `identity-binding-mismatch`;
  RF-4 `undeclared-capability`; RF-5 `semantic-content-request`; RF-6 `unauthorized-host-effect`;
  RF-7 `protocol-state-violation`; RF-8 `handshake-replay-or-downgrade`.
  `$.capabilityEnvelope.refusalFamilies.discipline`: "Typed, loud, terminal-for-the-channel, and
  surface-local: these family identifiers name control-plane refusal classes ONLY. They are not D9
  codes, not exit codes, not fates, and never map to any of those by this artifact - the mapping
  enters solely through DR-007's successor chain (identityDependencies ID-DEP-2)."
- `$.capabilityEnvelope.messageVocabulary` — the closed sixteen: `["hello","helloAck","select",
  "selectAck","refusal","ping","pong","cancel","health","healthReport","resourceReport","fault",
  "effectRequest","effectResult","shutdown","shutdownAck"]`.
- `$.transportAndFraming.framing.channelState` — the channel state machine CC-4 quantifies over:
  > "The control channel is a closed state machine: AWAIT-HELLO -> AWAIT-HELLO-ACK -> AWAIT-SELECT
  > -> AWAIT-SELECT-ACK -> STEADY -> TEARDOWN -> CLOSED, plus FAULTED reachable from every state."
- `$.handshake.sequence[0..3]` — the four handshake steps CC-4 and CC-6 quantify over:
  step 1 `hello (host -> component, fd3, seq 1)`; step 2 `helloAck (component -> host, fd4, seq 1)`;
  step 3 `select (host -> component)`; step 4 `selectAck (component -> host)`.
- `$.nonTranslationObligation.octetIdentityProperty` — the byte-opacity property the goldens judge
  against, whose operative clause is: "the octet sequence the component emits on fd1 is exactly the
  octet sequence the owning provider contract's host-side participant receives - equal length, equal
  bytes, equal order - and symmetrically for fd0 in the host-to-component direction. No insertion,
  deletion, substitution, reordering, or duplication of octets." and "after boundary recovery under
  the owning contract's own framing, the recovered frames must be byte-for-byte equal in equal order
  (judged exactly so by CC-1, CC-2, CC-9)."
- `$.nonTranslationObligation.noSuppressionRule` — bounds CC-1 and J-4's late-data half:
  "Suppressing provider octets IS assigning a fate: after cancel is issued and until data-plane EOF,
  arriving provider octets are still delivered unmodified in order to the owning contract's
  participant, which alone decides what late data means under its own rules. The control plane never
  closes, drains-to-null, or edits the data plane mid-stream; it only observes EOF and process death
  as events in the merged order."

**COORD D-111 — the sentence about goldens remaining named-not-authored.**
`docs/coop/COORDINATOR-DECISIONS.md` `1ee9def72c44acd96f36da3392d4980d0e06afb731b0a4003b5bde73247e136c`,
heading at line 4411 (`## D-111 — Record anti-lockstep-contract.v7 as DR-127's accepted
design-contract successor candidate`), inside the `- **Decision:**` block, **line 4442**, verbatim:

> "Hostile dual-channel goldens remain named, not authored here."

Its immediate neighbour, line 4443–4444, verbatim:

> "CC-1..CC-11 remain specifications (D-015), not this row's
> executed SATISFIED evidence."

D-111's status block records the standing that makes v7 usable as a governing byte:
`**ADOPTED 2026-08-15.** Turn 1 of 3: CONSENT from both independent reviewers, 0 MUST-FIX, 0
SHOULD-FIX.` and the subject digest
`8c41bddd7c351abc3a0b4b721f9302df29ba7d053352cb950ec8b23e4afdd671`.

## 2. Coverage set

Every explicit quantifier the governing bytes name, verbatim, grouped by axis.

**Axis A — the five golden axes named in the obligation and the file 08 cell.**
`anti-lockstep-leftover-join.v3.json#$.obligations[1].namedNotAuthored`, and identically
`08-decision-and-readiness-register.md:309` column 5 second limb:

> "hostile dual-channel race/fault/EOF/duplicate/teardown goldens with byte-opaque provider frames"

Enumerated, the five axes plus the qualifying property:

1. **race** — goldens over the cancellation-versus-result race.
2. **fault** — goldens over the control-fault-versus-provider-fault race.
3. **EOF** — goldens over EOF and process death.
4. **duplicate** — goldens over duplicate or late frames.
5. **teardown** — goldens over the teardown ladder.
6. **byte-opaque provider frames** — not a sixth axis but a property every golden must satisfy;
   defined at `control-protocol-contract.v2#$.hostileDualChannelConformance.discipline` ("Every
   class that touches the data plane judges provider semantic frames BYTE-FOR-BYTE against the
   injected reference stream") and at
   `anti-lockstep-contract.v7#$.raceCatalogByReference.byteOpacity` ("Provider semantic frames are
   compared byte-for-byte. The control plane may decide supervision/fate only under the owning
   contract.").

**Axis B — the five joins the goldens must exercise.** `control-protocol-contract.v2#$.joinPrecedenceTable.joins[i].id` /
`.race`, verbatim:

7. `joins[0].id` = `"J-1"`, `joins[0].race` = `"cancellation versus result"`.
8. `joins[1].id` = `"J-2"`, `joins[1].race` = `"control fault versus provider fault"`.
9. `joins[2].id` = `"J-3"`, `joins[2].race` = `"EOF/process death"`.
10. `joins[3].id` = `"J-4"`, `joins[3].race` = `"duplicate or late frames"`.
11. `joins[4].id` = `"J-5"`, `joins[4].race` = `"teardown"`.

**The five golden axes and the five joins are ordinally identical** — race→J-1, fault→J-2, EOF→J-3,
duplicate→J-4, teardown→J-5, matching each `joins[i].race` string word-for-word. That correspondence
is an observation from the two byte sets; **no artifact in the record states it**. See OQ-HG-3.

**Axis C — the eleven conformance classes the goldens must exercise.**
`control-protocol-contract.v2#$.hostileDualChannelConformance.classes[i].id` / `.name`, verbatim:

12. `classes[0]` — CC-1 `"race-ordering matrix"`.
13. `classes[1]` — CC-2 `"mid-frame interleave"`.
14. `classes[2]` — CC-3 `"duplicate/late/reordered control frames"`.
15. `classes[3]` — CC-4 `"EOF at every state"`.
16. `classes[4]` — CC-5 `"oversized and malformed framing"`.
17. `classes[5]` — CC-6 `"handshake downgrade and replay"`.
18. `classes[6]` — CC-7 `"subprotocol-name spoofing versus manifest declarations"`.
19. `classes[7]` — CC-8 `"fate-assignment smuggling"`.
20. `classes[8]` — CC-9 `"pass-through byte identity under stress"`.
21. `classes[9]` — CC-10 `"identity-binding mismatch"`.
22. `classes[10]` — CC-11 `"non-canonical encoding indifference"`.

**Axis D — fates.** The refusal families a golden's expected outcome may name.
`control-protocol-contract.v2#$.capabilityEnvelope.refusalFamilies.families[0..7]`:

23. RF-1 `control-version-unsupported`; RF-2 `frame-violation`; RF-3 `identity-binding-mismatch`;
    RF-4 `undeclared-capability`; RF-5 `semantic-content-request`; RF-6
    `unauthorized-host-effect`; RF-7 `protocol-state-violation`; RF-8
    `handshake-replay-or-downgrade` — **8 families**, closed.
24. Bounded by `$.capabilityEnvelope.refusalFamilies.discipline`: "They are not D9 codes, not exit
    codes, not fates, and never map to any of those by this artifact".

**Axis E — the within-class quantifiers. Named but NOT enumerated anywhere in the record.**
These are the reason a total case count cannot be supplied:

25. CC-1: "Every pairwise and every reachable total ordering of {cancel-issued,
    provider-final-octet, control-fault, provider-fault-report, provider-EOF, process-death,
    teardown-initiated}" — **7 events named**, but neither "every pairwise" nor "every reachable
    total ordering" is enumerated, and *reachable* is nowhere defined for this event set.
26. CC-2: "split at every byte offset of the provider frame's length prefix and at chunk sizes of 1
    byte" — offset count depends on the provider frame's length prefix width, which
    `control-protocol-contract.v2` does not fix for the data plane (it fixes the *control* frame
    encoding only, at `$.controlFrameEncoding`).
27. CC-4: "injected at EVERY channel state (AWAIT-HELLO through TEARDOWN) and at every handshake
    step boundary". The state machine *is* enumerated —
    `$.transportAndFraming.framing.channelState` names `AWAIT-HELLO -> AWAIT-HELLO-ACK ->
    AWAIT-SELECT -> AWAIT-SELECT-ACK -> STEADY -> TEARDOWN -> CLOSED, plus FAULTED`. "AWAIT-HELLO
    through TEARDOWN" reads as six of those eight, excluding CLOSED and FAULTED — but the record
    does not say so, and three injection kinds (fd3, fd4, fd1 EOF) plus process death are named
    without a product being stated. The handshake steps are enumerated at `$.handshake.sequence`
    (4 steps).
28. CC-5: "Length prefix 0; prefix exactly at, one over, and far over the operative bound (pre- and
    post-handshake bounds separately); truncated bodies; invalid UTF-8; duplicate members; unknown
    members; floats, negative and over-uint53 integers" — twelve injection kinds named, and
    `g21-leftover-join.v13.json#$.obligations[3].remainingNotAuthored.remainingCc5Injections`
    enumerates ten of them as still unauthored (see the overlap subsection below).
29. CC-7: "case variants, NFC/NFKC-equal-but-code-point-different variants, homoglyphs,
    trailing/leading whitespace, zero-width insertions, same string declared by a DIFFERENT
    stableId's manifest, and subprotocolVersion off-by-one" — seven mutation kinds, no per-kind
    vector count.
30. CC-9: "1-byte writes, maximum-size writes, pathological flush patterns, interleavings with heavy
    control traffic, cancellation mid-stream" — five stress kinds, "pathological" undefined.

**Arithmetic.**

- Closed, enumerated specification units the goldens must exercise: **5 joins (J-1..J-5) + 11
  classes (CC-1..CC-11) = 16**.
- Closed fate vocabulary available to those goldens: 8 refusal families (RF-1..RF-8).
- Golden *cases* per class: **not enumerable from the record.** Axis E's six quantifiers are named
  as universals ("Every pairwise and every reachable total ordering", "every byte offset", "EVERY
  channel state", "every handshake step boundary") without a member list or a product. Supplying a
  number here would be inventing the coverage set, which the D-293 default policy places outside the
  grant.

**Total coverage members: 16 named specification units (5 joins J-1..J-5 + 11 classes CC-1..CC-11),
each with a verbatim exact-byte `intent` or `rule` string. The per-class golden case count is NOT
enumerated anywhere in the record — see OQ-HG-5.**

### The overlap with G21's CC-1..CC-11 coverage

The same eleven CC classes appear as unauthored on a **different row under a different obligation
id**: `g21-leftover-join.v13.json`
sha256 `058717f51ee62e85fa3094e9a65c207fb78a7f706e57a35a854f1a9a55ecc66e`,
`$.obligations[3]` = `OBL-G21-FX-AUTHORING`, whose
`$.obligations[3].remainingNotAuthored.dr102` is verbatim:

```json
["CC-1","CC-2","CC-3","CC-4","remaining CC-5 injections","CC-6","CC-7","CC-8","CC-9","CC-10","CC-11"]
```

and whose `$.obligations[3].remainingNotAuthored.remainingCc5Injections` is verbatim:

```json
["CC-5 prefix exactly at the operative bound","CC-5 prefix far over the operative bound","CC-5 truncated bodies","CC-5 invalid UTF-8","CC-5 duplicate members","CC-5 unknown members","CC-5 floats","CC-5 negative integers","CC-5 over-uint53 integers","CC-5 prefix one over the postHandshake bound"]
```

Two CC-5 injections are **already authored** on the G21 side, per
`g21-leftover-join.v13.json#$.obligations[3].authoredImplementations`:
`"cc5LengthPrefix0": "G21.cc5.length-prefix-0 at g21-fixture-corpus.v7 (D-245)"` and
`"cc5PrefixOneOverPrehandshake": "G21.cc5.prefix-one-over-prehandshake at g21-fixture-corpus.v7
(D-245)"`, with per-platform copies at `g21-fixture-corpus.v8` (D-247)
sha256 `e8149a865e49bdcda9eda923e9918f332a83078f43ab6a3af9a10d6d31ef6359`.

**Does the record make one corpus serve both, or keep them separate?** The record **keeps the
custodies separate and does not say whether the bytes are shared.** What it does say, verbatim:

- `anti-lockstep-leftover-join.v3.json#$.doesNot[8]`: "Does not steal G21 leftover remaining on
  DR-114."
- `anti-lockstep-leftover-join.v3.json#$.doesNot[7]`: "Does not treat CC-1..CC-11 execution as
  SATISFIED evidence."
- `anti-lockstep-leftover-join.v3.json#$.executionRoutesVerbatim["CC-1-to-CC-11"]`: "DR-G21 /
  condition 4, and DR-012 qualification where that row applies. Specifications consumed, not
  SATISFIED evidence."
- `anti-lockstep-contract.v7.json#$.raceCatalogByReference.rule`: "This row CONSUMES those joins and
  classes. It does not copy them. Execution remains DR-G21 / condition 4 and DR-012 qualification
  where that row applies. D-015: DR-127 gains no design-level SATISFIED supplier from CC-1..CC-11
  existing."
- `control-protocol-contract.v2.json#$.hostileDualChannelConformance.discipline`: "The harness that
  executes these classes is DR-G21/blueprint work (identityDependencies ID-DEP-3)".
- `anti-lockstep-leftover-join.v3.json#$.basedOn.g16v2.role`: "G16 v2 does not apply v16 IR-1..IR-4
  / G16-12 and states hostile dual-channel goldens ride DR-127 / G21."

Read together: **execution** of CC-1..CC-11 is unambiguously G21's (`OBL-CC-EXECUTION`,
leftoverDesign false, existingGate DR-G21); **authoring the golden bytes** is measured
leftoverDesign true on *both* rows, under two different ids
(`OBL-HOSTILE-GOLDENS` on DR-127, `OBL-G21-FX-AUTHORING` on DR-G21). Nothing in the record says a
single authored byte set discharges both, and nothing says it cannot. `$.doesNot[8]` forbids DR-127
*claiming* G21's leftover as closed, which is a custody rule, not a byte-sharing rule. This is
unsettled: **OQ-HG-4**.

## 3. Prohibitions bounding the authoring

**From the join** `anti-lockstep-leftover-join.v3.json#$.doesNot` (19 entries), verbatim:

```
[0]  Does not SATISFY DR-127.
[1]  Does not open D-056 Class A.
[2]  Does not close leftover-design.
[3]  Does not add a DR-G* row.
[4]  Does not change live required-now 28.
[5]  Does not apply anti-lockstep-contract.v7.
[6]  Does not author hostile dual-channel goldens.
[7]  Does not treat CC-1..CC-11 execution as SATISFIED evidence.
[8]  Does not steal G21 leftover remaining on DR-114.
[9]  Does not retarget DR-107 or DR-110.
[10] Does not invent numeric windows.
[11] Does not mint a D-096 (A) grant.
[12] Does not evaluate versionConstraint.
[13] Does not produce a lock.
[14] Does not edit file 08.
[15] Does not invent a D9 code or a section 7.1 recipe.
[16] Does not authorize docs/v2/implementation/.
[17] Does not discharge CLAUDE-V7-A-1.
[18] Does not fold CLAUDE-V4-A-1..A-3, CLAUDE-V5-A-1..A-3, or CLAUDE-V6-A-1..A-3.
```

And `$.obligations[1].reason`, last sentence: "This join does not invent those golden bytes."

**From the consumed contract** `anti-lockstep-contract.v7.json#$.whatThisDoesNotDo` (8 entries),
verbatim:

```
[0] Does not SATISFY DR-127 until independently reviewed and recorded by a later D-000 MF-6.
[1] Does not fork or rewrite DR-102.
[2] Does not treat CC-1..CC-11 execution as this row's SATISFIED evidence.
[3] Does not adopt file 11 as a narrowing D-000.
[4] Does not evaluate DR-111 windows.
[5] Does not mint a D-096 (A) grant or defer an inside-slice DR-127 obligation.
[6] Does not authorize docs/v2/implementation/.
[7] Does not retarget anti-lockstep-contract.v1.json.
```

`$.raceCatalogByReference.rule` carries the sharpest one: "This row CONSUMES those joins and
classes. **It does not copy them.**" A golden corpus on DR-127 may cite J-1..J-5 and CC-1..CC-11 at
path + digest + JSON path; reproducing their definitions into a DR-127 artifact as if DR-127 owned
them would be the copy this forbids.

**From the class-defining contract** `control-protocol-contract.v2.json` — the clauses that bound
what a golden may fix:

- `$.joinPrecedenceTable.deadlineDiscipline`: "The numeric values are host operational configuration
  bound at blueprint/qualification, NOT here: a duration constant without a named runner and
  workload would be a threshold that measures nothing, and the containment harness (DR-G21) is where
  expiry behavior gets its goldens". A golden may not pin a timeout number. This is the byte behind
  join `$.doesNot[10]` ("Does not invent numeric windows").
- `$.controlFrameEncoding.nonCanonicalByConstruction`: "Consequently NOTHING may derive identity,
  signature, digest, equality-of-record, or any evidence commitment from control-frame BYTES;
  digests carried INSIDE control frames (for example admittedManifestDigest) are data computed by
  their owning surfaces over their own bytes, never by this protocol over its frames." A golden may
  not hash a control frame to identify it.
- `$.capabilityEnvelope.refusalFamilies.discipline`: "They are not D9 codes, not exit codes, not
  fates, and never map to any of those by this artifact - the mapping enters solely through DR-007's
  successor chain".
- `$.hostileDualChannelConformance.classes[8]` (CC-9), closing clause: "No fixture declares a
  subprotocol sensitive to carrier write boundaries: the pipe transport preserves none
  (nonTranslationObligation.octetIdentityProperty), so such a subprotocol is untransportable here by
  contract - **a fixture-design error, not a conformance dimension.**" This is the one place the
  record names a specific fixture-authoring mistake in advance.
- `$.hostileDualChannelConformance.classes[10]` (CC-11), bound clause: "The bound is the claim:
  these fixtures show serialization indifference on the exercised vectors and nothing more - a
  finite fixture set cannot prove the universal negative that no receiver anywhere compares control
  frames by bytes."
- `$.hostileDualChannelConformance.discipline`: "Fixture CLASSES with exact-byte intent … **not
  implementations.**"

**From `IMPLEMENTATION-FREEZE.md` §7.1** (the referent of join `$.doesNot[15]`, "Does not invent … a
section 7.1 recipe"): `docs/coop/IMPLEMENTATION-FREEZE.md`
sha256 `e809d4395f394a507c36c23c069d566c838b2283c931b6d2d13797be53406dbd`, line 1675
(`### 7.1 Parked identity recipes — named for escalation, NOT non-blocking`), line 1681 and
line 1711, verbatim:

> "Naming them makes escalation compliant. It does not make them optional and
> it does not authorise anyone to invent one."

> "Every row above must be closed by a binding artifact before signature. None may
> be closed by this record, by the blueprint, by a checker, or by an implementer."

**From the D9 class list** (the referent of join `$.doesNot[15]`, "Does not invent a D9 code"):
`docs/coop/artifacts/d9-exit-contract.v1.14.json`
sha256 `8dd3303855f49bfdbb2751ee65f54a906405f0654159ebe815472f73cdf7da31`, pinned live at file 08
line 40 (DR-007 source-pin cell). `$.codeVocabulary.closed` = `true`; `$.codeVocabulary.rule`:

> "A code outside this vocabulary is a contract violation. Codes are grouped by remedy: two codes
> with the same remedy are a smell, two remedies behind one code is a defect."

`$.codeVocabulary.errorCodes` includes `"SERVE.PROTOCOL_FAULT"` and
`"PROVIDER.PROTOCOL_VIOLATION"`. A golden that names an outcome must select from that closed list,
never mint. The RF families are explicitly *not* D9 codes (see the refusalFamilies discipline
above), so a golden's expected outcome is an RF family plus a merged-order assertion, not a D9 code.

**From COORD D-186** (the recording), lines inside the `- **Decision:**` block, verbatim:

> "Does not apply anti-lockstep-contract.v7. Does not author
> hostile dual-channel goldens. Does not invent numeric
> windows. Does not steal G21 leftover from DR-114. Does
> not rewrite G21, G31, or G32. Does not edit file 08.
> Does not invent a D9 code."

**The D-293 constraint clause that applies to this obligation.**
`DECISION-PACKETS/D1-fixture-authoring-delegation.claude-recommendation.r2.md`
sha256 `f530cedca1c799097ed0fc30cf8ec6f0480abe9a56d495236909a3a23b84fc33`, line 3, verbatim:

> "Effective only within already-recorded semantics: no adapter, CI encoding, journal, SDK API, new
> D9/HostTermination/pack semantics, reserved list, or number is authorised; G15, G16 and G18 keep
> their recorded prohibitions (adapter, CI encoding, journal)."

The words "**or number**" are the binding half here: they are the D-293-level restatement of join
`$.doesNot[10]` and of `$.joinPrecedenceTable.deadlineDiscipline`. And line 6, the default policy,
verbatim:

> "**Default policy (replaces round 1):** coverage, not one-case-per-member — every explicit
> platform, matrix, mutation, transition and fate quantifier in the governing bytes is preserved;
> for delegated byte sets, concrete witness bytes may be selected only within already-recorded
> schemas and fates, and any choice that would create a new semantic member, identifier, value, list
> or implementation stays outside the grant (recorded as a named open decision instead)."

The clause "every explicit … **transition** … quantifier … is preserved" is what makes J-5's
five-step teardown ladder (T-1..T-5) and the eight-state channel machine mandatory coverage rather
than optional.

## 4. Dependencies

**(a) The unenumerated CC-1 ordering set — the sharpest one.**
`control-protocol-contract.v2.json#$.hostileDualChannelConformance.classes[0].intent`, verbatim:

> "Every pairwise and every reachable total ordering of {cancel-issued, provider-final-octet,
> control-fault, provider-fault-report, provider-EOF, process-death, teardown-initiated} is
> exercised with scripted channel actors."

Seven events are named. **"Reachable" is not defined anywhere in the artifact**: there is no
reachability relation, no state-to-event map, and no enumeration of the admissible total orders.
J-3 constrains one of them ("Death is therefore always the LAST event of a child's merged order")
and J-5 constrains the teardown ladder's direction ("the ladder never skips backward"), but the
record nowhere composes those constraints into a member list. Choosing the set would create "a new
semantic … list" — outside the grant under the D-293 default policy. This does not block authoring
*some* CC-1 goldens; it blocks any claim that CC-1 is covered.

**(b) Numeric bounds the goldens reference but may not fix.**
`$.joinPrecedenceTable.deadlineDiscipline`, verbatim:

> "Every 'bounded wait' above MUST exist, MUST be finite, and its expiry MUST be a typed appended
> event - that is bound HERE. The numeric values are host operational configuration bound at
> blueprint/qualification, NOT here: a duration constant without a named runner and workload would
> be a threshold that measures nothing, and the containment harness (DR-G21) is where expiry
> behavior gets its goldens (identityDependencies ID-DEP-3)."

CC-4's pass property references "a hang without a bounded-wait expiry event" and J-5's ladder has
two bounded waits (T-2, T-3). A golden asserting *that* an expiry event is appended is authorable; a
golden asserting *when* is not. Same for CC-5's "operative bound" (pre- and post-handshake bounds
"separately") — `$.handshake.sequence[1]` fixes only `maxControlFrameBytes` as "at most the offer,
at least 65536", a negotiated value, not a constant. Bounded, not blocking, provided the goldens
stay on the existence half.

**(c) The owning provider contract's framing, for byte-opacity judging.**
`$.hostileDualChannelConformance.discipline`: "equality means equal octet sequences per frame **after
boundary recovery under the owning contract's own framing**". `$.nonTranslationObligation.
octetIdentityProperty` names the applied bindings: "Both existing majors frame IN-BAND
(length-delimited canonical CBOR, self-delimiting)". `$.transportAndFraming.
measuredProviderTransportBindings.typescriptMajor1` resolves that to `delivery.v2`'s bytes via
`delivery.v4` (sha256 `3cffece076289a4e62f3e0680cb8cc7c6a134b3190a6b39b7ec14b007704a121`;
`delivery.v2` sha256 `47b6cfd17338fafd407c554afe1951ab23d2896aac99bcfd272fc0894e3cabf3`). Those
bytes exist. Not blocking.

**(d) DR-102's own standing.** `control-protocol-contract.v2.json#$.status` =
`"CANDIDATE-NOT-APPLIED"`, `$.reviewStatus` = `"AWAITING-INDEPENDENT-REVIEW"`, `$.binds` =
`"NOTHING"`, and its review file on disk is `control-protocol-contract.v2.review-independent.json`
(a single verdict; no `.codex.` counterpart). So the contract whose classes the goldens must
exercise is itself unapplied and single-reviewed. That is the same standing as every other
governing byte in this plan (all the gate occupancies are CANDIDATE-NOT-APPLIED too), so it is not a
new blocker — but it does mean a golden corpus cites an unapplied specification, which
`$.raceCatalogByReference.rule` already anticipates ("Specifications consumed, not SATISFIED
evidence"). Not blocking; see §6 risk.

**(e) Not dependencies.** No reserved list, reserved number, reserved axis, undecided threshold, or
other gate's authored corpus is *required* before a DR-127 golden can be constructed. The class
definitions exist (dual-reviewed v7 pointing at a pinned v2), the fate vocabulary is closed
(RF-1..RF-8), the byte-opacity property is stated, and the file 08 acceptance-evidence cell is live
and unchanged. In particular:

- **The G21 corpus is not a prerequisite.** `g21-fixture-corpus.v1/v2/v7/v8` exist and authored two
  CC-5 injections, but nothing on DR-127 says the DR-127 goldens wait on them.
- **DR-117 Class A sequencing does not apply.** D-293 Decision 5 (COORD line 16228) orders "then
  G29/G30 fixture authoring" for DR-117 only; `OBL-HOSTILE-GOLDENS` is on DR-127 and appears in
  D-293 Decision 8's delegated list (COORD line 16264) with no ordering clause attached.
- **No DR-127-side sequencing clause exists.** `DECISIONS-RECOMMENDED.md`
  sha256 `42f27394746d4aac569a09a01da719c0cf318cf114086635e73097a6add97370` has no `## B`-series
  heading for DR-127; its only mentions of `OBL-HOSTILE-GOLDENS` are the D1 delegation list at
  line 253 and `DECISION-PACKETS/C5-9-reserved-encodings-owners-units.md` line 58, which records it
  as "`OBL-HOSTILE-GOLDENS` (rides DR-127)" in a not-leftover list for a different gate.

**Standing: NOT BLOCKED**

(The CC-1 ordering set at (a) blocks *claiming CC-1 coverage*, not authoring. A successor that
authors witnesses and records the unenumerated remainder as a named open decision is inside the
grant; one that asserts CC-1 complete is not.)

## 5. Recommended artifact shape

**Closest precedent: `docs/coop/artifacts/g21-fixture-corpus.v1.json`**
sha256 `861bb4e7d26a80158cc1cc3a0518c5e8e95311bee4d8c8ce63acd1e60d6c906d` (D-241) — the
**first-authoring** shape, payloads under `docs/coop/artifacts/fixtures/g21.v1/` with **no platform
subdirectory**. It is the closest for three reasons the record supports: it is the only corpus
lineage that authored against `control-protocol-contract.v2` classes (its later
`g21-fixture-corpus.v7` authored the two CC-5 injections named in
`g21-leftover-join.v13.json#$.obligations[3].authoredImplementations`); its payloads are `.bin`
rather than `.json`, matching a corpus of wire frames; and it carries a `failsIf` roster, which this
subject needs.

Top-level fields carried by `g21-fixture-corpus.v1.json` (verified key list):

`artifact, version, date, documentClass, registerRow, registerRowNote, namedGate, status,
reviewStatus, sealRecommendation, binds, authorityClaim, purpose, basedOn, parentReview, file08Pin,
head, requiredNowUnchanged, file08StatusToken, cborConstruction, pinnedHostContext, whatIsAuthored,
whatIsNotAuthored, authoredCatalog, leftoverDesignClosedIfAcceptedAndRecorded,
leftoverDesignRemainingOnG21, remainderAfterThisCorpus, summary, doesNot, failsIf, proposedLaterWork,
recordedInputs, remeasurementClause`

`$.authoredCatalog` keys: `standing, doesNotMutate, executionRemains, members`.
`$.authoredCatalog.members[i]` keys: `id, class, inputCorpusId, path, sha256, mutation, expected`.

The four-platform variant `g23-fixture-corpus.v4.json`
sha256 `b3fce9f5bab6764919f5dc43c28a43f3d9c3b6be310e45c2c1bd08a617c755c5` adds
`platformsQuotedFromOccupancyV2` and `windowsStandingQuotedFromOccupancyV2` and its members carry
`payloadSha256`, `snapshotMembership` and `platformCopies`.

**Proposed artifact name:** `docs/coop/artifacts/anti-lockstep-hostile-goldens.v1.json`
**Proposed fixture directory:** `docs/coop/artifacts/fixtures/anti-lockstep-goldens.v1/<id>.bin`,
mode 0444, no platform subdirectory. **First authoring** — no DR-127 golden corpus of any version
exists in `docs/coop/artifacts/`.

**Two structural departures this subject forces from the precedent, each with its governing byte:**

1. **No `namedGate`, no `file08StatusToken` from a `DR-G*` row, no occupancy pin.** The precedent
   corpora all carry `namedGate` (a `DR-G*` id) and pin an occupancy. This one has none
   (§1.3). It must instead pin the file 08 **acceptance-evidence cell** at line 309 column 5 —
   quoted byte-exact — plus `$.file08StatusToken` = `"OPEN"` from column 6, and cite the two
   contracts by path + sha256 + JSON path.
2. **No `inputCorpusId` per member.** The precedent's `$.authoredCatalog.members[i].inputCorpusId`
   points at a `*-input-corpus.vN` artifact. **No DR-127 input corpus exists** — there is no
   `anti-lockstep-input-corpus.*` in `docs/coop/artifacts/`. The initial states must be derived
   directly from the eleven CC `intent` strings and the five join `rule` strings. A successor should
   either author a `anti-lockstep-input-corpus.v1` first (the shape `g29-input-corpus.v1` /
   `g30-input-corpus.v1` demonstrate: `initialStates[]` with `id`, `classMemberVerbatim`,
   `stateNamed`, `source`, `fixtureBytes: "NOT-AUTHORED"`, `assertsNamedNotAuthored[]`), or carry an
   equivalent block inline and say so. See OQ-HG-6.

**Fields the successor should carry beyond the v1 skeleton**, each traceable to a governing byte:

- `file08AcceptanceEvidenceCellVerbatim` — line 309 column 5, quoted whole, with the semicolon split
  recorded so the AL-1..AL-5 limb is visibly not claimed.
- `consumesNotCopies` — restating `anti-lockstep-contract.v7#$.raceCatalogByReference.rule` ("It does
  not copy them") and citing J-1..J-5 / CC-1..CC-11 by `control-protocol-contract.v2` path + sha256 +
  JSON path rather than reproducing their text as owned definitions.
- `joinCoverage` — a J-1..J-5 map to authored golden ids.
- `classCoverage` — a CC-1..CC-11 map to authored golden ids, with an explicit
  `remainingNotAuthored` for every class whose within-class quantifier is unenumerated (Axis E).
- `byteOpacityConstruction` — how each golden judges provider-frame equality, quoting
  `$.nonTranslationObligation.octetIdentityProperty` and naming the owning contract's framing used
  for boundary recovery. (The analogue of `g21-fixture-corpus.v1#$.cborConstruction`.)
- `doesNotInventNumericWindows` — because join `$.doesNot[10]` and
  `$.joinPrecedenceTable.deadlineDiscipline` both bite.
- `doesNotStealG21Leftover` — because join `$.doesNot[8]` bites, and because the G21 overlap
  (OQ-HG-4) makes the temptation concrete.
- `cc1OrderingSetNotEnumerated` — a named open decision recording that "every reachable total
  ordering" has no member list in the record, so CC-1 is witnessed, not covered.
- `leftoverDesignRemainingOnDR127` — must stay non-empty and must still list
  `OBL-AL3-CORE-ROLLBACK` and `OBL-AL1-AL2-AL5`, which this corpus does not touch.

## 6. Effort and risk

**Number of cases:** not fixed by the record. The authorable floor is **16 witnesses** — one per
named specification unit (J-1..J-5, CC-1..CC-11) — which is the smallest set that touches every
enumerated member without inventing an axis. The ceiling is unbounded, because six of the eleven
classes carry universal quantifiers with no member list (Axis E). A first authoring in the
`g21-fixture-corpus.v1` shape would sensibly land in the 16–40 range, with an explicit
`remainingNotAuthored` block; the two-payload `g21-fixture-corpus.v1` and four-payload
`g23-fixture-corpus.v4` precedents show that a small, fully-declared first corpus is the accepted
form.

**(a) Witness-byte selections inside recorded schemas — permitted under the grant.**

1. Concrete control-frame bodies for each RF family exercised, within
   `control-protocol-contract.v2#$.controlFrameEncoding.messageEnvelope` ("Every frame body object
   has exactly these members: type …, seq …, controlMajor …, body …") and the closed sixteen-message
   `$.capabilityEnvelope.messageVocabulary`.
2. Concrete `seq` values for CC-3's "repeats, gaps, decreases", within the seq discipline J-4 names.
3. Concrete byte-offset split points for CC-2, and concrete chunk patterns for CC-9, chosen from the
   named kinds ("1-byte writes, maximum-size writes, pathological flush patterns").
4. Concrete injected provider octet sequences for the byte-opacity comparison — the *reference
   stream* — since `$.hostileDualChannelConformance.discipline` fixes only how equality is judged,
   not what is injected.
5. Concrete spoofing tokens for CC-7 within its seven named mutation kinds.
6. Concrete out-of-vocabulary member names for CC-8's smuggling attempts, within RF-5/RF-2.
7. The serialization of each payload and its `sha256` over those bytes.
8. Golden ids, following the recorded `G21.cc5.length-prefix-0` /
   `G21.cc5.prefix-one-over-prehandshake` naming shape rather than minting a new scheme.

**(b) Choices that would create new semantics — record as a named open decision, do not choose.**

1. **Enumerating CC-1's "every reachable total ordering" as a closed set.** Violates the D-293
   default policy ("any choice that would create a new semantic member, identifier, value, list or
   implementation stays outside the grant") because *reachable* is undefined in
   `control-protocol-contract.v2`. Record as a named open decision, do not choose.
2. **Fixing any bounded-wait duration, drain deadline, or CC-5 "operative bound" as a number.**
   Violates join `$.doesNot[10]` ("Does not invent numeric windows"),
   `$.joinPrecedenceTable.deadlineDiscipline`, and D-293's "or number is authorised" exclusion.
   Record as a named open decision, do not choose.
3. **Minting a D9 code or exit number for any golden's expected outcome, or mapping an RF family to
   one.** Violates join `$.doesNot[15]`, `$.capabilityEnvelope.refusalFamilies.discipline` ("never
   map to any of those by this artifact - the mapping enters solely through DR-007's successor
   chain"), and `d9-exit-contract.v1.14.json#$.codeVocabulary.rule`. Record as a named open
   decision, do not choose.
4. **Deriving any identity or digest from control-frame bytes.** Violates
   `$.controlFrameEncoding.nonCanonicalByConstruction` ("NOTHING may derive identity, signature,
   digest, equality-of-record, or any evidence commitment from control-frame BYTES"). Note this
   interacts with the corpus's own `sha256` fields: hashing a *payload file* is fine; hashing a
   control frame *as its identity on the wire* is not. Record as a named open decision, do not
   choose.
5. **Declaring a subprotocol sensitive to carrier write boundaries.** Named in advance as an error
   by `$.hostileDualChannelConformance.classes[8]`: "a fixture-design error, not a conformance
   dimension." Record as a named open decision, do not choose.
6. **Copying J-1..J-5 or CC-1..CC-11 definitions into a DR-127-owned artifact.** Violates
   `anti-lockstep-contract.v7#$.raceCatalogByReference.rule` ("It does not copy them"). Cite at
   digest instead. Record as a named open decision, do not choose.
7. **Claiming the goldens discharge `OBL-G21-FX-AUTHORING`, or that CC execution is DR-127's
   SATISFIED evidence.** Violates join `$.doesNot[7]`, `$.doesNot[8]`, and
   `$.raceCatalogByReference.rule`'s D-015 clause. Record as a named open decision, do not choose —
   this is exactly OQ-HG-4.
8. **Inventing a CC or J identifier, or a twelfth class.** The two sets are closed at eleven and
   five. Record as a named open decision, do not choose.
9. **Claiming `leftoverDesignClosedIfAcceptedAndRecorded: ["OBL-HOSTILE-GOLDENS"]`.** Six of eleven
   classes have unenumerated within-class quantifiers; the obligation cannot be exhausted by a first
   authoring. Record as a named open decision, do not choose.

**Risk.** The reviewer-attack pattern on the two recorded corpus lineages was (a) inventing a
vocabulary or encoding the record does not carry, (b) collapsing two classes the occupancy keeps
separate, (c) classifying a witness under a closed identifier it does not belong to, (d)
over-claiming closure. This subject is the most exposed of the four in this plan set, for a reason
that is structural rather than incidental: **it has no occupancy file.** Every other obligation in
D1 has a `harness.DR-G*` artifact with `exactByteIntent` and `passProperty` fields that a reviewer
can diff a corpus against. Here the reviewer has only two contracts on a different row (DR-102) and
one table cell, so a corpus must *manufacture* the mapping from cell wording to classes — and every
manufactured mapping is an (a)-class finding waiting to happen. The ordinal race→J-1 … teardown→J-5
correspondence in §2 is precisely such a manufactured mapping; it is obvious, and it is still not in
the record (OQ-HG-3).

On (c), the closed identifier risk is concrete and has already fired once on this exact contract:
`g21-fixture-corpus.v3/.v4.review-independent.codex.json` REJECTed with `G21FXV3-M1` — "The
non-object-top-level payload is an RF-2 case but is not authorized as a member of the closed CC-5
corpus" — and `G21FXV4-M1` recorded that the repair did not fully land it. That defect is a golden
correctly typed RF-2 but filed under the wrong CC class. A DR-127 corpus authoring across all eleven
classes multiplies that exposure elevenfold, and CC-3 (RF-7), CC-5 (RF-2), CC-6 (RF-1/RF-8), CC-7
(RF-4), CC-8 (RF-5/RF-2) and CC-10 (RF-3) are close enough in their refusal families that
misfiling is easy.

On (d), the over-claim risk is unusually sharp because the join carries **three** leftoverDesign-true
obligations and a corpus touching one of them must leave the other two visibly untouched:
`$.summary.leftoverDesign` = `["OBL-HOSTILE-GOLDENS","OBL-AL3-CORE-ROLLBACK","OBL-AL1-AL2-AL5"]`.
The `$.doesNotCloseLeftoverAlone` sentence — "Gates 2 and 3 do not hold. Class A is not opened. The
file 08 token stays OPEN. Not SATISFIED." — is the standing a successor must not disturb.

Two further risks specific to this subject:

- **Single-reviewer governing bytes.** `control-protocol-contract.v2` has one review file on disk
  (`control-protocol-contract.v2.review-independent.json`, no `.codex.` counterpart), unlike v7,
  which is dual ACCEPT 0/0. A corpus resting its class definitions on a single-reviewed DR-102
  candidate is weaker evidence than the g23/g21 corpora, which rested on dual-ACCEPT occupancies.
- **Stale `file08Pin` on the join.** §1.1 records the mismatch
  (`f909ddff…` pinned vs `e503b75b…` live). A successor must re-pin and state that the DR-127 row
  text is unchanged, or a reviewer will treat the corpus as measured against a file that moved.
  This is OQ-HG-1.

## 7. Open questions

**OQ-HG-1:** Does the stale `file08Pin` on `anti-lockstep-leftover-join.v3` need a join successor
before a golden corpus can cite it? `$.file08Pin.sha256` =
`"f909ddff7f3a8e9be864259808c4a2320170181001bdb746814b07393dd9d5e1"`; live file 08 is
`e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e`. `$.remeasurementClause` requires
re-measurement "If a cited file moves in a way that is not append-only COORD growth or COORD heading
hygiene", and file 08 is not COORD. The DR-127 row text at line 309 re-extracts byte-identically, so
nothing substantive moved — but whether a fixture corpus may cite a join whose own file-08 pin is
stale, or must wait for `anti-lockstep-leftover-join.v4`, is not settled.

**OQ-HG-2:** May a DR-127 golden corpus cite `control-protocol-contract.v2` directly?
`anti-lockstep-leftover-join.v3.json#$.recordedInputs` (15 entries) does **not** include
`control-protocol-contract.v2.json`; the join reaches it only through
`$.basedOn.contractV7` → `anti-lockstep-contract.v7.json#$.recordedInputs.governingSources[2]`.
Meanwhile `$.raceCatalogByReference.rule` says "This row CONSUMES those joins and classes. It does
not copy them." Whether a corpus on this row records DR-102's contract as a direct `recordedInputs`
entry (making it a first-class governing byte of a DR-127 artifact) or must cite it transitively
through v7 is not stated. The `DECISIONS-RECOMMENDED.md` A4 cross-lineage citation convention is
adopted "in principle" only (COORD D-293 Decision 4, lines 16222-16227: "its RULE-GOVERNED entry proceeds
through the dual-CONSENT cycle … regenerated as D-294 because this entry took D-293"), so the
convention that would settle this is itself unrecorded.

**OQ-HG-3:** Is the race/fault/EOF/duplicate/teardown ↔ J-1..J-5 mapping recorded anywhere?
The file 08 cell's five words and `$.joinPrecedenceTable.joins[i].race`'s five strings correspond
ordinally and word-for-word (race↔"cancellation versus result" as a race, fault↔"control fault
versus provider fault", EOF↔"EOF/process death", duplicate↔"duplicate or late frames",
teardown↔"teardown"). **No artifact states this mapping.** A corpus must assert it to organise its
coverage, and asserting it is a reading of two byte sets rather than a quotation. Whether that
reading is inside the grant, or is itself a named open decision, is unsettled.

**OQ-HG-4:** Does one authored byte set serve both `OBL-HOSTILE-GOLDENS` (DR-127) and the CC half of
`OBL-G21-FX-AUTHORING` (DR-G21), or are they separate corpora? The same eleven classes are measured
unauthored on both rows under different ids
(`anti-lockstep-leftover-join.v3.json#$.obligations[1]`;
`g21-leftover-join.v13.json#$.obligations[3].remainingNotAuthored.dr102`). The record separates
**custody** — `$.doesNot[8]` "Does not steal G21 leftover remaining on DR-114";
`$.executionRoutesVerbatim["CC-1-to-CC-11"]` "DR-G21 / condition 4 … Specifications consumed, not
SATISFIED evidence" — and separates **execution** (`OBL-CC-EXECUTION`, leftoverDesign false,
existingGate DR-G21). It says nothing about whether the golden *bytes* may be shared, nor whether
authoring on one row makes the other's measurement stale the way
`g21-leftover-join.v13.json#$.obligations[3].reason` records for NT-1/NT-2 ("leftover-design of
those two implementations is therefore stale as an authoring claim"). **Unsettled.**

**OQ-HG-5:** How many goldens does each class require? Six of the eleven classes carry universal
quantifiers with no member list: CC-1 ("Every pairwise and every reachable total ordering" of seven
events, *reachable* undefined), CC-2 ("every byte offset of the provider frame's length prefix",
width unfixed for the data plane), CC-4 ("EVERY channel state (AWAIT-HELLO through TEARDOWN)" — the
machine is enumerated at `$.transportAndFraming.framing.channelState` as eight states, but whether
"through TEARDOWN" includes or excludes CLOSED and FAULTED is not said — "and at every handshake
step boundary", four steps at `$.handshake.sequence`), CC-5 (twelve injection kinds, no per-kind
vector count), CC-7 (seven mutation kinds, no vector count), CC-9 ("pathological flush patterns",
undefined). The record names the axes and declines to enumerate their members, so no total is
derivable from bytes.

**OQ-HG-6:** Should a DR-127 input corpus be authored first? Every other D1 fixture obligation with
a completed INPUT layer has a `*-input-corpus.vN` artifact naming initial states with
`fixtureBytes: "NOT-AUTHORED"` (`g29-input-corpus.v1`
sha256 `7a176c542f2fb4db652671cfe1475bae4e22889efa0729a26f1338343317993b`; `g30-input-corpus.v1`
sha256 `5b23f3a6228a84a2945e21786f6a9b1549345c8aa6d851458dc2915a48e174e1`), and the precedent
corpora carry `$.authoredCatalog.members[i].inputCorpusId` pointing at it. **No DR-127 input corpus
exists** and `anti-lockstep-leftover-join.v3` names no obligation for one. Whether the goldens are
authored directly against the CC/J `intent` and `rule` strings, or whether an
`anti-lockstep-input-corpus.v1` should land first to match the recorded two-layer practice, is not
settled by the record.
