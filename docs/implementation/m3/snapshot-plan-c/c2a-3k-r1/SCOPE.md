# C2a-3k r1: the pure retained-tree verification kernel

**Standing:** UNREVIEWED CANDIDATE. Library only: no production caller, no public API, no custody, no admission, no qualification.

**Authority:**
- the C2a plan r4 (`c2a/PLAN-r4.md`; `codex-c2a-plan-r4`, ACCEPT), sub-unit C2a-3k (§2, the r3 Q6 ruling), with LD-C2A-5, LD-C2A-9, LD-C2A-10's C2a-3k prices and LD-C2A-12;
- law M3-C r8 item 7 (`PROPOSAL-r8.md`:405-450): a component closure is admitted only if it retains its manifest body and its whole tree;
- SL:41-48 (`security-and-lifecycle.md`): each identity Blob's retained length matches (`BLOB_LENGTH`).

**Candidate base:** product main `d704ed4`: contract successor 177 (S-OP-2c), over the v227 lock, D3a-3 (`2fbb779`) and the v226 lock. It holds C2a-1 r1 (`e770404`) and C2a-2 r2 (`1749259`). The worktree `opensip-c2a3k` was created at `5de9fd4`. The lane runner followed main inside the lock, because main's changes since then (D3a-3's components and operability paths, the v227 lock and successor 177) touch none of the candidate's paths.

## 1. The change

| Path | Change |
| --- | --- |
| `crates/security/src/component_closure.rs` (base-clean) | `Retention {Missing, Length, Digest}` and `ClosureRefusal::Retention(Retention)` (LD-C2A-9); `verify_retained_tree` and its `retention` helper (§2). The module header and the refusal enum's comment now name C2a-3k. Nothing else changes, and C2a-1's allocation pin still holds over the whole production source. |
| `crates/security/src/component_closure_tests.rs` (base-clean) | 8 controls (§4), appended. |
| `crates/security/src/trust/trust_bootstrap_tests.rs` (base-clean) | C2-T6's kernel leg: the shared ordinary-reader helper takes `through_the_kernel`, and the new test runs it over the default and the escapable synthetic trees. C2a-2's two tests pass `false` and are otherwise unchanged. |

No path is new, and `lib.rs` is untouched: the module is already declared `#[allow(dead_code)]` by C2a-1.

## 2. The kernel

`verify_retained_tree(candidate: &ClosureCandidate<'_>, retained: &BTreeMap<&str, &[u8]>, body: &[u8], work: &mut WorkScope<'_>) -> Result<(), ClosureFailure>`, the plan's signature. It runs in this order, and the first failure returns:

1. **For each Blob, in the descriptor's path order:**
   1. **presence:** one ordered walk of `retained` beside the Blobs, both in path-byte order (`str`'s `Ord`). A key below the Blob's path is passed over; an equal key is its slice; a greater key, or the end of `retained`, is `Retention(Missing)`;
   2. **length:** the slice's length must equal the Blob's `bytes` (`BLOB_LENGTH`), or `Retention(Length)`. This is checked before the digest, so a slice is never hashed past its declared length;
   3. **digest:** the slice's raw SHA-256, as lowercase hex written in place, must equal the Blob's `sha256`, or `Retention(Digest)`.
2. **The body:** its raw SHA-256 must equal the candidate's `manifestDigest`, or `Retention(Digest)`.

It returns `()`. A verified candidate is still a `ClosureCandidate`: the kernel constructs nothing admitted, and `AdmittedClosure::Component` is C2a-3's (LD-C2A-12). It reads no file, opens nothing, copies no slice, allocates nothing and holds no custody (the Q6 ruling).

**The charges** (LD-C2A-10), each immediately before what it prices, in the caller's borrowed scope:
- one `COMPARISON_COST` edge before each key comparison of the walk;
- one `COMPARISON_COST` edge before the length comparison;
- `digest_cost(len)` (⌈len / 64⌉ + 1 edges) before each slice's SHA-256, where len is then the Blob's `bytes`;
- one `COMPARISON_COST` edge before each digest comparison;
- `digest_cost(body.len())` and one comparison edge for the body.

No object or byte is charged, because nothing is allocated. For a `retained` map holding exactly the Blobs, the price is Σᵢ (3 + ⌈lenᵢ / 64⌉ + 1) + ⌈|body| / 64⌉ + 2 edges. Each retained slice that is no Blob's and sorts before a later Blob adds one comparison edge.

## 3. Lead-decision candidates

- **LD-C2A3K-1. Presence is a charged ordered walk, not a map lookup.**
  - `BTreeMap::get` makes O(log m) key comparisons that the kernel could not charge one by one. LD-C2A-10 requires "each comparison ... charged first".
  - The candidate's Blobs are already in path-byte order and unique (C2a-1's sort and duplicate pass), and a `BTreeMap<&str, _>` iterates in the same order. So one forward walk finds every slice with at most m + 1 comparisons in all, each charged with C2a-1's published `COMPARISON_COST`.
  - It reuses that price and invents none.
