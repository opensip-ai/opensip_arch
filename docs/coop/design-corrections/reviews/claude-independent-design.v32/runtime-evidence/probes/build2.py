"""review.json part 2 — the six keyed maps, each row with actual current owner paths/selectors,
evidence, limits and a current status free of stale inherited prose."""
import json, os

BASE = '/tmp/opensip-design-corrections/claude-independent-design.v32'
REC = os.path.join(BASE, 'receipts')
V31 = json.load(open('/tmp/opensip-design-corrections/claude-independent-design.v31/review.json'))
p01 = json.load(open(os.path.join(REC, 'p01-delta.json')))
CH = {c['path'] for c in p01['changed']} | {a['path'] for a in p01['added']}
p20 = None
O = {}

C = 'docs/v2/contracts/product-v1/'
F = 'docs/coop/design-corrections/foundation/'
N = 'docs/coop/design-corrections/native/'
S = 'docs/coop/design-corrections/security/'
Wf = 'docs/coop/design-corrections/workflows/'
A = 'docs/v2/architecture/'
REPAIR = Wf + 'repair_closed_world_selection.v1.py'
GLOB = F + 'glob-pattern-contract.v1.md'


def row(owners, status, evidence, limits, extra=None):
    ch = sorted(p for p in owners if p in CH)
    d = {'currentOwnerFiles': owners,
         'ownerFilesChangedIn31to32': ch,
         'ownerFilesUnchangedIn31to32': [p for p in owners if p not in CH],
         'currentStatusOn32': status,
         'evidence': evidence,
         'limits': limits,
         'readingStanding': ('changed owner regions read in this session'
                             if ch else
                             'inherited from my v31 complete reading after exact-byte verification '
                             'that these owner files are unchanged in my derived 31->32 delta'),
         'appliedByThisReview': False,
         'finalApplicationOutcomeGranted': False}
    if extra:
        d.update(extra)
    return d


# ---------------- 16 AR ----------------
AR = {}
AR['AR-01'] = row([C + 'admission-and-qualification.md', F + 'canonical.py', C + 'identity-and-evidence.md'],
                  'Exact integer admission is unchanged on 32.',
                  'check-identity / check-integration pass in the 32 suite run; owner files unchanged.',
                  'Design law only; no product parser exists.')
AR['AR-02'] = row([C + 'admission-and-qualification.md'],
                  'Authenticated qualification subject and independent verification unchanged on 32.',
                  'owner file unchanged in my delta.',
                  'Remains measurement no design document can discharge.')
AR['AR-03'] = row([C + 'security-and-lifecycle.md'],
                  'Repository/config custody and discovery unchanged on 32.',
                  'owner unchanged; security suite unaffected by this delta.',
                  'No repository was discovered.')
AR['AR-04'] = row([C + 'security-and-lifecycle.md'],
                  'Clock excursion and poisoned-floor rules unchanged on 32.', 'owner unchanged.',
                  'Unexecuted product obligation.')
AR['AR-05'] = row([C + 'security-and-lifecycle.md'],
                  'Expired root continuity and live revocation unchanged on 32.', 'owner unchanged.',
                  'Unexecuted product obligation.')
AR['AR-06'] = row([C + 'security-and-lifecycle.md', S + 'carrier-format.v3.md'],
                  'Support population and platform provenance unchanged on 32.', 'owners unchanged.',
                  'Carrier qualification separately required.')
AR['AR-07'] = row([C + 'native-evidence.md'],
                  'Sealed Rust dependencies and authorized preparation unchanged in substance; the '
                  'native chapter changed only to add the repair/closed-world link to workflows §6.',
                  'I read the three changed native lines; they add a cross-owner link and no new '
                  'native obligation.',
                  'No real provider is exercised.')
