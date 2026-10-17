# Review request: D3A-3-r1 (discard, admission gating, records and the outcome route; M3-D r5 items 20 to 22; D3a plan r4 sub-unit D3a-3), round 1

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-d3a-3-r1/`).

## Boundaries

- Do not edit either repository, the worktrees or the control files.
- Do not run Cargo, rustc, builds or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees, any T2 store or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries; in the candidate worktree, `python3 -I -B tools/check_operability.py source --repository .`.

## Subject

- **Manifest:** `docs/implementation/m3/supervisor-d/d3a-3-r1-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 20842 bytes, SHA-256 `a6e9a3c5f0a6490af9e82ce04ea910af317ede511c43b689251c243e779985dd`, 86 members. Rehash every member.
- **The candidate worktree:** `/Users/sb/code/opensip-ai/opensip-d3a3`, detached at product main `f05c5d5cda5f68aec607cdc8731c277e4e29491b` (D3a-2 integrated at `caa71e2`), holding the exact bytes `product-map.json` lists: 15 files, 1 new (`crates/components/src/supervisor_records.rs`).

## Authority

- **M3-D r5** (`docs/implementation/m3/supervisor-d/PROPOSAL-r5.md`): item 20 (:664-679), item 21 (:681-702) and item 22 (:705-731), as LD-D3A-17, LD-D3A-18 and LD-D3A-19 amend them.
- **The D3a plan r4** (`d3a/PLAN-r4.md`): §3's D3a-3 row, its controls and its mutations; LD-D3A-3, LD-D3A-10 and LD-D3A-11.
- **S-OP-2 r6** (`docs/implementation/m3/operability/s-op-2/PROPOSAL-r6.md`): item 2 (the name grammar), item 3 (registration, provenance, ordinary registration), item 4 (asserted values), item 23 (:853-890), C-2 and C-4.
- **The carried observations:**
  - D3a-1's D3A1-R2-NBO-1 (`reviews/codex-d3a-1-r2/`);
  - D3a-2's D3A2-R1-NBO-1 (`reviews/codex-d3a-2-r1/`, recorded in `d3a-2-r1-unit.json` as carried to D3a-3).
- **The lead's decisions in SCOPE** (LD-D3A3-1 to LD-D3A3-11). The coordinator assented to LD-D3A3-1 to -4 before the code.

## What to review

1. **Item 20's gate:**
   - `Settlement::release()` as the only way out;
   - `Participant::discard()` at every non-admissible settlement;
   - `TerminalOutput` holding the `Spool`;
   - the controls D3-T22 to D3-T24, the bad-commitment gate, and admission requiring the output.
2. **The registrations (LD-D3A-10):**
   - **the tables:** each provenance class and its source, the `protocol-enum` members against their schemas (the components control), and no member invented;
   - **the seventeen events:** fields, kinds, classes, optionality, assertion, levels, identities and export, against S-OP-2 item 23 and item 21;
   - **C-2 extended:** the transcribed inventory and its planted-difference controls;
   - **the `supervision_event!` macro:** optional and asserted fields, and the crate-private constructors with typed builders;
   - **`scratch.retained`:** its three shapes;
   - **the emission:** `EmitOn` on `PlanAttemptScope` and `ProjectScope`;
   - **the per-name budget slots** (`BUDGET_EVENTS` 23);
   - **the read-back descriptors;**
   - **the regenerated references** and O1's drift test;
   - **the mint audit:** the re-censused rows of `registry.rs`, a mint-owner file.
3. **The four blockers** (LD-D3A3-2; `BLOCKED-TABLES.md`). Is each table truly unresolved in every pinned source, and is blocking, rather than reducing, the right fate? Is item 21 rightly not claimed complete?
4. **The ordinary registrations:**
   - the `tool` domain and `IdentitySet::Project` (LD-D3A3-3), and O1's updated assertion;
   - the tool events' fields (LD-D3A3-4);
   - `supervision.liveness.missed`'s `miss` and `refusal_family` (LD-D3A3-5);
   - `supervision.sample.incomplete` (LD-D3A3-7);
   - `supervision.child.settled` for item 21's two-segment `supervision.settled` (LD-D3A3-11).
5. **LD-D3A3-1's two halves:**
   - `RecordFact`: mint-free, carrying no text, nonce, path or environment value;
   - `record_facts`;
   - each fact's completeness against its event's fields, the minted ones aside;
   - J2b's composition left to J2b, with no mint call outside operability.
6. **Each fact's values:**
   - a breach's observed value and unit (LD-D3A3-6, including the walk that could not finish);
   - the wait's configured bound;
   - the cancel as written;
   - the spans from the participant's boundaries (LD-D3A3-8);
   - the asserted resources, never progress;
   - the fault and refusal detail lengths.
7. **D3A2-R1-NBO-1:** `ESRCH` versus every other sampling failure, a failed listing, the disclosure once per change of shape, a partial sum never reported as complete, and the injected-error controls.
8. **D3A1-R2-NBO-1:** the projection of `LivenessMiss` into the record.
9. **The route (LD-D3A-11, LD-D3A3-9):** every cause's one route, no host-observed cause on the provider-protocol route, `userInterrupted` first, and the pre-spawn, zero-fit, spawn-failure and tool routes.
10. **C-4 with D3's fixture:** the canary in stderr and in a control `fault` detail absent from every fact, event and settlement, with its digest.
11. **The lane** `evidence/d3a3-r1-checks/` and its attempt history:
    - components 98 → 124, with 0 candidate failures, and operability 95 → 99;
    - **the base run's 12 handshake-deadline failures under load:** existing D3a-1 and D3a-2 tests, each passing 6 of 6 times in isolation. Judge whether treating them as isolation-flaky is right;
    - Clippy, rustfmt, the workspace check, the edges (components gains operability), the feature scope, the environment exceptions, the operability census, the closure and verify_design;
    - the fifteen mutations;
    - attempt 1's runner defect and the missing control, both fixed.
12. **No regression** in D3a-1's and D3a-2's provider and tool paths, and the rules:
    - no new mint call outside operability;
    - no environment read (the components test reads the pinned carrier schema through `CARGO_MANIFEST_DIR`, a compile-time path);
    - no `let _ =`;
    - no new third-party dependency.

Write `review.json` as `{"verdict": "ACCEPT-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `D3A3-R1-RF-n` / `D3A3-R1-NBO-n`.
