# Independent bounded review — anchor adapter regressions 156 (Rust, test-only)

Reviewer: Claude (actual independent reviewer; Codex remains implementation owner). 2026-09-19.
Request: `anchor156-20260919-REQUEST.md` (bytes as read: `claude-out/REQUEST-as-read.md`). Scope: the delta of frozen
`anchor-adapter-regressions-checkpoint-156` over frozen 155 — two `cfg(test)` modules. It answers my 150 F-1 and
documents 150 F-2. No production change, no host mapping, no custody or authority claim. No frozen/selected/product
edit; scratch only, `-I -B`, dedicated targets; no commit, push or delegation; no cumulative approval.

## 1. Subject verification (before use)
| Item | Value |
|---|---|
| `subject.tar.xz` | 4,131,496 bytes, SHA-256 `aa3003ac18ebebf34a88afb75ebfe390f6cc3e5088d4d10908bb6a6d908e0563` = request = `archive-pin.json` |
| Members | 392/392 regular, length + SHA-256 equal to the manifest, from the tar before extraction; 0 unsafe/extra; re-verified at the end |
| Product pins | 341/341; none unpinned |
| Parent | `parent-inputs.json` = **my own** verified 155 extraction (341/341); 339 unchanged; 2 changed (`bracketed_capture.rs`, `generation_anchor.rs`); 0 added |
| **Production equality** | in both files everything before the single `#[cfg(test)]` module is byte-identical to 155, that module is the tail of the file, and the files with the test module removed are equal |
| Owner checks, fresh scratch | 114/114 security tests; strict workspace Clippy clean |

No host receipt is claimed for the added tests; 155's host98 covers the unchanged production (verified in my 155 review).

## 2. Closure of 150 F-1 — executed, not read
I re-applied the nine mutants that survived frozen 150 (same edits, adapted to 155's `g.generation()` spelling) to the
156 tree (`probes/mutation.py`, all compiled, baseline green):

| 150 survivor | 156 | Killing test |
|---|---|---|
| A1 any TERMINAL counts as closed (the 146 defect at this seam) | **killed** | closure cause × marker (6 real carriers) |
| A2 closed always false | **killed** | same |
| A3 marker ignored | **killed** | same |
| A4 first generation instead of the requested one | **killed** | requested-generation test (+ an existing 155 test) |
| A5 / A6 after-slot filled with the before observation | **killed** | within-bracket test, via the existing private phase hook |
| A8 run join short-circuited | **killed** | right digest / wrong run |
| A10 project taken from the witness | **killed** | foreign-project witness on a real carrier |
| R6 second-capture failure downgraded to `UnavailableBusy` | **killed** | malformed marker in either capture, queried or other generation |

The tests are real I/O (SQLite file, codec-encoded witness/floor, physical captures); none forges a capture or adds a
production hook. The malformed-marker test also pins the exact typed error, the retained raw bytes, the retry count
and a successful `TRUNCATE` checkpoint after unwinding. **150 F-1: closed.**

**My frozen-150 probes, unchanged, on this tree** (`probes/stage2.py`): 12,432 physical reads + 96 between-capture
scenarios judged by the reference law → **0 mismatches**; so 155's migrated-carrier production changes did not move
the fresh-carrier anchor behaviour.

## 3. Test masking — five further mutants
| Mutant | Owner's 114 tests | My 150 probes | Verdict |
|---|---|---|---|
| mask-1 witness **before**-slot filled with the after observation | survive | within-capture probe differs | **T-1** |
| mask-2 floor **before**-slot filled with the after observation | survive | differs | **T-1** |
| mask-3 witness before/after exchanged | survive | differs | **T-1** |
| mask-6 a marker on **any** generation quarantines the requested one | survive | 135 physical mismatches | **T-2** |
| mask-4 `closed` also true when marked | survive | no difference | equivalent: a marked generation returns `generation-quarantined` before `closed` is read |

- **T-1 (low) — the within-bracket test asserts only that the judgment *differs* from the baseline.**
  `assert_ne!(judgment, baseline)` kills "after slot discarded" but not "wrong slot used": with the before-slot wired
  to the after read, the witness case yields `Consistent / sc-trust-floor` instead of `Retry / witness-committed-tail`
  — different from the baseline, so the assertion passes, and it is a *more permissive* answer. Asserting the expected
  state and reason (`Retry`, the anchor's own reason, `stable_w == false` / `stable_h == false`) closes all three.
- **T-2 (low) — every marker in the new tests sits on the queried generation** (well-formed) or is malformed. A
  well-formed marker on *another* generation must not quarantine the queried one (reference: `quarantine_present` is
  per requested generation); one carrier — generation 1 marked, generation 2 queried — pins it.

## 4. 150 F-2 and the notes
README now names capture failure as an additional outcome of `read`, says a malformed marker fails population
admission even outside the queried generation, that a second-capture failure drops the first owned capture, that the
host must map `MarkerUnavailable` to unknown custody (never busy, not-committed or absence), and that the reference's
projected `quarantine_present` precondition differs from production. That is accurate and is what I asked to be
stated; **F-2 is documented, deliberately not closed** — no host mapping exists yet, and I infer none. N-1 (consume
the sealed `AnchorAssessment`), N-2 (direct capture still holds its transaction) and N-3 (covered hazard unreachable,
as in the reference) are stated as they are.

## 5. Bounded verdict
**156: reviewed, no blocking finding. Production bytes are identical to 155. All nine adapter / `read_inner` mutants
that survived frozen 150 now fail real-I/O tests — 150 F-1 is closed, including the purge-as-closed seam. Two small
masking gaps remain: the within-bracket test asserts inequality rather than the expected judgment (before-slot wiring
unpinned), and no test places a well-formed marker on a generation other than the queried one. 150 F-2 is honestly
documented as an open host obligation.** Not approval of host mapping, custody, ledger composition or any cumulative
standing.

Evidence (`claude-out/`): `pin-verification.json`, `pins.py` → `product-pins.json`, `diffs/`, `owner/`,
`probes/{mutation.py, mutation.json, mutation.log, stage2.py, stage2.json, stage2.log}`, `io/*/` (stage-2 outputs;
the large `physical.ndjson` files are deleted after comparison — regenerate with `stage2.py`), `hashes.txt`. The
probes themselves are the unchanged files of my 150 review (`claude-anchor150-20260919-r1/claude-out/probes/`).
