Codex review: the B3-b implementation plan r2 (multi-repository workspaces, D15: members, readers and the member-observation bound). A **plan review**. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only `REVIEW.md` and `review.json` under /tmp/opensip-implementation/reviews/codex-b3b-plan-r2.

**Rules:** read-only; no repository edits, commits, pushes or delegation; no product build, test, generator or census run (reading, hashing and `git show` / `git diff` are fine). Never touch `~/Library/Application Support/OpenSIP`, the private 413 UUID fixture, signing keys, or any T2 held-out store or overlay. No network.

## Subject

- **Subject manifest:** `docs/implementation/m3/config-discovery-b/b3-b-plan-r2-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted), SHA-256 `834bfe1450eff6096b651a05a69b1a8b97fd4f344d54fba00a16c7e97c2ab9ef`. It pins `b3-b/PLAN-r2.md` (diff it against `PLAN-r1.md`).
- **Bases:** product `/Users/sb/code/opensip-ai/opensip` at main `2b297e6` (clean); architecture at `2cd0bb7712b2c7d4663a2301ed70eaea27934001`.

## Authority to check the plan against

- Law M3-B r9 (`config-discovery-b/PROPOSAL-r9.md`): items 12 (the ledger, "Measuring the caps", the member-observation bullet), 19 to 24, and "Units after the law" (the B3-b row).
- Design unit B-S1 (`config-discovery-b/b-s1/`): `registry/workspace-declaration-readers.v1.json`, the schema additions, `PASSAGES.md`.
- The B2-b0 discovery reference (`b2-b-reference/`) and the B2-c0 native unit reference (`b2-c-reference/`).
- Product: `crates/security/src/custody/{git_tracking.rs,discovery_scan.rs,discovery_walk.rs,discovery_rule.rs}`, `tools/security/discovery_census.py` (its `CLOSURE`), `crates/security/src/custody/discovery_census_held_out.json` (the blind receipt's bindings).
- The owner decision of 2026-10-16 for the held-out margin (the mechanical blind run; `docs/implementation/m3/owner-decisions/` and the B2-b4 plan r6).

## Round 2

Your `codex-b3b-plan-r1` (`/tmp/opensip-implementation/reviews/codex-b3b-plan-r1/review.json`) raised RF-1 to RF-3 and NBO-1. The plan's "r2 changes" table resolves them. NBO-1's drift was remediated first as B2-b4c3: you accepted its pre-run gate (`codex-b2b4c3-prerun`) and its post-run review (`codex-b2b4c3-r1`), and the census `--check` passes on main `2b297e6`. **Judge first** whether each finding is resolved, then re-check the questions below against r2.

## Decide

1. **Coverage.** Does the plan cover everything the law and the B3-b unit row assign to B3-b (item 6b, the readers in both branches and root-in-repository, members in the V3 records, the link declaration half, item 24's rows, the item-12 member bound, and the law's controls in items 20 to 24), and nothing assigned elsewhere (C1/S4, S5, S6, B3-c, J1)?
2. **Decomposition.** Are B3-b0 (a reference wrapper over B2-b0, contract successor 168) and the product sub-units B3-b1 to B3-b3 sound, in the right order? Is supplying 6b's verdicts to the reference (LD-B3B-2) acceptable?
3. **The census closure.** Is LD-B3B-4 (re-pinning the closure with a byte-identical no-member census over every lead-readable entry) sound and sufficient? Is there a lawful way to avoid touching the closure that the plan missed?
4. **The blind receipt (LD-B3B-5).** Is a mechanical re-run of the reviewed blind mode within the owner's 2026-10-16 decision, or does it need a fresh owner decision?
5. **The T2 link-map control (LD-B3B-6).** Is reconstructing each lead-readable workspace with synthetic conventional `.git` members a lawful reading of item 20's first control, given that T2's assembly has no `.git` and B-S1 admits a member only by a `.git` directory?
6. **The link record (LD-B3B-3).** Is producing typed link rows with no published `WorkspaceLinkSetV1` record consistent with the law and the unit row?
7. **Anything else** that blocks acceptance.

Write `review.json` as `{"verdict": "ACCEPT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `B3BPLAN-R2-RF-n` / `B3BPLAN-R2-NBO-n`.