AR['AR-08'] = row([C + 'workflows-and-surfaces.md', Wf + 'workflows_model.v1.py',
                   Wf + 'workflows_model.v3.py', REPAIR],
                  'REASSESSED ON THE REPAIRED SOURCE. The invocation/attempt/step/Run and action '
                  'lifecycle obligation now includes a published repair ClosedWorld evidence '
                  'selection law in workflows §6 with a named reference owner. The gap root '
                  'confirmed against source31 is closed in these bytes: ownership comes from the '
                  'retained EnumerationPlan census, unavailable owners are typed unresolved, '
                  'unselected programs are not inferred, and the conjunction is non-vacuous.',
                  'Executed the module myself across 10 property groups (p05) and ran '
                  'check-workflow-projection.v3.py (rc=0, 92.5s) and check_workflows.v1.py '
                  '(1803/1803).',
                  'Design and reference only: no product repair preview/apply exists, and the '
                  'synthetic host projection is gate integration, not admitted descriptor evidence.')
AR['AR-09'] = row([C + 'identity-and-evidence.md', F + 'identity-schemas.v3.json'],
                  'Identity/proof/custody/retention closure unchanged on 32.',
                  'owners unchanged; evaluator3 launcher 16/16 with 1244 pins valid.',
                  'No precision defect from my earlier reviews is open against this owner.')
AR['AR-10'] = row([C + 'workflows-and-surfaces.md', C + 'security-and-lifecycle.md'],
                  'Runnable prior detector and portable baseline unchanged in substance; the '
                  'workflows chapter changed elsewhere (§6 repair law and the §8 glob link).',
                  'I read the changed chapter regions; §2 is untouched by them.',
                  'Detector remains unexecuted product work.')
AR['AR-11'] = row([C + 'workflows-and-surfaces.md'],
                  'Typed delta attribution and admitted imported evidence unchanged in substance on 32.',
                  'changed regions of this file are §6 and the §8 glob link, not §3/§4.',
                  'No real import corpus.')
AR['AR-12'] = row([C + 'native-evidence.md', N + 'native-evidence.schemas.v2.json'],
                  'Resolution-complete authoritative negative provenance unchanged on 32; the native '
                  'schema file is NOT in my 31->32 delta.',
                  'native suite passes; schema file unchanged this window.',
                  'Provider truth remains trusted extraction evidence.')
AR['AR-13'] = row([C + 'native-evidence.md', C + 'workflows-and-surfaces.md'],
                  'TS/JS/Rust native cells, monorepos and output handling unchanged in substance on 32.',
                  'changed regions assessed and do not alter these sections.',
                  'No compiler is run.')
AR['AR-14'] = row([C + 'security-and-lifecycle.md', S + 'carrier-format.v3.md',
                   S + 'carrier-migration.v1.md', S + 'carrier-dispatch.v3.json'],
                  'Core/state/trust migration and concurrent operation unchanged on 32.',
                  'none of these owners is in my delta.',
                  'All 54 recovery cases remain unexecuted.')
AR['AR-15'] = row([C + 'README.md', 'docs/coop/design-corrections/current-source-map.proposed.md',
                   A + 'report-asset-binding.v1.json'],
                  'One effective current narrative and obligation map holds on 32.',
                  'owners unchanged; check-integration passes 412 checks.',
                  'No precision defect from my earlier reviews is open here.')
AR['AR-16'] = row([C + 'workflows-and-surfaces.md', C + 'native-evidence.md'],
                  'Provenance-specific remedies and exact outcomes: strengthened on 32, because the '
                  'repair dissent remedy now names all six ordering members including the retained '
                  'coverage2 identity, so a remedy identifies the actual record.',
                  'verified by execution that two records differing only in targetUniverse, '
                  'subjectScopeCommitment and identity now produce distinct coordinates.',
                  'Remedy text quality only; no product surface emits it yet.')

