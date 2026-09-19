# Implementation status — September 19, 2026

OpenSIP is not fully implemented. M1 development groundwork is accepted; M2 core, security and storage integration remains in progress. M3 providers, M4 reporting, M5 workflows and M6 qualification remain open.

## Repositories and authority

- Product: `/Users/sb/code/opensip-ai/opensip`, installed commit `fa72e50`, runtime selection 24 and design selection 30/44. The product working tree is unchanged.
- Architecture, candidate source archives and review evidence: this repository. Latest checkpoint at this update: `037e3aa92`.
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

| [150 conditional anchor assessment](trials/anchor-assessment-checkpoint-150/README.md) | Claude found no behavioral defect; adapter regression gaps addressed in156; host capture-error mapping remains open | At most two actual physical captures, reviewed anchor decision, owned evidence without retaining WAL readers |
| [151 population contract](trials/population-contract-reference-checkpoint-151/README.md) | Claude reviewed; wording follow-up in153 | Clarifies independent marker/terminal-cause predecessor rule; all84 Python sources unchanged; all seven reference lanes pass |

| [152 historical bodies](trials/historical-records-checkpoint-152/README.md) | Claude found no behavioral defect; regression follow-up158 frozen | All14 recordSchema1 shapes, canonical bytes, domain digest and historical platform aliases |
| [153 population wording](trials/population-wording-reference-checkpoint-153/README.md) | Claude reviewed successfully;151 W1/W2 closed | Addresses151 wording notes; names reserved lifecycle ownership |
| [154 inherited SQL reader](trials/historical-sql-checkpoint-154/README.md) | Claude found no behavioral defect; explicit mirror-policy decision and regression follow-up159/160 | One generation from a retained SQL transaction, exact stored bytes in all3 encodings, physical mirrors and historical chain diagnostics |

| [155 migrated carrier population](trials/migrated-carrier-checkpoint-155/README.md) | Claude found no behavioral defect; three regression gaps tracked | Exact legacy schemas and migration boundary, complete inherited/current population and historical SEAL incompatibility |
| [156 anchor adapter regressions](trials/anchor-adapter-regressions-checkpoint-156/README.md) | Claude confirms150F1 closed; exact-judgment and other-generation-marker follow-up163 frozen | Five actual-I/O tests address150 F1; explicit capture failure semantics document150 F2 |

Actual Claude reports through184 and the173/181 proposal assistance have been read and archived. Candidate150 closes two regression gaps and the completed-assessment WAL lifetime obligation. Full location/ancestor custody, exclusion and ledger composition remain required. No candidate here is installed product code.

| [157 owned ledger evidence](trials/ledger-evidence-checkpoint-157/README.md) | Claude found no defect; foreign-row regression and private-view follow-up163 frozen | One snapshot owns joined receipt/association/attempt evidence and a gated borrowed anchor view |
| [158 historical regressions](trials/history-regressions-checkpoint-158/README.md) | Claude reviewed successfully;152T1/N2/N5 closed | Three152 T1 negatives, structural vocabulary equality and cumulative fixture provenance; production unchanged |

| [159 historical SQL follow-up](trials/history-sql-regressions-checkpoint-159/README.md) | Claude reviewed successfully;154T1 closed | Explicit legacy mirror compatibility choice and four actual-SQL regression tests; production unchanged |
| [160 historical mirror policy](trials/historical-mirrors-reference-checkpoint-160/README.md) | Claude agrees with policy; error-routing precision and writer disposition need reference165 follow-up | Design explicitly names strict mirror admission and its compatibility cost;84 Python files unchanged |
| [161 retained directory names](trials/directory-binding-checkpoint-161/README.md) | Claude reviewed; file/symlink classification corrected in164 | Retains and checks every root-to-leaf directory name; sampled binding, not exclusion or authority |

| [162 migrated regressions](trials/migrated-regressions-checkpoint-162/README.md) | Claude confirms155T1 closed; sibling propagation tests included in166 | Empty inherited population and aggregate stored/logical byte limits; production unchanged |
| [163 recovery follow-ups](trials/recovery-evidence-followups-checkpoint-163/README.md) | Claude reviewed successfully;156/157 follow-ups closed | Exact capture judgments, foreign association rows and borrowed anchor invariant |

| [164 bound operational capture](trials/bound-operational-capture-checkpoint-164/README.md) | Claude reviewed successfully;161F1 closed on macOS | Full retained name-chain checks around every actual witness/floor read;161F1 corrected |
| [165 reader failure routes](trials/reader-routes-reference-checkpoint-165/README.md) | Claude closed160 findings; contract conflict corrected167 | Exact unknown-custody route and explicit writer prerequisite |
| [167 marker admission routes](trials/marker-routes-reference-checkpoint-167/README.md) | Claude reviewed successfully;165F1/W1 closed | Malformed marker prevents the whole capture in any retained generation; kernel receives admitted flags only |
| [166 physical carrier dispatch](trials/carrier-dispatch-checkpoint-166/README.md) | Claude reviewed; refusal/constructor/regression follow-ups included in168 | One read-only snapshot distinguishes legacy, missing, incomplete and published carrier states |

| [168 dispatch capture composition](trials/dispatch-capture-checkpoint-168/README.md) | Claude reviewed successfully;166F1/T1/N1 closed;166N2 closed for the bracket | Actual dispatch in recovery capture, owned non-current evidence with SQL released,166 refusal/constructor corrections |

| [169 admission boundary proposal](trials/recovery-admission-proposal-169/PROPOSAL.md) | Claude confirmed the conflict; correction frozen in reference169 | Reconcile normal S7 fence-to-lease admission with the recovery algorithm’s prohibition on taking the fence |

