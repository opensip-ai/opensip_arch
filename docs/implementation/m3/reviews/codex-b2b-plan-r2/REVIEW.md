# B2B-PLAN-r2 review

**Verdict: REQUIRED-FINDINGS.** B2BPLAN-2 through B2BPLAN-5 are resolved. B2BPLAN-1 remains partially resolved because the proposed current oracle still exposes observations beneath pruned anchors.

## Subject verification

Rehashed `subject.json`: 449 bytes, SHA-256 `1ffe8b264ce3b4fdcbb2aadef67227b3d2839fb933566547779366c27b0a2cb7`. Rehashed its sole member, `docs/implementation/m3/config-discovery-b/b2-b/PLAN-r2.md`: 18,780 bytes, SHA-256 `9da700c701cb4d9cb4d88aef4dd392efc6ef049fe378dc04a20ee1f0bd1919d1`. Both match.

Product HEAD remains `94e5fdebd63a174694dadbb5e647063855614b77`; architecture HEAD remains `424f64a3f331261d0f1e8fb323948492cda5a06d`. Both tracked states are clean. The implementation facts remain consistent with the prior source inspection and the unchanged product base. The T2 acquisition state is documentary evidence; no store or held-out entry was inspected or freshly verified.

## Required finding: B2BPLAN-1, current oracle still needs observation confinement

Section 1.0 says replacing SLM's DD global yields SLM's algorithm with the corrected rule and SX-1, then describes a V3 shape projection. This updates calls into DD but does not update independent SLM scans. In particular, `security_lifecycle_model_v1.py`'s `finish(root)` (around lines 751–758) appends every supplied descendant directory with a `vcs` observation to `nestedRepositories`, without a DD classification check.

Independently reproduced using permitted read-only model imports and the provisioned Python package snapshot. Installed the exact bound B2-a reference as SLM.DD and supplied only synthetic metadata:

```python
# Directory observations: uid/gid 1000, mode 0755, dev 1
fs = {
    '/h/w': directory(),
    '/h/w/.opensip': directory(),
    '/h/w/.opensip/hidden-repo': directory(vcs=True),
}
# explicitProject=/h/w, cwd=/h/w, accountHome=/h,
# invokingUid=1000, prunedTreeMarkerInventory='not-enumerated'
```

The call accepts and returns both:

```json
{
  "nestedRepositories": ["/h/w/.opensip/hidden-repo"],
  "prunedTrees": [{"path":"/h/w/.opensip","reason":"opensip-custody-state","markerCount":null,"markerCountBasis":"not-enumerated"}]
}
```

The planned native walker cannot observe the hidden repository because it never opens or lists `.opensip`. The stated shape/version projection does not remove it. A schema-valid inventory can still carry this invalid observation; schema validation alone cannot establish SX-1. This also prevents the promised byte-for-byte comparison of every partial-provenance field.

**Required correction:** define the current oracle's observation-population adapter or an explicit reviewed algorithm correction in B2-b0, beyond the DD swap. Prevent boundary observations below custody/pruned anchors and align supplied observations with what the native walker can lawfully obtain. Keep historical SLM replay separate. Add a repository-under-`.opensip` control and related pruning/nested-boundary population controls, ensuring the oracle does not invent hidden boundary or excluded-unit observations from subtrees the walker never enters. Retain the complete inventory comparison and the newly explicit partial-provenance contract.

## Prior findings and decisions

| Finding | Assessment |
|---|---|
| B2BPLAN-1 | Partial: the separate reviewed reference, current/historical distinction, pending type and shape-only fill are improvements; observation confinement above remains missing. |
| B2BPLAN-2 | Resolved: choose the source before observation; separate strategies confine explicit/config observations to roots, chains and necessary in-root boundary/pruning evidence. Sibling trace and budget controls test the distinction. Boundary-only traversal inside named roots does not enumerate additional units. |
| B2BPLAN-3 | Resolved: all-entry objects/edges margin remains a B2-b completion gate; held-out results remain outstanding for an authorized nondisclosing harness or a separately accepted law change. Store re-verification and no-follow counting are required; bytes are distinguished. |
| B2BPLAN-4 | Resolved at plan level: typed waiver plumbing is assigned to core judgments and analysis selection; owner-only scope, unwaived markers, unchanged legacy paths and mode/ACL negative controls are explicit. |
| B2BPLAN-5 | Resolved: by-name observation carries metadata and device/inode/kind, compared before use; same-kind directory and marker replacement controls are specified. |

The design-reference prerequisite followed by four product sub-units is a sound split; successor 164 is the next contract position at this base. LD-B2B-1/2/3/4/6/7/8/9 are sound as plan decisions. Pending provenance is explicitly internal and unserializable, while the boundary inventory is complete; shape-only reader fills are not emitted or claimed as observations. B3-b retains the completing readers. The historical/current replay decision LD-B2B-5 and B2-b0 remain unsound until the oracle-population gap is corrected.

Existing CI trace, identity-swap, exhaustion, exact-source, waiver, FW-01 and margin-stop controls are appropriate. Add the observation-confinement controls above before calling the set sufficient. B2-c, B3-b, C1 and J1 retain their stated responsibilities; no production completion or qualification follows from this plan.

## Boundaries

Used only permitted read-only inspection, hashing, JSON parsing, Git queries and architecture model imports over synthetic inputs. Ran no Cargo, tests, builds or lane; used no network, other panes or delegation; read no private 413 fixture, installation directory, signing keys, held trees or T2 held-out entry. Neither repository, stage nor control files were edited. Wrote only `REVIEW.md` and `review.json` in this review directory. No code, binding, law change or qualification was made.
