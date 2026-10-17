# C1C-PLAN-r2 review

**Verdict: REQUIRED-FINDINGS.** Two required findings and one nonblocking observation.

## Subject verification

Verified the 572-byte manifest, SHA-256 `2dee52328359d82c57112c12cd9d109b071f03a5cd599f4c3f8d5ce6d9b397bb`, and both members. PLAN-r2.md is 33,396 bytes, SHA-256 `682088c37c89adf1ca846f91b7caf27b4264cea66876c13c3ad19ae8aaae8186`. PLAN-r1.md remains 22,877 bytes, SHA-256 `b9c040834b12535cd88f0ea4c6bbf9c2682c5a1507d1fb14dc13698e3ad01eb4`, matching the prior review. Live product HEAD `3d1d771ecc5a8772d57f8393ce09cc82ce5f025a` and architecture HEAD `2d169666ee5c28eedea5e43083b7968b6ba80e9f` match the manifest bases.

## Required findings

### C1CPLAN-R2-RF-1 (P1): Reject non-dependency exclusions in the authorized directory ancestry

Location: `docs/implementation/m3/snapshot-plan-c/c1c/PLAN-r2.md:62`.

The new API checks authorized ancestry for a node_modules segment and VCS segments, but its Cargo roots are derived only within the authorized package. It therefore does not reject Cargo output containing the authorized directory itself. For example, with Cargo.toml at the project root and realPath=target/node_modules/a, relative index.js passes the enumerated ancestry and descendant checks even though the whole package is Cargo build output. A separately listed nested package can similarly sit inside an enclosing package's Cargo target. SL:272-274 and item 3 exclude Cargo output at any depth, not only target directories discovered after starting at realPath. The API also lacks the exact root/member .opensip custody-anchor check: .opensip/node_modules/a meets its stated ancestry tests, while LD-C1C-12 only adds boundaries and ignorePaths. SnapshotExtent does carry member roots, but neither its boundary/ignore predicates nor the specified API applies that anchor rule. A layout must not override these exclusions. The evaluator's dependency-path branch continues before its Cargo test, so the cross-check does not close the Cargo gap.

Required change: Specify a shared-rule-owned check over the full authorized path and descendant path that preserves Cargo build-output and exact root/member .opensip exclusions as well as VCS exclusions. Supply or derive the necessary ancestor Cargo-root and member-root evidence, rather than only package-local markers. Apply it before opening/descending an authorized package, reaching a capture or changing origin, and in the sealing guard. Keep ordinary non-anchor .opensip directories and target directories without a Cargo parent eligible. Add controls for target/node_modules/a under a first-party Cargo root, a separately listed package inside another package's Cargo target, root/member .opensip ancestry, and the corresponding allowed lookalikes.

### C1CPLAN-R2-RF-2 (P2): Schedule a new interval when C1c-1 follows an already refreshed C1c-0

Location: `docs/implementation/m3/snapshot-plan-c/c1c/PLAN-r2.md:126`.

The two batch cases in LD-C1C-9 describe C1c-0 joining C1b's batch, or C1c-0 opening a standalone interval that normally lasts through C1c-1. They do not describe C1c-1 integrating after C1c-0's interval has closed. This is a permitted and likely order: C1c-0 joins C1b, C1b freezes and completes its reviewed refresh, then C2b and C1c-1 land; it also occurs when C2b requires a separate early C1c-0 refresh. C1c-1 then changes the snapshot recipe and sealing pins and stales the companion receipt again. The generic rule that every interval ends current does not open or schedule this later interval. Round one explicitly said C1c-1 opens its own interval after C1b's refresh; that sentence was removed.

Required change: State explicitly that C1c-1 joins an existing reviewed open interval only before its final-input freeze; otherwise C1c-1 opens a new interval at integration and owns its pre-run review, frozen-input blind refresh and post-run review before dependent work relies on the companion receipt. Cover both a closed C1b batch and a separately refreshed C1c-0, with receipt-specific deltas and a fresh accepted baseline. Do not treat an earlier refresh as covering later recipe edits.

## Nonblocking observation

**C1CPLAN-R2-NBO-1: Explain the allocation-free form of the sealing predicate** (`docs/implementation/m3/snapshot-plan-c/c1c/PLAN-r2.md:82`).

LD-C1C-7 now re-applies read_set_path while retaining the promise that step 2 allocates nothing and adds no charge. LD-C1C-5/8 describe charged temporaries and Cargo-root derivation for that API. This is implementable if sealing uses an allocation-free predicate over already retained evidence, but the split between preparation and checking is not stated.

