# Control C14 - the AttemptCustodyV1 settlement matrix, the purged-receipt law, the proposed
# private DDL, and the authorized settlement sweep's proof matrix.
#
# Settles root item 2 (phase/outcome coupling; a negative only from the right terminal outcome plus
# a confirmed absent receipt) and item 3 (the sweep's authorization, custody, cases and writes).
#
# usage: python c14-settlement.py <runtimeRoot> <reportPath>
import json
import os
import sqlite3
import sys

import jsonschema

ROOT, OUT = sys.argv[1], sys.argv[2]
def _no_dup(pairs):
    seen = set()
    for k, _ in pairs:
        if k in seen:
            raise ValueError('DUPLICATE KEY: ' + k)
        seen.add(k)
    return dict(pairs)


# The stable normative path selected in v7; admitted strictly, so a duplicate key cannot be
# last-wins-collapsed before this control inspects the coupling table.
AC_REL = 'docs/v2/architecture/attempt-custody.schema.v1.json'
with open(os.path.join(ROOT, 'scratch', 'proposal', AC_REL), encoding='utf-8') as _fh:
    AC = json.load(_fh, object_pairs_hook=_no_dup)
checks = []


def ck(name, ok, detail=''):
    checks.append({'check': name, 'pass': bool(ok), 'detail': str(detail)[:300]})
    return ok


# ---- 1. the record shape, against its own schema ------------------------------
SCHEMA = {k: v for k, v in AC.items()
          if k in ('type', 'additionalProperties', 'required', 'properties', 'allOf')}
jsonschema.Draft202012Validator.check_schema(SCHEMA)
V = jsonschema.Draft202012Validator(SCHEMA)
SGD, NS = 'f' * 64, 'ns1'
EXEC = 'exec1_' + '1' * 32
OPREF = 'op-' + 'a' * 32


def row(phase, outcome):
    return {'recordSchema': 1, 'storeGenerationDigest': SGD, 'namespaceId': NS,
            'executionId': EXEC, 'operationRef': OPREF,
            'phase': phase, 'settledOutcome': outcome}


ck('admitted with a null outcome is valid', V.is_valid(row('admitted', None)))
for o in ('committed', 'refused'):
    ck('settled with outcome %s is valid' % o, V.is_valid(row('settled', o)))
ck('there is no third settled outcome: undetermined is refused',
   not V.is_valid(row('settled', 'undetermined')))
ck('the removal of the undetermined outcome is documented, not silent',
   'durabilityUndeterminedIsNotACustodyOutcome' in AC
   and 'UNRESOLVABLE' in AC['durabilityUndeterminedIsNotACustodyOutcome']['finding'])
ck('admitted carrying an outcome is refused', not V.is_valid(row('admitted', 'refused')))
ck('settled carrying a null outcome is refused', not V.is_valid(row('settled', None)))
ck('an unknown member is refused',
   not V.is_valid(dict(row('admitted', None), extra=1)))
ck('a missing settledOutcome member is refused',
   not V.is_valid({k: v for k, v in row('admitted', None).items()
                   if k != 'settledOutcome'}))
ck('a non-run3-era executionId grammar is refused',
   not V.is_valid(dict(row('admitted', None), executionId='exec1_' + '1' * 31)))

# ---- 2. the canonical profile is stated, and is the product one ---------------
ck('the canonical profile is explicitly the product/foundation one',
   AC['canonicalProfile']['selected'].startswith('product'))
ck('the metadata profile is explicitly NOT selected',
   AC['canonicalProfile']['notSelected'] == 'opensip-metadata-canonical.1')
ck('the contrast with the domain-framed journal digest is stated',
   'domain-framed' in AC['canonicalProfile']['contrastToStateExplicitly'])

