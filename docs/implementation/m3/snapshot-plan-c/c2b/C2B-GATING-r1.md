# C2b gating memo r1: what blocks the C2b implementation plan

**Lead record, 2026-10-17. Not a plan and not a review subject.** It records why no C2b implementation plan is written yet, who acts, and the smallest units that unblock it. Bases: product main `3d1d771`, architecture `2d169666`.

## C2b's scope

C2b is "the TypeScript context and universe resolver, and the layout (item 10)", which depends on C2a. It is a hard XL part of 5 days (`PROPOSAL.md`:1184, M3-C r8). Item 10 names its pieces (`PROPOSAL.md`:564-571):
- the config graph `TypeScriptConfigGraphV1` (NE:1330-1386);
- the honored and stripped options (NE:1487-1488);
- `libSelection` and the stdlib inventory join (NE:1501-1519);
- the layout `ResolvedNodeModulesLayoutV1` (item 3, `PROPOSAL.md`:302-323; NE:1399-1420);
- `bind_typescript_universe` (NE:1583-1598).

The target-default `lib` table is "pinned data taken from the selected compiler closure" (`PROPOSAL.md`:571).

## What already exists on main

- **The config graph:** `crates/host/src/typescript_config.rs`, from units B2-c2 and B2-c2b, with no production caller.
- **The Run-closure admission side:** `inspect_native_context` (`crates/evaluator/src/native_context.rs`:368) and `inspect_typescript_universe` (`crates/evaluator/src/native_universe.rs`:142), including the layout's retained-input checks (:235-252). Item 10 makes the minting adapter call these same functions (`PROPOSAL.md`:562).
- **The schema:** `ResolvedNodeModulesLayoutV1` in `schemas/sources/native-v2.schema.json` (`maxItems` 100000).

## What blocks

1. **C2a is not implemented and has no implementation plan.** Item 7's one admission path is a signed component-manifest body under `opensip-signature-envelope.2` and a TR-INDEX catalog entry, both verified by the trust owner, plus a projection of the selected platform's TreeCommitment and a `closure2` descriptor (`PROPOSAL.md`:409-430).
   - On main, `crates/security/src/component_manifest.rs`:39-49 holds only CR-1's role-to-kind table. Its own comment says that signature, tree capture, closure identity and field-use admission are separate owners.
   - No code mints a manifest-admitted `closure2`. The only `closure_id` is the core inventory's (`crates/security/src/trust/core_inventory.rs`:435), which serves item 9's core roles, not manifest closures.
   - Item 8's synthetic-signed closure generator, the only lawful source of test closures (`PROPOSAL.md`:455-469), does not exist either.
   - The board's C2 row agrees: "Full C2a incomplete … Actual authenticated C2a projection/source profile/custody/admitted membership/nativeworker remain open" (`status/2026-10-16-r107/unit-register.json`).
2. **C2b's TypeScript context cannot be minted without C2a.**
   - `standardLibraryComponentDigests` and the `libSelection` membership rule need the retained **stdlib closure tree** (NE:1501-1519). A missing component refuses `native.native-context-lib-not-retained:<n>`.
   - The target-default `lib` table comes from the **selected compiler closure** (`PROPOSAL.md`:571).
   - Both closures are manifest-admitted, item 7's `toolchain` and `stdlib` roles (`PROPOSAL.md`:419-425). Every native context names one (`PROPOSAL.md`:434). With no admitted closures, item 7 states that no context is minted and no universe is bound (`PROPOSAL.md`:432-434).
   - Item 8 forbids unsigned test closures (`PROPOSAL.md`:462-465), so the context half cannot even be authored and tested against a substitute.
3. **Not blocking:** neither the E2s nor the J4a held tree is needed, and no unpublished native successor law is needed for C2b's pieces as item 10 lists them.

## Who acts

The lead, as M3-C's implementation lead. Item 7's verification is the M2 trust owner's (security, `crates/security/src/trust.rs`), and CR-1's widening is already bound (contract successor, `cr-1/`). No owner decision is needed.

## The smallest unblocking units

1. **A C2a implementation plan (r1)**, for items 7 and 8:
   - the signed manifest-to-`closure2` path: the envelope and TR-INDEX verification by the trust owner, the TreeCommitment projection onto regular files, `manifestDigest`, the `role → kind` table already in CR-1, retention, and the ephemeral no-trust-view case (`PROPOSAL.md`:431-437);
   - item 8's synthetic generator on the joint fixture predicate, with C2-T1 to C2-T8 and C2-T18.

   Item 9's core role closures are bound designs (CRC-1, CRC-2). The plan should state which of their code legs remain.
2. **A layout-only C2b sub-unit (C2b-0), plannable now.** `ResolvedNodeModulesLayoutV1` needs no closure. It is computed from the snapshot's installed package manifests, read with `readlinkat` and never followed (`PROPOSAL.md`:305; NE:1399-1420), and its rows are joined by digest, not snapshot membership. Its inputs are C1a (integrated), which supplies the snapshot and custody, and C1c-0, which supplies the pruned-tree capture its manifest reads need (C1c plan r1).
   - **Recommendation:** write C2b's plan as two sub-units. C2b-0 is the layout resolver. C2b-1 is the context, the options, `libSelection` and `bind_typescript_universe`, and waits for C2a.
   - C2b-0 alone satisfies the law's C1c edge "C1a; C2b's layout" (`PROPOSAL.md`:1182), so C1c-1 is unblocked without waiting for C2a.
   - The suffix table belongs to C2's resolution semantics and is reviewed with F (`PROPOSAL.md`:310). C1c reads by it; C2b-0 does not.

## Not claimed

- No plan, no code, no review.
- No change to item 10, to the Units table or to the C1c edge.
