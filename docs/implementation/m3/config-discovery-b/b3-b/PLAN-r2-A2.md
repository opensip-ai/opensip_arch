# B3-b plan r2, amendment A2: B3-b2b as a pure decision core, then its native observation and composition

**Lead plan amendment, 2026-10-16. Unreviewed, round 2** (round 1: Codex `codex-b3b-plan-a2-r1`, REQUIRED-FINDINGS; see A2-4). It amends the accepted B3-b plan r2 (`PLAN-r2.md`), as A1 already amends it (`PLAN-r2-A1.md`, Codex `codex-b3b2a-r1`). Law M3-B r9 is unchanged. B3-b2a is bound (product `58d450c`, inventory v204).

## A2-1. B3-b2b in two steps

A1-1 leaves B3-b2b as the rest of section 3: the readers, placement, the cap, branches A and B, root-in-repository, item 6b per counted candidate, `workspaceDeclarations`, links, item 24's rows, the vectors, the T2 link-map controls and the joint sweep. Under A2 it is delivered in two steps. **Every obligation of section 3 stays, and lands in one of them.**

### B3-b2b1: the readers and the membership decision, as a pure core

**The core, `custody/workspace_declarations.rs`.** It is B3-b0's `discover` without SLM's two passes. It reads everything through an observation interface, `WorkspaceObservation`, which mirrors the reference's only access paths (`_entry`, `_bytes`, `_markers`, the listings, and `memberObservations`):
- an entry's observed metadata (kind, owner, mode, device, ACL state, link count, size), keyed relative to W;
- a carrier's or provider manifest's bytes;
- the VCS markers a directory holds, with each marker's kind;
- a directory's children, for the lawfully visible repositories;
- item 6b's verdict for a counted candidate.

