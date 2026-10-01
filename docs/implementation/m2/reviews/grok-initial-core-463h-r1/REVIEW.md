# 463h r1

ACCEPT. The diff is the code successor of accepted law 463 r9. It retains the admitted catalog pair and each component-manifest pair on `InitialCore`, pairs them by carrier stored digest, and leaves signature, quorum, and role standing for X4B. Judgment calls 1–7 are the narrowest reading. The accessor is enough for X4B r5 items 2 and 4. Skipping inventory v115 is right. No contract successor is needed.

## Subject

Worktree `/Users/sb/code/opensip-ai/opensip-463h` is detached at `97f630a5d0a39cb65f36e55dbb044d99ae792a61`. `git diff` equals the saved `subject.diff` (36018 bytes, sha256 `fde5e5f371481c003e687e5b047742e92f34c313cb16824503dc95fbcf1fd8bf`). The diff modifies `core_authentication.rs`, `initial_core.rs`, and `initial_core_tests.rs`, and adds no file. The lock’s inventory-successor tip is v108 (376570 bytes, sha256 `9c6953f28572f6882bbdc71ae945104e4a4e65e5d7b87cae9cf91318d9eb1f44`). Every hashes.txt pin matches. `~/Library/Application Support/OpenSIP` is absent.

Law pins match the accepted texts: `PROPOSAL-r9.md` (`f47c22c0…8b6f`, 23367 bytes) and X4B `PROPOSAL-r5.md` (`97c2eef3…29a3`, 21552 bytes). The combined acceptance review is `141ade6c…514f`.

## Law

Item 2’s r9 store bullet is implemented in `produce_in`. When item 9 admits a catalog envelope, F10 inserts the catalog body and that envelope. It inserts every `members.manifests` body with the envelope whose stored digest equals that body. `MemberOpener::open` uses the same no-follow exact-name opens, subdirectory memo, core-tree custody judgment, and shared `MAX_MEMBER_BYTES` (16 MiB) budget, and pushes each file as a `HeldFile` with `CoreMember::Member`. `recheck_in` reaches those files through `recheck_held`. The store keys them by `raw_sha256` in the same `MemoryStore`, sharing one `Arc` with the retained documents. A separate allowance covers the pair vector and the two path copies per pair. The insertion set is the anchor record, the inventory and payload pairs, the chain, the revocation, the envelopes, the manifests, and the admitted catalog.

Item 9’s body set is the chain digests, the revocation digest, every manifest digest, and the catalog digest only when some listed envelope’s stored digest equals it. `bodies.len()` must equal that count and `|envelopes|` must equal the set. Each stored digest must remove one body (`BTreeSet::remove`’s bool). A duplicate digest, a second catalog envelope, an extra root envelope, or a manifest with no envelope refuses `BootstrapEnvelopeSet`. Pairing reads `parse_carrier` for the stored digest only. `bootstrap_documents` returns the raw bytes, paths, lengths, and digests. `InitialCore` has no verifier and no permit on these pairs. `core_anchor::capture` still selects only the root chain (line 332) and `revocation` still selects only the revocation path (line 405). Those are the documents item 4 and item 5 already authenticate.

The r9 code successor is that F8, F9, the r9 body set, F10, and the crate-private accessor, plus the test and builder updates below. The diff adds no dependency. A release with neither a catalog envelope nor a component manifest still produces: six bootstrap members, `catalog()` is `None`, and deleting the unopened `catalog.json` still produces.

## Judgment calls

1. **No inventory successor.** No file is added. v115 stays unused. The v108 `core_authentication.rs` and `initial_core_tests.rs` descriptions stay exact. The `initial_core.rs` description still says “(law 463 r3–r8)”, which remains true and is now incomplete. That belongs in the D1 description batch, the same way v108 handled stale descriptions. It is not a required finding.

2. **Byte identity.** After pairing, each retained manifest or admitted catalog body, and the envelope `paired` names for it, must hash to the manifest row’s listed digest, or the release refuses `BootstrapEnvelopeSet` (lines 1022–1035). Chain and revocation members stay on the r8 path: `authenticate` looks them up by row digest. The check compares opened bytes with the listed digest. Signature, quorum, and role standing stay with X4B. The four mutations (`component-0.json`, `component-0.sig.json`, `catalog.json`, `catalog.sig.json`) refuse `BootstrapEnvelopeSet`.

3. **Open order.** Chain, revocation, and every envelope are opened before pairing. Manifest bodies open next, then the catalog body only when admitted. A missing or ill-custodied r9 body therefore refuses at that later open. The unadmitted catalog is never passed to `open`.

4. **Member bound.** F8 counts chain + revocation + manifests + envelopes and omits the catalog body, so the r8 boundary stays put (`BootstrapLocator` above `MAX_MEMBERS` 130). After the bijection, `listed + envelopes.len() <= MAX_MEMBERS` states the bound with the catalog body included only when admitted. Under the bijection the admitted total is `2·|envelopes|` and F8’s count is that total minus one; that count is odd, so it cannot sit on the even cap 130, and any release F8 accepts also meets the stated bound. The test pins the unadmitted boundary: 62 manifests and no catalog envelope are exactly 130 opened members and pass; 63 refuses `BootstrapLocator` only.

