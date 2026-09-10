# Proposed normative contract clarification — not applied

Root proposes inserting the following directly after the relation payload digest-law paragraph in `docs/v2/contracts/product-v1/identity-and-evidence.md` (before the `x-opensip-relation-registry` snapshotJoins paragraph). This addresses actual independent v10 advisories A1/A2 without editing the registered schema document bytes or inventing new payload semantics. The source contract is a blind-kit normative input; the reference Python is not. Original advisory severity remains nonblocking in the historical review. Root chooses to settle the implementer's rule now, before another blind pass.

## Exact proposed text

The relation document's annotation law also governs schema structure. A governed
occurrence is a reference to `DigestHex`, `Sha256Text` or `CanonicalPath`, including
an intermediate local `$defs` alias, or an inline pattern exactly equal to one of
those definitions' patterns. Follow local references, nested `properties`,
`items`, `additionalProperties` and `oneOf`/`anyOf`/`allOf` branches when checking
these occurrences. An annotation on the occurrence, its enclosing schema path,
or an intermediate alias applies to that occurrence. An annotation on the
terminal governed scalar definition does **not** provide a blanket default for
all references to that type. Directly annotated properties remain subject to
retention and join checks even when their scalar form is not one of these three.

Every governed occurrence must have an effective annotation. An annotated
alternative does not cover an unannotated alternative; a parent annotation may
cover each alternative it encloses. When multiple schema paths reach the same
location, any occurrence lacking an effective annotation makes that location
inadmissible. Later annotated occurrences cannot undo that absence. Object-key
order and the order in which these paths are visited must not change admission.

There is no precedence rule between disagreeing effective annotations at one
location: distinct annotations conflict and the document refuses; repeated
annotations that are equal under typed canonical equality do not conflict.
Every effective annotation must use the declared retention vocabulary. These
same effective annotations govern coverage, retention and join/exemption checks;
none of those checks may silently revert to inspecting only direct properties.

The current registry's join fields address top-level selector properties.
Taking a scalar alternative of such a property preserves that address; entering
an object member, array element or map value does not. A governed occurrence at
one of those nested locations must explicitly declare `retention: not-joined`
with its reason. It cannot claim a joinable retention that the current join
vocabulary cannot address. An addressable annotated property requires its
registry join unless it declares that exemption, and every named join field
must exist in the selector. Missing annotations, conflicting annotations,
undeclared retention values, unaddressable claimed joins, missing joins and
joins naming absent fields all refuse at schema-law admission. This check
establishes coherence of the registered schema; the owning-fact snapshot and
retained-byte joins below still establish the truth of each admitted payload.

## Review request to actual coauthor

Please substantively assess this exact text against your actual corrected reference and the existing law. If a phrase is broader than the supported reference or would change semantics, propose exact corrected wording in your handoff. Do not edit the live or frozen contract; root owns its application after both current passes finish. You may place your proposed exact version here as a separate output file, preserving this input. Record the version/hash you actually assessed. No acceptance is inferred from merely seeing this request.
