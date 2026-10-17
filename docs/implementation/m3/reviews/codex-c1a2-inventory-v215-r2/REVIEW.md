# C1A2 inventory v215 round-2 review

Verdict: **ACCEPT-UNIT**. Inventory candidate assessment: **ACCEPT**. No required findings or non-blocking observations. Product qualification: false.

## Corrected successor identity

The candidate is now at **`docs/implementation/m2/repository-file-inventory.v215.json`**, distinct from the parent **`docs/implementation/m2/repository-file-inventory.v214.json`**. Both the manifest member and `successor.json.candidate.path` name v215. The stage contains no replacement at v214. The architecture's v214 parent retains its exact original bytes.

Round 1 accepted the inventory content but did not catch the incorrect candidate destination. This review checks the corrected path explicitly and binds its verdict to the new subject and record hashes. The candidate's content hash is unchanged from round 1; that earlier verdict is not substituted for this path-corrected assessment.

Independently verified:

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| Subject manifest | 689 | `8cd116fd5d59fdfa395368ef7375263d2841c8d193406d1c4d57611456b0685e` |
| Parent inventory v214, architecture | 721288 | `ae6d27dae65f7e369038c9a5989020aed170ca6fea44e5c3ed27943c8bbf543e` |
| Candidate inventory v215, stage | 725221 | `a2d3fb7d87f484168352dd8a93f8cad843bcfa3d3c42b1cf9f2e8199a7dd140a` |
| Integration source census, stage | 769 | `4f29c30b8464517f3575efb73ab7403edc818e413b1d8a5226c72758fd1d410a` |
| Successor record, stage | 5684 | `f4cdae86f7ec54395eb6e4cfabd3f2cd175e5f6b5118ce102c19f995cc81095a` |

All three manifest members were rehashed successfully. Product main is clean at `41f6cae7c03e975b16db52a9b5f4d015e7468682`; architecture HEAD is `0272078ece3de70e4d6e0bd62712acfccca45609`, as requested.

## Inventory assessment

Independently compared the parent and candidate by value. The candidate is a sorted, unique strict superset: 1,308 file rows versus 1,301, with exactly seven additions and no changed or removed inherited row. All 20 packages, all 9 pending decisions and other inherited top-level values are unchanged. All 1,212 tracked product paths are covered. The 96 inherited paths still absent from product are retained unchanged; their list exactly equals `inheritedPlannedFilesRetained`.

The added rows are accurate:

| Path | Package | Role | Generated |
| --- | --- | --- | --- |
| `crates/host/src/candidate_custody.rs` | opensip-host | service | false |
| `crates/host/src/candidate_custody_tests.rs` | opensip-host | test | false |
| `crates/host/src/snapshot_session_vectors.json` | opensip-host | fixture | true |
| `crates/host/src/snapshot_tests.rs` | opensip-host | test | false |
| `crates/platform/src/custody_entry.rs` | opensip-platform | adapter | false |
| `crates/platform/src/custody_entry_tests.rs` | opensip-platform | test | false |
| `crates/security/src/snapshot_route_tests.rs` | opensip-security | test | false |

The descriptions remain within the accepted library/model unit: candidate custody, charged exclusive rename/unlink primitives, session charge predictions and corresponding tests. Only the added session-vector fixture is generated, by the ledger model's `--write` route. No production caller or qualification is implied. The successor's `addedFiles` exactly matches these additions.

`crates/host/src/snapshot.rs` alone realizes an inherited planned row. Its unchanged description, “Capture exact admitted source/read-set bytes through the selected custody boundary,” remains true of CaptureSession's role. It does not claim C1c read-set determination or J1 composition of B2/C2 reads is implemented. No override is needed. The inherited descriptions of the host/platform API modules, security source and scenario seam, walk vectors and ledger model remain applicable; none is altered by this successor.

## Acceptance pins and census

The accepted code review is independently verified at 185 bytes, SHA-256 `5c65887749dd3921e048d273ee29e5ba884674aeef30f397155a6d66c5a85540`. It says ACCEPT-UNIT and binds the 13,345-byte code subject manifest, independently hashed as `8e9105aecc75b28256553886a4eb5d94f7da57fa043aa906fd175a788ff66498`. All 14 integrated product files match the accepted product-map candidate pins. This checks integration identity without reopening the closed code review.

The source census's product commit, checker and exception pins match live product. Independently ran only the permitted command:

`python3 -I -B tools/check_operability.py source --repository /Users/sb/code/opensip-ai/opensip`

It passed with 114 rows and no findings, matching the staged census. The mint-audit record is unchanged from the product parent and contains 439 rows; the source check includes comparison against the actual lexical mint census. No mint authority is added.

None of the integration's changed paths intersects the discovery census's 19 pinned closure files. Thus this integration introduces no closure change requiring a new blind receipt. The successor's parent/candidate, accepted-review, accepted-subject and integration-census pins are exact. Its realized and retained lists are exact and productQualification remains false.

Lead assent, architecture publication and the separate lock commit re-pointing inherited passages to v215, with fresh verify_design, remain subsequent binding steps. This review accepts the staged successor and does not claim those steps occurred.

## Boundaries

No compiler, Cargo, tests, generator or lane was run. No network, other pane, delegation, private fixture, installation, signing key or held tree was accessed. Neither repository, the stage nor control files were edited. Only the requested REVIEW.md and review.json were written.
