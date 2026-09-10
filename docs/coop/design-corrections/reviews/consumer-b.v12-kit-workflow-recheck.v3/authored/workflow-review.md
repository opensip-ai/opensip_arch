# Workflow-scope independent review

**Verdict: `WORKFLOW_SCOPE_ADMITS`**

This is a bounded independent kit-only review of **another actor’s** authored workflow snapshot. It is the same fresh origin, not a new origin, and **not** independent acceptance of this reviewer’s own prior authoring. Frozen Run stores were hash-verified only; their `close_run` admission is **unverified**. This is **not** whole-consumer `ACCEPT`.

First actual refusal on the 48 in-scope IDs: **none**.

## Input hashes

| Item | Value |
|---|---|
| Snapshot manifest | `b2e92652443df230f532c7c4eef81110e27ef1be078adbd312bd1c050274f65c` **MATCH** |
| Snapshot files | **PASS 259/259**, 0 undeclared |
| Kit manifest | `ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8` |
| `requirements.json` | `855a1464fee8c3f2565e3374dcb2cbbd8dfd343c047c24ab0923093722a7f495` |
| Independent checker | `probes/workflow_admit.py` `324c8a9115135205be09f17793edf708f3edfa895fe6eac1e221b706759c5f80` |
| Results | `probes/workflow_admit.results.json` `0774b07387105f7df8bccb644551498e733669abbb2fa4dad716ce6b6ca7102b` |

Python: `/tmp/opensip-architecture-review-env/bin/python -I -B`. Source metadata names `/tmp/opensip-design-corrections/consumer-b.v12-team-workflow-corrections.v1/output` — that actor directory was **not** read. Snapshot bytes were not reminted.

## Reproduction

```text
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-kit-workflow-recheck.v3/output/probes/workflow_admit.py
```

Isolated exact copy of consumer helper/scripts after path redirection into this output (snapshot preserved; path-only helper diffs recorded):

```text
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-kit-workflow-recheck.v3/output/isolated-copy/scripts/workflow_correct_test.py
# measured: exit 0; assertions PASS nfail 0
# test source contains raise SystemExit(1) on FAILED (nonzero-on-required-failure is real)
```

The isolated consumer test is **not** the expected-output oracle. Expected identities, query items, atom values, and classification were recomputed from kit recipes in the independent checker.

## 134-ID mapping (outside-scope retained)

| reviewedScope | Count |
|---|---:|
| in-scope workflow correction (this pass, all independently executed) | **48 PASS** |
| standing of consumer continuation (not re-executed here) | 24 |
| historical vector notReached | 23 |
| out-of-scope frozen Run | 24 |
| out-of-scope frozen Run replay | 12 |
| futureQualification | 3 |
| **total** | **134** |

Full rows: `workflow-review.json#/original134`. Copied historical claims are not accepted by copy.

## What was independently executed (all 48, not a 15-item whitelist)

Kit owners used: `repair.schema.json` repair-apply key recipe; `H("workflow.repair-plan"|"workflow.comparison"|"workflow.baseline"|"workflow.mutation-intent", …)`; `query-projection-contract.v3.md` §§1–8; `atom-evaluation-contract.v1.md`; `identity-schemas.v3` languageVersionBinding / body-language-version; native `TypeScriptConfigGraphV1` / `SourceUnitOwnershipV1`; evaluator3 command-envelope / invocation-record / StepTermination; `command-inventory.v3.json`; D9 `classToExitCode`.

Measured independently (not consumer saved flags):

| Family | Result |
|---|---|
| Repair-apply key = raw SHA-256 of `C({operation, projectId, repairPlanId, baseSnapshotId})`, unequal to mutation-intent H | PASS |
| `repairplan2:` / `comparison2:` / `baseline2:` reminted from published H domains; counts = entries | PASS |
| Pivot-only fingerprint: B=false, E0=true, E4=false; classification matches kit first-axis | PASS |
| Scope-only comparison: two retained scope digests unequal; policy digest equal | PASS |
| Three min-resolution levels: exists no-coverage indeterminate; complete coverage no-match false; type level present | PASS |
| Unknown suffix refuses; clones negatives execute firstRefusal; JS body through TS is javascript | PASS |
| Two ownership maps, derived edition 2018, same claimed L0; 2021 map moves L0; ownership stock | PASS |
| Candidate-only `kinds=[]` + `candidateSourcePaths`; hostCapture labeled synthetic | PASS |
| Config graphs stock-inhabit `TypeScriptConfigGraphV1` (synthesized / multi-base / js-shared) | PASS |
| Command envelopes / invocation records stock-inhabit evaluator3 schemas | PASS |
| Invocation disclosure **joined to kit inventory bytes** (count 45, analyze/query steps/formats/parityFields) | PASS |
| Six public termination examples each inhabit `StepTermination` | PASS |
| Graph query: independently projected 3 `calls@resolved-callee` edges; neighbors/path/reach **item bytes equal** claimed; hopCount 1 is the shortest path; `file@enumerated` refuses `QUERY.RELATION_UNSUPPORTED`; cursor `q3.<64hex>.<64hex>.<position>`; `coverageIds` from selected views; human/json/agent **values** (runId, availability, truncated, totalItems=2, nItems=2) match the neighbors response — not format-name presence | PASS |
| `underlyingRunAdmissionUnverified` retained; no `close_run` claimed | PASS |

All 48 IDs: **PASS**. Per-ID selectors and details: `workflow-review.json#/scope48` and `probes/workflow_admit.results.json`.

## Existing-law implementation notes (not refusals of required observables)

These are **not** absent/contradictory kit laws.

1. Consumer `SYNTAX_SUFFIX_TABLE` yields `rust-syntax` for `.rs`; kit dialect table yields `rs`. Required observable is unknown-suffix refusal, which executed.
2. Consumer `rust_body_l0` builds `dialect.edition` as a string; kit `body-language-version` requires integer. The required ownership-stability property still holds on the retained maps. Claimed L0 was not reminted here from a retained span (none in the vector).

Genuinely absent/contradictory laws: **none**.

## Frozen Runs

Five stores match `frozen-run-hashes.json` byte-for-byte (`syntax-code` `2e74a6b2…`, ts `885b8e45…`, rust `67dc12f8…`, syntax-data `1d07e4c8…`, rust-partial `b6c2b240…`). That is **not** Run admission.

## Limitations (not waivers)

1. Frozen Run `close_run` / other-Run replay remain out of scope (Main B12).
2. `ROOT-ADMISSION` of exported frames was not performed.
3. Real host/OS/compiler/crypto is future qualification.
4. 24 standing IDs, 23 historical notReached vectors, 36 frozen Run/replay IDs, and 3 futureQualification IDs keep their outside-scope status.
5. Whole-consumer `ACCEPT` is **not** issued.

Original failed workflow examples remain under `consumer-snapshot/preserved-failures/workflow-review-v2-refused-original/` (not rewritten).
