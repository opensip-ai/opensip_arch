# B3-b0 reference r3 review

Verdict: **ACCEPT-DESIGN-UNIT**.

Subject manifest SHA-256: `8e6c337b42b861182768968e1a21ccedff0a5f32a937da16bff877f248967e07`. All six manifest members match their byte counts and hashes. The reference is 35,625 bytes, SHA-256 `9c45d01651e3e33bb394dbdac543993db4f9803492cb8db118d330aa899c929c`. All nine successor parents and five candidates also match. Architecture HEAD is `67b8f8bcaa6e25804a61b56693a87b6b39da311e`; product main is clean at `2b297e68e07aeae31a3fe71b6fb227f9758dcc5a`.

No required findings or non-blocking observations.

## Round-2 finding

**B3B0REF-R2-RF-1 is resolved.** The npm glob branch uses `_visible_repositories`, rather than testing every raw-tree directory for VCS evidence. The helper walks parent-first from W, classifies pruned anchors before metadata lookup, stops at visible repositories and nested projects, and does not probe boundary descendants to decide a crossing. A visible enclosing repository still proves a crossing when the glob prefix points farther inside it.

I independently reran the original paired reproductions using read-only imports and synthetic observations. For `.opensip/*`, adding only a repository and its `.git` below W/.opensip leaves the complete discovery result identical: ACCEPT, no members and no unresolved npm entry. The analogous node_modules pair is also identical. The `_entry` spy records no descendant lookup below either anchor. The checker additionally covers crossing by a visible enclosing repository without consulting its interior, and a repository hidden inside a nested project.

The negative control is effective. An in-memory substitution restoring the old raw-tree repository scan reproduces exactly the four failures named in `negative-control-r3.json`: the two hidden-anchor glob cases, visible-enclosing-repository observation control, and nested-project visibility control. No repository file was mutated to perform this check.

The other reader paths retain the r2 anchor fix: literal placement classifies every prefix before looking it up, using observed Cargo roots and the candidate member root for SX-1; a target behind an anchor yields no provider read or link. Carrier and provider metadata reads use `_entry`. The observation hook describes reader metadata access, not all accesses by SLM, B2-b0 or side-table input validation. Literal placement still performs the registry's explicit segment-by-segment existence checks for D, including entries inside inner boundaries; this is distinct from glob enumeration and from admitting or linking the inner repository. Synthetic inner-project and inner-repository probes confirmed that links remain suppressed. No additional pruned-anchor reader access was found.

## Fidelity and lead decisions

The r1 fixes remain present and their regression cases pass: SLM-first branch-A error priority, unified positive VCS evidence, literal-anchor protection, and applying M1's depth bound to the candidate rather than the declaring entry.

Both membership branches preserve placement-only admission independently of package metadata. Branch A derives members solely from the admitted roots and lets SLM decide grammar, disallowed crossings, pruning, absence and directory custody before member terminal decisions. Branch B excludes unsuccessful candidates and preserves their boundary evidence. The cap counts distinct placement-qualified candidates in either branch before supplied 6b verdicts; it refuses rather than truncating. Root-in-repository declares no members or links and uses the specified literal-entry disclosure.

Carrier absent/read/refused states, exact JSON and TOML parsing, closed patch shapes, unresolved reasons and ordering, provider failures, ambiguity, memberConfigs, and typed link rows remain consistent with the registry and law items 19–24. The directory owner waiver does not reach carrier/provider files or supplied member Git verdicts. The reference does not implement the real 6b decoder or descriptor custody.

The requested vocabulary rulings remain unchanged: **LD-B3B0-7's extended `entry-not-in-a-member` is acceptable** for a link target outside a member's analyzed tree, including a pruned target that must not be inspected to distinguish absence. It preserves the outer candidate's independent placement declaration and introduces no new reason. **`DEPTH` is acceptable** for a candidate exceeding M1's 256-segment bound: branch A uses item 24's placement-refusal route and branch B discloses exclusion. A deep declaring directory inside a shallow member is not itself an M1 failure.

LD-1/2's side tables and supplied Git verdicts fit the accepted reference/product split. LD-3's placement subjects and crossing split, LD-4's absent reader rows before usable selection, LD-5's synthetic refusal provenance, LD-6's stated SLM-first order, LD-8's scope-limit D9, LD-9's directory-only owner waiver, and LD-10/11/12's parser, upstream layer-resolution and typed-link interfaces remain sound within that scope. Provisional member evaluation is a reference calculation; refused output is not an accepted boundary inventory. The carried plan NBO concerning the future `vcs: none` link-stage seam remains applicable to B3-b2 and is not product admission evidence here.

## Equality, checks and successor

The expressly permitted checker reports:

- 64/64 inherited no-member cases equal to B2-b0 on every non-D15 field.
- 73/73 D15 expectations passed.
- 136 schema-valid results and 83 valid accepted inventories.

The request's reference to 42 expectations is the original r1 count; the current README, checker and evidence consistently use 73. The checker output was byte-identical to the archived 28,931-byte checks.json, SHA-256 `2b196f7fc0601971ac7e0de07e045adfe6bdbc1efb1e7b1572e687b492cb423c`; the permitted temporary output was removed after comparison.

The no-member projection is the correct inherited regression comparison, not an exhaustive equivalence proof. The member-aware second pass withholds only admitted member VCS evidence and root configuration markers, keeps nested boundary evidence, binds pruning and population to member roots, preserves the original selection/source and upward evidence, and completes the three D15 fields. The controls cover every registry disposition and the principal branch, cap, depth, custody and boundary combinations. Schema validation establishes record shape; the paired observation and mutation controls supply the missing semantic evidence from r2.

The successor's nine parents, five candidates and empty passageOverrides are appropriate for this additive executable reference: no contract text is replaced. The negative-control artifact is now pinned as a candidate and manifest member. The lead's scratch file reports a synthetic successor-168 verification PASS; I read that report but did not rerun verify_design. Acceptance here permits the design-unit binding process; it does not establish an already integrated successor, product correctness, qualification, real Git observation, or link honouring before S5/S6.

## Boundaries

Review used read-only reading, hashing, JSON parsing, Git queries, the expressly permitted checker and read-only imports over synthetic inputs. No Cargo, other test command, census, lane, network, pane or delegation was used. Neither repository nor control files were edited. No private fixture, installation directory, signing key, held tree or T2 held-out entry was accessed. Only REVIEW.md and review.json remain as new review outputs in this directory.
