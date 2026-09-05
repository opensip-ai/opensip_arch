# D1 fixture-authoring plan records — index

Recorded at HEAD `8bc9963f68784842de643d5dbb1269bd4cf4411a`, 2026-08-28.

This directory is a **pre-authoring inventory** of the fixture obligations delegated to the
orchestrator by COORD `## D-293 — User decisions: adopt the agreed recommendations on
DECISIONS-NEEDED A–F`, Decision 8. It authors no fixture byte, records no successor artifact,
proposes no COORD entry, and decides nothing. Every claim in every file cites a path, a sha256, and
a JSON path or line number; every quoted string was re-extracted from the live bytes and
machine-verified against them.

## Scope

D-293 Decision 8 delegates **16 obligations**. They are written up in **15 files** — the two DR-122
SARIF obligations share `DR-122-SARIF.md` because both sit on one join, `sarif-leftover-join.v4`.

Owner-reserved and therefore absent from this directory (D-293 Decision 8, verbatim): "the gate
obligations at G07, G08, G09, G12, G14 and G22 (with every current same-id ROW twin);
`OBL-WINDOWS-PATH`, `OBL-ENVELOPE-MISMATCH`, `OBL-UNICODE-NORM`, `OBL-JOIN-FX-AUTHORING`,
`OBL-R10-AUTHORING`, `OBL-R6-AUTHORING`; and the G09/DR-105 decision-record envelope. G10 stays
selector-blocked; G22 stays reserved until C4 resolves."

## Shared pins

| Artifact | sha256 |
|---|---|
| `docs/v2/architecture/08-decision-and-readiness-register.md` | `e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e` |
| `docs/coop/COORDINATOR-DECISIONS.md` | `1ee9def72c44acd96f36da3392d4980d0e06afb731b0a4003b5bde73247e136c` |
| `docs/coop/artifacts/coordinator-decisions.D-056.turn2.draft.md` | `dfb0c2af39ff31df9bf3609c131f03ee2d87a585dcd684abd633d47ffb11ed82` |
| `DECISIONS-RECOMMENDED.md` | `42f27394746d4aac569a09a01da719c0cf318cf114086635e73097a6add97370` |

All 15 governing GATE/ROW leftover-joins carry **dual independent ACCEPT** (Claude 2 and Codex),
verified from the frozen `*.review-independent.*.json` verdict files.

## The table

Join and occupancy paths are relative to `docs/coop/artifacts/`. "Recorded at" gives the COORD
heading that recorded the artifact.

