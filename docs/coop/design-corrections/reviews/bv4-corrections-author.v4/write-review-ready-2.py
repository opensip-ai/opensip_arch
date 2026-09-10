"""Compose review-ready-2.json from MEASURED bytes. review-ready.json and all earlier logs are preserved."""
import hashlib, json
from pathlib import Path

S = Path('/tmp/opensip-design-corrections/bv4-corrections-author.v4')
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
M = json.loads((S / 'root-input/candidate-subject.v14.json').read_text())
FROZEN = {r['path']: r['sha256'] for r in M['files']}
W, B = S / 'work', S / 'before-images'
first = json.loads((S / 'review-ready.json').read_text())
suite = json.loads((S / 'logs/suite-final-v4c.json').read_text())
p4c = json.loads((S / 'logs/p4-corrected.json').read_text())
p4f = json.loads((S / 'logs/p4-frozen-v14.json').read_text())
v4a = json.loads((S / 'logs/suite-final-v4a.json').read_text())

changed = [{'path': p, 'beforeSha256': h, 'afterSha256': sha(W / p),
            'beforeImage': str((B / p).relative_to(S)),
            'beforeImageEqualsFrozen': (B / p).exists() and sha(B / p) == h}
           for p, h in sorted(FROZEN.items()) if sha(W / p) != h]
added = sorted(str(p.relative_to(W)) for p in W.rglob('*')
               if p.is_file() and str(p.relative_to(W)) not in FROZEN)
deleted = sorted(p for p in FROZEN if not (W / p).exists())

