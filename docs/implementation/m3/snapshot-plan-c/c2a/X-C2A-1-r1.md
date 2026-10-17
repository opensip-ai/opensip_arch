# X-C2A-1 r1: what component-tree delivery and custody must provide for C2a-3

**Lead cross-law memo, 2026-10-17. Input to a law draft; not law, not a plan, not a review subject.** It is raised by the C2a plan r2 (LD-C2A-5, C2a-3). The lead owns the law it asks for, DR-103's delivery owner.

## The gap

M3-C r8 item 7 admits a component closure only if it "retains its manifest body and its whole tree" (`PROPOSAL.md`:430). NE requires the compiler and stdlib closures retained whole, and re-admitted, before any digest comparison (NE:1493-1499). C2a-3 verifies that retention, and nothing provides the tree's bytes.

**What the trust side carries today** is metadata only:
- X4B's bootstrap carries the catalog and the component-manifest pairs, and verifies them against the final root at their roles' quorums (`m2/trust-bootstrap-x4b/PROPOSAL.md`:100-137);
- unit 463h retains the catalog and component-manifest pairs (:199);
- the ordinary reader joins a validated manifest to its catalog release, envelope and preimage (`opensip/crates/security/src/trust_ordinary_metadata.rs`:90-160).

The signed catalog names, per release, `artifacts[{platform, archiveProfileId, archiveDigest, sha256}]` (SL:35-38). The product admits that row's shape, with four platform tokens (`recovery_catalog.rs`:67-79). But **no law defines an archive profile** (`archiveProfileId` appears only at SL:38), and **no law or code installs, extracts or holds a component tree.**

A verified catalog is not tree custody (`codex-c2a-plan-r1`, Q3 ruling).

## What the law must provide

1. **What is installed.**
   - For each component release the host admits, and for the host's own platform only: the regular files of the selected platform's TreeCommitment (`platforms[].tree.entries`, `type=file`), with their bytes.
   - The `dir` and `symlink` rows are materialized only as the TreeCommitment states them, with symlink targets inside the tree (RJ-3; SL:41-48), and are never followed when the tree is read for identity.
   - Mode bits are applied from the TreeCommitment, and are not identity members.
2. **Where the bytes come from, and how they are verified.**
   - **The source** is the release's catalog artifact for the selected platform. The archive's raw SHA-256 must equal the signed `archiveDigest`, and the artifact's `sha256` must equal its signed value, with both signed under TR-INDEX.
   - **The archive profile** (`archiveProfileId`): the law must define at least one closed, bounded profile. That means a container format, entry types, path rules (no absolute paths, no `..`, NFC or exact bytes as the TreeCommitment states), size and count limits, and the refusal of every entry not in the TreeCommitment. The archive is parsed as hostile input, and nothing in it is executed during installation.
   - **Each extracted file** must equal its TreeCommitment row by path, length and SHA-256. A missing, extra or mismatched file refuses the installation, which leaves nothing installed.
3. **Custody.**
   - The installed tree lives in an installation-owned store whose custody is the installation's own: S3/S1 directory custody, a private ACL, and no writer other than the installer. It is reachable only through no-follow opens.
   - Files are retained by raw SHA-256 with `BLOB_LENGTH`, so C2a-3 verifies each identity Blob against bytes in custody, never against a path's current content.
   - The law must state who may write it (the installer transaction only), how a partially extracted tree is never visible (staged, then published), and what an observed later change means: it refuses, and is never repaired by a silent re-read.
4. **Identity.**
   - The installed tree's identity Blobs are exactly SL:41-48's projection of the TreeCommitment. The closure's identity stays item 7's `closure2` (C2a-1's candidate).
   - Installation adds no identity member. The installed store is an origin of retained bytes, not an identity input.
   - It is one of WS §2's admitted origins for a `closure2`: "an installed signed release with the same `closure2`" (`workflows-and-surfaces.md`:293).
5. **The read interface C2a-3 consumes.**
   - Given a `ClosureCandidate`, return each Blob's bytes from custody, or a typed `Missing`, `Length` or `Digest` failure. Each read is bounded and charged to the caller's scope, under the descriptor discipline.
   - The interface must also cover the synthetic fixture path, so that C2a-2's synthetic trees go through the same verifier (C2a plan r2, RF-2).
6. **Lifecycle, as the minimum for M3.**
   - Installation: when, by whom, and under which trust instant.
   - Removal, and its interaction with Run retention (a retained Run pins its closures' bytes).
   - The durable and ephemeral paths. The ephemeral path installs nothing, so with no delivered tree it admits nothing, consistent with item 7's no-trust-view rule (`PROPOSAL.md`:431-437).
7. **Refusals and routes.**
   - Each typed failure of installation and of retained reads, and its public route, are mapped onto the existing codes.
   - A not-installed required closure keeps the durable `COMPONENT.REQUIRED_CLOSURE_NOT_INSTALLED` disclosure (`PROPOSAL.md`:435). A corrupted promised tree keeps its own cause (C2a plan r2, LD-C2A-5).

## The smallest unit that closes it

**One law unit, "component release installation and tree custody"**, owned by the lead as DR-103's delivery owner, with:
- one archive profile;
- the installer transaction for the host's platform (staged, verified, published);
- the installation-owned tree store and its custody;
- the retained-tree read interface of point 5;
- the refusals.

**Excluded:** multi-platform installation, updates and migration (DR-110, DR-112), removal policy beyond Run-retention pinning, and any network acquisition. Those stay out unless M3's first-party release needs them.

Its first consumer is C2a-3. C2b-1's successful context admission follows it (C2a plan r2, Q1 ruling).

## Not claimed

No law text, no plan, no review. No change to item 7, C2PM-1, CR-1 or the trust owner.
