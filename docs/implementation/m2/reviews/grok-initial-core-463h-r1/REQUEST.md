Grok review: 463h, the `InitialCore` code successor of law 463 r9. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-initial-core-463h-r1. If you build or test, use a CARGO_TARGET_DIR under that directory. Run git only read-only, and only against the worktree below.

## Law

- `docs/implementation/m2/initial-core-launch-463/PROPOSAL-r9.md` (23367 bytes, sha256 `f47c22c0…8b6f`), which you accepted with X4B r5 in `reviews/grok-initial-core-463-r9-trust-bootstrap-x4b-r5/` (review.json `141ade6c…514f`). The relevant parts are item 2's r9 store bullet, item 9 and the "r9 code successor" section. The live PROPOSAL.md differs only by the acceptance note.
- `trust-bootstrap-x4b/PROPOSAL-r5.md` (`97c2eef3…29a3`), items 2 and 4: how X4B will consume the pairs.

## Subject

The worktree `/Users/sb/code/opensip-ai/opensip-463h`, detached at product main 97f630a (lock selects inventory v108). The diff is saved as `subject.diff` in your output directory (36018 bytes, sha256 `fde5e5f3…bd6f`). It changes three existing files and adds none. Pins are in hashes.txt.

## What it does

**`crates/security/src/trust/initial_core.rs`.**
- **F8.** The locator now also takes `members.catalog` and `members.manifests`. The bound is chain + revocation + manifests + envelopes ≤ `MAX_MEMBERS` (130).
- **F9.** `MemberOpener` replaces the inline loop. It does the same no-follow opens, the exact-name check, the core-tree custody judgment, the subdirectory memo and the shared `MAX_MEMBER_BYTES` budget, and pushes each opened file as a `HeldFile` (`CoreMember::Member`).
  - First it opens the root chain, the revocation and every listed envelope, as in r8. Item 9 says the index loads every envelope before any selection.
  - After pairing, it opens the component-manifest bodies, then the catalog body only if pairing admitted it. An unadmitted catalog is never opened.
- **Item 9 (r9 body set).**
  1. Each listed envelope is parsed to its carrier stored digest.
  2. The catalog is admitted if any stored digest equals `members.catalog`'s digest.
  3. The body set is the chain, the revocation, every manifest, and the catalog if admitted. It must have no duplicate digests, and `|envelopes|` must equal its size.
  4. Each stored digest must remove one body.

  Anything else is `BootstrapEnvelopeSet`. Which keys or role signed is not judged.
- **F10.** The store gains the admitted catalog pair and every component-manifest pair. Their bytes are `Arc`s shared with the retained documents and charged once at insertion. A separate allowance covers the pair vector and its path copies.
- **The accessor.** `InitialCore::bootstrap_documents() -> &BootstrapDocuments` is crate-private. It gives `catalog() -> Option<&BootstrapPair>` and `manifests() -> &[BootstrapPair]`, in `members.manifests` order. Each `BootstrapPair` has `body()` and `envelope()`, each a `DocumentBytes` with `path()` (manifest path under the bootstrap directory), `raw()`, `bytes()` and `sha256()`. It grants nothing and verifies nothing.
- **Recheck.** `recheck` reaches the new members, because they are `HeldFile`s.

**`core_authentication.rs` test builder (`signed_release`).**
- `catalog-placeholder` is replaced by a real catalog body:
  - `catalogSchema` 1;
  - empty `releases`;
  - `rootVersionRequired` is the final root version;
  - `revocationVersionRequired` 1;
  - expires 2027-04-01.
- The catalog is signed under TR-INDEX by seeds 11 and 12.
- One component manifest is added. Its body is manifest268-semantic's `POS/empty-capabilities` body, canonicalized, with its version varied per component. It is signed under TR-COMPONENT by seeds 14 and 15.
- Both use the public quorum62 seeds.
- `Spec` gains `catalog_signers` and `component_signers`. Each is a list of `(header role, seed indices)`, and a `None` component signer means a manifest listed with no envelope. The defaults are one of each.
- The new public items are `Signer`, `INDEX_SIGNER` and `COMPONENT_SIGNER`.
- Only one existing pin moved: the opened-file count in the positive test (2+2+6 → 2+2+10). No ledger total elsewhere moved; every 462/465/466/467/458c/X-unit test passes unchanged.

**`initial_core_tests.rs`.**
- **Positive cases.** Both (two manifests); neither (the r8 shape, 6 members, nothing retained); a catalog and no manifests; manifests and no catalog. Also: deleting an unadmitted catalog file changes nothing. Every case checks the accessor's paths, bytes, lengths and digests against the tree, and each produced core passes `recheck`.
- **Keys not judged.** A catalog signed by TR-COMPONENT seeds under a TR-INDEX header, and a manifest signed the other way round, are retained.
- **Refusals (`BootstrapEnvelopeSet`).** A second root envelope (existing); a second catalog envelope; a manifest with no envelope, alone or beside a paired one; and a retained body or envelope whose bytes are not its listed digest (judgment call 2).
- **The bound.** 62 manifests with no catalog makes 130 members and passes; 63 refuses `BootstrapLocator`.
- **Custody.** `recheck` refuses a group-writable component envelope and catalog (`Custody(Member, GroupWrite)`), and an omitted ACL on a component body refuses at production.

## Judgment calls (lead decisions, narrowest reading)