doc = {
 'unit': 'bv4-corrections-author.v4',
 'checkpoint': 2,
 'supersedes': {'file': 'review-ready.json', 'sha256': sha(S / 'review-ready.json'),
   'note': 'Preserved unchanged. This document is ADDITIVE and corrects it where root found it inaccurate.'},
 'answersRootReview': {'file': 'root-review.json', 'sha256': sha(S / 'root-review.json'),
   'verdict': 'CHANGES_REQUIRED', 'itemsAccepted': 3, 'itemsContested': 0},
 'standing': first['standing'],
 'sourceRoot': str(W), 'subjectManifestSha256': sha(S / 'root-input/candidate-subject.v14.json'),
 'frozenSnapshotRoot': M['snapshotRoot'], 'frozenFileCount': M['fileCount'],
 'additionalRootInput': {'path': 'root-input/root-additional-mirror-note.v1.json',
   'sha256': sha(S / 'root-input/root-additional-mirror-note.v1.json'),
   'readInFull': True, 'bothObservationsAccepted': True},
 'delta': {'againstFrozenV14': {'changedFiles': changed, 'additions': added, 'deletions': deleted,
   'changedFileCount': len(changed), 'newSinceCheckpoint1':
     ['docs/coop/design-corrections/native/native-evidence.schemas.v2.json'],
   'noSourcePinChange': True, 'noGeneratedReportChange': True, 'noValidationSummaryChange': True,
   'noReadinessOrCrosswalkChange': True, 'noHistoricalArtifactChange': True}},

 'followupDispositions': [
  {'id': 'CX-V4-REMAINING-CARRIER-MIRRORS', 'disposition': 'ACCEPTED AND CORRECTED',
   'agreedWithRoot': ('Both findings are right and both are the SAME defect class this pass exists to '
     'fix: the prose contracts were corrected while two authoritative-looking definitions a consumer '
     'would actually look up still described the superseded route.'),
   'corrections': [
     {'where': 'native-evidence.schemas.v2.json x-opensip-public-route-registry keys '
        'native.release-capability-undeclared route.operationalCarrier',
      'what': ('Now names CommandEnvelope.availability in the ORIGINAL invocation, the '
        'CapabilityAvailabilityV1 per-step notices and the typed ownership tuple including '
        'workspaceRoot, with section 1.4 as the owning definition. The generic environment note is '
        'explicitly LIMITED rather than deleted - a DoctorResult.defects[] entry or a '
        'StepTermination.domainDetail may still carry one - with the reason neither is this route: '
        'the termination detail is singular, a doctor report is a DIFFERENT invocation, and a '
        'DomainDetail subject cannot hold the tuple without discarding workspaceRoot. The '
        'domainDetail code, the alias/remedy and notATermination are unchanged.')},
     {'where': 'native_evidence_model.v2.py release_absence_details docstring',
      'what': ('Rewritten as SUPERSEDED, NON-AUTHORITATIVE. The false claims are gone: it no longer '
        'calls itself the delivered disclosure, and the SUPERSEDED SHAPE paragraph claiming '
        'invocation_availability composes THIS helper is removed - invocation_availability calls '
        'release_absence_notices and the docstring now says so. It states why it cannot carry the '
        'account (subject concatenation DISCARDS workspaceRoot) and names the actual replacement '
        'route. The function itself is RETAINED as a compatibility projection; no API is removed. '
        'The still-true facts - existing code member, alias, shared remedy, advisory in every '
        'carrier, candidate-only capabilities having no Coverage entry - are kept.')}],
   'controlsAdded': 6, 'historicalFrozenEvidenceRewritten': False},

  {'id': 'CX-V4-PREPLAN-BOUNDARY-AND-ATTRIBUTION', 'disposition': 'ACCEPTED AND CORRECTED',
   'theOverclaimWithdrawn': ('I claimed an analysis-spec-wide guard. That was false. The guard sat '
     'inside admit_requested_capabilities, and a complete explicitly supplied spec reaches '
     'validate_foundation FIRST, so it never touched the guard - my own control hid this by passing a '
     'bare requestedCapabilities array to the vocabulary helper instead of traversing a spec.'),
   'theSecondDefectRootDidNotHaveToSpellOut': ('That placement was also unsafe. '
     'admit_requested_capabilities ALSO runs over the RETAINED analysis-spec at Run closure, where '
     'identity-model admit_run catches this module AdmissionError - and ScopeRefusal is a SUBCLASS of '
     'AdmissionError. An oversized RETAINED array means CORRUPTION, not an oversized request, and my '
     'guard would have been caught there and reclassified as an ordinary request-rejected scope '
     'refusal. That is exactly the broadening root warned against, and it is now impossible: the '
     'guard is not on that path at all.'),
   'correction': ('New narrow owning helper admit_analysis_spec(spec) is THE pre-Plan boundary for a '
     'complete spec, defaulted or explicit, in a published order: (1) bounded selection cardinality, '
     '(2) generic schema validation of the whole record, (3) closed native capability vocabulary. '
     'default_capability_selection now takes the same boundary. admit_requested_capabilities no '
     'longer guards cardinality and says why in the code. The order is published in native section '
     '10, together with the statement that this is the REQUEST boundary only and that retained-payload '
     'validation is a different question with a different answer.'),
   'whyCardinalityPrecedesTheSchema': ('A maxItems breach is reported generically by restating the '
     'entire instance - measured at 263663 characters for a 1025-row spec. An oversized ordinary '
     'selection is not a malformed record. One condition is reordered; none is added, and everything '
     'the schema is better at still refuses at the schema step.'),
   'attributionClaimCorrected': ('The published sentence said no plan2/run2 is minted "so nothing is '
     'retained to attribute the refusal to". The second clause was wrong and is withdrawn in source. '
     'It now reads pre-Plan FOR THE ANALYSIS STEP IT REFUSES: that step mints no plan2 and no run2, '
     'while the request and invocation keep their ordinary operational attribution under workflow '
     'law and any earlier committed step outcome stands. The model docstring is scoped the same way.'),
   'oneBehaviourStatedRatherThanSlippedIn': ('admit_analysis_spec also runs the closed vocabulary '
     'admission at REQUEST time for an explicitly supplied spec; on frozen bytes only the retained '
     'Run-closure path did that. This matches the already published native section 10 row for an '
     'invalid capability REQUEST (request-rejected / CONFIG.INVALID) rather than adding a law, but it '
     'is a real ordering statement and I am not going to let it pass as nothing. If root wants the '
     'boundary to stop at cardinality plus schema, that is a two-line change.'),
   'demonstration': {'probe': 'probes/p4_preplan_order.py',
     'sha256': sha(S / 'probes/p4_preplan_order.py'),
     'standing': ('Reference-model probe run on BOTH the frozen v14 bytes and the corrected bytes, so '
       'every observation is discriminating. No host, renderer, agent surface, D9 interpreter or Run '
       'was executed; the retained-path evidence is read-only ordering evidence over source, and is '
       'not an executed full-Run counterexample.'),
     'onFrozenV14': {'log': 'logs/p4-frozen-v14.json', 'sha256': sha(S / 'logs/p4-frozen-v14.json'),
       'hasPreplanBoundaryHelper': p4f['hasPreplanBoundaryHelper'],
       'completeExplicitSpecOverBound': p4f['completeExplicitSpec']['overBound'],
       'defaultOneUnitBeyond': p4f['defaultPath']['oneUnitBeyond'],
       'carrierMirrors': p4f['carrierMirrors']},
     'onCorrectedBytes': {'log': 'logs/p4-corrected.json', 'sha256': sha(S / 'logs/p4-corrected.json'),
       'hasPreplanBoundaryHelper': p4c['hasPreplanBoundaryHelper'],
       'completeExplicitSpec': p4c['completeExplicitSpec'], 'order': p4c['order'],
       'defaultPath': p4c['defaultPath'], 'retainedPath': p4c['retainedPath'],
       'carrierMirrors': p4c['carrierMirrors']}},
   'retainedCorruptionUntouched': ('No corruption classification was broadened or reclassified. '
     'identity-model is NOT edited; the changed-file list contains no foundation model.')},

  {'id': 'CX-V4-PUBLICATION-AND-EVIDENCE-PRECISION', 'disposition': 'ACCEPTED AND CORRECTED',
   'corrections': [
     {'inaccuracy': 'native section 10 said "two arrays" / "both arrays" / "a second field"',
      'correction': ('Now FOUR fields across TWO record families: workspaceRoots, pathPrefixes and '
        'excludedPathPrefixes on the scope descriptor, and requestedCapabilities on the analysis '
        'spec. The model docstring and the control name are corrected the same way, and the control '
        'now reads all four field names from the two schemas rather than from prose.')},
     {'inaccuracy': 'said 93 TypeScript units "fit exactly (1023 rows)", which reads as filling 1024',
      'correction': ('Now "fit, at 1023 rows - one row under the bound, not exactly at it". The probe '
        'records headroomAtLargestFitting = %d explicitly, and a control refuses the phrase '
        '"fit exactly" in that paragraph.' % p4c['defaultPath']['headroomAtLargestFitting'])},
     {'inaccuracy': ('checkpoint 1 recorded reports/check_native_evidence.v2.json, which that checker '
        'never writes: it IGNORES --report and writes in-tree'),
      'correction': ('Runner v3 records, per checker, whether the --report argument was honoured and '
        'the path and SHA-256 of the report ACTUALLY written. The native report is recorded at its '
        'real in-tree path inside the disposable copy.'),
      'actualNativeReport': next({'path': r['reportActuallyWritten'], 'sha256': r['reportSha256'],
                                  'honouredReportArgument': r['honouredReportArgument']}
                                 for r in suite['results'] if 'native' in r['script'])},
     {'inaccuracy': ('checkpoint 1 called suite-final-v4a four argparse failures'),
      'correction': ('It was THREE argparse failures - foundation, array-orders, workflows - and ONE '
        'native PIN MISMATCH, which is a different failure with a different cause: with zero repins '
        'measured, the native checker refused on pins before argparse mattered. Corrected count '
        'below, read from the retained log.'),
      'measuredFromRetainedLog': [{'script': r['script'], 'exitCode': r['exitCode'],
                                   'failure': ('argparse: missing --report'
                                     if 'required: --report' in r['lastLine'] else 'pin mismatch')}
                                  for r in v4a['results'] if r['exitCode'] != 0]},
     {'inaccuracy': ('preservedPriorWork.note called the accidental native-report write an "outside '
        'work/" write; it was INSIDE work/'),
      'correction': ('Corrected below. The write was inside work/, at '
        'docs/coop/design-corrections/native/native-evidence-report.v2.json, caused by invoking that '
        'checker --help in the live copy; it was found by a full-manifest drift audit and restored '
        'byte-exact to the frozen v14 bytes. Root is right that this is not a custody blocker and I '
        'am not going to dress it up as one: the identical failure-report bytes were PRESERVED in '
        'the retained failed attempt and are still readable there.'),
      'preservedFailureBytes': {
        'path': 'disposable/suite-final-v4a/work/docs/coop/design-corrections/native/native-evidence-report.v2.json',
        'sha256': sha(S / 'disposable/suite-final-v4a/work/docs/coop/design-corrections/native/native-evidence-report.v2.json'),
        'stillPresent': True},
      'liveCopyNow': {'path': 'docs/coop/design-corrections/native/native-evidence-report.v2.json',
        'sha256': sha(W / 'docs/coop/design-corrections/native/native-evidence-report.v2.json'),
        'equalsFrozenV14': sha(W / 'docs/coop/design-corrections/native/native-evidence-report.v2.json')
                          == FROZEN['docs/coop/design-corrections/native/native-evidence-report.v2.json']}}],
   'originalCheckpointAndLogsPreserved': True,
   'suiteRerunReason': ('Not metadata: real source changed for the two other items, so a run was '
     'required regardless. No suite was repeated solely to restate a number.')}],

 'exactObservations': dict(first['exactObservations'], **{
   'boundedSelectionFields': 4, 'boundedSelectionRecordFamilies': 2,
   'headroomAtLargestFittingDefault': p4c['defaultPath']['headroomAtLargestFitting'],
   'genericValidationErrorScalars': {'oversizedDefault1034Rows': 265492,
     'oversizedExplicitSpec1025Rows': p4f['completeExplicitSpec']['overBound']['messageScalars'],
     'wellSizedMalformedSpec': p4c['order']['wellSizedAndMalformed']['messageScalars']},
   'typedRefusalMessageScalars': p4c['completeExplicitSpec']['overBound']['messageScalars']}),

 'retainedControls': {'file': 'docs/coop/design-corrections/foundation/check-identity.py',
   'identityPassingCalls': {'v3Released': 1282, 'checkpoint1': 1305, 'here': 1319},
   'note': ('Checkpoint-1 controls that were written against the wrong boundary were REPLACED, not '
     'kept alongside: the explicit-path control now traverses a complete spec through '
     'admit_analysis_spec instead of handing a bare array to the vocabulary helper. Net +14.')},
 'probes': [{'path': str(p.relative_to(S)), 'sha256': sha(p),
             'standing': 'reference-model probe; no host, renderer, agent surface or Run executed'}
            for p in sorted((S / 'probes').glob('*.py'))],
 'probeHonesty': ('probes/p2_cardinality.py is RETAINED unchanged and its default-path observations '
   'still hold, but its EXPLICIT-path case called admit_requested_capabilities directly, which is not '
   'the boundary an explicitly supplied spec traverses. p4_preplan_order.py supersedes that case and '
   'says so; the retained file is not rewritten to look correct in hindsight.'),
 'inputHashesActuallyRead': first['inputHashesActuallyRead'] + [
   {'path': 'root-review.json', 'sha256': sha(S / 'root-review.json')},
   {'path': 'root-input/root-additional-mirror-note.v1.json',
    'sha256': sha(S / 'root-input/root-additional-mirror-note.v1.json')},
   {'path': 'docs/coop/design-corrections/native/native-evidence.schemas.v2.json',
    'sha256': FROZEN['docs/coop/design-corrections/native/native-evidence.schemas.v2.json']},
   {'path': 'docs/coop/design-corrections/foundation/identity-model.py',
    'sha256': FROZEN['docs/coop/design-corrections/foundation/identity-model.py']}],
 'completedSourceSuite': {'disposableRoot': suite['disposableRoot'], 'runner': 'repin-and-run.v3.py',
   'method': ('ONE run of the seven checkers on the completed source in a FRESH disposable copy with '
     'an explicit MEASURED temporary repin of %d manifest entries over %d files across three pin '
     'manifests. The runner refuses a destination that already exists, so no earlier run directory '
     'was overwritten. These repinned bytes are a DEVELOPMENT INSTRUMENT and are NOT accepted pin '
     'evidence.' % (suite['temporaryRepinCount'], len(suite['changedFilesVsFrozenV14']))),
   'temporaryRepinEntries': suite['temporaryRepinEntries'],
   'results': suite['results'], 'allExitZero': suite['allExitZero']},
 'allCopyRoots': sorted(str(p) for p in (S / 'disposable').iterdir() if p.is_dir()),
 'retainedFailedAttempts': [
   {'root': str(S / 'disposable/suite-final-v4a'), 'log': 'logs/suite-final-v4a.json',
    'whatFailed': ('Runner v1 detected changed files by BASENAME against before-images/, a mirrored '
      'tree, so it measured 0 repins. With no repin: three checkers exited 2 on argparse for the '
      'required --report argument, and the native checker exited 2 on a PIN MISMATCH. Retained '
      'unmodified, including the failure-report bytes.')},
   {'root': str(S / 'disposable/suite-a'), 'log': 'logs/suite-a-identity.json',
    'whatFailed': 'Not a failure: an early identity-only run before the full suite. Retained.'},
   {'root': str(S / 'disposable/probe-preplan'),
    'whatFailed': ('Scratch identity run that FAILED 1 control - a mirror assertion written without '
      'the backticks the actual docstring uses. The control was corrected to the real bytes, not the '
      'bytes loosened to the control. Retained.')}],
 'limits': first['limits'] + [
   'The retained-path evidence is read-only ordering evidence over source. No full Run was executed '
   'and no corrupt retained payload was driven through a real host.'],
 'rootOwnsNext': first['rootOwnsNext'],
 'implementationAuthorized': False, 'sourceEditingStopped': True,
}
(S / 'review-ready-2.json').write_text(json.dumps(doc, indent=2) + '\n')
print(json.dumps({'changed': len(changed), 'additions': len(added), 'deletions': len(deleted),
                  'copyRoots': len(doc['allCopyRoots']), 'allExitZero': suite['allExitZero'],
                  'sha256': sha(S / 'review-ready-2.json')}, indent=1))
