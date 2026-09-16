"""Apply the v3 carrier-owner revision to work/edited ONLY (a copy of the retained v2 final tree).

Adopts root's encoding-independent grammar exactly: every length(CAST(column AS BLOB)) = N becomes
instr(column, char(0)) = 0, retaining typeof TEXT, character length, prefix and whole-hex guards. Removes the v2
UTF-8-only restriction and the 'no lawful row is refused' claim, states storage-class enforcement as typeof() or exact
enumeration, keeps all storage-class, publication and route laws. Refuses to run unless the nine files equal the v2
final hashes. Emits the complete frozen37 -> v3 nine-file diff and the v2 -> v3 diff with hashes.
"""
import difflib, hashlib, json, re
from pathlib import Path

BASE = Path('/tmp/opensip-design-corrections/claude-source37-carrier-owner-author.v3')
FZ, V2, ED = BASE / 'work/frozen37', BASE / 'work/v2final', BASE / 'work/edited'
v2review = json.loads(Path('/tmp/opensip-design-corrections/claude-source37-carrier-owner-author.v2/review.json').read_text())
NINE = [f['path'] for f in v2review['files']]
V2HASH = {f['path']: f['v2'] for f in v2review['files']}
SEC = 'docs/coop/design-corrections/security/'
DDL, FMT, DISP, CHK = SEC + 'grant-journal.carrier.v3.sql', SEC + 'carrier-format.v3.md', SEC + 'carrier-dispatch.v3.json', SEC + 'check-carrier-v3.py'
AC = 'docs/v2/architecture/attempt-custody.schema.v1.json'
BYTELEN = re.compile(r'length\(CAST\((\w+) AS BLOB\)\) = \d+')


def sha(b):
    return hashlib.sha256(b).hexdigest()


for rel in NINE:
    if sha((ED / rel).read_bytes()) != V2HASH[rel] or sha((V2 / rel).read_bytes()) != V2HASH[rel]:
        raise SystemExit('not the v2 final bytes: ' + rel)
texts = {rel: (ED / rel).read_text(encoding='utf-8') for rel in NINE}


def rep(rel, old, new):
    n = texts[rel].count(old)
    if n != 1:
        raise SystemExit('anchor count %d in %s: %r' % (n, rel, old[:100]))
    texts[rel] = texts[rel].replace(old, new)


def slice_rep(rel, start, end, new, must_contain):
    t = texts[rel]
    if t.count(start) != 1 or t.count(end) != 1:
        raise SystemExit('slice markers in %s' % rel)
    a, b = t.index(start), t.index(end)
    if not a < b or any(m not in t[a:b] for m in must_contain):
        raise SystemExit('slice content in %s' % rel)
    texts[rel] = t[:a] + new + t[b:]


def strict(text):
    def hook(pairs):
        keys = [k for k, _ in pairs]
        if len(keys) != len(set(keys)):
            raise SystemExit('duplicate JSON key')
        return dict(pairs)
    return json.loads(text, object_pairs_hook=hook)


# ------------------------------------------------------------------ DDL: root substitution + header
texts[DDL], n_ddl = BYTELEN.subn(r'instr(\1, char(0)) = 0', texts[DDL])
if n_ddl != 7:
    raise SystemExit('expected 7 byte-length predicates, found %d' % n_ddl)
