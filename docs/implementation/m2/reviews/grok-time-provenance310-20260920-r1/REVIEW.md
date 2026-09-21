# Independent source review — first-clock historical core-anchor 310

**Standing:** source-only investigation of frozen `time-provenance-investigation-310`. Not a schema correction, product candidate, cumulative approval, or implementation. Installed product remains `fa72e50`. 309 REVIEW was not edited. ROOT-NOTES.md is treated as hypotheses. TIME-INPUT-JOINS.md / PROOF-NODE-JOINS.md are used as semantic scope; a generic old-T walker is an implementation obligation, not a newly discovered design defect.

Python 3.12.13 `-I -B`. Frozen pinfiles over live docs.

---

## Verification

Pins, tar bytes, member counts, and every `subject.json` hash matched **before** extract.

Frozen archive: **412372 B, 191 members, SHA256 `120c4046172c38d879540d7238f01b1eb871cede7efca5c81900f03527987dd5`**. Standing: source-only root investigation310; not a schema correction or acceptance candidate. Extract rehashed **191/191**. Nested frozen pins match live tars: 215 r14 `cd338af6…dd9c` (1445), 225 r2 `84e48e36…c413` (84), 222 r6 `5b6df2a5…1d5c` (165), 227 r9 `818604dd…6e44` (211), 229 r3 `edde8b4f…6b4e` (88). Full125 copies (`trust-capsule-shapes.v1.json` `1328ba16…4208`, `trust_input_reference.py` `13491b74…4393`, `trust_record_reference.py` `00ad3a34…e6df`) are byte-identical to frozen 309, 308, and 307 verified-reference. Local `/tmp/opensip-implementation/time-provenance310` matches this extract.

---

## Hypothesis under test

215 D and 225 require that a write establishing or advancing L retain, **before** publishing P1/L, the original authentication context: admitted **core anchor or authority head**, admission chain, revocation context, and evaluation inputs. Future replay must not substitute the currently selected core, current head, current expiry, or later revocations.

`S4EvaluationInputV1` encodes `beforeImage`, `beforeClock`, `observation`, invocation/store, and `source` `{none | ordinary+closure NodeRef | recovery+closure NodeRef}`. P0/P1 capsules must have `heads`/`history` **null**. `CreationInputV1.deliveringCore` is a `ClosureId`. `CoreAnchorNodeV1` retains three DocRefs (inventory/bootstrap/root) plus binding. Question: after first S4, even if later metadata entry fails (stay P1), is that CoreAnchor unambiguously addressable from retained T if the core cache is gone?

**Independent result: for P0 first S4 and P1 subsequent S4, no. For P2 ordinary S4, the capsule head chain encodes it; the first T still does not.**

---

## 1. Encoded dependency paths

Frozen 227 schema inventory from `S4EvaluationInputV1` NodeRefs: `beforeImage` → image (`TrustCapsuleV1`); `source.closure` → closure (`PayloadMetadataClosureV1`). `beforeClock` is an embedded `ClockPhase` (P1/P2 may embed `timeEvidence` → prior T). There is **no** inventory edge from the time input to `root` / `CoreAnchorNodeV1`. CreationInput is `pending:creation-input`.

### P0 first S4 (unevaluated → evaluated)

| Edge | Target | Reaches CoreAnchor? |
|---|---|---|
| `beforeImage` | P0 capsule | **No.** `heads` and `history` are null (227 CODECS; `shape_join_model.py` `pre-acceptance heads absent`). Clock is `{phase:unevaluated}` only — no `timeEvidence`. |
| `source.closure` | `PayloadMetadataClosureV1` | **No.** 227 PROOF-NODE-JOINS: closure must stay free of root-admission backreferences. `rootChain` is ≤64 **DocRefs** of payload roots, not `coreInventory`/`bootstrapManifest`/index-0 root of the delivering core. Using that chain as the delivering-core locator is the substitution 215 forbids (“never a payload-supplied self-signed anchor”). |
| `CreationInputV1.deliveringCore` | `ClosureId` (`closure2:` + 64 hex) | **No.** Identity string, not a NodeRef. 229 C.5: copy six blobs into records **when the CoreAnchor node is written**; “No source guarantees a superseded core generation stays readable.” A ClosureId is not those six blobs. Selected-core lookup is not historical proof. `storeMarker` is a store marker, not the anchor. |
| Event walk to `CreationEventV1` | pending codec | **No unique bounded locator.** Not in the 227 time-input inventory; even if walked, it still yields only ClosureId. |

After a successful first S4, P1 `clock.timeEvidence` points at this S4EvaluationInput. Replay of that T still has only the edges above. Metadata-entry failure leaving the store in P1 does not later attach `heads`. Cached selected core cannot be substituted (215 D, 225 “Retained provenance”).

**Exact missing join:** no `NodeRef` on the first time proof whose target kind is `RootAdmissionNodeV1` / `CoreAnchorNodeV1`, and no deterministic records-key from ClosureId to the six retained blobs.

### P1 subsequent S4

Same null heads/history. `beforeClock.timeEvidence` / `beforeImage.clock.timeEvidence` may name the first T. That first T still lacks the CoreAnchor edge. The new `source.closure` is the **current** payload, not the delivering core. Walking old T is how you recover the first proof; it does not invent a core NodeRef that was never encoded.

### P2 ordinary S4

`beforeImage.heads` is non-null `AcceptedHeads`. `heads.root.admission` is a `NodeRef` whose 227 inventory target is **root** (`RootAdmissionNodeV1`).

`RootAdmissionNodeV1` is a closed union:

