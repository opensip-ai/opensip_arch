Codex review: M3-J1 r7, the guarded durable host pipeline. This is a **law review**, round 7. r7 is a **record revision of item 10 only**: it places one new outcome-matrix row, row 59, for the refusal accepted law M3-B r8 item 14a decides. Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only `REVIEW.md` and `review.json` under /tmp/opensip-implementation/reviews/codex-host-pipeline-j-r7.

**Rules:**
- Read-only. No repository edits, commits, pushes or delegation.
- No product build, test, generator or `verify_design` run is needed. Reading files and `git show` / `git diff` are fine.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read the private 413 UUID fixture, signing keys, or any held-out store.

## Subject

Repositories: architecture `/Users/sb/code/opensip-ai/opensip_arch` at `03c1c43ae` plus the uncommitted subject files below; product `/Users/sb/code/opensip-ai/opensip` at main `1f70dba` (167 contract successors, inventory v201), read-only.

- **The subject manifest:** `docs/implementation/m3/host-pipeline-j/j1-r7-subject.json` (its sha256 is in `hashes.txt` as `subjectSha256`). It pins one file, `docs/implementation/m3/host-pipeline-j/PROPOSAL-r7.md`.
- **The diff base:** `docs/implementation/m3/host-pipeline-j/PROPOSAL-r6.md` (`086e804a…`), the r6 bytes Codex accepted. Diff r6 against r7: every change must appear in r7's "r7 changes" table.
- **The sources** (pinned in `hashes.txt`):
  - `docs/implementation/m3/config-discovery-b/PROPOSAL-r8.md` (M3-B r8, Codex accepted in `reviews/codex-m3b-r8-r3`), item 14a, lines 567-680, especially "Refusals", "The public termination" and "The subject" (628-642);
  - successor S10: design unit S10-TSC (`config-discovery-b/s10-tsc/README.md`, `s10-tsc-unit.json`, its registry copy `s10-tsc/registry/public-detail-registry.v1.json`), Codex ACCEPT-DESIGN-UNIT in `reviews/codex-s10-tsc-r1`, bound as contract successor 167 at product lock `1f70dba`. Its product carrier is `crates/host/src/outcomes.rs` `REMEDY_TYPESCRIPT_CONFIG_UNRESOLVED` and the generated `Common4DomainDetailCode::NativeTypescriptConfigUnresolved`.

## What r7 changes

1. **Row 59** in item 10's table: request-rejected 2, `CONFIG.INVALID` (no fault cause), detail `native.typescript-config-unresolved` with S10's remedy keyed by that detail (never `CONFIG.INVALID`'s), subject the internal class and the project-relative path of the configuration file that refused, no runId or executionId; basis M3B8:628-642 and S10.
2. **A bullet after the table** recording that M3-B owns the row's content and J1 only places it (the r4 SD-6 precedent), and that B2-c2, the unit producing the keys, adds the observation and its test.
3. **J-C20** gains one sentence for row 59.
4. **Short name M3B8** for the r8 snapshot; every other M3B citation stays at r2's bytes.
5. **Header, the r7 paragraph and the "r7 changes" table; one Not claimed line.**

**Why a J1 revision.** S10-TSC's LD-4 (Codex accepted) said that adding the `Observation` variant for this refusal changes item 10's matrix and belongs to the unit that produces the keys, B2-c2. Item 10's totality bullet says a detail with no row is a model error (NE:3543). No existing row names this detail: row 12's is `CONFIG.INVALID` itself, and row 24 is the explicit-root row. M3-B r8 itself carries no cross-law item for J1. So the lead places the row by record revision before B2-c2's code cites it.

## Decide

1. **Fidelity.** Is row 59 exactly what M3-B r8 item 14a and S10 fix: class, exit, code, absent fault cause, detail, remedy key and subject? Does r7 add anything no source states?
2. **Placement.** Is a new row, rather than an edit of rows 12 or 24, the lawful placement? Is a J1 record revision the right instrument, with no M3-B or NE change?
3. **Completeness.** Does r7 leave item 10's other rows, its "existing codes only" heading (the detail is S10's, not J1's), J-C20's other sentences, and items 13 and 14 unchanged and consistent?
4. **Anything else** that blocks acceptance.

Write `review.json` as `{"verdict": "ACCEPT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `J1R7-R1-RF-n` and `J1R7-R1-NBO-n`.
