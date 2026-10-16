# REQUIRED-FINDINGS — C1a implementation plan, round 2

Subject manifest SHA-256: `b41e3472951cb880d31a40d663fc2d71e8b7fcef4d145b77f3555fe0a6d02e4b`. Both members rehash correctly. Archived r1 remains 18,118 bytes, SHA-256 `4848fe7eaae7c915bc07c2035695ccbc537de0c99492c5b08c58fde53f929d7b`; r2 is 25,523 bytes, SHA-256 `a1101f566cd8250d77da451d4945c33421295ad2e3e0bb5b7cc60d442c709f73`. Product HEAD is clean at `808ad6476fb848f84e732ee233a47229370081f4`; architecture HEAD is `43402bbc8543b0e4f265bcb4fd482c1c113f562c`.

## Prior findings

- **C1APLAN-R1-RF-1:** The source-read placement and missing pre-walk service are addressed: security owns the opening/re-observation service, custody takes chunks, and only `snapshot.rs` reads source content. C1A-T1 and the expanded source pin are appropriate. The new opener introduces the distinct retained-parent gap in R2-RF-2.
- **C1APLAN-R1-RF-2:** Addressed at plan scope. Durable and released-read constructors use the existing lawful lendings. Ephemeral I-complete walks require no lease or fence; the I-absent route is explicitly pending E-1/S7b and J2c remains gated. This is a disclosed dependency, not a fabricated construction from writer authority.
- **C1APLAN-R1-RF-3:** Addressed. Any admitted D15 member now triggers `SnapshotVcsPending`; only authenticated NoRepository with no members can seal the interim schema-2 none observation. C1A-T4 covers the previously missing workspace case.
- **C1APLAN-R1-RF-4:** Moving recipe/derivation ahead of the C1a1 constructor resolves the sequencing objection. Named re-pin/stale/refresh transitions also improve fidelity. The replacement derivation is not yet sound, and LD-C1A-8 introduces a separate law issue, detailed below.

The full r1-to-r2 diff was reviewed, including the changed read interface, new root service, recipe, incremental bounds, controls and receipt transitions. No implementation or corpus result is inferred from the new prose.

## Required findings

### C1APLAN-R2-RF-1 — The new cap derivation does not bound the operations the plan specifies

`docs/implementation/m3/snapshot-plan-c/c1a/PLAN-r2.md:106`. The derivation prices payload reads as one complete 64 KiB chunk per read plus EOF, although Read may return short reads or Interrupted and the platform reader explicitly requires a finite attempt allowance. SnapshotRoot::open also reopens and judges every ancestor for each path, but the formula counts directory listing/ACL costs by distinct directory count rather than per opening. It does not establish bounds for non-inventory listed names, per-component temporaries and copies, or the custody verification reads required by C1a2. Final inventory bytes do not bound those cumulative costs. Doubling an incomplete or best-case formula does not make it an upper bound.

Required change: Replace the formula with a complete operation-count and storage-cost model matching the chosen opener, capture, custody-verification and retention design. State a finite read-attempt envelope including short reads, Interrupted and EOF, and the terminal outcome when it is exhausted. Bound all listed entries and repeated component operations, not only inventoried rows and distinct directories. Add worst-envelope model controls and undercount mutants before deriving the profile and claiming census margins.

### C1APLAN-R2-RF-2 — The new root-relative opener is not bound to the walk enumeration parent

`docs/implementation/m3/snapshot-plan-c/c1a/PLAN-r2.md:68`. The walk enumerates a retained directory but opens every resulting logical path through SnapshotRoot::open, which starts again at the root. The plan only compares the observation and open within that new path walk; it does not bind the reopened ancestors or final file to the parent descriptor and entry observation used by enumeration. If a directory is replaced after it is listed, the root-relative reopen can judge and read a replacement tree without comparing it to the enumerated directory. M3-C item 2 requires examination and open relative to the same retained parent descriptor.

