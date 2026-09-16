# Native wire carriers — root correction07 of Grok06 finding

The current proposed pattern dialect standing now carries the root-acceptance/source-promotion condition. The wording check scans the entire published carrier, including privateRepresentation, and two new controls exercise restoration of the premature claim and removal of the condition. Prior native06 bytes are preserved; this correction is not independent acceptance. Current test evidence is separate from the historical candidate06 evidence below. No runtime framing, pattern evaluation or sender algorithm is changed.

# Native wire carriers, TS2 and Rust3: root continuation of author candidate 06

**Standing.** Root is completing the partial actual-Claude author06 work after its weekly quota interruption. Original author06 bytes and inherited candidate05 result files remain preserved. This is an unreviewed correction candidate for root and fresh independent review. It is not approval, source promotion, product integration, a production codec, admission, sender or generator. It claims no platform, M2/M3, full `admit_frame` or regex-lowering qualification.

The in-memory scoped successors are author candidates: `owner-pattern-successor.v1.json`, `public-route-successor.v1.json`, `p3-guard-successor.v1.json` and the rows of `successor.json`. Each is a proposed correction, effective as selected semantics only after root acceptance and source-bridge promotion.

It answers independent review 05 (`/tmp/opensip-implementation/m1-native-wire-owner-review-05`, verdict changes-required): required findings RF-1 and RF-2, and advisories A-1..A-4.

## Custody and provenance

- **Parent verified before work.** Frozen `m1-native-wire-owner-subject-05`, sibling manifest sha256 `7b9d94c31df9aa41d83599400e6beb9b5451bb39b9c0e174858f2fde4c686f1d`. All 102 listed files match by sha256 and size, the walk has no extra files and there is no bytecode.
- **Pins verified before work.** All 44 architecture pins match, and so does the Node 24.16.0 pin. Pins are verified again at the end; see Evidence.
- **Root validation 04 ran 478 checks only.** Its receipt, `docs/implementation/m1/trials/native-wire-owner-04/root-validation/receipt.json` (sha256 `a0b8d8f587fb56ed322dd310a334b463617aec9f03dbf7ff8736bd474bca42c5`), records `rootSelftestExecuted: false` and `rootIsolationExecuted: false`. The 108 mutants of candidate 04 were run by the author and by reviewer 04, not by root.
- **Root validation 05 ran 567 checks only.** Its receipt, `docs/implementation/m1/trials/native-wire-owner-05/root-validation/receipt.json` (sha256 `d8f6377d6220e84108d920ee773f01420fc0748ab170787cf32b27dff9e2ae2c`), records `rootSelftestExecuted: false`. The 132 controls of candidate 05 were run by the author and by reviewer 05, not by root.
- **Candidate-05 root attribution error.** Candidate 05 incorrectly attributed 108 mutants to root; root did not run them. It is preserved unchanged in `prior/subject-05/contract.md` and corrected here.
- **Preserved as byte copies (verified with sha256):**
  - the full subject-05 tree, including every earlier `prior/` file and the failed-control disclosures;
  - `prior/subject-05/`: its results, contract and successor documents;
  - `prior/subject-05-manifest.json`;
  - `prior/review-05/`: review.md, review.json, probe_05.py with its output, probe_05b.py with its output, mutants.py with its output, custody-after.json;
  - `prior/root-validation-05/`: stdout.txt, stderr.txt, result.json.
- **Method.** Root continued in a separate mutable copy after actual Claude reached its quota. `prior/root-resumption.json` preserves the partial author input hashes. Root validation uses the reference interpreter with `-I -B`; isolation supplies a minimal environment and private scratch. Root also maintains architecture evidence outside this candidate. These are reference tests, not a product sender or an independent review.

## Candidate, how to run, and source overrides

`/tmp/opensip-implementation/m1-native-wire-owner-root-candidate-06/`; `tools/filelist.py` lists the 41 inputs; `subject-files.json` lists inputs, outputs and evidence.

```
cd <subject>; PY=/tmp/opensip-implementation/metadata-reference-env/bin/python
R() { env -i PATH=/usr/bin:/bin HOME=/tmp OPENSIP_ARCH=/Users/sb/code/opensip-ai/opensip_arch TMPDIR=$PWD/tmp PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=$PWD/tmp/pycache $PY -I -B "$@"; }
R tools/build.py; R tools/vectors.py; R tools/manifest.py --inputs-only; R check.py; R selftest.py; R tools/isolation.py; R tools/outcome.py; R tools/manifest.py
```