slice_rep(DDL, '-- Source37 owner correction (review advisories A37-01 and A37-02), revised after root reproduced embedded-NUL',
          '\n--\n-- Publication: no grant_journal_v3 row may exist',
    "-- Source37 owner correction (review advisories A37-01 and A37-02). Revised after root reproduced embedded-NUL\n"
    "-- and ASCII-hex BLOB admissions against the source37 v1 bytes, and again after root showed that the source37 v2\n"
    "-- byte-length predicate refused lawful rows in UTF-16 databases. These bytes supersede the earlier PROPOSED\n"
    "-- carrierFormat 3 bytes in place. No product implementation or deployed carrier was created from the earlier\n"
    "-- bytes. Reference in-memory SQLite instances were created from them by earlier design checks and review\n"
    "-- probes; those instances and their receipts remain historical evidence. The open dispatch validates the\n"
    "-- stored definitions byte-exactly, so a carrier created from earlier bytes is refused MIGRATION.CORRUPT\n"
    "-- rather than read as this definition. carrierFormat 1 and 2 bytes stay frozen.\n"
    "--\n"
    "-- Storage class and whole-value grammar. SQLite types values dynamically: TEXT affinity keeps a BLOB,\n"
    "-- INTEGER affinity keeps a non-integral REAL, and length() and GLOB stop at an embedded NUL. Every column's\n"
    "-- storage class is enforced either by an explicit typeof() guard (every INTEGER column, every free TEXT\n"
    "-- column and every hex-bearing column) or by exact enumeration (record_type and platform, whose IN lists\n"
    "-- hold only TEXT literals and so never equal a BLOB, a number or a NUL-suffixed text). Every hex-bearing\n"
    "-- column is an exact whole TEXT value: typeof(column) = 'text', length(column) = N, no NUL anywhere\n"
    "-- (instr(column, char(0)) = 0), the prefix GLOB where a prefix exists, and NOT GLOB '*[^0-9a-f]*' over\n"
    "-- the hex part. With no NUL, length() and GLOB see the whole value, and the case-sensitive hex class admits\n"
    "-- only ASCII 0-9 and a-f, so multibyte and malformed characters are refused by the same conjunction. The\n"
    "-- conjunction evaluates the TEXT value by character and does not depend on the database text encoding\n"
    "-- (exercised under UTF-8, UTF-16le and UTF-16be); no encoding is required of a carrier. CHECKs see values\n"
    "-- after column affinity, so an integer supplied as text '5' is stored and checked as integer 5. Host\n"
    "-- record admission still validates the closed record bodies; these CHECKs are defence in depth.",
    ['Byte lengths assume the SQLite database text encoding UTF-8', 'Every column\n-- therefore states its storage class with typeof()'])
ddl_rootalt = BYTELEN.subn(r'instr(\1, char(0)) = 0', (V2 / DDL).read_text())[0]


def strip_comments(sql):
    return '\n'.join(l for l in sql.splitlines() if not l.lstrip().startswith('--'))


if strip_comments(texts[DDL]) != strip_comments(ddl_rootalt):
    raise SystemExit('v3 DDL statements differ from root alternative applied to v2')

# ------------------------------------------------------------------ attempt custody planned private DDL and note
ac_before = strict(texts[AC])
old_ddl = ac_before['proposedPrivateDDL']
new_ddl, n_ac = BYTELEN.subn(r'instr(\1, char(0)) = 0', old_ddl)
if n_ac != 3:
    raise SystemExit('expected 3 attempt-custody byte-length predicates, found %d' % n_ac)
rep(AC, json.dumps(old_ddl, ensure_ascii=False), json.dumps(new_ddl, ensure_ascii=False))
AC_NOTE = {
    "standing": "Source37 owner correction (review advisory A37-01), revised after root reproduced embedded-NUL and ASCII-hex BLOB admissions against the source37 v1 bytes, and again after root showed that the source37 v2 byte-length predicate refused lawful rows in UTF-16 databases. The planned private DDL is corrected in place. No product implementation or deployed ledger table was created from the earlier bytes; reference in-memory SQLite instances were created from them by earlier design checks and review probes, and those instances and their receipts remain historical evidence.",
    "law": "Every column's storage class is enforced: by typeof() on store_generation_digest, namespace_id, execution_id and operation_ref (text) and on record_schema (integer), and by exact enumeration on phase and settled_outcome. Each hex-bearing column is an exact whole TEXT value: length(column) = N, instr(column, char(0)) = 0, its prefix GLOB and NOT GLOB '*[^0-9a-f]*' over the whole value, matching this record's patterns ^[0-9a-f]{64}, ^exec1_[0-9a-f]{32} and ^op-[0-9a-f]{32}. The conjunction does not depend on the database text encoding (exercised under UTF-8, UTF-16le and UTF-16be); no encoding is required.",
    "authority": "The ledger's record admission remains the owner of the closed record; the DDL is defence in depth. namespace_id keeps its character-length bound, which SQLite counts before any embedded NUL; the record's own minLength and maxLength govern. No member, phase, outcome, key or join changes."
}
lines = texts[AC].split('\n')
idx = [i for i, l in enumerate(lines) if l.startswith('  "ddlGrammarCorrection": ')]
if len(idx) != 1 or not lines[idx[0]].endswith(',') or 'Byte lengths assume' not in lines[idx[0]]:
    raise SystemExit('attempt custody note anchor')
