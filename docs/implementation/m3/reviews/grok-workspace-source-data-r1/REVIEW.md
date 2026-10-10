# WORKSPACE-SOURCE-DATA-R1

ACCEPT-UNIT. The isolated candidate adds a library-only classifier for supplied opaque package ids under the closed MWS-1 rule. Exact opaque equality is the only join. Complete package and workspace-member populations are validated before any selection receives a label. A workspace member, including a member that another member depends on, is `snapshot-member`. A selected nonmember, including the pinned nonworkspace path package, is `dependency-closure-member`. Supplied selection order and repeated occurrences stay intact. Duplicate and unknown ids refuse, including when the selection list is empty. The labels are unadmitted data. Metadata admission, the used resolve and dependency join, activation, source, profile, custody, and owner admission stay outside this unit. Under the standing effective L, ML5, this acceptance grants no dependent gate.

Subject manifest `docs/implementation/m3/snapshot-plan-c/workspace-source-data-r1-subject.json` is 4064 bytes, SHA-256 `063246b014bce277338eb2afa41bab09d41db084f069d683ffba2658fd52c310`, with one trailing newline. It lists 17 unique members, and every staged member matches its recorded length and SHA-256. The product files stand before `product-map.json`, and the vectors fixture stands before `workspace_source_data.rs`. Live product HEAD `390270ec914ad3e9c020947648e6fa08ec2f206b` is clean. Live architecture HEAD `0f5969b01d88a956ff7b5e4d5d0f552a46a64f1c` matches the recorded architecture base. The only untracked architecture path is `docs/implementation/m3/syntax-e/e2s/`, outside this unit. This review directory and this subject are absent from that architecture head. The isolated worktree `/Users/sb/code/opensip-ai/opensip-workspace-source-data` is at `5d6027aa40739f86057609c73ce24a07ee1c8596`, an ancestor of main. Its status is exactly one modified path and three new paths.

## The four product paths

`crates/host/src/lib.rs` is 4773 bytes, SHA-256 `29b7fe27bff0e78193598cb5914f0d4447b3d752c12f9c438885d352acfc4d0b`, on both main and the worktree base. The candidate is 4917 bytes, SHA-256 `b36533f289f48d8417d965433a2105bdc5572f7e63df0b563c413429c9710870`. The hunk is the four-line private module inclusion, with `#[allow(dead_code)]`, and the staged copy matches the worktree. Three new files are absent from main and from the base, and each staged copy matches the worktree:

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `crates/host/src/workspace_source_data.rs` | 2165 | `c1aee6ed51d5bda376fb9b20b7458669792fae6ce31323adef8fb5ba249d962f` |
| `crates/host/src/workspace_source_data/fixtures/vectors.json` | 3980 | `d473212970d4667f6ed34ff368516b638353ad78903e4aedb9ccfb538ff5a3ad` |
| `crates/host/src/workspace_source_data_tests.rs` | 3545 | `5892afff41aeb7ae544e0f20e76cef24a2775a8e4a1d6d8eb269429c85d8969f` |

`classify_candidates` is `pub(crate)`. `lib.rs` does not re-export it. The function builds the package set and the member set, refuses a duplicate package, a duplicate member, or a member id absent from the packages, and only then labels each selected occurrence. Output order is the supplied selection order. A repeated selected id is kept. There is no PackageId parse, Unicode normalization, name or version comparison, source or null test, package-key test, path-prefix test, default-member input, or resolve-root input. There is no new public route and no owner authorization.

## Bound law and the three observations

The closed MWS-1 contract is `docs/implementation/m3/snapshot-plan-c/native-workspace-owner-selection-r1/CONTRACT.md`, 5084 bytes, SHA-256 `3ff9ef15b71a57f8b898b5c003dfc266a24cbf1cc3b06f2ee8037a9f94a369bd`. Its subject is 5509 bytes, SHA-256 `79aa618934b4f844cb0142caa57d335a944fb7c61d5d47e01fd505ef0ed38e64`. Its review is 543 bytes, SHA-256 `1209aa3cc8f9be967ac38be96def931341a2c244e5a0a62cced8e1211ac41909`. Its assent record is 2251 bytes, SHA-256 `0bf55307527b8fac2334c810d50c560ed9e9862444254a6124799ac2eff951b7`, with `rootSubstantiveAssent` true and an empty unit-finding list. That design unit stays closed.

