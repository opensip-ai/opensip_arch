# B3-B0-REFERENCE-r4, round 2

**Verdict: ACCEPT-DESIGN-UNIT.** No required findings or nonblocking observations.

Subject manifest SHA-256: `da0ee22dfe5876d2e1c3d3fe1f86d4cbe1e5ba4a8a6aee1def19561f71fceff3`. All six members, all eleven successor parents and all five successor candidates match their pinned sizes and hashes. Architecture HEAD is `16de973a1986ac07277df1ee6e7b9421cb430ff3`; product main is clean at `d47f9892d5709a1e108c4ecf9a9f60ed7aae12b2`.

**B3B0REF-R4-RF-1 is resolved.** The validator checks the mapping/string-key container first, then each keyed list and every element's individual type/grammar before duplicate or prefix relationships. No unvalidated element reaches the path comparison. A malformed container has the documented unqualified diagnostic; an invalid keyed entry has the directory-qualified diagnostic.

Fresh reproductions of ["sub", 17] and [17, "sub"] both raise exactly ValueError("MEMBER_GITLINKS_INCONSISTENT:/h/w/a"). String, null and object values receive the same keyed rejection. List, string and null tables, and a non-string key, receive exactly ValueError("MEMBER_GITLINKS_INCONSISTENT"). The checker asserts the exact exception type and diagnostic and no preceding reader lookup, item-6b verdict consultation or population walk. Its nine added cases cover the reported ordering and container defects, including malformed grammar after a valid element.

Restoring only the validator implementation and its docstring in memory reproduces the exact round-one reference hash, `025a9313934efb18ca31b12b63e41c8f3853452c31c982f21be7c806ce78aa93`. The rest of the reference is unchanged, so the round-one semantic judgments remain applicable:

- Admitted gitlinks affect only pass-two directory boundaries and link exclusion. Excluded candidates' gitlinks do not become boundaries, and absent/file targets bound no directory. Projection into SLM's boundary flag does not fabricate emitted VCS evidence. Population filtering preserves pruning, depth and nested-project limits.
- Branch A follows accepted A4: array size, global grammar, member placement/volume rules, member cap, custody and item 6b per candidate, then the member-aware walk. The no-members walk supplies gate/refusal provenance without replacing the chosen verdict. Walk refusals clear member/config rows and retain declaration rows. The revised and retained rf2 cases match that priority.
- LD-14 preserves membership by placement while excluding links within a gitlink. LD-15's glob argument remains sound because an admitted member is already a visible physical repository. LD-16 permits metadata placement probes before admission while forbidding the later walk from entering the index boundary; its device-change precedence is the settled member-rule priority.
- notWalked covers the union of modeled population paths across all passes, so a forbidden earlier trial cannot be hidden by a corrected final record. no6b covers the reference's verdict/gitlink consultation methods. These are reference-model controls, not product I/O qualification.

The README now correctly limits the 64-case equality statement to regression coverage. Global grammar priority intentionally changes some other no-member inputs; the D15 controls bind those changes. The previous NBO is addressed.

The successor structure remains appropriate: r3's parents plus its reference and successor record, five r4 candidate artifacts, and no passage override. The manifest additionally pins successor.json. The supplied synthetic successor-169 verification receipt remains supporting binding evidence; this acceptance does not claim actual product integration or qualification.

**Fresh verification:** the permitted checker passes 64/64 discovery equality cases and 124/124 D15 cases, with 173 schema-valid V3 results and 94 valid accepted inventories. Its output exactly equals the archived checks.json. All eight in-memory negative-control mutants reproduce the archived failed-case sets: 7 boundary, 3 link, 18 grammar, 2 size, 12 old-trial, 1 old-validator, 3 unchecked-container and 14 validation-disabled failures. The two new mutants therefore detect the corrected validation behavior.

To honor the two-file output limit, the checker temporarily wrote review.json, which this final verdict replaces. No additional checker or mutant file was created. Read-only imports and mutants ran with bytecode writing disabled. No Cargo, other tests, census, lane, network, other panes or delegation was used. No private fixture, installation directory, signing key, held tree or T2 held-out entry was read. Neither repository nor any control file was edited; only REVIEW.md and review.json in the requested directory were written.
