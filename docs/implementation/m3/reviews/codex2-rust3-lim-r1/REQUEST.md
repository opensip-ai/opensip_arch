CODEX2 review: **RUST3-LIM**, the native contract successor that answers M3-L r3's cross-law item X13 (open question R12). Rust3 caps a request's subject list at `maxSubjectsPerStage` 256, and the list holds every non-empty `.rs` file of the snapshot. So a product Rust provider cannot be spawned for 9 of the 22 Rust-bearing T2 repositories, among them axum (301) and tokio (808). RUST3-LIM fixes this within Rust major 3 with a new optional token, `subject-scope-reference-v1`. Under it, each `Analyze` stage names its subject array by count and commitment, and host and worker rebuild the array from the manifest the worker has already accepted. This is a **design unit** (a `verify_design` contract successor). Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT-DESIGN-UNIT** or **REQUIRED-FINDINGS**.

Write only under `/tmp/opensip-implementation/reviews/codex2-rust3-lim-r1`.

**Rules:**
- **Read-only.** No repository edits, commits, pushes or delegation. Run git only read-only.
- **No builds or tests.** P0's lanes are running on this machine. Run no cargo, no tests and no crash-matrix binary or checker.
- **Scripts.** If you run anything, use only the evidence scripts below and read-only commands, at `nice -n 19`, with any scratch files under your review directory.
- **`verify_design`.** The lead ran the real `tools/verify_design.py` through `evidence/verify_scratch.py`, against a lock held in memory. If you run it, do so the same way, or against a scratch copy of the lock passed with `--lock`. Never edit the product.
- **Never fetch.** Nothing here needs the network.
- **Never touch the real home.** `~/Library/Application Support/OpenSIP` stays absent; do not read or create it.
- **Never read the private 413 UUID fixture.**

## Subject

The pins are in `hashes.txt`. Every file is untracked in arch until acceptance.
- **The subject manifest** is `docs/implementation/m3/native-successors-fa/rust3-lim-subject.json`. Its sha256 is `subjectManifestSha256`.
- **Its 14 members**, all under `docs/implementation/m3/native-successors-fa/rust3-lim/`, are:
  - `successor.json`, the record;
  - `README.md`, the design record, with every decision, the facts and the cascade;
  - `section-9-3a.md`, the text appended as NE §9.3a;
  - the two handshake successor copies, `design/native/provider-handshake.schemas.v1.json` and `product/schemas/sources/handshake-v1.schema.json`, which are identical;
  - the new stage-record schema, `design/native/rust-subject-scope.schemas.v1.json`, and its product copy `product/schemas/sources/rust-subject-scope-v1.schema.json`, which are identical;
  - `materialization-map.json`;
  - `evidence/build_rust3_lim.py`, `copies-report.json`, `vectors.json`, `count_rust_subjects.py`, `rust-subject-counts.json` and `verify_scratch.py`.
- **Not part of the subject:** `native-successors-fa/rust3-lim-unit.json`, the lead's DRAFT-PENDING-REVIEW record.

**Product.** Main is `cd5958b`, read-only. Its lock has 82 contract successors, I1-P being the 82nd. RUST3-LIM changes no product byte. D2b will copy the two product schema sources later.

**Order with FA-2.** RUST3-LIM's handshake parents are FA-2's two handshake copies (`32aeec8c…`, 33,812 bytes each), so it binds after FA-2.
- **FA-2's state.** FA-2 is in review with Codex. Its r1 returned REQUIRED-FINDINGS (FA2-R1-01, the NE:1927 text; FA2-R1-02, its cascade table). Its r2 is being prepared.
- **What this unit depends on.** Only on those two copies, which are the same in FA-2's r1 subject (`c339f4fb…`) and in its r2 candidate (`dca02900…`) as they stood when this request was written. FA-2's record and subject are read from disk as they stand.
- **If the copies change,** the build refuses. If you find FA-2's copies changed when you review, say so; the lead will rebuild this unit on them.

**Laws and records cited.** None is changed. The pins are in `hashes.txt`.
- **M3-L r3**, `provider-protocol-l/PROPOSAL-r3.md` (`6df524a4…`). These are the bytes at arch commit `e35272519` that Grok reviewed, REQUIRED-FINDINGS. **Not accepted.** It is cited only as the source of X13 and R12, whose facts Grok confirmed (`reviews/grok-provider-protocol-l-r3/REVIEW.md:44`). The live `PROPOSAL.md` may move to r4 while you review; if it does, read `git show e35272519:docs/implementation/m3/provider-protocol-l/PROPOSAL.md`.
- **M3-C r7**, `snapshot-plan-c/PROPOSAL-r7.md` (`a1ee9386…`), which you accepted in review: item 5's bounds and S-R, and item 6's sealed set.
- **M3-PLAN r6**, `M3-PLAN-r6.md`.

## What it does

The README has the full tables. In brief:

