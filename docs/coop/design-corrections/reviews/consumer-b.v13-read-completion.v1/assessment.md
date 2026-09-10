This is the same-origin read-completion subturn. I’ll verify the six kit hashes, then read each contract end-to-end in contiguous chunks before any reassessment.Hashes match. I’ll read the six contracts in contiguous 180-line chunks, starting with identity-and-evidence and the two shorter documents.All six contracts are read. I’ll sample my helpers and `requirements.json` so the reassessment cites exact kit selectors against actual artifacts.I'll finish the six full-contract reads, then reassess our own helpers and artifacts against that law and write the four read-completion deliverables. Starting by verifying the kit files, output directory, and current reconstruction state.Hashes match. Reading all six contracts in contiguous chunks so every line is actually delivered in this window.Continuing contiguous reads of the remaining contract chunks.Continuing the remaining identity, security, workflows, and native chunks.Identity is complete. Continuing security, workflows, and native remaining ranges.Security and workflows are complete. Continuing native-evidence from line 1261.All six contracts are fully delivered. Next I’ll reassess our own helpers and artifacts against that law and write the four deliverables.I have the six complete reads and the helper/artifact contradictions. Writing the four read-completion deliverables now.**Verdict: `READING-COMPLETED`.** `readingCompleted: true`. `reconstructionAccepted: false`. This subturn does not grant `ACCEPT-RECONSTRUCTABLE` and does not claim the original reconstruction is done.

All six originally required documents were read first line through last line via contiguous `read_file` chunks. Hashes match. Remaining omissions: none.

| Document | Lines | SHA-256 |
|---|---|---|
| `identity-and-evidence.md` | 1–1660 | `afded6d3…9a1a` |
| `security-and-lifecycle.md` | 1–1256 | `12dcebea…496b` |
| `native-evidence.md` | 1–3645 | `06f61474…69db` |
| `workflows-and-surfaces.md` | 1–1287 | `3d89b511…98cf` |
| `admission-and-qualification.md` | 1–349 | `69cd6ba3…e6b3` |
| `query-projection-contract.v3.md` | 1–189 | `aa378ca4…e738` |

Against that law, continuation helper passes and `executed: 131` are not admission. Independently identified contradictions include:

- Graph query over `imports@syntactic-specifier` is a refused request (`QUERY.RELATION_UNSUPPORTED`); neighbor order is not the published utf-8 tuple; `projectId` and `GraphEvidenceDisclosure` are missing. `R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR` is accept-blocking and incorrectly executed.
- H-identity retention stores `C(X)` rather than the framed H preimage.
- Public `close_run` is owner-closure joins, not complete evaluator3 replay, and does not re-run `admit_native_context` / `bind_*_universe`.
- Default analysis-spec requests four capabilities instead of every non-`NOT-SELECTED` cell; `EnumerationPlanV1` and `EvaluatorEmissionPlanV1` are not `analysis-spec.parameters`.
- `FileMembershipRowV1.rows` is empty; complete `file@enumerated` Coverage does not cover every inventoried path.
- Invocation `CapabilityAvailabilityV1` is unexecuted.

Classified separately: D9 `faultCause=host-invariant` is a genuine owed successor artifact, not a helper bug. Real OS/compiler/crypto/SQLite remains future qualification. Original 123 / 8 / 3 IDs are unreduced.

Delivered only under `/tmp/opensip-design-corrections/consumer-b.v13-read-completion.v1/output`: `read-completion.json`, `reassessment.md`, `reassessment.json`, `next-work.md`. Kit and both earlier outputs were not modified. Reconstruction was not regenerated. The next same-origin turn should follow `next-work.md`.
