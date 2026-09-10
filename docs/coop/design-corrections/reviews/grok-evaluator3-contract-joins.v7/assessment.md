I'll check the isolated v11 schema, current tree-mapping owners, and the S1 paragraph so the reserved-path listing can be bound to existing admission rather than an unbound receipt.Isolated v11 matches the cited pin. Next I’ll read TreeCommitment, identity Blob projection, and any existing `.opensip` or reserved-path owners.The reserved path is lawful on identity `LogicalPath` and v11 `pathRule`. I'll bind the S1 paragraph to that tree path and write the closed receipt, selectors, and controls.**The reserved-path plan is consistent** with existing tree mapping. A receipt without a tree path was not an association owner; this is. S1 is amended to that binding.

## Join (existing owners)

Identity `closure.tree` is **regular files only** (`Blob` `{path, sha256, bytes}`, ordered unique by path, `BLOB_LENGTH`). DR-103 v11 TreeCommitment is `file|dir|symlink` plus mode. Mapping without an identity fork:

| TreeCommitment | identity |
|---|---|
| `type=file` | `{path, sha256: entry.sha256, bytes: entry.length}` + retained blob of that length |
| `type=dir` / `type=symlink` | delivery-only; never followed; RJ-3 keeps symlink targets inside the tree |
| `mode` | stays on the TreeCommitment row; listing is never executed |

`.opensip/detector-compatibility.json` is a lawful **exact** path (not `.`/`..`; identity `LogicalPath` + `ordered()` + v11 `pathRule`). It is not project-host `.opensip/project-id.v1`. Case-fold aliases are not the selector; they cannot coexist with the reserved path (RJ-3).

Generated/repacked adapters already emit that full-tree contract (architecture 02). Omit at pack → no declaration. Generate at pack → include the file in the signed tree **before** the envelope. Inject after sign → length/digest refuse. Archive recompress changes catalog `archiveDigest` only, not `closure2`.

## Semantics

- path absent → no declaration  
- empty `compatibleClosures` → complete declaration  
- present symlink/dir/malformed/digest mismatch → **refuse**, no downgrade  
- tree/path/digest swap → fails closure or delivery; never catalog-digest-only  
- listing is **not** `closure.manifestDigest`  
- protocol/platform stay on `closure2`

## Receipt

```
{closureId, manifestDigest, admissionOrigin, listing}
listing = {state: absent}
         | {state: declared, path, digest, bytes}
admissionOrigin = retained-generation | installed-signed-release | signed-closure-bundle
```

Parse the existing W DetectorManifestV1 only under `declared`. No second schema, no new signature domain, no `signatureVerified`. `host.closures[].trust='admitted'` remains TCB.

## This turn

- S1 paragraph only: `security-and-lifecycle.md` 93971 bytes, `451c0cc7…`  
- `reserved-path-listing-proposal.md` (joins + C-ABSENT…C-TCB)  
- `review.md` / `review.json` verdict `RESERVED_PATH_LISTING_CONSISTENT`  
- W not edited. Official suites not run. Isolated v11 pin `1c0b8868…` verified.
