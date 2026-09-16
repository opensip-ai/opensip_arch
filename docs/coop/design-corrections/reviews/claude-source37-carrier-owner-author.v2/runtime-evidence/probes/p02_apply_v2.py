"""Apply the v2 carrier-owner revision to work/edited ONLY (a copy of the retained v1 final tree).

Remedy: exact storage class for every carrierFormat 3 / attempt_custody column and whole-value grammar for every
hex column (typeof + character length + byte length + prefix + hex), after root's embedded-NUL and ASCII-hex BLOB
counterexamples. Also corrects the v1 wording that earlier carrierFormat 3 bytes were never instantiated.
Routes are unchanged. Refuses to run unless the nine files equal the v1 final hashes. Emits the complete
frozen37 -> v2 nine-file diff and the v1 -> v2 diff with before/after hashes.
"""
import difflib, hashlib, json
from pathlib import Path

BASE = Path('/tmp/opensip-design-corrections/claude-source37-carrier-owner-author.v2')
FZ, V1, ED = BASE / 'work/frozen37', BASE / 'work/v1final', BASE / 'work/edited'
v1review = json.loads(Path('/tmp/opensip-design-corrections/claude-source37-carrier-owner-author.v1/review.json').read_text())
NINE = [f['path'] for f in v1review['proposedEdits']['files']]
V1AFTER = {f['path']: f['after'] for f in v1review['proposedEdits']['files']}
SEC = 'docs/coop/design-corrections/security/'
DDL, FMT, DISP, CHK = SEC + 'grant-journal.carrier.v3.sql', SEC + 'carrier-format.v3.md', SEC + 'carrier-dispatch.v3.json', SEC + 'check-carrier-v3.py'
AC = 'docs/v2/architecture/attempt-custody.schema.v1.json'


def sha(b):
    return hashlib.sha256(b).hexdigest()


for rel in NINE:
    if sha((ED / rel).read_bytes()) != V1AFTER[rel] or sha((V1 / rel).read_bytes()) != V1AFTER[rel]:
        raise SystemExit('not the v1 final bytes: ' + rel)
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


# ------------------------------------------------------------------ DDL
slice_rep(DDL, '-- Source37 owner correction (review advisories A37-01 and A37-02).', '\nCREATE TABLE carrier_format (',
    "-- Source37 owner correction (review advisories A37-01 and A37-02), revised after root reproduced embedded-NUL\n"
    "-- and ASCII-hex BLOB admissions against the source37 v1 bytes. These bytes supersede the earlier PROPOSED\n"
    "-- carrierFormat 3 bytes in place. No product implementation or deployed carrier was created from the earlier\n"
    "-- bytes. Reference in-memory SQLite instances were created from them by earlier design checks and review\n"
    "-- probes; those instances and their receipts remain historical evidence. The open dispatch validates the\n"
    "-- stored definitions byte-exactly, so a carrier created from earlier bytes is refused MIGRATION.CORRUPT\n"
    "-- rather than read as this definition. carrierFormat 1 and 2 bytes stay frozen.\n"
    "--\n"
    "-- Storage class and whole-value grammar. SQLite types values dynamically: TEXT affinity keeps a BLOB,\n"
    "-- INTEGER affinity keeps a non-integral REAL, and length() and GLOB stop at an embedded NUL. Every column\n"
    "-- therefore states its storage class with typeof(). Every hex-bearing column also requires\n"
    "-- length(column) = N (characters before any NUL) and length(CAST(column AS BLOB)) = N (every byte); the\n"
    "-- two agree only for a NUL-free ASCII value, so the prefix GLOB and NOT GLOB '*[^0-9a-f]*' then see the\n"
    "-- whole value. Enumerated TEXT columns compare whole values, which never equal a BLOB or a NUL-suffixed\n"
    "-- text. CHECKs see values after column affinity, so an integer supplied as text '5' is checked as 5.\n"
    "-- Byte lengths assume the SQLite database text encoding UTF-8 (the default, fixed at creation); under\n"
    "-- another encoding every hex-bearing row is refused, which fails closed. Host record admission still\n"
    "-- validates the closed record bodies; these CHECKs are defence in depth.\n"
    "--\n"
    "-- Publication: no grant_journal_v3 row may exist before the carrier_format row is published, and\n"
    "-- first_generation is 1 on the fresh path and at least 2 on the migrated path.\n",
    ['No carrierFormat 3 instance was ever created', 'first_generation is 1 on the fresh path'])