- **LD-C2A3K-2. Every comparison is charged, including the two the plan's price list leaves implicit.**
  - LD-C2A-10's C2a-3k bullet prices one SHA-256 and one length comparison per Blob, and one SHA-256 over the body. Its text also says "each comparison and digest is charged first".
  - The digest equality per Blob and for the body, and the presence walk's key comparisons, are comparisons too. Each is charged one `COMPARISON_COST` edge. That only adds to the bullet's price, and the plan's `digest_cost` is unchanged. Its +1 is the padding block, and the comparison is not folded into it (Q-C2A3K-2).
- **LD-C2A3K-3. A retained slice that is no Blob's is not a member.**
  - The kernel's question is whether the candidate's Blobs and body are retained exactly. A key in `retained` at no Blob's path, including a `dir` or `symlink` row's path, is passed over. It is never accepted in a file's place (the lookalike control).
  - Whether a delivered store may hold anything else is the delivery law's question, and C2a-3's to enforce (X-C2A-1 §2: "a missing, extra or mismatched file refuses the installation"). The kernel has no `Extra` refusal, because LD-C2A-9 names none (Q-C2A3K-1).
- **LD-C2A3K-4. The order of the checks, and the cause kept.**
  - The Blobs come in path order, then the body, as the plan's row lists them. Per Blob the order is presence, then length, then digest, so a slice of the wrong length is `Length` and is never hashed.
  - A corrupted promised tree or body is `Retention(Digest)` (or `Length`, or `Missing` when a slice is absent) and keeps that cause. The kernel has no not-installed outcome to relabel it as (LD-C2A-5).
- **LD-C2A3K-5. Test scopes.** Every ledger in the controls is `WorkLedger::new()`, the platform's default caps, or an exact `with_limits`, each a test scope. None is a production profile (Q5).

## 4. Controls (C2a plan r4, §4, as they fall to C2a-3k)

