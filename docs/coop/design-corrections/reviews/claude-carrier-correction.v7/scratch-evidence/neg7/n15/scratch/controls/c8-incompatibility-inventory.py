# Control C8 - exact inventory of which CURRENT schema-3 operational rows the frozen
# carrierFormat 2 carrier can and cannot physically admit.
#
# This exists to replace an overclaim. It is NOT true that no current operational record is
# physically writable; the incompatible cases are specific and this control enumerates them.
#
# usage: python c8-incompatibility-inventory.py <source25Root> <reportPath>
import json
import os
import re
import sqlite3
import sys

SRC, OUT = sys.argv[1], sys.argv[2]
DDL2 = open(os.path.join(SRC, 'docs/coop/completion/security-schemas.v2/grant-journal.sql'),
            encoding='utf-8').read()
SL = json.load(open(os.path.join(
    SRC, 'docs/coop/design-corrections/security/security-lifecycle.schemas.v1.json'),
    encoding='utf-8'))
SEC = open(os.path.join(SRC, 'docs/v2/contracts/product-v1/security-and-lifecycle.md'),
           encoding='utf-8').read()

SCHEMA3_TYPES = SL['$defs']['JournalRecord']['properties']['recordType']['enum']
TBL = re.findall(r'^\| `([a-z0-9x_-]+)` \| ([a-z0-9x_-]+) \| ', SEC, re.M)
MACHINE_IDS = [x[0] for x in TBL]
ALIASES = [x[1] for x in TBL]
ALIAS_ONLY = sorted(set(ALIASES) - set(MACHINE_IDS))

COLS = ('grantGeneration', 'seq', 'record_type', 'operation_ref', 'request_ref', 'token',
        'install_generation_id', 'manifest_digest', 'platform', 'body', 'body_sha256',
        'prev_sha256')
Q = ('INSERT INTO grant_journal (' + ','.join(COLS) + ') VALUES ('
     + ','.join(['?'] * len(COLS)) + ')')
OP = 'op-' + 'a' * 32
H = 'b' * 64


def attempt(rt, platform=None, token=None, ig=None, md=None):
    c = sqlite3.connect(':memory:')
    c.executescript(DDL2)
    row = (1, 1, rt, OP, None, token, ig, md, platform, '{}', H, H)
    try:
        c.execute(Q, row)
        c.commit()
        return True, None
    except sqlite3.Error as e:
        return False, str(e).split('\n')[0]
    finally:
        c.close()


rep = {'control': 'c8-incompatibility-inventory',
       'frozenCarrier': 'docs/coop/completion/security-schemas.v2/grant-journal.sql',
       'schema3OperationalTypes': SCHEMA3_TYPES,
       'machineIds': MACHINE_IDS, 'displayAliasOnly': ALIAS_ONLY}

# 1. each schema-3 operational record type, with only the members that type requires
by_type = {}
for rt in SCHEMA3_TYPES:
    if rt == 'GRANT':
        ok, err = attempt(rt, platform='macos-arm64', token='PT-FS-READ-PROJECT',
                          ig='ig1', md='c' * 64)
        note = 'GRANT needs its four completeness members; probed with a lawful alias platform'
    else:
        ok, err = attempt(rt)
        note = ''
    by_type[rt] = {'physicallyAdmitted': ok, 'error': err, 'note': note}
rep['schema3TypeAdmission'] = by_type

# 2. GRANT across the whole platform vocabulary
by_platform = {}
for pf in sorted(set(MACHINE_IDS) | set(ALIASES)):
    ok, err = attempt('GRANT', platform=pf, token='PT-FS-READ-PROJECT', ig='ig1', md='c' * 64)
    by_platform[pf] = {'physicallyAdmitted': ok, 'isMachineId': pf in MACHINE_IDS,
                       'isAliasOnly': pf in ALIAS_ONLY, 'error': err}
rep['grantPlatformAdmission'] = by_platform

refused_types = sorted(t for t, v in by_type.items() if not v['physicallyAdmitted'])
admitted_types = sorted(t for t, v in by_type.items() if v['physicallyAdmitted'])
refused_machine = sorted(p for p, v in by_platform.items()
                         if v['isMachineId'] and not v['physicallyAdmitted'])
admitted_machine = sorted(p for p, v in by_platform.items()
                          if v['isMachineId'] and v['physicallyAdmitted'])

rep['exactIncompatibility'] = {
    'refusedSchema3RecordTypes': refused_types,
    'admittedSchema3RecordTypes': admitted_types,
    'refusedMachinePlatformIds': refused_machine,
    'admittedMachinePlatformIds': admitted_machine,
    'statement': (
        'The frozen carrier physically admits %d of the %d current schema-3 operational record '
        'types. The incompatible cases are exactly: the record type %s, and the machine platform '
        'ids %s on a GRANT. It is therefore wrong to say no current operational record is '
        'physically writable.'
        % (len(admitted_types), len(SCHEMA3_TYPES), ', '.join(refused_types) or 'none',
           ', '.join(refused_machine) or 'none')),
}
rep['correctedOverclaim'] = {
    'v3Wording': ('So the current logical journal cannot be written to any inherited physical '
                  'carrier at all'),
    'defect': ('Overbroad. Eight of the nine schema-3 operational record types insert cleanly, '
               'and a GRANT carrying macos-x86_64 inserts cleanly because that value is its own '
               'display alias.'),
    'corrected': rep['exactIncompatibility']['statement'],
}

with open(OUT, 'w', encoding='utf-8') as fh:
    fh.write(json.dumps(rep, indent=1, sort_keys=True) + '\n')
print('WROTE', OUT)
print('schema-3 types refused by the frozen carrier:', refused_types)
print('schema-3 types admitted by the frozen carrier:', admitted_types)
print('machine platform ids refused:', refused_machine)
print('machine platform ids admitted:', admitted_machine)
print()
print(rep['exactIncompatibility']['statement'])
