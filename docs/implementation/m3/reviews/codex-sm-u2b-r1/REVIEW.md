# Review: SM-U2B-DEPENDENCY-SOURCE-SETS-r1

**Verdict: ACCEPT.** No required findings or nonblocking observations.

## Exact subject and boundaries

Rehashed subject.json in `/tmp/opensip-implementation/sm-u2b-r1-stage`:12128 bytes, SHA-256 `e188d752147d33094b6fb55198a389d3e179594977347fd51a6fa9ee9a22264b`. All **48 members** match declared sizes and hashes. The five working pipeline scripts match their staged bytes.

Live product HEAD is clean `95279fa8ae086f98bd221cd827f6c0efc156c0c5`; architecture HEAD is `bbe41c9a35e8d2544144a452d819547416b75407`. Its existing untracked held E2s tree was not read or changed.

Read all **1389 archive members** in memory. Every member matches its index size/hash and named external original. Archive SHA-256 is `630fc2ba5fcaa5b09e8b6181a8a43c242e6db7817c7aa0d2b831f52f85269652`. Nothing was extracted.

Only read-only reads, hashing, parsing, source inspection, Git queries and the expressly permitted reference-model identity computations were used. No Cargo, image, harness, bridge, runner, tests, lane, network, other panes or delegation. No private413 fixture, installation, signing keys or held-tree contents were read. Neither repository, stage, working directory nor control files were edited. Only this directory's REVIEW.md and review.json were written.

## Receipts and accepted harness

Independently checked all nine receipt pins and lock pins. Registry package tuples/checksums equal each lock's crates.io rows; path packages remain excluded from the dependency cache receipt. All archive, index-cache and registry-config source paths resolve under r117 and match its file pins. `/tmp` and `/private/tmp` aliases were normalized through filesystem resolution for this comparison.

Rehashed all **519 distinct locked archives** used by the receipts. Each matches its lock checksum and receipt bytes/hash. Independently decoded every used stock `.cache` input: byte3 format marker, little-endian index version2, Unknown terminated by NUL, then version/JSON-line pairs. Versions and names agree, and the decoded JSONL bytes match the retained output exactly. Every locked version/checksum occurs in its index. No additional cache source is used.

Compared the runner with accepted run_axum_resolved_metadata.py. It generalizes the same receipt checks, private home, packet, environment, priority10, lane custody, harness entry and whole-corpus before/after immutability comparison across entries. The accepted image rehashes to73176200 bytes and SHA-256 `4581616330816ce2d3c95694b218b86a054473ae56431d1daf3816883b256f92`. Retained attempt receipt/stdout/stderr/metadata pins match; the successful eight attempts record unchanged source copies and no generated/updated lock or repository-code execution.

The accepted retained harness source seeds its explicit private home from the receipt, configures frozen/locked/offline operation, includes dependencies and filters metadata to aarch64-apple-darwin. Its projected-values context takes no overlay patches from ordinary config files. No harness was executed for this review.

## Source audit and steps 5–7

The source audit preserves accepted check_axum_dependency_sources.py's archive/member validation and extracted-tree comparison, with entry iteration and honest failed-entry handling. Independently compared every audited package's archive contents, recorded regular-file rows and retained extracted tree. All **38015 file observations across866 package instances** match; `.cargo-ok` remains operational metadata rather than a source-manifest row.

Step5 retains the accepted unique lock-tuple/metadata join, canonical tuple package key, sorted activated-feature population and producer identity. Verified every package key from its canonical tuple and every activated row against the retained metadata node population.

Step6 reconstructs the accepted format faithfully: UTF-8 path-sorted arrays of `{path, contentSha256, byteLength}`, indent2 and final newline. Reconstructed every retained manifest from its source audit; bytes match exactly. Recomputed all866 manifest identities with the reference model. Axum's187 manifests also match the accepted manifests byte for byte.

Step7 retains the accepted descriptor construction: lock/checksum joins, registry-only packages, file identity/count/byte values, acquisition null self-reference fields, tuple sorting and lock identity. Independently reconstructed all eight descriptor byte sequences from the pinned locks and step6 records; all match exactly. The inherited provenanceAssurance field is part of the accepted descriptor representation; this outside-product experiment does not thereby establish source authentication or import admission.

## Identities and Axum control

Loaded the permitted reference model with the product's vendored jsonschema on sys.path, using Python -I -B. Recomputed **all eight set identities and unified-feature identities**, exceeding the requested two-entry spot check, and every file-manifest identity. They match the retained observations and summary.

Axum's descriptor is byte-identical to the accepted retained descriptor, with set identity `sha256:879ff2348eb48e9c3f4559bb39be84c6688c9e69beddeb6ac3c84c29d0c5e4a8`. Its package-key population equals the accepted control, all187 manifests match, and its unified-features object equals the accepted object (accepted identity prefix7dfdb8a1). Counts remain187 registry packages,7338 files and75258910 bytes.

The rebuilt bridge executable rehashes to474032 bytes and SHA-256 `34ba4f5cc57cb501fc157b3e48bdd546d19046e59668134c73a8c7af5fa6c7f7`. Its staged source is byte-identical to accepted hash_bridge.rs, matching source SHA-256 `cc202447ac2a61ae3af2bbf6a652764f93d2932365270cd38d68b7a45afd4b0d`; its Cargo.lock matches the build record. The retained build log records the current product opensip-identity release build. Inspected the builder's mandatory reference/bridge equality assertions for unified features, manifests and sets and the resulting pinned observations. Independent reference recomputation corroborates those recorded identities and the Axum control. These checks validate retained bridge reproduction evidence; the bridge was not freshly executed.

## Decisions, pending entry and scope

The eight built descriptors remain accurately labelled: Axum uses its original lock; the seven other entry records use generated experimental locks as **sizing stand-ins**. The report explicitly states that a product run with the missing original lock would refuse under NE:1264, rather than treating generation as admission.

Resolver bases match inspected workload manifests: explicit workspace resolver2 for Axum, Napi, Serde, Tokio and the Serde overlay entry; workspace resolver3 for Lambda; edition2021 default2 for Hyper and Serde JSON. Per-entry overlay sets follow D-3. The Serde overlay entry has the same set as ordinary Serde, as recorded.

Entry8 remains pending, with no built descriptor or claimed identity. Both retained attempts report serde_core unavailable and exit101; retry config/stdout/stderr/receipt pins match. The private config text supplies the disclosed sibling patches, while the accepted harness does not consume that configuration. The report correctly leaves a projected-overlay harness variant owed before entry8's U-2c series.

Exactly **8 sets are built**, with no source authentication, import admission, Plan, SM-5 value or SM-7 value. U-2c measurements and the pending overlay work remain separate. O7, D3 and D13 stay closed; only L-G1 remains open among L's gates. Full S-M, L-G1, effective L and qualification remain false. Native admission is not an additional gate on this outside-product experiment. Exact lead assent and fresh design verification before architecture-only publication remain lead work. Nothing was pushed.
