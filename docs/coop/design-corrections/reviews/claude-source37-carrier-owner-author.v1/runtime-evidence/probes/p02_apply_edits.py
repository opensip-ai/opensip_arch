"""Apply the source37 carrier-owner correction (A37-01..A37-04, owned A37-07 wording) to work/edited ONLY.

Text edits require exactly one anchor. JSON files are admitted strictly (duplicate keys refused) before and after;
JSON edits are structural when the untouched file round-trips byte-exactly, otherwise exact text insertion,
and the result is re-parsed and compared with the intended structure. Refuses to run when a target already
differs from baseline. Emits proposed-edits.diff and before/after hashes.
"""
import copy, difflib, hashlib, json
from pathlib import Path

BASE = Path('/tmp/opensip-design-corrections/claude-source37-carrier-owner-author.v1')
BL, ED = BASE / 'work/baseline', BASE / 'work/edited'
SEC = 'docs/coop/design-corrections/security/'
ARCH = 'docs/v2/architecture/'
DDL = SEC + 'grant-journal.carrier.v3.sql'
FMT = SEC + 'carrier-format.v3.md'
MIG = SEC + 'carrier-migration.v1.md'
DISP = SEC + 'carrier-dispatch.v3.json'
CHK = SEC + 'check-carrier-v3.py'
AC = ARCH + 'attempt-custody.schema.v1.json'
RO = ARCH + 'commit-recovery-readonly.v3.md'
LIN = ARCH + 'store-instance-lineage.v1.json'
S12 = 'docs/v2/contracts/product-v1/security-and-lifecycle.md'
CHANGED = [DDL, FMT, MIG, DISP, CHK, AC, RO, LIN, S12]


def sha(b):
    return hashlib.sha256(b).hexdigest()


for rel in CHANGED:
    if (ED / rel).read_bytes() != (BL / rel).read_bytes():
        raise SystemExit('edited copy already differs from baseline: ' + rel)

texts = {rel: (BL / rel).read_text(encoding='utf-8') for rel in CHANGED}


def rep(rel, old, new):
    n = texts[rel].count(old)
    if n != 1:
        raise SystemExit('anchor count %d in %s: %r' % (n, rel, old[:90]))
    texts[rel] = texts[rel].replace(old, new)


def strict(text):
    def hook(pairs):
        keys = [k for k, _ in pairs]
        if len(keys) != len(set(keys)):
            raise SystemExit('duplicate JSON key')
        return dict(pairs)
    return json.loads(text, object_pairs_hook=hook)


STANDING = ('**Current standing.** The Source25 authoring baseline stated above is historical and is not '
            'relabelled. The current bytes carry the source37 owner correction of review advisories A37-01 to '
            'A37-04 (`design-corrections/security/carrier-format.v3.md` §8.1). They remain '
            'PROPOSED-NOT-SELF-ACCEPTED and are bound only by whichever candidate manifest selects them; no '
            'acceptance, readiness or implementation authorization follows.')

# ------------------------------------------------------------------ A37-01 / A37-02: carrierFormat 3 DDL
rep(DDL, "-- carrierFormat 3: this file.\n",
    "-- carrierFormat 3: this file.\n"
    "--\n"
    "-- Source37 owner correction (review advisories A37-01 and A37-02). These bytes supersede the earlier\n"
    "-- PROPOSED carrierFormat 3 bytes in place. No carrierFormat 3 instance was ever created from the\n"
    "-- earlier bytes (design/reference only), and the open dispatch binds exactly these definitions, so the\n"
    "-- earlier bytes are never a second admitted definition. carrierFormat 1 and 2 bytes stay frozen.\n"
    "--\n"
    "-- Grammar: every hex-bearing column is lowercase hex over its whole hex part with an exact length,\n"
    "-- checked as  substr(column, prefix + 1) NOT GLOB '*[^0-9a-f]*'. GLOB is case-sensitive, so an\n"
    "-- uppercase or non-hex character anywhere refuses. Host record admission still validates the closed\n"
    "-- record bodies; these CHECKs are defence in depth that match the stated grammar exactly.\n"
    "--\n"
    "-- Publication: no grant_journal_v3 row may exist before the carrier_format row is published, and\n"
    "-- first_generation is 1 on the fresh path and at least 2 on the migrated path.\n")
rep(DDL, "CHECK (length(project_key_digest) = 64\n                               AND project_key_digest GLOB '[0-9a-f]*'),",
    "CHECK (length(project_key_digest) = 64\n                               AND project_key_digest NOT GLOB '*[^0-9a-f]*'),")
rep(DDL, "(migration_op_ref GLOB 'op-[0-9a-f]*'\n                                   AND length(migration_op_ref) = 35)),",
    "(migration_op_ref GLOB 'op-*'\n                                   AND length(migration_op_ref) = 35\n"
    "                                   AND substr(migration_op_ref, 4) NOT GLOB '*[^0-9a-f]*')),")
rep(DDL, "  CHECK ((migrated_from IS NULL AND migration_op_ref IS NULL)\n      OR (migrated_from IS NOT NULL AND migration_op_ref IS NOT NULL))\n) WITHOUT ROWID;",
    "  CHECK ((migrated_from IS NULL AND migration_op_ref IS NULL)\n      OR (migrated_from IS NOT NULL AND migration_op_ref IS NOT NULL)),\n"
    "  -- first_generation at publication: the fresh path publishes generation 1 exactly; the migrated path\n"
    "  -- publishes (max inherited generation) + 1, at least 2 because act A closed a generation >= 1.\n"
    "  CHECK ((migrated_from IS NULL AND first_generation = 1)\n      OR (migrated_from IS NOT NULL AND first_generation >= 2))\n) WITHOUT ROWID;")
rep(DDL, "operation_ref TEXT   NOT NULL CHECK (operation_ref GLOB 'op-[0-9a-f]*'\n                              AND length(operation_ref) = 35),",
    "operation_ref TEXT   NOT NULL CHECK (operation_ref GLOB 'op-*'\n                              AND length(operation_ref) = 35\n"
    "                              AND substr(operation_ref, 4) NOT GLOB '*[^0-9a-f]*'),")
