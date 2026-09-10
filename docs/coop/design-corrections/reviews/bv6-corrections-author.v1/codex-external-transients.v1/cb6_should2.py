import pathlib

W = pathlib.Path('/private/tmp/opensip-design-corrections/bv6-corrections-author.v1/work')

P = W / 'docs/v2/contracts/product-v1/identity-and-evidence.md'
s = P.read_text(encoding='utf-8')
OLD = """states for that relation. Coverage scopes partition the claimed universe without
overlaps or omissions, and a `complete` result for a rung the registry marks
total over the inventory (`file@enumerated`) must carry a fact for every
inventoried subject it claims to have examined — a fact that agrees with **that
scope** on its own snapshot, relation, rung and *both* universes. The fact/scope
join above is existential, so in a view carrying two universes a fact of one
lawfully sits beside a scope of the other and must not discharge its obligation.
"""
NEW = """states for that relation.

**Coverage scopes partition, and the two halves of that word have different
owners.** *Disjointness* is the general rule and applies to every relation: two
Coverage scopes of one view that share the **full owning tuple** — the same
`(snapshotId, relation, resolution, sourceUniverse, targetUniverse)` — carry
disjoint subject sets, so no subject is claimed twice under one interpretation.
This is decidable from the retained scopes alone and is a producer obligation
stated here; a differing tuple is a different claim, not an overlap, which is why
the same path may lawfully appear under two universes.

*Omission* is **not** a general rule and is never inferred. A scope owes a
complete enumeration only where the relation registry gives its rung a
`coverageTotality` row, which today is `file@enumerated` alone: a snapshot
inventories exactly the files it contains, so a `complete` result there must carry
a fact for every inventoried subject it claims to have examined — a fact that
agrees with **that scope** on its own snapshot, relation, rung and *both*
universes. `package@manifest-declared` and `vcs-change@vcs-reported` have no row
and owe nothing, because most paths declare no package and most were not changed.
Neither do the nine `symbol`-kind relations, and that is a **stated trust
boundary rather than an omission**: native §1.2 records that the enumerator's
attribution of symbols to files is trusted and **not re-derivable from the
retained Run**, no enumeration of the symbol universe is published, and inventing
one would be fabricated evidence. Reading "without omissions" as a universal
obligation would therefore make the clause either unenforceable or a demand for
evidence the design deliberately does not claim.

This does **not** make `complete` vacuous where no totality row exists. It remains
a claim about the **examined** partition, and it is held to that claim by the
entry's own committed evidence: RC-0 decides the relation's registered
`(relation, rung)` pair before any fact is read, RC-1 keeps enumeration
completeness separate from resolution completeness, RC-2 forces
`unresolvedEdgeClasses` to equal the admitted `unresolved-edge` facts of the view
and never lets a zero edge count imply `complete`, `examinedUniverse` carries the
counts, and `partial`/`not-attempted`/`unknown` with a disclosed deficiency stay
representable so nothing is forced into a false `complete`. The fact/scope join
above is existential, so in a view carrying two universes a fact of one lawfully
sits beside a scope of the other and must not discharge its obligation.
"""
assert s.count(OLD) == 1
P.write_text(s.replace(OLD, NEW), encoding='utf-8')

# native §1.2 gains the pointer back, so the two statements are reconciled from both ends
P2 = W / 'docs/v2/contracts/product-v1/native-evidence.md'
s2 = P2.read_text(encoding='utf-8')
OLD2 = """so their empty results are ordinary findings. Which relations owe totality is
stated in the relation registry (`coverageTotality`), where only `file` has a
row, and never inferred.
"""
NEW2 = """so their empty results are ordinary findings. Which relations owe totality is
stated in the relation registry (`coverageTotality`), where only `file` has a
row, and never inferred. This is the specific rule that identity §3's "partition
the claimed universe without overlaps or omissions" defers to: the **disjointness**
half is general and applies within the full owning
`(snapshotId, relation, resolution, sourceUniverse, targetUniverse)` tuple, while
the **omission** half is discharged only where this registry carries a row. For
the nine `symbol`-kind relations it carries none, and the reason is the trust
boundary stated below — symbol-to-file attribution is not re-derivable from the
retained Run — so no omission obligation exists there and none is invented.
"""
assert s2.count(OLD2) == 1
P2.write_text(s2.replace(OLD2, NEW2), encoding='utf-8')
print('ok')