| # | Obligation | GATE join (sha256 / recorded at) | Occupancy (sha256 / recorded at) | Contract pinned | Coverage members | BLOCKED? | Precedent shape | Order |
|---|---|---|---|---|---|---|---|---|
| 1 | `OBL-FC-NONAUTH-TERM-FX` + `OBL-FC-OUTFAIL-FX` (DR-122) → [`DR-122-SARIF.md`](DR-122-SARIF.md) | `sarif-leftover-join.v4.json` `a2ab59d7…` / D-182 | none; file 08 DR-122 row L304 plays that role | `sarif-fc-nonauth-term-bind.v1.json` `5d2b7052…`, `sarif-fc-outfail-golden-bind.v1.json` `5bc60d33…` | **2 (A) + 2 (B) = 4** | **partly** — A not blocked; B blocked on `RUNID-RECIPE-PARK` for one of its two cases | `sarif-fc-*-bind` one-bind-per-class; first-authoring, no platform dirs | 1 |
| 2 | `OBL-G20-FX-AUTHORING` → [`G20.md`](G20.md) | `g20-leftover-join.v6.json` `d666a449…` / D-269 | `harness.DR-G20.component-operability.v2.json` `2c4823b7…` / D-217 | — | **40** (1 role × 8 surfaces × 4 platforms, + NT-4/NT-7 × 4) | no | `g23-fixture-corpus.v4` fields, `g21-fixture-corpus.v1` first-authoring layout | 2 |
| 3 | `OBL-G19-FX-AUTHORING` → [`G19.md`](G19.md) | `g19-leftover-join.v5.json` `d7bce01e…` / D-291 | `harness.DR-G19.state-class-authority.preview-classes.v2.json` `57f392b2…` / D-222 | — | **48** (2 classes × 4 ops × 4 platforms, + 4 cross-class × 4) | no | same as G20 | 3 |
| 4 | `OBL-HOSTILE-GOLDENS` (DR-127) → [`OBL-HOSTILE-GOLDENS.md`](OBL-HOSTILE-GOLDENS.md) | `anti-lockstep-leftover-join.v3.json` `820d724a…` / D-186 | none; file 08 DR-127 row L309 plays that role | `control-protocol-contract.v2.json` `c50a79fe…`; `anti-lockstep-contract.v7` (D-111) | **16** named specification units (J-1..J-5 + CC-1..CC-11); case count not fixed by the record | no | `g21-fixture-corpus.v1` first-authoring | 4 |
| 5 | `OBL-G21-FX-AUTHORING` → [`G21.md`](G21.md) | `g21-leftover-join.v13.json` `058717f5…` / D-292 | `harness.DR-G21.component-failure-containment.v4.json` `13addb3c…` / D-218 | `control-protocol-contract.v2.json` `c50a79fe…` | **128** *remaining* (32 remaining classes × 1 identity × 4 platforms) | no | its **own** v7/v8 lineage — a continuation, not a first-authoring | 5 |
| 6 | `OBL-G25-FX-AUTHORING` → [`G25.md`](G25.md) | `g25-leftover-join.v5.json` `9f2b137f…` / D-249 | `harness.DR-G25.preview-analyze-missing-rung.preview.v3.json` `4f124cd7…` / D-225 | `preview-analyze-contract.v2.json` `081ff7fb…` | **2** payloads / 6 obligations | **sequencing only** — DR-131 Class A opening | `g23-fixture-corpus.v3` first-authoring | 6 |
| 7 | `OBL-G26-FX-AUTHORING` → [`G26.md`](G26.md) | `g26-leftover-join.v4.json` `aba91c5a…` / D-251 | `harness.DR-G26.preview-analyze-sarif-not-advertised.preview.v2.json` `3a6f1379…` / D-226 | same | **3** payloads / 3 obligations | **sequencing only** — DR-131 | `g21-fixture-corpus.v1` lean first-authoring | 7 |
| 8 | `OBL-G27-FX-AUTHORING` → [`G27.md`](G27.md) | `g27-leftover-join.v4.json` `630b226a…` / D-252 | `harness.DR-G27.preview-analyze-not-sealed-run.preview.v2.json` `436a6011…` / D-227 | same | **3** payloads / 3 obligations | **sequencing only** — DR-131 (sealed-Run class is unauthored but is *not* a byte blocker) | `g21-fixture-corpus.v1` lean first-authoring | 8 |
| 9 | `OBL-G24-FX-AUTHORING` → [`G24.md`](G24.md) | `g24-leftover-join.v4.json` `c451f7ce…` / D-250 | `harness.DR-G24.preview-analyze-well-formed-admission.preview.v3.json` `ee41d14c…` / D-224 | same | **4** payloads / 12 obligations | **sequencing only** — DR-131 | `g23-fixture-corpus.v3` first-authoring | 9 |
| 10 | `OBL-G28-FX-AUTHORING` → [`G28.md`](G28.md) | `g28-leftover-join.v4.json` `604dc98d…` / D-253 | `harness.DR-G28.preview-analyze-host-must-not-mint.preview.v4.json` `e540ea53…` / D-228 | same + `d9-exit-contract.v1.14.json` `8dd33038…` | **4** payloads / EV-1..EV-4 over 2 classes | **sequencing only** — DR-131 (the D9 v1.14 class list is present and pinned) | `g23-fixture-corpus.v3` + `pinnedHostContext` D9 citation | 10 |
| 11 | `OBL-G30-FX-AUTHORING` → [`G30.md`](G30.md) | `g30-leftover-join.v4.json` `3f3d84e0…` / D-255 | `harness.DR-G30.preview-boundary-install-shape.preview.v2.json` `371695b8…` / D-230 | `product-boundary-successor-contract.v8.json` `52c70f77…` | **7** (4 initial states + 3 not-that-gate records) | **sequencing only** — DR-117 Class A opening | first-authoring, flat, mode 0444 | 11 |
| 12 | `OBL-G29-FX-AUTHORING` → [`G29.md`](G29.md) | `g29-leftover-join.v4.json` `9e1af4ba…` / D-254 | `harness.DR-G29.preview-boundary-excluded-form-admission.preview.v3.json` `94a40de9…` / D-229 | same | **10** (8 initial states + 2 not-that-gate records) | **sequencing only** — DR-117 | first-authoring, flat, mode 0444 | 12 |
| 13 | `OBL-G16-FX-AUTHORING` → [`G16.md`](G16.md) | `g16-leftover-join.v5.json` `7ce75ea5…` / D-278 | `harness.DR-G16.ci-isolation-integration.v5.json` `3e310749…` / D-215 | `monorepo-ci-contract.v16.json` | **24** class-level cells; the component multiplier is unenumerated | **BYTE** — `BLOCKED-ON-UNENUMERATED-COMPARISON-BASIS-COMPONENT-AXIS` | `g21-fixture-corpus.v1` first-authoring | 13 |
| 14 | `OBL-G18-FX-AUTHORING` → [`G18.md`](G18.md) | `g18-leftover-join.v6.json` `f531ba6a…` / D-276 | `harness.DR-G18.lifecycle-generation-recovery.v4.json` `2ce9aa52…` / D-216 | live file 04 (atomic-rename rule) | **40** (4 platforms × 10 initial states) | **BYTE** — `BLOCKED-ON-OBL-ENCODING-RESERVED` | `g21-fixture-corpus.v1` first-authoring | 14 |
| 15 | `OBL-AT-FX-AUTHORING` (G15) → [`G15.md`](G15.md) | `g15-leftover-join.v6.json` `4b2ac34c…` / D-290 | `harness.DR-G15.packaging-adapter-conformance.v9.json` `d82fac57…` / D-214 | `at-named-corpus-catalog.v1.json` `868bea85…` | **324** (27 AT-* keys × 12 reports) | **BYTE** — `BLOCKED-ON-OBL-ADAPTER-IMPL` | `g21-fixture-corpus.v1` first-authoring | 15 |

