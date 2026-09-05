-- PROPOSED lifecycle carrier v2. Design DDL, not product implementation.
-- Requires SQLite >= 3.37.0 for STRICT tables. Exact bundled version is a
-- release inventory input. All connections register the closed callbacks in
-- lifecycle-carrier.contract.v2.json; absence raises and fails closed.
PRAGMA encoding = 'UTF-8';
PRAGMA foreign_keys = ON;
PRAGMA recursive_triggers = ON;
PRAGMA journal_mode = WAL;
PRAGMA synchronous = FULL;
PRAGMA user_version = 1;

CREATE TABLE generation (
  id TEXT PRIMARY KEY NOT NULL CHECK (length(CAST(id AS BLOB))=36 AND id=lower(id) AND substr(id,9,1)='-' AND substr(id,14,1)='-' AND substr(id,19,1)='-' AND substr(id,24,1)='-' AND length(replace(id,'-',''))=32 AND replace(id,'-','') NOT GLOB '*[^0-9a-f]*' AND substr(id,15,1)='4' AND substr(id,20,1) IN ('8','9','a','b')) CHECK(instr(id,char(0))=0),
  manifestDigest TEXT NOT NULL CHECK (length(CAST(manifestDigest AS BLOB))=64 AND manifestDigest NOT GLOB '*[^0-9a-f]*') CHECK(instr(manifestDigest,char(0))=0),
  lockDigest TEXT NOT NULL CHECK (length(CAST(lockDigest AS BLOB))=64 AND lockDigest NOT GLOB '*[^0-9a-f]*') CHECK(instr(lockDigest,char(0))=0),
  platform TEXT NOT NULL CHECK(platform IN ('macos-arm64','macos-x86_64','linux-arm64','linux-x86_64')) CHECK(instr(platform,char(0))=0),
  immutablePath TEXT NOT NULL UNIQUE CHECK(immutablePath='generations/' || id) CHECK(instr(immutablePath,char(0))=0),
  state TEXT NOT NULL CHECK(state IN ('PREPARING','VERIFIED','READY','QUARANTINED')) CHECK(instr(state,char(0))=0),
  rootVersion INTEGER CHECK(rootVersion BETWEEN 1 AND 9223372036854775807),
  indexSnapshotVersion INTEGER CHECK(indexSnapshotVersion BETWEEN 1 AND 9223372036854775807),
  revocationVersion INTEGER CHECK(revocationVersion BETWEEN 1 AND 9223372036854775807),
  permissionPolicyDigest TEXT CHECK (length(CAST(permissionPolicyDigest AS BLOB))=64 AND permissionPolicyDigest NOT GLOB '*[^0-9a-f]*') CHECK(instr(permissionPolicyDigest,char(0))=0),
  CHECK((rootVersion IS NULL AND indexSnapshotVersion IS NULL AND revocationVersion IS NULL AND permissionPolicyDigest IS NULL)
     OR (rootVersion IS NOT NULL AND indexSnapshotVersion IS NOT NULL AND revocationVersion IS NOT NULL AND permissionPolicyDigest IS NOT NULL)),
  CHECK(state NOT IN ('VERIFIED','READY') OR rootVersion IS NOT NULL)
) STRICT;

