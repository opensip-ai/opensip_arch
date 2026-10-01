REVIEWER review: X3a-1, the selected store endpoint, with inventory v83. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/REVIEWDIR.

Law: `docs/implementation/m2/store-admission-x3a/PROPOSAL.md`. r5 is accepted. It drops the creator as an endpoint producer, and a creator invocation never reaches a store.

## Subject

Pins are in hashes.txt.
- **Product:** the worktree `/Users/sb/code/opensip-ai/opensip-x3a1`, rebased onto 84a8bfd (X10a). Save `git -C <worktree> diff` (new files are intent-to-add) as product.diff, and report its sha256.
- **Arch:** `repository-file-inventory.v83.json` (parent: X10a's v82, selected at 84a8bfd), `store-endpoint-inventory-v83-subject.json` and `store-endpoint-inventory-v83/`. `evidence/verify_scratch.py` appends only v83 in memory, over the real lock that selects v82 and X10b.

## What it does

- **`SelectedStoreEndpoint<'a>`** (new `custody/store_endpoint.rs`). It is borrowed from the fenced session, and its `validate_endpoint` runs in memory and is charged. It checks:
  - the pair names the receipt's core;
  - K is the core's state writer;
  - S is the marker's;
  - the chain runs from (S, G, K) to exactly one root;
  - `C.store` equals the admitted triple.

  The module reads no file, and a source test pins that.
- **Write side.** `OrdinaryWriteAdmission::admit_store_endpoint(self) -> StoreAdmittedWriter`. It validates the endpoint on the gate ledger, then runs the full gate recheck and the receipt recheck. On failure it releases the fence and returns the failure's row. It adds `DurableWriteGate::recheck` and `charged`, and `DurableInstallation` keeps the account.
- **Read side.** `ReadSession::store_endpoint()` validates on the session ledger, then rechecks. Any failure latches the session.
- **Retained files.** `RequiredFile` holds the full `DescriptorMetadata`, and one shared `recheck_files` compares all of it, so an in-place rewrite ends as `required-files-changed`. The gate's step 2 reads the pair, marker, nodes and `state.v1` once and retains the decoded values, and step 5 rechecks the retained samples.
- **`state.v1`.** Read with the trust record's own 4 MiB bound and decoded by its own decoder (`trust::decode_current_store` and `CURRENT_STATE_CAP`).
- **Chain bound.** At most min(G+1, 64) nodes. Reaching the 64-node session limit is the budget row; a chain longer than its own generation allows is a `Chain` finding. Measured on a deep home:
  - gate: 1,612 objects, 27,815 edges, 2.8 MB;
  - session: 3,069 objects, 48,149 edges, 17.3 MB.
- **Rows.**
  - `IncompleteRefusal::Core` and `CurrentStore`, both on the incomplete row.
  - `GateRefusal::StateSchemaUnsupported`, projected as request-rejected, exit 2, `REQUEST.SCHEMA_MAJOR_UNSUPPORTED` / `STATE.SCHEMA_UNSUPPORTED`.
  - Doctor findings `Core` and `CurrentStore`, with subjects `:core` and `:current-store` and fixed remedies.
- **No creator producer.** A test pins that 468c's routing names no endpoint producer.

## Judgment calls: please rule on each

1. The write-side recheck design: `DurableInstallation` keeps the account, the gate is retained, and `recheck` and `charged` are added.
2. The read side records the `Core` finding itself, using the receipt's closure. Non-doctor reads refuse a core-mismatched installation.
3. "K supported" means exactly the core's state writer: Stage1 is 1, Stage2 is 2.
4. One existing test changed: an in-place rewrite of `selection.pair` after open is now refused, per law item 2.
5. `doctor_report.rs` is touched for the two new arms and remedies. It will need a merge with X10a.
6. Several descriptions now omit X3a's additions. Plain rows are deferred to a later description-only successor, and inherited rows to VD1. Is that acceptable?

## Checks

- Workspace: 1170/0, on two runs. Clippy and fmt are clean.
- `check_package_edges --lane host` (v83) passes.
- verify_scratch passes with v83 selected.

## Decide

- Does it implement X3a r4 items 1 to 7 exactly, including the `C.store` join, the retained `state.v1`, one read per session, and the rows?
- Rule on the judgment calls.
- Is v83 right on top of v82?
- Is anything else wrong?

review.json must contain:
- "verdict": `ACCEPT-UNIT` or `REQUIRED-FINDINGS`;
- "requiredFindings";
- "subjectManifestSha256": a single string, the sha256 of store-endpoint-inventory-v83-subject.json;
- "inventoryCandidateAssessment": {verdict, requiredFindings, path, bytes and sha256 of v83, parent (the v82 pin), successorRecord}.

Write REVIEW.md and review.json. Do not commit.
