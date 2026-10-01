Grok review: law X3b r7, the grant journal, with grant-generation rollover. Claude Opus 5.5 leads, and you are the single reviewer.
- Make no repository edits, commits or pushes, and do not delegate.
- Write only under `/tmp/opensip-implementation/reviews/grok-journal-x3b-r7`.
- This is a law review: no product cargo.

## Subject

The subject is `docs/implementation/m2/journal-x3b/PROPOSAL.md` r7, in the arch repository `~/code/opensip-ai/opensip_arch`. Its pin is in `hashes.txt`: sha256 `b9aad8f68fd150ca5245378a7c3925b7f80e8b282fde0a772b35c7d3c948c3c5`, 52076 bytes.

The accepted r6 is preserved as `PROPOSAL-r6.md`: sha256 `4ee7e465e790fa3bc04ddd40c6e07e96e00e08a1487e0f10049b57dec4a72765`, 25772 bytes. That equals the subjectSha256 of your r6 acceptance in `reviews/grok-ledger-x3c-r3-x3b-r6/x3b/review.json`. Diff r7 against it.

## Why r7 exists

You accepted X7 r3 (`finalization-x7/PROPOSAL.md`, sha256 `aa390f82…`). Its item 6 and dependency note require X3b r7 to define grant-generation rollover inside X3b r6 item 4's end step, under the fence that step holds. r7 must cover:
- the `EXCLUSIVE` closure, as `carrier-format.v3.md` §7 step 1 closes a generation;
- the `TERMINAL` append (cause `grantGenerationClosure`) through item 5's protocol, with its own `op-` token and how that token is minted;
- the opening of generation g+1: its carrier, witness and floor, and their crash states and reconciliation;
- the end step's floor write for g+1;
- skip-if-busy;
- charging all of it to the attempt ledger (X7 r3 item 7), never the gate ledger.

## What changed (r6 to r7)

- **New item 4a, generation succession.**
  - **Opening.** g+1 has no carrier row until its first record, which is `seq` 1 with the genesis chain value for (N, g+1). Opening g+1 is the witness `COMMITTED (g+1, 0, null)`, and later, under the fence with no lease, the floor `(g+1, 0, null)`. Rejected: a marker row, a carrier file per generation, and a `carrier_capacity_pause` row.
  - **The successor rule.** When the last row is a `TERMINAL` in G:
    - a witness naming G+1 reconciles against the successor's empty tail;
    - any other witness reconciles against the `TERMINAL` row. There, OK or ADVANCE is the new action **OPEN**, which writes only the witness `COMMITTED (G+1, 0)`. REVERT is QUARANTINE, because no record can follow a `TERMINAL`.
  - **Who opens.** Any authorized writer performs OPEN, as it already performs INIT. Rejected: OPEN only under `EXCLUSIVE`.
  - **Tails.** The start tail, the confirmation tail and the floor copy tail are each fixed by the item.
  - **Checks.** A predecessor check runs at every writer open: the newest generation's predecessor must be closed by a `TERMINAL` in G − 1. G = 2^63 − 1 is the invariant row.
- **New item 5a, the capacity window and the exact trigger.**
  - **The defect.** The carrier admits `TERMINAL` at any `seq`. X3b-2 at product 9dbefb9 builds it only at tail `9007199254740990`. X3d r3 item 3 lets a `SEAL` take `…990`, and that `SEAL`'s end-path `REV` and `CLN` then have no ordinary slot.
  - **The rule.** A `SEAL` is admitted only at tail ≤ `…987`. `RA`, `REV` and `CLN` are admitted up to `…990`, as before. `TERMINAL` is admitted only at tails `…988` to `…990`, and only from item 13.
  - **The trigger** is "the open generation's tail is ≥ `9007199254740988`" (no `SEAL` fits). X3d item 3's `…990` threshold is superseded through an exported `seal_fits` predicate.
  - **Refusals.** `REV`, `CLN` or `RA` at `…990` is `GenerationFull`, which takes the busy row and is not an invariant.
  - The item states why closing earlier than v2 §5.4's "when the tail reaches `…990`" is the same cause.
  - **Rejected:** keeping the single slot, closing on request, and a wider window.
