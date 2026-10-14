# Review: SM-U2C-r2

**Verdict: ACCEPT.** SM-U2C-R1-RF-01 and NBO-01 are resolved. No required findings or nonblocking observations.

## Exact subject and preservation

Rehashed subject.json in `/tmp/opensip-implementation/sm-u2c-r2-stage`:11515 bytes, SHA-256 `dce3a18f069db6add330fbb914c97b0b8d2a6ca4b2f121d71cc8ef1203dcda7a`. All **48 members** match declared sizes and hashes.

The retained round-1 subject matches SHA-256 `403af21fa31166ca09d613596a66468f5e0bd9ed2a02a8ca7c5f4c9f8c4ae291`. Its report and audit are preserved byte for byte, as is SM-7 r2 in history. SM-5 results, runner, probe, log, input records and package-manifest index remain byte-identical to round1; every archived SM-5 two-part child retains its original pin. No earlier review was modified.

Read all **1019 evidence archive members** in memory. Each matches its index size/hash and named external original. Archive SHA-256 is `d772629b9ede72d879b5a840450e3d32704edb0be2bda018afe61957b498231f`. Nothing was extracted.

## RF-01: corrected SM-7 shape

The r3 sender carries DependencySourceManifest's set id, manifest digest and entries, then each chunk's set id, package key, path, per-entry chunk index, byte offset and raw bytes, followed by the full seal and accepted echo. The receiver checks the manifest's exact field set and recomputed digest; each chunk header equals the expected current set/package/path/index/offset. Index and offset advance from zero by actual received bytes. Empty, oversized and overrun chunks refuse; file digests, package grouping, duplicate entries, aggregate limits, seal equality and trailing-byte refusal remain checked.

The representation is clearly disclosed: canonical JSON headers plus raw chunk bytes, and manifestSha256 computed over canonical manifest payload with that member omitted. This is expressly a lead representation of NE's self-referential description, rather than an amendment to NE or protocol conformance. The same computed digest appears in the manifest and seal. This resolves the missing-field finding within the requested experimental scope.

The positive control accepts one entry split into two chunks, demonstrating contiguous index/offset progression. Twenty negative controls cover snapshot frame/digest/truncation, dependency content, manifest digest/field omission, wrong chunk set/package/path, index gap, offset mismatch, empty/overrun/oversized chunks, seal counts/digest, duplicate/grouping and trailing bytes. Inspected the constructed cases and retained nonzero-exit logs. The smoke log additionally records valid streams with and without a snapshot. No control or receiver was executed during review.

The first r3 attempt and evidence are retained. Its rerun differs only by removing the stale dependencyManifestBytes assertion; the correct dependencyManifestFrameBytes check remains.

## SM-5 and snapshot consistency

SM-5's repository timed body remains verbatim from the accepted typed probe, ending at mid; dependencies are read and hashed and manifest/set identities computed before end. No-follow regular-file/inode and before/after stat checks remain unchanged. The split is exact: elapsed equals repository part plus dependency part.

Consistency checks against round1 and accepted typed records cover all90 children: empty stderr, recorded success,3 warmups plus7 measured runs, and repository rows/bytes, snapshot/plan digests, descriptor sizes, inventory and exclusions. The unchanged dependency inputs retain the previously checked U-2b manifests and set binding. Each overlay child includes the439-row whole-overlay union under D-3.

SM-7 preserves accepted snapshot sealing, canonical manifest and u32 framing. Rehashed all seven single-entry sealed manifests against accepted transfer records; they match. Both overlay entries carry439 rows and explicitly have no earlier repository-only transfer baseline. The receiver retains the accepted snapshot checks refactored into content(), as disclosed. Dependency keys are drawn from accepted U-2b file-manifest observations in descriptor package order.

## Statistics, bounds and NBO-01

Independently recomputed all SM-5 whole-span and part medians/maxima from raw records and all r3 transfer/receiver statistics from raw child receipts and result samples. They match u2c-audit-r2.json, result aggregates and report rounding. Every one of90 r3 children records digest/header verification and the expected seal echo; stderr is empty. Independently reconstructed dependency manifest payloads from accepted descriptor/package-key/manifests and checked their byte counts, full-frame hashes, disclosed digest computation, entry/byte/chunk totals and seals.

SM-7 median/max pairs in table order (ms) are185.669/191.653,180.126/180.980,307.326/309.429,71.925/73.055,29.186/30.114,38.182/38.633,160.183/161.512,30.967/31.629 and42.269/43.074.

R8 sums reproduce: SM-5 whole229.734/233.766ms, repository27.599/29.414ms, dependency202.303/204.673ms, and SM-7 **73.236/74.703ms**. These remain sums of per-entry medians/maxima, not an unrecorded combined schedule's statistics.

NBO-01 is resolved: the exact repository median differences are +8.399%, +4.855%, +8.113%, +1.817%, +2.286%, -0.196%, +1.765%, -0.814%, +0.164%, relative to each accepted typed workload median. The denominator and descriptive-only standing are explicit. The revised SM-5 audit rows add only this comparison field to their unchanged round1 data.

Bounds remain sourced separately: repository100000 rows,4MiB snapshot descriptor,8GiB; dependency4096 packages,1000000 entries,8GiB; transport64MiB payload and1MiB raw dependency chunks. All recorded populations/frames fit. Dependency descriptor bytes remain informational with no invented bound; dependency entries are reported beside snapshot rows.

## History, scope and boundaries

SM-5 r1, SM-7 r1 and SM-7 r2 remain superseded history with accurate reasons. Recomputed their medians/maxima against the new audit. Round1 report/audit and the failed r3 attempt remain retained. Generated-lock sets stay labelled sizing stand-ins; only Axum's lock is original.

No S-M value, F/T, placeholder fill, source authentication, import admission, protocol conformance, qualification or gate effect is inferred. O7, D3 and D13 remain closed; only L-G1 remains open among L's gates. U-6 report assembly and the other remaining report work are separate.

Live product HEAD remains clean `95279fa8ae086f98bd221cd827f6c0efc156c0c5`; architecture HEAD remains `a49151299650642be278813941c0957e739b3eb7`. Its existing held E2s tree was not read or changed. Only read-only file reading, hashing, parsing, source inspection and Git queries were used. No runner, probe, receiver, image, Cargo, tests, lane, network, other panes or delegation. No private413, installation, signing keys or held-tree contents were read. Neither repository, stage, working directories nor control files were edited. Only this directory's REVIEW.md and review.json were written. Nothing was pushed. Exact lead assent and fresh design verification remain lead work.
