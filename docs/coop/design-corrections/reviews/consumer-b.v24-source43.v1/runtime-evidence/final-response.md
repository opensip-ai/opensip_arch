**Verdict: ACCEPT-RECONSTRUCTABLE.** All 123 requirements and 8 standing rules are executed, with nothing failed or unexecuted. All background processes have finished, and kit custody passed again just before phase 11. The review is in `output/blind-review.md` and `output/blind-review.json`.

## What changed in source43
The kit checks out (104 members, manifest `6d8912f4…`, parent `db43ee76…`). Compared with my own source42 records, exactly one document changed: `workflows/query-projection-contract.v3.md`, which grew from 29699 to 30278 bytes. I only have the hash of the old version, not its text, so I couldn't diff it. Instead I checked every rule in the current text against my graph-query tool.

That tool is the only code that reads the changed document. Everything else loads the kit's JSON only. The exported stores are byte-identical to source42.v3 (104/104), and apart from the files I edited here, the only change to my code is the rebind to the new path.

## Graph query (HC-54)
Before any change, my old tool still passed its own 53 checks on source43. Those checks just never tested the rules it had skipped:
- **Path edges:** it reported each edge in its stored direction, not the direction actually walked, for `incoming` and `both` queries.
- **Availability input:** it treated `missing` and unrecognised values as permission to answer. It also lacked the host-adapter error route and the check on a retained availability record.
- **Closure outcomes:** it chose error routes by matching message text. It reported a replay mismatch as `evidence.corrupt` instead of `evidence.regeneration-mismatch`, and let unexpected exceptions escape. It also used its own remedy text instead of the kit's.
- **Ambiguous endpoints:** the kit's refusal for an endpoint matching two vertices was only implicit.

The corrected tool passes 66 checks with 0 failures (`logs/s43-hc54c.0`). I ran the old and new tools on identical inputs. Every new check separates them except two controls where both should agree, and do.

One check builds a tampered store: the proof's verdict flipped, with all enclosing IDs recomputed. It passes both admission stages, fails replay, and now routes to `evidence.regeneration-mismatch`; the old tool said `evidence.corrupt`.

The old document grew by only 579 bytes, while the rules I corrected run to thousands. So most of them were already in source42, which means my source42.v3 graph-query result rested on those omissions. That result is superseded.

Three errors in my own new tooling are preserved in their logs:
- `logs/s43-hc54.0` wrongly expected every check to differ;
- `logs/s43-hc54b.0` compared old and new outputs in different shapes;
- `logs/s43-prov.0` counted mere mentions of the document as reads.

## Executed fresh versus reused
- **Fresh in this runtime:**
  - From-scratch closure and full proof replay of all 27 claimed positives passed. The designed negative is still refused.
  - Export replay of all 27 is byte-equal.
  - The per-record admission log has 0 failures.
  - Also fresh: the graph query, phase-0 custody, all checkpoints, provenance, and final custody.
- **Reused from source42 as-is:** everything else, recorded in `selfcheck/s43-provenance.json`. This includes the source42.v3 provider-trace payload work (71 payload checks, 25 traces), which I kept because every document it depends on is byte-identical in source43.

## Issues
There are no new MUST or SHOULD issues. One new advisory, A-s43-1: a successful query with no availability input must still report `availability`, but the contract doesn't say what value. This only arises in the reference harness, because a real host always has an availability record. I report `retained`.

**From-scratch command:**
`cd /private/tmp/opensip-design-corrections/consumer-b.v24-source43.v1/output && /tmp/opensip-architecture-review-env/bin/python -I -B tools/from_scratch.py && /tmp/opensip-architecture-review-env/bin/python -I -B tools/replay_export.py`

This makes no product qualification or implementation claim, and root admission of the exports has not been observed.
