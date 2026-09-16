"""Assemble review.json for the final independent application review of application-stage.v46.
Per-item assessments are this reviewer's own; the unchanged portion cites the exact prior45 item plus verified byte identity."""
import json, hashlib, os
RT = '/private/tmp/opensip-design-corrections/application-review.v46/'
PK = '/private/tmp/opensip-design-corrections/application-stage.v46/'
S = PK + 'files/'
S45 = '/private/tmp/opensip-design-corrections/application-stage.v45.2/files/'
R = '/Users/sb/code/opensip-ai/opensip_arch/'
DC = 'docs/coop/design-corrections/'
MS = 'dab6e00fc3ccf82f015941bc767a10b18be9e6ca5f1c8598fa1fe9a4d05743f7'
def h(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
def load(p): return json.load(open(p))
prior = load(R + DC + 'reviews/application-review.v45/review.json')
PRIOR_SHA = h(R + DC + 'reviews/application-review.v45/review.json')
assert PRIOR_SHA == '6ff6e1858dd3b606a638b7c780ac2b9c4dce146799786849653831ea8040812f'
P = {k: load(RT + 'probes/out/' + k + '.json') for k in ['p05_row_gates', 'p06', 'p08', 'p09']}
rm46 = load(S + DC + 'readiness-row-map.v1.json'); rm45 = load(S45 + DC + 'readiness-row-map.v1.json')
qg = load(S + DC + 'qualification-gates.applied.v1.json')
ir = load(S + DC + 'inherited-residuals.applied.v1.json')
ev = load(S + DC + 'evaluation-residual-dispositions.applied.v1.json')
own = load(S + DC + 'review-owner-dispositions.v1.json')
app = load(S + DC + 'application.v1.json')
m46 = load(PK + 'application-subject.v46.json')
m45 = load(R + DC + 'reviews/application-subject.v45.json')
f45 = {e['path']: e['sha256'] for e in m45['files']}; f46 = {e['path']: e['sha256'] for e in m46['files']}
def same(path): return f45.get(path) == f46.get(path)
TCB13 = ["RES-EP13-02", "RES-EP13-04", "RES-EP13-12", "RES-EP13-13", "RES-EP13-16", "RES-EP13-18", "IR-EP13-NB-01", "IR-EP13-NB-03", "IR-EP13-NB-04", "AX6", "AX9", "MD5", "RX2c"]
RM = DC + 'readiness-row-map.v1.json'

# ---------- condition-2 rows ----------
p05 = {r['row']: r for r in P['p05_row_gates']['rows']}
prior_rows = {r['id']: r for r in prior['condition2RowAssessments']}
rows45 = {r['id']: r for r in rm45['rows']}
SIX = {
 'DR-103': ('DR-G08', 'Snapshot register 08 line 291 (DR-103 historical cell): "admission execution remains G07/G08/G15". G08 is root/index/core/component/repair trust survival (qualification-gates.applied.v1.json#/items/7, security contract), which exercises DR-103\'s signed metadata/index/lock/signature-preimage surface. Now routed with G07/G15.'),
 'DR-114': ('DR-G12', 'G12 is the doctor gate ("Doctor and purge are safe, stable, and honest"; productExpansion "Doctor report-only no source/grant/trust write..."), and register line 302 says "G12/G32 execution remains". DR-114 owns doctor schema/exit/redaction/consented probes. Now routed with G32.'),
 'DR-117': ('DR-G09, DR-G14, DR-G16, DR-G23', 'Admission §5 item 4 (snapshot line 344): "G09/G21/G29/G30 must exercise these refusal and authority boundaries", so G09 is named by the row\'s own successor. Register line 305 routes the fourteen enforcement-evidence classes to exactly DR-G09, G14, G16, G21, G23, G29, G30, and the routed set now equals that list. Adding G14/G16/G23 retains the historical EE-class measurement owners as mandatory; it narrows no gate and changes no contract.'),
 'DR-119': ('DR-G14', 'The retained D-008 fragment (fragmentSha256 84e6483d...) and register line 307 both say "closure evidence per role at DR-G14 qualification". G14\'s acceptance ("Supported language analyzers are self-contained") restates DR-119\'s rule.'),
 'DR-123': ('DR-G01, DR-G02, DR-G05, DR-G12', 'The retained D-009 fragment (53653dc8...) and register line 311 say "evidence at DR-G01..G05 and DR-G12" (G17 is separately re-entered by D-372). The routed set now contains G01-G05, G12 and G17, plus G06/G20/G28 from the current contracts.'),
 'DR-124': ('DR-G09', 'Register line 312 (DR-124 historical cell; compatible inherited /rows/11) says "G09/G18/G19 execution remains". Now routed with G18/G19.'),
}
c2 = []
for i, r in enumerate(rm46['rows']):
    rid = r['id']; pr = p05[rid]; old = rows45[rid]
    others_same = {k: v for k, v in r.items() if k != 'releaseGates'} == {k: v for k, v in old.items() if k != 'releaseGates'}
    added = sorted(set(r['releaseGates']) - set(old['releaseGates'])); removed = sorted(set(old['releaseGates']) - set(r['releaseGates']))
    incidental = {'compatibleOrAdditionalInheritedAccountHits': pr['missingVsInherited'], 'citedSectionHits': pr['missingVsSectionExact']}
    entry = {'id': rid, 'selector': RM + '#/rows/%d' % i, 'releaseGates46': r['releaseGates'], 'addedIn46': added, 'removedIn46': removed,
             'otherRowFieldsByteEqual45': others_same, 'independentGradeRecorded': r['independentGrade'], 'productQualified': r['productQualified'],
             'gateCrossCheck': {'missingVsHistoricalRegisterCell': pr['missingVsRegister'], 'missingVsRowSourceText': pr['missingVsRowText'], 'unroutedIncidentalMentions': incidental}}
    if rid in SIX:
        g, basis = SIX[rid]
        entry['assessment'] = 'ACCEPT-DESIGN supported; APP45-S1 row account CORRECTED (added %s)' % g
        entry['basis'] = basis + ' Design substance, successors and all other row fields are byte-identical to v45; the prior45 substantive design basis (%s) remains valid and I re-checked it against the exact snapshot selectors.' % prior_rows[rid]['assessment']
    else:
        entry['assessment'] = 'ACCEPT-DESIGN supported'
        entry['basis'] = 'Row record byte-identical 45->46 (probe p03). Prior45 basis, which I verified against the unchanged governing contracts and selectors and adopt as my own assessment: ' + prior_rows[rid]['basis']
    if incidental['compatibleOrAdditionalInheritedAccountHits'] or incidental['citedSectionHits']:
        entry['incidentalMentionJudgement'] = 'Unrouted gate tokens are incidental and not per-row obligations: G13 appears as the historical G13 roster/matrix (ACT-G13-ROSTER, "G13 alone never authorizes release"); workflows §8 names DR-G17/DR-G20 only as general host-exception/renderer qualification; S11 names the OD-112-4 G08 waiver (owned by DR-112, which routes G08); DR-103 /rows/1 cites "D-006 decided DR-G01..G05 only" about DR-115; DR-112 "G15.SIGNED" is a reference evidence-target clause of the historical g15 unit, not a gate route; DR-131 G17/G19/G26 are preview non-advertisement/not-G19 history, with G26 routed on DR-122.'
    c2.append(entry)

# ---------- inherited residuals ----------
prior_inh = {r['id']: r for r in prior['inheritedResidualAssessments']}
inh = []
coll = [('parents', x) for x in ir['parents']] + [('residuals', x) for x in ir['residuals']]
for k, (cname, x) in enumerate(coll):
    idx = ir[cname].index(x)
    e = {'id': x['id'], 'selector': DC + 'inherited-residuals.applied.v1.json#/%s/%d' % (cname, idx), 'proposedDesignGrade': x.get('designGrade'),
         'literalDesignReviewDisposition': x['independentDisposition']['disposition'], 'literalDispositionByteEqualToDesignReview': True,
         'appliedByDesignReview': x['independentDisposition'].get('appliedByThisReview'), 'finalApplicationOutcomeGrantedByDesignReview': x['independentDisposition'].get('finalApplicationOutcomeGranted'),
         'assessment': prior_inh[x['id']]['assessment'], 'basis': 'My assessment on the unchanged record and governing owners (literal design disposition equal, probe p08). Prior45 basis verified and adopted: ' + prior_inh[x['id']]['basis']}
    if x['id'] == 'DR-011-R10':
        e['changeIn46'] = '/residuals/9/dispositionText now says the independent blind-origin continuation completed on source45, blind but not a fresh origin (APP45-ADV-03). The literal design-review disposition (CONDITION-1-OBLIGATION-RETAINED-ASSESSED; "OPEN: this nonblind source45 review cannot close the fresh blind implementer litmus") is preserved unchanged and remains correct for that nonblind review. Closure rests on blind-review.json#/verdict ACCEPT-RECONSTRUCTABLE (7ee66bb5), origin "continuation; independence not claimed anew".'
    if x['id'] in ('DR-007', 'DR-011-R08'):
        e['carriedCrossUnitObligation'] = 'D9-SUCCESSOR-ARTIFACT present and identical on both rows; not discharged (see d9App1Assessment).'
    if x['id'] == 'DR-011-R12':
        e['jointContingency'] = 'Reopens with TCB-SCOPE-01 (record mentions TCB-SCOPE-01).'
    inh.append(e)

# ---------- evaluation residuals ----------
prior_ev = {r['id']: r for r in prior['evaluationResidualAssessments']}
evs = []
for i, x in enumerate(ev['items']):
    evs.append({'id': x['id'], 'selector': DC + 'evaluation-residual-dispositions.applied.v1.json#/items/%d' % i, 'literalDesignReviewDispositionByteEqual': True,
                'authorGradeStillPending': True, 'tcbScope01Dependent': x['id'] in TCB13,
                'assessment': prior_ev[x['id']]['assessment'], 'basis': 'Record byte-identical 45->46; literal design disposition equal (p08). My assessment adopts the verified prior45 basis: ' + prior_ev[x['id']]['basis']})

# ---------- AR / FW ----------
ars = [{**{k: v for k, v in a.items() if k in ('id', 'contract', 'literalDesignDisposition')}, 'literalDispositionByteEqual': True, 'assessment': a['assessment'],
        'basis': 'Contract bytes and correction-crosswalk.applied.v1.json byte-identical 45->46; literal NO-NEW-ISSUE preserved (p08: 31 crosswalk rows equal). Verified prior45 basis adopted: ' + a['basis'] + (' APP45-S1 is now corrected, so gate-routing precision is no longer an open qualification of AR-15.' if a['id'] == 'AR-15' else '')} for a in prior['arAssessments']]
fws = [{**{k: v for k, v in a.items() if k in ('id', 'owner', 'literalDesignDisposition')}, 'literalDispositionByteEqual': True, 'assessment': a['assessment'],
        'basis': 'Current-source-map row and design-review owner routing unchanged 45->46; nothing executed. ' + a['basis']} for a in prior['fwAssessments']]

# ---------- scoped owners ----------
prior_own = {r['id']: r for r in prior['scopedReviewOwnerAssessments']}
owns = []
for i, rec in enumerate(own['records']):
    b = prior_own[rec['id']]['basis']
    if rec['id'] == 'DR-204':
        b = 'V1/coop invariant coverage: design review verified all 6,264 pins; in 46 I verified every staged file hash, all 12 prerequisite path/hash pairs in the bound and input receipts, the workflows report leaf delta and recording delta, the unchanged five ledgers, and the per-row gate routing for all 28 rows (APP45-S1 corrected, no remaining omission). APP45-ADV-01 is corrected.'
    owns.append({'id': rec['id'], 'selector': DC + 'review-owner-dispositions.v1.json#/records/%d' % i, 'literalDesignDisposition': 'ROUTING-ASSESSED-ONLY-NOT-APPLIED (both authority flags false)',
                 'literalDesignReviewFieldsPreservedAsSubset': True, 'proposedApplicationDisposition': rec.get('applicationDisposition'),
                 'assessment': 'ACCEPT-DESIGN supported (subject-specific, this review)', 'basis': b, 'historicalGradeExtended': False})

# ---------- gates ----------
mem46 = {}; mem45 = {}
for r in rm46['rows']:
    for g in r['releaseGates']: mem46.setdefault(g, []).append(r['id'])
for r in rm45['rows']:
    for g in r['releaseGates']: mem45.setdefault(g, []).append(r['id'])
prior_g = {g['id']: g for g in prior['qualificationGateAssessments']}
gates = []
for i, it in enumerate(qg['items']):
    gid = it['id']
    gates.append({'id': gid, 'selector': DC + 'qualification-gates.applied.v1.json#/items/%d' % i, 'owner': it['owner'], 'currentContract': it['currentContract'],
                  'routedByRows46': mem46.get(gid, []), 'rowsAddedIn46': sorted(set(mem46.get(gid, [])) - set(mem45.get(gid, []))),
                  'assessment': 'DESIGN-CONTRACT MAPPING ACCEPTABLE; REQUIRED PRODUCT QUALIFICATION UNPERFORMED',
                  'qualified': it['qualified'], 'demonstrated': it['demonstrated'], 'implementationHarnessAuthored': it['implementationHarnessAuthored'],
                  'note': 'Gate item byte-identical 45->46. ' + prior_g[gid]['note']})

# ---------- F ----------
fs = [{**{k: v for k, v in f.items() if k in ('id', 'severity', 'area', 'rootPackage13Standing', 'source45Disposition')},
       'assessment': 'ACCOUNTED; provenance intact; not regraded by this application', 'basis': 'Design review 427ae73e unchanged and no application record in 46 grades or re-verifies F items. Prior45 account verified and adopted: ' + f['assessment']} for f in prior['fDispositionAssessments']]

# ---------- prior findings ----------
pv1 = []
for f in prior['priorApplicationFindingDispositions']:
    d = {'id': f['id'], 'priorSeverity': f['priorSeverity'], 'selectors': f['selectors']}
    fid = f['id']
    if fid == 'M-1':
        d['disposition'] = 'RESOLVED'; d['finding'] = 'application.v1.json and readiness-row-map.v1.json are staged after-images (f37142c8, 493e7f40) applied by the finalizer. Probe p07: 47 staged Markdown files, 541 local links (whole files, including COORDINATOR history), 538 resolve with anchors, 3 target the activation the finalizer writes last, 0 failures.'
    elif fid == 'M-2':
        d['disposition'] = 'RESOLVED'; d['finding'] = 'All 28 rows keep independentGrade ACCEPT-DESIGN with effectiveWhen bound to activation; register condition 2 agrees. With APP45-S1 corrected the per-row accounts are complete, so this is no longer only "in form".'
    elif fid == 'M-5':
        d['disposition'] = 'RESOLVED'; d['finding'] = 'G06/G11 stay routed (DR-106 G06/G11; DR-109/113/124 G11). The recurrence APP45-S1 is corrected: 12 memberships across DR-103/114/117/119/123/124; p05 finds no remaining register-cell, row-text or D-fragment omission on any of the 28 rows.'
    elif fid == 'M-6':
        d['disposition'] = 'RESOLVED'; d['finding'] = 'DR-106 admission §2/§3 + S9.1 + G06/G11; DR-109/113/124 G11; DR-117 admission §5 items 1-7 = file02 lines 287-293 (re-read) and now routes G09 named by item 4 plus the retained EE-class owners; DR-122 explicitReentryAct, workflows §8 and command-inventory.v3 SARIF on exactly default/analyze/audit/repair-verify (re-measured), G17 routed; DR-130 S16 5 preservations / 5 distinctions / 6 prohibitions = file05 lines 67-81 (re-read), S16 gates equal the routed set.'
    elif fid == 'S-3':
        d['disposition'] = 'RESOLVED'; d['finding'] = 'Executed by this review: generate-current-design-catalog.py --check on staged classification/catalogue prints PASS. See APP46-ADV-01 about the self-referential labels.'
    elif fid == 'A-2':
        d['disposition'] = 'RETAINED LIMITATION'; d['finding'] = 'Working-tree delivery only (D-372 "Delivery and reversal": commit and push are not part of this task). The committed tree alone must not be assumed to contain the delivered design; A-2 is not closed by committing. Git tracking was not measured: the harness denied a read-only git ls-files call.'
    else:
        d['disposition'] = f['disposition']; d['finding'] = 'Governing bytes unchanged 45->46 except as noted in the delta assessment; re-verified: ' + f['finding']
    pv1.append(d)
p45 = [
 {'id': 'APP45-S1', 'priorSeverity': 'SHOULD', 'disposition': 'RESOLVED', 'selectors': [RM + '#/rows/2,12,14,16,20,21/releaseGates'], 'finding': 'Exactly the 12 memberships were added (p03: 39 leaf diffs, all inside those six releaseGates arrays, sorted; no other field of any row changed; total memberships 118 -> 130). Each addition is justified by the row\'s own source (see condition2RowAssessments). Independent p05 over all 28 rows, extended to compatible inherited architecture-application rows and cited sections, finds no further omission. No other applied record lists per-row gates (gate map items carry no row lists; register per-row table carries dispositions only).'},
 {'id': 'APP45-ADV-01', 'priorSeverity': 'ADVISORY', 'disposition': 'RESOLVED', 'selectors': ['docs/coop/design-corrections/workflows/workflows-report.v1.json (b607db8a)', 'support/workflows-recording-delta.v1.json', 'application.v1.json#/workflowRecordingDelta', 'application.v1.json#/acceptedDesignReproduction/outputPolicy'], 'finding': 'Staged report differs from the snapshot report in exactly one leaf /sourceSha256/source-pins.v1.json 6e75029f -> 9a802377, which equals the staged workflows ledger. The v46 rerun receipt reportSha256 is b607db8a and the staged after-image stayed byte-identical. No ledger pins the report. The accepted report stays in the snapshot; validation-summary.applied keeps it explicitly resolved against candidate-subject.v45 (observation only).'},
 {'id': 'APP45-ADV-02', 'priorSeverity': 'ADVISORY', 'disposition': 'RETAINED EDITORIAL LIMITATION (accepted)', 'selectors': ['docs/coop/design-corrections/README.md historical chronology'], 'finding': 'Unchanged bytes; the current header, D-372 body and register are explicit. Non-blocking.'},
 {'id': 'APP45-ADV-03', 'priorSeverity': 'ADVISORY', 'disposition': 'CORRECTED FOR ITS THREE SELECTORS; SAME CLASS REMAINS ELSEWHERE (APP46-ADV-02)', 'selectors': ['08-decision-and-readiness-register.md line 398', 'COORDINATOR-DECISIONS.md line 24077', 'inherited-residuals.applied.v1.json#/residuals/9/dispositionText'], 'finding': 'All three now state the independent blind-origin continuation. Four other current occurrences of "fresh blind" remain.'},
 {'id': 'APP45-ADV-04', 'priorSeverity': 'ADVISORY', 'disposition': 'DOCUMENTED (accepted)', 'selectors': ['application.v1.json#/interruptedCopyRecovery', 'finalize-application.v1.py lines 40-56'], 'finding': 'The manual, fail-closed recovery procedure is recorded; the finalizer still refuses torn bytes before activation. No atomicity claimed.'},
 {'id': 'APP45-ADV-05', 'priorSeverity': 'ADVISORY', 'disposition': 'ACCOUNTED (accepted)', 'selectors': ['COORDINATOR-DECISIONS.md D-372 body lines 24073-24201'], 'finding': 'I read the applying body: identity profile-3/profile-2 and §8/§9 SARIF wording agree with the accepted contracts; the only 46 change is the evidence-sentence wording.'},
 {'id': 'APP45-ADV-06', 'priorSeverity': 'ADVISORY', 'disposition': 'QUALIFIED (accepted)', 'selectors': ['accepted-review-advisories.v1.json#/blindItems A-c2', 'inherited-residuals.applied.v1.json#/parents/6,/residuals/7'], 'finding': 'Current carriage verified: A-c2 applicationAccount routes to DR-007/DR-011-R08; the two carriedCrossUnitObligation records are equal.'},
]

advisories = [
 {'id': 'APP46-ADV-01', 'severity': 'ADVISORY', 'title': 'Generated catalogue labels are now self-referential for 16 current-architecture paths',
  'selectors': ['docs/catalog/current-design.md lines 22,23,25,28-40', 'docs/operations/document-classification.v1.json rows for the 16 paths: currentNavigationReferences == ["docs/catalog/current-design.md"], referencedByCount 0', 'docs/operations/generate-current-design-catalog.py line 16'],
  'measured': 'p08: exactly 16 current/architecture rows (attempt-custody.schema.v1.json, carrier-fault-cases.v1.json, commit-recovery-readonly.v3.md, implementation-normative-inputs.v1..v13.json) are referenced only by the generated catalogue itself. v45 labelled them NO LINK RECORDED; v46 LINK RECORDED. The generator --check passes and the 50 paths are unchanged.',
  'assessment': 'The label is literally true but no longer distinguishes paths that no other current navigation document links; after one regeneration every catalogued path is self-linked. The frozen package does not explain this change (only the external root delta record does). No authority, grade or normative claim depends on it. A later documentation pass should exclude the generated catalogue from its own navigation sample or define the label.'},
 {'id': 'APP46-ADV-02', 'severity': 'ADVISORY', 'title': '"Fresh blind" wording remains in four current places after the APP45-ADV-03 correction',
  'selectors': ['docs/v2/architecture/08-decision-and-readiness-register.md lines 383-384 ("fresh blind consumer B", unified section)', 'docs/coop/design-corrections/README.md line 3 ("the fresh blind consumer result", current header)', 'docs/START-HERE.md line 47 ("independent design and fresh blind consumer reviews")', 'docs/coop/design-corrections/validation-summary.applied.v1.json#/priorReviewLimitation ("fresh blind evidence")'],
  'assessment': 'Same class as APP45-ADV-03, which listed only three selectors; those are corrected. The pinned blind review, R10 disposition, register condition 1 and D-372 evidence sentence disclose the continuation, and "fresh blind consumer B" is the program role name. The corrections.json disposition CORRECTED-IN-APPLICATION is accurate for its selectors but not class-complete. Non-blocking editorial precision.'},
 {'id': 'APP46-ADV-03', 'severity': 'ADVISORY', 'title': 'Root 45->46 delta record accounts the files layer only',
  'selectors': ['docs/coop/design-corrections/reviews/root-application46-delta.v1/delta.json (4cb7d03c)', 'application-subject.v46.json#/support'],
  'measured': 'p02: files 187 identical / 10 changed / 0 added / 0 removed (delta.json agrees with both manifests); beforeImages 76 identical; support 242 identical, 1 changed (support/staged-reference-checks.v1.json c588cfcd -> 82768a93), 76 added (reference-rerun.v46, root-application46-corrections.v1, application46-review-binding.v1, workflows-recording-delta, retention tools), 3 removed (package-root accepted-source-application-delta.json, assembly-metadata.json, bound-review-receipt.json of the v45 package). No applied file references the removed names; the v46 bound receipt (17905c87) is support/application46-review-binding.v1/bound-review-receipt.json and equals application.v1.json#/boundReceiptSha256; the v45 package remains retained (application-source.v45.tar.gz row).',
  'assessment': 'The support changes are sound. The delta record honestly reports the failed nine-file guard, which is not a pass. My own diff finds the ten-file delta correct. A future delta record should also state the support-layer delta.'},
]

d9 = {
 'historicalAssessment': 'Actual Claude bounded assessor, session 9a209c44-b765-43a0-bef9-044e308f57fc, claude-opus-5, 57 turns (support/d9-obligation-evidence/actual-claude/custody.json), scoped only to the D9 obligation; it is not a Grok session. It raised D9-APP-1 SHOULD for row-specific visibility, executed no integration checks and did not conduct a final application review.',
 'codexQualifiedAssessment': 'coauthor-assessment.v20-d9-application.v1.json rootQualifications: the broad no-record premise was false because CB-ADV-4 was dynamically copied by the source20 assembler; the valid improvement is row-specific carriage; IMPLEMENTATION-PHASE ARTIFACT PUBLICATION is a planning classification, not verbatim phase authority or a restriction on the user authorization; the abbreviated native schema hash was corrected.',
 'currentGeneratedRecords': 'Assessed on the actual generated applied record, not builder strings: carriedCrossUnitObligation D9-SUCCESSOR-ARTIFACT exists on exactly inherited-residuals.applied.v1.json#/parents/6 (DR-007) and #/residuals/7 (DR-011-R08), byte-equal, on no other row. owedBy "the D9 exit-contract unit"; owed: successor to d9-exit-contract.v1.14.json carrying faultCause host-invariant mapped to existing SYSTEM.OUTCOME.ILLEGAL_STATE; inheritedArtifactUnchanged 8dd33038 verified; notDischargedBy names Condition 1 MET, ACCEPT-DESIGN on both rows, the application, activation and the final independent application review. Current carriage also by blind A-c2 applicationAccount. CB-ADV-4 rationale is historical (APP45-ADV-06).',
 'selectorsVerified': ['native-evidence.schemas.v2.json 2d37b810 /x-opensip-public-route-registry/successorArtifactObligation resolves; whatIsNotOwed "Nothing in the product source"', 'common.schema.json b7b25d5e /$defs/D9FaultCause = 12 members (inherited 11 + host-invariant)', 'd9-exit-contract.v1.14.json 8dd33038 faultCause enum = 11 members without host-invariant', 'check-integration.py 6102bfdf lines 381-394 assert the inherited omission, the selected extension and ILLEGAL_STATE vocabulary', 'workflows-and-surfaces.md line 1362 maps host-invariant'],
 'selectedCurrentCompositionComplete': True,
 'futureOwningUnitArtifactPublicationIntegrationQualificationComplete': False,
 'phaseLabel': 'Planning classification only; not a normative phase requirement and not a new restriction on the architecture authorization.',
 'designLevelBlocker': False,
 'disposition': 'D9-APP-1 RESOLVED in the current generated records. The D9 successor-artifact obligation remains LIVE, MANDATORY, CROSS-UNIT and UNDISCHARGED. Condition 1 MET, ACCEPT-DESIGN, activation and this review do not discharge it.'
}
tcb = {
 'id': 'TCB-SCOPE-01', 'assessedOnceAsOneAssumption': True,
 'position': 'ACCEPTED AS AN EXPLICIT PRODUCT SCOPE ASSUMPTION: not rejected and not changed',
 'assumption': 'Authenticated selected in-process host/evaluator code is trusted; providers and inert inputs are untrusted; adversarial code sharing the process is outside the product threat model.',
 'dependentRows': TCB13, 'dependentRowCount': 13,
 'dependentRowReconciliation': 'application.v1.json#/sharedTrustedCodeAssumption/acceptedDesignAccount is byte-equal (as JSON) to claude-independent-design.v45 review.json#/sharedAssumptionTCBSCOPE01, and rootDesignAccount is equal to it as well (source codex design-assent.v45 #/sharedAssumption, 36830f6e). The 13 IDs equal exactly the evaluation-residual-dispositions.applied.v1.json items that mention TCB-SCOPE-01 (p09), and DR-011-R12 also mentions it.',
 'basis': ['Admission §5 items 3-5 (snapshot lines 343-345): providers produce typed facts/Coverage only; no untrusted native/WASM admitted; no imperative contributions, hooks or root-parser extensions.', 'Security S10: repository-code is a separately authorized trusted principal, not a plugin admission path.', 'Native §9/§9.7: provider process and wire boundaries; the pre-analysis closedWorld is host-minted from published law with no provider-authored member.', 'Gate map DR-G21 does not claim security confinement; G02/G07/G09/G21/G22 remain unperformed.', 'Codex rootTrustAssessment agrees: one assumption with 13 joint dependents that neither repairs historical attacks nor proves runtime containment.'],
 'sourceReviewerGraded': False,
 'notClaimed': ['repair of historical attacks (AX6/AX9/MD5/RX2c and RES/NB limits remain historical)', 'in-process adversarial containment', 'native, host or platform qualification', 'an implemented authenticated closure/TCB inventory'],
 'consequence': 'If TCB-SCOPE-01 is rejected or changed, all thirteen dependents and DR-011-R12 reopen jointly. It is one assumption, not thirteen independent successes.',
 'effective': 'Only through the finalizer-verified D-372 activation that binds this exact review.'
}

counts = {'condition2Rows': 28, 'condition2RowsUnchanged': 22, 'condition2RowsCorrectedIn46': 6, 'addedGateMemberships': 12, 'totalGateMemberships46': sum(len(r['releaseGates']) for r in rm46['rows']),
          'inheritedResiduals': 27, 'evaluationSubresiduals': 30, 'tcbDependents': 13, 'arItems': 16, 'fwItems': 15, 'scopedOwners': 5, 'productGatesUnperformed': 32,
          'plannedRecoveryCasesUnexecuted': 54, 'fDispositions': 14, 'blindAdvisories': 16, 'designAdvisories': 2, 'historicalClaudeV13Advisories': 2,
          'priorApplicationV1Findings': {'must': 7, 'should': 6, 'advisory': 2}, 'priorApplication45Findings': {'should': 1, 'advisory': 6},
          'manifestEntries': {'files': 197, 'beforeImages': 76, 'support': 322}, 'newMust': 0, 'newShould': 0, 'newAdvisories': 3}

review = {
 'schema': 'opensip.final-application-review.v46.v1',
 'verdict': 'ACCEPT',
 'subjectManifestSha256': MS,
 'subjectManifestPath': PK + 'application-subject.v46.json',
 'retainedManifestPath': m46['retainedManifestPath'],
 'reviewer': {'vendor': 'claude', 'model': 'claude-opus-5', 'role': 'fresh final independent application review origin for application-stage.v46', 'authoredSubjectBytes': False, 'resumedSessions': 'none (no author, design, blind, coauthor or application45 session)', 'agentsUsed': False, 'privateSessionLogsRead': False},
 'standing': 'Final independent application review of the complete application-stage.v46 package. ACCEPT is design/application acceptance for the finalizer only; it grants no implementation authorization, product qualification, commit, push or publication, and discharges no carried obligation.',
 'verdictBasis': 'APP45-S1 is resolved exactly and completely. The full 45->46 ten-file delta is correct. All 595 manifest entries verify, normative bytes are unchanged, and prerequisite reviews, reference rerun, finalizer, links, generator, inventory, D9 carriage and TCB-SCOPE-01 are sound. Remaining items are three non-blocking advisories.',
 'newMustIssues': [], 'newShouldIssues': [], 'advisories': advisories,
 'priorApplicationReview': {'path': DC + 'reviews/application-review.v45/review.json', 'sha256': PRIOR_SHA, 'verdict': prior['verdict'], 'summaryCountNote': 'Its actual arrays identify 22 otherwise acceptable rows and 6 gate-routing-defective rows.'},
 'priorApplication45FindingDispositions': p45,
 'priorApplicationFindingDispositions': pv1,
 'delta45to46Assessment': {
   'manifests': {'v45': '948d9bdd50169ad54871b6816d7f970a2f203fd9b1e84b7bea87dcc5c9ca6757', 'v46': MS},
   'files': '187 identical, 10 changed, 0 added, 0 removed; root delta.json agrees with both manifests (p02).',
   'correctionBeforeImages': 'All seven support/root-application46-corrections.v1/before/* equal the v45 staged after-images.',
   'perFile': {
     RM: 'Only the six releaseGates arrays (39 leaves, 12 added IDs, sorted).',
     DC + 'inherited-residuals.applied.v1.json': 'One leaf: /residuals/9/dispositionText (APP45-ADV-03); literal design disposition unchanged.',
     DC + 'application.v1.json': '11 leaves: applicationSubject/finalIndependentApplicationReview/outcomeAuthority paths -> v46; appliedRecords/0,3,6 hashes equal the staged after-images; boundReceiptSha256 17905c87 equals the v46 bound receipt; added interruptedCopyRecovery, priorApplicationReview (6ff6e185, CHANGES_REQUIRED), workflowRecordingDelta; outputPolicy sentence.',
     DC + 'accepted-review-advisories.v1.json': 'One leaf: added priorApplicationReviewAccount equal to corrections.json.',
     DC + 'workflows/workflows-report.v1.json': 'One leaf: embedded workflows ledger hash 6e75029f -> 9a802377.',
     'docs/v2/architecture/08-decision-and-readiness-register.md': 'One line: condition 1 continuation wording.',
     'docs/coop/COORDINATOR-DECISIONS.md': 'One line: D-372 exact-evidence wording.',
     'docs/catalog/current-design.md': '16 labels NO LINK RECORDED -> LINK RECORDED; same 50 paths; generator --check PASS (APP46-ADV-01).',
     'docs/operations/document-classification.v1.json': '+188 rows (all evidence/artifacts), 38 changed rows (8 sha256 = the changed files, 31 currentNavigationReferences); counts sum 135406; path set and hashes equal the inventory.',
     'docs/operations/document-inventory.v1.json': 'fileCount 135406 (+188); workingTreeDelta.contentPaths 126203 (+188), excludedPaths 4 (activation, NEXT-REVIEW.md, two inventories), lateEvidencePrefix application-review.v46/. 161 application-review.v45 rows and 27 other added rows are hash-exact against live bytes; every staged path row carries its after-image hash; no post-freeze artifact (v46 retained manifest, root delta record, v46 review, activation) is inventoried.'},
   'failedGuard': 'The root ad-hoc nine-file guard failed and is not treated as a pass; my independent diff establishes the actual ten-file delta.',
   'normativeChange': False},
 'condition2RowAssessments': c2,
 'inheritedResidualAssessments': inh,
 'evaluationResidualAssessments': evs,
 'sharedTrustedCodeAssumptionAssessment': tcb,
 'd9App1Assessment': d9,
 'arAssessments': ars, 'fwAssessments': fws, 'scopedReviewOwnerAssessments': owns,
 'qualificationGateAssessments': gates,
 'gateLanguageReconciliation': 'Register line 342 D-372 preface: G06/G11 inherited blockers have accepted prospective dispositions; G10 uses TS major2/Rust major3; G17 reactivated for the four SARIF commands. Historical cells (lines 351, 355, 356) stay verbatim under historical column labels. The gate map is byte-identical 45->46; only row memberships changed.',
 'fDispositionAssessments': fs,
 'designAdvisoryAccounts': prior['designAdvisoryAccounts'],
 'blindAdvisoryAccounts': [{**a, 'reviewedIn46': 'accepted-review-advisories.v1.json#/blindItems unchanged 45->46 (only priorApplicationReviewAccount added); account accepted.'} for a in prior['blindAdvisoryAccounts']],
 'prerequisites': {
   'designSubject': {'path': DC + 'reviews/candidate-subject.v45.json', 'sha256': '8b4efbb04d9e25126ec7955931cf364f7013b3710a45c48bae8bc563a0c82155', 'files': 12920},
   'independentDesignReview': {'sha256': '427ae73e715799a5a1375d231d8d5e1022c7eb11c95555b4cf9fd93f79af1f6c', 'verdict': 'ACCEPT', 'origin': '85a08aec (nonauthor independent-origin successor; not fresh-origin)', 'scope': 'Carries 27 inherited, 30 evaluation, 16 AR, 15 FW and 5 scoped owners as literal dispositions with appliedByThisReview false and finalApplicationOutcomeGranted false; TCB-SCOPE-01 NOT REJECTED, final adjudication not granted. No grade is inferred from it.'},
   'codexCoauthorAssent': {'sha256': '36830f6e4fac4d21e78949ee578930b2e1e95fc87c1289cf67690dee7bb10eef', 'rootDesignAssent': True, 'finalApplicationGranted': False, 'implementationAuthorized': False, 'limitationCorrect': True},
   'blindConsumerB': {'sha256': '7ee66bb559488109a51d2c64eca8e48c93db7b830a071947e1eaf695c79ac2f1', 'verdict': 'ACCEPT-RECONSTRUCTABLE', 'origin': '9d3dfb70 (continuation; independence not claimed anew)', 'codexBlindAssessment': 'd71b8942'},
   'receiptPairsVerified': 12, 'receiptPairFailures': 0},
 'referenceRerunAssessment': {
   'record': 'support/staged-reference-checks.v1.json (82768a93) and support/reference-rerun.v46',
   'procedure': 'validate.py verifies all 12920 snapshot entries, copies the snapshot, overlays the 197 staged files, runs run-application-reference-suites.py and asserts no staged after-image changed.',
   'commands': '7 command receipts, exit 0; every source hash equals the snapshot; stdout/stderr hashes equal the retained files.',
   'vs45_2': '60/60 files; 54 byte-identical; 6 differ only in scratch-root paths.',
   'vsAcceptedExecution': 'foundation.json, five foundation reports, security.json and integration.json byte-equal; workflows.json differs only in reportSha256 bc84b7dc -> b607db8a; evaluator3 report differs in scratch paths and two path-bearing stdout hashes.',
   'previous45_2RerunRetainedWithOriginalScope': True},
 'v12A1CountAccount': {'selectedMeasurement': 'identity-check-counts.v45.json (e25de4bd): 1596 passing calls, 1584 distinct IDs, 12 duplicate extra instances', 'independentRecount': 'p09 recount of support/reference-rerun.v46/foundation/identity-report.json (byte-equal to accepted 6de40d1c): 1596 calls, 0 non-pass, 1584 distinct, closed-closure x7 and exact-version-closure x7 = 12 extra.', 'applicationSummary': 'application.v1.json#/referenceEvidenceSummary 2006/1596/1584/12 matches; accepted frozen summary 43f3eb80 (2000) preserved.', 'historicalV12': '767/757/10 belongs to v12 only.'},
 'v12A2Reproduction': {'commands': 7, 'result': 'p10: original record 5dc0de60 verified; for all 7 commands replacing the single historical absolute source prefix /private/tmp/opensip-design-corrections/source44-closed-world-successor.v1/source/ with the relative source and each recordedOutput with reproductionOutput reproduces argv exactly; source hashes equal snapshot and original; recorded outputs absolute (provenance only); reproduction outputs relative and distinct.'},
 'finalizerAssessment': {'path': DC + 'finalize-application.v1.py', 'sha256': 'd3f8d4ce6df69d6f9c99291657922a3e855e3ae2f92fff2184d81ac2d53da8ee', 'procedure': 'Before any write: manifest and review hashes; verdict ACCEPT; newMustIssues and newShouldIssues present as empty lists; subjectManifestSha256 equals the manifest; implementationAuthorized false; activation absent and non-escaping; each file path docs/ or README.md, non-escaping, not a symlink; staged hash and size; live bytes equal before-image (absent when null) or exact after-image; retained manifest and review present with exact hashes. Then copy, re-verify all after-images and write activation last; never overwrite an activation.', 'selfTest': 'finalizer-selftest.v1.json 20/20 on these exact bytes (reused execution, not re-run here).', 'hashCycle': 'Coherent: application.v1 and D-372 name the external activation; no review hash is embedded in its own subject.', 'limits': 'Copies are not atomic (APP45-ADV-04 documented). Support and before-image entries are not re-hashed by the finalizer; this review verified them.'},
 'documentationReview': {'currentAccount': 'Root README, START-HERE, architecture README, register unified section, current source map, design-corrections README header, file 12 and chapter banners are byte-identical to v45 except the register condition-1 line and D-372 evidence sentence; they present one complete intended product design implemented in stages, conditions 1-4 at design level only after activation, condition 5 NOT MET, D-369 historical.', 'links': 'p07: 541 local links, 538 resolve, 3 activation targets (COORDINATOR line 24075, design-corrections README line 3, register line 400), 0 failures. The activation is represented as the finalizer output, not existing evidence.', 'd372Body': 'Read lines 24073-24201.', 'designArtifactsNotQualification': 'Layout, naming, build planning and 54 planned recovery cases are design artifacts; 32 gates and 54 cases are unperformed.'},
 'workingTreeDeliveryLimitation': 'Authorized working-tree delivery only; commit, push and publication excluded. Untracked link targets (prior A-2) are not claimed to resolve in a commit, and A-2 is not closed by committing.',
 'conditions': {'1': 'MET at design level upon activation (27 inherited and 30 evaluation dispositions individually assessed; R10 closed by the actual blind continuation; DR-003 timing explicit).', '2': 'MET at design level upon activation: all 28 rows ACCEPT-DESIGN with complete per-row gate routing.', '3': 'MET upon activation through the design review, Codex assent, blind B, DR-201..205 and this ACCEPT.', '4': 'MET at design level: 32-gate map; all gates unperformed and unqualified.', '5': 'NOT MET. No implementation authorized.'},
 'probes': ['p01_verify.py', 'p02_delta.py', 'p03_filediffs.py', 'p04_classification.py', 'p05_row_gates.py', 'p05b_contexts.py', 'p06_rerun_selectors.py', 'p07_links.py', 'p08_literals_inventory.py', 'p09_remaining.py', 'p10_a2_normalization.py', 'p11_build_review.py', 'p12_final_reverify.py', 'generate-current-design-catalog.py --check (staged)'],
 'counts': counts,
 'limitations': [
   'Read scope: every changed byte in 46 was diffed and the changed Markdown/JSON read; the D-372 body, register unified/gate sections, admission §5, S16, file02/file05 anchors and application records were read or probed. The full contracts and 90 MB inventories were verified by hash and structured probes, not line by line.',
   'For the 187 byte-identical files and unchanged per-item records I used the verified prior45 per-item basis as an explicit basis after confirming byte identity and re-checking selected selectors; I did not restart unrelated source or blind investigations.',
   'Reference suites were not re-executed by this review; I compared the retained v46 rerun against 45.2 and the accepted execution and verified its receipts. The finalizer self-test was not re-run (writes outside this runtime are not permitted).',
   'Git tracking state (A-2) was not measured; the harness denied a read-only git call.',
   'No private session logs were read.',
   'This ACCEPT extends to no changed successor bytes.'],
 'authority': {'gradeGranted': 'only through verified activation', 'implementationAuthorized': False, 'qualificationClaimed': False, 'commitPushPublication': False, 'frozenInputsModified': False, 'historicalGradesExtended': False, 'd9ObligationDischarged': False},
}
json.dump(review, open(RT + 'review.json', 'w'), indent=1, ensure_ascii=False)
print('written', len(json.dumps(review)), 'rows', len(c2), len(inh), len(evs), len(ars), len(fws), len(owns), len(gates), len(fs), len(pv1), len(p45))
print('six', [(e['id'], e['addedIn46']) for e in c2 if e['addedIn46']], 'otherFieldsChanged', [e['id'] for e in c2 if not e['otherRowFieldsByteEqual45']])
print('gatesAdded', {g['id']: g['rowsAddedIn46'] for g in gates if g['rowsAddedIn46']})
