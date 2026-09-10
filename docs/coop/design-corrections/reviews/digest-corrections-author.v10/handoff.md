# Coauthor handoff — v10 bounded correction: one typed equality rule for annotations

**Author:** actual Claude COAUTHOR session `5dec928a-6357-4726-9ea8-49a3079fb726`, working with root
(Codex). **Not** the independent reviewer.

**Subject:** frozen v11, base manifest
`a03b7fe987ee886101a6d5b85bf4b0760f59b06a5a9e9c5f627accb9a7263bdf`.

**Source root:** `/tmp/opensip-design-corrections/digest-corrections-author.v10/work` — a disposable
exact copy of frozen v11 (2786 files, all hash-identical at start).

## Standing

Schema and reference-model evidence only. **No acceptance, no readiness, no product qualification,
no runtime security claim, no implementation authority**, none claimed and none was granted. This is
a hypothetical schema/reference correction, not a current payload or Run attack.

The independent actual Claude reviewer `cd236691-03ef-4863-b612-e7d8cdf0d3ad` **is still reviewing
v11 and its final severity and verdict do not exist yet**. I am not that reviewer, I do not speak for
it, and nothing here should be read as its result. I read only the p10 source and result root routed
to me; I re-verified the reviewer's directory is still being written by the reviewer (files newer
than my session start, e.g. `probes/p13_insert_custody.py`) and I wrote nothing in it.

## What changed — exactly two files

| Path (relative to source root) | frozen v11 sha256 | delivered sha256 |
|---|---|---|
| `docs/coop/design-corrections/foundation/identity-model.py` | `de3ae06bac169cf3b41b9cea43c2b0c7113ed2de6b4a3ae164fc8b4d9cc77557` | `ed38f172291a30c590e6a424794f345802892c27e455ff682df7e8f5599a0fcd` |
| `docs/coop/design-corrections/foundation/check-identity.py` | `90a3b590eec305ad72b839e2135fe46de7a6789e3f7218cf20ddc108a35993c8` | `f9b427a8671da7dcf761ad0de7037334c30cac1128bc457661de13b6648f21f5` |

**Whole-tree sweep** (`runs/work-vs-frozen-v11.json`): frozen 2786 files, work 2786 files, changed =
exactly the two rows above, **0 missing, 0 extra**. Exact PRE bytes retained at
`PRE-identity-model.py` / `PRE-check-identity.py`, which hash to the frozen v11 values.

**Nothing else was written.** The live repository
`/Users/sb/code/opensip-ai/opensip_arch` still carries the frozen v11 bytes at both owned paths, and
exactly one file under it changed during my session window —
`docs/coop/design-corrections/reviews/NEXT-REVIEW.md`, which is root's, not mine. No frozen snapshot
and no reviewer directory was written. The captured reviewer inputs still hash to their recorded
values (`p10_typed_equality.py` `9d4dc735…`, `p10-typed-equality.json` `24885358…`), as does root's
prepared recheck script (`47e2cfe7…`).

## The defect, stated precisely

The contract's rule is that repeated effective annotations conflict unless they are equal under
**typed canonical equality**. The conflict limb had always used `C.equal_typed`. Collection and alias
inheritance had not: they used Python membership (`not in inherited`, and `[a for a in on_chain if a
not in inherited]`). Python `==` is not that rule — `1 == True` is true, while `C({…ordinal: 1})` and
`C({…ordinal: true})` are **different registered bytes**.

So a typed-**distinct** annotation was dropped during collection and the conflict check never saw the
pair. Measured on frozen v11, the reviewer's shape (`ordinal=1` on the property, `ordinal=true` on
the intermediate alias) **admits in both orientations with one surviving annotation**:

| Vector | frozen v11 | corrected | surviving annotations v11 → corrected |
|---|---|---|---|
| `intOnProperty_boolOnAlias` | ADMIT | `RELATION_DIGEST_ANNOTATION_CONFLICT` | 1 (`1/int`) → 2 (`1/int`, `True/bool`) |
| `boolOnProperty_intOnAlias` | ADMIT | `RELATION_DIGEST_ANNOTATION_CONFLICT` | 1 (`True/bool`) → 2 (`True/bool`, `1/int`) |
| `controlDisagreeingPair` (ordinary strings) | CONFLICT | CONFLICT (unchanged) | 2 → 2 |
| `controlIdenticalPair` | ADMIT | ADMIT (unchanged) | 1 → 1 |

