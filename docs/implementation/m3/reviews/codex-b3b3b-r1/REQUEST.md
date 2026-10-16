# Review request: B3-B3B-r1, the post-run review of the blind held-out run over the full ledger (M3-B unit B3-b)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b3b3b-r1/`).

## Boundaries

- Do not edit either repository, the worktrees or the control files.
- Do not commit.
- Do not run Cargo, tests, the blind mode, or the run script.
- No network.
- Never read any T2 held-out store or overlay, the private 413 fixture, signing keys, held trees or `~/Library/Application Support/OpenSIP`.
- Do not use other panes and do not delegate.
- **Permitted:**
  - reading the receipts (ids, verdicts and margins only);
  - hashing, JSON parsing and Git queries;
  - in the run worktree `/Users/sb/code/opensip-ai/opensip-b3b3b`, `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B tools/security/discovery_census.py --check --architecture /Users/sb/code/opensip-ai/opensip_arch --packages-root /Users/sb/code/opensip-ai/opensip --t2-cache /Users/sb/code/.opensip-implementation-cache/t2-corpus-c8cc48e1`. The ordinary mode never opens a held-out store.

## Subject

- **Manifest:** `docs/implementation/m3/config-discovery-b/b3-b3b-r1-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 4241 bytes, SHA-256 `11dbbacd753b6d66ea39fe084d699c8fd0deadd42e870c91544799a87d4dff19`, 14 members, plus a `gate` list pinning the B3-b3a2 records. Rehash every member and every gate pin.
- **The run worktree:** `/Users/sb/code/opensip-ai/opensip-b3b3b`, detached at product main `ffd2c8e740177a33d6fdba04dc551465f863cb27`. The receipt and the census record are its only changes.
- **Architecture:** `f274442606631322246a0bb1765ed02f0bc0e68c`, which holds the gate: `b3-b3a2-r1/`, `RUN-PLAN.md`, `evidence/run_b3b3b_blind.py` and your `codex-b3b3a2-r1`.

## Decide

1. **The authorized run.** Did it follow `run_b3b3b_blind.py` exactly as authorized?
   - one blind invocation, empty stderr;
   - the tool and the member model at the reviewed bytes, on main and in the run worktree, after B3-b3a2's code was integrated;
   - only the stale receipt removed;
   - the lane, nice 10 and a private TMPDIR.
2. **The receipt.**
   - Is it in the closed format, with every row measured and every binding current against today's bytes?
   - Is `RUN-RECORD.md`'s explanation of the unexpected `sizes` binding change correct? That is, did B3-b3a1's size-inventory additions postdate the old receipt?
   - Is each margin at or below the walker-only one?
3. **The census record.**
   - Do only `entries` (the ten held-out rows) and `heldOutMargin` change from main's?
   - Are the lead-readable and workspace rows unchanged?
   - Are `failingEntries: []` and `caps: recorded-margin-holds` right?
   - Does the ordinary `--check` pass with the new receipt?
4. **Outcomes.** Under RUN-PLAN's outcomes, may the lead commit exactly these two files with no inventory successor?
5. **Disclosure.** Does anything in the record disclose held-out content beyond the owner's allowlist?
6. **The record's history.** Is `RUN-RECORD.md`'s history of `heldOutMargin` on main accurate, for status r102?

Write `review.json` as `{"verdict": "ACCEPT-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `B3B3B-R1-RF-n` / `B3B3B-R1-NBO-n`.
