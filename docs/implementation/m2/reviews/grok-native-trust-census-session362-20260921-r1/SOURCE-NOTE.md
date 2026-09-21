# SOURCE-NOTE — S9.3 standing vs 358 ADDENDUM (not 362 code approval)

**Standing:** targeted pin and after-image membership audit only. Not a 595-entry application replay, not new design/application acceptance, not implementation authorization, and not 362 product approval. Prior store-binding 358 `REVIEW.md` (`cf1903f4…17ff`, 8261 B) and `ADDENDUM.md` (`84da081d…9a8b`, 5589 B) are **unchanged**. Regardless of this note, native acquisition of five-member `StoreGenerationBindingV1` through an admitted handle and registry remains **unimplemented**; no header is invented and three-field `C.store` comparison is not promoted.

This audit verified eight files in `selected-source-audit/pins.json` (bytes and SHA256). It does not reread the rest of application 46.

---

## Pins (independently rehashed)

| Artifact | SHA256 prefix | Bytes |
|---|---|---|
| application-subject.v46.json | `dab6e00f…43f7` | 126405 |
| application-activation.v1.json | `faf90047…c4a8` | 758 |
| application-review.v46/review.json | `375b2e9d…5eb4` | 186003 |
| root-application46 assessment | `e59b2ff7…e238` | 5479 |
| security-and-lifecycle.md (current S9) | `a319da39…d9d6` | 119915 |
| store-instance-lineage.v1.json | `919d1717…5210` | 68487 |
| implementation-boundaries-and-build-plan.md | `8e6e8bab…d33b` | 112850 |
| product-design-lock.json | `64b3f3e5…e5dd` | 87064 |

Live product `design-lock.json` is **byte-identical** to the audit lock. Those three owner hashes appear as **after-image** rows in application 46 (`sha256` match). Distinct `beforeSha256` values in the same manifest are previous images, not the current lock.

Activation standing: “D-372 application activation; **design acceptance only**.” Independent review verdict ACCEPT. Root assessment: `rootApplicationAssent: true`. All four receipts still record `implementationAuthorized: false`. That historical flag is **not** current user authorization to implement.

---

## Does the ADDENDUM improperly infer S9.3 standing from a historical header?

**No.** The ADDENDUM’s line that “S9 still cannot express this validation … the S9.3 companion is proposed, not this join” tracks **current owning-source text**, not a stale receipt header.

- Current locked S9 (`a319da39…`) heading is still: `### S9.3 Private store-instance lineage (successor; proposed, not accepted)`.
- Current locked implementation-boundaries (`8e6e8bab…`) lines 266–269 still say current S9 cannot express the five-member handle/registry validation.
- Application 46 ACCEPT + root assent + activation accepted **those exact bytes** as the after-image. Accepting a file whose S9.3 heading remains “proposed, not accepted” does **not** upgrade S9.3 to accepted S9 law.
- The lineage companion (`919d1717…`) is also an after-image row. Membership of a companion artifact is not silent promotion of S9.3.

What would have been improper: treating an old “proposed” label as current standing **without** checking the locked S9 file. The ADDENDUM cited implementation-boundaries 266–269 (`8e6e8bab…`), which is the current lock, and the current S9 heading still says proposed.

---

## What this does not close

- Full 595-entry application replay (not performed; if a later question needs per-item S9.3 dispositions across every scoped review, that is a deeper audit).
- Native five-member `StoreGenerationBindingV1` via admitted handle/registry (still unimplemented in 361/362).
- Waiver of namespace/handle/registry; promotion of three-field current `StoreBinding` / `C.store` comparison.
- Implementation authorization (`implementationAuthorized: false` remains on these receipts).

Code verdict for 362 is separate from this note.
