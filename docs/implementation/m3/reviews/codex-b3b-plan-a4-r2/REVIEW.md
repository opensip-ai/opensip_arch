# B3-b plan r2 amendment A4, round 2

**Verdict: ACCEPT.** No required findings or nonblocking observations.

Subject: `docs/implementation/m3/config-discovery-b/b3-b/PLAN-r2-A4.md`, 8,857 bytes, SHA-256 `f85a0751db3aebde3256e3932fc79d6b29a3e2b5bad21c36c0ded47aa613b486`. Size and hash match the request. Architecture HEAD is `5c581b5c5a4e22ff3fa28d5e9f522df92a27c4a0`; product main is clean at `d47f9892d5709a1e108c4ecf9a9f60ed7aae12b2`.

## Previous finding

**B3BA4-R1-RF-1 is resolved.** A4-2 now selects the array-gate refusal directly. The no-members walk supplies provenance, and its ordinary discovery verdict cannot replace the selected gate verdict. This fixes the earlier repository/absence/custody-before-later-grammar counterexamples.

The gate matches the owning SLM records:

- More than 4,096 roots: `PROJECT.EXPLICIT_PATH_INVALID`, null path, `TOO_MANY_JOINS` for explicit joins or `TOO_MANY_WORKSPACE_ROOTS` for config roots.
- Otherwise, the first malformed root in array order: the same code, `JOIN_PATH_GRAMMAR`, and the raw string path or null for a non-string.
- Both use request-rejected / exit 2 / `CONFIG.INVALID`.

These agree with SLM's `_explicit_units`, its source-specific call sites and D9 map, and the shared rule's `MAX_WORKSPACE_UNITS = 4096`. The amendment explicitly chooses no-members discovery provenance and documents the intentional global-grammar priority over an earlier root's ordinary walk refusal. Size-before-grammar is explicit. The planned controls retain both existing grammar families, add the mixed-failure arrays under both sources, require exact records and no item-6b consultation, and cover 4,096 versus 4,097 roots.

## Requested judgments

**Necessity and order.** Within the accepted model, gitlinks are obtained through item 6b. An unrestricted member-entering trial before that observation cannot preserve index-only boundaries, and a later re-walk cannot undo forbidden descent. Moving member decisions before the member-aware walk is a sound resolution. A speculative index prepass would itself change the accepted observation order.

The amended order supplies admitted gitlinks before descent. Placement and counting precede the cap; the cap precedes member Git configuration/index reads. Directory custody and item 6b then run together per candidate in path order, stopping at the first refusal. The clarified short-circuit scope correctly permits the earlier placement observations needed to form and count candidates. A member-rule refusal still uses a no-members provenance walk, whose physical repository boundary at M prevents provisional entry into that member.

The settled public priority—array size, global grammar, member rules, then walk refusals—is acceptable under the explicitly permitted change to LD-B3B0-6. It is now described as a change rather than equivalence to SLM's per-root priority. Branch B remains unchanged in its ordering.

**Reference binding.** A separately reviewed B3-b0 r4 with `memberGitlinks`, bound as successor 169 before product use, is the appropriate authority route. The proposed reference must consistently apply admitted gitlinks to population, nestedRepositories, exact crossings and link exclusion; it need not fabricate filesystem VCS observations or change B2-b0, SLM or the schemas. Its input validation and actual boundary behavior remain matters for that design review.

The revised checker families are correctly identified: `rf2-*-absent-before-layout` and `rf2-*-crossing-before-layout`, each under configWorkspaceRoots and explicitJoins. The existing grammar families can retain their results with the corrected gate. The proposed failing-interior, custody-below-gitlink and mixed-member controls address the original ordering finding; their access assertions must prove lack of traversal as well as output equality.

**Product step and retained obligations.** Removing the trial phase and TrialRefused from the decision core, regenerating vectors from bound r4, and performing one member-aware walk is coherent. A final walk refusal must still clear member rows and retain the specified declaration rows. A4-4 explicitly carries forward the reopened-ancestor/Git-evidence binding and repeated-provider-read fixes from B3B2B2B-R2-RF-2/RF-3. Plan acceptance does not declare those implementation findings fixed.

A3's retained-object binding, one discovery ledger, no-follow access, custody capture, non-latching refusal handling, access controls and scenario obligations remain. A1's closure re-pin/equality obligations remain where code changes closure files. B3-b2b2c's T2 controls and joint sweep, and B3-b3a/b/c's bound, gated refresh and margins, remain in the stated sequence. Neither the future reference nor the product implementation is accepted by this plan verdict.

## Review limits

This was a read-only plan review against the stated authorities and previous findings. I verified the exact amendment hash, bases, SLM refusal logic and source-specific details, the shared limit, and the existing checker case identities. No tests, builds, reference execution, lane, network, other panes or delegation were used. No protected fixture, installation directory, signing key, held tree or T2 held-out entry was read. Only REVIEW.md and review.json in the requested directory were written; neither repository nor any control file was edited.
