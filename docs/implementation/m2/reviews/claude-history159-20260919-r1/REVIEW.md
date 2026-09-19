# Independent bounded review — historical SQL regression controls 159 (Rust, test-only)

Reviewer: Claude (actual independent reviewer; Codex remains implementation owner). 2026-09-19.
Request: `history159-mirrors160-20260919-REQUEST.md` (bytes as read: `claude-out/REQUEST-as-read.md`); README and
OWNER-DECISION.md read in full. Scope: the delta of frozen `history-sql-regressions-checkpoint-159` over frozen 158 —
one `cfg(test)` module in `historical_rows.rs`, answering my 154 T-1 and making the cost of 154 F-1 visible. No
production change, host mapping, repair or authority. The owner decision itself is assessed in my separate 160 review.
No frozen/selected/product edit; scratch only, `-I -B`, dedicated targets; no commit, push or delegation; no cumulative
approval.

## 1. Subject verification (before use)
| Item | Value |
|---|---|
| `subject.tar.xz` | 4,107,656 bytes, SHA-256 `146da24dd77b920a09129e72519d12e29db270caca27a5734b0dd72bfe42b3b7` = `archive-pin.json` (the request gives no digest; I pinned the archive's own pin and every member) |
| Members | 381/381 regular, length + SHA-256 equal to the manifest, from the tar before extraction; 0 unsafe/extra; re-verified at the end |
| Product pins | 342/342; none unpinned |
| Parent | `parent-inputs.json` = **my own** verified 158 extraction (342/342); 341 unchanged; 1 changed |
| **Production equality** | `historical_rows.rs` before its first `#[cfg(test)]` item is byte-identical to 158; the two test-only DDL constants are unchanged; the tests module is the tail. (My first check wrongly demanded a single `cfg(test)` item and reported "false" — slip preserved in `product-pins.json`.) |
| Owner checks, fresh scratch | 118/118 security tests; strict workspace Clippy clean |

## 2. Evidence (`probes/closure.py`)
**2.1 My 154 carriers, unchanged, on this tree:** 319 Python-built scenarios → results **byte-identical** to my 154 run
(production did not move).

**2.2 Closure of 154 T-1, executed.** My five surviving mutants re-applied here:

| 154 survivor | 159 | Killing test |
|---|---|---|
| mirror may be NULL although the body has the value | **killed** | DDL1 GRANT with NULL token; RA with NULL `request_ref` |
| body `seq` not bound to the row `seq` | **killed** | independent body-sequence refusal |
| non-hex / upper-case previous digest still `Consistent` | **killed** | chain test (values preserved, `Unverifiable`) |
| genesis previous ignores the requested generation | **killed** | consistent generation 2 |
| lone surrogate replaced by U+FFFD | **killed** | file-patched UTF-16le/be body |

The surrogate test is well built: the *original* body held U+FFFD, so digest and request mirror still describe U+FFFD
— a lossy decoder would reproduce exactly the admitted record, and only refusing the octets distinguishes the two.

**2.3 Masking.** Five further narrow mutants: surplus mirror tolerated only for `token`; only for `request_ref`;
missing `token` tolerated (the DDL1-lawful GRANT) while other missing mirrors stay refused; only lone *low* surrogates
replaced — **all killed**. One survives both suites and is equivalent: a case-insensitive chain comparison is
unreachable behind the `!hex(..)` guard, which already sends upper-case values to `Unverifiable`.

**2.4 The compatibility controls say what they claim.** The named test inserts, under the **unchanged** frozen DDL1, a
GRANT with `token` NULL (accepted by DDL1's CHECK) and, under both DDLs, a NARROW with surplus metadata — by `INSERT`,
after the honest r1 attempt by `UPDATE` was refused by the frozen append-only trigger (evidence retained). Each is
refused `RowBinding`. So the cost of the policy is demonstrated on physically lawful legacy rows, not asserted.

## 3. Findings
No defect and no finding of substance.
- **N-1 (note)** The compatibility test pins the *policy*, so it will (rightly) fail the day a diagnostic compatibility
  reader is added unless that reader is a separate entry — which is what OWNER-DECISION.md requires. Worth keeping the
  test's name as explicit as it is.
- 154 N-1..N-4 are restated accurately in the README as obligations of the opening owner / as limits; I confirm the
  wording matches what I observed (deferred `BEGIN`, write transaction, `SAVEPOINT`; `usize::MAX`; per-generation
  `WHERE`; defensive odd-length check).

## 4. Closure of my 154 items
| Item | Status |
|---|---|
| **T-1** five unpinned regressions | **Closed** — all five killed; four masking variants killed; one equivalent |
| **F-1** NULL-iff-absent mirror rule undecided | **Decided and demonstrated here; reconciled in reference 160** — see that review for the assessment of the decision and one wording gap in its public route |

## 5. Bounded verdict
**159: reviewed, no finding of substance. Production bytes are identical to 158; my 319 independent carriers give
byte-identical results; all five 154 T-1 mutants and four further masking mutants are killed by real-SQL tests built
under the unchanged frozen DDLs in all three encodings; the compatibility cost of the strict mirror policy is shown on
physically lawful legacy rows.** Not approval of the policy's reference wording (160), of host mapping, custody,
population composition or any cumulative standing.

Evidence (`claude-out/`): `pin-verification.json`, `pins.py` → `product-pins.json`, `diffs/`, `owner/`,
`probes/{closure.py, closure.json, closure.log}`, `io/carriers/`, `hashes.txt`. The carriers and the Rust probe are the
unchanged files of my 154 review.
