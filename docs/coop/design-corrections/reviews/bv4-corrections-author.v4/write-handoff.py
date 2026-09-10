"""Final handoff, composed from measured bytes AFTER root technical assent. Source is unchanged."""
import hashlib, json
from pathlib import Path

S = Path('/tmp/opensip-design-corrections/bv4-corrections-author.v4')
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
M = json.loads((S / 'root-input/candidate-subject.v14.json').read_text())
FROZEN = {r['path']: r['sha256'] for r in M['files']}
W, B = S / 'work', S / 'before-images'
cp3 = json.loads((S / 'review-ready-3.json').read_text())
assent = json.loads((S / 'root-review-3.json').read_text())
assert assent['checkpointSha256'] == sha(S / 'review-ready-3.json'), 'assent does not bind these bytes'
suite = json.loads((S / 'logs/suite-final-v4d.json').read_text())

changed = [{'path': p, 'beforeSha256': h, 'afterSha256': sha(W / p),
            'beforeImage': str((B / p).relative_to(S)),
            'beforeImageEqualsFrozen': (B / p).exists() and sha(B / p) == h}
           for p, h in sorted(FROZEN.items()) if sha(W / p) != h]
assert [c['path'] for c in changed] == [c['path'] for c in assent['sourceDelta']]
assert all(c['afterSha256'] == a['afterSha256'] for c, a in zip(changed, assent['sourceDelta'])), \
    'source moved after assent'
added = sorted(str(p.relative_to(W)) for p in W.rglob('*')
               if p.is_file() and str(p.relative_to(W)) not in FROZEN)
deleted = sorted(p for p in FROZEN if not (W / p).exists())