Specify which evidence is retained from charged preparation and how sealing checks it without allocating or reading sources. If sealing actually needs new charged temporaries, revise the no-charge statement, full-ledger model and census anchors accordingly.

## Round-one dispositions

**R1-RF-1: substantially addressed, with the ancestry gap in R2-RF-1 above.** The new shared-rule-owned API correctly separates authorization from discovery's outermost classifier, admits ordinary and pnpm descendants, stops at further exact node_modules segments, excludes VCS throughout the full path and derives package-local Cargo roots without duplicating private tables. C1c-0 owns the API and the whole-file discovery closure re-pin, with unchanged discovery semantics/vector controls. Full Cargo/custody-state ancestry still needs specification.

**R1-RF-2: addressed for boundaries and ignorePaths.** LD-C1C-12 takes the walk's exact SnapshotExtent, states same-root provenance as a composition precondition and applies exclusions before descent, capture reach/origin changes and admission. Excluded required C2 captures remain leftovers. The controls include ignored packages with captured manifests, admitted boundaries and package subtrees. Workspace-link Walk rows remain intact. This disposition does not make boundary/ignore predicates stand in for the conventional-anchor checks in R2-RF-1.

**R1-RF-3: addressed for binding and status mechanics.** LD-C1C-9 accurately names each receipt's inputs, the C1c-0 shared-rule closure change that now stales discovery, and C1c-1's snapshot-only changes. Evidence compares against accepted baseline bindings: unchanged receipts have an empty delta and remain current; changed receipts show actual cumulative differences and their own stale status. In an unrefreshed C1c-0 interval, discovery remains stale for C1c-0 even if C1c-1 adds no new discovery delta; the plan's current-row example is correctly conditional on a refresh. Both generated-output checks must pass, and malformed receipts, bad pins, missing artifacts and output differences remain failures. The missing later interval is R2-RF-2, not a reason to fabricate staleness.

**R1-NBO-1: addressed.** Full-ledger inputs explicitly include normalized/deduplicated bookkeeping, per-row digest joins, classifier/Cargo temporaries, root reach, buffers and actual overlapping traversal. The 100,000 limit is per layout; no global layout-count cap is inferred. Excess setup/non-row/overlap work is explicitly in the typed-refusal regime. Acceptance of C1c-1 requires soundness vectors and the cumulative walk/session/sealing/VCS/read-set derivation at r9's unchanged caps with its 2x margin, or a law-record revision. The future evidence must include any extra preparation required by R2-RF-1/NBO-1.

**R1-NBO-2: addressed for C2b inside an open interval.** C2b must not rely on stale receipts; all intervening census-input changes are tracked before freeze; the pre-run review reconfirms the accepted baseline and final inputs. C1c-0 refreshes separately if C2b needs current evidence. R2-RF-2 covers the subsequent C1c-1 transition after that interval closes.

## Folded rulings and retained behavior

Q1 remains the accepted preparatory order C1c-0, C2b, C1c-1, with the item-3 reader integrating after layout production. Q2 correctly preserves S3 custody above the anchor, descriptor discipline below it and C2-owned read/parsing bounds without imposing the first-party marker's 4 MiB ceiling. Q3 is the exact case-sensitive raw-byte suffix set, including declaration-file endings. Q4 filters unread regular-file names before LogicalPath admission while validating candidate rows and descended directories and leaving first-party name rules unchanged. Q5 correctly permits a conservative full derivation with synthetic/native soundness and boundary controls until an admitted-layout census exists; the no-layout census is not read-set evidence, and receipt review/refresh duties remain.

The per-layout-row manifest digest join survives realPath deduplication, so conflicting digests refuse. First-party workspace-link manifests use the existing Walk capture without origin conversion. Capture observations, no-second-read, leftovers, no-layout identity preservation, side-record origin outside identity, suffix filtering, no-follow descriptor checks, no retry, special-file handling and joint item-5 bounds remain. The sealing guard retains Run-closure public refusal ownership; it is not proof of host read completeness. The C1b shared-file rebase and unique-current-anchor duties remain appropriate, subject to NBO-1. Typed refusals and separate Budget failure are retained.

The added controls/mutations target the earlier defects; add the ancestry and interval coverage above. No other regression was identified. This review accepts neither code nor a future companion receipt implementation; C1a4's reviewed refresh must establish that receipt contract before dependent batch entry.

## Review boundaries

Used only read-only reading, hashing, JSON parsing and Git queries. No Cargo, rustc, builds, tests, lanes, network, panes or delegation. No private fixture, installation directory, signing keys, held trees, T2 stores or cache were accessed. Neither repository, worktree nor control files were edited. Only REVIEW.md and review.json were written in the requested directory.
