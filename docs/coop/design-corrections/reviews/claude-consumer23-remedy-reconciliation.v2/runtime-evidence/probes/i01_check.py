"""I01 — consistency of reconciliation.md/json with the receipts, the recommended-edit anchors and the captured inputs."""
import hashlib, json, os

BASE = '/tmp/opensip-design-corrections/claude-consumer23-remedy-reconciliation.v2'
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
J = json.load(open(os.path.join(BASE, 'reconciliation.json')))
MD = open(os.path.join(BASE, 'reconciliation.md'), encoding='utf-8').read()
C, bad = {}, []


def chk(name, cond):
    C[name] = bool(cond)
    print('%-90s %s' % (name, 'OK' if cond else 'FAIL'))
    if not cond:
        bad.append(name)


chk('standing is not acceptance', 'NOT independent acceptance' in J['standing'] and 'NOT successor acceptance' in J['standing'] and J['grantsNothing'] is True)
chk('input digests match files', J['inputs']['authorReportMd'] == sha(os.path.join(BASE, 'author-report.md')) and J['inputs']['authorReportJson'] == sha(os.path.join(BASE, 'author-report.json'))
    and J['inputs']['afterManifest'] == sha(os.path.join(BASE, 'after-manifest.json')))
chk('three issues with verdicts', J['issues']['1-S1-schema-first']['verdict'].startswith('COHERENT') and J['issues']['2-native-schema-annotation']['verdict'].startswith('KEEP EXACT')
    and J['issues']['3-section10-scope']['verdict'].startswith('REAL SCOPE CONFLATION'))
chk('diff digest matches', J['recommendedEditsRehearsal']['diffSha256'] == sha(os.path.join(BASE, 'recommended-edits.diff')))
chk('all anchors exactly once', J['recommendedEditsRehearsal']['allAnchorsExactlyOnceInAuthorImages'])
edits = [e for k in J['issues'] for e in J['issues'][k]['recommendedEdits']]
chk('five recommended edits', len(edits) == 5)
norm = lambda s: ' '.join(s.replace('>', ' ').split())
mdn = norm(MD)
for e in edits:
    chk('md carries recommended text for issue %d (%s)' % (e['issue'], e['file'].split('/')[-1]),
        norm(e['text'])[:160] in mdn if e['file'].endswith('.md') else 'STAGE\'s native primary deficiency' in MD)
chk('receipt digests still match', all(sha(os.path.join(BASE, 'receipts', f)) == h for f, h in J['receipts'].items()))
for tok in ('not independent acceptance', 'PARAMS_MALFORMED', 'ENDPOINT_AMBIGUOUS', 'publicD9Termination', 'payloadSchemaDigest', 'invariant-one-mapper',
            'concurrentConditionReducer', 'secondaryDeficiencies', 'none-in-entry', 'TCB-SCOPE-01', '32 product gates', '54 planned recovery', 'recommended-edits.diff'):
    chk('md states %r' % tok, tok.lower() in MD.lower())
C['failed'] = bad
C['reconciliationJsonSha256'] = sha(os.path.join(BASE, 'reconciliation.json'))
C['reconciliationMdSha256'] = sha(os.path.join(BASE, 'reconciliation.md'))
json.dump(C, open(os.path.join(BASE, 'receipts', 'i01-check.json'), 'w'), indent=1)
print('\nchecks %d failed %d | json %s | md %s' % (len([v for v in C.values() if isinstance(v, bool)]), len(bad), C['reconciliationJsonSha256'], C['reconciliationMdSha256']))
