// The D15 readers and membership decision (M3-B r9 items 19 to 24; unit
// B3-b2b1, B3-b plan r2 amendment A2; branch A's order, unit B3-b2b2b r3,
// amendment A4): B3-b0's `discover` (r4, contract successor 169) without
// SLM's two passes, over a `WorkspaceObservation`.
//
// Two readers, `cargo-config-patch@1` and `npm-workspaces-members@1`, read
// their carriers at W as data. The registry's rules then decide placement,
// the 64-member cap, membership, every entry's disposition and the links:
// branch A from the workspace-roots array or `--workspace-root`, branch B
// from the readers, and nothing when W is in a repository (W2 fails). The
// core never walks. Branch A decides its members before any walk (A4-2): the
// array gate, then the member decisions; the caller walks once with the
// admitted members and their index gitlinks, and only an accepted walk
// reaches the links (`phase_one`, then `links`). Every record the walk
// writes is B3-b2a's. Paths are W-relative (`""` is
// W); the composition spells them under W. Pure: every observation goes
// through the `WorkspaceObservation` the caller supplies.
use super::discovery_rule as rule;
use super::discovery_scan::{EntryJudgment, ObservedEntry, judge_entry};
use super::project_chain::ProjectObject;
use crate::grants::ProjectOwnerWaiver;
use opensip_identity::{JsonValue, RawSha256, TomlValueView, parse_json, parse_toml};
use std::collections::{BTreeMap, BTreeSet};

/// The two declaration readers, in record order.
pub(crate) const READERS: [&str; 2] = ["cargo-config-patch", "npm-workspaces-members"];
const CARGO: &str = READERS[0];
const NPM: &str = READERS[1];
/// D15's member cap (law M3-B item 24 row 5).
pub(crate) const MAX_MEMBERS: usize = 64;
/// M1's bound on a candidate's depth below W.
const MAX_DEPTH: usize = 256;
/// A reader carrier's bound.
pub(crate) const CARRIER_CAP: usize = 4 * 1024 * 1024;
/// The characters that make an npm entry a glob.
const GLOB: &[char] = &['*', '?', '[', ']', '{', '}', '!'];

/// What the core may observe below W, and nothing else. Every path is
/// W-relative. The test adapter reads B3-b0's synthetic tree; B3-b2b2's
/// native observation reads W's retained descriptor on the discovery ledger.
pub(crate) trait WorkspaceObservation {
    type Error;
    /// The entry at `rel`, or `None` when nothing is there.
    fn entry(&mut self, rel: &str) -> Result<Option<ObservedEntry>, Self::Error>;
    /// The VCS markers directory `rel` holds, each with whether it is a
    /// directory, in `.git`, `.hg`, `.svn`, `.jj` order.
    fn markers(&mut self, rel: &str) -> Result<Vec<(&'static str, bool)>, Self::Error>;
    /// The names of directory `rel`'s children.
    fn children(&mut self, rel: &str) -> Result<Vec<String>, Self::Error>;
    /// A regular file's bytes, after its custody passed.
    fn bytes(&mut self, rel: &str) -> Result<FileBytes, Self::Error>;
    /// The entry at `rel` as a custody judgment needs it: with its ACL
    /// captured where the judgment of `object` would need it, from the very
    /// object observed (r2, Codex B3B2B2B-R1-RF-2 and RF-4). Every custody
    /// judgment the core makes is of an entry from here.
    fn custody_entry(
        &mut self,
        rel: &str,
        object: ProjectObject,
    ) -> Result<Option<ObservedEntry>, Self::Error>;
    /// Item 6b's outcome for one counted candidate. The core asks in path
    /// order, only for candidates whose directories passed custody, and in
    /// branch A stops at the first refusal (Codex B3B2B1-R1-RF-2). The
    /// pass-level sources are the observation's to check once per decision.
    fn member_verdict(&mut self, candidate: &str) -> Result<MemberOutcome, Self::Error>;
}

/// Item 6b's outcome for one candidate.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) enum MemberOutcome {
    /// Admitted, with its index's gitlink paths, member-relative: nested
    /// repositories inside the member, which stay boundaries (law M3-B r9
    /// items 21 and 22; r2, Codex B3B2B2B-R1-RF-1).
    Admitted { gitlinks: Vec<String> },
    /// Refused, with its subject.
    Refused(String),
}

/// A bounded read's outcome.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) enum FileBytes {
    Read(Vec<u8>),
    /// Longer than `CARRIER_CAP`.
    TooLarge,
}

/// The invocation facts the decision needs.
pub(crate) struct DecisionInputs<'a> {
    pub(crate) invoking_uid: u32,
    pub(crate) groups: &'a BTreeSet<u32>,
    /// The owner waiver, when it applies (explicit `--project` with
    /// `--trust-project-owner`). It reaches member directories, never files
    /// or Git evidence (law item 23).
    pub(crate) waiver: Option<&'a ProjectOwnerWaiver>,
    /// Item 6a observed W in no repository (W2).
    pub(crate) no_repository: bool,
    /// The workspace-roots array (branch A), with its source; empty for
    /// branch B.
    pub(crate) array: &'a [String],
    pub(crate) array_source: ArraySource,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum ArraySource {
    ConfigWorkspaceRoots,
    ExplicitJoins,
}
impl ArraySource {
    pub(crate) fn as_str(self) -> &'static str {
        match self {
            Self::ConfigWorkspaceRoots => "config-workspace-roots",
            Self::ExplicitJoins => "explicit-joins",
        }
    }
    /// SLM's detail for an array longer than its bound, for this source.
    fn too_many(self) -> &'static str {
        match self {
            Self::ConfigWorkspaceRoots => "TOO_MANY_WORKSPACE_ROOTS",
            Self::ExplicitJoins => "TOO_MANY_JOINS",
        }
    }
}