slice_rep(DDL, 'CREATE TABLE carrier_format (', '  CHECK ((migrated_from IS NULL AND migration_op_ref IS NULL)',
    "CREATE TABLE carrier_format (\n"
    "  singleton          INTEGER NOT NULL PRIMARY KEY CHECK (typeof(singleton) = 'integer' AND singleton = 1),\n"
    "  carrier_format     INTEGER NOT NULL CHECK (typeof(carrier_format) = 'integer' AND carrier_format = 3),\n"
    "  project_key_digest TEXT    NOT NULL CHECK (typeof(project_key_digest) = 'text'\n"
    "                               AND length(project_key_digest) = 64\n"
    "                               AND length(CAST(project_key_digest AS BLOB)) = 64\n"
    "                               AND project_key_digest NOT GLOB '*[^0-9a-f]*'),\n"
    "  first_generation   INTEGER NOT NULL CHECK (typeof(first_generation) = 'integer'\n"
    "                               AND first_generation >= 1\n"
    "                               AND first_generation <= 9223372036854775807),\n"
    "  -- Exactly the selected chain law. Value 2 (a recursive chain) is NOT selected and is NOT\n"
    "  -- implemented, so the column refuses it rather than advertising an unbuilt alternative.\n"
    "  -- Widening this CHECK is a reviewed successor act, not a configuration choice.\n"
    "  chain_law          INTEGER NOT NULL CHECK (typeof(chain_law) = 'integer' AND chain_law = 1),\n"
    "  migrated_from      INTEGER          CHECK (migrated_from IS NULL\n"
    "                               OR (typeof(migrated_from) = 'integer' AND migrated_from IN (1, 2))),\n"
    "  migration_op_ref   TEXT             CHECK (migration_op_ref IS NULL\n"
    "                               OR (typeof(migration_op_ref) = 'text'\n"
    "                                   AND length(migration_op_ref) = 35\n"
    "                                   AND length(CAST(migration_op_ref AS BLOB)) = 35\n"
    "                                   AND migration_op_ref GLOB 'op-*'\n"
    "                                   AND substr(migration_op_ref, 4) NOT GLOB '*[^0-9a-f]*')),\n",
    ["project_key_digest NOT GLOB '*[^0-9a-f]*'", 'substr(migration_op_ref, 4)'])
