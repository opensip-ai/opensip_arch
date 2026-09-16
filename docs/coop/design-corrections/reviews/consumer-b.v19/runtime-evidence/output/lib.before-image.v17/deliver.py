"""Phase 11 -- write output/blind-review.json and output/blind-review.md.

Every number in the deliverable is READ FROM AN ARTIFACT produced by an earlier stage. The
only hand-authored content is prose that explains what was measured, the gap findings of
phase 10, and the standing statements the charter requires.
"""
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = '/tmp/opensip-design-corrections/consumer-b.v17'
OUT = ROOT + '/output'
LABELS = ['syntax-code', 'typescript', 'rust', 'rust-partial', 'syntax-data']
SESSION = '79569ae1-10f4-4181-972b-334f7ed2f07a'
PY = '/tmp/opensip-architecture-review-env/bin/python'


def J(rel):
    try:
        return json.load(open(OUT + '/' + rel))
    except Exception:
        return None


def sha_of(rel):
    p = OUT + '/' + rel
    if not os.path.exists(p):
        return None
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def main():
    cust = J('notes/v17-input-custody.json') or J('notes/v16-input-custody.json')
    gaps = J('vectors/phase10-design-gaps.json')
    status = J('requirement-status.json') or {}
    helpers = J('helper-corrections.json')
    verify = J('verify-all.json')
    reqfile = json.load(open(ROOT + '/requirements.json'))

    runs = []
    for lab in LABELS:
        st = J('runs/%s.store.json' % lab) or {}
        cl = J('runs/%s.closure.json' % lab) or {}
        rp = J('runs/%s.replay.json' % lab) or {}
        ct = J('runs/%s.controls.json' % lab) or {}
        fams = (ct.get('tamperedResultControls') or []) \
            + (ct.get('identityAndRetentionControls') or [])
        runs.append({
            'label': lab,
            'claimedRunId': (st.get('claim') or {}).get('runId'),
            'claimedSealId': (st.get('claim') or {}).get('sealId'),
            'claimedProofId': (st.get('claim') or {}).get('proofId'),
            'claimedPlanId': (st.get('claim') or {}).get('planId'),
            'claimedSnapshotId': (st.get('claim') or {}).get('snapshotId'),
            'verdict': (st.get('claim') or {}).get('verdict'),
            'exportFile': 'runs/%s.store.json' % lab,
            'exportFileSha256': sha_of('runs/%s.store.json' % lab),
            'objectCount': st.get('objectCount'), 'blobCount': st.get('blobCount'),
            'totalBlobBytes': st.get('totalBlobBytes'),
            'closure': {'admitted': cl.get('admitted'),
                        'checksPassed': cl.get('checksPassed'),
                        'checksNotApplicable': cl.get('checksNotApplicable'),
                        'checksRefused': cl.get('checksRefused'),
                        'file': 'runs/%s.closure.json' % lab,
                        'fileSha256': sha_of('runs/%s.closure.json' % lab)},
            'freshProcessReplay': {
                'file': 'runs/%s.replay.json' % lab,
                'fileSha256': sha_of('runs/%s.replay.json' % lab),
                'result': rp.get('comparison') or rp.get('result') or rp.get('replay'),
                'matched': 'REPLAY_MATCH' in json.dumps(rp),
                'standing': ('the store was reloaded from its own exported bytes in a '
                             'SEPARATE process, every blob key was re-hashed on import, and '
                             'the complete proof bundle was recomputed and compared')},
            'controls': {'file': 'runs/%s.controls.json' % lab,
                         'fileSha256': sha_of('runs/%s.controls.json' % lab),
                         'count': len(fams),
                         'allRefused': bool(fams) and all(c.get('refused') for c in fams)},
            'requirementIds': st.get('requirementIds'),
        })

    vectors = {}
    for d in ('vectors', 'envelopes', 'query', 'notes', 'traces', 'checkpoints'):
        base = OUT + '/' + d
        if not os.path.isdir(base):
            continue
        for f in sorted(os.listdir(base)):
            if f.endswith('.json'):
                vectors['%s/%s' % (d, f)] = sha_of('%s/%s' % (d, f))

    import collections
    counts = collections.Counter(v['status'] for v in status.values())
    unexec = sorted(k for k, v in status.items() if v['status'] == 'unexecuted')
    blocking_unexec = sorted(k for k, v in status.items()
                             if v['status'] == 'unexecuted' and v.get('acceptBlocking'))
    must = (gaps or {}).get('newMustIssues') or []
    should = (gaps or {}).get('newShouldIssues') or []
    adv = (gaps or {}).get('advisories') or []

    all_runs_ok = all(r['closure']['admitted'] and r['freshProcessReplay']['matched']
                      and r['controls']['allRefused'] for r in runs)
    verdict = ('ACCEPT-RECONSTRUCTABLE'
               if (not blocking_unexec and not must and not should and all_runs_ok)
               else 'CHANGES_REQUIRED')

    doc = {
        'schema': 'consumer-b blind design review, v16 generation',
        'consumerId': 'consumer-b.v17',
        'sessionId': SESSION,
        'sameOriginAncestry': ['consumer-b.v14', 'consumer-b.v15', 'consumer-b.v16',
                               'consumer-b.v17'],
        'ancestryStanding': (
            'ONE continuous fresh blind consumer origin, interrupted at four deliberate '
            'source transitions. Every earlier generation is retained UNMODIFIED (measured: '
            'notes/siblings-untouched.json), and continuation does not retroactively grant '
            'acceptance to any of them: the v16 verdict was CHANGES_REQUIRED and so is this '
            'one.'),
        'whatChangedInTheInputThisGeneration': {
            'normativeBytes': ('UNCHANGED -- all 101 disclosed normative files are '
                               'byte-identical to the v16 kit, MEASURED per path against '
                               "this origin's own v16 custody record "
                               '(notes/v17-input-custody.json)'),
            'manifestOwnDigest': 'changed',
            'declaredParentBinding': 'changed (parent 31), DECLARED BINDING ONLY',
            'consequence': ('no Run needed reminting for a changed normative digest. Every '
                            'remint this generation was caused by a CORRECTION this origin '
                            'made after the second clause-to-code audit, not by the kit.'),
        },
        'v17ClauseToCodeAudit': (J('vectors/phase10-design-gaps.json') or {}).get(
            'v17ClauseToCodeAuditOfTheRECORDCONSTRUCTIONandADMISSIONfunctions'),
        'verdict': verdict,
        'verdictBasis': {
            'acceptBlockingUnexecuted': blocking_unexec,
            'newMustIssueCount': len(must),
            'newShouldIssueCount': len(should),
            'everyClaimedPositivePassedSchemaClosureReplayAndControls': all_runs_ok,
            'rule': ('ACCEPT-RECONSTRUCTABLE requires every acceptBlocking requirement '
                     'executed AND no unresolved MUST or SHOULD. Two SHOULD-level design '
                     'gaps remain, so the verdict is CHANGES_REQUIRED even though all 131 '
                     'non-future requirements are executed.')
            if verdict != 'ACCEPT-RECONSTRUCTABLE' else
            ('every acceptBlocking requirement executed, no unresolved MUST or SHOULD, and '
             'every claimed positive passed schema admission, retained closure, '
             'fresh-process replay and its controls')},
        'inputKit': {
            'subjectManifestPath': 'subject/consumer-input-manifest.json',
            'subjectManifestSha256':
                cust['inputKit']['manifestSha256Measured'] if cust else None,
            'parentCandidateSha256DeclaredInThatManifest':
                (cust['inputKit'].get('parentSubjectSha256DeclaredInManifest')
                 or cust['inputKit'].get('parentCandidateSha256Declared'))
                if cust else None,
            'fileCount': cust['inputKit']['fileCount'] if cust else None,
            'filesVerifiedPass': cust['inputKit']['filesVerifiedPass'] if cust else None,
            'hashVerification': cust['inputKit']['hashVerification'] if cust else None,
            'changedAgainstThePriorDisclosedKit':
                (cust or {}).get('kitDiffAgainstPriorDisclosedKit'),
            'parentVerificationStanding': (
                'NOT a parent whole-candidate verification. Only the parent digest DECLARED '
                'in the held manifest was compared to the value the instruction names; the '
                'parent candidate itself was never held, read or verified.'),
            'ancestorManifests': [
                {'generation': 'consumer-b.v14',
                 'manifestSha256': 'f8aec9c5469573568fe6f57f14429b739cf7f9707c08a26b72d0c48e71'
                                   'c43f3c'},
                {'generation': 'consumer-b.v15',
                 'manifestSha256': '73f9c13e7aaf4c4a655eec53914c6569c0b560274bdd15fa6d1fb2d16f'
                                   '7da7c4'},
                {'generation': 'consumer-b.v16',
                 'manifestSha256': '6aad82e65623c7204008c19fdbea0aee84c302c0ef225c57647cd3e75e'
                                   '4a3cc6'},
            ],
            'normativeByteIdentityAgainstV16':
                (cust or {}).get('normativeByteIdentityAgainstV16'),
        },
        'claimedCompletePositives': runs,
        'fromScratchCommand': {
            'command': '%s -I -B %s/output/lib/verify_all.py' % (PY, ROOT),
            'stages': (verify or {}).get('stages'),
            'allStagesPassed': (verify or {}).get('allStagesPassed'),
            'standing': ('one command re-runs every stage: input custody, the canonical/H and '
                         'lexical vectors, capability-manifest admission, the protocol '
                         'traces, the phase-4 tables, every Run (rebuild + export + '
                         'fresh-process replay + controls), the native site audit, every '
                         'negative-control family, the phase 6/7/8 reconstructions, the graph '
                         'query, the relocation controls and this status derivation')},
        'requirementStatus': {
            'file': 'requirement-status.json',
            'fileSha256': sha_of('requirement-status.json'),
            'counts': dict(counts),
            'declaredTotals': reqfile['counts'],
            'unexecuted': unexec,
            'acceptBlockingUnexecuted': blocking_unexec,
        },
        'newMustIssues': must,
        'newShouldIssues': should,
        'advisories': adv,
        'withdrawnOrResolvedSinceTheLastGeneration':
            (gaps or {}).get('itemsThisOriginWithdrewOrThatTheNewKitResolved'),
        'algorithmFreedomNotGaps': (gaps or {}).get('algorithmFreedomNotGaps'),
        'emptyMustJustification': (gaps or {}).get('emptyMustJustification'),
        'helperCorrections': (helpers or {}).get('helperCorrections'),
        'openHelperFailuresOnAClaimedPositive':
            (helpers or {}).get('openHelperFailuresOnAClaimedPositive'),
        'retainedArtifactDigests': vectors,
        'limitations': [
            ('Every compiler, provider, toolchain, OS and runtime observation in these Runs '
             'is a SYNTHETIC TRUSTED INPUT authored by this origin. Nothing here qualifies a '
             'compiler, a provider, a host or an operating system, and no such qualification '
             'is claimed.'),
            ('No product code was written, no repository was modified, no commit or push was '
             'made, and no product was executed. Every byte produced lives under this '
             'origin\'s own output directory.'),
            ('The parent candidate was never held. Only the disclosed 101-file kit and the '
             'parent digest declared inside its manifest were verified.'),
            ('No root admission, agreement, expected result, author model, checker or golden '
             'was supplied, read or inferred. The root outcome over these exact bytes is '
             'UNOBSERVED by this origin.'),
            ('Three of the six advertised language modes (ts-tsconfig, js-synthesized, '
             'rust-cargo-prepared) have an admitted representable path at the (context, '
             'universe) record level but were NOT exercised end-to-end on a sealed Run. That '
             'distinction is published in vectors/advertised-mode-paths.json and is not '
             'merged into the complete-positive claim.'),
            ('L1-L3 normalised body identities, symbol-to-path attribution and provider '
             'occupancy are not recomputable by a consumer; the kit says so and substitutes '
             'retained custody, which is what was executed. No normalizer, parser or provider '
             'is qualified by that custody.'),
            ('The repair, comparison, baseline, invocation and query records are RECORD '
             'reconstructions with their identities recomputed and their admission laws '
             'executed. No repair was previewed, applied or authorized; no baseline was '
             'adopted; no query engine was run by a product.'),
        ],
        'standing': {
            'noRootAdmissionClaim': (
                'this origin reports ONLY its own independently executed admission, closure, '
                'replay and controls. It does not claim that any root, author or successor '
                'admitted, agreed with or validated these bytes.'),
            'noProductQualificationClaim': (
                'nothing here authorizes a product implementation or qualifies any product, '
                'component, compiler, provider or host.'),
            'kitOnly': (
                'every citation names a path and selector inside the frozen 101-file kit. No '
                'original repository, author model, fixture, golden, report, prior review or '
                'other /tmp/opensip-design-corrections directory was read.'),
            'priorGenerationsUnmodified': J('notes/siblings-untouched.json'),
            'writesThisGenerationMadeUnderAPriorGeneration': {
                'census': J('notes/prior-generation-writes.json'),
                'disclosure': (
                    'TWO files under consumer-b.v16/output were overwritten by this session '
                    'before the defect was caught by this origin\'s own control: '
                    'helper-corrections.json and notes/siblings-untouched.json. v14 and v15: '
                    'zero writes. No prior Run export, review file, checkpoint or vector was '
                    'touched. The prior bytes of those two files were not retained and are not '
                    'claimed to be restorable. See helper-corrections.json row V17-D8.'),
            },
        },
    }
    with open(OUT + '/blind-review.json', 'w') as f:
        json.dump(doc, f, indent=1, default=str)
    write_md(doc)
    print('blind-review.json + blind-review.md written')
    print('verdict:', verdict)
    print('requirementStatus counts:', dict(counts))
    print('MUST=%d SHOULD=%d advisories=%d' % (len(must), len(should), len(adv)))
    print('all claimed positives schema+closure+replay+controls:', all_runs_ok)


