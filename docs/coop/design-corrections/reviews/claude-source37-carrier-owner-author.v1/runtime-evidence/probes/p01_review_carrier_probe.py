"""Replay of the independent review's P-CARRIER probe over one disposable copy (argv[1] = baseline | edited).

Two input sets are recorded and never merged:
  reviewExact  - the review's exact rows, including its format row (first_generation 5, migrated_from NULL);
  lawfulRow    - the same grammar and footprint cases with a format row that is lawful under the corrected
                 DDL (fresh: first_generation 1; migrated: first_generation >= 2 with migration op ref),
                 so a grammar refusal cannot be confused with a format-row refusal.
Reference evidence only; in-memory SQLite; no OS durability.
"""
import hashlib, json, sqlite3, sys
from pathlib import Path

BASE = Path('/tmp/opensip-design-corrections/claude-source37-carrier-owner-author.v1')
COPY = sys.argv[1]
SRC = BASE / 'work' / COPY
V3 = SRC / 'docs/coop/design-corrections/security/grant-journal.carrier.v3.sql'
V2 = SRC / 'docs/coop/completion/security-schemas.v2/grant-journal.sql'
AC = SRC / 'docs/v2/architecture/attempt-custody.schema.v1.json'
ddl3, ddl2 = V3.read_text(), V2.read_text()
ac_sql = json.loads(AC.read_text())['proposedPrivateDDL']
hx = 'b' * 64
OP = 'op-' + 'a' * 32
RUN = 'run3:' + 'c' * 64
INS = ("INSERT INTO grant_journal_v3 (grantGeneration,seq,record_schema,record_type,operation_ref,run_id,body,body_sha256,prev_sha256)"
       " VALUES (?,?,?,?,?,?,?,?,?)")


def attempt(con, sql, args=()):
    try:
        con.execute(sql, args)
        return 'ADMIT'
    except sqlite3.DatabaseError as e:
        return 'REFUSE:' + str(e)


def db(row):
    con = sqlite3.connect(':memory:', isolation_level=None)
    con.executescript(ddl3)
    if row is not None:
        con.execute('INSERT INTO carrier_format VALUES (?,?,?,?,?,?,?)', row)
    return con