-- Opaque keys never become path segments. The local namespace UUID does.
CREATE TABLE project_registry (
  projectKey TEXT PRIMARY KEY NOT NULL CHECK (length(CAST(projectKey AS BLOB)) BETWEEN 1 AND 1024 AND instr(projectKey,char(0))=0) CHECK(instr(projectKey,char(0))=0),
  namespaceId TEXT NOT NULL UNIQUE CHECK (length(CAST(namespaceId AS BLOB))=36 AND namespaceId=lower(namespaceId) AND substr(namespaceId,9,1)='-' AND substr(namespaceId,14,1)='-' AND substr(namespaceId,19,1)='-' AND substr(namespaceId,24,1)='-' AND length(replace(namespaceId,'-',''))=32 AND replace(namespaceId,'-','') NOT GLOB '*[^0-9a-f]*' AND substr(namespaceId,15,1)='4' AND substr(namespaceId,20,1) IN ('8','9','a','b')) CHECK(instr(namespaceId,char(0))=0),
  platform TEXT NOT NULL CHECK(platform IN ('macos','linux')) CHECK(instr(platform,char(0))=0),
  rootPathBytesHex TEXT NOT NULL CHECK(length(CAST(rootPathBytesHex AS BLOB))>=2 AND length(CAST(rootPathBytesHex AS BLOB))%2=0 AND substr(rootPathBytesHex,1,2)='2f' AND rootPathBytesHex NOT GLOB '*[^0-9a-f]*') CHECK(instr(rootPathBytesHex,char(0))=0),
  deviceId TEXT NOT NULL CHECK(length(CAST(deviceId AS BLOB)) BETWEEN 1 AND 20 AND deviceId NOT GLOB '*[^0-9]*' AND (deviceId='0' OR substr(deviceId,1,1)<>'0') AND (length(CAST(deviceId AS BLOB))<20 OR deviceId<='18446744073709551615')) CHECK(instr(deviceId,char(0))=0),
  inodeId TEXT NOT NULL CHECK(length(CAST(inodeId AS BLOB)) BETWEEN 1 AND 20 AND inodeId NOT GLOB '*[^0-9]*' AND (inodeId='0' OR substr(inodeId,1,1)<>'0') AND (length(CAST(inodeId AS BLOB))<20 OR inodeId<='18446744073709551615')) CHECK(instr(inodeId,char(0))=0),
  birthSeconds INTEGER NOT NULL,
  birthNanoseconds INTEGER NOT NULL CHECK(birthNanoseconds BETWEEN 0 AND 999999999),
  status TEXT NOT NULL CHECK(status IN ('ACTIVE','RETIRED')) CHECK(instr(status,char(0))=0)
) STRICT;
CREATE UNIQUE INDEX one_active_root_locator ON project_registry(platform,rootPathBytesHex) WHERE status='ACTIVE';
CREATE UNIQUE INDEX one_active_root_object ON project_registry(platform,deviceId,inodeId,birthSeconds,birthNanoseconds) WHERE status='ACTIVE';

CREATE TABLE project_selection (
  projectKey TEXT PRIMARY KEY NOT NULL CHECK (length(CAST(projectKey AS BLOB)) BETWEEN 1 AND 1024 AND instr(projectKey,char(0))=0) REFERENCES project_registry(projectKey) ON DELETE RESTRICT ON UPDATE RESTRICT CHECK(instr(projectKey,char(0))=0),
  generationId TEXT NOT NULL REFERENCES generation(id) ON DELETE RESTRICT ON UPDATE RESTRICT CHECK(instr(generationId,char(0))=0)
) STRICT;

CREATE TABLE operation_lease (
  leaseId TEXT PRIMARY KEY NOT NULL CHECK (length(CAST(leaseId AS BLOB))=36 AND leaseId=lower(leaseId) AND substr(leaseId,9,1)='-' AND substr(leaseId,14,1)='-' AND substr(leaseId,19,1)='-' AND substr(leaseId,24,1)='-' AND length(replace(leaseId,'-',''))=32 AND replace(leaseId,'-','') NOT GLOB '*[^0-9a-f]*' AND substr(leaseId,15,1)='4' AND substr(leaseId,20,1) IN ('8','9','a','b')) CHECK(instr(leaseId,char(0))=0),
  projectKey TEXT NOT NULL CHECK (length(CAST(projectKey AS BLOB)) BETWEEN 1 AND 1024 AND instr(projectKey,char(0))=0) REFERENCES project_registry(projectKey) ON DELETE RESTRICT ON UPDATE RESTRICT CHECK(instr(projectKey,char(0))=0),
  generationId TEXT NOT NULL REFERENCES generation(id) ON DELETE RESTRICT ON UPDATE RESTRICT CHECK(instr(generationId,char(0))=0),
  supervisorBootId TEXT NOT NULL CHECK (length(CAST(supervisorBootId AS BLOB))=36 AND supervisorBootId=lower(supervisorBootId) AND substr(supervisorBootId,9,1)='-' AND substr(supervisorBootId,14,1)='-' AND substr(supervisorBootId,19,1)='-' AND substr(supervisorBootId,24,1)='-' AND length(replace(supervisorBootId,'-',''))=32 AND replace(supervisorBootId,'-','') NOT GLOB '*[^0-9a-f]*' AND substr(supervisorBootId,15,1)='4' AND substr(supervisorBootId,20,1) IN ('8','9','a','b')) CHECK(instr(supervisorBootId,char(0))=0),
  processStartToken TEXT NOT NULL CHECK(length(processStartToken) BETWEEN 1 AND 256 AND instr(processStartToken,char(0))=0) CHECK(instr(processStartToken,char(0))=0)
) STRICT;

