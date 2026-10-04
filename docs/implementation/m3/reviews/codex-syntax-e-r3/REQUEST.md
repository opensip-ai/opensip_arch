Codex review: **M3-E1 r3**, the syntax crate and grammar registry law. Claude Opus 5.5 leads, and you are the single reviewer. This is a **law and contract-soundness** review, round 3. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/codex-syntax-e-r3.

**Rules:**
- Read-only. No repository edits, commits, pushes or delegation.
- No product builds, cargo or test runs: a timing-sensitive crash-matrix run is using this machine. The lead keeps the native lane.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read the 413 fixture.
- If you compute digests, counts or schedules, use read-only scratch scripts under your review directory.
- Read-only crates.io and GitHub API calls are allowed. Do not download or build upstream sources.

## Subject

- **The subject:** `docs/implementation/m3/syntax-e/PROPOSAL.md`, r3. It is the subject of `subjectSha256`. It is untracked in arch until acceptance.
- **The previous revision:** `docs/implementation/m3/syntax-e/PROPOSAL-r2.md`. It is byte-identical to your r2 subject (`c9287db9…`, 104,394 bytes). Your r2 review is in `/tmp/opensip-implementation/reviews/codex-syntax-e-r2/`.
- **Pins:** `hashes.txt` pins the subject, both earlier revisions, this request and the context files.
- **The product:** `/Users/sb/code/opensip-ai/opensip` at main `3e64266`, read-only.

## What r3 changes

The "r3 changes and review responses" table at the top of PROPOSAL.md maps each finding to its change. Every fix follows yours, with the lead's stated preferences.

1. **E-R2-01, the body-union bound (items 11 and 14a).**
   - The candidate bounds now include the envelope's `sourceBodies` limit of **100,000**, computed over the **union of member ids of the retained groups**.
   - Group retention is one declared rule:
     - a group of more than 4,096 members is withheld whole;
     - the remaining groups are ordered by ascending group digest;
     - the **longest prefix** within 1,000,000 groups and 100,000 member ids is retained;
     - every later group is withheld whole.
   - Every retained member keeps its custody row. Any withholding gives `partial`/`budget-exhausted`/null, subject to precedence. An envelope that withheld anything is never `complete`.
   - The case table and E3-T9 now include the 100,000 / 100,001 distinct-id boundary across individually valid groups, admitted by the existing execution-input owner.
2. **E-R2-02, the normalization map (item 4, A3 and A6, SYN-NS).**
   - The lead's preference is taken: the closed tree has **two declared roots**, the bundle manifest and IE's fixed map at `opensip-interface/normalization/specification-map.v1.json`.
   - The map must be canonical (IDS:2858-2910), with `normalizerId` equal to the manifest's and exactly the four levels L0 to L3.
   - Exactly its validated level-digest references resolve to the tree members at `opensip-interface/normalization/levels/<level>.v1.json`, with path, size, digest and byte joins.
   - The native normalizer stays a separate manifest member. Unrelated files still refuse.
   - IE's Run-closure joins are unchanged; A3 and A6 are their admission-side twins.
   - New key `-normalization-map-mismatch`. Controls E2-T33 to E2-T36 cover a positive complete closure, a missing map, missing or mismatched levels, and an unrelated extra file, on both branches.
3. **E-R2-03, the startup "mirror" (SYN-1 (f), E2s).**
   - SYN-1 (f) now states that `provider-startup.schemas.v1.json` has **no** `NativeCause` copy. Its `:83` and `:610` lists are the TypeScript post-Analyze `Unavailable.reason` vocabulary and are **unchanged**. Its Coverage entries reach the new member through the native URN reference.
   - SYN-1 names its NES selectors. SYN-1F names the five foundation copies by selector.
   - E2s now lists exact product selectors:
     - five schema sources, with `startup-v1` and `UnavailableReasonV3` untouched;
     - the cause lists in the four evaluator registries;
     - the closed eight-output generation registry, regenerated with unchanged outputs verified.
   - New controls: E2s-T1, a selector-level mirror check; and E2s-T2, the new cause admitted on `input-closure-incomplete` Coverage and candidate records while `Unavailable.reason` stays closed.

4. **Housekeeping.** The **C** short name now cites C's exact r3 bytes (`PROPOSAL-r3.md`, `2e455c70…`), which its line numbers match. It records C r5 (accepted in review by CODEX2), whose relevant provisions are unchanged. r2's `hashes.txt` had labelled the live r5 file "C r3". Both C files are pinned.

## Decide

1. **E-R2-01.** Does item 14a's retention rule, with the case table and E3-T9, satisfy EXS:994-1002 and EXC §6 in every case, with deterministic withholding and custody for every retained member?
2. **E-R2-02.** Do item 4's two roots and A3/A6 admit exactly a truthful closure, under IE:1068-1089 and IDS `normalizationSpecificationLaw`? Do they keep the native normalizer separate and refuse unrelated members, on both branches?
3. **E-R2-03.** Are the SYN-1, SYN-1F and E2s selector lists exactly the `NativeCause` and `allowedCauses` copies? Are the startup and `UnavailableReasonV3` vocabularies untouched, and are E2s-T1 and E2s-T2 adequate?
4. **Regressions.** Did any r3 edit contradict decisions you assessed as sound in r1 or r2? In r2 you confirmed: item 14a's other rows, X-C1, X-C2, the admission chain, `SymbolTableV1`, the static and execution routes, and E-R3's schedule.

## Output

Write REVIEW.md and review.json. review.json needs:
- `"verdict"`: ACCEPT or REQUIRED-FINDINGS;
- `"requiredFindings"`: each with id, location, problem or claim, evidence and fix;
- `"nonBlockingObservations"`;
- `"subjectSha256"`: PROPOSAL.md's sha256.

This is a law review, not a `verify_design` unit. SYN-1, SYN-1F and SYN-NS need `ACCEPT-DESIGN-UNIT` reviews of their own. X-C1 and X-C2 are reviewed in C's next revision. E2a, E2s, E2b, E2c and E3 are inventory units, reviewed with `ACCEPT-UNIT` and `inventoryCandidateAssessment`. Do not commit.
