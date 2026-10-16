# B3-B0-REFERENCE-r4 review

**Verdict: REQUIRED-FINDINGS.** One P2 validation finding blocks acceptance of these exact bytes.

Manifest SHA-256: `d01d4174a0b82cc45fa7a9ca43cfadce68e4d884faa9551964633f16ab16268f`. All six manifest members, all eleven successor parent pins and all five candidate pins match. Architecture HEAD is `16de973a1986ac07277df1ee6e7b9421cb430ff3`; product main is clean at `d47f9892d5709a1e108c4ecf9a9f60ed7aae12b2`.

## B3B0REF-R4-RF-1 — Validate every gitlink element before comparing paths (P2)

The per-element loop compares a validated g against every other h before validating those other elements. With memberGitlinks={"/h/w/a": ["sub", 17]} on an otherwise valid conventional candidate, discover raises TypeError (unsupported operand types for +: int and str) from _within, rather than ValueError("MEMBER_GITLINKS_INCONSISTENT:/h/w/a"). Reversing the same invalid entries to [17, "sub"] produces the documented rejection. Thus malformed-table rejection depends on element order, and the new validator does not implement its stated closed inconsistency contract. A non-mapping table also reaches .items without a shape check. These inputs fail closed; this finding does not claim a traversal bypass.

**Required change:** Validate the table/container shape and all element types and individual canonical paths before duplicate/prefix comparisons. Then check relationships only among validated strings. Preserve the documented MEMBER_GITLINKS_INCONSISTENT rejection for invalid keyed lists, and explicitly define the rejection for an invalid table container rather than exposing incidental Python exceptions.

**Validation:** Add invalid-element controls with a non-string before and after a valid string, plus non-list values and a non-mapping table. Assert the intended exception type and diagnostic, independent of element order, before discovery or item-6b consultation. Refresh the checker, evidence and exact pins.

## Requested judgments

**Gitlink semantics.** For valid tables, the new side table is separated from physical VCS observations. _gitlinks consults the candidate's values only after _six_b admits it. Input validation inspects the supplied table earlier; that is validation, rather than applying excluded candidates' gitlinks to discovery. _finish projects admitted directory gitlinks into the pass-two boundary representation, population pruning limits which evidence reaches SLM, and the upward fields are restored from pass one. The result records nested-repository paths rather than fabricated VCS records. The link filter precedes provider-manifest reads. An absent or regular-file target does not become a directory boundary.

Additional read-only probes confirmed:

- Gitlinks at member .opensip, .git, node_modules and a known Cargo target do not reveal their interiors or add those anchors as nested repositories.
- At absolute W-relative depth 256, automatic discovery records the boundary and omits its descendants. At depth 257, automatic discovery follows the existing marker-only depth policy and does not export the injected VCS flag. An exact root through the boundary at either depth refuses JOIN_CROSSES_NESTED_REPOSITORY without the descendant entering the population.
- A gitlink hidden beneath a nested project is not exported past that project; a sibling gitlink and nested project remain separate repository/project boundaries. The upward vcs record remains null in the sibling probe.
- A branch-B candidate refused by item 6b stays the physical repository boundary; its supplied gitlinks do not become admitted boundaries.

These probes found no boundary/evidence leak. The table validation defect is separate.

**Branch-A order.** The implementation returns size and global-grammar gate records through refused, using the no-members result only for provenance. It uses SLM's code/D9, source-specific size detail, and raw malformed path or null. Placement/volume checks, cap, then custody plus 6b per candidate preserve A4's priority and short circuit. The member-aware walk follows admission and clears member/config rows on refusal while retaining declaration rows. On acceptance, the reference recomputes the same pure pass-two result with the final declaration rows; this documented recomputation is not the removed unrestricted native trial.

The two revised rf2 families are the specified absent-before-layout and crossing-before-layout cases, under both sources. Their new layout-refusal outcomes match A4. Existing grammar, member-then-absent and member-decisions-in-path-order results remain, with added grammar-path/no6b assertions.

**LD-14 to LD-16.** LD-14 preserves membership by placement independently of whether a provider lies within the analyzed tree: the index boundary suppresses its link and read. LD-15's glob argument holds for admitted members: M is already a visible physical repository, so any literal prefix comparable to a gitlink within M is already comparable to M. Pruning, an intervening project or excessive candidate depth prevents admission rather than hiding an admitted M from that visible set. LD-16 correctly distinguishes pre-admission positive placement lookups from the forbidden walk/listing/custody/read inside a gitlink; a device change found during those permitted lookups follows the settled member-rule priority.

**Controls and spies.** The union of walker_population outputs across calls makes notWalked sensitive to an earlier unrestricted trial even if a later pass corrects the record. It proves absence from the reference's modeled walk population, not every dictionary access used to construct that population. The verdict/gitlink get spies cover the reference's actual consultation methods, so no6b checks the promised gate behavior. The 42 new cases and paired controls cover A4's principal boundary, priority and access requirements. The five invalid-table cases omit the mixed-type/container defect above.

I reproduced all six negative-control mutants in memory against the checker cases. Their failed-case sets exactly match the archived artifact: respectively 7, 3, 18, 2, 12 and 5 failures for boundaries, links, grammar, size, old trial and validation. None required repository edits or persistent mutant files. The grammar mutant is caught through exceptions as well as wrong outcomes; its label should not be read as proof that it cleanly implements every detail of r3.

**Successor.** The eleven parents are exactly the inherited r3 parents plus r3's reference and successor record. The five candidates are the README, checker, checks, negative controls and new reference. The manifest additionally pins successor.json itself. Empty passageOverrides is appropriate for this separately bound reference successor: no contract passage is replaced. The lead's synthetic successor-169 verification receipt is supporting evidence of binding compatibility, not actual integration or qualification.

**B3B0REF-R4-NBO-1 — No-member equality is regression coverage, not a universal equivalence proof.** All 64 existing discovery cases remain equal, but global grammar priority intentionally changes some inputs even when no member is ultimately admitted, for example ["missing", "../bad"]. The new D15 cases bind that documented change. The 64-case result is valid as stated; it must not be generalized to all no-member inputs or to every behavior outside a supplied member set.

## Verification and limits

The permitted checker ran with the pinned Python 3.14 interpreter: 64/64 equality cases and 115/115 D15 cases pass, with 173 valid V3 records and 94 valid accepted inventories. Its fresh JSON exactly equals the archived checks.json. To honor the user's two-file output limit, its temporary output used review.json, which this final review replaces; no checks.json was created in the review directory.

The additional inputs and in-memory mutants used read-only imports from this directory with bytecode writing disabled. No Cargo, census, lane, network, other panes or delegation was used. No protected fixture, installation directory, signing key, held tree or T2 held-out entry was read. Neither repository nor any control file was edited. Only REVIEW.md and review.json in the requested directory were written.
