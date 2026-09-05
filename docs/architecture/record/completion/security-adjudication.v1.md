# Security turn-3 independent adjudication

Frozen authoritative ruling: `security-adjudication.v1.json`, SHA-256 `7030a258493f1ee020ffe3f3a8f8ef8393158b3fb14e094bd183b6cb02092871`.

Dispatch: `security-adjudication-dispatch.v1.md`, SHA-256 `b28ceacac2b3122fad18ab26a3e254ae4f3e8f3c6e3c356926c2c1c7b7d1b18c`.

Fresh independent Codex session `/root/security_adjudicator`; no subject or repair authorship. The ruling pins all nine dispatched inputs, the dispatch itself, all 65 subject files, and additional cited inherited sources. All pins match. All 65 subject files are read-only. Supporting assist evidence was initially writable with matching bytes; its mode was subsequently corrected without changing bytes.

**UPHOLD SEC3-M1, SEC3-M2, SEC3-M3, SEC3-M4, SEC3-M5 and SEC3-M6.** Third-exchange history remains CONTESTED. Author acceptance does not provide independent proof or reset the exchange count.

## SEC3-M1 — Root admission boundary

UPHOLD. The preview expressly forbids kernel attestation keys and repeated keys in any list. The direct signature boundary calls semantic admission without closed root-shape validation. Both a nonempty preview list and five copies of one recovery key pass semantic admission and yield VERIFIED for the retained manifest; the duplicate recovery input fails the root schema. Shape validation at another optional caller cannot establish this boundary.

Repair boundary: Enforce closed parsing/shape and every semantic list/key rule before consuming root authority, including preview kernelAttestationKeys == []. A validated-root wrapper is acceptable only with an enforced construction/use invariant that cannot be bypassed by passing a raw or subsequently mutated root. Preserve both exact negatives and a valid threshold control. This does not adjudicate root bootstrap authenticity or prove a production exploit.

Evidence: security-completion.v3.md:114-137; security_unit_lib_v3.py:217-264,299-307; security-schemas.v3/root.schema.json:recoveryAuthority.keys and kernelAttestationKeys.

## SEC3-M2 — Policy narrowing

UPHOLD. Schema-valid project prefixes src/../private and src/../../outside receive effective grants with no refusal beneath global src. The lexical comparison does not prove subtree containment. The legal descendant src/a is admitted and sibling srcx refused, isolating the traversal defect. A later path guard refusing the target does not repair the incorrect effective-policy admission claim.

Repair boundary: Validate path syntax at source-policy admission, including the global-only path, before a narrowing decision; compare canonical component-delimited paths. Retain both traversals and descendant/sibling controls. Apply the inherited path grammar, rejecting forbidden absolute, dot, dotdot, empty-segment and backslash forms; this ruling does not invent Windows path semantics for supported Unix platforms. No actual unauthorized file access is established.

Evidence: security_unit_lib_v3.py:854-916; security-completion.v3.md:6.11 and 7.5; security-schemas.v3/permission-policy.schema.json:pathPrefixes.

## SEC3-M3 — Witness reconciliation

UPHOLD. The malformed-witness quarantine promise is bypassed by concrete dictionaries: boolean sequence returns OK, missing PENDING hash returns REVERT, and PENDING zero on an empty carrier returns ADVANCE. Python integer membership admits bool and no state-specific hash/genesis validation precedes the recovery branches. Valid INIT/OK/REVERT/ADVANCE and lost-tail controls behave as intended.

Repair boundary: Validate a closed witness carrier before recovery: strict integer ranges excluding bool, carrier identity, allowed state, required hash, and explicit genesis/PENDING constraints. Invalid bytes or dictionaries must quarantine; a valid verified tail is also a required precondition, not evidence supplied by a malformed witness. Retain the three exact negatives and lawful transition/lost-tail controls. No particular new witnessSchema field is mandated; equivalent enforced validation is sufficient.

Evidence: security-completion.v3.md:214-230; security_unit_lib_v3.py:266-296.

## SEC3-M4 — Broker and courier admission require context

UPHOLD. HE2 admission skips exact snapshot membership when omitted and treats a missing grant snapshotDigest as matching the target. The broker checks grant token/status/binding but never its scope; replacing that scope by {} leaves admission successful. The result resolver returns probe bytes with no carrying response, request association, scratch custody or file stat; a trailing newline reference also returns OK. These are enforcing-boundary counterexamples to mandatory checks, not merely internal unscored conveniences.

