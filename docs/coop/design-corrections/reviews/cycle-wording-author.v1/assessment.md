# Coauthor assessment — v11-A3 cycle-termination wording

**Author:** actual Claude COAUTHOR session `5dec928a-6357-4726-9ea8-49a3079fb726`, working with root
(Codex). **Not** the independent reviewer.

**Scope:** a bounded normative *wording* assessment. It is not a review, not a readiness act, not an
acceptance, and it authorises no implementation. No source, schema, registry, model or checker was
edited; nothing outside `/tmp/opensip-design-corrections/cycle-wording-author.v1` was written.

**Standing of the in-flight review:** the independent v11 review is still finalizing. I read its
**currently authored** `review.json` findings and advisories as they stand, not a presumed final
verdict, and I claim no outcome for it.

---

## 1. The exact bytes assessed

| Item | Value |
|---|---|
| Proposal file | `/tmp/opensip-design-corrections/cycle-wording-author.v1/CODEX-PROPOSED-INSERT.md` |
| File bytes | **52** (51-byte sentence + trailing newline), read in full |
| File sha256 | `685e92b728c161ffa0f4c2eea400880b98c410e8b2eccc5730da92e8522da885` |
| Sentence sha256 (51 bytes, no newline) | `beedf8bd5006a5d52ba2704af6e7afcaabfefa2eae78efc4ebd6f851f20f4cc0` |
| Sentence | `Local-reference traversal must terminate on cycles.` |

I read the whole file. **I claim agreement only about these 52 bytes**, and about nothing I have not
read.

### Target and placement

| Item | Value |
|---|---|
| File | `docs/v2/contracts/product-v1/identity-and-evidence.md` |
| Bytes / sha256 | 83004 / `1dd7ebce1359a7376b1bd05c04363d27372c07e109b5fbdc2580fbc91a6adfc9` |
| Live vs frozen v11 | **byte-identical** (same sha256) |
| Anchor `these occurrences.` | line **582**, and it occurs **exactly once** in the file — the placement is unambiguous |
| Paragraph | lines 577–586, beginning "The relation document's annotation law also governs schema structure." |

### Sources the sentence is assessed against

| Source | sha256 |
|---|---|
| released `identity-model.py` (repo `reviews/digest-corrections-author.v10/author-source/…`) | `ed38f172291a30c590e6a424794f345802892c27e455ff682df7e8f5599a0fcd` |
| same bytes loaded from my retained v10 work tree | `ed38f172…` — **byte-identical**, verified in the probe |
| released `check-identity.py` | `f9b427a8671da7dcf761ad0de7037334c30cac1128bc457661de13b6648f21f5` |
| frozen v11 manifest | `a03b7fe987ee886101a6d5b85bf4b0760f59b06a5a9e9c5f627accb9a7263bdf` |

Root has since applied the v10 delta to the live tree: `docs/coop/design-corrections/foundation/`
now carries `ed38f172…` and `f9b427a8…`. **The two chain guards assessed below are therefore also the
live ones**, not only the retained release copy's. I wrote nothing there; the repository changes in
this window are root's application and retention.

The repository's retained release copy has no sibling `canonical.py` or schema JSON, so it cannot be
imported where it sits. Rather than copy anything into place I loaded the **same bytes** from my
retained v10 work tree, which carries the correct frozen-v11 neighbours, and hashed both paths to
show they agree. Nothing was written to either tree; `-B` kept bytecode out of both.

---

## 2. Verdict: **agrees — the sentence is accurate, adds nothing, and belongs there**

The sentence states a property the released reference actually has, by two explicit guards, and it
introduces no admission verdict, no evaluation strategy and no schema feature.

**The two chain guards it describes** (released `identity-model.py`):

| Guard | Line | Code | Reached by |
|---|---|---|---|
| `governed_form`'s alias-chain guard | 337–338 | `if target in defs and target not in chain: form,inherited=governed_form(defs[target],chain+(target,))` | an alias-only cycle, where the resolver would otherwise recurse forever looking for a governed form |
| `walk`'s container-`$ref` guard | 389–390 | `if target in defs and target not in chain: walk(defs[target],path,inherited,field,joinable,chain+(target,))` | a cyclic container `$def` |

Both are *path*-scoped: `chain` accumulates along one descent (and is passed through `properties`,
`items` and branch recursion unchanged), so a definition already open on the current path is not
re-entered, while the same definition reached by a *different* path still is.

### Measured controls

`probes/cycle-termination.v1.py` → `probes/result-cycle-termination.v1.json`, run with
`/tmp/opensip-architecture-review-env/bin/python -I -B`, recursion limit 1000:

