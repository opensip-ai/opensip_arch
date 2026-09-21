# Independent review — project-registry owner371 r3

**Verdict: `NEEDS-CHANGES`**

Frozen OWNER/REFERENCE only. **Not** selected, **not** five-member binding, **not** S9.3, **not** native/OS qualification, **not** product runtime. Archive `81d87380…314a` / **213836 B / 118 members**; every subject member rehashed (0 mismatches). Candidate `registry-draft.md` `b7f2f23f…71f6` / 25969 B; schema **byte-equal r2** `b8059210…0d5e`. r2 review `32faf2e8…3660` archived and unchanged. No product/architecture edits.

Independent replay in new dirs (`-I -B`, jsonschema 4.25.1): **254/254** cases (results byte-equal author `f204b9ff…e52d`; 251 unique names); **23/23** schema+extra-rule; capacity max **320555**; **7** faults detected after baseline, including `ordinary-bypasses-adoption-context`. Extract not overwritten. No native suites.

---

## r2 required findings

**Addressed for the absent-namespace+exact-marker pair:**

- Ordinary first-use: absent marker; RESERVED → 0700/two empty 0600 leases → **create-new** marker → ACTIVE.
- Ordinary recovery **refuses** absent namespace + exact marker (`ADOPTION_CONTEXT_REQUIRED`).
- Adoption section: admitted bundle/source-target first; exact existing marker **retained**, file+parent durability **reconfirmed**, **not** create-new; absent marker may create-new **after** namespace under the same admitted adoption context; registry activation does **not** complete import/evidence/origin.
- `mode` is a supplied-context **label**; unknown/caller-adopt → `NO_COMPLETION_AUTHORITY`. Observation matrix is not a crash-reachability proof. Three ordinary durable prefixes only: reserved-only; namespace-before-marker; marker-before-active.
- RESERVED/ABANDONED flock is **unregistered-lease**, not BUSY. Pure `initial_namespace_footprint` checks exactly two empty regular 0600 files in 0700 dir (not custody).

That **narrows** ordinary recovery for the r2 hole. It does **not** rubber-stamp the whole distinction.

---

## Remaining required gap (do not broaden ordinary recovery)

Ordinary-recovery still returns `publish-ACTIVE` for **`complete-initial` + `exact` marker** (`ordinary-durable-prefix-marker-before-active`).

That filesystem shape is lawful for **interrupted first-use** (namespace published, create-new marker done, ACTIVE not yet published). It is **also** the shape of **interrupted adoption** after fresh-N publication when the target already held the bundle marker. The RESERVED row has **no kind** (`random` vs `adopt`). `reservation_completion` does not receive the document, so it cannot see that the reserved ProjectId already exists on a historical row.

**Trace:** `reserve-adopt` RESERVED (prj1-A, N_new); copy exact bundle marker; publish two-file namespace; crash before ACTIVE. Observations: complete-initial + exact. **Ordinary-recovery ACTIVEs** without re-acquiring admitted-bundle context. Prose says adoption interruption must reacquire bundle context, but the **model allows ordinary-recovery** on this prefix. Registry-only ACTIVE of an adoption ProjectId then leaves import/origin owners unsatisfied — draft admits that for “complete namespace/marker pair,” which is exactly this path.

Refusing only **absent-namespace+exact** is necessary and not sufficient. Broadening ordinary recovery further would be wrong; the fix is to **keep ordinary recovery narrow**:

1. Persist reservation **kind** on the RESERVED row, **or** treat reserved ProjectId already present in any historical entry as adopt-shaped.
2. Ordinary-recovery may ACTIVE **only** first-use/random reservations.
3. Adopt-shaped RESERVED requires `admitted-adoption` (real bundle context, not a mode string) for **every** completion, including complete-initial+exact.
4. If bundle context cannot be reacquired: unavailable/refuse; do not ACTIVE.

Mode remaining a label is acceptable **once** the row/document distinguishes adopt vs random so ordinary-recovery cannot ACTIVE the former.

---

## Initial namespace / other notes

Two empty lease files after durable RESERVED, no-replace onto positively absent `I/host/projects/N`, recovery join RESERVED+root+complete footprint: conservative and not SQLite revival. `complete-initial` token is still not automatically AND-ed with `initial_namespace_footprint` inside `reservation_completion` — native must compose them (same honesty as r2 supplied observations). Not a second required finding if the kind-split above is done.

No opaque-`projectKey` revival. T1–T4, T6–T8 prose from r2 remain on these bytes.

---

## requiredFindings

1. Ordinary-recovery of **complete-initial + exact marker** can ACTIVE an **adoption-shaped** RESERVED because the row has no random-vs-adopt kind. Close that without widening ordinary recovery.

Not selected. Not implementation. Root’s selection wrapper must wait on a freeze that closes this trace.
