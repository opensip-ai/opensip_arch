Grok review: unit X4B-c r1. It moves X4T-0's test-only accepted-store generator onto X4B's real producer. Claude Opus 5.5 leads, and you are the single reviewer.

## Rules
- No repository edits, commits, pushes or delegation.
- Write only under `/tmp/opensip-implementation/reviews/grok-trust-fixture-x4bc-r1`.
- If you build or test, use a `CARGO_TARGET_DIR` under that directory.
- Run git only read-only, and only against the worktree below.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent. It was absent throughout the lead's work. Never read or print the private 413 UUID fixture.
- Toolchain: `PATH=/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:/usr/bin:/bin`, and python3.14 at `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14`.
- **Scratch temp.** The lead's runs used `TMPDIR=/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T/opensip-x4bc-tmp` (mode 0700, under `getconf DARWIN_USER_TEMP_DIR`). Other worktrees run cargo concurrently on this host. If you replay, use a private 0700 directory of your own and say which one.

## The law
Arch paths are under `/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/`. `hashes.txt` pins every file named here.

- **X4B r5** (`trust-bootstrap-x4b/PROPOSAL.md`, 21587 bytes, sha256 `77b9ab1e…c62c`), accepted.
  - **Item 9:** "Once X4B's producer exists, X4T-0's test-only constructor is replaced by calls to it, wherever X4B can produce the requested role states: Trusted, Expired, StaleRevocation and Revoked, through item 4's sequences. X4T-0 keeps only the states acceptance can't reach, such as QuorumLost and Recovery, as test-only constructions. Its source pin stays."
  - **Item 11:** "X4B-c: moving X4T-0 onto X4B's producer (item 9)."
  - Items 2 to 4 define what the producer accepts and which events it records. Item 10's round trip requires X4T-a's loaders to accept what X4B writes.
- **X4T r11** (`trust-admission-x4t/PROPOSAL.md`, 53378 bytes), accepted.
  - Item 12 lists the reader's cases, all of which run on X4T-0's stores.
  - Item 13 defines X4T-0, its test-only record constructor and its source pin. It also covers the X4T-a3 rotation knob, with the rejected alternative "building X4T-a3's tests on X4B-a's producer or test release" (see call 9).
- **X8 r3** (`refusal-suite-x8/PROPOSAL.md`) item 4b, with **X9 r2** item 6 (`crash-matrix-x9/PROPOSAL.md`, whose item 6 is unchanged from r1 except a clock label).
  - X4T-0, meaning `accepted_store_fixture.rs` and its module declaration, is one of the shared fixture sites.
  - Each shared site is written `cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))`. X9-1 pins the exact site list, and a site outside it is a law revision.
  - X9-1 is in flight on another worktree. On main the module is still `#[cfg(test)]`.
- **Your X4B-a r2 and X4B-b r1 reviews** (`reviews/grok-trust-bootstrap-x4ba-r2/`, `reviews/grok-trust-bootstrap-x4bb-r1/`): ACCEPT-UNIT and ACCEPT.

## Subject
The worktree is `/Users/sb/code/opensip-ai/opensip-x4bc`, detached at product main `f097c5b` (X7a). Its lock selects inventory v125 (`1d157eea…2d10`, 506284 bytes). Nothing is committed and no file is added.

Save `git -C /Users/sb/code/opensip-ai/opensip-x4bc diff` as `subject.diff` in your output directory. It should be 45126 bytes, sha256 `9bfd8e13b6d5f353caefd12343ac7b9ccd927f6fec8021845a400e21f02337e2`. Nine existing files change, with 735 insertions and 59 deletions. All are in `crates/security/src/trust/`.

The work started on `81214cb`. Main then moved to `f097c5b`, whose X7a diff touches only host files and the lock. The worktree was moved onto `f097c5b` without conflict, and every check below ran on `f097c5b`.

## What it does

### The producer (`trust_bootstrap.rs`, production, behaviour unchanged)
- `build_acceptance(owner, …)` is now a thin call of the new `build_over_p0(p0, p0_raw, payload, observation, invocation, work)`. That function is the same body, reading the P0 capsule and its exact bytes from arguments instead of from the owner. It writes and grants nothing; only `accept_bootstrap` publishes, and it still goes through `build_acceptance`.
- `build_over_p0` and the field `BootstrapAcceptance::files` are `pub(in crate::trust::root_payload)`.