| Case | Verdict | Elapsed | Sightings |
|---|---|---|---|
| **cycle negative** — self-cycle `$def`, unannotated governed leaf | `RELATION_DIGEST_UNANNOTATED` | 0.46 ms | `file.probe.leaf` |
| **annotated positive control** — same cycle, leaf annotated | `ADMIT` | 0.40 ms | `file.probe.leaf` |
| mutual cycle `CycleB→CycleC→CycleB`, unannotated leaf | `RELATION_DIGEST_UNANNOTATED` | 0.39 ms | `file.probe.down.leaf` |
| mutual cycle, annotated leaf | `ADMIT` | 0.45 ms | `file.probe.down.leaf` |
| alias-only cycle `AliasP→AliasQ→AliasP`, no governed leaf | `ADMIT` | 0.37 ms | none |
| shared alias reached at **two** paths, unannotated | `RELATION_DIGEST_UNANNOTATED` | 0.37 ms | `file.probeOne.leaf`, `file.probeTwo.leaf` |
| cycle visited **before** an unannotated governed sibling | `RELATION_DIGEST_UNANNOTATED` | 0.43 ms | `file.probeCycle.leaf`, `file.probeSibling` |

`terminationObserved: true` (no `RecursionError`, every case sub-millisecond),
`guardIsPerPathNotGlobal: true`, `cycleDoesNotStopTheTraversal: true`.

### What this establishes about the three things the sentence must not do

- **No new admission verdict.** A cycle is not itself a refusal cause: the annotated cycle admits,
  and the alias-only cycle admits with no sighting at all. The negatives refuse for the *ordinary*
  reason (`RELATION_DIGEST_UNANNOTATED`), exactly as the same leaf would outside a cycle.
- **No evaluation strategy imposed.** The sentence states a property, not a mechanism. Any
  terminating discipline that still visits each occurrence reaches these same seven verdicts.
- **No recursive-schema feature promised.** I enumerated the `$defs` reference graph of the
  registered relation document: **20 definitions, zero cycles.** The sentence therefore changes
  nothing about the admitted corpus; it is a robustness requirement for a blind implementer facing a
  document that could contain one, which is exactly how the reviewer framed A3.

---

## 3. One non-blocking refinement, and why I still say "agrees"

The exact sentence is safe **in its context**. Read alone it carries two misreadings, and I measured
that both would change verdicts — which is why it is worth thirty extra bytes:

1. **"terminate *on* cycles" can be read as "stop when a cycle is found."** An implementer who
   aborted the traversal at the cycle would never reach `file.probeSibling` in the last case above,
   and would **ADMIT** where the reference **refuses** `RELATION_DIGEST_UNANNOTATED`.
2. **"just make it terminate" invites a global visited-set.** Marking definitions globally visited
   would produce **one** sighting for the shared alias instead of the measured **two**, so a document
   unannotated only at the second path would **ADMIT** where the reference refuses.

Both misreadings are contradicted two paragraphs later by "Every governed occurrence must have an
effective annotation" and "the order in which these paths are visited must not change admission"
(lines 588–593), which I re-read for this purpose. The contradiction is real but it is at a distance,
and a blind implementer reads forward. So: **the wording does not need correction to be correct**,
and I would rather it were unambiguous on its own line.

