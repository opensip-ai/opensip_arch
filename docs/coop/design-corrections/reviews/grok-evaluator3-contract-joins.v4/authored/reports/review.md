# Evaluator3 analysis-SEAL authority split — v4

**Standing.** Actual Grok architecture/reference. Isolated `evaluator-successor.v1`. Same native/security/three-chapter ownership. v3 handoff retained. Not independent acceptance. Not a product host. Not official pin qualification.

**Verdict.** `PREFIX_AND_CLOSE_RUN_SEAL_BOUNDARIES_SPLIT`. Official security/native suites were not run (pins unsealed; prior cancellation respected). New independent adapter check `check-analysis-seal-adapter.v1.py`: 8/8 PASS. That is not the official suite.

## What changed

`admit_host_seal_run_id` advertised `identity-model.v3.close_run` while only checking a `run3:` pattern. That is no longer the public analysis-SEAL boundary.

| Helper | What it is | What it is not |
|---|---|---|
| `linearize` | Abstract brokered-effect schedule. SEAL id is `FIXTURE_SEAL_RUN_ID` (`run3:` + 64 zeros). | Product host, native fact, close_run |
| `admit_seal_run_id_prefix` | Narrow `run3` pattern. Refuses `run2` and the fixture id. Alias: `admit_host_seal_run_id`. Output authority `run3-pattern`, standing `prefix-dispatch`. | close_run, retained-graph admission |
| `admit_journal_record` | Schema 3 → exact current `JournalRecord` fields via ExactValidator. Schema 2 + run2 → `JOURNAL_RECORD_SCHEMA_HISTORICAL`. Mixed prefixes → `JOURNAL_RECORD_MIXED_PREFIX`. Missing required field → `JOURNAL_RECORD_SCHEMA_INVALID`. | Reading schema-2 as 3 |
| `admit_analysis_seal` | Full current JournalRecord + `identity-model.v3.close_run(run,objects,blobs)` + byte-equal RunId. Fixture id refused before close_run. | Prefix-only; owner-only `open_run_closure` |

Core identity/execution-input files were **not** edited. Root has already required `proof-bundle.executionInputsDigest` (`identity-schemas.v3.json` now `c9351e9c…` / 184054; v3 handoff still cited `4ed626ec…` / 183663). Reconstruct requires exactly one `evaluationInputRefs` member `domain=execution-inputs`. The adapter check calls public `execution_inputs_fixture.v3.attach_host_capture` **before** seed seal, then derive, then close_run.

## Adapter check (new source, not cancelled command)

`/tmp/opensip-architecture-review-env/bin/python -I -B security/check-analysis-seal-adapter.v1.py`

| case | result |
|---|---|
| prefix-nonfixture-admits-without-close-run | PASS (`run3-pattern`) |
| prefix-fixture-refused | `SEAL_RUN_ID_FIXTURE_NOT_AUTHORITY` |
| journal-missing-recordType-invalid | `JOURNAL_RECORD_SCHEMA_INVALID` |
| journal-historical-2-unchanged | `JOURNAL_RECORD_SCHEMA_HISTORICAL` |
| analysis-seal-full-admitted | PASS (`close_run`, live run3) |
| analysis-seal-wrong-id | `SEAL_RUN_ID_MISMATCH` (close_run still ran) |
| analysis-seal-fixture-id-not-authority | fixture refused |
| analysis-seal-owner-only-semantically-false | reminted finding: `open_run_closure` admits; `admit_analysis_seal` → `SEAL_CLOSE_RUN_REFUSED:` |

Official `check-security-lifecycle.v1.py` and `check_native_evidence.v2.py` were **not** invoked. Historical pins were not edited.

## Official JSON cases (unrun until pin seal)

- `host-seal-prefix-admits-nonfixture-run3` now expects `prefix-dispatch` / `run3-pattern` (the old “fully replayed” expect was the misleading claim).
- `journal-record-schema-3-missing-recordType-refused` → `JOURNAL_RECORD_SCHEMA_INVALID`.
- Historical 2 / mixed prefix / revocation-blocks-SEAL unchanged in law.
- Sweep `sweep_journal_record_dispatch` no longer asserts close_run on the prefix helper.

## Limitations

1. Prefix helper still admits any well-formed non-fixture `run3:` with no graph. That is now an explicit lesser boundary.
2. `admit_analysis_seal` lazy-loads M3. Linearize does not. This is a reference join, not a shipping host.
3. Full-admitted graphs use the synthetic file fixture plus `attach_host_capture`. They do not qualify a compiler or a real store.
4. Owner-only case remints severity; it is one semantic falsehood, not every replay refusal class.
5. `check-identity.py` old flag name remains root.
6. R1 requiredForEvaluatorMajors and R5 workflow leftovers remain root.

## Hashes (sha256)

| file | bytes | sha256 |
|---|---|---|
| `security_lifecycle_model_v1.py` | 203267 | `340ac50a8051a5a833177050a0e58807942822a275cc040f4e8ce9e647be33dd` |
| `security-lifecycle.schemas.v1.json` | 121701 | `d5d030570a620c57cbbedcbc9303f35aaa24029daf5907e8ef7c6c59f9dcea72` |
| `revocation-live-cases.v1.json` | 22780 | `50097088dd0b3e3f71c70e1e5a1a178ffa696e8ea126337b98940e9bb7cfdbe5` |
| `check-security-lifecycle.v1.py` | 44585 | `11b700132a9e688034307a56b3843972907499d27446d5c5baa2fc62bab99d65` |
| `check-analysis-seal-adapter.v1.py` | 9484 | `7272696a22382960b03c58133484950bdc8fa1a4b7860cde392bcdd9b452df59` |
| `native-evidence.md` | 262904 | `bc88c7fcc77423b7a66a56bdfa24d0480c86046eed83f325118207376bc61466` |
| `security-and-lifecycle.md` | 90737 | `0162d6108686a728cf5b71c2d27f4de50ef074a25d32b66f2904a68d6eaacd8c` |
| `admission-and-qualification.md` | 27044 | `5cd608344014bab14593fa3ca696f10245d42c846458af49af8462db1f92b30e` |

Unedited core (read for join): `identity-model.v3.py` `e3fe8e5a…` / 137882; `identity-schemas.v3.json` `c9351e9c18544e606765e2206d7112a3785837b6ae76f357927cc5eb36a86958` / 184054 (executionInputsDigest required); `execution_inputs_fixture.v3.py` `a6ec0dcb…` / 22433.