CREATE TABLE transition (
  txId TEXT PRIMARY KEY NOT NULL CHECK (length(CAST(txId AS BLOB))=36 AND txId=lower(txId) AND substr(txId,9,1)='-' AND substr(txId,14,1)='-' AND substr(txId,19,1)='-' AND substr(txId,24,1)='-' AND length(replace(txId,'-',''))=32 AND replace(txId,'-','') NOT GLOB '*[^0-9a-f]*' AND substr(txId,15,1)='4' AND substr(txId,20,1) IN ('8','9','a','b')) CHECK(instr(txId,char(0))=0),
  projectKey TEXT NOT NULL CHECK (length(CAST(projectKey AS BLOB)) BETWEEN 1 AND 1024 AND instr(projectKey,char(0))=0) REFERENCES project_registry(projectKey) ON DELETE RESTRICT ON UPDATE RESTRICT CHECK(instr(projectKey,char(0))=0),
  oldGeneration TEXT REFERENCES generation(id) ON DELETE RESTRICT ON UPDATE RESTRICT CHECK(instr(oldGeneration,char(0))=0),
  newGeneration TEXT NOT NULL REFERENCES generation(id) ON DELETE RESTRICT ON UPDATE RESTRICT CHECK(instr(newGeneration,char(0))=0),
  phase TEXT NOT NULL CHECK(phase IN ('PREPARING','VERIFIED','READY','COMMITTED','ABORTED')) CHECK(instr(phase,char(0))=0),
  CHECK(oldGeneration IS NULL OR oldGeneration<>newGeneration)
) STRICT;
CREATE UNIQUE INDEX one_pending_transition_per_project ON transition(projectKey)
  WHERE phase IN ('PREPARING','VERIFIED','READY');

CREATE TABLE quarantine (
  generationId TEXT PRIMARY KEY NOT NULL REFERENCES generation(id) ON DELETE RESTRICT ON UPDATE RESTRICT CHECK(instr(generationId,char(0))=0),
  reason TEXT NOT NULL CHECK(reason IN ('INCOMPLETE-PUBLICATION','CONTENT-MISMATCH','CURRENT-TRUST-REFUSAL','AMBIGUOUS-STATE')) CHECK(instr(reason,char(0))=0),
  observedDigest TEXT CHECK (length(CAST(observedDigest AS BLOB))=64 AND observedDigest NOT GLOB '*[^0-9a-f]*') CHECK(instr(observedDigest,char(0))=0)
) STRICT;