### Visibility only, no new cfg site
- `TrustWrite::path` (`floor_publication.rs`) is `pub(in crate::trust::root_payload)`. It is publish's own locator.
- The modules `current_trust_admission` (`ordinary_targets.rs`) and `trust_bootstrap` (`current_trust_admission.rs`) are `pub(in crate::trust::root_payload)`. The latter stays `cfg(target_os = "macos")`.
- No re-export and no `cfg(test)` item is added on the production side (call 4).

### The generator (`accepted_store_fixture.rs`, still `cfg(test)`)
`generate(spec)` keeps its asserts. On macOS it first tries `produce(spec)`, and falls back to `construct(spec)`:
- **`construct`** is the previous generator body, unchanged in substance. Three blocks are factored out with no change to values or order: `p0_publication` (467's P0), `signed_chain` (the root chain with X4T-a3's signer override), and the constants `anchor()` and `invocation()`. The lead checked byte identity against HEAD's generator; see Tests.
- **`Knobs::for_roles(roles)`** decides whether one acceptance reaches the requested six-role assignment (call 2).
  - TR-PROFILE and TR-REPAIR must be `Unbootstrapped`. TR-BUNDLE, TR-CORE and TR-INDEX must be carried. TR-COMPONENT may be `Unbootstrapped`, meaning no component manifest.
  - It then searches the eight (root expired, catalog expired, stale) combinations in binary order. For each carried role it computes the end state with `role_machine::bootstrap_sequence`, the function the producer itself dispatches through (item 4). `revoked` is set exactly where Revoked is requested.
  - The first combination that matches every carried role wins. If none does, the result is `None`.
- **`produce(spec)`** returns `None` if `chain_end` is not `Head`, if any signer is replaced, or if no knobs fit. Otherwise it signs a payload with the public quorum62 seeds:
  - the same root chain as before, with the final root's `expiresAt` set to 2026-10-01T12:00:00Z when the root must be expired;
  - the revocation list: the caller's entries plus, for each revoked role, the keyId of its document's third signer. It is issued 2026-07-01 when stale, otherwise 2026-10-01, with `revokedAt` equal to that time. It is signed under the final root, as before;
  - the catalog, under TR-INDEX by keys 11, 12 and 13. It expires at 2026-10-01T12:00:00Z when the catalog must be expired. It carries a release row for the component manifest;
  - the component manifest `component-0.json`, unless TR-COMPONENT is requested `Unbootstrapped`. Its body is 463h's `COMPONENT_MANIFEST`, signed under TR-COMPONENT by keys 14, 15 and 16;
  - the bootstrap manifest, under TR-BUNDLE by keys 17, 18 and 19, listing every member;
  - a core inventory under TR-CORE by keys 8, 9 and 10 (call 5);
  - the embedded binding of root 1.

  It then calls `BootstrapPayload::from_parts(…, CORE_CLOSURE, …)` and `build_over_p0` over the P0 it produced, using the fixture's sample (W 2026-10-02T00:00:00Z, mono 7, `boot-1`) and invocation.
  - If the producer refuses, or any stored role state differs from the request, `produce` returns `None`. That covers a caller's own list entry that revokes a document requested Trusted.
  - Otherwise the store is P0's files, then the producer's files at `TrustWrite::path`, de-duplicated by path, then the producer's `state.v1`.
- **`AcceptedStore::produced`** says which route built the store.

### Test signing helpers (`core_authentication.rs`, `cfg(test)` module `tests`)
- `component_body(i)` and `component_release(i, body, signer, root)` are factored out of `signed_release`'s loop. `signed_release` now calls them, with identical bytes; 463h's and X4B-a's suites pass unchanged.
- X9-1 already widens this module to the joint predicate in its worktree.

## Which consumer stores change route
The lead logged every `generate` call during one security lib run with temporary instrumentation (175 calls, since removed).

**Now produced**, previously constructed:
- `Spec::default()` and every variant of it, used by X4T-a, X4T-b, X4a, X2e (`operation_handoff`), X3d-1 (`commit_session`), live observation, and `write_accepted_trust` / `swap_trust`. Those variants are state schema 2, other stores, successor lists of version 2 naming an unrelated release, and the rotated chains with 2 or 3 roots;
- `each_continuation_refusal…`: core Revoked, index Revoked, component Unbootstrapped;
- `an_expired_or_stale_index…`: index Expired;
- `a_revoked_closure_component…`: a root-key keyId entry, which the producer accepts with every role Trusted;
- `entries_naming_no_closure_component…`;
- `the_revocation_list_is_verified_under_the_signing_root`: an unused keyId.

