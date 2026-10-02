Grok review of three subjects together: the identity contract successor EC1 (the core evaluator closure), the X3d r8 amendment and the record-only X9 r7. Claude Opus 5.5 leads, and you are the single reviewer.

**Rules for this review:**
- No repository edits, commits, pushes or delegation.
- Write only under /tmp/opensip-implementation/reviews/grok-evaluator-closure-x3d-r8.
- This is a law and contract review, with no product cargo. You may run the three EC1 evidence scripts named below, which only read. Run git read-only.
- The real home (`~/Library/Application Support/OpenSIP`) must stay absent. Never read the private 413 UUID fixture.

## The defect

X3d r7 item 3 step 1 says: "Its evaluator closure equals the session's selected core closure." At product main a36da7c, `plan` (`crates/storage/src/commit.rs`, lines 248–256) enforces `run.evaluator_closure() == session.core_closure()`. The two ids can never be equal:
- `core_closure()` is `InitialCore::closure()`, the authenticated core inventory's `closure2:` over a `kind: "core"` descriptor (`crates/security/src/trust/core_inventory.rs`, lines 378–398).
- Replay requires the seal's `evaluatorClosure` to name a retained, Plan-selected closure of `kind: "evaluator"` (`crates/evaluator/src/execution_inputs.rs`, lines 688–695; `execution_reader.rs`, line 201).

So `prepare_commit` refuses every real `ReplayedRun`. X3d-2's tests missed it, because `bound()` (`crates/storage/src/commit_tests.rs`, line 111) copied the closure, and the project, from the Run under test. X9-2 found it (EXIT-PLAN, "BLOCKER: commit closure binding"). It blocks X8c, X9-2 to X9-6 and any production commit.

## What the design and runtime said (the lead's investigation)

- **No accepted text relates the two closures.**
  - The build plan binds `CommitSession` to an "admitted producer closure" (line 51), and storage compares "producer selections" (line 67).
  - The identity contract makes the seal's evaluator kind `evaluator` and Plan-selected (`closureKinds`, `closureMembership`). Its `closure.manifestDigest` is "the admitted component manifest body bytes", for every kind.
  - 463 item 3 makes the core closure "the inventory's closure identity". The core inventory contract v16, security-completion v8 and X4B r5 never mention an evaluator closure.
  - The build plan's component-manifest list (line 703) omits the evaluator, and D1-plan G28 says `.evaluator` = "pure core".
- **No runtime value names one.** The core inventory has `semanticVersion`, `protocolMajor`, `servedProtocolMajors`, `platforms` and `embeddedBootstrap`, with no evaluator member. An admitted component manifest is fixed to `kind: "component"`, `role: "analyzer"` (`crates/security/src/generated/component_manifest_shape.rs`, `node_2` and `node_8`). The write receipt does hold the running, authenticated `InitialCore`, so the inventory descriptor is reachable from the session.

So the fix needs a definition, and EC1 supplies it. The lead took it as a lead decision under the owner's standing direction of 2026-09-30. It is flagged to the owner, who may override it, because it gives every core release a new evaluator closure and so new PlanIds and RunIds.

## Pins

Pins are in hashes.txt.

- **EC1** (contract successor, new). The subject manifest is `core-evaluator-closure-ec1-subject.json`. Its members are `core-evaluator-closure-ec1/README.md`, `successor.json` and `evidence/{build_ec1.py, check_ec1.py, vector.json, verify_scratch.py}`. Its two parents are accepted inputs of the product lock:
  - `docs/coop/design-corrections/foundation/identity-schemas.v3.json`, `a76c9e2f…`;
  - `docs/v2/contracts/product-v1/identity-and-evidence.md`, `c82404f3…`.
- **X3d r8** (amendment). `commit-session-x3d/PROPOSAL.md`. The snapshot `PROPOSAL-r7.md` already existed, and it was checked, not rewritten. Its sha256 `84cd377e…` equals `reviews/grok-record-x3d-r7-x7-r6-x9-r3/x3d/review.json`'s subjectSha256, and it equals PROPOSAL.md before r8 with its "r7 ACCEPTED" note removed.
- **X9 r7** (record-only). `crash-matrix-x9/PROPOSAL.md`. The snapshot `PROPOSAL-r6.md` already existed, and it was checked, not rewritten. Its sha256 `34bff15d…` equals `reviews/grok-crash-matrix-x9-r6/review.json`'s subjectSha256, and it equals PROPOSAL.md before r7 with its "r6 ACCEPTED" note removed.