### ROW twins

Five obligations are measured `leftoverDesign: true` on **both** a GATE join and a ROW join with the
same id. Closing one requires a successor on both.

| Obligation | ROW twin | sha256 | Recorded at |
|---|---|---|---|
| `OBL-AT-FX-AUTHORING` | `packaging-leftover-join.v4.json` (DR-120) | `03251cc8…` | D-266 |
| `OBL-G16-FX-AUTHORING` | `monorepo-leftover-join.v4.json` (DR-121) | `03d4478c…` | D-277 |
| `OBL-G18-FX-AUTHORING` | `lifecycle-leftover-join.v4.json` (DR-107) | `bcc76ee3…` | D-275 |
| `OBL-G19-FX-AUTHORING` | `state-class-leftover-join.v4.json` (DR-124) | `16b00ce6…` | D-284 |
| `OBL-G20-FX-AUTHORING` | `sdk-leftover-join.v6.json` (DR-125) | `e91d6e92…` | D-267 |

G21, G24–G30, `OBL-HOSTILE-GOLDENS` and the two DR-122 obligations have no same-id ROW twin.

Two asymmetries found while checking these: `packaging-leftover-join.v4` carries **no** "does not
steal that leftover as a closure" sentence naming the G15 GATE join, unlike the G16/G18/G19 twins;
and `sdk-leftover-join.v6` contains neither the string `g20 leftover-join` nor `GATE` anywhere.
Recorded in `G15.md` and `G20.md` respectively.

## Suggested authoring order

The order is unblocked-and-simplest first, then the two sequencing-blocked groups kept together,
then the three byte-blocked obligations last. Positions 1–5 are the only ones that can be recorded
today.

**Tier 1 — no dependency; author now (positions 1–5).**

1. **`DR-122-SARIF.md`** — 4 cases, the smallest set and the only one whose case count is closed by
   the record. Obligation A's two cases are fully clear; obligation B has one clear case and one
   parked. Start here: it is the cheapest way to establish the D-000 review rhythm for this
   delegation.