-- Every mutation requires the same permanent install-root writer lock.
CREATE TRIGGER generation_writer_insert BEFORE INSERT ON generation
BEGIN SELECT CASE WHEN lifecycle_writer_authorized() IS NOT 1 THEN RAISE(ABORT,'LIFECYCLE-WRITER-LOCK-REQUIRED') END; END;
CREATE TRIGGER generation_writer_update BEFORE UPDATE ON generation
BEGIN SELECT CASE WHEN lifecycle_writer_authorized() IS NOT 1 THEN RAISE(ABORT,'LIFECYCLE-WRITER-LOCK-REQUIRED') END; END;
CREATE TRIGGER generation_writer_delete BEFORE DELETE ON generation
BEGIN SELECT CASE WHEN lifecycle_writer_authorized() IS NOT 1 THEN RAISE(ABORT,'LIFECYCLE-WRITER-LOCK-REQUIRED') END; END;
CREATE TRIGGER project_selection_writer_insert BEFORE INSERT ON project_selection
BEGIN SELECT CASE WHEN lifecycle_writer_authorized() IS NOT 1 THEN RAISE(ABORT,'LIFECYCLE-WRITER-LOCK-REQUIRED') END; END;
CREATE TRIGGER project_selection_writer_update BEFORE UPDATE ON project_selection
BEGIN SELECT CASE WHEN lifecycle_writer_authorized() IS NOT 1 THEN RAISE(ABORT,'LIFECYCLE-WRITER-LOCK-REQUIRED') END; END;
CREATE TRIGGER project_selection_writer_delete BEFORE DELETE ON project_selection
BEGIN SELECT CASE WHEN lifecycle_writer_authorized() IS NOT 1 THEN RAISE(ABORT,'LIFECYCLE-WRITER-LOCK-REQUIRED') END; END;
CREATE TRIGGER operation_lease_writer_insert BEFORE INSERT ON operation_lease
BEGIN SELECT CASE WHEN lifecycle_writer_authorized() IS NOT 1 THEN RAISE(ABORT,'LIFECYCLE-WRITER-LOCK-REQUIRED') END; END;
CREATE TRIGGER operation_lease_writer_update BEFORE UPDATE ON operation_lease
BEGIN SELECT CASE WHEN lifecycle_writer_authorized() IS NOT 1 THEN RAISE(ABORT,'LIFECYCLE-WRITER-LOCK-REQUIRED') END; END;
CREATE TRIGGER operation_lease_writer_delete BEFORE DELETE ON operation_lease
BEGIN SELECT CASE WHEN lifecycle_writer_authorized() IS NOT 1 THEN RAISE(ABORT,'LIFECYCLE-WRITER-LOCK-REQUIRED') END; END;
CREATE TRIGGER transition_writer_insert BEFORE INSERT ON transition
BEGIN SELECT CASE WHEN lifecycle_writer_authorized() IS NOT 1 THEN RAISE(ABORT,'LIFECYCLE-WRITER-LOCK-REQUIRED') END; END;
CREATE TRIGGER transition_writer_update BEFORE UPDATE ON transition
BEGIN SELECT CASE WHEN lifecycle_writer_authorized() IS NOT 1 THEN RAISE(ABORT,'LIFECYCLE-WRITER-LOCK-REQUIRED') END; END;
CREATE TRIGGER transition_writer_delete BEFORE DELETE ON transition
BEGIN SELECT CASE WHEN lifecycle_writer_authorized() IS NOT 1 THEN RAISE(ABORT,'LIFECYCLE-WRITER-LOCK-REQUIRED') END; END;
CREATE TRIGGER quarantine_writer_insert BEFORE INSERT ON quarantine
BEGIN SELECT CASE WHEN lifecycle_writer_authorized() IS NOT 1 THEN RAISE(ABORT,'LIFECYCLE-WRITER-LOCK-REQUIRED') END; END;
CREATE TRIGGER quarantine_writer_update BEFORE UPDATE ON quarantine
BEGIN SELECT CASE WHEN lifecycle_writer_authorized() IS NOT 1 THEN RAISE(ABORT,'LIFECYCLE-WRITER-LOCK-REQUIRED') END; END;
CREATE TRIGGER quarantine_writer_delete BEFORE DELETE ON quarantine
BEGIN SELECT CASE WHEN lifecycle_writer_authorized() IS NOT 1 THEN RAISE(ABORT,'LIFECYCLE-WRITER-LOCK-REQUIRED') END; END;

CREATE TRIGGER generation_insert_preparing BEFORE INSERT ON generation BEGIN
  SELECT CASE WHEN NEW.state<>'PREPARING' OR NEW.rootVersion IS NOT NULL
    THEN RAISE(ABORT,'GENERATION-MUST-START-PREPARING') END;
END;
CREATE TRIGGER generation_immutable BEFORE UPDATE ON generation BEGIN
  SELECT CASE WHEN NEW.id<>OLD.id OR NEW.manifestDigest<>OLD.manifestDigest
    OR NEW.lockDigest<>OLD.lockDigest OR NEW.platform<>OLD.platform OR NEW.immutablePath<>OLD.immutablePath
    THEN RAISE(ABORT,'IMMUTABLE-GENERATION-IDENTITY') END;
  SELECT CASE WHEN NOT (
    (OLD.state='PREPARING' AND NEW.state='VERIFIED') OR
    (OLD.state='VERIFIED' AND NEW.state IN ('VERIFIED','READY')) OR
    (OLD.state='READY' AND NEW.state='READY') OR
    (OLD.state IN ('PREPARING','VERIFIED','READY') AND NEW.state='QUARANTINED'))
    THEN RAISE(ABORT,'INVALID-GENERATION-TRANSITION') END;
  SELECT CASE WHEN NEW.state IN ('VERIFIED','READY') AND lifecycle_verified_generation(NEW.id,NEW.manifestDigest,NEW.lockDigest,NEW.platform,NEW.rootVersion,NEW.indexSnapshotVersion,NEW.revocationVersion,NEW.permissionPolicyDigest) IS NOT 1
    THEN RAISE(ABORT,'CURRENT-VERIFICATION-TICKET-REQUIRED') END;
  SELECT CASE WHEN NEW.state='READY' AND lifecycle_durable_ready(NEW.id,NEW.immutablePath) IS NOT 1
    THEN RAISE(ABORT,'DURABLE-TREE-REQUIRED') END;
  SELECT CASE WHEN NEW.state='QUARANTINED' AND (NOT EXISTS(SELECT 1 FROM quarantine WHERE generationId=NEW.id)
     OR EXISTS(SELECT 1 FROM project_selection WHERE generationId=NEW.id))
    THEN RAISE(ABORT,'QUARANTINE-MUST-DEACTIVATE-SELECTIONS') END;
