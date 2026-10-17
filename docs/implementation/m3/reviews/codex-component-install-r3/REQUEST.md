# Review request: CI r3, the law "component release installation and tree custody", round 3

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-component-install-r3/`).

## Boundaries

- Do not edit either repository, the worktrees or the control files.
- Do not run Cargo, rustc, builds or lanes. Do not take the shared lane lock.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, private test keys, held trees, any T2 store, the T2 cache or any held-out material.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries in both repositories.

## Subject

- **Manifest:** `docs/implementation/m3/component-install/proposal-r3-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 961 bytes, SHA-256 `6d9610db69ef71460881db947d6d52016a806a14bc347e293731a95b5d075e50`, 4 members. Rehash all four.
  - `component-install/PROPOSAL-r3.md` is the subject.
  - `PROPOSAL-r2.md` (`e514ee26…`) and `PROPOSAL-r1.md` (`286ebf5a…`) are history and unchanged.
  - `snapshot-plan-c/c2a/X-C2A-1-r1.md` is the input memo, not law.
- **Bases:** as the manifest names, product `b7538549` and architecture `a87c1234`.
- **Your rounds:** `codex-component-install-r1` and `codex-component-install-r2` (REQUIRED-FINDINGS: CI-R2-RF-1 to RF-5, NBO-1; rulings Q8 to Q10), at `/tmp/opensip-implementation/reviews/`.

## Authority

As in round 2. The primitives the law now selects:
- `crates/platform/src/filesystem/directory_publication.rs`: the stage, its prefix, same-parent publication and law 467 item 7's classes;
- `filesystem/directory_effects.rs` and `filesystem/file_effects.rs`;
- `crates/platform/src/work_ledger.rs`: `effect` and `ReservedPostchecks`, and the snapshot profile;
- `crates/host/src/snapshot.rs`:33-70, the read discipline;
- `crates/platform/src/process.rs`, D3a-0's walk prices;
- `crates/host/src/installation_termination.rs`:389-396, law 468's budget route.

## What to review

`PROPOSAL-r3.md` opens with an r3 changes table. Judge:
1. **R2-RF-1:** the stage as a prefixed sibling in the store; the same-parent rename; the final barrier on the store; the generation lookup's name rule; inert-stage exclusion; GC's census obligation; and CI-T19 and CI-T23.
2. **R2-RF-2:** V1, stage verification at the staging modes, and V2, the final prerequisites (final modes, association and `pin.lock`) before the rename. Neither constructs `RetainedTree`. Check CI-T24.
3. **R2-RF-3:** each final mode change precedes the barrier covering it, bottom-up, with `pin.lock` and `tree/` covered. Check P-1 to P-4 as CI-2's named platform obligations, and CI-T19's crash prefixes after metadata changes and barriers.
4. **R2-RF-4 and LD-CI-13:** `LostRace` ends the act, with its route, and nothing verifies the winner, resets or retries. Check CI-T25.
5. **R2-RF-5 and LD-CI-11 (r3):**
   - the admission bound `B` and its recipe table, with existing and new prices and worst-case counts, kept distinct from actual charges;
   - the reserved publication suffix under `WorkLedger::effect`, so that a shortfall prevents the rename;
   - the "publication uncertain" post-rename outcome;
   - LD-CI-12: no installer cleanup, with inert stages left to GC;
   - X-CI-1's owner and disposition;
   - CI-T22 and CI-T26.
6. **R2-NBO-1:** authenticated modes stay in the manifest and TreeCommitment evidence, and `generation.json` is unchanged.
7. **Your round-2 LD-CI-9 disposition points:** ER10a's pin under the read-session fence; no pin file created by an ephemeral read; a missing or invalid `pin.lock` failing `Pin` and never recreated; pin calls priced; and the close-on-exec descriptor.
8. **No regression** in what rounds 1 and 2 accepted.

Write `review.json` as `{"verdict": "ACCEPT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `CI-R3-RF-n` / `CI-R3-NBO-n`. Accepting this law accepts no code, binding or qualification.