lines[idx[0]] = '  "ddlGrammarCorrection": ' + json.dumps(AC_NOTE, ensure_ascii=False) + ','
texts[AC] = '\n'.join(lines)
ac_after = strict(texts[AC])
assert ac_after['proposedPrivateDDL'] == new_ddl and ac_after['ddlGrammarCorrection'] == AC_NOTE
assert {k: v for k, v in ac_after.items() if k not in ('proposedPrivateDDL', 'ddlGrammarCorrection')} == \
       {k: v for k, v in ac_before.items() if k not in ('proposedPrivateDDL', 'ddlGrammarCorrection')}

# ------------------------------------------------------------------ dispatch (structural; routes unchanged)
disp = strict(texts[DISP])
if json.dumps(disp, indent=2, ensure_ascii=False) + '\n' != texts[DISP]:
    raise SystemExit('dispatch JSON does not round-trip')
old_others = json.dumps({k: v for k, v in disp.items() if k != 'ddlGrammar'}, sort_keys=True)
g = disp['ddlGrammar']
g['standing'] += (' Revised in v3: root showed that the v2 predicate length(CAST(column AS BLOB)) = N refused lawful rows in UTF-16le '
                  'and UTF-16be databases; it is replaced by instr(column, char(0)) = 0 and no database text encoding is required.')
g['law'] = ("Every hex-bearing column of the carrierFormat 3 DDL and of the private attempt_custody DDL is an exact whole TEXT value: "
            "typeof(column) = 'text', length(column) = N (characters before any NUL), instr(column, char(0)) = 0 (no NUL anywhere), a "
            "prefix GLOB where a prefix exists, then substr(column, prefix + 1) NOT GLOB '*[^0-9a-f]*'. With no NUL, length() and GLOB see "
            "the whole value; the case-sensitive hex class admits only ASCII 0-9 and a-f, so multibyte and malformed characters are refused "
            "by the same conjunction. Removing any one conjunct admits a hostile value.")
g['storageClassLaw'] = ("Every carrierFormat 3 and attempt_custody column's storage class is enforced by one of two mechanisms. An explicit "
                        "typeof() guard: 'integer' for the INTEGER columns (the v1 range checks admitted a non-integral REAL in first_generation "
                        "and grantGeneration), 'text' for the free TEXT columns request_ref, token, install_generation_id, body and "
                        "namespace_id (a BLOB was admitted) and for every hex-bearing column. Exact enumeration: record_type, platform, phase "
                        "and settled_outcome have IN lists of TEXT literals only, and a whole-value comparison never equals a BLOB, a number or "
                        "a NUL-suffixed text. CHECK constraints see values after column affinity, so an integer supplied as text '5' is stored "
                        "and checked as integer 5.")
if 'encodingAssumption' not in g:
    raise SystemExit('v2 encodingAssumption missing')
del g['encodingAssumption']
g['encodingIndependence'] = ("The grammar evaluates TEXT values by character and does not depend on the database text encoding. The reference "
                             "matrix and the owner checker admit every canonical lawful row and refuse the NUL, BLOB, REAL, malformed UTF-8 or "
                             "UTF-16, multibyte, non-ASCII digit, prefix and length variants under UTF-8, UTF-16le and UTF-16be, and a UTF-16 "
                             "carrierFormat 2 carrier migrates, publishes and seals. No carrier or ledger is required to use a particular "
                             "encoding.")
