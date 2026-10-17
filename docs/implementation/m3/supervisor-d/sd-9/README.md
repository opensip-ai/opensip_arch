# SD-9: R10a's and ER10a's work ledger (M3-D successor; law record)

2026-10-17. Drafted by the implementation lead (Claude Opus 5.5), as the owner LD-D4-SD9 names, with the J1 and D4 admission owners. Those are also the lead: J1's author and M3-D's author. **Draft r1, PROPOSED, not accepted.**
- It is a design unit, and it edits only arch. It adds no product file, code, cap, constructor, public code, route or detail.
- It needs Codex `ACCEPT-DESIGN-UNIT` and the lead's root assent.
- J1's and M3-D's next revisions then record it (§9).

**What it is.** SD-9 is the successor D4 plan r2 records as owed (LD-D4-SD9, `d4/PLAN-r2.md`:175), after the round-1 review's Q6 ruling (`reviews/codex-d4-plan-r1/REVIEW.md`:47). It owns R10a's and ER10a's **production work profile**:
- the ledger's lifetime;
- its aggregate cost model across the trust read's hand-off, D4, C2a-1, CI-3's open, C2a-3's retained-byte transfers and C2a-3k;
- its caps;
- its `Budget` projection.

It is the "production work-profile selection (the profile, its caps, its aggregate cost model and its `Budget` projection)" that C2a plan r4's Q5 ruling makes a named gate of C2a-4 (`c2a/PLAN-r4.md`:19, :85, :168). CI r5 defers R10a's profile to the same owners (CI:221, :302).

**What it gates.** Production R10a and ER10a composition, C2a-4, and J3d's and J2c's R10a and ER10a wiring (LD-D4-SD9; `codex-d4-plan-r2` "Ordering"). It gates no pure library unit: D4-1 to D4-4, C2a-1, C2a-3k and CI-3 charge a borrowed scope and are tested on explicitly identified test scopes.

## Short names and pins

Every pin is checked by `evidence/check_sd9.py` (its output is `evidence/check_sd9.output.json`).

