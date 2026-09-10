# Coauthor assessment of root's proposed normative clarification — one correction

**Assessed version:** `CODEX-PROPOSED-NORMATIVE-CLARIFICATION.md`, **3908 bytes**,
`sha256 a3705e7e1cf69301cb0646b919a71eb5da5a6e0d4540648ecf6ede65bbdf2c5e`, read in full.

**Assessed against:** the corrected reference in my disposable work root,
`identity-model.py sha256 de3ae06bac169cf3b41b9cea43c2b0c7113ed2de6b4a3ae164fc8b4d9cc77557`.

I hold no authority to apply this and none is claimed; root owns the wording and its application
after both current passes finish. This file is my assessment, placed beside root's input, which is
preserved unmodified.

## Verdict: accurate except for one clause, which is broader than the reference

I checked each sentence against the actual implementation rather than against my memory of it.
Seventeen of eighteen claims match exactly:

| Proposed claim | Reference |
|---|---|
| governed occurrence = `$ref` to the three defs, **including an intermediate local `$defs` alias**, or an inline pattern **exactly equal** | `governed_form`: `#/$defs/…` only, transitive through aliases, exact `pattern` string equality |
| follow local references, nested `properties`, `items`, `additionalProperties`, `oneOf`/`anyOf`/`allOf` | `walk`, including a `$ref` to a non-scalar container, with a chain guard |
| annotation on the occurrence, its enclosing path, or an intermediate alias applies | `inherited` + the chain's own annotations |
| terminal governed scalar definition is **not** a blanket default | asserted in-suite; still refuses |
| directly annotated properties stay subject to retention and join checks even when not one of the three | the second pass records them with `form: null` |
| every governed occurrence must have an effective annotation | limb `RELATION_DIGEST_UNANNOTATED` |
| an annotated alternative does not cover an unannotated one; a parent may cover each alternative | per-branch paths; parent flows through `inherited` |
| any occurrence lacking an effective annotation makes the location inadmissible; later annotated occurrences cannot undo it | the new monotonic `missing` fact — this is exactly the v10-S1 correction |
| object-key order and visit order must not change admission | measured on both reviewer cases, pre and post |
| no precedence; distinct annotations conflict; **equal under typed canonical equality** do not | `C.equal_typed`, which this correction also adopted for the merge |
| every effective annotation must use the declared retention vocabulary | `RELATION_DIGEST_RETENTION` |
| the same effective annotations govern coverage, retention and join/exemption; none may revert to direct properties | one account, all limbs |
| join fields address top-level selector properties; a scalar alternative preserves the address; an object member, array element or map value does not | `joinable` |
| cannot claim a joinable retention the join vocabulary cannot address | `RELATION_DIGEST_UNJOINABLE_LOCATION` |
| an addressable annotated property requires its join unless it declares the exemption | `RELATION_DIGEST_LAW_RESIDUE` |
| every named join field must exist in the selector | `RELATION_JOIN_FIELD_UNKNOWN` |
| the six listed conditions all refuse at schema-law admission | all six causes exist and are reachable |
| schema coherence here; owning-fact snapshot and retained-byte joins still establish payload truth | unchanged, and the contract already says this |

### The one clause to correct

> "A governed occurrence at one of those nested locations must explicitly declare
> `retention: not-joined` **with its reason**."

**The reference does not enforce "with its reason", and the phrase would also name a key that does
not exist.** Measured on the corrected model: a nested governed occurrence declaring
`retention: not-joined` **admits with a reason, without a reason, and with an empty reason**. And the
one shipped exemption, `vcs-change.previousPath`, carries its explanation under the key `join`, not
`reason` — its annotation keys are exactly `{authority, join, representation, retention}`.

This is not a defect I am proposing to fix: adding a required reason would be a new admission
condition and a new key name, which root's note explicitly rules out ("No additional semantic or
product requirement"). The existing law already asks for the reason as an authoring expectation —
`x-opensip-digest-law.retention.not-joined` says "the reason is stated on the field" and
`residueRule` says "must declare retention not-joined with its reason" — and admission has never
checked it. The clarification should describe that division rather than promote it to a checked
condition, or a reader would implement a check the reference does not have. That is the same class
of mismatch as v9-S1, in the opposite direction.

### Proposed exact replacement for that one sentence

> A governed occurrence at one of those nested locations must explicitly declare
> `retention: not-joined`. As elsewhere in this law, the reason for an exemption is stated on the
> field for a reader; admission checks the declared retention, not the presence or content of that
> prose.

If root would rather make the reason checkable, that is a coherent alternative but a **different**
change: it needs a named key, an admission condition and its own cause, and I have not implemented
one.

## Two notes, neither a change request

- The proposed text says "local references", which is exactly right: the reference resolves only
  `#/$defs/…` and follows nothing external. Worth keeping that word.
- "repeated annotations that are equal under typed canonical equality do not conflict" now matches
  the reference precisely, because this correction replaced the merge's `in` test with
  `C.equal_typed`. Before this delta the two would have diverged on values that are equal
  canonically but not by Python `==` semantics for typed scalars.

## Standing

Root's advisory A3 — missing merge-branch reachability — is addressed by the discriminating checks in
this delta. **A1 and A2 are root's to apply**, and the original advisory severity is root's record to
keep. I assessed the text; I did not accept it, and nothing here infers the independent reviewer's
verdict, which does not yet exist.

---

## Confirmation of the final agreed bytes

**Read:** `CODEX-AGREED-NORMATIVE-INSERT.md`, **2825 bytes**,
`sha256 32db349536ffc74081b5081aa698f9966d100485268fc24822fde2a1a94cd13f`, in full, together with
the note at 3621 bytes `e16c5c84aa277a2e75a01b8e220cdb17996444993c933038a943fab3dd8672c5`.

Two things changed from the version I assessed above, and I checked both against the reference
rather than accepting them on sight:

1. **My replacement for the reason clause is present verbatim** — "must explicitly declare
   `retention: not-joined`. As elsewhere in this law, the reason for an exemption is stated on the
   field for a reader; admission checks the declared retention, not the presence or content of that
   prose." That is what the reference does, and no `reason` key is invented.

2. **Root tightened "Directly annotated properties" to "Directly annotated top-level selector
   properties".** That tightening is **correct and it fixes a real inaccuracy in the version I
   assessed**, which I had passed. Measured on the corrected model: a directly annotated *top-level*
   non-governed property (`$ref: UInt64`, `retention: preimage`, no join) refuses with
   `RELATION_DIGEST_LAW_RESIDUE:file:stray`; the same annotation on a *nested* non-governed member
   produces **no sighting at all** and admits. The direct second pass iterates the selector's own
   `properties` only, so "top-level selector properties" states exactly what the reference does and
   the unqualified phrase would have overstated it. Good catch, and I should have caught it.

**Assessment of the final bytes: they accurately state the corrected reference**, including the
reason clarification. I have no further wording change to propose. I hold no authority to apply
them, I applied nothing, and no acceptance is inferred.
