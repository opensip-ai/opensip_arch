"""READ-ONLY diagnostic (generation 22): one-screen summary of the last from-scratch command --
failed stages, claimed-positive audit refusals, measured read-graph findings, requirement status
and the deliverable verdict conditions. Writes nothing."""
import collections
import json

OUT = '/tmp/opensip-design-corrections/consumer-b.v23/output'


def J(rel):
    try:
        return json.load(open(OUT + '/' + rel))
    except Exception as e:
        return {'_error': str(e)}


def main():
    va = J('verify-all.json')
    print('stages recorded %s / declared %s; failed %s' % (va.get('stagesRecorded'), va.get('declaredStageCount'),
                                                          va.get('failedStages')))
    print('static guard violations', (va.get('readOrderGuard') or {}).get('violations'))
    au = J('vectors/claimed-positive-audit.json')
    print('audit', au.get('counts'), au.get('evidenceClassCounts'))
    for k, r in sorted((au.get('requirements') or {}).items()):
        if r.get('result') == 'FAIL':
            print('  FAIL %s [%s] %s' % (k, r['evidenceClass'], json.dumps(
                [(c['check'], c['detail']) for c in r['refusals'][:3]], default=str)[:700]))
    rg = J('notes/v22-read-graph.json')
    print('read graph', rg.get('result'), 'stagesLogged', rg.get('stagesLogged'),
          'dir==', rg.get('commandStageIoDir') == va.get('stageIoDir'))
    for x in rg.get('orderViolations') or []:
        print('  ORDER', x)
    for x in rg.get('undeclaredEdges') or []:
        print('  UNDECLARED', x)
    print('  UNKNOWN', dict(collections.Counter((x['reader'], x['artifact']) for x in
                                                rg.get('readsOfArtifactsNoStageWrote') or [])))
    st = J('requirement-status.json')
    print('status', dict(collections.Counter(v['status'] for v in st.values() if isinstance(v, dict))))
    print('  not executed', sorted(k for k, v in st.items() if isinstance(v, dict)
                                   and v['status'] in ('unexecuted', 'failed')))
    br = J('blind-review.json')
    print('verdict', br.get('verdict'))
    print('conditions', json.dumps((br.get('verdictBasis') or {}).get('conditions'), default=str)[:900])
    hc = J('helper-corrections.json')
    print('helper rows', len(hc.get('helperCorrections') or []), 'open', hc.get('openHelperFailuresOnAClaimedPositive'))


main()
