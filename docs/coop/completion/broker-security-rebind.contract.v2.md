# Broker final security dependency successor

FROZEN-PROPOSED for independent review against exact frozen security v7.
Independent security acceptance remains a separate adoption condition.
Author: Codex protocol fixture author.

This successor retains the thirteen immutable broker v3 subjects and replaces
only the security receipt, host request join and their executable checker/report
paths. The closed bootstrap schema, parser, typed SDK API, physical courier
implementation, D-006 limits and launch contract remain the exact v3 bytes.

Security v6 consumes the complete closed effectResult body already emitted
by the courier: requestSeq, decisionSeq, outcomeSeq, commitClass and effectOutcome,
plus optional resultRef. No three-member result projection is an admission input.
The new checks join the full shape to valid_effect_result and resolve_result,
retaining callback non-invocation and no returned bytes for structural failures,
FAILED and INDETERMINATE. Host request bodies remain exactly effectClass,
authorizationRef and operationRef.

New exact hostile scope fixtures provide pathPrefixes as a string separately in
the broker and underlying grants and add an unknown scope member. Each must
refuse before RA, file access or returned bytes. Existing valid scopes name a
list of normalized member paths, snapshot digest and exact sealed membership.

This is conditional design evidence. The security acceptance receipt and an
independent review of this successor are required before adoption. No production
qualification or register change is claimed.

The retained execution passes 273/273 courier/security-join checks and 93/93
bootstrap checks. Its historical launch regression retains 150 broker checks and
484 control checks. These are design evidence with the original physical versus
model-only limitations; no durable journal or native support-matrix claim.