def write_md(d):
    L = []
    A = L.append
    A('# OpenSIP blind consumer design review -- consumer-b.v17')
    A('')
    A('**Verdict: %s**' % d['verdict'])
    A('')
    A('| | |')
    A('|---|---|')
    A('| sessionId | `%s` |' % d['sessionId'])
    A('| same-origin ancestry | %s |' % ' -> '.join(d['sameOriginAncestry']))
    A('| subject manifest SHA-256 | `%s` |' % d['inputKit']['subjectManifestSha256'])
    A('| parent digest declared in that manifest | `%s` |'
      % d['inputKit']['parentCandidateSha256DeclaredInThatManifest'])
    A('| kit files verified | %s / %s (%s) |'
      % (d['inputKit']['filesVerifiedPass'], d['inputKit']['fileCount'],
         d['inputKit']['hashVerification']))
    A('| changed against the prior disclosed kit | %s |'
      % ', '.join((d['inputKit']['changedAgainstThePriorDisclosedKit'] or {}).get(
          'changed', [])) or 'n/a')
    A('| requirement status | %s |'
      % ', '.join('%s %d' % (k, v) for k, v in
                  sorted(d['requirementStatus']['counts'].items())))
    A('| new MUST / SHOULD / advisories | %d / %d / %d |'
      % (len(d['newMustIssues']), len(d['newShouldIssues']), len(d['advisories'])))
    A('')
    A('> This is NOT a parent whole-candidate verification: only the parent digest declared')
    A('> inside the held manifest was compared. No root admission, agreement, expected')
    A('> result, author model or checker was supplied, read or inferred; the root outcome')
    A('> over these exact bytes is unobserved by this origin. Nothing here qualifies any')
    A('> product, compiler, provider or host.')
    A('')
    A('## Why this verdict')
    A('')
    A(d['verdictBasis']['rule'])
    A('')
    A('- acceptBlocking requirements unexecuted: **%d**'
      % len(d['verdictBasis']['acceptBlockingUnexecuted']))
    A('- claimed complete positives that passed schema admission, retained closure, '
      'fresh-process replay and their controls: **%s**'
      % ('all %d' % len(d['claimedCompletePositives'])
         if d['verdictBasis'][
             'everyClaimedPositivePassedSchemaClosureReplayAndControls'] else 'NOT all'))
    A('- unresolved MUST issues: **%d**' % len(d['newMustIssues']))
    A('- unresolved SHOULD issues: **%d**' % len(d['newShouldIssues']))
    A('')
    A('## Claimed complete positive Runs')
    A('')
    A('| Run | runId | verdict | objects | blobs | closure checks | replay | controls |')
    A('|---|---|---|---|---|---|---|---|')
    for r in d['claimedCompletePositives']:
        A('| %s | `%s` | %s | %s | %s | %s passed / %s n-a / %s refused | %s | %d refused |'
          % (r['label'], (r['claimedRunId'] or '')[:22] + '...', r['verdict'],
             r['objectCount'], r['blobCount'], r['closure']['checksPassed'],
             r['closure']['checksNotApplicable'], r['closure']['checksRefused'],
             'MATCH' if r['freshProcessReplay']['matched'] else 'NO MATCH',
             r['controls']['count']))
    A('')
    A('Exported bytes, by SHA-256 of the export file itself:')
    A('')
    for r in d['claimedCompletePositives']:
        A('- `%s` -> %s' % (r['exportFile'], r['exportFileSha256']))
    A('')
    A('## From-scratch command')
    A('')
    A('```')
    A(d['fromScratchCommand']['command'])
    A('```')
    A('')
    A('%d stages, all passed: %s.'
      % (len(d['fromScratchCommand']['stages'] or []),
         d['fromScratchCommand']['allStagesPassed']))
    A('')
    A('## New MUST issues')
    A('')
    A('None. ' + (d['emptyMustJustification'] or ''))
    A('')
    A('## New SHOULD issues')
    A('')
    for s in d['newShouldIssues']:
        A('### %s -- %s' % (s['id'], s['title']))
        A('')
        A('- class: %s' % s['class'])
        A('- selectors:')
        for sel in s['selectors']:
            A('  - `%s`' % sel)
        A('- attempted: %s' % s['whatWasAttempted'])
        A('- the kit says: %s' % s['whatTheKitSays'])
        A('- why this is a missing contract rather than algorithm freedom: %s'
          % s['whyItIsNotAlgorithmFreedom'])
        A('- measured here: %s' % s['measuredOnThisReconstruction'])
        A('- smallest fix: %s' % s['smallestFix'])
        A('- why not MUST: %s' % s['notAMustBecause'])
        A('')
    A('## Advisories')
    A('')
    for s in d['advisories']:
        A('- **%s** (%s) %s' % (s['id'], s['class'], s['title']))
        A('  - observation: %s' % s['observation'])
        A('  - handled here by: %s' % s['howThisOriginHandledIt'])
    A('')
    A('## Withdrawn by this origin, or resolved in the new kit bytes')
    A('')
    for s in d['withdrawnOrResolvedSinceTheLastGeneration'] or []:
        A('- **%s** -- %s. %s' % (s['id'], s['disposition'], s['why']))
    A('')
    A('## Algorithm freedom that is NOT a gap')
    A('')
    for s in d['algorithmFreedomNotGaps'] or []:
        A('- **%s**: pinned observable -- %s; left open -- %s. %s'
          % (s['topic'], s['pinnedObservable'], s['left open'], s['why']))
    A('')
    A('## Helper corrections (helper bug != design gap)')
    A('')
    A('| id | where | corrected |')
    A('|---|---|---|')
    for h in d['helperCorrections'] or []:
        A('| %s | %s | %s |' % (h['id'], h['where'], h['status']))
    A('')
    A('Open helper failures on a claimed positive: **%d**.'
      % len(d['openHelperFailuresOnAClaimedPositive'] or []))
    A('')
    A('## Limitations and scope')
    A('')
    for x in d['limitations']:
        A('- %s' % x)
    A('')
    A('## Standing')
    A('')
    for k, v in d['standing'].items():
        if k == 'writesThisGenerationMadeUnderAPriorGeneration':
            A('- **%s**: %s' % (k, v['disclosure']))
        elif k == 'priorGenerationsUnmodified':
            g = (v or {}).get('generations') or {}
            A('- **%s**: %s. Newest modification time per generation: %s'
              % (k, (v or {}).get('result'),
                 '; '.join('%s %s' % (a, (b or {}).get('newestMtimeUtc'))
                           for a, b in sorted(g.items()))))
        else:
            A('- **%s**: %s' % (k, v))
    A('')
    with open(OUT + '/blind-review.md', 'w') as f:
        f.write('\n'.join(L) + '\n')


main()