slice_rep(DDL, 'CREATE TABLE grant_journal_v3 (', '  -- Capacity records are the FROZEN recordSchema-1 TERMINAL body',
    "CREATE TABLE grant_journal_v3 (\n"
    "  grantGeneration INTEGER NOT NULL CHECK (typeof(grantGeneration) = 'integer'\n"
    "                              AND grantGeneration >= 1\n"
    "                              AND grantGeneration <= 9223372036854775807),\n"
    "  seq          INTEGER NOT NULL CHECK (typeof(seq) = 'integer'\n"
    "                              AND seq >= 1 AND seq <= 9007199254740991),\n"
    "  record_schema INTEGER NOT NULL CHECK (typeof(record_schema) = 'integer' AND record_schema IN (1, 3)),\n"
    "  record_type  TEXT    NOT NULL CHECK (record_type IN\n"
    "                 ('GRANT','RA','ICI','RCI','ICO','RCO','REV','CLN','SEAL','TERMINAL')),\n"
    "  operation_ref TEXT   NOT NULL CHECK (typeof(operation_ref) = 'text'\n"
    "                              AND length(operation_ref) = 35\n"
    "                              AND length(CAST(operation_ref AS BLOB)) = 35\n"
    "                              AND operation_ref GLOB 'op-*'\n"
    "                              AND substr(operation_ref, 4) NOT GLOB '*[^0-9a-f]*'),\n"
    "  request_ref  TEXT    CHECK (request_ref IS NULL OR typeof(request_ref) = 'text'),\n"
    "  token        TEXT    CHECK (token IS NULL OR typeof(token) = 'text'),\n"
    "  install_generation_id TEXT CHECK (install_generation_id IS NULL OR typeof(install_generation_id) = 'text'),\n"
    "  manifest_digest TEXT CHECK (manifest_digest IS NULL OR (typeof(manifest_digest) = 'text'\n"
    "                              AND length(manifest_digest) = 64\n"
    "                              AND length(CAST(manifest_digest AS BLOB)) = 64\n"
    "                              AND manifest_digest NOT GLOB '*[^0-9a-f]*')),\n"
    "  platform     TEXT    CHECK (platform IS NULL OR platform IN\n"
    "                 ('macos-aarch64','macos-x86_64','linux-x86_64-gnu','linux-aarch64-gnu')),\n"
    "  run_id       TEXT    CHECK (run_id IS NULL OR (typeof(run_id) = 'text'\n"
    "                              AND length(run_id) = 69\n"
    "                              AND length(CAST(run_id AS BLOB)) = 69\n"
    "                              AND run_id GLOB 'run3:*'\n"
    "                              AND substr(run_id, 6) NOT GLOB '*[^0-9a-f]*')),\n"
    "  body         TEXT    NOT NULL CHECK (typeof(body) = 'text'),\n"
    "  body_sha256  TEXT    NOT NULL CHECK (typeof(body_sha256) = 'text'\n"
    "                              AND length(body_sha256) = 64\n"
    "                              AND length(CAST(body_sha256 AS BLOB)) = 64\n"
    "                              AND body_sha256 NOT GLOB '*[^0-9a-f]*'),\n"
    "  prev_sha256  TEXT    NOT NULL CHECK (typeof(prev_sha256) = 'text'\n"
    "                              AND length(prev_sha256) = 64\n"
    "                              AND length(CAST(prev_sha256 AS BLOB)) = 64\n"
    "                              AND prev_sha256 NOT GLOB '*[^0-9a-f]*'),\n",
    ["body_sha256 NOT GLOB '*[^0-9a-f]*'", 'substr(run_id, 6)', 'request_ref  TEXT,'])

# ------------------------------------------------------------------ attempt custody planned private DDL and note
ac_before = strict(texts[AC])
old_ddl = ac_before['proposedPrivateDDL']
new_ddl = old_ddl
for old, new in (
        ("store_generation_digest TEXT NOT NULL CHECK (length(store_generation_digest) = 64 AND store_generation_digest NOT GLOB '*[^0-9a-f]*'),",
         "store_generation_digest TEXT NOT NULL CHECK (typeof(store_generation_digest) = 'text' AND length(store_generation_digest) = 64 AND length(CAST(store_generation_digest AS BLOB)) = 64 AND store_generation_digest NOT GLOB '*[^0-9a-f]*'),"),
        ("namespace_id    TEXT NOT NULL CHECK (length(namespace_id) BETWEEN 1 AND 4096),",
         "namespace_id    TEXT NOT NULL CHECK (typeof(namespace_id) = 'text' AND length(namespace_id) BETWEEN 1 AND 4096),"),
        ("execution_id    TEXT NOT NULL CHECK (execution_id GLOB 'exec1_*' AND length(execution_id) = 38 AND substr(execution_id, 7) NOT GLOB '*[^0-9a-f]*'),",
         "execution_id    TEXT NOT NULL CHECK (typeof(execution_id) = 'text' AND length(execution_id) = 38 AND length(CAST(execution_id AS BLOB)) = 38 AND execution_id GLOB 'exec1_*' AND substr(execution_id, 7) NOT GLOB '*[^0-9a-f]*'),"),
        ("operation_ref   TEXT NOT NULL CHECK (operation_ref GLOB 'op-*' AND length(operation_ref) = 35 AND substr(operation_ref, 4) NOT GLOB '*[^0-9a-f]*'),",
         "operation_ref   TEXT NOT NULL CHECK (typeof(operation_ref) = 'text' AND length(operation_ref) = 35 AND length(CAST(operation_ref AS BLOB)) = 35 AND operation_ref GLOB 'op-*' AND substr(operation_ref, 4) NOT GLOB '*[^0-9a-f]*'),"),
        ("record_schema   INTEGER NOT NULL CHECK (record_schema = 1),",
         "record_schema   INTEGER NOT NULL CHECK (typeof(record_schema) = 'integer' AND record_schema = 1),")):
    if new_ddl.count(old) != 1:
        raise SystemExit('attempt custody DDL anchor: ' + old[:60])
    new_ddl = new_ddl.replace(old, new)
