# C1C-PLAN-r1 review

**Verdict: REQUIRED-FINDINGS.** Three required findings and two nonblocking observations.

## Subject verification

Manifest: 383 bytes, SHA-256 `6a603d1c445b7700446ef3886a325b87a4137380352987ac6a9a991a9a0c1d2b`. Its single member PLAN-r1.md is 22,877 bytes, SHA-256 `b9c040834b12535cd88f0ea4c6bbf9c2682c5a1507d1fb14dc13698e3ad01eb4`; both hashes and sizes verified. Live product HEAD `3d1d771ecc5a8772d57f8393ce09cc82ce5f025a` and architecture HEAD `2d169666ee5c28eedea5e43083b7968b6ba80e9f` match the manifest bases.

## Required findings

### C1CPLAN-R1-RF-1 (P1): Separate read authorization from the outermost pruning classifier

Location: `docs/implementation/m3/snapshot-plan-c/c1c/PLAN-r1.md:50`.

LD-C1C-3 correctly uses classify_path to decide whether a path lies in a pruned tree, but LD-C1C-5 then uses the shared rule to decide descent below an authorized realPath. The actual classify_path (discovery_rule.rs:153-180) returns only the outermost anchor. For node_modules/a/lib it still returns node_modules, so descending unless the rule prunes rejects ordinary package subdirectories. Ignoring that outer hit instead does not reveal node_modules/a/node_modules/b or node_modules/a/.git: they return the same outer hit. cargo_roots_from_markers also deliberately excludes markers inside every pruned tree (:182-199), so the existing first-party Cargo-root set cannot identify package-local target output. IE explicitly states that the outermost pruned anchor is not the read-authorization boundary. The proposed API cannot implement the positive and negative controls as stated.

Required change: Define a shared-rule-owned read-set predicate/API with explicit authorized-directory semantics, retaining the existing outermost classification for discovery. It must admit ordinary descendants, stop at further exact node_modules segments, enforce VCS exclusions throughout the full path and discover package-local Cargo roots for target exclusions. Check forbidden ancestry of realPath itself as well as descendants. Do not duplicate private rule tables in the reader. If this changes discovery_rule.rs or another closure file, revise LD-C1C-9 to include its whole-file closure re-pin and receipt impact. Add controls for ordinary lib/x.ts, pnpm paths, nested packages, VCS above/at/below realPath and Cargo output inside a package.

### C1CPLAN-R1-RF-2 (P1): Preserve ignore and boundary exclusions when admitting read-set rows

Location: `docs/implementation/m3/snapshot-plan-c/c1c/PLAN-r1.md:43`.

The reader is described as taking admitted layouts and including suffix-matching files whenever classify_path says they are pruned. That classifier knows only conventional pruning and Cargo/member anchors, not Config2 ignorePaths or admitted boundaries. No read-set decision in LD-C1C-3/5 or sealing check in LD-C1C-7 applies those other extent exclusions. Thus a layout for node_modules/a can add node_modules/a/x.ts even when node_modules/a is explicitly ignored or lies under an excluded boundary. Item 6 retains boundaries and ignorePaths as exclusions, and item 1 requires captures outside the admitted extent to remain leftovers. A layout is an exception to dependency-tree pruning; it is not authority to override every exclusion.

Required change: Pass or bind the applicable admitted extent to the read-set owner and apply exact ignorePaths/boundary exclusions before descent, capture reach/origin changes and inventory admission. Preserve the same-root provenance of that extent. Define the outcome for a required manifest excluded this way without silently inventorying it; keep the leftover/refusal rules. Add ignored-package and excluded-boundary controls, including a C2-captured manifest, and retain first-party workspace-link behavior.

### C1CPLAN-R1-RF-3 (P2): Record freshness separately for each receipt and its actual bindings

Location: `docs/implementation/m3/snapshot-plan-c/c1c/PLAN-r1.md:80`.

LD-C1C-9 says neither sub-unit changes a discovery closure file, but copies the requirement to render discovery stale rows into every C1c stale interval. Under the listed changes, the discovery receipt remains current: receipt_bindings (discovery_census.py:1086-1095) binds its tool, closure, member model, caps/sizes, roots and reference inputs; it does not bind snapshot.rs, snapshot_source.rs, snapshot_ledger_model.py, snapshot_seal.rs or the proposed new module. A standalone C1c interval after an accepted refresh therefore stales the companion snapshot receipt, not the discovery receipt, and compose_held_out cannot produce the mandated stale discovery rows. Joining an already stale C1b batch is a different case.

Required change: Make the evidence receipt-specific: compare each receipt with the actual baseline/current bindings, report an empty delta and current discovery rows where unchanged, and require stale rendering only for a receipt whose inputs changed. Distinguish a standalone C1c interval from joining C1b and any revised shared-rule closure change under RF-1. Keep both generated-output checks passing and ensure every receipt is current at the final reviewed refresh without treating fabricated discovery staleness as required evidence.

## Nonblocking observations

**C1CPLAN-R1-NBO-1: Make the full-ledger derivation inputs explicit** (`docs/implementation/m3/snapshot-plan-c/c1c/PLAN-r1.md:71`).

The intended fixed-cap gate is sound, but its implementation evidence should explicitly include normalized/deduplicated layout bookkeeping, charged classifier temporaries, root reaches, buffers and overlapping-directory traversal, in addition to per-row session work. The 100,000-row limit is per layout, not a global limit on the input slice. The shared item-5 descriptor bounds the combined inventory, not all layout-processing work.

