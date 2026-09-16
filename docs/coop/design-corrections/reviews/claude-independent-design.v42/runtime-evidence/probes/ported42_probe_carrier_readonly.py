"""Independent read-only carrier precedence probe (ADV38-02) on real in-memory SQLite carriers.

The expected standing of every scenario is the reviewer's own reading of commit-recovery-readonly.v3.md section 1
precedence rows 1-4 (written below as a table, not derived from the model). The observed standing is the owner reference
dispatch of check-carrier-v3.py (_s37_open, mapped through carrier-dispatch.v3.json readOnlyStandingOfDispatchResult).
Each resulting public projection is validated against the actual evaluator3 StepTermination schema. The reference model has
no Step 4 stability observation, so a quarantine-class standing here assumes stable observations. Writes only
receipts/probes/carrier-readonly.json."""
import contextlib, importlib.util, io, json, sqlite3, sys, traceback
from pathlib import Path

RT = Path('/private/tmp/opensip-design-corrections/claude-independent-design.v42')
DC = RT / 'work/source42-pkg/docs/coop/design-corrections'
OUT = RT / 'receipts/probes/carrier-readonly.json'
ROWS = []


def row(case, ok, observed=None, expected=None):
    r = {'case': case, 'ok': bool(ok), 'observed': observed}
    if expected is not None:
        r['expected'] = expected
    ROWS.append(r)


def load(name, path, cwd=None):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        spec.loader.exec_module(module)
    return module, buf.getvalue()


import hashlib, os, shutil
# The exact disposable layout check-integrated-carrier.v1.py builds (scratch/proposal and scratch/patched), under this runtime.
T = RT / 'work/source42-pkg'
SCR = RT / 'work/carrier-scratch'
if SCR.exists():
    shutil.rmtree(SCR)
S = 'docs/coop/design-corrections/security/'
for rel in [S + x for x in ['carrier-highwater.schema.v1.json', 'carrier-dispatch.v3.json', 'carrier-format.v3.md', 'carrier-migration.v1.md',
                           'grant-journal.carrier.v3.sql', 'check-carrier-v3.py']] + \
           ['docs/v2/architecture/' + x for x in ['attempt-custody.schema.v1.json', 'carrier-fault-cases.v1.json', 'commit-recovery-readonly.v3.md']]:
    q = SCR / 'scratch/proposal' / rel
    q.parent.mkdir(parents=True, exist_ok=True)
    q.write_bytes((T / rel).read_bytes())
for name in ['commit-recovery-plan.v1.json', 'implementation-boundaries-and-build-plan.md']:
    q = SCR / 'scratch/patched' / name
    q.parent.mkdir(parents=True, exist_ok=True)
    q.write_bytes((T / 'docs/v2/architecture' / name).read_bytes())
saved_argv = sys.argv
sys.argv = [str(T / (S + 'check-carrier-v3.py')), str(T), str(SCR), str(SCR / 'report.json')]
try:
    K, text = load('p40_carrier', T / (S + 'check-carrier-v3.py'))
finally:
    sys.argv = saved_argv
# Harness restoration, not a law change: check-carrier-v3.py:451 binds _S37_CF to the carrier_format INSERT that its own
# _s37_publish uses, and :1166 later rebinds the same global name to the carrier-format.v3.md prose for a text check. After a
# full module run the publish helper therefore sees prose; restore exactly the :451 value before reusing the helper.
K._S37_CF = 'INSERT INTO carrier_format VALUES (?,?,?,?,?,?,?)'
owner_report = json.loads((SCR / 'report.json').read_text()) if (SCR / 'report.json').exists() else None
row('owner-carrier-validator-report', bool(owner_report) and not owner_report.get('failed'),
    {k: owner_report.get(k) for k in ('passed', 'failed', 'total')} if owner_report else None)
row('owner-carrier-checker-import-completed', True, text.strip().splitlines()[-1][:300] if text.strip() else '')
Q, _ = load('p40_qpm', DC / 'workflows/query_projection_model.v3.py')