1. **No inventory successor; v115 unused.** No file is added and every changed file's description stays true. Precedent: 461a and 464 code.
   - The `initial_core.rs` row says "(law 463 r3–r8)". That is still true but no longer complete, so it is noted for the D1 description batch, as the v108 README handled stale descriptions.
   - The `core_authentication.rs` and `initial_core_tests.rs` rows remain exact.
2. **Retained pairs carry their listed bytes.** For each retained catalog or manifest body, and its paired envelope, the raw sha256 must equal the manifest row's digest, or the release refuses `BootstrapEnvelopeSet`.
   - Why: chain and revocation members get this check implicitly, because `authenticate` looks them up by row digest and a mismatch is `Missing`. Nothing looks the r9 pairs up, so without this check `InitialCore` could retain a "pair" that is not the pairing item 9 made.
   - Not applied to chain or revocation members, so r8 refusal behaviour is unchanged.
   - This is a byte identity, not a trust decision.
3. **Open order.** Chain, revocation and envelopes are opened first, as in r8. Then pairing runs, then manifests, then the admitted catalog. A missing or ill-custodied r9 body therefore refuses after the envelope-set check. The unadmitted catalog is never opened: item 2 stores it only when admitted, and r9's "nothing else is stored" names exactly those opens.
4. **The member bound counts the catalog body only when admitted.** F8 leaves it out, so the r8 boundary does not move. After pairing, an explicit check adds it. Under the bijection, F8's bound already implies that check: the total is 2·|envelopes|, and F8's count is that total minus one. It is kept as the stated bound.
5. **Not a contradiction: the header route check.** The existing manifest index (`retained_metadata_index::Data::build`, inside `authenticate`) refuses any listed envelope whose header role is not its kind's route. For example, a catalog envelope declaring TR-COMPONENT refuses `Release(Authentication(Core(Budget(Route))))`.
   - It did this in r8 for every listed envelope.
   - It is the carrier's shape, not "which role signed": keys, quorum and role standing remain unjudged, and the keys test pins that.
   - X4B's "signed outside its role" case uses correct headers with the wrong keys.
6. **A catalog whose digest equals another listed body.** Read literally, item 9 puts it in the body set, the set has a duplicate, and the release refuses. This only happens on pathological data.
7. **The test catalog lists no release rows.** X4B r5 needs role reverification only. An X4B-a test that needs `releases` rows extends the builder.

## Contract check (law's claim, verified)

- `EmbeddedBootstrapV1` in `tools/security/inputs/trust-record-schema.json` has required properties `{directory, manifest, envelope}`, and `additionalProperties` is false. It does not list the envelope set.
- `index_payload_shape` (verified_recovery_bundle.rs) requires `catalog` and `revocation`, and allows `manifests` and `envelopes` arrays. `admitted_payload_paths::admit` already classifies `Catalog`, `Manifest` and untyped envelope rows.
- `core_anchor.rs:285` still requires every manifest member to be a tree row (`bootstrap-member-tree`), and the builder lists the new files as tree rows.
- `bootstrap-envelope-set` appears only in `installation_routing.rs:190`. No contract or docs registry names it.
- The golden `crates/security/tests/fixtures/core-auth323.ndjson` (`3c8fb9a2…e211`) is unchanged. Its only reader is `placeholder_fixture_releases_refuse_without_a_signed_revocation`, which reads the fixture's own stores and still passes (13 refused).

No contract successor is needed.

## Checks on 97f630a + subject

- **Full workspace, twice, on the final bytes:** 1463 passed, 0 failed, 3 ignored each time. That is the baseline 1459 plus 4 (5 tests added, 1 replaced). The security lib has 809 passed and 2 ignored, including the 15 initial_core tests.
  - An earlier run, before a one-line formatting split, saw one failure in `custody::namespace_lease::tests::the_target_holds_no_project_lock_for_the_floor_step` while the x2e worktree's `cargo test` ran concurrently.
  - That test passed 3 times in isolation and in every other run.
  - The failure was in a namespace-lease gate, which this diff does not touch.
- **Lint:** clippy `--workspace --all-targets -D warnings` and `cargo fmt --check` are clean.
- **Package edges:** `check_package_edges --lane host` against v108 passes (19 declared and 19 resolved internal edges).
- **verify_design:** the live run passes with v108 selected.
- **Home:** `~/Library/Application Support/OpenSIP` is absent.

## Decide

- Does the diff implement 463 r9 item 2's store bullet, item 9 and the r9 code successor exactly? Is `InitialCore` free of any trust decision on the pairs?
- Are judgment calls 1–7 sound and the narrowest reading? In particular:
  - 2: the byte-identity refusal;
  - 5: the route check is not a contradiction.
- Is the accessor enough for X4B r5 items 2 and 4, without granting anything?
- Is the test builder right for X4B-a, with real TR-INDEX and TR-COMPONENT signatures, and does the r8-shaped release still pass?
- Is the contract check right? Is skipping inventory v115 right?
- Is anything else wrong?

review.json must contain top-level "verdict" (`ACCEPT` or `REQUIRED-FINDINGS`), "requiredFindings" and "subjectSha256" (the sha256 of subject.diff, `fde5e5f371481c003e687e5b047742e92f34c313cb16824503dc95fbcf1fd8bf`). Write REVIEW.md and review.json. Do not commit.
