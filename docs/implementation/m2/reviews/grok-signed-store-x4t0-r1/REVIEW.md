# Review: signed accepted-store generator X4T-0 r1

Verdict: ACCEPT-UNIT. Inventory v87: ACCEPT.

The product worktree is `/Users/sb/code/opensip-ai/opensip-x4t0` at `99f1c35b50ddd7a3a2724d9acadf9c72f27ce7da`. `product.diff` is `git diff` of that worktree, intent-to-add included: 38882 bytes, sha256 `8aa8cb7e19c356b273a4213c4b9306fe2798f0457877d69454d7a2c54cdbda1b`, three files. The pinned sources match hashes.txt. The real OpenSIP support directory is absent.

Law is X4T r5 items 12 and 13. The generator is `trust/accepted_store_fixture.rs`, included from `root_payload.rs` only inside `#[cfg(test)] mod accepted_store_fixture`. `generate` builds a real P0 publication with `initial_publication::build`, then one retained revision-2 publication. Root, revocation, catalog and payload manifest are signed with the public quorum seeds through the existing test helper. Admissions, history, time evidence, the closure and the operation are stored as records. Events are stored as events. The descriptor is stored as a publication. `state.v1` is the retained capsule.

## Test-only

The module is private and `cfg(test)`. The source-pin test requires the declaration to sit under `#[cfg(test)]` and scans the security crate for any other file that names `accepted_store_fixture`. Replay of that test passed. No release build compiles the constructor.

## Binders

The round trip calls `current_record_bindings::bind`, `publication_events::bind_events` from the P0 roles and event head, `capsule_clock` then `bind_retained_head`, and `capture_p2` on a scratch installation under a supplied fence. The store handed to the binders is the map of the bytes `generate` wrote, looked up by collection and digest. Those functions still admit shapes and check the joins. Replay: 7 passed, 618 filtered out, Rust 1.95.0, `cargo test --locked --offline -p opensip-security --lib`. The cargo target was removed. The workspace suite, clippy, fmt, `check_package_edges` and `verify_scratch` were not replayed.

## X4T r5 accepted.by

Each role that leaves unbootstrapped gets an `EV-PRESENT-PAYLOAD` event in the current descriptor. `accepted.by` is that event's reference, and the event body carries that role and `to: ST-TRUSTED`. A later conditioning event keeps the same `accepted` object, so `by` still names the acceptance event, which remains one of that role's events in the descriptor. The role-state test checks the pointed-at event's role and `to`.

The files X4T-a's `Budget::load` will open are in the collections the typed references name: signed bodies and envelopes in `trust/objects`, admission records, history and time evidence in `trust/records`, the descriptor in `trust/publications/by-predecessor/…`, events in `trust/stores/S/events/<sequence>-<digest>`. Those are the locators `native_record_capture` uses. `capture_p2` and `bind_retained_head` already open the head, the descriptor, the events and the root body and envelope from a written tree.

## Judgment calls

1. The clock-write records unevaluated to evaluated while the capsule phase is retained. Acceptable for X4T-a. Item 6 admits time from the retained clock record. The existing binders accept this store, and the acceptance transition's real phase story belongs to X4B.
2. Acceptance through `EV-PRESENT-PAYLOAD`, closure payload evidence and a clock-write input is acceptable. `bind` and `bind_events` accept those events on the replay.
3. An empty closure `members` array, with the manifest listing the signed documents, is acceptable. The closure's `manifest`, `rootChain`, `catalog` and `revocation` point at those documents, the closed shape admits the empty array, and X4T-a authenticates the heads rather than a manifest-to-members join.
4. Signing only the documents that have envelopes is acceptable. Admission records, history and time evidence have no signature field; they are admitted by their closed shapes. Inventing a signature field would fail that admit.
5. Copying the P0 capsule into `trust/records/` so time evidence's `beforeImage` resolves is acceptable. The retained publication replaces `state.v1`, and the evidence cites the predecessor bytes.
6. Omitting Recovery is acceptable. A recovery role needs a live ceremony batch, and the continuation states this generator is asked to drive (trusted, expired, stale revocation, quorum lost, revoked, unbootstrapped) do not. The P0 creator-only refusal remains `initial_publication`'s output; this generator always emits a retained store with at least one accepted role.
7. v87 provisional on parent v84, to be renumbered at integration, is acceptable. v85 and the reserved v86 are siblings.

## Inventory v87

`repository-file-inventory.v87.json` is 324832 bytes, sha256 `f4240a79718874c8d8e323750b918b11a86ec0b22f7e050f30b53f2472a8d209`. Parent v84 is 322464 bytes, sha256 `99b80dc4eb4790b380223c7eb575f9259f6fac69e0f33922ea7df1ab45653c2b`. The file-row diff against v84 is two added rows and no removed or changed rows: `accepted_store_fixture.rs` (fixture) and `accepted_store_fixture_tests.rs` (test). `root_payload.rs` gains only the `cfg(test)` module, and its existing description stays true. Subject manifest sha256 `edeffef3ca5d894b636038e407236ea4f1e4a70233e968cb26b70d59d8fa54be`.
