"""Check the r124 front door against its current records; ordinary file reads only."""
from pathlib import Path
import json
import re

PREFIX = 'status/2026-10-22-r124/'
ROLES = ('UPDATE-PROTOCOL.md', 'accepted-work.json', 'bindings-since-plan-cutoff.json',
         'decisions.json', 'unit-register.json', 'source.json')


def validate(board, ledger, source, checks):
    links = re.findall(r'\[[^\]]*\]\(([^)]+)\)', board)
    for role in ROLES:
        actual = [link for link in links if link.rsplit('/', 1)[-1] == role]
        if actual != [PREFIX + role]:
            raise ValueError('wrong current-record link: ' + role)
    header = board.splitlines()[2]
    if 'E405' not in header or 'planning-only callback-price publication' not in header:
        raise ValueError('wrong current delta summary')
    if '**M3 is not complete.**' not in header:
        raise ValueError('M3 completion standing changed')
    records = ledger['records']
    if len(records) != 405 or [row['id'] for row in records[-1:]] != ['E405']:
        raise ValueError('current accepted-work population differs')
    if source['acceptedScopedRecords'] != 405 or checks['scopedRecords'] != 405:
        raise ValueError('current machine-record population differs')
    if source['productQualification'] is not False or checks['entirePlanComplete'] is not False:
        raise ValueError('project standing changed')
    for record in records[-1:]:
        evidence = record['recordedEvidence']
        for field in ['mainProductUnitIntegrated', 'productCodeChanged', 'nativeExecutionAuthorized',
                      'unitAcceptance', 'productQualification']:
            if evidence[field] is not False:
                raise ValueError('planning publication overclaim: ' + field)
    return {'currentRecordLinks': len(ROLES), 'acceptedScopedRecords': 405,
            'newPlanningPublicationRecords': 1, 'productQualification': False,
            'entireProjectComplete': False}


def main():
    records_dir = Path(__file__).parent
    board = (records_dir.parent.parent / 'IMPLEMENTATION-STATUS.md').read_text()
    load = lambda name: json.loads((records_dir / name).read_text())
    result = validate(board, load('accepted-work.json'), load('source.json'), load('checks.json'))
    # Memory-only regressions exercise each current routing role and the header.
    refused = []
    for role in ROLES:
        bad = board.replace(PREFIX + role, 'status/2026-10-22-r123/' + role)
        try:
            validate(bad, load('accepted-work.json'), load('source.json'), load('checks.json'))
        except ValueError as error:
            assert str(error) == 'wrong current-record link: ' + role
            refused.append(role)
        else:
            raise AssertionError('stale current-record link accepted: ' + role)
    bad = board.replace('E405', 'E403-E404', 1)
    try:
        validate(bad, load('accepted-work.json'), load('source.json'), load('checks.json'))
    except ValueError as error:
        assert str(error) == 'wrong current delta summary'
        refused.append('delta-header')
    else:
        raise AssertionError('stale delta header accepted')
    print(json.dumps(dict(result, memoryOnlyRegressionsRefused=refused,
                          nativeToolsRun=False, physicalFixtures=False)))


if __name__ == '__main__':
    main()