rep(DDL, "manifest_digest TEXT CHECK (manifest_digest IS NULL OR length(manifest_digest) = 64),",
    "manifest_digest TEXT CHECK (manifest_digest IS NULL OR (length(manifest_digest) = 64\n"
    "                              AND manifest_digest NOT GLOB '*[^0-9a-f]*')),")
rep(DDL, "run_id       TEXT    CHECK (run_id IS NULL OR (run_id GLOB 'run3:[0-9a-f]*'\n                              AND length(run_id) = 69)),",
    "run_id       TEXT    CHECK (run_id IS NULL OR (run_id GLOB 'run3:*'\n                              AND length(run_id) = 69\n"
    "                              AND substr(run_id, 6) NOT GLOB '*[^0-9a-f]*')),")
rep(DDL, "body_sha256  TEXT    NOT NULL CHECK (length(body_sha256) = 64),\n  prev_sha256  TEXT    NOT NULL CHECK (length(prev_sha256) = 64),",
    "body_sha256  TEXT    NOT NULL CHECK (length(body_sha256) = 64\n                              AND body_sha256 NOT GLOB '*[^0-9a-f]*'),\n"
    "  prev_sha256  TEXT    NOT NULL CHECK (length(prev_sha256) = 64\n                              AND prev_sha256 NOT GLOB '*[^0-9a-f]*'),")
rep(DDL, "CREATE TRIGGER gj3_append_laws BEFORE INSERT ON grant_journal_v3\n  BEGIN\n",
    "CREATE TRIGGER gj3_append_laws BEFORE INSERT ON grant_journal_v3\n  BEGIN\n"
    "    SELECT CASE WHEN NOT EXISTS (SELECT 1 FROM carrier_format WHERE singleton = 1)\n"
    "      THEN RAISE(ABORT, 'carrierFormat 3 is not published; no append precedes the format row') END;\n")

# ------------------------------------------------------------------ A37-01: private attempt custody DDL
ac_before = strict(texts[AC])
rep(AC, "store_generation_digest GLOB '[0-9a-f]*')", "store_generation_digest NOT GLOB '*[^0-9a-f]*')")
rep(AC, "execution_id GLOB 'exec1_[0-9a-f]*' AND length(execution_id) = 38)",
    "execution_id GLOB 'exec1_*' AND length(execution_id) = 38 AND substr(execution_id, 7) NOT GLOB '*[^0-9a-f]*')")
rep(AC, "operation_ref GLOB 'op-[0-9a-f]*' AND length(operation_ref) = 35)",
    "operation_ref GLOB 'op-*' AND length(operation_ref) = 35 AND substr(operation_ref, 4) NOT GLOB '*[^0-9a-f]*')")
AC_NOTE = {
    "standing": "Source37 owner correction (review advisory A37-01). The planned private DDL is corrected in place; no attempt_custody table was ever created from the earlier bytes, which remain retained review evidence only.",
    "law": "store_generation_digest, execution_id and operation_ref are lowercase hex over the whole hex part with an exact length, matching this record's own patterns ^[0-9a-f]{64}, ^exec1_[0-9a-f]{32} and ^op-[0-9a-f]{32}. The earlier GLOB '[0-9a-f]*' forms checked only the first character after a prefix.",
    "authority": "The ledger's record admission remains the owner of the closed record; the DDL is defence in depth that now matches the grammar exactly. No member, phase, outcome, key or join changes."
}
anchor = '  "ddlStanding": '
i = texts[AC].index(anchor)
j = texts[AC].index('\n', i)
if texts[AC].count(anchor) != 1 or not texts[AC][j - 1] == ',':
    raise SystemExit('attempt custody ddlStanding anchor')
texts[AC] = texts[AC][:j + 1] + '  "ddlGrammarCorrection": ' + json.dumps(AC_NOTE, ensure_ascii=False) + ',\n' + texts[AC][j + 1:]
ac_after = strict(texts[AC])
ac_expect = copy.deepcopy(ac_before)
ac_expect['proposedPrivateDDL'] = ac_after['proposedPrivateDDL']
assert set(ac_after) - set(ac_before) == {'ddlGrammarCorrection'}
assert {k: v for k, v in ac_after.items() if k != 'ddlGrammarCorrection'} == ac_expect

# ------------------------------------------------------------------ dispatch JSON (structural when byte round-trip holds)
disp = strict(texts[DISP])
round_trip = (json.dumps(disp, indent=2, ensure_ascii=False) + '\n') == texts[DISP]
d = copy.deepcopy(disp)
order = d['openDispatch']['order']
assert order[4]['step'] == 5
order[4]['then'] += (' Before any resume the incomplete footprint must hold no grant_journal_v3 row: a row there is not a lawful '
                     'durable prefix and is MIGRATION.CORRUPT. The corrected DDL refuses every append before publication.')
pdc = d['openDispatch']['postDetectionChecks']
assert pdc[1].startswith('For a published carrierFormat 3 row, carrier_format.project_key_digest')
pdc[1] = ('For a published carrierFormat 3 row, carrier_format.project_key_digest must equal the admitted projectKeyDigest. '
          'A mismatch is a CARRIER PROJECT BINDING MISMATCH, not migration corruption: the carrier\'s own binding names another '
          'project, the same condition the frozen reconcile_witness reports as witness names another carrier. It never borrows '
          'MIGRATION.CORRUPT; its route is publicProjectionByPhase. Before publication do not read absent row fields.')
assert pdc[2].startswith('If an inherited grant_journal table exists')
pdc[2] = ('If an inherited grant_journal table exists and carrierFormat 3 is published, max(grantGeneration) in it must be strictly '
          'less than carrier_format.first_generation and no inherited row may follow a TERMINAL in its generation; otherwise the '
          'published generation boundary is violated (the F51 split-brain custody condition), MIGRATION.CORRUPT at a writer or '
          'maintenance open. An absent inherited table is the lawful fresh-install path and is never queried.')
pdc.insert(3, 'For a published carrierFormat 3 row, min(grantGeneration) in grant_journal_v3, when any row exists, must be at least '
              'carrier_format.first_generation; otherwise MIGRATION.CORRUPT. The corrected DDL already refuses such a row; this check '
              'verifies rows, not only definitions.')
