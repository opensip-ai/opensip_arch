# SD-7 — NE §10's follow-ups from M3-D r4: SD-5's row conformed, and item 25's row (contract successor)

2026-10-04. Drafted for Claude Opus 5.5, implementation lead, by a lead-dispatched drafting agent during the overnight autonomous run. **Draft r1, PROPOSED, not accepted.** It is a design unit: it edits only arch, and adds no product file, code, class, exit code, error code or public detail code. It needs Grok's `ACCEPT-DESIGN-UNIT` and the lead's root assent before it can be bound in the product's `design-lock.json`.

**What it is.** The accepted supervisor law **M3-D r5** (`docs/implementation/m3/supervisor-d/PROPOSAL-r5.md`, Grok ACCEPT, `224b9228…`) names successor **SD-7**, "NE §10's follow-ups from r4" (MD5:1182; X-D4-NE, MD5:1215; F14 and F15, MD5:1204-1205). It has two parts:
- **(a) SD-5's bound row follows item 24 (LD-R4-1).** SD-5 (bound at product `052d3cb`) copied r3's wording into NE §10. Its EE-3b parenthetical counts "a `commands` entry for role `analyzer`", and its remedy says no component may "declare a project hook, root command or probe". Read literally, that refuses every analyzer. r4 replaced it with an exact root-command predicate (MD5:780-795). Until SD-7 binds, the row "is read through this predicate" (MD5:795).
- **(b) Item 25's request-class row (LD-R4-2).** A request-class `ExcludedForm` at R1 takes `request-rejected` 2, `REQUEST.UNSATISFIABLE`, `domainDetail` `PROVIDER.NOT_SELECTED` with subject `excluded-form:<class>`, and no runId or executionId (MD5:837). `PROVIDER.NOT_SELECTED`'s code-keyed remedy must be widened to stay true for both conditions (MD5:839).

M3-D r5 also fixes the form question: "NE:3540 already carries SD-5's override, and `verify_design` refuses a second override of one line … So (a) needs a superseding form: B-S9's complete-copy form or a `verify_design` successor. The remedy table is in B-S9's selected model copy (NEM). SD-7's drafter chooses." (MD5:1182). The choice is LD-7.1.

