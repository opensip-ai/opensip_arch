# Advisory — selection.pair ownership and native join (not 354 approval)

**Standing:** source-and-ownership adjudication only. Not a review of unfrozen 354 product, not codec validation, not selected-I/current authority. Frozen 353 REVIEW `5fb5ea84…9b5b` (7242 B), 352 `9a2fbd3f…f18e`, 351 `ca61ae4c…534f`, and 350 `a2815d6b…d084` were read and are **unchanged**. No candidate/frozen/history edits. Unfrozen 354 product bytes were **not** inspected.

Source-audit copies match their pins: `physical-owner203.md` `292dbab3…e5ac` (14728 B); `private-trust-127.json` `a0431300…7928`; inventory v32 `105a260d…b72e`. 203 remains **working unselected** physical-owner text; 127 is the current private schema bound from frozen 353 fixture provenance, not an older 203-era schema.

---

## 1. Normative split (what the sources require)

**203 physical owner (working):** lifecycle owns slot, **selection**, carriers, lineage. Security owns trust state and **source fencing**. Storage owns retained store **data and floor decoding**. The **host** joins them under **one retained installation fence**. `selection.pair` is the sole executable-core/store selection carrier. The record **alone proves neither** marker/full store binding nor closure. Absence of the pair is **not** permission to initialize an existing I. Bytes and the **same retained descriptor** share owner/mode/ACL/name/nlink/local-FS/exclusion-through-use; **owned bytes or observations alone grant none of them**. No arbitrary caller path.

**Inventory v32 (proposed DAG):** lifecycle **may** depend on identity, security, storage. Security **must not** depend on storage. Host depends on security, storage, and lifecycle. That permits host-join; it does **not** require lifecycle to import security in order to decode JSON.

**Frozen 351–353 (established):**

| Fact | Consequence for the next native join |
|---|---|
| 351 groups-only I from OS account; real==effective; missing ≠ create | Native I is not selected S/core/profile |
| 352 `NativeInstallationFence` crate-private; source lives **inside** the inner guard; `as_supplied()` is how 350 keeps account/home; supplied factory stays `None` | A public root handle that skips native source is a provenance escape |
| 350 `ProfiledCensus` needs a **verified profile first**, then qualifies contributing operational Files vs I-root (device+fsid+type/local/nonunion) | Pair **use** cannot precede profile bind; pair **read** can |
| 353 generic `Store::read` stays `Capture`; `complete()` is owned, **not** a `Store`-trait obligation | Do not invent a second generic “must complete” trap at the crate boundary |
| Public `observe_bound_operational_file(parent, leaf, cap)` takes a **supplied** `RetainedDirectoryPath`, does not carry native fence/account, and `into_parts()` yields a `File` that outlives any fence | **Not** the selection.pair join API |

Frozen 353 **lifecycle** depends only on **platform**. Inventory already lists identity; adding **identity** for canonical JSON is the codec step. Frozen **host** does not yet depend on security/storage/lifecycle.

**127 current fields (syntax only):** `ClosureId` = `closure2:` + 64 lower-hex; `StoreId` = 32 lower-hex; `StoreBinding` = `{storeInstanceId, storeGeneration: 0..=i64::MAX, stateSchema: 1\|2}`. There is **no** `InstallationSelectionV1` schema object in 127; 203’s five-member pair is the working layout that **composes** ClosureId + StoreBinding + `selectionSchema:1`.

---

## 2. Smallest correct next steps (two layers)

**A. Codec (what 354 is for; root is validating this separately).**  
Private lifecycle decoder of exact five members, 4096-byte cap **before** parse/copy, product-canonical JSON, `StoreComponent` grammar reused `pub(super)` (not a public S API). Direct **identity** dependency only. **No** security or storage dependency, **no** I/O, **no** fence, **no** marker/closure proof. `coreClosure` is identifier **syntax**, not 323/229 inventory/tree. This must not be described as native selection composition.

**B. Native composition (after the codec freeze, not inside it).**  
Host-owned join only:

1. `NativeInstallationFence::try_acquire(&supplied_groups)` (352; groups still **SUPPLIED**).
2. Security mechanism: **single-component** leaf under that held I, cap supplied by the **semantic owner**, all 203/341/352 checks, **source pre/post**, no JSON.
3. Lifecycle: decode those bytes (codec A).
4. Storage: admit **marker** at `stores/S` and **full** binding `(S,G,K)`.
5. Host: require pair.S/G/K **equal** storage’s admitted binding; bind pair.C through the **existing** closure/inventory owner (323/229), then a verified profile, then 350-class FS qualification of the **original held File** (and other contributing operational descriptors) before **use**.

Do **not** put SelectionV1 in security. Do **not** make security depend on storage. Do **not** make lifecycle the fence holder. Inventory **allows** lifecycle→security; the **smallest** join does **not** need it — host already has to depend on all three.

---

## 3. Assessment of the proposed boundary

