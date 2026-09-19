# Independent bounded review — Rust clock regression follow-ups 139

Reviewer: Claude (actual independent reviewer; Codex remains implementation owner). 2026-09-19.
Request: `clock139-20260918-REQUEST.md`. Scope: the delta of frozen `clock-followups-checkpoint-139` over frozen 136 —
test rows and one comment closing my clock134 T-1 (signed straddle) and T-2 (inclusive continuity maximum), and N-1.
**No predicate or error changed.** Private, uninstalled; no adapter, renderer, host authority or storage claim. No
frozen/selected/product edit; scratch builds, dedicated target dirs; no commit, push or delegation. Test-only keys have
no authority.

## 1. Subject verification (before use)

| Item | Value |
|---|---|
| `subject.tar.xz` | 4,266,168 bytes, SHA-256 `c29b0ab005ff1e183e5003826f9e2edfa4cccdd523a43e6f3db199c92d8218c3` = request and `archive-pin.json` |
| Members | 384/384 regular, length + SHA-256 equal to the manifest, from the tar before extraction; 0 unsafe/extra; re-verified clean at the end |
| Product pins | 330/330 equal; none unpinned |
| Parent | `parent-inputs.json` equals **my own** verified 136 extraction (330/330); 325 unchanged |
| Changed | `trust.rs` (one 3-line comment + a row count), `trust_time.rs` (a row count), three fixtures |
| Fixtures | old bytes are **exact prefixes**: clock 1,892 → 1,894, recovery cases 871 → 873, recovery epochs 282 → 284 |
| Host pins | host85 receipt: 210 sources, all equal the product pins |
| Reference | `reference138/` pin and manifest copies equal the repository's 138, which I verified and reviewed today |

## 2. Evidence

**Source delta is comments and counts only** (both diffs read in full: 8 + 4 lines). So behaviour must equal 134/136 —
and does: my 40,000-case cross-language clock corpus and my 11 genuinely signed edge recovery epochs produce outputs
**byte-identical to the 134 run**. 80/80 security tests; strict workspace Clippy clean.

**The four appended rows re-derived from reference 138** (`probes/owner_rows.py`, my extraction of 138):
- recovery `issuedAt 9999-10-03T00:00:00Z` / wall `…10-02T23:59:59Z` → `REFUSE TIME_RANGE`; the reverse → `APPLIED`
  with equal writes. Both epochs verify at the carrier with **3 valid signers** — genuinely signed, inside the issue
  skew, on opposite sides of the edge. 2/2 agree.
- clock rows (ordinary and report-only): anchor wall `9999-12-31T23:59:58Z`, +1 s same boot → continuity
  `[253402300799, 0]` is *present* and the outcome is the ordinary `BeyondHorizon` refusal, not a range refusal —
  i.e. the inclusive maximum is exercised and the plausibility/horizon logic, not the range guard, decides. 2/2 agree.

**Discrimination** (`probes/mutation.py`): the two mutants that **survived** the owner's tests on 134 are re-run
unchanged and are now **killed** — guard testing the wall (by the signed recovery test) and exclusive continuity
maximum (by the clock projection test). Three variants I added to check the rows discriminate rather than merely exist
are killed too: guard on `max(issued, wall)`, guard on `min(issued, wall)` (each needs *one* of the two straddle
directions, so both rows are doing work), and a continuity maximum one second too generous. **5/5.**

**N-1 comment** is accurate: a shape-admitted wall is a calendar instant, so `wall ± 86,400` cannot overflow `i64`;
`Input("TIME_RANGE")` is an unreachable arithmetic backstop and the reachable spelling is `Refused("TIME_RANGE")`.

## 3. Closure of clock134

| Item | Status |
|---|---|
| **T-1** guard operand unpinned by signed rows | **Closed** — two genuinely signed straddle epochs, both directions; original and min/max variants killed |
| **T-2** inclusive continuity maximum unpinned | **Closed** — ordinary and report-only rows at exactly the last second; exclusive and over-generous bounds killed |
| **N-1** two spellings of one overflow | **Closed** by comment; no code change was needed |
| **N-2** no Rust mapping of the typed refusal to a public detail/subject/remedy | **Open by design** — no adapter or renderer exists; the reference side (138) now fixes the vocabulary the adapter must reproduce |

## 4. Findings
None. One observation for the next successor rather than this one: with 138 the reference binds each public remedy
to its tag by schema constant; when the Rust adapter arrives, the cheapest cross-language check is to feed its
projected detail through those same two schemas.

## 5. Bounded verdict
**139: reviewed, no finding. Test-only successor: behaviour is byte-identical to 134 on my 40,000-case and signed
corpora; the four appended rows re-derive from reference 138 with genuinely verifying signatures; old fixtures are
exact prefixes; and both of my 134 survivors, plus three variants, are now killed. clock134 T-1, T-2 and N-1 are
closed.** Not approval of an adapter, renderer, storage, host authority, OS, release or any cumulative standing.

Evidence: `claude-out/pin-verification.json`, `product-pins.json`, `trust.rs.diff`, `trust_time.rs.diff`, `owner/`,
`probes/{owner_rows.py,mutation.py,mutation.json,mutation.log}`, `io/clock/`, `io/owner-rows-rederived.json`, `hashes.txt`.
