# Review: native current-trust admission X4T r5

Verdict: ACCEPT.

Subject `docs/implementation/m2/trust-admission-x4t/PROPOSAL.md` is 34497 bytes, sha256 `dc5393e6582565cc0eb13d482fb84e2f23639bb3f24389f1656cd4814529e6be`, matching hashes.txt. Preserved r4 is 31454 bytes, sha256 `f6a9a27bf6d1f998606c54373f84d456b8266404f109abf03de1e5cda7a7fe50`. Preserved r3 is 24820 bytes, sha256 `8831dedb2fa59e486ac701b4ac27831d6a4928c4c288c935f0542ab22db84958`. Preserved r2 is 24424 bytes, sha256 `d4c30645b79b2a58577b63f07effbbd93f3996a12fe1abb62f8f5c793ce3437a`. Preserved r1 is 17029 bytes, sha256 `131c59273fd48670c7174f4e33c8e43d8dc6d949fab92f3453c249dcf60baf91`. The live product HEAD is `8bfc78a741158e961f727dd44f481549ec09225d`. The real OpenSIP support directory is absent. No product cargo.

The diff against r4 is the header, item 1's checks and openers, item 2's order, item 4's revocation opener, item 12's closure bullet, item 13's generator and round-trip, and the X4 note. `TRUST_VIEW_COST` stays 128 objects, 2048 edges and 112 MiB. The doubled ledger stays 256 objects, 4096 edges and 224 MiB. The 32-event list bound, the 40 MiB closure total, the `ChainBudget` row and the F-absent row are unchanged.

## r4 RF-1

Closed. At `8bfc78a` the named functions do what item 1 now says.

`native_current::capture_p2` loads `state.v1` and the publication descriptor (`Budget::load_at` on `Collection::Publications`), then calls `current_record_bindings::bind`. `bind` admits the inline `clock.record` through `clock::admit` and loads the descriptor's events through `current_event_trace::bind_trace`. It does not open `history` or `timeEvidence`. `bind_trace` requires `eventHead` to equal the last listed event. Neither `bind_trace` nor `publication_events::bind_events` reads `accepted.by`. `check_capsule_projection` requires `accepted` non-null for `ST-TRUSTED` and `ST-REVOKED` and checks the head-counter identity.

`trust_ordinary_roots::bind_retained_head` loads `heads.root`'s body and envelope with `Budget::load(Collection::Objects, …)` and keeps the root admission as a reference. No existing binder opens the root admission record, `heads.catalog` (body, envelope, admission), `heads.revocation` (body, envelope, admission), `history` or `timeEvidence`. Item 1 assigns those opens to X4T-a, through the same `retained_metadata_index::Budget::load` (`load_at` where the reference is a native event or publication reference). Signed bodies and envelopes are `Collection::Objects`. Admission records, `history` and `timeEvidence` are node references, and the closed shapes name `Collection::Records` for them (`RootAdmissionNodeV1`, `MetadataAdmissionNodeV1`, `RevocationHistoryNodeV1`, `TimeEvidenceV1`). `Budget::load` takes that collection from the caller. Item 2 steps 3 and 4 name those loaders. After step 2, X4T-a checks `accepted.by` against the events `bind_trace` loaded, for that role. An event body carries `role`, so a reference to another role's event is a check X4T-a can perform. A reference outside that chain refuses and does not walk `history`.

`admitted_revocations::verify_revocation` verifies the body bytes and envelope value it is given. Item 4 has X4T-a open `heads.revocation` and pass that load's body and envelope to it.

Items 12 and 13 use the same split: X4T-a's members are opened by `Budget::load`, and the existing binders remain the parsers of the records they already admit. The round-trip requires `capture_p2`, `bind`, `bind_trace`, `bind_retained_head`, X4T-a's loads and `accepted.by` check, and `publication_events::bind_events` as an additional acceptor. The X4 note's point 2 follows item 2.

## Held from r3

A recorded root chain past `ChainBudget { max_links: 16, max_stored_bytes: 16 MiB }` stays on `WORK.BUDGET_EXHAUSTED`, operational-failed, exit 4, `SYSTEM.OUTCOME.ILLEGAL_STATE`, fault cause `host-invariant`, and the chain is never truncated.
