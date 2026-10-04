# CODEX2 — M3-I1 r2 review

**Verdict: ACCEPT.** All three r1 required findings are resolved. No new required finding remains.

- `PROPOSAL.md`: 52,522 bytes; SHA-256 `1eb47d1e292660b15cb0016a280899a384364f2c3d99ab61d18f12b133eba2c7`.
- `UNITS.md`: 9,196 bytes; SHA-256 `0c3c0f44d61a64813b2e1156e8ecb0b97adeeecbd48149a00bf77a8c8950e785`.

All 19 request pins match, including the preserved r1 subjects. I compared both complete r1-to-r2 diffs with the previous review. The changes are confined to the stated three findings and three observations, their supporting explanations and unit content, and revision metadata. No unrelated substantive change was found.

## Required-finding resolution

### I1-RF-1 — Resolved

Item 2.5(b) now positively closes the **imports-symbol** source census, independently of the file-rule population and of the cell's `required` flag. The expected IDs come from owed inventory rows and union by universe, as ATOM:257 specifies. Every known expected source must appear by exact ID in a retained exact `imports@resolved-target` scope. Every such scope still needs paired sufficient Coverage.

The old optional-cell counterexample now yields `uncovered-expected-source-subject` for B rather than pass (UNITS case 15). Partial/unavailable source census yields `population-unknown`, with known rows still checked (case 16). Broad partitions may cover several sources (case 17). A complete-empty census closes through an explicit empty-subject scope with complete Coverage; absence of all scopes remains unknown (case 18). That matches the admitted empty shape at ATOM:242-245.

The cause choices match ATOM:210-212,423,430. EXI:198-211's missing-work carrier stays (null, null); neither gap manufactures `provider-unavailable`. Real source carriers remain retained. These semantic atom causes do not replace structural admission refusal for omission of a promised expected inventory record (ENUM:111; COMP:82).

### I1-RF-2 — Resolved

The proposal withdraws the interpretation that unchanged IE permits widening. Item 4 now explicitly succeeds IE:213-214 and IDS:4978. The exception is narrow: exactly `cycle-representative` in proof-bundle `predicateProofs[].operation` and `program-predicate.operation`; no other vocabulary, field, bound, ordering, recipe, prefix or major changes.

**I confirm the lead's reading:** no cited identity rule makes the major/migration requirement unamendable by a reviewed passage successor. This expressly scoped exception is a legitimate successor decision. It is different from a permissive parser or a mixed-output-major graph: the selected successor remains a closed schema, the output profile remains 3, and older readers refuse the new member.

The new member must still originate in the admitted policy/program and satisfy the existing predicate-address, node-digest, program and proof joins (COMP:32; IDS:2758). Older valid records cannot contain it. Their unchanged descriptors preserve their bytes and identities, while the new closed member denotes the newly reviewed atom. The exception's passage does not license a second member or a different schema/domain change. The major-bump fallback is therefore unnecessary for this successor.

I1-L explicitly owns both new identity passages, and I1-a carries the IDS `majorLaw` text, schemas, source pins and generated enums. I1-L's later review must verify the actual passage bytes and compatibility controls.

### I1-RF-3 — Resolved

Condition (d) is removed from the atom's completeness decision. File population remains exclusively in composition, where partial/unavailable relevant file inventories already produce the gating rule's enumeration deficiency (COMP:28,56,161-166).

The third-row false is sound under the declared admitted scope: if a selected subject lay on a cycle wholly in V, complete source census and sufficient fully resolved imports Coverage would retain that cycle. If the cycle left V, its first outgoing edge from V would have an unselected or unknown project target, which item 2.3 treats as uncertain. Either possibility defeats the false row's conditions. Complete **file** population is not needed for that atom conclusion.

Every remaining atom-indeterminate path has a cause: binding failure, census/source/pairing failure, insufficient Coverage, or an uncertain endpoint. UNITS case 19 now yields false at the known `a.ts` subject and an indeterminate gating rule through composition's `incomplete-inventory`, with no host fault. That agrees with FAULT:18,34-35.

## Other r2 changes

The three previous observations are addressed:

- P(s)'s representative is explicitly relative to this Run's admitted component, with non-monotone representative selection disclosed (proposal:132-143).
- The short order includes I1-b1 → I1-b2 and agrees with UNITS.md's detailed dependencies (proposal:445).
- LD-10 is a recommendation only. C2/C4 must define and review the exact detector-tree signed-core provenance, component and role joins, retained bytes/descriptor and Plan selection (proposal:426).

The supporting witness/cause text, H feed, forbidden substitutes and cases 15–19 follow the specified fixes. Unit numbers, sizes and detailed dependencies are unchanged. The X9-6 gate, root-only admission law, graph/SCC emission, known-cycle failure with deficiencies, registry row, scoped X12 amendment and downstream gates remain unchanged.

## Pack bytes and digests

The canonical 574-byte policy document is byte-for-byte identical to r1, including no trailing newline. I independently recomputed the three values again with a read-only standard-library-only scratch script:

| Value | SHA-256 |
|---|---|
| `programDigest` = SHA-256(C(emitWhen)) | `8e8936af513ae93eeb8227fb991330b523761930d85d077b044f4312706a57de` |
| `policySha256` | `96675a5e20fcfd8ba6501f20b9017aa205e300b9f1984d7e74ad534996acdcd1` |
| `ruleProgramDigest` (457 canonical bytes) | `e796f81764d0ee452c591c852e98f59647518a1894d4bd0fd5c70b674ecc3ecb` |

The results and all requested source pins are in `digest-check.json`; the inspected subject changes are in `r1-to-r2.diff`.

## Non-blocking observations

- **I1-R2-NB-1 (PROPOSAL.md:242).** The phrase 'no schema digest enters any identity' is too broad. IE's coverage identity includes its exact schema digest (IE:185); fact/view and stage-spec/Plan-related commitments also bind schema bytes (IE:184-186,1288-1298,1323). Limit this explanation to the relevant descriptors: H has no additional implicit owning-schema preimage component, so an unchanged existing proof-bundle or program-predicate descriptor retains its identity. Newly constructed descriptors committing changed schema or closure bytes derive changed identities normally. The narrowly scoped passage itself and the preservation of existing descriptor bytes remain sound.
- **I1-R2-NB-2 (PROPOSAL.md:212-219).** Keep the budget paragraph clear about semantic work-unit granularity. A scan of each scope's subjects once is not a strict bound on elementary operations by E alone: several broad scopes can repeat the same inventory IDs, so their total membership occurrences may exceed E. Describe E+S*(1+F+I+K) as the unchanged COMP:38 deterministic semantic preflight charge, and avoid presenting the displayed E+S+F+K expression as a CPU-step bound. Reuse admitted indexes where useful and retain the existing independent descriptor/output limits. This is a clarification of the work explanation, not a change to the normative charge or the atom's outputs.

## Review boundary

This accepts the r2 law and unit plan at the hashes above. I1-L and I1-P still need their own `ACCEPT-DESIGN-UNIT` reviews. No product-unit acceptance, harness qualification or live-provider result is claimed.

Inspection was read-only. Static product-source checks used `git show` at the proposal's `2967905d8152a5f2e431cd8006e1b82f898c3fe2` commit. No cargo, builds, tests, reference-model runs, delegation, repository edits, pushes or commits were performed. No application runtime/home state or 413 fixture was read. Every written artifact is under the requested r2 review directory.
