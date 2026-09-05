# `make-ppbs-v9.py` — generator for `preview-product-boundary-successor.v9.json`

Builds the DR-117 preview-scoped successor candidate **v9** from the frozen
predecessor `docs/coop/artifacts/preview-product-boundary-successor.v8.json`
(sha256 `f2e788e5…`, recorded at COORD `## D-207`), per the owner-adopted
programme in COORD `## D-293` Decision 5 / `DECISIONS-RECOMMENDED.md` §B3 /
`DECISION-PACKETS/B3-DR-117-class-A.md`.

The script writes **only** the file you name. It never touches `docs/`, and it
runs no state-changing git command (`git rev-parse` and `git status` only).

## Run

From the repository root:

```sh
python3 /path/to/ppbs-v9/make-ppbs-v9.py [OUTPUT] [--audit AUDIT.json] [--quiet]
```

* `OUTPUT` — a directory (the file lands inside it as
  `preview-product-boundary-successor.v9.json`) or a path ending in `.json`.
  Default: the directory the script lives in.
* `--audit PATH` — also write the rewrite / carry / new-field ledger as JSON
  (this is how `audit.json` in this directory was produced).
* Exit `0` on success; exit `2` with `make-ppbs-v9.py: FAILED: …` on stderr if
  any measurement disagrees with the record. **Nothing is written on failure.**

The dry run in this directory:

```sh
cd /Users/sb/code/opensip-ai/opensip
python3 …/ppbs-v9/make-ppbs-v9.py …/ppbs-v9 --audit …/ppbs-v9/audit.json
```

Output is byte-deterministic for a given repository state and calendar day:
`json.dumps(doc, indent=2, ensure_ascii=False) + "\n"`, the same serialization
that reproduces the predecessor's 55,298 bytes exactly.

## What it measures at run time (nothing is hard-coded as a value)

| Field | Source |
|---|---|
| `head`, `recordedInputs.HEAD` | `git rev-parse HEAD` |
| `date` | the system clock |
| `file08Pin.sha256`, `registerRowQuoted.sourceSha256` | live sha256 of file 08 |
| `file08StatusToken` | DR-117's leading Status label parsed out of file 08's register table |
| `sevenItems.sourceSha256` | live sha256 of file 02 |
| `enforcementEvidence.v1SlicePin.sha256` | live sha256 of `docs/coop/v1-slice.md` |
| the twelve current leftover-joins | highest non-`CONTESTED` COORD heading per lineage |
| every `recordedInputs` digest | recomputed from bytes |

## The twelve re-citations

For each lineage the current version is whatever the **highest non-CONTESTED**
COORD heading `## D-NNN — Record <lineage>[- ]leftover-join.vN as …` names. The
programme's expectation is encoded in the `JOINS` table and the run **fails** if
the live measurement differs:

| lineage | predecessor cited | current now |
|---|---|---|
| g29 | v3 (D-204) | v4 (D-254) |
| g30 | v3 (D-205) | v4 (D-255) |
| g09 | v10 (D-189) | v12 (D-288) |
| language-runtime | v4 (D-179) | v7 (D-274) |
| g16 | v3 (D-192) | v5 (D-278) |
| g21 | v4 (D-196) | v13 (D-292) |
| g23 | v4 (D-198) | v8 (D-240) |
| permission | v9 (D-171) | v12 (D-283) |
| distribution-core | v7 (D-173) | v9 (D-287) |
| monorepo | v3 (D-181) | v4 (D-277) |
| language-quality | v3 (D-206) | v5 (D-273) |
| doctor-actor | v11 (D-170) | v12 (D-285) |

For each, the script additionally requires that the join's digest **and both
Stage A verdict digests** appear inside that recording entry's own text, that
both verdicts read `ACCEPT`, and that the join is still
`CANDIDATE-NOT-APPLIED` / `binds NOTHING`.

## Assertions that abort the run

* the predecessor's sha256 still equals the `D-207` recording;
* no *tracked* file under `docs/` is modified (untracked files are ignored — they
  move no pin);
* the **fourteen** EE classes and the **seven** dispositions are byte-identical to
  the predecessor's (deep equality plus canonical-JSON equality);
* the EE routing derived from each class's own `existingGate` first clause matches
  the recorded gate map;
* file 08 still carries `**28 of 28 required gates name a recorded identifier**`,
  which is what `requiredNowUnchanged: 28` reproduces;
