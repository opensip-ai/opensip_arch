"""p02: item 3 (read-only association naming a bound carrier observed absent) by exact counted replacements in
work/edited. Every anchor must occur exactly once and each file must still equal its v1 edited bytes before anything
is written; otherwise nothing is written (exit 1). The dispatch JSON is re-parsed. Output: receipts/p02-apply-absent-carrier.json.
"""
import hashlib, json, sys
from pathlib import Path

BASE = Path('/tmp/opensip-design-corrections/claude-source38-advisory-author.v2')
ED = BASE / 'work' / 'edited'
V1 = Path('/tmp/opensip-design-corrections/claude-source38-advisory-author.v1/work/edited')
DISP = 'docs/coop/design-corrections/security/carrier-dispatch.v3.json'
CF = 'docs/coop/design-corrections/security/carrier-format.v3.md'
SL = 'docs/v2/contracts/product-v1/security-and-lifecycle.md'
RO = 'docs/v2/architecture/commit-recovery-readonly.v3.md'
CK = 'docs/coop/design-corrections/security/check-carrier-v3.py'

UNKNOWN_CUSTODY_ROUTE = '''      "unknown-custody": {
        "class": "operational-failed",
        "exit": 4,
        "errorCode": "HOST.IO_FAILURE",
        "faultCause": "host-io",
        "domainDetail": null,
        "securityRefusal": null,
        "s12Row": "read-only recovery: unreadable ledger or carrier",
        "observations": [
          "with the association naming the admitted carrier, the journal snapshot holds neither an inherited grant_journal nor any carrierFormat 3 object (open dispatch result fresh-install): the bound carrier is lost, emptied or a fallback, which is never absence of the attempt, never not-committed and never success",
          "a read-only open of the bound carrier location that refuses because no database exists there; the reader never creates, initializes or migrates a carrier"
        ]
      },
      "unavailable-busy": {'''

