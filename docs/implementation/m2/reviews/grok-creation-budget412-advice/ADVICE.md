# Creation budget412 — architecture advice

**Status: advisory, not approval.** Draft412 is uncompiled-into-product, unfrozen, unselected. Root implements. This does not review runtime35/source410, does not run native/Node jobs, and does not claim creator eligibility.

Product `e60ce01`, lock 35 inventory / 56 contract. Selected owner406 §1a/§2: host ingress allocates one `InitialInstallationAttempt` and one shared `CreationBudget` **before** account/path work; receipts borrow that attempt; counters are not authority.

## Dependency graph (why host cannot own the type)

Live edges: `identity` and `platform` have no OpenSIP deps; `security` → evaluator, platform, identity; `storage` → security, identity, platform; `lifecycle` → platform, identity; `host` → identity, contracts, platform, reporting, lifecycle, security, storage, evaluator. Host→security already exists. Security **must not** import host. Platform **must not** import security. Storage **can** import security, so a `pub` constructor on security is a reset hazard (a helper could `new()` a second ledger).

## Placement recommendation

**Do not freeze the draft’s private-host-only `CreationBudget`.** Host callbacks can use it; security graph/custody cannot name it.

**Reject a public accounting trait** (`WorkAccount`, `BudgetSink`). Arbitrary impls become boolean receipts. Owner §1a forbids caller-constructible capabilities.

**Reject “security-owned bookkeeping exported to host” as the constructor site.** Today `retained_metadata_index::Budget::new` is `pub(super)` and created inside trust after capture. Owner §2 says this act **extends** pre-installation ownership; it does not claim the post-capture helper already covers it. If `CreationBudget::new` is `pub` on security, host *and* storage can mint a fresh ledger mid-act.

**Select: non-authority work ledger in `platform`, owned once by the host attempt, borrowed downward.**

- `crates/platform/src/work_ledger.rs` — counters, limits, failure latch, Drop-guarded scope. No native handles, no receipts, no serde/Clone/Default. Only host’s attempt should call the constructor; security/storage/platform observers take `&mut WorkLedger` and **never** `WorkLedger::new`.
- `crates/host/src/initial_installation.rs` — `InitialInstallationAttempt` holds the unique ledger plus receipt lineage (`CreationIntent` … `InitialCreationPermit`). Matches owner §2 and existing `installation_*.rs` names.
- Adapt `crates/security/src/trust/retained_metadata_index.rs`: `Budget` must **borrow** that ledger (`Budget<'a> { work: &'a mut WorkLedger, raw, current, directories }`) instead of `Budget::new(objects,edges,bytes)` during this act. Digest/inode maps stay in security; they are caches, not a second cap.

A new crate would add a DAG node for little gain. Identity is the wrong owner (`no_std`, no native work).

Constructor discipline is the remaining leak: `platform` cannot hide `new` from security. Mitigate by a loud `for_initial_attempt()` name, no `Default`, and security/platform helpers that only accept `&mut WorkLedger`. Do not add `Budget::new` on the creation path.

## Joining trust `Budget` to the same ledger

Live `Budget` (same ceilings 65536 / 131072 / 268435456, record 4 MiB):

- **Objects** = `raw.len() + directories.len() + current.len()` (digest / device+inode / current identity). Cache hit does **not** consume a second object or re-add bytes (`retain` 208–216, `capture_current` 181–185).
- **Edges** increment on every `edge`/`directory`/`entry`/`load`, including repeat visits (`directory` 108 always `edge(1)`; `load` 274 always `edge(1)`).
- **Bytes** grow on first insert of name/`retain`/`current`; identical digest/inode does not double-count payload.
- **Latch:** `scope` sets `failed` on `Err` (72–82). It does **not** Drop-latch on panic, and it does **not** close before invoking `f`.
- `HostCapture` **ignores** `&mut Budget` (365–368). Unusable as a real producer.

Owner §2: digest/inode cache may dedupe **owned objects**; read/parse/lookup work and temporary buffers remain charged; repeated work is never free.

Join rule:

1. One `WorkLedger.used` / `failed` for the whole attempt. No nested `Budget::new`.
2. Keep security maps for digest/inode/`state.v1` identity. Cache hit: skip second object/payload bytes; still `work.edge` (and charge temp buffers explicitly, like `entry`).
3. Charge object **before** open/bind, not after `observe_directory` (today `directory` observes then maybe inserts).
4. Replace `Budget::scope` latch with the ledger’s Drop-guard so unwind and swallowed nested `Err` share one `failed` bit.
5. Never let cache helpers (`retain`, `capture_current`, `available`) zero or replace `used`.

Draft `record()` charges **bytes only**. P0 records in live `Budget` consume an **object slot**. When joining, `record` must reserve object+bytes, or graph validation will under-count versus trust.

## Draft arithmetic (bookkeeping only)

The six standalone tests in `checks.json` are **not** native qualification.

Sound: inclusive caps; `checked_add` on charge/effect; reservations kept on `Operation` failure; Drop latches unwind; swallowed nested `run` Err becomes outer `Closed` (272–279); unused postchecks stay in `used` (347); postcheck overrun still closes (365–376); over-cap refuses before action.

Defects to fix before integration:

1. **Cap check `OBJECT_LIMIT - used` is not `checked_sub`.** If `used` were ever above the cap, debug overflow / release wrap could skip the compare. Use `checked_sub` and map `None` to `Arithmetic`.
2. **`scope` does not set `failed` before the closure.** Drop covers panic; it does not match owner “pessimistically closes before invoking.” Set `failed = true`, run, clear only on success (and still Drop-latch if the flag is already true).
3. **`ReservedPostchecks.attempt` is same-module-visible.** `effect`’s closure must not `charge` extra on that field. Keep the field private; only `spend` the precharged remainder.
4. **`record()` omits an object slot** (see join).
5. **`charge(Cost::default())` after a full cap succeeds** if not latched. Zero-cost probes must still be on the latched path after a real failure; do not treat zero-cost as a reset.

`run` wrapping `charge` wrapping `scope` is redundant but consistent: inner Drop latches on charge refusal.

## Filenames

Inventory style: `crates/host/src/installation_*.rs`, `crates/platform/src/filesystem/*.rs`, `crates/security/src/trust/retained_metadata_index.rs`.

Add later via inventory successor (not this advice):

| Path | Role |
| --- | --- |
| `crates/platform/src/work_ledger.rs` | non-authority shared counters |
| `crates/host/src/initial_installation.rs` | attempt + receipts |

Do not add `crates/security/src/creation_budget.rs` as a second constructor. Touch `retained_metadata_index.rs` in place. `platform/src/lib.rs` only re-exports. No identity/lifecycle new file for this ledger.

## Gaps counters do not close

- Account lookup: caller buffers 130048 + ≤65535 owned home bytes must be **derived and precharged**; OS name-service allocations stay an external TCB premise.
- ACL 411: `fgetattrlist` omits `EXTENDED_SECURITY` for both null ACL and unsupported (`NOTES.md`, XNU vfs_attrlist); r4/r5 are fixture API notes, not a bound. No budget constant qualifies the observer.
- §1a producers (`InitialActor`/`InitialCore`/`InitialPlatform`/`InitialParentPreparation`/`InitialCreationPermit`) are unimplemented. Mock tests must not mint them.
- No boolean receipt constructors.

Root implements; later actual source review is required.