**Product.** Main at `6190e66` (SYN-NS's binding, 92 contract successors), read only. The lock is pinned there and the record is built and checked against it. SYN-NS, bound after M3-D r5 was written (at `218465f`), overrides no passage, so NE's effective text is the same at both commits.

## Short names

Each sha256 prefix is the first 8 hex of the exact bytes pinned in the review request (`reviews/grok-sd-7-r1/hashes.txt`).

| Name | Document | sha256 |
|---|---|---|
| **MD5** | `docs/implementation/m3/supervisor-d/PROPOSAL-r5.md`, M3-D r5, the accepted snapshot (`reviews/grok-supervisor-d-r5`) | `224b9228…` |
| **MJ** | `docs/implementation/m3/host-pipeline-j/PROPOSAL-r4.md`, M3-J1 r4, the accepted snapshot | `c18c0d3c…` |
| **NE** | `docs/v2/contracts/product-v1/native-evidence.md`, the parent (329,013 bytes) | `83b99783…` |
| **NE7** | `docs/implementation/m3/supervisor-d/sd-7/contracts/native-evidence.md`, this unit's complete successor copy of NE | see request |
| **SD5** | `docs/implementation/m3/supervisor-d/sd-5/`, accepted (`reviews/grok-sd-5-r1`) and bound at `052d3cb`; its record `sd-5/successor.json` | `5e115818…` (record) |
| **NEM** | B-S9's two native-model copies, `docs/implementation/m3/config-discovery-b/b-s9/reference/native_evidence_model.py` (the selected reference, `a7e40715…`) and `…/native_evidence_model.v2.py` (`4f800faa…`) | |
| **NES** | `docs/coop/design-corrections/native/native-evidence.schemas.v2.json`, the registered native bundle and its route registry | `2d37b810…` |
| **D9** | `docs/coop/artifacts/d9-exit-contract.v1.14.json` | `8dd33038…` |
| **REG** | `docs/coop/design-corrections/public-detail-registry.v1.json` | `2702e6ca…` |
| **DR103** | `docs/coop/artifacts/component-manifest-schemas.v11.json`, DR-103's field authority | `1c0b8868…` |
| **CD** | `docs/coop/COORDINATOR-DECISIONS.md`, D-012 (CD:1076-1088) | `cccc2dda…` |
| **CR-1** | `docs/implementation/m3/snapshot-plan-c/cr-1/README.md`, M3-C's role successor, bound at `3fe7eb5` | `1898c3a2…` |

## Files

| File | What it is |
|---|---|
| `README.md` | this proposal |
| `contracts/native-evidence.md` | generated: the complete successor copy of NE (NE7) |
| `evidence/copies-report.json` | generated: the parent, the 39 bound overrides applied, the effective parent's digest, the copy, its two hunks, an exact raw-to-copy line map, and the two remedy overrides |
| `PASSAGES.md` | generated: the two hunks, the effective table rows in the copy, and the two remedy overrides |
| `successor.json` | the record: four parents, two line overrides (line 1159 of each B-S9 model copy), no supersession, seven candidates |
| `evidence/build_sd7.py` | builds every generated file, the record, the subject manifest and the draft unit record; `--check` compares instead of writing |
| `evidence/check_sd7.py` | read-only checks, recomputing the effective NE independently |
| `evidence/verify_scratch.py` | the real `verify_design` with a synthetic review and assent, the rejected-form probes and the later-successor probes |
| `../sd-7-subject.json` | the subject manifest (generated) |
| `../sd-7-unit.json` | the lead's assent draft, `DRAFT-PENDING-REVIEW`, naming `reviews/grok-sd-7-r1/review.json` as the review it awaits; not part of the subject |

## The form (LD-7.1)

| Part | Where the text lives | Bound already? | Form |
|---|---|---|---|
| (a) SD-5's row | the second line of SD-5's `after` for NE:3540 | yes: SD-5 | **(ii) B-S9's complete-copy form** for NE |
| (b) item 25's row | NE §10, after the NOT-SELECTED row (raw NE:3539) | no | in the same copy, because the copy becomes the selected NE |
| (b) the remedy | `PUBLIC_ROUTE_REMEDIES["PROVIDER.NOT_SELECTED"]`, line 1159 of both NEM copies; nowhere else (not NE, NES, D9 or the product) | no | **(i) fresh line selectors** |

**Why not (i) for (a).** The row is the meaning of the bound key `(NE, {"line": 3540})`, and `verify_design` keys every override by `(parent path, selector)`. `verify_scratch.py` shows both direct routes refuse on `6190e66`: a second override of NE:3540 gives "conflicting contract passage overrides", and a VD1 supersession of SD-5's entry gives "passage supersession must select an inventory row description". No other selector changes those bytes. An erratum on a fresh line, such as NE:3542, would leave two class lists and two remedy strings for one route. That is a contradiction plus a precedence note, not a correction, and it would not "rewrite the row and its remedy".

**Why (ii) is lawful and (iii) is not needed.** A copy at a new path is an ordinary candidate. NE is an accepted parent that is not overwritten (`verify_design.py` `contract_successor`), and selection is declared in the record's `standing`, exactly as B-S9 did for the model and capability-totality-reference-selection-v1 before it. It binds on today's `verify_design` with no tooling change. A `verify_design` successor (VD2) would change `tools/verify_design.py`, which the generator closure and the TypeScript lane registry pin, so it means another generator rebuild and re-pin (B-S9 LD-1). It is a brief worth writing only if a later case cannot use the copy form.

## What changes

### 1. NE7, the complete successor copy of NE

NE7 is NE's **effective text** under the lock at `6190e66`: the raw parent with every bound override applied. That is 39 line overrides from six records: B-S1 (11), FA-2 (13), RUST3-LIM (6), SYN-1 (5), FA-1 (3) and SD-5 (1). It has exactly two hunks (`copies-report.json`; `check_sd7.py` recomputes the effective text independently and diffs it):

| Hunk | Copy line | Change |
|---|---|---|
| 1 | 3822 | **inserted:** item 25's request-class row, directly after the NOT-SELECTED row (raw NE:3539, unchanged) |
| 2 | 3824 | **replaced:** SD-5's row, conformed. The release declaration row above it (raw NE:3540's own text) is unchanged. |

Every other byte of the effective text is carried, including every other bound successor's text. The copy is 380,848 bytes; the effective parent is 378,351 bytes, `03b498b7…`.

### 2. SD-5's row, conformed (MD5 item 24, LD-R4-1)