State the full walk/session/sealing/read-set subtotal and include the accepted VCS term when present. Source any layout-count bound actually used; otherwise place excess non-row/setup work explicitly in the typed-refusal regime. Require soundness vectors and full fixed-cap/2x evidence before C1c-1 acceptance.

**C1CPLAN-R1-NBO-2: Name the C2b obligations if the stale interval spans its integration** (`docs/implementation/m3/snapshot-plan-c/c1c/PLAN-r1.md:83`).

If C1c-0 opens a standalone interval and refresh waits for C1c-1, C2b necessarily integrates during it. This is compatible with the no-reliance rule only if C2b does not require the stale companion receipt, and all intervening census-input changes are tracked before the final freeze.

List C2b as an intervening integration in that batch schedule, with its census-input ownership and no-stale-reliance obligation, or refresh C1c-0 separately if C2b requires current evidence. Reconfirm the exact accepted baseline and final frozen inputs at the pre-run review.

## Question rulings

**Q1.** Accept the preparatory split: C1c-0 supplies item-1 capture machinery needed by C2b and may land first; C1c-1 remains the item-3 read-set unit and integrates only after C2b's layout. This does not waive C2b or C1c-1 acceptance, nor authorize a production read set before the integration edge is met.

**Q2.** Agree: S3 directory custody applies above the dependency-tree anchor; at and below it use descriptor discipline, metadata/inode checks and no retry. Do not impose config-file custody or its 4 MiB marker ceiling on an installed manifest merely because its name is package.json. Keep first-party captures on the existing opener. C2 must separately account for parsing/retention and its own read bounds; no new unsourced per-manifest cap is approved.

**Q3.** Agree with exact, case-sensitive byte suffixes for the nine listed suffixes. Declaration suffixes are included by their .ts/.mts/.cts ending. No extra suffix, case folding or compiler-driven late read. The table remains C2/F-owned.

**Q4.** Accept filtering nonmatching regular-file names before LogicalPath admission: they are outside item 3's read set and are counted/disclosed without being read. Validate every candidate row and every directory actually descended; a malformed matching name refuses with escaped bytes. Use raw-name suffix filtering safely for non-UTF-8 names, and never open special files or follow links. This is the read-set suffix exclusion, not permission to weaken the first-party walk's name rule.

**Q5.** A complete conservative derivation plus synthetic/native soundness and boundary controls can gate C1c-1 while no representative admitted-layout T2 population exists. It must cover the full cumulative ledger at r9's fixed caps and 2x margin, with explicit typed-refusal terms; the existing no-layout census is not measured read-set evidence. Keep the ordinary census checks and required reviewed receipt refreshes. Add a measured installed-layout population when H-NM supplies it; no compiler/harness recipe execution or held-out inspection is authorized by this review.

## Other conclusions

The C1c-0/C2b/C1c-1 split is coherent as a preparatory capture unit followed by the layout-dependent reader. The custody distinction in LD-C1C-2 agrees with SL:266 and item 3. LogicalPath validation after removing at most one trailing slash is a defensible inventory-path restriction: CanonicalPath admits spellings that cannot be inventory Blob paths, and they must not be silently normalized into different identities.

Deduplicating realPath traversal is compatible with the read-once session. Preserve the per-layout-row digest join even when multiple rows share a normalized realPath; conflicting manifest digests must refuse rather than disappear during deduplication. Reached C2 captures must be re-observed through the enumerating parent and reused, never read again. First-party workspace-link package manifests may already be Walk captures: their digest join must not require converting them into ReadSet rows. Unreached required captures remain leftovers. No-layout identity preservation, origin outside identity, and joint item-5 row/descriptor/total bounds are appropriate.

The proposed sealing check is a useful structural guard and can keep its public refusal at Run closure. It does not prove the host performed every permitted read; IE expressly treats completeness as a host-TCB observation. Its layout/provenance and effective-extent inputs must agree with the reader after RF-1/RF-2. The evaluator join currently accepts installed-package rows without testing package-local Cargo output because its dependency branch continues before the Cargo check; the plan correctly requires the reader to be stricter. A passing evaluator cross-check alone does not validate that stricter exclusion.

The shared sealing-file arrangement with C1b is sound: distinct steps, rebase onto the accepted other edit and retain unique current census anchors. No new sealing allocation/charge is required merely for a borrowed structural comparison. Typed read/layout/digest/change/custody/I/O refusals and distinct WorkFailure::Budget are appropriate; J2 owns public projection.

Controls and mutations cover C1-T12 to C1-T14, suffixes, special files, descriptor races, custody split, reuse, manifest digests, first-party containment and bounds. Add the RF-1/RF-2 controls before treating the set as complete. Model vectors/cap evidence and receipt refreshes are future implementation gates, not delivered by this plan. Ruling Q5 does not replace them with a no-layout census.

## Review boundaries

Used only read-only reading, hashing, JSON parsing and Git queries. No Cargo, rustc, builds, tests, lanes, network, panes or delegation. No private fixture, installation directory, signing keys, held trees, T2 stores or cache were accessed. Neither repository, worktree nor control files were edited. Only REVIEW.md and review.json were written in the requested directory.