def cases(row, gen):
    out = {}
    out['formatRow'] = attempt(sqlite3.connect(':memory:', isolation_level=None), 'SELECT 1')
    c = sqlite3.connect(':memory:', isolation_level=None)
    c.executescript(ddl3)
    out['formatRowAdmitted'] = attempt(c, 'INSERT INTO carrier_format VALUES (?,?,?,?,?,?,?)', row)
    del out['formatRow']
    out['lawful_seal'] = attempt(db(row), INS, (gen, 1, 3, 'SEAL', OP, RUN, '{}', hx, hx))
    out['op_ref_nonhex_uppercase'] = attempt(db(row), INS, (gen, 1, 3, 'SEAL', 'op-a' + 'Z' * 31, RUN, '{}', hx, hx))
    out['op_ref_uppercase_hex'] = attempt(db(row), INS, (gen, 1, 3, 'SEAL', 'op-' + 'A' * 32, RUN, '{}', hx, hx))
    out['run_id_nonhex_tail'] = attempt(db(row), INS, (gen, 1, 3, 'SEAL', OP, 'run3:c' + 'Q' * 63, '{}', hx, hx))
    out['body_sha256_nonhex'] = attempt(db(row), INS, (gen, 1, 3, 'SEAL', OP, RUN, '{}', 'Z' * 64, hx))
    out['prev_sha256_uppercase'] = attempt(db(row), INS, (gen, 1, 3, 'SEAL', OP, RUN, '{}', hx, 'B' * 64))
    grant = ("INSERT INTO grant_journal_v3 (grantGeneration,seq,record_schema,record_type,operation_ref,token,"
             "install_generation_id,manifest_digest,platform,body,body_sha256,prev_sha256) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)")
    out['grant_manifest_lawful'] = attempt(db(row), grant, (gen, 1, 3, 'GRANT', OP, 'PT', 'ig1', 'c' * 64, 'macos-x86_64', '{}', hx, hx))
    out['grant_manifest_nonhex'] = attempt(db(row), grant, (gen, 1, 3, 'GRANT', OP, 'PT', 'ig1', 'c' + 'G' * 63, 'macos-x86_64', '{}', hx, hx))
    bad_pkd = list(row)
    bad_pkd[2] = 'a' + 'X' * 63
    out['project_key_digest_nonhex_tail'] = attempt(db(None), 'INSERT INTO carrier_format VALUES (?,?,?,?,?,?,?)', tuple(bad_pkd))
    bad_mig = (1, 3, 'a' * 64, 5, 1, 2, 'op-a' + 'Z' * 31)
    out['migration_op_ref_nonhex_tail'] = attempt(db(None), 'INSERT INTO carrier_format VALUES (?,?,?,?,?,?,?)', bad_mig)
    a = sqlite3.connect(':memory:', isolation_level=None)
    a.executescript(ac_sql)
    acq = 'INSERT INTO attempt_custody VALUES (?,?,?,?,1,?,NULL)'
    out['attempt_custody_lawful'] = attempt(a, acq, ('a' * 64, 'ns', 'exec1_' + 'a' * 32, OP, 'admitted'))
    out['attempt_custody_execution_id_nonhex_tail'] = attempt(a, acq, ('a' * 64, 'ns2', 'exec1_a' + 'Z' * 31, OP, 'admitted'))
    out['attempt_custody_store_digest_nonhex_tail'] = attempt(a, acq, ('a' + 'Z' * 63, 'ns3', 'exec1_' + 'a' * 32, OP, 'admitted'))
    out['attempt_custody_op_ref_nonhex_tail'] = attempt(a, acq, ('a' * 64, 'ns4', 'exec1_' + 'a' * 32, 'op-a' + 'Z' * 31, 'admitted'))
    # incomplete footprint {A,B}: seven objects present, no format row
    c = db(None)
    out['append_without_format_row'] = attempt(c, INS, (1, 1, 3, 'REV', OP, None, '{}', hx, hx))
    rows = [r[0] for r in c.execute('SELECT grantGeneration FROM grant_journal_v3')]
    pub = attempt(c, 'INSERT INTO carrier_format VALUES (?,?,?,?,?,?,?)', row)
    first = row[3]
    out['publication_after_attempted_append'] = {'publication': pub, 'v3GenerationsBelowFirst': [g for g in rows if g < first]}
    return out


rec = {'copy': COPY, 'v3Sha256': hashlib.sha256(V3.read_bytes()).hexdigest(),
       'attemptCustodySha256': hashlib.sha256(AC.read_bytes()).hexdigest(),
       'v2Sha256': hashlib.sha256(V2.read_bytes()).hexdigest(),
       'reviewExact': cases((1, 3, 'a' * 64, 5, 1, None, None), 5),
       'lawfulRowFresh': cases((1, 3, 'a' * 64, 1, 1, None, None), 1),
       'lawfulRowMigrated': cases((1, 3, 'a' * 64, 5, 1, 2, 'op-' + 'd' * 32), 5)}
c2 = sqlite3.connect(':memory:', isolation_level=None)
c2.executescript(ddl2)
rec['historicalV2'] = {
    'operation_ref_check_text': [l.strip() for l in ddl2.splitlines() if 'operation_ref' in l][:2],
    'op_ref_nonhex_uppercase_admitted_by_historical_bytes': attempt(
        c2, 'INSERT INTO grant_journal (grantGeneration,seq,record_type,operation_ref,body,body_sha256,prev_sha256) VALUES (1,1,?,?,?,?,?)',
        ('REV', 'op-a' + 'Z' * 31, '{}', hx, hx))}
out = BASE / 'receipts' / ('p01-review-carrier-probe.' + COPY + '.json')
if out.exists():
    raise SystemExit('preserve earlier receipt: ' + str(out))
out.write_text(json.dumps(rec, indent=1) + '\n')
print(json.dumps(rec, indent=1))