| Plan control | Test |
| --- | --- |
| C2-T6's kernel leg; retention (RF-2): "the fixture's synthetic tree goes through the same verifier" | `c2a3k_synthetic_trees_verify_through_the_kernel` (`trust_bootstrap_tests.rs`). The signed release of every role goes through the InitialCore, acceptance, the full ordinary reader and C2a-1's candidate, and then through the kernel over the supplied bytes and the authenticated body. This is done over the default and the escapable trees. Every role verifies, and one supplied byte changed refuses `Retention(Digest)`. |
| retention over every role; C2-T4 | `c2a3k_every_role_verifies_its_retained_tree`: entries reversed, a symlink row, an empty file. Each verifies at exactly the published price. |
| a missing tree file refuses `Retention(Missing)` | `c2a3k_missing_slice_refuses_missing`: each slice withheld in turn (both the walk's end and a passed path), an empty map, and lookalike keys (`bin/entr`, `bin/entry/`, a trailing space, a case change, a dir path and a symlink path). |
| a short file refuses `Retention(Length)` | `c2a3k_wrong_length_refuses_length_before_its_digest`: one byte short and one long for each slice, and the empty file given a byte. The ledger shows that no digest of the failing slice was charged. |
| C2-T1: retained bytes that disagree refuse `Retention(Digest)`, keeping the cause | `c2a3k_wrong_bytes_refuse_digest`: one byte changed in each slice at the right length; a changed body, the envelope as body, another component's body and an empty body over the verified tree. |
| LD-C2A3K-3 | `c2a3k_slices_that_are_no_blobs_are_passed_over`: extras before, between and after the Blobs, and at dir and symlink paths, each priced exactly. |
| LD-C2A-10: the charge equals the published price and is exactly funded | `c2a3k_charge_is_the_published_price_and_exactly_funded`: exact funding verifies; every smaller edge allowance stops `Budget(Edges)` within its allowance; no object or byte is charged. |
| LD-C2A-10: across components | `c2a3k_aggregate_exhaustion_in_the_second_component` |
| LD-C2A-10's source pin | `c2a3k_verifies_without_allocating_and_charges_first`. The kernel names no `Vec`, `String`, `Box`, `with_capacity`, `to_owned`, `to_vec`, `clone`, `collect`, `format!`, file or read API, and no candidate or admitted constructor. Each of its two SHA-256 calls is immediately after its `digest_cost` charge, and each of its four comparisons is immediately after a `COMPARISON_COST` charge. |

C2a-1's `c2a1_allocates_only_what_it_charges` still passes over the extended production source: still five allocation sites, and still one sort comparison.

**Not C2a-3k's:**
- obtaining bytes from delivered custody, and the `AdmittedClosure` type with its `Component` constructor (C2a-3, gated on X-C2A-1 and the installation law's CI-3 reader);
- the type-level pin that a `ClosureCandidate` handed to a context or selection API does not compile (it needs C2a-3's types; LD-C2A1-9);
- placement, after the draw, the core branch and composition (C2a-3, C2a-4).

## 5. Mutations

13, each run against the focused tests, which must fail (a compile failure never counts as caught):
- the presence check removed (a greater key accepted);
- the end of the walk accepted;
- later Blobs skipped;
- the length check removed;
- the Blob digest check removed;
- the body digest check removed;
- a digest failure relabelled `Missing`;
- a length failure relabelled `Digest`;
- the length comparison uncharged;
- the digest charged after it is computed;
- the digest under-priced;
- a slice copied;
- the walk not advanced on a match (an extra comparison per Blob).

## 6. The lane

`evidence/run_c2a3k_checks.py`, under the lane lock, nice 10, with a private 0700 TMPDIR:
- the security and host suites at base and candidate (security +9 new tests, host +0, with equal failure sets);
- rustfmt on the three edited files, all base-clean; the edited set exactly those three, with `lib.rs` untouched;
- warning-denied all-targets Clippy on security; a workspace all-targets check; security's `scenario-fixtures` and `crash-matrix` debug checks; a release build of security;
- the focused C2a-1, C2a-2 and C2a-3k tests;
- the environment exceptions; the operability source census with its mint audit; the census closure, unchanged; verify_design;
- the mutations.

Results: `evidence/c2a3k-checks-r1/checks.json` and `controls.json`.

The lane ran at `d704ed4`. Every row passed, and all 13 mutations were caught.
- **Suites:** security 1248 → 1257 (+9) and host 412 → 412, with 14 and 8 pre-existing failures, equal on both sides.
- **Static checks:** rustfmt (all three files base-clean and candidate-clean), the exact edited set, Clippy, the workspace check, the feature checks and the release build.
- **Tests:** the focused tests (C2a-1's 14, C2a-2's 8 and C2a-3k's 9).
- **Censuses and design:** the environment exceptions, operability (mint audit unchanged), the census closure and verify_design.

Before the lane, one ad-hoc focused run under the lock passed 31 of 31. It is not packaged.

**Rules held:** no environment read; no `let _ =`; no new mint-census call; no signing or private test key read; no new key, root, role, feature, constant or cap. The prices are C2a-1's published `COMPARISON_COST` and `digest_cost`.

## 7. Open questions

- **Q-C2A3K-1:** is passing over a retained slice that is no Blob's right for the kernel (LD-C2A3K-3), with any refusal of extra delivered files left to the delivery law and C2a-3? The alternative is a new refusal variant, which LD-C2A-9 does not name.
- **Q-C2A3K-2:** is charging the digest equalities and the walk's key comparisons one `COMPARISON_COST` edge each (LD-C2A3K-2) the right reading of LD-C2A-10, given that its C2a-3k bullet lists only the SHA-256s and the length comparison?

## 8. Inventory

No path is new. The three changed paths keep their rows, so **no inventory successor** follows.