HIST = Path('/tmp/opensip-design-corrections')
doc = {
 'unit': 'bv4-corrections-author.v4',
 'standing': ('Narrowly bounded publication follow-up against frozen v14. Root recorded '
   'ASSENT-TO-EXACT-COAUTHOR-SOURCE (technicalAssent true) on the exact bytes of review-ready-3.json. '
   'That is ROOT TECHNICAL SOURCE ASSENT ONLY - not independent review, not blind reconstruction, '
   'not application acceptance, not readiness, not product qualification and not user approval. '
   'Source is UNCHANGED after that assent.'),
 'sourceRoot': str(W),
 'assent': {'file': 'root-review-3.json', 'sha256': sha(S / 'root-review-3.json'),
   'verdict': assent['verdict'], 'technicalAssent': assent['technicalAssent'],
   'boundToCheckpoint': {'file': 'review-ready-3.json', 'sha256': sha(S / 'review-ready-3.json')},
   'implementationAuthorized': assent['implementationAuthorized']},
 'subject': {'manifest': 'root-input/candidate-subject.v14.json',
   'sha256': sha(S / 'root-input/candidate-subject.v14.json'),
   'snapshotRoot': M['snapshotRoot'], 'fileCount': M['fileCount'],
   'successorFreezeRequired': ('These corrections do NOT mutate frozen v14. They need a successor '
     'freeze and review. The separate independent session on immutable v14 was never accessed, '
     'influenced or impersonated, and its subject is unaffected.')},
 'preservedPriorWork': {'v1v2v3Untouched': True, 'frozenV14Untouched': True,
   'liveRepositoryUntouched': True, 'identityModelUntouched': True},
 'delta': {'againstFrozenV14': {'changedFiles': changed, 'changedFileCount': len(changed),
   'additions': added, 'deletions': deleted,
   'noSourcePinChange': True, 'noGeneratedReportChange': True, 'noValidationSummaryChange': True,
   'noReadinessOrCrosswalkChange': True, 'noHistoricalArtifactChange': True,
   'noProductImplementation': True}},

 'theTwoItems': [
  {'id': 'CX-V14-ADMISSION-AVAILABILITY-MIRROR', 'disposition': 'CONFIRMED and corrected',
   'summary': ('Admission 1.1 still named the checkpoint-1 carrier - a singular DomainDetail via '
     'DoctorResult.defects[] or StepTermination.domainDetail - after v3 superseded it in native 1.4 '
     'and workflows 8, and the same section opened by saying the release registry supplies the EXACT '
     'applicable capabilities, contradicting its own later sentence that the registry states '
     'availability, never scope. Both now mirror the selected law: absence is delivered in the '
     'invocation that selected it, on CommandEnvelope.availability, as a CapabilityAvailabilityV1 '
     'whose per-step notices carry the complete ownership tuple in typed fields including the unit '
     'own workspaceRoot; a declared parity field of every requestClass analysis command; advisory '
     'throughout. The registry declares availability and does not fix request scope - the matrix does.'),
   'thenTwoMoreMirrorsRootFound': ('Correcting the prose was not enough. Root found two '
     'authoritative-looking definitions a consumer would actually look up still describing the '
     'superseded route: the x-opensip-public-route-registry operationalCarrier annotation, and the '
     'release_absence_details docstring, which additionally claimed a composition that does not '
     'happen - invocation_availability calls release_absence_notices, never that helper. Both are '
     'corrected. The legacy helper is RETAINED as an explicitly non-authoritative compatibility '
     'projection; no API was removed, and the generic environment note is limited rather than denied.'),
   'newBehaviour': False},
  {'id': 'default-cardinality-boundary', 'disposition': 'INVESTIGATED - real narrow gap; corrected',
   'severityAssignedBy': 'coauthor, stated openly; root did not pre-assign one',
   'theGap': ('scope-descriptor.workspaceRoots admits 1024 unit roots while the matrix-fixed default '
     'requests 11 capabilities per TypeScript unit, so 93 units fit at 1023 rows - one under the '
     'bound, not exactly at it - and 94 do not, at 1034. Units 94..1024 were an ordinary reachable '
     'band that the scope law ADMITS and the default analysis could not express, and the only '
     'outcome was a generic ValidationError of 265492 characters naming no field, count or limit. '
     'It was not default-only: an explicitly supplied over-long spec hit the same thing. No existing '
     'law owned it and no earlier refusal fired.'),
   'theCorrection': ('A new narrow owning pre-Plan helper, admit_analysis_spec, is THE boundary for a '
     'complete spec, defaulted or explicit, in a published order: bounded selection cardinality '
     'first - CONDITIONAL on the field actually being a JSON array in an object - then generic schema '
     'validation of the whole record, then the closed native capability vocabulary. An oversized '
     'valid array refuses TYPED: request-rejected, exit 2, REQUEST.UNSATISFIABLE, public detail '
     'PROJECT.SCOPE_LIMIT with subject field:count>limit, composing a schema-admitted StepTermination '
     'and complete failure envelope.'),
   'whatWasDeliberatelyNotDone': [
     'nothing truncated; no capability dropped',
     'the matrix-fixed product default is unchanged and no promise is lowered',
     'no sharding, no raised bound, no extra steps executed - none of those is a selected feature',
     'NOT a host defect: the host computes the default correctly and the REQUEST cannot be served '
     'within a published bound, so never host-invariant and never SYSTEM.OUTCOME.ILLEGAL_STATE',
     'no new public DomainDetailCode member; the registry stays at 287',
     'no retained-corruption classification broadened or reclassified; identity-model is not edited'],
   'theJudgementCall': ('Reusing PROJECT.SCOPE_LIMIT was the contestable choice and I put both sides '
     'at the first checkpoint rather than defending it. Root agreed the reuse is appropriate BECAUSE '
     'the widened meaning and the pre-Plan owning boundary are explicit in the same change: the '
     'published law now names four bounded fields across two record families - workspaceRoots, '
     'pathPrefixes and excludedPathPrefixes on the scope descriptor, requestedCapabilities on the '
     'analysis spec - so the code is stated rather than silently stretched.'),
   'newBehaviour': ('Yes, stated plainly: a condition that previously escaped as an untyped exception '
     'now refuses typed, and the boundary runs the closed vocabulary admission at REQUEST time for an '
     'explicitly supplied spec where previously only retained Run closure did. No existing class, '
     'exit code, reason code, error code or public detail member changes, and no previously admitted '
     'input is now refused: 0, 1 and 1024-row explicit specs and 1 and 93-unit defaults all admit.')}],

 'defectsIIntroducedAndRootFound': [
  {'id': 'CX-V4-PREFLIGHT-MALFORMED-ARRAY', 'foundBy': 'root', 'severity': 'the serious one',
   'what': ('admit_analysis_spec indexed requestedCapabilities and took its length unconditionally, '
     'breaking the very promise its new paragraph made. Root ran 17 independently selected cases on '
     'my halted bytes: 12 held and FIVE failed - one missing field (KeyError), three non-length '
     'scalar types null/boolean/integer (TypeError), and one oversized string, which was published '
     'as 1025 capabilities with a full typed refusal and a schema-admitted failure envelope. That '
     'last one is a public misclassification of a malformed record as a scope limit, introduced by '
     'me while removing a different misclassification.'),
   'whyMyControlsMissedIt': ('My checkpoint-2 controls exercised only well-formed specs. A boundary '
     'tested only with valid input is not tested.'),
   'fix': ('The precheck is conditional on an actual list inside an object; every other shape reaches '
     'the schema untouched and nothing is coerced. Eight malformed/missing-field controls were added, '
     'each asserting ValidationError rather than merely not-a-ScopeRefusal, plus a no-coercion '
     'control comparing against a snapshot taken BEFORE the calls so it can actually fail, plus two '
     'controls for a case root did not test: an actual 1025-item array of malformed items still '
     'refuses typed because the count is genuine, while the same items within the bound refuse on '
     'the schema. All 17 of root cases now hold, verified by root own unmodified probe bound to the '
     'final checkpoint.')},
  {'id': 'CX-V4-RETAINED-PATH-CLAIM', 'foundBy': 'root', 'disposition': 'RETRACTED',
   'what': ('I claimed the earlier guard placement WOULD have been reached on an oversized retained '
     'payload and WOULD have reclassified corruption as a request refusal, and presented it as a '
     'defect root had not had to spell out. It goes beyond the evidence: admit_run obtains the '
     'retained analysis-spec through payload(digest, "analysis-spec"), which schema-validates it '
     'before the vocabulary helper is invoked, so an oversized retained array refuses there and never '
     'arrives. The subclass relationship I cited is real; a real subclass relationship on an '
     'unreachable path is not a defect.'),
   'fix': ('Retracted in source - both docstrings, the published paragraph, the control comment and '
     'the p4 probe comment. What remains is an architectural separation and two controls that measure '
     'the ACTUAL ordering instead of asserting a story about it.')},
  {'id': 'checkpoint-1 evidence inaccuracies', 'foundBy': 'root',
   'what': ('two arrays where there are four fields across two record families; 93 units described '
     'as fitting EXACTLY when 1023 is one under 1024; a report path recorded for the native checker '
     'which ignores --report and writes in-tree; four argparse failures recorded for suite-final-v4a '
     'when it was THREE argparse failures plus one PIN MISMATCH; and an accidental write described '
     'as outside work/ when it was inside it.'),
   'fix': 'All corrected additively at checkpoints 2 and 3; the original checkpoint is preserved.'}],

 'oneCustodySlipOfMine': {
   'what': ('Invoking native/check_native_evidence.v2.py --help inside work/ rewrote its in-tree '
     'PIN-MISMATCH report, docs/coop/design-corrections/native/native-evidence-report.v2.json, which '
     'that checker writes regardless of --report - the same trap as v1.'),
   'howItWasCaught': 'a full 6047-file manifest drift audit, not by noticing',
   'resolution': ('restored BYTE-EXACT to the frozen v14 bytes and confirmed by re-audit; it is not '
     'among the changed files. Root noted the identical failure-report bytes were PRESERVED in the '
     'retained failed attempt and that this is not a custody blocker; I am not dressing it up as one.'),
   'preservedBytes': {
     'path': 'disposable/suite-final-v4a/work/docs/coop/design-corrections/native/native-evidence-report.v2.json',
     'sha256': sha(S / 'disposable/suite-final-v4a/work/docs/coop/design-corrections/native/native-evidence-report.v2.json')},
   'allLaterCheckerRunsConfinedToDisposableCopies': True},

 'checkpointHistory': [
  {'checkpoint': 1, 'file': 'review-ready.json', 'sha256': sha(S / 'review-ready.json'),
   'rootReview': 'root-review.json', 'sha256Review': sha(S / 'root-review.json'),
   'verdict': 'CHANGES_REQUIRED', 'findings': 3},
  {'checkpoint': 2, 'file': 'review-ready-2.json', 'sha256': sha(S / 'review-ready-2.json'),
   'rootReview': 'root-review-2.json', 'sha256Review': sha(S / 'root-review-2.json'),
   'verdict': 'CHANGES_REQUIRED', 'findings': 2,
   'rootProbe': {'root': '/tmp/opensip-design-corrections/bv4-v4-checkpoint2-preflight.v1',
                 'cases': 17, 'hold': 12, 'fail': 5}},
  {'checkpoint': 3, 'file': 'review-ready-3.json', 'sha256': sha(S / 'review-ready-3.json'),
   'rootReview': 'root-review-3.json', 'sha256Review': sha(S / 'root-review-3.json'),
   'verdict': 'ASSENT-TO-EXACT-COAUTHOR-SOURCE', 'findings': 0,
   'rootProbe': {'root': '/tmp/opensip-design-corrections/bv4-v4-checkpoint3-preflight.v2',
                 'cases': 17, 'allHold': True}}],
 'checkpointFeedbackAccount': ('Root raised 3 + 2 findings across two reviews. Every one was read in '
   'full, agreed, and corrected; NONE was contested. Two were defects I introduced in this same pass '
   '- the unconditional precheck and the unreachable reclassification claim - and one was a set of '
   'evidence inaccuracies in my own checkpoint. Root also supplied an additive immutable mirror note, '
   'both of whose observations were accepted.'),

 'rootAdditiveClarificationsHonoured': [
  {'clarification': ('my checkpoint-3 limits said the boundary was broken for SIX malformed shapes; '
     'root measured FIVE failing cases among 17'),
   'honoured': ('This handoff uses the exact five: one missing field, three non-length scalar types '
     '(null, boolean, integer), one oversized string. The short-string, object, missing-schemaVersion '
     'and unknown-property cases already held. Checkpoint 3 is preserved unchanged; no source edit '
     'and no rerun were needed.')},
  {'clarification': 'the amended p4 probe comment is accurate, and root retained the exact prior bytes',
   'honoured': ('Cited: root reconstructed and retained the pre-amendment p4 bytes '
     '(e21b4c9c...), independently SHA-matching checkpoint 2, in '
     '/tmp/opensip-design-corrections/bv4-v4-checkpoint3-final.v1/probe-history. The amendment '
     'changed a COMMENT that asserted the retracted claim; no recorded measurement changed and '
     'logs/p4-corrected.json and logs/p4-frozen-v14.json are untouched.'),
   'rootHistoryRoot': '/tmp/opensip-design-corrections/bv4-v4-checkpoint3-final.v1/probe-history'},
  {'clarification': ('checkpoint 3 metadata was rewritten twice after first publication - once to add '
     'the verbatim replay account, once to remove a circular hash - and root first feedback assembly '
     'rejected the changed checkpoint hash before delivering assent'),
   'honoured': ('Stated plainly rather than smoothed over. Source bytes were IDENTICAL across all '
     'three metadata revisions; only the checkpoint document changed, and the second revision existed '
     'because I had recorded the hash of a report that itself hashes the document - a circular '
     'reference I should not have written. Root recovered and SHA-verified all three revisions and '
     'their replay reports. The assent binds ONLY the final checkpoint, and this handoff is issued as '
     'a separate document rather than as a further rewrite of it.'),
   'rootHistoryRoot': '/tmp/opensip-design-corrections/bv4-v4-checkpoint3-metadata-history.v1',
   'assentBindsOnly': sha(S / 'review-ready-3.json')}],

 'finalChecksOnFinalBytes': {
   'disposableRoot': suite['disposableRoot'], 'runner': 'repin-and-run.v3.py',
   'method': ('ONE run of the seven checkers on the completed source in a FRESH disposable copy with '
     'an explicit MEASURED temporary repin of %d manifest entries over %d files across three pin '
     'manifests. The runner refuses a destination that already exists, so no earlier run directory '
     'was ever overwritten. These repinned bytes are a DEVELOPMENT INSTRUMENT and are NOT accepted '
     'pin evidence and not the repository final seal; root runs the six actual pinned commands after '
     'integration.' % (suite['temporaryRepinCount'], len(suite['changedFilesVsFrozenV14']))),
   'results': {r['script']: '%s (exit %d)' % (r['lastLine'][:80], r['exitCode'])
               for r in suite['results']},
   'allExitZero': suite['allExitZero'],
   'identityPassingCalls': {'v3Released': 1282, 'checkpoint1': 1305, 'checkpoint2': 1319,
                            'final': 1331},
   'rootSelectedCases': '17/17 hold, verified by root own unmodified probe bound to the final checkpoint',
   'releasedVsSuiteDifferences': [
     'docs/coop/design-corrections/foundation/source-pins.v1.json (temporary repin, 4 entries)',
     'docs/coop/design-corrections/workflows/source-pins.v1.json (temporary repin, 4 entries)',
     'docs/coop/design-corrections/native/source-pins.v2.json (temporary repin, 4 entries)',
     'docs/coop/design-corrections/native/native-evidence-report.v2.json (regenerated INSIDE the '
     'disposable copy; the released copy keeps the frozen v14 bytes)']},

 'probes': [{'path': str(p.relative_to(S)), 'sha256': sha(p)} for p in sorted((S / 'probes').glob('*.py'))],
 'probeHonesty': ('p1_mirror.py and p4_preplan_order.py were run against the FROZEN v14 bytes as well '
   'as the corrected ones, so their controls are demonstrably discriminating rather than assumed to '
   'be - on frozen v14 all six mirror assertions are FALSE and the complete explicit over-bound spec '
   'produces an untyped 263663-character ValidationError. p2_cardinality.py is RETAINED UNCHANGED '
   'even though its explicit-path case called the vocabulary helper directly, which is not the '
   'boundary an explicit spec traverses; p4 supersedes that case and says so, rather than the file '
   'being rewritten to look correct in hindsight. p5_root_cases_replay.py replays ROOT case list and '
   'attributes it at the top; it is my account and not a substitute for root own evidence.'),
 'allCopyRoots': sorted(str(p) for p in (S / 'disposable').iterdir() if p.is_dir()),
 'retainedFailedAttempts': [
  {'root': str(S / 'disposable/suite-final-v4a'), 'log': 'logs/suite-final-v4a.json',
   'whatFailed': ('Runner v1 detected changed files by BASENAME against before-images/, a mirrored '
     'tree, so it measured 0 repins. With no repin: THREE checkers exited 2 on argparse for the '
     'required --report argument (foundation, array-orders, workflows) and the NATIVE checker exited '
     '2 on a PIN MISMATCH - a different failure with a different cause, which checkpoint 1 '
     'miscounted as a fourth argparse failure. Retained unmodified, including its failure-report '
     'bytes.')},
  {'root': str(S / 'disposable/probe-preplan'),
   'whatFailed': ('Scratch identity run that FAILED one control: a mirror assertion written without '
     'the backticks the actual docstring uses. The CONTROL was corrected to the real bytes; the '
     'bytes were not loosened to the control. Retained.')},
  {'root': str(S / 'disposable/probe-preflight-b'),
   'whatFailed': 'Not a failure: the scratch run confirming the conditional precheck. Retained.'},
  {'root': str(S / 'disposable/suite-a'), 'log': 'logs/suite-a-identity.json',
   'whatFailed': 'Not a failure: an early identity-only run. Retained.'},
  {'attempt': 'checkpoint-3 metadata revisions', 'retainedBy': 'root',
   'root': '/tmp/opensip-design-corrections/bv4-v4-checkpoint3-metadata-history.v1',
   'whatFailed': ('The first published checkpoint 3 lacked the verbatim replay account; the second '
     'recorded the hash of a report that hashes the checkpoint, which is circular. Source bytes were '
     'identical across all three. Root recovered and SHA-verified all three revisions.')},
  {'attempt': 'p4 probe comment before amendment', 'retainedBy': 'root',
   'root': '/tmp/opensip-design-corrections/bv4-v4-checkpoint3-final.v1/probe-history',
   'whatFailed': 'the comment asserted the reclassification claim that was later retracted.'}],
 'logs': sorted(str(p.relative_to(S)) for p in (S / 'logs').rglob('*.json')),

 'limits': [
  'No product exists to measure and none was assumed. No real CLI, renderer, agent surface, D9 '
  'interpreter, native host or invocation was executed, and no Run was closed. Every compiler, '
  'provider, release declaration and permission value is a synthetic trusted input, and schema '
  'admission is not host execution.',
  'The retained-path evidence is read-only ordering evidence over source. No full Run was executed '
  'and no corrupt retained payload was driven through a real host.',
  'Passing-call totals are development evidence under TEMPORARY pins. They are not the six pinned '
  'commands, not distinct-case counts, not the repository final seal and not qualification.',
  'The five failing cases at checkpoint 2 were found by ROOT on my halted bytes, not by me. My own '
  'controls exercised only well-formed specs, which is exactly why they passed while the boundary '
  'was broken.',
  'No product implementation, commit, push, publication or subagent, in this pass or any prior one.'],
 'rootOwnsNext': [
  'complete custody and integration of these exact assessed bytes',
  'processing the separate ongoing independent v14 review, whose findings are not supplied or assumed here',
  'the successor freeze and pin seal, and records BEFORE pins',
  'the six actual pinned commands',
  'fresh independent review and a NEW blind reconstruction',
  'full independent application review'],
 'notClaimed': ['independent acceptance', 'blind reconstruction', 'application acceptance',
   'readiness', 'product qualification', 'user approval',
   'that the unseen concurrent v14 independent verdict agrees with any of this'],
 'implementationAuthorized': False,
}
(S / 'handoff.json').write_text(json.dumps(doc, indent=2) + '\n')
print(json.dumps({'changedFiles': len(changed), 'additions': len(added), 'deletions': len(deleted),
                  'copyRoots': len(doc['allCopyRoots']), 'sha256': sha(S / 'handoff.json')}, indent=1))
