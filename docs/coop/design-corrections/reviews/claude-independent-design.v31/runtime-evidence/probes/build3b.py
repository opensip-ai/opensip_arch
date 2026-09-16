"""Give every DR-011-R row its own current scope for source31, so no row carries generic text."""
import json, os

BASE = '/tmp/opensip-design-corrections/claude-independent-design.v31'
P3 = os.path.join(BASE, 'part3.json')
O = json.load(open(P3))
S = {
    'DR-011-R01': ('FACT-PLANE. CoverageResultV3 with RC-0..RC-6, RequirementV2 and the closed '
                   'deficiency/cause registry are unchanged on 31, as are coveragePartitionLaw and '
                   'coverageTotality at retained Run closure. No provider is measured.'),
    'DR-011-R02': ('FACT-IDENTITY. fact-identity-policy.v2 is still reused by exact selector rather '
                   'than restated, with the framed bodyIdentity preimage unchanged on 31.'),
    'DR-011-R03': ('C-2. plan2/exec-plan2 with the closed stage-spec record and the operation-token '
                   'ownership statement are unchanged on 31; the historical defective C-2 join stays '
                   'preserved history, as RES-EP13-01 and RES-EP13-15 record.'),
    'DR-011-R04': ('DELIVERY. Native protocol 3 / TS 2 and the security lifecycle core bridge remain '
                   'the explicit successors on 31.'),
    'DR-011-R05': ('Rust PC-7. Protocol major 3 with identity negotiation, reject-before-disclosure '
                   'ordering, the 22-phase state machine and the 34-row transition table are '
                   'unchanged on 31. No real provider process is exercised.'),
    'DR-011-R06': ('EVIDENCE. identity-and-evidence remains the owning packet for proof outcomes, '
                   'retained verification and regeneration closure on 31; applied v15 stays applied '
                   'and its rejected validator is not elevated.'),
    'DR-011-R07': ('RETENTION. CD-RT-5 and the v28 posture are preserved on 31 and joined to the '
                   'evidence/D9 contract and the reviewed transition suite.'),
    'DR-011-R08': ('D9. Closed host-owned termination with its observation-to-faultCause mapping, '
                   'branch-specific optional fields, cancellation and post-commit required-output '
                   'exit 4 are unchanged on 31. The successor D9 artifact carrying host-invariant '
                   'remains a disclosed, attributed implementation obligation, carried forward and '
                   'not closed by this review.'),
    'DR-011-R09': ('R-1. Semantic IDs still exclude RequestId/ExecutionId, lifetime, credentials, '
                   'cache state, receipt timestamps and storage paths on 31, and the Plan binds the '
                   'semantic grain.'),
    'DR-011-R10': ('Blind consumer-B. Closable only by an actual fresh implementer litmus, which this '
                   'review is explicitly not. The separate blind original 123/8/3 charter remains '
                   'required and uninfluenced: I did not read or touch any blind runtime, report or '
                   'output, and I claim no blind acceptance.'),
    'DR-011-R11': ('OPERABILITY G19. Durable commit, acknowledgements, recovery, retention pins, GC, '
                   'backup/import and availability are defined on 31 and remain measurement '
                   'obligations no design document can discharge.'),
    'DR-011-R12': ('EVALUATION PROOF. Product proof/evidence/seal plus authenticated trusted evaluator '
                   'replay replace the v8/v13 lineages. All 30 nested residuals carry individual '
                   'dispositions in this report, with TCB-SCOPE-01 assessed once over exactly 13 of '
                   'them. No malicious same-process containment is claimed.'),
    'DR-011-R13': ('VERSIONING. The workflow executable detector pivot, portable baseline and typed '
                   'multi-axis comparison still own this on 31, with current D9 and retention as '
                   'explicit dependencies.'),
    'DR-011-R14': ('CFG-6 / TM. Sealed inputs, identity/proof/custody, the explicit trusted '
                   'repository-code principal, storage and G19 supply the current threat-model '
                   'assumptions on 31. This is the same trust posture TCB-SCOPE-01 makes explicit for '
                   'the residual set.'),
    'DR-011-R15': ('Trusted request context. ProjectId marker/registry/namespace and '
                   'RequestId/ExecutionId remain operationally explicit on 31 with end-anchored '
                   'successor grammars.'),
    'DR-011-R16': ('Product authority. D-367 delegation and D-370/D-371 scope are preserved on 31, '
                   'admission section 5 dispositions all seven boundary items, and CD-RT-5 remains '
                   'binding.'),
}
n = 0
for rid, txt in S.items():
    if rid in O['inheritedResidualDispositions']:
        O['inheritedResidualDispositions'][rid]['currentScopeOn31'] = txt
        n += 1
texts = [v['currentScopeOn31'] for v in O['inheritedResidualDispositions'].values()]
print('updated %d rows; %d rows, %d duplicates' % (n, len(texts), len(texts) - len(set(texts))))
assert len(texts) == len(set(texts))
json.dump(O, open(P3, 'w'), indent=1)
print('rewrote part3.json')
