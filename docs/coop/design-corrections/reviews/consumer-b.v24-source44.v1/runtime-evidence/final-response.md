## Verdict: CHANGES_REQUIRED

The source44 kit has one gap that blocks acceptance. When a provider stops before analysis because its native context doesn't match, the host must write one coverage record per requested key. The kit fixes every field of that record except `closedWorld`. It names that value only as `closed_world_v2(no manifest, entry points none, no edges, externalConsumers unknown)`, and no kit document defines that function. This is MUST **M-s44-1**.

- **What the text does settle:** `entryPointsRecognized none`, `nonliteralLoading none`, `externalConsumers unknown`, `deadCodeRepairEligible false`. FR-3 (line 2771) supports `exportsClosed unknown`.
- **What nothing publishes:** `dynamicDispatch` (resolved or not-applicable) and the `reasons` array.
- **Measured:** four candidate values each pass every published check in both languages, and each gives the same requested key a different `coverage2` identity. Two conforming hosts can therefore commit different evidence for the same outcome. My traces use one reading and label it.
- **Fix needed:** publish that record's `closedWorld` value, or what `closed_world_v2` returns for this input.

Everything else held. All 123 requirements and 8 standing rules are executed, with none failed. The 3 future-qualification items are recorded as not performed. No SHOULD issues.

## What changed and what I did
Against my own source43 rows, six kit members changed and three were added. All are provider handshake, startup or payload owners. A read-census shows only my provider-trace code reads them.

1. **Unchanged source43 helpers first** (outputs in `preserved/s44-original/`). The trace script exited 0 and missed every new rule. The payload vectors still admitted a TypeScript FactBatchV2; that run failed only on a stale token-count assertion.
2. **Corrected from the kit:**
   - **HC-57:** without the negotiated token, TypeScript now sends FactBatchV1 with a recomputed `batchCommitment`, and Rust sends FactBatchV2. My earlier advisory A-s42v3-1 is withdrawn.
   - **HC-58:** TypeScript runs on the TypeScript protocol-2 table and Rust on protocol3, with the dependency/prepared modes derived from the OpenUniverse payload. Every handshake, startup, coverage, terminal and cancellation payload is checked before the table.
3. **Results:**
   - 78 payload vectors, 116 startup vectors, 43 traces plus 5 table-only tests, all passing.
   - Every row of both tables is exercised. Only P3-09 and P3-10 are table-only, because no valid OpenUniverse can reach them.
   - Three conclusions changed from source43: a TypeScript Unavailable after output and a TypeScript ProviderFault now fault, and skipping Rust dependency custody faults.
4. **Re-run fresh:**
   - All 27 claimed complete positives still admit, replay from scratch and export equal, and the designed negative still refuses.
   - The graph query (66 vectors), reference census and 32 retention negatives pass.
   - All 27 run ids equal source43, and 251 of 473 result files are byte-identical. Of the rest, 89 differ only by an embedded process id (they also change between two source44 runs), and 14 are the expected phase-3, census, custody and edited-script changes.
5. **Reused with custody** (`selfcheck/s44-provenance.json`): phases 1–2 and 4–8 vectors, stores, mutation replay and tamper, labelled as reused rather than re-executed.

## Advisories
- **A-s44-1:** three summary sentences in the return schema still say "FactBatchV2" for any worker without the token, while every payload-selection owner is per-language. Advisory, because what the return law captures is the same for both languages.
- **A-s44-2:** `native/source-pins.v2.json` is cited but isn't in the subject. The Hello contract digest is still fixed by the wire law.
- The other earlier advisories carry over; their native-evidence line numbers were re-checked against the new bytes.

## Own errors, preserved
My own tool errors are kept in `logs/s44-smoke.0`, `s44-p3.1`, `s44-cp.7` and `s44-diff.0`.

## Limits
- The provider law runs on constructed payloads, not on built Runs or a real worker process.
- Snapshot, dependency and prepared payloads stay abstract events.
- Commitments are not recomputed.
- Descriptors are synthetic.
- Rust `CancelledV2.observedPhase` is not checked.

This makes no product qualification claim, and root admission of the exports has not been observed.

## From-scratch replay
```
cd /private/tmp/opensip-design-corrections/consumer-b.v24-source44.v1/output
for s in tools/from_scratch.py tools/replay_export.py tools/phase9_admission_log.py vectors/phase3_payload_vectors.py vectors/phase3_startup_vectors.py vectors/phase3_traces.py; do /tmp/opensip-architecture-review-env/bin/python -I -B $s || exit 1; done
```

## Files
All in `output/`:
- `blind-review.md`
- `blind-review.json`
- `requirement-status.json`
- `checkpoints/phase-0..11.json`
- `notes/13-source44-provider-wire.md`
- `notes/10-gaps.md`
- `tools/hc_source44.py`
