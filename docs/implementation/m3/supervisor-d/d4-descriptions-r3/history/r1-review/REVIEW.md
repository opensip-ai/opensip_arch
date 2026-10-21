# CODEX2 review — D4 descriptions r1

## Verdict

**REQUIRED-FINDINGS**

The frozen subject manifest SHA-256 is `af3aa66bf070960e8da8772b12a102eee6e8c78e23b7c9f12341f75351158449`. Its three declared members rehash exactly. The live product and architecture heads match `639922d58ae03acf6576d07e65970440aee512ff` and `962d3783503fbdc524cb6a2c44e9efc04e79d192`; the current design lock is 784,306 bytes with SHA-256 `58a4b2240a80f18ee2e29743f34174d430c5c61a2047fc437ba6f1c178efc676`.

The integrated D4-4 code commit `b79fee94f9b8f61b4fe207b1884573ceb3ecbbe1` is an ancestor of the current product head. The accepted D4-4 subject, review, unit/root assent, bound inventory239, and prior description authorities match their exact pins. All 32 accepted D4 source pins equal the current product bytes.

The successor's passage mechanics otherwise reconcile exactly. All 186 prior contract successors, 199 inventory bindings, and 161 inheritance rows are unchanged by value. The eight direct overrides resolve to raw inventory239 descriptions on paths without inherited meanings. The fourteen supersessions resolve to the final inherited meanings and uniquely identify their accepted predecessor passages; three correctly continue supersession-of-supersession chains. The 22 physical paths are unique and collision-free, the ten rows added by inventory239 are disjoint and retain their accepted raw descriptions, and 161 inherited meanings plus eight direct additions would yield 169 effective meanings.

## Required finding

### D4-DESC-R1-RF-1 — the `installation.rs` passage describes the wrong implementation

The direct override at `/files/510/description` resolves to `crates/lifecycle/src/installation.rs`. Its proposed addition says that D4 accounts a retained `LaunchMember` member offset and constructs it from the actual resolved bound path.

That behavior is not implemented in `installation.rs`. The accepted D4 diff for this file only extends `read_seam`: test/debug and debug-plus-`scenario-fixtures` paths call `crate::retained_tree::read_fixture::check()` and preserve failure as `TreeFault::Io { call: "read", error }`. The `LaunchMember.member_offset`, resolved-member suffix, and moved bound-path implementation is in `crates/lifecycle/src/retained_tree.rs`, whose separate `/files/518/description` supersession already describes it.

The current override therefore duplicates another path's behavior while omitting the actual D4 meaning added to `installation.rs`. This violates the request's path-specific source accuracy and no-silent-meaning-loss requirements.

Required correction: replace the `/files/510/description` addition with a path-specific description of the installation read seam's narrow debug/scenario-only fixture check and its typed read-Io mapping. Keep the member-offset/path behavior solely with the retained-tree passage, then freeze a new exact successor and manifest.

## Acceptance boundary

This review does not accept contract187. It does not change the accepted D4-4 code unit or bound inventory239, and it does not establish binding, status publication, push, or product qualification. C4/native selection/Plan/signed-descriptor producers, production operation lifetime enforcement, J2/H/CI4/source39/D5/platform/Linux/privacy/owner/clock/T2/CF, and full-project qualification remain open.

## Non-blocking observations

None.