Only the condition cell's provenance and class list, and the remedy phrase, change. The class, code and detail cells, the subject rule, the route-boundary sentences (row 27 and the release-declaration precedence) and every other word are SD-5's.

| | SD-5 (bound) | SD-7 |
|---|---|---|
| Provenance | "(contract successor SD-5 of law M3-D r3, item 24)" | adds "; conformed by contract successor SD-7 to law M3-D r5, item 24, lead decision LD-R4-1" |
| EE-3b | "(a `commands` entry for role `analyzer`, or a capability outside the native capability matrix's provider capabilities)" | "(a capability outside the native capability matrix's provider capabilities)", the capability form only (MD5:776, MD5:788) |
| EE-5a | "a project hook, root command or contribution-granted probe" | "a project hook, a contribution-granted probe, or a root-command claim on the host-owned root namespace, which is exactly" item 24's predicate (MD5:782-785): **(a)** a closure-only manifest (`toolchain`, `stdlib`, `rust-dev-llvm`, `grammar`) that declares `commands` at all; **(b)** an `analyzer` whose tree has not exactly one entry without `parent`, or whose parentless entry's `name` differs from the manifest's `name`; **(c)** a reserved root-command name among its root-namespace keys (its `name`, its `aliases`, and for `analyzer` its parentless entry's aliases) |
| Admitted | — | "An `analyzer` manifest's own name-bound mounted root, with any declared depth below it, is not a root-command claim, and neither is a collision with another component's live name; a command tree is never an `EE-3b` form" (MD5:786-788) |
| First refusal | — | "A manifest that the security owner's manifest admission refuses first never reaches component admission and keeps that route" (MD5:789-794: RJ-2 refuses (b) and (c) in both entry points; RJ-6 refuses (a) once C2a lands; D4 is the backstop, and enforces (a) until then) |
| Remedy | "… or declare a project hook, root command or probe. …" | "… or claim a project hook, a reserved or additional root command, or a probe. …", MD5:1182's words exactly |

The route is unchanged: `request-rejected` 2, `EXTENSION.ADMISSION_REJECTED`, `PAYLOAD-NOT-ADMISSIBLE`, subject `excluded-form:<class>:<manifestDigest>`, no runId or executionId. D4 emits only the internal refusal (MD5:1182), so no consumer changes.

### 3. Item 25's row (MD5 item 25, LD-R4-2)

| Field | Value | Basis |
|---|---|---|
| Condition | a well-formed request refused at typed request admission, before the durable entry, the creation prelude and any `ExecutionId` draw, as `ExcludedForm {class, subject}` | MD5:829 (R1, J1:315) |
| Classes | `EE-2`, a PlanIntent or admission request that requires an external discovery or public-lifecycle endpoint; `EE-4` (request part), a PlanIntent requesting untrusted native or WASM admission; `EE-6a`, a PlanIntent whose analysis branch requests network-granted analysis | MD5:833-835 |
| Why this route | each is outside D-371's selected product, as the NOT-SELECTED cell of the row above is; nothing is malformed and the host made no error, so the route is the same whatever the origin, and never a malformed request or a host fault | MD5:838, MD5:844; NE:3577-3579 |
| Class / exit / code | `request-rejected` / 2 / `REQUEST.UNSATISFIABLE` | D9 `rejectionCauseToErrorCode["unsatisfiable"]`; NE:3539 |
| `domainDetail` | `PROVIDER.NOT_SELECTED`, subject `excluded-form:<class>`; the first class in the order EE-2, EE-4, EE-6a when one request carries several | MD5:837 |
| Remedy | the widened code-keyed remedy (below), quoted in the row | MD5:839 |
| `errors`, record, ids | `errors` is exactly that detail; every `ExcludedForm` goes to the operational record; no runId and no executionId | MD5:837 |

It sits right after the NOT-SELECTED row it reuses, so "the row above" in its text is that row.

### 4. The widened remedy (both NEM copies, line 1159)

Before: "this capability is not selected for that language mode; no promise is made for it"

After (254 ASCII characters): "this capability is not selected for that language mode, or the request asks for an external discovery or public-lifecycle endpoint, untrusted native or WASM admission, or network-granted analysis; no promise is made for it; restate the request without it"

