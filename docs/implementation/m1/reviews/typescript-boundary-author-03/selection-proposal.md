# Selection proposal: TypeScript lane dependency checker (author-03)

**Standing.** This is a proposal for independent review and root selection. It is not an acceptance, and it does not change the build plan.

## Proposal

For the build plan's "TS dependencies" decision, propose the author-03 `check-boundary` design (candidate B) as the successor candidate to the dependency-cruiser trial (candidate A).
- **Build and declaration edges:** TypeScript 6.0.3 program resolution, with per-usage modes.
- **Node runtime edges:** Node 24.16.0's own non-executing resolvers, over TypeScript-emitted and materialized JavaScript.
- **Browser runtime edges:** enhanced-resolve 5.25.1, as the declared bundler policy until a bundler is selected.
- **Boundary policy and censuses:** checker-owned.

This is a change of candidate tool, so it needs independent review before it replaces anything.

## Rationale

**Evidence** (details in `comparison.md`):
- The same 158 cases and 29 Node-oracle rows give B all correct, with oracle agreement 29/29. A misses 14 review-02 probes and 6 regressions, has 3 false refusals, and disagrees with the oracle on 8 rows.
- All seven review-02 required findings are fixed in B, and each has an isolating case and a killed mutant.
- On the real staged `tools/contracts` lane, B passes in 1.31 s at 719 MiB, with three exact, reviewable trusted usages. A refuses it in 2.08 s at 1133 MiB.

**Fewer overlapping authorities:**
- A emulated TypeScript mode selection, type elision, Node format and Node resolution on top of one enhanced-resolve cruise per condition set.
- B delegates each of those to its owner. The remaining checker-owned semantics are request extraction (cross-checked against TypeScript's loaded files), Node package scope and syntax detection for untyped `.js`, emitted-output mapping, and boundary policy.

**Interfaces and closure:**
- B uses public TypeScript APIs and one documented experimental Node flag, which it verifies at startup. A used four undocumented dependency-cruiser behaviours.
- B's closure is 4 packages, all archive-verified, against A's 44.

## Boundary between the checker and upstream inventory selection

**What upstream owns.** The acceptance of the selected inventory is owned by `tools/verify_design.py` and the design lock: review, root assent and successor rules.

**What the checker owns.** Verifying that the lock's last inventory successor pins match the architecture bytes, then deriving lane authority from the selected inventory package:
- package root;
- kind;
- platform policy;
- inventory dependencies.

**Caller lane records** may only list inputs and exact trusted usages. The checker refuses a record that tries to set policy, and it censuses package sources and inventory rows so that no source can be hidden from it.

**Demonstrated join.** Fixture lanes for `report` and `typescript-provider` bind through the real product design-lock bytes and the pinned architecture files. Tampered pins, wrong package kinds and unbound-flag misuse exit 2.

## Decisions requested from the owner or root before integration

1. **Runtime dependency classes (A5):** confirm or replace the proposal that provider and browser runtime groups exclude devDependencies.
2. **TypeScript's compiler-plugin loader** (`typescript.js:8405`, `require(modulePath)`) in the `tools/contracts` closure: accept it as a no-target trusted usage, or change the lane so that it is not reached statically.
3. **`tools/contracts` in the inventory:** add a package or successor row for `tools/contracts` so the lane can be bound rather than an unbound trial, and adopt a product tsconfig for it.
4. **Package manager and lock policy:** decide how the checker's own closure is provisioned (currently npm-materialized bytes with archive verification) relative to the pnpm-managed lane closure.
5. **Bundler selection:** when a bundler is selected, replace the declared enhanced-resolve browser policy with that bundler's resolver configuration, and re-run the browser cases.
