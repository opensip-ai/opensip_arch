# Staged design-lock extension (description only)

This describes a future product lock change. It is not a lock, a review or an
assent. Do not apply it until an actual independent review and root assent exist
for this unit. Every `<...>` value below is a placeholder, not a fabricated pin.

## Preconditions

1. Root freezes this closure (`subject-files.json`) and an independent reviewer
   accepts it. The review must be a separate architecture file with:
   - `verdict: "ACCEPT-DESIGN-UNIT"` and `requiredFindings: []`;
   - `subjectManifestSha256` equal to the SHA-256 of `selection-subject.json`.
     The v4 verifier binds that two-file selection subject. The reviewer may also
     record the whole-closure manifest digest in an extra field.
2. Root writes a separate assent with `status: "ACCEPTED-DESIGN-UNIT"`,
   `rootSubstantiveAssent: true` and `requiredUnitFindings: []`. It also pins, each
   as exact `path`, `sha256` and `bytes`:
   - `subjectManifest`: the selection subject;
   - `actualClaudeReview`: the actual review;
   - `acceptedSuccessor`: `successor.json`.
3. Both staged files are placed byte-identical in the architecture checkout:
   - `docs/implementation/m1/control-source-v1/successor.json`
   - `docs/implementation/m1/control-source-v1/selection-subject.json`

   The candidate stays at its existing path,
   `docs/coop/completion/control-completion.schema.v3.json`. It is not copied,
   renamed or given a new ID.

## The only lock change

Append one element to `contractSuccessors`, after the existing metadata-v2
element:

```json
{
  "record": {
    "path": "docs/implementation/m1/control-source-v1/successor.json",
    "sha256": "<sha256 of successor.json>",
    "bytes": <bytes of successor.json>
  },
  "subjectManifest": {
    "path": "docs/implementation/m1/control-source-v1/selection-subject.json",
    "sha256": "<sha256 of selection-subject.json>",
    "bytes": <bytes of selection-subject.json>
  },
  "review": {
    "path": "<actual independent review path>",
    "sha256": "<actual review sha256>",
    "bytes": <actual review bytes>
  },
  "assent": {
    "path": "<actual root assent path>",
    "sha256": "<actual assent sha256>",
    "bytes": <actual assent bytes>
  }
}
```

Everything else stays unchanged:

- `schemaVersion` 4, `approvals`, `inputs`, `inventorySuccessors` and the existing
  metadata-v2 contract element;
- `inventoryPassageInheritance: []`;
- `tools/verify_design.py` and its tests;
- the schema, the architecture application, review5, freeze5 and all prior
  acceptance records.

## Expected v4 effect

- The appended unit has one parent: `architecture-application.v1.json`. It is
  selected by source45 and not overridden by application46.
- It has one candidate, the existing schema3 path, and no passage overrides.
  `successor_chain` accepts it because the schema path is not already accepted.
- With `--implementation`, the accepted source set becomes the effective overlay
  plus both contract units. The control source row then passes, and the exact
  refusal `generation source is not selected by accepted design` no longer
  occurs for it.
- Generator options, the executable closure, output drift, CA2 to CA5, native and
  report owners, and control semantics remain separate obligations.

## Verification once actual files exist

From this closure, with `TMPDIR` set outside it:

```
python3 -B check_bridge.py --architecture <opensip_arch> \
  --review <actual review path> --assent <actual assent path>
```

This first runs every historical join. It then runs the snapshotted accepted
verifier over the live lock plus the binding, including the source preflight,
and refuses synthetic fixtures. After integration, also run the product's own
`tools/verify_design.py --architecture <opensip_arch> --implementation <tree>`.