# ---------------- 15 FW ----------------
FW = {}
FW['FW-01'] = row([C + 'security-and-lifecycle.md', C + 'native-evidence.md',
                   C + 'admission-and-qualification.md', C + 'workflows-and-surfaces.md'],
                  'zero-config/recommend unchanged in substance on 32.', 'changed regions do not touch it.',
                  'No repository discovered.')
FW['FW-02'] = row([C + 'native-evidence.md', C + 'identity-and-evidence.md'],
                  'clones unchanged on 32.', 'owners unchanged in substance.',
                  'No normalizer qualified.')
FW['FW-03'] = row([C + 'native-evidence.md'], 'native semantics unchanged in substance on 32.',
                  'the native chapter change is the workflows §6 link only.', 'No provider measured.')
FW['FW-04'] = row([C + 'workflows-and-surfaces.md', C + 'native-evidence.md'],
                  'richer evidence unchanged on 32.', 'changed regions are §6 and the glob link.',
                  'Imported observations stay non-authoritative.')
FW['FW-05'] = row([C + 'workflows-and-surfaces.md'], 'delta gate unchanged on 32.',
                  'changed regions do not touch §2/§3.', 'Unexecuted.')
FW['FW-06'] = row([C + 'identity-and-evidence.md', F + 'evaluator-composition-contract.v3.md',
                   F + 'identity-model.v3.py', F + 'identity-schemas.v3.json'],
                  'Determinism unchanged on 32 and still satisfied: the explicit ruleResults key '
                  'order remains implemented and the selection order in the new repair law is '
                  'likewise published on UTF-8 bytes with a total six-member key.',
                  'check-replay.v3.py rc=0; the new SELECTION_ORDER_KEY is total by construction.',
                  'Finite controls show distinct identities for finitely changed inputs; they do not '
                  'prove global SHA-256 injectivity.')
FW['FW-07'] = row([C + 'workflows-and-surfaces.md'], 'coherent workflow unchanged on 32.',
                  'chapter read; §1 untouched by the delta.', 'Design law only.')
FW['FW-08'] = row([C + 'native-evidence.md', C + 'workflows-and-surfaces.md'],
                  'omissions unchanged on 32.', 'changed regions assessed.', 'Unexecuted.')
FW['FW-09'] = row([C + 'workflows-and-surfaces.md'], 'candidate -> inspect -> review unchanged on 32.',
                  '§5 untouched by the delta.', 'No product surface.')
FW['FW-10'] = row([C + 'workflows-and-surfaces.md', REPAIR, Wf + 'schemas/repair.schema.json',
                   Wf + 'schemas/evaluator3/repair.schema.json', C + 'native-evidence.md',
                   C + 'security-and-lifecycle.md'],
                  'REASSESSED ON THE REPAIRED SOURCE. Repair evidence now has a published selection '
                  'law, a named reference owner, both repair-schema annotations describing the '
                  'five-field display as non-authoritative with its least-closed sentinel, and a '
                  'native chapter link naming workflows §6 as the consuming owner. The source31 gap '
                  'is closed in these bytes.',
                  'p05 execution across ownership, unavailability, unselected exclusion, extent '
                  'distinctness, witness union, remedy coordinates, absence folding and gate '
                  'conservatism; plus check-workflow-projection.v3.py rc=0.',
                  'No repair is applied anywhere: preview/apply/recovery, trust, consent and '
                  'snapshot equality all remain separate product obligations. The synthetic host '
                  'projection demonstrates gate integration only.')
FW['FW-11'] = row([C + 'workflows-and-surfaces.md'],
                  'weakened safeguards / metric redistribution unchanged on 32.',
                  'the §12 numeric-comparison region is untouched by the delta.', 'Unexecuted.')
FW['FW-12'] = row([C + 'workflows-and-surfaces.md'], 'bounded review unchanged on 32.',
                  '§5 review brief untouched.', 'Design law only.')
