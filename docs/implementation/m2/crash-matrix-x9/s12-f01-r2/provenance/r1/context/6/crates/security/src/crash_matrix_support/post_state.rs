//! Law X9 r1 item 7's post-state (unit X9-1): `raw`, `logical` and
//! `normalizedSha256` of one scratch tree, captured between processes.
//!
//! - `raw` is every regular file under the root, by relative path, size and
//!   SHA-256 (line 1072's "actual state bytes").
//! - `logical` dumps every SQLite database under the root table by table and
//!   row by row (the carrier, the ledger), decodes the operational witness
//!   and floor files, lists the object sets, and reduces the trust store to
//!   one digest (`trustState`). A database is read from a private copy of
//!   its file and `-wal`, so the capture never opens, locks, checkpoints or
//!   creates anything under the root, and a later capture of an unchanged
//!   tree compares equal (R1's `stateUnchanged` is a comparison).
//! - `normalizedSha256` hashes `logical` after every drawn value is replaced
//!   by a placeholder numbered in order of first appearance: ExecutionIds,
//!   `op-` and `req1_` tokens, staging and temporary-name nonces, drawn
//!   identifiers (S, N, project ids), digests over drawn content, wall-clock
//!   data and native clock samples. The traversal that numbers them orders
//!   each object's members by their unnumbered shape, so the numbering does
//!   not depend on how two runs' drawn values happen to sort.
use opensip_identity::{JsonInteger, JsonValue as V, canonical_bytes, digest_hex, raw_sha256};
use std::collections::BTreeMap;
use std::fs;
use std::io::Read;
use std::path::{Path, PathBuf};

/// One regular file of the tree.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct RawEntry {
    pub path: String,
    pub bytes: u64,
    pub sha256: String,
}

/// Item 7's `postState`.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct PostState {
    pub raw: Vec<RawEntry>,
    pub logical: V,
    pub normalized_sha256: String,
}
impl PostState {
    /// `{raw, logical, normalizedSha256}` as the run record carries it.
    pub fn to_json(&self) -> V {
        let raw = self
            .raw
            .iter()
            .map(|e| {
                object([
                    ("path", V::String(e.path.clone())),
                    ("bytes", integer(i128::from(e.bytes))),
                    ("sha256", V::String(e.sha256.clone())),
                ])
            })
            .collect();
        object([
            ("raw", V::Array(raw)),
            ("logical", self.logical.clone()),
            (
                "normalizedSha256",
                V::String(self.normalized_sha256.clone()),
            ),
        ])
    }
}

pub(super) fn object<const N: usize>(pairs: [(&str, V); N]) -> V {
    V::Object(pairs.into_iter().map(|(k, v)| (k.to_owned(), v)).collect())
}
pub(super) fn integer(n: i128) -> V {
    V::Integer(JsonInteger::new(n).expect("a 64-bit integer"))
}
fn hex_sha256(bytes: &[u8]) -> String {
    digest_hex(&raw_sha256(bytes))
}

/// Every entry under `root`, sorted by relative path, without following
/// symbolic links: `(relative, path, is_directory)`.
fn walk(root: &Path) -> Result<Vec<(String, PathBuf, bool)>, String> {
    let mut out = Vec::new();
    let mut stack = vec![root.to_path_buf()];
    while let Some(dir) = stack.pop() {
        let entries = fs::read_dir(&dir).map_err(|e| format!("{}: {e}", dir.display()))?;
        for entry in entries {
            let entry = entry.map_err(|e| format!("{}: {e}", dir.display()))?;
            let path = entry.path();
            let kind = entry
                .file_type()
                .map_err(|e| format!("{}: {e}", path.display()))?;
            let relative = path
                .strip_prefix(root)
                .map_err(|e| format!("{e}"))?
                .to_string_lossy()
                .into_owned();
            if kind.is_dir() {
                stack.push(path.clone());
            }
            out.push((relative, path, kind.is_dir()));
        }
    }
    out.sort();
    Ok(out)
}

const SQLITE_HEADER: &[u8; 16] = b"SQLite format 3\0";
fn is_sqlite(path: &Path) -> bool {
    let mut header = [0u8; 16];
    fs::File::open(path)
        .and_then(|mut f| f.read_exact(&mut header))
        .is_ok()
        && &header == SQLITE_HEADER
}

