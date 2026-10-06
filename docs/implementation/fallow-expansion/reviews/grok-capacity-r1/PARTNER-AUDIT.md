# Archived partner audit

This is the first technical-audit response delivered in the terminal before FX-CAP-1 was frozen. Herdr captured only its final page. It is advisory. It is not the FX-CAP-1 review verdict, and it did not author the candidate bytes.

The review verdict is in `REVIEW.md` and `review.json` beside this file.

---

Live pins match the baseline. Codex in w7:p1 is mid-turn on the Fallow comparison, so this reply stays here and that turn was not prompted. Nothing was accepted, bound, or written.

Product `f5f5b4d20eca34ab2312b3ffc141c378da326afe` is clean, and `design-lock.json` is 526786 bytes, sha256 `205eee0fcecb7076107db695b351c430cbc6866d10441857719f5bdeee235c83`: 102 contract successors and 103 inventory successors, through K1a v143. Architecture `2a5157d314ccfa9e37c0e1901391b2386c517369`. `native-evidence.md` is 329013 bytes, sha256 `83b99783893bec4bcca76bc043310e1d33305fc41ef85e012fbcb19e5b222ca0`. All 102 successor records match their lock hashes. No successor overrides native lines 4276, 4278, or 4280.

## Capacity

The current widest default is 11 requestable cells, not a permanent constant. The matrix `native-capability-matrix.v2.json` (36595 bytes, sha256 `4b1c19b03a34a271718b1e7e79335aa6f0735affd7cd36018035eeb4e7b18a14`) has eleven capabilities. `ts-tsconfig`, `js-allowjs`, and `js-synthesized` request 11. `rust-cargo`, `rust-cargo-prepared`, and `syntax-only` request 10. The unselected cell is `clones-cross-tsjs`. `syntax-only` still requests its six `UNSUPPORTED-TYPED` cells. So 1024 units need `requestedCapabilities.maxItems = 11264`, with 11265 refusing. The formula is `1024 × W`, where W is the widest mode's count of cells whose state is not `NOT-SELECTED`, evaluated on the matrix selected in that same successor. A later requestable cell is inadmissible until a successor recomputes the constant in the same schema generation as the cell.

That maxItems change leaves every historically admitted analysis-spec byte-identical, so those `PlanId`s stay stable. Identity schemas are not payload-registry documents under selected HSR-1, so this widening needs no new historical-reader row and no rewrite of retained digests. Same `$id`, `urn:opensip:product-v1:identity:v3`. The admission-source digest changes when the generator lane runs.

The 4 MiB canonical descriptor (identity-and-evidence.md:117, 4194304 bytes, depth 32) still bounds the record. The spike's own projection of 11264 rows is 1417243 bytes at 32-byte roots, 3940379 at 256-byte roots (253925 bytes of room), and 47194139 at 4096-byte roots. `Text` allows 4096, so legal roots already overflow the descriptor before the rest of the record is added. Publish that as the same pre-Plan refusal: `REQUEST.UNSATISFIABLE`, `PROJECT.SCOPE_LIMIT`, request-rejected, exit 2, subject `analysis-spec:bytes>4194304`, never truncated. Short-root 1024-unit requests can fit. Long-root ones refuse in full. That is the coordinated byte bound. It is not a measured performance envelope.

One Plan join belongs in the same successor. `plan.importIds` is 256 (`identity-v3.schema.json:538-540`) while `semantic-configuration.evidence.importIds` already admits 1024 (`:2668-2671`). Raise the Plan array to 1024 so an admitted import set is representable. Same maxItems-only effect on old records.

These stay as they are:

| Axis | Bound | Selector |
|---|---|---|
| Workspace roots | 1024 | identity-v3 `:2088-2091`; native `:4250-4256` |
| Path prefix arrays | 65536 | identity-v3 `:2097-2109` |
| Distinct native contexts | 128 | `plan.nativeContextDigests` `:524-526` |
| Semantic closures | 128 | `plan.semanticClosures` `:491-493` |
| Policy packs and analysis-spec parameters | 128 | `:2187-2199` |
| Plan stages | 1024 | `:813-815` |
| Stage-spec parameters | 128 | `:2946-2949` |
| Discovery population | 4096 | native `:4250-4254` |
| Descriptor cap | 4 MiB, depth 32 | identity-and-evidence.md:117 |

