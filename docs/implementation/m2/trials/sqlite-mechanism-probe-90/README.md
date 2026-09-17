# SQLite mechanism probe90

Standalone pinned rusqlite0.40.2, bundled SQLite3.53.2; no product dependency selection. The first open refused the symlink ancestor /tmp with extended CANTOPEN_SYMLINK1550. Only the owned probe directory was resolved to its physical path for retry; NOFOLLOW stayed enabled. Initial source/error and exact successful retry are retained.

The successful native macOS probe verified WAL, FULL synchronous, zero busy timeout, defensive mode, DQS off, trusted-schema off, foreign keys and fullfsync/checkpoint_fullfsync settings; competing writer BEGIN IMMEDIATE returned busy, an existing reader retained its snapshot across commit, a fresh connection saw the committed value, read-only missing-file access created no database, and a main-file symlink was refused. The measured six-microsecond busy return is an observation, not a response-time guarantee. SQLite sidecars are recorded as observed, not authenticated immutable evidence.

Primary API sources: https://docs.rs/rusqlite/0.40.2/rusqlite/struct.Connection.html ; https://www.sqlite.org/c3ref/open.html ; https://www.sqlite.org/pragma.html ; https://www.sqlite.org/wal.html . Engine/source/build features and11 archive checksums are recorded. This does not establish path custody, crash/power-loss recovery, release qualification or any committed OpenSIP Run. Review and guarded integration remain.
