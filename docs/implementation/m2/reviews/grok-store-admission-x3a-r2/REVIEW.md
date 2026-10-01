# Review: store admission X3a r2

Verdict: REQUIRED-FINDINGS.

Subject `docs/implementation/m2/store-admission-x3a/PROPOSAL.md` is 12356 bytes, sha256 `ac045ebbe5a6ac2eb5aa5285ba1356055c75a9259dc98ecca74e757ba386bcaa`, matching hashes.txt. `PROPOSAL-r1.md` is the r1 subject: 11034 bytes, sha256 `60288d02aece9f5dfd136c72de17206aa894bc37027904d7c5459bdeb98d2651`. The request names product `fdbedf4`. Live HEAD is `f7acb6d7f8acadcbc0bf81d141f39077d817f043`, the X1a receipt and `design-lock.json`. `installation_admission.rs`, `installation_session.rs` and `installation_routing.rs` are unchanged in that commit. The real OpenSIP support directory is absent. No product cargo.

## RF-2, RF-3 and RF-4

RF-2 is closed. An in-place rewrite fails on `CONFIG.CUSTODY_REFUSED` with the subject `gate_refusal` gives `CustodyRefusal::Changed`. At this HEAD that subject is `required-files-changed` (`installation_routing.rs`). The law says no second subject exists for the same rewrite.

RF-3 is closed. A missing, undecodable or misbound endpoint file, a broken chain, a key mismatch, a duplicate-key disagreement, and a node-law failure of kind `Chain` terminate on `CONFIG.CUSTODY_REFUSED` subject `installation-incomplete`. The colon subjects stay doctor report entries.

RF-4 is closed as a row. A pair `coreClosure` mismatch and a `C.store` mismatch are the incomplete row, as new `IncompleteRefusal` kinds. `NT-TCB-IDENTITY` is rejected. The core that already admitted stays admitted.

## Extending 458c item 12

Extending the doctor list from this law is acceptable. A separate 458c revision is not required.

458c r6 item 12 names six doctor entry subjects on the existing detail `CONFIG.CUSTODY_REFUSED`, and it adds no schema or registry row. The host assembler turns each `InstallationFinding` into that detail with a free-text subject (`Text::try_from`). Item 5 adds exactly two doctor-only subjects, `installation-incomplete:core` and `installation-incomplete:current-store`, each with one fixed remedy in that same form, and it keeps them out of every termination. That is the amendment. X3a-1's refusal mapping is where `IncompleteRefusal` and `InstallationFinding` gain the two kinds and the doctor assembler emits them. "No code or schema changes" here means no new public detail and no schema or registry edit. The K row is unchanged: `STATE.SCHEMA_UNSUPPORTED`, with the class and error code its S12 row fixes.

## RF-1

The comparison is named and the bytes it needs are not. See the finding below.

The header still says X1 r1 is under review. X1 r1 and X1a are accepted. The decisions use the admitted writer, so the stamp is stale and is not a finding.

## Required finding

### RF-1 — The C.store join has no retained decode

Item 1 compares the trust current record's `C.store` (S, G, K) with the admitted triple, and all three fields must be equal. Item 2 retains, from the session's one read, the decoded pair, marker and nodes. It does not retain a decoded trust current record. Admission adds no file read and validates the retained decoded values. At this HEAD both sessions open `trust/stores/S/state.v1` with no byte cap: `required_files` calls `judge(..., None)` and the observation reader calls `member(..., None)`. The file is judged and recorded by identity. Its bytes are not read, so `C.store` is not among the retained values. A record that does not decode is also not one of item 5's structural kinds. The mismatch row has no input.

Failure scenario: `state.v1` is present and private, and its `C.store` differs from the marker and node, or the bytes do not decode. Pair, marker and nodes retain their decoded values. Admission reads nothing more and still grants `SelectedStoreEndpoint`. The F27 endpoint join against `C.store` is skipped. A later unit is forbidden to repeat it.
