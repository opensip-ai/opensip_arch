The relation document's annotation law also governs schema structure. A governed
occurrence is a reference to `DigestHex`, `Sha256Text` or `CanonicalPath`, including
an intermediate local `$defs` alias, or an inline pattern exactly equal to one of
those definitions' patterns. Follow local references, nested `properties`,
`items`, `additionalProperties` and `oneOf`/`anyOf`/`allOf` branches when checking
these occurrences. An annotation on the occurrence, its enclosing schema path,
or an intermediate alias applies to that occurrence. An annotation on the
terminal governed scalar definition does **not** provide a blanket default for
all references to that type. Directly annotated top-level selector properties remain subject to retention
and join checks even when their scalar form is not one of these three.

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
one of those nested locations must explicitly declare `retention: not-joined`.
As elsewhere in this law, the reason for an exemption is stated on the field
for a reader; admission checks the declared retention, not the presence or
content of that prose. It cannot claim a joinable retention that the current
join vocabulary cannot address. An addressable annotated property requires its
registry join unless it declares that exemption, and every named join field
must exist in the selector. Missing annotations, conflicting annotations,
undeclared retention values, unaddressable claimed joins, missing joins and
joins naming absent fields all refuse at schema-law admission. This check
establishes coherence of the registered schema; the owning-fact snapshot and
retained-byte joins below still establish the truth of each admitted payload.