**Still constructed:**
- QuorumLost (core, index), and `all_targets()`, which includes TR-PROFILE and TR-REPAIR;
- `[Trusted; 6]`, the store for `MEASURED`;
- core Expired alone, component Stale alone, and index Stale alone;
- index Unbootstrapped;
- every `ChainEnd` other than `Head`;
- replaced root or list signers;
- caller lists naming `CORE_CLOSURE`'s release, the `opensip` namespace or catalog snapshot 1 while requesting Trusted, which the producer would end Revoked.

## Bytes and behaviour that change
Every consumer test's assertion passes unchanged except two measured pins.

- **Constructed stores** are byte-identical to before. The temporary check is described under Tests.
- **Produced stores** differ from the old constructed ones. For `Spec::default()`:
  - `lastAccepted` is A = 2026-10-01T00:00:00Z, per S4 step 2's L := A. The old construction wrote W. `evalHighWater` and the anchor are unchanged.
  - Two new objects: `component-0.json` (2177 bytes) and its envelope (1016 bytes).
  - The catalog carries the release row (893 bytes, previously 202).
  - The catalog and bootstrap-manifest envelopes carry three signatures.
  - The manifest lists the component manifest and its envelope, and the closure's `members` include the `manifests` slot.
  - The inventory pair is verified but not stored, as X4B-a does.
  - Role events, admissions, history and time evidence keep their shapes. Their bytes change with the documents they cite.
- **Measured pins.**
  - `current_trust_admission_tests::NATIVE_MEASURED` moves from (31, 265, 36_008) to (33, 291, 40_885).
  - `floor_publication_tests::NATIVE_AFTER_FLOOR` moves from (31, 265, 32_103) to (33, 291, 36_979).
  - The closure check opens the component pair: 2 more objects, 26 more edges, and 4,877 and 4,876 more bytes. The in-memory view of the same store measured (23, 50, 35_752) against (21, 44, 30_877) for the constructed one. Every distinct record read is one object with its exact bytes, so the r6 linear-charge pin holds.
  - `MEASURED` (23, 46, 35_371) is unchanged, because its six-role store is constructed. Both new figures are within `TRUST_VIEW_COST`.

## Judgment calls (lead decisions, narrowest reading)

1. **No inventory successor; ACCEPT on the diff sha256.** No file is added, and `verify_design` admits only a strictly additive successor (X4T-a3 call 1, X4B-b call 1). No v127 is built.
   - **Row this unit makes false,** for a later description batch: `accepted_store_fixture.rs` (v125). It says the module builds the retained publication itself, with "one conditioning event" per role, and that "It is the only constructor of these kinds and no production path reaches it; X4B owns the real producers". Reachable requests are now X4B's producer's records over the module's signed payload. The module remains `cfg(test)`, and no production path reaches it.
   - **Already false and already listed:** `trust_bootstrap.rs` ends "Not wired to the fenced first read (X4B-b)" (X4B-b call 1). That is not changed here.
   - **Understated but still true:** `accepted_store_fixture_tests.rs` (three new tests), `trust_bootstrap.rs` (`build_over_p0`), `current_trust_admission_tests.rs` and `floor_publication_tests.rs` (the pins move, and the text names no figures). The rows for `core_authentication.rs`, `current_trust_admission.rs`, `floor_publication.rs` and `ordinary_targets.rs` are untouched in substance.
2. **"Wherever X4B can produce the requested role states" is judged on the whole request.**
   - A request is the six-role assignment of one store. It is produced when one acceptance's item 4 sequences end every carried role in its requested state, with the profile and repair roles uncarried. Otherwise it is constructed. The fixture finds the time and revocation inputs by running `bootstrap_sequence` itself, so that function decides reachability, not a separate table.
   - **Consequences:**
     - Expired is produced through an expired catalog (TR-INDEX) or root (every carried role).
     - StaleRevocation is produced only store-wide.
     - Revoked is produced per role, through a signer the list names.
     - A lone expired core, or a lone stale role, cannot be reached by acceptance, because root expiry and staleness are store-wide under items 3 and 4. Those requests stay constructed, as do QuorumLost, an accepted TR-PROFILE or TR-REPAIR, and an uncarried TR-INDEX.
   - **Rejected:**
     - judging each role on its own, which would construct "produced" states for stores no acceptance writes;
     - deleting the construction for unreachable requests, which would drop X4T item 12 cases that item 9 keeps;
     - layering QuorumLost events onto a produced publication, which still constructs the descriptor and capsule and reorders events;
     - producing only all-Trusted requests, which would contradict item 9's list of Expired, StaleRevocation and Revoked.
