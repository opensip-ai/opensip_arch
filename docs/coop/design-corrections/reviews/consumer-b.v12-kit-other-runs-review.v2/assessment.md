I’ll continue this same kit-only origin and recheck all four corrected Run stores from the v2 snapshot, with full admission and replay rather than only the previous first refusals.I'll continue the same kit-only other-four-Run origin, verify the v2 snapshot, then independently recheck the four new Run stores against original laws.Snapshot SHA matches; I'll verify all 343 files and inventory the four new stores plus the kit contracts.Custody is 343/343. Next I’ll load the previous checker, original properties, and identity/execution/composition laws, then redirect the checker into v2.I’ll copy the checker into v2 with redirected paths, then read remaining admission, proof, and original-property contracts in parallel.Checker is redirected. Next I’ll load `admit_one`, original property observables, and the laws that must be upgraded for first-refusal, whole-Run tamper, and the Rust pair vector.I’ll read the remaining contracts and tamper/evidence schemas, then upgrade first-refusal handling, whole-Run remint, and the Rust pair vector.I’ll upgrade nested snapshot joins, strict first-refusal handling, and whole-Run remint admission, then run the four new stores.I’ll rewrite the four-Run reviewer for the v2 snapshot, original property map, independent Rust pair vector, and strict reached-boundary reporting.TS and Rust admitted; syntax-data and rust-partial failed semantic proof compare. I’ll inspect field diffs so a checker bug is not treated as a consumer refusal.Proof mismatch is only `executionDeficiencies`. I’ll compare claimed vs independently derived records against the composition schema before treating that as a consumer refusal.The proof mismatch was a checker rewrite of native causes to `required-cell-unsatisfied`. I’ll retain the originating typed pair and re-run.All four graphs admitted. I’ll audit original properties, tamper admission, v1 first-refusal corrections, and the written review before locking the verdict.**Verdict: `OTHER_RUNS_REFUSED`**

Same kit-only four-Run origin, foundation retained and not re-opened. This is not whole-consumer ACCEPT.

Wrote only `/tmp/opensip-design-corrections/consumer-b.v12-kit-other-runs-review.v2/output/other-runs-review.md` and `.json`. Checker paths were redirected before execution (kit stayed the original 80 files).

## Custody

| Object | SHA-256 | Result |
|---|---|---|
| kit `consumer-input-manifest.json` | `ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8` | PASS 80/80 |
| parent frozen SHA | `a70f5830c9d54f5a6bc3285cb05c34fb6331d5278ae1c46e12147a5f95a10bbb` | match |
| `requirements.json` | `855a1464fee8c3f2565e3374dcb2cbbd8dfd343c047c24ab0923093722a7f495` | match |
| this snapshot-manifest | `feb08879bff5dd7313e471f33cad161389371600ea472cb05169d187faed006c` | PASS 343/343 |

Reproduce:

```bash
/tmp/opensip-architecture-review-env/bin/python -I -B /tmp/opensip-design-corrections/consumer-b.v12-kit-other-runs-review.v2/output/independent/review_four.py
```

## Graph admission and replay

All four **NEW** stores admitted at raw/schema/structural/fullsemantic. First refusal: none. Expected proofs were reconstructed from selected inputs (not copied claimed fields). Proof C and proof identity matched on each graph.

| Run | Store SHA-256 | Run / Plan / Proof | Claimed / derived | Layers |
|---|---|---|---|---|
| ts | `ca1b44df3f89bc6d6cc63edfe239ce510a60c7fc47f2d531c5bcb10385b99086` | `run3:9fb05cf2…` / `plan2:9a6654ad…` / `proof3:6969b09b…` | pass / pass | all PASS |
| rust | `3b4daf1caa81f11cbaa255feede860c27fc81dd27b92e1f31cb9de634570d791` | `run3:db635639…` / `plan2:25d8e4df…` / `proof3:8c329c54…` | pass / pass | all PASS |
| syntax-data | `00fce98f9683084563b1bf54e1119813fc97d670250e49fd7d56ad5fe57e5099` | `run3:4ec370fb…` / `plan2:09e25c1e…` / `proof3:d0d5b5f1…` | indeterminate / indeterminate | all PASS |
| rust-partial | `89fd6accbc6181217e6605fbc6b4a058520b7ae8ce0cda3523f4a0a86b1a004c` | `run3:4852e398…` / `plan2:1539822b…` / `proof3:94063605…` | indeterminate / indeterminate | all PASS |

Whole-Run tamper was the remint of proof+evidence+seal+run, then admission of that replacement, then semantic refusal. Stale-hash C-inequality was a separate control. Distinct foreign proof IDs were not used as that execution.

## Existing-law corrections vs remaining miss

v1 first refusals were rechecked on these NEW graphs and did not recur:

- TS import payload inhabits `RuntimePayloadV1` (`istanbul-json`)
- Rust `crateRootPaths` is inventoried `#/a/Cargo.toml`
- toolchain tree member length joins
- sealed Rust selection is one edition; same-file two-editions is the pair vector, not `BODY_LANGUAGE_OWNER_AMBIGUOUS`
- syntax-data clones account is `supported-available`; Coverage unknown + `language-tier-unsupported`/`capability-missing`; required cell partial; seal indeterminate
- rust-partial required partial cell produces native `executionDeficiencies` and sealed indeterminate
- `evaluationInputRefs` = selectedRefs + execution-inputs only

**Remaining original accept-blocking miss (why the four-Run verdict is REFUSED):** `R-RUN-CLONES-L0-AND-NORMALIZED` and therefore `R-RUN-CLONES-CUSTODY`. TS and Rust retain only `normalisationLevel=L0-verbatim` clones facts. Resolution `normalized-body-hash` is the clones ladder rung, not a second normalisation-level fact with a retained frame. Syntax-code is frozen/outside this recheck and was not used as a waiver.

Rust pair property used the explicit pair vector (`runs/rust.body-identity-pair.json`) with independently derived L0/ownership identities. Two complete sealed graphs were not required.

Foundation/pilot/workflows/syntax-code were not this recheck. No product/real host/compiler/crypto. Consumer helper PASS was not an oracle.