END;
CREATE TRIGGER generation_gc BEFORE DELETE ON generation BEGIN
  SELECT CASE WHEN lifecycle_gc_authorized(OLD.id) IS NOT 1 THEN RAISE(ABORT,'GC-REFERENCE-CENSUS-REQUIRED') END;
END;

CREATE TRIGGER transition_insert_preparing BEFORE INSERT ON transition BEGIN
  SELECT CASE WHEN lifecycle_project_binding(NEW.projectKey) IS NOT 1 OR NOT EXISTS(SELECT 1 FROM project_registry WHERE projectKey=NEW.projectKey AND status='ACTIVE') THEN RAISE(ABORT,'CURRENT-OPEN-ROOT-BINDING-REQUIRED') END;
  SELECT CASE WHEN NEW.phase<>'PREPARING' THEN RAISE(ABORT,'TRANSITION-MUST-START-PREPARING') END;
  SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM generation WHERE id=NEW.newGeneration AND state IN ('PREPARING','VERIFIED','READY'))
    THEN RAISE(ABORT,'TARGET-GENERATION-UNAVAILABLE') END;
  SELECT CASE WHEN NEW.oldGeneration IS NOT (SELECT generationId FROM project_selection WHERE projectKey=NEW.projectKey)
    THEN RAISE(ABORT,'PROJECT-COMPARE-AND-SWAP-MISMATCH') END;
END;
CREATE TRIGGER transition_advance BEFORE UPDATE ON transition BEGIN
  SELECT CASE WHEN NEW.txId<>OLD.txId OR NEW.projectKey<>OLD.projectKey OR NEW.oldGeneration IS NOT OLD.oldGeneration OR NEW.newGeneration<>OLD.newGeneration
    THEN RAISE(ABORT,'IMMUTABLE-TRANSITION-IDENTITY') END;
  SELECT CASE WHEN NOT ((OLD.phase='PREPARING' AND NEW.phase='VERIFIED') OR (OLD.phase='VERIFIED' AND NEW.phase='READY')
      OR (OLD.phase='READY' AND NEW.phase='COMMITTED') OR (OLD.phase IN ('PREPARING','VERIFIED','READY') AND NEW.phase='ABORTED'))
    THEN RAISE(ABORT,'INVALID-PUBLICATION-TRANSITION') END;
  SELECT CASE WHEN NEW.phase='VERIFIED' AND NOT EXISTS(SELECT 1 FROM generation WHERE id=NEW.newGeneration AND state IN ('VERIFIED','READY'))
    THEN RAISE(ABORT,'TARGET-NOT-VERIFIED') END;
  SELECT CASE WHEN NEW.phase='READY' AND NOT EXISTS(SELECT 1 FROM generation WHERE id=NEW.newGeneration AND state='READY')
    THEN RAISE(ABORT,'TARGET-NOT-READY') END;
  SELECT CASE WHEN NEW.phase='COMMITTED' AND NOT EXISTS(SELECT 1 FROM project_selection WHERE projectKey=NEW.projectKey AND generationId=NEW.newGeneration)
    THEN RAISE(ABORT,'SELECTION-NOT-PUBLISHED') END;
END;
CREATE TRIGGER transition_prune BEFORE DELETE ON transition BEGIN
  SELECT CASE WHEN OLD.phase NOT IN ('COMMITTED','ABORTED') OR lifecycle_transition_prune_authorized(OLD.txId) IS NOT 1
    THEN RAISE(ABORT,'TRANSITION-RETENTION-ROOT') END;