5. **Header route.** `retained_metadata_index::Data::build` still loads every `members.envelopes` path and `route_matches` refuses a header role that is not the kind’s route (`Error::Route`), before any signature check. `parse_carrier`’s own comment records that the view authenticates neither body, signer, nor authority. A catalog envelope whose header says `TR-COMPONENT` refuses `Release(Authentication(Core(Budget(Route))))`. The keys test retains a catalog signed by seeds 14 and 15 under a `TR-INDEX` header and a component manifest signed by seeds 11 and 12 under a `TR-COMPONENT` header. X4B’s “signed outside its role” case, correct headers with the wrong keys, remains X4B’s.

6. **A catalog digest that equals another listed body** lands in the set twice, `bodies.len()` falls short of `listed`, and the release refuses `BootstrapEnvelopeSet`. That input is pathological.

7. **The test catalog has `releases: []`.** `recovery_catalog::schema_prefix` allows an empty `releases` array (the cap is 100_000). The body carries `catalogSchema` 1, `snapshotVersion` 1, `issuedAt` `2026-10-01T00:00:00Z`, `expiresAt` `2027-04-01T00:00:00Z`, `rootVersionRequired` equal to the final root version, `revocationVersionRequired` 1, and empty `reservedRootCommands`. X4B r5’s role reverification can use it. A later X4B-a test that needs release rows extends the builder.

## Accessor and builder

`InitialCore::bootstrap_documents` is `pub(crate)` and returns `&BootstrapDocuments`. `catalog()` is `Option<&BootstrapPair>` and `manifests()` is `&[BootstrapPair]` in `members.manifests` order. Each `DocumentBytes` exposes `path`, `raw`, `bytes`, and `sha256`. X4B r5 item 2 can read the catalog pair and each component-manifest pair from that accessor and reverify them. Item 4 can see a missing catalog (`None`) and an empty component list (TR-COMPONENT stays unbootstrapped at acceptance). The accessor grants nothing.

`signed_release` replaces `catalog-placeholder`. The default `Spec` signs one catalog under `INDEX_SIGNER` (`TR-INDEX`, quorum62 seeds 11 and 12, domain `opensip.metadata.catalog.1`) and one component manifest under `COMPONENT_SIGNER` (`TR-COMPONENT`, seeds 14 and 15, domain `opensip.metadata.manifest.1`). The manifest body is manifest268-semantic’s `POS/empty-capabilities` body with `version` set to `1.0.{i}`. `sign` uses the `opensip-public-test-only-quorum62-seed-` prefix. Empty `catalog_signers` lists no catalog envelope. A `None` component signer lists the manifest with no envelope. Every bootstrap file, including the new ones, is an inventory tree row. The only moved pin is the positive opened-file count, `2 + 2 + 6` to `2 + 2 + 10`. `catalog-placeholder` is gone. The r8-shaped case is the “neither” arm: six members, nothing retained, and the produced core passes `recheck`.

## Contract

`EmbeddedBootstrapV1` (`tools/security/inputs/trust-record-schema.json` lines 1490–1508) requires `directory`, `manifest`, and `envelope`, with `additionalProperties: false`. `index_payload_shape` requires `catalog` and `revocation` and allows `manifests` and `envelopes` from zero (`verified_recovery_bundle.rs` lines 113–132). `admitted_payload_paths::admit` classifies the catalog as `Catalog`, each manifests row as `Manifest`, and envelope rows as untyped. `core_anchor.rs` lines 280–287 still require every admitted payload path to be a tree row whose sha256 matches (`bootstrap-member-tree`). The string `bootstrap-envelope-set` occurs in product code only at `installation_routing.rs:190`. No docs registry JSON names it. `core-auth323.ndjson` is unchanged (`3c8fb9a2…e211`, 3839935 bytes). Its reader, `placeholder_fixture_releases_refuse_without_a_signed_revocation`, loads each row’s own `store` and still expects 13 refusals.

## Checks

Replayed on these bytes, with `CARGO_TARGET_DIR` under this review directory, Rust 1.95.0, `cargo test --locked --offline -p opensip-security --lib` filtered to `initial_core` and `placeholder_fixture_releases_refuse_without_a_signed_revocation`: 16 passed, 0 failed (the 15 `initial_core` tests and the golden reader). The target directory was removed afterward.

The lead’s two full workspace runs (1463 passed, 0 failed, 3 ignored), workspace clippy `-D warnings`, `cargo fmt --check`, `check_package_edges --lane host` (19/19 on v108), and the live `verify_design` run were not replayed here. The reported namespace-lease failure was in a gate this diff does not touch.

## Verdict

ACCEPT. `requiredFindings` is empty.