/// One database, read from a private copy of its file and `-wal`.
fn dump_sqlite(path: &Path, scratch: &Path) -> Result<(V, Vec<String>), String> {
    let copy = scratch.join("db");
    let _ = fs::remove_file(&copy);
    let _ = fs::remove_file(scratch.join("db-wal"));
    let _ = fs::remove_file(scratch.join("db-shm"));
    fs::copy(path, &copy).map_err(|e| format!("{}: {e}", path.display()))?;
    let wal = PathBuf::from(format!("{}-wal", path.display()));
    if wal.exists() {
        fs::copy(&wal, scratch.join("db-wal")).map_err(|e| format!("{}: {e}", wal.display()))?;
    }
    let c = rusqlite::Connection::open(&copy).map_err(|e| format!("{e}"))?;
    let sql = |e: rusqlite::Error| format!("{}: {e}", path.display());
    let mut statement = c
        .prepare("SELECT type,name,sql FROM sqlite_schema WHERE sql IS NOT NULL ORDER BY type,name")
        .map_err(sql)?;
    let schema: Vec<(String, String, String)> = statement
        .query_map([], |r| Ok((r.get(0)?, r.get(1)?, r.get(2)?)))
        .map_err(sql)?
        .collect::<rusqlite::Result<_>>()
        .map_err(sql)?;
    drop(statement);
    let mut tables = BTreeMap::new();
    let mut rowless = Vec::new();
    for (kind, name, text) in &schema {
        if kind != "table" || name.starts_with("sqlite_") {
            continue;
        }
        let rowid = !text.to_ascii_uppercase().contains("WITHOUT ROWID");
        let order = if rowid {
            "ORDER BY rowid".to_owned()
        } else {
            let columns: i64 = c
                .query_row(
                    &format!("SELECT count(*) FROM pragma_table_info('{name}')"),
                    [],
                    |r| r.get(0),
                )
                .map_err(sql)?;
            format!(
                "ORDER BY {}",
                (1..=columns)
                    .map(|n| n.to_string())
                    .collect::<Vec<_>>()
                    .join(",")
            )
        };
        let mut rows = c
            .prepare(&format!("SELECT * FROM \"{name}\" {order}"))
            .map_err(sql)?;
        let count = rows.column_count();
        let values: Vec<V> = rows
            .query_map([], |r| {
                (0..count)
                    .map(|i| {
                        Ok(match r.get_ref(i)? {
                            rusqlite::types::ValueRef::Null => V::Null,
                            rusqlite::types::ValueRef::Integer(n) => integer(i128::from(n)),
                            rusqlite::types::ValueRef::Real(x) => {
                                object([("real", V::String(format!("{x:?}")))])
                            }
                            rusqlite::types::ValueRef::Text(t) => {
                                V::String(String::from_utf8_lossy(t).into_owned())
                            }
                            // A BLOB holding UTF-8 text (a canonical JSON
                            // body) is dumped as that text, so item 7's
                            // normalizer reaches the drawn values inside it
                            // (unit X9-2); any other BLOB by its hex.
                            rusqlite::types::ValueRef::Blob(b) => match std::str::from_utf8(b) {
                                Ok(text) => object([("blobText", V::String(text.to_owned()))]),
                                Err(_) => object([(
                                    "blob",
                                    V::String(b.iter().map(|x| format!("{x:02x}")).collect()),
                                )]),
                            },
                        })
                    })
                    .collect::<rusqlite::Result<Vec<V>>>()
                    .map(V::Array)
            })
            .map_err(sql)?
            .collect::<rusqlite::Result<_>>()
            .map_err(sql)?;
        // A table without rowid lists its rows in primary-key order. Where
        // the key holds a drawn value (an ExecutionId), that order is a drawn
        // permutation, which first-appearance numbering would carry; so its
        // rows are ordered by their unnumbered shape, keeping the key order
        // among rows of one shape (unit X9-3, as X9-2's object set).
        let mut values = values;
        if !rowid {
            values.sort_by_cached_key(shape_bytes);
            rowless.push(name.clone());
        }
        tables.insert(name.clone(), V::Array(values));
    }
    drop(c);
    let schema = schema
        .into_iter()
        .map(|(kind, name, text)| {
            object([
                ("type", V::String(kind)),
                ("name", V::String(name)),
                ("sql", V::String(text)),
            ])
        })
        .collect();
    Ok((
        object([("schema", V::Array(schema)), ("tables", V::Object(tables))]),
        rowless,
    ))
}