/// A reader's declaration row state.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum ReaderState {
    Absent,
    Read,
    Refused,
}
impl ReaderState {
    pub(crate) fn as_str(self) -> &'static str {
        match self {
            Self::Absent => "absent",
            Self::Read => "read",
            Self::Refused => "refused",
        }
    }
}

/// An entry the reader could not use, with the registry's reason.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct Unresolved {
    pub(crate) entry: String,
    pub(crate) reason: &'static str,
    pub(crate) subject: Option<String>,
}

/// One `workspaceDeclarations` row.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct DeclarationRow {
    pub(crate) reader: &'static str,
    pub(crate) state: ReaderState,
    pub(crate) path: Option<String>,
    pub(crate) content_sha256: Option<String>,
    pub(crate) state_subject: Option<String>,
    /// Sorted by entry (bytes); empty unless the carrier was read.
    pub(crate) unresolved: Vec<Unresolved>,
}

/// What declared a member.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) enum Declarer {
    Reader {
        reader: &'static str,
        path: String,
        content_sha256: String,
    },
    Array {
        source: ArraySource,
        path: String,
    },
}
impl Declarer {
    fn sort_key(&self) -> (&'static str, &str) {
        match self {
            Self::Reader { path, .. } => ("reader", path),
            Self::Array { source, path } => (source.as_str(), path),
        }
    }
}

/// An admitted member and what declared it.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct MemberRow {
    pub(crate) path: String,
    pub(crate) declared_by: Vec<Declarer>,
}

/// A link: a package a member provides, by declaration (plan r2 LD-B3B-3).
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct LinkRow {
    pub(crate) ecosystem: &'static str,
    pub(crate) package_name: String,
    pub(crate) provider_member: String,
    pub(crate) package_dir: String,
    pub(crate) provided_version: String,
    pub(crate) cargo_patch_source: Option<String>,
    pub(crate) declared_by: &'static str,
}

/// A member rule's refusal (law item 24 rows 2 and 5).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum MemberRefusal {
    RootCustodyRefused,
    ScopeLimit,
}
impl MemberRefusal {
    pub(crate) fn code(self) -> &'static str {
        match self {
            Self::RootCustodyRefused => "PROJECT.ROOT_CUSTODY_REFUSED",
            Self::ScopeLimit => "PROJECT.SCOPE_LIMIT",
        }
    }
}

/// The decision.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) enum Decision {
    /// The member set is final: the walk runs with these members, and with
    /// their index gitlinks (W-relative, sorted) as nested repositories.
    Members {
        members: Vec<MemberRow>,
        gitlinks: Vec<String>,
        declarations: Vec<DeclarationRow>,
        links: Vec<LinkRow>,
    },
    /// A member rule refused. The record carries the provenance of the
    /// discovery without members (LD-B3B0-5): the walk runs with none.
    Refuse {
        refusal: MemberRefusal,
        path: String,
        detail: String,
        declarations: Vec<DeclarationRow>,
    },
    /// (r3, plan amendment A4-2) Branch A's array gate refused, before any
    /// member is decided: `PROJECT.EXPLICIT_PATH_INVALID` with SLM's record
    /// for the array's size (`path` `None`) or its first malformed root
    /// (`path` the root's raw text). The record carries the provenance of
    /// the discovery without members (LD-B3B0-5).
    ArrayRefused {
        path: Option<String>,
        detail: &'static str,
        declarations: Vec<DeclarationRow>,
    },
}

/// Phase one's outcome.
pub(crate) enum PhaseOne<'a> {
    Decided(Decision),
    /// Branch A, its members decided (A4-2): walk once with `members()` and
    /// `gitlinks()`; a refusal is the result, with `declarations()` and no
    /// members, and an accepted walk reaches `links`.
    Admitted(Admitted<'a>),
}

/// Branch A between its member decisions and its links.
pub(crate) struct Admitted<'a> {
    state: State<'a>,
    members: Vec<String>,
    declared_by: BTreeMap<String, Vec<Declarer>>,
    gitlinks: BTreeMap<String, Vec<String>>,
}
impl Admitted<'_> {
    /// The admitted members, ascending: the walk's member roots.
    pub(crate) fn members(&self) -> &[String] {
        &self.members
    }
    /// Their index gitlinks, W-relative and ascending: the walk's nested
    /// repositories.
    pub(crate) fn gitlinks(&self) -> Vec<String> {
        boundaries(&self.gitlinks)
    }
    /// The `workspaceDeclarations` rows as they stand at the walk, the rows a
    /// walk refusal carries.
    pub(crate) fn declarations(&self) -> Vec<DeclarationRow> {
        self.state.declarations()
    }
}

/// The admitted members' gitlinks (member-relative), W-relative, ascending.
fn boundaries(gitlinks: &BTreeMap<String, Vec<String>>) -> Vec<String> {
    let mut out: Vec<String> = gitlinks
        .iter()
        .flat_map(|(member, links)| links.iter().map(move |g| join(member, g)))
        .collect();
    out.sort_by(bytewise);
    out.dedup();
    out
}

// ------------------------------------------------------------------ paths

fn join(dir: &str, name: &str) -> String {
    if dir.is_empty() {
        name.to_owned()
    } else {
        format!("{dir}/{name}")
    }
}
fn parent(rel: &str) -> &str {
    rel.rsplit_once('/').map_or("", |(p, _)| p)
}
/// `rel` is at or below `base`; every path is below W (`""`).
fn within(rel: &str, base: &str) -> bool {
    base.is_empty() || rel == base || rel.strip_prefix(base).is_some_and(|r| r.starts_with('/'))
}
fn bytewise(a: &String, b: &String) -> std::cmp::Ordering {
    a.as_bytes().cmp(b.as_bytes())
}