d['readDispatch']['readerLaws'][1] = ('A recovery request whose association names a carrierFormat 1 or 2 generation returns '
                                      'unknown-carrier-incompatible, never not-committed; its route is publicProjectionByPhase.readOnlyRecovery.')
steps = d['migration']['steps']
assert steps[2].startswith('Insert the single carrier_format row')
steps[2] += (' Publication runs in one transaction that first verifies the seven definitions, that grant_journal_v3 holds no row '
             'and that a surviving witness names the admitted projectKeyDigest; the DDL couples first_generation to migrated_from.')
d['migration']['recoveryByPrefix']['AB'] = (
    'validate the existing object definitions against the selected creation path, require grant_journal_v3 to hold no row and a '
    'surviving witness to name the admitted projectKeyDigest, then resume at C by publishing in one transaction that re-verifies '
    'emptiness; invalid definitions or any grant_journal_v3 row is MIGRATION.CORRUPT, a witness naming another project is a carrier '
    'project binding mismatch, and nothing is published in either case')
d['migration']['splitBrainLimit'] += (' Its route is MIGRATION.CORRUPT at a writer or maintenance open and the quarantine-condition '
                                      'row at read-only recovery (publicProjectionByPhase).')
LC = {'class': 'operational-failed', 'exit': 4, 'errorCode': 'LEDGER.CORRUPT', 'faultCause': 'ledger-corrupt'}
MIGRATION_ROW = '`MIGRATION.CORRUPT` (incl. a registry differing'
BINDING_ROW = 'writer or maintenance carrier open, or maintenance format publication'
d['ddlGrammar'] = {
    'standing': 'Source37 owner correction (review advisory A37-01).',
    'law': ("Every hex-bearing column of the carrierFormat 3 DDL and of the private attempt_custody DDL is lowercase hex over its "
            "whole hex part with an exact length: a prefix GLOB where a prefix exists, then substr(column, prefix + 1) NOT GLOB "
            "'*[^0-9a-f]*'. SQLite GLOB is case-sensitive, so an uppercase or non-hex character anywhere refuses."),
    'carrierFormat3Columns': ['carrier_format.project_key_digest', 'carrier_format.migration_op_ref', 'grant_journal_v3.operation_ref',
                              'grant_journal_v3.run_id', 'grant_journal_v3.manifest_digest', 'grant_journal_v3.body_sha256',
                              'grant_journal_v3.prev_sha256'],
    'attemptCustodyColumns': ['store_generation_digest', 'execution_id', 'operation_ref'],
    'grammarSources': ['operation_ref: op- plus 32 lowercase hex (carrier-format.v3.md section 5)',
                       'run_id: security-lifecycle.schemas.v1.json JournalRecord runId ^run3:[0-9a-f]{64}',
                       'manifest_digest: security-schemas.v2 journal-record.schema.json manifestDigest ^[0-9a-f]{64}$',
                       'project_key_digest: security_unit_lib_v8 witness projectKeyDigest [0-9a-f]{64}',
                       'body_sha256 and prev_sha256: lowercase-hex SHA-256 text; security_unit_lib_v8 journal tail digest [0-9a-f]{64}',
                       'attempt_custody: attempt-custody.schema.v1.json storeGenerationDigest, executionId and operationRef patterns'],
    'authority': ('Host record admission still validates the closed record bodies. The DDL is defence in depth that now enforces the '
                  'stated grammar exactly rather than only its first character.'),
    'historicalScope': ('carrierFormat 1 and 2 bytes are frozen and unchanged, and their GLOB checks still inspect only the first '
                        'character after a prefix. That is a disclosed historical limit, not repaired: historical rows are read as '
                        'history under recordSchema-1 semantics, are never re-admitted through the schema-3 gate and can never satisfy '
                        'a schema-3 SEAL join (F46), so a malformed historical tail confers no commitment. The earlier PROPOSED '
                        'carrierFormat 3 and attempt_custody bytes were never instantiated; the open dispatch binds the corrected '
                        'definitions only.')}
d['publicationLaw'] = {
    'standing': 'Source37 owner correction (review advisory A37-02).',
    'ddl': ('gj3_append_laws refuses every append while no carrier_format row exists, so an {A, B} footprint cannot acquire a row '
            'that a later publication would contradict. A carrier_format CHECK couples first_generation to migrated_from: exactly '
            '1 on the fresh path and at least 2 when migrated.'),
    'actC': ('Publication, on the fresh path or resuming {A, B}, runs under the held fence and EXCLUSIVE lease in one transaction '
             'that first verifies the seven definitions, that grant_journal_v3 holds no row and that a surviving witness names the '
             'admitted projectKeyDigest, then recomputes first_generation and inserts the row. A failed precondition publishes '
             'nothing: a definition or row failure is MIGRATION.CORRUPT and a witness naming another project is a carrier project '
             'binding mismatch.'),
    'published': ('After publication the row-level post-detection checks verify rows, not only definitions: no inherited generation '
                  'at or above first_generation, no inherited row after a TERMINAL and no grant_journal_v3 row below first_generation.'),
    'noNewObject': 'The law lives in the existing trigger and table definitions; the seven object names are unchanged.'}
