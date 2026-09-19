# Independent bounded review — sealed retained clock bridge 141 (Rust)

Reviewer: Claude (actual independent reviewer; Codex remains implementation owner). 2026-09-19.
Request: `clock141-20260919-REQUEST.md`. Scope, as narrowed by the owner: the delta of frozen
`clock-bridge-checkpoint-141` over frozen 140 — a sealed `ClockProjection` minted only by complete eleven-member record
admission, and a **pure internal bridge** from it to the unchanged integer kernel. This is my record129 F-1 route
(the six-member projection left the seal as an untyped `V`). It is **expressly not a production adapter**: observation
and payload remain asserted values, there is no caller, OS provenance, signature or current-revocation binding,
renderer, persistence, custody or authority, and I infer none. Public range mapping (134 N-2 / 139 N-2) is a later
step. No frozen/selected/product edit; scratch builds, dedicated target dirs; no commit, push or delegation.

## 1. Subject verification (before use)

| Item | Value |
|---|---|
| `subject.tar.xz` | 4,194,360 bytes, SHA-256 `df613a91b90a1f5314596075975ba6f3fec51053951d6a8344c5f095cbd7717c` = request and `archive-pin.json` |
| Members | 418/418 regular, length + SHA-256 equal to the manifest, from the tar before extraction; 0 unsafe/extra; re-verified clean at the end |
| Product pins | 331/331 equal; none unpinned |
| Parent | `parent-inputs.json` equals **my own** verified 140 extraction (330/330); 328 unchanged; `trust.rs`, `trust_time.rs` changed; one fixture added (`admitted-clock-cases.ndjson`); no old fixture touched |
| Host pins | host86 receipt: 211 sources, all equal the product pins |

## 2. What changed (both diffs read in full)
`admitted_trust_records` gains `pub(crate) struct ClockProjection { document: V }` (private field, `document() -> &V`,
no `Clone`/`Default`/constructor) and `AdmittedTrustRecord.clock_projection` now holds and lends that type. Only the
**type** is re-exported; the consuming getter and the fixture constructor (complete `admit` → move the projection out)
are `cfg(test)`. In `trust_time`, the old `assess` becomes `assess_kernel` and the new private `assess` takes
`&ClockProjection`, decodes the six members and the anchor, and calls the kernel; an impossible shape returns
`Error::RetainedRecordInvariant`.

**The kernel did not change:** `assess` (140) and `assess_kernel` (141) are **byte-identical** — 4,994 bytes, no
normalisation at all (`probes/kernel-equivalence.json`), same four parameters.

## 3. Evidence

**Owner checks, fresh scratch:** 81/81 security tests; strict workspace Clippy clean. Owner's six compile clients and
six mutants: reports read.

**3.1 Owner's 44 bridge rows re-derived** (`owner_rows.py`, from reference 138, using only the ISO retained record):
**44/44 agree**; all 44 retained records are admissible; and in all 44 the row's raw `input.record` (seconds) is the
same state as its `retainedRecord` (ISO), so the fixture is self-consistent. Mix: 16 proceed, 22 range refusals over
the three operands, 4 payload-future, 2 horizon; 22 report-only, 22 with an anchor, 16 with a payload.

**3.2 Bridge parity, 30,000 cases** (`gen_cases.py`: my 134 generator, new seed, reference 138, each row carrying the
complete eleven-member record; `rust_probe.rs.txt`; `compare.py`). For every case the probe mints the projection by
complete admission, evaluates through the bridge, and also evaluates the raw kernel on the equivalent integer record:
- **bridge == raw kernel in 30,000/30,000**, every printed member;
- **bridge == reference 138 in 30,000/30,000** — refusal and operand, evaluation, plausibility, admitted time, floor
  and last writes, anchor write, the three expiry states; all ten outcome classes populated (incl. 9,863 range
  refusals and 167 `LastAcceptedRequired`);
- 0 panics, 0 `RetainedRecordInvariant`, projection always exactly six members, caller's record never mutated.

**3.3 Projection only after complete admission.** My 11,225-record admission corpus (129): a projection is minted for
**exactly** the 581 oracle-admissible records and for none of the 10,644 others — including **5,495 records whose six
clock members are perfectly valid** and that fail only on a counter, the serial, the pending challenge, a missing or an
extra member. The six-member seal really is downstream of the eleven-member gate.

