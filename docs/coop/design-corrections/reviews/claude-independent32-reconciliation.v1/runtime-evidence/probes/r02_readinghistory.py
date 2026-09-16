"""R02 — establish the TRUTHFUL reading/execution history of check-replay.v3.py from the ORIGINAL
public receipts of my own prior runtimes. Inherited executed evidence is cited at its original
location and never relabelled as work done in this session."""
import hashlib, json, os

V31 = '/tmp/opensip-design-corrections/claude-independent-design.v31'
V32 = '/tmp/opensip-design-corrections/claude-independent-design.v32'
SRC = '/tmp/opensip-design-corrections/candidate-subject.v32'
OUT = '/tmp/opensip-design-corrections/claude-independent32-reconciliation.v1/receipts'
REL = 'docs/coop/design-corrections/foundation/check-replay.v3.py'
R = {'standing': 'inherited executed evidence cited at its original receipt location'}

cur = os.path.join(SRC, REL)
R['currentSha256'] = hashlib.sha256(open(cur, 'rb').read()).hexdigest()
R['currentBytes'] = os.path.getsize(cur)
print('current check-replay.v3.py sha=%s bytes=%d' % (R['currentSha256'][:20], R['currentBytes']))

# v31 receipts that executed it
for base, tag in ((V31, 'v31'), (V32, 'v32')):
    rdir = os.path.join(base, 'receipts')
    hits = []
    for n in sorted(os.listdir(rdir)):
        p = os.path.join(rdir, n)
        if not os.path.isfile(p) or not n.endswith('.json'):
            continue
        try:
            t = open(p, encoding='utf-8', errors='replace').read()
        except Exception:
            continue
        if 'check-replay.v3.py' in t:
            hits.append({'receipt': n, 'path': os.path.relpath(p, base),
                         'sha256OfReceipt': hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]})
    R[tag + 'ReceiptsNamingIt'] = hits
    print('\n%s receipts naming check-replay.v3.py (%d):' % (tag, len(hits)))
    for h in hits:
        print('   %-34s %s' % (h['receipt'], h['sha256OfReceipt']))

# what did those receipts actually record?
p06_31 = os.path.join(V31, 'receipts', 'p06-replayorder.json')
if os.path.isfile(p06_31):
    d = json.load(open(p06_31))
    R['v31_p06'] = {'frozenRunReturncode': d.get('frozenRun', {}).get('returncode'),
                    'branchIsLoadBearing': d.get('branchIsLoadBearing'),
                    'receiptPath': 'claude-independent-design.v31/receipts/p06-replayorder.json'}
    print('\nv31 p06-replayorder.json: frozen run rc=%s (this is where I first executed the post-28 bytes)'
          % R['v31_p06']['frozenRunReturncode'])
p06_32 = os.path.join(V32, 'receipts', 'p06-changedchecks.json')
if os.path.isfile(p06_32):
    d = json.load(open(p06_32))
    job = next((j for j in d['jobs'] if 'check-replay' in j['checker']), None)
    R['v32_p06'] = {'job': job, 'receiptPath': 'claude-independent-design.v32/receipts/p06-changedchecks.json'}
    print('v32 p06-changedchecks.json: %s rc=%s (%s)' % (job['checker'], job['returncode'],
                                                          job.get('justification')))

R['truthfulHistory'] = {
    'myReviewLineage': ['source26', 'source27', 'source31', 'source32',
                        'bounded glob/repair review (prospective bytes, no source version)',
                        'this source32 record reconciliation'],
    'noSource28ReviewSessionExists': True,
    'fileLastChangedWindow': '27->28',
    'whenIFirstReviewedThePost28Bytes': ('my source31 review, which assessed the whole 27->31 delta '
                                         'including the source28 ruleResults ordering work, and '
                                         'executed this checker there'),
    'whenIExecutedItAgain': 'the source32 review, as a changed-input run (the fixture had changed)',
    'whatIDidInThisSession': ('freshly READ the current bytes of this file in this reconciliation '
                              'runtime and confirmed the deep-copy fixture isolation the row is '
                              'about is present; I did NOT re-execute it here and claim no new '
                              'execution'),
    'correction': ('My v32 row said the file "was read fresh in that session" about the 27->28 '
                   'window. There was no source28 review session in my lineage, so that phrasing '
                   'asserted a session that does not exist.')}
print('\n' + json.dumps(R['truthfulHistory'], indent=1)[:900])
json.dump(R, open(os.path.join(OUT, 'r02-readinghistory.json'), 'w'), indent=1, default=str)
print('\nwrote r02-readinghistory.json')