**What the core decides,** in B3-b0's order:
- carrier selection and the carrier rows;
- directory custody and config-file custody, judged by the existing pure checks (`check_project_object*`, as the scan core judges);
- the 4 MiB carrier cap;
- the readers' parsers: Cargo through `opensip-identity`'s `parse_toml` (B2-c1's precedent), and npm through `parse_json`, the product's exact JSON admission, which is the counterpart of the foundation's `canonical.parse` that B3-b0 uses. `TomlTableView` gains read-only iteration (`iter`, `len`) so that the reader can enumerate `[patch.<source>]` tables. **(r2) Parser failures, including resource bounds:** every `parse_toml` error is that object's existing `parse` disposition (`ByteLimit`, `RecursionLimit`, `NodeLimit`, `InvalidUtf8` and `Syntax`). For a carrier, that is `state: refused, stateSubject: parse`. For a provider manifest, it is `link-manifest-unusable` with subject `parse`. This is the accepted G2 precedent, where every `TomlError` is `DependencyLockError::Parse`. No public code is added and the admitted grammar does not change: these bounds are the parser's local limits (`MAX_NODES` 1,000,000, and its recursion limit). The npm side keeps `parse_json`'s profile, which equals `canonical.parse` on bytes (4 MiB), depth (32), integer range, duplicate keys, floats, negative zero and Unicode scalars;
- entry shapes and the entry-path grammar;
- npm glob classification over the visible repositories;
- placement (`_place`: absence, candidate, other volumes and inner boundaries, with SX-1 at W and at the candidate);
- candidate failures, the 64-member cap, branches A and B, and root-in-repository;
- item 6b's supplied verdicts, in path order;
- links and their dispositions;
- the declaration rows.

**Two phases around the walk.** Branch A decides SLM-first: B3-b0 runs a trial pass two with the provisional members and makes member decisions only if it accepts. So the core is:
1. **Phase one:** the readers, placement and the provisional members. This is branch B's final member set, or branch A's provisional set.
2. **Phase two:** branch A's member decisions, given the trial walk's verdict. These are placement, other volumes, the cap and 6b, each in path order. A member-rule refusal carries the provenance of the discovery without members (LD-B3B0-5).

Links follow once membership is final. The walk itself is B3-b2a's, and the core never walks.

**Vectors: `tools/security/workspace_member_vectors.py`.**
- **Inputs:** B3-b0's own D15 checker cases (`b3-b-reference/evidence/check.py`, `d15_cases`) and their synthetic inputs, at the reference's bound bytes. No case is invented.
- **Per case:** the observation, as the side tables and synthetic tree the core's test implementation of `WorkspaceObservation` reads; the phase-one result; the trial verdict; and the expected outcome. The outcome is the member set with `declaredBy`, the refusal code, path and detail, the declaration rows, and the links.
- **The check:** the security test runs the core over each case and compares the outcome byte for byte.
- **(r2) Forbidden access (Codex B3BA2-R1-RF-2).** Each vector carries the reference's access record: every W-relative path its reader code looked up (`_entry`, as B3-b0's checker `OBSERVED` spy records it) and every path it read (`contents`, the checker's `SpyContents`). It also carries the checker case's own `notRead` and `notObserved` lists. The test's `WorkspaceObservation` adapter records every `entry`, `markers`, `children` and `bytes` call. The test then asserts that:
  - the core looked up nothing the reference did not look up;
  - the core read nothing the reference did not read;
  - nothing in the case's `notRead` and `notObserved` lists was touched.

  These cover a member's SX-1 anchor, dependency, VCS and Cargo `target` anchors, hidden glob repositories, and the enclosing boundaries that are visible. **A mutation** that makes a forbidden lookup or read without changing any output (for example, a lookup below a pruned anchor before classifying it) must make the test fail.
- **(r2) Parser differential controls (Codex B3BA2-R1-RF-1).** These are added beside the bound checker cases, which stay the unchanged baseline. They are generated by the vector tool and labelled as controls, not as reference cases:
  - **TOML.** A Cargo carrier and a provider `Cargo.toml` that are otherwise usable, each with an unrelated field deeper than `parse_toml`'s recursion limit, and each with an unrelated array over its node limit within 4 MiB. The reference (`tomllib`) reads them. The product refuses them with the existing `parse` disposition: the carrier `refused/parse`, and the manifest `link-manifest-unusable/parse`. The vector records both outcomes, and the divergence is a stated product bound, not a grammar change.
  - **JSON.** npm carriers and provider `package.json` files at and past each `parse_json` bound (bytes, depth 32, integer range), with a duplicate key, a float, negative zero and a lone surrogate escape. The reference's and the product's dispositions must be equal for every one.
- **The walker records** (pass two) are not re-compared here: B3-b2a's member vectors already bind them.

### B3-b2b2: the native observation, item 6b and the composition

**The native `WorkspaceObservation`,** on the discovery ledger, from W's retained descriptor:
- no-follow opens;
- carrier and manifest reads bounded at 4 MiB, with their custody captures;
- positive VCS-marker lookups;
- the listings for the visible-repository classification, which never enter a pruned anchor or a boundary.

**Item 6b over the counted candidates,** in path order (B3-b1's `observe_members`).

**The NoRepository binding across the operation handoff.** Item 6a's fenced observation and the admission's chain end up stored together in the operation's subject (`Eligible { admission, tracking }`, or `RegisteredProject`). So B3-b1's borrowed `RootObservation` cannot be held there.

- **Recommended: a process-unique, never-reused identity for each `ProjectChain`.**
  - Item 6a records it in `TrackingObservation`. A recheck over the same chain sees the same identity.
  - The proof constructor admits only a chain whose identity equals the observation's, with `NoRepository`. This is a retained-object identity, not a label (Codex B3B1-R2-RF-1).
  - `ProjectChain` is not `Clone`.
  - This changes `project_chain.rs`, a closure file, so B3-b2b2 re-pins it with A1-2's equality projection.
- **Rejected:** an unfenced second item-6a pass before 6b. It would make 6b's precondition a different observation from the one item 6a decided under the fence.

**The composition, `discover_with_members`:**
- phase one;
- in branch A, the trial walk with the provisional members (B3-b2a), then phase two;
- in branch B, item 6b, then the walk with the final members;
- links;
- the complete `DiscoveryProvenanceV3`, with `workspaceDeclarations` serialized and the pending shape removed;
- for a member-rule refusal, the walk with no members.

**The scenario path uses it.**

**Section 3's T2 link-map controls (a) and (b), and the joint sweep, unchanged.** Control (a)'s seam supplies the member set at the link stage (plan r2 NBO-1). It sits in the composition and is not a production placement bypass.

## A2-2. Why

B3-b0 has about 20 interacting dispositions, and its checker already enumerates them. A pure core over a narrow observation interface lets every case run byte for byte without a filesystem, as B2-b2's scan core did against B2-b0. The native observation, the handoff binding, the census closure change and the T2 controls are then a separate review, about I/O, custody and composition, against an accepted decision core. **Rejected:** one B3-b2b unit, whose review would mix the dispositions with the native observation, the handoff binding and a closure re-pin.

## A2-3. Steps (section 5, LD-B3B-7, as amended by A1 and A2)

1. B3-b0 (bound).
2. B3-b1 (bound).
3. B3-b2a (bound). **Then B3-b2b1, then B3-b2b2,** each followed by its inventory.
4. B3-b3a, B3-b3b and B3-b3c. (r2, Codex B3BA2-R1-NBO-1) Every native charge B3-b2b2 adds is assigned to exactly one term of section 4.2, and no charge is counted twice:
   - **the reader term,** paid at n = 0: the carrier reads, their parse, their custody and the declaration rows;
   - **the member term,** at n members: placement, the visible-repository listing, item 6b and the provider-manifest reads for links;
   - **member descent,** in the walker rows.
5. The status round.

## A2-4. Round 2 (Codex `codex-b3b-plan-a2-r1`)

| Finding | Resolution |
| --- | --- |
| **B3BA2-R1-RF-1:** the bound checker cases omit `parse_toml`'s resource differences | Every `parse_toml` error, resource bounds included, is the existing `parse` disposition (G2 precedent). Targeted TOML differential controls record the divergence from `tomllib`, and JSON alignment controls require equality with `canonical.parse` on every bound (A2-1, the parser bullet and the controls). The checker cases stay the unchanged baseline. |
| **B3BA2-R1-RF-2:** output-only vectors drop the checker's access assertions | The vectors carry the reference's lookup and read records and each case's `notRead` and `notObserved` lists. The adapter records every observation call. The test asserts that the core's accesses are a subset of the reference's and avoid every forbidden path. A forbidden-access mutation that changes no output must fail (A2-1, the forbidden-access bullet). |
| **B3BA2-R1-NBO-1:** keep the reader and member terms disjoint | A2-3 step 4 assigns each native charge to exactly one term, and keeps the reader term at n = 0. |