Repair boundary: Require admitted request, connection binding, journal/grant, snapshot and courier context at the enforcing boundaries. Absent/malformed context refuses before authority or bytes are returned. Check both grant scopes against the exact prebound operation, target and parameters; do not simply copy a read scope into a broker scope without defining the broker scope contract. Preserve foreign/empty/narrowed scope, absent context, response correlation, stat/cap/integrity and actual byte-delivery cases. Require full-match canonical references. Pure helpers may remain only if clearly separated and never scored as admission. This finding does not prove exploitation of production software.

Evidence: security-completion.v3.md:365-425; security_unit_lib_v3.py:572-646,674-708; permission-truth-tables.v9.json:truthTables PT-HOST-EFFECT-BROKERED ENFORCED child-process.

## SEC3-M5 — HE1 durable effect ordering

UPHOLD. The concrete HE1 paragraph orders committing host-state bytes and unlinking the stage before appending RA/RCI/RCO, while inherited durable journal semantics require RA and the applicable commit intent before the effect. It also binds the receipt only to RCO while the inherited result contract and paired SDK permit irreversible commits. Generic inheritance does not remove the conflicting concrete algorithm.

Repair boundary: Specify one ordered HE1 algorithm with admission, durable RA, then durable RCI or ICI under the applicable REV rules before any committed effect; apply immutable bounded bytes, append the matching actual outcome RCO/ICO, and publish the correctly bound receipt/cleanup only at a lawful point. Retain crash/REV cases around actual boundaries. Preserve the reversible inverse/cleanup obligation and irreversible FAILED/INDETERMINATE semantics. An absent outcome never by itself proves not-performed. Reordering list labels in a synthetic trace without matching the concrete algorithm is insufficient.

Evidence: security-completion.v3.md:395-407; security-completion.v2.md:427-430,519; security-completion.v1.md:633-650; permission-truth-tables.v9.json:revocationLinearization transitions L-1 through L-6 and effectCommitDefinitions.

## SEC3-M6 — Linux profile and preserved qualification fleet

UPHOLD. Both Linux templates hard-code 6.8.0-generic in authenticity and pathless identity, and linux-image-6.8.0-*-generic for the package. The specified release-measurement slots cover other fields. Independently retrieved Ubuntu2404 runner documentation reports 6.17.0-1022-azure on image 20260823.283.1, incompatible with those fixed identities. The x86_64 class alone establishes the contradiction; no claim about the current ARM kernel is necessary.

Repair boundary: Define acquisition and qualification of publisher, package, flavor and series per actual preserved D-102 class. Make any 6.8 generic example explicitly illustrative; release profiles must consistently bind their measured supported series/flavor in every identity carrier while preserving Ubuntu publisher, OS, package and signature checks. Retain a non-6.8 Azure example and wrong-series refusal. Do not replace the four-class fleet, make arbitrary observed kernels automatically trusted, or treat a development template/source document as qualification.

Evidence: security-completion.v3.md:461-480,497-517; security-fixtures.v3/profile.P-LINUX-X86_64-UBUNTU2404-EXT4.json:25-26,102; security-fixtures.v3/profile.P-LINUX-ARM64-UBUNTU2404-EXT4.json:25-26,102; https://raw.githubusercontent.com/actions/runner-images/main/images/ubuntu/Ubuntu2404-Readme.md.

## Evidence and standing

Independent reproductions and their exact source are embedded in the JSON ruling. The original checker also passes 230/230; those checks do not cover the reproduced failures. Legal root, prefix, witness, member and courier controls were retained.

The [published Ubuntu 24.04 image](https://raw.githubusercontent.com/actions/runner-images/main/images/ubuntu/Ubuntu2404-Readme.md) reports kernel `6.17.0-1022-azure`, image `20260823.283.1`; the response digest and relevant lines are retained in the JSON. This establishes the fixed x86_64 profile mismatch, not release qualification or an ARM measurement.

No newly discovered concrete defect is added by this bounded ruling. Only the six dispatched IDs are adjudicated. The next permitted step is one frozen repair-diff confirmation by this adjudicator, outside the three-exchange budget. Mutable successor work is not confirmed. Failed or inconclusive confirmation returns CONTESTED.

**No row is SATISFIED and no unit is adopted by adjudication.** Register edit: none. No qualification or V1 freeze effect.
