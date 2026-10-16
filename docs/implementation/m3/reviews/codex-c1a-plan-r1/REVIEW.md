# REQUIRED-FINDINGS — C1a implementation plan r1

Subject manifest SHA-256: `93b715a831340641ccb9a4f805176a7716c0f0ca6da0e50598cba455cda9e216`. The sole member matches 18,118 bytes and SHA-256 `4848fe7eaae7c915bc07c2035695ccbc537de0c99492c5b08c58fde53f929d7b`. Product HEAD is the clean `808ad6476fb848f84e732ee233a47229370081f4`; architecture HEAD is `43402bbc8543b0e4f265bcb4fd482c1c113f562c`.

## Required findings

### C1APLAN-R1-RF-1 — The capture API does not establish the promised single source-read boundary

`docs/implementation/m3/snapshot-plan-c/c1a/PLAN-r1.md:86`. Section 1 assigns every source read to snapshot.rs, but C1a2 gives candidate_custody.rs a put(source: &mut dyn Read, ...) operation that streams and hashes the supplied source. Passing the handed source File directly moves the consuming read loop into candidate_custody.rs, outside the proposed two-file source pin. Conversely, CaptureSession::read(path) must capture B2/C2 inputs before the extent walk, but the only specified descriptor-opening surface is the completed-extent walk visitor. The plan does not explain how those earlier reads obtain custody-judged descriptors without a host path-string open or a second traversal rule.

Required change: Define the complete pre-walk capture boundary. Keep actual source-descriptor reads in snapshot.rs, with candidate custody accepting chunks/a sink, or explicitly specify an adapter that preserves that read site. Add a security-owned retained-root relative opening/re-observation service usable before the extent walk, under the same custody and charging rules. Pin all relevant reader/opener modules and add a pre-capture/reuse/change control that proves no second source read.

### C1APLAN-R1-RF-2 — The walk entry accepts only durable writer authority

`docs/implementation/m3/snapshot-plan-c/c1a/PLAN-r1.md:68`. walk_snapshot requires &ProjectOperation. That type is the writer handoff, lending its root through operation_handoff.rs:380 under the durable receipt/lease. Existing project_chain.rs explicitly supports a separate read lending through installation_read.rs ReleasedRead::discovery_root. M3-J1 item 6 forbids an ephemeral request from acquiring a writer lease or entering the ordinary writer, and also requires the positively-absent-installation route. The plan promises the library for J2b and J2c but gives no lawful root input for either ephemeral case.

Required change: Specify a narrow root/custody input with authenticated durable and ephemeral construction routes, including the released-read route and the positively-absent-installation premise. Keep the lease requirement specific to durable requests, with no fence during either walk. State which existing closure files each route needs to change and include route controls without wiring a production caller.

### C1APLAN-R1-RF-3 — The interim VCS gate must also cover D15 Git members

`docs/implementation/m3/snapshot-plan-c/c1a/PLAN-r1.md:133`. LD-C1A-5 only describes withholding sealing for a Git-tracked project. Under M3-C item 4, a D15 workspace root is NoRepository/kind none while its admitted member repositories are Git; such a workspace requires the schema-3 VCS observation with all members. This plan already walks admitted D15 members, but does not explicitly withhold sealing when the root is NoRepository and member VCS observations are still unavailable. Root kind none alone cannot authorize a schema-2 snapshot that omits those members.

Required change: Make SnapshotVcsPending cover every input requiring C1b, including any admitted D15 Git member, not just an enclosing root Git repository. Permit the interim none observation only with authenticated NoRepository and no members requiring observation. Add a NoRepository-root-with-Git-member control that refuses sealing until C1b.

### C1APLAN-R1-RF-4 — The ledger constructor precedes the derivation of its required byte cap

`docs/implementation/m3/snapshot-plan-c/c1a/PLAN-r1.md:74`. C1a1 is to introduce snapshot_profile with the derived byte cap, but C1a4 is where the pricing recipe and cap derivation are supplied and reviewed. There is no stated cap or derivation prerequisite for C1a1, nor an explicit incomplete intermediate API. Choosing a placeholder discovery/global cap would violate the stated snapshot profile; changing it later also moves the whole-file work_ledger.rs census pin again.

