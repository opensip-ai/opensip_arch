# B3-b0 reference r1 review

Verdict: **REQUIRED-FINDINGS**.

Subject manifest: 1,133 bytes, SHA-256 `4afb627ad37d90ac9e5391bd558007c0a3a0982084ca920e569e1b24e10ac42d`. All five members match their sizes and hashes. All nine successor parents and four candidates also match their pins.

Bases match the request: architecture `67b8f8bcaa6e25804a61b56693a87b6b39da311e`; clean product main `2b297e68e07aeae31a3fe71b6fb227f9758dcc5a`.

## Required findings

### B3B0REF-R1-RF-1 (P1): The link reader crosses member custody-state and VCS anchors

Location: `docs/implementation/m3/config-discovery-b/b3-b-reference/reference/member_reader_reference.py:550`.

The link loop excludes inner repository/project boundaries but never applies the admitted member’s pruning anchors before _link reads a provider manifest. A literal workspaces entry a/.opensip/p admits a and returns a link from a/.opensip/p/package.json, even while the provenance marks a/.opensip as an opensip-custody-state pruned tree. A literal a/.git similarly returns a link from a/.git/package.json. SX-1 makes the member-root .opensip an exact never-entered anchor, and item 21 admits only the specified three member Git objects before C1. The current reference therefore uses bytes its own discovery scope excludes.

Evidence:

- A supplied-content get spy recorded /h/w/a/.opensip/p/package.json, and discover returned ACCEPT with packageName=hidden, providerMember=/h/w/a and packageDir=a/.opensip/p.
- A separate a/.git entry returned ACCEPT with packageName=git-hidden and packageDir=a/.git.
- The resulting provenance still reports the same directories as opensip-custody-state/vcs-tree anchors.

Required change: Apply the owning anchor/read-boundary rules before consulting descendant placement/provider bytes. Do not read or link a provider under M/.opensip or a pruned VCS tree. Preserve membership-by-placement independently where lawful, and select a justified existing disclosure or obtain the needed narrow law/registry decision rather than inventing a public reason. Add Cargo and npm regression cases with an observation/read spy that proves the hidden manifest is never consulted.

### B3B0REF-R1-RF-2 (P2): Branch A skips earlier grammar/absence failures before returning a member failure

Location: `docs/implementation/m3/config-discovery-b/b3-b-reference/reference/member_reader_reference.py:483`.

Invalid root grammar and missing roots are deferred to pass two, while later candidate layout, volume, cap or 6b failures can return immediately. This contradicts LD-B3B0-6’s stated grammar-and-absence-first order and changes the earlier SLM refusal. Mixed-failure arrays are absent from the checker.

Evidence:

- configWorkspaceRoots=["../bad","a"] with a holding a .git file: pass one refuses PROJECT.EXPLICIT_PATH_INVALID/JOIN_PATH_GRAMMAR, but discover returns PROJECT.ROOT_CUSTODY_REFUSED/member-vcs-unsupported:git-not-directory.
- configWorkspaceRoots=["missing","a"] on the same tree: pass one refuses PROJECT.EXPLICIT_PATH_INVALID/ABSENT, but discover returns the later member-layout refusal.

Required change: Validate the array’s grammar and existence in the intended order before candidate-specific terminal decisions, preserving the appropriate owning SLM refusal/path/detail. Do not merely return every pass-one refusal: ordinary member crossings are precisely what this wrapper must resolve. Add mixed-failure controls with invalid/missing roots and otherwise independently failing member candidates for both config roots and explicit joins. If a different public priority is intended, settle and document that decision instead of claiming the current stated order.

### B3B0REF-R1-RF-3 (P1): VCS side-table evidence is not carried into selection and boundary discovery

Location: `docs/implementation/m3/config-discovery-b/b3-b-reference/reference/member_reader_reference.py:378`.

_markers uses vcsMarkers to decide W2 and placement, but base drops that side table without projecting its positive observations into the legacy fs VCS evidence. _finish then feeds that unchanged representation to B2-b0/SLM. Under the documented side-table interface, a directory with a positive .hg side-table observation and no legacy vcs flag is excluded as a member but is not recorded as a nested repository; its package is discovered as an ordinary unit. One positive VCS fact is thus used for exclusion and ignored for the boundary it must preserve.

Evidence:

- A synthetic /h/w/a with a physical .hg directory, vcsMarkers={"/h/w/a":[".hg"]}, and no legacy vcs flag produces member-excluded/member-vcs-unsupported:vcs-other for reader entry a.
- The same result has nestedRepositories=[] and includes /h/w/a as a workspace-auto unit, despite that positive VCS observation.
- The input API documents vcsMarkers as carrying VCS information not expressed by the legacy single flag; no consistency requirement is validated.

Required change: Define and enforce one consistent VCS observation representation before pass one and pass two. Project side-table markers into the legacy selection/population evidence, withholding that evidence only for admitted members, or reject an incomplete/inconsistent observation before discovery with a documented input contract. Add side-table-only .hg/.svn/.jj and .git-file cases, including root/ancestor selection, excluded candidates and nested repositories inside admitted members. An excluded repository must remain a boundary and its contents must not become ordinary units.

