# Declared configuration disclosure owner proposal

Root proposal for RP-DO-04/R23. Not accepted or integrated. Security selects the
closed `semantic-configuration-public-fields-v1` policy for the report's resolved
configuration projection. This is a useful summary of the actual analysis inputs
without copying arbitrary repository strings into the report.

## Exact source

The source is the retained `semantic-configuration` whose canonical raw SHA-256
equals the admitted selected Plan's `resolvedConfigDigest`. The host first
admits that Plan and its association with the exact selected Run. The projection
names the same PlanId and digest, checks the source schema and recomputes that
existing digest. It never reads current project configuration to fill an older
Run's record. A missing, purged, expired or corrupt retained input uses the
report's owned unavailable-source state; it is not an empty configuration.

This is the **resolved semantic configuration**, not raw declaration files or
overridden layers. The existing resolver's winning-layer provenance, operational
retention/UI settings and native-context source text are not retained by this
semantic configuration commitment. Their absence is stated in the carrier;
the report cannot reconstruct or invent them from today's checkout. A future
projection for those inputs needs a separately retained, owned source record.
This proposal does not change which inputs contribute to Plan/Run identity.

## Closed redaction rule

The current owner has exactly 13 field slots. Every slot appears as disclosed,
redacted, or not-present. Field names come from the pinned schema, never from an
untrusted free-form map. Unknown fields or future source schemas fail admission;
they are never passed through on a best-effort basis.

Only `analysis.budget` and `components.allowedScopes` disclose their exact
values. These are a bounded work-unit count and a closed priority choice over
global/project scope. Other values are redacted, including profile identifiers,
capability arrays, component versions/constraints, policy/waiver identifiers,
import identifiers and discovery paths. Array cardinalities are disclosed, but
their elements, string lengths, prefixes and per-value hashes are not. There is
no keyword heuristic or assumption that a syntactically valid identifier/version
cannot contain sensitive information. The existing Plan/configuration commitment
is a source identity, not a new value-level fingerprint.

Names/descriptions of selected rules and capabilities in their separately
admitted public catalogue remain governed by that catalogue owner. Required
finding fields, evidence paths, native context disclosures and renderer parity
also retain their own contracts. This policy does not claim to redact every
other field in a report. It supplies the missing rule for this additional
configuration panel without changing those existing surfaces.

Missing optional values say not-present. A present empty array says redacted
with itemCount 0. Neither is confused with a missing source record. The two
public values remain in their original exact types; booleans and floating-point
approximations cannot replace integer budgets. Redaction never changes the
selected inputs, evaluation, authority, verdict or D9 result.

## Host and report integration

The policy/schema are compiled selected host inputs, not caller-provided
permission to disclose more fields. The reference checks policy coverage and
the closed output shape, but its dictionary inputs do not establish runtime
authority. The actual host supplies admitted immutable source handles and binds
the PlanId to the report's selected Run. The redacted carrier cannot independently
recompute the hidden configuration; that source association is a named host duty.

The browser receives only this carrier, not the raw configuration hidden in a
script tag, diagnostic, attribute, search index, download or debug object. Tests
must inspect the final serialized report as well as the visible text. No current
file fallback or secret-bearing refusal text is allowed when construction fails.
The existing typed source-availability route owns the public failure; the local
reference labels are not new D9 codes.

The report carrier successor must add this projection with provenance and its
fixed limitations, replace the declared-configuration feature placeholder, and
account for its bytes under the existing exploration bound. All 13 field slots
are emitted together or the panel carries an explicit bounded/unavailable state;
the user must not mistake an omitted field for a default. Static parity and other
mandatory findings remain unchanged. Root/actual-Claude selection, source binding,
report construction, browser rendering and leakage checks are still required.