if not g['alternativesRejected'][0].startswith('STRICT tables'):
    raise SystemExit('v2 STRICT alternative missing')
g['alternativesRejected'] = [
    g['alternativesRejected'][0],
    ('length(CAST(column AS BLOB)) = N (source37 v2): the byte count of a TEXT value depends on the database text encoding, so it '
     'refused every lawful hex-bearing row in UTF-16le and UTF-16be databases; withdrawn.'),
    ("instr(CAST(column AS BLOB), x'00') = 0: the BLOB view of a UTF-16 value contains zero bytes, so it also refuses lawful UTF-16 "
     "rows; the selected guard is the TEXT instr(column, char(0)) = 0."),
    ('instr(column, char(0)) = 0 without the character length, prefix and hex guards: admits uppercase, non-hex, short and long values; '
     'each retained conjunct is necessary.')]
old_scope = 'earlier PROPOSED carrierFormat 3 or attempt_custody bytes.'
if g['historicalScope'].count(old_scope) != 1:
    raise SystemExit('historical scope anchor')
g['historicalScope'] = g['historicalScope'].replace(
    old_scope, 'earlier PROPOSED carrierFormat 3 or attempt_custody bytes, including the source37 v1 and v2 revisions.')
assert json.dumps({k: v for k, v in disp.items() if k != 'ddlGrammar'}, sort_keys=True) == old_others
texts[DISP] = json.dumps(disp, indent=2, ensure_ascii=False) + '\n'

# ------------------------------------------------------------------ carrier-format.v3.md
rep(FMT, "class, character and byte length, prefix and hex tail (§5.1).", "class, character length, no NUL, prefix and hex tail (§5.1).")
slice_rep(FMT, '**Storage class and grammar (A37-01, revised).**', '**Revision history of this law.**',
    "**Storage class and grammar (A37-01, revised).** SQLite types values dynamically: a column's TEXT affinity\n"
    "keeps a BLOB, INTEGER affinity keeps a non-integral REAL, and `length()` and `GLOB` stop at an embedded NUL.\n"
    "Every carrierFormat 3 column's storage class is therefore enforced, by one of two mechanisms. An explicit\n"
    "`typeof()` guard states `integer` for `singleton`, `carrier_format`, `first_generation`, `chain_law`,\n"
    "`migrated_from`, `grantGeneration`, `seq` and `record_schema`, and `text` for `request_ref`, `token`,\n"
    "`install_generation_id`, `body` and every hex-bearing column. Exact enumeration enforces it for\n"
    "`record_type` and `platform`: their `IN` lists hold only TEXT literals, and a whole-value comparison never\n"
    "equals a BLOB, a number or a NUL-suffixed text. Each hex-bearing column (`carrier_format.project_key_digest`\n"
    "and `migration_op_ref`, and `grant_journal_v3.operation_ref`, `run_id`, `manifest_digest`, `body_sha256` and\n"
    "`prev_sha256`) is then an exact whole TEXT value: `typeof(column) = 'text'`, `length(column) = N`, no NUL\n"
    "anywhere (`instr(column, char(0)) = 0`), the prefix `GLOB` where a prefix exists, and\n"
    "`NOT GLOB '*[^0-9a-f]*'` over the hex part. With no NUL, `length()` and `GLOB` see the whole value, and the\n"
    "case-sensitive hex class admits only ASCII `0`–`9` and `a`–`f`, so a multibyte or malformed character is\n"
    "refused by the same conjunction. Removing any one conjunct admits a hostile value. The conjunction evaluates\n"
    "the TEXT value by character and does not depend on the database text encoding; it was exercised under\n"
    "UTF-8, UTF-16le and UTF-16be, and no encoding is required of a carrier. CHECKs see values after column\n"
    "affinity, so an integer supplied as text `'5'` is stored and checked as integer 5. The private\n"
    "`attempt_custody` DDL applies the same laws: `typeof()` on `store_generation_digest`, `execution_id`,\n"
    "`operation_ref`, `namespace_id` and `record_schema`, and exact enumeration on `phase` and `settled_outcome`.\n"
    "Host record admission still validates the closed record bodies; the DDL is defence in depth.\n\n",
    ['length(CAST(column AS BLOB)) = N', 'which fails closed.', 'no lawful row is refused'])
