# Independent review — native recovery authorization 260

**Standing:** bounded native-Rust review of frozen `native-recovery-authorization-checkpoint-260`. Ports reviewed 250 authorization **body** joins onto the 259 carrier snapshot as a private evidence constructor. **Not** held-root selection/custody, complete current revocation population, incoming union, payload/metadata members, ancestry/floors/S4, role/batch effects, live census/fence/slot/durability/writers, aggregate Operation budget, or source selection. Next 261 is expected to own full body-envelope raw retention. Archived 259 (`88cb9f66…409a`) and 258 were not edited.

Rust 1.95.0. Review-local `product/` copy only; installed product was not written. Frozen fixture/key/result directories were not overwritten. Keys are **TEST ONLY**. 259 workspace 472+2 was **not** rerun.

---

## Verification

Frozen archive: **4211292 B, 442 members, SHA256 `d5ac8acdb86bb9ae3b43a87ad7862ce29e7f79e5c0a6c79b9109aebe6ffa5e50`**. Pin, tar, member count, and every `subject.json` hash matched before extract; extract rehashed 442/442. Standing: Unaccepted private 260.

Parent 259 pin `233fee7d…da4b` matches the reviewed 259 archive. Nested 250 r2 pin `dbf1aa27…cf85` (35248 B / 117 members) matches the frozen 250 r2 trial tar; all 117 `subject.json` members rehashed. Reviewed helper bytes equal that extract: `authorization_reference.py` `6b6f0fb2…3353`, `check_authorization.py` `44a38c7d…cea2b`.

Product: **360** files vs 259. **358** byte-identical, **1** changed (`crates/security/src/trust.rs`), **1** new fixture (`root-recovery260-cases.ndjson`). `trust-before.rs` is byte-identical to 259 `trust.rs`. Product-input hashes match extract 360/360.

---

## What 260 adds

Private `mod verified_root_recovery` (not `pub`). `verify_root_recovery` / `RootRecoveryEvidence` are `pub(super)` with **private fields** and no public constructor. Inputs are typed `WireRootLink { stored: &[u8], envelope: &V }` plus an already-admitted held root and a `BTreeSet` of retained key ids. That link holds a raw body slice and a **parsed** envelope value; it does not claim to own exact envelope source bytes. Per-document `MAX_BYTES` is applied; there is no aggregate Operation capture.

Body checks match 250: closed seven fields; `authorizationSchema` integer 1; kind `root-recovery-authorization`; 1–6 known sorted unique roles; literal held/new **domain** RootBindings (`rootSchema`/`rootVersion`/`rootDigest`), not raw SHA; strictly increasing version; `held.issue <= new.issue <= RA.issue < notAfter <= new.expiry`. Held expiry is intentionally **not** an activation check. Then actual held RECOVERY (`RootRecoveryAuthorization`) and new self-ROOT envelope signatures, both filtered by the supplied retained-key set.

Reuse existing admit-root / carrier / Ed25519 / calendar. No publisher or caller-supplied signer shortcut.

---

## Reproduction vs inspection

| Kind | Corpus | Result |
|---|---|---|
| Exact live | `cargo test --offline --locked -p opensip-security` | **176/176** |
| Exact live | workspace Clippy `--all-targets -D warnings` | **pass** |
| Exact live | 7 compiled omission controls + baseline | **8/8**, source SHA equal frozen `mutation-check-r1` |
| Inspected | Recording r1 (adapted 250 checker) | **50/50** python assertions; **34** native rows, **7** successes |
| Inspected | 16 budget/failstop/DocRef/missing-raw/malformed-revocation/standing rows | **not** native tests |

Seven successes: 2→2 actual old-RECOVERY/new-ROOT; schema pairs 1-1 / 1-2 / 2-1; expired held; recovery 3 surviving; root 2 surviving. Negatives cover bool schema, duplicate/unknown/empty roles, extra binding field, raw SHA vs domain digest, calendars/windows, non-increasing version, wrong old keys, both revocation-filtered thresholds.

Controls (compile, then fail the native test): omit authority binding; omit replacement binding; omit version increase; omit role order; omit time window; omit authority revocation filter; omit replacement revocation filter.

Document refusal categories (`RecoveryAuthorizationError`) are private, not a public mapping.

---

## Independent probes

| Probe | Result |
|---|---|
| Public API | module/evidence/fn/`WireRootLink` not `pub`; fields private |
| Integer schema / closed 7 fields | bool kind/schema refuse |
| Binding digest | `rootDigest` == admitted root digest; raw SHA case refuses `ReplacementBinding` |
| Expired held | success case present; comment: not activation |
| Both quorums + retained filter | RECOVERY then ROOT; empty-set mutants fail |
| 250 helper/checker | byte-equal frozen 250 r2 |
| 259/258 REVIEW.md | hashes unchanged |

Returned evidence still does not prove current population, prospective keys, or command authority.

---

## Remaining (do not count closed)

Held-root selection and custody; complete incoming/retained revocation union; full payload/metadata/path members; accepted ancestry, floors, S4; role/batch/whole-image effects; native fence/slot/census/durability/writers; aggregate capture context and exact envelope-source-byte retention (261). 260 is not installed runtime source and adds no product callsite.

---

## Verdict

- [x] Archive/pins/members verified. 360 product files: 358 unchanged vs 259. Nested 250 r2 117/117 rehashed.
- [x] **176** security tests and workspace Clippy reproduced. Seven omission controls caught; baseline passes. 34 native cases / 7 successes match the recording fixture.
- [x] Closed 7-field integer body, domain RootBindings, version/time, actual old RECOVERY + new ROOT, both revocation filters. No public constructor.
- [ ] **Not** current authority, complete population, envelope-byte custody, native publication, or source selection.
