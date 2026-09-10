# v14 advisory clarification — coauthor technical assessment

**`technicalAssent: false`** — because one of the two proposals is wrong as written.

| change | assent |
|---|---|
| **V14-ADV-2** (`relation-payload-schemas.v2.json`, `anchorLaw.enforcedAt`) | **yes, exactly as proposed** |
| **V14-ADV-1** (`native-evidence.md` §10 sentence) | **no** — substance right, cross-reference wrong; precise alternative supplied |

`proposalSha256 = 48c3ddd9c65be2d3832e221197dfdd7355a5782d0cf2564ba43a693cb7b6c15f`
`reviewSha256 = 857b2e3a1342c79146bf09f4c598fcd31d26995e16b96b0faa3c4deab8bd84a1`

Both advisories keep the severity the independent review gave them. Nothing here
is raised to a MUST or a SHOULD, and nothing is closed. This is a coauthor
technical assessment — not design acceptance, not independent review, not blind
reconstruction, not application acceptance.

## Hashes — all correct

Every declared hash recomputed from the actual bytes; the live repository equals
`before` for both files; each `old` occurs **exactly once**; applying `old → new`
mechanically reproduces the `proposed` bytes **byte for byte**; each change is a
single hunk.

| id | before | proposed | live == before |
|---|---|---|---|
| V14-ADV-1 | `55dec8bf…` | `f36942b5…` | yes |
| V14-ADV-2 | `629c2868…` | `ef0c244e…` | yes |

V14-ADV-1's `before` is the **integrated v4** byte, not the v14 reviewed byte
(`20b4cc04…`). I checked the advisory transfers cleanly: both statements sit at
the same lines (2267 and 2376) and in the same section in both files.

---

## V14-ADV-1 — the advisory is real; the proposed wording is not

**The advisory is right**, verified against the owning law rather than accepted
from the review. §10's paragraph is entirely about how a *lawful* entry's
deficiency and cause reach the public surface — the deficiency projects as an
existing closed `DomainDetailCode`, the cause travels as typed detail in the
`coverage2` record — and for **that route** no code is added. The sentence "No
new public code is added and none is needed" carries no scope in its own text,
while four members are added ~109 lines later for **refusal** branches, one of
them (`native.coverage-cause-unsupported`) named for the very Coverage-cause
route the paragraph discusses. Scoping the sentence is correct and adds no
behaviour.

**The proposed replacement says "The refusal branches in section 13".** That is
false, and measurably so in *both* files:

- unqualified sentence — line **2267**, inside `## 10. Deficiencies, precedence and D9 mapping` (2140–2537)
- four-codes paragraph — line **2376**, inside **the same section 10**
- `## 13. Joins (closed; current spellings, no future owner choices)` begins at line **2750** and contains **no occurrence of `DomainDetailCode`**

The public detail registry corroborates independently: the `selector` on all four
added records names **"native-evidence.md section 10"**, never section 13. A
reader following the new cross-reference would be sent to the joins section and
find nothing.

This is not root's invention — the independent review's own V14-ADV-1 text says
"section 13 of the same document adds four DomainDetailCode members" while its
*own selector* cites lines 2376–2385, which are section 10. The proposal
faithfully carried that forward. The review's verdict, severity and measured
evidence (registry 283 → 287, 0 removed) are unaffected; only the section label
is wrong. But integrating the string would write a false cross-reference into
normative prose — the same staleness class both advisories exist to remove.

**Precise alternative** (`706b7e0fc94bb1467e33c9f75d5406046e32ab9859f57f08a1f6642dfbdc7d46`,
full file at `claude-alternative/docs/v2/contracts/product-v1/native-evidence.md`).
Four words differ from root's:

> `nativeCause`-carried rows. No new public code is added for this projection of
> a lawful entry's deficiency and cause. The refusal branches **later in this
> section** separately add four public detail codes; those additions do not
> change this projection.

True of the current bytes, still true under renumbering, and it still gives the
reader a direction. Naming the intervening sub-heading would be more precise, but
that heading reads "Admission and event routes (existing; unchanged rows)", which
would import a second inaccuracy into the fix. Root's first sentence and closing
clause are accurate and I assent to both.

## V14-ADV-2 — assent, exactly as proposed

Every factual claim in the new text checks out at the call sites:

- **`anchor_law` has exactly one call site.** Defined at `identity-model.py:840`,
  called at `:939`; the only other occurrence (`:1081`) is a comment. That call is
  inside `relation_payload_rules` (`:923`), whose only call site is `:755` —
  inside `open_run_closure` (`:566`). `close_run` (`:561`) delegates to it, and
  `admit_cache_entry` (`:1484`) reaches it too. The reference model exhibits this
  law at retained Run closure and nowhere else.
- **No producer-boundary call site exists, and none could be named.** The native
  model defines no fact-anchor cardinality guard at all. This decides the choice
  of repair: the review offered "narrow `enforcedAt` **or** name the
  producer-boundary call site the way the cause registry names
  `admit_coverage_result_v3`" — the second option is unavailable, because there is
  no such function. The asymmetry the review cites is real:
  `admit_coverage_result_v3` does exist and the cause registry does name it
  alongside `close_run`.
- **The ordering clause is true.** `anchor_law` runs at `:939`, before
  `relation_source_joins` — "the per-relation snapshot-join registry, enforced on
  EVERY owning fact" (`:1003`, called `:957`). Re-scoping it to "At retained Run
  closure" is accurate.

**It does not weaken producer obligation — it strengthens the statement of it.**
The before text asserted as *fact* that the law "is checked … at the producer
boundary", which the reference model does not exhibit. The new text makes it an
explicit obligation — "The producer **must** enforce this law on every owning
fact" — and keeps "on every owning fact" attached to the obligation rather than
to the model exhibit. An obligation that is stated and unmet is a conformance
failure with a sentence to cite; before, a reader could believe the reference
model already discharged it.

It invents no producer implementation (it names no function, call site or
boundary), adds no field, code or test, and alters no admission semantics.
`enforcedAt` is a prose value; **no checker asserts on its text** — the only live
occurrences of the old sentence outside retained review archives are the file
itself.

## One consequence root must handle

`relation-payload-schemas.v2.json` is **not merely prose-bearing**:
`identity-model` joins this document **by digest** at admission and refuses
`PAYLOAD_SCHEMA_NOT_THE_REGISTERED_DOCUMENT` on a mismatch. The change moves the
document digest `629c2868… → ef0c244e…`.

Nothing in the fixtures breaks: `check-identity` computes
`RELATION_DOCUMENT_DIGEST` from the file bytes rather than hardcoding it, so the
reference cases follow the new bytes, and no retained fixture, generated report or
checker carries the old digest as a literal. But **four live pin manifests do** —
`foundation/`, `workflows/`, `native/` and `security/source-pins` — and must be
re-sealed at the successor freeze. That is ordinary freeze work and root's own; I
changed nothing and re-pinned nothing.

## Required follow-up

1. **Blocking.** Do not integrate the V14-ADV-1 proposed bytes (`f36942b5…`). Use
   the supplied alternative (`706b7e0f…`), or any wording that does not send the
   reader to section 13.
2. Non-blocking. Record — **without editing the frozen review artifact** — that
   `post-reset-review.v14` V14-ADV-1 mislabels the paragraph as section 13 while
   its own selector cites section 10, so a successor reviewer does not inherit it.
3. **Blocking.** Re-seal the four pin manifests carrying the
   `relation-payload-schemas.v2.json` digest and re-run the reference commands and
   regenerated reports at the successor freeze. The digest change is an expected
   consequence of V14-ADV-2, not a defect.
4. Observation only, **not** proposed and assigned **no severity**: the four-codes
   paragraph sits under the §10 sub-heading "Admission and event routes (existing;
   unchanged rows)", which reads oddly over text that adds four members. Outside
   this proposal's scope.

## Limitations

Read-only: no source, pin, report, repository or frozen input was edited, and
everything written is under this directory. No suite was rerun and none is needed
for two non-executable strings — the successor reference commands and the **new**
independent review assess the frozen bytes. No host, renderer, CLI, D9 interpreter
or Run was executed; the call-site evidence is static reading of
`identity-model.py`. I am the coauthor of the integrated v4 bytes that
V14-ADV-1's before-file contains, so I am **not independent** on that file — but
the defect I identify is checkable from the bytes alone, in section headings and
line numbers, in both the live and the frozen file.

Machine-readable form, with every measurement, is in `assessment.json`; the raw
inspection record is in `inspection.json` and the script that produced it is
`inspect.py`.
