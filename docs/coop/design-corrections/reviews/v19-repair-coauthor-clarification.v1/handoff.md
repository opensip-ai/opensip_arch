# v19 repair coauthor — clarification: one-sentence scope refinement

Source coauthorship, not fresh independent acceptance. Continues
`v19-repair-coauthor.v1`; that handoff's findings stand and its deliverables are
untouched (all eight verified by hash below).

## Assessment: agree, and the defect is a conformance risk

Assessed independently against what the frozen model emits. Two things go wrong in the
published clause, not one.

**1. Scope binding.** The relative clause — "which names that requirement's `relation`,
`minResolution`, evidence plane and exact `deficiency`" — attached to *the remedy* after
*the remedy* had just been introduced as the discriminator for **both** routes. Bound
there, it requires every remedy carrying this code, including the retention entry's, to
name the four fields. The observed retention remedy is `restore or regenerate the Run
evidence; assurance must be replayable`, which names none of them. So the sentence
admitted a reading under which the frozen model is **non-conforming with its own
contract**. That is why this is worth fixing, not a matter of taste.

**2. Dangling referent.** "That requirement's" has no antecedent on the retention route.
Control C4 fires that entry with *every* requirement satisfied, so there is no
requirement to refer to. Under the bad reading the clause is not merely false but
unsatisfiable.

**Why it survived the first pass:** the sentence was written to defend the shared-code
claim — one code on two routes is still discriminable — and it compressed the
discriminator and the field list into a single clause. The compression created the
ambiguity.

**One thing I deliberately did not do.** The refinement does not pin the retention
entry's literal string. `remedy` is `BoundedText` free text (maxLength 1024); the
contract now says what that remedy is *about* (Run-level restoration) and does not
mandate fixture wording. Pinning the string would have been a second, unrequested
normative change.

The load-bearing claims are all preserved: one code, two routes in preview; the two are
told apart by the remedy; the per-requirement entry's remedy names the four fields. Only
the attribution of the field list is made specific.

## The change

Before:

> …and this per-requirement insufficiency, **and the two are told apart by the remedy,
> which names that requirement's `relation`, `minResolution`, evidence plane and exact
> `deficiency`.**

After:

> …and this per-requirement insufficiency, **and the remedy is what tells them apart: the
> retention entry's remedy names the Run-level restoration that route needs, while the
> per-requirement entry's remedy names that requirement's `relation`, `minResolution`,
> evidence plane and exact `deficiency`.**

One contiguous hunk (`641,643c641,644`); every other byte identical. Against frozen18 the
result is still a **pure insertion** (`634a635,650`) — no pre-existing frozen byte is
changed, removed or reordered. +113 bytes; max refined line width 81. `refine.py` asserts
`after == before[:i] + NEW + before[i+len(OLD):]`, `after.replace(NEW, OLD) == before`,
and that the three neighbouring untouched passages occur exactly once in both.

## SHA binding

| | sha256 |
|---|---|
| frozen18 contract | `a6e34134d73495a5ce32502173daf452bbc7b207c25e83f78c4571ef609bad29` |
| **before** (`v19-repair-coauthor.v1/workflow.proposed.md`) | `b3a3bf65ca0cd1bd00654e6dfc0f4f0a9814da96b59aca4e51bf318828721477` |
| **after** (`workflow.proposed.md`) | **`8d4d9c892c34ec991c8dd2ffc86946d267adc90adbc506422fbe3f01ccf66b1d`** |
| `refine.py` | see `handoff.json` |

## Evidence

No probe rerun and no environment created here — root is rerunning the exact existing
probe under pinned Python 3.12. Values cited are the already-observed ones from
`probe_repair_unmet_mapping.v1.json`
(`29d8711b023fd512abda448f78eb782d31b3ddecfb541ec2c3f845c6ec82d460`):

- **C1** per-requirement remedy: `evidence requirement unsatisfied:
  references@resolved-binding (native: resolution-incomplete)` — names all four fields.
- **C4** retention remedy: `restore or regenerate the Run evidence; assurance must be
  replayable` — names none, and fires with all requirements satisfied.
- **C5** both routes at once: 2 entries, same code, 2 distinct remedies — the case the
  refined sentence now describes correctly.

The refinement changes **no probe expectation**: the probe asserts observed remedies, not
contract prose, so the pinned-3.12 rerun is unaffected by this edit.

## Unchanged

Prior deliverables verified byte-identical: `workflow.before.md` `a6e34134…bad29`,
`workflow.proposed.md` `b3a3bf65…1477`, `handoff.json` `8cbd5754…4d7c`, `handoff.md`
`b024a54d…deb0`, `probe_repair_unmet_mapping.v1.py` `7e543dfe…4e87`,
`probe_repair_unmet_mapping.v1.json` `29d8711b…2d460`, `integrate.py` `3a646943…5dfa0`,
`probe-attempts.md` `4a8ff2af…351ad`. (The one file with a newer mtime in that directory
is the harness-written `response.json` of that session — not a deliverable, not touched
by me.)

0 files modified under `candidate-subject.v18`. No model, schema, case, registry or
history changed; no new code minted. Did not read or edit `v19-native-coauthor.v1`; no
broad scans, no new environment, no tests.

**changesRequired: none.**

**Residual for reviewers:** the prior handoff's three findings stand as written —
including the explicit statement that this correction **widens** the published meaning of
`REPAIR.EVIDENCE_RUN_UNAVAILABLE` rather than merely restating it. This refinement
narrows one sentence's scope and adds no new normative claim.