d['publicProjectionByPhase'] = {
    'standing': ('Source37 owner correction (review advisories A37-03 and A37-04). Exact existing D9 v1.14 class, exit, errorCode and '
                 'faultCause for every carrier open, publication and read-only recovery observation. Nothing is minted: no class, '
                 'code, exit, faultCause or DomainDetailCode. domainDetail null means the member is omitted. Prose owner: '
                 'carrier-format.v3.md section 8.1. Security rows: security-and-lifecycle.md S12. Read-only rows: '
                 'commit-recovery-readonly.v3.md section 1.'),
    'phaseLaws': [
        ('The phase decides only which existing route applies. A writer or maintenance open refuses: it appends nothing, publishes '
         'nothing and writes no quarantine marker, because carrier_quarantine.reason is the unchanged inherited enum. Every open '
         're-detects from the bytes it reads; a cached verdict, first_generation, projectKeyDigest or earlier successful open is '
         'never reused.'),
        ('Read-only recovery writes nothing, never uses MIGRATION.CORRUPT, and reports the quarantine-condition row only with the '
         'Step 4 stable observations of commit-recovery-readonly.v3.md; otherwise it reports unavailable-busy.'),
        ('No route confirms, negates or settles an attempt, merges split-brain rows, rewrites the immutable format row or grants any '
         'authority.')],
    'writerOrMaintenanceOpen': {
        'migration-footprint-corrupt': dict(LC, domainDetail='MIGRATION.CORRUPT', securityRefusal='MIGRATION.CORRUPT', s12Row=MIGRATION_ROW,
            observations=['some but not all seven carrierFormat 3 object names', 'all seven names with an invalid definition',
                          'a grant_journal_v3 row while no format row is published', 'a published grant_journal_v3 row below first_generation']),
        'split-brain-custody-condition': dict(LC, domainDetail='MIGRATION.CORRUPT', securityRefusal='MIGRATION.CORRUPT', s12Row=MIGRATION_ROW,
            observations=['an inherited grant_journal generation at or above the published first_generation (F51)',
                          'an inherited row after a TERMINAL in its generation']),
        'carrier-project-binding-mismatch': dict(LC, domainDetail=None, securityRefusal=None, s12Row=BINDING_ROW,
            observations=['published carrier_format.project_key_digest differs from the admitted projectKeyDigest',
                          'a surviving witness names another project (frozen reconcile_witness: witness names another carrier)'])},
    'maintenanceActCPublication': {
        'migration-footprint-corrupt': dict(LC, domainDetail='MIGRATION.CORRUPT', securityRefusal='MIGRATION.CORRUPT', s12Row=MIGRATION_ROW,
            publishes=False, observations=['a grant_journal_v3 row before publication', 'a partial object set or an invalid definition']),
        'carrier-project-binding-mismatch': dict(LC, domainDetail=None, securityRefusal=None, s12Row=BINDING_ROW,
            publishes=False, observations=['a surviving witness names another project'])},
    'readOnlyRecovery': {
        'binding-unusable': {'class': 'request-rejected', 'exit': 2, 'errorCode': 'EXTENSION.ADMISSION_REJECTED', 'faultCause': None,
                             'domainDetail': 'RECOVERY.REFUSED', 'securityRefusal': 'RECOVERY.REFUSED',
                             's12Row': 'read-only recovery: the requested binding',
                             'observations': ['the association storeGenerationDigest, namespaceId or journalCarrierDigest differs from the admitted binding']},
        'unknown-quarantine-condition': dict(LC, domainDetail=None, securityRefusal=None,
            s12Row='read-only recovery: stably observed carrier quarantine condition', requiresStableObservations=True,
            otherwise='unavailable-busy',
            observations=["with the association naming the admitted carrier, the carrier's own published row or witness names another project",
                          'a migration footprint that is not a lawful durable prefix', 'the F51 split-brain condition',
                          'the inherited quarantine conditions uncertainTailLoss, witnesslessRestore and witnessMalformed']),
        'unknown-carrier-incompatible': {'class': 'operational-failed', 'exit': 4, 'errorCode': 'HOST.IO_FAILURE', 'faultCause': 'host-io',
                                         'domainDetail': None, 'securityRefusal': None,
                                         's12Row': 'read-only recovery: the association names a carrierFormat 1 or 2 generation',
                                         'observations': ['the association grantGeneration is below the first_generation read in the same journal snapshot (F46)']},
        'unavailable-busy': {'class': 'operational-failed', 'exit': 4, 'errorCode': 'LEDGER.BUSY_TIMEOUT', 'faultCause': 'ledger-busy',
                             'domainDetail': 'PROJECT.BUSY', 'securityRefusal': None,
                             's12Row': 'read-only recovery: requested attempt still `admitted` **with no receipt**',
                             'observations': ['a lawful {A} or {A, B} migration prefix (carrier-migration.v1.md section 4)',
                                              'an unstable observation where a quarantine condition would otherwise be reported']}},
    'readOnlyStandingOfDispatchResult': {'binding-unusable': 'binding-unusable', 'carrier-project-binding-mismatch': 'unknown-quarantine-condition',
                                         'migration-footprint-corrupt': 'unknown-quarantine-condition',
                                         'split-brain-custody-condition': 'unknown-quarantine-condition',
                                         'unknown-carrier-incompatible': 'unknown-carrier-incompatible',
                                         'incomplete-footprint': 'unavailable-busy'}}
if round_trip:
    texts[DISP] = json.dumps(d, indent=2, ensure_ascii=False) + '\n'
else:
    raise SystemExit('dispatch JSON does not round-trip; structural edit would reformat')
assert strict(texts[DISP]) == d

# ------------------------------------------------------------------ carrier-format.v3.md
rep(FMT, "not an OS durability claim. No historical or frozen file is modified by this correction.\n",
    "not an OS durability claim. No historical or frozen file is modified by this correction.\n\n" + STANDING + "\n")
rep(FMT, "- **operation_ref grammar.** `op-` plus 32 lowercase hex, length 35.\n",
    "- **operation_ref grammar.** `op-` plus 32 lowercase hex, length 35, enforced over the **whole** tail\n"
    "  (`substr(operation_ref, 4) NOT GLOB '*[^0-9a-f]*'`). An earlier revision of this DDL, like the frozen\n"
    "  carrierFormat 2 bytes, used `GLOB 'op-[0-9a-f]*'`, which checks only the first character after the\n"
    "  prefix; see §5.1.\n")