/// `(rel, None)` for a canonical relative directory, else the reason.
fn entry_path(text: &str) -> Result<String, &'static str> {
    if text.starts_with('/') || text.split('/').any(|s| s == "..") {
        return Err("entry-path-outside-root");
    }
    if text.is_empty()
        || text.split('/').any(|s| s.is_empty() || s == ".")
        || text.contains('\0')
        || text.contains('\\')
    {
        return Err("entry-path-grammar");
    }
    Ok(text.to_owned())
}

// ------------------------------------------------------------------ the decision

/// One reader entry.
struct Entry {
    reader: &'static str,
    entry: String,
    /// A Cargo patch's `path`, or `None` when the spec is not `{ path }`.
    cargo_path: Option<String>,
    /// A Cargo patch's (source, name).
    cargo: Option<(String, String)>,
    directory: Option<String>,
    placement: Option<Placement>,
}

#[derive(Default, Clone)]
struct Placement {
    absent: bool,
    candidate: Option<String>,
    offvolume: bool,
    offvolume_at_or_before_candidate: bool,
    inner: bool,
}

/// The rows, the entries' dispositions and the inputs, carried between the
/// phases.
struct State<'a> {
    rows: BTreeMap<&'static str, DeclarationRow>,
    unresolved: BTreeMap<&'static str, Vec<Unresolved>>,
    decided: BTreeMap<&'static str, BTreeSet<String>>,
    placed: Vec<Entry>,
    uid: u32,
    groups: BTreeSet<u32>,
    waiver: Option<&'a ProjectOwnerWaiver>,
}
impl State<'_> {
    fn disclose(
        &mut self,
        reader: &'static str,
        entry: &str,
        reason: &'static str,
        subject: Option<String>,
    ) {
        let decided = self.decided.entry(reader).or_default();
        if !decided.insert(entry.to_owned()) {
            return;
        }
        self.unresolved.entry(reader).or_default().push(Unresolved {
            entry: entry.to_owned(),
            reason,
            subject,
        });
    }
    fn decide(&mut self, reader: &'static str, entry: &str) {
        self.decided
            .entry(reader)
            .or_default()
            .insert(entry.to_owned());
    }
    fn is_decided(&self, reader: &'static str, entry: &str) -> bool {
        self.decided.get(reader).is_some_and(|d| d.contains(entry))
    }
    /// The `workspaceDeclarations` rows as they stand.
    fn declarations(&self) -> Vec<DeclarationRow> {
        READERS
            .iter()
            .map(|reader| {
                let mut row = self.rows[reader].clone();
                if row.state == ReaderState::Read {
                    let mut unresolved = self.unresolved.get(reader).cloned().unwrap_or_default();
                    unresolved.sort_by(|a, b| a.entry.as_bytes().cmp(b.entry.as_bytes()));
                    row.unresolved = unresolved;
                }
                row
            })
            .collect()
    }
    fn refuse(&self, refusal: MemberRefusal, path: &str, detail: String) -> Decision {
        Decision::Refuse {
            refusal,
            path: path.to_owned(),
            detail,
            declarations: self.declarations(),
        }
    }
    fn custody(
        &self,
        entry: Option<&ObservedEntry>,
        object: ProjectObject,
        waive: bool,
    ) -> Option<&'static str> {
        let waiver = if waive { self.waiver } else { None };
        match judge_entry(entry, object, self.uid, &self.groups, waiver) {
            EntryJudgment::Passed => None,
            EntryJudgment::Refused(refusal) => Some(refusal.code()),
            // An observation always captures the ACL its judgment needs; an
            // uncaptured one is never a pass.
            EntryJudgment::NeedsAcl => Some(super::Refusal::AclUnreadable.code()),
        }
    }
}

fn is_file(entry: &Option<ObservedEntry>) -> bool {
    entry
        .as_ref()
        .is_some_and(|e| e.metadata.mode & 0o170000 == 0o100000)
}
fn is_dir(entry: &Option<ObservedEntry>) -> bool {
    entry
        .as_ref()
        .is_some_and(|e| e.metadata.mode & 0o170000 == 0o040000)
}

fn sha256_hex(raw: &[u8]) -> Option<String> {
    let digest = RawSha256::new().update(raw).ok()?.finish();
    Some(digest.iter().map(|b| format!("{b:02x}")).collect())
}