E, OTHER = K._S37_ADMITTED, K._S37_OTHER
RO_MAP, PROJ = K._S37_RO_MAP, K._S37_PROJ


def conn():
    return sqlite3.connect(':memory:', isolation_level=None)


def cf2():
    c = conn()
    c.executescript(K.ddl2)
    c.execute(K._S37_GJ2, (1, 1, 'REV', K._OP, K._H, K._H))
    return c


def cf1():
    c = cf2()
    c.execute('DROP TRIGGER gj_seq_contiguous')
    return c


def published(kind, admitted=E):
    c = K._s37_carrier(kind)
    got = K._s37_publish(c, admitted=admitted)
    if got != 'published':
        # record the exact DDL refusal of this reviewer construction instead of guessing; then fail this scenario
        migrated = 'grant_journal' in {r[0] for r in c.execute('SELECT name FROM sqlite_master')}
        first = c.execute('SELECT MAX(grantGeneration) FROM grant_journal').fetchone()[0] + 1 if migrated else 1
        try:
            c.execute(K._S37_CF, (1, 3, admitted, first, 1, 2 if migrated else None, 'op-' + '9' * 32 if migrated else None))
            err = 'manual insert admitted'
        except sqlite3.Error as exc:
            err = type(exc).__name__ + ':' + str(exc)
        raise RuntimeError('publish returned %s; manual insert: %s' % (got, err))
    return c


def partial():
    c = K._s37_carrier('fresh')
    c.execute('DROP TRIGGER cf_no_delete')
    return c


def invalid_definition():
    c = K._s37_carrier('fresh')
    c.execute('DROP TRIGGER gj3_no_update')
    c.execute('CREATE TRIGGER gj3_no_update BEFORE UPDATE ON grant_journal_v3 BEGIN SELECT 1; END')
    return c


def split_brain():
    c = published('migrated')
    c.execute(K._S37_GJ2, (2, 1, 'REV', K._OP, K._H, K._H))
    return c


CARRIERS = {
    'absent-carrier (fresh-install dispatch)': conn,
    'carrierFormat1-unmigrated': cf1,
    'carrierFormat2-unmigrated': cf2,
    'fresh-install-prefix-B (no row)': lambda: K._s37_carrier('fresh'),
    'migration-prefix-A-B (no row)': lambda: K._s37_carrier('migrated'),
    'partial-object-set': partial,
    'all-names-invalid-definition': invalid_definition,
    'published-fresh (first_generation 1)': lambda: published('fresh'),
    'published-migrated (first_generation 2)': lambda: published('migrated'),
    'published-row-names-another-project': lambda: published('fresh', admitted=OTHER),
    'split-brain-F51': split_brain,
}
ASSOC = {'another-binding': {'journalCarrierDigest': OTHER, 'grantGeneration': 7},
         'generation-1': {'journalCarrierDigest': E, 'grantGeneration': 1},
         'generation-7': {'journalCarrierDigest': E, 'grantGeneration': 7}}
WITNESS = {'no-witness': None, 'witness-admitted': E, 'witness-another-project': OTHER}
QUAR, BUSY, INCOMP, CUST, BIND, SEAL = ('unknown-quarantine-condition', 'unavailable-busy', 'unknown-carrier-incompatible',
                                        'unknown-custody', 'binding-unusable', 'continue-to-SEAL-join')