EDITS = [
    # ---------------- carrier-dispatch.v3.json
    (DISP, ' and the read-only precedence phase law."',
     ' and the read-only precedence phase law. A source38 follow-up adds the unknown-custody read-only route for a bound carrier '
     'observed absent (dispatch fresh-install) and the carrier-stage totality phase law."'),
    (DISP, ' It is not a quarantine or corruption report, so Step 4 does not gate it, and the reader migrates, publishes and writes nothing."\n    ],',
     ' It is not a quarantine or corruption report, so Step 4 does not gate it, and the reader migrates, publishes and writes nothing.",\n'
     '      "The read-only carrier stage is total (source38 follow-up): every open dispatch result except carrierFormat3 has exactly one '
     'standing in readOnlyStandingOfDispatchResult, and carrierFormat3 alone continues to the SEAL join. With no carrierFormat 3 object and '
     'no inherited grant_journal (dispatch fresh-install), an association naming the admitted carrier is unknown-custody, after '
     'binding-unusable and whatever generation the association or a surviving witness names; it is decided from the object names alone. '
     'A missing, empty or fallback carrier is never absence, never not-committed and never success, and the reader never creates, '
     'initializes or migrates it. The fresh-install path of a writer or maintenance open (openDispatch.freshInstallPath) remains a '
     'separate owner that read-only recovery never takes."\n    ],'),
    (DISP, '          "with the association naming the admitted carrier, the carrier read in the same journal snapshot is observed unmigrated: none of '
           'the seven carrierFormat 3 objects and an inherited grant_journal (open dispatch result carrierFormat1 or carrierFormat2; F46)"\n'
           '        ]\n      },\n      "unavailable-busy": {',
     '          "with the association naming the admitted carrier, the carrier read in the same journal snapshot is observed unmigrated: none of '
     'the seven carrierFormat 3 objects and an inherited grant_journal (open dispatch result carrierFormat1 or carrierFormat2; F46)"\n'
     '        ]\n      },\n' + UNKNOWN_CUSTODY_ROUTE),
    (DISP, '      "carrierFormat2": "unknown-carrier-incompatible"\n    }',
     '      "carrierFormat2": "unknown-carrier-incompatible",\n      "fresh-install": "unknown-custody"\n    }'),
    (DISP, 'carrierFormat3 continues to the SEAL join. The reader migrates, publishes and writes nothing.",',
     'carrierFormat3 continues to the SEAL join. The reader migrates, publishes and writes nothing.",\n'
     '      "A recovery request whose association names the admitted carrier where the journal snapshot holds no grant_journal and no '
     'carrierFormat 3 object (open dispatch result fresh-install) returns unknown-custody (HOST.IO_FAILURE, host-io), never absence, '
     'not-committed or success; the reader never creates, initializes or migrates a carrier.",'),
    # ---------------- carrier-format.v3.md
    (CF, '`carrierFormat1` or `carrierFormat2`) | `unknown-carrier-incompatible` | operational-failed / 4 / `HOST.IO_FAILURE` / `host-io` | omitted |\n',
     '`carrierFormat1` or `carrierFormat2`) | `unknown-carrier-incompatible` | operational-failed / 4 / `HOST.IO_FAILURE` / `host-io` | omitted |\n'
     '| read-only recovery | association names the admitted carrier, but the journal snapshot holds no `grant_journal` and no carrierFormat 3 '
     'object (dispatch `fresh-install`: the bound carrier is observed absent) | `unknown-custody` | operational-failed / 4 / `HOST.IO_FAILURE` / '
     '`host-io` | omitted |\n'),
    (CF, '`carrierFormat1` and `carrierFormat2`; exact precedence: `commit-recovery-readonly.v3.md` §1.\n',
     '`carrierFormat1` and `carrierFormat2`; exact precedence: `commit-recovery-readonly.v3.md` §1.\n\n'
     '**An association naming a carrier observed absent (source38 follow-up).** When the recovery snapshot holds neither\n'
     'the inherited `grant_journal` nor any carrierFormat 3 object, the open dispatch result is `fresh-install`. At a\n'
     'writer or maintenance open that is the fresh-install path. On read-only recovery an association already names this\n'
     'carrier, so it is lost, emptied or replaced by a fallback: the result is `unknown-custody` (`HOST.IO_FAILURE`,\n'
     '`host-io`), after `binding-unusable` and whatever generation the association or a surviving witness names. It is\n'
     'never absence, never not-committed and never success, and the reader never creates, initializes or migrates a\n'
     'carrier. This makes the read-only carrier stage total: every dispatch result except `carrierFormat3`, which\n'
     'continues to the SEAL join, has one standing in `readOnlyStandingOfDispatchResult`.\n'),
    # ---------------- security-and-lifecycle.md S12
    (SL, '| read-only recovery: unreadable ledger or carrier, unobserved attempt, or an anchor that does not reach the requested sequence | '
         'operational-failed / 4 / `HOST.IO_FAILURE`, `faultCause` `host-io` |',
     '| read-only recovery: unreadable ledger or carrier, a bound carrier observed absent (an association names it, but the journal '
     'snapshot holds no `grant_journal` and no carrierFormat 3 object; never absence, not-committed or success, and never initialized), '
     'unobserved attempt, or an anchor that does not reach the requested sequence | operational-failed / 4 / `HOST.IO_FAILURE`, '
     '`faultCause` `host-io`, `domainDetail` omitted |'),
    # ---------------- commit-recovery-readonly.v3.md
    (RO, '3. with no carrierFormat 3 object and an inherited `grant_journal` → `unknown-carrier-incompatible`,\n'
         '   whatever generation the association or a surviving witness names.\n',
     '3. with no carrierFormat 3 object and an inherited `grant_journal` → `unknown-carrier-incompatible`,\n'
     '   whatever generation the association or a surviving witness names;\n'
     '4. with no carrierFormat 3 object and no inherited `grant_journal` (open dispatch result `fresh-install`) →\n'
     '   `unknown-custody`, whatever generation the association or a surviving witness names.\n'),
    (RO, 'Row 3 is decided from the object names alone and needs no witness comparison, so the witness and anchor rows\n'
         'of Step 3 (`uncertainTailLoss`, `witnesslessRestore`, `witnessMalformed`, a witness naming another carrier and\n'
         'the anchor table) are not reported for that request. `unknown-carrier-incompatible` is not a quarantine or\n'
         'corruption report, so Step 4 does not gate it. The reader performs no migration, publishes no format row and\n'
         'writes nothing on any of these paths.',
     'Rows 3 and 4 are decided from the object names alone and need no witness comparison, so the witness and anchor\n'
     'rows of Step 3 (`uncertainTailLoss`, `witnesslessRestore`, `witnessMalformed`, a witness naming another carrier and\n'
     'the anchor table) are not reported for that request. Row 4 is a lost, emptied or fallback carrier: an association\n'
     'already names it, so the absent carrier is custody the reader cannot observe, exactly as Step 1 treats an empty\n'
     'fallback ledger. It is never absence, never `terminal-not-committed` and never success, and the fresh-install path\n'
     'of a writer or maintenance open is a separate owner that read-only recovery never takes. Neither\n'
     '`unknown-carrier-incompatible` nor `unknown-custody` is a quarantine or corruption report, so Step 4 does not gate\n'
     'them. **The carrier stage is total:** every open dispatch result except `carrierFormat3`, which continues to the\n'
     'SEAL join, has exactly one §1 standing. The reader performs no migration, publishes no format row, creates or\n'
     'initializes no carrier and writes nothing on any of these paths.'),
    (RO, '`first_generation`. Their conclusions, including a carrier observed unmigrated, are the carrier rows and\n'
         'precedence of §1; a quarantine-class conclusion also requires Step 4.',
     '`first_generation`. Their conclusions, including a carrier observed unmigrated or absent, are the carrier rows\n'
     'and precedence of §1; a quarantine-class conclusion also requires Step 4. As in Step 1, a missing, empty or\n'
     'fallback carrier is never absence: it is `unknown-custody`.'),
    # ---------------- check-carrier-v3.py
    (CK, "    ('readOnlyRecovery', 'carrierFormat2'): ('operational-failed', 4, 'HOST.IO_FAILURE', 'host-io', None),\n",
     "    ('readOnlyRecovery', 'carrierFormat2'): ('operational-failed', 4, 'HOST.IO_FAILURE', 'host-io', None),\n"
     "    ('readOnlyRecovery', 'fresh-install'): ('operational-failed', 4, 'HOST.IO_FAILURE', 'host-io', None),\n"),
    (CK, "ck('source38 ADV38-02 map: carrierFormat1 and carrierFormat2 map to F46; carrierFormat3 and fresh-install have no read-only standing',\n"
         "   _S37_RO_MAP.get('carrierFormat1') == 'unknown-carrier-incompatible' and _S37_RO_MAP.get('carrierFormat2') == 'unknown-carrier-incompatible'\n"
         "   and 'carrierFormat3' not in _S37_RO_MAP and 'fresh-install' not in _S37_RO_MAP, _S37_RO_MAP)\n",
     "ck('source38 ADV38-02 map: carrierFormat1 and carrierFormat2 map to F46; carrierFormat3 has no read-only standing',\n"
     "   _S37_RO_MAP.get('carrierFormat1') == 'unknown-carrier-incompatible' and _S37_RO_MAP.get('carrierFormat2') == 'unknown-carrier-incompatible'\n"
     "   and 'carrierFormat3' not in _S37_RO_MAP, _S37_RO_MAP)\n"),
    (CK, "   and any(l.startswith('Read-only precedence') and 'observed unmigrated' in l for l in _S37_PROJ['phaseLaws']))\n\n_s37_need = (",
     "   and any(l.startswith('Read-only precedence') and 'observed unmigrated' in l for l in _S37_PROJ['phaseLaws']))\n"
     "\n"
     "# ---- source38 follow-up: an association naming a bound carrier observed absent (no grant_journal, no carrierFormat 3\n"
     "# object). Real SQLite databases; the dispatch function above is unchanged; read-only maps fresh-install to unknown-custody.\n"
     "import ast as _s37_ast\n"
     "import tempfile as _s37_tempfile\n"
     "c = sqlite3.connect(':memory:', isolation_level=None)\n"
     "_before = _s37_state(c)\n"
     "_s37_expect('absent carrier: an empty SQLite carrier is still the fresh-install path at a writer open (separate owner)',\n"
     "            'writerOrMaintenanceOpen', _s37_open(c, 'writerOrMaintenanceOpen'), 'fresh-install')\n"
     "for _gen in (1, 2, 7):\n"
     "    _s37_expect('absent carrier: an association (grantGeneration %d) naming the admitted carrier over an empty SQLite carrier '\n"
     "                'is unknown-custody' % _gen, 'readOnlyRecovery',\n"
     "                _s37_open(c, 'readOnlyRecovery', assoc={'journalCarrierDigest': _S37_ADMITTED, 'grantGeneration': _gen}), 'fresh-install')\n"
     "_s37_expect('absent carrier: a surviving witness naming another project does not displace unknown-custody', 'readOnlyRecovery',\n"
     "            _s37_open(c, 'readOnlyRecovery', assoc=_RO_OK, witness=_S37_OTHER), 'fresh-install')\n"
     "_s37_expect('absent carrier: a surviving witness naming the admitted project does not make the absent carrier absence',\n"
     "            'readOnlyRecovery', _s37_open(c, 'readOnlyRecovery', assoc=_RO_OK, witness=_S37_ADMITTED), 'fresh-install')\n"
     "_s37_expect('absent carrier: an association naming another carrier is binding-unusable first', 'readOnlyRecovery',\n"
     "            _s37_open(c, 'readOnlyRecovery', assoc={'journalCarrierDigest': _S37_OTHER, 'grantGeneration': 2}), 'binding-unusable')\n"
     "ck('source38 absent-carrier scenario: read-only dispatch over an empty SQLite carrier creates, initializes and writes nothing',\n"
     "   _s37_state(c) == _before and not c.execute('SELECT name FROM sqlite_master').fetchall())\n"
     "c = sqlite3.connect(':memory:', isolation_level=None)\n"
     "c.execute('CREATE TABLE unrelated_fallback (x INTEGER)')\n"
     "_s37_expect('absent carrier: a fallback database holding only an unrelated table is unknown-custody, never absence',\n"
     "            'readOnlyRecovery', _s37_open(c, 'readOnlyRecovery', assoc=_RO_OK), 'fresh-install')\n"
     "_s37_dir = _s37_tempfile.mkdtemp(prefix='opensip-absent-carrier-')\n"
     "_s37_path = os.path.join(_s37_dir, 'grant-journal.sqlite')\n"
     "try:\n"
     "    sqlite3.connect('file:%s?mode=ro' % _s37_path, uri=True).execute('SELECT name FROM sqlite_master').fetchall()\n"
     "    _s37_ro = 'opened'\n"
     "except sqlite3.Error:\n"
     "    _s37_ro = 'refused'\n"
     "ck('source38 absent-carrier scenario: a read-only open of a missing carrier file refuses and creates no file (S12 unreadable carrier)',\n"
     "   _s37_ro == 'refused' and not os.path.exists(_s37_path), _s37_ro)\n"
     "_s37_path2 = os.path.join(_s37_dir, 'empty-carrier.sqlite')\n"
     "sqlite3.connect(_s37_path2).close()\n"
     "_s37_bytes = open(_s37_path2, 'rb').read()\n"
     "c = sqlite3.connect('file:%s?mode=ro' % _s37_path2, uri=True)\n"
     "_s37_expect('absent carrier: an existing empty carrier file opened read-only is unknown-custody', 'readOnlyRecovery',\n"
     "            _s37_open(c, 'readOnlyRecovery', assoc=_RO_OK), 'fresh-install')\n"
     "c.close()\n"
     "ck('source38 absent-carrier scenario: the empty carrier file bytes are unchanged after the read-only dispatch',\n"
     "   open(_s37_path2, 'rb').read() == _s37_bytes)\n"
     "c = _s37_carrier('fresh')\n"
     "_s37_expect('absent carrier: an interrupted fresh install {B} with an association keeps its carrierFormat 3 precedence (busy prefix)',\n"
     "            'readOnlyRecovery', _s37_open(c, 'readOnlyRecovery', assoc=_RO_OK), 'incomplete-footprint')\n"
     "_s37_fn = next(n for n in _s37_ast.parse(open(os.path.abspath(__file__), encoding='utf-8').read()).body\n"
     "              if isinstance(n, _s37_ast.FunctionDef) and n.name == '_s37_open')\n"
     "_s37_results = {k.value for r in _s37_ast.walk(_s37_fn) if isinstance(r, _s37_ast.Return)\n"
     "                for k in _s37_ast.walk(r.value) if isinstance(k, _s37_ast.Constant) and isinstance(k.value, str)}\n"
     "ck('source38 absent-carrier totality: every _s37_open result except carrierFormat3 has exactly one published read-only standing',\n"
     "   'fresh-install' in _s37_results and set(_S37_RO_MAP) == _s37_results - {'carrierFormat3'}\n"
     "   and all(_S37_RO_MAP[r] in _S37_PROJ['readOnlyRecovery'] for r in _S37_RO_MAP), sorted(_s37_results))\n"
     "ck('source38 absent-carrier law: the unknown-custody route, reader law and totality phase law name the absent carrier',\n"
     "   _S37_RO_MAP.get('fresh-install') == 'unknown-custody'\n"
     "   and any('fresh-install' in o for o in _S37_PROJ['readOnlyRecovery'].get('unknown-custody', {}).get('observations', []))\n"
     "   and any('fresh-install' in l and 'unknown-custody' in l for l in disp['readDispatch']['readerLaws'])\n"
     "   and any(l.startswith('The read-only carrier stage is total') for l in _S37_PROJ['phaseLaws']))\n"
     "\n_s37_need = ("),
    (CK, "   and re.search(r\"it is the store\\s+transition's detail\", _S37_READONLY) is None)\n",
     "   and re.search(r\"it is the store\\s+transition's detail\", _S37_READONLY) is None)\n"
     "ck('source38 absent-carrier prose: the S12 unreadable-carrier row, carrier-format section 8.1 and read-only section 1 name the absent carrier',\n"
     "   len([l for l in _S37_S12 if 'observed absent' in l]) == 1 and 'observed absent' in _S37_CF\n"
     "   and '4. with no carrierFormat 3 object and no inherited `grant_journal`' in _S37_READONLY\n"
     "   and 'The carrier stage is total' in _S37_READONLY)\n"),
]


