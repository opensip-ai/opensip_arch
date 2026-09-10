"""Compose review-ready.json from MEASURED bytes: every hash is read here, none is restated."""
import hashlib, json, subprocess
from pathlib import Path

S = Path('/tmp/opensip-design-corrections/bv4-corrections-author.v4')
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
MANIFEST = json.loads((S / 'root-input/candidate-subject.v14.json').read_text())
FROZEN = {r['path']: r['sha256'] for r in MANIFEST['files']}
WORK = S / 'work'
BEFORE = S / 'before-images'

changed = [{'path': p, 'beforeSha256': h, 'afterSha256': sha(WORK / p),
            'beforeImage': str((BEFORE / p).relative_to(S)),
            'beforeImageEqualsFrozen': (BEFORE / p).exists() and sha(BEFORE / p) == h}
           for p, h in sorted(FROZEN.items()) if sha(WORK / p) != h]
added = sorted(str(p.relative_to(WORK)) for p in WORK.rglob('*')
               if p.is_file() and str(p.relative_to(WORK)) not in FROZEN)
deleted = sorted(p for p in FROZEN if not (WORK / p).exists())
suite = json.loads((S / 'logs/suite-final-v4b.json').read_text())

doc = {
 'unit': 'bv4-corrections-author.v4',
 'standing': ('Coauthor source corrections offered for root technical review at a stable checkpoint. '
   'Source editing has STOPPED. This is not an independent review, not blind reconstruction, not '
   'application acceptance, not readiness and not product qualification. These corrections require a '
   'SUCCESSOR freeze and review; frozen v14 is not mutated and the concurrent independent session on '
   'immutable v14 was never accessed, influenced or impersonated.'),
 'sourceRoot': str(WORK),
 'subjectManifestSha256': sha(S / 'root-input/candidate-subject.v14.json'),
 'frozenSnapshotRoot': MANIFEST['snapshotRoot'],
 'frozenFileCount': MANIFEST['fileCount'],
 'preservedPriorWork': {
   'v1v2v3Untouched': True,
   'frozenV14Untouched': True,
   'note': ('The only write outside work/ and disposable/ this turn was an accidental one: invoking '
     'native/check_native_evidence.v2.py --help inside work/ rewrote its in-tree PIN-MISMATCH report '
     'docs/coop/design-corrections/native/native-evidence-report.v2.json, which that checker writes '
     'regardless of --report. It was detected by a full-manifest drift audit and restored BYTE-EXACT '
     'to the frozen v14 bytes; it is not among the changed files below. All later checker runs are '
     'confined to disposable copies.')},
 'delta': {'againstFrozenV14': {'changedFiles': changed, 'additions': added, 'deletions': deleted,
   'changedFileCount': len(changed),
   'noSourcePinChange': True, 'noGeneratedReportChange': True, 'noValidationSummaryChange': True,
   'noReadinessOrCrosswalkChange': True, 'noHistoricalArtifactChange': True}},
 'items': [
  {'id': 'CX-V14-ADMISSION-AVAILABILITY-MIRROR',
   'disposition': 'CONFIRMED and corrected',
   'owningFile': 'docs/v2/contracts/product-v1/admission-and-qualification.md',
   'whatWasWrong': ('Section 1.1 still named the checkpoint-1 carrier - a singular DomainDetail via '
     'DoctorResult.defects[] or StepTermination.domainDetail - which v3 superseded in native 1.4 and '
     'workflows 8. The same section also opened by saying the release declaration registry supplies '
     'the exact applicable capabilities, contradicting its own later sentence that the registry '
     'states availability, never scope.'),
   'correction': ('Both sentences now mirror the selected law: absence is delivered in the invocation '
     'that selected it, on CommandEnvelope.availability, as CapabilityAvailabilityV1 = '
     '{stepCount, totalNoticeCount, steps[]} whose per-step entries carry the complete ownership '
     'tuple in typed fields (capabilityId, languageMode, the unit own workspaceRoot) with code '
     'native.capability-unavailable; a declared parity field of every requestClass analysis command; '
     'advisory - terminates nothing, mints no Coverage, grants no Control verdict or repair '
     'authority. The superseded carrier is named only to repudiate it, with the reason it cannot '
     'work: one is singular where an invocation has many absences, and a doctor report is a '
     'DIFFERENT invocation. The registry sentence now says available, not exact, and states '
     'explicitly that it does not fix request scope - the matrix does. No new behaviour; native '
     '1.4/10 remain the owning detail.'),
   'newBehaviour': False},
  {'id': 'default-cardinality-boundary',
   'disposition': 'INVESTIGATED - real, narrow, reachable gap; corrected',
   'severityAssignedBy': 'coauthor, stated openly for root to overrule',
   'owningFiles': ['docs/v2/contracts/product-v1/native-evidence.md',
                   'docs/coop/design-corrections/native/native_evidence_model.v2.py'],
   'threeOpenQuestionsAnswered': {
     'isItDefaultHelperOnly': ('No. An explicitly supplied 1025-row analysis-spec hit the same '
       'untyped ValidationError. This is the analysis-spec boundary in general.'),
     'doesAnExistingLawOwnIt': ('No. The published scope-refusal paragraph said "a scope array" and '
       'named only workspaceRoots, pathPrefixes, excludedPathPrefixes; no section 10 row and no '
       'contract sentence mentioned requestedCapabilities as a refusal condition.'),
     'doesAnEarlierRefusalFire': ('No. unit_scope_descriptor ADMITS at 94 units because '
       'workspaceRoots maxItems is also 1024. Units 94..1024 were a band of ordinary repositories '
       'that the scope law admits and the default analysis could not express, with no owning route.')},
   'whatWasWrong': ('The matrix-fixed default requests one row per (discovered unit, capability whose '
     'cell is not NOT-SELECTED) - 11 per TypeScript unit, 10 per Rust unit - so 93 TS units fit '
     'exactly (1023 rows) and 94 do not (1034 > 1024). The only outcome was a generic ValidationError '
     'of 265492 scalars naming no field, count or limit. A pure helper ValidationError is not a '
     'public host termination, which is precisely why the condition needed an owning typed refusal.'),
   'correction': ('admit_requested_capability_cardinality reads the bound FROM the schema and raises '
     'the already field-generic ScopeRefusal, called at the analysis-spec admission boundary and in '
     'default_capability_selection, so the generic exception is never the public path. '
     'scope_refusal_termination composes the real StepTermination and the required nonempty failure '
     'envelope errors array. Outcome: request-rejected / exit 2 / REQUEST.UNSATISFIABLE, detail '
     'PROJECT.SCOPE_LIMIT with subject requestedCapabilities:1034>1024. Refuses pre-Plan: no plan2 '
     'and no run2 minted.'),
   'whatWasDeliberatelyNotDone': [
     'nothing truncated and no capability dropped',
     'the matrix-fixed product default is unchanged and no promise is lowered',
     'no sharding and no raised bound introduced as an unreviewed feature',
     'no further steps auto-executed',
     'NOT classified as a host defect: the host computed the default correctly, the REQUEST cannot be '
     'served within a published bound, so never host-invariant and never SYSTEM.OUTCOME.ILLEGAL_STATE',
     'no new public DomainDetailCode member added; the registry stays at 287'],
   'judgementCallForRoot': ('Reusing PROJECT.SCOPE_LIMIT is the one contestable choice. FOR: a D9 code '
     'is a remedy class and the remedy is identical - narrow your selection explicitly, nothing was '
     'truncated - the subject already encodes field:count>limit, and the paragraph already says the '
     'public code is shared across host/native scope admission. AGAINST: the code is named for the '
     'project scope descriptor and requestedCapabilities is an analysis-spec field, so a consumer '
     'switching on it currently expects one of three scope fields. My position: reuse is honest ONLY '
     'because the published meaning is widened in the SAME edit, from "a scope array" to "a bounded '
     'selection array that exceeds its published schema bound", naming both arrays. If root prefers a '
     'distinct registry member instead, that is a one-line change and I will make it rather than '
     'defend reuse for its own sake.'),
   'newBehaviour': ('Yes, and stated plainly: a condition that previously escaped as an untyped '
     'exception now refuses typed. No existing class, exit code, reason code, error code or public '
     'detail member changes, and no previously admitted input is now refused - 93 units and an '
     'explicit selection at exactly 1024 still ADMIT.')}],
 'exactObservations': {
   'analysisSpecRequestedCapabilitiesMaxItems': 1024,
   'scopeDescriptorWorkspaceRootsMaxItems': 1024,
   'defaultCapabilitiesPerTypeScriptUnit': 11, 'defaultCapabilitiesPerRustUnit': 10,
   'largestFittingTypeScriptUnitCount': 93, 'requestsAt93Units': 1023,
   'firstRefusingUnitCount': 94, 'requestsAt94Units': 1034,
   'frozenOutcomeAt94Units': {'exception': 'ValidationError', 'scalars': 265492,
     'namesField': False, 'namesCountOrLimit': False, 'isTypedRefusal': False},
   'correctedOutcomeAt94Units': {'exception': 'ScopeRefusal',
     'detail': 'PROJECT.SCOPE_LIMIT', 'subject': 'requestedCapabilities:1034>1024',
     'class': 'request-rejected', 'exitCode': 2, 'errorCode': 'REQUEST.UNSATISFIABLE',
     'stepTerminationSchemaAdmission': 'ADMIT', 'failureEnvelopeSchemaAdmission': 'ADMIT',
     'planMinted': False, 'runMinted': False},
   'explicitOverLongSpec': {'rows': 1025, 'subject': 'requestedCapabilities:1025>1024'},
   'explicitSpecAtExactlyTheBound': {'rows': 1024, 'outcome': 'ADMIT'},
   'inheritedScopeArrayRefusalUnchanged': 'workspaceRoots:1025>1024, same code, same class',
   'publicDetailRegistryMembers': 287, 'publicDetailMembersAdded': 0},
 'retainedControls': {
   'file': 'docs/coop/design-corrections/foundation/check-identity.py',
   'identityPassingCalls': {'v3Released': 1282, 'here': 1305, 'added': 23},
   'mirrorControls': 7, 'cardinalityControls': 16,
   'mirrorControlsAreDiscriminating': ('Proven, not assumed: disposable/mirror-negative runs the same '
     '6 paragraph-bound assertions against the FROZEN v14 bytes, where all 6 are FALSE. They are '
     'bound to the unique owning paragraph, not a file-wide substring or a count, because the file '
     'also contains correct text.'),
   'cardinalityControlsExerciseRealArtifacts': ('The overflow control calls the ACTUAL guard and '
     'reads the exception field/count/limit; the envelope control instantiates the real '
     'StepTermination and CommandEnvelope schemas rather than asserting over prose. The fitting '
     'positive control (93 units -> 1023 rows, ADMIT) and the at-bound explicit control (1024 rows, '
     'ADMIT) exist so the guard cannot pass by refusing everything.')},
 'probes': [{'path': str(p.relative_to(S)), 'sha256': sha(p),
             'standing': 'reference-model probe; no host, renderer, agent surface or Run executed'}
            for p in sorted((S / 'probes').glob('*.py'))],
 'inputHashesActuallyRead': [{'path': p, 'sha256': FROZEN[p]} for p in sorted([
   'docs/v2/contracts/product-v1/admission-and-qualification.md',
   'docs/v2/contracts/product-v1/native-evidence.md',
   'docs/v2/contracts/product-v1/workflows-and-surfaces.md',
   'docs/coop/design-corrections/native/native_evidence_model.v2.py',
   'docs/coop/design-corrections/native/native-evidence.schemas.v2.json',
   'docs/coop/design-corrections/foundation/check-identity.py',
   'docs/coop/design-corrections/public-detail-registry.v1.json',
   'docs/coop/design-corrections/workflows/schemas/common.schema.json',
   'docs/coop/design-corrections/workflows/schemas/command-envelope.schema.json',
 ]) if p in FROZEN] + [
   {'path': 'root-input/root-publication-probe/report.json',
    'sha256': sha(S / 'root-input/root-publication-probe/report.json')},
   {'path': 'root-input/root-publication-probe/probe.py',
    'sha256': sha(S / 'root-input/root-publication-probe/probe.py')}],
 'completedSourceSuite': {
   'disposableRoot': suite['disposableRoot'], 'runner': 'repin-and-run.v2.py',
   'method': ('ONE run of the seven checkers on the completed source in a FRESH disposable copy with '
     'an explicit MEASURED temporary repin of %d manifest entries over %d files across three pin '
     'manifests. No earlier run directory was overwritten; the runner refuses a destination that '
     'exists. These repinned bytes are a DEVELOPMENT INSTRUMENT and are NOT accepted pin evidence.'
     % (suite['temporaryRepinCount'], len(suite['changedFilesVsFrozenV14']))),
   'temporaryRepinEntries': suite['temporaryRepinEntries'],
   'results': suite['results'], 'allExitZero': suite['allExitZero'],
   'releasedVsSuiteDifferences': [
     'docs/coop/design-corrections/foundation/source-pins.v1.json (temporary repin, 3 entries)',
     'docs/coop/design-corrections/workflows/source-pins.v1.json (temporary repin, 3 entries)',
     'docs/coop/design-corrections/native/source-pins.v2.json (temporary repin, 3 entries)',
     'docs/coop/design-corrections/native/native-evidence-report.v2.json (regenerated INSIDE the '
     'disposable copy; the released copy keeps the frozen v14 bytes)']},
 'allCopyRoots': sorted(str(p) for p in (S / 'disposable').iterdir() if p.is_dir()),
 'retainedFailedAttempts': [
   {'root': str(S / 'disposable/suite-final-v4a'), 'log': 'logs/suite-final-v4a.json',
    'whatFailed': ('Runner v1 detected changed files by BASENAME against before-images/, which is a '
      'mirrored tree, so it measured 0 repins; and it invoked the checkers without their required '
      '--report argument, so four exited 2 on argparse. Retained unmodified; superseded by '
      'repin-and-run.v2.py in suite-final-v4b.')}],
 'limits': [
   'No product exists to measure and none was assumed. No real CLI, renderer, agent surface, D9 '
   'interpreter or native host was executed; every compiler, provider and release declaration is a '
   'synthetic trusted input, and schema admission is not host execution.',
   'Passing-call totals are development evidence under TEMPORARY pins. They are not the six pinned '
   'commands, not distinct-case counts, and not qualification.',
   'Root is right that no real host was shown to emit the generic ValidationError string. The '
   'correction does not depend on that: it makes the typed refusal the public path so what a host '
   'does with a helper exception stops mattering.',
   'No implementation, commit, push, publication or subagent. No product code was written.'],
 'rootOwnsNext': ['technical review of these exact bytes', 'the PROJECT.SCOPE_LIMIT reuse decision',
   'successor freeze and pin seal', 'the six actual pinned commands',
   'fresh independent review and a new blind reconstruction', 'full independent application review'],
 'implementationAuthorized': False,
 'sourceEditingStopped': True,
}
(S / 'review-ready.json').write_text(json.dumps(doc, indent=2) + '\n')
print(json.dumps({'changed': len(changed), 'additions': len(added), 'deletions': len(deleted),
                  'copyRoots': len(doc['allCopyRoots']), 'allExitZero': suite['allExitZero'],
                  'reviewReadySha256': sha(S / 'review-ready.json')}, indent=1))