Required change: Move the pricing recipe and initial cap derivation ahead of or into C1a1, leaving corpus margin measurements and the gated blind refresh for C1a4; alternatively explicitly scope C1a1 as an incomplete internal primitive with no claimed finished snapshot profile. Account for all retained/cumulative charges and read attempts, and name every later cap/closure change and receipt-staleness transition. Do not infer a full work-cost bound solely from final inventory path bytes.

## Requested decisions and scope

**Q1 / LD-C1A-1:** Security can walk, judge custody and open descriptors without reading source content; that split is compatible with C1-T2. Acceptance requires the complete capture interface in RF-1 and the mode-correct authority in RF-2. A wider source pin alone does not cure placing the actual source-reading loop outside its required owner. Reuse of `judge_entry`, the shared discovery rule and admitted boundaries is appropriate; host must not copy custody or exclusion logic.

**Q2 / LD-C1A-7:** A separate snapshot profile is justified. Current `with_limits` cannot exceed 65,536 objects / 131,072 edges / 256 MiB, while `discovery_profile` fixes 2^22 objects / 2^21 edges / 2^30 bytes. Neither gives the law's snapshot object cap of 2^20 and its separately derived byte cap. `work_ledger.rs` is whole-file pinned in `discovery_census.py`; adding the constructor therefore stales the receipt. The declared re-pin, unchanged discovery cost projection, explicit outstanding status and pre-/post-reviewed blind refresh follow the B3-b A1 and B2-b4-r6 precedents in principle. RF-4 corrects the cap sequencing. No current margin or authorization to execute a run is inferred by this review.

The recipe correctly distinguishes charged storage from payload volume. A reused buffer, metadata/ACL owners and exact charging are appropriate. Its derivation must cover the entire cumulative work population, including non-inventory names/directories, temporary listings, copies, capture/reverification work and read-attempt costs; a bounded final descriptor is not by itself a bound on these. Actual-versus-model controls and undercount mutations should cover those terms. The later T2 measurements must report failed or incomplete margins faithfully rather than treating the recipe as evidence that the corpus passes.

**Q3 / LD-C1A-5:** An internal, unreachable interim `SnapshotVcsPending` is reasonable while C1b follows, with no public route or completed C1 claim. RF-3 makes its scope complete for D15. It must not turn unavailable VCS evidence into a false none observation.

**LD-C1A-2 to 6:** The shared extent, single streamed capture, caller-owned private temporary custody and no ambient TMPDIR selection are sound directions. Empty read-set support is an explicit C1a limit, with C1c still owed. Retained captures, metadata comparisons, no retry, no late source reads, leftover-dependent-capture refusal and the operational origin record match item 1; their implementation/source controls remain required. The public bound projection belongs to J, and Git/read-set completion belongs to C1b/C1c.

**Carrier join:** Using `ResolverInputV1.project` is correct: hash the exact captured project-carrier bytes, including the presence observation, rather than infer presence from winning leaves. Pass only the observation to sealing, not X2 source bytes. The law's seven-row table is complete. Its root listing/type/exclusion distinctions must remain available even when an entry is not inventoried; local and member carriers do not enter this root join. The named seven controls are appropriate.

**Sealing and controls:** The proposed order, sorting/uniqueness, identity-v3 admission through `IdentityCandidate::from_json`, raw canonical source-inventory digest, row/descriptor/total-byte bounds, and exclusion of operational fields align with items 5 and 6. The C1a control families are allocated across the four steps, with C1b/C1c and J controls explicitly pending. Base/candidate failure comparisons, warning-denied Clippy, format checks, FW-01/environment checks, design verification, custody/race/bound/carrier mutations and pre-/post-run blind reviews are appropriate planned checks. They do not resolve the interface and sequencing gaps above and were not executed in this review.

No non-blocking observations. This is a plan review, not implementation acceptance or product qualification. Review used only reading, hashing, JSON parsing and Git queries. No build, test, generator, network, delegation or prohibited private-data access occurred. Only this directory's `REVIEW.md` and `review.json` were written; neither repository was edited.