END;

CREATE TRIGGER selection_insert_guard BEFORE INSERT ON project_selection BEGIN
  SELECT CASE WHEN lifecycle_project_binding(NEW.projectKey) IS NOT 1 OR NOT EXISTS(SELECT 1 FROM project_registry WHERE projectKey=NEW.projectKey AND status='ACTIVE') THEN RAISE(ABORT,'CURRENT-OPEN-ROOT-BINDING-REQUIRED') END;
  SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM generation g WHERE g.id=NEW.generationId AND g.state='READY'
    AND lifecycle_generation_project_scope(NEW.projectKey,g.id,g.lockDigest)=1
    AND lifecycle_verified_generation(g.id,g.manifestDigest,g.lockDigest,g.platform,g.rootVersion,g.indexSnapshotVersion,g.revocationVersion,g.permissionPolicyDigest)=1
    AND lifecycle_durable_ready(g.id,g.immutablePath)=1)
    THEN RAISE(ABORT,'SELECT-ONLY-CURRENT-VERIFIED-READY') END;
  SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM transition WHERE projectKey=NEW.projectKey AND oldGeneration IS NULL AND newGeneration=NEW.generationId AND phase='READY')
    THEN RAISE(ABORT,'MATCHING-READY-TRANSITION-REQUIRED') END;
END;
CREATE TRIGGER selection_update_guard BEFORE UPDATE ON project_selection BEGIN
  SELECT CASE WHEN lifecycle_project_binding(NEW.projectKey) IS NOT 1 OR NOT EXISTS(SELECT 1 FROM project_registry WHERE projectKey=NEW.projectKey AND status='ACTIVE') THEN RAISE(ABORT,'CURRENT-OPEN-ROOT-BINDING-REQUIRED') END;
  SELECT CASE WHEN NEW.projectKey<>OLD.projectKey THEN RAISE(ABORT,'IMMUTABLE-PROJECT-IDENTITY') END;
  SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM generation g WHERE g.id=NEW.generationId AND g.state='READY'
    AND lifecycle_generation_project_scope(NEW.projectKey,g.id,g.lockDigest)=1
    AND lifecycle_verified_generation(g.id,g.manifestDigest,g.lockDigest,g.platform,g.rootVersion,g.indexSnapshotVersion,g.revocationVersion,g.permissionPolicyDigest)=1
    AND lifecycle_durable_ready(g.id,g.immutablePath)=1)
    THEN RAISE(ABORT,'SELECT-ONLY-CURRENT-VERIFIED-READY') END;
  SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM transition WHERE projectKey=NEW.projectKey AND oldGeneration=OLD.generationId AND newGeneration=NEW.generationId AND phase='READY')
    THEN RAISE(ABORT,'MATCHING-READY-TRANSITION-REQUIRED') END;
END;
CREATE TRIGGER selection_insert_commit AFTER INSERT ON project_selection BEGIN
  UPDATE transition SET phase='COMMITTED' WHERE projectKey=NEW.projectKey AND oldGeneration IS NULL AND newGeneration=NEW.generationId AND phase='READY';
END;
CREATE TRIGGER selection_update_commit AFTER UPDATE ON project_selection BEGIN
  UPDATE transition SET phase='COMMITTED' WHERE projectKey=NEW.projectKey AND oldGeneration=OLD.generationId AND newGeneration=NEW.generationId AND phase='READY';
END;

CREATE TRIGGER lease_insert_guard BEFORE INSERT ON operation_lease BEGIN
  SELECT CASE WHEN lifecycle_project_binding(NEW.projectKey) IS NOT 1 OR NOT EXISTS(SELECT 1 FROM project_registry WHERE projectKey=NEW.projectKey AND status='ACTIVE') THEN RAISE(ABORT,'CURRENT-OPEN-ROOT-BINDING-REQUIRED') END;
  SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM project_selection WHERE projectKey=NEW.projectKey AND generationId=NEW.generationId)
    THEN RAISE(ABORT,'LEASE-MUST-PIN-SELECTED-GENERATION') END;
  SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM generation g WHERE g.id=NEW.generationId AND g.state='READY'
    AND lifecycle_generation_project_scope(NEW.projectKey,g.id,g.lockDigest)=1
    AND lifecycle_verified_generation(g.id,g.manifestDigest,g.lockDigest,g.platform,g.rootVersion,g.indexSnapshotVersion,g.revocationVersion,g.permissionPolicyDigest)=1)
    THEN RAISE(ABORT,'LEASE-CURRENT-TRUST-REQUIRED') END;
  SELECT CASE WHEN lifecycle_lease_acquired(NEW.leaseId,NEW.supervisorBootId,NEW.processStartToken) IS NOT 1
    THEN RAISE(ABORT,'OS-LEASE-CAPABILITY-REQUIRED') END;
