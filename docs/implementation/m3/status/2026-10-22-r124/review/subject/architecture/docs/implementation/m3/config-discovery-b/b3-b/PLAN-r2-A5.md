# B3-b plan r2, amendment A5: B3-b3a in two units, the bound before the gate

**Lead plan amendment, 2026-10-17. Unreviewed.** It amends the accepted B3-b plan r2 (`PLAN-r2.md`) as amended by A1 to A4. Law M3-B r9 is unchanged.

## A5-1. Why split

Plan r2 §4.3 makes B3-b3a one unit, the census successor accepted before any held-out read. It carries:
- the closure re-pin;
- three new cost terms (§4.2);
- their measured-against-model validation at three root lengths;
- the under-count mutations;
- the walker rows' equality projection;
- the blind mode's extension to the new terms;
- the receipt's confidentiality and lifecycle controls.

**The new terms are the larger part.** They mirror, charge by charge:
- the D15 decision core's observation requests over the native observation (`workspace_observation.rs`): directory opens through its reused stack, a record per new binding, by-name observations, custody captures, bounded carrier and manifest reads with their post-read checks, and kept-read copies;
- item 6b's member producer (`git_tracking.rs`): placement, layout, the config and index reads at their ceilings, the config parse and index decode, custody, the identity list and its records.

That is a model the size of the walker's, with its own anchors. A single review would mix it with the receipt's confidentiality controls. So B3-b3a becomes two units, and the pre-run gate stays on the second.

## A5-2. The units

**B3-b3a1: the bound (product tooling and tests).**
- **The closure.** The cost closure gains the member producer's and the readers' files: `git_tracking.rs`, `workspace_declarations.rs`, `workspace_observation.rs` and `workspace_discovery.rs`, with the platform helpers they call. The constants are read by anchors, as the walker's are. Any change refuses.
- **The model.** The census model gains §4.2's three terms, each separate and charged to exactly one term (A2-3 step 4):
  - **the reader term,** paid at n = 0: the carrier reads, their custody and their declaration rows;
  - **the member term,** at n members: placement, the visible-repository listing, item 6b and the provider-manifest reads. The placement and listing charges are paid at n = 0 over the declaring entries and the listed population (A2 r2's carried observation);
  - **member descent,** in the walker rows: the walker over admitted members, with the binding table and gitlinks.
- **The repository rows.** Each lead-readable repository entry's row gains its reader and member terms. Its full-ledger cost is their sum with the walker's, and its margin is re-evaluated under the r7 caps. Workspace rows stay walker-only (B3-b3c).
- **The equality projection.** Every walker field of every lead-readable row equals B2-b4b3's, with an explicit allowlist of changed fields (§4.2).
- **The validation.** §4.2's measured-against-model controls cover:
  - the native readers, member producer and walker on synthetic cases: a member, a shared path, exact roots, an excluded member, a nested repository inside a member, and boundaries;
  - each at the worst read growth and retry envelope;
  - each at root lengths 134, 1,024 and 4,096.

  The existing actual-against-predicted checks stay. There is one under-count mutation per new term.
- **No held-out store is opened.** The blind receipt stays stale, as A1 states.

**B3-b3a2: the gate.**
- **The blind mode is extended** to the new terms over held-out entries: margins only, with B2-b4c's output allowlist unchanged.
- **The receipt's binding** covers the extended closure.
- **The synthetic confidentiality and lifecycle controls** are extended to the new terms.
- **The pre-run gate:** Codex accepts these exact bytes before any held-out store is opened (§4.3).

**B3-b3b and B3-b3c are unchanged.** B3-b3b is the blind run of B3-b3a2's accepted tool. B3-b3c is the workspace margins, each row walker plus reader term plus member term at its member count.

## A5-3. One reading of §4.2, settled (lead decision)

**The bound is the ledger's** (law M3-B r9 item 12: "everything item 6b charges … and every other charged step"). §4.2's reader term lists "its parse". The readers' TOML and JSON parses run inside the pure decision core, which holds no ledger, and are not charged. That code was accepted in B3-b2b1 (Codex `codex-b3b2b1-r2`) and B3-b2b2b (`codex-b3b2b2b-r5`). Each carrier is bounded at 4 MiB before it is parsed. So the reader term has no parse component.

The member producer's config parse and index decode are charged (`git_tracking.rs`: one object, one edge and the config's length; twice the index length), and the member term carries them.

**Rejected:** adding parse charges to the decision core here. That would change accepted product code in a census unit, and item 12 asks for a bound on what is charged.

## A5-4. Steps (as amended by A1 to A5)

1. Through B3-b2b2c (bound).
2. **B3-b3a1**, then **B3-b3a2** (the pre-run gate).
3. B3-b3b (the blind run) and B3-b3c (the workspace margins).
4. The status round.
