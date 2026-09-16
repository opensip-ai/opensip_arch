-- OpenSIP product grant-journal physical carrier, carrierFormat 3 (PROPOSED).
-- Standing: PROPOSED-NOT-SELF-ACCEPTED. Design/reference only: no acceptance, no readiness,
-- no application and no implementation authorization.
-- Additive successor to the frozen historical carriers. Creates new objects only.
-- It never alters, rewrites, relabels or reinterprets a carrierFormat 1 or 2 row,
-- and it disables no inherited constraint or trigger.
--
-- Three independent axes, never conflated:
--   carrierFormat  1 | 2 | 3   physical table/trigger shape of this SQLite carrier
--   recordSchema   1 | 2 | 3   logical journal record body format (security-owned)
--   stateSchema    1 | 2       logical store state format (S9, StoreGenerationBindingV1)
--
-- carrierFormat 1: security-completion.v1 section 5.4 embedded DDL.
-- carrierFormat 2: security-schemas.v2/grant-journal.sql (adds the uint53 seq CHECK,
--                  operation_ref format, contiguity, TERMINAL closure, reserved slot).
-- carrierFormat 3: this file.
--
-- Source37 owner correction (review advisories A37-01 and A37-02). Revised after root reproduced embedded-NUL
-- and ASCII-hex BLOB admissions against the source37 v1 bytes, and again after root showed that the source37 v2
-- byte-length predicate refused lawful rows in UTF-16 databases. These bytes supersede the earlier PROPOSED
-- carrierFormat 3 bytes in place. No product implementation or deployed carrier was created from the earlier
-- bytes. Reference in-memory SQLite instances were created from them by earlier design checks and review
-- probes; those instances and their receipts remain historical evidence. The open dispatch validates the
-- stored definitions byte-exactly, so a carrier created from earlier bytes is refused MIGRATION.CORRUPT
-- rather than read as this definition. carrierFormat 1 and 2 bytes stay frozen.
--
-- Storage class and whole-value grammar. SQLite types values dynamically: TEXT affinity keeps a BLOB,
-- INTEGER affinity keeps a non-integral REAL, and length() and GLOB stop at an embedded NUL. Every column's
-- storage class is enforced either by an explicit typeof() guard (every INTEGER column, every free TEXT
-- column and every hex-bearing column) or by exact enumeration (record_type and platform, whose IN lists
-- hold only TEXT literals and so never equal a BLOB, a number or a NUL-suffixed text). Every hex-bearing
-- column is an exact whole TEXT value: typeof(column) = 'text', length(column) = N, no NUL anywhere
-- (instr(column, char(0)) = 0), the prefix GLOB where a prefix exists, and NOT GLOB '*[^0-9a-f]*' over
-- the hex part. With no NUL, length() and GLOB see the whole value, and the case-sensitive hex class admits
-- only ASCII 0-9 and a-f, so multibyte and malformed characters are refused by the same conjunction. The
-- conjunction evaluates the TEXT value by character and does not depend on the database text encoding
-- (exercised under UTF-8, UTF-16le and UTF-16be); no encoding is required of a carrier. CHECKs see values
-- after column affinity, so an integer supplied as text '5' is stored and checked as integer 5. Host
-- record admission still validates the closed record bodies; these CHECKs are defence in depth.
--
-- Publication: no grant_journal_v3 row may exist before the carrier_format row is published, and
-- first_generation is 1 on the fresh path and at least 2 on the migrated path.