**Explicit source overrides.** All are in memory or declarative; no pinned byte is changed.

| Override | Parent (pinned) | Applied by |
|---|---|---|
| 35 pattern rows and a closed 4-pair scope (`owner-pattern-successor.v1.json`) | native-evidence.schemas.v2, relation-payload-schemas.v2, occupancy companion; native, startup and wire models, identity-model.v3 | `tools/owner_successor.py` install on fresh model instances |
| 4 route keys, 2 domain detail members, 1 origin (`public-route-successor.v1.json`) | public route registry, public-detail-registry, workflows common, native model | `tools/check_routes.py` overlay |
| P3 guard additions (`p3-guard-successor.v1.json`) | protocol3-transitions.v1 | reference overlay |
| Carrier successor rows (`successor.json`), including the new `SUCC-PREPARED-READ-AUTHORITY` | rust2, delivery2, native evidence md and model | declarative rows; the reference selectors are in `tools/representability.py` |
| Canonical send plan and sender contract (`HOST-SEND-SCHEDULE`, `REQUEST-WIRE-ACCOUNTING`) | rust2 framing and limitPolicy, P3-29 | `tools/representability.py`, `tools/sender_ref.py` |

## RF-1: every sender slot bound to its planned payload; typed Cancel echo of the sent correlation

**Plan.** `tools/representability.py` gives every schedule slot `payloadSha256`: the SHA-256 of the deterministic-CBOR bytes of the planned payload. It is streamed by `wirecodec.encoded_digest`, which a check compares against the full encoding.
- **Chunk slots.** The digest covers the chunk payload without `bytes` (`payloadSha256Scope: payload-without-bytes`), because the planner never materializes chunk bytes.
- **Chunk content.** An entry's last chunk slot also carries `entryContentSha256`, the manifest entry `contentSha256`.

**Sender (`tools/sender_ref.py consume`).** Each slot is compared on:
- sequence, frameType, chunk coordinates and seal count;
- payload byte length and payload digest;
- for chunk bytes actually sent, the running entry hash against `entryContentSha256`.

Every applicable comparison happens before that frame becomes sent state. Whole-entry content integrity can only be checked at its last chunk: an earlier corrupt chunk may already have been sent. The entry is not verified until its last chunk passes, and a receiver must not publish or use it before complete manifest/seal admission. This reference is not a prevalidated immutable source-file custody proof. Length-only reference transcripts cannot be hashed, so `chunkContentVerifiedEntries` reports how many entries were verified.

**The Cancel echo:**
- It is derived from the correlation actually consumed: the executionId of the OpenUniverse frame consumed and the analysisOrdinal of the Analyze frame consumed.
- It is compared by deterministic-CBOR encoded typed bytes, so `false` is not `0`, `0.0` is unencodable and refused first by the wire codec as UNENCODABLE, and `false` is not `null`. Sequence numbers also require exact integers; Python false is not sequence zero.
- Request-limit re-checks run before commit, so a refused frame never extends the already-sent prefix (exposed as `progress`).
- Unchanged: the Cancel position law, the single reserved Cancel counted in the totals, the P3-29 row and the budget laws.

**The review's attacks, reproduced and now refused:**

| Attack (review-05 probe S on candidate 05) | Candidate 05 | Candidate 06 |
|---|---|---|
| OpenUniverse executionId same-length substitution, then the planned echo | accepted | refused `payload-digest` at the OpenUniverse slot, 1 frame sent |
| The same substitution, then an echo of the sent value | refused `cancel-echo` | refused `payload-digest` at the slot |
| SnapshotManifest manifestSha256 same-length substitution | consumed as complete | refused `payload-digest` |
| Cancel with analysisOrdinal `false` for planned `0` | accepted | refused `cancel-echo` |

**Permanent cases (`vectors:HOST-SEND-SCHEDULE`, 50 cases):**
- the four attacks above;
- same-length substitutions of the dependency manifest digest, seal digest, Analyze ordinal and chunk header, plus the TS2 OpenUniverse;
- typed echo cases: `false`/`0`, `0.0`/`0`, `false`/`null`, and TS2 `false`;
- materialized chunk bytes verified, and a flipped byte refused as `chunk-content` for snapshot and dependency chunks.

