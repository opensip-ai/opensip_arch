# Independent bounded review — migrated-carrier regressions 162 (Rust, test-only)

Reviewer: Claude (actual independent reviewer; Codex remains implementation owner). 2026-09-19.
Request: `migrated162-20260919-REQUEST.md` (bytes as read: `claude-out/REQUEST-as-read.md`); README read. Scope: the
delta of frozen `migrated-regressions-checkpoint-162` over frozen 161 — the `cfg(test)` module of
`inherited_schema.rs`, answering my 155 T-1 and naming 155 N-1/N-2 as limits. No production change and no migration
authority claim. No frozen/selected/product edit; scratch only, `-I -B`, dedicated targets; no commit, push or
delegation; no cumulative approval.

## 1. Subject verification (before use)
| Item | Value |
|---|---|
| `subject.tar.xz` | 4,104,576 bytes, SHA-256 `36f3ec6d9a8e3bbad8820956b73a6eb81a9978a4594c6880d072f077d8f91efe` = request = `archive-pin.json` |
| Members | 372/372 regular, length + SHA-256 equal to the manifest, from the tar before extraction; 0 unsafe/extra; re-verified at the end |
| Product pins | 343/343; none unpinned |
| Parent | `parent-inputs.json` = **my own** verified 161 extraction (343/343); 342 unchanged; 1 changed |
| **Production equality** | `inherited_schema.rs` before its single `#[cfg(test)]` module is byte-identical to 161; every file under a `fixtures/` directory is unchanged |
| Owner checks, fresh scratch | 121/121 security tests; strict workspace Clippy clean |

## 2. Evidence (`probes/closure.py`)
**2.1 My 155 carriers, unchanged, on this tree:** 166 Python-built migrated carriers → results **byte-identical** to my
155 run.

**2.2 Closure of 155 T-1, executed.**
| 155 survivor | 162 | Killing test |
|---|---|---|
| empty inherited table accepted as a migrated carrier | **killed** | refused at `open` itself, before any population read |
| stored-octet budget not carried across inherited generations | **killed** | two fully closed generations; UTF-16 logical-only budget must fail *inside* the historical reader |
| inherited logical bytes not counted | **killed** | independent SQL totals of logical and stored bytes across two generations, both formats × three encodings |

The aggregate test computes its expectations from SQL (`length(CAST(body AS BLOB))` and the decoded text), not from
the code under test — the right kind of oracle. The third test admits a closed-and-marked last inherited generation and
a foreign object *read-only* and says in its name that this neither certifies act C nor forbids foreign objects: 155
N-1/N-2 are now named limits, not silent behaviour.

**2.3 Masking** — four further variants:
| Mutant | Owner's tests |
|---|---|
| stored octets counted as logical bytes | killed |
| current-generation bodies not counted | killed |
| **logical** budget not carried across inherited generations | **survives** (also my carriers) |
| **record** budget not carried across inherited generations | **survives** (also my carriers) |

## 3. Findings
- **T-1 (very low) — the stored-cap propagation now has a test; its two twins do not.** With the per-reader limit for
  logical bytes or for records left at the full budget, every outcome stays a refusal, because the outer aggregate
  check still fires — but one inherited generation later, after that generation has been read and copied. That is
  exactly the "too late for the per-reader retained copy bound" argument the README makes for stored octets. The same
  two-generation fixture with (a) `max_body_bytes` = logical total − 1 under UTF-8 and (b) `max_records` = total − 1,
  asserting the refusal comes from the historical reader (`Historical(Bound)`), pins both.
- No other finding. 155 N-3 (strict mirrors refuse the whole carrier) is now an explicit owner decision (159/160);
  155 N-4 and N-5 are restated accurately.

## 4. Closure of my 155 items
| Item | Status |
|---|---|
| **T-1** three unpinned regressions | **Closed** — all three killed; two sibling propagation checks remain (T-1 above) |
| **N-1** closed-and-marked last inherited generation; **N-2** foreign objects | **Named as read-only limits** in a test and the README; act C's obligation stays open, correctly |

## 5. Bounded verdict
**162: reviewed, no finding of substance. Production bytes and all fixtures are identical to 161; my 166 independent
migrated carriers give byte-identical results; all three 155 T-1 mutants are killed by real-SQL tests whose
expectations come from SQL itself; two further accounting variants are killed. The per-reader propagation of the
logical-byte and record budgets is still unpinned (the outer bound refuses in every case, one generation late).**
Not approval of act C, migration writes, custody or any cumulative standing.

Evidence (`claude-out/`): `pin-verification.json`, `pins.py` → `product-pins.json`, `diffs/`, `owner/`,
`probes/{closure.py, closure.json, closure.log}`, `io/carriers/`, `hashes.txt`. Carriers and Rust probe are the
unchanged files of my 155 review.
