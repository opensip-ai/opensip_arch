"""Compose review-ready-3.json from MEASURED bytes. Checkpoints 1 and 2 and all logs are preserved."""
import hashlib, json
from pathlib import Path

S = Path('/tmp/opensip-design-corrections/bv4-corrections-author.v4')
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
M = json.loads((S / 'root-input/candidate-subject.v14.json').read_text())
FROZEN = {r['path']: r['sha256'] for r in M['files']}
W, B = S / 'work', S / 'before-images'
prev = json.loads((S / 'review-ready-2.json').read_text())
suite = json.loads((S / 'logs/suite-final-v4d.json').read_text())
p5 = json.loads((S / 'logs/p5-root-cases-corrected.json').read_text())
rootrev = json.loads((S / 'root-review-2.json').read_text())
rootprobe = json.loads(Path('/tmp/opensip-design-corrections/bv4-v4-checkpoint2-preflight.v1/report.json').read_text())

changed = [{'path': p, 'beforeSha256': h, 'afterSha256': sha(W / p),
            'beforeImage': str((B / p).relative_to(S)),
            'beforeImageEqualsFrozen': (B / p).exists() and sha(B / p) == h}
           for p, h in sorted(FROZEN.items()) if sha(W / p) != h]
added = sorted(str(p.relative_to(W)) for p in W.rglob('*')
               if p.is_file() and str(p.relative_to(W)) not in FROZEN)
deleted = sorted(p for p in FROZEN if not (W / p).exists())

