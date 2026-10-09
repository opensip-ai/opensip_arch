# S-M-TYPED-SEALING-THIRTEEN-READSETS-PARTIAL-R1

ACCEPT. Thirteen prepared development read sets have new preliminary sealing measurements: 130 fresh children, three warmups and seven measured runs each, with empty stderr and exit 0. The parent niceness is set to 10 and read back before any child, and every direct child reads back 10. Every inventory is inside 100,000 rows, 4 MiB for the snapshot-equivalent descriptor, and 8 GiB of source bytes. This is a partial measurement. `SM5FigureComplete` stays false, and `⟨SM-5⟩` stays unfilled. Full S-M, L-G1, effective L, and product qualification stay open. The accepted foundation, the SM-6 read-set review, and the L law stay closed.

## Subject

`subject.json` is 132655 bytes, SHA-256 `5627dea33ef1e4a26f5c44534d9d31c203978cb1a2c6c1d6b9a104e66b053caf`, schemaVersion 1, unit `S-M-TYPED-SEALING-THIRTEEN-READSETS-PARTIAL-R1`. It pins 557 sorted unique members, and every hash matches the stage. The archive path `docs/implementation/m3/spikes/s-m-sealing-typed-2026-10-09` is absent at architecture `380fbf906a832236fd3b0914f793c97960cda6d6` (log: “Record preliminary pinned-runtime callback-ready SM3 measurement.”). Product `37581132d8099b8fb4ad9ef8fb2f90ff8b89d02d` is clean (log: “Bind reviewed SD-3 launcher closure and loader design.”). The architecture tree’s only untracked path is `docs/implementation/m3/syntax-e/e2s/`, outside this packet. Product `design-lock.json` remains 615658 bytes, SHA-256 `018dbfe27c1bbba48dedcf88ff6625ce62072b01bfb0fae0aee8c3dc463fc283`, with inventory v179 (`repository-file-inventory.v179.json`), 139 inventory successors, and 155 contract successors. The lock bytes contain no `s-m-sealing-typed` name. The packet labels the host as preliminary lead macOS, withheld from D12. A live `sw_vers` reading on this machine is macOS 27.0.1, build `26A434`.

The five architecture authorities match that tree: L-law `PROPOSAL-r5.md` at 172198 bytes, SHA-256 `f654ee4e9149e62693ebae8177adcc1f3a8a595b745c1e7503e5f279b80e3e88`; `M3-PLAN-r10.md` at 226011 bytes, SHA-256 `ec8c38f8c6ac8d522989ea6226363817a1b77c5b37560e72e2520088601bb964`; `t2-corpus-manifest.draft.json` at 322483 bytes, SHA-256 `c8cc48e1549a05e9d563728fcac776ceca6c2ba63fa2004779385bd2fa4b7578`; the closed foundation review at 377 bytes, SHA-256 `65f2796f80b74d112d878dcd25774e72dc227b4d97018111092559b65a13f4ff`; and the closed SM-6 review at 526 bytes, SHA-256 `0eac2a9b38a58504a8fdb7fa992c5a2626ce57ab4b7cc88cc5d561526346b536`.

The five product authorities match that tree: `design-lock.json` at the bytes and SHA-256 above; `schemas/sources/identity-v3.schema.json` at 198423 bytes, SHA-256 `eb6ec9571f0a14f88139a42184a54d2dfc50042be304174ac23dce90bf3580b0`; the public synthetic replay fixture `crates/host/tests/fixtures/replay-fixtures.json` at 4181278 bytes, SHA-256 `4004eb2a751eb5d55a0dd8170d1ff81545282ca27a863215763e8b7c4393d163`; `tools/quality/corpus.py` at 4839 bytes, SHA-256 `539f158fd07b60d27e776f2137e2f0c9f651db98b2ac8cec742e28ce0b1bb6c7`; and `tools/quality/store.py` at 9504 bytes, SHA-256 `5fd74f14479a3e502dcf763ca3b52094f2da5c5385f28dab50fb7cc18aee0f28`. The fixture pin is the public replay fixture. `~/Library/Application Support/OpenSIP` is absent.

## Read sets

The T2 manifest’s medium development ids are the sorted union of the TypeScript and Rust lists, twelve ids, each with `heldOut` false. The workspace `mr-rs-medium-serde-json` also has `heldOut` false. Its members are `rs-medium-serde` mounted at `rs-medium-serde/` and `rs-medium-serde-json` mounted at `rs-medium-serde-json/`, and both member entries have `heldOut` false. This review checked those flags on the manifest before any source consideration and did not open a corpus tree.

Each single-repository workload retains one `verify` result, and the overlay retains both member results. All fourteen retained `treeDigest` and `contentDigest` values equal the corresponding accepted manifest pins. The overlay input sets `overlayConfigurationNotCaptured` true. Its 439 regular rows are exactly the path-prefixed union of the two member inventories, and its exclusion list is the same prefixed union. No overlay row sits outside those two prefixes, and no root `Cargo.toml` is present. The twelve single-repository inputs use an empty prefix and leave the overlay flag false.

The six JavaScript and TypeScript repository-only inventories match the closed SM-6 review in regular rows, content bytes, canonical inventory bytes, and snapshot-descriptor byte lengths. Express, smithy-typescript, and umami exclude nothing. napi-rs excludes one nonregular entry, powertools-lambda excludes two symlink directories, and Vite excludes five entries. The Rust inventories and the overlay are this packet’s additional prepared sets.

## Framing and samples

