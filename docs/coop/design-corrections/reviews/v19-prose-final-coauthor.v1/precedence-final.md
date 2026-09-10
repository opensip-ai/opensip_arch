It is **not** the only scope-capability guard, and an earlier revision of this
paragraph read as if it were. A separate and weaker law, stated in §10 and
published as
`identity-schemas.v2.json#/x-opensip-digest-domains/scopeCapabilityLaw`, applies
to **any** universe whose dialect form is a closed suffix table — TypeScript and
the syntax universe both — and asks only whether a scoped path's own suffix
selects a variant in the table that universe published. For the syntax universe
that condition is strictly weaker than the grammar law above and is implied by
it, because the capability registry's `data-document` class law already states
that **no suffix of a data grammar appears in the syntax dialect table**. For
TypeScript it is the *only* such law, and it is what a `clones` scope over
`package.json` is now answered by. Which guard reaches a given scope first,
however, is decided by what each boundary can see, not by which law is stronger.
The suffix law needs nothing but the scope's own paths, so the native Coverage
producer boundary already applies it to the one case it can judge from a single
record — a `source-path` relation carrying a body-identity join, which is
`clones` — whenever the caller hands it the owning universe's dialect, as Run
closure does. Closure runs that producer admission **before** any of its own
prerequisites, so a false claim of complete Coverage for a `clones` scope over
a path no dialect table lists is refused there, as a producer-admission failure
naming the source variant, before the grammar guard. The grammar law is neither weakened nor reordered: among
closure's own prerequisites it is still applied ahead of the suffix backstop,
and it remains the sole owner, under its own refusal names, of everything a
suffix table cannot see — the `symbol` relations, the other syntax relations,
and the selection case where a path's suffix *is* in the table but no selected
grammar row owns it. An honestly disclosed unsupported scope still carries
`coverage: unknown` and the published `language-tier-unsupported` /
`capability-missing` pair. A false claim of complete Coverage is rejected; its
internal first-refusal name depends on which admission boundary detects it.
