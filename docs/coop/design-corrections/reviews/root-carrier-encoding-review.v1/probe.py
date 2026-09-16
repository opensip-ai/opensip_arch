from pathlib import Path
import sqlite3, json, re, hashlib
ROOT = Path(__file__).parent
carrier = (ROOT / 'captured-carrier.sql').read_text()
attempt = json.loads((ROOT / 'captured-attempt.json').read_text())['proposedPrivateDDL']
rows = []
for label, original, table, sql, lawful in [
    ('carrier', carrier, 'carrier_format', 'INSERT INTO carrier_format VALUES(1,3,?,1,1,NULL,NULL)', 'a' * 64),
    ('attempt', attempt, 'attempt_custody', "INSERT INTO attempt_custody VALUES(?,'ns',? ,?,1,'admitted',NULL)", 'a' * 64),
]:
    alternative, replacements = re.subn(r'length\(CAST\((\w+) AS BLOB\)\) = \d+', r'instr(\1, char(0)) = 0', original)
    for variant, ddl in [('captured-v2', original), ('NUL-guard-alternative', alternative)]:
        for encoding in ['UTF-8', 'UTF-16le', 'UTF-16be']:
            for case, value in [('lawful', lawful), ('NUL-suffix', lawful + '\x00Z'), ('ASCIIhexBLOB', lawful.encode()), ('uppercase', lawful[:-1] + 'A')]:
                connection = sqlite3.connect(':memory:')
                connection.execute("PRAGMA encoding = '%s'" % encoding)
                connection.executescript(ddl)
                args = (value,) if label == 'carrier' else (value, 'exec1_' + 'a' * 32, 'op-' + 'a' * 32)
                try:
                    connection.execute(sql, args)
                    result = 'ADMIT'
                    error = None
                except sqlite3.Error as exc:
                    result = 'REFUSE'
                    error = str(exc)
                observed_encoding = connection.execute('PRAGMA encoding').fetchone()[0]
                rows.append({'table': table, 'variant': variant, 'encoding': observed_encoding, 'case': case, 'result': result, 'error': error})
                connection.close()
    assert replacements > 0
report = {'standing': 'Root captured provisional coauthor-v2 bytes. In-memory SQLite grammar comparison only; not final author assessment or product qualification.', 'inputs': {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in ['captured-carrier.sql', 'captured-attempt.json']}, 'rows': rows}
(ROOT / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
for row in rows:
    if row['case'] == 'lawful' or (row['case'] != 'lawful' and row['result'] != 'REFUSE'):
        print({key: row[key] for key in ['table', 'variant', 'encoding', 'case', 'result']})
