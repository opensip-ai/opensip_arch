"""Independent probe P-CARRIER: does the carrierFormat 3 DDL enforce the laws its prose claims?

Checks (in-memory SQLite, frozen DDL bytes from the verified copy):
  1. operation_ref 'op-' + 32 lowercase hex grammar (carrier-format.v3 §5 claims preserved)
  2. run_id run3 grammar and body_sha256 hex
  3. first_generation law before the carrier_format row exists (incomplete footprint {A,B})
  4. same checks against the inherited carrierFormat 2 DDL for attribution (inherited vs new)
Reference evidence only; no OS durability.
"""
import json, sqlite3, hashlib

SRC = '/tmp/opensip-design-corrections/claude-independent-design.v37/work/source37'
V3 = SRC + '/docs/coop/design-corrections/security/grant-journal.carrier.v3.sql'
V2 = SRC + '/docs/coop/completion/security-schemas.v2/grant-journal.sql'
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v37/receipts/probe-carrier-ddl.json'
res = {'v3Sha256': hashlib.sha256(open(V3, 'rb').read()).hexdigest()}


def try_exec(con, sql, args=()):
    try:
        con.execute(sql, args)
        return 'ADMIT'
    except sqlite3.DatabaseError as e:
        return 'REFUSE:' + str(e)


def v3_db(with_row=True):
    con = sqlite3.connect(':memory:', isolation_level=None)
    con.executescript(open(V3).read())
    if with_row:
        con.execute("INSERT INTO carrier_format VALUES (1,3,?,5,1,NULL,NULL)", ('a' * 64,))
    return con

ins = ("INSERT INTO grant_journal_v3 (grantGeneration,seq,record_schema,record_type,operation_ref,run_id,body,body_sha256,prev_sha256)"
       " VALUES (?,?,?,?,?,?,?,?,?)")
hx = 'b' * 64
con = v3_db()
res['v3_lawful_seal'] = try_exec(con, ins, (5, 1, 3, 'SEAL', 'op-' + 'a' * 32, 'run3:' + 'c' * 64, '{}', hx, hx))
con = v3_db()
res['v3_op_ref_nonhex_uppercase'] = try_exec(con, ins, (5, 1, 3, 'SEAL', 'op-a' + 'Z' * 31, 'run3:' + 'c' * 64, '{}', hx, hx))
con = v3_db()
res['v3_run_id_nonhex_tail'] = try_exec(con, ins, (5, 1, 3, 'SEAL', 'op-' + 'a' * 32, 'run3:c' + 'Q' * 63, '{}', hx, hx))
con = v3_db()
res['v3_body_sha256_nonhex'] = try_exec(con, ins, (5, 1, 3, 'SEAL', 'op-' + 'a' * 32, 'run3:' + 'c' * 64, '{}', 'Z' * 64, 'Z' * 64))
con = v3_db(with_row=False)
res['v3_project_key_digest_nonhex_tail'] = try_exec(con, "INSERT INTO carrier_format VALUES (1,3,?,5,1,NULL,NULL)", ('a' + 'X' * 63,))
con = v3_db(with_row=False)
res['v3_migration_op_ref_nonhex_tail'] = try_exec(con, "INSERT INTO carrier_format VALUES (1,3,?,5,1,2,?)", ('a' * 64, 'op-a' + 'Z' * 31))
ac_sql = json.load(open(SRC + '/docs/v2/architecture/attempt-custody.schema.v1.json'))['proposedPrivateDDL']
ac = sqlite3.connect(':memory:', isolation_level=None)
ac.executescript(ac_sql)
res['attempt_custody_execution_id_nonhex_tail'] = try_exec(ac, "INSERT INTO attempt_custody VALUES (?,?,?,?,1,'admitted',NULL)", ('a' * 64, 'ns', 'exec1_a' + 'Z' * 31, 'op-' + 'a' * 32))
# incomplete footprint {A,B}: objects present, no carrier_format row
con = v3_db(with_row=False)
res['v3_append_without_format_row_gen1'] = try_exec(con, ins, (1, 1, 3, 'REV', 'op-' + 'a' * 32, None, '{}', hx, hx))
try:
    con.execute("INSERT INTO carrier_format VALUES (1,3,?,5,1,2,?)", (hx, 'op-' + 'd' * 32))
    rows = con.execute('SELECT grantGeneration FROM grant_journal_v3').fetchall()
    res['v3_row_published_after_lower_generation_append'] = {'formatRowAdmitted': True, 'v3GenerationsBelowFirst': [r[0] for r in rows if r[0] < 5]}
except sqlite3.DatabaseError as e:
    res['v3_row_published_after_lower_generation_append'] = 'REFUSE:' + str(e)
# inherited carrierFormat 2 attribution
try:
    c2 = sqlite3.connect(':memory:', isolation_level=None)
    c2.executescript(open(V2).read())
    cols = [r[1] for r in c2.execute('PRAGMA table_info(grant_journal)')]
    res['v2_columns'] = cols
    sqltext = open(V2).read()
    res['v2_operation_ref_check_text'] = [l.strip() for l in sqltext.splitlines() if 'operation_ref' in l][:4]
except Exception as e:
    res['v2_error'] = repr(e)
res['interpretation'] = {
    'claim': 'carrier-format.v3 §5 lists operation_ref grammar op- plus 32 lowercase hex among laws preserved/re-executed',
    'ddlGlobOnlyChecksFirstCharacter': res['v3_op_ref_nonhex_uppercase'] == 'ADMIT'}
json.dump(res, open(OUT, 'w'), indent=1)
print(json.dumps(res, indent=1))
