# Core role derivations r1

ACCEPT-DESIGN-UNIT. implementationVerdict ACCEPT-UNIT. requiredFindings empty.

Subject manifest `docs/implementation/m3/snapshot-plan-c/core-role-derivations-r1-subject.json` is 3924 bytes, sha256 `d6c9bf1ab30419593dd159abe568c28dd241107440bb1f05fd2463947628bc2d`. All 17 members match. Successor `docs/implementation/m3/snapshot-plan-c/core-role-derivations-r1/successor.json` is 4405 bytes, sha256 `0442ce75132bda3f0e3f9b1b73878779f166c89ef59565c6a92983e17f6e39e7`. `passageOverrides` is `[]`. The record has no `passageSupersessions` key, so this review omits `supersededPassages`. Standing: "PROPOSED CRC-1 core role derivations implementation; C2a remains incomplete".

Product HEAD `86fbe0547c94220f7c33d514173f8620e0dcff7a` and architecture HEAD `d559012c9b0e0324457cd390fb9fa14015bd9dfd` are the pinned bases. Product is tracked-clean. Architecture is tracked-clean. Its untracked S-OP and E2s drafts stay outside this unit. `~/Library/Application Support/OpenSIP` is absent. Against the pinned product tree of 967 tracked files, the candidate differs in exactly the three security sources below. Stage copies match the candidate bytes, and those bytes match `productAfter`. The same paths at the product base match `productBefore`. The candidate `design-lock.json` equals the product lock. This successor is not yet in that lock. CRC-1 is already bound.

## Parents

The three parents match the architecture bytes. There is no passage override and no inventory successor.

- Inventory v166 remains 614780 / `d1d5e69aeacbef99d33fcfd4f4881c72e8671cda04e036156f1412c17c30926d`. `core_inventory.rs` and `initial_core.rs` stay role `validator`. `initial_core_tests.rs` stays role `test`. None of the rows pins content.
- Bound CRC-1 `README.md` is 31758 / `4e551e37d8bd838ffdd5c6b68c29ac26bd200eb6e5bd4daa45c77f49c005dc6e`. A core release has five closures from one selected-platform descriptor. The detector, provider, and adapter closures differ from that descriptor only by `kind`. `manifestDigest` is the raw SHA-256 of the TR-CORE-signed inventory body, and `tree` is the platform's regular files. The identity is the existing `closure2:` plus `H("closure", D)` recipe. The baseline vector and the 53 accepted cases are the control.
- `crc-1/evidence/vector.json` is 16122 / `288045ffc0d246a27ef16d94f029ea65d25586b4d9a7044d5c3654894447af63`.

Bound CR-1 states that no accepted text says which manifest field supplies `closure2.protocolMajor` for a component role, and that C2a applies one rule to every role. This unit does not choose `compatibility.control` or `providerProtocol`, and it does not add a component projection.

## Derivations

`CoreRole` is a private enum with `Detector`, `Provider`, and `Adapter` only. `role_descriptor` is private. It clones the validated core descriptor and replaces `kind`. `bind` still builds that descriptor with `manifestDigest` equal to `raw_sha256` of the admitted body and `tree` from the selected platform row, then caches `closure_id` of the core descriptor, the existing `evaluator_descriptor`, and the three role descriptors. `closure_id` remains `closure2:` plus `hash_canonical_value("closure", D)`. `project` and `project_v3` both go through `bind`, so a V3 body and a different selected platform change the ids with the descriptor. A noncanonical body still fails `shapes::Error::NonCanonical` before a descriptor exists.

`evaluator_descriptor` and its call are unchanged. The EC1 getter on `InitialCore` is unchanged. `Projection`'s new getters return the cached strings and grant no signature, Plan membership, or field use. `InitialCore::detector_closure`, `provider_closure`, and `adapter_closure` read `self.release.authentication().core().inventory()`, the projection stored on the existing authenticated capture. They take no kind, role, or `Projection` argument. No alternate constructor, manifest role, or signer is added. The other `initial_core.rs` and test edits are formatting. Parser, signature checks, clock and X9 sources, counts, and cost constants are outside the diff.

The unit stops at these identities. It does not retain a component tree, join a detector contribution or a selected evaluator, admit an import role, or place a closure in `semanticClosures` or a Plan. An identity string is not a field-use permission. CRC-2's third provider use is not implemented. C2a remains incomplete, and no C2a inventory successor is emitted.

## Controls

`evidence/checks.py` and `evidence/validate.py` were not run. The supplied logs were read.

`role-tests.log` is four passed and zero failed: `crc1_vector_core_role_closures`, `crc1_all_accepted_inventory_cases_preserve_members_and_distinct_ids`, `crc1_v3_role_ids_bind_selected_platform_and_raw_body`, and `crc1_authenticated_initial_core_exposes_the_same_selected_role_ids`. The vector test pins body length 5990, manifest digest `1d012c7d606524c238109dd4c1882b431e27325d57636f9a09099ec3cf98ac5d`, and the three CRC-1 closure ids and canonical descriptor SHA-256 values for detector, provider, and adapter. The 53-case test requires each role descriptor, with `kind` set back to `core`, to equal the original descriptor, and requires the five ids to be pairwise distinct. The V3 test requires the selected platform and its tree, a changed raw body and another platform to change the ids, and a trailing space to refuse as noncanonical. The `InitialCore` test produces a core through the existing injected proof path and requires its three role ids and the evaluator id to equal `project_v3` of that same signed inventory. Existing refusal tests remain in the file.

`unit-tests.log` is the ordinary `opensip-security` library: 1030 passed, 0 failed, 2 ignored. The ignored tests are the pre-existing host-observation pilot and the real-host S4 composition. `feature-clippy.log` is `cargo clippy --locked --offline -p opensip-security --lib --features scenario-fixtures,crash-matrix -- -D warnings`: zero `warning:` lines, zero `error:` lines, `Finished`. The three `format-*.log` files are empty. `checks.json` records `passed` true, `newTests` 4, inventory 166, and `qualification` false.

After this dual acceptance and root assent, `verify_design` runs on the current main lock, the three Rust files land in one code commit, and this bind lands in a separate lock commit. Nothing is pushed. The record does not grant native or product qualification.