**Checks:**
- `schedule-slots-content-bound`: every planned digest equals the independently realized frame digest.
- `sender-refusal-before-sent-state`: the refused frame index equals frames sent, and neither the sent correlation nor the cancelled state changes.
- `sender-echo-derived-from-sent-state`.
- `review05-sender-attacks-replayed`: replays the reviewer's recorded candidate-05 outcomes against the same plan.
- `sender-cancel-echo-matches-cancel-nullability`.

**Controls:**
- `r5_sender_slot_digest_unchecked`
- `r5_manifest_slots_unbound`
- `r5_cancel_python_equality`
- `r5_planner_slot_digest_dropped`
- `rf1_echo_ignores_sent_state`
- `rf1_chunk_content_unchecked`
- `rf1_sent_state_committed_before_limit_checks`
- `rf1_slot_binding_text_dropped`

**Equivalent mutant, stated.** Replacing the consume-level sent-state echo with the planned echo is equivalent while digest binding holds, because the consumed correlation then equals the planned one. It is therefore not a control. Its derivation is exercised directly by `sender-echo-derived-from-sent-state`.

## RF-2: provenance and authority wording

- **Root attribution.** The contract attributes root runs exactly as the receipts above record them. `root-attribution-matches-receipts` requires both receipt digests, both check counts and `rootSelftestExecuted`, and refuses unqualified attributions; root did not run selftest or isolation in either earlier reproduction. Control: `rf2_root_mutants_attributed`.
- **Authority wording.** `OWNER-PATTERN-EVALUATION` now names `owner-pattern-successor.v1.json` as the proposed reference owner correction: an author candidate applied in memory, effective as selected semantics only after root acceptance and source-bridge promotion.
  - The prior misleading selector key is renamed `proposedOwnerCorrection`.
  - The standing of the owner pattern successor, the route successor and `successor.json` carries the same condition, as do the successor row and the restated review-03 resolution.
  - `unpromoted-successor-authority-wording` forbids premature owner-selection claims in the carrier rules, all successor documents and this contract.
  - Controls: `rf2_selected_owner_wording_restored`, `rf2_owner_standing_without_promotion_condition`.

## Advisories

**A-1: fact-plane framing and the relation-registry path gap.**
- **Corrected framing.** fact-plane.v1 `sharedTypes.CanonicalPath` is "non-empty NFC project-relative path, slash separators, no empty/dot/dot-dot segment, no leading slash or backslash"; it has no control-scalar clause. `check-fact-plane.py _is_path` is the historical v1 deterministic-CBOR profile checker, stricter than its own type because it reuses `_is_nfc_text`.
- **fact2 does not use it.** Retained fact2 admission (identity-model.v3 `registered_payload`) validates the relation v2 schema through `validate_registered_record` and never calls `_is_path`; the check verifies this against the pinned source. Candidate 05's statement that legitimate newline names "would still be refused at fact-plane admission" was wrong and is withdrawn.
- **The actual gap, recorded separately and not corrected here.** Relation v2 `CanonicalPath` admits `a//b.rs`, `a/` and `a<BEL>b.rs`, pinned and scoped alike. The inherited type forbids empty segments, and the v2 document says every inherited logical restriction survives.
  - `FilePayloadV1.path` is further bound by its snapshot-inventory join, which is not executed here.
  - The `PackagePayloadV1.manifestPath` and `VcsChangePayloadV1.previousPath` join laws are unchecked.
  - This is a relation-registry / fact-plane duty. The scoped successor keeps exactly one relation row, the terminator lookahead correction.
- **Checks:** `relation-registry-path-normalization-gap-recorded` and `fact-plane-path-law-no-change`. **Controls:** `a1_fact2_is_path_misattributed`, `a1_relation_gap_duty_dropped`.

