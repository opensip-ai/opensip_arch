# Review: store admission X3a r3

Verdict: ACCEPT.

Subject `docs/implementation/m2/store-admission-x3a/PROPOSAL.md` is 13079 bytes, sha256 `9956fd143a4b3f07a66158020dbe71be3c7704118a3f28996e7af513f312ad97`, matching hashes.txt. The diff against `PROPOSAL-r2.md` (12356 bytes, sha256 `ac045ebbe5a6ac2eb5aa5285ba1356055c75a9259dc98ecca74e757ba386bcaa`) is the r3 header, the item 2 retention paragraph, and the item 5 `installation-incomplete:current-store` sentence. Live product HEAD is `f7acb6d7f8acadcbc0bf81d141f39077d817f043`. The proposal still names `fdbedf4`. `installation_routing.rs` still maps `CustodyRefusal::Changed` to `required-files-changed`, and both sessions still open `trust/stores/S/state.v1` with no byte cap. The real OpenSIP support directory is absent. No product cargo.

## RF-1

RF-1 is closed. `RequiredFile` retains the decoded trust current record with the pair, the marker and the nodes. The session reads `trust/stores/S/state.v1` once, through the retained I, charged before the read, and decodes it with the existing trust state decoder. That decoder's `C.store` (S, G, K) is what item 1 compares with the admitted triple. Admission adds no file read. A present `state.v1` that exceeds the cap, does not decode, or whose `C.store` mismatches is kind `CurrentStore`: the incomplete row in a termination (`CONFIG.CUSTODY_REFUSED`, subject `installation-incomplete`) and the doctor entry `installation-incomplete:current-store`. A missing file stays the missing finding. The doctor list remains the two subjects accepted in r2.

## The cap

The cap is the existing decoder's byte bound, 4194304. That is `opensip_identity::MAX_BYTES` (`4 * 1024 * 1024`), the bound `canonical::parse` enforces before it accepts a document. The same number is `retained_metadata_index::CAP` and `work_reader::MAX_RECORD`. `directory_record_capture::read_one` refuses when `metadata.size` is above the cap, before the read. `read_bounded` accepts `max == MAX_RECORD`: EOF before `max + 1` returns the shorter bytes, and filling that ceiling is `Bound`. `Record::parse`'s `131072` argument is `EDGE_CAP`, the edge limit.

A document shorter than that bound that decodes is retained. The failure the law names is exceeding the cap or failing the decode. An empty file fails the decoder, and `capture_current` also treats empty as its cap error, so it is `CurrentStore`. A charge that cannot be reserved stays the budget row: the read is charged before it runs, and a limit failure is `SYSTEM.OUTCOME.ILLEGAL_STATE` / `WORK.BUDGET_EXHAUSTED` / `host-invariant`.

## The trust reader's capture

`ProvisionalInstallationTrust::read_existing` still calls `NativeTrustReadSession::capture`, and that calls `native_current::capture_head`, which reads `state.v1` on the same `InstallationReadFence`. 458c item 8 keeps that capture. This law leaves trust current admission unclaimed. Item 4 moves `installation_lineage`, `installation_records`, `installation_selection` and `ProvisionalStoreMarker::read_existing` onto the retained endpoint. The session read in item 2 is the read admission uses, and admission adds no further read. The trust capture keeps the raw record and the successor census for the later admission.

## Otherwise

Items 1, 3, 4, 6, 7 and 8 stand as accepted in r2. The header still says X1 r1 is under review, and the body still says `fdbedf4`. X1 r1 and X1a are accepted, and the cited routing line is the live one. Those stamps are stale.