rep(FMT, "- **Witness and high-water laws.** Unchanged in substance; see §8 and §10.\n",
    "- **Witness and high-water laws.** Unchanged in substance; see §8 and §10.\n\n"
    "### 5.1 Lowercase-hex grammar and the publication law (source37 owner correction)\n\n"
    "**Grammar (A37-01).** Every hex-bearing carrierFormat 3 column is lowercase hex over its whole hex part\n"
    "with an exact length: `carrier_format.project_key_digest` and `migration_op_ref`, and\n"
    "`grant_journal_v3.operation_ref`, `run_id`, `manifest_digest`, `body_sha256` and `prev_sha256`. The\n"
    "check is a prefix `GLOB` where a prefix exists, then `substr(column, prefix + 1) NOT GLOB '*[^0-9a-f]*'`;\n"
    "SQLite `GLOB` is case-sensitive, so an uppercase or non-hex character anywhere refuses. The private\n"
    "`attempt_custody` DDL applies the same law to `store_generation_digest`, `execution_id` and\n"
    "`operation_ref`. Host record admission still validates the closed record bodies; the DDL is defence in\n"
    "depth that now matches the stated grammar exactly.\n\n"
    "**Historical scope.** carrierFormat 1 and 2 bytes are frozen and unchanged, and their `GLOB` checks still\n"
    "inspect only the first character after a prefix. That weakness is disclosed, not repaired: historical\n"
    "rows are read as history under recordSchema-1 semantics, are never re-admitted through the schema-3 gate\n"
    "and can never satisfy a schema-3 `SEAL` join (§9, F46), so a malformed historical tail confers no\n"
    "commitment. The earlier PROPOSED carrierFormat 3 bytes were never instantiated, and the open dispatch\n"
    "binds only the corrected definitions, so they are never a second admitted definition.\n\n"
    "**Publication law (A37-02).** `gj3_append_laws` refuses every append while no `carrier_format` row\n"
    "exists, so an `{A, B}` footprint cannot acquire a row that a later publication would contradict. A\n"
    "`carrier_format` CHECK couples `first_generation` to `migrated_from`: exactly 1 on the fresh path, at\n"
    "least 2 on the migrated path. Act C verifies, in the same transaction that inserts the row, the seven\n"
    "definitions, that `grant_journal_v3` holds no row and that a surviving witness names the admitted\n"
    "`projectKeyDigest`; any failure publishes nothing. Both laws live inside existing definitions, so the\n"
    "seven object names are unchanged.\n")
rep(FMT, "| superseded-generation trigger | enforces WA-13 generation ordering physically |\n\n"
         "The last two are genuinely new laws. Neither can affect an inherited row: both live only on the\nnew table.",
    "| superseded-generation trigger | enforces WA-13 generation ordering physically |\n"
    "| no append before the format row | an `{A, B}` footprint holds no row that publication could contradict (§5.1) |\n"
    "| `first_generation` coupled to `migrated_from` | the fresh path publishes 1; the migrated path publishes at least 2 (§5.1) |\n"
    "| whole-tail lowercase-hex CHECKs | the stated grammar is enforced, not only its first character (§5.1) |\n\n"
    "The last five are genuinely new laws. None can affect an inherited row: all live only on the new\nobjects.")
rep(FMT, "       row absent   -> INCOMPLETE FOOTPRINT: inherited format; a fresh admitted\n                       maintenance attempt resumes at act C\n",
    "       row absent   -> if grant_journal_v3 holds any row -> MIGRATION.CORRUPT\n"
    "                       else INCOMPLETE FOOTPRINT: inherited format; a fresh admitted\n"
    "                       maintenance attempt resumes at act C\n")
rep(FMT, "2. `carrier_format.project_key_digest` must equal the carrier's own `projectKeyDigest` derived from\n"
         "   the admitted project key; otherwise `MIGRATION.CORRUPT`.\n"
         "3. `max(grantGeneration)` in `grant_journal` must be strictly less than\n"
         "   `carrier_format.first_generation`; otherwise `MIGRATION.CORRUPT`.\n",
    "2. `carrier_format.project_key_digest` must equal the carrier's own `projectKeyDigest` derived from\n"
    "   the admitted project key. A mismatch is a **carrier project binding mismatch**, not migration\n"
    "   corruption: nothing in the migration footprint is inconsistent, but the carrier's own binding names\n"
    "   another project, the condition the frozen `reconcile_witness` reports as *witness names another\n"
    "   carrier*. It never borrows `MIGRATION.CORRUPT`; its route is §8.1.\n"
    "3. `max(grantGeneration)` in `grant_journal` must be strictly less than\n"
    "   `carrier_format.first_generation`, and no inherited row may follow a `TERMINAL` in its generation;\n"
    "   otherwise the published generation boundary is violated (the F51 split-brain custody condition)\n"
    "   and the carrier is `MIGRATION.CORRUPT` at a writer or maintenance open.\n"
    "3a. `min(grantGeneration)` in `grant_journal_v3`, when any row exists, must be at least\n"
    "   `carrier_format.first_generation`; otherwise `MIGRATION.CORRUPT`. The corrected DDL already refuses\n"
    "   such a row; this check verifies rows, not only definitions.\n")
