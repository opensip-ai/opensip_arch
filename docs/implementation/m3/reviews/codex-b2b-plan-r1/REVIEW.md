# B2B-PLAN-r1 review

**Verdict: REQUIRED-FINDINGS.** Five plan corrections are required before implementation.

## Subject and facts

Rehashed `subject.json`: 449 bytes, SHA-256 `fe677ea48f2f84b18585ff335500ddaa37dadd1214f3036febf5159049824a23`. Its sole member, `docs/implementation/m3/config-discovery-b/b2-b/PLAN-r1.md`, is 13,906 bytes, SHA-256 `fdac2eac9fe9eecbbf8c0b4b1971ca94c06e85dbdc6a45bbae3c1062b200e7d6`. Both match.

Verified product HEAD `94e5fdebd63a174694dadbb5e647063855614b77` and architecture HEAD `424f64a3f331261d0f1e8fb323948492cda5a06d`, with clean tracked state. Section 0's implementation facts are accurate: the internal pure rule exists; ordinary ledger limits are 65,536 objects, 131,072 edges and 256 MiB; with_limits cannot raise them; ACL capture reserves 131 edges; selection omits the proposed upward provenance; native owner waiver remains unapplied; listing supplies names rather than a by-name metadata observation; the host projections exist; and discovery V3 schemas remain unmaterialized. The archived acquisition summary supports the 49 verified materialized T2 entries. No T2 tree, held-out entry or private cache contents were inspected; this review does not claim a fresh store verification.

The four-way split is reasonable, as are custody judgments focused on unit chains/markers, the existing host observation route and the test-only scenario seam. The split does not itself relax the parent unit's law or completion gates.

## B2BPLAN-1: Define a usable current-reference oracle and separate pending records from V3 serialization

Location: Section 1 B2-b2 vectors; LD-B2B-3 and LD-B2B-5.

The unchanged SLM imports the original DD, initializes provenance with schemaVersion 2, and recognizes only provenance versions 1 and 2. It lacks SX-1 and the accepted pruning-reference corrections. Its outputs cannot both reproduce byte for byte and validate as B-S1 V3. The planned Pending workspaceDeclarations also cannot validate as DiscoveryProvenanceV3. X2-only case supersessions do not resolve these differences.

Required correction: Specify the reviewed reference/projection path for B2-a pruning corrections, SX-1 and V3, explicitly separating historical SLM replay from current expected behavior. State which partial fields can be compared before B3-b, which complete outputs actually undergo V3 validation, and how the pending internal type is prevented from being accepted or serialized as current provenance. Preserve B3-b ownership without inventing absent reader observations.

## B2BPLAN-2: Choose the unit source before deciding traversal scope

Location: Section 1 B2-b3, each listed parent and observed-tree output; B2-b2 source selection.

The walker is specified as descending ordinary directories from the selected root and producing the observed tree before the core chooses explicit/config/automatic discovery. That widens an explicit source into a whole-root scan, contrary to MB item 13: explicit and configured roots are exact roots, never scan roots. Unrelated subtrees could consume the ledger or produce observations/refusals for an invocation that selected only a small root.

Required correction: Define separate observation strategies selected before walking. Explicit/config modes must observe only named roots and the necessary ancestor, boundary and pruning evidence; automatic mode may recursively enumerate. Add trace and budget controls proving that unrelated sibling and descendant trees are not scanned and that an admitted array does not fall through to automatic discovery.

## B2BPLAN-3: Retain the all-entry T2 margin as a B2-b acceptance gate

Location: Section 1 B2-b4, LD-B2B-4, section 3 completion condition.

MB item 12 requires a twofold objects/edges margin for every pinned T2 entry before B2-b lands. The plan excludes ten held-out entries and transfers their margin to qualification while allowing B2-b completion after B2-b4. Preserving the no-inspection boundary is correct, but it does not authorize weakening that gate.

Required correction: Keep all-entry margin evidence explicitly outstanding until an authorized harness supplies nondisclosing results for held-out entries, or obtain a separate accepted law change before altering the gate. The lead must not read held-outs. State that partial census success cannot complete B2-b. For a materialized-store census, require current integrity verification and no-follow counting equivalent to the pinned Git-tree population, with objects/edges margin distinguished from the separately bounded bytes.