**A-2: worker stale/failed partition and read authority.** This is the new rule `PREPARED-V3-READ-AUTHORITY` with row `SUCC-PREPARED-READ-AUTHORITY`, a narrowly declared owner correction that adds no field.
- **The worker cannot recompute PO-1.** `worker-po1-context-not-carried` walks every host-to-worker Rust3 carrier and extern schema, excluding the carried `planRow` itself, and finds no `toolchain`, `toolchainDigest`, `ToolchainIdentityV1`, `ownerFileManifestSha256` or `ownerManifests`.
- **SET-JOIN already refuses some stale rows.** `PREPARED-V3-SET-JOIN` refuses rows whose `dependencySourceSetId` or `cfgSetId` does not join.
- **No partition carrier exists.** No reviewed carrier conveys the owner's usable/stale partition.
- **Host duty.** The host selects a prepared set (non-null `preparedOutputSetId`) only when the owner outcome is admitted, meaning no row is stale. A defaulted partially stale set is not selected: `fallback-non-prepared`, zero usable rows, owner `staleRows` kept, `readAuthorityDisclosure: stale-rows`. This is the same shape as the over-limit fallback, and it replaces the owner's per-owner partial fallback on this wire.
- **Worker duty.** Within a selected set every carried row is fresh. The worker reads, mounts and consumes exactly the entries whose carried `planRow.status` is `ok`. It never reads a `failed` row, which is carried only for set identity; its owner is analyzed non-prepared per PO-2.
- **Vectors:** `PREPARED-V3-READ-AUTHORITY` (4). The earlier `defaulted-one-stale-256/10` owner-fallback-kept vectors are superseded by not-selected versions, kept under new ids in `PREPARED-V3-WIRE-LIMIT` and `PREPARED-V3-PATH-REPRESENTABILITY`.
- **Controls:** `a2_partial_stale_set_selected`, `a2_failed_row_readable`, `a2_worker_context_list_weakened`.

**A-3: the carried-row limit is kept.** A defaulted set of 257 rows with one stale row falls back with 0 usable rows and disclosure `entries`. The vector and the carried-row and usable-only controls are retained.

**A-4: pins and trust boundary.**
- **Pins:** all 44 exact pins are retained and verified before import and after the run, including the 8 identity-model.v3 registry-closure documents.
- **Node:** the binary is pinned by sha256 and size.
- **Unpinned system libraries:** CoreFoundation, Security, libc++ and libSystem, which the Node binary loads dynamically. They are a trusted, unselected boundary: the reference ECMA-262 results depend on them, but their bytes are not selected, pinned or verified.
- **Audit:** the open/`subprocess.Popen` audit is closure evidence for these code paths, not filesystem or process confinement.

## Remaining integration duties

These are declared in `successor.json` `futureQualification`:
- source-bridge promotion of the pattern rows and scope;
- production Rust/TS matchers with ECMA semantics for `[\s\S]*` inside a lookahead (regex-crate lowering);
- an M3 sender implementing `HOST-SEND-SCHEDULE`: per-slot payload digests, entry content binding over the bytes sent, and the typed-bytes Cancel echo of the sent correlation;
- M3 host and worker `PREPARED-V3-READ-AUTHORITY`;
- relation-registry / fact-plane: the relation v2 `CanonicalPath` path-normalization gap and the inventory and join laws, plus a full retained-closure `admit_frame` run;
- generator work, the renderer rebase and the D9 exit-contract successor.

## Evidence

- **Check:** root check02: 596 checks, zero failures; the final check result is `check-result.json`.
- **Selftest:** root full mutation run: 149/149 caught, no baseline failures; `selftest-result.json`.
- **Admission vectors:** 353 cases across 31 groups.
- **Isolation:** `isolation-result.json` records the final declared-input-only reproduction and its actual result; no broader confinement claim.
- **Pins after the run:** the final check rehashes all 44 architecture pins and the declared Node binary; system libraries remain an explicitly trusted, unpinned boundary.

Failures during this round, preserved: initial root check01 had four failures (two prose scans, one float-Cancel expected route and its aggregate); the initial manifest rejected four unclassified quota-harness files. Logs remain under `prior/root-continuation-06/`. The original author06 was interrupted by quota; it did not produce these fresh root results.

## Not claimed

- approval, acceptance or source promotion
- product integration
- production decoder, admission, sender or generator
- a full retained-closure `admit_frame` run
- regex-crate lowering
- platform or M2/M3 qualification
- commit or push, or a clean git state
- general confinement
- the unpinned Node system libraries
