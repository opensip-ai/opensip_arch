# Review request: B3-B0-REFERENCE-r4 (the members-and-readers reference with index gitlinks; contract successor 169)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b3b0-reference-r4/`).

## Boundaries

- Do not edit either repository or the control files.
- Do not run Cargo, tests, the census or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees or any T2 held-out entry.
- Do not use other panes and do not delegate.
- **Permitted:**
  - read-only reading, hashing, JSON parsing and Git queries;
  - running the checker, `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B /Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/config-discovery-b/b3-b-reference-r4/evidence/check.py --architecture /Users/sb/code/opensip-ai/opensip_arch --reference /Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/config-discovery-b/b3-b-reference-r4/reference/member_reader_reference.py --packages-root /Users/sb/code/opensip-ai/opensip --out <your dir>/checks.json`;
  - importing the reference read-only in a scratch script under this directory, to try your own inputs, and running a mutant of it from this directory.

## Subject

- **Manifest:** `docs/implementation/m3/config-discovery-b/b3-b-reference-r4-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted), SHA-256 `d01d4174a0b82cc45fa7a9ca43cfadce68e4d884faa9551964633f16ab16268f`. It has 6 members: the README, the checker, `checks.json`, `negative-control-r4.json`, the reference and `successor.json`.
- **Bases:**
  - product main `d47f9892d5709a1e108c4ecf9a9f60ed7aae12b2` (168 contract successors);
  - architecture `16de973a1986ac07277df1ee6e7b9421cb430ff3`.
- **The lead's scratch binding:** `lead-verify-scratch.json` in this directory. `verify_design` passes with a synthetic successor-169 entry.
- **The predecessor:** B3-b0 r3, `b3-b-reference/` (contract successor 168), unchanged. `diff -r` the two `reference/` and `evidence/check.py` files to see r4's whole change.

## Authority

- Law M3-B r9, items 19 to 24 (`config-discovery-b/PROPOSAL-r9.md`).
- B-S1: `b-s1/PASSAGES.md`, the schema additions and the reader registry.
- B2-b0 (`b2-b-reference/`, contract successor 164) and SLM at its pinned bytes.
- B3-b0 r3 (contract successor 168).
- **The B3-b plan r2 amendment A4** (`b3-b/PLAN-r2-A4.md`, your `codex-b3b-plan-a4-r2`, ACCEPT). A4-2 is branch A's order and public priority, and A4-3 is this unit's scope and controls.

## Why r4

Your `codex-b3b2b2b-r2` RF-1 showed that the product's branch-A trial walk crossed index-only nested repositories before item 6b reported them. A4 resolves that by deciding branch A's members before any walk. It makes B3-b0 r4 the authority: it models the index gitlinks as a supplied side table and binds the new order. Your plan review asked that the reference apply admitted gitlinks consistently to:
- the population;
- `nestedRepositories`;
- exact crossings;
- link exclusion.

It must not fabricate filesystem VCS observations, and the access assertions must prove lack of traversal, not only equal output.

## What to review

1. **The gitlinks.** Does `memberGitlinks` behave as A4-3 says?
   - It is consulted only on item 6b's admission.
   - In pass two, an admitted member's gitlink directory is a nested repository: never entered, recorded, and a crossing for an exact root.
   - An entry at or below it links nothing and reads nothing.
   - A gitlink with no directory bounds nothing.
   - The table is validated.

   Is giving the gitlink SLM's `vcs` boundary flag in pass two's input only, with only its path in the result, a faithful representation and not fabricated VCS evidence? Construct inputs where it might leak: a gitlink under a pruned anchor, at depth 256 or 257, beside a nested project, or in branch B with an excluded member.
2. **Branch A's order** against A4-2:
   - the gate's records, D9 and provenance, and size before grammar;
   - the member decisions in path order, with the short circuit;
   - one walk, whose refusal clears the members and keeps the rows.

   Are the two revised `rf2-*` cases, and the unchanged ones, exactly A4's priority?
3. **LD-B3B0-14 to 16:**
   - **LD-B3B0-14:** an entry below a gitlink still declares its member by placement, as one inside a physical nested repository does.
   - **LD-B3B0-15:** globs are unchanged by gitlinks, because every admitted member is itself a visible repository. Try to break this argument.
   - **LD-B3B0-16:** placement lookups may pass a gitlink's directory, and a device change found there is a member rule.

   LD-B3B0-6 is replaced as A4 says.
4. **The controls and spies.** Do `notWalked` (the wrapped `walker_population`) and `no6b` prove what they claim? Are the 42 new cases, the paired controls and the six negative-control mutants enough for A4-3's list?
5. **No-member equality.** It still holds on all 64 discovery cases. Is that still the right proof that nothing outside D15 changed, given the global grammar change? Equality holding means no SLM discovery case reaches a root where the order changes the result. The changed priorities are pinned only by the D15 cases.
6. **The successor record.** Its parents are r3's parents plus r3's reference and successor record. Its candidates are the five r4 files. Are these right for a successor that changes no contract text, with no passage override?

Write `review.json` as `{"verdict": "ACCEPT-DESIGN-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `B3B0REF-R4-RF-n` / `B3B0REF-R4-NBO-n`.