def expected(carrier, assoc, witness):
    """Reviewer reading of commit-recovery-readonly.v3.md section 1 precedence (one journal snapshot, before the SEAL join)."""
    if assoc == 'another-binding':
        return BIND                                                     # row 1, before any carrier read
    if carrier == 'absent-carrier (fresh-install dispatch)':
        return CUST                                                     # row 4, object names alone
    if carrier in ('carrierFormat1-unmigrated', 'carrierFormat2-unmigrated'):
        return INCOMP                                                   # row 3, whatever generation or witness
    if carrier in ('partial-object-set', 'all-names-invalid-definition', 'published-row-names-another-project', 'split-brain-F51'):
        return QUAR                                                     # row 2 quarantine conditions
    if witness == 'witness-another-project':
        return QUAR                                                     # row 2: surviving witness naming another project
    if carrier.startswith('fresh-install-prefix') or carrier.startswith('migration-prefix'):
        return BUSY                                                     # row 2: unpublished lawful prefix
    if carrier.startswith('published-migrated') and assoc == 'generation-1':
        return INCOMP                                                   # row 2 tail: below first_generation
    return SEAL


def public(standing):
    p = PROJ['readOnlyRecovery'][standing]
    t = {'class': p['class'], 'errorCode': p['errorCode']}
    if p['faultCause']:
        t['faultCause'] = p['faultCause']
    if p['domainDetail']:
        t['domainDetail'] = {'code': p['domainDetail'], 'remedy': 'retry or restore custody'}
    try:
        Q.validate_schema(Q.COMMON_ID + '#/$defs/StepTermination', t)
        return t, True
    except Exception as exc:  # noqa: BLE001
        return t, str(exc).split('\n')[0][:160]


def main():
    seen = set()
    for cname, make in CARRIERS.items():
        for aname, assoc in ASSOC.items():
            for wname, witness in WITNESS.items():
                try:
                    c = make()
                except Exception as exc:  # noqa: BLE001 - a reviewer construction failure is recorded, never a pass
                    row('%s | %s | %s' % (cname, aname, wname), False, 'CONSTRUCTION-FAILED:' + str(exc)[:300], expected(cname, aname, wname))
                    continue
                before = c.execute('SELECT type, name, sql FROM sqlite_master ORDER BY name').fetchall()
                dispatch = K._s37_open(c, 'readOnlyRecovery', admitted=E, assoc=assoc, witness=witness)
                after = c.execute('SELECT type, name, sql FROM sqlite_master ORDER BY name').fetchall()
                got = SEAL if dispatch == 'carrierFormat3' else RO_MAP.get(dispatch, 'NO-STANDING:' + dispatch)
                want = expected(cname, aname, wname)
                row('%s | %s | %s' % (cname, aname, wname), got == want and before == after,
                    {'dispatch': dispatch, 'standing': got, 'schemaObjectsUnchanged': before == after}, want)
                if got not in (SEAL,) and not got.startswith('NO-STANDING'):
                    seen.add(got)
    for standing in sorted(seen):
        t, ok = public(standing)
        row('public-projection-is-a-valid-StepTermination: ' + standing, ok is True, {'termination': t, 'valid': ok})
    row('every-non-carrierFormat3-dispatch-result-has-one-read-only-standing',
        set(RO_MAP) >= {'carrierFormat1', 'carrierFormat2', 'fresh-install', 'incomplete-footprint', 'binding-unusable',
                        'carrier-project-binding-mismatch', 'migration-footprint-corrupt', 'split-brain-custody-condition',
                        'unknown-carrier-incompatible'} and 'carrierFormat3' not in RO_MAP, sorted(RO_MAP))
    row('read-only-projections-never-use-MIGRATION.CORRUPT',
        all(p.get('domainDetail') != 'MIGRATION.CORRUPT' for p in PROJ['readOnlyRecovery'].values()),
        {k: p.get('domainDetail') for k, p in PROJ['readOnlyRecovery'].items()})


try:
    main()
except Exception:  # noqa: BLE001
    row('probe-crashed', False, traceback.format_exc()[-2000:])
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps({'standing': 'independent reviewer probe over real in-memory SQLite carriers; reference dispatch; no OS durability or stability observation',
                           'rows': ROWS, 'failed': [r for r in ROWS if not r['ok']]}, indent=1, default=str))
print(json.dumps({'total': len(ROWS), 'failed': [(r['case'], r['observed'], r.get('expected')) for r in ROWS if not r['ok']]}, indent=1, default=str)[:6000])
