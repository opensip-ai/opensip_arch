# Review request: CI r2, the law "component release installation and tree custody", round 2

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-component-install-r2/`).

## Boundaries

- Do not edit either repository, the worktrees or the control files.
- Do not run Cargo, rustc, builds or lanes. Do not take the shared lane lock.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, private test keys, held trees, any T2 store, the T2 cache or any held-out material.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries in both repositories.

## Subject

- **Manifest:** `docs/implementation/m3/component-install/proposal-r2-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 770 bytes, SHA-256 `42fff5ee7288c0895c239a03f2e67b81954c0569824070e3c6cc5c80c928313e`, 3 members. Rehash all three.
  - `component-install/PROPOSAL-r2.md` is the subject.
  - `component-install/PROPOSAL-r1.md` is history and is unchanged (`286ebf5a…`).
  - `snapshot-plan-c/c2a/X-C2A-1-r1.md` is the input memo, not law.
- **Bases:** as the manifest names, product `b7538549` and architecture `a87c1234`.
- **Your round 1:** `codex-component-install-r1` (REQUIRED-FINDINGS: CI-R1-RF-1 to RF-6, NBO-1; rulings Q1 to Q7), at `/tmp/opensip-implementation/reviews/codex-component-install-r1/`.

## Authority

As in round 1. In addition:
- the platform filesystem primitives the law now selects: `crates/platform/src/filesystem.rs`, `filesystem/directory_publication.rs` (private staging, exclusive publication and law 467 item 7's route classes), `filesystem/file_effects.rs` and `filesystem/directory_effects.rs`;
- `crates/platform/src/work_ledger.rs` (the snapshot profile);
- the snapshot session's read discipline, `crates/host/src/snapshot.rs`:33-70;
- law 468's budget route, as `crates/host/src/installation_termination.rs`:389-396 implements it;
- `schemas/sources/common-v4.schema.json` (the `WORK.BUDGET_EXHAUSTED` detail).

## What to review

`PROPOSAL-r2.md` opens with an r2 changes table. Judge:
1. **RF-1:** the capability carries the authenticated TreeCommitment and verifies the complete tree. That covers exact paths, types, symlink text, installed modes, and file lengths and digests, with extras and missing entries refused, and `generation.json` used only for association. Check the new typed failures and CI-T17.
2. **RF-2, LD-CI-10:** the installed-mode policy by entry type; staging at `0700` and `0600` with bottom-up finalization; no granted execution; no mode operation on symlinks; and CI-T18.
3. **RF-3:** the durable sequence on the selected primitives; the outcomes by law 467's route classes; restart recovery with no automatic replacement or retry; inert stages; and CI-T19's crash prefixes through the post-rename barrier.
4. **RF-4:** the pin (a shared `flock` on `pin.lock`, taken under the fence, kept across the lease handoff and released at operation end, with GC's exclusive non-blocking check); the bounded verified-byte transfer into the owner's sink; the Run releasing only after its own retention holds; and replay kept separate from WS pivot resolution.
5. **RF-5:** `NotInstalled` as a typed input to the existing owners; the detail qualified by RTC's committed-Run authority; X-8 carried as a gate; nothing minted or dropped; no ephemeral detail.
6. **RF-6, LD-CI-11:**
   - the priced installer operations;
   - the exact pre-acquisition cost, with `install-budget` as an admission refusal;
   - the snapshot-profile ledger as an interim reuse, under X-CI-1;
   - exhaustion during installation taking law 468's existing budget route;
   - signed capacities kept distinct from work limits and disk space.
7. **NBO-1:** CI-T1's exact 15 cases, with codec and capacity controls labelled separately, and the verified re-install no-op (LD-CI-6).
8. **The lead decisions** that need your judgement: LD-CI-5 (r2), LD-CI-6 (r2), LD-CI-9 (r2), LD-CI-10 and LD-CI-11, and the new open questions Q8 to Q10.
9. **No regression** in what round 1 accepted (LD-CI-1 to LD-CI-4, LD-CI-7, LD-CI-8, and the Q1 to Q7 rulings).

Write `review.json` as `{"verdict": "ACCEPT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...], "questionRulings": {"Q8": "...", "Q9": "...", "Q10": "..."}}`, with ids `CI-R2-RF-n` / `CI-R2-NBO-n`. Accepting this law accepts no code, binding or qualification.