- **New item 13, the rollover operation**, called from the end step's new step 3. In order:
  1. a precondition that every journal outcome was certain;
  2. one up-front reservation on the attempt ledger;
  3. `EXCLUSIVE` in X2 item 7's order, skipping if busy;
  4. an observation and decision table, including `AlreadyRolled` and a floor-regression check before any write;
  5. the token: `op-` plus 16 CSPRNG bytes, fresh per attempt and distinct from the released operation's; and `wallClockData` from one clock sample;
  6. the `TERMINAL` append through item 5;
  7. OPEN;
  8. release.

  The item also covers the g+1 floor written by the end step after release, uncertain outcomes, a crash-state table and the outcomes.
- **Amended:**
  - item 3 (OPEN joins the floor table's reconcile outcomes);
  - item 4 (the start applies item 4a; the end step gains step 3 and reads the witness to choose its copy tail);
  - item 5 (the `TERMINAL` bullet, and the narrowing of whole-generation `REV` closure, which is not claimed);
  - item 6 (the rollover's own lock);
  - item 8 (the r7 rows);
  - item 9 (the rollover budget);
  - item 10 (F32's journal half);
  - item 11 (the r7 tests);
  - item 12 (the new code unit **X3b-4**, its relation to X7b and X3d-1, and X3b-3 threading the exhaustion);
  - the forbidden substitutes and the not-claimed list.

Nothing else changed.

## Read

- **Arch** (`docs/implementation/m2/` unless stated otherwise):
  - `journal-x3b/PROPOSAL.md`, `PROPOSAL-r6.md`, and the earlier X3b reviews (`reviews/grok-journal-x3b-r*`, `reviews/grok-ledger-x3c-r*-x3b-r*`, `reviews/grok-journal-append-x3b2-r1`);
  - `finalization-x7/PROPOSAL.md` (X7 r3) with `reviews/grok-finalization-x7-r3`;
  - `commit-session-x3d/PROPOSAL.md` (X3d r3, items 3, 7 and 8);
  - `ordinary-platform-x1/PROPOSAL.md` (item 5);
  - `project-root-x2/PROPOSAL.md` (item 7);
  - `docs/coop/design-corrections/security/grant-journal.carrier.v3.sql` and `carrier-format.v3.md` (§4, §5, §7, §8 and §8.1);
  - `docs/coop/completion/security-completion.v8.md` §5.4 to §5.6, and `security-completion.v2.md` §5.4.
- **Product** at 9dbefb918aa2fb10848e6203fb0cb79338c7ce2f, read-only: `crates/security/src/journal_store/carrier_floor.rs`, `carrier_start.rs` and `carrier_append.rs`, and `crates/security/src/journal_store.rs` (`reconcile_observations`, `terminal_body` and the prefix reader).

## Decide

1. Does r7 meet X7 r3 item 6's dependency, with each element defined exactly?
2. Is item 5a's window right? Is its trigger the exact condition, and is the X3d threshold change sound? Or should r7 keep the single reserved slot?
3. Is item 4a's successor rule complete and consistent with the frozen `reconcile_witness` and the floor table? Are all crash states found and reconciled?
4. Does anything in item 13 violate S7: a floor write under a lease, a wait, a second gate, a fence of its own, or a gate-ledger charge?
5. Is the `op-` token and `wallClockData` minting lawful?
6. Is anything else wrong?

`review.json` must contain the top-level members `verdict` (`ACCEPT` or `REQUIRED-FINDINGS`), `requiredFindings` and `subjectSha256`. Write `REVIEW.md` and `review.json`. Do not commit.