/// A reader's carrier: its row and its entries (B3-b0 `_carrier`).
fn carrier<O: WorkspaceObservation>(
    obs: &mut O,
    state: &State<'_>,
    reader: &'static str,
) -> Result<(DeclarationRow, Option<Vec<Entry>>), O::Error> {
    let mut row = DeclarationRow {
        reader,
        state: ReaderState::Absent,
        path: None,
        content_sha256: None,
        state_subject: None,
        unresolved: Vec::new(),
    };
    let candidates: &[&str] = if reader == CARGO {
        &[".cargo/config.toml", ".cargo/config"]
    } else {
        &["package.json"]
    };
    let mut names = Vec::new();
    for name in candidates {
        if obs.entry(name)?.is_some() {
            names.push(*name);
        }
    }
    if names.len() == 2 {
        row.state = ReaderState::Refused;
        row.state_subject = Some("carrier-ambiguous".to_owned());
        return Ok((row, None));
    }
    let Some(path) = names.first().copied() else {
        return Ok((row, None));
    };
    row.path = Some(path.to_owned());
    let refused = |mut row: DeclarationRow, subject: String| {
        row.state = ReaderState::Refused;
        row.state_subject = Some(subject);
        Ok((row, None))
    };
    // Directory custody from the carrier's directory up to W, then the
    // carrier's config-file custody (the owner waiver reaches directories,
    // never files).
    let mut directory = parent(path);
    loop {
        let entry = obs.custody_entry(directory, ProjectObject::Directory)?;
        if let Some(why) = state.custody(entry.as_ref(), ProjectObject::Directory, true) {
            return refused(row, format!("custody:{why}"));
        }
        if directory.is_empty() {
            break;
        }
        directory = parent(directory);
    }
    let entry = obs.custody_entry(path, ProjectObject::ConfigurationFile)?;
    if let Some(why) = state.custody(entry.as_ref(), ProjectObject::ConfigurationFile, false) {
        return refused(row, format!("custody:{why}"));
    }
    let raw = match obs.bytes(path)? {
        FileBytes::Read(raw) => raw,
        FileBytes::TooLarge => return refused(row, "custody:TOO_LARGE".to_owned()),
    };
    row.content_sha256 = sha256_hex(&raw);
    if row.content_sha256.is_none() {
        return refused(row, "custody:TOO_LARGE".to_owned());
    }
    if reader == CARGO {
        // Every parse_toml error, its resource bounds included, is `parse`
        // (plan amendment A2 r2; the G2 precedent).
        let Ok(doc) = parse_toml(&raw) else {
            return refused(row, "parse".to_owned());
        };
        let mut entries = Vec::new();
        if let Some(patch) = doc.table().get("patch") {
            let Some(patch) = patch.as_table() else {
                return refused(row, "parse".to_owned());
            };
            let mut tables = Vec::new();
            for (source, table) in patch.iter() {
                let Some(table) = table.as_table() else {
                    return refused(row, "parse".to_owned());
                };
                tables.push((source, table));
            }
            for (source, table) in tables {
                for (name, spec) in table.iter() {
                    entries.push(Entry {
                        reader,
                        entry: format!("patch.{source}.{name}"),
                        cargo_path: patch_path(spec),
                        cargo: Some((source.to_owned(), name.to_owned())),
                        directory: None,
                        placement: None,
                    });
                }
            }
        }
        row.state = ReaderState::Read;
        return Ok((row, Some(entries)));
    }
    let Ok(JsonValue::Object(doc)) = parse_json(&raw) else {
        return refused(row, "parse".to_owned());
    };
    let Some(workspaces) = doc.get("workspaces") else {
        row.state = ReaderState::Read;
        return Ok((row, Some(Vec::new())));
    };
    let JsonValue::Array(items) = workspaces else {
        return refused(row, "workspaces-shape-unsupported".to_owned());
    };
    let mut entries = Vec::new();
    for item in items {
        let JsonValue::String(text) = item else {
            return refused(row, "workspaces-shape-unsupported".to_owned());
        };
        entries.push(Entry {
            reader,
            entry: text.clone(),
            cargo_path: None,
            cargo: None,
            directory: None,
            placement: None,
        });
    }
    row.state = ReaderState::Read;
    Ok((row, Some(entries)))
}

/// A Cargo patch spec's path, only for exactly `{ path = "<string>" }`.
fn patch_path(spec: TomlValueView<'_>) -> Option<String> {
    let table = spec.as_table()?;
    if table.len() != 1 {
        return None;
    }
    table.get("path")?.as_str().map(str::to_owned)
}

/// The placement of entry directory `rel` (B3-b0 `_place`).
fn place<O: WorkspaceObservation>(obs: &mut O, rel: &str) -> Result<Placement, O::Error> {
    let mut out = Placement::default();
    let dev = obs.entry("")?.map(|e| e.metadata.device);
    let mut cargo = BTreeSet::new();
    if is_file(&obs.entry("Cargo.toml")?) {
        cargo.insert(String::new());
    }
    let parts: Vec<&str> = rel.split('/').collect();
    for i in 0..parts.len() {
        let prefix = parts[..=i].join("/");
        let members: BTreeSet<String> = out.candidate.iter().cloned().collect();
        if rule::classify_path(&prefix, &cargo, &members).is_some() {
            // A pruned anchor: never entered, nothing below it consulted.
            out.inner = true;
            return Ok(out);
        }
        let entry = obs.entry(&prefix)?;
        if !is_dir(&entry) {
            out.absent = true;
            return Ok(out);
        }
        if entry.as_ref().map(|e| e.metadata.device) != dev && !out.offvolume {
            out.offvolume = true;
            out.offvolume_at_or_before_candidate = out.candidate.is_none();
        }
        if out.candidate.is_none() {
            if !obs.markers(&prefix)?.is_empty() {
                out.candidate = Some(prefix.clone());
                if out.offvolume {
                    out.offvolume_at_or_before_candidate = true;
                }
            }
        } else if !obs.markers(&prefix)?.is_empty()
            || is_file(&obs.entry(&join(&prefix, "opensip.json"))?)
        {
            out.inner = true;
        }
        if is_file(&obs.entry(&join(&prefix, "Cargo.toml"))?) {
            cargo.insert(prefix);
        }
    }
    Ok(out)
}

/// The repositories a downward walk from W can lawfully see, for npm globs
/// (B3-b0 `_visible_repositories`): never into a pruned anchor or past a
/// boundary.
fn visible_repositories<O: WorkspaceObservation>(obs: &mut O) -> Result<Vec<String>, O::Error> {
    let mut cargo = BTreeSet::new();
    if is_file(&obs.entry("Cargo.toml")?) {
        cargo.insert(String::new());
    }
    let none = BTreeSet::new();
    let mut repos = Vec::new();
    let mut queue = std::collections::VecDeque::new();
    queue.push_back((String::new(), 0usize));
    while let Some((dir, depth)) = queue.pop_front() {
        let mut names = obs.children(&dir)?;
        names.sort_by(bytewise);
        for name in names {
            let rel = join(&dir, &name);
            if rule::classify_path(&rel, &cargo, &none).is_some() {
                continue;
            }
            if !is_dir(&obs.entry(&rel)?) || depth + 1 > MAX_DEPTH {
                continue;
            }
            if !obs.markers(&rel)?.is_empty() {
                repos.push(rel);
                continue;
            }
            if is_file(&obs.entry(&join(&rel, "opensip.json"))?) {
                continue;
            }
            if is_file(&obs.entry(&join(&rel, "Cargo.toml"))?) {
                cargo.insert(rel.clone());
            }
            queue.push_back((rel, depth + 1));
        }
    }
    Ok(repos)
}