## B2BPLAN-4: Assign implementation and controls for the typed project-owner waiver

Location: Section 0 custody; B2-b2 custody checker; B2-b3 analysis selection and LD-B2B-5.

The plan notices that every native custody check uses waive_owner=false, but assigns no change that consumes ProjectOwnerWaiver. ProjectChainPolicy::from_grants accepts groups only, and check_project_object unconditionally passes false to the shared owner check. Reusing those APIs cannot reproduce S3 owner-waiver behavior, including the required discovery cases.

Required correction: Assign the narrowly scoped typed-waiver plumbing to the appropriate sub-unit and applicable selection/unit-chain judgments, preserving X2 placement and non-owner custody checks and legacy behavior where required. Add a foreign-owned project inside an otherwise admissible home to avoid relying on the old outside-home case, plus no-flag, no-explicit-project and mode/ACL negative controls. Define marker-file waiver behavior from the governing rule rather than broadly weakening custody.

## B2BPLAN-5: Carry the by-name identity needed for the required observation/open comparison

Location: Section 1 B2-b1 observe_child_kind and B2-b3 identity recheck.

observe_child_kind returns only Directory/File/Symlink/Other/Absent. The walker later promises to compare st_dev/st_ino between observation and open, but that return type discards both identifiers. A fresh post-open sample alone cannot detect a replacement between the original by-name observation and open.

Required correction: Specify a charged no-follow by-name observation retaining kind and the identity metadata needed for the comparison, then compare it against the opened descriptor before using the object. Define absence/change behavior and refusal without retry. The swap control must replace an entry with another of the same kind and prove that the original identity is compared.

## Authority checks and decision assessment

MB item 12 expressly requires every pinned T2 tree and a twofold margin, before B2-b lands; its census bounds objects and edges, with bytes bounded separately. A materialized store can support equivalent mechanical evidence if verified and counted without following links, but an uncensused held-out population cannot silently become a qualification-only obligation.

MB item 13 expressly requires exclusive unit sources and exact explicit roots, the owner-waiver/group authorizations, a closed V3 provenance record for every project, and replay of all discovery cases. The 68-case file includes owner-waiver cases. Read-only SLM inspection confirms that its import remains the original DD (`security_lifecycle_model_v1.py:77-78`), its current provenance initializer is V2 (around line 624), and its version validator supports V1/V2 (line 85). These are reference differences beyond the X2-only supersessions listed in LD-B2B-5.

The proposed pending intermediate state can be useful before B3-b; it must have an explicit partial-record acceptance contract rather than simultaneous claims of complete V3 validation. B-S1 LD-4 makes V3 current for all projects; LD-10 and the schema require real reader observations. This review does not recommend fabricated absent declarations or moving the readers into B2-b.

`ProjectChainPolicy::from_grants` currently carries AuthorizedGroups only (`project_chain.rs:105-111`); `check_project_object` supplies literal false to the owner-waiver argument (around lines 545-557). The existing pure check supports the distinction, but the proposed reuse has no route for the typed waiver. X2's stricter placement can supersede an old outside-home fixture without eliminating the need to implement the waiver on admissible paths.

LD-B2B-1, LD-B2B-2, LD-B2B-6 and LD-B2B-7 are sound in principle. LD-B2B-3, LD-B2B-4 and the completeness of LD-B2B-5 require the corrections above. B2-c, B3-b, C1 and J1 should retain their stated responsibilities.

The listed CI trace, entry kinds, no-follow traversal, exhaustion, source modes and FW-01 controls are useful. They are insufficient until the five gaps are addressed, especially a same-kind identity swap, exact-source observation traces, the typed waiver and a usable current-reference oracle. No implementation or future test success is inferred from this plan review.

## Boundaries

Used read-only source/authority inspection, hashing, JSON parsing and Git queries. Ran no Cargo, tests, builds or lane; used no network, other panes or delegation; accessed no private 413 fixture, installation directory, signing keys, held trees or T2 held-out entry. Neither repository, stage nor control files were edited. Wrote only `REVIEW.md` and `review.json` in this review directory. No code, binding, law change or product qualification is claimed.
