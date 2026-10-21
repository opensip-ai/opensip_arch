# CODEX2 review — D2b-4c descriptions r1

## Verdict

**ACCEPT-DESIGN-UNIT**

## Independent assessment

I independently rehashed subject manifest `d586d31778ef01f24a99bbdf955e44f35882f0542441e025a71a868c3e88df15` and its three declared members. The frozen stage contains exactly the manifest, README, source record, and successor record. The outer review subject resolves to those exact bytes and identifies contract186 with eleven passage overrides and six passage supersessions.

The live product and architecture heads match `071dc8a3327c4c6991d6c9ada3036faeb83bda80` and `102e9d6aa7d0181aa6770ef1f50160dcc7aeb215`. The current design lock is 769648 bytes with SHA-256 `a732bfb35818bd470aa5296edbb5a7c99ca23b617ac84e96bb70cac800a9b656`. The accepted inventory238, D2b-4c r2 subject, independent review, root-assented unit record, prior description contract185, its review, and its unit record all match the source record's exact byte and hash pins.

The integrated D2b-4c code commit `700a3b77407ef203c65729781e54072712f32fa5` is an ancestor of the current product head. All 35 accepted D2b-4c source pins match that integration commit and current product bytes. All 37 current source pins, including the shared dispatch path and FA-2 vectors used by the replay, also match the current product tree. No source difference from the accepted unit is present.

The current lock contains 185 contract successors, 198 inventory successors, and 150 inventory-passage inheritance entries. The source record preserves all 150 inheritance entries by value. Inventory238 remains 803437 bytes with SHA-256 `a999a53ad099cbf10f8fd9bb482b46c9351b560438f32b18cf5134ca42e8cc6f`.

The successor has the required collision-free 17-path shape:

- All eleven passage overrides point into inventory238, resolve to the declared physical paths, and have `before` values equal to the raw inventory descriptions. None of those paths already has an inherited effective meaning, so they add eleven meanings.
- All six passage supersessions point into inventory238 and have `before` values equal to the final current inherited meanings for their physical paths. Each `supersedes` reference uniquely identifies the matching accepted contract185 passage and its inventory237 selector.
- The dispatch supersession correctly continues a two-record chain: contract186 supersedes contract185's dispatch passage, which itself supersedes contract184's passage. Every link retains the same physical `crates/components/src/provider_protocol.rs` path despite inventory reindexing.
- The eleven direct paths and six supersession paths are pairwise unique. Replacing six existing meanings and adding eleven to the preserved 150 produces exactly 161 effective meanings for the next inventory, with no double replacement, collision, or silent loss.
- The twelve paths added by inventory238 are disjoint from these 17 qualified existing paths. Their raw rows remain byte-for-byte equal to the separately accepted D2b-4c inventory descriptions.

The proposed passages accurately describe the integrated implementation and its limits:

- The schema, dispatch, and receive passages preserve the closed selected carrier/source model, exact immutable census/reference/target-attribution token selection, source-checked CompleteV3 decomposition, independently reconstructed reference subject/count/scope/domain values, and existing P3T/generated-carrier publication sequence.
- The schema-work passage matches the exact 52-source registry and 25 explicit consumed roots, including seven census roots. It describes the existing conservative checked coefficient bound without creating a new evaluator, schema owner, JSON escaping cap, CAN extension, or admission authority.
- The request/domain/sender passages accurately distinguish supplied admitted Plan/native projections from C4 authority. They retain exact D-empty expected-value checks, nullable census selection, inline/reference non-substitution, all eight immutable token variants, bounded custody, exact slot and aggregate accounting, and the participant's physical-write gate.
- The receive and participant passages preserve the original received census and candidate/Coverage/Complete buffers until the typed one-shot handoff after DONE, ZeroExit, and EOF. Only returned symbol scope/count settlement defers to H; nonsymbol and clean-terminal D-empty echoes stay exact. Pending Analyze bytes complete before one Cancel, and admitted `input-rejected` faults remain typed.
- The test passages identify public synthetic predicate and composition evidence without converting fixtures into C4 admission, source authority, spawn/production behavior, or qualification. Historical replay wording keeps current-context projections, literal profile refusals, symbolic GiB predicate controls, and other-owner results separate from original whole-executor outcomes.
- The operability passage matches 115 accepted owner-annotated rows and 463 conservative lexical rows. It retains all 462 parent lexical rows and correctly treats the single census `into` occurrence as ordinary conversion/error construction rather than mint or native authority.
- The FA-2 vector passage matches its actual TS2 and Rust3 predicate use while preserving the separation from C4 selection/admission and H returned-census settlement.

Contract186 changes descriptions only. It introduces no C4 selection, Plan/native/freshness authority, H census/fact settlement, production factory/caller/source39, schema ownership, private or blind invocation, product qualification, or entire-project completion. Root assent, binding, status reconciliation, and push remain separate work. The unchanged verifier profile remains a binding-time requirement.

## Findings

None.

## Non-blocking observations

None.
