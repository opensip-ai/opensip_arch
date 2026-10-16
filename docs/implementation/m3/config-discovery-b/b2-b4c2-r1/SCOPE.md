# B2-b4c2 r1: the blind held-out run, its receipt and the regenerated census record (M3-B unit B2-b4, sub-unit B2-b4c2)

**Lead scope record, 2026-10-16. Unreviewed candidate.** This is the owner's "reviewed after" step: the run of the B2-b4c1 code that Codex accepted (`codex-b2b4c1-r2`), under B2-b4 plan r6 section 2.5.

The base is product `c1778a1`:
- B2-b4c1 is bound (code `ab0eb2c`);
- inventory is v199;
- the B2-b4 description successor is contract successor 165.

## The run

`evidence/run_b2b4c2_blind.py` ran once, under the lane lock at nice 10 with a private TMPDIR:
- **The blind mode, on the reviewed tool bytes** (asserted equal to product main's). It printed exactly `Blind held-out census: 10 entries, 10 measured, 10 passing, 0 errors.` and exited 0. Stderr was empty.
- **Then the ordinary mode:** `--write` regenerated the census record from the lead-readable stores plus the receipt, and `--check` verified it. Both exited 0.

`evidence/run.json` records the run: the exit codes, the stdout line, that stderr was empty, the receipt pin and the tool pin.

**The lead saw:**
- the summary line;
- the receipt, which holds only ids, verdicts and per-mille margins, as the owner decision allows;
- the regenerated census record.

The lead opened no held-out store. Nothing else in this unit, and no check in it, opens one.

## What changes

| Path | Change |
| --- | --- |
| `crates/security/src/custody/discovery_census_held_out.json` | **New, generated** by the blind mode: the receipt. Its state is `holds (blind census)`. It has ten measured rows, each with `integrity: true`, `population: true`, three per-mille margins and `passes2x: true`. It binds the manifest, the tool, the closure, the sizes, the caps, the root lengths and the reference-loading code. |
| `crates/security/src/custody/discovery_census.json` | **Regenerated** by the ordinary mode. Exactly the ten held-out entry rows change, from `outstanding: held-out` to `blind-census` with the receipt row as `result`, and `heldOutMargin` becomes `holds (blind census)`. Every lead-readable and workspace row, `failingEntries` (empty), `caps` (`recorded-margin-holds`) and every other field is unchanged: `evidence/record-diff.json` checks this field by field. |
| `tools/tests/test_discovery_census_blind.py` | **One control adjusted (a lead decision).** The abbreviation control asserted that the repository's receipt was absent, which was true only before the run. It now asserts that the subprocess leaves that receipt exactly as it was (absent before the run, the same bytes after). No other line changes. The tests do not bind the receipt, so the receipt stays current. |

## The result

All ten held-out entries are measured and pass the 2× margin in every dimension. The smallest per-mille margins over the ten are:

| Dimension | Smallest margin |
| --- | --- |
| Objects | 80,944 (about 80.9×) |
| Edges | 39,008 (about 39.0×) |
| Bytes at R = 4,096 | 88,958 (about 89.0×) |

So `heldOutMargin` is `holds (blind census)`, the one state that meets the gate. With the B2-b4b3 lead-readable claim, the T2 margin now holds for every repository entry under the recorded caps (2^22 objects, 2^21 edges, 2^30 bytes).

**Still outstanding:** each workspace row's full-ledger margin. It waits on the B3-b member-observation bound (M3-B r6 item 12). **B2-b is not complete:** B2-c, the host export, remains, as does that bound.

## Checks

See `evidence/checks.json`. The rows are:
- the security suite at base and candidate, with equal failure sets. The margin test over the composed record classifies all ten rows as measured and passing, binds them to the manifest identities, and checks that the state equals the one derived from the rows;
- the census `--check` (the ordinary mode, receipt current);
- the census-tool controls, old and blind;
- the vector checks, the walker storage check, the configuration tables, the operability census and verify_design.

**Receipt controls.** Each must make the ordinary `--check` fail:
- one margin tampered (with `passes2x` still consistent): the record differs;
- the tool drifted by one comment byte: the receipt is stale and the record differs;
- the receipt removed: the rows read outstanding and the record differs.

No Rust source changes, so rustfmt and Clippy are not rerun.

## Inventory

The receipt is a new path. Inventory v200 follows the code commit and adds it as a generated fixture.

## Not claimed

- No workspace full-ledger margin.
- No production caller and no qualification.
- No law change.

B2-b is not complete.
