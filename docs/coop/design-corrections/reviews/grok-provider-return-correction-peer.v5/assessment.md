I'll verify the v5 manifest and the 27-file root delta, then independently probe the contiguous candidate-stream fix without rerunning the sealed global launcher.Hashes match. I’ll verify the 27 delta files and read the candidate-stream, producerSupply, and array-order changes.**Verdict: `ACCEPT_SCOPED`.** The root integration delta does not add a required occupancy correction. This is not a new blind or final whole-design acceptance.

Manifest SHA256 `7aed37276b8ff95c8b33e36e17751cc192a10d96ec101850a8fd46d60eeebd69` matches; **1323/1323** files and **27/27** delta hashes match. Output is only under `grok-provider-return-correction-peer.v5/output`. The sealed 6-suite launcher was **not** re-run.

### Candidate stream
Root’s measurement (buffer accepting candidates `[0,2]`) is closed. `_candidate_stream` now requires `list(range(expectedFirstCandidateOrdinal, …))`.

Independent **helper** probes (TCB-assumed dispatch/tokens):
- CANDIDATES `[0,1,2]` + COMPANIONS `[0,2]` → buffered
- CANDIDATES `[0,2]` → `PROVIDER_RETURN_CANDIDATE_STREAM`
- Later `[3,4]` with `expectedFirst=3` → buffered
- `[3,4]` with `expectedFirst=0` → `PROVIDER_RETURN_CANDIDATE_STREAM`

The `candidateOrdinal` array token still allows companion gaps; contiguous stream is a separate host join.

### Other delta
Stale “After fact2 mint” producerSupply is gone; current text is in-worker companion then post-mint projection. Array-order no longer silently skips a missing explicit schema path. Query contract uses captured V2 projections of OccupancyCompanionV1 and does not parse payload spelling — occupancy law is not contradicted; query/proof/closure were **not** re-audited. No new StageReceipt `outputDomains`/`state` double-validation.

### Counts (helper scope)
Focused occupancy checker independently re-run: **43/43**, `fullRun: false`, first failure none. Array-order delta control: **121/121**. All five independent probes are **`helper_only: true`** (TCB assumptions). Prior v4 `helper_only: false` on bind probes was too broad. 43 rows are not compiler/OS/D9 discharge. Full final/fresh-blind after integrated globals remain required.
