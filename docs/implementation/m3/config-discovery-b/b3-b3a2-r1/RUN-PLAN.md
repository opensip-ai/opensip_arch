# B3-b3b: the blind held-out run of B3-b3a2's tool (run plan, under the B3-b3a2 gate)

**Lead record, 2026-10-17. For Codex's pre-run review with B3-b3a2 r1; nothing has been run.**

**Authority:**
- the owner's decision of 2026-10-16 (`owner-decisions/2026-10-16/HELD-OUT-T2-MARGIN.md`): the mechanical blind run;
- the B2-b4 plan r6 §2.5: the receipt and its lifecycle;
- the B3-b plan r2 amendment A5 (A5-2: "B3-b3b is the blind run of B3-b3a2's accepted tool").

Same method, population and disclosure allowlist as B2-b4c2 and B2-b4c3. The only change is that the margins are the full ledger's.

## Preconditions

1. **Codex accepts B3-b3a2 r1** with `runAuthorized: true`.
2. **B3-b3a2's code commit and lock are on product main,** with the tool and the member model at exactly the reviewed bytes:
   - `tools/security/discovery_census.py`: `6e52bd5b…99c6`;
   - `tools/security/discovery_member_model.py`: `582bad12…21f1`.

   The script asserts both, in the run worktree and on main.
3. **A clean detached worktree of main,** `/Users/sb/code/opensip-ai/opensip-b3b3b`.

## The run (`evidence/run_b3b3b_blind.py`), once

1. **Under the lane lock,** at nice 10, with a private 0700 TMPDIR and `PATH=/usr/bin:/bin`.
2. **The stale walker-only receipt is removed, in the run worktree only.** The reviewed `--held-out-blind` mode then runs exactly once. The lead sees only:
   - its one-line summary;
   - its exit code;
   - its stderr, which must be empty;
   - the receipt: ids, verdicts and per-mille margins.
3. **The ordinary mode** runs `--write`, then `--check`.
4. **The recorded comparison:**
   - the receipt's ids against the old receipt's;
   - its state;
   - per entry, whether each full-ledger margin is at or below the walker-only margin of the old receipt (expected everywhere, since the terms are non-negative and the walker is unchanged for repository trees);
   - which bindings changed (expected: `tool`, `closure` and the new `memberModel`);
   - which top-level census keys changed (expected: `entries`, `heldOutMargin`, and, on a failure, `failingEntries` and `caps`);
   - that every lead-readable row and every workspace row is unchanged.

## Outcomes

- **The run errors, a row is an error row, or stderr is non-empty.** Nothing is committed. The result goes to Codex and the owner as data, and the held-out margin stays outstanding.
- **Every row is measured.** Codex's post-run review of the receipt and the composed census record follows. Then:
  - the lead's assent;
  - a product commit of the receipt and the census record, with no inventory successor, since the paths exist;
  - B3-b3c.

  If any full-ledger margin is under 2×, the census records `fails (blind census)` and `returned-to-law`, and the caps go to the law (item 12). That is data, not a reason to rerun.

**The expectation, not a claim.** The B2-b4c receipt's tightest walker margin is ts-large-vitest's 39,008‰ edges. Over the 39 lead-readable repository rows, the D15 terms lower a walker margin by at most 60.5% (js-small-body-parser's edges: 7,825,194‰ to 3,088,589‰).
- The largest relative drops are on small trees. There the reader term's carrier custody and read (about 400 edges) is a large share of a small walk.
- Where a carrier names workspace globs, the member term's placement and listing adds more (ts-medium-smithy-typescript, poly-small-node-rs). No repository row starts an item 6b session.
- On the large trees the drop is at most about 17% (aws-sdk-rust's bytes: 2,995‰ to 2,488‰).

Even a 60.5% drop on the tightest held-out row would leave about 15,400‰. So every row is expected to hold.

## Not claimed

- No held-out content is opened or disclosed beyond the owner's allowlist.
- No new method, population or access.
- No workspace margin (B3-b3c).
