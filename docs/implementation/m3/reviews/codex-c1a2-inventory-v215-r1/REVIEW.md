# C1A2 inventory v215 review

Verdict: **ACCEPT-UNIT**. Inventory candidate assessment: **ACCEPT**. No required findings or non-blocking observations. Product qualification: false.

## Exact subject and acceptance binding

Independently verified the 689-byte subject manifest SHA-256 `c0744a5060e38de7608eb1d90c517a9c18779d5e44d72a7548298fee2c1f3944` and all three members in `/tmp/opensip-implementation/c1a2-inventory-v215/architecture`:

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| Candidate `docs/implementation/m2/repository-file-inventory.v214.json` | 725221 | `a2d3fb7d87f484168352dd8a93f8cad843bcfa3d3c42b1cf9f2e8199a7dd140a` |
| Integration `source-census.json` | 769 | `4f29c30b8464517f3575efb73ab7403edc818e413b1d8a5226c72758fd1d410a` |
| Successor `successor.json` | 5684 | `e1b7167b87c27bc2e0e098fcf23c14147184d18c04e9a6a468123db135df941a` |

The architecture parent inventory remains 721,288 bytes with SHA-256 `ae6d27dae65f7e369038c9a5989020aed170ca6fea44e5c3ed27943c8bbf543e`. Architecture HEAD is `0272078ece3de70e4d6e0bd62712acfccca45609`. Clean product main is `41f6cae7c03e975b16db52a9b5f4d015e7468682`.

The successor's accepted-review pin matches the 185-byte archived `codex-c1a2-r2/review.json`, SHA-256 `5c65887749dd3921e048d273ee29e5ba884674aeef30f397155a6d66c5a85540`. Its verdict is ACCEPT-UNIT and its subject hash matches the independently hashed 13,345-byte code subject manifest, `8e9105aecc75b28256553886a4eb5d94f7da57fa043aa906fd175a788ff66498`. All 14 integrated product files match that accepted package's product-map candidate pins. This verifies integration identity without reopening the code review.

## Inventory assessment

The candidate has 1,308 unique, lexically sorted file rows versus 1,301 parent rows. It is a strict superset with exactly these seven additions:

| Path | Package | Role | Generated |
| --- | --- | --- | --- |
| `crates/host/src/candidate_custody.rs` | opensip-host | service | false |
| `crates/host/src/candidate_custody_tests.rs` | opensip-host | test | false |
| `crates/host/src/snapshot_session_vectors.json` | opensip-host | fixture | true |
| `crates/host/src/snapshot_tests.rs` | opensip-host | test | false |
| `crates/platform/src/custody_entry.rs` | opensip-platform | adapter | false |
| `crates/platform/src/custody_entry_tests.rs` | opensip-platform | test | false |
| `crates/security/src/snapshot_route_tests.rs` | opensip-security | test | false |

Their descriptions accurately identify the accepted preparatory custody service, charged entry primitives, session predictions and native controls. They retain library/no-caller and non-qualification boundaries rather than claiming J1 integration or completed snapshot construction. Only the session-vector addition is generated; the model's `--write` path writes it alongside the inherited walk-vector fixture. This generation route was inspected, not executed.

Every inherited row is equal by value; no description or generated flag was overridden. All 20 packages, all 9 pending decisions and the other top-level values are unchanged. Each tracked product path is covered. The successor's `addedFiles` exactly equals the computed seven-path difference.

`crates/host/src/snapshot.rs` is the one realized planned row. Its unchanged description—“Capture exact admitted source/read-set bytes through the selected custody boundary.”—remains accurate for the accepted CaptureSession role. It does not say C1c's read-set determination or J1's B2/C2 composition is complete. Its existing service role and non-generated flag remain appropriate; no description override is needed.

The inherited public API rows remain applicable to the host/platform module declarations. The security source, scenario seam, generated walk vectors and model descriptions still describe their roles after the accepted additions; the inventory need not enumerate every new helper or model term to remain accurate. All 96 inherited paths still absent from product are retained unchanged, and the successor's `inheritedPlannedFilesRetained` list exactly matches that computed set. Their retention makes no implementation claim.

## Census and scope

The C1a2 integration changes no member of the census's 19-file pinned closure. The discovery census, operability checker and exception record are unchanged from the product parent. The integration census's checker and exception hashes match the live files.

Independently ran the expressly permitted command:

`python3 -I -B tools/check_operability.py source --repository /Users/sb/code/opensip-ai/opensip`

It passed with 114 rows and no findings, exactly matching the integration census. The unchanged exception record contains 439 mint-audit rows; the passing source check also compares that record to the actual lexical census. No mint authority is added by this inventory or census.

The successor's parent, candidate, review, code-subject and integration-census pins are exact. Its added, realized and retained lists are correct, and it explicitly sets productQualification to false. Acceptance is for this staged additive inventory successor. Lead assent, architecture publication, the separate lock binding of inherited passages to v215 and fresh verify_design remain subsequent steps; this review does not claim those steps occurred.

No compiler, Cargo, tests, model generator or lane was run. No network, other pane, delegation, private fixture, installation, signing key or held tree was accessed. Neither repository, the stage nor control files were edited. Only the two requested review artifacts were written.