The proposed split (opaque security observation/fence + borrowed bounded capture; lifecycle-private five-field decode; storage marker/full; host joins C/S/G/K) **matches 203 and inventory**, with these corrections:

**Path/cap must not become authority.** Security must not accept a caller-built `RetainedDirectoryPath` (that is today’s `observe_bound_operational_file`). The only root is the **native** fence’s I. The leaf is **one** component (no `/`, `.`, `..`); lifecycle passes the documented name `selection.pair` and cap `4096` as **its** constants, not as a discovery walk. Cap is a **read bound**, not admission of the JSON. Storage’s marker path is `stores/` + S under the **same** fence, not a second root.

**Do not leak raw root / `as_supplied()` / `into_parts()`.** 352 keeps account/home because source is inside the inner guard and 350 borrows that guard. If lifecycle or host receives `root(): &RetainedDirectoryPath` or `File` after dropping the fence, 351/352 provenance is gone. Public `ObservedOperationalFile::into_parts` is exactly that escape; a selection join type must **not** offer it. Keep `File`+bytes under `&'fence NativeInstallationFence` (or a session that **owns** the fence). Recheck source+leaf+descriptor before promoting from provisional to used.

**Provisional read until core/profile/marker — yes, and it should be a type.** 203: admit marker/full binding **and** closure **before use**. 350: profile before census FS-name law. Bootstrap order is therefore:

| Stage | Allowed | Not allowed |
|---|---|---|
| Fence + single-leaf capture | Custody, same-volume vs **already sampled I-root** (350 device+fsid, local/nonunion), exact name/nlink/ACL | Profile `installRootFilesystems`, selected S, core proof |
| Lifecycle decode | Five-field syntax, 4096 cap, canonical raw equality | “This is the selected installation” |
| Storage marker/full | `(S,G,K)` identity of an existing store | Current/CLEAN/BEHIND/FORK, writers |
| Host equality + closure/profile | Bind C and profile; **then** 350 qualify the **same** held File | Using the pair as launch/current authority before that |

So the first read **must** be a `ProvisionalHeldFile<'fence>` (or equivalent). Decode produces `DecodedSelectionV1` **without** a `SelectedInstallation` type. Promotion is a later host join, not a decode side-effect. Same-volume vs I-root at capture does **not** replace profile qualification; it only keeps host-foundation §1 operational descendants on I’s filesystem **before** a profile exists.

**`complete()` analogy:** do not add a trait that type-forces every reader to “finish” selection. Host is the only production joiner, like `capture_p2` is the only production `NativeStore::complete` caller (353).

---

## 4. Implementation advice (not new public commands)

Concrete lifetimes (names illustrative):

- Host **owns** `NativeInstallationFence`.
- Security (crate-public, opaque, macOS-gated as today):  
  `capture_i_leaf<'f>(&'f NativeInstallationFence, leaf: &str, cap: usize) -> Result<ProvisionalHeldFile<'f>, …>`  
  — `leaf` one component; openat from the fence’s I; 352 source + 341 lock/name/inode + 203 file policy; bounded read; **no** JSON; **no** `root()` getter; **no** `into_parts`.
- Lifecycle: `decode_selection_pair(bytes: &[u8]) -> Result<DecodedSelectionV1, …>` — bytes only; cap already enforced by the capture; owns exact raw + five fields after full validation.
- Storage: existing/next marker and full-binding admit under the **same** borrowed fence (storage may use security; security must not call storage).
- Host keeps `ProvisionalHeldFile<'f>` alive through marker/closure/profile, rechecks, then may form a later join type. Missing leaf is **unavailable**, not create.

Reuse 352’s inner recheck so a 350-style borrow of the **native** wrapper still samples account/home. Do not expose the historical supplied factory as the selection path (`native_source: None`).

**Facts that must not be claimed:** decoded pair = selected I/S/core; ClosureId syntax = inventory/tree/digest; marker match = current authority; provisional File = 350 profile FS qualification; fence = 5s scheduler or `--trust-group`; missing pair = initialize; `observe_bound_operational_file` = this join; codec 354 = native composition; 203 working text = frozen selected protocol.

Writers/replace of `selection.pair` are out of scope here (203 publication profile stays later).

---

## Verdicts

- [x] **Codec stays in lifecycle** (identity + `StoreComponent`); **not** in security. Inventory allows identity; frozen 353 lifecycle is platform-only today.
- [x] **Native join is host-owned.** Smallest path does **not** require lifecycle→security or security→storage. Security remains fence + opaque single-leaf capture.
- [x] **Caller path/cap are not authority:** only native I, one documented leaf, cap as read bound. No public root escape / `into_parts`.
- [x] **Initial read is provisional** until marker/full `(S,G,K)`, closure bind, and profile-qualified held File. Type-level, not a comment.
- [x] **203 “record alone proves neither”** and 351–353 “no S/core/profile from I/fence” remain. 127 has no InstallationSelection object; five fields compose ClosureId + StoreBinding.
- [ ] **Not** unfrozen-354 review, codec pass/fail, selected-I, or product installation.