### B3B0REF-R1-RF-4 (P2): The member depth limit is incorrectly imposed on the declaring entry

Location: `docs/implementation/m3/config-discovery-b/b3-b-reference/reference/member_reader_reference.py:253`.

_place rejects any declaring entry directory deeper than 256 segments as entry-path-absent before locating its candidate. Law item 19 M1 bounds the member M’s depth, while the registry’s entry placement requires the actual directory to exist without links/device changes; it does not impose this limit on D. A shallow member can therefore disappear solely because its declaring package directory is deeper. Native walker depth behavior is not authority to report an existing reader entry as absent or change membership-by-placement.

Evidence:

- A conventional member a at depth 1, declared solely by an existing package directory at depth 256, is admitted and linked.
- Moving only that provider/entry directory to depth 257 produces members=[], no link and entry-path-absent, although the candidate remains at depth 1, every segment is a directory on the same device and the entry spelling is canonical.
- The 257-segment example is only 513 ASCII path bytes, so this is not the schema’s string-length limit.

Required change: Apply M1’s depth bound to the candidate member, separately from any owning rule for the declaring entry or provider read. Preserve the shallow candidate’s lawful declaration. If a depth restriction/disposition for reader entries is wanted, obtain an explicit law/registry decision and cite it. Replace LD-B3B0-3’s unsupported entry-depth rule and add boundary cases distinguishing candidate depth from entry depth.

## Other requested assessments

**Architecture and non-D15 equality.** A wrapper over the unchanged accepted references, with supplied 6b verdicts, is the decomposition the accepted plan permits. Withholding admitted members' VCS evidence and own root opensip.json from the downward boundary calculation, restoring upward provenance, and binding the shared/population rules to member roots is a reasonable composition. The 64-case comparison of every non-D15 field is the correct regression projection; it cannot prove new side-table and D15 behavior absent from those cases. RF-3 identifies a missing consistency condition at that composition boundary.

**Lead decisions.** LD-1/2's side tables and supplied Git verdicts are appropriate in principle. LD-3's existing layout/custody subjects and branch-A refusal versus branch-B exclusion are generally grounded in item 24; its entry-depth rule is not (RF-4). LD-4's absent reader rows are reasonable before usable root selection, without claiming a carrier read. LD-5's plain-discovery provenance is an explicit synthetic baseline policy; product consumers must not treat reconstructed facts as an actual observed prefix unless their execution collected them. LD-6 is not implemented as stated (RF-2). LD-7's distinction between an outer admitted member and a provider inside its inner repository/project boundary appropriately prevents that provider from linking; RF-1 shows that the same protection is missing for exact anchors. LD-8's cap D9 matches B-S1. LD-9 preserves the member-directory-only owner waiver and supplied Git refusal; it adds no waiver for carrier/provider files. LD-10/11's parser and upstream layer interfaces are within the plan, with the three source paths still owed product controls. LD-12 correctly provides typed declarations without inventing published link-set bytes or consumer satisfaction.

**Checks and coverage.** The permitted checker was rerun using the specified Python 3.14 command. It reports 64/64 no-member equalities, 42/42 D15 expectations, 106 valid DiscoveryResultV3 results and 66 valid inventories. Its output is byte-identical to the archived 21,548-byte checks.json, SHA-256 `584bf097e994222ef6741465bd4a5cc339f2a642ee3342488bb91bfb7b47eb8c`. The temporary permitted output was removed so only the requested review outputs are added here.

The handwritten cases exercise the reported carrier states, parser failures, both branches, cap, waiver, placement exclusions, ambiguity, link failures, memberConfigs, nested boundaries and ordinary member anchors. They are not complete assurance: they omit the mixed-failure priority, hidden-provider anchor access, side-table-only VCS and member-versus-entry depth cases above. Schema validation checks shape and cannot detect those semantic violations. An exploratory empty-array example was excluded from findings because the admitted product configuration schema requires minItems=1 for workspaceRoots; malformed synthetic input is not evidence of an admitted-array defect.

**Successor record.** The candidate is an additive reference design unit with existing, exact parent pins, four new candidate artifacts and no passage overrides. That is the correct form for leaving contract text and the accepted base models untouched. The reported scratch binding of a synthetic successor 168 is compatible with this shape, but the base-lock scratch PASS does not establish selection of these new artifacts; their eventual real lock binding still matters. Neither scratch verification nor the passing checker establishes semantic correctness against the findings. No product code, integration or qualification is accepted here.

No non-blocking observations.

## Review limits

Review used reading, hashing, JSON parsing, Git queries, the expressly permitted checker, and read-only reference imports on supplied synthetic inputs. No Cargo, other tests, census, lane or network was run. Neither repository nor control files were edited. No private fixture, installation, signing key, held tree or T2 held-out entry was accessed. No other panes or delegation were used. Only REVIEW.md and review.json remain as new review outputs in the requested directory.
