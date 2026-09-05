# DR-122-SARIF — OBL-FC-NONAUTH-TERM-FX and OBL-FC-OUTFAIL-FX — D1 fixture-authoring plan record

Recorded at HEAD `8bc9963f68784842de643d5dbb1269bd4cf4411a`. This is an inventory of already-recorded
bytes. It authors no fixture byte, records no successor, and decides nothing.

This file covers **two** obligations that sit on one join. Where they differ, the sections split
**A** (`OBL-FC-NONAUTH-TERM-FX`) and **B** (`OBL-FC-OUTFAIL-FX`). Section 1.2 splits into **1.2a**
and **1.2b**, one obligation object each.

## 1. Governing bytes

### 1.1 GATE leftover-join

Both obligations are **ROW-only**, on the DR-122 architecture-row leftover-join, not on a `DR-G*`
gate join. `DECISION-PACKETS/D1-fixture-authoring-delegation.md`
sha256 `bc8484cc7159af26a142b97a55b1095049f7ea2ac10c283cd1e2428ba2569ea9` places both in
`### 3.3 ROW-only fixture obligations (8 measurements, 8 distinct ids)`.

- Path: `docs/coop/artifacts/sarif-leftover-join.v4.json`
- sha256: `a2ab59d79051337906ae610b4c34f8203dcac0d9038f2826b32f68630bd07640`
- `$.artifact` = `"sarif-leftover-join.v4"`
- `$.version` = `4`
- `$.date` = `"2026-08-21"`
- `$.documentClass` = `"DESIGN-CONTRACT-CANDIDATE"`
- `$.registerRow` = `"DR-122"`
- `$.status` = `"CANDIDATE-NOT-APPLIED"`
- `$.reviewStatus` = `"AWAITING-INDEPENDENT-REVIEW"`
- `$.sealRecommendation` = `"DO-NOT-SEAL"`
- `$.binds` = `"NOTHING"`
- `$.head` = `"4141d36077ea0aad23c5569c0d246b142f0425f1"`
- `$.requiredNowUnchanged` = `28`
- `$.file08StatusToken` = `"PROPOSED-CLOSED-FOR-REVIEW"` (note: not `OPEN`, unlike every gate join
  in this plan set — it is DR-122's own live token, matching file 08 line 304 column 6)

COORD heading that recorded it (`docs/coop/COORDINATOR-DECISIONS.md`
`1ee9def72c44acd96f36da3392d4980d0e06afb731b0a4003b5bde73247e136c`, line 7786), verbatim:

> `## D-182 — Record sarif-leftover-join.v4 as DR-122 leftover remasurement`

**`$.file08Pin` is stale against live file 08.** The join carries:

```json
{
  "path": "docs/v2/architecture/08-decision-and-readiness-register.md",
  "sha256": "f909ddff7f3a8e9be864259808c4a2320170181001bdb746814b07393dd9d5e1"
}
```

Live file 08 at HEAD hashes to `e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e`.
`$.recordedInputs["docs/v2/architecture/08-decision-and-readiness-register.md"]` carries the same
stale value. The DR-122 row text re-extracts byte-identically from live file 08 line 304 (quoted in
§1.5), so nothing substantive moved. `$.remeasurementClause`, verbatim:

> "If a cited file moves in a way that is not append-only COORD growth or COORD heading hygiene,
> with file 08, contract v15, leftover-join v1/v2/v3, advertisement table v1, FC-OUTFAIL bind v1,
> FC-NONAUTH-TERM bind v1, G26 v1, D-056 turn-2 draft, and this draft unmoved, re-measure before
> recording. recordedInputs.HEAD must equal the top-level head. This join does not unwrite D-167
> through D-181. Frozen v3 remains a historical measurement as of HEAD 5d5d778."

See OQ-SARIF-1.

`$.leftoverDesignOpenStanding`, verbatim:

> "The live DR-122 token is PROPOSED-CLOSED-FOR-REVIEW. leftover-design of the FC-APPLIC table, the
> FC-OUTFAIL bind, and the FC-NONAUTH-TERM bind is stale as an authoring claim. leftover-design of
> executable fixture bytes remains. Inactive FC-PARITY/FC-LOSS/FC-NONAUTH-COVERAGE wait on DR-006."

`$.summary`, the parts that matter:

- `$.summary.leftoverDesign` = `["OBL-FC-OUTFAIL-FX","OBL-FC-NONAUTH-TERM-FX"]` — **exactly the two
  obligations this file covers, and nothing else.**
- `$.summary.specifiedNotLeftover` = `["OBL-PREVIEW-NOT-ADVERTISED","OBL-G17","OBL-FC-APPLIC",
  "OBL-FC-OUTFAIL","OBL-FC-NONAUTH-TERM"]`
- `$.summary.fixturesExecuted` = `false`; `$.summary.sarifAdvertised` = `false`;
  `$.summary.g17Resurrected` = `false`; `$.summary.classAOpened` = `false`;
  `$.summary.requiredNowUnchanged` = `28`.

`$.doesNotCloseLeftoverAlone`, verbatim:

> "This candidate does not make DR-122 D-056-eligible. OBL-FC-OUTFAIL-FX and OBL-FC-NONAUTH-TERM-FX
> remain leftover-design. OBL-FC-APPLIC, OBL-FC-OUTFAIL bind, and OBL-FC-NONAUTH-TERM bind authoring
> are measured closed. Gates 2 and 3 do not hold. Class A is not opened. The file 08 token stays
> PROPOSED-CLOSED-FOR-REVIEW. Not SATISFIED."

`$.liveGateOwners` = `{"DR-G26": "Output/operability + CLI/product owners"}` — names the *G26 gate*
owner. DR-122's own owner cell is file 08 line 304 column 3: `Output/operability owner + CLI/product
owner`.

**The six fixture classes and their preview standing.** `$.fixtureClassesVerbatim`, verbatim and
complete:

```json
[
  {"id": "FC-APPLIC", "previewStanding": "ACTIVE"},
  {"id": "FC-PARITY", "previewStanding": "INACTIVE"},
  {"id": "FC-LOSS", "previewStanding": "INACTIVE"},
  {"id": "FC-NONAUTH-TERM", "previewStanding": "ACTIVE"},
  {"id": "FC-NONAUTH-COVERAGE", "previewStanding": "INACTIVE"},
  {"id": "FC-OUTFAIL", "previewStanding": "ACTIVE"}
]
```

Three ACTIVE, three INACTIVE. The two obligations in this file are the fixture-byte halves of the
two ACTIVE classes that are not FC-APPLIC. The three INACTIVE classes are held by a separate
obligation, `$.obligations[8]`:

```json
{
  "id": "OBL-INACTIVE-DR006",
  "leftoverDesign": false,
  "existingGate": "none on DR-122. Deferred with DR-006.",
  "inactiveFixtureClasses": ["FC-PARITY","FC-LOSS","FC-NONAUTH-COVERAGE"],
  "executionObligationOwnerToday": "none on this row",
  "rideStanding": "deferred-to-DR-006",
  "reason": "v15 FC-PARITY, FC-LOSS, and FC-NONAUTH-COVERAGE have previewStanding INACTIVE and ride ID-DEP-S1/S2 / DR-006. They are not leftover-design to close on DR-122 while advertisement stays dropped. This join does not mint RunId/Finding recipes and does not restore SARIF advertisement."
}
```

`$.findingDisposition` records why the two bind obligations flipped to `leftoverDesign: false` at
this version, verbatim:

```json
[
  {"id":"FC-OUTFAIL-BIND-AUTHORED","severity":"MEASUREMENT","disposition":"ACCEPTED","landedAt":["obligations.OBL-FC-OUTFAIL","summary.specifiedNotLeftover"]},
  {"id":"FC-NONAUTH-TERM-BIND-AUTHORED","severity":"MEASUREMENT","disposition":"ACCEPTED","landedAt":["obligations.OBL-FC-NONAUTH-TERM","summary.specifiedNotLeftover"]}
]
```

### 1.2a The obligation object — OBL-FC-NONAUTH-TERM-FX (verbatim)

JSON path: **`$.obligations[5]`** of `docs/coop/artifacts/sarif-leftover-join.v4.json`. **Verified**:
the `obligations` array is, in order,
`[0] OBL-CONTRACT-V15, [1] OBL-PREVIEW-NOT-ADVERTISED, [2] OBL-G17, [3] OBL-FC-APPLIC,
[4] OBL-FC-NONAUTH-TERM, [5] OBL-FC-NONAUTH-TERM-FX, [6] OBL-FC-OUTFAIL, [7] OBL-FC-OUTFAIL-FX,
[8] OBL-INACTIVE-DR006, [9] OBL-G26, [10] OBL-ADVISORY-HONESTY` — 11 entries. Index 5 and index 7
are as the assignment states.

```json
{
  "id": "OBL-FC-NONAUTH-TERM-FX",
  "leftoverDesign": true,
  "existingGate": "none as authored implementations",
  "executionObligationOwnerToday": "none",
  "rideStanding": "not-capable-of-riding as execution-only remainder",
  "reason": "sarif-fc-nonauth-term-bind.v1 namedCases carry fixtureBytes NOT-AUTHORED. D-056 Decision clause 5: authoring fixtures remains design work, distinct from the bind. This join does not invent those bytes and does not mint a D9 code."
}
```

Field-by-field:

- `$.obligations[5].reason` — quoted in full. Three sentences: the bind's `namedCases` carry
  `fixtureBytes: "NOT-AUTHORED"`; D-056 clause 5 separates authoring from binding; and the two
  prohibitions ("does not invent those bytes", "does not mint a D9 code").
- `$.obligations[5].existingGate` = `"none as authored implementations"`.
- `$.obligations[5].rideStanding` = `"not-capable-of-riding as execution-only remainder"`.
- `$.obligations[5].executionObligationOwnerToday` = `"none"`.
- `namedCorpusNotAuthored`, `remainingNotAuthored`, `namedCases`, `namedNotAuthored` — **all absent**
  on this obligation object. The naming lives one level out, in the bind artifact the reason names.
  That indirection is what makes §1.3 below the occupancy-equivalent.

The **paired non-FX obligation** that holds the bind, `$.obligations[4]`, quoted because it fixes
what is and is not already closed:

```json
{
  "id": "OBL-FC-NONAUTH-TERM",
  "leftoverDesign": false,
  "existingGate": "none as a bind. Authored at sarif-fc-nonauth-term-bind.v1.",
  "executionObligationOwnerToday": "Output/operability owner + CLI/product owner",
  "rideStanding": "specified-not-leftover",
  "reason": "v15 FC-NONAUTH-TERM requires a renderer-chosen D9 refuse and a rewritten HostTermination refuse. Exact-byte intent now exists at sarif-fc-nonauth-term-bind.v1 (Claude ACCEPT 0/0; Codex not reviewed; CANDIDATE-NOT-APPLIED). Leftover-design of authoring that bind is therefore stale as an authoring claim. Remainder is executable fixture bytes. This join does not mint a D9 code, does not record that bind, and does not execute fixtures."
}
```

The operative split: **"Remainder is executable fixture bytes."**

### 1.2b The obligation object — OBL-FC-OUTFAIL-FX (verbatim)

JSON path: **`$.obligations[7]`** of `docs/coop/artifacts/sarif-leftover-join.v4.json` (verified
above).

```json
{
  "id": "OBL-FC-OUTFAIL-FX",
  "leftoverDesign": true,
  "existingGate": "none as authored implementations",
  "executionObligationOwnerToday": "none",
  "rideStanding": "not-capable-of-riding as execution-only remainder",
  "reason": "sarif-fc-outfail-golden-bind.v1 namedCases carry fixtureBytes NOT-AUTHORED. D-056 Decision clause 5: authoring fixtures remains design work, distinct from the bind. This join does not invent those bytes and does not mint a D9 code."
}
```

Field-by-field: identical shape to 1.2a, differing only in which bind the reason names.
`namedCorpusNotAuthored`, `remainingNotAuthored`, `namedCases`, `namedNotAuthored` — all absent.

The **paired non-FX obligation**, `$.obligations[6]`:

```json
{
  "id": "OBL-FC-OUTFAIL",
  "leftoverDesign": false,
  "existingGate": "none as a bind. Authored at sarif-fc-outfail-golden-bind.v1.",
  "executionObligationOwnerToday": "Output/operability owner + CLI/product owner",
  "rideStanding": "specified-not-leftover",
  "reason": "v15 requiredOutputFailure.ownerOfValues: D9 v1.14 already records the golden; the projection binds to it. That bind now exists at sarif-fc-outfail-golden-bind.v1 (Claude ACCEPT 0/0; Codex not reviewed; CANDIDATE-NOT-APPLIED). Leftover-design of authoring that bind is therefore stale as an authoring claim. Remainder is executable fixture bytes. This join does not mint a D9 code, does not record that bind, and does not execute fixtures."
}
```

**The two obligations are symmetric in shape and disjoint in subject.** Each bind's own
`whatThisDoesNotClose` says so: `sarif-fc-nonauth-term-bind.v1#$.whatThisDoesNotClose[0]` =
`"FC-OUTFAIL"`; `sarif-fc-outfail-golden-bind.v1#$.whatThisDoesNotClose[0]` = `"FC-NONAUTH-TERM"`.

### 1.3 The artifacts that play the occupancy role

**There is no `harness.DR-G*` occupancy for either obligation.** `$.registerRow` is `"DR-122"`, an
architecture row. The one harness file the join names is cited for exclusion:
`$.basedOn.g26v1.role` = "Cited only. G26 is the already-named preview-analyze SARIF-not-advertised
gate (D-152 / D-086). It does not SATISFY DR-122. This join does not steal G26 leftover from DR-131
and does not treat G26 existing as DR-122 SATISFIED evidence."

**What plays the occupancy role is the pair of bind artifacts named in the two reasons.** Each is
pinned in `$.basedOn` and listed in `$.recordedInputs`, and each carries the `namedCases` array that
*is* the coverage set.

#### A. `sarif-fc-nonauth-term-bind.v1`

- Path: `docs/coop/artifacts/sarif-fc-nonauth-term-bind.v1.json`
- sha256: `5d2b7052cf99200b1785250fded856df1ccefa15d97df95f72549a324e02c99c` (re-hashed at HEAD;
  matches `$.basedOn.nonauthBindV1.sha256` and `$.recordedInputs`)
- `$.artifact` = `"sarif-fc-nonauth-term-bind.v1"`, `$.version` = `1`, `$.date` = `"2026-08-16"`,
  `$.documentClass` = `"DESIGN-CONTRACT-CANDIDATE"`, `$.registerRow` = `"DR-122"`,
  `$.status` = `"CANDIDATE-NOT-APPLIED"`, `$.reviewStatus` = `"AWAITING-INDEPENDENT-REVIEW"`,
  `$.sealRecommendation` = `"DO-NOT-SEAL"`, `$.binds` = `"NOTHING"`,
  `$.head` = `"5d5d77819ae3019d9e6e02f1e66de3d93c060402"`, `$.requiredNowUnchanged` = `26`.
- `$.namedGate` = `"none. Host-owned projection non-authority bind. Does not occupy G26."`
- Review standing, `$.basedOn.nonauthBindV1.review` of the join: Claude
  `sarif-fc-nonauth-term-bind.v1.review-independent.claude2.json`
  `98215ee51ecb30a7b22b198a22c3c7ecc22c538de0aa4e9fc5cf44accf2d8148`, verdict
  `"Claude ACCEPT 0/0; Codex not reviewed"`. Role verbatim: "Independently reviewed exact-byte intent
  for the two live FC-NONAUTH-TERM negatives. CANDIDATE-NOT-APPLIED. Does not mint a D9 code.
  fixtureBytes NOT-AUTHORED. **Not recorded by any decision.**"

`$.authorityClaim`, verbatim:

> "This artifact BINDS FC-NONAUTH-TERM to the live v15 nonAuthority rules. The two required
> negatives are a renderer-chosen D9 refuse and a rewritten HostTermination refuse. It does not mint
> a D9 code. It does not choose which D9 a renderer attempts. It does not include Coverage
> preservation (FC-NONAUTH-COVERAGE remains INACTIVE on ID-DEP-S2). It does not author FC-OUTFAIL.
> It does not advertise SARIF. It does not resurrect G17. It does not SATISFY DR-122. It applies
> nothing and does not authorize docs/v2/implementation/."

`$.purpose`, verbatim:

> "Continue leftover-design of OBL-FC-NONAUTH-TERM / OBL-ACTIVE-FX-AUTHORING by stating exact-byte
> intent for the two live v15 negatives, without inventing a D9 code or executable fixture bytes."

`$.quotedNonAuthorityRules` — the four rules the goldens must exercise, verbatim:

```json
["A renderer cannot affect policy.","A renderer cannot affect evidence.","A renderer cannot affect sealed HostTermination.","A renderer cannot choose D9 or exit."]
```

**`$.namedCases` — the coverage set, both members verbatim with JSON paths:**

`$.namedCases[0]`:

```json
{
  "id": "FC-NONAUTH-TERM.renderer-chosen-d9-refuse",
  "fixtureBytes": "NOT-AUTHORED",
  "intentVerbatim": "a renderer-chosen D9",
  "passProperty": "A renderer-supplied D9 is refused. This artifact does not choose or mint the attempted code.",
  "doesNotInventD9": true
}
```

`$.namedCases[1]`:

```json
{
  "id": "FC-NONAUTH-TERM.rewritten-hosttermination-refuse",
  "fixtureBytes": "NOT-AUTHORED",
  "intentVerbatim": "a rewritten HostTermination refuse",
  "passProperty": "A rewritten HostTermination is refused."
}
```

Note the asymmetry: `namedCases[0]` carries a fifth field `doesNotInventD9: true`;
`namedCases[1]` does not.

Other scope-fixing fields, verbatim:

- `$.coveragePreservation` = `"EXCLUDED. v15 FC-NONAUTH-TERM: Does not include Coverage
  preservation. FC-NONAUTH-COVERAGE remains INACTIVE on ID-DEP-S2 / DR-006."`
- `$.ordinaryOutputFailure` = `"FC-OUTFAIL. Not this class."`
- `$.sarifAdvertisementRequired` = `false` — **the field that settles the D-077 tension for this
  obligation; see §4.**
- `$.whatThisClosesIfAcceptedAndRecorded` = `["FC-NONAUTH-TERM exact-byte intent for the two live
  negatives"]`
- `$.whatThisDoesNotClose` = `["FC-OUTFAIL","FC-NONAUTH-COVERAGE","executable FC-NONAUTH-TERM
  fixture bytes","OBL-ACTIVE-FX-AUTHORING as a whole","DR-122 leftover-design","DR-122 SATISFIED"]`
- `$.basedOn.contractV15.fcNonauthTermRequiresVerbatim` — the v15 requirement quoted inside the bind:
  > "Negative tests of renderer authority-injection on D9 and HostTermination only: a
  > renderer-chosen D9 and a rewritten HostTermination refuse. Does not include Coverage
  > preservation. Ordinary required serialization/atomic-write failure is FC-OUTFAIL. These tests do
  > not require SARIF to be advertised."
- `$.basedOn.contractV15.nonAuthorityVerbatim`:
  > "rendering success or failure cannot rewrite a committed Run or change policy, evidence, or its
  > sealed `HostTermination`. A renderer never chooses public termination or exit"

#### B. `sarif-fc-outfail-golden-bind.v1`

- Path: `docs/coop/artifacts/sarif-fc-outfail-golden-bind.v1.json`
- sha256: `5bc60d3364845d36f312d5fbbac02a9408551bff095179dfeb465370858da407` (re-hashed at HEAD;
  matches `$.basedOn.outfailBindV1.sha256` and `$.recordedInputs`)
- `$.artifact` = `"sarif-fc-outfail-golden-bind.v1"`, `$.version` = `1`, `$.date` = `"2026-08-16"`,
  `$.documentClass` = `"DESIGN-CONTRACT-CANDIDATE"`, `$.registerRow` = `"DR-122"`,
  `$.status` = `"CANDIDATE-NOT-APPLIED"`, `$.reviewStatus` = `"AWAITING-INDEPENDENT-REVIEW"`,
  `$.sealRecommendation` = `"DO-NOT-SEAL"`, `$.binds` = `"NOTHING"`,
  `$.head` = `"5d5d77819ae3019d9e6e02f1e66de3d93c060402"`, `$.requiredNowUnchanged` = `26`.
- `$.namedGate` = `"none. Host-finalization projection bind. Does not occupy G26."`
- Review standing, `$.basedOn.outfailBindV1.review` of the join: Claude
  `sarif-fc-outfail-golden-bind.v1.review-independent.claude2.json`
  `e479f1bb9dced073e7949c935bebeec3b39cb3fe4f523076475bc9063146c45f`, verdict
  `"Claude ACCEPT 0/0; Codex not reviewed"`. Role verbatim: "Independently reviewed bind of the
  host-finalization projection to the live D9 v1.14 machine-output-serialization-failed golden.
  CANDIDATE-NOT-APPLIED. Does not mint a D9 code. fixtureBytes NOT-AUTHORED. **Not recorded by any
  decision.**"

`$.authorityClaim`, verbatim:

> "This artifact BINDS the DR-122 host-finalization projection to the already-recorded D9 v1.14
> golden machine-output-serialization-failed. v15 requiredOutputFailure.ownerOfValues states that D9
> v1.14 already records this golden and that v15 does not mint a new D9 code or a new exit number.
> This artifact quotes those live bytes. It does not mint a D9 code. It does not mint an exit
> number. It does not store exitCode on HostTermination. It does not advertise SARIF. It does not
> resurrect G17. It does not author FC-NONAUTH-TERM. It does not SATISFY DR-122. It applies nothing
> and does not authorize docs/v2/implementation/."

`$.purpose`, verbatim:

> "Continue leftover-design of OBL-FC-OUTFAIL / OBL-ACTIVE-FX-AUTHORING by binding the projection to
> the live D9 v1.14 golden, without inventing a D9 code, an exit number, a CommandEnvelope, or
> executable fixture bytes."

**`$.namedCases` — the coverage set, both members verbatim with JSON paths:**

`$.namedCases[0]`:

```json
{
  "id": "FC-OUTFAIL.committed-run-preserved",
  "fixtureBytes": "NOT-AUTHORED",
  "intentVerbatim": "if an authoritative Run was already committed, preserve its identity and sealed termination"
}
```

`$.namedCases[1]`:

```json
{
  "id": "FC-OUTFAIL.no-committed-run",
  "fixtureBytes": "NOT-AUTHORED",
  "intentVerbatim": "Help/version or any command with no committed Run MUST NOT acquire a fictitious Run/RunId."
}
```

Note: unlike the FC-NONAUTH-TERM cases, **neither FC-OUTFAIL case carries a `passProperty` field.**
The pass condition lives instead in the quoted D9 golden and in v15's `requiredOutputFailure`
(quoted below). See OQ-SARIF-3.

The quoted live bytes this bind pins, verbatim:

`$.quotedD9Golden`:

```json
{
  "id": "machine-output-serialization-failed",
  "scenarioVerbatim": "a host-finalization projection: the requested CommandEnvelope cannot be serialized or atomically written; scenarioAxes.lifecycle and durability describe ONLY the failing output operation. If an authoritative Run was already committed, its identity and sealed termination remain; the command still ends operational-failed with OUTPUT.SERIALIZATION_FAILED",
  "expectedTerminationVerbatim": {"class": "operational-failed", "errorCode": "OUTPUT.SERIALIZATION_FAILED"},
  "hostFinalizationProjectionVerbatim": {"describes": "the failing host output operation only", "preservesSettledRun": true, "doesNotClaimUniversalLifecycle": true},
  "projectionScopeVerbatim": "host-finalization-only"
}
```

`$.quotedClassToExitCode`:

```json
{
  "operational-failed": 4,
  "source": "d9-exit-contract.v1.14 classToExitCode.operational-failed",
  "exitCodeInPayloadVerbatim": "NOT a union field. exitCode is derived from class via classToExitCode and must not be stored on HostTermination, so the two can never disagree (A2-D9-V12-01)."
}
```

`$.quotedV15OwnerOfValues`:

> "D9 v1.14 already records this golden. This artifact binds the projection to that golden. It does
> not mint a new D9 code or a new exit number."

`$.whatThisClosesIfAcceptedAndRecorded` = `["FC-OUTFAIL projection-bind to the live D9 v1.14 golden"]`.
`$.whatThisDoesNotClose` = `["FC-NONAUTH-TERM","executable FC-OUTFAIL fixture bytes",
"OBL-ACTIVE-FX-AUTHORING as a whole","DR-122 leftover-design","DR-122 SATISFIED"]`.

**Both binds are stale in their own file08Pin and head.** Each carries
`$.file08Pin.sha256` = `"3a9442d1761864de59f103374489a9fbffdd12cc4ba39ddd7c7f491f64357e44"`,
`$.head` = `"5d5d77819ae3019d9e6e02f1e66de3d93c060402"` and `$.requiredNowUnchanged` = `26` —
one generation older than the join's own stale pin, and two generations older than live. The
`sarif-leftover-join.v4` re-measurement at HEAD `4141d36` is what carries them forward. See
OQ-SARIF-1.

**Fields a gate occupancy would have that these binds do not.** No `platforms`, no
`windowsStanding`, no `retainedEvidence[]`, no `failsIf`, no `liveRowVerbatim`, no
`liveHarnessCellVerbatim`, no `namedCorpusClasses[]`, no `exactByteIntent` (the equivalent is
`namedCases[i].intentVerbatim`), no `liveGateOwner`. Both carry `doesNot`,
`whatThisDoesNotClose`, `remeasurementClause` and `recordedInputs`.

### 1.4 ROW twin join (or: none)

**None, for either obligation.** Both are ROW-only:
`DECISION-PACKETS/D1-fixture-authoring-delegation.md`
sha256 `bc8484cc7159af26a142b97a55b1095049f7ea2ac10c283cd1e2428ba2569ea9`, §3.3, two rows verbatim:

> `| `sarif-leftover-join.v4` / `OBL-FC-NONAUTH-TERM-FX` | DR-122 `Output/operability owner + CLI/product owner` | `sarif-fc-nonauth-term-bind.v1 namedCases` | "sarif-fc-nonauth-term-bind.v1 namedCases carry fixtureBytes NOT-AUTHORED." | byte-set (goldens) | "does not mint a D9 code" |`

> `| `sarif-leftover-join.v4` / `OBL-FC-OUTFAIL-FX` | DR-122 `Output/operability owner + CLI/product owner` | `sarif-fc-outfail-golden-bind.v1 namedCases` | "sarif-fc-outfail-golden-bind.v1 namedCases carry fixtureBytes NOT-AUTHORED." | byte-set (goldens) | "does not mint a D9 code" |`

No GATE-side join carries either id. The packet's §3.2 cross-custody rule —

> "Closing a fixture obligation would require a successor on *both* the GATE join and its ROW twin,
> since the same id is measured true on both."

— is **inapplicable**. Closing either obligation needs a successor on `sarif-leftover-join` alone.
Because both obligations sit on the *same* join, a single `sarif-leftover-join.v5` could measure
both, but each still needs its own authored byte set.

### 1.5 Governing contract/spec the join pins

#### The class-defining contract — `sarif-projection-contract.v15`

Pinned at `$.basedOn.contractV15` and in `$.recordedInputs`.

- Path: `docs/coop/artifacts/sarif-projection-contract.v15.json`
- sha256: `8996a92d00ddd47d212dbeecaf51f25b77b90d87aaa618cda9ad00749fd1d589` (re-hashed at HEAD)
- `$.artifact` = `"sarif-projection-contract.v15"`, `$.version` = `15`, `$.date` = `"2026-08-15"`,
  `$.registerRow` = `"DR-122"`, `$.status` = `"CANDIDATE-NOT-APPLIED"`,
  `$.reviewStatus` = `"AWAITING-INDEPENDENT-REVIEW"`, `$.binds` = `"NOTHING"`.
- **Dual ACCEPT 0/0** (`$.basedOn.contractV15.reviews`): Claude
  `sarif-projection-contract.v15.review-independent.claude2.json`
  `fe5f55181b305c5cafd3993b672d30296b7d62c7f10dd236585a81bd99aaaad0`; Codex
  `sarif-projection-contract.v15.review-independent.codex.json`
  `9f402c72267ed7c92657a1aa38e4c0fc185a25eaf23bb7aad69042dd9dbfad76`. Recorded at **D-115**
  (COORD line 4612: `## D-115 — Record sarif-projection-contract.v15 as DR-122's accepted
  design-contract successor candidate`).
- `$.basedOn.contractV15.role` verbatim: "Accepted DR-122 design-contract successor candidate. Not
  applied. Not SATISFIED. binds NOTHING. Preview still does not advertise SARIF. G17 stays
  inapplicable. This join does not apply v15."

**A — the FC-NONAUTH-TERM class definition, `$.fixtureClasses[3]`, verbatim:**

```json
{
  "id": "FC-NONAUTH-TERM",
  "requires": "Negative tests of renderer authority-injection on D9 and HostTermination only: a renderer-chosen D9 and a rewritten HostTermination refuse. Does not include Coverage preservation. Ordinary required serialization/atomic-write failure is FC-OUTFAIL. These tests do not require SARIF to be advertised.",
  "previewStanding": "ACTIVE",
  "scope": "any host-owned projection including JSON; does not require SARIF advertisement",
  "ride": null,
  "rideNote": "Active host-projection fixture with no parked dependency for D9/HostTermination negatives."
}
```

**B — the FC-OUTFAIL class definition, `$.fixtureClasses[5]`, verbatim:**

```json
{
  "id": "FC-OUTFAIL",
  "requires": "Exact D9 v1.14 machine-output-serialization-failed golden at host-finalization-only scope: if an authoritative Run was already committed, preserve its identity and sealed termination; otherwise no Run identity is created. Public termination is operational-failed with OUTPUT.SERIALIZATION_FAILED; exit derives from classToExitCode (recorded 4). Help/version or any command with no committed Run MUST NOT acquire a fictitious Run/RunId.",
  "previewStanding": "ACTIVE",
  "scope": "host-finalization only; any host-owned required projection including JSON",
  "ride": null,
  "rideNote": "Active host-projection fixture with no parked dependency. ride:null is the explicit representation, same as FC-APPLIC."
}
```

**The non-authority law both A and B sit under, `$.nonAuthority`, verbatim:**

```json
{
  "verbatim": "rendering success or failure cannot rewrite a committed Run or change policy, evidence, or its sealed `HostTermination`. A renderer never chooses public termination or exit",
  "rules": ["A renderer cannot affect policy.","A renderer cannot affect evidence.","A renderer cannot affect sealed HostTermination.","A renderer cannot choose D9 or exit."]
}
```

**B's full requirement block, `$.requiredOutputFailure`, verbatim:**

```json
{
  "source": "file 01 L92-99",
  "golden": "machine-output-serialization-failed",
  "behavior": "Host-finalization-only. A required host serialization/atomic-write failure: if an authoritative Run was already committed, preserve that Run identity and sealed HostTermination; otherwise create no Run identity. The public command ends operational-failed with OUTPUT.SERIALIZATION_FAILED; exit derives from D9 v1.14 classToExitCode (operational-failed -> 4). This is not a renderer-authority refusal.",
  "ownerOfValues": "D9 v1.14 already records this golden. This artifact binds the projection to that golden. It does not mint a new D9 code or a new exit number.",
  "componentsCannotSelect": "Components cannot select the sealed termination or this host output failure.",
  "projectionScope": "host-finalization-only",
  "committedRunBoundary": "Run preservation is conditional on an already-committed authoritative Run. Commands with no committed Run (help/version and any other) do not gain a Run to satisfy this golden.",
  "notARendererRefusal": "Ordinary output failure is distinct from FC-NONAUTH-TERM (D9/HostTermination authority-injection) and FC-NONAUTH-COVERAGE (Coverage/verdict rewrite; INACTIVE on ID-DEP-S2). The host applies the D9 golden; it does not refuse the renderer."
}
```

**The applicability block — where D-077 enters, `$.applicability`, verbatim:**

```json
{
  "law": "SARIF is optional and only for commands/capabilities that advertise it. It is not required of every command. It is not the native result or evidence format.",
  "d002Advertisement": "D-002 advertised SARIF 2.1.0 for analyze only.",
  "previewLiveApplicability": "NONE. D-077 / namedD002RidesIfOwnerRecorded.SARIF_for_analyze: DROPS from the preview, because the ride is DR-006 RunId/Finding fingerprint recipes and the preview disposition is scoped. A command that advertised SARIF in preview would be a false claim.",
  "laterApplicability": "If DR-006 closes by binding recipes rather than scoped disposition, analyze may advertise SARIF under this law. If DR-006 stays scoped, SARIF stays dropped. Prose here does not revive the advertisement.",
  "g17": "harness.DR-G17.sarif-projection-parity.analyze is DROPPED / inapplicable (D-077, D-086). This artifact does not resurrect it."
}
```

**The identity dependencies, `$.identityDependencies.dependencies`, verbatim** (S1/S2 are why three
classes are INACTIVE; S3 is why B is *not* blocked):

```json
[
  {"id":"ID-DEP-S1","feature":"Canonical RunId and Finding fingerprint","ridesOn":"DR-006","consequence":"If DR-006 closes by scoped disposition, advertised SARIF drops (already the preview fact). This artifact does not invent the recipes."},
  {"id":"ID-DEP-S2","feature":"Coverage field semantics","ridesOn":"DR-006 subjectScopeCommitment","consequence":"Parity goldens that require Coverage identity wait on that recipe."},
  {"id":"ID-DEP-S3","feature":"D9/exit values for output failure","ridesOn":"DR-007 / applied D9 v1.14 golden","consequence":"This artifact cites the existing golden. It mints no code."},
  {"id":"ID-DEP-S4","feature":"Whether this schema is a DR-111 matrix row","ridesOn":"DR-111","consequence":"Proposed, not admitted."}
]
```

#### The D9 class list — pinned, and the code the goldens need

- Path: `docs/coop/artifacts/d9-exit-contract.v1.14.json`
- sha256: `8dd3303855f49bfdbb2751ee65f54a906405f0654159ebe815472f73cdf7da31` (re-hashed at HEAD;
  matches `sarif-fc-outfail-golden-bind.v1#$.basedOn.d9v114.sha256` and its `$.recordedInputs`)
- `$.artifact` = `"opensip.d9-exit-contract"`, `$.version` = `"v1.14"`,
  `$.status` = `"CANDIDATE-NOT-APPLIED / AWAITING-INDEPENDENT-REVIEW (v1.14 API/coherence-only repair
  over independently passed v1.13)"`, `$.supersedes` = `"d9-exit-contract.v1.13.json"`.
- **Live pin**: file 08 line 40, DR-007 row, column 4 (`Exact source pin or selector`) contains
  `` `d9-exit-contract.v1.14` `8dd3303855f49bfdbb2751ee65f54a906405f0654159ebe815472f73cdf7da31` ``.
  DR-007's status cell reads `HARD-BLOCKED — Preview-scope owner recording 2026-08-14 …`.

The closed class list, `$.exitClasses` (6 members) and `$.classToExitCode`, verbatim:

```json
{"success":0,"policy-failed":1,"request-rejected":2,"indeterminate":3,"operational-failed":4,"interrupted":130}
```

The closed code vocabulary, `$.codeVocabulary`:

- `$.codeVocabulary.closed` = `true`
- `$.codeVocabulary.reasonCodes` — 9 members: `["COVERAGE.PROVIDER_UNAVAILABLE",
  "COVERAGE.LANGUAGE_TIER_UNSUPPORTED","COVERAGE.REQUIRED_RELATION_MISSING",
  "COVERAGE.BUDGET_EXHAUSTED","SNAPSHOT.CONVERGENCE_EXHAUSTED","BASELINE.RECIPE_UNSUPPORTED",
  "VERDICT.INDETERMINATE","QUERY.COMPLETENESS_UNMET","COVERAGE.CONFIDENCE_FLOOR_UNMET"]`
- `$.codeVocabulary.errorCodes` — 19 members, including **`"OUTPUT.SERIALIZATION_FAILED"`** (the one
  B needs): `["CAS.LINK_FAILED","CONFIG.INVALID","DELIVERY.REQUIRED_FAILED",
  "DURABILITY.COMMIT_FAILED","EXTENSION.ADMISSION_REJECTED","EXTENSION.INSTALL_IO_FAILED",
  "HOST.IO_FAILURE","IDENTITY.EXPIRED","IDENTITY.UNKNOWN","LEDGER.BUSY_TIMEOUT","LEDGER.CORRUPT",
  "OUTPUT.SERIALIZATION_FAILED","PROVIDER.PROTOCOL_VIOLATION","REQUEST.PRECONDITION_FAILED",
  "REQUEST.SCHEMA_MAJOR_UNSUPPORTED","REQUEST.UNKNOWN_OPTION","REQUEST.UNSATISFIABLE",
  "SERVE.PROTOCOL_FAULT","SYSTEM.OUTCOME.ILLEGAL_STATE"]`
- `$.codeVocabulary.rule`, verbatim:
  > "A code outside this vocabulary is a contract violation. Codes are grouped by remedy: two codes
  > with the same remedy are a smell, two remedies behind one code is a defect."

**The golden B binds to exists.** `$.goldenCases` has 45 members; index **37** is verbatim:

```json
{
  "id": "machine-output-serialization-failed",
  "commandKind": "any",
  "scenario": "a host-finalization projection: the requested CommandEnvelope cannot be serialized or atomically written; scenarioAxes.lifecycle and durability describe ONLY the failing output operation. If an authoritative Run was already committed, its identity and sealed termination remain; the command still ends operational-failed with OUTPUT.SERIALIZATION_FAILED",
  "scenarioAxes": {"lifecycle":"not-applicable","requiredCoverage":"not-applicable","verdict":"not-applicable","durability":"not-applicable","interruption":"none","requiredPostconditions":"not-applicable","domainCondition":"host-fault","admission":"admitted","commandKind":"any","deficiency":"none","rejectionCause":"none","faultCause":"output-serialization","secondaryDeficiencies":[],"projectionScope":"host-finalization-only"},
  "expectedTermination": {"class":"operational-failed","errorCode":"OUTPUT.SERIALIZATION_FAILED"},
  "hostFinalizationProjection": {"describes":"the failing host output operation only","preservesSettledRun":true,"doesNotClaimUniversalLifecycle":true}
}
```

`$.hostTerminationUnion.exitCodeInPayload`, verbatim (the rule B's fixtures must not violate):

> "NOT a union field. exitCode is derived from class via classToExitCode and must not be stored on
> HostTermination, so the two can never disagree (A2-D9-V12-01)."

#### The file 08 acceptance-evidence cell

Live file 08 `e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e`, table header at
**line 280** (`| ID | Decision | Owner / decision authority | Source pin / affected sections |
Required acceptance evidence | Status | Blueprint impact |`), DR-122 row at **line 304**.
Column 5, `Required acceptance evidence`, verbatim:

> ` Explicit per-command/capability applicability; stable machine/schema/version contract; parity/loss goldens preserving canonical Run/Finding IDs, Coverage, verdict, truncation, and artifact references; negative tests proving a renderer cannot affect policy/evidence/sealed termination or choose D9/exit, plus exact host-owned required-output failure golden `

Column 4, `Source pin / affected sections`, verbatim:

> ` V1 `operability.v10.json` `9bacbbf43dfb941a0d87330f79844d395b3ac838ae5bf54026ef4d69681696be` `$.projectionParity` / `$.projectionFixtures`; [V2 output projections](01-semantic-model-and-host-authority.md#output-projections-including-sarif) `

Column 3 (owner) = ` Output/operability owner + CLI/product owner `; column 6 (status) =
` PROPOSED-CLOSED-FOR-REVIEW `; column 7 = ` Hard blocker for any first-slice command or reporting
component that advertises SARIF; does not require every command to emit SARIF `.

The cell's semicolon split maps onto the six fixture classes: "Explicit per-command/capability
applicability" is FC-APPLIC; "parity/loss goldens preserving canonical Run/Finding IDs, Coverage,
verdict, truncation, and artifact references" is FC-PARITY + FC-LOSS (both INACTIVE); "negative
tests proving a renderer cannot affect policy/evidence/sealed termination or choose D9/exit" is
**A** (FC-NONAUTH-TERM), with the Coverage half at FC-NONAUTH-COVERAGE (INACTIVE); "plus exact
host-owned required-output failure golden" is **B** (FC-OUTFAIL). That mapping is stated in the
record at `$.fixtureClasses[i].requires` rather than in the cell itself.

## 2. Coverage set

### A — OBL-FC-NONAUTH-TERM-FX

**Axis A1 — named cases.** `sarif-fc-nonauth-term-bind.v1.json#$.namedCases[i].id`:

1. `$.namedCases[0].id` = `"FC-NONAUTH-TERM.renderer-chosen-d9-refuse"`,
   `intentVerbatim` = `"a renderer-chosen D9"`,
   `passProperty` = `"A renderer-supplied D9 is refused. This artifact does not choose or mint the
   attempted code."`, `fixtureBytes` = `"NOT-AUTHORED"`, `doesNotInventD9` = `true`.
2. `$.namedCases[1].id` = `"FC-NONAUTH-TERM.rewritten-hosttermination-refuse"`,
   `intentVerbatim` = `"a rewritten HostTermination refuse"`,
   `passProperty` = `"A rewritten HostTermination is refused."`, `fixtureBytes` = `"NOT-AUTHORED"`.

**Axis A2 — the v15 requirement the two cases discharge.**
`sarif-projection-contract.v15.json#$.fixtureClasses[3].requires`:

3. > "Negative tests of renderer authority-injection on D9 and HostTermination only: a
   > renderer-chosen D9 and a rewritten HostTermination refuse. Does not include Coverage
   > preservation. Ordinary required serialization/atomic-write failure is FC-OUTFAIL. These tests
   > do not require SARIF to be advertised."

The words "**on D9 and HostTermination only**" close the axis at two.

**Axis A3 — non-authority rules the goldens exercise.**
`sarif-fc-nonauth-term-bind.v1.json#$.quotedNonAuthorityRules` (identical to
`sarif-projection-contract.v15.json#$.nonAuthority.rules`), 4 members:

4. "A renderer cannot affect policy."
5. "A renderer cannot affect evidence."
6. "A renderer cannot affect sealed HostTermination."
7. "A renderer cannot choose D9 or exit."

Note the arity mismatch: **4 rules, 2 named cases.** The bind maps rules 3 and 4 onto its two cases
(HostTermination → `namedCases[1]`, D9 → `namedCases[0]`) and leaves rules 1 and 2 (policy,
evidence) unmapped, because `$.fixtureClasses[3].requires` scopes the class to "D9 and
HostTermination **only**". The policy/evidence and Coverage halves live at FC-NONAUTH-COVERAGE,
which `$.coveragePreservation` records as "EXCLUDED … INACTIVE on ID-DEP-S2 / DR-006". See
OQ-SARIF-4.

**Axis A4 — projection surfaces.** `sarif-projection-contract.v15.json#$.fixtureClasses[3].scope`:

8. > "any host-owned projection including JSON; does not require SARIF advertisement"

The surface set is "any host-owned projection", which the record does not enumerate. The one
enumeration that exists is the FC-APPLIC advertisement table:
`sarif-preview-advertisement-table.v1.json`
sha256 `c1a7e8bb8f9f8975b6cbffa25400156cb0b453bfab452a9a9aef20c7f068ed3d`, whose role at
`sarif-leftover-join.v4.json#$.basedOn.advertTableV1.role` is "analyze/doctor/help/version advertise
human+json only; SARIF is not-advertised." So the projections available in preview are **human** and
**json**, across **four commands** (analyze, doctor, help, version). Whether A's goldens must cover
that cross-product is unstated. See OQ-SARIF-5.

**Axis A5 — the attempted D9 code.** `namedCases[0]` requires "a renderer-chosen D9" but
`$.authorityClaim` says "It does not choose which D9 a renderer attempts" and `passProperty` repeats
"This artifact does not choose or mint the attempted code." The value is deliberately left open. The
closed vocabulary that bounds a choice is `d9-exit-contract.v1.14.json#$.codeVocabulary` (6 classes,
9 reason codes, 19 error codes) plus `$.codeVocabulary.rule` ("A code outside this vocabulary is a
contract violation"), so two distinct witness families exist — in-vocabulary and out-of-vocabulary —
and the record does not say which the fixture wants. See **§4 A(a)** and OQ-SARIF-2.

**Arithmetic (A).** 2 named cases (Axis A1), fixed by Axis A2's "only". Zero platform axis (no
`platforms` field anywhere in the DR-122 lineage; `$.identityDependencies.dependencies[3]` records
DR-111 matrix membership as "Proposed, not admitted"). Per-case witness count not enumerated.

**Total coverage members (A): 2** — `FC-NONAUTH-TERM.renderer-chosen-d9-refuse` and
`FC-NONAUTH-TERM.rewritten-hosttermination-refuse`. Arithmetic: 2 named cases x 1 projection-surface
axis (unenumerated, treated as one) x 1 platform axis (absent) = 2.

### B — OBL-FC-OUTFAIL-FX

**Axis B1 — named cases.** `sarif-fc-outfail-golden-bind.v1.json#$.namedCases[i].id`:

1. `$.namedCases[0].id` = `"FC-OUTFAIL.committed-run-preserved"`,
   `intentVerbatim` = `"if an authoritative Run was already committed, preserve its identity and
   sealed termination"`, `fixtureBytes` = `"NOT-AUTHORED"`. No `passProperty` field.
2. `$.namedCases[1].id` = `"FC-OUTFAIL.no-committed-run"`,
   `intentVerbatim` = `"Help/version or any command with no committed Run MUST NOT acquire a
   fictitious Run/RunId."`, `fixtureBytes` = `"NOT-AUTHORED"`. No `passProperty` field.

**Axis B2 — the v15 requirement the two cases discharge.**
`sarif-projection-contract.v15.json#$.fixtureClasses[5].requires`:

3. > "Exact D9 v1.14 machine-output-serialization-failed golden at host-finalization-only scope: if
   > an authoritative Run was already committed, preserve its identity and sealed termination;
   > otherwise no Run identity is created. Public termination is operational-failed with
   > OUTPUT.SERIALIZATION_FAILED; exit derives from classToExitCode (recorded 4). Help/version or
   > any command with no committed Run MUST NOT acquire a fictitious Run/RunId."

The "if … otherwise" structure closes the axis at two: committed-run and no-committed-run.
`$.requiredOutputFailure.committedRunBoundary` restates it: "Run preservation is conditional on an
already-committed authoritative Run. Commands with no committed Run (help/version and any other) do
not gain a Run to satisfy this golden."

**Axis B3 — fates.** One termination, fixed exactly, no choice available.

4. `d9-exit-contract.v1.14.json#$.goldenCases[37].expectedTermination` =
   `{"class":"operational-failed","errorCode":"OUTPUT.SERIALIZATION_FAILED"}`.
5. `d9-exit-contract.v1.14.json#$.classToExitCode["operational-failed"]` = `4`, quoted at
   `sarif-fc-outfail-golden-bind.v1.json#$.quotedClassToExitCode`.
6. `sarif-fc-outfail-golden-bind.v1.json#$.quotedClassToExitCode.exitCodeInPayloadVerbatim`: "NOT a
   union field. exitCode is derived from class via classToExitCode and must not be stored on
   HostTermination, so the two can never disagree (A2-D9-V12-01)."

**Axis B4 — the failing operation.** `$.requiredOutputFailure.behavior`: "A required host
serialization/atomic-write failure". Two operations named — **serialization** and **atomic write** —
in both the v15 behavior string and the D9 golden's `scenario` ("cannot be serialized or atomically
written"). The record does not say whether each needs its own witness. See OQ-SARIF-6.

**Axis B5 — the fourteen scenario axes.** `d9-exit-contract.v1.14.json#$.goldenCases[37].scenarioAxes`
fixes every axis value for this golden, so a fixture has **no** freedom on them:
`lifecycle: "not-applicable"`, `requiredCoverage: "not-applicable"`, `verdict: "not-applicable"`,
`durability: "not-applicable"`, `interruption: "none"`, `requiredPostconditions: "not-applicable"`,
`domainCondition: "host-fault"`, `admission: "admitted"`, `commandKind: "any"`,
`deficiency: "none"`, `rejectionCause: "none"`, `faultCause: "output-serialization"`,
`secondaryDeficiencies: []`, `projectionScope: "host-finalization-only"`.

**Axis B6 — commands.** `$.goldenCases[37].commandKind` = `"any"`; the no-committed-run case names
`"Help/version or any command with no committed Run"`. The four preview commands are enumerated only
at the FC-APPLIC table (analyze, doctor, help, version). Whether B needs a witness per command is
unstated. See OQ-SARIF-5.

**Arithmetic (B).** 2 named cases (Axis B1), fixed by Axis B2's "if … otherwise". Termination fully
determined (Axis B3), scenario axes fully determined (Axis B5). Zero platform axis.

**Total coverage members (B): 2** — `FC-OUTFAIL.committed-run-preserved` and
`FC-OUTFAIL.no-committed-run`. Arithmetic: 2 named cases x 1 fully-determined termination x 1
platform axis (absent) = 2.

### Combined

**Total coverage members: 4** (A: 2 + B: 2), one per `namedCases[i]` across the two binds, each
carrying `fixtureBytes: "NOT-AUTHORED"`. No platform multiplier applies: neither bind, nor the join,
nor `sarif-projection-contract.v15` carries a `platforms` array or a `windowsStanding` field, and
`$.identityDependencies.dependencies[3]` records DR-111 matrix membership as "Proposed, not
admitted". This is the smallest coverage set of the four obligations in this plan set, and the only
one whose axes are all closed by the governing bytes rather than left as universals.

## 3. Prohibitions bounding the authoring

### Shared — from the join

`sarif-leftover-join.v4.json#$.doesNot` (18 entries), verbatim:

```
[0]  Does not SATISFY DR-122.
[1]  Does not open D-056 Class A.
[2]  Does not close leftover-design.
[3]  Does not add a DR-G* row.
[4]  Does not change live required-now 28.
[5]  Does not apply sarif-projection-contract.v15.
[6]  Does not advertise SARIF in preview.
[7]  Does not resurrect G17.
[8]  Does not mint RunId/Finding recipes.
[9]  Does not mint a D9 code or exit number.
[10] Does not require every command to emit SARIF.
[11] Does not steal G26 leftover from DR-131.
[12] Does not make SARIF the native result or evidence format.
[13] Does not discharge traveling honesty advisories.
[14] Does not edit file 08.
[15] Does not invent a section 7.1 recipe.
[16] Does not authorize docs/v2/implementation/.
[17] Does not author FC-NONAUTH-TERM or FC-OUTFAIL fixture bytes.
```

`$.authorityClaim` adds, verbatim: "It does not mint a D9 code. It does not close leftover-design of
OBL-FC-OUTFAIL-FX or OBL-FC-NONAUTH-TERM-FX."

Both obligation reasons carry the same closing clause: "This join does not invent those bytes and
does not mint a D9 code."

### Shared — from the contract

`sarif-projection-contract.v15.json#$.whatThisDoesNotDo` (8 entries), verbatim:

```
[0] Does not SATISFY DR-122 until independently reviewed and recorded by a later D-000 MF-6.
[1] Does not advertise SARIF in the architecture preview.
[2] Does not resurrect G17.
[3] Does not mint RunId/Finding recipes.
[4] Does not mint a D9 code or exit number.
[5] Does not require every command to emit SARIF.
[6] Does not authorize docs/v2/implementation/.
[7] Does not make SARIF the native result or evidence format.
```

And `$.applicability.laterApplicability`, whose last sentence is a prohibition on prose itself:

> "If DR-006 closes by binding recipes rather than scoped disposition, analyze may advertise SARIF
> under this law. If DR-006 stays scoped, SARIF stays dropped. **Prose here does not revive the
> advertisement.**"

### A — from `sarif-fc-nonauth-term-bind.v1`

`$.doesNot` (13 entries), verbatim:

```
[0]  Does not SATISFY DR-122.
[1]  Does not mint a D9 code.
[2]  Does not choose which D9 a renderer attempts.
[3]  Does not include Coverage preservation.
[4]  Does not author FC-OUTFAIL.
[5]  Does not advertise SARIF.
[6]  Does not resurrect G17.
[7]  Does not author executable fixture bytes.
[8]  Does not change required-now 26.
[9]  Does not add a DR-G* row.
[10] Does not edit file 08.
[11] Does not invent a section 7.1 recipe.
[12] Does not authorize docs/v2/implementation/.
```

Entry `[2]` — "Does not choose which D9 a renderer attempts" — is the one that bites hardest on
authoring, because `namedCases[0]` cannot be instantiated without choosing one. It is a prohibition
on the **bind**, not necessarily on a successor corpus; whether it travels is OQ-SARIF-2.

`$.coveragePreservation` = "EXCLUDED. v15 FC-NONAUTH-TERM: Does not include Coverage preservation.
FC-NONAUTH-COVERAGE remains INACTIVE on ID-DEP-S2 / DR-006."
`$.ordinaryOutputFailure` = "FC-OUTFAIL. Not this class."

### B — from `sarif-fc-outfail-golden-bind.v1`

`$.doesNot` (14 entries), verbatim:

```
[0]  Does not SATISFY DR-122.
[1]  Does not mint a D9 code.
[2]  Does not mint an exit number.
[3]  Does not store exitCode on HostTermination.
[4]  Does not invent a CommandEnvelope, decision-record, grant, journal, or report-golden envelope.
[5]  Does not advertise SARIF.
[6]  Does not resurrect G17.
[7]  Does not author FC-NONAUTH-TERM.
[8]  Does not author executable fixture bytes.
[9]  Does not change required-now 26.
[10] Does not add a DR-G* row.
[11] Does not edit file 08.
[12] Does not invent a section 7.1 recipe.
[13] Does not authorize docs/v2/implementation/.
```

Entry `[4]` — "Does not invent a CommandEnvelope, decision-record, grant, journal, or report-golden
envelope" — is B's sharpest, because the D9 golden's own scenario says "the requested
CommandEnvelope cannot be serialized or atomically written". The fixture must exhibit a
CommandEnvelope failing to serialize without defining what a CommandEnvelope is. See OQ-SARIF-7.
Entry `[3]` restates `d9-exit-contract.v1.14.json#$.hostTerminationUnion.exitCodeInPayload`.

### From `IMPLEMENTATION-FREEZE.md` §7.1

Both binds' `$.doesNot` and the join's `$.doesNot[15]` prohibit "a section 7.1 recipe". The referent
is `docs/coop/IMPLEMENTATION-FREEZE.md`
sha256 `e809d4395f394a507c36c23c069d566c838b2283c931b6d2d13797be53406dbd`, line 1675:

> `### 7.1 Parked identity recipes — named for escalation, NOT non-blocking`

Line 1681 and line 1711, verbatim:

> "Naming them makes escalation compliant. It does not make them optional and
> it does not authorise anyone to invent one."

> "Every row above must be closed by a binding artifact before signature. None may
> be closed by this record, by the blueprint, by a checker, or by an implementer."

The governing property, blockquoted at line 1728:

> "**Any identity-, digest-, commitment- or ref-typed field for which no binding
> artifact states a rule producing its value from real inputs is parked under
> this section and is escalable, whether or not it appears as a row above.**"

**§7.1 is directly load-bearing for B.** The section's own parked-row table names `RunId` derivation
as its first row, sourced from `operability.v10#requestIdContract.fixtures[8].parked` with the
verbatim disclaimer "No exact RunId derivation recipe is binding yet.", and the same table names
`Finding fingerprint recipe`. B's `namedCases[0]` requires preserving "its identity and sealed
termination" for a committed Run, and `namedCases[1]` requires that no "fictitious Run/RunId" be
acquired. See §4 B(b).

### From the D9 class list

`d9-exit-contract.v1.14.json#$.codeVocabulary.rule`, verbatim:

> "A code outside this vocabulary is a contract violation. Codes are grouped by remedy: two codes
> with the same remedy are a smell, two remedies behind one code is a defect."

`$.hostTerminationUnion.unknownFieldPolicy` = `"reject"`; `$.hostTerminationUnion.nullabilityPolicy`:

> "Optional fields are ABSENT or present-and-valid. No field is ever explicitly null; absence is the
> only way to express 'not applicable'. This resolves A2-D9-V12-07: a pre-admission failure omits
> runId entirely rather than carrying null."

That last sentence is the recorded shape for B's `no-committed-run` case: **omit `runId`**, do not
null it.

### The D-293 constraint clause that applies to these obligations

`DECISION-PACKETS/D1-fixture-authoring-delegation.claude-recommendation.r2.md`
sha256 `f530cedca1c799097ed0fc30cf8ec6f0480abe9a56d495236909a3a23b84fc33`, line 3, verbatim:

> "Effective only within already-recorded semantics: no adapter, CI encoding, journal, SDK API, new
> D9/HostTermination/pack semantics, reserved list, or number is authorised; G15, G16 and G18 keep
> their recorded prohibitions (adapter, CI encoding, journal)."

The words "**new D9/HostTermination … semantics**" are the D-293-level restatement of the "does not
mint a D9 code" prohibition on both obligations, and "**journal**" matches B's `$.doesNot[4]`.

Line 6, the default policy, verbatim:

> "**Default policy (replaces round 1):** coverage, not one-case-per-member — every explicit
> platform, matrix, mutation, transition and fate quantifier in the governing bytes is preserved;
> for delegated byte sets, concrete witness bytes may be selected only within already-recorded
> schemas and fates, and any choice that would create a new semantic member, identifier, value, list
> or implementation stays outside the grant (recorded as a named open decision instead)."

## 4. Dependencies

### The D-077 tension — settled for these two obligations, with one residue

**The tension as put:** D-077 dropped SARIF from the preview (making G17 inapplicable), yet DR-122
still carries SARIF fixture obligations. Does the drop block them?

**The record settles it: no.** Three bytes, each verbatim:

1. `sarif-projection-contract.v15.json#$.fixtureClasses[3].requires`, last sentence:
   > "These tests do not require SARIF to be advertised."
2. `sarif-projection-contract.v15.json#$.fixtureClasses[3].scope`:
   > "any host-owned projection including JSON; does not require SARIF advertisement"
   and `$.fixtureClasses[5].scope`:
   > "host-finalization only; any host-owned required projection including JSON"
3. `sarif-fc-nonauth-term-bind.v1.json#$.sarifAdvertisementRequired` = `false`.

Both ACTIVE classes are therefore **host-projection** classes, not SARIF classes. `$.ride` is
`null` on both, and both `rideNote` strings say so: `$.fixtureClasses[3].rideNote` = "Active
host-projection fixture with no parked dependency for D9/HostTermination negatives.";
`$.fixtureClasses[5].rideNote` = "Active host-projection fixture with no parked dependency.
ride:null is the explicit representation, same as FC-APPLIC."

The three classes that *do* depend on advertisement are the INACTIVE ones, and the record parks them
explicitly: `$.fixtureClasses[1].previewStanding` (FC-PARITY) = `"INACTIVE"` with
`$.fixtureClasses[1].conditionality` = "Activates if a later DR-006 recipe-close restores analyze
advertisement."; FC-LOSS the same; FC-NONAUTH-COVERAGE rides `ID-DEP-S2/DR-006`. The join holds them
at `$.obligations[8]` (`OBL-INACTIVE-DR006`, leftoverDesign false).

D-077's own words, COORD line 3077, verbatim:

> "SARIF drops; cache
> keys, Coverage, and PlanId stay conceptual."

(from `## D-077 — Owner-record the DR-006 preview Route B disposition`, COORD line 3053; the same
`- **Decision:**` block also reads "Does not mark DR-006 SATISFIED. Binding recipes remain owed.")
`$.applicability.previewLiveApplicability` carries the drop forward: "NONE. D-077 /
namedD002RidesIfOwnerRecorded.SARIF_for_analyze: DROPS from the preview, because the ride is DR-006
RunId/Finding fingerprint recipes and the preview disposition is scoped. A command that advertised
SARIF in preview would be a false claim." And `$.applicability.g17`:
"harness.DR-G17.sarif-projection-parity.analyze is DROPPED / inapplicable (D-077, D-086). This
artifact does not resurrect it."

**Not a dependency. The D-077 drop does not block either obligation.** The residue — what the
fixtures render *through*, given that SARIF is not advertised and only human+json are — is
OQ-SARIF-5.

### A — OBL-FC-NONAUTH-TERM-FX

**(a) The attempted D9 code. BLOCKED-ON a named choice, not on a missing artifact.**

`namedCases[0].intentVerbatim` = "a renderer-chosen D9". To author executable bytes the fixture must
carry a concrete attempted value. The bind refuses to supply one; the dependency sentence, verbatim
from `sarif-fc-nonauth-term-bind.v1.json#$.namedCases[0].passProperty`:

> "A renderer-supplied D9 is refused. **This artifact does not choose or mint the attempted code.**"

restated at `$.authorityClaim` ("It does not choose which D9 a renderer attempts") and as
`$.doesNot[2]` ("Does not choose which D9 a renderer attempts").

**The D9 class list exists and is closed**, so nothing is missing:
`d9-exit-contract.v1.14.json` sha256 `8dd3303855f49bfdbb2751ee65f54a906405f0654159ebe815472f73cdf7da31`,
pinned live at file 08 line 40; `$.codeVocabulary.closed` = `true`; 6 exit classes, 9 reason codes,
19 error codes. **The goldens do not need a D9 code that does not exist** — so this is **not**
BLOCKED-ON a missing artifact.

What is unresolved is *which* value the fixture uses, and the record makes two readings available:

- **In-vocabulary reading**: the renderer attempts an existing code (say `operational-failed` /
  `OUTPUT.SERIALIZATION_FAILED`) and is refused because a renderer has no authority to choose *any*
  D9, per `$.nonAuthority.rules[3]` ("A renderer cannot choose D9 or exit."). Selecting an existing
  member of a closed vocabulary is a witness-byte selection inside a recorded schema — inside the
  grant.
- **Out-of-vocabulary reading**: the renderer attempts a string outside the closed vocabulary,
  refused under `$.codeVocabulary.rule` ("A code outside this vocabulary is a contract violation").
  Composing that string is minting a value the record does not carry — outside the grant.

The record does not say which. Under the D-293 default policy the second reading "would create a new
semantic member, identifier, value, list or implementation" and "stays outside the grant (recorded
as a named open decision instead)". This is OQ-SARIF-2.

**(b) Nothing else.** `$.fixtureClasses[3].ride` = `null` and `$.fixtureClasses[3].rideNote` = "Active
host-projection fixture with **no parked dependency** for D9/HostTermination negatives." The
HostTermination union is fully defined at `d9-exit-contract.v1.14.json#$.hostTerminationUnion`
(discriminator, `unknownFieldPolicy: "reject"`, `nullabilityPolicy`, `exitCodeInPayload`,
`fieldTypes`), so `namedCases[1]` ("a rewritten HostTermination refuse") has a schema to rewrite
against.

**Standing (A): NOT BLOCKED** — the coverage set, the class definition, the non-authority rules and
the D9 vocabulary all exist; OQ-SARIF-2 is a named choice to record, not a missing byte.

### B — OBL-FC-OUTFAIL-FX

**(a) The D9 golden. Present.** `d9-exit-contract.v1.14.json#$.goldenCases[37]` is the exact golden
B binds to, quoted in §1.5. `$.codeVocabulary.errorCodes` contains
`"OUTPUT.SERIALIZATION_FAILED"`; `$.classToExitCode["operational-failed"]` = `4`. The dependency
sentence that records the absence of any minting need, verbatim from
`sarif-fc-outfail-golden-bind.v1.json#$.quotedV15OwnerOfValues`:

> "D9 v1.14 already records this golden. This artifact binds the projection to that golden. It does
> not mint a new D9 code or a new exit number."

**Not blocked. B needs no D9 code that does not exist.**

**(b) RunId. This is the real dependency, and it is a §7.1 park.**

`namedCases[0].intentVerbatim` requires the fixture to "preserve its identity and sealed
termination" for an already-committed authoritative Run. `namedCases[1].intentVerbatim` requires
that a command with no committed Run "MUST NOT acquire a fictitious Run/RunId". Both cases turn on a
`RunId` value.

The dependency sentence, from `docs/coop/IMPLEMENTATION-FREEZE.md`
sha256 `e809d4395f394a507c36c23c069d566c838b2283c931b6d2d13797be53406dbd`, §7.1's parked-row table,
**line 1696**, the `RunId` derivation row. Column 2 ("Source of the disclaimer"), verbatim as an
excerpt of a longer cell:

> "`operability.v10#requestIdContract.fixtures[8].parked`; the verbatim “No exact RunId derivation recipe is binding yet.” C-2 supplies only the wire pattern `^run1:[0-9a-f]{64}$` and says derivation/custody is a Run identity concern"

and column 4 ("Implementer rule") of the same row, verbatim:

> "Escalate. Do **not** choose CSPRNG bytes, a `RunDescriptor` digest, or an evidence-bundle digest — they have opposite retry-determinism consequences"

and, from the same section's prose at line 1711:

> "Every row above must be closed by a binding artifact before signature. None may
> be closed by this record, by the blueprint, by a checker, or by an implementer."

The corresponding prohibition on this row is `sarif-leftover-join.v4.json#$.doesNot[8]` ("Does not
mint RunId/Finding recipes") and `sarif-projection-contract.v15.json#$.whatThisDoesNotDo[3]` (same),
with `$.identityDependencies.dependencies[0]` (ID-DEP-S1) recording the ride: "Canonical RunId and
Finding fingerprint … ridesOn DR-006 … This artifact does not invent the recipes."

**Whether this blocks depends on which case:**

- `namedCases[1]` (`FC-OUTFAIL.no-committed-run`) is a **negative** assertion — no Run/RunId is
  acquired. The recorded shape for expressing it needs no derivation:
  `d9-exit-contract.v1.14.json#$.hostTerminationUnion.nullabilityPolicy` says "a pre-admission
  failure **omits runId entirely** rather than carrying null." Absence is authorable. **Not
  blocked.**
- `namedCases[0]` (`FC-OUTFAIL.committed-run-preserved`) requires a fixture in which an authoritative
  Run *was* committed and its identity survives. Whether that fixture must carry a *derived* RunId
  (which §7.1 parks and `$.doesNot[8]` forbids) or may carry an **opaque pinned literal** matching
  C-2's wire pattern is not stated anywhere in the DR-122 lineage. §7.1's own property is explicit
  that a literal is not a rule — line 1731: "A value that appears only as a literal in a vector,
  fixture, golden or example is not a rule." Read one way that *permits* the fixture (a literal is
  not a recipe, so using one mints nothing); read the other way the fixture would be asserting an
  identity it cannot produce. The record does not choose.

**Standing (B): BLOCKED-ON-RUNID-RECIPE-PARK for `FC-OUTFAIL.committed-run-preserved` only.**
`FC-OUTFAIL.no-committed-run` is not blocked. See OQ-SARIF-8.

**(c) CommandEnvelope. Bounded, not blocking.** The D9 golden's scenario names "the requested
CommandEnvelope", and `sarif-fc-outfail-golden-bind.v1.json#$.doesNot[4]` forbids inventing one. The
fixture must exhibit a serialization failure of a CommandEnvelope without defining the envelope. The
`$.purpose` sentence records the same boundary: "without inventing a D9 code, an exit number, a
CommandEnvelope, or executable fixture bytes." A fixture that treats the envelope as opaque bytes
that fail to write is authorable; one that specifies its members is not. OQ-SARIF-7.

**(d) Not dependencies for either A or B.**

- **No sequencing clause.** D-293 Decision 5 (COORD line 16228) orders "then G29/G30 fixture
  authoring" for DR-117 only. Both DR-122 obligations appear in D-293 Decision 8's delegated list
  (COORD line 16264: "the two DR-122 SARIF fixture obligations") with no ordering attached.
  `DECISIONS-RECOMMENDED.md` sha256 `42f27394746d4aac569a09a01da719c0cf318cf114086635e73097a6add97370`
  has no `## B`-series heading for DR-122.
- **DR-006 does not gate the ACTIVE classes.** `$.fixtureClasses[3].ride` = `null`;
  `$.fixtureClasses[5].ride` = `null`. Only the three INACTIVE classes ride DR-006.
- **G17 is not required and must not be revived.** `$.obligations[2]` (`OBL-G17`,
  leftoverDesign false): "v15 applicability.g17: harness.DR-G17.sarif-projection-parity.analyze is
  DROPPED / inapplicable (D-077, D-086). This artifact does not resurrect it. D-115 records G17 stays
  inapplicable."
- **G26 is not required.** `$.obligations[9]` (`OBL-G26`, leftoverDesign false, rideStanding
  `"rides-G26"`): "This join does not steal G26 leftover from DR-131, does not SATISFY DR-122 by
  citing G26, and does not execute G26."
- **The FC-APPLIC table already exists.** `sarif-preview-advertisement-table.v1.json`
  sha256 `c1a7e8bb8f9f8975b6cbffa25400156cb0b453bfab452a9a9aef20c7f068ed3d`, Claude ACCEPT 0/0.
- **No platform axis to satisfy.** Absent from the whole lineage.

**Standing: BLOCKED-ON-RUNID-RECIPE-PARK (B, one case of two; A and B's other case NOT BLOCKED)**

## 5. Recommended artifact shape

**The closest precedent for these two is not `g23-fixture-corpus.v4` or `g21-fixture-corpus.v1` — it
is the `sarif-fc-*-bind` form itself.** The assignment's framing is confirmed by the record: the
successor is "a golden-bind successor in the sarif-fc-*-bind form", because both obligations are
defined by reference to a bind artifact's `namedCases` rather than by an occupancy's
`retainedEvidence`, and because those binds are the only artifacts in the DR-122 lineage that carry
per-case `fixtureBytes` markers to flip.

**Fields each bind carries** (verified key lists, in file order):

`sarif-fc-nonauth-term-bind.v1.json` — 25 top-level keys:

`artifact, version, date, documentClass, registerRow, namedGate, status, reviewStatus,
sealRecommendation, binds, authorityClaim, purpose, basedOn, file08Pin, head, requiredNowUnchanged,
recordedInputs, remeasurementClause, quotedNonAuthorityRules, namedCases, coveragePreservation,
ordinaryOutputFailure, sarifAdvertisementRequired, whatThisClosesIfAcceptedAndRecorded,
whatThisDoesNotClose, doesNot`

with `$.namedCases[i]` keys: `id, fixtureBytes, intentVerbatim, passProperty` (and `doesNotInventD9`
on `[0]` only), and `$.basedOn` keys `contractV15` (carrying `path, sha256, recording,
fcNonauthTermRequiresVerbatim, nonAuthorityVerbatim`) and `leftoverJoinV1`.

`sarif-fc-outfail-golden-bind.v1.json` — 25 top-level keys:

`artifact, version, date, documentClass, registerRow, namedGate, status, reviewStatus,
sealRecommendation, binds, authorityClaim, purpose, basedOn, file08Pin, head, requiredNowUnchanged,
recordedInputs, remeasurementClause, quotedD9Golden, quotedClassToExitCode, quotedV15OwnerOfValues,
namedCases, whatThisClosesIfAcceptedAndRecorded, whatThisDoesNotClose, doesNot`

with `$.namedCases[i]` keys: `id, fixtureBytes, intentVerbatim` (no `passProperty`), and `$.basedOn`
keys `d9v114`, `contractV15`, `leftoverJoinV1`.

**Common skeleton across both:** `artifact, version, date, documentClass, registerRow, namedGate,
status, reviewStatus, sealRecommendation, binds, authorityClaim, purpose, basedOn, file08Pin, head,
requiredNowUnchanged, recordedInputs, remeasurementClause, namedCases,
whatThisClosesIfAcceptedAndRecorded, whatThisDoesNotClose, doesNot` — 22 shared keys. Each then adds
its own `quoted*` block (A: `quotedNonAuthorityRules`; B: `quotedD9Golden`, `quotedClassToExitCode`,
`quotedV15OwnerOfValues`) and its own scope fields (A: `coveragePreservation`,
`ordinaryOutputFailure`, `sarifAdvertisementRequired`).

**What a golden-bind successor must add that neither v1 has**, since these v1 artifacts declare
`fixtureBytes: "NOT-AUTHORED"` and the successor's job is to author them:

- a per-case `path` and `sha256` over the authored payload bytes — the field pair the corpus
  precedents use (`g21-fixture-corpus.v1.json#$.authoredCatalog.members[i].path` / `.sha256`;
  `g23-fixture-corpus.v4.json#$.authoredCatalog.members[i].payloadSha256`);
- a digest-construction declaration, the analogue of
  `g21-fixture-corpus.v1.json#$.cborConstruction`, because the reviewer M2 finding on
  `g23-fixture-corpus.v1` was exactly an undeclared digest construction;
- `fixtureBytes` flipped from `"NOT-AUTHORED"` to the authored marker, per case;
- a `failsIf` roster (both binds have `doesNot` but neither has `failsIf`; the corpus precedents and
  every gate occupancy do);
- a `leftoverDesignRemainingOnDR122` block, since neither obligation can be exhausted while
  OQ-SARIF-8 stands.

**Proposed artifact names** (one per obligation, matching the one-bind-per-class precedent — the
record has never put both classes in one artifact, and each bind's `whatThisDoesNotClose[0]` names
the other class explicitly):

- **A:** `docs/coop/artifacts/sarif-fc-nonauth-term-golden.v1.json`
- **B:** `docs/coop/artifacts/sarif-fc-outfail-golden.v1.json`

**Proposed fixture directories:**

- **A:** `docs/coop/artifacts/fixtures/sarif-fc-nonauth-term.v1/<id>.json`, mode 0444
- **B:** `docs/coop/artifacts/fixtures/sarif-fc-outfail.v1/<id>.json`, mode 0444

**First-authoring, no platform subdirectories.** Two reasons from the bytes: no `sarif-fc-*` fixture
corpus of any version exists in `docs/coop/artifacts/`; and there is no platform axis anywhere in
the DR-122 lineage to copy across (no `platforms`, no `windowsStanding`;
`$.identityDependencies.dependencies[3]` records DR-111 matrix membership as "Proposed, not
admitted"). This matches `g21-fixture-corpus.v1`'s first-authoring shape, where the per-platform
copy version was a separate later artifact.

## 6. Effort and risk

**Number of cases: 4** — two per obligation, one per `namedCases[i]`. This is the smallest of the
four obligations in this plan set, and the only one whose case count is fully closed by the
governing bytes (A by "on D9 and HostTermination only"; B by the "if … otherwise" structure).

### (a) Witness-byte selections inside recorded schemas — permitted under the grant

**A:**

1. The concrete renderer-supplied D9 value for `namedCases[0]`, **if** the in-vocabulary reading is
   taken: an existing member of `d9-exit-contract.v1.14.json#$.codeVocabulary.errorCodes` (19) or
   `$.exitClasses[i].class` (6). Selecting an existing member of a closed list is a witness-byte
   selection. (The out-of-vocabulary reading is (b)1 below.)
2. The concrete rewritten-HostTermination payload for `namedCases[1]`, within
   `d9-exit-contract.v1.14.json#$.hostTerminationUnion.fieldTypes` (`runId`, `executionId`,
   `errorCode`, `reasonCodes`, `coverageId`, `signal`, `details`) and its
   `unknownFieldPolicy: "reject"`.
3. The projection surface used to exercise the negative — `$.fixtureClasses[3].scope` says "any
   host-owned projection including JSON", and the FC-APPLIC table records human+json as the
   advertised preview projections, so **json** is an already-recorded choice.
4. Serialization of each payload and its `sha256` over those bytes, with the construction declared.

**B:**

5. The concrete opaque bytes whose serialization/atomic write fails — the record fixes the *fate*
   entirely (`expectedTermination`, all fourteen `scenarioAxes`) and leaves only the failing artifact
   open.
6. The command used for `namedCases[1]` — `intentVerbatim` names "Help/version or any command with
   no committed Run", and the FC-APPLIC table enumerates help and version among the four preview
   commands, so either is an already-recorded choice.
7. Whether the failure is a serialization failure or an atomic-write failure, or one witness of
   each — both are named in `$.requiredOutputFailure.behavior` and in the D9 golden's `scenario`.
8. `runId` **absence** for `namedCases[1]`, following
   `$.hostTerminationUnion.nullabilityPolicy` ("omits runId entirely rather than carrying null").

### (b) Choices that would create new semantics — record as a named open decision, do not choose

1. **Composing an out-of-vocabulary D9 code string** for A's `namedCases[0]`. Violates the D-293
   constraint "no … new D9/HostTermination/pack semantics … is authorised",
   `d9-exit-contract.v1.14.json#$.codeVocabulary.rule`, and the join's `$.doesNot[9]`. Record as a
   named open decision, do not choose. (OQ-SARIF-2.)
2. **Supplying a RunId derivation, or any Finding-fingerprint, EvidenceDigest, FactViewId, cache-key
   or `subjectScopeCommitment` recipe.** Violates `sarif-leftover-join.v4.json#$.doesNot[8]`,
   `sarif-projection-contract.v15.json#$.whatThisDoesNotDo[3]`, both binds' `$.doesNot[…] "Does not
   invent a section 7.1 recipe."`, and `IMPLEMENTATION-FREEZE.md` §7.1 line 1711. Record as a named
   open decision, do not choose. (OQ-SARIF-8.)
3. **Defining a CommandEnvelope, decision-record, grant, journal, or report-golden envelope.**
   Violates `sarif-fc-outfail-golden-bind.v1.json#$.doesNot[4]` verbatim. Record as a named open
   decision, do not choose. (OQ-SARIF-7.)
4. **Minting an exit number, or storing `exitCode` on HostTermination.** Violates
   `sarif-fc-outfail-golden-bind.v1.json#$.doesNot[2]`, `$.doesNot[3]`, and
   `d9-exit-contract.v1.14.json#$.hostTerminationUnion.exitCodeInPayload`. Record as a named open
   decision, do not choose.
5. **Advertising SARIF, emitting a SARIF document as the fixture's projection, or reviving G17.**
   Violates the join's `$.doesNot[6]`, `$.doesNot[7]`, both binds' `$.doesNot`, and
   `$.applicability.previewLiveApplicability` ("A command that advertised SARIF in preview would be
   a false claim"). Record as a named open decision, do not choose.
6. **Adding Coverage preservation to A.** Violates
   `sarif-fc-nonauth-term-bind.v1.json#$.coveragePreservation` ("EXCLUDED") and `$.doesNot[3]`;
   that half is FC-NONAUTH-COVERAGE, INACTIVE on ID-DEP-S2. Record as a named open decision, do not
   choose.
7. **Collapsing A and B into one artifact or one case set.** Each bind's
   `$.whatThisDoesNotClose[0]` names the other class, and
   `$.ordinaryOutputFailure` = "FC-OUTFAIL. Not this class." and
   `$.requiredOutputFailure.notARendererRefusal` = "Ordinary output failure is distinct from
   FC-NONAUTH-TERM … The host applies the D9 golden; it does not refuse the renderer." Record as a
   named open decision, do not choose.
8. **Adding a fifth case to either class, or a platform axis.** A is closed at two by "on D9 and
   HostTermination only"; B at two by "if … otherwise"; no platform axis exists in the lineage.
   Record as a named open decision, do not choose.
9. **Claiming `leftoverDesignClosedIfAcceptedAndRecorded` for either obligation** while OQ-SARIF-8
   stands on `FC-OUTFAIL.committed-run-preserved`. Record as a named open decision, do not choose.

### Risk

The reviewer-attack pattern on the two recorded corpus lineages was (a) inventing a vocabulary or
encoding the record does not carry, (b) collapsing two classes the occupancy keeps separate, (c)
classifying a witness under a closed identifier it does not belong to, (d) over-claiming closure.

**On (b), this subject is the most exposed of the four in this plan set, and the record anticipates
it in prose.** FC-NONAUTH-TERM and FC-OUTFAIL are two ways for a host projection to fail, and the
contract spends three separate clauses keeping them apart:
`$.fixtureClasses[3].requires` — "Ordinary required serialization/atomic-write failure is
FC-OUTFAIL."; `$.requiredOutputFailure.behavior` — "This is not a renderer-authority refusal.";
`$.requiredOutputFailure.notARendererRefusal` — "Ordinary output failure is distinct from
FC-NONAUTH-TERM (D9/HostTermination authority-injection) and FC-NONAUTH-COVERAGE (Coverage/verdict
rewrite; INACTIVE on ID-DEP-S2). The host applies the D9 golden; it does not refuse the renderer."
Plus `sarif-fc-nonauth-term-bind.v1.json#$.ordinaryOutputFailure` = "FC-OUTFAIL. Not this class."
Four clauses drawing one line is the record's own signal that the line is easy to cross. A witness
in which a renderer's attempted D9 injection *also* causes an output-serialization failure would
collapse A into B and reproduce the `g23-fixture-corpus.v2` M1 shape ("collapsing EV-2 into EV-3
against the governing occupancy's explicit non-collapse requirement") exactly.

**On (a), the trap is the digest construction**, as it was on `g23-fixture-corpus.v1` ("M2 —
coverageCommitment is a SHA-256 over compact JSON, not deterministic-CBOR, and its construction is
undeclared"). Neither bind declares one, because neither authors bytes; a golden-bind successor must.

**On (c), the closed identifier is the D9 code vocabulary**, and the risk is sharper here than
elsewhere because the fixture's whole point is a *wrong* code being attempted. Filing an
out-of-vocabulary attempt under an in-vocabulary identifier, or vice versa, is the `G21FXV3-M1`
shape ("The non-object-top-level payload is an RF-2 case but is not authorized as a member of the
closed CC-5 corpus").

**On (d)**, the join already names the over-claim it will not tolerate: `$.doesNotCloseLeftoverAlone`
— "OBL-FC-OUTFAIL-FX and OBL-FC-NONAUTH-TERM-FX remain leftover-design. … Gates 2 and 3 do not hold.
Class A is not opened."

**Two risks specific to this subject:**

- **Single-reviewer precedent.** Both binds carry `Claude ACCEPT 0/0; Codex not reviewed`
  (`sarif-leftover-join.v4.json#$.basedOn.nonauthBindV1.review.verdict` and
  `$.basedOn.outfailBindV1.review.verdict`), and on disk each has only a
  `.review-independent.claude2.json` with no `.codex.` counterpart. That makes them a **weaker
  precedent shape** than the `g23`/`g21` fixture corpora, which reached dual ACCEPT 0/0 before being
  recorded. Both bind roles also end "**Not recorded by any decision.**" — so the successor's
  precedent is an unreviewed-by-Codex, unrecorded artifact. A reviewer may reasonably ask why the
  successor follows that form rather than the dual-ACCEPT corpus form; the answer is in §5, and it
  should be stated in the artifact rather than left implicit.
- **Stale pins three generations deep.** The join's `$.file08Pin` is `f909ddff…` against live
  `e503b75b…`; each bind's `$.file08Pin` is `3a9442d1…` with `$.head` `5d5d778` and
  `requiredNowUnchanged` 26. A successor that quotes the binds must re-pin all three levels and say
  the DR-122 row text is unchanged, or it inherits three stale measurements at once. (OQ-SARIF-1.)

## 7. Open questions

**OQ-SARIF-1:** Do the stale pins require join and bind successors before goldens can be authored?
`sarif-leftover-join.v4.json#$.file08Pin.sha256` = `"f909ddff7f3a8e9be864259808c4a2320170181001bdb746814b07393dd9d5e1"`
and both binds carry `$.file08Pin.sha256` =
`"3a9442d1761864de59f103374489a9fbffdd12cc4ba39ddd7c7f491f64357e44"`, `$.head` =
`"5d5d77819ae3019d9e6e02f1e66de3d93c060402"`, `$.requiredNowUnchanged` = `26`. Live file 08 is
`e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e` at required-now 28. The DR-122
row text at line 304 re-extracts byte-identically, so nothing substantive moved, and the join's
`$.remeasurementClause` requires re-measurement only "If a cited file moves in a way that is not
append-only COORD growth or COORD heading hygiene" — which file 08 movement is not. Whether a golden
successor may cite artifacts pinned two and three generations back, or whether a
`sarif-leftover-join.v5` and re-pinned binds must land first, is not settled.

**OQ-SARIF-2:** Which D9 value does `FC-NONAUTH-TERM.renderer-chosen-d9-refuse` carry?
`sarif-fc-nonauth-term-bind.v1.json#$.namedCases[0].intentVerbatim` = "a renderer-chosen D9", and
`$.namedCases[0].passProperty` ends "This artifact does not choose or mint the attempted code."
`$.doesNot[2]` = "Does not choose which D9 a renderer attempts." Executable bytes require a concrete
value. `d9-exit-contract.v1.14.json#$.codeVocabulary.closed` = `true` with 19 error codes and 6 exit
classes, and `$.codeVocabulary.rule` says "A code outside this vocabulary is a contract violation" —
so both an in-vocabulary attempt (refused for lack of renderer authority) and an out-of-vocabulary
attempt (refused as a contract violation) are coherent readings, and they test different properties.
The record picks neither. It is also unstated whether `$.doesNot[2]`'s prohibition binds only the
bind artifact or travels to a successor that must instantiate the case.

**OQ-SARIF-3:** What are the FC-OUTFAIL cases' pass properties?
`sarif-fc-nonauth-term-bind.v1.json#$.namedCases[i]` each carry a `passProperty` field;
`sarif-fc-outfail-golden-bind.v1.json#$.namedCases[i]` carry **none** — only `id`, `fixtureBytes`
and `intentVerbatim`. The pass condition is instead distributed across
`sarif-projection-contract.v15.json#$.fixtureClasses[5].requires`,
`$.requiredOutputFailure.behavior`, `$.requiredOutputFailure.committedRunBoundary` and
`d9-exit-contract.v1.14.json#$.goldenCases[37].expectedTermination`. Which of those a successor must
reproduce as the per-case `passProperty`, and in what wording, is not stated. The asymmetry between
the two binds is itself unexplained by the record.

**OQ-SARIF-4:** Do the two unmapped non-authority rules need coverage?
`sarif-fc-nonauth-term-bind.v1.json#$.quotedNonAuthorityRules` lists four rules — policy, evidence,
sealed HostTermination, D9-or-exit — but `$.namedCases` has only two members, covering the last two.
`sarif-projection-contract.v15.json#$.fixtureClasses[3].requires` scopes the class to "renderer
authority-injection on D9 and HostTermination **only**", and `$.coveragePreservation` sends the
Coverage half to the INACTIVE FC-NONAUTH-COVERAGE. But the file 08 acceptance-evidence cell (line
304, column 5) says "negative tests proving a renderer cannot affect **policy/evidence**/sealed
termination or choose D9/exit" — naming all four. Whether the policy and evidence rules are covered
elsewhere, deferred, or simply unowned on the current record is not settled.

**OQ-SARIF-5:** Through which projection are the goldens rendered, and across how many commands?
`$.fixtureClasses[3].scope` = "any host-owned projection including JSON"; `$.fixtureClasses[5].scope`
= "host-finalization only; any host-owned required projection including JSON". Neither enumerates
the projection set. The only enumeration in the lineage is the FC-APPLIC table
(`sarif-preview-advertisement-table.v1.json`
sha256 `c1a7e8bb8f9f8975b6cbffa25400156cb0b453bfab452a9a9aef20c7f068ed3d`), whose role string records
"analyze/doctor/help/version advertise human+json only; SARIF is not-advertised" — two projections,
four commands. `d9-exit-contract.v1.14.json#$.goldenCases[37].commandKind` = `"any"`. Whether the
four goldens are one-per-case, or a per-command or per-projection cross-product, is unstated. This is
the residue of the D-077 tension: the drop is settled (§4), but what the fixtures render *through*
is not.

**OQ-SARIF-6:** Does B need one witness or two for the failing operation?
`sarif-projection-contract.v15.json#$.requiredOutputFailure.behavior` says "A required host
**serialization/atomic-write** failure" and `d9-exit-contract.v1.14.json#$.goldenCases[37].scenario`
says the envelope "cannot be **serialized or atomically written**". Two distinct operations, one
`faultCause` value (`"output-serialization"`) and one `errorCode`
(`OUTPUT.SERIALIZATION_FAILED`). Whether the record intends both operations to be exercised, or
treats them as one fate with one witness, is not stated — and `$.namedCases` splits on the
committed-Run axis instead, leaving this axis unsplit.

**OQ-SARIF-7:** How does a fixture exhibit a CommandEnvelope failing to serialize without defining
one? `d9-exit-contract.v1.14.json#$.goldenCases[37].scenario` names "the requested CommandEnvelope";
`sarif-fc-outfail-golden-bind.v1.json#$.doesNot[4]` = "Does not invent a CommandEnvelope,
decision-record, grant, journal, or report-golden envelope." and `$.purpose` repeats "without
inventing a D9 code, an exit number, a CommandEnvelope, or executable fixture bytes." No
CommandEnvelope schema is pinned anywhere in the DR-122 lineage. Whether the fixture treats the
envelope as opaque bytes, cites a schema from another surface, or whether authoring the case at all
requires that schema first, is not settled.

**OQ-SARIF-8:** May `FC-OUTFAIL.committed-run-preserved` carry a literal RunId?
`sarif-fc-outfail-golden-bind.v1.json#$.namedCases[0].intentVerbatim` requires preserving "its
identity and sealed termination" for an already-committed Run. `RunId` derivation is a parked §7.1
row (`IMPLEMENTATION-FREEZE.md` sha256
`e809d4395f394a507c36c23c069d566c838b2283c931b6d2d13797be53406dbd`, line 1675 onward, citing
`operability.v10#requestIdContract.fixtures[8].parked` and the verbatim "No exact RunId derivation
recipe is binding yet."), and `sarif-leftover-join.v4.json#$.doesNot[8]` forbids minting the recipe.
§7.1's own property at line 1731 says "A value that appears only as a literal in a vector, fixture,
golden or example is not a rule" — which can be read as permitting a literal (it mints no rule) or as
warning that a literal proves nothing. The sibling case is unaffected:
`d9-exit-contract.v1.14.json#$.hostTerminationUnion.nullabilityPolicy` gives the recorded shape for
`FC-OUTFAIL.no-committed-run` ("omits runId entirely rather than carrying null"). This is the
standing recorded in §4 as BLOCKED-ON-RUNID-RECIPE-PARK for one case of two.

**OQ-SARIF-9:** Is the `sarif-fc-*-bind` form the right precedent given its review standing?
Both binds are `Claude ACCEPT 0/0; Codex not reviewed` and both `basedOn` roles end "Not recorded by
any decision." The two fixture-corpus lineages the record does hold up as precedent —
`g23-fixture-corpus.v4.json` sha256 `b3fce9f5bab6764919f5dc43c28a43f3d9c3b6be310e45c2c1bd08a617c755c5`
(D-239) and `g21-fixture-corpus.v8.json`
sha256 `e8149a865e49bdcda9eda923e9918f332a83078f43ab6a3af9a10d6d31ef6359` (D-247) — reached dual
ACCEPT 0/0 and were recorded by decisions. Whether a DR-122 golden successor should follow the
single-reviewed bind form (which matches its subject) or the dual-ACCEPT corpus form (which matches
its grade) is not settled by the record.
