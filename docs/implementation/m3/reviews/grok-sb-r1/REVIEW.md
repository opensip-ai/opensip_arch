# S-B / J1 S16 design successor r1

Verdict: ACCEPT-DESIGN-UNIT.

This is the producer-bound public projection owed by accepted M3-C r8 item 5, item 12 and the S-B row, M3-H r3 item 9 / X-H6, and M3-J1 r6 item 5.4c / S16. It adds no code, schema member, bound, Plan identity, or provider authority. FX-CAP-1 is not re-reviewed.

Product HEAD is `2c2016d00dccecafa3f9985ad8e58a52bbcb1cd5` and architecture HEAD is `9f5ecbd4ac84a8ebd8cd1fb00225db292d4663c3`. Both tracked trees are clean. Inventory v166 remains 614780 bytes, sha256 `d1d5e69aeacbef99d33fcfd4f4881c72e8671cda04e036156f1412c17c30926d`. The OpenSIP support directory is absent.

## Projection

Every proven crossing stays `request-rejected`, exit 2, `REQUEST.UNSATISFIABLE`, detail `PROJECT.SCOPE_LIMIT`. Count subjects keep `field:count>limit`, with the observed value and ceiling written as exact decimals. Byte subjects use that same numeric form on an explicitly byte-labelled field. The eleven owner quantities are:

| Refusal | Field | Ceiling | Population |
|---|---|---:|---|
| SnapshotBound | snapshot.sourceInventory | 100000 rows | Complete captured source inventory |
| SnapshotBound | snapshot.descriptorBytes | 4194304 canonical bytes | Full canonical snapshot descriptor |
| SnapshotBound | snapshot.totalFileBytes | 8589934592 content bytes | Entire retained snapshot; smallest applicable bound |
| DependencySetBound | dependency-source-set.packages | 4096 packages | Final admitted, activated, non-path set |
| DependencySetBound | dependency-source-set.files | 1000000 logical files | Sum of committed fileCount on that set |
| DependencySetBound | dependency-source-set.totalBytes | 8589934592 content bytes | Sum of committed totalBytes on that set |
| DependencyAcquisitionBound | dependency-acquisition.sources | 16384 candidates | Full candidate population, before activation |
| DependencyAcquisitionBound | dependency-acquisition.files | 4000000 logical files | Decoded or read candidate regular files, before activation |
| DependencyAcquisitionBound | dependency-acquisition.totalBytes | 34359738368 content bytes | Decoded or read candidate content, before activation |
| Host subject-scope bound | subject-scope.subjects | 100000 subjects | Complete host-derived census, after execution |
| Host subject-scope bound | subject-scope.descriptorBytes | 4194304 canonical bytes | Full canonical subject-scope descriptor, after execution |

These match M3-C r8 item 5 (100,000 rows, 4 MiB canonical descriptor, 8 GiB content), item 12 (4,096 / 1,000,000 / 8 GiB on the final admitted set, and 16,384 / 4,000,000 / 32 GiB before activation), and M3-H r3 item 9 (100,000 subjects and the 4 MiB descriptor). `subject-scope.subjects` keeps H's spelling. `subject-scope.descriptorBytes` is the byte form S-B was left to fix. The labels are public subject coordinates. The identity schema still bounds `source-inventory` and `subject-scope.subjects` at 100,000, `canonical.rs` still has `MAX_BYTES` of 4 MiB, and the Rust provider protocol still has `maxSnapshotTotalFileBytes` 8589934592. Native evidence still states the three dependency-source maxima. No schema bound moves.

The populations stay independent. Acquisition reports the first crossing in canonical order: candidates ascending by UTF-8 `(name, version, sourceId)`, then archive order or ascending logical path, and a simultaneous crossing is sources, then files, then content. Snapshot, final-set, and subject-scope refusals stay their owners' observations. There is no truncation, shard, protocol-threshold shortcut, or decoder-to-set reroute. Per-archive D1–D4 crossings, ledger exhaustion, and adapter scratch stay on their existing routes. Narrowing never drops a required package row or fabricates a census or activation. Malformed inputs and corrupt retained records stay on the schema-first routes. The count or byte subject applies only to a proven owner-computed quantity.

Snapshot, dependency, and acquisition refusals occur before Plan minting and mint no Plan or Run for the refused step. Subject scope refuses after provider execution. This passage does not undo an existing Plan or mint an admitted Run from refused assembly. H/J effect, settlement, and termination composition stay as they are.

## Passages

Subject manifest sha256 `f447180a6e854831a9de56088f758864239eafc89f8a4781e62de46a1d0be7f5` (1641 bytes). All eight members match. Successor `docs/implementation/m3/snapshot-plan-c/s-b-r1/successor.json` is 20839 bytes, sha256 `d57f3bc513b0e066a7e25c2aa4eab782c48127f375a5b9b5ff55bdd6ff3fb5a6`. Its one parent is the selected `docs/v2/contracts/product-v1/native-evidence.md`, 329013 bytes, sha256 `83b99783893bec4bcca76bc043310e1d33305fc41ef85e012fbcb19e5b222ca0`. `passageOverrides` is empty. The two VD2 supersessions name capacity-r2 `9f7de1a2a27414d24834ee41ddbd8fa7017580e70c75a526fa4fa55540c51d16` on that parent at lines 3534 and 4276, in that order. No bound successor already supersedes either selector.

Both before texts are the current FX-CAP-1 after meanings. Both after texts keep those texts as an exact prefix and then add the S-B routes. The NE:4276 addition is the contract text. The preserved prefix still states seven array rules, prospective-Plan order `semanticClosures`, `nativeContextDigests`, `importIds`, the earlier native-context boundary, `requestedCapabilities` 11264, and `nativeContextDigests` 1024. The candidates are the other seven subject members.

The read-only checker was run as named, with `nice -n 10` and `python3.14 -I -B`. Its stdout matches `evidence/checks.json`, 7378 bytes, sha256 `4401ab57a70bc52c6e8db0b7ce2cf6e7133628fbe2bdccd7de06f0f82b7000d3`. It checked nine authority pins, the current passage meanings, the schema and protocol limits, and 33 arithmetic specimens: for each of the eleven ceilings, the values one below, equal, and one above, with only the eleven values above the ceiling marked crossed. Those specimens are text and arithmetic. They are not live consumer boundary or completeness controls. C, H, and J consumers stay separately gated. No producer, provider, or product qualification is claimed.

No required findings.
