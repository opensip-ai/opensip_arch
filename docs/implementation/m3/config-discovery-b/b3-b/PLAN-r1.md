# B3-b implementation plan r1: multi-repository workspaces (D15) — members, readers and the member-observation bound

**Lead plan, 2026-10-16. Proposed; it needs Codex review.**

**Bases:**
- product `15a8ac0` (inventory v202, 167 contract successors);
- architecture `2cd0bb771` (shared status r101).

**What precedes it:**
- B1-a, B1-b, B3-a and B2-a are bound.
- B2-b is bound through B2-b4c: the walker, the census, caps 2^22/2^21/2^30, and the blind held-out run.
- B2-c's four plan-r2 steps are bound, so the native unit instrument already applies B-S1's member rules over `AdmittedBoundaryInventoryV3`.
- **B2-b's workspace full-ledger margins are outstanding until this unit's member-observation bound** (M3-B item 12).

**Authority:**
- law M3-B r9, items 12, 19 to 24 and the unit table row "B3-b: D15: X2 r9 item 6b in `git_tracking.rs`; the readers (item 20); members in V3 records; `WorkspaceLinkSetV1`; item 24's rows" (`PROPOSAL-r9.md`, "Units after the law");
- X2 r9, which is M3-B item 21 (successor S1, accepted);
- design unit **B-S1**: SL S3 and NE §1.4 passages, the V3 schemas (`DiscoveryProvenanceV3`, `MemberRepositoryV1`, `MemberDeclarationV1`, `WorkspaceDeclarationV1`, `UnresolvedDeclarationEntryV1`, `AdmittedBoundaryInventoryV3`), and the closed reader registry `workspace-declaration-readers.v1.json`;
- B2-b0, the current discovery reference (contract successor 164);
- B2-c0 (contract successor 166).

## 0. What B3-b delivers, and what it does not

**Delivers:**
- **X2 r9 item 6b, the member observation** (law item 21). For each counted candidate it checks placement M1 to M3, the closed Git layout, the effective configuration with item 6a's refusals, `commondir` and `config.worktree` absence, and item 6a's exact index decoder. It reads `M/.git`, `M/.git/config` and `M/.git/index` only, through retained no-follow descriptors, charged on the discovery ledger.
- **The two declaration readers** (law item 20), exactly as B-S1's registry fixes them: `cargo-config-patch@1` and `npm-workspaces-members@1`. They cover branch A (an admitted `workspaceRoots` array: readers declare no member and only link), branch B (absent: readers declare members), and the root-in-repository rule (W fails W2: nothing declared, literal entries disclosed).
- **Membership in the discovery records.** Members are not boundaries. The walker enters them as ordinary directories, and nested repositories inside a member stay boundaries. The outputs are complete `DiscoveryProvenanceV3` (`memberRepositories`, `memberConfigs`, `workspaceDeclarations` with `unresolved`) and `AdmittedBoundaryInventoryV3.memberRepositories`. The B2-b "pending provenance" shape (LD-B2B-3) is retired.
- **The declaration half of the link set.** The link rows B-S1's registry fixes, as typed values. They are honoured by no one before successors S5 and S6.
- **Item 24's rows:** refusals and disclosures, with no new code.
- **The member-observation ledger bound** (item 12), a reviewed upper bound derived from the 6b code with its cost closure pinned. With it, **the workspace rows' full-ledger margin**, which closes B2-b's outstanding gate, or returns the caps to the law if a row fails.

**Not delivered:**
- C1's snapshot of members and the version-3 `vcs-observation` (successor S4, C1).
- Cargo and npm link honouring (S5, S6).
- The FW-14 harness outputs and S8's `git-conventional` assembly (B3-c).
- Recognition (B2-d).
- Production callers (J1).

## 1. B3-b0: the members-and-readers reference (design unit; contract successor 168)

**Why.** B-S1 fixes the readers, placement, the member cap, dispositions, links and records as text. The B2-b0 reference (`discovery_scan_reference.py`) leaves `workspaceDeclarations` pending and members empty. No executable oracle exists for item 20 or item 24. Following B2-b0 and B2-c0, a reference comes first.

**Content.** A wrapper over the B2-b0 reference at its accepted bytes, which edits none of them. It adds:
- **The readers,** over an in-memory tree model: carrier custody verdicts, Cargo TOML parsed as data with Python's standard `tomllib` (the pinned interpreter's; no added package), and exact JSON.
- **Placement and candidates** (`membershipByPlacementOnly`), the cap (n > 64 refuses `PROJECT.SCOPE_LIMIT`, `members:<n>>64`, counted before any 6b read), and branches A and B with root-in-repository.
- **Item 6b as a supplied verdict per candidate.** The layout, configuration and index decisions are item 6a's reviewed decoders, unchanged (law item 21: "item 6a's admitted layout, unchanged"). The reference does not re-model them; B3-b1's product tests own them with Git fixtures.
- **Links,** with `ambiguous-provider`, `patch-target-name-mismatch`, `provided-version-unusable` and `link-manifest-unusable`.
- **The `unresolved` rows,** one disposition per entry, ordered by the UTF-8 bytes of the entry.
- **The completed `DiscoveryProvenanceV3` and `AdmittedBoundaryInventoryV3`,** validated against B-S1's schemas.
- **The member-aware walk:** members entered, with their nested repositories as boundaries.