`probe.py` walks with `followlinks` false, opens regular files with `O_NOFOLLOW`, and checks the inode across the open and the size, mtime, and ctime across the read. Symlink directories and other nonregular entries are listed and not read. Every retained relative path is within 4096 bytes. Each segment is from 1 to 255 bytes, and no segment is `.` or `..`. The names contain neither a backslash nor a NUL. Rows are unique and sorted by UTF-8 path. The timed span is enumeration, read, SHA-256, canonical inventory, and snapshot/plan-equivalent framing. Registered schema validation runs after `elapsedNanos` is stored.

The snapshot and plan templates are the unique public-fixture preimages for their descriptors. Their recomputed identities are `snapshot2:8d2f4e8682ce2a987325f8d520133864d371d57a0cae78ecdeac00035eaa8b07` and `plan2:0fe15a7b2958b5a9d8843ce9b8028303f18edf8b5d148eac7abd6bc06553fd23`. Both templates validate against `identity-v3` `snapshot` and `plan`. For each workload, the substituted snapshot differs by `sourceInventory` alone, and the substituted plan differs by `snapshotId` alone. The recomputed snapshot and plan identities, canonical inventory length, and descriptor lengths match the retained shape. All thirteen substituted pairs validate. The thirteen snapshot-equivalent ids are distinct from each other and from the template snapshot id. `snapshotPlanIdentitiesAdmitted` stays false: these are equivalent digests around the public synthetic template, and this packet admits none of them.

`run_set.py` calls `os.setpriority(os.PRIO_PROCESS, 0, 10)` and reads back 10 before the lane, the tree verification, and the children. `observedParentNiceness` is 10. Each child is `probe.py` on that workload’s input. The parent reads `getpriority` for the child pid immediately after `Popen` and before `wait4`. All 130 stored `observedChildNiceness` values are 10. The child’s `elapsedNanos` excludes that parent readback. The child environment is a fresh dictionary: `PATH`, `CARGO_HOME`, `TMPDIR` set to the measurement directory, and `HOME`, `LANG`, `LC_ALL`, and `TZ` when already set. The retained directory still exists, mode `0700`, and its parent is the Darwin user temporary directory. The driver holds the ordinary lane for the set and removes it afterward.

Ordinals 0–2 are warmups. For every workload the seven measured samples have the stored median and maximum. Each stderr file is empty, each exit is 0, and `rssBytes` equals `rssNative` with unit `bytes`. Across all 130 children those RSS values run from 37666816 to 44875776. They stay informational. The snapshot-equivalent descriptor is 372 bytes longer than the canonical inventory for every workload, and every plan-equivalent descriptor is 1207 bytes.

| Workload | Rows | Source bytes | Snapshot descriptor bytes | Median ms | Max ms |
| --- | ---: | ---: | ---: | ---: | ---: |
| js-medium-express | 214 | 717115 | 27305 | 6.890541 | 7.077583 |
| poly-medium-napi-rs | 644 | 11675794 | 88420 | 23.218750 | 23.350958 |
| rs-medium-aws-lambda-rust-runtime | 567 | 2446357 | 86122 | 19.475667 | 19.733584 |
| rs-medium-axum | 498 | 1968335 | 71338 | 17.446042 | 17.713125 |
| rs-medium-hyper | 138 | 1447837 | 17039 | 4.719250 | 4.864958 |
| rs-medium-serde | 347 | 1331295 | 50946 | 11.043250 | 11.481250 |
| rs-medium-serde-json | 92 | 737131 | 11578 | 2.948458 | 2.990458 |
| rs-medium-tokio | 883 | 6256646 | 116528 | 27.853375 | 28.274500 |
| ts-medium-powertools-lambda | 1389 | 7818881 | 206175 | 45.720167 | 46.150125 |
| ts-medium-smithy-typescript | 2315 | 11541863 | 381452 | 80.098750 | 80.843958 |
| ts-medium-umami | 2026 | 9083336 | 283572 | 66.081375 | 66.752750 |
| ts-medium-vite | 2836 | 17644692 | 419807 | 102.498958 | 102.926375 |
| mr-rs-medium-serde-json | 439 | 2068426 | 69635 | 13.844417 | 14.332042 |

These medians and maxima match `REPORT.md`. The preserved `prior-unobserved-priority` driver records `nice` 10 and has no parent or child `getpriority` readback. All thirteen of its elapsed lists differ from the current lists, and the median sets are disjoint. The current figures are the new root observations. This review left the probe, the lane, and the corpus trees unexecuted.

## Partial SM-5 scope

L-r5 item 9 defines SM-5 as sealing: enumerate the read set, read and SHA-256 every member, compute the `snapshot2` and `plan2` equivalent digests, and report rows, total bytes, and canonical descriptor bytes against 100,000 rows, a 4 MiB descriptor, and 8 GiB. The unit includes milliseconds. The placeholder is `⟨SM-5⟩`. S-M is a throwaway harness outside the product.

`SM5FigureComplete` stays false. The packet measures these thirteen prepared repository read sets and the prefixed serde/json overlay. It captures no overlay root configuration, includes no dependency-source set, selects no whole-workspace profile, and admits no snapshot or plan identity. `SM5PlaceholderFilled`, `SMComplete`, `LG1Met`, `effectiveL`, and `productQualification` stay false. `snapshotPlanIdentitiesAdmitted`, `dependencySourceSetsIncluded`, `wholeWorkspaceProfileSelected`, and `sourceAdmissionClaimed` stay false. F remains start (SM-1 or SM-3) plus SM-5, SM-7, and SM-9. T remains F plus analysis. This packet computes neither F nor T and selects no budget.

## Disposition

`verify_design.py` was not run. It has to pass before a later lock or publication commit. Archival is architecture-only, after this acceptance, root assent, and the actual design check. This review binds no lock and pushes nothing. Inventory stays 179. Contract successors stay 155. Product code stays unchanged.
