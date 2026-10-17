# Review request: D3A-4-r1 (the four record events S-OP-2c unblocks; M3-D r5 item 21 with S-OP-2c item 23a), round 1

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-d3a-4-r1/`).

## Boundaries

- Do not edit either repository, the worktrees or the control files.
- Do not run Cargo, rustc, builds or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees, any T2 store or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries; in the candidate worktree, `python3 -I -B tools/check_operability.py source --repository .`.

## Subject

- **Manifest:** `docs/implementation/m3/supervisor-d/d3a-4-r1-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 20,964 bytes, SHA-256 `27819282a9b8821dc54d0c8f11f6cc1ced7f94ed4c5e8ea59454261b41051736`, 86 members. Rehash every member.
- **The candidate worktree:** `/Users/sb/code/opensip-ai/opensip-d3a4`, detached at product main `2ead5cf1796bb85f363c34fa8ff8fba715462369` (S-OP-2c bound as contract successor 177 at `d704ed4`), holding the exact bytes `product-map.json` lists: 16 files, no new path.

## Authority

- **S-OP-2 r6 item 23** (`docs/implementation/m3/operability/s-op-2/PROPOSAL-r6.md`:853-915), as **S-OP-2c item 23a** amends it (`operability/s-op-2c/PROPOSAL.md`; your `codex-s-op-2c-r1`, ACCEPT-DESIGN-UNIT, with SOP2C-R1-NBO-1). Also S-OP-2 item 3 (ordinary registration) and C-2.
- **M3-D r5 item 21** (`supervisor-d/PROPOSAL-r5.md`:681-702); M3-L r1's spans (`provider-protocol-l/PROPOSAL-r1.md`:396-406).
- **D3a-3 r2** (`d3a-3-r2/`, your `codex-d3a-3-r2`), its LD-D3A3-1 and BLOCKED-TABLES.md; the D3a plan r4's LD-D3A-10.
- **The coordinator's LD-D3A4-1:** register only the tables D3's events use.

## What to review

1. **The tables:**
   - **membership:** `StageKind`, `ProviderState`, `ChildSignal`, `ProviderReason` and `StageTerminal`, each equal to S-OP-2c item 23a's members and provenance, member for member and in order;
   - **`ChildSignal`'s comment:** does it describe the set as the chosen common subset (SOP2C-R1-NBO-1)?
   - **`Signal`:** is leaving it to `host.signal.received`'s owner right (LD-D3A4-1)?
2. **The four events:**
   - fields, kinds, classes, optionality, levels, identities and export against SOP2:879-881 and :886, with `provider.process.reaped.signal` taking `ChildSignal` (SOP2:881 as S-OP-2c amends it);
   - the typed builders enforcing S-OP-2c's presence rules: `reason` exactly for `unavailable`, and `signal` only for `signaled` with a member;
   - the emission on `PlanAttemptScope`, the budget slots (33), the reader descriptors, C-2's inventory, and the regenerated references.
3. **`tool.process.reaped`'s `signal`:** an ordinary field (S-OP-2c LD-OPT-4's "also usable by").
4. **The platform's `TerminatingSignal`:** mapping only by the pinned `libc` constants, `None` otherwise, and its control's macOS numbers.
5. **The record facts and spans (LD-D3A4-3 to LD-D3A4-5):**
   - the phase changes, never repeated;
   - the stage terminal once, or `crash` for an analyzed provider with no terminal, and none for one that never analyzed;
   - the frame counts;
   - the analysis, teardown and `since` spans;
   - `stage` always `semantic-provider`.
6. **The participant seam (LD-D3A4-2):**
   - **additive:** three `Boundary` variants, and no new field, trait method or changed variant;
   - **`records::provider_state`**, the explicit phase map, checked against the vendored P3T and T2O lists.

   D2b-3b's `Ts2Participant` is to adopt it on rebase.
7. **Item 21:** is its provider and supervision set now complete, with no event registered in a reduced form?
8. **The lane** `evidence/d3a4-r1-checks/` (SCOPE's Checks: the base's 22 isolated-pass failures, the worktree's in-lock move onto main, and the two archived attempts): the suites, Clippy, rustfmt, the workspace check, the edges, the feature scope, the environment exceptions, the operability census with the mint audit, the closure and verify_design, and the eight mutations.
9. **No regression** in D3a-1 to D3a-3, and the rules:
   - no new mint call outside operability;
   - no environment read;
   - no `let _ =`;
   - no new dependency.

Write `review.json` as `{"verdict": "ACCEPT-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `D3A4-R1-RF-n` / `D3A4-R1-NBO-n`.