`pythonEqual: true`, `equalTyped: false`, `annotationCanonicalDistinct: true` — the two documents are
genuinely different bytes, so admitting both was the model disagreeing with its own law.

## The correction — one rule, routed through one primitive

I audited **every** annotation comparison in `identity-model.py` rather than patching the reviewer's
orientation. There were exactly two Python-equality sites, both in early collection. All comparison
sites now route through a single module-level helper (`identity-model.py:284`), which uses the
**existing** canonical primitive `C.equal_typed` — no new coercion, no weakening of the normative
text, no schema, contract or registry edit:

```python
def annotation_already_collected(annotation,collected):
    return any(C.equal_typed(annotation,other) for other in collected)
```

Call sites, all four stages:

| Line | Stage | Was |
|---|---|---|
| `identity-model.py:376` | alias / parent / container inheritance into `inherited` | `not in inherited` |
| `identity-model.py:381` | `$ref`-chain contribution filtered against `inherited` | `a not in inherited` |
| `identity-model.py:364` | same-path merge in `record()` | already `C.equal_typed`; now folds the incoming list through the same rule even with no previous sighting |
| `identity-model.py:486` | the conflict limb's distinct-annotation list | already `C.equal_typed` |

`governed_form` performs no annotation comparison (it concatenates), so there is no fifth site.

## Evidence

### 1. Root's own prepared recheck, adapted and passing — 35/35

Root's `recheck-annotation-typed-equality-final-v12.py` (4193 bytes, `47e2cfe7…`) was **not executed
as written**: it writes into a repository `reviews/` path, asserts `not out.exists()`, and reads a
`handoff.json`/`custody.json` that only exist after root retains this delta. Running it would have
written outside my ownership and burned root's one-shot output directory. I ran a **labelled
adaptation** (`probes/adapted-codex-v12-typed-equality-recheck.v1.py`) that keeps root's pair table,
five document shapes, metaschema check, two-image comparison and pass rule byte-for-byte, and changes
only the roots and the output path.

```
35 typed annotation cases pass across five collection/inheritance/merge locations;
9 refusals discriminate frozen v11 from final source.
discriminating shapes  : ['enclosing-container', 'parent-nullable-branch', 'property-alias']
already correct on v11 : ['alias-chain', 'same-path-merge']
```

**Root's stated prediction is confirmed exactly:** the same-path merge control already behaved
correctly on frozen v11, and the early-collection negatives discriminate. All 7 pairs × 5 shapes pass
— the three typed-distinct pairs refuse with `RELATION_DIGEST_ANNOTATION_CONFLICT` in both
orientations, the three same-value positive controls (`same-integer`, `same-boolean`, `same-nested`)
admit, and the ordinary string conflict refuses.

### 2. Nothing else moved

`probes/result-prior-classes-pre-vs-post.v1.json`: every prior counterexample class measured on both
images, `classesDifferingBetweenTheImages: []`. The 39 prior injections still all refuse; the nine
inherited-limb vectors are identical; all three law limbs, monotonic missingness, top-level join
addressing, the terminal no-default rule and the `vcs-change.previousPath` exemption are unchanged.

### 3. In-suite discriminating matrix

`check-identity.py` now carries **six** propagation classes × five typed pairs (`int/true`,
`int/false`, nested dict, nested list, deep nested) × two orientations = **60 negatives**, each
asserting `RELATION_DIGEST_ANNOTATION_CONFLICT:file:`; **30 identical-annotation positive controls**
that must still admit; a check that both annotations survive collection at every location; a check
that the equality rule is typed-canonical and not Python equality; and an ordinary disagreeing-string
conflict control.

### 4. Suites