Required change: Have the extent walk open from its enumerating retained parent and compare the original entry observation, using the shared custody/opening primitive. Keep root-relative component traversal for pre-walk captures, or retain and revalidate an authenticated chain that proves it is the same enumeration parent. State the binding explicitly and add an ancestor-directory replacement control; per-file lstat/open swap tests alone do not cover it.

### C1APLAN-R2-RF-3 — LD-C1A-8 does not preserve the law's descriptor bound and check order

`docs/implementation/m3/snapshot-plan-c/c1a/PLAN-r2.md:182`. LD-C1A-8 counts canonical source-inventory bytes against 4 MiB, but item 5 bounds the whole canonical snapshot descriptor, which also contains schemaVersion, projectId, resolvedConfigDigest, scopeDigest, vcsDigest and the object framing. An inventory below 4 MiB can therefore yield an oversized descriptor, so the promised crossing-row refusal and agreement with final checks do not follow. LD-C1A-8 also returns SnapshotBound during the walk before reading the crossing file, whereas item 6 orders the walk/read set and VCS observation before bounds. For an over-limit tree with a later changed or custody-refusing file, early return changes which typed refusal is produced.

Required change: Separate resource-accounting guards from the law's final semantic bounds. If an incremental full-descriptor size calculation is used, include the complete canonical snapshot envelope and correct escaping/separators, with boundary controls where the inventory fits but the descriptor does not. Preserve the law's refusal order, or obtain a law decision authorizing early-bound precedence and its mixed-error controls before calling the final and incremental checks equivalent.

## Other requested decisions

**Q1:** The security/host split is compatible with C1-T2 once the parent binding in RF-2 is fixed. Chunk custody and one source-read loop preserve the one-read rule. Reuse, no retry, retained observations and post-seal custody consumption remain the correct obligations.

**Q2:** A snapshot constructor remains justified: `with_limits` cannot raise the global profile to the required caps, while `discovery_profile` has the wrong object limit and a separately fixed byte cap. Whole-file `work_ledger.rs` pinning necessarily makes the receipt stale. The explicit C1a1 re-pin, honest outstanding status, C1a4 pre-/post-reviewed blind refresh and return-to-law path follow the accepted precedent. This approves neither an unproved pricing model nor a blind run in this review. RF-1 must be resolved before the profile or margins can claim the recipe's coverage.

**Q3 / LD-C1A-5:** The interim internal VCS refusal is appropriately limited and now covers D15. C1b still owes Git/member observations; no public route is invented for this unreachable partial-library state.

**Other lead decisions:** The shared extent, caller-owned private custody, no ambient TMPDIR input, fixed reused buffer and empty read set until C1c remain appropriate. The B1 resolver input's project carrier is the correct source of the presence/digest observation; winning leaves alone would lose presence. The seven-row join stays complete, including type/exclusion and absent-present cases, with local/member carriers outside the root join. No operational X2 bytes may supply inventory rows.

The identity-v3 snapshot shape confirms that the inventory is only one field of the descriptor. `IdentityCandidate::from_json` supplies registered-schema admission, order checking and the snapshot identity recipe; the final row, descriptor and total-byte checks must retain the law's typed outcome and sequencing. C1b, C1c and J retain their own VCS, read-set, composition, public-projection and end-to-end controls.

Planned base/candidate suites, warning-denied Clippy, format checks, vector/source pins, FW-01/environment checks, design verification and mutation gates are useful, but need the mixed-error, ancestor-replacement and worst-cost-envelope controls identified above. No tests, builds, generators or census runs were executed.

No non-blocking observations. This is a plan review, not implementation acceptance, product qualification or C1 completion. Only read-only file reads, hashing, JSON parsing and Git queries were used. No network, delegation or prohibited private-data access occurred. Only this directory's `REVIEW.md` and `review.json` were written; neither repository was edited.
