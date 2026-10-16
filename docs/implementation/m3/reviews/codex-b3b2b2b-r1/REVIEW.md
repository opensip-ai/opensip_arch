# B3-B2B2B-r1 review

**Verdict: REQUIRED-FINDINGS.** Four required findings block acceptance.

Subject manifest: `68e817efdd5c8f960279913e10653685632d2617e76f663ca1427dc365e5de13` (12,793 bytes; all 53 members rehashed successfully). The candidate's 11 product-map rows match their archived bytes; every mapped parent, authority pin and product-lock pin also matches. Product main is clean at `d47f9892d5709a1e108c4ecf9a9f60ed7aae12b2`; candidate HEAD is that base; architecture HEAD is `5c581b5c5a4e22ff3fa28d5e9f522df92a27c4a0`.

## B3B2B2B-R1-RF-1 — Carry admitted index gitlinks into discovery boundaries (P1)

Locations: `crates/security/src/custody/workspace_observation.rs:510-513`, `crates/security/src/custody/workspace_discovery.rs:230-250`, `crates/security/src/custody/discovery_walk.rs:922-935`.

member_verdict converts MemberVerdict::Admitted { gitlinks } to None and discards every gitlink. Neither the composition nor WalkRequest has another route for this evidence. The walker discovers nested repositories from physical VCS markers only. A real admitted member whose index contains a mode-160000 path sub, with an ordinary populated sub directory and no physical sub/.git, is therefore traversed as an ordinary directory. A Cargo.toml or package.json below sub can become a unit, and an exact join through sub can succeed. Law M3-B r9 item 21 explicitly makes an index gitlink a nested-repository boundary; item 22 preserves those boundaries. This is a static-input error, independent of races and C1 snapshot work. The 19 vectors use git init members without gitlink index entries, so record equality against their marker-only reference inputs cannot catch it.

**Required change:** Preserve the admitted gitlink paths and apply them to the discovery population, nested-repository provenance and exact-join checks before returning the complete result. Branch A must also respect this evidence when deciding whether its earlier trial remains usable. Extend the reference/control representation as necessary without treating a physical .git marker as a substitute for index-only evidence.

**Validation:** Add composition controls for a real valid member index with a gitlink at a populated directory lacking a physical VCS marker: automatic discovery must not enter it, an exact join crossing it must refuse, and descendants must not supply admitted links. Cover both membership branches and a mutation that drops gitlink evidence.

## B3B2B2B-R1-RF-2 — Bind retained stack directories to the objects custody judges (P1)

Locations: `crates/security/src/custody/workspace_observation.rs:116-149`, `crates/security/src/custody/workspace_observation.rs:298-305`, `crates/security/src/custody/workspace_observation.rs:364-370`.

directory records neither its newly opened directory sample in seen nor checks retained entries in the keep prefix against later observations. The carrier call order exposes this within one phase: probing .cargo/config.toml first opens and retains .cargo A before .cargo itself is observed. Replace W/.cargo with directory B before the subsequent carrier-parent custody lookup. entry(.cargo) now observes and ACL-captures B through W, while directory("") leaves the stack containing A. bytes(.cargo/config.toml) reuses A because the keep prefix is skipped, without comparing it to seen[.cargo] = B. The original file identity check still passes. Thus custody of B can authorize a read through A, including when A itself would fail directory custody. The same-object guarantee in A3 is not met even within the advertised per-phase scope.

**Required change:** Give every opened directory a durable object binding, reconcile later by-name entry observations with it, and validate retained prefix entries before reusing them. A disagreement must produce the existing change refusal before a read or listing; do not let an independently captured directory replace the custody evidence for the descriptor actually used.

**Validation:** Add a deterministic hook/control that swaps .cargo between the carrier-name probes and parent custody, with A failing custody and B passing. Require a change/refusal and no carrier read through A. Also exercise a reused multi-component prefix and a mutation disabling retained-prefix identity comparison.