/// Candidate R's placement verdict before 6b (B3-b0 `_candidate_failure`):
/// `(true, subject)` when the repository cannot become a member (a boundary),
/// `(false, subject)` for a placement failure.
fn candidate_failure<O: WorkspaceObservation>(
    obs: &mut O,
    candidate: &str,
) -> Result<Option<(bool, &'static str)>, O::Error> {
    let parts: Vec<&str> = candidate.split('/').collect();
    for i in 1..parts.len() {
        let between = parts[..i].join("/");
        if is_file(&obs.entry(&join(&between, "opensip.json"))?) {
            return Ok(Some((true, "JOIN_CROSSES_NESTED_PROJECT")));
        }
    }
    if parts.len() > MAX_DEPTH {
        return Ok(Some((false, "DEPTH")));
    }
    let markers = obs.markers(candidate)?;
    if markers.len() != 1 || markers[0].0 != ".git" {
        return Ok(Some((false, "member-vcs-unsupported:vcs-other")));
    }
    if !markers[0].1 {
        return Ok(Some((false, "member-vcs-unsupported:git-not-directory")));
    }
    Ok(None)
}

/// Directory custody of every directory from W's child to R, with the owner
/// waiver: the first failing directory and its reason.
fn member_custody<O: WorkspaceObservation>(
    obs: &mut O,
    state: &State<'_>,
    candidate: &str,
) -> Result<Option<(String, &'static str)>, O::Error> {
    let parts: Vec<&str> = candidate.split('/').collect();
    for i in 1..=parts.len() {
        let dir = parts[..i].join("/");
        let entry = obs.custody_entry(&dir, ProjectObject::Directory)?;
        if let Some(why) = state.custody(entry.as_ref(), ProjectObject::Directory, true) {
            return Ok(Some((dir, why)));
        }
    }
    Ok(None)
}

/// Phase one: the readers, every entry's shape and placement, and either the
/// decision (W in a repository, branch B, or a branch-A refusal) or branch
/// A's admitted members for its one walk.
pub(crate) fn phase_one<'a, O: WorkspaceObservation>(
    obs: &mut O,
    inputs: &DecisionInputs<'a>,
) -> Result<PhaseOne<'a>, O::Error> {
    let mut state = State {
        rows: BTreeMap::new(),
        unresolved: BTreeMap::new(),
        decided: BTreeMap::new(),
        placed: Vec::new(),
        uid: inputs.invoking_uid,
        groups: inputs.groups.clone(),
        waiver: inputs.waiver,
    };
    let w2 = inputs.no_repository;
    let mut entries: BTreeMap<&'static str, Vec<Entry>> = BTreeMap::new();
    for reader in READERS {
        let (row, read) = carrier(obs, &state, reader)?;
        state.rows.insert(reader, row);
        entries.insert(reader, read.unwrap_or_default());
    }
    let mut visible: Option<Vec<String>> = None;
    for reader in READERS {
        let mut seen = BTreeSet::new();
        for mut e in entries.remove(reader).unwrap_or_default() {
            if !seen.insert(e.entry.clone()) {
                continue;
            }
            let text = if reader == CARGO {
                match e.cargo_path.clone() {
                    Some(path) => path,
                    None => {
                        if w2 {
                            state.disclose(reader, &e.entry, "patch-entry-not-path", None);
                        } else {
                            state.decide(reader, &e.entry);
                        }
                        continue;
                    }
                }
            } else {
                let text = e.entry.clone();
                if text.contains(GLOB) {
                    if w2 {
                        let literal: Vec<&str> = text
                            .split('/')
                            .take_while(|seg| !seg.contains(GLOB))
                            .collect();
                        let prefix = literal.join("/");
                        if visible.is_none() {
                            visible = Some(visible_repositories(obs)?);
                        }
                        let crosses = visible.as_ref().is_some_and(|repos| {
                            repos.iter().any(|r| {
                                within(r, &prefix) || (!prefix.is_empty() && within(&prefix, r))
                            })
                        });
                        if crosses {
                            state.disclose(
                                reader,
                                &e.entry,
                                "workspace-glob-crosses-repository",
                                None,
                            );
                        } else {
                            state.decide(reader, &e.entry);
                        }
                    } else {
                        state.decide(reader, &e.entry);
                    }
                    continue;
                }
                text
            };
            let rel = match entry_path(&text) {
                Ok(rel) => rel,
                Err(why) => {
                    if w2 {
                        state.disclose(reader, &e.entry, why, None);
                    } else {
                        state.decide(reader, &e.entry);
                    }
                    continue;
                }
            };
            let placement = place(obs, &rel)?;
            if placement.absent {
                if w2 {
                    state.disclose(reader, &e.entry, "entry-path-absent", None);
                } else {
                    state.decide(reader, &e.entry);
                }
                continue;
            }
            e.directory = Some(rel);
            e.placement = Some(placement);
            state.placed.push(e);
        }
    }

    if !w2 {
        // Root in a repository: the readers declare nothing and derive no
        // link. A literal entry inside a nested repository is disclosed; no
        // other entry is recorded (law item 24 row 6).
        let placed = std::mem::take(&mut state.placed);
        for e in &placed {
            if placement(e).candidate.is_some() {
                state.disclose(
                    e.reader,
                    &e.entry,
                    "member-excluded",
                    Some("workspace-root-inside-repository".to_owned()),
                );
            } else {
                state.decide(e.reader, &e.entry);
            }
        }
        return Ok(PhaseOne::Decided(Decision::Members {
            members: Vec::new(),
            gitlinks: Vec::new(),
            declarations: state.declarations(),
            links: Vec::new(),
        }));
    }

    if !inputs.array.is_empty() {
        return branch_a(obs, state, inputs);
    }

    // Branch B: the readers declare members by placement alone.
    let mut by_candidate: BTreeSet<String> = BTreeSet::new();
    for e in &state.placed {
        let p = placement(e);
        if p.offvolume {
            continue;
        }
        if let Some(candidate) = &p.candidate {
            by_candidate.insert(candidate.clone());
        }
    }
    let offvol: BTreeSet<String> = state
        .placed
        .iter()
        .filter_map(|e| {
            let p = placement(e);
            (p.offvolume && p.offvolume_at_or_before_candidate)
                .then(|| p.candidate.clone())
                .flatten()
        })
        .collect();
    let mut all: Vec<String> = by_candidate.union(&offvol).cloned().collect();
    all.sort_by(bytewise);
    let mut placed_ok = Vec::new();
    let mut excluded: BTreeMap<String, String> = BTreeMap::new();
    for candidate in all {
        let bad = candidate_failure(obs, &candidate)?;
        if offvol.contains(&candidate) {
            excluded.insert(candidate, "member-outside-volume".to_owned());
        } else if let Some((_, subject)) = bad {
            excluded.insert(candidate, subject.to_owned());
        } else {
            placed_ok.push(candidate);
        }
    }
    if placed_ok.len() > MAX_MEMBERS {
        return Ok(PhaseOne::Decided(state.refuse(
            MemberRefusal::ScopeLimit,
            "",
            format!("members:{}>{MAX_MEMBERS}", placed_ok.len()),
        )));
    }
    let mut members = Vec::new();
    let mut gitlinks = BTreeMap::new();
    for candidate in placed_ok {
        if let Some((_, why)) = member_custody(obs, &state, &candidate)? {
            excluded.insert(candidate, format!("DIRECTORY_CUSTODY:{why}"));
            continue;
        }
        match obs.member_verdict(&candidate)? {
            MemberOutcome::Refused(subject) => {
                excluded.insert(candidate, subject);
            }
            MemberOutcome::Admitted { gitlinks: links } => {
                gitlinks.insert(candidate.clone(), links);
                members.push(candidate);
            }
        }
    }
    let mut declared_by: BTreeMap<String, Vec<Declarer>> = BTreeMap::new();
    let placed = std::mem::take(&mut state.placed);
    for e in &placed {
        let p = placement(e);
        if p.offvolume {
            state.disclose(
                e.reader,
                &e.entry,
                "member-excluded",
                Some("member-outside-volume".to_owned()),
            );
            continue;
        }
        let Some(candidate) = &p.candidate else {
            state.disclose(e.reader, &e.entry, "entry-not-in-a-member", None);
            continue;
        };
        if let Some(subject) = excluded.get(candidate) {
            state.disclose(e.reader, &e.entry, "member-excluded", Some(subject.clone()));
            continue;
        }
        let row = &state.rows[e.reader];
        let declarer = Declarer::Reader {
            reader: e.reader,
            path: row.path.clone().unwrap_or_default(),
            content_sha256: row.content_sha256.clone().unwrap_or_default(),
        };
        let list = declared_by.entry(candidate.clone()).or_default();
        if !list.contains(&declarer) {
            list.push(declarer);
        }
    }
    state.placed = placed;
    Ok(PhaseOne::Decided(finish(
        obs,
        state,
        members,
        declared_by,
        gitlinks,
    )?))
}

