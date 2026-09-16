# Downstream identity trace for the XA-02 / CR-25 pruned-tree row

Standing: authored trace over the isolated successor copy. Executed, not asserted. No product qualification.

## What the pruned row actually reaches

| Consumer | What it reads | Identity effect |
|---|---|---|
| unit_scope_descriptor | t[path] only, unioned into excludedPathPrefixes | scopeDigest = raw_sha256(C(descriptor)), then plan2, then RunId |
| _boundaries_out (scope disclosure) | nested repos/projects, custody exclusions, source | carries NO pruned row |
| discover_units boundary test | (path, reason) | refusal only, not a digest |
| DiscoveryProvenanceV2 / AdmittedBoundaryInventoryV2 bytes | whole row | operational provenance digest over those records |

markerCount and markerCountBasis reach NOTHING in the first three rows. Control C5b holds the
scopeDescriptor and scopeDigest bit-identical while flipping every count to null and every basis to
not-enumerated; C11a holds the selected unit set identical; C5a shows they are not equality keys.

## Where they DO change bytes, honestly

Control C5c shows the raw SHA-256 over the canonical boundary-inventory record changing when only the
count/basis change. That is correct and must not be denied: the record bytes changed, so any OPERATIONAL
digest taken over the record changes. The claim is narrower than cannot enter any digest: count and basis
do not alter semantic source scope, unit selection, native Coverage or Plan bounds, or Run identity.

## The one real semantic consequence, disclosed

CR-25 makes previously invisible anchors visible, and an anchor PATH does enter excludedPathPrefixes
(control C11b: vendorish/.hg). For a repository holding a pruned anchor outside the conventional set
(.git and node_modules under a unit root, target under a Cargo root) the scope descriptor, and therefore
scopeDigest / plan2 / RunId, differs from the pre-correction value.

The analysed byte set does not change: the segment rule already pruned that tree, and unit_scope_descriptor
documents that the segment rule applies IN ADDITION to the prefixes. What changes is that the Plan now
DISCLOSES the exclusion instead of omitting it. This is the same class of disclosed discovery correction as
XA-01, which also moves unit selection and therefore Run identity for affected repositories. Historical Runs
keep their bytes. A reviewer must accept this consequence explicitly; it is not hidden inside the
provenance-only argument.

## Not selected

Suppressing observation-only anchors from excludedPathPrefixes to keep identity bit-stable was considered
and rejected: it would make the Plan omit a known exclusion, and it would make the descriptor depend on HOW
an anchor became known, which is the same hidden-provenance dependence that produced XA-01.