## B3B2B2B-R1-RF-3 — Preserve object bindings across phases, trial walking and item 6b (P1)

Locations: `crates/security/src/custody/workspace_discovery.rs:141-166`, `crates/security/src/custody/workspace_discovery.rs:230-233`, `crates/security/src/custody/workspace_observation.rs:489-513`.

LD-2 drops the first observation and all its bindings before constructing a fresh phase-two observation. The trial walk has independent bindings, and MemberSession also reopens the member path independently of NativeObservation. Consequently each observer can consistently inspect a different inode at the same spelling without detecting a change. For example, phase one places M and the accepted trial discovers M/pkg in directory A; replacing M with a conventional same-volume repository B before phase two lets placement, custody and 6b succeed on B while the final result reuses units and provenance from A. B need not even contain pkg. Independently, swapping a candidate between member_custody and session.observe gives the session a directory other than the one the decision custody-judged. C1 later rechecks snapshot bytes; it cannot retroactively bind this discovery result to the objects that produced its placement, links and trial outcome. A3 explicitly requires a path seen twice to be the same object.

**Required change:** Carry and compare the relevant native object bindings across the phase handoff and the walker/6b interfaces. Reusing an accepted trial is sound only after establishing the required consistency with the later member decision. Retained descriptors or explicit compared samples can implement this; a new ledger or an assumption about future snapshot checks cannot.

**Validation:** Add deterministic composition controls replacing a member after an accepted trial and between member custody and 6b. Require the existing change/refusal behavior before emitting an accepted combined record, and add a mutation that removes the cross-observer binding comparison. This asks for the planned object-identity consistency, not an atomic snapshot of every file.

## B3B2B2B-R1-RF-4 — Read carriers from custody-bound descriptors and validate their capture (P1)

Locations: `crates/security/src/custody/workspace_observation.rs:342-358`, `crates/security/src/custody/workspace_observation.rs:456-482`, `crates/security/src/custody/discovery_walk.rs:282-284`.

observe opens a regular file for ACL capture and then drops that descriptor. bytes opens it again by name, and its only validation is same_object, which compares device, inode and file type, not custody metadata or ACL. For a carrier captured as 0644, changing that same inode to 0666 or adding an unauthorized write ACL before bytes leaves the comparison true, so its newly writable contents are read and used under the old custody verdict. There is also no post-read capture/stability check before exposing the buffer. Plan r2 section 3 requires carrier reads under S3 config-file custody from retained descriptors. C1 snapshot custody does not cover these already-consumed declaration carrier bytes.

**Required change:** Retain the descriptor whose capture supplies carrier custody and read from that descriptor, with the accounted validation needed to keep the metadata/ACL custody sample applicable to the read. Handle ordinary bounded-read outcomes provisionally so required checks can finish without latching, and expose bytes only after validation succeeds. Apply the same custody-binding discipline to provider-manifest reads.

**Validation:** Add controls changing mode and ACL on the same inode between capture and read, plus a change during the bounded read. They must not yield usable carrier/provider bytes under the stale custody verdict. Include ordinary oversize/read-failure cases to show the necessary checks remain funded and non-latching where required.

## Other requested judgments

On the covered static inputs, the composition follows B3-b0's branch ordering: phase one, provisional-member trial before phase two, no-members walk for a member-rule refusal, then the complete record. The scope-limit D9 is correctly request-rejected / exit 2 / REQUEST.UNSATISFIABLE. Spelling of member rows, declarers, declaration paths and providerMember, while retaining relative packageDir, follows the reference. The accepted-trial reuse needs RF-1 and RF-3 resolved. LD-5's no-members refusal walk is appropriate.

LD-3's metadata-only ACL eligibility and normalization are consistent with the stated walker policy; capture and ordinary bounded-read outcomes are returned as values outside the charged scopes. The session starts lazily at the first member verdict. I found no ordinary custody-refusal ledger latch in these paths. This does not establish that the later read uses applicable custody evidence (RF-2 and RF-4), or that session evidence belongs to the previously judged objects (RF-3).

