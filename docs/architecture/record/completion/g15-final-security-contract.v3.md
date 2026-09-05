# Final signed G15 security join

FROZEN-PROPOSED executable design evidence for independent review.
Author: Codex protocol fixture author. The exact dependency is frozen security v8.
Independent security acceptance remains a separate gate to architecture adoption;
no production component, OS qualification, register cell or implementation grant
is created here. The exact final dependency version is named by
`g15-final-security-inputs.v3.json`, not inferred from an earlier report.

## Exact custody and policy meaning

The selector imports the security library/schema directory from the retained
receipt and checks every pinned source before evaluating a request. The receipt
records frozen bytes and the conditional standing; it does not assert that an
independent review has passed. Matrix `compatibility-matrix.completed.v5.json`
is pinned as exact stored bytes and supplies compatibilityPolicyDigest via plain
SHA-256, preserving its existing custody meaning. Lock grammar remains completed
v3 and all independent surface windows remain unchanged.

The final permissionPolicyDigest is the digest of the effective policy under
`opensip.metadata.policy-effective.1`. The selector separately reads and validates
the global/project sources, compares their domain digests under
`opensip.metadata.policy.1` with the trusted host observations, calls the security
owner's combination function, validates the closed effective-policy schema and
requires exact equality with the retained effective body and source pins. An
attacker recomputing a lock pin for a forged effective body cannot bypass the
source comparison or combination. No policy file or lock grants permission merely
by carrying these bytes.

Trusted host presence observations distinguish PRESENT, ABSENT and (project only)
NO-NAMESPACE. An observed absent global file becomes the explicit empty global
policy; an absent file for a selected project becomes the explicit empty project
policy and denies by absence. Expected PRESENT bytes that go missing refuse.
Only a global/core operation without a selected namespace uses project=None.
Selected-project scope cannot be relabeled global-only to choose that branch.
The effective source hashes still bind the canonical empty source values when
files are absent. No namespace or file is created to materialize absence.

## Root authority and revocation

The selector performs structural admission and calls admit_root_document to
obtain the security owner's AdmittedRoot. Every envelope verification receives
that admitted value. It never constructs an AdmittedRoot directly or uses a
caller-supplied admitted Boolean. Revoked key IDs remove signatures from the
verification view; the admitted root's role/key lists remain immutable. This
preserves root structural invariants while producing ordinary threshold refusal
when revocation removes a required signer. The original received envelope bytes
remain the custody authority and are never rewritten in the fixture bundle.

The final TEST root differs from the older G15 root by kernelAttestationKeys=[]
and a freshly computed envelope/external trusted-root pin. All active root and
role public keys are unchanged, so existing catalog and component signatures
remain valid. The exact old root document and envelope are retained unchanged
as a final-schema rejection case. They also remain in the independently replayed
historical G15 v2 package; older evidence is not reinterpreted under new rules.

## Concrete property coverage

The five previously conditional classes still run across four declared platforms
and three states, with exact signed manifests, catalogs, registry views, archive
and file bytes, complete two-component locks, and stored/canonical digest goldens.
The final matrix assigns all 960 slots concrete input pointers; its other 900
members keep their original bytes and stated evidence limitations. These axes
are reference fixtures and do not claim native OS execution.

Additional source/effective-policy cases cover explicit absence, global-only
operation, narrowing, deny-wins, changed source with stale pin, missing expected
source, wrong scope label, forged effective body/source field, widening, path
traversal, duplicate grant pairs and an old effective lock pin. Invalid policies
produce neither a partial lock nor a resolved prefix.

Freshly signed negative roots isolate schema/semantic admission from simple
signature or stored-byte failure. Cases cover kernel keys, weak threshold,
key-ID mismatch, recovery/role key overlap, active-role typed absence, origin/
previous-version inconsistency and expiry ordering. Independent signature checks
show the negative root envelopes still have two valid public TEST signatures.
Additional signed revocations prove that removing a used catalog signer refuses
on threshold while revoking an unused role key preserves the unchanged lock.

The signed just-inside/equality/just-outside 90-day freshness cases, malformed
timestamps and the retained independent stale-revocation counterexample are
rejoined to the final root/policy custody. The original G15 v2 report is also
replayed byte-for-byte with its own historical semantics. The reviewed 149-case
selection core is replayed unchanged, covering SemVer comparison, dependency
closure, duplicate requests, pins/holds, deterministic order and refusal behavior.

All private TEST seeds are explicitly public fixture material, never release
keys. Golden locks are design evidence only (`admitted: false`). Full persistent
trust transitions, registry publication, journal durability, platform process
confinement and release qualification remain their separately reviewed gates.

## Security v8 composition repair

This successor retains the prior frozen unit and rebinds its exact dependencies
to security v8. New cases distinguish equal stateClass, widening SC-CACHE to
SC-OPS, and supplying a project stateClass when the global grant has none.
Malformed raw policies contain an unknown member, string pathPrefixes, null
grants or missing denies. Each negative runs through the selector and must
produce no partial lock; the security merge boundary also returns zero grants.
The positive equal-stateClass case prevents refusal-only coverage.

The original received signature envelope is canonicalized and fully schema
validated before creating the revoked-signer verification view. Malformed or
duplicate revoked signatures, more than sixteen original entries, floating
schema numbers and unknown envelope/subject members refuse without a partial
lock. A correctly signed revoked unused signer remains an accepted control;
revocation removes authority, never original structural obligations.

This version rebinds the prior frozen unit to exact security v8. The previous
unit and its findings remain preserved; no API or regression expectation changes
are introduced by this dependency successor. Independent unit review remains
required before the final application may use this receipt.