/// Rows of a table without rowid whose shapes tie keep their primary-key
/// order, which a drawn key (two `admitted` attempts' ExecutionIds) makes a
/// drawn permutation. Ties are ordered by each row as it normalizes against
/// the rest of the dump: a numbering primed on `logical` with every tied
/// row left out, then applied to each tied row alone (unit X9-3).
fn order_tied_rows(logical: &mut V, rowless: &[(String, String)]) {
    fn rows_of<'a>(logical: &'a mut V, db: &str, table: &str) -> Option<&'a mut Vec<V>> {
        let V::Object(top) = logical else { return None };
        let V::Object(databases) = top.get_mut("databases")? else {
            return None;
        };
        let V::Object(dump) = databases.get_mut(db)? else {
            return None;
        };
        let V::Object(tables) = dump.get_mut("tables")? else {
            return None;
        };
        match tables.get_mut(table)? {
            V::Array(rows) => Some(rows),
            _ => None,
        }
    }
    let tied = |rows: &[V]| -> Vec<bool> {
        let shapes: Vec<Vec<u8>> = rows.iter().map(shape_bytes).collect();
        shapes
            .iter()
            .map(|s| shapes.iter().filter(|t| *t == s).count() > 1)
            .collect()
    };
    let mut primed = logical.clone();
    let mut any = false;
    for (db, table) in rowless {
        if let Some(rows) = rows_of(&mut primed, db, table) {
            let flags = tied(rows);
            any |= flags.iter().any(|f| *f);
            let mut flags = flags.into_iter();
            rows.retain(|_| !flags.next().unwrap_or(false));
        }
    }
    if !any {
        return;
    }
    let mut base = Numbering {
        seen: BTreeMap::new(),
        next: BTreeMap::new(),
    };
    base.value(&primed);
    for (db, table) in rowless {
        if let Some(rows) = rows_of(logical, db, table) {
            rows.sort_by_cached_key(|row| {
                (
                    shape_bytes(row),
                    canonical_bytes(&base.clone().value(row)).unwrap_or_default(),
                )
            });
        }
    }
}