/// Branch A's members (r3, plan amendment A4-2), decided before any walk so
/// that item 6b's index gitlinks bound every descent. Public priority: the
/// array's size, then grammar for the whole array, then the member rules in
/// path order; the walk's refusals come after (the caller's).
fn branch_a<'a, O: WorkspaceObservation>(
    obs: &mut O,
    state: State<'a>,
    inputs: &DecisionInputs<'a>,
) -> Result<PhaseOne<'a>, O::Error> {
    // 1. The array gate: pure, no observation. SLM's own records for its
    //    first two array checks, with the shared rule's bound and grammar.
    if inputs.array.len() > rule::MAX_WORKSPACE_UNITS {
        return Ok(PhaseOne::Decided(Decision::ArrayRefused {
            path: None,
            detail: inputs.array_source.too_many(),
            declarations: state.declarations(),
        }));
    }
    if let Some(spec) = inputs
        .array
        .iter()
        .find(|spec| rule::normalize_explicit_root(spec).is_err())
    {
        return Ok(PhaseOne::Decided(Decision::ArrayRefused {
            path: Some(spec.clone()),
            detail: "JOIN_PATH_GRAMMAR",
            declarations: state.declarations(),
        }));
    }
    // 2. The member decisions, in path order, each stopping at the first
    //    refusal: placement and other volumes (row 2), the cap (row 5), then
    //    directory custody and item 6b per candidate (row 2). The placement
    //    lookups that form and count the candidates precede them; nothing
    //    below a candidate is listed, judged or read before its admission.
    let mut candidates: BTreeMap<String, Vec<Declarer>> = BTreeMap::new();
    let mut offvolume: BTreeMap<String, String> = BTreeMap::new();
    for spec in inputs.array {
        let Ok(rel) = rule::normalize_explicit_root(spec) else {
            continue;
        };
        if rel.is_empty() {
            continue;
        }
        let placement = place(obs, &rel)?;
        let Some(candidate) = placement.candidate.clone().filter(|_| !placement.absent) else {
            continue;
        };
        candidates
            .entry(candidate.clone())
            .or_default()
            .push(Declarer::Array {
                source: inputs.array_source,
                path: rel.clone(),
            });
        if placement.offvolume {
            offvolume.entry(candidate).or_insert(rel);
        }
    }
    // A candidate behind a nested project (LD-B3B0-7's boundary kind) stays
    // withheld: a root inside it refuses in the walk.
    let mut provisional = Vec::new();
    for candidate in candidates.keys() {
        if !matches!(candidate_failure(obs, candidate)?, Some((true, _))) {
            provisional.push(candidate.clone());
        }
    }
    provisional.sort_by(bytewise);
    for candidate in &provisional {
        if let Some((_, subject)) = candidate_failure(obs, candidate)? {
            return Ok(PhaseOne::Decided(state.refuse(
                MemberRefusal::RootCustodyRefused,
                candidate,
                subject.to_owned(),
            )));
        }
        if let Some(path) = offvolume.get(candidate) {
            return Ok(PhaseOne::Decided(state.refuse(
                MemberRefusal::RootCustodyRefused,
                path,
                "member-outside-volume".to_owned(),
            )));
        }
    }
    if provisional.len() > MAX_MEMBERS {
        return Ok(PhaseOne::Decided(state.refuse(
            MemberRefusal::ScopeLimit,
            "",
            format!("members:{}>{MAX_MEMBERS}", provisional.len()),
        )));
    }
    // Directory custody, then 6b, for each candidate in path order; the
    // first refusal ends the decision, and no later candidate is observed
    // (r2, Codex B3B2B1-R1-RF-2).
    let mut gitlinks = BTreeMap::new();
    for candidate in &provisional {
        if let Some((dir, why)) = member_custody(obs, &state, candidate)? {
            return Ok(PhaseOne::Decided(state.refuse(
                MemberRefusal::RootCustodyRefused,
                &dir,
                why.to_owned(),
            )));
        }
        match obs.member_verdict(candidate)? {
            MemberOutcome::Refused(subject) => {
                return Ok(PhaseOne::Decided(state.refuse(
                    MemberRefusal::RootCustodyRefused,
                    candidate,
                    subject,
                )));
            }
            MemberOutcome::Admitted { gitlinks: links } => {
                gitlinks.insert(candidate.clone(), links);
            }
        }
    }
    let members = provisional;
    let mut declared_by = BTreeMap::new();
    for member in &members {
        declared_by.insert(
            member.clone(),
            candidates.remove(member).unwrap_or_default(),
        );
    }
    Ok(PhaseOne::Admitted(Admitted {
        state,
        members,
        declared_by,
        gitlinks,
    }))
}

