# B1B-PLAN-r3 with M3-B r5 review

Verdict: **ACCEPT**

Required findings: none. Non-blocking observations: none.

Verified the 1,036-byte subject manifest, SHA-256 `dd375c13ee384d9251bab9e07ca2e77d6cf16c1f2946f20a97921ef9ad4b84c2`, and all four members by byte count and SHA-256:

- M3-B PROPOSAL-r5.md: 110,930 bytes, `0d1c88a60f354181232c9554e3481b986c42fb8a5ee9f08d9ad1df29bb503f5b`.
- PLAN-r1.md: 10,949 bytes, `441547162b42493d89b2adfb5f3138891b842062abdde487db8f2c07ca971f7e`.
- PLAN-r2.md: 15,928 bytes, `bdf6ef03bdbc186361370d03058d8ec07804fa06adcc5ebc1fbc243b851d1cc6`.
- PLAN-r3.md: 17,666 bytes, `47cdb02488b8e44669c1e189358f6f91a6c9709091940de4a77787d382547e93`.

Both historical plans match their prior staged bytes. Product HEAD is the requested clean `c0151bc6b7fdb6db9157124fa068c8be5061f5d4`; architecture HEAD is `93960ed5327615ead9af08845a4bc27ce3409e76`, with no tracked differences.

## Prior findings

Round-2 RF-01 is resolved. The proposed law and plan now distinguish the account-home comparison in `installation_root_native_source_ignores_environment_child` from the three installation-absence probes. The files, enclosing test names and stated uses match the product: `installation_root.rs:787`, `installation_routing_tests.rs:1024`, `ordinary_writer_tests.rs:116` and `read_premise_tests.rs:104`. This review inspected their source only; it did not execute the probes or access those paths.

Round-2 RF-02 is resolved. The CI appearance control uses a custody-valid `.opensip` without `project-id.v1`, proves no local-carrier lookup or refusal attributable to `local.json`, and retains contrasting marker/custody refusals. The environment-equivalence control explicitly stops before tracking. The separate full-path control expects the permitted Git-environment refusal, consistent with `check_environment` running before repository discovery (`git_tracking.rs:321-339,697-718`).

Round-2 NBO-01 is resolved: the revision table correctly reports 17 current call sites, one production and 16 test-only, across 13 test variable names.

All round-1 findings remain resolved at plan level. Explicit charged negative observations and held-fence rechecks cover absent `opensip.json`, absent interactive `.opensip`, and absent `local.json` under its judged parent. The corrected inherited-recheck facts remain accurate. The proposed law correction explicitly supplies the authority for the concrete test exceptions; production retains only the refusal-only Git read. A separate analysis path keeps legacy read-session and write-gate admission non-capturing, with unchanged charges, reads, refusals, rechecks and latching, supported by compatibility controls.

## Law and exception census

Compared r5 against live M3-B r4, SHA-256 `71f185512a5028d7fcf7464dd23484251b2715ea87aacdbf5786f2e294b99e9e`. Only the title, banner, inserted r5 changes block and item 9 Enforcement bullet differ. The remaining byte ranges are identical.

The environment-call census matches the enumerated exceptions exactly at the pinned product base:

| Product location | Calls | Authorized use |
|---|---:|---|
| `git_tracking.rs:345` | 1 | Production refusal-only `vars_os` |
| `commit_matrix_tests.rs:1980,2007,2033,2107` | 4 | X9 test controls |
| `admission_tests.rs:1257,1283,2341,2482` | 4 | RUSTC/CARGO and X8 helper/input |
| `journal_store.rs:1277` | 1 | Retained-path test child |
| `installation_fence.rs:305,311` | 2 | Fence test child controls |
| `installation_root.rs:779,787` | 2 | Root test child and account-home comparison |
| `installation_routing_tests.rs:1024` | 1 | Installation-absence assertion |
| `ordinary_writer_tests.rs:116` | 1 | Installation-absence assertion |
| `read_premise_tests.rs:104` | 1 | Installation-absence assertion |

All 16 existing test calls are confined to test targets or cfg(test) modules. The X8 names resolve to `OPENSIP_X8_HELPER` and `OPENSIP_X8_INPUT`; the journal marker is `OPENSIP_TEST_RETAINED_PATH_130`. The future hostile-environment child marker is separately authorized for that specific test control and is not counted as an existing call. The law does not authorize a general test-code exemption or another production read. Per-crate configuration, audited item-level allowances, exact list/configuration pinning and planted production reads in both crates are sound plan-level enforcement.

## Whole-plan assessment

The plan matches MB:876 and its FW-01, SL:3 and --project gate cells. Section 0 accurately describes the existing selection, registry capture, recheck, private capture and duplicate invocation types. The analysis path retains the judged carrier descriptor, reads without reopening by name, bounds each read to 4 MiB, charges the operation ledger, compares metadata around capture and joins the held-fence recheck. CI never looks up the local carrier.

LD-B1B-1 preserves X2 r9's placement/chain-before-carrier order and separates the carrier phase from registry capture. Configuration resolution and pack admission run between them in the later J1 composition. The refused-project-pack control excludes registry capture, RESERVED rows, leases and journals; legacy wrappers have independent compatibility controls.

LD-B1B-2 uses installation-private custody for optional global capture, positively records and rechecks absence, latches custody failures and creates neither settings nor its parent. The absent-prefix case follows the same positive observation/recheck rule under its existing parent. Global keys remain subject to B1-a's allowlist.

Invocation mode has one type and computes exactly the stdin/stderr terminal conjunction without environment input; production wiring remains with J1. Controls cover capture races, replacements, oversize/wrong-kind/custody refusals, absence appearances, CI isolation, interactive provenance, mode, optional global settings, environment enforcement/equivalence and FW-01 no writes. They are sufficient for this implementation plan; their execution and the resulting code require their own review.

Acceptance covers the exact proposed plan and item-9 law correction. It does not claim code, a binding, J1 wiring, discovery, member carriers, S-OP-5, qualification or project completion.

Only read-only reading, hashing, JSON parsing and Git queries were used. No Cargo, tests, builds, lane or network was run. No private fixture, installation directory, signing keys or held trees were read. Neither repository, the stage, controls nor prior reviews was edited. Only this directory's REVIEW.md and review.json were written.