Contexts are toolchain closures, not units. Stages follow snapshot-plan C r7 item 16: one syntax stage per selected syntax universe, producer the core closure. Coverage keys are `(relation, rung, universes, subject-scope commitment)` (`CoverageKeyV2` in `native-v2.schema.json:1366-1416`), and the TypeScript key cap is 128 (`native:2964-2965`). One scope per universe stays inside that cap. A per-unit scope partition would not.

Provider numeric limits stay on the Hello equality pins. TypeScript `maxAnalyzeStages` is already 1024. Rust `ProtocolLimitsV3` keeps v2's 256 stages, 256 subjects per stage, 64 relations per stage, 64 MiB frames (`rust-provider-protocol.v2.json:96-120`). Selected RUST3-LIM says no limit member or value changes, and negotiated `subject-scope-reference-v1` is the transport when a snapshot has more than 256 subjects. Protocol majors stay Rust 3 and TypeScript 2.

S-R and S-B are not this amendment. S-R, in C r7 item 5, is the unwritten `snapshot2` successor that would name the inventory by reference. It waits on S-M SM-5 and SM-6 and has no draft. S-B is the unwritten eighth bounded field for the snapshot inventory, and fact-admission H's X-H6 subject-scope field is 100000 subjects and 4 MiB. A 1024-unit workspace can still refuse on the snapshot descriptor. That refusal remains typed and complete.

The selected handshake copies are not what the product tree contains. The product `handshake-v1.schema.json` is 32009 bytes, sha256 `9090e2ad51b767a176f51da09f201803d1cc82c047ade68102adcae1ee3a5f84`, with `TypeScriptCapabilitiesV2.maxItems` 11 and `RustCapabilitiesV3.maxItems` 13. Selected RUST3-LIM copies are 35746 bytes, sha256 `a08cc59e060581a8ca9dc43a0c79aed6fd2a8d12abf47afde6334ea734740fbc`, with 12 and 15. Those are wire tokens, not the eleven analysis capabilities. Leave that generation to its own lane. Do not fold it into FX-P1.

## Component model

The shared model can be normative before any adapter exists. Its minimum is:

1. A region over original snapshot bytes: path, content sha256, a closed kind, and a byte range into that file. Unmapped bytes stay explicit. Generated bytes are a separate retained blob and are never the span authority.
2. Whole-file JS, JSX, TS, TSX, and Rust are the degenerate region. Existing fact-anchor encoding stays. Embedded script, template, and style relations are additive. The model law adds no requestable capability. The adapter successor that does recomputes W with the capacity formula in one generation.
3. A missing grammar, preprocessor, dynamic component or class, or config that requires execution is a named incomplete result. It does not become a determinate non-use or a repair permission.
4. A source map that fails validation leaves the region incomplete. The parser closure id is retained and is the replay identity. No grammar crate or framework version is chosen here.
5. CSS starts as candidate evidence. Dynamic classes stay unknown. No qualified metric or completeness claim.

The recognizer registry is a separate widening. The closed nine are `node-package`, `typescript-config`, `npm-workspaces`, `pnpm-workspace`, `cargo-package`, `cargo-workspace`, `nextjs`, `vite`, `vitest-jest` (native `:2758-2760`, and the same enum at `framework-recognition-plan-v1.schema.json:131-140`, sha256 `49aacd8607e3f3195ac350b678f318388a5faf8f56f42e52087ec9ebe57ef822`). Config-discovery B r4 item 8 pins a generated host enum to that list. Unknown is a host invariant. FR-1 reads manifests and executes nothing. FR-5 makes a version change Plan-visible. New ids need a native passage, a schema enum, and that generated enum together. They do not authorize template parsing. Astro, Svelte, Vue, and CSS adapters wait on target-repository evidence. No member list should be invented in the model law.

## Plan amendment, after acceptance only

Record both owner selections in the successor, not by treating the current planning files as accepted. They still say the selections are pending. Then the implementation plan records, per affected unit, the base, the consumed successor, and the integration order. In-flight review subjects stay frozen. Unaffected units continue. Schema generation stays one document family at a time, with the handshake drift already ahead of FX-P1. No inventory version is reserved. S-R and S-B keep their own identities.

## Blockers before a frozen subject

- The byte conjunct and the 11264 formula have to be in the same subject as the row change. A row-only subject overclaims the target.
- S-R's reference-inventory recipe and S-B's eighth field are unspecified. This subject should cite them as unchanged owners.
- Component capability ids, grammar pins, and recognizer additions are not law yet. The capacity subject should say they recompute W later, and should not name them.
- I have no frozen manifest to review. This is not acceptance.