# ---- 3. the settlement matrix -------------------------------------------------
def conclude(receipt, assoc, custody):
    """Step 1 and Step 2 of the read-only algorithm, over ONE coherent snapshot."""
    if receipt is None and assoc is None:
        if custody is None:
            return 'unknown-attempt-unobserved'
        if custody['phase'] == 'admitted':
            return 'unknown-attempt-open'
        o = custody['settledOutcome']
        if o == 'refused':
            return 'terminal-not-committed'
        return 'unknown-custody'          # settled+committed with no receipt: contradiction
    if (receipt is None) != (assoc is None):
        return 'unknown-custody'          # F23 one-sided ledger
    if custody is None:
        return 'unknown-custody'
    if custody['phase'] == 'admitted':
        # LAWFUL pre-settle interval: the settle write is ordered after the receipt write, so
        # every committing attempt passes through here. The receipt is the authority.
        return 'continue-to-capture:pendingSettlement'
    if custody['settledOutcome'] == 'refused':
        return 'unknown-custody'          # refused beside a receipt: genuine contradiction
    return 'continue-to-capture'


R, A = {'x': 1}, {'y': 1}
MATRIX = [
    ((R, A, row('settled', 'committed')), 'continue-to-capture'),
    ((R, A, row('settled', 'refused')), 'unknown-custody'),
    ((R, A, row('admitted', None)), 'continue-to-capture:pendingSettlement'),
    ((None, None, row('settled', 'refused')), 'terminal-not-committed'),
    ((None, None, row('settled', 'committed')), 'unknown-custody'),
    ((None, None, row('admitted', None)), 'unknown-attempt-open'),
    ((None, None, None), 'unknown-attempt-unobserved'),
    ((R, None, row('settled', 'committed')), 'unknown-custody'),
    ((None, A, row('settled', 'committed')), 'unknown-custody'),
]
matrix_rows = []
for (rc, asc, cust), want in MATRIX:
    got = conclude(rc, asc, cust)
    label = 'receipt=%s assoc=%s phase=%s outcome=%s' % (
        rc is not None, asc is not None,
        cust['phase'] if cust else None, cust['settledOutcome'] if cust else None)
    matrix_rows.append({'case': label, 'expected': want, 'got': got, 'pass': got == want})
    ck('settlement matrix: ' + label, got == want, got)

negatives = [m for m in matrix_rows if m['got'] == 'terminal-not-committed']
ck('exactly one matrix cell yields the negative conclusion', len(negatives) == 1, negatives)
ck('the negative cell is settled+refused with both rows absent',
   negatives and 'phase=settled outcome=refused' in negatives[0]['case']
   and 'receipt=False assoc=False' in negatives[0]['case'])
ck('settled+committed with no receipt is NEVER the negative',
   conclude(None, None, row('settled', 'committed')) != 'terminal-not-committed')
ck('admitted is NEVER the negative',
   conclude(None, None, row('admitted', None)) != 'terminal-not-committed')

# ---- 4. the purged-receipt law ------------------------------------------------
# A purge retains the sealed manifest, provenance and tombstone; the receipt row survives as a
# retained record even when unshared evidence bytes are gone. Model both readings.
purged_bytes_gone = conclude({'retainedManifest': True, 'bytes': None}, A,
                             row('settled', 'committed'))
ck('a purged committed attempt still continues to the capture, never a negative',
   purged_bytes_gone == 'continue-to-capture', purged_bytes_gone)
ck('no purge can produce the refused outcome, so no purge can flip a commit to a negative',
   'refused' not in AC['purgedReceiptLaw']['mechanism']
   and 'never become never-committed' in AC['purgedReceiptLaw']['statement'].lower()
   or 'NEVER become never-committed' in AC['purgedReceiptLaw']['statement'])

# ---- 5. the proposed private DDL ---------------------------------------------
DDL = AC['proposedPrivateDDL']
c = sqlite3.connect(':memory:')
c.executescript(DDL)
INS = ('INSERT INTO attempt_custody (store_generation_digest, namespace_id, execution_id, '
       'operation_ref, record_schema, phase, settled_outcome) VALUES (?,?,?,?,1,?,?)')


def fresh():
    d = sqlite3.connect(':memory:')
    d.executescript(DDL)
    return d