def sha(b):
    return hashlib.sha256(b).hexdigest()


texts, problems = {}, []
for rel in sorted({e[0] for e in EDITS}):
    raw = (ED / rel).read_bytes()
    if raw != (V1 / rel).read_bytes():
        problems.append('edited copy differs from v1 before applying: ' + rel)
    texts[rel] = raw.decode('utf-8')
for rel, old, new in EDITS:
    n = texts[rel].count(old)
    if n != 1:
        problems.append('%s anchor count %d: %r' % (rel, n, old[:90]))
        continue
    texts[rel] = texts[rel].replace(old, new)
out = {'standing': 'item 3 exact replacements in v2 work/edited', 'edits': len(EDITS)}
if problems:
    out.update(problems=problems, written=False)
else:
    json.loads(texts[DISP])
    rows = []
    for rel, text in texts.items():
        before = sha((ED / rel).read_bytes())
        (ED / rel).write_text(text, encoding='utf-8')
        rows.append({'path': rel, 'before': before, 'after': sha((ED / rel).read_bytes())})
    out.update(written=True, files=rows)
(BASE / 'receipts' / 'p02-apply-absent-carrier.json').write_text(json.dumps(out, indent=1) + '\n')
print(json.dumps(out, indent=1))
sys.exit(0 if not problems else 1)