**Proposed alternative (root's call, not a condition):**

> `Following local references must terminate even when a local definition is cyclic.`

81 bytes, sha256 `7375c21035ed4c3f0aba9c229a702249422d73dd76365ad8bcc1f5099cef10da`.

It is still termination-only: no verdict, no strategy, no feature. "Following local references" also
picks up the verb of the preceding sentence ("Follow local references, nested `properties`, …"), so
it reads as a constraint on the traversal just prescribed. If root wants the occurrence-completeness
point stated explicitly rather than inherited from the later paragraph, the belt-and-braces form
would be "… cyclic, and no occurrence may be skipped to achieve it" — but that edges toward
prescribing a strategy, so I do **not** propose it.

### Mechanical note: the insertion needs a re-wrap

The paragraph is hard-wrapped at 70–84 columns. Inserting the sentence in place makes line 582 **130
characters**. Exact drop-in replacements, both verified against the live bytes:

- **Root's exact sentence** — replace lines **582–584** (232 bytes, sha256 `72fae25a…`) with this
  284-byte block, sha256 `9ca24f991008d5c96f8c4b060eea1927deae1ea03a560cd54b424c0fd4b3ba34`:

```
these occurrences. Local-reference traversal must terminate on cycles. An
annotation on the occurrence, its enclosing schema path, or an intermediate
alias applies to that occurrence. An annotation on the terminal governed
scalar definition does **not** provide a blanket default for
```

- **Refined sentence** — replace lines **582–586** (409 bytes, sha256 `c6c61d28…`) with this 491-byte
  block, sha256 `79c9484979ddd1534bd26a1d77b374c5e91b5eb12e9f2751d07feab6532ed315`:

```
these occurrences. Following local references must terminate even when a local
definition is cyclic. An annotation on the occurrence, its enclosing schema
path, or an intermediate alias applies to that occurrence. An annotation on
the terminal governed scalar definition does **not** provide a blanket default
for all references to that type. Directly annotated top-level selector
properties remain subject to retention and join checks even when their scalar
form is not one of these three.
```

Note the second block also re-wraps the pre-existing **105-character** line 585 (a leftover of the
v11 "top-level selector" tightening). That is a byte change root did not ask for; I flag it rather
than fold it in silently, and root may prefer to keep 585 as it is.

---

## 4. Assessment of the two required recording issues

Both are **root's**, and both match what I independently ran into.

**v11-M1 — stale pins (MUST).** Accurate as stated, including its bounded scope. Independently, in my
v10 pass I found the same thing from the other side: the security and workflows launchers exit 1 on an
unmodified copy of frozen v11, which is why I ran those suites in a separate disposable sandbox with
pins regenerated inside it and deleted it afterwards, leaving my delta free of any pin or report
change. My own audit agreed with the reviewer's count — **exactly 2 stale entries among 1308**. The
reviewer's root cause is the sharp part: `finish-v11-records.py` mutates
`correction-crosswalk.proposed.json` *after* the pin refresh and after the six commands, and its
`assert report['passed']` reads the pre-mutation report, so the guard is self-satisfying. The fix is
a fixpoint, not a hex edit: refresh pins and re-run the commands **after** the last record-writing
mutation, and re-seal. Record ordering and the final pin seal are root's.

**v11-S1 — pending-version field (SHOULD).** Accurate. One thing worth pinning down, because it is the
exact shape of the recurring slip: the reviewer says the frozen-v11 field *should have read*
`PENDING-FROZEN-V11`, and that is right **about v11**. But the field root is about to write lives in
the **successor**, so applying the reviewer's literal string would reproduce the defect one version
on — which is precisely how frozen v8 came to carry `PENDING-FROZEN-V7`. Root's stated successor
value, **`PENDING-FROZEN-V12`**, is the correct one for the v12 tree. The durable form of the rule is
that the field is `PENDING-FROZEN-<the version being frozen>` and must therefore be **derived at
freeze time from the version being frozen**, not carried forward by hand — which puts it under the
same post-mutation reconciliation v11-M1 already requires. Root owns it.

## 5. Assessment of the three advisories

**v11-A1 — typed equality.** This is my retained two-file v10 correction, and I record it at **the
reviewer's severity: ADVISORY, non-blocking**, with the reviewer's three bounds intact — unreachable
in the registered documents (no numeric or boolean annotation scalar exists today), order-independence
is unaffected either way, and reaching it needs a future registered-schema edit. **I do not upgrade
it.** My v10 handoff described measured behaviour, not severity; severity is the reviewer's to set,
and nothing in my delta changes it. What the correction does is make the implemented notion match the
notion the contract prose already promises, at every comparison site rather than one.

**v11-A2 — duplicate check ids.** Accepted as the reviewer states it, and I agree with root's framing:
account it as **call counts vs unique ids**, with no silent historical cleanup and no claim that any
failure was masked. On frozen v11 the reviewer measured 673 reported / 663 distinct, from two ids
(`closed-closure`, `exact-version-closure`) at six instances each. My v10 delta touched neither id and
added parameterised ids that are unique per (location, pair, orientation), so on the released
`check-identity.py` the reported total is 767 with the same 2 duplicated ids and the same 10 extra
instances. **That last figure is a derivation, not a re-measurement** — the prompt asked me not to
re-run suites, so I did not, and the authoritative distinct-id count on the released file is root's or
the reviewer's to take.

**v11-A3 — this assessment.** Agreed and substantiated above.

---

## 6. Bounds and limitations

- Wording and reference-model measurement only. Nothing here establishes payload truth, and no
  admitted document changes: the registered relation document has **zero** `$defs` cycles.
- Termination is measured on **seven** bounded cases plus the reviewer's own `cyclic-container-ref`
  fixture already in the suite. It is not a proof. The argument that it generalises is that `chain`
  grows by one distinct definition per `$ref` hop out of a finite `$defs`, and non-`$ref` recursion is
  bounded by the finite document — but that is reasoning, not measurement.
- **A real bound the sentence does not mention, and I am not proposing it should:** because the guard
  is per-path rather than global, termination does not imply *bounded work*. A document whose local
  definitions form a dense reference graph can cost time exponential in the number of definitions
  while still terminating. Today's document (20 definitions, acyclic) is nowhere near that, and
  stating a complexity bound would be a new requirement, not a clarification of an existing one. Root
  should know it exists.
- I did not re-run any suite, did not re-derive the v11 review, and did not read the reviewer's final
  verdict, which does not exist yet.
- I read the whole 52-byte proposal. I claim no agreement about any wording I have not read.

## 7. Claims explicitly not made

No acceptance, no readiness change, no product qualification, no implementation authority, no
independent-review verdict, and no statement about the in-flight v11 review's outcome. All existing
correction and review history remains immutable and untouched.
