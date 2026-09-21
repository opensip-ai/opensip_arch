# Addendum — `NonNull<DIR>` is not auto-`Send`/`Sync`

**Standing:** factual correction to the already-written 330 REVIEW. REVIEW.md is **unchanged** (SHA256 `75b9b10e…468e`). Not an implementation patch and not a 331 start.

REVIEW FFI ownership said: “`NonNull<DIR>` is auto-`Send`/`Sync`; the API never stores the stream across threads.” That **trait assertion is false** on the review toolchain.

---

## Independent check

Local Rust **1.95.0** `library/core/src/ptr/non_null.rs` (Homebrew sysroot):

```text
impl<T: PointeeSized> !Send for NonNull<T> {}
impl<T: PointeeSized> !Sync for NonNull<T> {}
```

Stable since 1.25. The file comments that the negative impls exist for diagnostics (`*const T` is already not `Send`/`Sync`).

Compile probes with `rustc 1.95.0 --edition 2024` in `grok-out/independent/nonnull-send-probe/` (not product):

| Probe | Result |
|---|---|
| `need_send`/`need_sync` on `NonNull<u8>` | **E0277**, exit 1 (`Send` and `Sync` both missing) |
| `NativeEntries { stream: Option<NonNull<DIR>> }` | **E0277**, exit 1 (`NonNull` → `Option` → `NativeEntries`) |
| `need_send::<std::fs::File>()` | exit 0 (positive control) |

So 330’s private `NativeEntries` is **`!Send` and `!Sync`**. It cannot be sent or shared across threads by auto trait.

---

## Does any conclusion change?

**No** FFI, census, or verdict change.

The mistaken sentence treated auto-`Send` as a residual caveat and then said the API never stores the stream across threads. The language already **forbids** sending `NativeEntries`. That is stricter than the caveat, not weaker. Concurrent `visit_entry_names` on `&RetainedDirectory` still each `openat` a new description; `File` remains `Send`. No product edit is required.

Remaining 330 bounds stand: `Summary` is not a qualified census; Apple skip/null-without-errno; Linux ABI unexecuted; union flags not a union mount.

---

## Verdicts

- [x] **Trait correction:** 1.95 `NonNull<T>` has explicit `!Send`/`!Sync`; 330 `NativeEntries` inherits both.
- [ ] **Not** a 330 implementation defect, census promotion, or 331 review.
