# Review request: B3-B0-REFERENCE-r2 (the members-and-readers reference; contract successor 168)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b3b0-reference-r2/`).

## Boundaries

- Do not edit either repository or the control files.
- Do not run Cargo, tests, the census or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees or any T2 held-out entry.
- Do not use other panes and do not delegate.
- **Permitted:**
  - read-only reading, hashing, JSON parsing and Git queries;
  - running the checker, `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B /Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/config-discovery-b/b3-b-reference/evidence/check.py --architecture /Users/sb/code/opensip-ai/opensip_arch --reference /Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/config-discovery-b/b3-b-reference/reference/member_reader_reference.py --packages-root /Users/sb/code/opensip-ai/opensip --out <your dir>/checks.json`;
  - importing the reference read-only in a scratch script under this directory, to try your own inputs.

## Subject

- **Manifest:** `docs/implementation/m3/config-discovery-b/b3-b-reference-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted), SHA-256 `1def8904959c1ec347969dcc9b8c88d73077c09d0065779621ed5c9d2a2a8db6`, 5 members: the README, the checker, `checks.json`, the reference and `successor.json`.
- **Bases:** product main `2b297e68e07aeae31a3fe71b6fb227f9758dcc5a` (167 contract successors), architecture `67b8f8bcaa6e25804a61b56693a87b6b39da311e`.
- **The lead's scratch binding:** `lead-verify-scratch.json` in this directory. `verify_design` passes with a synthetic successor-168 entry.

## Authority

- Law M3-B r9, items 19 to 24 (`config-discovery-b/PROPOSAL-r9.md`).
- B-S1: `b-s1/PASSAGES.md` (S3's multi-repository passage), `b-s1/schemas/security-lifecycle.schemas.v1.b-s1-additions.json`, and `b-s1/registry/workspace-declaration-readers.v1.json`.
- B2-b0 (`b2-b-reference/`, contract successor 164).
- The B3-b plan r2, section 1 (`b3-b/PLAN-r2.md`; your `codex-b3b-plan-r2`), and its carried NBO-1 (the `vcs: none` seam) for B3-b2.

## Round 2

Your `codex-b3b0-reference-r1` (`/tmp/opensip-implementation/reviews/codex-b3b0-reference-r1/review.json`) raised B3B0REF-R1-RF-1 to RF-4. The README's "r2 changes" table resolves them: pruned anchors are never entered or read (with read-spy controls); branch A is SLM-first (with mixed-failure controls for both sources); there is one VCS representation (with side-table controls); and the depth bound applies to the candidate. **Judge first** whether each is resolved, re-running your reproductions. Then re-check the questions below against r2. LD-B3B0-7's extended use of `entry-not-in-a-member` and the `DEPTH` subject (LD-B3B0-3) are the lead's choices of existing vocabulary; rule on them explicitly.

## What to review

1. **Fidelity.** Does `discover` implement the registry and law items 19 to 24 exactly? Cover both branches, root-in-repository, placement and `membershipByPlacementOnly`, the cap (counted after placement and before 6b, in both branches), every unresolved reason, the carrier states, the links and ambiguity, `memberConfigs`, members entered as ordinary directories with their nested boundaries kept, and SX-1 at member roots. Construct inputs where it might deviate.
2. **No-member equality.** Is equality with B2-b0 on all 64 discovery cases (every non-D15 field) the right proof that nothing else changed? Is the pass-two construction (withheld member evidence, bound rule, population rule) sound?
3. **The lead decisions LD-B3B0-1 to 12,** especially:
   - **LD-B3B0-3:** the placement vocabulary, and which failures refuse in branch A versus fall to SLM's crossing;
   - **LD-B3B0-4:** `absent` reader rows on a selection refusal;
   - **LD-B3B0-5:** the refusal provenance;
   - **LD-B3B0-6:** the order;
   - **LD-B3B0-7:** an entry inside a member's inner boundary;
   - **LD-B3B0-9:** the waiver's reach.
4. **The checks.** Are the 42 hand-written D15 expectations the law's? Is anything the registry or items 19 to 24 name left uncovered?
5. **The successor record.** Are its parents and candidates right for a contract successor that changes no contract text, with no passage override?

Write `review.json` as `{"verdict": "ACCEPT-DESIGN-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `B3B0REF-R2-RF-n` / `B3B0REF-R2-NBO-n`.