rep(AC, json.dumps(old_ddl, ensure_ascii=False), json.dumps(new_ddl, ensure_ascii=False))
AC_NOTE = {
    "standing": "Source37 owner correction (review advisory A37-01), revised after root reproduced embedded-NUL and ASCII-hex BLOB admissions against the source37 v1 bytes. The planned private DDL is corrected in place. No product implementation or deployed ledger table was created from the earlier bytes; reference in-memory SQLite instances were created from them by earlier design checks and review probes, and those instances and their receipts remain historical evidence.",
    "law": "Every column states its storage class with typeof(): text for store_generation_digest, namespace_id, execution_id and operation_ref, integer for record_schema; phase and settled_outcome compare whole values against their enumerations. Each hex-bearing column additionally requires length(column) = N and length(CAST(column AS BLOB)) = N, which agree only for a NUL-free ASCII value, then its prefix GLOB and NOT GLOB '*[^0-9a-f]*' over the whole value, matching this record's patterns ^[0-9a-f]{64}, ^exec1_[0-9a-f]{32} and ^op-[0-9a-f]{32}. Byte lengths assume the SQLite database text encoding UTF-8; under another encoding every hex-bearing row is refused, which fails closed.",
    "authority": "The ledger's record admission remains the owner of the closed record; the DDL is defence in depth. namespace_id keeps its character-length bound, which SQLite counts before any embedded NUL; the record's own minLength and maxLength govern. No member, phase, outcome, key or join changes."
}
lines = texts[AC].split('\n')
idx = [i for i, l in enumerate(lines) if l.startswith('  "ddlGrammarCorrection": ')]
if len(idx) != 1 or not lines[idx[0]].endswith(','):
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
old_projection = json.dumps(disp['publicProjectionByPhase'], sort_keys=True)
g = disp['ddlGrammar']
g['standing'] = ('Source37 owner correction (review advisory A37-01), revised after root reproduced embedded-NUL and ASCII-hex BLOB '
                 'admissions against the source37 v1 DDL (sha256 f0a22382f8a5a5bc356334cfde16f7ca1fa6caa37e537cc7924cd46ffd81e3ba). '
                 'Those are DDL admission counterexamples, not a demonstrated product exploit; host record admission remains separate.')
g['law'] = ("Every hex-bearing column of the carrierFormat 3 DDL and of the private attempt_custody DDL is an exact whole TEXT value: "
            "typeof(column) = 'text', length(column) = N (characters before any NUL), length(CAST(column AS BLOB)) = N (every byte), "
            "a prefix GLOB where a prefix exists, then substr(column, prefix + 1) NOT GLOB '*[^0-9a-f]*'. The two lengths agree only "
            "for a NUL-free ASCII value, so GLOB sees the whole value; GLOB is case-sensitive.")
