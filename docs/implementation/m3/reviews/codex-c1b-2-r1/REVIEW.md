# C1b-2 r1 review

**Verdict: ACCEPT-UNIT.** No required findings or non-blocking observations.

## Subject and authority

Verified the 19,617-byte subject manifest, SHA-256 `cf9ab20c35a92f76eeb133d66855454df3771046ad6a8a0b4ec603be2df1eb7f`, and all 83 members against their recorded sizes and hashes. Also verified all 18 authority pins in `source.json`.

The candidate HEAD is the declared product base `114d2ac9708cca10563316a0cb11f09b30d1b919`. All four product-map entries match the candidate, archived bytes and parent pins. Git shows exactly those four changed files and no untracked files. The three model vector files remain byte-identical to the base.

## Review conclusions

1. **Sealing order and refusals.** Step 4 calls `observe_vcs(root, custody, inputs.boundaries, work)` after inventory/order, leftover and carrier checks and before item-5 bounds and sealing allocations. It uses the lending's VCS subject, discovery's record and the same caller scope. `encoded_len() == None` is the sole `VcsPending` return and denotes `Unobserved`; observation refusals become `SealError::Vcs`, while budget failures remain budget failures. The existing observer enforces the record's root and subject preconditions.

2. **Canonical records.** The three encodings preserve schema-2 `none` and `git` and add schema-3 members with the required top-level `none` values. Git `dirty` values are literal `true`; top-level `none` values are literal `false`. Members retain path order, with a strict byte-order check before encoding. The inventory is hashed once for its digest; that digest appears once in the VCS record. The record's raw digest is the descriptor's `vcsDigest`. Independent canonical-encoder comparisons and schema admission cover the record shapes, enclosing and nested repositories, loose and packed refs, and the two- and 64-member workspaces. The empty admitted member list selects schema 2. Schema-2 preservation and changes across observation kinds are checked separately.

3. **Exact allocation charge.** `vcs_record_len` counts canonical syntax and escaped paths before allocating and is cross-checked against C1b-1's `encoded_len`. `charged_vcs_record` charges `owned_record(len)` immediately before its sole `Vec::with_capacity(len)`; it borrows member paths and uses stack commit/digest arrays. The written length is checked. The allocation source guard covers the new buffer and its preceding charge. Encoder controls cover escape classes, multibyte strings and the 1,573,798-byte maximum, with exact funding succeeding and one byte short refusing Budget. The lane's charge-site equality matches that maximum to C1b-1's derivation; the model term and vectors do not change. The disclosed counting, ordering and hashing computations follow the existing sealing convention.

4. **Census and cumulative receipts.** The census anchors the new exact-charge site and obtains the record maximum from the model. `afterWalk.bytes` rises by exactly 1,573,638 (1,573,798 minus 160); objects and edges do not change. The regenerated record has no failing 2× rows and retains its recorded margin status. The live permitted receipt checker reproduced the archived receipt-specific record exactly. For both receipts it verifies the refresh baseline and unchanged receipt bytes, the C1b-0/C1c-0/C1b-1 batch delta, C1b-2's own delta, their cumulative union, ten stale rendered rows and `heldOutMargin: outstanding`. This is valid evidence of the open stale interval, not current blind qualification. The combined reviewed freeze, blind run and refresh remain due after integration.

5. **Rules and scope.** The changes introduce no new mint-census call, environment read or `let _ =`. No caller, J2 refusal projection, ephemeral observation, batch refresh or product qualification is supplied by this unit.

## Validation and limits

Independently ran only the three permitted checks: snapshot-ledger model `--check` (all three vector outputs verified), operability source (114 rows, no findings), and the package's receipt-specific checker (passing and equal to the archived result). The receipt checker temporarily used `review.json` for its output; the final file contains the requested verdict schema.

Reviewed the pinned final lane evidence, not the superseded void attempt. It records successful preparation, build, warning-denied all-targets Clippy, formatting of the two base-clean Rust files, 17 focused sealing tests, model and census output checks, FW-01, environment exceptions, operability and verify_design. The recorded closure intersection is empty. All six mutations are caught by test failures: the four plan mutations plus allocation-before-charge and maximum-precharge.

The broad suites are not wholly green: host has the same eight failures at base and candidate, with seven new passing tests. Security has 15 base failures versus 14 candidate failures; the sole difference, `every_member_refusal_has_its_subject`, passed three isolated reruns on each side, and the lane classifies it as flaky. The remaining failure sets match. The request's six-new-test wording predates the seventh control recorded in SCOPE and the final evidence.

No Cargo, rustc, build, lane, network, other pane or delegation was used during this review. No forbidden fixture, installation, key, tree, store, overlay or cache was accessed. Only REVIEW.md and review.json were written; neither repository or worktree was edited.