**3.4 Escape routes** (`compile_boundaries.py`, 19 clients in three positions — the owner module's parent, the clock
owner, an unrelated module). **16 must-fail, all rejected inside my line:** literal projection from the parent, from
the clock owner and from an unrelated module (E0451); parent-written inherent impls forging or lending `&mut`;
replacing the projection inside an admitted record; write through `document()`; `document()` as `&mut`; **type
erasure — a cloned JSON copy of the six members handed to the bridge** (E0308: the copy "does not carry this type");
`Clone`; `Default`; destructuring; both `cfg(test)` helpers from non-test code; and an unrelated module reaching either
`assess_kernel` or the bridge (E0603 — both are private to the clock owner, which is why no production caller can
exist yet). **3 compile and mark the boundary:** swap of two genuine projections; and, *inside the clock owner*, the
raw kernel with a hand-built `Record`, and the bridge with a hand-built `Observation` — see N-1.

**3.5 Mutants** (9, complementary to the owner's six; all compiled; baseline green): **9/9 killed by the owner's
44-row test** — floor/last swapped, revocation/catalog swapped, root expiry dropped, `lastAccepted` dropped, anchor
ignored, anchor wall taken from the observation, anchor mono erased, bridge forced to report-only, a null member read
as the Unix epoch. No survivor needed my corpus.

## 4. Closure

| Item | Status |
|---|---|
| record129 **F-1** (clock projection leaves the seal as an untyped `V`) | **Closed for the retained-input route** — sealed type, minted only after complete admission, and the bridge accepts nothing else |
| record129 F-1, `RecoveryChallengeProposal` half | closed earlier in 136 |
| 134 N-2 / 139 N-2 public mapping of `TimeRange` | open, next step, as stated |

## 5. Findings and notes
No defect found in the delta.

- **N-1 (note — the production-misuse note the request asks for).** After 141 the *retained* input is sealed, but the
  other two inputs of `assess` are plain structs any code in `trust_time` can build, and `assess_kernel` remains
  callable there with a hand-built `Record`. That is correct for a "trusted clock owner" and is what the owner
  discloses. The consequences to carry forward: (i) the production adapter must live where it cannot reach
  `assess_kernel` — or the kernel must move into a child module of the bridge — otherwise the seal is optional for
  exactly the code that matters; (ii) `Observation` (OS provenance) and `Payload` (signature-verified times, which
  should come from the now-sealed envelope evidence of 135, not from asserted integers) need the same treatment as
  the record before "adapter" can be said; (iii) when callers appear, `RetainedRecordInvariant` must map to a
  fail-stop, not to a clock refusal — it can only mean the admission owner and the bridge disagree about the shape.
- **N-2 (note)** The bridge re-parses timestamps that admission already parsed. Harmless and total (0 invariant
  errors in 30,000); if the projection stored decoded seconds the backstop branch and the double parse would both
  disappear — a simplification for the adapter step, not a request for this one.

## 6. Unresolved limits
Pure internal bridge; no caller; macOS host only; privacy is a compile-time property of this tree. Agreement is with
reference 138.

## 7. Bounded verdict
**141: reviewed, no finding. The kernel is byte-identical to 140; the bridge equals both the raw kernel and reference
138 on 30,000/30,000 independently generated cases and on the owner's 44 rows; a projection is minted for exactly the
admissible records of my 11,225-record corpus, never for the 5,495 whose six clock members alone are valid; all 16
escape routes — including passing a raw JSON copy to the bridge — are refused; 9/9 adapter mutants are killed.
record129 F-1 is closed for the retained-input route. As the owner states, this is not a production adapter: N-1 lists
what must be sealed or relocated before one exists.** Not approval of callers, provenance, signatures, revocation
currency, persistence, custody, OS, release or any cumulative standing.

Evidence: `claude-out/pin-verification.json`, `product-pins.json`, `trust.rs.diff`, `trust_time.rs.diff`, `owner/`,
`probes/{kernel-equivalence.json,gen_cases.py,rust_probe.rs.txt,compare.py,owner_rows.py,compile_boundaries.py,compile-boundaries.json,compile-boundaries.log,compile-*.stderr,mutation.py,mutation.json,mutation.log}`,
`io/{cases.ndjson,cases.rust,records.ndjson,records.rust,generation-stats.json,comparison.json,owner-rows-rederived.json}`, `hashes.txt`.
