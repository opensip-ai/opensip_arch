# consumer-b.v24 — blind consumer review of the OpenSIP design kit

**Verdict: CHANGES_REQUIRED**

## Standing

- This is an independent blind consumer reconstruction of the selected kit only. It reports only the admission, closure, replay and vectors this review executed itself.
- There is **no product qualification claim** and no implementation authorization.
- External root admission of the exported bytes is a separate gate. Its outcome is unobserved here.
- The following are future qualification: real OS/compiler/crypto/SQLite measurement, native compiler or provider execution as enforcement proof, host authentication, and synthetic TCB enforcement. They were explicitly not performed and are not counted as design omissions.

## Custody

`runs/final-custody.json`, re-verified at the end of the session:
- `subject/consumer-input-manifest.json` SHA-256 is `e57ef3a785d5e25cfdfd02955cb4249f5f2443da1790832dce50d9d64bb4cc3c`.
- Its `parentSubjectSha256` is `245ef613243aafeaac2dcdca7f0b398d5a770ec338abbf712039fdfd91676680`.
- All 102 members are hash- and length-exact, no file is unlisted, and the file set is identical to the phase-0 custody rows.
- The charter prose says "101 kit files"; the manifest lists 102 (advisory A3).

## What was executed

Accounting is in `requirement-status.json`, `checkpoints/phase-0.json` … `phase-11.json` and `blind-review.json#/requirementStatus`:
- All 123 requirements (R-*) and all 8 standing rules (S-*) are executed with measured artifacts.
- The 3 future-qualification IDs (F-OS-COMPILER-CRYPTO-SQLITE, F-SYNTHETIC-TCB, F-AUTH-HOST) are recorded as unperformed.
- Failed attempts were preserved before each correction: `*.attempt*.json` files, `runs/phase8-envelopes.attempt*.log`, and `checkpoints/phase-9.attempt*.json`.

### Claimed complete positive Runs

There are 26, each exported as `runs/<run>.store.json` (object table plus every blob/frame keyed by digest):

| Family | Runs |
|---|---|
| Syntax | syntax-code, syntax-data, syntax-mixed-disclosed, syntax-mixed-omitted |
| TypeScript | ts-pass, ts-fail, ts-clones-required |
| Rust | rust-mixed, rust-mixed-clones-required, rust-extra-unit, rust-same-file-2021, rust-ambiguous, rust-partial |
| Comparison (one project) | cmp-base, cmp-code, cmp-hidden, cmp-scope, cmp-policy, cmp-waiver, cmp-evidence, cmp-gbase, cmp-gevidence, cmp-gmissing, cmp-empty, cmp-code-det2, cmp-code-detc |

For every one of them:
- **Schema.** Every admitted record was re-validated against its owning kit schema (typed scalars, stock JSON Schema, `x-opensip-order`) and the `x-opensip-digest` law. There were 0 refused records (`runs/<run>.records.json`).
- **Closure.** Complete retained-closure admission ran, then independent semantic replay in a **fresh reference-interpreter process**: `runs/<run>.replay.json` and `runs/<run>.replay.fromscratch.json`, all ADMIT. The one designed negative, `syntax-mixed-falsecomplete`, still refuses.
- **Replay export.** `runs/<run>.replay-export.json` holds the replayed inputs, per-rule enumeration, every predicate witness (matching fact ids, Coverage ids, children, deficiencies, values), findings, verdict and the complete recomputed proof. The recomputed proof is **byte-equal** to the retained proof frame, proof/evidence/seal/run identities are equal, and every witness is byte-equal.
- **Tamper controls** (syntax-code, ts-pass, rust-mixed). Identities and citations stay valid while the logical result changes, and replay refuses every such control. Identity controls refuse earlier, at graph admission.
- **Four boundaries.** Schema, helper predicates, closure/replay and host enforcement are kept distinct; host enforcement is never claimed.

Mutation variants are in `runs/*~*.replay.json`; there are 32:
- **30 refuse** with a typed first refusal: published keys where the kit names one, `cb24.*` where it does not.
- **2 admit.** These are deliberate measurement variants, not negatives:
  - `syntax-code~budget-exhausted` admits and seals indeterminate.
  - `syntax-code~stage-output-schema-relation-doc` admits with a different executionPlanId (the evidence for S1).

### Vectors

Every vector carries a valid/invalid/explanatory label, and every negative carries its first refusal and masking. By phase:

- **Canonical / H / lexical admission, CVE1 capability manifests, provider traces:** phases 1–3.
- **Relation/rung tables, count/class/attempt, cell-outcome state rules:** phase 4.
- **Complete Runs, including the Rust body-identity pairs:** phase 5.
- **Configuration, clones, repair descriptor, minimum resolution, imported observation boundary, mutation replay scope, pinned purge:** phase 6.
- **Phase 7 — invocation, availability, envelopes:**
  - zero-config multi-unit selection with missing capabilities and candidate-only clones;
  - invocation disclosure, single-step and multi-step envelopes;
  - four public failure envelopes derived from actual internal refusals and their originating boundary;
  - the D9 selected composition compared with the inherited artifact;
  - durable receipts and availability.
- **Phase 8 — baselines, comparisons, authorizations, public terminations:**
  - baseline adoption with fresh-host admission, and comparisons under four audit profiles;
  - missing-evidence, evidence-changed, empty-result and scope-policy-only comparisons;
  - E0 (a committed pivot Run over the current snapshot) vs E1–E3 (re-evaluations of current inputs); pivot-only fingerprints;
  - test/preparation/repair authorization records;
  - purge, replay and required-output failures;
  - 43 D9 goldens;
  - host-captured vs candidate-only work; the four evidence states; the detector compatibility listing vs the component manifest.
- **Phase 9 — graph query and three-valued replay:**
  - `vectors/graph-query.json`: 53 executed `graph.neighbors|path|reach` vectors over admitted Runs. They cover selection, endpoint membership, canonical order, bounds vs pages, continuation after a newer latest observation or cache loss, evidence limitations, failure envelopes, and renderer/summary parity.
  - `vectors/replay-three-valued.json`.

### From-scratch recompute command

```text
cd /tmp/opensip-design-corrections/consumer-b.v24/output
/tmp/opensip-architecture-review-env/bin/python -I -B tools/from_scratch.py     # fresh process per Run: identities, closure, replay
/tmp/opensip-architecture-review-env/bin/python -I -B tools/replay_export.py    # admission-gated export of replayed inputs, witnesses, complete proof, comparison
```

Every vector script exits nonzero on a failed expectation. See `notes/09-reconstruction.md` for the remaining commands.

### Helper corrections

HC-1 … HC-13 are listed in `blind-review.json#/helperCorrections`. Each was corrected from the kit only, with the original failure preserved. No author model, fixture or report was read. None of these is counted as a design gap.

## New MUST issues

**M1 — The required clones-fact census makes default TypeScript/syntax Runs permanently indeterminate, while Rust passes the same shape.**
- *Selectors:*
  - native-evidence.md line 789 (default selection: every capability, `required=true`);
  - enumeration-plan.schema.v1 `x-opensip-kind-derivation` (clones-fact → `[file]`) and `x-opensip-file-membership-extent-law.fileKind`;
  - identity-schemas.v3 `scopeCapabilityLaw`, and the native s1.2 grammar law;
  - contradicted by native-evidence.md line 443.
- *Measured:*
  - `ts-clones-required`: ADMIT, sealed indeterminate.
  - `syntax-mixed-disclosed` and `syntax-mixed-omitted`: indeterminate.
  - `syntax-mixed-falsecomplete`: refused.
  - `rust-mixed-clones-required`: ADMIT, pass.

**M2 — `program-predicate.nodeDigest` digests RuleProgramV2 nodes under the policy-1 `Predicate` record.**
- *Selectors:* identity-schemas.v3 `#/$defs/program-predicate/properties/nodeDigest/x-opensip-digest` names `workflows/schemas/policy-document.schema.json#/$defs/Predicate` with retention `fragment`, while the program is `policy-document.v2.schema.json#/$defs/RuleProgramV2`.
- *Measured:* `syntax-code~explicit-endpoint-source` REFUSES with `DIGEST_FRAGMENT_RECORD_REFUSED:$.nodeDigest`. Any v2 `endpoint` atom, including every incoming target atom, makes a lawful Run unclosable.

**M3 — UnitMembershipV1 unit/row order and `unitOrdinal` assignment are unpublished, but they reach PlanId.**
- *Selectors:*
  - native-evidence.schemas.v2 `#/$defs/UnitMembershipV1` (`sequence` order);
  - native-evidence.md lines 610-646. Line 649 points to `docs/coop/design-corrections/discovery-defaults.py`, which is absent from the kit;
  - `membershipDigest` → analysis-spec parameter → PlanId.
- *Measured:* `syntax-code~membership-reordered` is schema-valid and refused only by this reconstruction's own chosen order.