END;
CREATE TRIGGER lease_immutable BEFORE UPDATE ON operation_lease BEGIN
  SELECT RAISE(ABORT,'OPERATION-GENERATION-IS-IMMUTABLE');
END;
CREATE TRIGGER lease_delete_guard BEFORE DELETE ON operation_lease BEGIN
  SELECT CASE WHEN lifecycle_lease_release_authorized(OLD.leaseId) IS NOT 1
    THEN RAISE(ABORT,'EXPLICIT-RELEASE-OR-PROVEN-DEATH-REQUIRED') END;
END;

CREATE TRIGGER quarantine_immutable BEFORE UPDATE ON quarantine BEGIN
  SELECT RAISE(ABORT,'QUARANTINE-RECORD-IS-IMMUTABLE');
END;
CREATE TRIGGER quarantine_apply AFTER INSERT ON quarantine BEGIN
  UPDATE generation SET state='QUARANTINED' WHERE id=NEW.generationId;
END;
CREATE TRIGGER quarantine_delete_guard BEFORE DELETE ON quarantine BEGIN
  SELECT CASE WHEN lifecycle_gc_authorized(OLD.generationId) IS NOT 1
    THEN RAISE(ABORT,'QUARANTINE-RETENTION-ROOT') END;
END;
CREATE TRIGGER registry_writer_insert BEFORE INSERT ON project_registry BEGIN SELECT CASE WHEN lifecycle_writer_authorized() IS NOT 1 THEN RAISE(ABORT,'LIFECYCLE-WRITER-LOCK-REQUIRED') END; END;
CREATE TRIGGER registry_writer_update BEFORE UPDATE ON project_registry BEGIN SELECT CASE WHEN lifecycle_writer_authorized() IS NOT 1 THEN RAISE(ABORT,'LIFECYCLE-WRITER-LOCK-REQUIRED') END; END;
CREATE TRIGGER registry_writer_delete BEFORE DELETE ON project_registry BEGIN SELECT CASE WHEN lifecycle_writer_authorized() IS NOT 1 THEN RAISE(ABORT,'LIFECYCLE-WRITER-LOCK-REQUIRED') END; END;

CREATE TRIGGER registry_insert_guard BEFORE INSERT ON project_registry BEGIN
  SELECT CASE WHEN NEW.status<>'ACTIVE' OR lifecycle_project_root_verified(NEW.projectKey,NEW.namespaceId,NEW.platform,NEW.rootPathBytesHex,NEW.deviceId,NEW.inodeId,NEW.birthSeconds,NEW.birthNanoseconds) IS NOT 1
    THEN RAISE(ABORT,'VERIFIED-HOST-ROOT-BINDING-REQUIRED') END;
END;
CREATE TRIGGER registry_update_guard BEFORE UPDATE ON project_registry BEGIN
  SELECT CASE WHEN NEW.projectKey<>OLD.projectKey OR NEW.namespaceId<>OLD.namespaceId OR NEW.platform<>OLD.platform
    OR NEW.deviceId<>OLD.deviceId OR NEW.inodeId<>OLD.inodeId OR NEW.birthSeconds<>OLD.birthSeconds OR NEW.birthNanoseconds<>OLD.birthNanoseconds
    THEN RAISE(ABORT,'ROOT-OBJECT-REBIND-REQUIRES-NEW-KEY') END;
  SELECT CASE WHEN OLD.status='RETIRED' THEN RAISE(ABORT,'RETIRED-PROJECT-KEY-NOT-REUSABLE') END;
  SELECT CASE WHEN NEW.status='ACTIVE' AND lifecycle_project_root_verified(NEW.projectKey,NEW.namespaceId,NEW.platform,NEW.rootPathBytesHex,NEW.deviceId,NEW.inodeId,NEW.birthSeconds,NEW.birthNanoseconds) IS NOT 1
    THEN RAISE(ABORT,'VERIFIED-SAME-OBJECT-RENAME-REQUIRED') END;
  SELECT CASE WHEN NEW.status='RETIRED' AND EXISTS(SELECT 1 FROM project_selection WHERE projectKey=NEW.projectKey)
    THEN RAISE(ABORT,'RETIRE-MUST-DEACTIVATE-PROJECT') END;
