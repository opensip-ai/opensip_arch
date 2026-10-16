# Review request: S10-TSC round 1 (design unit with a product commit: M3-B r8 successor S10, the TypeScript configuration refusal)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-s10-tsc-r1/`).

## Boundaries

- Do not edit either repository, the worktree, the stage or the control files.
- Do not run Cargo, tests, builds, generators or the lane. No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees or any T2 held-out entry.
- Do not use other panes and do not delegate.

Permitted: read-only file reading, hashing, JSON parsing, source reading and Git queries over:
- the product (`/Users/sb/code/opensip-ai/opensip`, clean at `01c73e2d54e037e3e41adc2f5d97df854552921e`: 166 contract successors, inventory v201);
- the candidate worktree (`/Users/sb/code/opensip-ai/opensip-s10tsc`, detached at that commit, with the S10-TSC changes uncommitted);
- the architecture repository (`/Users/sb/code/opensip-ai/opensip_arch`, at `1e701730c47f912c0465d61bb83fdeb5f32fdb47`; the unit's files are untracked there and staged below);
- the work directory (`/tmp/opensip-implementation/s10-tsc`).

You may run these read-only checkers, writing output only inside this review directory:

```
python3 -I -B /tmp/opensip-implementation/s10-tsc-r1-stage/docs/implementation/m3/config-discovery-b/s10-tsc/evidence/check_s10_tsc.py --architecture /Users/sb/code/opensip-ai/opensip_arch --product /Users/sb/code/opensip-ai/opensip-s10tsc --packages /Users/sb/code/opensip-ai/opensip/tools/contracts/python-packages --work <dir under this review directory> --out <file under this review directory>
```

`verify_scratch_s10_tsc.py` writes a scratch directory under the architecture root, so do not run it; its result is `evidence/verify-scratch.json`.

## Subject

- **Stage.** `/tmp/opensip-implementation/s10-tsc-r1-stage`, a copy of the subject members at their architecture paths.
- **Subject manifest.** `docs/implementation/m3/config-discovery-b/s10-tsc-subject.json`: 16686 bytes, SHA-256 `8c9e98470bd0288cf57cd6592dec28539e6f43d72153ecac1009a2cfc0a29e5c`, 72 members. Rehash every member.
- **Record.** `docs/implementation/m3/config-discovery-b/s10-tsc/successor.json`: 19503 bytes, `ed8fecfba90ea9cc0fea70f704d6c16c35d13d68d200a52b34e82b6fe9b9180b`.
- **Unit.** S10-TSC, law M3-B r8's successor S10, a contract successor in B-S9's complete-copy form with B-S10's product materialization. It binds as contract successor 167. It is not design unit B-S10.
- **Product diff.** `git -C /Users/sb/code/opensip-ai/opensip-s10tsc diff` covers 13 files, each copied under `s10-tsc/product/`.

## Authority

- Law M3-B r8 (`docs/implementation/m3/config-discovery-b/PROPOSAL-r8.md`, your `codex-m3b-r8-r3` ACCEPT): item 14a (lines 566-650, especially the refusals and the public termination, 628-641) and the S10 row (line 1038).
- The B2-c plan r2 (`config-discovery-b/b2-c/PLAN-r2.md`), §3 step 4.
- The precedents: B-S9 (`config-discovery-b/b-s9/README.md`, the complete-copy form and selection), B-S10 (`config-discovery-b/b-s10/`, the materialization form), and native-common-materialization-r1 (`native-publication/native-common-materialization-r1/`, enum members appended).
- SD-7 (`docs/implementation/m3/supervisor-d/sd-7/successor.json`), the line-1159 overrides.
- The registry's `aliasRule` (context-free aliases) and native-v2's `remedyKeyingConstraint`.
- `tools/verify_design.py` `contract_successor`, `generation_sources` and `admission_sources` in the product.

## What to review

`README.md` describes the unit. Judge:
1. **S10's four obligations.** Does the unit discharge each one, and only these?
   - The record and its four alias rows.
   - The D9 row.
   - The remedy keyed by the public detail, in the model and its product carrier.
   - The product vocabulary and generated code.
2. **The registry (LD-2).**
   - Are the two parents really the heads of two accepted lines, with disjoint additions and equal shared fields?
   - Is the union the right single selected registry?
   - Is each alias context-free under `aliasRule`?
3. **The model copies (LD-1, LD-3).**
   - Is each copy its effective parent plus exactly the two keyed entries?
   - Is restoring SD-7's line 1159 on the v2 copy right? Is the rustflags chain's loss of it real?
   - Is the remedy (LD-5) a true next step for each of the four internal keys in item 14a's table, before and after C1?
   - Is it kept distinct from `CONFIG.INVALID`'s remedy?
4. **The product.**
   - Is `product/` exactly the worktree's changed files?
   - Does the generation follow from the pinned generator?
   - Do the re-pins (source maps, admission registry, `SOURCE_PINS`, closure, recipe) follow?
   - Is the constant the model string byte for byte, and is its test sufficient?
   - Is LD-4's scope right: no `Observation` row, no instrument alias table, and no materialization of the two M3-line codes?
5. **LD-6 and LD-7.**
   - Does the B2-c0 replay show that B2-c0 is unaffected?
   - Is including the design mirror right, and is its recorded gap exactly the v4-only members?
6. **Checks.**
   - The base/candidate comparison.
   - rustfmt, Clippy and the operability census.
   - The content checker and the five mutations.
   - Do `checks.json` and `content-check.json` agree with a rerun of the content checker?
7. **The record.**
   - Parents are accepted and sorted.
   - There is no override.
   - The candidates cover the subject.
   - The scratch binding passes as successor 167, and the base lock refuses the candidate tree.
   - Is the selection statement in `standing` complete?

## Output

`review.json` must carry `verdict` (`ACCEPT-DESIGN-UNIT` or `REQUIRED-FINDINGS`), `requiredFindings` (array) and `nonBlockingObservations` (array). It must also carry exactly these expected fields, with your independently checked values. Report the actual value, and raise a finding if any differs:

```json
{
  "verdict": "ACCEPT-DESIGN-UNIT",
  "requiredFindings": [],
  "subjectManifestSha256": "8c9e98470bd0288cf57cd6592dec28539e6f43d72153ecac1009a2cfc0a29e5c",
  "dischargesS10": true,
  "registryUnionSound": true,
  "aliasesContextFree": true,
  "modelCopiesExact": true,
  "sd7LineRestoredSound": true,
  "remedyTrueForAllFourKeys": true,
  "remedyKeyedByPublicDetail": true,
  "productCopiesExact": true,
  "generationAndRepinsSound": true,
  "productCarrierExact": true,
  "scopeSound": true,
  "b2c0Unaffected": true,
  "mutationsCaught": 5,
  "bindsAsContractSuccessor167": true,
  "productQualification": false
}
```

The lead then gives its own assent, makes the product code commit and the separate lock commit binding successor 167, and publishes the architecture record. Nothing is pushed.