- `kind: "anchor"` → `CoreAnchorNodeV1` (`coreInventory`, `bootstrapManifest`, `root` DocRefs + `RootBinding` + `coreClosure` + platform). 229 C.1–C.2: index-0 embedded bootstrap root; joins recomputed from retained bytes.
- `kind: "ordinary"` → `parent` NodeRef (another admission) + `root` DocRef + `OriginalContextV1` `{time, priorRevocationHistory, incomingRevocation}`.
- `kind: "recovery"` → parent + authorization + closure + context.

`beforeImage.history` is a revocation-history NodeRef. `source.closure` carries presented roots and incoming revocation for **this** payload. `OriginalContextV1.time` on a later admission is the S4 input that authenticated **that** root edge.

**P2 wire data for original authority is present** on the **before capsule**, via `heads.root.admission` parent-walk to `kind:anchor`. That is not implemented admission (joins, original vs current revocation, proof-only successors, budget, acyclicity). It also does **not** retrofit the **first** T: historical replay of P1’s timeEvidence still uses the P0/P1 encoding.

Payload `rootChain` maxItems 64 is per-payload presented roots (225: final chain document’s issuedAt), not unbounded lifetime ancestry. Do not confuse it with the CoreAnchor parent walk.

---

## 2. Revocation, successors, T, cycles

**Original vs current revocation.** P2 `beforeImage.history` plus `OriginalContextV1.priorRevocationHistory` / `incomingRevocation` are the encoded original revocation facts. P0/P1 have `history: null`; first T has only whatever revocation **DocRefs** sit on the payload closure (current presented list), not a retained history node. Missing **algorithm**: re-admit original context, never later lists/expiry (215 D, 225, 227 “context.priorRevocationHistory must match the actual admitted BEFORE history”).

**Proof-only successor roots.** 215: a root authenticated only inside this proof is not an accepted head. 227: authentication is not accepted standing. Encoded as RootAdmission vs `AcceptedHeads`; missing **algorithm** to keep those distinct.

**Accepted head vs new head.** 227 acyclicity: S4 authenticates from the **BEFORE** image. A `RootAdmission.context.time` may name that S4 input. The S4 input must **not** take `authority` from the AFTER head it helps publish. Replacing BEFORE with the new head is a circular proof. Missing **algorithm**, not a new cycle field.

**T keep vs new.** 227 TIME-INPUT-JOINS: new T iff `lastAccepted` is written; equal/older source keeps prior T; BEGIN/COMMIT still create a **fresh evaluation input** under current context. Old T in `beforeImage.clock.timeEvidence` is a historical dependency, not a license to skip original context. Narrow S4.5/ABORT/diagnostic exceptions must not be applied to ordinary entry (implementation scoping; not a new 310 defect).

**Roles/OLD/R.** P2 `roles` / `batch` can retain those records; they are premises until typed population/admission exists (308 remainder).

---

## 3. Minimal correction (if a later freeze corrects 125)

Existing typed formats are **sufficient as targets**. Do not add `trusted:true`, do not retune S4/S4.5, do not put root-admission on `PayloadMetadataClosureV1`, do not treat ClosureId as a six-blob locator, do not walk payload `rootChain` as delivering-core ancestry.

**Smallest closed field:** on `S4EvaluationInputV1` add `authority: NodeRef` whose target kind is already `RootAdmissionNodeV1` (union includes `CoreAnchorNodeV1`).

Joins (typed admission, not cache):

- If `beforeImage.heads` is null (P0/P1): `authority.kind` must be `"anchor"`; `CoreAnchor.coreClosure` equals this store’s original `CreationInput.deliveringCore`; 229 C.2 bindings; six blobs present as records. This is the first-T locator after core-cache removal.
- If `beforeImage.heads` is non-null (P2): `authority` SHA/length **equals** `beforeImage.heads.root.admission` (BEFORE accepted root). Do not bind the AFTER head.

Owner: 227 time-input codec + 229 anchor joins. Charge 222 budgets (131072 edges / 65536 objects / 256 MiB / 4 MiB object). Canonical private bytes. Native/reference tests: P0 first S4 with six blobs; P0 with only ClosureId refuses; P1 replays the same `authority` after selected-core change; payload `rootChain` cannot substitute; P2 `authority` matches BEFORE head; new RootAdmission.context.time may cite the S4 input, not the reverse.

**Do not silently edit frozen 125 in this packet.** 309 remains P2-only candidate assembly and does not claim this solved.

---

## Combined table

| Path | CoreAnchor from retained T? | What is missing |
|---|---|---|
| P0 first S4 | **No encoded NodeRef** | Wire: `authority` → CoreAnchor; ClosureId/payload rootChain/cache are not locators |
| P1 subsequent S4 | **No** (heads still null; first T still incomplete) | Same wire gap on every T minted in P0/P1 |
| P2 ordinary S4 | **Yes, via `beforeImage.heads.root.admission` parent-walk** | Algorithm: original auth, acyclicity, proof-only vs accepted, revocation context, budgets |
| Generic old-T walk | Must not be the policy | 227 scoped exceptions (S4.5/ABORT/diagnostic) vs dependent entry |

---

## Remaining (do not count closed)

309 does not walk or persist these proofs. 311 (fresh evaluation records on Keep) is 227 publication law, not this core-anchor gap. Original T admission, current population, 222 durability, custody/census, and M3–M6 remain open.

---

## Verdicts

- [x] **310 source conclusion:** P0/P1 first-clock CoreAnchor is **not** unambiguously reconstructible from retained S4EvaluationInput / P1 T after core-cache removal. P2 has an encoded head-admission path that is not an implemented admitter. Smallest later correction is an `authority` NodeRef on `S4EvaluationInputV1` targeting existing `RootAdmissionNodeV1`.
- [ ] **Not** a 125 edit, product implementation, 309 defect, or cumulative approval.
