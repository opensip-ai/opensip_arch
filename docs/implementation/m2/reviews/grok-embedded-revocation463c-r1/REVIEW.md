# Review: embedded revocation 463c code r1

Grok is the single reviewer. Claude Opus 5.5 leads. Code review of the uncommitted embedded-release authentication. No repository edits.

Product HEAD `bf49fcb29c8249e4b9604f16e0c50b3ca996ce4d`. The two files match `hashes.txt`. `core_anchor.rs` is 20248 bytes, sha256 `b6f52d1c91db9bc6389ca9437ea0a2e2ac59c932520f4e920ab93e7abc6705e4`. `core_authentication.rs` is 30230 bytes, sha256 `e075a571213e406c1d346f015062a8073da6b2d1260bfe3cc844433d87a5e833`. No file is added. Law is 463 r6 items 4 and 5. The live proposal is that text plus the r6 acceptance stamp (14264 bytes, sha256 `1db9ca07b3f433b4a876e3e1ba1cc8d6b3419bf588d8ca761eae1794d877b730`). Rustc `1.95.0` (`59807616e`). `cargo --locked --offline`.

## Verdict

**ACCEPT-UNIT.**

## Answers

Items 4 and 5 are implemented in that order, and nothing is returned before the last re-filter. `authenticate_embedded_release` takes no revoked set. It calls `authenticate` with an empty set. The final root is the last chain link, or the anchor when there is no link. `verify_revocation` runs under that root with an empty previously-revoked set, so the document's `rootVersion` must be the final root's version. The revoked set is then the `keyId` subjects only. The inventory envelope is verified under the final root as `EnvelopeKind::Inventory` (TR-CORE) and the bootstrap manifest envelope as `EnvelopeKind::Payload` (TR-BUNDLE), each from `initial()`, then `filter_envelope_revoked`. After that, `filtered_again` must be `Met` for every link's continuity and possession, then the revocation quorum, then TR-CORE, then TR-BUNDLE. A failure returns `ReleaseError` and there is no fallback. `authenticate` and `capture` are unchanged. `revocation` rebuilds the manifest index on the anchor platform's embedded tree and selects `members.revocation.path`; the index pairs the envelope from `members.envelopes`, and the bytes come from the store.

Reading "every chain link's quorum" as continuity and possession is correct. `RootLinkEvidence` has those two reports and no other quorum. `links()` is the successors after the index-0 anchor. The anchor root is the chain's starting body. Law 229 makes the anchor prove which bytes are index 0, and that proof is not a signature quorum. `capture` still checks the index-0 carrier subject. There is no link quorum on that envelope to re-filter.

Non-key revocation entries need a law decision, not a finding against this code. The list shape admits `keyId`, `namespace`, `release`, and `catalogSnapshot`. Items 4 and 5 re-filter quorums, and a quorum is a set of keys, so only `keyId` entries belong in that set. `verify_revocation` still checks the whole document. `observe_revocation` is the existing predicate that matches `release`, `namespace`, and `catalogSnapshot` against a caller-supplied closure, and only when the list's version is above the operation's start epoch. That predicate says the verified document is not yet a current revocation view: it still needs admitted time, counters, and root custody. Items 4 and 5 do not say the pre-installation producer refuses when the list names this closure or a catalog snapshot. Whether InitialCore must do that, before those owners exist, is a decision for the law, not a hole in this quorum order.

The synthetic release is a sound test of the real path. It calls `authenticate_embedded_release` with documents signed from the public quorum62 seeds. The positive cases are a two-root chain with non-critical keys revoked, a single root with an empty list, and a single root revoking one of its own root keys. The refusals are self-revocation of the revocation signers (`Quorum(Revocation)`), final-root keys and root-0 continuity (`Quorum(Root)`), TR-CORE (`Quorum(Inventory)`), and TR-BUNDLE (`Quorum(Payload)`), plus a missing member and a list at the wrong root version. All 13 accepted core-auth323 rows refuse `RevocationMember`. The inner `authenticate` with an empty set still succeeds on the cases whose later re-filter refuses, which is the no-fallback check.

Untested, and not defects of the path that is tested: an unlisted or ambiguous revocation envelope, the `Envelope(kind)` carrier errors, `KeySubject`, a schema-2 root, budget counters, and a real signed tree. The last is 463g.

## Replay

- `cargo test --locked --offline -p opensip-security --lib`: exit 101. 458 passed, 1 failed, 2 ignored. The failure is `native_session_census_shares_current_budget_and_distinguishes_missing_from_empty`: `ChangedDuringRead` on a live installation descriptor. The four 463c tests passed. A rerun of that one census test passed.
- `cargo clippy --locked --offline --workspace --all-targets -- -D warnings`: exit 0.
- `cargo fmt --all -- --check`: exit 0.

Do not commit.