* DR-117's live leading label is `OPEN`, and its acceptance-evidence cell equals
  the predecessor's quotation;
* file 02 is unmoved (file 08 line 299: any change to the seven-item enumeration
  re-opens the row);
* every pinned digest recomputes, and no path the predecessor pinned is dropped;
* the two Stage A verdicts on the predecessor still carry the exact shapes the
  artifact recites — `whatThisVerdictDoesNotDo` containing
  `"Does not claim Gate 1 Class A holds."`, and
  `authorityBoundaryAudit.eligibility.gate1ClassA` `false` with `gate1Authority`
  `"D-137 express reservation remains controlling"`.

## House rules enforced by the final audit

The whole emitted document (keys and values) is scanned; any hit fails the run:

1. **no deictic predecessor self-reference** — `[Tt]his v[0-8]\b`. Every speaker
   sentence names itself: `This preview-product-boundary-successor.v9 …`.
2. **no bare version token** — every `\bv\d+\b` must be lineage-qualified, i.e.
   attached to an artifact identifier (`g21-leftover-join.v13`,
   `product-boundary-successor-contract.v8`, `permission-truth-tables.v9`). The
   only exemptions are the record's fixed path forms `docs/v2/…` and
   `v1-slice`.
3. **no unsubstituted `{`/`}` token.**

Two further rules are enforced by construction rather than by regex:

* **no claim contradicted by bytes.** Every `leftoverDesign` list in the emitted
  roles and in `leftoverDesignOpenStanding` is read from the current join's own
  obligations. This is why `g23-leftover-join.v8` (D-240) is described as
  flagging **no** obligation `leftoverDesign true` — the predecessor's
  `leftoverDesign remains [OBL-G23-FX-AUTHORING]` sentence is no longer
  supported, and `doesNot` says so instead of repeating it.
* **numbers agree with counts** — `twelve` joins, `fourteen` classes, `seven`
  dispositions are derived from `len()` checks, and the `remeasurementClause`
  states the pinned-row count computed from `recordedInputs`.

## What changed from the predecessor

See `audit.json` (`rewrittenFields`, `carriedFields`, `newFields`). In summary:
`authorityClaim`, `purpose`, `eligibilityNote`, `remeasurementClause`,
`leftoverDesignOpenStanding`, `basedOn.relation` and all sixteen `basedOn` roles
are written for v9 rather than string-patched; the fourteen EE classes, the seven
dispositions, `p1p2g3Mapping`, `registerRowQuoted.cellLimbs` and most of
`doesNot` are carried byte-identical; `predecessorStanding`,
`joinCurrencyAudit`, `lineage.contractRelationship` and
`basedOn.predecessorPinningShape` are new. `recordedInputs` grows from 51 rows to
92 and is regenerated from every path pinned anywhere in the document plus every
path the predecessor pinned.

The advisories on the predecessor are landed: **CLAUDE-PPBS-V8-ADV-1** (uniform
pinning — every predecessor and every one of the twelve joins now pins both Stage
A verdicts) and **CLAUDE-PPBS-V8-ADV-2** (`remeasurementClause` generated from
`recordedInputs`, with its trigger stated to reach every pinned row).

## What this artifact does not do

It is `CANDIDATE-NOT-APPLIED`, `AWAITING-INDEPENDENT-REVIEW`, `binds NOTHING`,
`DO-NOT-SEAL`. It records nothing, opens no D-056 Class A, lifts no D-137
reservation, SATISFIES no row, authors no fixture bytes, and does not replace,
apply or succeed `product-boundary-successor-contract.v8` (D-116). Recording it
is a later D-000 act; per D-293 Decision 5 a fresh application-grade dual review
bound to its final digest comes first, then the owner-controlled opening entry.

---

# `make-ppbs-v10.py` — successor after the v9 Stage A rejection

`preview-product-boundary-successor.v9` was frozen at
`docs/coop/artifacts/preview-product-boundary-successor.v9.json`
(sha256 `e0221a1c…`) and **rejected by both Stage A reviewers**; it was never
recorded, so `preview-product-boundary-successor.v8` (D-207) is still the
current recording. `make-ppbs-v10.py` builds the successor that lands the
findings.

## Run

```sh
cd /Users/sb/code/opensip-ai/opensip
python3 …/ppbs-v9/make-ppbs-v10.py [OUTPUT] [--audit AUDIT.json] [--quiet]
```