rep(FMT, "generations (§9).\n\n**Historical scope.**",
    "generations (§9).\n\n"
    "The source37 v2 revision then paired `length(column) = N` with a byte count,\n"
    "`length(CAST(column AS BLOB)) = N`, assumed a UTF-8 database and described the refusal of every UTF-16\n"
    "hex-bearing row as failing closed. Root showed that this refused otherwise lawful rows in UTF-16le and\n"
    "UTF-16be databases, although no earlier owner requires a text encoding for historical SQLite carriers. This\n"
    "revision replaces the byte count with `instr(column, char(0)) = 0`; with the retained storage class,\n"
    "character length, prefix and whole-hex guards it gives the same exact grammar in all three encodings, and\n"
    "the v2 encoding restriction is withdrawn.\n\n"
    "**Historical scope.**")
rep(FMT, "created from the earlier PROPOSED carrierFormat 3 bytes. Reference",
    "created from the earlier PROPOSED carrierFormat 3 bytes, including the source37 v1 and v2 revisions. Reference")

# ------------------------------------------------------------------ checker
slice_rep(CHK, '# ---- 7. source37 owner correction: exact storage class and whole-value grammar (A37-01, revised v2)',
          '# ---- 8. source37 owner correction: publication and first_generation law',
          (BASE / 'probes' / 'check_carrier_v3_section7_v3.py.txt').read_text(encoding='utf-8'),
          ['under a UTF-16 database encoding hex-bearing rows fail closed'])

# ------------------------------------------------------------------ write, diffs, hashes
full, delta, files = [], [], []
for rel in NINE:
    (ED / rel).write_text(texts[rel], encoding='utf-8')
    f, v, e = (FZ / rel).read_bytes(), (V2 / rel).read_bytes(), (ED / rel).read_bytes()
    files.append({'path': rel, 'frozen37Sha256': sha(f), 'v2Sha256': sha(v), 'v3Sha256': sha(e), 'changedInV3': v != e,
                  'bytes': {'frozen37': len(f), 'v2': len(v), 'v3': len(e)}})
    full += difflib.unified_diff(f.decode().splitlines(keepends=True), e.decode().splitlines(keepends=True),
                                 fromfile='a/' + rel, tofile='b/' + rel, n=3)
    delta += difflib.unified_diff(v.decode().splitlines(keepends=True), e.decode().splitlines(keepends=True),
                                  fromfile='v2/' + rel, tofile='v3/' + rel, n=3)
full_b, delta_b = ''.join(full).encode(), ''.join(delta).encode()
(BASE / 'proposed-edits.diff').write_bytes(full_b)
(BASE / 'v2-to-v3.diff').write_bytes(delta_b)
record = {'files': files, 'proposedEditsDiff': {'sha256': sha(full_b), 'lines': full_b.count(b'\n')},
          'v2ToV3Diff': {'sha256': sha(delta_b), 'lines': delta_b.count(b'\n')},
          'rootAlternativeReplacements': {'ddl': n_ddl, 'attemptCustody': n_ac}, 'ddlStatementsEqualRootAlternative': True,
          'attemptCustodyDdlEqualsRootAlternative': new_ddl == BYTELEN.subn(r'instr(\1, char(0)) = 0', old_ddl)[0], 'routesUnchanged': True}
(BASE / 'receipts' / 'p02-apply-v3.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps(record, indent=2))
