# Review: SM-U2C-r1

**Verdict: REQUIRED-FINDINGS.** One required finding, SM-U2C-R1-RF-01, on the incomplete NE transport shape. One nonblocking observation concerns the descriptive timing comparison. SM-5, evidence custody, recorded statistics and part bounds otherwise pass.

## Required finding: SM-U2C-R1-RF-01

NE:2876–2879 requires a DependencySourceManifest containing **dependencySourceSetId, manifestSha256 and entries**, followed by DependencySourceChunk objects containing **dependencySourceSetId, packageKey, path, chunkIndex, byteOffset and bytes**, then seal and exact accepted echo.

The r2 sender constructs a manifest with only dependencySourceSetId and entries, then writes raw file content as length-prefixed frames. The receiver explicitly requires the two-key manifest and consumes unlabelled content positionally. A manifest digest appears only in the seal. No chunk association, index or offset fields are sent or checked.

The sequence and content/seal digest checks are useful, but they do not meet the request's NE **order and fields** criterion. The JSON/no-CBOR/no-protocol-conformance disclosure addresses encoding and standing; it does not justify omitted semantic fields or their serialization/checking costs. Hence dependencyPhaseNeOrder=false for the requested full criterion. receiverControlsAdequate=false for that intended shape: existing controls adequately exercise the simplified stream but cannot validate absent fields.

**Required correction:** represent the full NE manifest/chunk/seal fields in a new variant, retain the disclosed JSON encoding if desired, validate manifest digest and set/package/path association plus contiguous chunk indexes/offsets, and add corresponding valid/refusal controls. Preserve current r2 as history and measure the corrected shape. Alternatively classify current timings as simplified-stream information, explicitly disclose omitted fields/costs, remove the NE-shaped/D-2 measurement claim and leave the required shaped series owed. No current observation should be upgraded into protocol conformance.

## Subject, custody and input checks

Rehashed subject.json:8473 bytes, SHA-256 `403af21fa31166ca09d613596a66468f5e0bd9ed2a02a8ca7c5f4c9f8c4ae291`. All **35 members** match declared sizes and hashes. Read all **788 evidence archive members** in memory; each matches its index pin and external working original. Archive SHA-256 is `80161ac82253e94fd6d8e3526f640e15f0a0538ee7a1914ee0eb70132ad2e802`. Nothing was extracted.

All nine staged descriptors are byte-identical to the appropriate accepted U-2b descriptor, including the overlay follow-on. Copied package manifests are byte-identical to accepted manifests and retain their accepted identities. Independently rehashed every cloned dependency file: **39505 file instances**, all matching lengths and SHA-256 values. The package-manifest index pins match its external copies.

Live product HEAD is clean `95279fa8ae086f98bd221cd827f6c0efc156c0c5`; architecture HEAD is `a49151299650642be278813941c0957e739b3eb7`. Architecture's existing held E2s tree was not read or changed.

## SM-5 and repository controls

The probe's timed repository body is verbatim from the accepted typed probe through snapshot2/plan2-equivalent identity construction; the closing mark is renamed mid. Dependency reads and manifest/set identity computation then occur before end. elapsedNanos equals repositoryPartNanos plus dependencyPartNanos in every child. Descriptor/manifest input loading and schema checks remain outside the reported span as disclosed.

Dependency reads use lstat regular-file checks, O_NOFOLLOW/O_CLOEXEC, inode equality and before/after size/time checks; read bytes are checked against accepted manifest lengths/digests. File-manifest and set identities are computed by the referenced model inside the dependency part. The copied inputs retain the accepted package ordering and set binding.

Independently checked all90 r2 children: successful recorded exits, empty stderr,3 warmups and7 measured runs, recorded child niceness10, exact part split and accepted repository shape. Rows, bytes, snapshot/plan digests, descriptor sizes, inventory size/hash and exclusions reproduce accepted typed controls. Each R8 entry uses the439-row whole-overlay union as D-3 requires.

## SM-7 snapshot and receiver

The sender preserves accepted snapshot sealing, canonical manifest, u32 framing and at-most1MiB content chunks. Each of the seven single-entry sealed-manifest hashes matches accepted transfer evidence. The two overlay entries have no earlier repository-only transfer baseline; this is explicitly disclosed, and both carry the whole overlay.

The receiver's snapshot checks are refactored into content(), retaining length/digest validation; they are not claimed verbatim in the report. Package keys for the dependency manifest come from accepted U-2b observations. The simplified dependency stream retains per-file content hashing, aggregate limits, seal equality and trailing-byte refusal, subject to RF-01.

The positive control records success, and nine negative controls record nonzero exits for oversized/truncated frames, snapshot/dependency digest mismatch, seal count/digest mismatch, oversized dependency chunk, duplicate entry and trailing bytes. Their code constructs those cases accurately. No control was executed during review. They validate the simplified stream, not the omitted NE chunk fields.

## Statistics, bounds and history

Independently recomputed all current SM-5 whole/repository/dependency medians and maxima from raw child records, and SM-7 transfer/receiver statistics from raw receipts/results. They match u2c-audit.json, result aggregates and report rounding. Recomputed both retained r1 series' median/max values.

R8 sums match exactly: SM-5 whole-span medians229.734ms/maxima233.766ms; repository27.599/29.414ms; dependency202.303/204.673ms; SM-7 transfer64.800/65.514ms. These are sums of each entry's median and maximum, not statistics of an unrecorded joint schedule.

Bounds are correctly separated: repository100000 rows,4MiB snapshot descriptor,8GiB; dependency4096 packages,1000000 entries,8GiB; transport1MiB chunks and64MiB frame payload. All recorded rows meet them. Dependency descriptor bytes are informational with no invented descriptor-byte bound. Dependency entries are not added to snapshot rows under D-9.

Both r1 series, runners and raw records remain retained and superseded for accurate reasons: SM-5 timed dependencies alone; SM-7 sent descriptor/per-package manifest frames rather than the requested sequence. Current r2 improves the sequence but still needs RF-01's field correction.

**Nonblocking observation SM-U2C-R1-NBO-01:** the report's “within a few percent” repository median comparison is imprecise. Differences relative to accepted typed medians, in table order, are +8.399%, +4.855%, +8.113%, +1.817%, +2.286%, -0.196%, +1.765%, -0.814%, +0.164%. State the exact descriptive range or per-row differences and denominator; no equivalence inference follows.

## Scope and boundaries

Generated-lock sets remain labelled sizing stand-ins; only Axum uses an original lock. These are preliminary measurement inputs, with no filled S-M placeholders, F, T, admission, protocol conformance or qualification. O7, D3 and D13 remain closed; only L-G1 remains open among L's gates. Full S-M, L-G1 and effective L remain false.

Only read-only file reading, hashing, parsing, source inspection and Git queries were used. No runner, audit script, probe, receiver, image, Cargo, tests, lane, network, other panes or delegation. No private413, installation, signing keys or held-tree contents were read. Neither repository, stage, working directories nor control files were edited. Only this directory's REVIEW.md and review.json were written. Nothing was pushed. Lead assent and fresh design verification remain separate work after correction.