CREATE TABLE carrier_format (
  singleton          INTEGER NOT NULL PRIMARY KEY CHECK (typeof(singleton) = 'integer' AND singleton = 1),
  carrier_format     INTEGER NOT NULL CHECK (typeof(carrier_format) = 'integer' AND carrier_format = 3),
  project_key_digest TEXT    NOT NULL CHECK (typeof(project_key_digest) = 'text'
                               AND length(project_key_digest) = 64
                               AND instr(project_key_digest, char(0)) = 0
                               AND project_key_digest NOT GLOB '*[^0-9a-f]*'),
  first_generation   INTEGER NOT NULL CHECK (typeof(first_generation) = 'integer'
                               AND first_generation >= 1
                               AND first_generation <= 9223372036854775807),
  -- Exactly the selected chain law. Value 2 (a recursive chain) is NOT selected and is NOT
  -- implemented, so the column refuses it rather than advertising an unbuilt alternative.
  -- Widening this CHECK is a reviewed successor act, not a configuration choice.
  chain_law          INTEGER NOT NULL CHECK (typeof(chain_law) = 'integer' AND chain_law = 1),
  migrated_from      INTEGER          CHECK (migrated_from IS NULL
                               OR (typeof(migrated_from) = 'integer' AND migrated_from IN (1, 2))),
  migration_op_ref   TEXT             CHECK (migration_op_ref IS NULL
                               OR (typeof(migration_op_ref) = 'text'
                                   AND length(migration_op_ref) = 35
                                   AND instr(migration_op_ref, char(0)) = 0
                                   AND migration_op_ref GLOB 'op-*'
                                   AND substr(migration_op_ref, 4) NOT GLOB '*[^0-9a-f]*')),
  CHECK ((migrated_from IS NULL AND migration_op_ref IS NULL)
      OR (migrated_from IS NOT NULL AND migration_op_ref IS NOT NULL)),
  -- first_generation at publication: the fresh path publishes generation 1 exactly; the migrated path
  -- publishes (max inherited generation) + 1, at least 2 because act A closed a generation >= 1.
  CHECK ((migrated_from IS NULL AND first_generation = 1)
      OR (migrated_from IS NOT NULL AND first_generation >= 2))
) WITHOUT ROWID;
CREATE TRIGGER cf_no_update BEFORE UPDATE ON carrier_format
  BEGIN SELECT RAISE(ABORT, 'carrier format binding is immutable'); END;
CREATE TRIGGER cf_no_delete BEFORE DELETE ON carrier_format
  BEGIN SELECT RAISE(ABORT, 'carrier format binding is immutable'); END;

CREATE TABLE grant_journal_v3 (
  grantGeneration INTEGER NOT NULL CHECK (typeof(grantGeneration) = 'integer'
                              AND grantGeneration >= 1
                              AND grantGeneration <= 9223372036854775807),
  seq          INTEGER NOT NULL CHECK (typeof(seq) = 'integer'
                              AND seq >= 1 AND seq <= 9007199254740991),
  record_schema INTEGER NOT NULL CHECK (typeof(record_schema) = 'integer' AND record_schema IN (1, 3)),
  record_type  TEXT    NOT NULL CHECK (record_type IN
                 ('GRANT','RA','ICI','RCI','ICO','RCO','REV','CLN','SEAL','TERMINAL')),
  operation_ref TEXT   NOT NULL CHECK (typeof(operation_ref) = 'text'
                              AND length(operation_ref) = 35
                              AND instr(operation_ref, char(0)) = 0
                              AND operation_ref GLOB 'op-*'
                              AND substr(operation_ref, 4) NOT GLOB '*[^0-9a-f]*'),
  request_ref  TEXT    CHECK (request_ref IS NULL OR typeof(request_ref) = 'text'),
  token        TEXT    CHECK (token IS NULL OR typeof(token) = 'text'),
  install_generation_id TEXT CHECK (install_generation_id IS NULL OR typeof(install_generation_id) = 'text'),
  manifest_digest TEXT CHECK (manifest_digest IS NULL OR (typeof(manifest_digest) = 'text'
                              AND length(manifest_digest) = 64
                              AND instr(manifest_digest, char(0)) = 0
                              AND manifest_digest NOT GLOB '*[^0-9a-f]*')),
  platform     TEXT    CHECK (platform IS NULL OR platform IN
                 ('macos-aarch64','macos-x86_64','linux-x86_64-gnu','linux-aarch64-gnu')),
  run_id       TEXT    CHECK (run_id IS NULL OR (typeof(run_id) = 'text'
                              AND length(run_id) = 69
                              AND instr(run_id, char(0)) = 0
                              AND run_id GLOB 'run3:*'
                              AND substr(run_id, 6) NOT GLOB '*[^0-9a-f]*')),
  body         TEXT    NOT NULL CHECK (typeof(body) = 'text'),
  body_sha256  TEXT    NOT NULL CHECK (typeof(body_sha256) = 'text'
                              AND length(body_sha256) = 64
                              AND instr(body_sha256, char(0)) = 0
                              AND body_sha256 NOT GLOB '*[^0-9a-f]*'),
  prev_sha256  TEXT    NOT NULL CHECK (typeof(prev_sha256) = 'text'
                              AND length(prev_sha256) = 64
                              AND instr(prev_sha256, char(0)) = 0
                              AND prev_sha256 NOT GLOB '*[^0-9a-f]*'),
  -- Capacity records are the FROZEN recordSchema-1 TERMINAL body
  -- (security-schemas.v2/journal-record.schema.json). Operational records are the
  -- current closed JournalRecord schema 3. TERMINAL is therefore carried without
  -- ever being admitted as a public schema-3 JournalRecord, and schema 3 is not
  -- widened. Never both, never neither.
  CHECK ((record_schema = 3 AND record_type <> 'TERMINAL')
      OR (record_schema = 1 AND record_type = 'TERMINAL')),
  -- Inherited GRANT completeness, retained verbatim in intent.
  CHECK (record_type <> 'GRANT' OR (install_generation_id IS NOT NULL
      AND manifest_digest IS NOT NULL AND platform IS NOT NULL AND token IS NOT NULL)),
  -- A SEAL names its replayed Run; run3 only. No run[23] alternation.
  CHECK (record_type <> 'SEAL' OR run_id IS NOT NULL),
  -- Capacity records carry no grant-bearing or platform-bearing members.
  CHECK (record_type <> 'TERMINAL' OR (token IS NULL AND install_generation_id IS NULL
      AND manifest_digest IS NULL AND platform IS NULL AND run_id IS NULL
      AND request_ref IS NULL)),
  PRIMARY KEY (grantGeneration, seq)
) WITHOUT ROWID;
CREATE TRIGGER gj3_no_update BEFORE UPDATE ON grant_journal_v3
  BEGIN SELECT RAISE(ABORT, 'grant journal is append-only'); END;