/// Item 7's capture of the tree under `root`. Nothing under `root` is
/// opened for writing, locked, or created.
pub fn capture(root: &Path) -> Result<PostState, String> {
    let entries = walk(root)?;
    let scratch = std::env::temp_dir().join(format!(
        "opensip-x9-capture-{}",
        hex_sha256(&opensip_platform::request_entropy().map_err(|_| "entropy")?)
    ));
    fs::create_dir(&scratch).map_err(|e| format!("{e}"))?;
    let result = capture_with(&entries, &scratch);
    let _ = fs::remove_dir_all(&scratch);
    result
}
fn capture_with(entries: &[(String, PathBuf, bool)], scratch: &Path) -> Result<PostState, String> {
    let mut raw = Vec::new();
    let mut databases = BTreeMap::new();
    let mut operational = BTreeMap::new();
    let mut objects = Vec::new();
    let mut directories = Vec::new();
    let mut trust = BTreeMap::new();
    let mut unreadable = Vec::new();
    let mut rowless = Vec::new();
    for (relative, path, directory) in entries {
        if *directory {
            directories.push(V::String(relative.clone()));
            continue;
        }
        let meta = fs::symlink_metadata(path).map_err(|e| format!("{relative}: {e}"))?;
        if !meta.file_type().is_file() {
            continue;
        }
        // A file the owner cannot read (a parent's mode-000 mutation, X9
        // rows F24 and F53) is recorded by its path, size and mode, never
        // read; its bytes are not in `raw` (unit X9-3).
        let bytes = match fs::read(path) {
            Ok(bytes) => bytes,
            Err(e) if e.kind() == std::io::ErrorKind::PermissionDenied => {
                use std::os::unix::fs::PermissionsExt;
                unreadable.push(object([
                    ("path", V::String(relative.clone())),
                    ("bytes", integer(i128::from(meta.len()))),
                    (
                        "mode",
                        V::String(format!("{:o}", meta.permissions().mode() & 0o7777)),
                    ),
                ]));
                continue;
            }
            Err(e) => return Err(format!("{relative}: {e}")),
        };
        let sha256 = hex_sha256(&bytes);
        raw.push(RawEntry {
            path: relative.clone(),
            bytes: meta.len(),
            sha256: sha256.clone(),
        });
        let parts: Vec<&str> = relative.split('/').collect();
        if relative.ends_with("-wal") || relative.ends_with("-shm") {
            continue;
        }
        if is_sqlite(path) {
            // A file with SQLite's header that SQLite cannot read (a
            // parent's truncated-header mutation, X9 row F24) is recorded as
            // undumpable; its bytes stay in `raw` (unit X9-3).
            let dumped = match dump_sqlite(path, scratch) {
                Ok((dump, tables)) => {
                    rowless.extend(tables.into_iter().map(|t| (relative.clone(), t)));
                    dump
                }
                Err(_) => object([("undumpable", V::Bool(true))]),
            };
            databases.insert(relative.clone(), dumped);
        } else if relative.ends_with(".witness.json")
            || parts.windows(2).any(|w| w == ["trust", "carrier-floors"])
        {
            let value = opensip_identity::parse_json(
                &bytes[..bytes
                    .iter()
                    .rposition(|b| !b.is_ascii_whitespace())
                    .map_or(0, |i| i + 1)],
            )
            .unwrap_or_else(|_| object([("unparsed", V::String(sha256.clone()))]));
            operational.insert(relative.clone(), value);
        } else if parts.windows(2).any(|w| w == ["objects", "sha256"]) {
            // The object set is unordered and its names are content
            // digests, some derived from drawn values (the synthetic
            // candidate's ProjectId): listed by name, its order is a drawn
            // permutation that first-appearance numbering would carry. So
            // it is recorded by each name's shape (its class placeholders),
            // sorted; each object's bytes stay in `raw` (unit X9-2).
            objects.push(shape_string(relative.as_str()));
        } else if parts.contains(&"trust") {
            let value = opensip_identity::parse_json(&bytes).unwrap_or_else(|_| {
                object([
                    ("bytes", integer(i128::from(meta.len()))),
                    ("sha256", V::String(sha256.clone())),
                ])
            });
            trust.insert(relative.clone(), value);
        }
    }
    let mut logical = object([
        ("directories", V::Array(directories)),
        ("databases", V::Object(databases)),
        ("operational", V::Object(operational)),
        (
            "objects",
            V::Array({
                objects.sort();
                objects.into_iter().map(V::String).collect()
            }),
        ),
        // The trust store, reduced to one digest (law X9 r1 item 7's
        // `trustState`): each file's path and decoded content normalized on
        // its own, then the sorted multiset of those. Content-addressed names
        // tie in shape, so one numbering across files would depend on how two
        // runs' digests sort; per file it cannot.
        ("trustState", V::String(trust_state(&trust)?)),
    ]);
    // Only present when a file was unreadable, so every earlier capture's
    // `logical` (and its digest) is unchanged.
    if !unreadable.is_empty()
        && let V::Object(members) = &mut logical
    {
        members.insert("unreadable".into(), V::Array(unreadable));
    }
    order_tied_rows(&mut logical, &rowless);
    let normalized_sha256 = normalized_sha256(&logical)?;
    Ok(PostState {
        raw,
        logical,
        normalized_sha256,
    })
}

/// `trustState`: the SHA-256 over the sorted, length-framed canonical
/// bytes of each trust file's `{path, content}`, normalized alone.
fn trust_state(trust: &BTreeMap<String, V>) -> Result<String, String> {
    let mut files = Vec::new();
    for (path, content) in trust {
        let file = object([
            ("path", V::String(path.clone())),
            ("content", content.clone()),
        ]);
        files.push(canonical_bytes(&normalize(&file)).map_err(|e| format!("{path}: {e:?}"))?);
    }
    files.sort();
    let mut framed = Vec::new();
    for file in files {
        framed.extend_from_slice(&(file.len() as u64).to_be_bytes());
        framed.extend_from_slice(&file);
    }
    Ok(hex_sha256(&framed))
}

// ------------------------------------------------------------ normalizing