g['storageClassLaw'] = ("Every carrierFormat 3 and attempt_custody column states its storage class with typeof(): 'integer' for the "
                        "INTEGER columns (the v1 range checks admitted a non-integral REAL in first_generation and grantGeneration), "
                        "'text' for the free TEXT columns request_ref, token, install_generation_id, body and namespace_id (a BLOB was "
                        "admitted) and for every hex-bearing column. The enumerated TEXT columns record_type, platform, phase and "
                        "settled_outcome compare whole values, which never equal a BLOB or a NUL-suffixed text, so they carry no further "
                        "guard. CHECK constraints see values after column affinity: an integer supplied as text '5' is stored and checked "
                        "as integer 5, and no lawful row is refused.")
g['carrierFormat3IntegerColumns'] = ['carrier_format.singleton', 'carrier_format.carrier_format', 'carrier_format.first_generation',
                                     'carrier_format.chain_law', 'carrier_format.migrated_from', 'grant_journal_v3.grantGeneration',
                                     'grant_journal_v3.seq', 'grant_journal_v3.record_schema']
g['carrierFormat3TextColumns'] = ['grant_journal_v3.request_ref', 'grant_journal_v3.token', 'grant_journal_v3.install_generation_id',
                                  'grant_journal_v3.body']
g['carrierFormat3EnumeratedColumns'] = ['grant_journal_v3.record_type', 'grant_journal_v3.platform']
g['attemptCustodyIntegerColumns'] = ['record_schema']
g['attemptCustodyTextColumns'] = ['namespace_id']
g['attemptCustodyEnumeratedColumns'] = ['phase', 'settled_outcome']
g['encodingAssumption'] = ('Byte lengths are UTF-8 byte lengths: the carrier and ledger database text encoding is UTF-8, the SQLite default '
                           'fixed at database creation. Under a UTF-16 encoding every hex-bearing row is refused, so a wrong encoding fails '
                           'closed and never widens admission.')
g['alternativesRejected'] = [
    ('STRICT tables: they refuse a BLOB in a TEXT column and a REAL in an INTEGER column, but do not refuse an embedded NUL, and '
     'SQLite documents that a database containing a STRICT table cannot be read by SQLite libraries older than 3.37.0, which would '
     'contradict the selected staging in which a format-unaware core still reads historical generations.'),
    ("instr(CAST(column AS BLOB), x'00') = 0 alone: refuses an embedded NUL but not a multibyte character of equal character count; "
     "the character and byte length pair refuses both.")]
g['authority'] = 'Host record admission still validates the closed record bodies. The DDL is defence in depth.'
g['historicalScope'] = ('carrierFormat 1 and 2 bytes are frozen and unchanged: their GLOB checks inspect only the first character after a '
                        'prefix, and they also admit embedded-NUL and BLOB values. That is a disclosed historical limit, not repaired: '
                        'historical rows are read as history under recordSchema-1 semantics, are never re-admitted through the schema-3 '
                        'gate and can never satisfy a schema-3 SEAL join (F46), so a malformed historical value confers no commitment. No '
                        'product implementation or deployed carrier or ledger table was created from the earlier PROPOSED carrierFormat 3 '
                        'or attempt_custody bytes. Reference in-memory SQLite instances were created from them by earlier design checks '
                        'and review probes and remain historical evidence; the open dispatch validates definitions byte-exactly, so a '
                        'carrier created from earlier bytes is refused MIGRATION.CORRUPT rather than read as this definition.')
assert json.dumps(disp['publicProjectionByPhase'], sort_keys=True) == old_projection
texts[DISP] = json.dumps(disp, indent=2, ensure_ascii=False) + '\n'