**Checker.** Cases for every registry reason and every item 24 row; both branches from each array source (project layer, local layer, `--workspace-root`); W failing W2; 64 and 65 members; a glob crossing; an ambiguous provider; a name mismatch; a member's own `opensip.json` recorded in `memberConfigs` and not consulted. The B2-b0 reference's own cases replay unchanged with no declaration (no-member equality).

**Bound** as contract successor 168 (`ACCEPT-DESIGN-UNIT`). It is design only.

## 2. B3-b1: item 6b in `git_tracking.rs` (product, security)

**Design:**
- **`observe_member`** composes item 6a's existing pure parts (`parse_config`, `check_config`, `check_environment`, `decode_index`) and its native helpers for one candidate under W. It runs the positive no-follow VCS-marker lookups at every directory strictly between W and M and at M, the layout, and the three objects.
- **Its result** is `Admitted { gitlinks }` or a refusal with X2 r9's subject: `member-vcs-unsupported:<reason>`, `member-outside-volume`, or the S3 custody subjects.
- **The environment check** runs once per pass.
- **It writes nothing** and reads nothing else under `M/.git`.
- **Precondition.** Item 6a's observation of W is `NoRepository`. The type system carries it: 6b takes the `NoRepository` evidence value.
- **Waiver.** `--trust-project-owner` never applies to member Git evidence (item 23). `--trust-group` applies as `judge_project_object` applies it.
- **`git_tracking.rs` is outside the census closure,** so this sub-unit leaves the census and the blind receipt current.

**Controls (law item 21).** Synthetic Git fixtures created by tests in a private 0700 scratch under a synthetic H:
- a conventional member;
- a `.git` file;
- `core.worktree`;
- an `include`;
- `extensions.objectformat=sha256`;
- `commondir` present;
- a split index;
- a submodule gitlink inside a member;
- a `.hg` between W and M;
- W inside a repository;
- a member on another volume (synthetic where the platform cannot create one).

Each refusal is tested with its subject. Item 23's control is included too: a waived explicit root admits an other-owned member directory but refuses that member's other-owned `.git`.

## 3. B3-b2: readers, membership and the V3 records (product, security)

**Design:**
- **A new module, `custody/workspace_declarations.rs`,** holds the two readers. Each reads its carrier at W as data, under S3 config-file custody, from retained descriptors on the discovery ledger.
- **Parsers.** Cargo uses the pinned `toml` crate through `opensip-identity`'s existing `parse_toml` (no new dependency; B2-c1's precedent). npm uses exact JSON admission.
- **Placement, the cap, branches A and B, and root-in-repository,** as B3-b0 states them. Then 6b (B3-b1) per counted candidate, in ascending path order.
- **Membership feeds the existing `member_roots` input** that B2-a and B2-b already thread through the shared rule and the scan. **The walker and the scan change only where members must be entered:**
  - a member root's VCS directory is not recorded as a nested repository;
  - the walker descends into a member as an ordinary directory, and its nested repositories stay boundaries;
  - `DiscoveryProvenanceV3` is completed and serialized with `workspaceDeclarations`, and the pending shape is removed.

  **These files are in the census cost closure** (`discovery_scan.rs`, `discovery_walk.rs`). See section 4 and LD-B3B-4.
- **Links.** Link rows are derived after membership is final, inside members only, with the registry's reasons.
- **Item 24's rows** route through the existing details: `PROJECT.EXPLICIT_PATH_INVALID`, `PROJECT.ROOT_CUSTODY_REFUSED`, `PROJECT.SCOPE_LIMIT` and their subjects. There are no new codes.

**Vectors.** `tools/security/workspace_member_vectors.py` runs B3-b0 and writes the vectors. The security tests compare the records byte for byte over scratch trees with synthetic conventional `.git` members.

