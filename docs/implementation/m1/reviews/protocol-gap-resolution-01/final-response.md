I've written `resolutions.json` and `resolutions.md` in the task folder, and the JSON parses cleanly. They are a proposal for root review; I changed nothing in the architecture repo. One caveat: the repo has uncommitted edits in other files, including `COORDINATOR-DECISIONS.md`, so my hashes are of the files as they stand today.

Of the 14 gaps, 4 need a design change from an owner, 1 needs only your confirmation of a source, and 9 are already settled by current documents.

## Needs a scoped successor (exact patch text is in both files)
- **TS2-G4, subject-scope commitment (P-1):** delivery.v2 says every coverage key in a stage shares one commitment. The current native-evidence and identity documents give each key its own `scope2` commitment, and keys within a stage differ, so both can't hold. §0 has no row superseding the old rule. The fix keeps `SubjectScopeV1` and `domainCommitment` exactly as they are. The host mints each key's commitment before spawn and the worker just echoes it. No wire change.
- **TS2-G5, `fact-ref` anchors (P-2):** fact identity is always fact2 under major 2, and fact2 anchors can't point at another fact, so a `fact-ref` anchor can never be admitted. The proposal refuses it at admission and leaves the wire vocabulary unchanged. The `source-span` member types are already settled.
- **TS2-G10, `manifestSha256` (P-3):** delivery.v2 contradicts itself here. The field is plain hex over the CBOR entries. I chose that over the domain-prefixed reading because the field's type can't hold a `sha256:` prefix, and the Rust v2 contract states the same plain-hex recipe explicitly.
- **Audit G10, report projection (P-5):** no report projection schema exists anywhere. Envelope4 is closed and has no history, catalog or graph panels, and the owners forbid adding them to it. So report.ts has to stay blocked. I proposed a `report-projection:1` document that references envelope4 for the parity fields and adds optional panels.

## Already settled
- **TS2-G1, byte strings:** the wire stays CBOR bstr. The private carriers are a `ByteString(Vec<u8>)` newtype in Rust and `Uint8Array` in TS, with hex only in JSON vectors.
- **TS2-G3, stageId length:** the 1..255 bound applies to request, result and `dependsOn` ids through `DispatchBindingV1.expectedStageId`.
- **TS2-G12, commitment domains:** the full field-to-domain table is in the files; P-4 is optional wording.
- **The rest (G2, G6, G7, G8, G9, G11):** handled in code as stated in the files, with no design text needed.

## Audit G9, control protocol: the owner exists
The earlier audit missed it. `control-protocol-contract.v2.json` (DR-102, accepted in D-015 and retained by D-372) owns framing and the handshake. `control-completion.schema.v3.json` owns the closed bodies of all 16 control messages and was reviewed with no objection. Control frames are JSON on separate channels, and their version is independent of the provider protocol versions. That schema is reachable only through `architecture-application.v1.json`, not directly as a source45 member, so you need to confirm it as a registry source.

## Code changes
- Register the control schema for `protocol.rs`.
- Handle the settled gaps in the provider protocol code now. The G4, G5 and G10 behaviour waits on P-1, P-2 and P-3.
- Have the host build one subject-scope descriptor per key before spawn.
- Implement control framing and its state machine by hand. The effect messages stay inactive until the security journal work lands.

## Still open
**UQ-1:** the report panel size limits and which record backs the catalog panel. The report inventory requires measured limits and bars reusing the prototype's budgets, so only the workflow/output owner can set them.

Rust major-3 gaps were outside this task.