**B3B2B2B-R1-NBO-1 — Keeping an unexportable pending partial satisfies the completion requirement.** LD-1 is acceptable: DiscoveryResultV3 is the complete serializable discovery result, the scenario consumes that result, and DiscoveryProvenancePending remains an internal walker/core partial without a provenance serializer. Removing the type name itself is unnecessary. This does not waive any of the object-binding findings.

**B3B2B2B-R1-NBO-2 — Retired mutations have different evidentiary standing.** Treating a .git file as a directory at the placement gate is plausibly equivalent for the stated case because unchanged 6b independently refuses git-not-directory. Keeping members on a refused trial is only shown equivalent on these 19 vectors; SCOPE itself leaves later refusal populations, including the unit cap, unproved. Retiring a redundant vector mutation is reasonable, but do not claim global semantic equivalence. Preserve the clearing code and preferably add a late-refusal case whose incoming provenance actually contains members.

**B3B2B2B-R1-NBO-3 — Access tracing checks the advertised paths but does not establish custody consistency.** The control checks core requests against the reference consulted/read/listed sets and traced native operations against requested paths, ancestor opens and marker lookups. This is useful for the covered static trees. It does not compare object identities, and calls inside the reused MemberSession/platform helpers are not individually included in this trace. Existing item-6b controls remain relevant; passing this access check does not settle RF-1 through RF-4.

The scenario obtains the precondition from the operation's own subject and constructs MemberInputs from the lent root's premise and home-filesystem predicate, with the scenario's empty environment/system sources and trust groups, as LD-9 states. The host evidence records all seven discovery_flag_tests passing. No production CLI composition is claimed here.

## Verification and evidence limits

I ran only the two permitted commands in the candidate worktree:

- `python3 -I -B tools/check_operability.py source --repository /Users/sb/code/opensip-ai/opensip-b3b2b2b`: passed, 114 rows, no findings.
- `python3 -I -B tools/security/workspace_discovery_vectors.py --check --architecture /Users/sb/code/opensip-ai/opensip_arch --packages-root /Users/sb/code/opensip-ai/opensip`: passed against the bound B3-b0 bytes.

Read-only JSON comparison independently confirms that each census file changes only `/closure/0/{bytes,sha256}` and `/closure/6/{bytes,sha256}`. The walker diff only exposes the shared helpers, and custody.rs adds the two modules. No census/lane was rerun, and no held-out store, overlay or entry was opened. The outstanding margins remain outstanding.

Archived evidence, rather than newly executed tests, records:

- Security base and candidate have the same 14 failures. Library passes increase 1,145 to 1,146; including the six documentation tests, totals increase 1,151 to 1,152. Five library tests remain ignored. This is equal-failure-set evidence, not a green full suite.
- The one new test compares all 19 scratch-tree composition records and link sets; the focused discovery/member run has 90 passes, and the host discovery run has seven passes.
- Warning-denied Clippy with and without scenario-fixtures, the vector checks, formatting, FW-01/storage checks, census controls/check, environment checks, operability and verify_design are recorded passing in checks.json and the pinned logs.
- All eleven mutation logs show the composition test failing after successful compilation. The misleadingly named member-refusal-keeps-walk-members mutation actually drops declaration rows, as SCOPE discloses; it is not coverage of retaining member provenance on a trial refusal.

The 19 cases give useful branch and static access coverage, but contain no real gitlink-index composition case or deterministic object-replacement/custody-change control. They are insufficient to discharge the required findings. The race examples above are source-derived execution sequences, not experiments run during this restricted review.

B3-b2b2c's T2 controls/joint sweep, B3-b3a's bound, later margin work, J1 and qualification remain outside this unit. No repository, worktree or control file was edited; only the two requested review artifacts were written.