**The T2 link-map control (law item 20's first control).** The four T2 workspaces must give their overlay's exact link maps. T2's own assembly has no `.git` (law item 19), and B-S1 admits a member only by a `.git` directory. **Plan:** the test reconstructs, in scratch, each lead-readable workspace's carrier (`W/.cargo/config.toml` or `W/package.json`, generated from the overlay as T2F §6 and item 20 state) and each linked package's manifest from the pinned T2 store. It gives each member a synthetic conventional `.git` with an empty valid index, and compares the derived links to the overlay's map (`overlayDigest`). Held-out workspaces are not read (see 4.3).

**The joint sweep (item 22's control).** The P3 fixture extended with members runs through the walker and B2-c1's native unit instrument: the subset test passes, and a removed member refuses `native.boundary-inventory-mismatch`.

## 4. B3-b3: the member-observation bound, the census successor and the workspace margins

### 4.1 The bound (item 12, "Each workspace row also carries its D15 member observation's ledger cost")

The bound is derived from B3-b1's and B3-b2's code, in objects, edges and bytes, over everything 6b and the readers charge for n members:
- each bounded read's full buffer growth (a 4 MiB index can charge 12,578,817 bytes of buffers);
- decoding (twice the index length);
- opens, status and custody;
- retained records;
- the reader carriers (4 MiB each) and provider manifests;

all under an explicit read-retry envelope. X2's ceilings (4 MiB index, 64 KiB config) are inputs to the derivation. The cost closure (`git_tracking.rs`, `workspace_declarations.rs` and the platform read helpers they call) is pinned as the census pins the walker's.

### 4.2 The census successor

B3-b2 changes two closure files, so the census tool's `CLOSURE` and cost anchors must be re-pinned and its cost model extended for member descent.

**The no-member invariant.** The census, re-run over every lead-readable repository entry with the new closure, must produce records byte-identical to B2-b4b3's. A non-workspace project's charges must not change.

### 4.3 The blind held-out receipt and the workspace rows

- **The blind receipt.** It binds the closure, so it becomes stale. **Lead decision LD-B3B-5:** refresh it by re-running the reviewed blind mode (B2-b4c1) mechanically with the re-pinned closure. That is the method the owner chose on 2026-10-16 for the held-out margin, with no held-out content opened by the lead. Codex is asked to rule whether this needs a fresh owner decision.
- **The workspace rows.** For each T2 workspace row, the full-ledger cost is the walker's census cost (with members entered) plus the member-observation bound at the row's member count. Each row must hold the 2× margin under the r7 caps. **If any row fails,** the caps return to the law (a recording or revision step), as item 12 requires; nothing is truncated. **Held-out workspace rows,** if any, are measured only through the blind mode.

## 5. Lead decisions

- **LD-B3B-1. A reference first** (B3-b0), as B2-b0 and B2-c0 were. **Rejected:** writing the product against B-S1's prose alone, because item 24 and the registry have about 20 interacting dispositions with no oracle.
- **LD-B3B-2. Item 6b reuses item 6a's reviewed decoders unchanged;** the reference supplies 6b's verdicts. **Rejected:** a second Python Git decoder, which would duplicate X2b-2's reviewed code with no added assurance.
- **LD-B3B-3. The link rows are typed values, not a published record.** No contract defines `WorkspaceLinkSetV1`'s bytes. Its Plan binding belongs to S5 and S6, so B3-b fixes only the declaration half B-S1's registry states. **Rejected:** inventing the record's schema here.
- **LD-B3B-4. The census closure changes, and is re-pinned with a no-member equality proof.** Members must be entered by the walker and must not be recorded as nested repositories, which the closure files decide. **Rejected:** a parallel member walk outside the closure that rewrites the observed scope, which would misstate observed VCS facts to avoid a re-pin.
- **LD-B3B-5. The blind receipt is refreshed by the owner-chosen mechanical blind mode** (section 4.3).
- **LD-B3B-6. The T2 link-map control uses scratch reconstructions with synthetic conventional `.git` members** (section 3). T2's `vcs: none` assembly cannot admit members under B-S1.
- **LD-B3B-7. Five steps under one plan,** each followed by its inventory where paths are added:
  1. B3-b0, the reference (design);
  2. B3-b1, 6b (product);
  3. B3-b2, the readers and members (product);
  4. B3-b3, the bound, the census successor, the blind refresh and the workspace margins (product and evidence);
  5. a status round.

  B3-b1 can proceed in parallel with B3-b0, because it depends only on item 21 and X2b-2's code.

## 6. Questions for the reviewer

1. Is LD-B3B-5 (the mechanical blind refresh under the existing owner decision) within that decision, or is a new owner decision needed?
2. Is LD-B3B-6 the lawful reading of item 20's first control, given that T2's assembly has no `.git`?
3. Is the no-member equality proof (4.2) sufficient for the census successor?
4. Is LD-B3B-3 (no published link record) consistent with the unit table's "`WorkspaceLinkSetV1`"?

## 7. Not claimed

- No snapshot of members and no version-3 VCS observation (C1, S4).
- No link honouring (S5, S6).
- No harness outputs (B3-c).
- No production caller (J1).
- No qualification.

B3-b is complete only when its five steps bind, and B2-b only when the workspace margins hold.