2. **`G20.md`** — 10 payloads. One component role, eight surfaces, both already enumerated.
3. **`G19.md`** — 12 payloads, matching the 12 already-accepted `g19-input-corpus.v2` initial states.
4. **`OBL-HOSTILE-GOLDENS.md`** — 16 named specification units. Placed after G19/G20 because the
   record does not fix a case count, which is the single largest sizing risk in Tier 1.
5. **`G21.md`** — 32 remaining payloads, the largest set, but the best-precedented: it continues its
   own recorded v7/v8 lineage rather than starting one.

**Tier 2 — DR-131 preview gates, blocked on sequencing only (positions 6–10).** No byte dependency
in any of the five; the corpora can be drafted now and recorded after the DR-131 Class A opening.
Within the group, ascending by case count: **G25** (2), **G26** (3), **G27** (3), **G24** (4),
**G28** (4). They share one contract, `preview-analyze-contract.v2.json`
`081ff7fb529b34a3db3ac9f4c7505848e2253be12b5a867d39b49b3a26d56970`, so the section 1.5 work is done
once for all five.

**Tier 3 — DR-117 boundary gates, blocked on sequencing only (positions 11–12).** **G30** (7) then
**G29** (10). Both share `product-boundary-successor-contract.v8.json`
`52c70f7715fb869bae70bc588043dc5b4d731b73408d2d451e868b8de963f362`. D-293 Decision 5 puts
`preview-product-boundary-successor.v9`, then a fresh application-grade dual review, then the
owner-controlled opening entry, ahead of G29/G30 fixture authoring.

That first step is **in progress and has not passed**. As remeasured at 13:14 on 2026-08-28 (same
HEAD), `docs/coop/artifacts/preview-product-boundary-successor.v9.json` now exists — authored at
12:58 by a concurrent session, sha256
`e0221a1c095f688dcd5b127bce9f712543165599c71dc8415b94fb7bfdea4dd5`, untracked, `$.status`
`CANDIDATE-NOT-APPLIED`, `$.reviewStatus` `AWAITING-INDEPENDENT-REVIEW`, `$.binds` `NOTHING` — and
**both independent reviews returned REJECT**, with no
`^## D-.*preview-product-boundary-successor.v9` heading in COORD. `G29.md` and `G30.md` were written
before v9 appeared and each state that v9 does not exist; both now carry a dated correction block
recording the live state. The Tier 3 standing is unchanged by this and is, on these bytes,
strengthened.

**Tier 4 — byte-blocked; a prior decision is required (positions 13–15).** **G16**, then **G18**,
then **G15**. Each needs something the record does not yet carry, not merely an ordering step.

### The two sequencing constraints, verbatim

COORD `## D-293 …` Decision 5:

> **B1 (DR-131), B2 (DR-133), B3 (DR-117).** The agreed programmes are authorized in the agreed
> order — for DR-117: `preview-product-boundary-successor.v9` re-citing the twelve current joins and
> stating its relationship to `product-boundary-successor-contract.v8` (D-116); a fresh
> application-grade dual review bound to v9's final digest; then the owner-controlled opening entry;
> then G29/G30 fixture authoring; then a separate SATISFIED-GRADE + MF-6 cycle. The D-056 Class A
> openings themselves are separate owner-controlled entries; this entry opens none of them.

`DECISIONS-RECOMMENDED.md` §B1, `### Recommendation (Claude, round 2)`, item 4:

> 4. G24–G28 fixture authoring (D1) before the separate DR-131 SATISFIED-GRADE + MF-6 cycle — as
>    conservative sequencing, not as a precedent-proven automatic reopening of gate 2.

Whether "the agreed order" gates the *recording act* or only the later SATISFIED-GRADE cycle is not
settled by the bytes; it is recorded as an open question in each of the seven affected files
(`OQ-G24-4`, `OQ-G25-4`, `OQ-G26-4`, `OQ-G27-4`, `OQ-G28-5`, and the G29/G30 equivalents) rather
than resolved here.

## The three byte dependencies, verbatim

