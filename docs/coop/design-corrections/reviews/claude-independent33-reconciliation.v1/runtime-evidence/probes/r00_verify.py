"""R00 — verify inputs, then test each R33-REC finding against my ACTUAL v33 review and the exact
cited code lines. Root is assessed, not rubber-stamped."""
import hashlib, json, os, re

V33 = '/tmp/opensip-design-corrections/claude-independent-design.v33'
SRC = '/tmp/opensip-design-corrections/candidate-subject.v33'
MAN = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v33.json'
OUT = '/tmp/opensip-design-corrections/claude-independent33-reconciliation.v1/receipts'
os.makedirs(OUT, exist_ok=True)
CHK = os.path.join(SRC, 'docs/coop/design-corrections/foundation/check-execution-inputs.v1.py')


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


R = {}
R['reviewJsonSha256'] = sha(os.path.join(V33, 'review.json'))
R['reviewMdSha256'] = sha(os.path.join(V33, 'review.md'))
R['rootQuotedJson'] = '800465853d626f49cdbaf48af2066b6a8e3e65f364d2a21a9263ab88a2eb0b90'
R['rootQuotedMd'] = 'f2f8a871ffaaee1c76aefb3b70bc30f9a65144fc85191e657ee9d103c03e77f3'
R['jsonMatches'] = R['reviewJsonSha256'] == R['rootQuotedJson']
R['mdMatches'] = R['reviewMdSha256'] == R['rootQuotedMd']
R['manifestSha256'] = sha(MAN)
R['manifestMatches'] = R['manifestSha256'] == '1cf3db70d4b73b0c42f1393331e6a874ee26f7ddf67aa05c6ac15a5753069299'
man = {f['path']: f for f in json.load(open(MAN))['files']}
R['manifestFiles'] = len(man)
print('my review.json/md match root quotes:', R['jsonMatches'], R['mdMatches'])
print('source33 manifest matches, files   :', R['manifestMatches'], R['manifestFiles'])
V = json.load(open(os.path.join(V33, 'review.json')))
MD = open(os.path.join(V33, 'review.md'), encoding='utf-8').read()

L = open(CHK, encoding='utf-8').read().splitlines()
R['checkerSha256'] = sha(CHK)
R['checkerLines'] = len(L)


def line(n):
    return L[n - 1].strip() if 0 < n <= len(L) else '<out of range>'


# ---------------- R33-REC-03: the exact cited lines ----------------
print('\n=== R33-REC-03: cited checker lines ===')
for n in (751, 886, 1177, 1180, 1185, 1187):
    print('%5d  %s' % (n, line(n)[:150]))
R['line751'] = line(751)
R['lines1177_1187'] = [line(n) for n in range(1177, 1188)]
R['line886'] = line(886)
R['fullRunUsesAdmissionDigestVsProof'] = bool(
    re.search(r'admission_digest', line(751)) and re.search(r'executionInputsDigest', line(751)))
R['digest0AssertionIsInHelperUnit'] = any('digest0' in x for x in R['lines1177_1187'])
print('\nline 751 compares admission_digest to proof executionInputsDigest:',
      R['fullRunUsesAdmissionDigestVsProof'])
print('digest0 assertion lives in the 1177-1187 helper unit  :', R['digest0AssertionIsInHelperUnit'])
# what did MY review claim?
R['myReviewDigestClaim'] = V['sourceChangeAssessment']['executionInputsLaw']['fullRunColumn'][
    'digestEqualityAsserted']
R['myMdDigestClaim'] = 'executionInputsDigest == digest0' in MD
print('my review.json fullRunColumn claim:', R['myReviewDigestClaim'][:170])
print('my review.md quotes the digest0 form:', R['myMdDigestClaim'])
R['REC03_digestMiscited'] = R['myMdDigestClaim'] or 'digest0' in R['myReviewDigestClaim']

# owner-graph-two-universes standing
ctx886 = [line(n) for n in range(880, 895)]
R['context886'] = ctx886
print('\ncontext around 886:')
for i, x in enumerate(ctx886, 880):
    print('%5d  %s' % (i, x[:130]))
R['myTwoUniversesClaim'] = V['sourceChangeAssessment']['executionInputsLaw']['perUniverseAttribution']['assessment']
print('\nmy perUniverseAttribution claim:', R['myTwoUniversesClaim'][-200:])

# ---------------- R33-REC-01 ----------------
print('\n=== R33-REC-01 ===')
R['myRequestClaim'] = V['sourceChangeAssessment']['executionInputsLaw'][
    'requestVersusSelectionVersusDisclosure']['assessment']
print('my claim:', R['myRequestClaim'][-260:])
R['REC01_claimsNoProviderExecution'] = 'not forced to execute a provider' in R['myRequestClaim']
R['REC01_inMd'] = 'not forced to execute a provider to close' in MD
print('claims "not forced to execute a provider" in json/md:',
      R['REC01_claimsNoProviderExecution'], R['REC01_inMd'])
# what does the control actually establish?
idx = [i for i, x in enumerate(L, 1) if 'optional-unsupported-cell-owes-no-required-cell-row' in x]
R['optionalUnsupportedControlLines'] = idx
print('control defined at lines:', idx)
for n in idx[:2]:
    for k in range(max(1, n - 12), n + 4):
        print('%5d  %s' % (k, line(k)[:140]))

# ---------------- R33-REC-02 ----------------
print('\n=== R33-REC-02 ===')
p09 = json.load(open(os.path.join(V33, 'receipts', 'p09-optional33.json')))
R['p09Assessment'] = p09['assessment']
R['p09FullRunFlag'] = p09['optionalFullRunClosesWithoutRequiredDeficiency']
R['p09CandidateFlag'] = p09['candidateRefsOnlyWhenEnvelopeExists']
optcand = [c for c in p09['optionalCases'] if 'candidate' in c['case']]
R['optionalCandidateCases'] = optcand
print('optional candidate cases in p09:')
for c in optcand:
    print('   %-52s result=%-7s fullRunId=%s' % (c['case'][:52], c['result'], c['fullRunId']))
fullrun = [c for c in p09['optionalCases'] if c['fullRunId']]
R['p09FullRunCases'] = [{'case': c['case'], 'runId': c['fullRunId']} for c in fullrun]
print('full-Run cases in p09:', [(c['case'][:46], str(c['fullRunId'])[:24]) for c in fullrun])
R['REC02_differentFixtures'] = (optcand and fullrun
                                and optcand[0]['case'] != fullrun[0]['case']
                                and optcand[0]['fullRunId'] is None)
print('optional-candidate case has NO fullRunId and the fullRun case is a DIFFERENT fixture:',
      R['REC02_differentFixtures'])
extra = [c for c in json.load(open(os.path.join(V33, 'receipts', 'p04-newlawcontrols.json')))['refusingControls']
         if 'extra-candidate-ref' in c['case']]
R['extraCandidateRefusals'] = extra
print('extra-candidate-ref-no-outcome refusals:', json.dumps(extra)[:200])
R['REC02_extraCandidateNotIsolating'] = any(
    len(c.get('refusals', [])) > 1 for c in extra)

json.dump(R, open(os.path.join(OUT, 'r00-verify.json'), 'w'), indent=1, default=str)
print('\nwrote r00-verify.json')