| Condition reaching `PROVIDER.NOT_SELECTED` | The next step the string gives |
|---|---|
| `native.requested-capability-mode-not-selected`, the only route-registry key that reaches it (NES `keys`) | "this capability is not selected for that language mode … no promise is made for it; restate the request without it" |
| EE-2 at R1 | "the request asks for an external discovery or public-lifecycle endpoint … restate the request without it" |
| EE-4 (request part) at R1 | "… untrusted native or WASM admission … restate the request without it" |
| EE-6a at R1 | "… network-granted analysis … restate the request without it" |

Both original clauses are kept word for word. The new next step, "restate the request without it", is MD5:839's "the next step is the same for both conditions: restate the request without what the product does not serve". `PUBLIC_ROUTE_REMEDIES` keeps every other key and value, and the two copies stay identical, as X12-0 and B-S9 kept them. This satisfies NES's `remedyKeyingConstraint` ("widen it or choose another code").

## Selection and its consequences

The record's `standing` states it:
- the current selected native-evidence contract becomes `docs/implementation/m3/supervisor-d/sd-7/contracts/native-evidence.md`;
- the parent, and every bound override's meaning on it, become historical. That meaning is carried into the copy byte for byte, except SD-5's row, which SD-7 conforms;
- **every later NE successor overrides the copy**, not the raw NE.

The copy keeps the file name `native-evidence.md`, so every name reference ("native-evidence.md section 10", "NE §10", WS:1340-1344's "the composition in native §10") resolves to it.

**Line numbers.** The copy's lines equal raw NE's through line 122; from raw line 123, where RUST3-LIM's override adds two lines, they shift. Laws cite NE by raw line (`NE:NNNN`), and those citations stay true of the historical parent. `copies-report.json`'s `lineMap` translates every raw line exactly: unchanged lines map in runs `[rawStart, rawEnd, copyStart]`, and each overridden line lists its first copy line and span. New citations should name NE7 lines.

**Residual hazard (probe 3c).** `verify_design` has no notion of selection. A later override of a raw NE line binds, and only review catches it. This is the copy form's hazard, the same as B-S9's and capability-totality's. When the drafting scan ran, no unbound draft in arch overrides NE or either NEM copy.

**Binding order.** NE7 is the effective text at `6190e66`. If any NE override binds before SD-7, `build_sd7.py`'s lock assertions fail, and the copy must be rebuilt on the new lock and re-reviewed.

## Lead decisions

Each decision is made under the owner's standing direction to decide on the lead's recommendation and to block only where no recommendation exists. Each names the alternatives it rejects. The owner may reverse any of them.

**LD-7.1. Form: B-S9's complete-copy form for NE; fresh line overrides for the remedy.** See "The form".
- **Rejected:**
  - **(i) for NE**: refused by `verify_design`, or an erratum that contradicts the bound row.
  - **(iii) a `verify_design` successor**: a generator rebuild and re-pin for a case the copy form already handles lawfully.
  - **Unbinding SD-5**: rewriting an accepted binding (B-S9 LD-1).
  - **Item 25's row as a raw-NE line override** (NE:3539 is free): it would bind a new meaning onto the very file this unit makes historical.

**LD-7.2. The copy is NE's effective text, carried byte for byte except the two hunks.**
- **Rejected:** a copy of raw NE plus SD-7's edits. It would drop 39 bound meanings from six accepted successors (B-S9 LD-1: "Raw-parent copies … carry no bound meaning").

**LD-7.3. The conformed row changes only what MD5 changes.**
- The provenance, EE-3b's parenthetical, EE-5a's description, item 24's admitted cases and first-refusal sentence, and the remedy phrase (MD5:1182's words exactly). Everything else is SD-5's.
- **Rejected:**
  - restating item 24's "who refuses each form" phases (C2a) in the contract row: they are D's implementation order, and the first-refusal sentence states the route consequence for every phase;
  - rewording the remedy beyond MD5's phrase.

**LD-7.4. Item 25's row sits after the NOT-SELECTED row.**
- It reuses that row's class, code and detail, so the two are adjacent and "the row above" is literal.
- **Rejected:** after the SD-5 row, which separates the precedent from its reuse.

**LD-7.5. The remedy keeps both clauses and adds the three forms and one next step, in both NEM copies.**
- **Rejected:**
  - a replacement string, which drops the NOT-SELECTED wording that the only other reaching key needs;
  - one copy only, which splits the two model files that X12-0 and B-S9 keep equal;
  - the historical capability-totality copy and the frozen v2 file, which B-S9's selection retired.

