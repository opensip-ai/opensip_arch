# Review request: D3A-3-r2 (discard, admission gating, records and the outcome route; M3-D r5 items 20 to 22; D3a plan r4 sub-unit D3a-3), round 2

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-d3a-3-r2/`).

## Boundaries

- Do not edit either repository, the worktrees or the control files.
- Do not run Cargo, rustc, builds or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees, any T2 store or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries; in the candidate worktree, `python3 -I -B tools/check_operability.py source --repository .`.

## Subject

- **Manifest:** `docs/implementation/m3/supervisor-d/d3a-3-r2-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 22221 bytes, SHA-256 `ad3da9c24123ade090e4e645f7ab5c9446cee22615893d0d783b7ac7689c6484`, 92 members. Rehash every member.
- **The candidate worktree:** `/Users/sb/code/opensip-ai/opensip-d3a3`, detached at product main `5de9fd4740ea17018d0bd3fbff9496c94ddacda9`, holding the exact bytes `product-map.json` lists: 15 files, 1 new (`crates/components/src/supervisor_records.rs`).
- **Your round 1:** `codex-d3a-3-r1` (REQUIRED-FINDINGS: D3A3-R1-RF-1, RF-2), at `/tmp/opensip-implementation/reviews/codex-d3a-3-r1/` and copied under the architecture repository's `docs/implementation/m3/reviews/`. The round-1 package `d3a-3-r1/` is history.

## Authority

- **M3-D r5** (`docs/implementation/m3/supervisor-d/PROPOSAL-r5.md`): item 20 (:664-679), item 21 (:681-702) and item 22 (:705-731), as LD-D3A-17, LD-D3A-18 and LD-D3A-19 amend them.
- **The D3a plan r4** (`d3a/PLAN-r4.md`): §3's D3a-3 row, its controls and its mutations; LD-D3A-3, LD-D3A-10 and LD-D3A-11.
- **S-OP-2 r6** (`docs/implementation/m3/operability/s-op-2/PROPOSAL-r6.md`): item 2 (the name grammar), item 3 (registration, provenance, ordinary registration), item 4 (asserted values), item 23 (:853-890), C-2 and C-4.
- **The carried observations:**
  - D3a-1's D3A1-R2-NBO-1 (`reviews/codex-d3a-1-r2/`);
  - D3a-2's D3A2-R1-NBO-1 (`reviews/codex-d3a-2-r1/`, recorded in `d3a-2-r1-unit.json` as carried to D3a-3).
- **The lead's decisions in SCOPE** (LD-D3A3-1 to LD-D3A3-11). The coordinator assented to LD-D3A3-1 to -4 before the code.

## What to review

`SCOPE.md` opens with a "Round 2" table. Judge each finding's resolution exactly as you requested it:
1. **D3A3-R1-RF-1:**
   - **the six registrations:** `tool.limit.breached`, `.sample.incomplete`, `.wait.expired`, `.teardown.started`, `.scratch.retained` (its three typed shapes) and `.child.settled`. Each is Project-only, with no role or universe, and has its emission on `ProjectScope`, its reader descriptor, its C-2 inventory row and its budget slot (`BUDGET_EVENTS` 29);
   - **the routing:** `RecordFact::for_tool`, applied to every fact of the tool class; no provider-only fact for a tool; `RecordFact::requires()`;
   - **the control:** the normal, timed-out, output-bound, sample-failing and scratch-retaining tool paths each produce only Project-only facts, and all eight tool events are produced; a provider's facts each need Project, Plan and Execution;
   - **no fabrication:** no Plan, Execution, role or universe is invented.
2. **D3A3-R1-RF-2:**
   - **the mechanism:** the pending write carries its record, which is made once on the full write, kept across short writes and `WouldBlock`, and dropped on a failed or abandoned write;
   - **the controls:** queued, partly written (three bytes), complete, an injected `EPIPE` on the queued cancel, and a child whose control reader closes;
   - **unchanged:** control-session validation and sequencing.
3. **The carried obligations** (`carried-obligations.json`): is each open obligation listed, with a reasonable proposed owner? The coordinator confirms the owners at assent.
4. **The lane** `evidence/d3a3-r2-checks/` and its attempt history:
   - the suites, with the base's isolation-flaky handshake failures as in round 1;
   - Clippy, rustfmt, the workspace check, the edges, the feature scope, the environment exceptions, the operability census with the re-censused mint-audit rows, the closure and verify_design;
   - components 101 → 127 (17 new) with 0 candidate failures, the base's 9 isolation-flaky handshake failures each passing 6 of 6 in isolation, and operability 95 → 99;
   - the nineteen mutations, round 2's four among them;
   - **attempt 1:** its failed-write mutation went uncaught, because the early-closing reader never had a cancel queued; the injected-`EPIPE` control is added.
5. **No regression** in what round 1 accepted, and the rules:
   - no new mint call outside operability;
   - no environment read;
   - no `let _ =`;
   - no new dependency.

Write `review.json` as `{"verdict": "ACCEPT-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `D3A3-R2-RF-n` / `D3A3-R2-NBO-n`.