3. **The producer is called below publication.**
   - `generate` is a pure in-memory generator. Readers use `lookup`, and `write` lays the files under any scratch root. So it calls the producer's builder over P0 bytes it produced, not `accept_bootstrap` on a fenced installation.
   - `build_over_p0` is the body of `build_acceptance`, which now only supplies the owner's capsule and bytes.
   - Files are placed by `TrustWrite::path`, so `write` lays them where `publish` would. As before, `write` is not `publish`: it has no barriers and no confirm.
   - A source pin limits `build_over_p0(` to `trust_bootstrap.rs` (definition and the one call) and `accepted_store_fixture.rs`.
   - **Rejected:**
     - running `accept_bootstrap` inside `generate`, which would need a fenced ACL-scratch installation in a generator called about 175 times, many in memory;
     - a second locator in the fixture.
4. **No new fixture-gate site; X8/X9's joint predicate stays intact.**
   - Every production change is a visibility widening to `pub(in crate::trust::root_payload)`, used in production. It adds no cfg and no `cfg(test)` re-export.
   - The fixture's new dependencies are production items, the macOS-only producer module, and `core_authentication::tests`, a site X9-1 already widens.
   - **Simulation.** On a scratch copy of the worktree, the lead applied X9-1's widening: the two security features, the joint predicate on `mod accepted_store_fixture`, and the same predicate on `core_authentication`'s `tests` module and `Collection` import.
     - `cargo check -p opensip-security --features crash-matrix` compiled with no error or warning;
     - `--features scenario-fixtures` alone also compiled cleanly.
     - The copy was then deleted.
   - **Rejected:** `#[cfg(all(test, target_os = "macos"))]` re-exports. They would be new fixture-gate sites outside X9-1's list, which X8 r3 item 4b makes a law revision.
5. **The payload adds only what item 2 requires, and stays synthetic.**
   - The old constructed payload had no core inventory and no component manifest. Item 2 needs the inventory, and TR-COMPONENT is carried only with a manifest.
   - **Inventory.** It is signed under TR-CORE. Its body binds only the embedded bootstrap pair: `embeddedBootstrap` with the manifest's and envelope's bytes, path and sha256, and `inventorySchema` 3. It is not a full v3 core inventory, and its projection would not be `CORE_CLOSURE`. The producer verifies its envelope and stores nothing of it.
   - **Running core.** It stays the synthetic `CORE_CLOSURE` that P0 names and every consumer passes as `core_closure`.
   - **Component manifest.** It is 463h's tested manifest with its catalog release row, which X4T-a's catalog join requires.
   - **Third signer.** Every role document carries all three role keys, so a revoked signer leaves threshold 2. X4B-a's revoked cases do the same.
   - **Rejected:** a full v3 inventory. Its closure would differ from `CORE_CLOSURE`, and making the closure vary per spec would change every consumer.
6. **Produced bytes differ, and two pins move.** These are the changes listed above. The `lastAccepted` difference corrects the old construction toward S4 step 2. No consumer depended on it.
7. **The producer route is macOS-only.** `trust_bootstrap` is compiled only for macOS. On any other target, `generate` constructs every store, as before. Linux is not claimed (X4T r11 "Not claimed"). The new producer-route test is `cfg(target_os = "macos")`.
8. **The source pin stays (item 9).** `no_production_source_reaches_the_constructor` is unchanged: the module is declared only under `cfg(test)` on main, and no other source names it. X9-1's rebase changes that pin's predicate, as its own diff already does.
9. **X4T r11 item 13's X4T-a3 rejection is not a contradiction.**
   - That rejected alternative governs how unit X4T-a3 was built. Its reader tests had to land before, and independently of, X4B-a's producer, as item 13 already rejected "moving X4B before X4T-a".
   - X4B r5 item 9 is the accepted, later step that moves X4T-0 onto the producer once it exists.
   - After X4B-c, X4T-a3's lawful rotated stores (`roots` 2 and 3, `Head`) are produced. Its refusal stores (other envelopes, short or empty chains, replaced signers) keep their construction byte-for-byte.
   - The reader's tests now also exercise the producer's output. That is item 10's round trip, and the reader's code does not depend on the producer.
   - The lead records this as a reading, not a law change. If you read item 13 as forbidding it, that is a finding against the law, not the code.
10. **Recovery stays not offered,** as before. `RoleTarget` has no Recovery variant, and item 9 names it only as a test-only state.

