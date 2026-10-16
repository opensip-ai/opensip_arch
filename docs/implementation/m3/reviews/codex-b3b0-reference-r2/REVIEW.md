# B3-b0 reference r2 review

Verdict: **REQUIRED-FINDINGS**.

Subject manifest: 1,134 bytes, SHA-256 `1def8904959c1ec347969dcc9b8c88d73077c09d0065779621ed5c9d2a2a8db6`. All five members match their pins. The revised reference is 33,566 bytes, SHA-256 `1ee715f8e73e2e3c8be317c4fd597ea19ce951f56f8f459542a012ff2658f134`. All nine successor parents and four candidates match their sizes/hashes; passageOverrides remains empty.

Architecture HEAD matches `67b8f8bcaa6e25804a61b56693a87b6b39da311e`; product main is clean at `2b297e68e07aeae31a3fe71b6fb227f9758dcc5a`.

## Required finding

**B3B0REF-R2-RF-1 (P1): Glob classification still consults repository evidence below pruned anchors**

Location: `docs/implementation/m3/config-discovery-b/b3-b-reference/reference/member_reader_reference.py:474`.

The literal-entry placement walk now stops at anchors, but the npm glob branch searches every directory in inp["fs"] and calls _markers on it without applying pruning or the observed boundary population. Consequently a positive VCS fact hidden below W/.opensip changes workspaceDeclarations even though that exact anchor must never be entered and its descendants are absent from discovery. The same behavior occurs below node_modules. This leaves the no-hidden-observation part of round 1 RF-1 incomplete through another entry path.

Evidence:

- With W=/h/w, its ordinary project carrier, an empty W/.opensip directory and package.json workspaces=[".opensip/*"], discover returns ACCEPT with no unresolved npm entry.
- Adding only W/.opensip/secret with vcs=True and its .git directory changes that result to workspace-glob-crosses-repository; nestedRepositories remains empty in both results.
- The same paired change under node_modules changes the disposition of node_modules/* while leaving those paths pruned.
- The comprehension at lines 474-476 reads the raw supplied map instead of the population used by _finish; the current content-read spies do not cover this metadata path.

Required change: Classify glob crossings from the legally observable repository/boundary population, stopping at exact/pruned anchors before consulting descendants. Preserve crossings proved by a visible enclosing repository without opening its protected subtrees. Add paired fixtures differing only in a repository hidden below W/.opensip and a dependency anchor, plus metadata-observation spies; the hidden addition must not change the reader disposition or be consulted. Extend the controls beyond provider-content reads, and refresh the pinned checks and successor artifacts.

## Round-1 findings and lead decisions

- **RF-1: literal reproductions fixed; anchor coverage remains incomplete.** Re-running a/.opensip/p, a/.git and a/node_modules/pkg now retains the lawful outer member, returns no link and records entry-not-in-a-member. The placement loop classifies each prefix before descendant lookup/provider reading. The added npm/Cargo content-read controls are useful. The glob branch above still depends on protected descendant observations and prevents full discharge of the finding.
- **RF-2 resolved for the reproduced priority defect.** The provisional-member pass now lets SLM return root grammar, absence and disallowed-crossing failures before candidate terminal decisions. The ../bad plus .git-file example returns PROJECT.EXPLICIT_PATH_INVALID/JOIN_PATH_GRAMMAR; missing plus .git-file returns PROJECT.EXPLICIT_PATH_INVALID/ABSENT. The new controls cover both config roots and explicit joins, including grammar after another candidate. LD-6 now explicitly states its SLM-first priority instead of promising an order the code did not implement. Supplied 6b verdicts are still applied after the member cap; no Git decoder is run in this reference.
- **RF-3 resolved.** _project_vcs projects positive side-table evidence into the legacy representation before selection and population, and rejects the stated inconsistent observations. Re-running a side-table-only .hg candidate now excludes it, retains it in nestedRepositories and excludes its package from ordinary units. The added .svn/.jj, .git-file, ancestor and member-inner-boundary controls extend this fix. Only admitted members have VCS evidence withheld in the final member-aware pass.
- **RF-4 resolved.** Both 256- and 257-segment declaring entries retain the same depth-1 member and link. Candidate placement, rather than declaring-entry depth, now bears the M1 limit. The new candidate-depth-257 controls exercise branch-B exclusion and branch-A refusal.

**Explicit vocabulary rulings.** LD-B3B0-7's extended entry-not-in-a-member is a reasonable use of the existing diagnostic reason for a link target outside the member's analyzed tree. It preserves the independently declared outer member, emits no link, invents no public code and avoids inspecting a pruned target to distinguish nonexistent versus excluded descendants. It must not be used to justify probing an anchor, as the glob finding demonstrates. The DEPTH subject for an over-depth candidate is also sound: M1 is a placement condition, item 24 row 2 supplies the branch-A refusal route, and branch B discloses exclusion using the existing S3 depth vocabulary. This adds no new refusal code or limit.

LD-1/2's side tables and supplied 6b verdicts remain appropriate for the accepted reference/product split. LD-3's other layout/custody subjects, LD-4's absent rows before usable selection, LD-5's explicit synthetic baseline provenance, LD-8's cap D9, LD-9's directory-only waiver, LD-10/11's parser/upstream-layer interfaces and LD-12's typed link declaration scope remain within that split. A provisional pass is a reference calculation, not evidence of completed member admission or a product read trace. In particular, a refused trial must not be presented downstream as an accepted boundary inventory.

## Checks, scope and successor

The expressly permitted checker was rerun with the specified Python 3.14 command. It reports 64/64 no-member equalities, 67/67 D15 cases, 130 valid results and 77 valid inventories. The output is byte-identical to the archived 27,619-byte checks.json, SHA-256 `b96322aa0e14af979a8d2932f4c56ed46fcf5951932484e56dc21feb020cd445`. The temporary checker output was removed after comparison. The request's later reference to 42 expectations is the r1 count; README and actual checker now agree on 67.

The non-D15 equality projection is still the right regression check for the inherited 64 cases. The added paired branch-priority, literal-anchor, VCS side-table and depth controls materially address the prior findings. Schema validation proves admissible shapes for those cases, not that every observation was lawful; the missing glob/anchor combination above passes schema checks. Independent imports reproduced the four prior issues and additionally exercised hidden glob repositories, inner boundaries and mixed-failure provenance.

The wrapper continues to leave B2-b0, SLM, the shared rule, B-S1 schemas and contract text unchanged. Carrier states, both membership branches, cap counting, reader exclusions, links/ambiguity, memberConfigs and member-aware downward composition remain represented in the checker. The additive successor record's parent/candidate structure and lack of passage overrides are appropriate for a reference-only unit. The lead's scratch result reports a synthetic successor-168 PASS; this review did not rerun verify_design, and that result does not resolve the semantic finding or establish a real lock binding.

No non-blocking observations. This verdict does not accept the design unit for binding yet.

## Review limits

Review used reading, hashing, JSON parsing, Git queries, the permitted checker and read-only imports over supplied synthetic observations. No Cargo, other tests, census, lane or network was run. Neither repository nor control files were edited. No private fixture, installation, signing key, held tree or T2 held-out entry was accessed. No other panes or delegation were used. Only REVIEW.md and review.json remain as new review outputs in the requested directory.