CREATE TRIGGER gj3_no_delete BEFORE DELETE ON grant_journal_v3
  BEGIN SELECT RAISE(ABORT, 'grant journal is append-only'); END;
CREATE TRIGGER gj3_append_laws BEFORE INSERT ON grant_journal_v3
  BEGIN
    SELECT CASE WHEN NOT EXISTS (SELECT 1 FROM carrier_format WHERE singleton = 1)
      THEN RAISE(ABORT, 'carrierFormat 3 is not published; no append precedes the format row') END;
    SELECT CASE WHEN NEW.seq <> (SELECT COALESCE(MAX(seq), 0) + 1 FROM grant_journal_v3
        WHERE grantGeneration = NEW.grantGeneration)
      THEN RAISE(ABORT, 'grant journal sequence must be tail+1') END;
    SELECT CASE WHEN EXISTS (SELECT 1 FROM grant_journal_v3
        WHERE grantGeneration = NEW.grantGeneration AND record_type = 'TERMINAL')
      THEN RAISE(ABORT, 'grant journal carrier is TERMINAL') END;
    SELECT CASE WHEN NEW.seq = 9007199254740991 AND NEW.record_type <> 'TERMINAL'
      THEN RAISE(ABORT, 'grant journal seq 9007199254740991 is the reserved terminal slot; roll the grant generation') END;
    SELECT CASE WHEN NEW.grantGeneration <
        (SELECT first_generation FROM carrier_format WHERE singleton = 1)
      THEN RAISE(ABORT, 'grant generation precedes the carrierFormat 3 first generation') END;
    SELECT CASE WHEN NEW.grantGeneration <
        (SELECT COALESCE(MAX(grantGeneration), 0) FROM grant_journal_v3)
      THEN RAISE(ABORT, 'cannot append to a superseded grant generation') END;
  END;

-- Inherited non-appending side tables. IF NOT EXISTS so that one script serves both
-- fresh creation and migration onto an existing carrierFormat 1/2 database. The open
-- dispatch additionally verifies the stored SQL text of these two tables byte-equals
-- the frozen definition, so IF NOT EXISTS can never silently accept a variant.
CREATE TABLE IF NOT EXISTS carrier_quarantine (
  grantGeneration INTEGER PRIMARY KEY,
  reason     TEXT NOT NULL CHECK (reason IN ('uncertainTailLoss','witnesslessRestore')),
  observed_tail_seq INTEGER,
  body       TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS carrier_capacity_pause (
  grantGeneration INTEGER PRIMARY KEY,
  proven_tail_seq INTEGER NOT NULL,
  reserved_terminal_slot INTEGER NOT NULL DEFAULT 1
);