rep(FMT, "## 9. Read dispatch\n",
    "### 8.1 Phase-specific public routes (source37 owner correction)\n\n"
    "Every route below is an existing D9 v1.14 class, exit, `errorCode` and `faultCause`; nothing is minted.\n"
    "The phase decides which existing route applies, never a new class. Machine-readable:\n"
    "`carrier-dispatch.v3.json#/publicProjectionByPhase`. Security owner rows: S12.\n\n"
    "| Phase | Observation | Internal standing | class / exit / errorCode / faultCause | `domainDetail` |\n"
    "|---|---|---|---|---|\n"
    "| writer or maintenance open | partial object set; all names with an invalid definition; a `grant_journal_v3` row with no published row; a published boundary violated (checks 3, 3a) | migration footprint not a lawful prefix | operational-failed / 4 / `LEDGER.CORRUPT` / `ledger-corrupt` | `MIGRATION.CORRUPT` |\n"
    "| writer or maintenance open | F51: inherited generation at or above `first_generation`, or an inherited row after `TERMINAL` | `split-brain-custody-condition` | operational-failed / 4 / `LEDGER.CORRUPT` / `ledger-corrupt` | `MIGRATION.CORRUPT` |\n"
    "| writer or maintenance open | published `project_key_digest` (check 2) or a surviving witness names another project | carrier project binding mismatch | operational-failed / 4 / `LEDGER.CORRUPT` / `ledger-corrupt` | omitted |\n"
    "| maintenance act C (fresh or `{A, B}` resume) | a `grant_journal_v3` row, a partial set or invalid definition; or a witness naming another project | as the rows above | as above; **nothing is published** | as above |\n"
    "| read-only recovery | the association's `storeGenerationDigest`, `namespaceId` or `journalCarrierDigest` differs from the admitted binding | `binding-unusable` | request-rejected / 2 / `EXTENSION.ADMISSION_REJECTED` / — | `RECOVERY.REFUSED`, typed subject |\n"
    "| read-only recovery | association names the admitted carrier, but the carrier's own row or witness names another project; an unlawful footprint; or F51 | `unknown-quarantine-condition` | operational-failed / 4 / `LEDGER.CORRUPT` / `ledger-corrupt` | omitted |\n"
    "| read-only recovery | F46: association names a generation below the `first_generation` read in the same journal snapshot | `unknown-carrier-incompatible` | operational-failed / 4 / `HOST.IO_FAILURE` / `host-io` | omitted |\n"
    "| read-only recovery | lawful `{A}` or `{A, B}` prefix (`carrier-migration.v1.md` §4), or an unstable observation | `unavailable-busy` | operational-failed / 4 / `LEDGER.BUSY_TIMEOUT` / `ledger-busy` | `PROJECT.BUSY` |\n\n"
    "**Why a digest mismatch is not migration corruption.** A partial object set, an invalid definition, a\n"
    "row before publication and a violated generation boundary are failures of the migration footprint\n"
    "itself, so `MIGRATION.CORRUPT` names their remedy. A project digest mismatch leaves that footprint\n"
    "intact: the carrier at this namespace carries another project's binding. The frozen v8 witness law\n"
    "already treats the same fact as a carrier quarantine, and S12 keeps journal-carrier quarantine free of\n"
    "`MIGRATION.CORRUPT` so that one code never carries two remedies. On read-only recovery the\n"
    "association's own carrier naming decides first: an association that names another carrier is the\n"
    "existing `binding-unusable` refusal of the recovery request.\n\n"
    "**Why F46 is `HOST.IO_FAILURE`.** An association is written only with a committed carrierFormat 3\n"
    "`SEAL`, so one naming a historical generation contradicts two retained owners. That is the\n"
    "`unknown-custody` family (`HOST.IO_FAILURE`, `host-io`): not a caller defect (request-rejected), not a\n"
    "stably observed quarantine (`LEDGER.CORRUPT`) and not contention. It never becomes not-committed or a\n"
    "confirmation.\n\n"
    "**Interrupted state and stale custody.** Each phase re-evaluates every predicate from the bytes it\n"
    "reads at that open or in that journal snapshot: a cached verdict, `first_generation`,\n"
    "`projectKeyDigest` or earlier successful open is never reused. A writer or maintenance refusal appends\n"
    "nothing, publishes nothing and writes no marker, because `carrier_quarantine.reason` keeps its inherited\n"
    "enum; the next open detects the same condition again. Read-only recovery writes nothing, uses\n"
    "`MIGRATION.CORRUPT` on no path, and reports the quarantine-condition row only with its Step 4 stable\n"
    "observations, otherwise `unavailable-busy`. A lawful `{A}` or `{A, B}` prefix stays a resumable\n"
    "interrupted migration, never a corruption diagnosis. No route confirms, negates or settles an attempt,\n"
    "merges split-brain rows, rewrites the immutable format row or grants authority.\n\n"
    "## 9. Read dispatch\n")
rep(FMT, "  `unknown-carrier-incompatible` (F31/F46), never `not-committed`.\n",
    "  `unknown-carrier-incompatible` (F31/F46), never `not-committed`; its public route is §8.1.\n")
rep(FMT, "  valid history, and is never merged into the current generation sequence. The mitigation is the\n",
    "  valid history, and is never merged into the current generation sequence (public route §8.1). The mitigation is the\n")

# ------------------------------------------------------------------ carrier-migration.v1.md
rep(MIG, "Authored against frozen Source25\n`fa8cdc796c4dbab514c8b8a91a593b740e3f8e69d19574f4be11c6e00c3a536d`.\n",
    "Authored against frozen Source25\n`fa8cdc796c4dbab514c8b8a91a593b740e3f8e69d19574f4be11c6e00c3a536d`.\n\n" + STANDING + "\n")
rep(MIG, "| **C** | the single `carrier_format` row inserted, publishing `first_generation` and `chain_law` | single INSERT, immutable by trigger |",
    "| **C** | the single `carrier_format` row inserted, publishing `first_generation` and `chain_law` | single INSERT, immutable by trigger, in one transaction that first verifies the definitions, that `grant_journal_v3` holds no row and that a surviving witness names the admitted `projectKeyDigest` |")
rep(MIG, "under the same held `EXCLUSIVE` lease. It is never fixed at planning time, so a benign\ninterleaving (§5) cannot make it stale.\n",
    "under the same held `EXCLUSIVE` lease. It is never fixed at planning time, so a benign\ninterleaving (§5) cannot make it stale.\n\n"
    "**Publication law at C (source37 owner correction, A37-02).** The corrected DDL refuses every\n"
    "`grant_journal_v3` append while no format row exists, and couples `first_generation` to\n"
    "`migrated_from` (exactly 1 fresh, at least 2 migrated). Act C, fresh or resuming `{A, B}`, therefore\n"
    "verifies in the transaction that publishes the row: the seven definitions, an empty `grant_journal_v3`,\n"
    "and a surviving witness naming the admitted `projectKeyDigest`. A row or definition failure is\n"
    "`MIGRATION.CORRUPT`; a witness naming another project is a carrier project binding mismatch; either\n"
    "way nothing is published and no marker is written. Values are read under the held lease at C, never\n"
    "carried from the stopped attempt. Routes: `carrier-format.v3.md` §8.1.\n")