- **G15 — `BLOCKED-ON-OBL-ADAPTER-IMPL`.** `harness.DR-G15.packaging-adapter-conformance.v9.json`
  `$.at8.identityCase`: "AT-ARCHIVE-IDENTITY is two adapter RUNS with identical CI-1/CI-5 pins
  emitting identical archive bytes and archiveDigest." — with the same file's `$.slice1Adapter`
  ending "Adapter implementation remains reserved (D-108)." Whether AT fixture *bytes* depend on the
  adapter or only AT *execution* does is itself unresolved — the D1 packet already records it at
  `DECISION-PACKETS/D1-fixture-authoring-delegation.md` §7 item 4, and `G15.md` cites that rather
  than resolving it.
- **G16 — `BLOCKED-ON-UNENUMERATED-COMPARISON-BASIS-COMPONENT-AXIS`.** Not blocked on the CI
  encodings: the six `reservedForBlueprint` members of `monorepo-ci-contract.v16.json`
  (`$.reservedForBlueprint`, 6 entries) are expressly *not* the impact authority, and expressing one
  **fails** the class — `harness.DR-G16.ci-isolation-integration.v5.json`
  `$.namedCorpusClasses[0].passProperty` ends "CI vendor/YAML/path-filter authority fails this
  class." — so `OBL-CI-ENCODING-RESERVED` is not a precondition. What blocks it is that "one cell
  per declared comparison-basis component identity" has no members anywhere in the record.
- **G18 — `BLOCKED-ON-OBL-ENCODING-RESERVED`.** The settling sentence is the occupancy's
  `$.retainedEvidence[1].exactByteIntent`: "Quarantine is required; on-disk quarantine format is
  reserved."