Same conventions as the v9 generator, whose helpers it imports (`sha256_file`,
the COORD/file-08 parsers, `current_join_recording`, `pin_review`, the `JOINS`
table, the `Ledger`, the bare-version-token rule). Default output is the
script's own directory; exit `2` and nothing written on any failed measurement;
never writes under `docs/`.

## What v10 changes, and nothing else

| # | Finding | Change |
|---|---|---|
| 1 | `CLAUDE-PPBS-V9-B1`, `PPBSV9-B1` | The **40** present-tense cross-lineage currency citations inside `enforcementEvidence.classes[*].existingGate` / `.laterExecution` are refreshed to the versions current at dispatch — computed from COORD at run time, never hard-coded — under **D-294 Decision 3**. |
| 2 | `CLAUDE-PPBS-V9-B2` | EE-3a's `leftoverDesign remains [OBL-G21-FX-AUTHORING] and [OBL-G23-FX-AUTHORING].` becomes the measured partition: `[OBL-G21-FX-AUTHORING]` on `g21 leftover-join.v13` (D-292); `g23 leftover-join.v8` (D-240) flags none. **2** sites. |
| 3 | `CLAUDE-PPBS-V9-SF1` | `basedOn.predecessorV8.role` and `joinCurrencyAudit.standing` name **both** D-293 Decision 5 limbs and list the other rewritten fields instead of "the whole reason" / "nothing else is disturbed". |
| 4 | `CLAUDE-PPBS-V9-ADV-1` | `joinCurrencyAudit.method` quotes the COORD heading form with the **em dash** the live headings use. |
| — | history | `basedOn.predecessorV9` (path, digest, both REJECT verdicts, role); five new `findingDisposition` entries; `predecessorStanding` records that v9 never became current; `recordedInputs` gains the v9 file and both v9 reviews (92 → 95 rows); every v9 speaker sentence becomes v10. |

Refreshed sites total **42** = 40 currency citations + 2 partition sentences.
Per lineage the 40 break down exactly as both reviews tabulate them: g29 14,
g30 6, and 2 each for g09, language-runtime, g16, g21, g23, permission,
distribution-core, monorepo, language-quality, doctor-actor.

## The "nothing else" half is proved, not asserted

After normalizing (a) every `<lineage> leftover-join.vN (D-NNN)` token and
(b) the EE-3a partition sentence in **both** documents, v10's fourteen classes
must equal **v8's** fourteen classes by canonical-JSON comparison, or the run
fails. The seven dispositions and `p1p2g3Mapping` must still be byte-identical
to v8's. The result is recorded in the artifact at
`enforcementEvidence.classesRefresh.classEqualityAssertion`.

Consequently every "byte-identical" claim about the classes is replaced by the
exact truth: *identical except the cross-lineage currency sentences refreshed
under D-294 Decision 3 and the EE-3a leftoverDesign partition sentence, 42
sites; the seven dispositions and p1p2g3Mapping byte-identical.*

## Audit rules added on top of the v9 set

1. Fail if any sentence of the inverted currency form (`Current <row>
   leftover-join is <lineage> leftover-join.vN`) or the `remain(s) on <lineage>
   leftover-join.vN` form names a version other than the current one for that
   lineage — applied to the **whole** document, not just the classes.
2. Fail on any byte-identity claim (`byte-identical` / `byte-identically` /
   `byte-for-byte`) in a sentence that also names the classes.
3. Fail on `This v<digit>` anywhere.
4. Fail on bare version tokens outside the record's fixed `docs/` path forms.
5. Fail if any field still speaks as `preview-product-boundary-successor.v9`.

All five were verified by negative tests: skipping a lineage, refreshing one to
a wrong version, re-introducing a byte-identity claim, using a deictic speaker,
and tampering with a class `invariant` each abort the run with nothing written.

## Deliberately not landed

`CLAUDE-PPBS-V9-B1` carries a rider — "not separately counted" — asking that the
**34** deictic `"This successor"` occurrences inside the classes be aligned with
the speaker form. v10 does not land it: it is outside the enumerated changes,
and doing it would break the class-equality proof that is what shows nothing
else moved. `enforcementEvidence.classesRefresh` and the `CLAUDE-PPBS-V9-B1`
disposition (`riderNotLanded`) say so in the artifact.