The arch files are committed in the commit that assigns this review. The successor is not in any lock. Product main is a36da7c, read-only, and nothing in the product changes in this round.

## EC1: the core evaluator closure (verdict: ACCEPT-DESIGN-UNIT or REQUIRED-FINDINGS)

**The rule.** A core release's evaluator closure is `closure2:` + H("closure", D′). D′ is the authenticated core inventory's selected-platform descriptor that security already projects for the core closure, with `kind` set to `"evaluator"` and every other member unchanged. For kind evaluator, `manifestDigest` is the raw SHA-256 of the TR-CORE-signed inventory body (`opensip.metadata.inventory.1`), excluding its envelope. The two ids of one release differ only by `kind`.

**Overrides.** There are five, and each only inserts text: every word of its `before` survives.
- `identity-schemas.v3.json`:
  - `/$defs/closure/properties/manifestDigest/x-opensip-digest/artifact`: the artifact for kind evaluator;
  - `/x-opensip-digest-domains/closureKinds/note`: the rule.
- `identity-and-evidence.md`:
  - line 273: the `manifestDigest` sentence;
  - line 278: a new "Core evaluator closure" paragraph, with the rule, retention and identity consequences, and historical bytes unchanged;
  - line 455: the `raw-artifact` row.

No accepted successor overrides these selectors. `closureKinds.byField`, `closureMembership` and the closure kind list are unchanged, and no kind `core` is added.

**Test vector.** `evidence/vector.json` uses product fixture `crates/security/tests/fixtures/core-inventory318.ndjson`, case `baseline-macos`, at a36da7c. It holds:
- the 5990-byte inventory body;
- core closure `closure2:54322a2c18a7ed6d5a2c92ab7e1204884e7095cfc254d40d352f879761fa118d`, the fixture's own expected value, recomputed;
- core evaluator closure `closure2:7da97b9a4686fe5dc6ff69d83ddde230ac6895afb699717f2ef07a05810b89e2`;
- both descriptors' canonical SHA-256.

**Checks the lead ran:**
- `python3 -I -B evidence/check_ec1.py /Users/sb/code/opensip-ai/opensip` passed. It covers:
  - every override's `before` and its insert-only form;
  - the body hashing to `manifestDigest`;
  - the descriptors being equal except `kind`, and the ids differing;
  - the evaluator descriptor fitting the closure schema's closed shape and kind list;
  - all 53 accepted fixture cases recomputing their core ids and giving different evaluator ids.
- `python3 -I -B evidence/verify_scratch.py /Users/sb/code/opensip-ai/opensip`, which runs the real verify_design with EC1 appended and a synthetic in-memory review and assent, passed. It reported 75 contract successors, inheritance at 55 rows, v118 selected, 40 generation sources, and 48 admission sources with 15 aliases.
- Two runs of `build_ec1.py` produced the same bytes.

**Judgment calls. Please rule on each.**
1. **The pure core is the evaluator.** D1-plan G28 (`.evaluator` = "pure core") is read as making the core release the evaluator's closure. It is not read as calling for a separately delivered component.
2. **`manifestDigest` for kind evaluator is the TR-CORE inventory body.** It is not a component manifest. Rejected: inventing an evaluator component manifest that no release carries.
3. **Text-only overrides.**
   - The product's `schemas/sources/identity-v3.schema.json` (the same two annotation strings) and the generated `apps/report/src/generated/report.ts` keep their bytes. This follows stage-meta-reference-selection-v1 ("current schema bytes/hash recipes/generated artifacts remain unchanged; explicit passage overrides will describe the new semantic owner"). No code dispatches on either string.
   - `crates/identity/src/closure.rs` and `crates/evaluator/src/view-joins-registry.json` are unchanged.
   - Say whether X3d-3 must instead update the product schema source.