END;
CREATE TRIGGER registry_no_delete BEFORE DELETE ON project_registry BEGIN
  SELECT RAISE(ABORT,'PROJECT-KEY-TOMBSTONE-RETAINED');
END;

-- LCR-1: replacement is never an alternate lifecycle mutation operation.
-- BEFORE INSERT collision guards run even with recursive_triggers accidentally
-- disabled and cover all primary/UNIQUE identities, including partial indexes.
CREATE TRIGGER generation_no_insert_collision BEFORE INSERT ON generation BEGIN
  SELECT CASE WHEN EXISTS(SELECT 1 FROM generation WHERE id=NEW.id OR immutablePath=NEW.immutablePath) THEN RAISE(ABORT,'INSERT-COLLISION-REPLACE-FORBIDDEN') END;
END;
CREATE TRIGGER project_selection_no_insert_collision BEFORE INSERT ON project_selection BEGIN
  SELECT CASE WHEN EXISTS(SELECT 1 FROM project_selection WHERE projectKey=NEW.projectKey) THEN RAISE(ABORT,'INSERT-COLLISION-REPLACE-FORBIDDEN') END;
END;
CREATE TRIGGER operation_lease_no_insert_collision BEFORE INSERT ON operation_lease BEGIN
  SELECT CASE WHEN EXISTS(SELECT 1 FROM operation_lease WHERE leaseId=NEW.leaseId) THEN RAISE(ABORT,'INSERT-COLLISION-REPLACE-FORBIDDEN') END;
END;
CREATE TRIGGER quarantine_no_insert_collision BEFORE INSERT ON quarantine BEGIN
  SELECT CASE WHEN EXISTS(SELECT 1 FROM quarantine WHERE generationId=NEW.generationId) THEN RAISE(ABORT,'INSERT-COLLISION-REPLACE-FORBIDDEN') END;
END;
CREATE TRIGGER project_registry_no_insert_collision BEFORE INSERT ON project_registry BEGIN
  SELECT CASE WHEN EXISTS(SELECT 1 FROM project_registry WHERE projectKey=NEW.projectKey OR namespaceId=NEW.namespaceId OR (status='ACTIVE' AND NEW.status='ACTIVE' AND platform=NEW.platform AND (rootPathBytesHex=NEW.rootPathBytesHex OR (deviceId=NEW.deviceId AND inodeId=NEW.inodeId AND birthSeconds=NEW.birthSeconds AND birthNanoseconds=NEW.birthNanoseconds)))) THEN RAISE(ABORT,'INSERT-COLLISION-REPLACE-FORBIDDEN') END;
END;
CREATE TRIGGER transition_no_insert_collision BEFORE INSERT ON transition BEGIN
  SELECT CASE WHEN EXISTS(SELECT 1 FROM transition WHERE txId=NEW.txId OR (projectKey=NEW.projectKey AND phase IN ('PREPARING','VERIFIED','READY') AND NEW.phase IN ('PREPARING','VERIFIED','READY'))) THEN RAISE(ABORT,'INSERT-COLLISION-REPLACE-FORBIDDEN') END;
END;
CREATE TRIGGER registry_no_update_collision BEFORE UPDATE ON project_registry BEGIN
  SELECT CASE WHEN EXISTS(SELECT 1 FROM project_registry p WHERE p.projectKey<>OLD.projectKey AND
    (p.projectKey=NEW.projectKey OR p.namespaceId=NEW.namespaceId OR
     (p.status='ACTIVE' AND NEW.status='ACTIVE' AND p.platform=NEW.platform AND
      (p.rootPathBytesHex=NEW.rootPathBytesHex OR
       (p.deviceId=NEW.deviceId AND p.inodeId=NEW.inodeId AND p.birthSeconds=NEW.birthSeconds AND p.birthNanoseconds=NEW.birthNanoseconds)))))
    THEN RAISE(ABORT,'UPDATE-COLLISION-REPLACE-FORBIDDEN') END;
END;