| Suite | Result |
|---|---|
| `check-identity` | **767 / 767**, 0 failed (was 673 at v11 freeze) |
| `check-foundation` | 231 / 231 |
| `check-array-orders` | 65 / 65 |
| `check-product-configuration` | 28 / 28 |
| `check-product-quality` | 24 / 24 |
| `check_workflows.v1` | 1290 / 1290 |
| `check_native_evidence.v2` | 151 / 151, matrix cells 60, open objects 0 |
| `check-security-lifecycle.v1` | 456 / 456 |
| `check-integration` | 363 / 363 |

All runs used `/tmp/opensip-architecture-review-env/bin/python -I -B`.

**Labelled adaptation for the three pin-bearing suites.** Root's recording error (the v10 crosswalk
bytes named by the frozen security and workflows pins) makes those launchers fail on an unmodified
copy. As instructed I did **not** fix the pins in my work root and did **not** regenerate work-root
pins or reports. Native, security and integration were therefore run in a **separate disposable
sandbox** — a throwaway copy of the work tree with pins regenerated inside it — which was deleted
after the run. That sandbox is why those three results are trustworthy as suite results but are not
evidence about pin content. My delta contains no pin or report change.

## Honest record of what I got wrong

**My own five-location probe mislabelled a class and I over-claimed coverage.**
`probe-five-locations-pre-vs-post.v1.py` reported `enclosing-container` as non-discriminating. What it
actually built under that name was a `$ref` container with a sibling `properties` overlay — two
separate arrivals at the same path, i.e. a second same-path merge. It never put an annotation on the
container itself, so it never touched the `inherited` filter. Root's shape does, and that class
**does** discriminate. The correction already covered it; only my coverage claim was wrong. The probe
and its result are retained unmodified with a superseding note
(`probes/CORRECTION-five-locations-enclosing-container-mislabel.md`), and `check-identity.py` now
carries both shapes under accurate names (`enclosing-container`, `container-ref-overlay`) — that is
the 752 → 767 change.

This is the fifth time root's control matrix has caught a class mine missed (container-ref,
branch-order, alias-location, inherited-limb, enclosing-container). I am recording that rather than
presenting my matrices as adequate.

**Carried forward from earlier sessions, still present in the frozen bytes:** the doubled anchor
comment in `check-identity.py` introduced by my v7 edit. I deliberately did **not** tidy it, here or
in v9, because silently changing frozen bytes would put an unrequested change into root's delta. It
is mine, it is cosmetic, and it is root's call.

## Interface note for root's v12 recheck

`recheck-annotation-typed-equality-final-v12.py` asserts, before running:

- `docs/coop/design-corrections/reviews/digest-corrections-author.v10/handoff.json` exists and each
  `ownedFilesChanged` row's `sha256` matches the file at the repository root. The rows in the shipped
  `handoff.json` are exactly the two paths and hashes tabled above, in that field shape.
- `docs/coop/design-corrections/reviews/digest-corrections-author.v10/custody.json` exists. **I did
  not author one** — custody of the retention is root's record, and fabricating it would be me
  writing root's provenance. Root will need to place it, as in v9.
- The output directory must not already exist; my adapted run wrote only into my own `probes/`, so
  root's one-shot directory is untouched.

## Limitations

- Reference-model and schema evidence only. Nothing here establishes payload truth, which still rests
  on the owning fact's snapshot inventory and retained source bytes.
- The typed pairs are Python-equal / typed-distinct scalars and their nestings. I did not enumerate
  every possible canonically-distinct-but-`==`-equal value; the correction is structural (one rule at
  every site) rather than a value enumeration, which is why the six-class matrix matters more than
  the pair list.
- I did not re-review the completed independent review, and no verdict of the in-flight v11 review is
  inferred or implied.
- Root's pin/recording error is untouched by design; the two stale entries among 1308 remain in my
  work root exactly as frozen.
- I read `CODEX-PUBLIC-NOTE.md` in full before this handoff: **1778 bytes**, `sha256
  f56a42c9a8806c277b123e72836bfb1697cb234404dadc0e16447efc91744916` — unchanged from my earlier read
  this session.

## Next steps, all root's

Retain and apply the two-file delta, place `custody.json`, run the prepared v12 recheck plus the five
previous final rechecks against the applied source, correct the crosswalk/pin ordering, and re-freeze.
No readiness, acceptance or implementation authority is claimed by this handoff.