**M4 — `detectorId` has no derivation, but it is identity-bearing in `baselineId` and in the exact E0 detector map join.**
- *Selectors:*
  - evaluator3 baseline-artifact `DetectorClosureEntry`/`BaselineEntry` and comparison-result `Entry`/`DetectorDisposition` (no description; a separate `contributionId`);
  - workflow-projection-contract.v3 s11, line 190;
  - evaluator-emission-plan rows (no detectorId).
- *Consequence:* portable baselines diverge across conforming hosts. This review chose `detectorId = contributionId` (cb24).

**M5 — The query parity field `query-response` has no carrier in the JSON parity reference.**
- *Selectors:*
  - workflows-and-surfaces.md lines 1055-1060;
  - command-inventory.v3 query `parityFields` and the JSON renderer `parityRule`;
  - evaluator3 command-envelope schema (`additionalProperties: false`; `query` is only the compact QueryResult).
- *Measured:* `vectors/graph-query.json#/measuredQueryResponseCarrier`. Every envelope carrying the complete response is refused.

## New SHOULD issues

- **S1 — No closed registry of stage output schema documents.**
  - *Selector:* identity-schemas.v3 `stage-spec.outputSchemaDigest`.
  - *Measured:* `syntax-code~stage-output-schema-relation-doc` has the same planId and a different executionPlanId, and both ADMIT.
- **S2 — The clone level-specification custody join is unnamed.**
  - *Measured:* `syntax-code~clone-level-spec-not-in-grammar` is refused only by `cb24.CLONE_LEVEL_SPEC_NOT_IN_GRAMMAR_CLOSURE`.
- **S3 — No rule mints a zero-config syntax-only unit or scope.**
  - *Selectors:* enumeration-contract s1 vs native U-1 and line 178.
- **S4 — The `NativeCoverageAccountV1.targetUniverse` carried value is unstated.**
  - *Selector:* execution-inputs s5. The field is identity-bearing in `executionInputsDigest`.
- **S5 — The `argvDigest` recipe is unpublished.**
  - *Selectors:* security `RepoExecutionGrantV2.argvDigest`; security-and-lifecycle.md lines 1065, 1115, 1122; `TestPayloadV1.argvDigest`.
- **S6 — Three failure goldens have no DomainDetail, but `kind=failure` requires `errors[]`.**
  - *Goldens:* `doctor-report-not-producible`, `query-latest-empty`, `envelope-major-unsupported`. `query-latest-empty` also disagrees with query-projection-contract s7.
  - *Measured:* `envelopes/public-termination.json`, 40/43 goldens form complete examples.
- **S7 — `IndeterminateReason` cannot express unknown absence that has neither an evidence nor a pivot cause.**
  - *Selectors:* comparison-result `IndeterminateReason`; workflows lines 348-352.

## Advisories

- **A1** Unannotated 64-hex fields: execution-inputs (16 positions), incoming-search (3).
- **A2** identity-schemas.v2 selector drift in enumeration-plan and subject-inventory.
- **A3** Charter says 101 kit files; the manifest lists 102.
- **A4** Pruned-tree bytes captured into the inventory are undecided.
- **A5** The TS universe `jsAdmittedToProgram` derivation is unwritten.
- **A6** `correspondence.reason` is singular.
- **A7** `viewDigests` observation standing.
- **A8** Abbreviated or unnamed internal refusal keys (carried as `cb24.*`).
- **A9** Outcome for required evidence unavailable while the root is decided elsewhere.
- **A10** The inherited D9 v1.14 artifact alone refuses the selected `host-invariant` termination (the kit records a live successor obligation).
- **A11** The test-execution `EnforcementValue` enum lacks the `ENFORCED-PLATFORM:<primitive>` form.
- **A12** `gateReason` has no member for a CODE-NET-NEW hidden by a detector-semantics change.
- **A13** Required-projection failure before commit has no registered DomainDetail.
- **A14** Exact-snapshot import correspondence makes gating evidence rules INDETERMINATE on any source change. The kit discloses this.

Details, freedom-vs-missing adjudication and the blocker statement are in `notes/10-gaps.md`.

## Why not ACCEPT and not BLOCKED

- **Not BLOCKED.** Every promised vector and complete Run was built and measured. Wherever a recipe was missing, the choice is named as cb24 with its selector, and no meaning was adjusted.
- **Not ACCEPT.** Five MUST and seven SHOULD design gaps remain, so the charter requires CHANGES_REQUIRED, independently of execution completeness.