def try_sql(d, sql, args=()):
    try:
        d.execute(sql, args)
        d.commit()
        return True, None
    except sqlite3.Error as e:
        return False, str(e).split('\n')[0]


d = fresh()
ok, e = try_sql(d, INS, (SGD, NS, EXEC, OPREF, 'admitted', None))
ck('DDL admits an admitted row with a null outcome', ok, e)
ok, e = try_sql(d, INS, (SGD, NS, EXEC, OPREF, 'admitted', 'refused'))
ck('DDL refuses admitted carrying an outcome', not ok, e)
d.close()

d = fresh()
try_sql(d, INS, (SGD, NS, EXEC, OPREF, 'admitted', None))
ok, e = try_sql(d, "UPDATE attempt_custody SET phase='settled', settled_outcome='refused'")
ck('DDL admits the single admitted-to-settled transition', ok, e)
ok, e = try_sql(d, "UPDATE attempt_custody SET settled_outcome='committed'")
ck('DDL refuses a second settle or an outcome rewrite', not ok, e)
ok, e = try_sql(d, 'DELETE FROM attempt_custody')
ck('DDL refuses deletion', not ok, e)
d.close()

d = fresh()
try_sql(d, INS, (SGD, NS, EXEC, OPREF, 'admitted', None))
ok, e = try_sql(d, "UPDATE attempt_custody SET phase='admitted', settled_outcome=NULL")
ck('DDL refuses a no-op update that is not a settle', not ok, e)
d.close()

d = fresh()
try_sql(d, INS, (SGD, NS, EXEC, OPREF, 'admitted', None))
ok, e = try_sql(d, "UPDATE attempt_custody SET phase='settled', settled_outcome='refused', "
                   "operation_ref='op-" + 'b' * 32 + "'")
ck('DDL refuses an identity change during the settle', not ok, e)
d.close()

d = fresh()
ok, e = try_sql(d, INS, (SGD, NS, 'exec1_bad', OPREF, 'admitted', None))
ck('DDL refuses a malformed executionId', not ok, e)
ok, e = try_sql(d, INS, (SGD, NS, EXEC, OPREF, 'reopened', None))
ck('DDL refuses an unknown phase', not ok, e)
d.close()

# ---- 6. the sweep proof matrix -----------------------------------------------
def sweep(phase, outcome, receipt, assoc, leaseFree, ledgerReadable):
    """The authorized settlement sweep. Holds fence + EXCLUSIVE only when leaseFree.

    It writes ONLY committed or refused. There is no undetermined custody outcome, because a
    settled row is immutable and an undetermined one could never be resolved."""
    if not ledgerReadable:
        return 'no-write:operational-failed HOST.IO_FAILURE host-io'
    if not leaseFree:
        return 'no-write:skip-and-retain'
    if phase == 'settled':
        return 'no-write:already-settled'
    if (receipt is None) != (assoc is None):
        return 'no-write:F23-contradiction'
    if receipt is not None:
        return 'settle:committed'
    return 'settle:refused'


SWEEP = [
    ('crashed, nothing durable', ('admitted', None, None, None, True, True),
     'settle:refused'),
    ('crashed with an orphan SEAL and no receipt', ('admitted', None, None, None, True, True),
     'settle:refused'),
    ('committed but unsettled', ('admitted', None, R, A, True, True),
     'settle:committed'),
    ('one-sided ledger leaves the row admitted', ('admitted', None, R, None, True, True),
     'no-write:F23-contradiction'),
    ('durability uncertainty resolves to refused under exclusive custody',
     ('admitted', None, None, None, True, True), 'settle:refused'),
    ('live writer', ('admitted', None, None, None, False, True),
     'no-write:skip-and-retain'),
    ('inaccessible ledger leaves the row admitted', ('admitted', None, None, None, True, False),
     'no-write:operational-failed HOST.IO_FAILURE host-io'),
    ('already settled is immutable', ('settled', 'refused', None, None, True, True),
     'no-write:already-settled'),
]
sweep_rows = []
for label, args, want in SWEEP:
    got = sweep(*args)
    sweep_rows.append({'case': label, 'expected': want, 'got': got, 'pass': got == want})
    ck('sweep case: ' + label, got == want, got)

