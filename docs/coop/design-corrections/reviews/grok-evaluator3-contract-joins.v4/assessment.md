I’ll read the live M3 close_run and executionInputsDigest surfaces first, then split prefix-only SEAL dispatch from actual complete-replay admission without touching root-owned core.Root already requires `executionInputsDigest` on the proof bundle. I’ll split prefix dispatch from close_run SEAL admission and attach host capture before any public fixture seal.The misleading SEAL claim is split. Reports are in `/tmp/opensip-design-corrections/grok-evaluator3-contract-joins.v4/`. Official suites were not run. v3 is unchanged.

**Three boundaries**
- `linearize` — abstract grant-journal schedule; all-zero `run3:` is a fixture, not close_run.
- `admit_seal_run_id_prefix` (alias `admit_host_seal_run_id`) — `run3` pattern only. Authority is `run3-pattern`, not close_run.
- `admit_analysis_seal` — full current `JournalRecord` fields, then `identity-model.v3.close_run` on the retained graph, then RunId compare.

**JournalRecord:** schema 3 is ExactValidator on closed fields (missing `recordType` → `JOURNAL_RECORD_SCHEMA_INVALID`). Schema 2 + run2 is still `JOURNAL_RECORD_SCHEMA_HISTORICAL`. Mixed prefixes still refuse.

**executionInputsDigest:** core files were not edited. Root already requires it on proof-bundle. The adapter attaches host capture *before* seed seal via the public fixture API, then derive + close_run.

**New check** (not the cancelled pin-bypass, not the official suite): `check-analysis-seal-adapter.v1.py` **8/8** — prefix, historical 2, missing field, full admitted, wrong-id, fixture id, owner-only remint (`open_run_closure` admits, analysis SEAL refuses). Not product qualification.

**Left for root:** pin seal and official suites; `check-identity.py` flag name; R1/R5. Prefix helper still admits a well-formed `run3:` with no graph — that is now an explicit lesser boundary, not replay.