4. **Retention consequence.** Default `preimage` retention, enforced by the identity walk's raw-artifact rule, means a Run that names the core evaluator closure retains the inventory body and every core tree file. These are stored once per store per release under raw SHA-256. This is disclosed, not changed.
5. **Identity consequence.** Every core release gives new PlanIds, RunIds and cache keys. This is disclosed and flagged to the owner.
6. **The rejected alternatives**, in the README and in X3d r8's header:
   - (a) without a definition;
   - (b) a tree-membership test;
   - a signed inventory member;
   - a TR-COMPONENT evaluator;
   - admitting kind `core` in replay;
   - dropping the check.

review.json for EC1 must hold:
- "verdict": `ACCEPT-DESIGN-UNIT` or `REQUIRED-FINDINGS`;
- "requiredFindings";
- "subjectManifestSha256": a single string, the sha256 of `core-evaluator-closure-ec1-subject.json`;
- "successor": {path, bytes, sha256} of `core-evaluator-closure-ec1/successor.json`.

It has no `inventoryCandidateAssessment`.

## X3d r8 (verdict: ACCEPT or REQUIRED-FINDINGS; diff against PROPOSAL-r7.md)

The r8 header gives the defect, its evidence, the change and the rejected alternatives. In place:
- **Item 1.** `CommitSession` also holds the receipt's core evaluator closure.
- **Item 2.** `open` binds the core evaluator closure, derived by EC1's rule from the receipt's authenticated inventory and never from the Run. It is exposed as `CommitSession::core_evaluator_closure()`.
- **Item 3 step 1.** "Its evaluator closure equals the session's core evaluator closure, derived by security from the same authenticated inventory as the core closure", followed by an r8 note quoting r7's sentence. The project binding stays.
- **Item 12.** Test binding values come from a real session, never from the Run under test.
- **Item 13.** The new unit X3d-3 (security and storage):
  - the `Projection`, `InitialCore`, `PlatformReceipt` and `ProjectOperation` values, and the session getter;
  - one shared test-support accessor on X8 r3 item 4b's site list, which gives the descriptor, the inventory body and the tree bytes;
  - `Bound.evaluator_closure` and `plan`'s comparison;
  - the synthetic run candidate, moved from X9-2 into X3d-3;
  - `bound()` taking project and closure from a real `scenario-fixtures` session;
  - the EC1 vector test, the corpus-Run mismatch test, and the test that the core closure is not the evaluator closure;
  - the product annotation copies left unchanged;
  - no trust or release-format change.
  - Dependencies: EC1's selection and X8b. It lands before X8c and X9-2.
- **Forbidden substitutes.** A new (r8) entry forbids comparing a Run's evaluator closure with the core closure, and taking the session's side of step 1 from the Run, a worker claim, a build-time string or a test binding copied from the Run.

No outcome, row, code, detail, type, lock order or budget changes. Please check:
- every accepted sentence of r7 survives, apart from step 1's sentence, which the defect requires changing and which the r8 note quotes;
- the X3d-3 delta is complete and lawful, in particular:
  - the shared-site accessor;
  - moving the candidate into X3d-3;
  - the X8b dependency;
  - that `bound()` with real session values is achievable through `scenario-fixtures`.

## X9 r7 (verdict: ACCEPT or REQUIRED-FINDINGS; record-only; diff against PROPOSAL-r6.md)

It records X3d r8 and EC1:
- the r5 header's closure reason described X3d r7;
- the synthetic candidate rewrites the evaluator closure to `CommitSession::core_evaluator_closure()`, not `core_closure`, and keeps that closure's descriptor with its manifest and tree blobs;
- X3d-3 lands the candidate, and X9-2 uses it and depends on X3d-3.

The touched sentences (the r5 header's "How it is built", item 6's candidate bullet, and X9-2's unit line) each carry an "r7 (record)" note. Is it faithful to X3d r8, and does any accepted X9 outcome change?

## X8: not in this review

B2's wording is relayed to the X8b round for X8 r4. X8 is not edited here.

## Decide

For each subject separately:
- Is it correct and lawful?
- Does any accepted outcome change beyond what it declares?
- Is the predecessor snapshot exact?
- Rule on EC1's judgment calls.
- Is anything else wrong?

Write one REVIEW.md and three verdict files: `ec1/review.json` (the shape above), `x3d/review.json` and `x9/review.json`. Each law file must contain:
- "verdict";
- "requiredFindings";
- "noAcceptedOutcomeChanged" (for X3d, judged apart from step 1's declared change);
- "subjectSha256";
- the preserved snapshot's path, bytes and sha256.

Do not commit.
