"""p02: apply the ADV38-02 and ADV38-03 owner corrections to work/edited by exact, counted replacements.

Every anchor must occur exactly once in the edited copy and the edited copy must still equal the frozen source38
bytes for that file before anything is written; otherwise nothing is written and the probe exits 1. The dispatch
JSON is re-parsed after editing. Output: receipts/p02-apply-carrier.json.
"""
import hashlib, json, sys
from pathlib import Path

BASE = Path('/tmp/opensip-design-corrections/claude-source38-advisory-author.v1')
ED = BASE / 'work' / 'edited'
SRC = Path('/tmp/opensip-design-corrections/candidate-subject.v38')
DISP = 'docs/coop/design-corrections/security/carrier-dispatch.v3.json'
CF = 'docs/coop/design-corrections/security/carrier-format.v3.md'
SL = 'docs/v2/contracts/product-v1/security-and-lifecycle.md'
RO = 'docs/v2/architecture/commit-recovery-readonly.v3.md'
CK = 'docs/coop/design-corrections/security/check-carrier-v3.py'

EDITS = [
    # ---------------- carrier-dispatch.v3.json (ADV38-02)
    (DISP, 'Read-only rows: commit-recovery-readonly.v3.md section 1."',
     'Read-only rows: commit-recovery-readonly.v3.md section 1. Source38 advisory ADV38-02 adds the read-only map entries for a '
     'carrier observed unmigrated (carrierFormat1, carrierFormat2) and the read-only precedence phase law."'),
    (DISP, '      "No route confirms, negates or settles an attempt, merges split-brain rows, rewrites the immutable format row or grants any authority."\n    ],',
     '      "No route confirms, negates or settles an attempt, merges split-brain rows, rewrites the immutable format row or grants any authority.",\n'
     '      "Read-only precedence (source38 ADV38-02), inside one journal snapshot and before the SEAL join: an association naming another '
     'binding is binding-unusable before any carrier read. With any carrierFormat 3 object present, the footprint, project binding, F51 and '
     'row-boundary conditions (the quarantine-condition row with the Step 4 stable observations, otherwise unavailable-busy) and an '
     'unpublished lawful prefix (unavailable-busy) are decided before an association generation below first_generation '
     '(unknown-carrier-incompatible). With no carrierFormat 3 object and an inherited grant_journal, the carrier is observed unmigrated and '
     'the result is unknown-carrier-incompatible whatever generation the association or a surviving witness names; it is decided from the '
     'object names alone, needs no witness comparison, and the witness and anchor rows of commit-recovery-readonly.v3.md Step 3 are not '
     'reported for that request. It is not a quarantine or corruption report, so Step 4 does not gate it, and the reader migrates, publishes '
     'and writes nothing."\n    ],'),
    (DISP, '          "the association grantGeneration is below the first_generation read in the same journal snapshot (F46)"\n        ]',
     '          "the association grantGeneration is below the first_generation read in the same journal snapshot (F46)",\n'
     '          "with the association naming the admitted carrier, the carrier read in the same journal snapshot is observed unmigrated: none of '
     'the seven carrierFormat 3 objects and an inherited grant_journal (open dispatch result carrierFormat1 or carrierFormat2; F46)"\n        ]'),
    (DISP, '      "incomplete-footprint": "unavailable-busy"\n    }',
     '      "incomplete-footprint": "unavailable-busy",\n      "carrierFormat1": "unknown-carrier-incompatible",\n'
     '      "carrierFormat2": "unknown-carrier-incompatible"\n    }'),
    (DISP, '      "A recovery request whose association names a carrierFormat 1 or 2 generation returns unknown-carrier-incompatible, never '
           'not-committed; its route is publicProjectionByPhase.readOnlyRecovery.",',
     '      "A recovery request whose association names a carrierFormat 1 or 2 generation returns unknown-carrier-incompatible, never '
     'not-committed. That includes an association naming the admitted carrier when the carrier read in the same journal snapshot is observed '
     'unmigrated: none of the seven carrierFormat 3 objects and an inherited grant_journal (open dispatch result carrierFormat1 or '
     'carrierFormat2). Its route is publicProjectionByPhase.readOnlyRecovery through readOnlyStandingOfDispatchResult; carrierFormat3 '
     'continues to the SEAL join. The reader migrates, publishes and writes nothing.",'),
    # ---------------- carrier-format.v3.md (ADV38-02)
    (CF, '| read-only recovery | F46: association names a generation below the `first_generation` read in the same journal snapshot | '
         '`unknown-carrier-incompatible` |',
     '| read-only recovery | F46: association names a generation below the `first_generation` read in the same journal snapshot, or the '
     'carrier read in that snapshot is observed unmigrated (no carrierFormat 3 object and an inherited `grant_journal`; dispatch '
     '`carrierFormat1` or `carrierFormat2`) | `unknown-carrier-incompatible` |'),
    (CF, 'stably observed quarantine (`LEDGER.CORRUPT`) and not contention. It never becomes not-committed or a\nconfirmation.\n',
     'stably observed quarantine (`LEDGER.CORRUPT`) and not contention. It never becomes not-committed or a\nconfirmation.\n\n'
     '**An association naming a carrier observed unmigrated (source38 advisory ADV38-02).** When the carrier read in\n'
     'the recovery snapshot has none of the seven carrierFormat 3 objects and has the inherited `grant_journal`, every\n'
     'generation it holds is a carrierFormat 1 or 2 generation, so no schema-3 `SEAL` can exist for the association.\n'
     'The association points to a lost migration, a rollback or a swapped carrier, and the result is F46\n'
     '`unknown-carrier-incompatible` whatever generation it names. Read-only precedence, in one journal snapshot and\n'
     'before the SEAL join: `binding-unusable` first; then, only when a carrierFormat 3 object exists, the footprint,\n'
     'project binding, F51 and row-boundary rows and then the below-`first_generation` row; with no carrierFormat 3\n'
     'object, this row. It is decided from the object names alone and needs no witness comparison, so the witness and\n'
     'anchor rows of `commit-recovery-readonly.v3.md` Step 3, including a surviving witness naming another project, are\n'
     'not reported for that request. It is not a quarantine or corruption report, so Step 4 does not gate it, and the\n'
     'reader migrates, publishes and writes nothing. Machine-readable: `readOnlyStandingOfDispatchResult` maps\n'
     '`carrierFormat1` and `carrierFormat2`; exact precedence: `commit-recovery-readonly.v3.md` §1.\n'),
    (CF, '  exist there. A recovery request whose association names such a generation returns\n'
         '  `unknown-carrier-incompatible` (F31/F46), never `not-committed`; its public route is §8.1.',
     '  exist there. A recovery request whose association names such a generation, including any generation of a\n'
     '  carrier observed unmigrated, returns `unknown-carrier-incompatible` (F31/F46), never `not-committed`; its\n'
     '  public route is §8.1.'),
    # ---------------- security-and-lifecycle.md S12 (ADV38-02)
    (SL, '| read-only recovery: the association names a carrierFormat 1 or 2 generation (below the published `first_generation`), where no '
         'schema-3 `SEAL` can exist (`unknown-carrier-incompatible`, F46) |',
     '| read-only recovery: the association names a carrierFormat 1 or 2 generation (below the published `first_generation`, or of a '
     'carrier observed unmigrated, with no carrierFormat 3 object, in the same journal snapshot), where no schema-3 `SEAL` can exist '
     '(`unknown-carrier-incompatible`, F46; decided before the SEAL join, after the binding row and any carrierFormat 3 footprint row) |'),
    # ---------------- commit-recovery-readonly.v3.md (ADV38-02, ADV38-03)
    (RO, 'The current bytes carry the source37 owner correction of review advisories A37-01 to A37-04 '
         '(`design-corrections/security/carrier-format.v3.md` §8.1).',
     'The current bytes carry the source37 owner correction of review advisories A37-01 to A37-04 '
     '(`design-corrections/security/carrier-format.v3.md` §8.1) and the source38 advisory corrections ADV38-02 (a carrier observed '
     'unmigrated) and ADV38-03 (current scope wording).'),
    (RO, 'onto an existing class, `errorCode` and `faultCause`. Root owns the final generator and the\n'
         'clarification of the older internal `indeterminate` spelling in F00–F37; that is not treated as a\nblocker here.',
     'onto an existing class, `errorCode` and `faultCause`. Root owns the final generator and the\n'
     'clarification of the older internal `indeterminate` spelling in the failure-case plan. That plan was\n'
     'F00–F37 when this document was authored; the current `commit-recovery-plan.v1.json` holds F00–F53, and\n'
     'all 54 cases remain not executed. The clarification is not treated as a blocker here.'),
    (RO, '`DomainDetailCode` is minted for aesthetics. `MIGRATION.CORRUPT` is **not** reused: it is the store\n'
         'transition\'s detail, and borrowing it for ordinary journal corruption would put two remedies behind\n'
         'one code, which the D9 contract names a defect.',
     '`DomainDetailCode` is minted for aesthetics. `MIGRATION.CORRUPT` is **not** reused on any read-only path.\n'
     'Security S12 scopes it to a store transition footprint and, at a writer or maintenance carrier open only,\n'
     'to a carrierFormat 3 migration footprint that is not a lawful durable prefix or violates the published\n'
     'generation boundary (including F51). Borrowing it for ordinary journal corruption, a carrier project\n'
     'binding mismatch or any read-only carrier observation would put two remedies behind one code, which the\n'
     'D9 contract names a defect.'),
    (RO, 'family. A lawful `{A}` or `{A, B}` prefix is `unavailable-busy`. `MIGRATION.CORRUPT` is used on none of\n'
         'these read-only paths, and none confirms, negates or settles an attempt. Exact phase table:\n'
         '`design-corrections/security/carrier-format.v3.md` §8.1.',
     'family. So is an association naming the admitted carrier when the carrier read in that journal snapshot is\n'
     '**observed unmigrated**: none of the seven carrierFormat 3 objects exists and the inherited `grant_journal`\n'
     'does (open dispatch results `carrierFormat1` and `carrierFormat2`). Every generation of such a carrier is a\n'
     'carrierFormat 1 or 2 generation, so no schema-3 `SEAL` can exist; the association points to a lost\n'
     'migration, a rollback or a swapped carrier. A lawful `{A}` or `{A, B}` prefix is `unavailable-busy`.\n\n'
     '**Precedence of the read-only carrier observations** (source38 advisory ADV38-02), all inside one journal\n'
     'snapshot and before the SEAL join:\n\n'
     '1. an association naming another binding → `binding-unusable`, before any carrier read;\n'
     '2. with any carrierFormat 3 object present: a partial set, an invalid definition, a `grant_journal_v3` row\n'
     '   before publication, a published row or surviving witness naming another project, F51, or a\n'
     '   `grant_journal_v3` row below `first_generation` → `unknown-quarantine-condition` with the Step 4 stable\n'
     '   observations, otherwise `unavailable-busy`; an unpublished lawful prefix → `unavailable-busy`; then an\n'
     '   association generation below `first_generation` → `unknown-carrier-incompatible`;\n'
     '3. with no carrierFormat 3 object and an inherited `grant_journal` → `unknown-carrier-incompatible`,\n'
     '   whatever generation the association or a surviving witness names.\n\n'
     'Row 3 is decided from the object names alone and needs no witness comparison, so the witness and anchor rows\n'
     'of Step 3 (`uncertainTailLoss`, `witnesslessRestore`, `witnessMalformed`, a witness naming another carrier and\n'
     'the anchor table) are not reported for that request. `unknown-carrier-incompatible` is not a quarantine or\n'
     'corruption report, so Step 4 does not gate it. The reader performs no migration, publishes no format row and\n'
     'writes nothing on any of these paths. `MIGRATION.CORRUPT` is used on none of these read-only paths, and none\n'
     'confirms, negates or settles an attempt. Exact phase table:\n'
     '`design-corrections/security/carrier-format.v3.md` §8.1.'),
    (RO, '`first_generation`. Their conclusions are the carrier rows of §1; a quarantine-class conclusion also\nrequires Step 4.',
     '`first_generation`. Their conclusions, including a carrier observed unmigrated, are the carrier rows and\n'
     'precedence of §1; a quarantine-class conclusion also requires Step 4.'),
    # ---------------- check-carrier-v3.py (ADV38-02 and ADV38-03 controls)
    (CK, "    ('readOnlyRecovery', 'unknown-carrier-incompatible'): ('operational-failed', 4, 'HOST.IO_FAILURE', 'host-io', None),\n",
     "    ('readOnlyRecovery', 'unknown-carrier-incompatible'): ('operational-failed', 4, 'HOST.IO_FAILURE', 'host-io', None),\n"
     "    ('readOnlyRecovery', 'carrierFormat1'): ('operational-failed', 4, 'HOST.IO_FAILURE', 'host-io', None),\n"
     "    ('readOnlyRecovery', 'carrierFormat2'): ('operational-failed', 4, 'HOST.IO_FAILURE', 'host-io', None),\n"),
    (CK, "_s37_expect('no journal table at all is the fresh-install path', 'writerOrMaintenanceOpen',\n"
         "            _s37_open(sqlite3.connect(':memory:'), 'writerOrMaintenanceOpen'), 'fresh-install')\n",
     "_s37_expect('no journal table at all is the fresh-install path', 'writerOrMaintenanceOpen',\n"
     "            _s37_open(sqlite3.connect(':memory:'), 'writerOrMaintenanceOpen'), 'fresh-install')\n"
     "\n"
     "# ---- source38 advisory ADV38-02: read-only recovery of an association naming a carrier observed unmigrated. The open\n"
     "# dispatch stays a pure function of the carrier bytes; read-only maps carrierFormat1/carrierFormat2 to the F46 route.\n"
     "for _fmt, _ddl in (('carrierFormat1', ddl1), ('carrierFormat2', ddl2)):\n"
     "    c = sqlite3.connect(':memory:', isolation_level=None)\n"
     "    c.executescript(_ddl)\n"
     "    c.execute(_S37_GJ2, (1, 1, 'REV', _OP, _H, _H))\n"
     "    _before = _s37_state(c)\n"
     "    ck('source38 ADV38-02 scenario: the inherited %s DDL opens as %s at a writer open' % (_fmt, _fmt),\n"
     "       _s37_open(c, 'writerOrMaintenanceOpen') == _fmt, _s37_open(c, 'writerOrMaintenanceOpen'))\n"
     "    for _gen in (1, 2, 7):\n"
     "        _s37_expect('ADV38-02: an association (grantGeneration %d) naming the admitted carrier over an unmigrated %s is '\n"
     "                    'unknown-carrier-incompatible' % (_gen, _fmt), 'readOnlyRecovery',\n"
     "                    _s37_open(c, 'readOnlyRecovery', assoc={'journalCarrierDigest': _S37_ADMITTED, 'grantGeneration': _gen}), _fmt)\n"
     "    _s37_expect('ADV38-02: over an unmigrated %s an association naming another carrier is binding-unusable first' % _fmt,\n"
     "                'readOnlyRecovery', _s37_open(c, 'readOnlyRecovery', assoc={'journalCarrierDigest': _S37_OTHER, 'grantGeneration': 2}),\n"
     "                'binding-unusable')\n"
     "    _s37_expect('ADV38-02: over an unmigrated %s a surviving witness naming another project does not displace F46' % _fmt,\n"
     "                'readOnlyRecovery', _s37_open(c, 'readOnlyRecovery', assoc=_RO_OK, witness=_S37_OTHER), _fmt)\n"
     "    ck('source38 ADV38-02 scenario: read-only dispatch over an unmigrated %s migrates, publishes and writes nothing' % _fmt,\n"
     "       _s37_state(c) == _before\n"
     "       and not ({'carrier_format', 'grant_journal_v3'} & {r[0] for r in c.execute('SELECT name FROM sqlite_master')}))\n"
     "    c.execute('CREATE TABLE carrier_format (singleton INTEGER)')\n"
     "    _s37_expect('ADV38-02: one carrierFormat 3 object over an unmigrated %s is footprint corruption (quarantine row), not F46' % _fmt,\n"
     "                'readOnlyRecovery', _s37_open(c, 'readOnlyRecovery', assoc=_RO_OK), 'migration-footprint-corrupt')\n"
     "c = _s37_carrier('migrated')\n"
     "_s37_publish(c)\n"
     "_s37_expect('ADV38-02: the migrated below-first_generation association is still F46 through the carrierFormat 3 branch',\n"
     "            'readOnlyRecovery', _s37_open(c, 'readOnlyRecovery', assoc={'journalCarrierDigest': _S37_ADMITTED, 'grantGeneration': 1}),\n"
     "            'unknown-carrier-incompatible')\n"
     "_s37_inject(c, 1)\n"
     "_s37_expect('ADV38-02: a grant_journal_v3 row below first_generation is decided before the below-first_generation association',\n"
     "            'readOnlyRecovery', _s37_open(c, 'readOnlyRecovery', assoc={'journalCarrierDigest': _S37_ADMITTED, 'grantGeneration': 1}),\n"
     "            'migration-footprint-corrupt')\n"
     "ck('source38 ADV38-02 map: carrierFormat1 and carrierFormat2 map to F46; carrierFormat3 and fresh-install have no read-only standing',\n"
     "   _S37_RO_MAP.get('carrierFormat1') == 'unknown-carrier-incompatible' and _S37_RO_MAP.get('carrierFormat2') == 'unknown-carrier-incompatible'\n"
     "   and 'carrierFormat3' not in _S37_RO_MAP and 'fresh-install' not in _S37_RO_MAP, _S37_RO_MAP)\n"
     "ck('source38 ADV38-02 law: the F46 observations, reader law and read-only precedence phase law name a carrier observed unmigrated',\n"
     "   any('observed unmigrated' in o for o in _S37_PROJ['readOnlyRecovery']['unknown-carrier-incompatible']['observations'])\n"
     "   and any('observed unmigrated' in l for l in disp['readDispatch']['readerLaws'])\n"
     "   and any(l.startswith('Read-only precedence') and 'observed unmigrated' in l for l in _S37_PROJ['phaseLaws']))\n"),
    (CK, "    ck('source37 route: readOnlyRecovery/%s matches the commit-recovery-readonly.v3 section 1 row' % _standing, _ok, _cells)\n",
     "    ck('source37 route: readOnlyRecovery/%s matches the commit-recovery-readonly.v3 section 1 row' % _standing, _ok, _cells)\n"
     "_S37_CF = open(os.path.join(SEC, 'carrier-format.v3.md'), encoding='utf-8').read()\n"
     "_S37_F46_S12 = [l for l in _S37_S12 if 'unknown-carrier-incompatible' in l]\n"
     "ck('source38 ADV38-02 prose: the S12 F46 row, carrier-format section 8.1 and read-only section 1 name a carrier observed unmigrated',\n"
     "   len(_S37_F46_S12) == 1 and 'observed unmigrated' in _S37_F46_S12[0] and 'observed unmigrated' in _S37_CF\n"
     "   and 'observed unmigrated' in _S37_READONLY and 'Precedence of the read-only carrier observations' in _S37_READONLY)\n"
     "ck('source38 ADV38-03 prose: read-only section 1 states the current F00-F53 plan and the writer/maintenance MIGRATION.CORRUPT scope',\n"
     "   'F00–F53' in _S37_READONLY and 'all 54 cases remain not executed' in _S37_READONLY\n"
     "   and re.search(r'writer or maintenance carrier open only,\\s+to a carrierFormat 3 migration footprint', _S37_READONLY) is not None\n"
     "   and re.search(r\"it is the store\\s+transition's detail\", _S37_READONLY) is None)\n"),
]


