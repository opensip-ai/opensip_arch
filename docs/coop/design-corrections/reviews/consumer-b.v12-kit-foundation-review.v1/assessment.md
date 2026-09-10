I’ll continue this same kit-only origin and review only phases 0–4 plus `R-IMPORTED-OBSERVATION-BOUNDARY` against the new foundation snapshot, without carrying four-Run admission into that scope.Custody next: I’ll hash the foundation snapshot, then map phases 0–4 plus the import-advisory requirement onto exact retained vectors.Custody matches. Next I’ll read the kit laws for the named gates, traces, and import boundary, then re-run the retained foundation vectors independently.**Verdict: `FOUNDATION_SCOPE_ADMITS`**

This is the same kit-only origin as the four-Run review, scoped only to original phases 0–4 plus `R-IMPORTED-OBSERVATION-BOUNDARY`. It is not whole-consumer ACCEPT and does not treat frozen Run stores as admitted. The four-Run result remains `OTHER_RUNS_REFUSED` and was not imported as a pass.

Custody: origin kit `ea2fa750…e6bf8` (80/80), requirements `855a1464…f495`, foundation snapshot-manifest `95144541…4b94` (319/319). Shared historical `vectors/` bytes match `preserved-failures/foundation-shared-path-original/`. New exhibits are under `foundation/`.

Reproduce:

```bash
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-kit-foundation-review.v1/output/independent/foundation_review.py
```

Checker paths were redirected into this output directory; the kit used is this origin’s 80-file subject, not the consumer helper’s hardcoded other-origin path.

## What was independently re-derived

| ID | Result | Notes |
|---|---|---|
| C/H (`R-H-HELPER`) | PASS | Standalone snap-A identity `snapshot2:3324a39a…`; pairwise vcsDigest move to `snapshot2:496d2081…` |
| Semantic vs operational | PASS | Operational `requestId` on `#/$defs/run` is additionalProperties refuse |
| CVE1 eight types | PASS | Round-trip + map key-order + float/non-NFC refuse |
| Lexical / raw vs parsed | PASS | Duplicate/float/exponent/`-0`/leading-zero/range/surrogate/BOM/control on **raw** bytes; `C(true)≠C(1)` |
| Acyclic joins | PASS | Independently constructed schema-valid snapshot→plan→view→proof→evidence→seal→run; cycle `proof.evidenceId` refuses. Consumer claimed plan/view/proof/… IDs have **no retained preimages** and were not used as an identity oracle |
| Cap admission | PASS | CAP-MANIFEST-ID-V1 `6e6f63c7…652b` before encoding |
| Named first gate | PASS | Order ADM-TYPE → CLOSED → DOMAIN → ORDER. Combined boolean `schemaVersion` + extra key first-refuses **ADM-TYPE** and masks CLOSED/DOMAIN/ORDER |
| Protocol traces | PASS | Complete/unavailable/cancel/fault/post-terminal/`P3-34` unmatched OpenUniverse with `sourceBytesSent=false`. Transitions executed; process/payload codec labeled future-host |
| Relation/rung, RC-1/RC-2, code vs data, six modes | PASS | 13 relations from the registry; `file@enumerated` is `not-applicable`; json has no clones capability |
| File rung on frozen stores | PASS as **unverified-frozen** | Five file facts, all `enumerated`; not Run admission |
| Import-advisory boundary | PASS | Retained `import2:e52a8464…4af8` inhabits `#/$defs/import` + `RuntimePayloadV1` (`istanbul-json`); H and payload digest recomputed; not `fact2` / not native Coverage |

Deliverables: `foundation-review.md` and `foundation-review.json` under `/tmp/opensip-design-corrections/consumer-b.v12-kit-foundation-review.v1/output`. Snapshot bytes were not rewritten.
