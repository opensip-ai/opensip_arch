# Review: existing-root admission 468 r4

Grok is the single reviewer. Claude Opus 5.5 leads. Law review of the owner amendment after r3. No repository edits and no product cargo.

Subject `docs/implementation/m2/existing-root-admission-468/PROPOSAL.md`, 10395 bytes, sha256 `bbd48bad7c04e509b4e9d54b19e586f546f129d11fbd18615a36eb5660404e0a`. `PROPOSAL-r3.md` preserves the prior bytes. The diff is the premise, the charged walk to the fence, the chain in the recheck, the barrier reservation, and the incomplete-installation row.

## Verdict

**REQUIRED-FINDINGS.**

## What holds

The premise lent to the gate is 465 item 4's scope: root to H, `Library`, and `Application Support`, and only through that premise's own `fstatfs` on the descriptor. With no premise, an omitted ACL on those components refuses. `OpenSIP` and I do not use it. The capability stays sealed, implemented only by this invocation's `InitialPlatform`, and it grants no standing. Lending the premise the platform already holds does not mint a new one and does not widen 465.

The fence attempt opens `lifecycle.fence` no-follow through the retained I handle and takes the same nonblocking exclusive lock. Owner §5 and 467 item 9 exclude other holders by that lock, not by the uncharged chain walk inside `NativeInstallationFence::try_acquire`. A busy lock still ends at `LEDGER.BUSY_TIMEOUT` with detail `PROJECT.BUSY`, and the gate latches so this invocation does not try again. The walk uses the 460 and 465 predicates, charges each step, and the post-barrier recheck is reserved with the barriers.

A present but incomplete or contradictory I is request-rejected, exit 2, `CONFIG.INVALID`, with existing detail `CONFIG.CUSTODY_REFUSED` and subject `installation-incomplete`. That subject is not a new domain code. S12 already fixes this detail as that class and error code. A failed read stays on the `HOST.IO_FAILURE` row. Owner §6's "relevant owner" remains the internal refusal; this is its public projection, and the owner allows no fourth code.

## Required finding

### RF-1 — The observation path still takes the uncharged fence

Owner §5 requires the observation-only path to hold the same installation fence before its member reads. Item 4 charges those reads and does not give that path item 3's retained walk. `NativeInstallationFence::try_acquire` still re-observes the whole chain without a charge, which is the cost this amendment removes from the write gate, and it still treats an omitted ACL as "no writers", which 461 retires.

Item 9's 458c direction does not absorb this. It is a fence-free receipt limited to the root-to-H prefix. The observation path has to hold the fence, and its chain continues through `Library`, `Application Support`, `OpenSIP` and I.

Failure scenario: `doctor` or `query` on a `/Users/<name>` home calls the ordinary fence. The chain walk spends on the order of 126k edges without moving the ledger, then the charged member reads and the recheck cross the 131,072-edge cap, or the cap never sees the walk. An omitted ACL that 465 would refuse is read as admitting the chain.