/// Branch A after its walk accepted (step 3 of A4-2 is the caller's): the
/// readers declare nothing and link into array members only.
pub(crate) fn links<O: WorkspaceObservation>(
    obs: &mut O,
    admitted: Admitted<'_>,
) -> Result<Decision, O::Error> {
    let Admitted {
        mut state,
        members,
        declared_by,
        gitlinks,
    } = admitted;
    let placed = std::mem::take(&mut state.placed);
    for e in &placed {
        let p = placement(e);
        if p.offvolume {
            state.disclose(
                e.reader,
                &e.entry,
                "member-excluded",
                Some("member-outside-volume".to_owned()),
            );
        } else if p.candidate.is_none() {
            state.disclose(e.reader, &e.entry, "entry-not-in-a-member", None);
        } else if !p.candidate.as_ref().is_some_and(|c| members.contains(c)) {
            state.disclose(e.reader, &e.entry, "dropped-workspace-roots-present", None);
        }
    }
    state.placed = placed;
    finish(obs, state, members, declared_by, gitlinks)
}

fn placement(e: &Entry) -> &Placement {
    e.placement
        .as_ref()
        .expect("a placed entry carries its placement")
}

/// Links, only after membership is final and only inside admitted members,
/// never from a directory the member's analyzed tree excludes; then the
/// decision.
fn finish<O: WorkspaceObservation>(
    obs: &mut O,
    mut state: State<'_>,
    mut members: Vec<String>,
    mut declared_by: BTreeMap<String, Vec<Declarer>>,
    gitlinks: BTreeMap<String, Vec<String>>,
) -> Result<Decision, O::Error> {
    let placed = std::mem::take(&mut state.placed);
    let mut candidates: Vec<(&Entry, LinkRow)> = Vec::new();
    for e in &placed {
        let p = placement(e);
        let Some(candidate) = p.candidate.as_ref().filter(|c| members.contains(c)) else {
            continue;
        };
        if state.is_decided(e.reader, &e.entry) {
            continue;
        }
        // An entry at or below one of the member's index gitlinks is inside a
        // nested repository of the member, as an inner boundary is (r2, Codex
        // B3B2B2B-R1-RF-1).
        let dir = e.directory.as_deref().unwrap_or_default();
        let below_gitlink = gitlinks
            .get(candidate)
            .is_some_and(|links| links.iter().any(|g| within(dir, &join(candidate, g))));
        if p.inner || below_gitlink {
            state.disclose(e.reader, &e.entry, "entry-not-in-a-member", None);
            continue;
        }
        match link(obs, &state, e, candidate)? {
            Ok(row) => candidates.push((e, row)),
            Err((reason, subject)) => state.disclose(e.reader, &e.entry, reason, subject),
        }
    }
    let mut links: Vec<LinkRow> = Vec::new();
    for ecosystem in ["cargo", "npm"] {
        let mut by_name: Vec<(String, Vec<(&Entry, &LinkRow)>)> = Vec::new();
        for (e, row) in &candidates {
            if row.ecosystem != ecosystem {
                continue;
            }
            match by_name
                .iter_mut()
                .find(|(name, _)| name == &row.package_name)
            {
                Some((_, group)) => group.push((e, row)),
                None => by_name.push((row.package_name.clone(), vec![(e, row)])),
            }
        }
        for (_, group) in by_name {
            let dirs: BTreeSet<&String> = group.iter().map(|(_, row)| &row.package_dir).collect();
            if dirs.len() > 1 {
                for (e, _) in &group {
                    state.disclose(e.reader, &e.entry, "ambiguous-provider", None);
                }
            } else {
                for (e, row) in group {
                    state.decide(e.reader, &e.entry);
                    if !links.contains(row) {
                        links.push(row.clone());
                    }
                }
            }
        }
    }
    for e in &placed {
        state.decide(e.reader, &e.entry);
    }
    members.sort_by(bytewise);
    let rows = members
        .into_iter()
        .map(|path| {
            let mut declared = declared_by.remove(&path).unwrap_or_default();
            declared.sort_by(|a, b| {
                let (sa, pa) = a.sort_key();
                let (sb, pb) = b.sort_key();
                (sa, pa.as_bytes()).cmp(&(sb, pb.as_bytes()))
            });
            MemberRow {
                path,
                declared_by: declared,
            }
        })
        .collect();
    links.sort_by(|a, b| {
        (
            a.ecosystem,
            a.package_name.as_bytes(),
            a.package_dir.as_bytes(),
        )
            .cmp(&(
                b.ecosystem,
                b.package_name.as_bytes(),
                b.package_dir.as_bytes(),
            ))
    });
    Ok(Decision::Members {
        members: rows,
        gitlinks: boundaries(&gitlinks),
        declarations: state.declarations(),
        links,
    })
}