Two contingencies that resolved the *opposite* way to expectation, and are therefore **not**
blockers: G27's sealed-Run class is undefined anywhere in `docs/`, but the occupancy designs the
fixture around that absence (`$.retainedEvidence[0].exactByteIntent`: "This specification does not
invent a sealed-Run class against which to compare; it retains the absence of that label."); and
G28's D9 v1.14 class list **is** present and already pinned, at
`docs/coop/artifacts/d9-exit-contract.v1.14.json`
`8dd3303855f49bfdbb2751ee65f54a906405f0654159ebe815472f73cdf7da31`.

## Recorded precedent these plans follow

Six ADOPTED orchestrator-authored fixture-corpus recordings, none CONTESTED:

| COORD | Artifact |
|---|---|
| D-237 (L11190) | `g23-fixture-corpus.v3` — G23 leftover-design fixture implementations |
| D-239 (L11325) | `g23-fixture-corpus.v4` — G23 per-D-002-platform copies |
| D-241 (L11465) | `g21-fixture-corpus.v1` — G21 NT-1/NT-2 fixture implementations |
| D-243 (L11614) | `g21-fixture-corpus.v2` — G21 per-D-002-platform copies |
| D-245 (L11761) | `g21-fixture-corpus.v7` — G21 CC-5 prefix injections |
| D-247 (L11944) | `g21-fixture-corpus.v8` — G21 per-D-002-platform copies of two CC-5 payloads |

**Two acts per gate, verified on disk.** A first-authoring corpus puts payloads flat under
`fixtures/<gate>.vN/`; a separate later version puts per-platform copies under
`fixtures/<gate>.vM/<platform>/`, four platform directories named `linux-arm64`, `linux-x86_64`,
`macos-arm64`, `macos-x86_64`, from the JSON tokens `"macos/arm64"`, `"macos/x86_64"`,
`"linux/x86_64"`, `"linux/arm64"`. Every plan file's section 5 states which of the two acts it is
proposing.

**Cost, from the frozen verdicts.** `g23-fixture-corpus.v1` was REJECT at 5 MUST-FIX and 4
SHOULD-FIX; `v2` REJECT at 1 MUST-FIX (collapsing EV-2 into EV-3 against an explicit non-collapse
requirement); `v3` and `v4` dual ACCEPT. `g21-fixture-corpus.v3` and `v4` were Codex REJECT on
`G21FXV3-M1` / `G21FXV4-M1` (a payload classified under a closed identifier it did not belong to),
`v5` and `v6` on SHOULD-FIX about the repair history; `v7` and `v8` dual ACCEPT. Three of the four
first-authoring acts needed two or three rounds. **Both per-platform-copy acts passed first time.**

The four reviewer-rejection patterns that recur — invented vocabulary or encoding, collapsing two
classes the occupancy keeps separate, classifying a witness under a closed identifier, over-claiming
closure — are written into each file's section 6 risk paragraph.

## Open questions

**99 across the fifteen files**, all recorded rather than resolved: SARIF 9, G15 5, G16 5, G18 6,
G19 6, G20 9, G21 15, G24 5, G25 5, G26 5, G27 5, G28 6, G29 6, G30 6, HOSTILE-GOLDENS 6.

Three are cross-cutting and belong to no single file:

- **OQ-X1 — stale occupancy version tokens.** The obligation `reason` text on six joins names an
  earlier occupancy version than the same join's `basedOn` marks as current: G24 says "G24 v1"
  (current v3), G25 "G25 v2" (v3), G26 "G26 v1" (v2), G27 "G27 v1" (v2), G28 "G28 v3" (v4), G29
  "G29 v2" (v3). Verified example: `g25-leftover-join.v5.json#$.basedOn.occupancyV3.role` = "Current
  G25 occupancy remasurement…" while `#$.basedOn.g25v2.role` = "Predecessor occupancy… Occupancy v3
  is the current occupancy remasurement of that identifier." The joins do not state which version's
  cell text governs a corpus. G15, G16, G18, G19, G20, G21 and G30 have no such gap. Every plan file
  used the version the join's `basedOn` marks current, and says so.
- **OQ-X2 — the platform axis on the preview gates.** None of the G24–G28 occupancies has a
  `platforms` array, yet all five carry `$.proposedLaterWork[2]` naming "on the four D-002
  platforms" without enumerating them; G24 additionally carries `$.d002Standing` "The live G24 cell
  has no platform matrix; platforms are not live-cell members." The recorded practice for a gate
  whose occupancy lacks the array is `g21-fixture-corpus.v8`, which quotes G10 occupancy v2 and
  checks ORDERED-EQUAL against G23 occupancy v2. Whether each preview gate needs a copy version at
  all is left open per gate.
- **OQ-X3 — concurrent writes under `docs/` during this inventory.** Two other workstreams wrote
  into `docs/coop/artifacts/` while these files were being measured, so several files record a state
  that has since moved even though HEAD did not. Neither was produced by this task; nothing under
  `docs/` was modified by it, and `git status` shows no tracked-file change there.
  - The A4 cross-citation-convention cycle authorized by D-293 Decision 4:
    `_dispatch.D-294.txt`, `-t2`, `-t3`, `coordinator-decisions.D-294.draft.md`,
    `.review-prompt.md`, `.review-adversarial.codex.json`, from 12:18 onward. If D-294 is recorded,
    the COORD digest pinned by all fifteen files changes and every remeasurement clause is engaged.
  - The DR-117 step-1 authoring: `_dispatch.ppbs-v9.txt` and
    `preview-product-boundary-successor.v9.json` plus its two review verdicts, 12:58–13:08, both
    **REJECT**. This is the change that made the v9-absence bullet in `G29.md` and `G30.md` stale;
    both carry a dated correction block.

  The general point for anyone reading these files later: each pins HEAD `8bc9963` and a set of
  digests, but the untracked working tree under `docs/coop/artifacts/` is being written to by other
  sessions, so a digest recomputation is the only safe check before acting on any of them.

## What is in each file

1. Governing bytes — 1.1 GATE join, 1.2 the obligation object verbatim, 1.3 occupancy fields that
   name the fixture cells (the `exactByteIntent` strings quoted in full), 1.4 ROW twin, 1.5 the
   governing contract.
2. Coverage set — every explicit quantifier, verbatim, with source, grouped by axis, with the
   arithmetic shown.
3. Prohibitions — every `does not` / `doesNot` / `failsIf` / `whatIsNotAuthored` clause that bounds
   the authoring.
4. Dependencies, ending in a `**Standing:**` line.
5. Recommended artifact shape, naming the precedent file and its field list.
6. Effort and risk — case count, then witness-byte selections permitted under the grant versus
   choices that would create new semantics and must be recorded as named open decisions instead.
7. Open questions.