/// A drawn-value token's class, or none.
fn token_class(token: &str) -> Option<&'static str> {
    let hex = |s: &str| {
        !s.is_empty()
            && s.bytes()
                .all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b))
    };
    let digits = |s: &str| !s.is_empty() && s.bytes().all(|b| b.is_ascii_digit());
    if let Some(rest) = token.strip_prefix("exec1_") {
        return (rest.len() == 32 && hex(rest)).then_some("exec");
    }
    if let Some(rest) = token.strip_prefix("op-") {
        return (rest.len() == 32 && hex(rest)).then_some("op");
    }
    if let Some(rest) = token.strip_prefix("req1_") {
        return (rest.len() == 32 && hex(rest)).then_some("req");
    }
    match token.len() {
        64 if hex(token) => return Some("h64"),
        32 if hex(token) => return Some("h32"),
        36 => {
            let groups: Vec<&str> = token.split('-').collect();
            if groups.iter().map(|g| g.len()).collect::<Vec<_>>() == [8, 4, 4, 4, 12]
                && groups.iter().all(|g| hex(g))
            {
                return Some("uuid");
            }
        }
        20 => {
            let b = token.as_bytes();
            if b[4] == b'-'
                && b[7] == b'-'
                && b[10] == b'T'
                && b[13] == b':'
                && b[16] == b':'
                && b[19] == b'Z'
                && [
                    &token[..4],
                    &token[5..7],
                    &token[8..10],
                    &token[11..13],
                    &token[14..16],
                    &token[17..19],
                ]
                .iter()
                .all(|p| digits(p))
            {
                return Some("time");
            }
        }
        _ => {}
    }
    None
}

/// The maximal tokens of `s` (runs of `[A-Za-z0-9_:-]`), with their
/// positions. A drawn value is a whole token, or a whole hex run inside
/// one (a name like `<name>.<32 hex>` or `run3:<64 hex>`).
fn tokens(s: &str) -> Vec<(usize, usize, &'static str)> {
    let mut out = Vec::new();
    let bytes = s.as_bytes();
    let word = |b: u8| b.is_ascii_alphanumeric() || b == b'_' || b == b'-' || b == b':';
    let mut i = 0;
    while i < bytes.len() {
        if !word(bytes[i]) {
            i += 1;
            continue;
        }
        let start = i;
        while i < bytes.len() && word(bytes[i]) {
            i += 1;
        }
        let token = &s[start..i];
        if let Some(class) = token_class(token) {
            out.push((start, i, class));
            continue;
        }
        // Hex runs inside the token, bounded by non-hex characters.
        let mut j = start;
        while j < i {
            let is_hex = |b: u8| b.is_ascii_digit() || (b'a'..=b'f').contains(&b);
            if !is_hex(bytes[j]) {
                j += 1;
                continue;
            }
            let run = j;
            while j < i && is_hex(bytes[j]) {
                j += 1;
            }
            let bounded = run == start || !bytes[run - 1].is_ascii_alphanumeric();
            let closed = j == i || !bytes[j].is_ascii_alphanumeric();
            if bounded
                && closed
                && let Some(class) = token_class(&s[run..j])
            {
                out.push((run, j, class));
            }
        }
    }
    out
}

/// Members whose value is a native clock sample or wall-clock datum,
/// whatever its form (law X9 r1 item 7: "wall-clock datum"). Each is
/// replaced by its member name alone, not numbered: the monotonic and boot
/// readings stay native under X9 r2's scripted clock, so whether two of
/// them happen to be equal (two processes in one second) is not a property
/// of the product.
const CLOCK_MEMBERS: [&str; 4] = ["mono", "bootId", "wall", "wallClockData"];
/// Members whose value is already a normalized digest, kept as it is.
const NORMALIZED_MEMBERS: [&str; 1] = ["trustState"];