FW['FW-13'] = row([C + 'workflows-and-surfaces.md', Wf + 'command-inventory.v3.json'],
                  'common registry unchanged on 32; no new public detail code is minted by the '
                  'repair law, which reuses REPAIR.CLOSED_WORLD_NOT_ESTABLISHED.',
                  'I verified the chapter states no new code is minted and the closed registry is '
                  'unchanged.', 'Registry closure is design law.')
FW['FW-14'] = row(['docs/coop/design-corrections/current-source-map.proposed.md'],
                  'real configuration corpus remains an implementation-qualification obligation on 32.',
                  'owner unchanged.', 'Nothing measured.')
FW['FW-15'] = row([C + 'workflows-and-surfaces.md'], 'policy authoring/test unchanged on 32.',
                  '§5 DSL untouched.', 'No authoring harness exists.')

# ---------------- 27 inherited residual ----------------
INH = {}
BASE_OWN = {
    'DR-001': ['docs/coop/design-corrections/current-source-map.proposed.md', C + 'README.md',
               A + 'report-asset-binding.v1.json'],
    'DR-002': [C + 'identity-and-evidence.md'],
    'DR-003': [C + 'security-and-lifecycle.md', C + 'identity-and-evidence.md'],
    'DR-004': [C + 'identity-and-evidence.md', C + 'native-evidence.md'],
    'DR-005': [C + 'identity-and-evidence.md', A + 'commit-recovery-plan.v1.json'],
    'DR-006': [C + 'identity-and-evidence.md', F + 'identity-schemas.v3.json'],
    'DR-007': [C + 'workflows-and-surfaces.md', C + 'native-evidence.md',
               F + 'evaluator-fault-contract.v1.md'],
    'DR-008': [C + 'identity-and-evidence.md', C + 'admission-and-qualification.md'],
    'DR-009': [C + 'identity-and-evidence.md', F + 'identity-model.v3.py'],
    'DR-010': [C + 'admission-and-qualification.md'],
    'DR-011': ['docs/coop/design-corrections/inherited-residuals.proposed.md',
               'docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json'],
}
TXT = {
    'DR-001': 'A current source/selector/claim map holds on 32.',
    'DR-002': 'Identity sections 2-5 unchanged on 32.',
    'DR-003': 'Unperformed by design on 32 and correctly not claimed.',
    'DR-004': 'Provider truth remains trusted extraction evidence on 32.',
    'DR-005': 'All 54 commit-recovery cases unexecuted on 32.',
    'DR-006': 'The closure law and digest-domain registry unchanged on 32.',
    'DR-007': 'Exact D9 branch/cause/result behaviour unchanged on 32. The published D9 successor '
              'carrying host-invariant remains an ASSIGNED implementation obligation of that unit, '
              'carried forward and not closed by this review.',
    'DR-008': 'No store exists on 32; retention is design law only.',
    'DR-009': 'Reproducibility across machines unchanged on 32; the ordering laws are aligned.',
    'DR-010': 'The seven boundary items of admission section 5 unchanged on 32.',
    'DR-011': 'Both owners unchanged on 32; all 30 nested residuals are disposed individually below.',
}
for k in BASE_OWN:
    INH[k] = row(BASE_OWN[k], TXT[k], 'owner files checked against my derived delta; suites re-run '
                 'where inputs changed.', 'Design law only; nothing applied.')

