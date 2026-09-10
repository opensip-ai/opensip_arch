"""CB7-MUST-1: owning prose. Corrects a now-misleading scope claim in §1.2 and states the law in §10."""
import pathlib

W = pathlib.Path('/private/tmp/opensip-design-corrections/v19-native-coauthor.v1/work')
P = W / 'docs/v2/contracts/product-v1/native-evidence.md'
s = P.read_text(encoding='utf-8')

OLD1 = """The guard is **syntax-universe specific**. Every capability of the TypeScript and
Rust universes is unchanged, including all five semantic relations, and the Rust
compilation-ownership guards are untouched — see the ownership disclosure law in
§10, whose prerequisite is now derived from the actual universe kind so that a
grammar-only clone scope, which has no compilation unit at all, owes no
compiler-ownership obligation.
"""
NEW1 = """This particular guard — the one decided by the **selected grammar rows** — is
**syntax-universe specific**. Every *semantic* capability of the TypeScript and
Rust universes is unchanged, including all five semantic relations, and the Rust
compilation-ownership guards are untouched — see the ownership disclosure law in
§10, whose prerequisite is now derived from the actual universe kind so that a
grammar-only clone scope, which has no compilation unit at all, owes no
compiler-ownership obligation.

It is **not** the only scope-capability guard, and an earlier revision of this
paragraph read as if it were. A separate and weaker law, stated in §10 and
published as
`identity-schemas.v2.json#/x-opensip-digest-domains/scopeCapabilityLaw`, applies
to **any** universe whose dialect form is a closed suffix table — TypeScript and
the syntax universe both — and asks only whether a scoped path's own suffix
selects a variant in the table that universe published. For the syntax universe
that condition is strictly implied by the grammar law above, because the
capability registry's `data-document` class law already states that **no suffix
of a data grammar appears in the syntax dialect table**; the grammar law is
therefore applied first at Run closure and keeps its own refusal names. For
TypeScript it is the *only* such law, and it is what a `clones` scope over
`package.json` is now answered by.
"""
assert s.count(OLD1) == 1
s = s.replace(OLD1, NEW1)

OLD2 = """empty clones Coverage remains indeterminate rather than a finding of no clones.

**Fault law"""
NEW2 = """empty clones Coverage remains indeterminate rather than a finding of no clones.

**A scope whose subjects the universe cannot read as any source variant is
`unknown`, not `complete`
(`scopeCapabilityLaw`; `COVERAGE_SOURCE_VARIANT_UNSUPPORTED_SCOPE`,
`…_DEFICIENCY_MISMATCH`, `…_CAUSE_MISMATCH`, and
`native.coverage-source-variant-*` at the producer boundary).** The per-body
selector already refused an unlisted suffix — `BODY_LANGUAGE_SOURCE_VARIANT_UNKNOWN`
for TypeScript, `BODY_LANGUAGE_GRAMMAR_VARIANT_UNKNOWN` for the syntax universe —
but that selector is reached only while a body is being derived, and a scope that
produces **no fact** derives none. A `clones` scope over `package.json` under the
TypeScript universe was therefore classified by nothing at all and could seal a
determinate `complete` over an empty view: a finding of *no clones* in a file that
universe cannot read as TypeScript in any dialect. Coverage is a claim about the
**examination**, so it must not be decided by whether the examination happened to
produce output. The disclosed pair is the existing
`language-tier-unsupported` / `capability-missing` — no new deficiency, no new
`nativeCause`, no new public detail code — and it is *read from* the published law
rather than restated by the model.

This is deliberately **not** the treatment `BODY_LANGUAGE_OWNER_NOT_COMPILED`
gets two paragraphs above, and the difference is substantive rather than
stylistic. That refusal is about a path which **is** a Rust source file and which
no *selected* target compiles: the universe examined a known-language file and
correctly produced no fact, so `complete` stays lawful. A suffix outside the
table is not a body of that universe in any dialect, so a determinate answer
would assert a negative the universe never had the capability to establish —
exactly the principle the syntax capability law already encodes. The gate is the
relation registry's `bodyIdentityJoin`, so the law reaches only where the dialect
axis is consulted at all (today, `clones`); it claims nothing about symbol
capability, executes and qualifies no compiler or parser, and leaves inventory
evidence ungated on every inventoried path. A `source-path` scope is judged on
**all** of its own subjects, so a mixed `src/a.ts` + `package.json` scope
discloses rather than hiding its unsupported half, an empty subject list is
unsupported rather than vacuously complete, and a **supported** path with no
clone body in it remains a lawful `complete`.

**Fault law"""
assert s.count(OLD2) == 1
s = s.replace(OLD2, NEW2)
P.write_text(s, encoding='utf-8')
print('ok')