| [169 admission correction](trials/recovery-admission-reference-checkpoint-169/README.md) | Claude found admission write-scope gap; correction frozen171 | Ordinary S7 admission first, sealed held context for bounded read-only recovery; explicit wait scope, lifetime and nested handoff |
| [170 recovery availability](trials/recovery-availability-checkpoint-170/README.md) | Claude reviewed successfully; latest availability and same-snapshot boundary confirmed | Own actual availability generation and ledger join from one SQL snapshot; manifests, references and pins still owed |

| [171 read-only admission](trials/readonly-admission-reference-checkpoint-171/README.md) | Claude closed169 findings; terminal-definition gap addressed173 | Explicit no-write admission and pending installation-transition refusal;169F1/W1/W2 corrections |

| [172 Run recovery material](trials/recovery-material-checkpoint-172/README.md) | Claude reviewed successfully;375 workspace+2 doctests pass | Same-snapshot canonical Run manifest and receipt-bound per-execution inventory; closure/pins still owed |
| [173 active transition admission](trials/terminal-admission-reference-checkpoint-173/README.md) | Claude reviewed; command-scope corrections frozen175 | Active-slot retirement law and explicit read-only terminal checks;171F1/W1 corrections |

| [174 pin budget](trials/pin-budget-checkpoint-174/README.md) | Claude found no defect; three regression cases added176 | Exact supplied-inventory budget law and legacy mutation limits; SQL pin observation/transactions still owed |
| [175 transition commands](trials/transition-executor-reference-checkpoint-175/README.md) | Claude reviewed; remaining owner/trust policy corrections in178 | Explicit executor set, reader/nonexecutor barriers,173F1/F2/T1/N1 corrections |

[176 aggregate retained-body budget](trials/recovery-read-budget-checkpoint-176/README.md) was reviewed by Claude with no behavioral defect; two regression gaps are addressed in179. Validation:50 storage tests, Clippy and380 workspace+2 doctests pass. It is a supplied byte limit for retained raw records, not a total memory cap.

[177 stored-pin snapshot](trials/stored-pins-checkpoint-177/README.md) and179–184 have actual Claude reviews. Encoding and nonblocking causal-error corrections are in184; no production defect was found there, but a busy-only fault-injection gap and preexisting sidecar/write-custody obligations remain. All candidates remain unselected.

[181 phased recovery](trials/recovery-phases-reference-checkpoint-181/README.md) passed its reference tests, but Claude found real contradictions in the unchanged recovery model and missing floor-freshness rules. Correction186 was reviewed;188 addresses its remaining findings, including schema-changing core transitions and a distinct ancestor-rollback protocol. The latest proposal assistance is not acceptance.

[185 pin transactions](trials/pin-transactions-checkpoint-185/README.md) was reviewed by Claude: the 400-step sequence probe confirmed atomicity/scope, but REPLACE could bypass schema immutability.187 adds guards for all six protected storage tables and the identified regression gaps. Security carrier-format and historical-schema limits require separate reference treatment; the mutable current pin projection is intentionally unaffected.

[186 store recovery protocol](trials/store-recovery-protocol-checkpoint-186/README.md) has an actual Claude review. Its original wrong-ID fail-closed claim was corrected in a separately preserved note;188 adds the binding prerequisite. All seven suites pass, including1490 integration checks;12 behavioral mutants are caught. It corrects selection-case dispatch, rollback carrier ownership, execution attribution, floor freshness and durable ordering. Actual filesystem/store/selection effects remain unimplemented obligations.

## Next work and remaining boundaries

1. Finish188 reference corrections and obtain fresh actual Claude review, then adopt the carrier guard in189. Actual187 review found no defect in the six storage guards;186 wrong-ID limitation now has a separate corrected review note. Actual150F2 public host mapper, physical custody/exclusion and full writer integration remain required.
2. Compose the actual dispatch and bound operational captures with owned ledger evidence and retained custody/exclusion.164 now requires full directory chains for witness/floor reads, but SQLite path/sidecar custody is still separate.
3. Finish inherited-history admission, retained ancestor custody and exclusion, live lease/fence/writer composition, production clock input and current-revocation binding.
4. Finish actual pin transactions, recovery/cleanup ordering, output spooling and rendering, generated-consumer checks, and formal selection before installing the accumulated implementation candidates.
5. Complete the remaining M2 work and M3–M6.

Candidate155 now admits fully published migrated carriers; unmigrated carriers and partially published migration prefixes remain outside its open path. Owned records and passing local tests do not establish retained filesystem custody or permission to modify data. The full 118 I-2 integration issue and 124 F-1 ancestor-custody issue remain open.

## Resume evidence

The newest appended entries in [ACTIVE-WORK](../ACTIVE-WORK.md), [REVIEW-RESUME](REVIEW-RESUME.md) and [PENDING-REVIEW](PENDING-REVIEW.md) contain exact manifests, hashes, active processes and reviewer requests. Earlier entries are historical and may describe superseded authority, selections or reviewer availability. Read this summary and the latest entries before acting.

Herdr: actual Claude `wF:p1`, native session `de59b975-4f82-4aff-9252-ad6d68d6fb79`; Grok fallback `wN:p1`. Verify current pane status rather than assuming either remains available. No Claude quota error has been observed at this update.


Current successor188 is not frozen: six reference lanes pass, integration and behavioral mutation checks are running. Actual187 closes185F1 for six storage tables only. No cumulative readiness or product installation is claimed.