# the 16 DR-011-R rows, each with REAL current owners (RR31-01)
R16 = {
    'DR-011-R01': (['docs/coop/design-corrections/native/native-evidence.schemas.v2.json',
                    C + 'native-evidence.md', F + 'identity-schemas.v3.json'],
                   'FACT-PLANE. CoverageResultV3 with RC-0..RC-6, RequirementV2 and the closed '
                   'deficiency/cause registry are unchanged on 32, as are coveragePartitionLaw and '
                   'coverageTotality at retained Run closure.'),
    'DR-011-R02': ([F + 'fact-identity-policy.v2.json', C + 'identity-and-evidence.md'],
                   'FACT-IDENTITY. The policy is still reused by exact selector rather than '
                   'restated; the framed bodyIdentity preimage is unchanged on 32.'),
    'DR-011-R03': ([F + 'evaluator-composition-contract.v3.md', F + 'identity-schemas.v3.json'],
                   'C-2. plan2/exec-plan2 with the closed stage-spec record and the operation-token '
                   'ownership statement are unchanged on 32; the defective historical join remains '
                   'preserved history.'),
    'DR-011-R04': ([N + 'native-protocol.v3.md', C + 'security-and-lifecycle.md'],
                   'DELIVERY. Native protocol 3 / TS 2 and the security lifecycle core bridge remain '
                   'the explicit successors on 32.'),
    'DR-011-R05': ([N + 'native-protocol.v3.md', C + 'native-evidence.md'],
                   'Rust PC-7. Protocol major 3 with identity negotiation, reject-before-disclosure '
                   'ordering and the published transition table are unchanged on 32; no real '
                   'provider process is exercised.'),
    'DR-011-R06': ([C + 'identity-and-evidence.md'],
                   'EVIDENCE. identity-and-evidence remains the owning packet for proof outcomes, '
                   'retained verification and regeneration closure on 32.'),
    'DR-011-R07': ([C + 'identity-and-evidence.md', C + 'admission-and-qualification.md'],
                   'RETENTION. CD-RT-5 and the v28 posture are preserved on 32 and joined to the '
                   'evidence/D9 contract.'),
    'DR-011-R08': ([C + 'workflows-and-surfaces.md', F + 'evaluator-fault-contract.v1.md',
                    C + 'native-evidence.md'],
                   'D9. Closed host-owned termination with its observation-to-faultCause mapping is '
                   'unchanged on 32. The published D9 successor carrying host-invariant remains an '
                   'ASSIGNED implementation obligation, carried forward and not closed here.'),
    'DR-011-R09': ([C + 'identity-and-evidence.md', F + 'identity-schemas.v3.json'],
                   'R-1. Semantic IDs still exclude RequestId/ExecutionId, lifetime, credentials, '
                   'cache state, receipt timestamps and storage paths on 32.'),
    'DR-011-R10': (['docs/coop/design-corrections/inherited-residuals.proposed.md'],
                   'Blind consumer-B. Closable only by an actual fresh implementer litmus, which '
                   'this review is explicitly not. I read no consumer runtime, output or report, and '
                   'I claim no blind acceptance.'),
    'DR-011-R11': ([C + 'identity-and-evidence.md', C + 'security-and-lifecycle.md'],
                   'OPERABILITY G19. Durable commit, acknowledgements, recovery, retention pins, GC, '
                   'backup/import and availability are defined on 32 and remain measurement '
                   'obligations no design document discharges.'),
    'DR-011-R12': ([C + 'admission-and-qualification.md',
                    'docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json'],
                   'EVALUATION PROOF. Product proof/evidence/seal plus authenticated trusted '
                   'evaluator replay replace the v8/v13 lineages. All 30 nested residuals carry '
                   'individual dispositions below, with TCB-SCOPE-01 assessed once over 13.'),
    'DR-011-R13': ([C + 'workflows-and-surfaces.md'],
                   'VERSIONING. The workflow executable detector pivot, portable baseline and typed '
                   'multi-axis comparison still own this on 32.'),
    'DR-011-R14': ([C + 'admission-and-qualification.md', C + 'security-and-lifecycle.md'],
                   'CFG-6 / TM. Sealed inputs, identity/proof/custody, the explicit trusted '
                   'repository-code principal, storage and G19 supply the current threat-model '
                   'assumptions on 32. This is the same posture TCB-SCOPE-01 makes explicit.'),
    'DR-011-R15': ([C + 'workflows-and-surfaces.md', C + 'identity-and-evidence.md'],
                   'Trusted request context. ProjectId marker/registry/namespace and '
                   'RequestId/ExecutionId remain operationally explicit on 32.'),
    'DR-011-R16': ([C + 'admission-and-qualification.md'],
                   'Product authority. D-367 delegation and D-370/D-371 scope are preserved on 32, '
                   'admission section 5 dispositions all seven boundary items, and CD-RT-5 remains '
                   'binding.'),
}
for k, (owners, txt) in R16.items():
    present = [p for p in owners if os.path.isfile(
        os.path.join('/tmp/opensip-design-corrections/candidate-subject.v32', p))]
    INH[k] = row(present or owners, txt,
                 'owner paths resolved against the frozen32 snapshot and checked against my derived '
                 '31->32 delta; this replaces the empty currentOwnerFiles my v31 report carried.',
                 'Design law only; nothing applied, activated or graded.',
                 extra={'ownerPathsResolveInFrozen32': len(present) == len(owners),
                        'rr31_01Remediated': True})

