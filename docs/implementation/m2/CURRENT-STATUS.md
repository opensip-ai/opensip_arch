# Implementation status — September 19, 2026

OpenSIP is not fully implemented. M1 development groundwork is accepted; M2 core, security and storage integration remains in progress. M3 providers, M4 reporting, M5 workflows and M6 qualification remain open.

## Repositories and authority

- Product: `/Users/sb/code/opensip-ai/opensip`, installed commit `fa72e50`, runtime selection 24 and design selection 30/44. The product working tree is unchanged.
- Architecture, candidate source archives and review evidence: this repository. Latest checkpoint at this update: `b8175d032`.
- The user authorizes continued implementation and commits in both repositories when they change. The user will push; do not push.
- Use actual Claude as primary reviewer, then actual Grok if Claude becomes unavailable. A scoped review is not cumulative implementation approval. Candidate archives below are not installed source selections.

## Current work

| Candidate | Status | Scope |
| --- | --- | --- |
| [144 marker reader](trials/marker-snapshot-checkpoint-144/README.md) | Claude found no behavioral defect; regression gaps addressed in 147 | Exact quarantine-marker bytes, shape, physical mirrors and encoding from a retained SQLite snapshot |
| [145 purge reference](trials/purge-subclass-reference-checkpoint-145/README.md) | Claude reviewed the correction successfully | Refuses pinned-termination injection through Python dict subclasses; arbitrary non-JSON Python mappings remain outside the stated input contract |
| [146 population reader](trials/generation-population-checkpoint-146/README.md) | Claude confirmed the terminal-cause defect; otherwise the reviewed population behavior passed. Fix in 148 | Complete fresh-carrier generation population, origin, gaps, predecessors and aggregate read bounds |
| [147 marker regressions](trials/marker-regressions-checkpoint-147/README.md) | Claude reviewed successfully; all marker regression gaps closed | Two isolated negative rows and exact diagnostic assertions; production code unchanged |
| [148 terminal-cause correction](trials/generation-closure-checkpoint-148/README.md) | Claude found no behavioral defect; purge append-stop regression added in 150 | Separates a project-purge terminal from the generation-closure condition needed for a successor generation |
| [149 physical bracket capture](trials/bracket-capture-checkpoint-149/README.md) | Claude found no behavioral defect; after-read regression and WAL lifetime addressed in 150 | Reads witness/floor before and after one retained SQL population; owns exact observations, without a recovery judgment |

| [150 conditional anchor assessment](trials/anchor-assessment-checkpoint-150/README.md) | Frozen; queued for actual Claude; final isolated host checks passed | At most two actual physical captures, reviewed anchor decision, owned evidence without retaining WAL readers |
| [151 population contract](trials/population-contract-reference-checkpoint-151/README.md) | Claude reviewed; wording follow-up in153 | Clarifies independent marker/terminal-cause predecessor rule; all84 Python sources unchanged; all seven reference lanes pass |

| [152 historical bodies](trials/historical-records-checkpoint-152/README.md) | Frozen; queued for Claude | All14 recordSchema1 shapes, canonical bytes, domain digest and historical platform aliases |
| [153 population wording](trials/population-wording-reference-checkpoint-153/README.md) | Frozen; queued for Claude | Addresses151 wording notes; names reserved lifecycle ownership |
| 154 inherited SQL reader | 104 security tests pass; isolated build and mutation checks running | One generation from a retained SQL transaction, exact stored bytes in all3 encodings, physical mirrors and historical chain diagnostics |

Actual Claude148/149 reports have been read and archived. Candidate150 closes two regression gaps and the completed-assessment WAL lifetime obligation. Full location/ancestor custody, exclusion and ledger composition remain required. No candidate here is installed product code.

## Next work and remaining boundaries

1. Obtain actual Claude reviews of150/151 and address actionable findings. Reviews through149 and151 are archived. Continue154 physical history admission; whole inherited-carrier population and open dispatch remain separate.
2. Compose actual witness/floor reads with the owned SQL population and the reviewed historical-anchor decision. Keep the storage receipt/association owner; do not replace its evidence with caller assertions.
3. Finish inherited-history admission, retained ancestor custody and exclusion, live lease/fence/writer composition, production clock input and current-revocation binding.
4. Finish actual pin transactions, recovery/cleanup ordering, output spooling and rendering, generated-consumer checks, and formal selection before installing the accumulated implementation candidates.
5. Complete the remaining M2 work and M3–M6.

The fresh-carrier reader still refuses migrated/inherited carriers. Owned records and passing local tests do not establish retained filesystem custody or permission to modify data. The full 118 I-2 integration issue and 124 F-1 ancestor-custody issue remain open.

## Resume evidence

The newest appended entries in [ACTIVE-WORK](../ACTIVE-WORK.md), [REVIEW-RESUME](REVIEW-RESUME.md) and [PENDING-REVIEW](PENDING-REVIEW.md) contain exact manifests, hashes, active processes and reviewer requests. Earlier entries are historical and may describe superseded authority, selections or reviewer availability. Read this summary and the latest entries before acting.

Herdr: actual Claude `wF:p1`, native session `de59b975-4f82-4aff-9252-ad6d68d6fb79`; Grok fallback `wN:p1`. Verify current pane status rather than assuming either remains available. No Claude quota error has been observed at this update.
