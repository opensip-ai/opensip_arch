# Review request: B2B3-PLAN-r2 (the lead's implementation plan for B2-b3, the S3 downward walker)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b2b3-plan-r2/`).

## Boundaries

Do not edit either repository, the stage or control files. Do not run Cargo, tests, builds or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys, held trees or any T2 held-out entry. Do not use other panes and do not delegate. Read-only reading, hashing, JSON parsing and Git queries are permitted.

## Subject

- **Stage.** `/tmp/opensip-implementation/b2b3-plan-r2-stage`
- **Subject file.** `subject.json`: 452 bytes, SHA-256 `e2a4d3d57b91c131ce8ed8b71ecce456685539e0d9db2b0967fff5249990f4b0`, 1 member(s). Rehash every member.
- **Round 1.** Your `codex-b2b3-plan-r1` (REQUIRED-FINDINGS: B2B3PLAN-1 to B2B3PLAN-5, with NBO-1 and NBO-2) is at `/tmp/opensip-implementation/reviews/codex-b2b3-plan-r1`. PLAN-r2's "r2 changes" table maps each finding and observation to its resolution.
- **Bases.** Product `3b3ab6e0e354c8f81e4ac030ed3102757be43085`, clean: B2-b1 and B2-b2 are bound. Architecture `47bee3b55292a973e90bbff6e81e3c509b28f3c0`.

## Authority

- The accepted B2-b plan r4 (`docs/implementation/m3/config-discovery-b/b2-b/PLAN-r4.md`): section 1.3, LD-B2B-2 and LD-B2B-5 to LD-B2B-9.
- M3-B r5 items 12, 13 and 15, and the test owners.
- The bound B2-b0 reference's `walker_population` (contract successor 164).
- SL S3.
- X2 r9: items 1, 3a and 7a (the handoff).
- M3-C item 2's walk rules (`docs/implementation/m3/snapshot-plan-c/PROPOSAL.md` lines 268-296).
- COV:5288 and COV:5388.
- The product's `operation_handoff.rs`, `installation_read.rs`, `installation_session.rs`, `project_admission.rs`, `project_chain.rs`, `read_premise.rs`, `trust/initial_platform.rs`, platform `directory_entries.rs` and `directory_open.rs`, `custody/discovery_scan.rs`, `scenario.rs`, `configuration.rs`, and `tools/tests/test_environment_exceptions.py`.

## What to review

The plan refines plan r4 section 1.3 before any walker code exists. Judge:
0. **Round 1.** Is each of B2B3PLAN-1 to B2B3PLAN-5 resolved, in the decisions, in section 3 and in the controls? In particular: dot-entry discard and the complete-path bound; the core's metadata-only early rejection in reference order, with `NotObserved` faulting only at an ACL-dependent check; the seam order (phase 1, resolution and admission, phase 2, release, walk); the FW-01 pin over `configuration.rs` now; and the evidence and record cross-check with its explicit ACL projection. Are NBO-1 and NBO-2 addressed?
1. **Scope.** Does it stay within plan r4 section 1.3 and MB items 12, 13 and 15? Does it leave B2-c, B3-b, J1 and M4 their own?
2. **Facts.** Are section 0's facts accurate? That includes the post-fence holdings, the absent read-path release, the unrecorded upward walk, the unapplied waiver, the listing limits and grammar, `ObservedEntry`'s required ACL, the absent FW-01 pin, and the seam.
3. **The split** into B2-b3a, B2-b3b and B2-b3c.
4. **Each lead decision, LD-B2B3-1 to LD-B2B3-13.** In particular:
   - `DiscoveryRoot` and the read-path release, against MB item 12's "or the read session's equivalent release";
   - the unrepresentable-name refusal and its code;
   - `NotObserved`;
   - depth-first walking with an open ancestor stack;
   - listing costs and the limit mapping;
   - the upward rows and the `vcs` record;
   - the waiver threading;
   - no downward mount rule;
   - the FW-01 pin;
   - the read-path seam for the flag rows;
   - the test trace.
5. **Section 3, the walker,** and its tests. Is the cross-check against `walker_population` sound and sufficient?

## Output

`review.json` must carry `nonBlockingObservations` and the following, with your independently checked values:

```json
{
  "verdict": "ACCEPT",
  "requiredFindings": [],
  "subjectManifestSha256": "e2a4d3d57b91c131ce8ed8b71ecce456685539e0d9db2b0967fff5249990f4b0",
  "b2b3plan1Resolved": true,
  "b2b3plan2Resolved": true,
  "b2b3plan3Resolved": true,
  "b2b3plan4Resolved": true,
  "b2b3plan5Resolved": true,
  "refinesPlanR4Section13": true,
  "factsSection0Accurate": true,
  "splitSound": true,
  "ldB2B3_1Sound": true,
  "ldB2B3_2Sound": true,
  "ldB2B3_3Sound": true,
  "ldB2B3_4Sound": true,
  "ldB2B3_5Sound": true,
  "ldB2B3_6Sound": true,
  "ldB2B3_7Sound": true,
  "ldB2B3_8Sound": true,
  "ldB2B3_9Sound": true,
  "ldB2B3_10Sound": true,
  "ldB2B3_11Sound": true,
  "ldB2B3_12Sound": true,
  "ldB2B3_13Sound": true,
  "walkerSpecSound": true,
  "controlsSufficient": true,
  "codeWritten": false,
  "bindingMade": false,
  "lawChanged": false,
  "productQualification": false
}
```
