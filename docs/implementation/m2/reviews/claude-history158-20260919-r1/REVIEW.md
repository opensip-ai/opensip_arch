# Independent bounded review — historical decoder regressions 158 (Rust, test-only)

Reviewer: Claude (actual independent reviewer; Codex remains implementation owner). 2026-09-19.
Request: `history158-20260919-REQUEST.md` (bytes as read: `claude-out/REQUEST-as-read.md`). Scope: the delta of frozen
`history-regressions-checkpoint-158` over frozen 157 — three fixture rows, one test-count assertion, an owner
structural checker and cumulative provenance, answering my 152 T-1, N-2 and N-5. No production change; no authority,
custody or selection claim. No frozen/selected/product edit; scratch only, `-I -B`, dedicated targets; no commit, push
or delegation; no cumulative approval.

## 1. Subject verification (before use)
| Item | Value |
|---|---|
| `subject.tar.xz` | 4,118,436 bytes, SHA-256 `7bc503c08d3f82973a6e35bbf1c8b7ed0da241863670a3a4e7c756e3f86765d3` = `archive-pin.json` (the request gives no digest; I pinned the archive's own pin and every member) |
| Members | 393/393 regular, length + SHA-256 equal to the manifest, from the tar before extraction; 0 unsafe/extra; re-verified at the end |
| Product pins | 342/342; none unpinned |
| Parent | `parent-inputs.json` = **my own** verified 157 extraction (342/342); 340 unchanged; 2 changed (decoder file, fixture) |
| **Production equality** | `historical_record.rs` before its single `#[cfg(test)]` module is byte-identical to 157 |
| Fixture | the previous 1,624 rows are an exact **byte prefix** of the new file; exactly three rows appended |
| Checker origin | `table-check-origin.json` names my 152 script with SHA-256 `67fc7105…afda2` — equal to the file in my 152 evidence |
| Owner checks, fresh scratch | 114/114 security tests; strict workspace Clippy clean |

## 2. Evidence
**2.1 The three rows** (`probes/check158.py`). All 1,627 rows re-judged by my 152 oracle (third-party `jsonschema` +
pinned canonicalizer): **0 disagreements, 214 admitted**. Each new row is canonical bytes and violates **exactly one**
rule — undoing only the named violation makes it admissible (`recordSchema` 3→1; `SEAL`→`ICI`, the only kind that
shape fits; `z`→`Z`). No masking by a second violation.

**2.2 Closure, executed** (`probes/mutation.py`): my three 152 T-1 survivors, re-applied to this tree, are all
**killed** by the owner's Rust test.

**2.3 The structural checker** (`check158.py`, 20 source-level variants through the owner's script). It exits 0 on the
frozen source and **non-zero** for every vocabulary, field-set and array-bound change I tried: a word added to
effectClass / REV reason / TERMINAL cause / stateClass / RCO outcome; a word removed from platform / ICO outcome; an
extra required member; a 15th kind; a COMMON member removed; scope duplicates allowed; an item bound moved; residual
uniqueness flipped. It also fails closed on an unrecognised extraction shape (helper renamed; an arm rewritten around
its table) and on a schema file that differs by one byte. It fails on a pure *reordering* of a vocabulary as well —
harmless strictness. As the README says, it does **not** check numeric/length bounds or `recordSchema` (three such
variants exit 0); those are the fixture's job, and §2.4 shows the fixture does it.

**2.4 Are the two controls complementary?** Six mutants, each run through both:

| Mutant | Rust fixture test | structural checker |
|---|---|---|
| `recordSchema` 1 or 3 | killed | passes |
| `SEAL` as a kind | killed | fails |
| lower-case `z` | killed | passes |
| table intact but arm short-circuited (`choice(..) \|\| true`) | killed | passes |
| table intact but `choice()` accepts any string | killed | passes |
| closed-field count check dropped | killed | passes |

Text-level equality cannot see control flow; the sampled fixture can. Vocabulary extension cannot be seen by sampling;
the text-level check can. Together they cover what each misses.

## 3. Findings
No defect and no finding of substance.
- **N-1 (note, the honest residue)** One class escapes *both* controls: a short-circuit that admits a single
  *unsampled* word while leaving the table text intact (e.g. `choice(..) || text == "HE-3"`). Nothing cheap closes
  it; it is what code review of this 250-line decoder is for, and the README already says the checker "is not a proof
  of all Rust control flow". I mention it only so the pair of controls is not later described as complete.
- **N-2 (note)** The checker's schema pin is a hard-coded SHA-256 inside the script; if the frozen schema is ever
  legitimately re-pinned the script must change with it — good, but it means the script is part of the pinned set and
  should stay frozen with the fixture provenance (it is, under `scripts/`).

## 4. Closure of my 152 items
| Item | Status |
|---|---|
| **T-1** three unpinned boundaries | **Closed** — three isolated rows; my three mutants killed |
| **N-2** vocabularies cannot be pinned by sampling | **Closed** as far as it can be — owner structural check, fails for all 14 vocabulary/field/bound variants and fails closed on unknown shapes; residue in N-1 above |
| **N-5** provenance split over two files | **Closed** — cumulative provenance records 1,627 rows, pins and versions; 152's originals retained untouched |
| N-1, N-3, N-4 | documented as limits, accurately; open by design |

## 5. Bounded verdict
**158: reviewed, no finding of substance. Production bytes are identical to 157; the old fixture is a byte prefix of
the new one; each of the three new rows isolates one violation and all 1,627 agree with my independent oracle; my
three 152 mutants are now killed; the owner's structural checker rejects every vocabulary, field-set and array-bound
change I tried and fails closed on shapes it does not recognise, while the fixture catches the control-flow changes the
checker cannot see.** Not approval of any consumer of the decoder, of SQL/population/custody layers, or of any
cumulative standing.

Evidence (`claude-out/`): `pin-verification.json`, `pins.py` → `product-pins.json`, `owner/`,
`probes/{check158.py, mutation.py, mutation.json, mutation.log}`, `io/{check158.txt, checker-variants.json, variants/}`,
`hashes.txt`. The oracle is the unchanged `oracle.py` of my 152 review.