## Tests
**`accepted_store_fixture_tests.rs`: three new tests.** The existing eight pass unchanged, now on produced default stores.
- **`x4b_produces_every_request_its_sequences_reach`** (macOS). Ten requests:
  - default;
  - no component manifest;
  - expired catalog;
  - expired root;
  - stale list;
  - expired catalog plus stale list;
  - revoked core;
  - expired root with component and core revoked (three events each);
  - revoked bundle on a two-root chain;
  - a version-2 successor list on another store at schema 2 naming an unrelated release.

  For each, the test checks:
  - `produced` is true, and every role is in its requested state;
  - each role's events are exactly its item 4 sequence, in order;
  - `accepted.by` is the role's EV-PRESENT-PAYLOAD, and `revokedBy` is its EV-REVOKE or null;
  - uncarried roles are blank;
  - `current_record_bindings::bind`, `publication_events::bind_events` and `capsule_clock` plus `bind_retained_head` accept the store.

  It also pins the default store's `evalHighWater` = W and `lastAccepted` = A.
- **`a_request_no_acceptance_reaches_is_constructed`.** Ten requests stay constructed, each in its requested states: all targets, six trusted, quorum lost, a lone expired core, a lone stale component, no index, another envelope, replaced root signers, replaced list signers, and a list revoking the core.
- **`only_the_producer_and_the_generator_call_the_store_builder`.** The source pin of call 3.

**Byte identity of the constructed path.** This was a temporary check, removed afterwards; the diff sha256 was the same before and after.
- HEAD `f097c5b`'s `accepted_store_fixture.rs`, without its tests, was mounted as a sibling `cfg(test)` module, with `construct` temporarily `pub(crate)`.
- 23 constructed specs were compared: all targets at schemas 1 and 2, six trusted, quorum lost, lone expired core, lone stale component and index, no index, index quorum lost, every `ChainEnd` at 1 to 3 roots, both signer overrides, and the release, namespace and catalog-snapshot lists.
- Every file path and its bytes, the descriptor and the capsule were equal.

**The lead's runs** on these bytes, at `f097c5b`, with the TMPDIR above:
- `cargo test --locked --offline --workspace`, twice: 1658 passed, 0 failed, 3 ignored across 27 result lines, both times. That is 1640 outside the 18 doctests, which is X7a's recorded 1637 (`--all-targets`) plus this unit's 3.
- `cargo clippy --locked --offline --workspace --all-targets -- -D warnings`: clean.
- `cargo clippy --locked --offline -p opensip-security --all-targets --features opensip-platform/crash-matrix -- -D warnings`: clean.
- `cargo fmt --all -- --check`: clean.
  - `trust_bootstrap.rs` was standalone-rustfmt clean at base and is clean now.
  - `accepted_store_fixture.rs` has the same six standalone-rustfmt differences it had at base, all in untouched lines. The new code has none.
- `check_package_edges.py --lane host` against v125, with fresh `cargo metadata`: passed, 20 declared and 20 resolved.
- `python3.14 -I -B tools/verify_design.py --architecture ../opensip_arch --implementation .`: passed. It reports v125 selected, 85 inventory successors, 74 contract successors, 55 inheritance rows and 4 supersessions.
- Targeted: `cargo test -p opensip-security --lib -- accepted_store_fixture core_authentication trust_bootstrap native_read_admits the_next_admission_reaches` gives 42 passed.

## Decide
1. Does the diff implement X4B r5 item 9? Check:
   - every request item 4's sequences reach comes from the producer's records;
   - only unreachable requests keep the construction;
   - the source pin stays.
2. Is the producer unchanged in behaviour? Check:
   - `build_acceptance` reads exactly what it read before;
   - `accept_bootstrap` and `bootstrapping_first_read` are untouched;
   - no forbidden substitute of X4B or X4T becomes reachable, in particular X4T-0 from production, or a stored state not accepted by `decide`.
3. Are calls 1 to 10 the narrowest reading? Look especially at:
   - call 2, whole-request reachability;
   - call 4, the joint predicate;
   - call 5, the synthetic inventory;
   - call 9, the X4T-a3 rejection.
4. Are the changed pins and produced bytes explained exactly? Is any consumer's purpose lost? In particular, do X4T-a's closure-revocation cases still test the reader rather than the producer?
5. Is anything else wrong?

## review.json
There is no inventory candidate, so the verdict is `ACCEPT`, not `ACCEPT-UNIT`, and there is no `inventoryCandidateAssessment`. review.json must contain, at top level:
- "verdict": `ACCEPT` or `REQUIRED-FINDINGS`;
- "requiredFindings";
- "subjectSha256": the sha256 of `subject.diff`, `9bfd8e13b6d5f353caefd12343ac7b9ccd927f6fec8021845a400e21f02337e2`.

Write REVIEW.md and review.json. Do not commit.