/// A provider manifest read as data under config-file custody (B3-b0
/// `_manifest`): the document, or the unusable subject.
enum Manifest {
    Toml(Vec<u8>),
    Json(JsonValue),
}
fn manifest<O: WorkspaceObservation>(
    obs: &mut O,
    state: &State<'_>,
    rel: &str,
) -> Result<Result<Manifest, String>, O::Error> {
    let entry = obs.custody_entry(rel, ProjectObject::ConfigurationFile)?;
    if entry.is_none() {
        return Ok(Err("absent".to_owned()));
    }
    if let Some(why) = state.custody(entry.as_ref(), ProjectObject::ConfigurationFile, false) {
        return Ok(Err(format!("custody:{why}")));
    }
    let raw = match obs.bytes(rel)? {
        FileBytes::Read(raw) => raw,
        // Past the bound despite its metadata: the parsers' byte limit, so
        // `parse` (the reference's `canonical.parse`; A2 r2's `ByteLimit`).
        FileBytes::TooLarge => return Ok(Err("parse".to_owned())),
    };
    if rel.ends_with(".toml") {
        // Validated here; the caller re-parses the borrowed view.
        return Ok(match parse_toml(&raw) {
            Ok(_) => Ok(Manifest::Toml(raw)),
            Err(_) => Err("parse".to_owned()),
        });
    }
    Ok(match parse_json(&raw) {
        Ok(doc @ JsonValue::Object(_)) => Ok(Manifest::Json(doc)),
        _ => Err("parse".to_owned()),
    })
}

/// One entry's link, or its unresolved reason and subject (B3-b0 `_link`).
type LinkOutcome = Result<LinkRow, (&'static str, Option<String>)>;
fn link<O: WorkspaceObservation>(
    obs: &mut O,
    state: &State<'_>,
    e: &Entry,
    member: &str,
) -> Result<LinkOutcome, O::Error> {
    let dir = e.directory.as_deref().unwrap_or_default();
    if e.reader == CARGO {
        let (source, name) = e.cargo.clone().unwrap_or_default();
        let raw = match manifest(obs, state, &join(dir, "Cargo.toml"))? {
            Ok(Manifest::Toml(raw)) => raw,
            Ok(Manifest::Json(_)) => {
                return Ok(Err(("link-manifest-unusable", Some("parse".to_owned()))));
            }
            Err(why) => return Ok(Err(("link-manifest-unusable", Some(why)))),
        };
        let Ok(doc) = parse_toml(&raw) else {
            return Ok(Err(("link-manifest-unusable", Some("parse".to_owned()))));
        };
        let package = doc.table().get("package").and_then(TomlValueView::as_table);
        let Some(package_name) = package
            .and_then(|p| p.get("name"))
            .and_then(TomlValueView::as_str)
        else {
            return Ok(Err((
                "link-manifest-unusable",
                Some("name-absent".to_owned()),
            )));
        };
        if package_name != name {
            return Ok(Err(("patch-target-name-mismatch", None)));
        }
        let Some(version) = package
            .and_then(|p| p.get("version"))
            .and_then(TomlValueView::as_str)
        else {
            return Ok(Err(("provided-version-unusable", None)));
        };
        return Ok(Ok(LinkRow {
            ecosystem: "cargo",
            package_name: name,
            provider_member: member.to_owned(),
            package_dir: dir.to_owned(),
            provided_version: version.to_owned(),
            cargo_patch_source: Some(source),
            declared_by: e.reader,
        }));
    }
    let doc = match manifest(obs, state, &join(dir, "package.json"))? {
        Ok(Manifest::Json(JsonValue::Object(doc))) => doc,
        Ok(_) => return Ok(Err(("link-manifest-unusable", Some("parse".to_owned())))),
        Err(why) => return Ok(Err(("link-manifest-unusable", Some(why)))),
    };
    let Some(JsonValue::String(package_name)) = doc.get("name") else {
        return Ok(Err((
            "link-manifest-unusable",
            Some("name-absent".to_owned()),
        )));
    };
    let Some(JsonValue::String(version)) = doc.get("version") else {
        return Ok(Err(("provided-version-unusable", None)));
    };
    Ok(Ok(LinkRow {
        ecosystem: "npm",
        package_name: package_name.clone(),
        provider_member: member.to_owned(),
        package_dir: dir.to_owned(),
        provided_version: version.clone(),
        cargo_patch_source: None,
        declared_by: e.reader,
    }))
}

#[cfg(test)]
mod tests {
    include!("workspace_declarations_tests.rs");
}