#[derive(Clone)]
struct Numbering {
    seen: BTreeMap<String, String>,
    next: BTreeMap<&'static str, usize>,
}
impl Numbering {
    fn placeholder(&mut self, class: &'static str, value: &str) -> String {
        if let Some(p) = self.seen.get(value) {
            return p.clone();
        }
        let n = self.next.entry(class).or_insert(0);
        *n += 1;
        let p = format!("<{class}:{n}>");
        self.seen.insert(value.to_owned(), p.clone());
        p
    }
    fn string(&mut self, s: &str) -> String {
        let mut out = String::new();
        let mut at = 0;
        for (start, end, class) in tokens(s) {
            out.push_str(&s[at..start]);
            out.push_str(&self.placeholder(class, &s[start..end]));
            at = end;
        }
        out.push_str(&s[at..]);
        out
    }
    fn value(&mut self, v: &V) -> V {
        match v {
            V::String(s) => V::String(self.string(s)),
            V::Array(items) => V::Array(items.iter().map(|i| self.value(i)).collect()),
            V::Object(members) => {
                let mut ordered: Vec<(&String, &V)> = members.iter().collect();
                ordered.sort_by_key(|(k, v)| (shape_string(k), shape_bytes(v)));
                let mut out = BTreeMap::new();
                for (key, value) in ordered {
                    let value = if CLOCK_MEMBERS.contains(&key.as_str()) {
                        V::String(format!("<clock:{key}>"))
                    } else if NORMALIZED_MEMBERS.contains(&key.as_str()) {
                        value.clone()
                    } else {
                        self.value(value)
                    };
                    out.insert(self.string(key), value);
                }
                V::Object(out)
            }
            other => other.clone(),
        }
    }
}
/// `s` with every drawn value replaced by its class alone.
fn shape_string(s: &str) -> String {
    let mut out = String::new();
    let mut at = 0;
    for (start, end, class) in tokens(s) {
        out.push_str(&s[at..start]);
        out.push_str(&format!("<{class}>"));
        at = end;
    }
    out.push_str(&s[at..]);
    out
}
fn shape(v: &V) -> V {
    match v {
        V::String(s) => V::String(shape_string(s)),
        V::Array(items) => V::Array(items.iter().map(shape).collect()),
        V::Object(members) => V::Object(
            members
                .iter()
                .map(|(k, v)| {
                    let value = if CLOCK_MEMBERS.contains(&k.as_str()) {
                        V::String(format!("<clock:{k}>"))
                    } else if NORMALIZED_MEMBERS.contains(&k.as_str()) {
                        v.clone()
                    } else {
                        shape(v)
                    };
                    (shape_string(k), value)
                })
                .collect(),
        ),
        other => other.clone(),
    }
}
fn shape_bytes(v: &V) -> Vec<u8> {
    canonical_bytes(&shape(v)).unwrap_or_default()
}

/// `logical` with every drawn value replaced by a numbered placeholder.
pub fn normalize(logical: &V) -> V {
    Numbering {
        seen: BTreeMap::new(),
        next: BTreeMap::new(),
    }
    .value(logical)
}
/// The SHA-256 of the canonical bytes of `normalize(logical)`.
pub fn normalized_sha256(logical: &V) -> Result<String, String> {
    let bytes = canonical_bytes(&normalize(logical)).map_err(|e| format!("{e:?}"))?;
    Ok(hex_sha256(&bytes))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn drawn_values_normalize_by_first_appearance_and_structure_does_not() {
        let a = object([
            (
                "exec1_0123456789abcdef0123456789abcdef",
                V::String("op-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa".into()),
            ),
            ("witness.json.ffffffffffffffffffffffffffffffff", integer(1)),
            ("mono", integer(17)),
            ("at", V::String("2026-10-01T00:00:00Z".into())),
        ]);
        let b = object([
            (
                "exec1_fedcba9876543210fedcba9876543210",
                V::String("op-bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb".into()),
            ),
            ("witness.json.00000000000000000000000000000000", integer(1)),
            ("mono", integer(99)),
            ("at", V::String("2027-01-01T12:34:56Z".into())),
        ]);
        assert_ne!(canonical_bytes(&a).unwrap(), canonical_bytes(&b).unwrap());
        assert_eq!(normalize(&a), normalize(&b));
        assert_eq!(normalized_sha256(&a), normalized_sha256(&b));
        // A structural difference survives: one more row, or a reused value
        // where the other run drew a fresh one.
        let c = object([
            (
                "exec1_0123456789abcdef0123456789abcdef",
                V::String("exec1_0123456789abcdef0123456789abcdef".into()),
            ),
            ("witness.json.ffffffffffffffffffffffffffffffff", integer(1)),
            ("mono", integer(17)),
            ("at", V::String("2026-10-01T00:00:00Z".into())),
        ]);
        assert_ne!(normalize(&a), normalize(&c));
        let d = object([("x", integer(1)), ("y", integer(2))]);
        let e = object([("x", integer(1)), ("y", integer(3))]);
        assert_ne!(normalized_sha256(&d), normalized_sha256(&e));
        // Inside a token: `run3:<64 hex>` and a temporary name's nonce.
        let s = "run3:5555555555555555555555555555555555555555555555555555555555555555";
        assert_eq!(
            Numbering {
                seen: BTreeMap::new(),
                next: BTreeMap::new()
            }
            .string(s),
            "run3:<h64:1>"
        );
        assert_eq!(
            shape_string("grant-journal.witness.json.0123456789abcdef0123456789abcdef"),
            "grant-journal.witness.json.<h32>"
        );
        // Plain words and short hex stay.
        assert_eq!(
            shape_string("x3b.append.seal COMMITTED cafe 2026"),
            "x3b.append.seal COMMITTED cafe 2026"
        );
    }
}
