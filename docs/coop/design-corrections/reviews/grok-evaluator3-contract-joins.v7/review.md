# Reserved-path listing join — v6 follow-on

**Standing.** Actual Grok security owner. Isolated `evaluator-successor.v1`. W/core/schema not edited. Official suites not run. Not independent acceptance.

**Verdict.** `RESERVED_PATH_LISTING_CONSISTENT`. Root’s reserved-path plan is consistent with existing TreeCommitment → identity Blob file projection. S1 paragraph amended to that binding (unbound receipt replaced).

## Soundness

Identity hashes **files** (`Blob` `{path, sha256, bytes}`; `BLOB_LENGTH`; tree ordered unique by path). v11 TreeCommitment is `file|dir|symlink` plus mode. Mapping without identity fork: `type=file` → Blob with `sha256=entry.sha256`, `bytes=entry.length`; dir/symlink stay delivery-only and are never followed. Mode is not identity; listing is never executed.

`.opensip/detector-compatibility.json` is a lawful exact path (not `.`/`..`; identity `LogicalPath` + `ordered()` + v11 `pathRule`). It is not project-host `.opensip/project-id.v1`.

Generated/repacked adapters already must emit the common packaging tree (architecture 02). Optional listing is one more regular file in the signed tree. Archive recompress is catalog `archiveDigest`, not `closure2`. Post-sign inject fails length/digest join.

## Receipt

`{closureId, manifestDigest, admissionOrigin, listing}` with `listing` = `{state:absent}` | `{state:declared, path, digest, bytes}`. Parse existing W DetectorManifestV1 only under `declared`. Empty `compatibleClosures` = complete. Malformed present refuses. No second schema, no new signature domain, no `signatureVerified`.

## S1

One paragraph, `security-and-lifecycle.md` S1 (93971 bytes, `451c0cc7…`). W not edited; root forwards to W after W v11 finishes.

Full joins/controls: `reserved-path-listing-proposal.md`.
