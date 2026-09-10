import pathlib

P = pathlib.Path('/private/tmp/opensip-design-corrections/bv6-corrections-author.v1/work/'
                 'docs/v2/contracts/product-v1/native-evidence.md')
s = P.read_text(encoding='utf-8')

OLD = """`configOrigin` is **derived from that retained record, never asserted**:
`synthesized` exactly when the entry is null and `nodes` is empty; otherwise it
comes from the selected entry's kind (`jsconfig` for a jsconfig entry, otherwise
`tsconfig`). Node kind agrees with its path as specified by the schema and native
admission. A jsconfig entry extending a shared base remains a jsconfig program.
The universe's `configOrigin` must equal the derived value. This is the input
§2.4's agreement check needs; without the record the `tsconfig`/`jsconfig`
distinction was not derivable and two spellings minted two universe identities for
one admitted context.
"""
NEW = """`configOrigin` is **derived from that retained record, never asserted**:
`synthesized` exactly when the entry is null and `nodes` is empty; otherwise it
comes from the selected entry's kind (`jsconfig` for a jsconfig entry, otherwise
`tsconfig`). A jsconfig entry extending a shared base remains a jsconfig program.
The universe's `configOrigin` must equal the derived value. This is the input
§2.4's agreement check needs; without the record the `tsconfig`/`jsconfig`
distinction was not derivable and two spellings minted two universe identities for
one admitted context.

**Node `kind` is derived from the node's path by a published closed table, for
every node.** The rule is
`native-evidence.schemas.v2.json#/x-opensip-config-node-kind-law`, named by an
`x-opensip-vocabulary` annotation on the field itself: take the **basename** —
the final `/`-separated segment — and compare it **exactly and case-sensitively**;
`tsconfig.json` → `tsconfig`, `jsconfig.json` → `jsconfig`, **every other
basename → `other`**. No prefix, glob or stem matching, no case folding, nothing
read from the file's content, its depth or its position in the graph. It applies
to the **entry and to every non-entry node** alike:
`packages/web/tsconfig.json` reached as a base is `tsconfig`, and
`tsconfig.build.json` reached as a base is `other` — the widespread
`tsconfig*.json` naming convention has no specified meaning and is deliberately
**not** the rule, since `tsconfig.json` and `jsconfig.json` are the only two
basenames the language recognizes by name. `other` is an ordinary value, not a
defect: an explicitly selected custom-named configuration is an `other` entry that
still derives `configOrigin=tsconfig`.

This had to be written down rather than left to "the schema and native
admission", which stated it nowhere. `kind` is **inside the hashed record** —
`tsconfigGraphHash` is the raw SHA-256 of `C(TypeScriptConfigGraphV1)`, the
universe requires it, and the universe identity reaches `fact2`, `scope2`,
`coverage2`, `view2`, `evidence2`, `seal2` and the RunId — while `configOrigin`
reads only the entry's kind and therefore pins nothing, and a non-entry node's
kind derives no value at all. Two conforming hosts reading one repository that
contains `tsconfig.build.json` would have minted two RunIds and defeated
independent replay across machines, which is the same defect the analysis-spec
`capabilityId` vocabulary was closed for and is closed the same way. A node whose
declared kind is not the derived one refuses
(`native.config-graph-kind-contradicts-path`), so neither the entry nor a base can
be relabelled.
"""
assert s.count(OLD) == 1
P.write_text(s.replace(OLD, NEW), encoding='utf-8')
print('ok')