# ------------------------------------------------------------------ carrier-format.v3.md
rep(FMT, "- **operation_ref grammar.** `op-` plus 32 lowercase hex, length 35, enforced over the **whole** tail\n"
         "  (`substr(operation_ref, 4) NOT GLOB '*[^0-9a-f]*'`). An earlier revision of this DDL, like the frozen\n"
         "  carrierFormat 2 bytes, used `GLOB 'op-[0-9a-f]*'`, which checks only the first character after the\n"
         "  prefix; see §5.1.\n",
    "- **operation_ref grammar.** `op-` plus 32 lowercase hex, length 35, as one whole TEXT value: storage\n"
    "  class, character and byte length, prefix and hex tail (§5.1). The frozen carrierFormat 2 bytes check only\n"
    "  the first character after the prefix, and the source37 v1 revision of this DDL checked the tail but still\n"
    "  admitted an embedded-NUL suffix or an ASCII-hex BLOB; see §5.1.\n")
slice_rep(FMT, '### 5.1 Lowercase-hex grammar and the publication law (source37 owner correction)', '**Publication law (A37-02).**',
    "### 5.1 Exact storage class, whole-value grammar and the publication law (source37 owner correction)\n\n"
    "**Storage class and grammar (A37-01, revised).** SQLite types values dynamically: a column's TEXT affinity\n"
    "keeps a BLOB, INTEGER affinity keeps a non-integral REAL, and `length()` and `GLOB` stop at an embedded NUL.\n"
    "Every carrierFormat 3 column therefore states its storage class with `typeof()`: `integer` for `singleton`,\n"
    "`carrier_format`, `first_generation`, `chain_law`, `migrated_from`, `grantGeneration`, `seq` and\n"
    "`record_schema`; `text` for `request_ref`, `token`, `install_generation_id`, `body` and every hex-bearing\n"
    "column. Each hex-bearing column (`carrier_format.project_key_digest` and `migration_op_ref`, and\n"
    "`grant_journal_v3.operation_ref`, `run_id`, `manifest_digest`, `body_sha256` and `prev_sha256`) also\n"
    "requires `length(column) = N`, which counts characters before any NUL, and\n"
    "`length(CAST(column AS BLOB)) = N`, which counts every byte. The two agree only for a NUL-free ASCII value,\n"
    "so the prefix `GLOB` and `NOT GLOB '*[^0-9a-f]*'` then see the whole value; `GLOB` is case-sensitive. The\n"
    "enumerated columns `record_type` and `platform` compare whole values, which never equal a BLOB or a\n"
    "NUL-suffixed text, so they need no further guard. CHECKs see values after column affinity, so an integer\n"
    "supplied as text `'5'` is stored and checked as integer 5 and no lawful row is refused. The private\n"
    "`attempt_custody` DDL applies the same laws to `store_generation_digest`, `execution_id`,\n"
    "`operation_ref`, `namespace_id` and `record_schema`. Byte lengths assume the SQLite database text encoding\n"
    "UTF-8, the default fixed at database creation; under another encoding every hex-bearing row is refused,\n"
    "which fails closed. Host record admission still validates the closed record bodies; the DDL is defence in\n"
    "depth.\n\n"
    "**Revision history of this law.** The source37 v1 correction replaced a first-character-only `GLOB` with a\n"
    "whole-tail `NOT GLOB` and described the result as exact. Root then reproduced, against those v1 bytes, an\n"
    "embedded-NUL suffix being admitted in `body_sha256`, `operation_ref` and `run_id`, and an ASCII-hex BLOB\n"
    "being admitted in `body_sha256` and `project_key_digest`. The exhaustive storage-class matrix run for this\n"
    "revision found the same NUL and BLOB admissions in every hex-bearing column, a BLOB in every free TEXT\n"
    "column, and a non-integral REAL in `first_generation` and `grantGeneration`. These are DDL admission\n"
    "counterexamples, not a demonstrated product exploit. STRICT tables were not selected: they do not refuse an\n"
    "embedded NUL, and SQLite documents that a database containing a STRICT table cannot be read by libraries\n"
    "older than 3.37.0, which would contradict the staging in which a format-unaware core still reads historical\n"
    "generations (§9).\n\n"
    "**Historical scope.** carrierFormat 1 and 2 bytes are frozen and unchanged. Their `GLOB` checks inspect only\n"
    "the first character after a prefix, and they also admit embedded-NUL and BLOB values. That weakness is\n"
    "disclosed, not repaired: historical rows are read as history under recordSchema-1 semantics, are never\n"
    "re-admitted through the schema-3 gate and can never satisfy a schema-3 `SEAL` join (§9, F46), so a\n"
    "malformed historical value confers no commitment. No product implementation or deployed carrier was\n"
    "created from the earlier PROPOSED carrierFormat 3 bytes. Reference in-memory SQLite instances were created\n"
    "from them by earlier design checks and review probes, and those instances and their receipts remain\n"
    "historical evidence. The open dispatch validates definitions byte-exactly, so a carrier created from\n"
    "earlier bytes is refused `MIGRATION.CORRUPT` rather than read as this definition.\n\n",
    ['never instantiated', 'depth that now matches the stated grammar exactly.'])