def sha(b):
    return hashlib.sha256(b).hexdigest()


texts, problems = {}, []
for rel in sorted({e[0] for e in EDITS}):
    raw = (ED / rel).read_bytes()
    if raw != (SRC / rel).read_bytes():
        problems.append('edited copy differs from source38 before applying: ' + rel)
    texts[rel] = raw.decode('utf-8')
for rel, old, new in EDITS:
    n = texts[rel].count(old)
    if n != 1:
        problems.append('%s anchor count %d: %r' % (rel, n, old[:90]))
        continue
    texts[rel] = texts[rel].replace(old, new)
out = {'standing': 'ADV38-02/03 exact replacements in work/edited', 'edits': len(EDITS)}
if problems:
    out['problems'] = problems
    out['written'] = False
else:
    json.loads(texts[DISP])
    rows = []
    for rel, text in texts.items():
        before = sha((ED / rel).read_bytes())
        (ED / rel).write_text(text, encoding='utf-8')
        rows.append({'path': rel, 'before': before, 'after': sha((ED / rel).read_bytes())})
    out['written'] = True
    out['files'] = rows
(BASE / 'receipts').mkdir(exist_ok=True)
(BASE / 'receipts' / 'p02-apply-carrier.json').write_text(json.dumps(out, indent=1) + '\n')
print(json.dumps(out, indent=1))
sys.exit(0 if not problems else 1)