1. **The facts.**
   - **Where the cap lives.** `maxSubjectsPerStage` is a protocol constant (RPP:106). NE §9.3 retains it with an identical value (NE:2934), HS publishes it as `const` 256, and Hello checks it by exact equality (NE:2939-2941; HS:21). The cap is applied by `subjectsAlgorithm` before spawn (RPP:226-232).
   - **What depends on it:**
     - `Analyze` is one 64 MiB frame, and it repeats the inline array in every stage, up to 256;
     - the work-unit tuples are charged per `(stage, subjectOrdinal, entryOrdinal)`;
     - the commitments are fixed size, and the request keys do not depend on it.
   - **The counts.** All 22 Rust-bearing T2 entries are measured at their pinned trees, with nothing fetched. Nine T2a medium entries come from the E0 bare repositories with `git ls-tree -l`; all 22 come from the T2b per-blob listings, each digest-checked against the manifest. The two sources agree. Nine entries exceed 256: axum 301, tauri 327, tokio 808, deno 1,052, smithy-rs 1,084, rspack 1,384, rust-analyzer 1,483 (two empty files fewer than the manifest's 1,485), sui 3,318, and aws-sdk-rust 242,187. aws-sdk-rust is also beyond `snapshot2` and `maxSnapshotEntries`.
2. **The fix (LD-R1 to LD-R6).**
   - **The records.** `StageRequestV3` = `{stageOrdinal, planStage, analysisDomain: StageAnalysisDomainV3}`, and `StageAnalysisDomainV3` = `{subjectScope: RustSubjectScopeV1, requestedCoverageDomain, domainCommitment}`.
   - **The scope.** `RustSubjectScopeV1` = `{scopeKind: "nonempty-rs-files", subjectCount, subjectScopeCommitment}`. It carries no `snapshotId`.
   - **The commitments.** The recipes are RPP's own, over the rebuilt array, so `domainCommitment` equals the V2 value.
   - **Negotiation.** The V3 stage is used iff the token is negotiated, for every count. A mismatch is `PROVIDER.PROTOCOL_VIOLATION`.
   - **Bounds.** `ProtocolLimitsV3` is unchanged. `subjectCount` is at least 1 and at most `maxSnapshotEntries`, and `snapshot2`'s bounds apply first.
   - **Plan need.** The token is a token the Plan needs exactly when there are more than 256 subjects. Without it, the existing `capability-missing` route applies.
   - **The worker.** It rebuilds the array after `SnapshotAccepted` and verifies it before analysis. A mismatch is `ProviderFault` `input-rejected`.
3. **The form (LD-R7).**
   - **Six insert-only NE line overrides:** 123 (two §0 rows), 2790 (the token list), 2883 (a §9.2 row), 2942 (appends §9.3a), 3028 and 3070 (§9.6 consequential). They are disjoint from B-S1's eleven bound lines and FA-2's thirteen.
   - **Two complete successor copies of FA-2's handshake copies:** the token is appended last to `RustCapabilityToken`, `RustCapabilitiesV3.maxItems` goes from 14 to 15, three strings are extended insert-only, and a `subjectScope` wire-law entry is added. TS records, limits, Hello and HelloAck are byte-for-byte unchanged.
   - **A new schema document,** with a product copy.
   - **No ST override.** FA-2 holds the only pointer that names `StageAnalysisDomainV2`. §9.3a's reading rule covers it, EXC:276 and FA-2's `AnalyzeV3.stages` description.
4. **TS2 (LD-R9).** TS2 needs no change. DLV's `SubjectScopeV1` already names its file set by reference, and its limits have no subject member. The README says exactly when a TS2 limit successor is needed and what it must then also solve: the single-frame `SnapshotManifest`.
5. **S-M (README "What S-M must measure").** No number in the successor depends on S-M. SM-11 to SM-14 are proposed for L's item 9, with `⟨SM-n⟩` placeholders. They are per-subject analysis cost, rebuild cost, response volume (including FA-2 census rows) and work-unit tuples, and they set the Rust stage budget and the effective ceiling `S_eff`.

## Deviations and judgement calls, for you to rule on

1. **This unit depends on a unit in review.** Its parents are FA-2's candidates, not accepted bases. `verify_scratch.py` shows that it is refused alone and passes after FA-2. Is binding after FA-2, with a parent-only rebuild if FA-2's copies change, acceptable?
2. **The reading rule instead of overrides** for ST/PST `hostConversion` (FA-2 holds it), EXC:276 and FA-2's census-schema description. Is each covered, or must any be overridden?
3. **No new limit member.** The scope is bounded by `maxSnapshotEntries` through the accepted manifest, and the schema states `maximum: 200000`. Is that a finite, typed bound under `limitPolicy`, or does the change need a member, and so a changed Hello map?
4. **The Plan-time need is conditional on the count** (more than 256), not unconditional (LD-R5).
5. **`snapshotId` is omitted from `RustSubjectScopeV1`,** although DLV's `SubjectScopeV1` has it (LD-R2).
6. **The worker's refusal is `ProviderFault` `input-rejected`.** RPP states no worker-side domain rule today, and this follows DLV:758's rule in Rust's fault vocabulary.
7. **F-1 to F-6 are found in passing and routed, not fixed.** For example: an inline `Analyze` can exceed one frame even at 256 (F-1); the empty-subject refusal is untyped (F-2); the single-frame manifest limits S-R (F-3); the response safety bounds now come within reach (F-4).

## Decide

1. **Facts.** Is the cap's location and its nature (a constant, Hello-checked, not negotiated) stated exactly? Is the dependency list complete: frame, memory, request keys, work units and commitments? Are the counts right, and is each source's method sound? Rule on rust-analyzer's 1,483.
2. **Lawfulness within major 3.** Is a token-gated stage-request version lawful without a major bump, against NE:2799-2814 and NE:2835, F02:271-273, AQP:402 and EXC:270? Is anything here a frame, phase, terminal, limit or identity change in disguise?
3. **The choice.** Is candidate 4 the least-cost lawful change? Are candidates 1, 2, 3, 5, 6 and 7 rejected for the right reasons? In particular: candidate 1's frame coupling and limits-map change, and candidate 3's "no existing frame can carry it".
4. **The test.** Does every bound stay finite and typed? Do refusals stay typed? Are the work budgets still charged per subject? Is any bound weakened, including the response safety bounds (F-4)?
5. **Records and commitments.** Are `StageRequestV3`, `StageAnalysisDomainV3` and `RustSubjectScopeV1` exact and closed? Do the recipes really stay RPP's own, with equal values (`evidence/vectors.json`)? Does the worker's rebuild-and-verify close the trust gap?
6. **Exactness of the form.** Is every `before` the exact parent line? Is every `after` a true and minimal insertion? Does §0 row E name the right selectors? Does any other accepted passage still name the inline array as the only Rust domain shape?
7. **The copies.** Is each copy exactly its FA-2 parent plus the stated edits (`evidence/copies-report.json`)? Is appending the token last right? Is `maxItems` 15 right?
8. **FA-2 coordination.** No line conflict, a composable payload, census bounds as the next ceiling. Is anything in FA-2's §9.8, its §0 rows or its census schema contradicted?
9. **TS2.** Is "TS2 does not have this problem" right? Is the TS2 limit successor's trigger and duty stated exactly?
10. **S-M.** Are SM-11 to SM-14, the workloads and `S_eff` the right measurements to set the budgets? Is any figure missing?
11. **Cross-law items.** Rule on X-RL-L1 (the G11 recommendation), X-RL-L2, X-RL-L3, X-RL-FA2, X-RL-C1 to C3, X-RL-D, X-RL-G1 and G2, X-RL-F, X-RL-H and X-RL-P.
12. **Selection.** Is the successor well-formed for selection after FA-2, under `verify_design`'s `contract_successor` and `successor_chain` rules? Is anything else wrong?

## Running the evidence (optional)

Use `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B` at `nice -n 19`, from `/Users/sb/code/opensip-ai/opensip_arch`.

1. **Build check.** `docs/implementation/m3/native-successors-fa/rust3-lim/evidence/build_rust3_lim.py --product /Users/sb/code/opensip-ai/opensip --check` rebuilds everything in memory and compares it with the files on disk. It reads the product lock and one base blob read-only, and emulates FA-2 bound next.
2. **Dependencies for the schema cases.** The design encoder imports `jsonschema`. Install it offline into your review directory:

   `python3.14 -m pip install --no-index --no-cache-dir --find-links ~/opensip-deps/wheels --target /tmp/opensip-implementation/reviews/codex2-rust3-lim-r1/deps jsonschema==4.25.1`

   Then add `--deps <that dir>` to the build check.
3. **Counts.** `.../evidence/count_rust_subjects.py --check` recounts the 22 entries from the E0 trees and the T2b listings already on this machine, under the lead's session scratchpad. It refuses if they are absent; it never fetches.
4. **Selection.** `.../evidence/verify_scratch.py /Users/sb/code/opensip-ai/opensip --rev cd5958b` runs the product's real `verify_design` design-only. Without `--rev` it uses the checkout and also checks generation and admission sources. It writes nothing.

The lead ran each of them, the build check twice, with byte-identical results. `verify_scratch.py` passed in both modes: 82 base, refused alone, 83 with FA-2, and 84 with this unit.

## Output

Write REVIEW.md and review.json. review.json must contain:
- `"verdict"`: `ACCEPT-DESIGN-UNIT` or `REQUIRED-FINDINGS`;
- `"requiredFindings"`: each with id, location, problem, evidence and fix;
- `"nonBlockingObservations"`;
- `"subjectManifestSha256"`: a single string, the sha256 of `rust3-lim-subject.json`. The lead's value is `5dfd3cd993b9d1a364468ce2df4981ff78b08497d2521cfd8ce48754a86b34cc`.
- `"successor"`: `{path, bytes, sha256}` of `rust3-lim/successor.json`. The lead's value is 17130 bytes, `70f494d9a95b7ea82cfe066087969ca3ad68caa409e10a8a18db62a5cfb37703`.

This is a contract successor, so it has no `inventoryCandidateAssessment`. If you would change bytes, give the exact replacement text. Do not commit.