| Name | Document | Bytes | sha256 |
|---|---|---:|---|
| **D4P2** | `supervisor-d/d4/PLAN-r2.md`, D4 plan r2, Codex ACCEPT (`reviews/codex-d4-plan-r2`) | 34,204 | `fddf67e5…` |
| **D4P1** | `supervisor-d/d4/PLAN-r1.md` (X-D4P-1's facts, :126-135) | 35,993 | `2ae0bece…` |
| **D4R1** | `reviews/codex-d4-plan-r1/REVIEW.md` (Q6, :47) | 11,661 | `bdf62f8f…` |
| **D4R2** | `reviews/codex-d4-plan-r2/REVIEW.md` | 11,568 | `04529f78…` |
| **C2A** | `snapshot-plan-c/c2a/PLAN-r4.md`, C2a plan r4, Codex ACCEPT | 41,183 | `dad5a9de…` |
| **CI** | `component-install/PROPOSAL-r5.md`, the component installation law r5, Codex ACCEPT | 63,707 | `efdbf7e7…` |
| **CIP** | `component-install/PLAN-r3.md`, its plan r3 with CI-A1, Codex ACCEPT (LD-CIP-9, X-CI-1) | 35,877 | `b1db1e4d…` |
| **CIR2** | `reviews/codex-component-install-r2/REVIEW.md` (Q9, :71: the X-CI-1 interim) | 14,441 | `65fe893b…` |
| **J1** | `host-pipeline-j/PROPOSAL-r7.md`, M3-J1 r7, accepted | 178,993 | `d65481ba…` |
| **MD** | `supervisor-d/PROPOSAL-r5.md`, M3-D r5 (item 29, :1171) | 209,266 | `224b9228…` |
| **R9** | `snapshot-plan-c/c1a-r9/RECORD-r9.md`, M3-C r9's caps record, accepted | 29,463 | `f360d1aa…` |
| **RTC** | `docs/coop/design-corrections/foundation/run-termination-contract.v1.md` | 32,543 | `cfe793fc…` |
| **WL** | product `crates/platform/src/work_ledger.rs` at `274dccc` | 38,067 | `24d6d665…` |
| **CC** | product `crates/security/src/component_closure.rs` at `274dccc` (C2a-3k) | 26,357 | `e4d90cc2…` |
| **NRS** | product `crates/security/src/trust/native_read_session.rs` at `274dccc` | 36,976 | `694a7ee3…` |

The product base is main `274dccc` (C2a-3k), read only through `git show`. **CI-A2**, CI-2 r1's proposed amendment of `B_open` and `B_transfer`, is in preparation and is not pinned. The model includes its rows because they only add work (§3).

## 1. The ledger (LD-S9-1)

- **One ledger per admission.** R10a creates **one** `WorkLedger` at its entry, after R10's trust read has returned and while R10's fence is still held (J1:392). It never creates a second one, and never replaces or resets it. `WorkLedger` has no `Default` and no `Clone`, and a failed ledger refuses everything (WL:1-9, :201-202), so a failure cannot be retried on a fresh one.
- **Every R10a sub-step charges its scope:** D4-1's `admit`, D4-2's lend, and for each component C2a-1's candidate, CI-3's `open_retained_tree`, C2a-3's transfers of its retained bytes, and C2a-3k's kernel. They are funded in one aggregate, never one scope per component (C2A:19, :168).
- **ER10a** creates its own ledger in the same way, at its entry under the read session's fence (J1:493, :498). With no trust view (E-3, E-4), ER10a admits nothing and charges nothing.
- **Lifetime.** The ledger ends when R10a returns.
  - The pins that CI-3's capabilities hold outlive it (CI item 7), but their later work belongs to other ledgers.
  - A Run's retention copies through `transfer` on its retention owner's ledger (CI item 6).
  - D4-4's launch recheck runs on the factory's caller's ledger (D4P2 LD-D4-11).
- **Not the trust read's ledger.** R10's trust read runs on the read session's one ledger (law 458c item 6; NRS:84-85), at the global caps (`retained_metadata_index.rs`:127). R10a does not charge it, and SD-9 does not change it.
  - The trust evidence is handed over by reference. It is borrowed and is not charged again (C2A LD-C2A-10; CI item 4, "What is uncharged").
  - Only D4-2's charged lend (the reserved-name slice view, D4P2 LD-D4-13) and the per-sub-step allocations are charged.
- **Rejected:** charging R10a to the read session's ledger. Its global caps cannot hold whole-tree verification: 131,072 edges is about 8 MB of hashed tree (§4), and X-D4P-1's 100 MB example already needs about 1.6 M edges (D4P1:128; D4R1, "Coverage"). `with_limits` cannot raise them (WL:256-266).
- **Rejected:** one ledger per component. C2a forbids a per-component reset (C2A:19), and a per-component allowance would multiply the cap by the component count.

## 2. The aggregate model (LD-S9-2)

For one R10a (or ER10a) over the set Σ of components that the trust view admits and the analysis step can select (J1:392), the charged work is, coordinate by coordinate:

**A(Σ) = D4₁(Σ) + D4₂(Σ) + Σ_{c ∈ Σ} [ C2a₁(c) + B_open(c) + T(c) + K(c) + M(c) ]**

| Term | What | Owner and price | Status |
|---|---|---|---|
| D4₁(Σ) | `admit` over Σ's manifests: the policy order checks, two `u32` buffers, the charged merge sort, the duplicate pass, the count and fill passes' probes, and the result | D4P2 LD-D4-8, LD-D4-10 | accepted plan |
| D4₂(Σ) | the lend: `ManifestClaims` slice views and the reserved-name view (objects 1, bytes r·`size_of::<&str>()`, r edges) | D4P2 LD-D4-2, LD-D4-13 | accepted plan |
| C2a₁(c) | the candidate: two entry visits, the projection, two sort buffers, at most F·⌈log₂ F⌉ comparisons, the duplicate pass, the body's digest, the descriptor buffer D and the id | C2A LD-C2A-10 | integrated (C2a-1) |
| B_open(c) | CI-3's open: custody, the generation, `pin.lock` and its `flock`, `generation.json`, the buffer, the traversal, and **each file's open and read attempts, Σ env(len(f))**, which stream and hash every file | CI item 4 (CI:181-197), with CI-A2-b and -d as proposed | accepted law; CI-3 in preparation |
| T(c) | C2a-3's transfers of each Blob's verified bytes into the retained-byte map it hands to C2a-3k: Σ_f B_transfer(f) | CI item 4 (CI:199-207), with CI-A2-c as proposed | accepted law; C2a-3 not yet planned in detail |
| K(c) | C2a-3k over the map and the body: per Blob, its presence comparisons (one, plus one per passed-over key), one length comparison, digest_cost(len) = ⌈len / 64⌉ + 1 and one digest comparison; then digest_cost(body) and one comparison. No object or byte | CC (`verify_retained_tree`); C2A:179 | integrated (C2a-3k, `274dccc`) |
| M(c) | C2a-3's own allocations for the retained-byte map: at least F objects and Σ len(f) bytes for the slices, plus the map | **owed by C2a-3** | not priced: SD-9 names the term and invents no price |

- **Excluded, with their owners:** the identity admission's internals (the scoped exception of LD-C1A3-4, C2A:178); D4-4's recheck (`B_launch`, CI-A3); Run retention's transfers; the trust read itself.
- **Checked arithmetic.** Every sum and product in an owner's bound is checked. Exhaustion partway through any term is `Budget`, never a truncated or partial admitted set (D4P2 LD-D4-8; C2A:180).

## 3. The whole-tree hashing term (LD-S9-3)

The term **H(c) = B_open(c) + T(c) + K(c) + M(c)** is every operation that reads, copies or hashes c's retained tree at R10a:
- **CI-3's reads** stream every regular file once in B_open, verifying its length and SHA-256 (CI item 6, "Structural verification"). They stream it again in T(c), through `transfer` (CI item 6, "The bounded verified-byte transfer"). Each costs `env(len) = 2·⌈len / 64 KiB⌉ + 2` read attempts.
- **C2a-3k's kernel** hashes the same bytes a third time, in memory, at `⌈len / 64⌉ + 1` edges per Blob (CC; C2A:179). This is SHA-256's block bound, charged as one edge per 64-byte block.
- **So K dominates the edge coordinate.** Per byte, K costs 1/64 of an edge, and B_open plus T together cost about 4/65,536. In the model's shapes, K is 76 % to 99.6 % of all R10a edges at the interim boundary (§4).
- **Bytes.** M(c) holds Σ len(f) bytes while C2a-3k runs, so the byte coordinate carries the tree's size once, plus each owner's per-entry records.
- **Why all three are counted.** C2a plan r4 makes C2a-3 obtain the bytes "from delivered custody through the delivery law's interface", run C2a-3k over them, and only then construct `AdmittedClosure::Component` (C2A:82). CI's interface obtains them by `open_retained_tree` and `transfer`. Until C2a-3's plan chooses otherwise, SD-9 prices that shape, which is the largest. A C2a-3 that streamed into the kernel without the in-memory copy would only remove work (Q-SD9-5).

## 4. The caps: an explicit interim (LD-S9-4)

**No sourced R10a cap exists.** No census of M3's first-party release closures under these prices has been run: the releases are not built, and X-CI-1's census is owed too (CIP LD-CIP-9). SD-9 therefore selects, **as an explicit interim policy on X-CI-1's precedent**, an existing sourced profile's caps.

- **The interim:** R10a's and ER10a's ledger is **`WorkLedger::snapshot_profile()`**: 2^21 objects, 2^24 edges and 2^33 bytes (WL:28-30, :242; R9).
- **This is an interim policy:**
  - it is not evidence of R10a census coverage or of release qualification (as CIR2:71 says of X-CI-1);
  - it is not inferred from a caller's name (C2A:19);
  - it reuses the existing constructor, so **`work_ledger.rs` is not edited**, and neither the discovery `CLOSURE` nor the companion snapshot receipt changes (CIP LD-CIP-9's census impact does not arise).
- **Its feasible boundary** (`evidence/check_sd9.output.json`). The model applies §2's edge and object terms to illustrative shapes, with every price read from the product sources at `274dccc`. It finds the largest total file size of one component whose R10a edges fit each existing profile's edge cap:

  | Shape | global (2^17 edges) | discovery (2^21) | **snapshot (2^24)** | objects at the snapshot boundary |
  |---|---:|---:|---:|---:|
  | one file | 8,328,320 | 133,667,968 | **1,069,536,384** | 19 |
  | 1,000 files, depth 3 | 3,456,641 | 129,024,721 | **1,064,704,785** | 6,319 |
  | 10,000 files, depth 4 | does not fit | 73,608,171 | **1,010,568,235** | 93,119 |
  | 40,000 files, depth 6 | does not fit | does not fit | **796,181,735** | 612,019 |

  - Under the interim, one R10a can verify about **0.75 to 1.0 GB of retained tree in aggregate**, across all of Σ's components.
  - The object coordinate stays within 2^21 (612,019 at the deepest shape). The byte coordinate holds the tree once, in M, within 2^33.
  - Beyond the boundary, the admission refuses `Budget` on row 11 (§6). This is the typed-refusal regime of R9's caps, never truncation.
  - D4₁, D4₂, and M's map overhead are excluded from the model's edges, as small per-manifest terms or owed prices. The model's figures are illustrations of §2, not a census and not caps.
- **Rejected:** the global caps, which hold at most about 8 MB, and the discovery profile, which holds at most about 130 MB and cannot hold a 40,000-file tree at all. Neither holds a provider closure of X-D4P-1's 100 MB size with margin.
- **Rejected:** a new interim value, such as 2^25 edges. That would be an invented cap (no census, no law), and it would edit `work_ledger.rs`.
- **The gate on the interim (X-SD9-1).** The interim is replaced by a sourced R10a profile **before any first-party component release is qualified, or before R10a's composition is claimed for production use, whichever comes first**. This is X-CI-1's gate (CIP LD-CIP-9), and the lead owns it.

## 5. The sourced profile: the census procedure (LD-S9-5; Q-SD9-3)

SD-9 does not run the census. It fixes the procedure, so that the sourced profile is derived and not chosen:
1. **Population.** Every first-party component release of M3's catalog, on each of the four platform tokens (`recovery_catalog.rs`:67-79). Within a platform, take the **largest selectable set**: every component that one R10a could admit together, which is every release the analysis step can select for that platform. This is not a T2 corpus and holds no held-out entry, so no blind mode is needed.
2. **Quantity.** A(Σ) of §2, computed componentwise from the signed TreeCommitments and catalog rows alone, before any acquisition, by the owners' own bound functions. These are CI-3's `open_bound` and `transfer_bound` (as CI-2 r1 aligns them), C2a's published `const fn`s, D4's, and C2a-3's M once it is published. The tool is a reviewed census tool in the manner of `tools/security/snapshot_ledger_census.py`, ids and counts only.
3. **Rule.** For each coordinate, the cap is **the smallest power of two at least twice the census maximum**. That is the rule of M3-B r6 and R9 (WL:16-29), with work beyond the margin in the typed-refusal regime.
4. **Landing.**
   - If every coordinate's rule value is at most the interim's cap, the lead may confirm `snapshot_profile()`'s caps as the sourced R10a policy, with the census as their source and no constructor change (Q-SD9-3).
   - Otherwise a new constructor is added. It edits `work_ledger.rs`, so it is sequenced into a reviewed census batch, as LD-CIP-9 requires for X-CI-1-a: a fresh baseline, a pre-run review, the frozen-input blind refresh and a post-run review.
5. **Combined with X-CI-1-a.** The same population yields `B_install` for X-CI-1. **Recommendation:** run both censuses as one unit, with one census batch if any constructor changes.

## 6. The `Budget` projection (LD-S9-6)

- **Every exhaustion of R10a's or ER10a's ledger is J1's row 11:** "An attempt or admission ledger charge refused". That is operational-failed / 4, `SYSTEM.OUTCOME.ILLEGAL_STATE` / host-invariant, detail `WORK.BUDGET_EXHAUSTED`, no runId and no executionId (J1:781; L468:49; the product's existing projection, `installation_termination.rs`).
- **Each owner's typed exhaustion keeps its type until J2's projection.** This applies to D4's `Budget` (D4P2 LD-D4-8), C2a's `WorkFailure::Budget` (CC), CI-3's `TreeReadFailure::Budget` (CI item 8: "`Budget` takes the caller's existing budget route") and C2a-3's.
  - None becomes `Corrupt`, `Missing`, not-installed or `ExcludedForm`, so rows 27, 28 and 56 are never selected for exhaustion (CI item 8; D4P2 LD-D4-11).
  - Exhaustion proves nothing about the tree.
- **Before the draw.** An R10a or ER10a exhaustion is returned before R11 and R12, or before the ephemeral attempt starts. So no analysis-attempt ExecutionId is drawn or reserved (J1 J-C10b, :410-416), and no partial admitted set reaches row 8's selection (J1 S19).
- **The ephemeral path.** ER10a's exhaustion takes row 11 unchanged.
  - It occurs before the ephemeral attempt starts (J1:498), so it is not a step termination.
  - RTC §7.4's rule ("No §7.5 detail is admitted for an ephemeral attempt", RTC:280-292) governs an analysis termination's `domainDetail`. `WORK.BUDGET_EXHAUSTED` is not that detail: it is the operational-failure envelope's registered detail, which law 468 also uses.
  - This is a lead reading, put to the reviewer as Q-SD9-4.
- **No code is added,** and no row is added: row 11 already names "an attempt or admission ledger" and needs only SD-9 in its basis (X-SD9-J1).

## 7. No pre-admission bound (LD-S9-7)

R10a does not compute A(Σ) and refuse before work, as CI's installer does with `install-budget`.
- **Why not.** A pre-bound refusal decided by signed data would be a request-class refusal with its own route. J1 has no row for it, and adding one would be a new route.
- **Instead,** the owners charge before each operation, and exhaustion is row 11 partway through. Every sub-step is read-only or pin-only, so nothing needs undoing: the pins die with the operation (CI item 7).
- **Rejected:** reusing `install-budget` (`EXTENSION.ADMISSION_REJECTED`). That is an installation refusal, and R10a installs nothing.

## 8. Controls owed by the wiring units (J3d, J2c, C2a-4)

- **SD9-T1, one ledger.**
  - A source pin over R10a's and ER10a's wiring: exactly one `WorkLedger::snapshot_profile()` construction at entry, and its scope passed to every sub-step of §2.
  - No `WorkLedger::new()`, `with_limits`, other profile or scope reset inside, and no per-component ledger.
- **SD9-T2, the aggregate.**
  - Two synthetic components (C2a-2's fixtures, CI's fixture store) in one ledger, with the charge equal to the owners' published bounds summed.
  - A ledger funded short partway through the second component's K or T refuses `Budget`, with no partial admitted set.
- **SD9-T3, the route.**
  - Exhaustion inside each of D4₁, C2a₁, B_open, T and K projects row 11. It is never row 27, 28 or 56.
  - On paths 3a, 3b and ER10a, the reservation sample is J-C10b's.
- **SD9-T4, the interim boundary.** A synthetic tree just within the snapshot profile's edge cap admits, and one just over it refuses on row 11. The boundary is computed from the owners' bound functions, not typed in.
- **SD9-T5, no trust view.** ER10a with no trust view charges nothing and admits nothing.
- **SD9-T6, census (with the sourced profile).** The census tool's output, its rule and the profile's caps agree, and an entry over the 2× margin is classified as typed refusal, as R9's census is.

## 9. Cross-law items

- **X-SD9-J1 (for J1's next revision):**
  - row R10a (J1:392) gains "on SD-9's admission ledger", and ER10a's bullet (J1:493) its counterpart;
  - row 11's basis (J1:781) gains SD-9;
  - item 13 records SD-9 as bound for R10a's and ER10a's ledger.
- **X-SD9-MD (for M3-D's next revision):** item 29's successor list (MD:1171) gains SD-9's row. Its form is a law record; its content is §§1-7; its owner is the lead; it gates C2a-4, J3d and J2c.
- **X-SD9-C2A:** C2a-4's Q5 gate (C2A:19, :85) is met by SD-9's acceptance, with the interim's gate (X-SD9-1) carried. **C2a-3's plan owes M(c)'s price** and its transfer-and-kernel shape (§3).
- **X-SD9-CI:** CI r5's "R10a's production profile is D4's and J1's" (CI:221, :302) is answered by SD-9. X-CI-1-a and X-SD9-1 share a census (§5).
- **X-SD9-1 (the interim's gate):** owned by the lead (§4).

## 10. Lead decisions

LD-S9-1 to LD-S9-7 above, and:
- **LD-S9-0. The form is a law record, not a contract successor.**
  - SD-9 selects a ledger, its caps and a projection onto an existing row. It changes no contract text: no NE, WS, RTC or schema passage.
  - Like SD-6 (MD:1181, "law amendment") and R9 (M3-C r9's caps record), it is accepted as a design unit and recorded by J1's and M3-D's next revisions. It binds no lock entry.
  - **Rejected:** a contract successor carrying the caps. No contract owns an R10a ledger.
  - **Rejected:** folding SD-9 into J1 r8 directly. LD-D4-SD9 names SD-9 as the reviewed unit.

## 11. Questions for the reviewer

- **Q-SD9-1 (form, LD-S9-0).** Is a law record the right form, with J1 and M3-D recording it, rather than a contract successor?
- **Q-SD9-2 (the interim, LD-S9-4).** Is `snapshot_profile()`'s caps an acceptable explicit interim for R10a and ER10a on X-CI-1's precedent? Its feasible boundary is about 0.75 to 1.0 GB of retained tree per admission. Its gate is X-SD9-1.
- **Q-SD9-3 (the census, LD-S9-5).** Is the procedure right: population, A(Σ) from signed data, the smallest power of two at least twice the maximum, and the combined X-CI-1-a census? May a census whose rule values fall within the interim confirm `snapshot_profile()`'s caps, with no constructor change?
- **Q-SD9-4 (the ephemeral projection, LD-S9-6).** Does ER10a's exhaustion keep row 11's `WORK.BUDGET_EXHAUSTED`? It is an operational envelope's detail before any ephemeral attempt starts, not a §7.5 analysis detail, so RTC §7.4 does not drop it.
- **Q-SD9-5 (the hashing term, LD-S9-3).** Is pricing C2a-3's in-memory transfer and C2a-3k's per-block hash, on top of CI-3's verifying open, the right whole-tree term until C2a-3's plan decides its shape? K is about 99 % of the edges, so a reviewer may want C2a-3's plan to revisit whether the kernel's re-hash after CI-3's verified transfer is needed. SD-9 does not decide that.
- **Q-SD9-6 (scope, LD-S9-1).** Are D4-4's launch recheck and Run retention's transfers rightly outside R10a's ledger, on their own callers' ledgers?

## Files

| File | What it is |
|---|---|
| `README.md` | this record |
| `evidence/check_sd9.py` | read-only: pins every authority above, reads every price from the product sources, and evaluates §2's terms over illustrative shapes |
| `evidence/check_sd9.output.json` | its output at `274dccc` |
| `evidence/build_sd9.py` | builds the subject manifest and the draft unit record; `--check` compares instead of writing |
| `../sd-9-subject.json` | the subject manifest (generated) |
| `../sd-9-unit.json` | the lead's draft unit record, `DRAFT-PENDING-REVIEW`; not part of the subject |

## Not changed, and not claimed

- No product file, code, constructor, cap, row, route, detail or public code. `work_ledger.rs` is unchanged.
- No census has been run, and no census coverage, release qualification or production R10a is claimed. C2a-3's M is not priced.
- The model's shapes are illustrations, not caps.