rep(MIG, "| **{A, B}** | new objects exist, `carrier_format` has **no row** | still carrierFormat 1 or 2 by detection | resume at **C**, after verifying the existing object definitions byte-equal the selected DDL; otherwise `MIGRATION.CORRUPT` |",
    "| **{A, B}** | new objects exist, `carrier_format` has **no row** | still carrierFormat 1 or 2 by detection | resume at **C**, after verifying the existing object definitions byte-equal the selected DDL, that `grant_journal_v3` holds no row and that a surviving witness names the admitted `projectKeyDigest`; otherwise `MIGRATION.CORRUPT` (definitions or rows) or a carrier project binding mismatch (witness), and nothing is published |")
rep(MIG, "  as valid history, and never merges it into the current generation sequence.\n",
    "  as valid history, and never merges it into the current generation sequence. Its public route is\n"
    "  `carrier-format.v3.md` §8.1.\n")

# ------------------------------------------------------------------ commit-recovery-readonly.v3.md
rep(RO, "frozen Source25 `fa8cdc796c4dbab514c8b8a91a593b740e3f8e69d19574f4be11c6e00c3a536d`.\n",
    "frozen Source25 `fa8cdc796c4dbab514c8b8a91a593b740e3f8e69d19574f4be11c6e00c3a536d`.\n\n" + STANDING + "\n")
rep(RO, "| `binding-unusable` | `request-rejected` | `EXTENSION.ADMISSION_REJECTED` | — | `RECOVERY.REFUSED` with typed subject |\n",
    "| `binding-unusable` | `request-rejected` | `EXTENSION.ADMISSION_REJECTED` | — | `RECOVERY.REFUSED` with typed subject |\n"
    "| `unknown-carrier-incompatible` | `operational-failed` | `HOST.IO_FAILURE` | `host-io` | omitted |\n")
rep(RO, "A registered detail is used only where one already fits the event exactly:",
    "**Carrier binding, footprint and generation observations (source37 owner correction).** The\n"
    "association's own carrier naming is checked first: an association whose `journalCarrierDigest`,\n"
    "`storeGenerationDigest` or `namespaceId` differs from the admitted binding is `binding-unusable`. With\n"
    "the association naming the admitted carrier, a carrier whose own published `project_key_digest` or\n"
    "witness names another project, a migration footprint that is not a lawful durable prefix, and the F51\n"
    "split-brain condition are `unknown-quarantine-condition`, subject to Step 4 like every quarantine\n"
    "report and otherwise `unavailable-busy`. An association naming a generation below the published\n"
    "`first_generation` is `unknown-carrier-incompatible` (F46): an association is written only with a\n"
    "committed carrierFormat 3 `SEAL`, so this contradicts two retained owners and joins the `unknown-custody`\n"
    "family. A lawful `{A}` or `{A, B}` prefix is `unavailable-busy`. `MIGRATION.CORRUPT` is used on none of\n"
    "these read-only paths, and none confirms, negates or settles an attempt. Exact phase table:\n"
    "`design-corrections/security/carrier-format.v3.md` §8.1.\n\n"
    "A registered detail is used only where one already fits the event exactly:")
rep(RO, "Store-binding or namespace mismatch in the association → `binding-unusable` (F27).",
    "Store-binding, namespace or carrier mismatch in the association — its `storeGenerationDigest`,\n"
    "`namespaceId` or `journalCarrierDigest` differs from the admitted binding → `binding-unusable` (F27).")
rep(RO, "**The SEAL join at `k`, all members required.**",
    "**Carrier format, binding and generation, inside each journal snapshot.** Before the SEAL join the\n"
    "reader applies the carrier open dispatch to the bytes of that snapshot only, never to a cached\n"
    "result: the object names and definitions, the format row, `project_key_digest` against the admitted\n"
    "`projectKeyDigest`, the published generation boundary, and `A.grantGeneration` against\n"
    "`first_generation`. Their conclusions are the carrier rows of §1; a quarantine-class conclusion also\n"
    "requires Step 4.\n\n"
    "**The SEAL join at `k`, all members required.**")

# ------------------------------------------------------------------ security-and-lifecycle.md S12
rep(S12, "| `MIGRATION.CORRUPT` (incl. a registry differing from the frozen transition journal, S9.2) | operational-failed / 4 / `LEDGER.CORRUPT` |\n",
    "| `MIGRATION.CORRUPT` (incl. a registry differing from the frozen transition journal, S9.2; and, at a writer or maintenance carrier open, a carrierFormat 3 migration footprint that is not a lawful durable prefix (partial object set, invalid definitions, `grant_journal_v3` rows before format publication) or a violated published generation boundary, including the F51 split-brain custody condition, carrier-format.v3 §8.1) | operational-failed / 4 / `LEDGER.CORRUPT` |\n"
    "| writer or maintenance carrier open, or maintenance format publication: the published `carrier_format.project_key_digest` or a surviving witness names a project key other than the admitted one (carrier project binding mismatch; never `MIGRATION.CORRUPT`; nothing is appended or published) | operational-failed / 4 / `LEDGER.CORRUPT`, `faultCause` `ledger-corrupt`, **`domainDetail` omitted** |\n")
rep(S12, "| read-only recovery: stably observed carrier quarantine condition (`uncertainTailLoss`, `witnesslessRestore`, `witnessMalformed`) | operational-failed / 4 / `LEDGER.CORRUPT`, `faultCause` `ledger-corrupt`, **`domainDetail` omitted** |\n",
    "| read-only recovery: stably observed carrier quarantine condition (`uncertainTailLoss`, `witnesslessRestore`, `witnessMalformed`; and, with the association naming the admitted carrier, a carrier whose own published row or witness names another project, a migration footprint that is not a lawful durable prefix, or the F51 split-brain condition) | operational-failed / 4 / `LEDGER.CORRUPT`, `faultCause` `ledger-corrupt`, **`domainDetail` omitted** |\n")