doc = {
 'unit': 'bv4-corrections-author.v4', 'checkpoint': 3,
 'supersedes': [{'file': 'review-ready.json', 'sha256': sha(S / 'review-ready.json')},
                {'file': 'review-ready-2.json', 'sha256': sha(S / 'review-ready-2.json')}],
 'supersedesNote': 'Both preserved unchanged. This document is ADDITIVE and corrects them where root found them wrong.',
 'answersRootReview': {'file': 'root-review-2.json', 'sha256': sha(S / 'root-review-2.json'),
   'verdict': rootrev['verdict'], 'itemsAccepted': 2, 'itemsContested': 0},
 'standing': prev['standing'],
 'sourceRoot': str(W), 'subjectManifestSha256': sha(S / 'root-input/candidate-subject.v14.json'),
 'frozenSnapshotRoot': M['snapshotRoot'], 'frozenFileCount': M['fileCount'],
 'delta': {'againstFrozenV14': {'changedFiles': changed, 'additions': added, 'deletions': deleted,
   'changedFileCount': len(changed), 'noSourcePinChange': True, 'noGeneratedReportChange': True,
   'noValidationSummaryChange': True, 'noReadinessOrCrosswalkChange': True,
   'noHistoricalArtifactChange': True,
   'identityModelUnchanged': 'docs/coop/design-corrections/foundation/identity-model.py' not in
                             [c['path'] for c in changed]}},

 'followupDispositions': [
  {'id': 'CX-V4-PREFLIGHT-MALFORMED-ARRAY', 'disposition': 'ACCEPTED AND CORRECTED',
   'agreedWithRoot': ('Root is right and the defect is mine. admit_analysis_spec indexed '
     'requestedCapabilities and took its length unconditionally, so it broke the very promise the new '
     'paragraph makes. A missing field raised KeyError, a null/boolean/integer raised TypeError, and '
     'worst of the five, a 1025-CHARACTER STRING was published as 1025 capabilities with a full typed '
     'refusal, subject requestedCapabilities:1025>1024 and a schema-admitted failure envelope. That '
     'is a public misclassification of a malformed record as a scope limit - exactly the kind of '
     'thing this pass exists to remove, introduced by me while removing another one.'),
   'correction': ('The precheck is now CONDITIONAL: it runs only when the value is an actual list '
     'inside an object (isinstance(spec, dict) and isinstance(requested, list)). Every other shape - '
     'missing, null, boolean, number, string, object - proceeds untouched to the existing complete '
     'schema validation and refuses there. Nothing is coerced, defaulted or repaired. A valid array '
     'over the bound stays on the typed refusal path before generic maxItems validation, unchanged.'),
   'conditionalOrderPublished': ['docs/v2/contracts/product-v1/native-evidence.md section 10, the '
     'pre-Plan admission order paragraph, which now states the array condition, that nothing is '
     'coerced, and the 1025-character-string misclassification it prevents',
     'native_evidence_model.v2.py admit_analysis_spec docstring, same statement at the owning helper'],
   'controlsAdded': ('Eight malformed/missing-field controls, one per shape, each asserting '
     'ValidationError rather than merely not-a-ScopeRefusal; a no-coercion control comparing the '
     'inputs against a snapshot taken BEFORE the calls, so it can actually fail; and two controls for '
     'the boundary case root did not test - an ACTUAL array of 1025 malformed items still refuses '
     'typed, because the count is genuine, while the same malformed items within the bound refuse on '
     'the schema. The fitting and overflow positives are retained.'),
   'rootProbeReplay': {
     'rootProbe': {'root': rootrev['rootProbe']['root'], 'probeSha256': rootrev['rootProbe']['probeSha256'],
       'reportSha256': rootrev['rootProbe']['reportSha256'],
       'onCheckpoint2': {'cases': rootrev['rootProbe']['cases'], 'hold': rootrev['rootProbe']['hold'],
                         'fail': rootrev['rootProbe']['fail']},
       'originalFailingResultPreserved': True,
       'note': ('Root probe and report are left exactly as root wrote them. That probe binds itself '
         'to a checkpoint changedFiles hash set and so refuses to run on moved source; running it '
         'against checkpoint 2 after these corrections raises AssertionError on check-identity.py, '
         'which is the probe working as designed and is not a result.')},
     'replay': {'probe': 'probes/p5_root_cases_replay.py', 'sha256': sha(S / 'probes/p5_root_cases_replay.py'),
       'log': 'logs/p5-root-cases-corrected.json', 'sha256Log': sha(S / 'logs/p5-root-cases-corrected.json'),
       'caseListTakenVerbatimFromRootProbe': True,
       'cases': p5['cases'], 'hold': p5['hold'], 'fail': p5['fail'],
       'noMalformedInputWasCoercedOrRepaired': p5['noMalformedInputWasCoercedOrRepaired'],
       'fiveFailingCasesNow': [{'id': r['id'], 'expected': r['expected'], 'actual': r['actual'],
                                'holds': r['holds']}
                               for r in p5['results']
                               if r['id'] in {f['id'] for f in rootrev['requiredFollowup'][0]['actualFailures']}],
       'standing': ('Reference-model replay of root selected cases; synthetic requests and '
         'schema-admitted envelopes, not host, renderer, invocation execution or retained Run '
         'closure. Root should re-run its own probe bound to THIS checkpoint; this replay is my '
         'account, not a substitute for root evidence.')}},
     'rootProbeRunVerbatimOnTheseBytes': {
       'howItWasRun': ('Root own probe file, unmodified, bound to THIS checkpoint: '
         'probe.py --checkpoint review-ready-3.json --out logs/root-preflight-replay-checkpoint3.v1. '
         'It re-verified every changed-file hash before and after its cases, so it ran on exactly '
         'these bytes. Root wrote the probe and the case list; I only invoked it.'),
       'out': 'logs/root-preflight-replay-checkpoint3.v1',
       'reportHashNotRecordedHere': ('deliberately: that report carries its own checkpointSha256 of '
         'THIS document, so hashing it here would be circular. The report binds itself.'),
       'cases': 17, 'allHold': True, 'failures': []},
   'rootProbeCasesOnFrozenV14': ('Not applicable: admit_analysis_spec does not exist on frozen v14, '
     'so the case list cannot be run there. The frozen-vs-corrected discrimination for this item is '
     'in logs/p4-frozen-v14.json, where the complete explicit over-bound spec produces an untyped '
     '263663-character ValidationError and hasPreplanBoundaryHelper is false.')},

  {'id': 'CX-V4-RETAINED-PATH-CLAIM', 'disposition': 'ACCEPTED AND RETRACTED',
   'whatIClaimed': ('Checkpoint 2 said the earlier guard placement WOULD have been reached on an '
     'oversized retained payload and WOULD have reclassified corruption as an ordinary request '
     'refusal, and called it a defect root did not have to spell out.'),
   'whyItWasWrong': ('It goes beyond the evidence. I verified root position on the current source: '
     'admit_run obtains the retained analysis-spec through payload(digest, "analysis-spec"), which '
     'runs C.validate against the full schema (identity-model.py, the payload helper) BEFORE the '
     'native vocabulary helper is invoked further down. An oversized retained array therefore refuses '
     'as a ValidationError at that point and never reaches the helper, so the reclassification I '
     'described was not reachable. The subclass relationship I cited is real, but a real subclass '
     'relationship on an unreachable path is not a defect, and I presented it as one.'),
   'whatIsTrueInstead': ('Keeping cardinality out of the shared vocabulary helper is an ARCHITECTURAL '
     'SEPARATION: pre-Plan request selection and retained-record validation are different concerns '
     'and the guard belongs with the request boundary. That is the whole claim now.'),
   'correctedIn': ['native_evidence_model.v2.py admit_analysis_spec docstring',
     'native_evidence_model.v2.py admit_requested_capabilities docstring',
     'check-identity.py, where the control comment asserting the reclassification is replaced by two '
     'controls that measure the actual ordering: the retained record is schema-validated before any '
     'capability vocabulary admission, and an oversized retained analysis-spec refuses on the schema',
     'native-evidence.md section 10, which now says Run closure schema-validates the retained record '
     'before any capability vocabulary admission',
     'probes/p4_preplan_order.py, whose comment block is amended in place with the retraction stated; '
     'its recorded measurements are unchanged and logs/p4-*.json are untouched'],
   'noBehaviouralChange': ('Nothing about retained Run closure changed, no corruption classification '
     'was broadened, no new full-Run fixture was written, and identity-model.py is not edited.')}],

 'exactObservations': dict(prev['exactObservations'], **{
   'rootSelectedCasesHolding': '%d/%d' % (p5['hold'], p5['cases']),
   'rootSelectedCasesHoldingAtCheckpoint2': '%d/%d' % (rootrev['rootProbe']['hold'],
                                                       rootrev['rootProbe']['cases']),
   'malformedShapesRoutedToTheSchema': 8}),
 'retainedControls': {'file': 'docs/coop/design-corrections/foundation/check-identity.py',
   'identityPassingCalls': {'v3Released': 1282, 'checkpoint1': 1305, 'checkpoint2': 1319, 'here': 1331}},
 'probes': [{'path': str(p.relative_to(S)), 'sha256': sha(p),
             'standing': 'reference-model probe; no host, renderer, agent surface or Run executed'}
            for p in sorted((S / 'probes').glob('*.py'))],
 'probeHonesty': prev['probeHonesty'] + (' p4_preplan_order.py has its retained-path COMMENT amended '
   'in place with the retraction stated inside the file; no recorded measurement changed and its two '
   'logs are untouched. p5_root_cases_replay.py replays root case list and says so at the top.'),
 'inputHashesActuallyRead': prev['inputHashesActuallyRead'] + [
   {'path': 'root-review-2.json', 'sha256': sha(S / 'root-review-2.json')},
   {'path': '/tmp/opensip-design-corrections/bv4-v4-checkpoint2-preflight.v1/probe.py',
    'sha256': rootrev['rootProbe']['probeSha256'], 'readInFull': True},
   {'path': '/tmp/opensip-design-corrections/bv4-v4-checkpoint2-preflight.v1/report.json',
    'sha256': rootrev['rootProbe']['reportSha256'], 'allHold': rootprobe['allHold']}],
 'completedSourceSuite': {'disposableRoot': suite['disposableRoot'], 'runner': 'repin-and-run.v3.py',
   'method': ('ONE run of the seven checkers on the completed source in a FRESH disposable copy with '
     'an explicit MEASURED temporary repin of %d manifest entries over %d files across three pin '
     'manifests. The runner refuses a destination that already exists. DEVELOPMENT INSTRUMENT only; '
     'not accepted pin evidence.' % (suite['temporaryRepinCount'],
                                     len(suite['changedFilesVsFrozenV14']))),
   'temporaryRepinEntries': suite['temporaryRepinEntries'], 'results': suite['results'],
   'allExitZero': suite['allExitZero']},
 'allCopyRoots': sorted(str(p) for p in (S / 'disposable').iterdir() if p.is_dir()),
 'retainedFailedAttempts': prev['retainedFailedAttempts'] + [
   {'root': str(S / 'disposable/probe-preflight-b'),
    'whatFailed': ('Not a failure: the scratch identity run that confirmed the conditional precheck '
      'and the eight malformed-shape controls before the full suite. Retained.')}],
 'limits': prev['limits'] + [
   'The five cases root found failing were found by ROOT, on my halted bytes, not by me. My own '
   'controls at checkpoint 2 exercised only well-formed specs, which is why they passed while the '
   'boundary was broken for six malformed shapes.'],
 'rootOwnsNext': prev['rootOwnsNext'],
 'implementationAuthorized': False, 'sourceEditingStopped': True,
}
(S / 'review-ready-3.json').write_text(json.dumps(doc, indent=2) + '\n')
print(json.dumps({'changed': len(changed), 'additions': len(added), 'deletions': len(deleted),
                  'rootCases': '%d/%d' % (p5['hold'], p5['cases']),
                  'allExitZero': suite['allExitZero'],
                  'sha256': sha(S / 'review-ready-3.json')}, indent=1))