# ---------------- 5 scoped owner ----------------
SC = {}
SCOPED = {
    'DR-201': ([C + 'workflows-and-surfaces.md', C + 'identity-and-evidence.md'],
               'Semantic correctness routing. The workflows chapter changed (new §6 repair law and '
               'the §8 glob link); the branch separation this row is about is unchanged, and the new '
               '§6 law is additive rather than a restatement of step/derivation DAG behaviour.'),
    'DR-202': ([A + 'commit-recovery-plan.v1.json', A + 'commit-recovery-readonly.v3.md',
                S + 'carrier-format.v3.md', S + 'carrier-dispatch.v3.json'],
               'Delivery/operations. None of these owners is in my 31->32 delta. All 54 recovery '
               'cases remain unexecuted and every qualification gate remains unperformed.'),
    'DR-203': ([C + 'workflows-and-surfaces.md'],
               'Prototype lessons routing. The chapter changed in §6/§8 only; this routing is '
               'unaffected.'),
    'DR-204': ([A + 'repository-file-inventory.v1.json', A + 'implementation-coverage.v1.json',
                A + 'implementation-normative-inputs.v3.json', A + 'implementation-planning-sources.v1.json',
                A + '14-repository-and-module-layout.md'],
               'V1/coop invariant coverage. Measured on frozen32: 12,898 files and 736,666,114 bytes; '
               '198 planned paths across 20 packages; 320 source-bound mappings; M0-M6; 54 planned '
               'recovery cases, 0 executed. The current architecture input layer is '
               'implementation-normative-inputs.v3 with 29 pins, every one resolving against '
               'frozen32, with layer2 and the original layer1 both preserved. The new work is '
               'carried by EXISTING crates/evaluator/src/policy.rs and crates/host/src/repair.rs; no '
               'new package or planned filename appears.'),
    'DR-205': ([A + 'repository-file-inventory.v1.json', A + '14-repository-and-module-layout.md'],
               'Small-core/components routing. Chapter 14 regenerated with the two existing module '
               'descriptions; package count and path count unchanged.'),
}
for k, (owners, txt) in SCOPED.items():
    r = row(owners, txt,
            'planning groups re-run (198 unique paths; 320 mappings / 54 planned cases), layer3 pins '
            'resolved, chapter 14 lines read.',
            'Routing assessed only. Not applied, not re-accepted, no grade.')
    r['disposition'] = 'ROUTING-ASSESSED-ONLY-NOT-APPLIED'
    SC[k] = r

O['arDispositions'] = AR
O['fwDispositions'] = FW
O['inheritedResidualDispositions'] = INH
O['scopedReviewOwnerDispositions'] = SC
json.dump(O, open(os.path.join(BASE, 'part2.json'), 'w'), indent=1, default=str)
for k in O:
    print('%-34s %d' % (k, len(O[k])))
empt = [k for k, v in INH.items() if not v['currentOwnerFiles']]
print('inherited rows with empty currentOwnerFiles:', empt)
