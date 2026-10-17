# C2a-1 r1: the unadmitted closure candidate

**Standing:** UNREVIEWED CANDIDATE. Library only: no production caller, no public API, no qualification.

**Authority:**
- the C2a plan r4 (`c2a/PLAN-r4.md`; `codex-c2a-plan-r4`, ACCEPT), sub-unit C2a-1, with LD-C2A-2 to LD-C2A-4 and LD-C2A-9 to LD-C2A-12, and both of its NBOs;
- law M3-C r8 items 7 and 8 (`PROPOSAL-r8.md`:405-466);
- C2PM-1 (`c2pm-1-r2/CONTRACT.md`, ACCEPT-DESIGN-UNIT), whose body half is already in the product (`component_manifest.rs`:19, :513, :659).

**Candidate base:** product main `813d559` (C1c-0, on D3a-2, C1b-0's successor 176 and the v222 lock). The worktree `opensip-c2a1` was created at `3742822` and moved onto main before the lane. Since then main has changed only one candidate path: C1c-0 appended its own module to `crates/security/src/lib.rs`, and C2a-1's append now follows it. Main's other changes touch no candidate path. The lane runner follows main inside the lock only when main's changes are disjoint from the candidate's.

## 1. The change

| Path | Change |
| --- | --- |
| `crates/security/src/trust_admitted_components.rs` (new) | `AuthenticatedComponent<'a>`: one verified component, borrowed. It exposes the catalog member path, the authenticated body bytes, the verified envelope bytes, the validated manifest, CR-1's kind (`Validated::closure_kind`) and the release row, all read-only. Only `crate::trust` constructs one. There is also a `cfg(test)` `TestComponent`, which runs the real body validation. |
| `crates/security/src/trust.rs` | The bridge module is declared, and its type re-exported `pub(crate)`; `TestComponent` is re-exported under `cfg(test)` only. |
| `crates/security/src/trust_ordinary_metadata.rs` | `Evidence::admitted_components()` (the plan's `trust::admitted_components`) is one iterator over the ordinary reader's verified components, in catalog order. Each component carries the body and envelope of its own retained pair. No copy, no re-verification and no charge is made (LD-C2A-10, "borrowed evidence is not charged again"). The reference fixture test gains the bridge's assertions. |
| `crates/security/src/component_closure.rs` (new) | `component_candidate` and `ClosureCandidate<'a>` (§2), the published prices, the hand encoder and the charged merge sort. |
| `crates/security/src/component_closure_tests.rs` (new) | 14 controls (§4). |
| `crates/security/src/lib.rs` (base-dirty, append only) | `#[allow(dead_code)] mod component_closure;`, appended, as other library units precede their callers (`grants`). |

## 2. The candidate's order

`component_candidate(component, platform, analyzer, registry, work)` runs in this order. The first refusal returns, and nothing is minted.

1. **The platform join (LD-C2A-3).** The selected `{os, arch}` row of `platforms[]`; its token `os-arch` among the catalog's four (`recovery_catalog.rs`:67-79, pinned equal by a test); an artifact of that token in the **same** release row. Otherwise `Platform`. The closure's `platform` is the catalog's `&'static` token.
2. **The kind (LD-C2A-2):** `closure_kind()`, CR-1's table only.
3. **The projection:** each `type=file` entry of the selected row becomes a `BlobRef` that borrows its path and digest. `dir` and `symlink` rows are not Blobs. Then come the charged merge sort over `u32` indices, and the adjacent-duplicate pass (`Tree`).
4. **C2PM-1 guards 1 and 2** over the authenticated declaration:
   - missing → `DeclarationMissing`;
   - an analyzer's declaration ≠ `compatibility.providerProtocol` → `AnalyzerMismatch`.

   Both carry origin `AuthenticatedReleaseDeclaration`. The integer is copied exactly and never inferred.
5. **The descriptor:**
   - `manifestDigest` is the raw SHA-256 of the authenticated body (LD-C2A-4);
   - D is predicted by LD-C2A-3's formula and refused `Encoding` above 4,194,304 bytes, before anything is charged or allocated;
   - the encoding is charged, then hand-encoded into `Vec::with_capacity(D)`, with a production check that its length and capacity are exactly D (`Internal` otherwise; NBO-1: no production canonical encoding);
   - it is admitted through `IdentityCandidate::from_json(registry, Closure, &D, 64 MiB)` (LD-C1A3-4's scoped exception). A schema refusal is `Field`.
6. **C2PM-1 guards 3 and 4** over the admitted descriptor:
   - its `protocolMajor` ≠ the declaration → `DescriptorMismatch`, origin `HostGeneratedInternalLayer`;
   - then the role table → `Unsupported`, origin `AuthenticatedReleaseDeclaration`. `toolchain`, `stdlib`, `rust-dev-llvm` and `grammar` support exactly 1. `analyzer` is supported only when an `AnalyzerSubprotocol` is given and its major equals the declaration.
7. **The id** is charged, then copied out of the candidate (`closure2:` + H("closure", D)).

`ClosureCandidate` has private fields, and is not Clone, Default or serializable. It exposes the id, D, the manifest digest and the Blobs in path order. Nothing accepts it (LD-C2A-12).

## 3. Lead-decision candidates

- **LD-C2A1-1. The bridge's placement.**
  - The production trust view keeps no components, so the bridge is a method of the ordinary reader's `Evidence`, inside the trust owner. The type it lends lives in `trust`.
  - Wiring it to R10a's evidence is C2a-4's.
  - The plan's `trust::admitted_components` is this method; `AuthenticatedComponent` is the type it lends.
  - **Which reader.** The bridge is on the full ordinary reader (`trust_ordinary_metadata.rs`, `prepare`). That reader validates each body with `component_manifest::validate` under its host context, giving `Validated`, which carries CR-1's kind.
    - It is not on that file's `inventory` reader. Current-trust admission uses that reader (`ordinary_targets.rs`:312), and it holds only `InventoryBody` (`validate_inventory`). `component_manifest.rs` says such a body "cannot be converted into Validated without executing the full host checks".
    - So C2a-4's R10a wiring must reach a full-validation reading of each selectable component, and must not project from the inventory reader's bodies (Q-C2A1-5).
- **LD-C2A1-2. Where the guards sit around the descriptor.**
  - Guards 1 and 2 need only the declaration, and the descriptor needs the major. So they run before D.
  - Guard 3 compares the *admitted* descriptor's `protocolMajor` (the host's own encoding) with the declaration, so it follows admission, and guard 4 follows it.
  - `Encoding` and `Field` therefore fall between guards 2 and 3. They are the descriptor's own construction, not one of CONTRACT.md:43's named prerequisites (parse, shape, trust, body-semantic, tree, platform, role, field-use), which all run first.
  - The four guards keep their order (Q-C2A1-1).
- **LD-C2A1-3. The analyzer seam.**
  - `AnalyzerSubprotocol` has only a `cfg(test)` constructor.
  - CONTRACT.md:30: "An analyzer lacking an applicable selected subprotocol cannot obtain new native admission from this field." No production code selects an analyzer subprotocol yet, so every analyzer projection is `Unsupported` in production until that owner lands (Q-C2A1-3).
- **LD-C2A1-4. The origins carried.**
  - C2a-1 sees two origins: the authenticated release declaration (guards 1, 2 and 4) and its own recomputed descriptor (guard 3, a host bug).
  - The host's `ClosureProtocolOrigin::ExternallySuppliedSpec` (`outcomes.rs`:758) has no C2a-1 source. It is not mirrored.
  - Mapping to the host's `NativeRefusal::ClosureProtocol` and the public carriers is C2a-4's, where the R10a routes are wired.
- **LD-C2A1-5. The projection visits its row twice.**
  - The `Vec<BlobRef>` is reserved for exactly the n regular files, so the row's entries are visited once to count them and once to project. Each visit is charged at one edge per entry: `visit_cost(entries)` twice.
  - This is LD-C2A-10's "one edge per entry visited", applied per visit (Q-C2A1-2).
- **LD-C2A1-6. The manifest digest's price.**
  - LD-C2A-4 makes `manifestDigest` the body's raw SHA-256, which C2a-1 computes.
  - It is charged at C2a-3k's published SHA-256 price, `digest_cost(len)`: ⌈len / 64⌉ + 1 edges. That price is published here, beside its first use.
- **LD-C2A1-7. What is unreachable, and labelled so.**
  - **The schema's `tree` `maxItems` of 100,000** cannot be reached through identity admission. 100,000 minimal Blobs exceed 4 MiB, and the parser refuses any input over 4 MiB (`canonical.rs`:62). The count control shows, on constructed input, that `Encoding` refuses first at 100,000 and at 100,001.
  - **The upstream 100,001-entry body** exceeds the security metadata profile's 4 MiB parse limit (`trust/metadata.rs`:9, :37), so the reader refuses it before projection.
  - **`Encoding` is defence in depth for real bodies.** An authenticated body is at most 4 MiB, and every file entry in it is longer than its Blob. So the boundary is tested at the encoder's real edge, over constructed Blobs: the largest real unique 20-byte-path tree that fits admits through `$defs/closure`, D at exactly 4,194,304 admits, and one byte over refuses before any charge.
  - The feasible positive boundary under a production profile is C2a-4's (Q5).
- **LD-C2A1-8. Refusal variants.** C2a-1 raises `Platform`, `Tree`, `Field`, `Encoding`, `Protocol { key, origin }` and `Internal`.
  - `Retention` arrives with C2a-3k, its producer.
  - `Kind` has no C2a-1 source: CR-1's table is total over the validated roles. Its field-use refusals are at their owners (LD-C2A-8).
- **LD-C2A1-9. The composition pin waits for its type.**
  - The plan's "a `ClosureCandidate` handed to a context or selection API does not compile" needs `AdmittedClosure` and those APIs' parameter types, which C2a-3 introduces.
  - C2a-1 pins what it can: the candidate has no public constructor, no Clone or Default, and private fields.
- **LD-C2A1-10. Test scopes.**
  - Every ledger in the controls is `WorkLedger::new()` (the platform's default caps) or an exact `with_limits`, each named as a test scope.
  - None is a production profile (Q5). No discovery or snapshot profile is used.

## 4. Controls (C2a plan r4, §4, as they fall to C2a-1)

| Plan control | Test |
| --- | --- |
| C2-T6's C2a-1 leg; LD-C2A-2 to -4; C2-T4 | `c2a1_every_role_projects_its_exact_candidate`: all five roles, with entries reversed and a symlink row added. D equals `canonical_bytes` of the expected value; the id is `closure2:` + H("closure", D); the digest is the body's and not the envelope's; the Blobs are only the file rows, in path order. |
| C2-T5 | `c2a1_changed_version_is_a_new_closure` |
| C2-T1's platform legs; NBO-1 | `c2a1_platform_join_is_closed`: a missing row, another release's tokens, no artifacts, and the core spelling `macos-aarch64` (`core_authentication.rs`:603) each refuse `Platform`; the closure's platform is the catalog token. `c2a1_platform_tokens_are_the_catalogs` pins the four tokens. |
| C2PM-1 (RF-1): presence, support, analyzer, no inference | `c2a1_c2pm_guards_through_the_projection`: an absent declaration on each validated role refuses `DeclarationMissing`; grammar majors 2 and 2^63 − 1 are `Unsupported`; an analyzer is `Unsupported` with no subprotocol or a different one, and admits with an equal one; a toolchain with `providerProtocol` 7 keeps `protocolMajor` 1. |
| C2PM-1: order, combinations, origins | `c2a1_c2pm_guard_order_and_origins`: guard 1 before 2; guard 2 whatever the support table says; guard 3 before 4 and the host's; guard 4's table with no numeric union and no cross-role equivalence. |
| r4 RF-1 (R3-RF-1); size vectors | `c2a1_hand_encoder_equals_the_canonical_encoder`: an empty tree, one Blob, non-ASCII, `"`, `\`, `\b`, `\f`, `\n`, `\r`, `\t`, U+0000, U+001F and U+0001, DEL, `bytes` 2^64 − 1 and `protocolMajor` 2^63 − 1. Each is equal to `canonical_bytes` at exactly D, and a `{"bytes":0,"path":"p"}` Blob is 98 bytes. |
| r4 RF-2 (R3-RF-2) and NBO-2 | `c2a1_merge_sort_is_charged_and_bounded`: reverse, sorted, interleaved and pseudo-random orders, n from 2 to 4,097. Each sorts within n·⌈log₂ n⌉ (reverse 20: 40 of 100). r3's old estimate n·⌈log₂(n + 1)⌉ suffices and succeeds. An allowance one comparison short refuses `Budget(Edges)` after exactly that many comparisons. |
| the duplicate pass; the empty tree | `c2a1_duplicate_paths_refuse_tree`, which also covers an empty projection's zero price and the reference bound of 0 for n < 2. |
| r4 RF-1's funding; RF-4's charge equality | `c2a1_charge_is_the_published_price_and_exactly_funded`: the ledger's use equals the published prices summed, with comparisons counted by the production sort. Exact funding succeeds. One byte or one object short at the descriptor refuses with nothing more charged, and one object short at the id refuses after the descriptor. |
| aggregate exhaustion | `c2a1_aggregate_exhaustion_in_the_second_component` |
| the 4 MiB boundary | `c2a1_descriptor_boundary_at_the_encoder_edge` (LD-C2A1-7) |
| the count legs, labelled | `c2a1_count_predicate_on_constructed_input` (LD-C2A1-7) |
| the allocation pin | `c2a1_allocates_only_what_it_charges`: in production there is no `format!`, `to_string`, `write!`, `String::`, `canonical_bytes`, `digest_hex`, uncharged sort, `vec!`, `.collect`, `to_vec`, `clone()`, `Box::`, `concat` or `join(`, and the encoder region names no `String`. There are exactly five allocations, each immediately after its charge. The index buffers are filled within their reservations, and the one comparison is immediately after its charge. |
| the bridge over real evidence | `full_ordinary_catalog_and_component_joins_match_exact_reference` (extended). For every verified component of `metadata285.ndjson`, the bridge equals the reader's component, and its body and envelope hash to the release row's `manifestDigest` and `envelopeDigest`. All eight M2 bodies refuse `DeclarationMissing` through the real candidate path. |

**Not C2a-1's:**
- C2-T1's retention leg, the retention controls and C2a-3k's verifier (C2a-3k, C2a-3);
- C2-T3 (the trust reader's own);
- C2-T7, C2-T8 and the generator (C2a-2);
- placement, after the draw, the core branch and composition (C2a-3, C2a-4);
- the public route and envelope tables (C2a-4). C2a-1 changes none.

## 5. Mutations

26, each run against the focused tests, which must fail:
- a `dir` or `symlink` row projected;
- the kind from the role string;
- the digest over the envelope;
- the host's platform spelling;
- the release-artifact join skipped;
- the Blob order unsorted;
- an integer through a `String`;
- the descriptor through `canonical_bytes`;
- a comparison before its charge;
- an uncharged `sort_unstable_by`;
- the missing declaration inferred from `providerProtocol`;
- guards 2, 3 and 4 each skipped;
- the support check moved before guard 3;
- a numeric support union;
- analyzer cross-role equivalence;
- `protocolMajor` from `providerProtocol`;
- the host-bug origin routed as external, and the reverse;
- the 4 MiB bound off by one;
- the prediction off by one;
- the duplicate pass removed;
- the projection reserved before its charge;
- the bridge lending the envelope as the body.

## 6. The lane

`evidence/run_c2a1_checks.py`, under the lane lock, nice 10, with a private 0700 TMPDIR:
- the security and host suites at base and candidate (security +14 new tests, host +0, with equal failure sets);
- rustfmt on the base-clean edited files, and `lib.rs` checked append-only;
- warning-denied all-targets Clippy on security;
- a workspace all-targets check;
- security's `scenario-fixtures` and `crash-matrix` debug checks;
- a release build of security;
- the focused tests;
- the environment exceptions;
- the operability source census with its mint audit (unchanged: the new code makes no mint-census call);
- the census closure, unchanged;
- verify_design;
- the mutations.

Results: `evidence/c2a1-checks-r1/checks.json` and `controls.json`.

**Attempt history.** Attempt 1 (`/tmp/opensip-implementation/c2a1-checks-r1-void-attempt1/`, not packaged) passed every row except one mutation. `support-before-descriptor-guard` survived because every guard-3 case selected an analyzer subprotocol. The guard-order control now runs each guard-3 case both with and without one, and adds `grammar` and analyzer cases. The lane was rerun on those bytes. Attempt 1's suites were security 1187 → 1201 and host 409 → 409, with 14 and 8 pre-existing failures on both sides. Two further starts never ran a check: main moved while each waited for the lock (C1b-0, D3a-2 and C1c-0). The packaged lane ran at `813d559`: security 1198 → 1212 (+14) and host 412 → 412, with 14 and 8 pre-existing failures, equal on both sides; every row passed, and all 26 mutations were caught.

**Rules held:** no environment read (one compile-time `env!("CARGO_MANIFEST_DIR")` in the tests' schema registry, as `journal_store.rs` has); no `let _ =`; no signing or private test key read; no new key, root, role or feature.

## 7. Open questions

- **Q-C2A1-1:** is LD-C2A1-2's placement of `Encoding` and `Field` between guards 2 and 3 right? The alternative is a pre-descriptor guard 3 over the field copy, which is trivially equal, and loses the check on the host's actual encoding.
- **Q-C2A1-2:** is the projection's second visit priced right (LD-C2A1-5)? The alternative is reserving for all entries, which over-reserves.
- **Q-C2A1-3:** is the analyzer seam with no production constructor the right reading of CONTRACT.md:30, with selection left to its owner?
- **Q-C2A1-4:** are LD-C2A1-7's labelled count and boundary legs sufficient for RF-4's "count predicate at 100,000 and 100,001"?
- **Q-C2A1-5:** is it right to place the bridge on the full ordinary reader, and to leave C2a-4 to reach that reader's validation for R10a, rather than bridge the current-trust inventory reader's `InventoryBody`, which is not host admission?

## 8. Inventory

There are three new paths, and the three changed paths keep their rows. The successor is numbered from the lock's last bound successor plus one, at integration. v222 is named by the combined D3a-1 and C1a4-blind successor, so C2a-1's is v223 or later. Its draft is `/tmp/opensip-implementation/prepare_c2a1_inventory.py`.
