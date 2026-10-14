# Review: SM-U2B-OVERLAY-ENTRY-r1

**Verdict: ACCEPT.** No required findings or nonblocking observations.

## Subject and repository state

Rehashed subject.json in `/tmp/opensip-implementation/sm-u2b-entry8-r1-stage`:7518 bytes, SHA-256 `e28355e21d33b892f7ce8453a56f4a4d3196b1d0af4bc3b74743508a2c0478a7`. All **31 members** match declared sizes and hashes.

Live product HEAD remains clean `95279fa8ae086f98bd221cd827f6c0efc156c0c5`; architecture HEAD is `fbb8545668049ce8756a4e77b8e42565fbefd718`. Architecture's existing untracked held E2s tree was not read or changed.

## Variant, build and vendor

Compared full accepted and variant producer populations:3130 files each, no additions or omissions, with only src/cargo/util/context/experimental_command_data.rs changed. The staged parent equals the accepted file, which is an exact prefix of the staged and working variant. The sole append adds the ignored overlay metadata entry.

The appended entry reuses accepted values(None, links), the accepted information-query vectors/pin and new_experimental_query_context. It switches the operation to output_metadata, with dependencies included and aarch64-apple-darwin filtering. Its configure call matches the accepted metadata harness's frozen/locked/offline settings. It has no unit compilation or repository/build-script/proc-macro execution path. Compiler information queries remain the accepted query mechanism; they are distinct from compiling workload units. The retained producer-image build itself compiled the harness, as disclosed.

The retained build recipe uses cargo test --no-run --locked --offline with the vendored source replacement and owned lane. Rehashed its image:77046808 bytes, SHA-256 `478e5cfb89bfe2deca22f44829194ffb0667b7c665adc0896a7944e12a2f4d46`. No image was executed for this review.

The initial build log discloses the missing unicode-ident in the eroded /tmp vendor source. LD-WORKDIR-TMP-EROSION records the cleanup cause and requires locked, checksum-verified re-acquisition under the implementation cache. The retained vendor log/index disclose cargo vendor --locked --versioned-dirs and the new location. The producer Cargo.lock remains unchanged as part of the full producer comparison.

The new vendor has exactly the lost tree's **507 directory names**. Rehashed every pinned .cargo-checksum.json, checked each package checksum against the producer lock, and verified all **29550 vendor-file checksums**. Thus the replacement is a checked build-input re-acquisition, not a dependency-version change. The OS cleanup cause is a disclosed lead diagnosis corroborated by the retained build failure, rather than independently reconstructed OS telemetry.

## Controls and overlay

Independently compared both controls to U-2b's accepted harness metadata. Package-id populations match, and **full resolve-node objects match after sorting by id**, including dependency names, kinds/targets, package endpoints and features; resolve roots also match. This is stronger than the runner's endpoint/feature comparison and confirms its actual successful controls. Both controls retain32 packages,27 registry packages.

The target and control-B packet links equal accepted plans8 and7 respectively; control A has none. Each linked Cargo.toml rehashes to its accepted manifest pin. The accepted overlay projection supplies serde, serde_core and serde_derive through sibling path mounts. Target metadata succeeds with38 packages,34 registry packages; the three projected path packages remain in the snapshot rather than the non-path set.

The runner preserves whole-corpus before/after file-pin equality and asserts it before recording results, while using private homes cloned from r117. The overlay projection does not modify corpus manifests or locks. Metadata/run packet pins and staged versus external metadata bytes match. No failed U-2b evidence is upgraded; this successful follow-on resolves the previously pending entry.

## Set and identity

Diffed the audit and set scripts against accepted U-2b sources. Changes are comments and input/output/path names, including reuse of U-2b's pinned bridge; the archive audit and steps5–7 algorithms remain unchanged.

Read all **40 entry8 archive members** in memory; each matches its index pin and external original. Archive SHA-256 is `298b6bf65edc815a90eb96f44c0efeef01d613855ea336bf27939b9ba6907336`. Nothing was extracted.

Independently verified the34 source-package archives against lock checksums, their regular-file audit rows, and all **1490 extracted source-file observations**. Checked all34 manifest identities with the reference model. The set has34 registry packages,1490 files and15723557 bytes.

Using the reference model with product-vendored jsonschema, recomputed the set identity:

`sha256:f9a12b770a726cc66664dafa61cea5e04e052568092ad22839e757a3da60bd4d`

It matches the descriptor observations and summary. The unified-feature identity also reproduces. The reused product bridge matches its accepted build pin, and the unchanged builder enforces reference/bridge equality for set, feature and manifest identities. This validates retained agreement evidence; no bridge was freshly executed.

The generated lock is explicitly labelled a **sizing stand-in** under NE:1264, matching U-2b's limitation. It is not an admitted original-lock product input.

## Scope and boundaries

This completes the pending dependency-source-set record for the ninth Rust entry. It grants no source authentication, import admission or Plan and records no SM-5 or SM-7 value. U-2c measurements remain owed. O7, D3 and D13 stay closed; only L-G1 remains open among L's gates. Full S-M, L-G1, effective L and product qualification remain false.

Only read-only reading, hashing, parsing, source comparison, Git queries and the requested reference-model identity check were used. No Cargo, image, runner, tests, lane, network, panes or delegation. No private413, installation, signing keys or held-tree contents were read. Neither repository, stage, working directories nor control files were edited. Only this directory's REVIEW.md and review.json were written. Nothing was pushed. Exact lead assent and fresh design verification before architecture-only publication remain lead work.
