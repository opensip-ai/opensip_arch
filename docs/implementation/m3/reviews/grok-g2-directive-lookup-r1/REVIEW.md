# G2 directive lookup r1

ACCEPT-DESIGN-UNIT. implementationVerdict ACCEPT-UNIT. requiredFindings empty.

Subject manifest `docs/implementation/m3/native-g/g2-directive-lookup-r1-subject.json` is 2839 bytes, sha256 `f7de1c79c1b3f20e1c89e081dde8e99834e7d140299a1690f561411e5f2a1749`. All 13 members match. Their paths are sorted and unique, and `successor.json` appears once. Successor `docs/implementation/m3/native-g/g2-directive-lookup-r1/successor.json` is 3168 bytes, sha256 `de883d59e7da54fca6a524344abf807d0da3123c97a3470e446b03e4169b3bdd`. `passageOverrides` is `[]`. The record has no `passageSupersessions` key, so this review omits `supersededPassages`. Standing: "PROPOSED G2 declared inert directive lookup only; no directive interpretation or worker admission".

`candidates` is the other 12 subject members. The record path is absent. Each candidate pin equals its subject pin, and the candidate paths are sorted and unique.

Product HEAD `5945f97327c9ec3a0d1c121abc4712e04f1ab7de` and architecture HEAD `990d632f13367ec9ae761d4305f2c1341d527a8d` are the pinned bases. Product is tracked-clean. Architecture is tracked-clean. Its untracked drafts stay outside this unit. `~/Library/Application Support/OpenSIP` is absent. Against the pinned product tree of 967 tracked files, the candidate differs in exactly the two Rust files below. Stage copies match the candidate bytes, and those bytes match `productAfter`. The same paths at the product base match `productBefore`. `design-lock.json` does not yet contain this successor.

## Parents

The two parents match the architecture bytes. There is no passage override and no inventory successor.

- Selected `native.v2.schema.json` is 280357 / `e5834d37aebd96d77d352975878da349033f8633ecbd83322ad0fbea461f7773`. `PreparedOutputRowV3` requires `kind`, `ownerKey`, `configuration`, `site`, `generated`, `inputBinding`, `blob`, `status`, and `failureDetail`. `status` is `ok` or `failed`. `kind` includes `build-script-directives`. The row blob is `{sha256, byteLength, mediaType}`.
- Admitted NE `native-evidence.md` is 329013 / `83b99783893bec4bcca76bc043310e1d33305fc41ef85e012fbcb19e5b222ca0`. §3.6 PO-0 admits `build-script-directives` as captured `cargo:` lines with media `text/x-cargo-directives`, and a media label is not a trust proof. PO-2 retains a failed build script and analyzes that owner non-prepared. PO-1 staleness and PO-2 non-prepared fallback stay with the caller.

Inventory v166 remains 614780 / `d1d5e69aeacbef99d33fcfd4f4881c72e8671cda04e036156f1412c17c30926d`. `prepared_inputs.rs` stays role `validator`. `prepared_inputs_tests.rs` stays role `test`. Neither row pins content.

## Lookup

`providers/rust/src/prepared_inputs.rs` gains 73 lines after the expansion lookup and loses none. `check_declared_prepared_inputs`, the generated-file lookup, and the expansion lookup are unchanged. `lookup_declared_build_script_directives` calls that whole-set check first. The check joins the universe, context, snapshot, and ownership inputs, then checks every row for an inert kind and media, owner-manifest and toolchain and cfg and dependency binding, retained blob length, and the generated path and byte bounds. A missing owner or a removed preimage returns `DirectiveLookupError::Prepared` before a miss or a failed row can become `Missing`.

With no selected prepared digest the result is `Missing`. A row whose `ownerKey`, `kind` `build-script-directives`, and `status` `failed` all match returns `Missing` after a full scan, so an earlier `ok` row does not hide it. Only `ok` rows of that exact owner and kind are candidates. A second such row returns local `DirectiveLookupError::Ambiguous` and does not concatenate, prefer an order, or add a wire reason. One match copies `RetainedInputs::blob` after the digest check into `Arc<[u8]>`. `bytes()` is the full retained slice. The copy stays after the backing map is replaced and the fixture is dropped. The bytes are not parsed, decoded, or applied as `cfg` or environment settings.

`DirectiveLookupError` is `Prepared` or `Ambiguous`. `DeclaredBuildScriptDirectives` is `Missing` or `Bytes`. No process, compiler, loader, VFS, `NativeContextVerified`, Coverage, Plan, Run, or producer cardinality rule is added.

## Controls

`evidence/checks.py` and `evidence/validate.py` were not run. The supplied logs were read.

`prepared_inputs_tests.rs` keeps the product-base bytes as a prefix and appends six tests: `directive_lookup_retains_exact_uninterpreted_owned_bytes`, `directive_lookup_owner_and_kind_are_exact`, `directive_lookup_failed_owner_dominates_ok_rows_in_either_order`, `directive_lookup_duplicate_ok_rows_never_merge_or_choose_by_order`, `directive_lookup_empty_and_absent_sets_are_missing`, and `directive_lookup_miss_and_failed_owner_cannot_bypass_whole_set_checks`. The owned-bytes control uses `cargo:rustc-cfg` and `cargo:rustc-env` text plus `0xff` and NUL, then checks the owned arc after replacement and drop. Owner and kind mismatches, including a lone expansion row, are `Missing`. Failed and `ok` directive rows in both orders are `Missing`. Two `ok` rows in both orders are `Ambiguous`. An empty prepared set and an absent selection are `Missing`. A stale `cfgSetId` on a lookup miss is `Prepared(Binding)`, and a failed row whose blob was removed is `Prepared(Retained)`.

`unit-tests.log` is `cargo test --locked --offline --manifest-path providers/rust/Cargo.toml --lib`: 163 passed, 0 failed, 0 ignored. That is the 157 pre-existing library tests plus these six. `clippy.log` is the same package with `-- -D warnings`: zero `warning:` lines, zero `error:` lines, `Finished`. `format.log` is empty. `checks.json` records `passed` true, `newTests` 6, inventory 166, and `qualification` false.

After this dual acceptance and root assent, `verify_design` runs on the current main lock, the two Rust files land in one code commit, and this bind lands in a separate lock commit. Nothing is pushed. The record does not grant native or product qualification.
