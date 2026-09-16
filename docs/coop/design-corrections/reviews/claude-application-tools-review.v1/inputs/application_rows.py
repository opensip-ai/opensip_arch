"""Read the selected prospective row map; refuse prose/JSON drift before assembly."""
import json
import re
from pathlib import Path


def load_rows(draft, expected_ids):
    draft = Path(draft)
    document = json.loads((draft / 'readiness-row-map.proposed.json').read_text())
    rows = document['rows']
    assert [row['id'] for row in rows] == list(expected_ids), 'Condition2 row IDs/order changed'
    register = (draft / 'files/docs/v2/architecture/08-decision-and-readiness-register.md').read_text()
    header = '| Existing row | Accepted design disposition |'
    assert register.count(header) == 1, 'Expected one current disposition table'
    cells = {}
    for line in register.split(header, 1)[1].splitlines():
        if not line.strip():
            if cells:
                break
            continue
        assert line.startswith('|') and line.endswith('|'), 'Malformed disposition table'
        columns = [x.strip() for x in line[1:-1].split('|')]
        assert len(columns) == 2, 'Malformed disposition row'
        if all(re.fullmatch(r'[-: ]+', x) for x in columns):
            continue
        key, value = columns
        assert key not in cells, 'Duplicate disposition row: ' + key
        cells[key] = value
    assert list(cells) == list(expected_ids), 'Markdown disposition IDs/order changed'
    for row in rows:
        assert row['disposition'] == cells[row['id']], 'Markdown/JSON disposition drift: ' + row['id']
        assert row['productQualified'] is False, 'Draft cannot grant product qualification'
        assert row['independentGrade'] == 'PENDING', 'Draft cannot assert independent acceptance'
    return rows
