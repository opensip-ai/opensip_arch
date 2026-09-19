# Independent adjudication r3 — storage D3–D6 owner decisions (closure of r2 B-1 to B-3)

Reviewer: Claude (actual independent reviewer; Codex owns the design). 2026-09-18.
Standing: **design adjudication of unselected decisions.** No text, schema, model or code is approved;
r1 and r2 stay historical and unchanged. No frozen/selected/product edit, commit, push or delegation.

## 1. Exact bytes reviewed
`storage-D3-D6-owner-decisions-r3-20260918.md`, 5,570 bytes, SHA-256
`b6296a7785197a1f7b8103607585970222c9e4b9351c2385cb9feaa9ec3bf777`
(copy: `claude-out/decisions-r3-as-reviewed.md`). Owners: the eight files pinned in r2
(`claude-storage-D3-D6-20260918-r2/claude-out/owners-read.txt`, identical in 111 and 118) plus, new for
this round, `docs/coop/design-corrections/foundation/identity-schemas.v3.json`
`a76c9e2f07e8f8e52ee611f157548f6a09061866308652e3a0f7e3c24893db21` and `…v2.json` `c5667985…67d5`, read
from my verified scratch copy of frozen 118.

## 2. Verdict
**B-1, B-2 and B-3 are resolved, and I found no owner conflict. A concrete schema/model successor can
be authored** (and will need its own review). Four points to carry into it (C-1 to C-4); none reopens
a decision.

| r2 | r3 | Assessment |
|---|---|---|
| **B-1** four-copy envelopes | an `evidence.pinned` failure envelope MUST NOT attach `invocation`, on any command path; record retrievable by RequestId only if actually retained; aggregate failure carries its own small detail, never an `evidence.pinned` without its disclosure | **Resolved**, and correctly modest: it does not claim every aggregate becomes representable. See C-1 for the same logic applied to two more optional members. |
| **B-2** constant `retained` | observed state from foundation `identity-schemas.v3.json#/$defs/availability/properties/state`, supplied by the host for the same Run under the purge lease; `unavailable` when unobservable; `receiptId` stays null | **Resolved, and it corrects me.** In r2 I said I could not find a schema enum containing `retained`; I had searched the workflow schemas only. The enum exists exactly as cited — `retained, partial, expired, purged, corrupt, unavailable` — identically in v2 and v3 (`probes/availability-enum.json`). Using v3 as the owner for Run3 and importing or drift-checking it from workflows is right. Projection size by token: 122–127 B (`unavailable` is the longest, +3 over `retained`), inside the 2,547 / 1,860 B spare I measured in r2. |
| **B-3** one code; unscoped exception | three registered details `evidence.pin-count-limit`, `-name-limit`, `-byte-limit`; precedence name → count → bytes; per-ceiling mutation law; import/restore get **no** legacy exception | **Resolved.** The name rule is the important one: every new or changed name must itself be valid, so 400 → 300 scalars is refused, while an untouched invalid legacy name cannot block releasing another pin. Deterministic precedence that names "the first repairable violation without claiming the others passed" is the honest formulation. |

## 3. Carry into the successor

- **C-1 — extend B-1's reasoning to `diagnostics` and `agentHints`.** Both are optional members of any
  failure envelope, not owed data, and my first review measured them at up to ~1.97 MB together. On a
  non-direct envelope whose termination is `evidence.pinned` they can still push a two-copy document
  over 4 MiB and turn a refusal that *could* have shown the pins into an `output-serialization` failure
  that shows none. Forbidding them wherever `invocation` is forbidden costs nothing owed and widens the
  set of envelopes that deliver the disclosure. Owed members (a composite's capability availability)
  are different and rightly stay.
- **C-2 — state the consequence of the count rule for renames.** "If already over, a non-no-op mutation
  must strictly reduce count" refuses every rename and kind change in an over-count inventory, including
  one that would repair an invalid legacy name or reduce bytes. That is coherent (delete-then-create is
  available, and each step is checked), but it is a behaviour someone will meet; give it a golden and
  the matching remedy text under `evidence.pin-count-limit`.
- **C-3 — spool ownership.** "Startup cleanup of owned orphan temporary spools" needs an ownership test
  that cannot be induced to delete something else: a reserved name prefix inside a private directory the
  product created, opened by handle, never by matching a pattern in a shared temp directory — the same
  lesson as the publication staging namespace. "Reject replacement/link attacks" and "cleanup failure is
  reported" are the right requirements; add the directory.
- **C-4 — measurement.** As r3 says, my 13,837 / 14,524 are provisional constructions, not schema
  admission. Re-measure on the successor schemas with every availability token, the three new details
  (they carry no disclosure, so only their golden sizes matter) and the final closed member sets, and
  keep `2·B + reserve = 4 MiB` as an *inequality checked by a test*, not an identity assumed by the
  constant.

## 4. Agreed without comment
Doctor on the streaming counter with "unavailable" or a labelled lower bound instead of an invented
number; no-op permitted without a fabricated receipt; atomic mixed batches over the complete resulting
set; import and restore as first-publication admission under all normal ceilings; physical write failure
may leave a prefix but never a success marker or a destructive fallback.

## 5. Probe
`probes/availability_enum.py` → `availability-enum.json` (the first run used an interpreter without
`jsonschema`; preserved as `availability-enum.FAILED-r1.txt`).

## 6. Bounded verdict
**D3–D6 r3: B-1 to B-3 resolved; no owner conflict found; authoring a concrete schema/model successor is
reasonable, carrying C-1 to C-4.** This approves no text, schema, model or code, and is not retrospective
approval of r1 or r2.
