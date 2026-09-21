# Fact addendum — two factual corrections to my owner397 review

Separate note appended after the fact. **`REVIEW.md`, `findings.json`, `hashes.txt` and `evidence/` are
unchanged and remain the report of record.** This addendum is deliberately not listed in that
`hashes.txt`. The NEEDS-CHANGES verdict is unaffected, and so are B-1…B-3 and N-1…N-6, which this note
does not touch.

Root supplied three facts. I verified all three myself rather than accepting them. Two of my statements
need correcting — one of wording, one of substance — and the substantive one is mine alone.

---

## 1. `defectsFound` is a count, not a boolean — both wordings were wrong, the C-1 principle is not

**Verified.** `schemas/sources/invocation-v5.schema.json` → `$defs/DoctorResult`:

```json
"reportProduced": { "type": "boolean" },
"defectsFound":   { "$ref": "urn:opensip:product-v1:workflows:evaluator3:common:4#/$defs/Uint53" },
"defects":        { "type": "array", "maxItems": 256, "items": { "$ref": "…#/$defs/DomainDetail" } }
```

and `common-v4.schema.json` → `Uint53` is `{"type": "integer", "minimum": 0, "maximum": 9007199254740991}`.
`reportProduced` is the boolean; `defectsFound` is a **count**.

**Verified.** `docs/coop/design-corrections/workflows/workflows_model.v1.py:2055`:

```python
return {'kind': 'doctor', 'reportProduced': True, 'defectsFound': len(defects), 'defects': defects}, \
       terminate({'event': 'doctor-report', 'reportProduced': True, 'defectsFound': len(defects)})
```

So `defectsFound` is literally `len(defects)`.

**Both wordings are wrong.** 397's "set `defects-found` true" is wrong, and so is my C-1 text — I wrote
"`defects-found` becomes **permanently true**", "that boolean", and "the field selected law directs CI
to inspect becomes a constant". A count cannot be set true.

**The C-1 principle survives, and the correct reading makes it sharper, not weaker.** The same model
file, at lines 186-187, does this:

```python
if obs.get('defectsFound', 0) > 0:
    t['domainDetail'] = {'code': 'DOCTOR.DEFECTS_FOUND',
                         'remedy': 'inspect doctor.defects; exit 0 means the report was produced'}
```

Under 397 every healthy installation yields at least the one informational entry, so `defectsFound ≥ 1`
always, and therefore **every successful doctor run carries the `DOCTOR.DEFECTS_FOUND` termination
domain detail**. That is a stronger statement than the one I made: it is not only that a field loses its
signal, it is that a termination-level domain detail fires unconditionally, and the natural CI gate —
`defectsFound == 0` — is unsatisfiable on a healthy machine.

So C-1 should be read with "count" substituted for "boolean" throughout, and with the corrected
consequence above. Its requirement is unchanged: keep the diagnostic, but do not let it contribute to
`defectsFound`, or give it a filterable kind, or record the parity change §9 currently forbids.

---

## 2. C-3 is incorrect — `recover(ExecutionId)` is a real selected selector

**This one is my error, not a wording slip.** I wrote that `recover(ExecutionId)` "has no referent".
It does.

**Verified.** `docs/v2/contracts/product-v1/identity-and-evidence.md:1685`:

> **Read-only recovery selectors.** `recover(ExecutionId)` takes the `SHARED-READ` lease and reads
> **one** consistent committed ledger snapshot carrying the receipt, the private recovery association
> **and** the `AttemptCustodyV1` phase together.

and at line 1702, of that same selector:

> It performs no witness INIT/REVERT/ADVANCE, no high-water raise, no store-binding allocation, no new
> execution grant, **no fence acquisition** and no wait on a writer.

It is referenced again at line 1816 and in `attempt-custody.schema.v1.json`. So it is an internal
read-only recovery selector with its own owner, its own SHARED-READ lease rule, and an explicit
prohibition on acquiring the fence.

**How I got it wrong.** I searched `command-inventory.v3.json` and S7's command→lease map, found no such
*command*, and concluded absence. `recover(ExecutionId)` is not a CLI command, so neither source could
ever have contained it. Worse, my one grep that would have found it was truncated with `head -10` and
cut off well before line 1685. **I inferred absence from a truncated search** — an absence claim needs an
exhaustive one. I have since re-run it unbounded; the occurrences above are the complete set.

**Root's diagnosis of the real defect is correct and better than mine.** The entry does not belong in
§5's list as written, but for the opposite reason: §5 says those surfaces "may execute §7's exact
registry/endpoint/node/binding observations **under the fence**", and identity §5 line 1702 forbids this
selector from acquiring the fence at all. The error is one of **scope** — a separately owned, explicitly
fence-free selector mixed into a list of fenced CLI surfaces — not of a missing referent. The fix is to
cite its actual owner and preserve its no-write / no-fence algorithm, not to delete a legitimate
selector, which is what my finding as written would have caused.

C-3 should be read as: *the entry is misplaced because §5's fenced read path contradicts identity §5's
explicit "no fence acquisition" for this selector; correct its scope and citation rather than removing
it.* Its severity stays non-blocking.

---

## 3. What is unchanged

- **Verdict NEEDS-CHANGES stands**, and C-1 and C-2 remain blocking. C-2 — that `trust-doctor` has no
  `defects` parity field and `store-status` has no report channel — is untouched by any of this and I
  re-confirmed it while checking the schema.
- B-1, B-2, B-3 and N-1…N-6 closures are unaffected.
- No pin, limit or probe result changes. Probes S1–S8 stand; S2's observation that the surface model
  carries no defects concept at all is, if anything, reinforced: the model could not have exposed the
  boolean-versus-count distinction either.

## 4. Context root supplied, recorded but not reviewed

`native-creator-adapter-audit-398/NOTES.md` reportedly flags the creator "no network request" wording
against `platform/account.rs`'s explicit OS name-service activity, to be clarified in 399 as application
network versus OS TCB. I did **not** review 398, did not verify that flag, and express no view on it.
It is recorded here only because root supplied it as context for a later owner review. Source397 remains
unselected, and nothing here approves any part of the in-progress 399.

---

Addendum author: Claude Opus 5 (1M context). Read-only; no live, frozen, history, product or lock bytes
edited; no pin edited; no original report or hashes file changed; no commits; no pushes.
