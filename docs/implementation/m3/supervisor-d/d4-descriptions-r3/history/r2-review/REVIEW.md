# CODEX2 review — D4 descriptions r2

## Verdict

**ACCEPT-DESIGN-UNIT**

The frozen subject manifest SHA-256 is `c1825ee871445128fec3ea2d9a0583ccfb10b87cb8be88f5eda6f2dcd61e0455`. All eleven declared members rehash exactly, and the stage contains only those members plus the subject manifest. The live product and architecture heads match `639922d58ae03acf6576d07e65970440aee512ff` and `962d3783503fbdc524cb6a2c44e9efc04e79d192`; the current design lock is 784,306 bytes with SHA-256 `58a4b2240a80f18ee2e29743f34174d430c5c61a2047fc437ba6f1c178efc676`.

R1 remains a rejected historical subject. Its four stage artifacts and four review artifacts are preserved byte-for-byte, including subject manifest `af3aa66bf070960e8da8772b12a102eee6e8c78e23b7c9f12341f75351158449`, review verdict **REQUIRED-FINDINGS**, and required finding `D4-DESC-R1-RF-1`. R2 does not accept or rewrite R1.

## Correction assessment

The R1-to-R2 passage delta is exactly one field: `passageOverrides[5].after`, at inventory239 selector `/files/510/description` for `crates/lifecycle/src/installation.rs`. All other passage keys, selectors, `before` values, `after` values, and supersession references are unchanged.

The corrected text matches the accepted implementation. The test `read_seam` calls `retained_tree::read_fixture::check()` only with debug assertions; the non-test seam calls it only with debug assertions plus `scenario-fixtures`. A fixture failure remains `TreeFault::Io { call: "read", error }` inside `WorkFailure::Operation`. The lifecycle crate refuses `scenario-fixtures` without debug assertions, so ordinary production release behavior is unchanged. The `LaunchMember.member_offset`, resolved-member suffix, and moved bound-path behavior remains attributed solely to `retained_tree.rs`, closing `D4-DESC-R1-RF-1` without duplicating that meaning.

## Description-contract assessment

The integrated D4-4 code commit `b79fee94f9b8f61b4fe207b1884573ceb3ecbbe1` is an ancestor of the current product head. The accepted D4-4 subject, independent review, root-assented unit record, bound inventory239, and preceding description authorities match their exact pins. All 32 accepted D4 source pins equal the current product bytes.

The current lock contains 186 contract successors, 199 inventory successors, and 161 inventory-passage inheritance entries; all 161 inherited entries are preserved by value. The proposed contract has the required collision-free shape:

- Eight direct overrides resolve to their exact raw inventory239 descriptions and paths, none of which already has an inherited effective meaning.
- Fourteen supersessions resolve to the final current inherited meanings. Each names one exact accepted predecessor passage, including three supersession-of-supersession chains.
- All 22 qualified physical paths are unique. Replacing fourteen existing meanings and adding eight direct meanings to the preserved 161 yields 169 effective meanings.
- The ten paths added by inventory239 are disjoint from these 22 paths and retain their separately accepted raw descriptions.

The passages accurately describe the accepted code and its limits: accounted `ControlContext` and closed launch construction share the caller `WorkScope`; independent authorities judge actual pristine TS2 and Rust3 Hello output before native recheck; the selected TS2 identity-version map is independent of both assembled outputs; the exact checked sender is consumed by participant composition; retained native members use actual resolved labels and operation-borrowed capabilities while preserving typed failure partitions; and fixture conversion, read-Io injection, and their feature surfaces remain debug/test-only with release guards.

The factory remains a pre-spawn library boundary. The contract does not add a production caller, Source access, spawn, effects, settlement, C4/native selection, Plan or signed-descriptor production, or operation-lifetime enforcement. The operability passage accurately preserves 115 owner annotations and all 463 parent lexical rows while adding seven ordinary conversion calls for 470 total; it does not claim D5 Cargo/cfg reachability or identity authority.

## Findings

None.

## Non-blocking observations

None.

## Acceptance boundary

This review accepts contract187 as a description design unit only. Root assent, binding, status publication, and push remain separate. C4/native selection/Plan/signed-descriptor producers, production operation lifetime enforcement, J2/H/CI4/source39/D5/platform/Linux/privacy/owner/clock/T2/CF, and full-project qualification remain open.