The vectors are the package ids and `workspace_members` of three pinned synthetic installed Cargo observations, copied in observation order. Every package id is also the selected list, so the vector classifies the supplied rows as data and records no activation. The expected labels match the membership rule.

| Observation | Bytes | SHA-256 | Packages | Members |
| --- | ---: | --- | ---: | ---: |
| `workspace-and-path.stdout` | 6074 | `61d55d9b7db8498847dfc25aad11934308b8547f493d5e4b5c2a2cc5f72d8ef5` | 3 | 2 |
| `equal-tuple-root-one.stdout` | 2017 | `15e9a71ff4817c5e476d34e144772c7e0f4a88a4aeae427e3d66111295a22ad6` | 1 | 1 |
| `equal-tuple-root-two.stdout` | 2017 | `8658dfacb6a5842a55049852b44aff0a320ee720a2aef03edbbdf878b375c450` | 1 | 1 |

In the workspace observation, one workspace member is also a resolve dependency and its label is `snapshot-member`. The nonmember path package is `dependency-closure-member`. Every package source in these three observations is null, and the labels still follow membership, so a null source supplies no membership. The two equal-tuple roots use the same package name and version, each in its own observation, with distinct opaque ids, and each sole member is `snapshot-member`. A caller witness remains unadmitted.

## Tests, census, and the later inventory

The five `#[test]` functions cover the three observations, duplicate and unknown populations with an empty selection, exact opaque path and Unicode identity, package-order independence with retained selected repeats, and a twenty-thousand-row late member plus a late duplicate. The recorded focused run is 5 passed and 0 failed, with the rest of the host library filtered out. The recorded all-targets host Clippy run uses `-D warnings` and exits 0. The three rustfmt logs are empty. The full host library result of 281 passed and 0 failed remains the closed native-corpus unit. This review did not rerun Cargo.

The recorded source check has 113 rows, an empty finding list, and `passed` true. The recorded lock check has an empty found list and `passed` true. `tools/operability/exceptions.json` on main is 83200 bytes, SHA-256 `b5cc19ba3b1f29c14c534deb5d20eb6ab69408c710e8cb35d4c85f94226f3cb0`. The current native schema, admission registry, source map, schema registry, and `native_owner_tests.rs` match the recorded unchanged pins, including `native_owner_tests.rs` at 111742 bytes, SHA-256 `820db2d6547f469793189c4e74455571b1541f7a4c9993e86ce6ca27555daad5`. These checks were not re-run here.

Main `design-lock.json` is 624148 bytes, SHA-256 `8c214ce655bfd2b34ff015d270ee1de43e08562f34fc38b4bb77a7394673c10c`, with 143 inventory successors ending at v183 and 159 contract successors. The worktree lock remains the base lock, 622976 bytes, SHA-256 `da4e7de66aa1ff63cee765a3eeb436f55b051c30ba609e32bf33709a8874c6b6`. No inventory successor is in this subject. Inventory stays 183. An additive inventory 184 can follow only after this code is accepted and present on main, with parent 183, and only when no other bind has taken that generation. That successor needs its own review, the five lock pins, the 103 inheritance rows, and a separate lock commit. `verify_design.py` was not run for this review. Product code and the design lock stay separate commits. Nothing is pushed.

`focusedTestsPassed` is 5. `sourceAdmissionImplemented`, `activationDerived`, `ownerAdmissionImplemented`, and `productQualification` are false. Full MWS, R3, full C2a and C3a, the native worker, full S-M, and effective L stay open.

Required findings: none.