rep(FMT, "| whole-tail lowercase-hex CHECKs | the stated grammar is enforced, not only its first character (§5.1) |",
    "| whole-value storage-class and hex CHECKs | a value is admitted only in its exact storage class and whole grammar: no embedded NUL, BLOB or non-integral REAL (§5.1) |")

# ------------------------------------------------------------------ checker
slice_rep(CHK, '# ---- 7. source37 owner correction: lowercase-hex grammar (review advisory A37-01)',
          '# ---- 8. source37 owner correction: publication and first_generation law',
          (BASE / 'probes' / 'check_carrier_v3_section7_v2.py.txt').read_text(encoding='utf-8'),
          ['def _s37_bad(value):'])
rep(CHK, "c.executescript(ddl3.replace('CHECK (chain_law = 1)', 'CHECK (chain_law IN (1, 2))'))\n",
    "_s37_mutated = ddl3.replace('AND chain_law = 1)', 'AND chain_law IN (1, 2))')\n"
    "ck('source37 scenario: the invalid-definition mutation really changes the DDL', _s37_mutated != ddl3)\n"
    "c.executescript(_s37_mutated)\n")

# ------------------------------------------------------------------ write, diffs, hashes
full, delta, files = [], [], []
for rel in NINE:
    (ED / rel).write_text(texts[rel], encoding='utf-8')
    f, v, e = (FZ / rel).read_bytes(), (V1 / rel).read_bytes(), (ED / rel).read_bytes()
    files.append({'path': rel, 'frozen37Sha256': sha(f), 'v1Sha256': sha(v), 'v2Sha256': sha(e), 'changedInV2': v != e,
                  'bytes': {'frozen37': len(f), 'v1': len(v), 'v2': len(e)}})
    full += difflib.unified_diff(f.decode().splitlines(keepends=True), e.decode().splitlines(keepends=True),
                                 fromfile='a/' + rel, tofile='b/' + rel, n=3)
    delta += difflib.unified_diff(v.decode().splitlines(keepends=True), e.decode().splitlines(keepends=True),
                                  fromfile='v1/' + rel, tofile='v2/' + rel, n=3)
full_b, delta_b = ''.join(full).encode(), ''.join(delta).encode()
(BASE / 'proposed-edits.diff').write_bytes(full_b)
(BASE / 'v1-to-v2.diff').write_bytes(delta_b)
record = {'files': files, 'proposedEditsDiff': {'sha256': sha(full_b), 'lines': full_b.count(b'\n')},
          'v1ToV2Diff': {'sha256': sha(delta_b), 'lines': delta_b.count(b'\n')}, 'routesUnchanged': True}
(BASE / 'receipts' / 'p02-apply-v2.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps(record, indent=2))
