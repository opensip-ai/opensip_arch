# Final G15 security join preparation

DRAFT. Not frozen, reviewed, accepted or product qualification. Security v3 is
still mutable; no result is claimed against its current bytes. Frozen G15 v2
and compatibility selection v5 remain unchanged.

`compatibility-selection-model.v6.py` is a draft successor using the final v3
security library and schemas. It refuses success until a separate exact reviewed
security-input receipt exists. No receipt is authored during this preparation.
The receipt must pin the accepted library, effective-policy schema, source-policy
schema, root/envelope/catalog/revocation/registry/view schemas and security review
subjects. Parent dispatch is required before integration freezes.

The new admission order is exact dependency custody, closed resolver input,
global/project source-policy custody, owner-defined policy combination, exact
recomputed effective body, effective digest in the input and trusted host snapshot,
compatibility matrix custody, root structural AND semantic admission, signatures,
revocation freshness, signed catalog, private registry/view, full manifests and
artifact closure, followed by the unchanged reviewed selection core.

The old signed two-component root currently passes the draft semantic predicate.
This is an inspection observation, not acceptance of mutable v3. Existing signed
manifest/catalog/view/artifact bytes can remain identical. The old single project
policy document will be replaced in new fixture bundles by separately retained
global/project documents plus the effective policy body. The lock field remains
permissionPolicyDigest; it now pins the final effective object including both
source digests. No lock grammar change is expected.

Planned exact new fixtures:

- Positive global/project merge, narrower project scope, deny-wins, no-project
  global-only mode, and explicit empty project policy. Distinguish missing bytes
  from a host-authorized absent project source; missing expected bytes refuse.
- Source bytes changed with old source pin; forged effective body with recomputed
  attacker lock pin; swapped global/project labels; omitted source; widened scope;
  source-preserving grants mismatch; stale effective lock pin. All refuse without
  a partial lock or resolved list.
- Existing signed root plus all final semantic root negatives, re-signed with
  public TEST keys where necessary and trusted stored-byte pin advanced in the
  fixture to isolate semantic refusal from simple custody failure. Include weak
  threshold, overlapping role keys, invalid key IDs, active-role typed absence,
  origin/previous-version mismatch and invalid expiry ordering.
- Same five conditional G15 classes across four platforms and three states;
  preserve exact artifact/canonical/envelope cases while deriving new golden
  locks solely from final policy bytes. Retain the existing 960-slot manifest
  and 149-case selection regression suite rather than relabeling old evidence.
- Preserve signed revocation freshness equality/inside/outside and malformed
  timestamp refusals from G15-M1. Verify old frozen G15 v2 replay remains exact.

Pending security-owned prerequisites: the closed effective-policy carrier;
precise project-policy absence meaning; final root semantic admission bytes;
independent security review and exact custody pins. The v6 draft receipt's schema
path is supplied only after that carrier is finalized, not guessed here.

HE-2 advisory remains separate: successful effectResult/request correlation,
exact scratch publication/ownership/no-follow/regular-file/bounded-read rules,
per-spawn aggregate result storage, result lifetime and cleanup, and sealed-VFS
source binding must join the SDK courier. Mutable helper callback integrity tests
alone do not establish those boundaries. Text-prefix source scope checks need
an explicit prior canonical path admission rule to reject dot-dot traversal.
This file supplies no security byte edits and closes no HE-2 obligation.