rep(S12, "| read-only recovery: unreadable ledger or carrier, unobserved attempt, or an anchor that does not reach the requested sequence | operational-failed / 4 / `HOST.IO_FAILURE`, `faultCause` `host-io` |\n"
         "| read-only recovery: requested binding names a foreign carrier or a swapped store/namespace | request-rejected / 2 / `EXTENSION.ADMISSION_REJECTED` (detail `RECOVERY.REFUSED`, typed subject) |\n",
    "| read-only recovery: unreadable ledger or carrier, unobserved attempt, or an anchor that does not reach the requested sequence | operational-failed / 4 / `HOST.IO_FAILURE`, `faultCause` `host-io` |\n"
    "| read-only recovery: the association names a carrierFormat 1 or 2 generation (below the published `first_generation`), where no schema-3 `SEAL` can exist (`unknown-carrier-incompatible`, F46) | operational-failed / 4 / `HOST.IO_FAILURE`, `faultCause` `host-io`, `domainDetail` omitted; never not-committed and never a confirmation |\n"
    "| read-only recovery: the requested binding (the association's `storeGenerationDigest`, `namespaceId` or `journalCarrierDigest`) names a foreign carrier or a swapped store/namespace | request-rejected / 2 / `EXTENSION.ADMISSION_REJECTED` (detail `RECOVERY.REFUSED`, typed subject) |\n")
rep(S12, "that code is the store transition’s detail, and borrowing it for ordinary journal corruption would put two remedies behind one code.",
    "that code is the detail of a store transition footprint and of a carrierFormat 3 migration footprint at a writer or maintenance open, and borrowing it for ordinary journal corruption, a carrier project binding mismatch or any read-only carrier observation would put two remedies behind one code.")
rep(S12, "\nThe common scope stage additionally refuses PROJECT.SCOPE_LIMIT",
    "\n**Phase-specific carrier routes (source37 owner correction).** One carrier observation can reach a writer or maintenance open and read-only recovery; the phase selects one of the rows above and never a new class, code or exit. A writer or maintenance refusal appends nothing, publishes nothing and writes no quarantine marker (`carrier_quarantine.reason` keeps its inherited enum), and every open re-detects from the bytes it reads rather than reusing a cached verdict, `first_generation` or `projectKeyDigest`. Read-only recovery writes nothing, reports a quarantine row only with its stable observations and otherwise the busy row, and uses `MIGRATION.CORRUPT` on no path. A lawful interrupted carrier migration prefix remains resumable and is never a corruption diagnosis. No route confirms, negates or settles an attempt, merges split-brain rows or grants authority. Exact table: `design-corrections/security/carrier-format.v3.md` §8.1.\n"
    "\nThe common scope stage additionally refuses PROJECT.SCOPE_LIMIT")

# ------------------------------------------------------------------ store-instance-lineage.v1.json (A37-07 wording)
lin_before = strict(texts[LIN])
NOTE = ('Current standing: the F00-F37 references in this file record the case inventory at this companion\'s authoring time and are '
        'not relabelled. The current commit-recovery-plan.v1.json holds F00-F53, because the separate carrier correction appended '
        'F38-F53. This companion still proposes no failure case and changes no generated section.')
k1 = '    "existingCaseCoverage": '
i = texts[LIN].index(k1)
j = texts[LIN].index('\n', i)
if texts[LIN].count(k1) != 1 or texts[LIN][j - 1] != ',':
    raise SystemExit('lineage existingCaseCoverage anchor')
texts[LIN] = texts[LIN][:j + 1] + '    "currentStandingNote": ' + json.dumps(NOTE, ensure_ascii=False) + ',\n' + texts[LIN][j + 1:]
k2 = '    "This correction does not touch the closed CommitRecoveryAssociationV1 schema, the F00-F37 case inventory'
i = texts[LIN].index(k2)
j = texts[LIN].index('\n', i)
if texts[LIN].count(k2) != 1 or texts[LIN][j - 1] != ',':
    raise SystemExit('lineage limits anchor')
texts[LIN] = texts[LIN][:j + 1] + '    ' + json.dumps(NOTE, ensure_ascii=False) + ',\n' + texts[LIN][j + 1:]
lin_after = strict(texts[LIN])
exp = copy.deepcopy(lin_before)
ajr = {}
for key, value in exp['associationJoinRules'].items():
    ajr[key] = value
    if key == 'existingCaseCoverage':
        ajr['currentStandingNote'] = NOTE
exp['associationJoinRules'] = ajr
idx = next(n for n, s in enumerate(exp['limits']) if s.startswith('This correction does not touch the closed CommitRecoveryAssociationV1'))
exp['limits'].insert(idx + 1, NOTE)
assert lin_after == exp

# ------------------------------------------------------------------ check-carrier-v3.py controls
rep(CHK, "    c.execute('INSERT INTO carrier_format VALUES (1,3,?,?,1,NULL,NULL)', ('e' * 64, first))\n",
    "    # The fresh path publishes first_generation 1; a higher first generation is a migrated row with its\n"
    "    # migration op ref, as the corrected carrier_format CHECK requires.\n"
    "    c.execute('INSERT INTO carrier_format VALUES (1,3,?,?,1,?,?)',\n"
    "              ('e' * 64, first, None if first == 1 else 2, None if first == 1 else 'op-' + 'f' * 32))\n")
NEW_CHECKS = (BASE / 'probes' / 'check_carrier_v3_additions.py.txt').read_text(encoding='utf-8')
rep(CHK, "rep = {'control': 'c4-check-carrier-v3',", NEW_CHECKS + "\nrep = {'control': 'c4-check-carrier-v3',")

# ------------------------------------------------------------------ write, diff, hashes
diff, files = [], []
for rel in CHANGED:
    (ED / rel).write_text(texts[rel], encoding='utf-8')
    a, b = (BL / rel).read_bytes(), (ED / rel).read_bytes()
    files.append({'path': rel, 'beforeSha256': sha(a), 'afterSha256': sha(b), 'beforeBytes': len(a), 'afterBytes': len(b)})
    diff += difflib.unified_diff(a.decode().splitlines(keepends=True), b.decode().splitlines(keepends=True),
                                 fromfile='a/' + rel, tofile='b/' + rel, n=3)
patch = ''.join(diff).encode()
(BASE / 'proposed-edits.diff').write_bytes(patch)
record = {'files': files, 'diffSha256': sha(patch), 'diffLines': patch.count(b'\n'), 'dispatchStructuralRoundTrip': round_trip}
(BASE / 'receipts' / 'p02-apply-edits.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps(record, indent=2))
