Grok review: law X4T r10 (native current-trust admission), an amendment from your X4B-a r1 judgment call 12. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-trust-admission-x4t-r10.

Subject: `/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/trust-admission-x4t/PROPOSAL.md`, r10, 53028 bytes, sha256 3484dc5d966ffd41cc6c8f50d2caab29fa3bf8cd3cc3eba322038fdd016b30a8. r9 (accepted) is preserved as PROPOSAL-r9.md, 45488 bytes, sha256 c8c1bdc4a4330225558c3df829ec930fc6ac38e25ce891270b2ca130c4dd1367; it is the accepted text without the "r9 ACCEPTED" sentence. The pins for every file below are in `hashes.txt` beside this request.

Background: your X4B-a r1 review (`/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/reviews/grok-trust-bootstrap-x4ba-r1/REVIEW.md`, judgment call 12) ruled that r9 item 3 needs amending. X4T-a's `current_trust_admission::authenticate` passes `heads.root` to `trust_ordinary_roots::authenticate_shared` as both the accepted and the signing root. `verify_captured_core` requires the closure's first `rootChain` body to equal the accepted root and its last to equal the signing root, so X4B-a's rotated default release (root 1 to root 2, `heads.root` and `clock.record.rootVersion` at 2) refuses `FirstIdentity` at the confirming admission.

The change (lead decisions under the owner's standing direction, rejected alternatives recorded):
1. Item 3: `heads.root` stays the signing (final) root M that document signatures use and whose version is the epoch's `rootVersion`. The accepted root N is the first document of the closure `rootChain`, the `PayloadMetadataClosureV1` named by the root admission's `parent`. The documents after it are S5's N+1..M, evaluated link by link. `verify_captured_core` is unchanged. A new closure join: the last `rootChain` document must equal `heads.root.document` exactly (body and envelope references); an empty `rootChain` or one ending elsewhere refuses on the incomplete row. A one-root chain gives r9's result.
2. Knock-ons: item 1 (epoch `rootVersion` is M, never N); item 2 step 3 (where the accepted root is read, deduplicated by `Budget`); item 7 (one sentence: the `rootVersion` floor is `clock.record`'s, equal to `heads.root`'s, so no comparison changes); item 10 (the closure-join refusal on the incomplete row); item 11 (N's body and envelope counted with the chain; no figure changes); item 12 (rotation tests); item 13 (X4T-0 builds one-root chains only; new unit X4T-a3, the reader successor, which X4B-b depends on); forbidden substitutes; an "r10 note" listing the matching X4B correction (X4B-b's dependency and the X4B-a test that pins `FirstIdentity`).

Evidence (product main c2352ae, clean in crates/security/src; read-only):
- `/Users/sb/code/opensip-ai/opensip/crates/security/src/trust_ordinary_roots.rs`: `verify_captured_core` (lines 177 to 237), `authenticate_shared`, `bind_retained_head`, `RetainedHead::authentication_context`.
- `/Users/sb/code/opensip-ai/opensip/crates/security/src/trust_ordinary_inventory.rs`: `prepare` loads the closure from `records` and requires `rootChain` to contain the signing root and to match the manifest's count (`RootCount`).
- `/Users/sb/code/opensip-ai/opensip/crates/security/src/trust/current_trust_admission.rs`: `authenticate` (around line 537), `Floors::of_clock` and `check_evidence_floors`, `chain_bytes`, `admit_bound`'s epoch `rootVersion`.
- `/Users/sb/code/opensip-ai/opensip/crates/security/src/trust/floor_publication.rs`: check 3 (`owner.prior`, `Floors::below`).
- `/Users/sb/code/opensip-ai/opensip/crates/security/src/trust/accepted_store_fixture.rs`: `rootChain` is `[root_doc]` at `rootVersion` 1 (around lines 347 to 377).
- X4B-a worktree `/Users/sb/code/opensip-ai/opensip-x4ba` (uncommitted on daa7b01): `trust_bootstrap.rs` writes `heads.root.document` and the root admission's `root` as the chain's last document (around line 745); `trust_bootstrap_tests.rs` `a_multi_link_root_chain_is_authenticated_and_recorded_in_full` pins the `FirstIdentity` refusal.
- Security contract S5: `/Users/sb/code/opensip-ai/opensip_arch/docs/v2/contracts/product-v1/security-and-lifecycle.md`, section "S5. Root chain through expired roots".
- X4B r5: `/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/trust-bootstrap-x4b/PROPOSAL.md`.

Decide:
1. Diff r9 to r10 and confirm that nothing changed except the items listed above.
2. Does r10's item 3 close judgment call 12: does the stated split pass `verify_captured_core` for a rotated chain, and give r9's result for a one-root chain?
3. Is item 7 truly unchanged: are all five floors, including `rootVersion`, read from `clock.record` and equal to the signing root's counters, with nothing compared against N?
4. Is the closure join (last `rootChain` document equals `heads.root.document` by reference) lawful for every store X4B-a and X4T-0 write, and is anything else needed to bind N (for example its provenance, given that the reader authenticates N by its own threshold and its place in the root admission's closure, as r9 authenticated a one-root head)?
5. Is X4T-a3's scope right (reader change, closure join, rotation knob in X4T-0, tests), and is X4B-b's dependency on it correctly placed?

review.json must contain "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings" and "subjectSha256" (3484dc5d966ffd41cc6c8f50d2caab29fa3bf8cd3cc3eba322038fdd016b30a8). Write REVIEW.md and review.json. Do not commit.
