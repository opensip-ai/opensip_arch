CREATE TABLE grant_journal (
  grantGeneration INTEGER NOT NULL,
  seq          INTEGER NOT NULL CHECK (seq >= 1 AND seq <= 9007199254740991),
  record_type  TEXT    NOT NULL CHECK (record_type IN
                 ('GRANT','NARROW','EXPIRY','RA','RCI','RCO','ICI','ICO','REV','CLN','AUD',
                  'CHECKPOINT','MIGRATION','TERMINAL')),
  operation_ref TEXT   NOT NULL CHECK (operation_ref GLOB 'op-[0-9a-f]*' AND length(operation_ref) = 35),
  request_ref  TEXT,
  token        TEXT,
  install_generation_id TEXT,
  manifest_digest TEXT CHECK (manifest_digest IS NULL OR length(manifest_digest) = 64),
  platform     TEXT CHECK (platform IS NULL OR platform IN ('macos-arm64','macos-x86_64','linux-x86_64','linux-arm64')),
  body         TEXT    NOT NULL,
  body_sha256  TEXT    NOT NULL CHECK (length(body_sha256) = 64),
  prev_sha256  TEXT    NOT NULL CHECK (length(prev_sha256) = 64),
  CHECK (record_type <> 'GRANT' OR (install_generation_id IS NOT NULL AND manifest_digest IS NOT NULL AND platform IS NOT NULL AND token IS NOT NULL)),
  PRIMARY KEY (grantGeneration, seq)
) WITHOUT ROWID;
CREATE TRIGGER gj_no_update BEFORE UPDATE ON grant_journal
  BEGIN SELECT RAISE(ABORT, 'grant journal is append-only'); END;
CREATE TRIGGER gj_no_delete BEFORE DELETE ON grant_journal
  BEGIN SELECT RAISE(ABORT, 'grant journal is append-only'); END;
CREATE TRIGGER gj_seq_contiguous BEFORE INSERT ON grant_journal
  BEGIN
    SELECT CASE WHEN NEW.seq <> (SELECT COALESCE(MAX(seq), 0) + 1 FROM grant_journal WHERE grantGeneration = NEW.grantGeneration)
      THEN RAISE(ABORT, 'grant journal sequence must be tail+1') END;
    SELECT CASE WHEN EXISTS (SELECT 1 FROM grant_journal WHERE grantGeneration = NEW.grantGeneration AND record_type = 'TERMINAL')
      THEN RAISE(ABORT, 'grant journal carrier is TERMINAL') END;
    SELECT CASE WHEN NEW.seq = 9007199254740991 AND NEW.record_type <> 'TERMINAL'
      THEN RAISE(ABORT, 'grant journal seq 9007199254740991 is the reserved terminal slot; roll the grant generation') END;
  END;
CREATE TABLE carrier_quarantine (
  grantGeneration INTEGER PRIMARY KEY,
  reason     TEXT NOT NULL CHECK (reason IN ('uncertainTailLoss','witnesslessRestore')),
  observed_tail_seq INTEGER,
  body       TEXT NOT NULL
);
CREATE TABLE carrier_capacity_pause (
  grantGeneration INTEGER PRIMARY KEY,
  proven_tail_seq INTEGER NOT NULL,
  reserved_terminal_slot INTEGER NOT NULL DEFAULT 1
);