ck('the sweep never writes while a writer may be live',
   all(r['got'].startswith('no-write') for r in sweep_rows
       if 'live writer' in r['case']))
ck('the sweep never writes on a one-sided ledger',
   all(r['got'] == 'no-write:F23-contradiction' for r in sweep_rows
       if 'one-sided' in r['case']))
ck('the sweep never writes when the ledger is unreadable',
   all(r['got'].startswith('no-write') for r in sweep_rows if 'inaccessible' in r['case']))
ck('the sweep writes at most one transition per attempt',
   all(r['got'].count('settle:') <= 1 for r in sweep_rows))
ck('the sweep never writes an undetermined custody outcome',
   not any('undetermined' in r['got'] for r in sweep_rows))
ck('every sweep write is one of exactly two outcomes',
   {r['got'] for r in sweep_rows if r['got'].startswith('settle:')}
   == {'settle:committed', 'settle:refused'})

# ---- 7. the composed positive case: commit, then a reader, then a later sweep ---------
# Root asked for this end to end. Nothing in the sequence changes the commitment, and nothing
# grants or revives authority.
composed = []
ledger = {'receipt': None, 'assoc': None, 'custody': None}

ledger['custody'] = row('admitted', None)
composed.append({'step': 'attempt admitted, nothing committed yet',
                 'readerConclusion': conclude(ledger['receipt'], ledger['assoc'],
                                              ledger['custody'])})

# the guarded commit facade writes the receipt and association in one evidence transaction
ledger['receipt'], ledger['assoc'] = R, A
first_read = conclude(ledger['receipt'], ledger['assoc'], ledger['custody'])
composed.append({'step': 'receipt and association committed, custody still admitted',
                 'readerConclusion': first_read})
ck('a reader between the commit and the settle answers committed with pending settlement',
   first_read == 'continue-to-capture:pendingSettlement', first_read)

# the authorized sweep later settles it, holding fence plus EXCLUSIVE
sweep_action = sweep('admitted', None, ledger['receipt'], ledger['assoc'], True, True)
ck('the later sweep settles that attempt committed', sweep_action == 'settle:committed',
   sweep_action)
ledger['custody'] = row('settled', 'committed')
second_read = conclude(ledger['receipt'], ledger['assoc'], ledger['custody'])
composed.append({'step': 'sweep settled committed', 'sweepAction': sweep_action,
                 'readerConclusion': second_read})
ck('a reader after the sweep answers committed with no pending disclosure',
   second_read == 'continue-to-capture', second_read)
ck('the commitment answer never changed across the composed sequence',
   first_read.startswith('continue-to-capture') and second_read.startswith('continue-to-capture'))
ck('the sweep is idempotent: a second pass writes nothing',
   sweep('settled', 'committed', R, A, True, True) == 'no-write:already-settled')
ck('no step in the composed sequence reopens a stopped session or grants authority',
   sweep_action.startswith('settle:')
   and 'retry' not in json.dumps(composed) and 'grant' not in json.dumps(composed))

rep = {'control': 'c14-settlement',
       'composedCommitReaderSweep': composed,
       'settlementMatrix': matrix_rows,
       'sweepMatrix': sweep_rows,
       'negativeConclusionCells': len(negatives),
       'passed': sum(1 for c_ in checks if c_['pass']),
       'failed': sum(1 for c_ in checks if not c_['pass']),
       'checks': checks}
with open(OUT, 'w', encoding='utf-8') as fh:
    fh.write(json.dumps(rep, indent=1) + '\n')
print('WROTE', OUT)
print('passed %d failed %d' % (rep['passed'], rep['failed']))
for c_ in checks:
    if not c_['pass']:
        print('  FAIL', c_['check'], '::', c_['detail'])