**LD-7.6. NES's route registry is not extended.**
- Its keys are the capability and Coverage-cause guards' internal keys, and NES is registered bytes whose raw SHA-256 is a `payloadSchemaDigest`. `ExcludedForm` is D4's and the request owner's refusal, routed in NE §10's table as SD-5's is.

## Points for the reviewer

- **R1 (LD-7.1, LD-7.2).** Is the complete-copy form for NE lawful and right here? Is the selection statement, the line map and the residual hazard acceptable for a document many laws cite by line?
- **R2 (LD-7.3).** Does the conformed row state M3-D r5 item 24's predicate exactly, with EE-3b keeping only its capability form and an analyzer's own mounted root admitted? Is the remedy MD5's phrase exactly?
- **R3 (LD-7.4, LD-7.5).** Is item 25's row LD-R4-2's route exactly? Is the widened remedy true for every condition that reaches `PROVIDER.NOT_SELECTED`?
- **R4.** Is NE7 exactly the effective NE plus the two hunks? `check_sd7.py` diffs it.

## Cross-law items

| ID | For | Item |
|---|---|---|
| **X-SD7-NE** | every later NE successor; the native, WS and lead owners | NE7 is the selected NE. Override NE7's lines, cite NE7 lines, and translate older `NE:NNNN` citations with `copies-report.json`'s line map. |
| **X-SD7-J1** | M3-J1's next revision | Row 57 (MD5:1222) cites "NE §10 (SD-7)": NE7's line 3822. Row 56's basis is SD-5's row as SD-7 conforms it (NE7:3824). J-C20 tests both. |
| **X-SD7-D** | M3-D's next revision | X-D4-NE and F14/F15 are done. D4-T1's remedy assertion takes SD-7's remedy, and D4-T2's remedy assertion "follows SD-7" (MD5:850) with the widened string. |
| **FA1-F1** | the native reference owner | Unchanged and still owed (the `stage_authority` refresh). It overrides other lines of the same B-S9 copies, so it composes with SD-7's line 1159. |
| **SD-5b** | lead | Unchanged. Any contract row it adds goes into NE7. |

No owner question is raised.

## Binding

SD-7 has two passage overrides and seven candidates, so it binds on the `verify_design` at main `6190e66` with no prerequisite. After `ACCEPT-DESIGN-UNIT`:
- copy the review to `docs/implementation/m3/reviews/grok-sd-7-r1/review.json`;
- complete `sd-7-unit.json`;
- append `{record, subjectManifest, review, assent}` to the product lock in a binding-only product commit;
- run plain `verify_design`.

It changes no product byte and no generation source.

**Evidence runs** (`/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B` at `nice -n 19`, read-only):
- `build_sd7.py`, then `build_sd7.py --check`: identical bytes.
- `check_sd7.py`: pass.
- `verify_scratch.py --rev 6190e66` and on the main checkout at `6190e66`: SD-7 binds, 92 to 93, with two overrides and no supersession. The selected inventory and inheritance are unchanged. The rejected forms refuse as stated. Later successors give PASS (an NE7 line), REFUSED (a second line-1159 override) and PASS (a raw NE line, the residual hazard). On the checkout, 40 generation sources are verified.

## Controls owed by the implementing units

- **D4-T1 / D4-T4** (D4): a manifest-class refusal's envelope carries SD-7's conformed remedy. An `analyzer` manifest with its own name-bound mounted root passes R10a, and (a), (b) and (c) refuse as EE-5a (MD5:818-825).
- **D4-T2** (D4): a request-class refusal is `request-rejected` 2, `REQUEST.UNSATISFIABLE`, `PROVIDER.NOT_SELECTED`, subject `excluded-form:<class>` with the widened remedy, and no runId or executionId. Two forms in one request name the first class in the order EE-2, EE-4, EE-6a.
- **The NOT-SELECTED cell** keeps its route and now carries the widened remedy.

## Not claimed

- No product code, test, build or checker run was made. Only the three evidence scripts ran, read-only.
- Neither native model was imported: `check_sd7.py` parses both with `ast`.
- No law is amended. No class, exit, error code, fault cause or public detail code is added, and no NES, REG, D9, WS, WSE, SL or product byte changes.
- No Linux claim.
