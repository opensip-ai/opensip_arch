**Verdict: accept-conditional, not a promotion.** The one change to envelope6 (at `/allOf/19/then`) correctly adds a D9 `interrupted`/130 output for an invocation interrupted before any Run was committed. It only adds; nothing previously accepted is removed. The review is in `review.json` and `review.md` in the review directory.

**Pins:** The manifest SHA matches. The 40 files match exactly on the original and on my copy, before and after running. All 34 input pins match their source files. I ran everything in the reference environment (`python -I -B`, jsonschema 4.25.1) with my own TMPDIR, and no bytecode was written. Root `check.py` exits 0 and its output equals `root-result.json`.

**The gap is real, and I checked it rather than assuming it.** In envelope5:
- A failure must carry `errors`.
- Empty `errors` is only allowed for `UNKNOWN_OPTION` with exit 2 and diagnostics.
- None of the 315 detail codes names an interruption, yet 314 of them are accepted next to an interrupted termination. So the only way to express this in v5 is an unrelated detail, which the owner text forbids (workflows-and-surfaces.md:1367).
- No other kind works either: `run` and `doctor` need their payloads, `query` and `mutation` need records, and `meta` forces success. I ruled out `invocation` by reading the owner text, not with a schema test.

**Owner rules:** The new form matches the D9 exit table, the before/after-settle cancellation rule, and report04's aggregate `{interrupted, signal, runId?}`. It adds no new vocabulary and leaves the step ledger alone.

**My own tests (`work/probes.py`, 80 cases, all pass):**
- **Accepted:** all three signals, plus the optional correlation fields.
- **Refused in both versions:** null values and unknown keys.
- **Refused only because of the new form:** extra termination fields, wrong exits and classes, empty errors under other kinds, and mixes of UNKNOWN_OPTION with interruption.
- **Raw bytes:** a duplicate key or `130.0` is refused.
- **Old branch:** the `UNKNOWN_OPTION` form is unchanged.
- **Committed Run:** the report04 interrupted `kind=run` example is still accepted. Keeping `runId` on the new form is refused.
- **Superset:** across 46 values, nothing accepted by v5 is refused by v6.
- **Mutations:** removing the `not` clause, the closed termination object or exit 130 each gets caught. The mutations that survive are backed up by other existing rules.

**Findings:**
- **F1 (medium, blocks selection):** workflows-and-surfaces.md:1340–1341 still says a failure requires *nonempty* `errors`, and no integration duty covers changing that text.
- **F2 (medium):** The schema can't tell when a committed Run has been dropped. The interrupted Run example, rewritten into the new form without `run`/`runId`, is accepted by v6. The host needs a named check, with refusal examples, that compares the envelope against the ledger (committed Run, cancellation phase).
- **F3 (low-medium):** The contract says an existing Run-bearing interruption output covers interruptions after a Run is committed, but that's only shown for `kind=run`. Query commands that commit a Run and then run a query step (candidates, inspect, review-brief) have no demonstrated output for it.
- **F4 (low):** The root's `new-form-no-{run,meta,query,availability}` probes use `{}` payloads that fail their own schemas, so they don't prove the `not` clause matters. I repeated them with valid payloads: availability, findings, query and diagnostics depend on the clause; the others are also blocked by existing rules. retentionDisclosure and agentHints are still untested with valid payloads.
- **F5 (low):** The parent envelope5 is still an unaccepted report04 candidate and must stay marked that way. If report04 changes it, this review has to be redone against the new bytes.

I did not check signal handling, host delivery, runtime, CLI, or integration, and I'm not claiming anything about them.
