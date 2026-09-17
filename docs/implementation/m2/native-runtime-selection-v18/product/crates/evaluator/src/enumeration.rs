//! Pure extent, membership and package diagnostics over explicit inputs.
//! These helpers do not bind native inputs, admit a complete enumeration, or
//! mint evaluation subjects, a Run, or a replay result.
use crate::native_universe::{array, field, text};
use alloc::{
    collections::{BTreeMap, BTreeSet},
    string::String,
    vec::Vec,
};
use opensip_identity::{JsonValue as V, canonical_bytes};

// Selected enumeration_model.v1.py CODE_SUFFIX, not ambient filesystem rules.
const CODE_SUFFIXES: [&str; 9] = [
    ".ts", ".tsx", ".mts", ".cts", ".js", ".jsx", ".mjs", ".cjs", ".rs",
];
#[derive(Clone, Copy)]
pub enum EnumerationExtentKind {
    File,
    Symbol,
}
/// Data-only projection inputs. The complete enumeration owner must establish
/// their schema, membership derivation, retention and native binding first.
pub struct EnumerationExtentInputs<'a> {
    pub membership: &'a V,
    pub snapshot_paths: &'a [String],
    pub scope: &'a V,
    pub workspace_root: &'a str,
    pub language_mode: &'a str,
    pub universe: Option<&'a V>,
    pub retained: Option<&'a V>,
}
#[derive(Debug, PartialEq, Eq)]
pub enum EnumerationExtentError {
    Shape,
    Limit,
}
/// A path projection and ordered owner refusals, never admission authority.
pub struct EnumerationExtent {
    paths: Vec<String>,
    refusals: Vec<&'static str>,
}
impl EnumerationExtent {
    pub fn paths(&self) -> &[String] {
        &self.paths
    }
    pub fn refusals(&self) -> &[&'static str] {
        &self.refusals
    }
}
struct Projection {
    remaining: usize,
    refusals: Vec<&'static str>,
}
impl Projection {
    fn spend(&mut self) -> Result<(), EnumerationExtentError> {
        self.remaining = self
            .remaining
            .checked_sub(1)
            .ok_or(EnumerationExtentError::Limit)?;
        Ok(())
    }
    fn refuse(&mut self, cause: &'static str) {
        if !self.refusals.contains(&cause) {
            self.refusals.push(cause);
        }
    }
}
fn get<'a>(v: &'a V, key: &str) -> Result<&'a V, EnumerationExtentError> {
    field(v, key).map_err(|_| EnumerationExtentError::Shape)
}
fn string(v: &V) -> Result<&str, EnumerationExtentError> {
    text(v).map_err(|_| EnumerationExtentError::Shape)
}
fn rows(v: &V) -> Result<&[V], EnumerationExtentError> {
    array(v).map_err(|_| EnumerationExtentError::Shape)
}
fn optional_rows<'a>(v: &'a V, key: &str) -> Result<&'a [V], EnumerationExtentError> {
    let V::Object(o) = v else {
        return Err(EnumerationExtentError::Shape);
    };
    match o.get(key) {
        None | Some(V::Null) => Ok(&[]),
        Some(v) => rows(v),
    }
}
fn root(s: &str) -> &str {
    if s == "." { "" } else { s }
}
fn under(path: &str, root: &str) -> bool {
    root.is_empty()
        || path == root
        || path
            .strip_prefix(root.trim_end_matches('/'))
            .is_some_and(|tail| tail.starts_with('/'))
}
fn code(path: &str) -> bool {
    CODE_SUFFIXES.iter().any(|s| path.ends_with(s))
}
fn in_scope(path: &str, scope: &V, p: &mut Projection) -> Result<bool, EnumerationExtentError> {
    for excluded in optional_rows(scope, "excludedPathPrefixes")? {
        p.spend()?;
        if under(path, root(string(excluded)?)) {
            return Ok(false);
        }
    }
    let prefixes = optional_rows(scope, "pathPrefixes")?;
    if prefixes.is_empty() {
        return Ok(true);
    }
    for prefix in prefixes {
        p.spend()?;
        if under(path, root(string(prefix)?)) {
            return Ok(true);
        }
    }
    Ok(false)
}
fn canonical_paths(paths: Vec<String>) -> Result<Vec<String>, EnumerationExtentError> {
    // Canonical JSON string order, not raw string order (quotes/escapes differ).
    let unique: BTreeSet<_> = paths.into_iter().collect();
    let mut keyed = unique
        .into_iter()
        .map(|s| {
            canonical_bytes(&V::String(s.clone()))
                .map(|key| (key, s))
                .map_err(|_| EnumerationExtentError::Shape)
        })
        .collect::<Result<Vec<_>, _>>()?;
    keyed.sort_by(|a, b| a.0.cmp(&b.0));
    Ok(keyed.into_iter().map(|(_, s)| s).collect())
}
/// Project the file/symbol extent. `steps` bounds row visits and scope-prefix
/// comparisons for this helper; it is not a Plan work-unit or aggregate CPU cap.
/// Ordered refusals match the selected enumeration owner on admitted inputs.
pub fn project_enumeration_extent(
    input: &EnumerationExtentInputs<'_>,
    kind: EnumerationExtentKind,
    steps: usize,
) -> Result<EnumerationExtent, EnumerationExtentError> {
    let mut p = Projection {
        remaining: steps,
        refusals: Vec::new(),
    };
    p.spend()?;
    let mut membership = BTreeMap::new();
    for row in rows(get(input.membership, "rows")?)? {
        p.spend()?;
        membership.insert(string(get(row, "path")?)?, row);
    }
    let mut scoped = Vec::new();
    for path in input.snapshot_paths {
        p.spend()?;
        if !under(path, root(input.workspace_root)) || !in_scope(path, input.scope, &mut p)? {
            continue;
        }
        let Some(row) = membership.get(path.as_str()) else {
            p.refuse("ENUMERATION_ADMISSION_PRECONDITION");
            continue;
        };
        if string(get(row, "membership")?)? == "outside-project-boundary"
            || [
                "host-ignore-convention",
                "nested-repository",
                "nested-project",
                "custody-excluded",
            ]
            .contains(&string(get(row, "reason")?)?)
        {
            continue;
        }
        scoped.push(path.clone());
    }
    if matches!(kind, EnumerationExtentKind::File) {
        return Ok(EnumerationExtent {
            paths: canonical_paths(scoped)?,
            refusals: p.refusals,
        });
    }
    let scoped: BTreeSet<_> = scoped.into_iter().collect();
    let mut output = Vec::new();
    match input.universe {
        None | Some(V::Null | V::Bool(_) | V::Integer(_) | V::String(_) | V::Array(_)) => {
            for path in &scoped {
                p.spend()?;
                if code(path)
                    && (input.language_mode == "syntax-only"
                        || string(get(membership[path.as_str()], "membership")?)?
                            == "program-member")
                {
                    output.push(path.clone());
                }
            }
        }
        Some(V::Object(universe)) => match input.language_mode {
            "syntax-only" => {
                for path in &scoped {
                    p.spend()?;
                    if code(path) {
                        output.push(path.clone());
                    }
                }
            }
            "ts-tsconfig" | "js-allowjs" | "js-synthesized" => {
                if let Some(V::Array(roots)) = universe.get("programRootFiles") {
                    let snapshot: BTreeSet<_> = input.snapshot_paths.iter().collect();
                    for path in roots {
                        p.spend()?;
                        let path = string(path)?;
                        if !snapshot.contains(&String::from(path)) || !scoped.contains(path) {
                            p.refuse("ENUMERATION_BINDING_EXTENT_PATHS");
                            continue;
                        }
                        if code(path) {
                            output.push(path.into());
                        }
                    }
                } else {
                    p.refuse("ENUMERATION_ADMISSION_PRECONDITION");
                }
            }
            mode if mode.starts_with("rust") => {
                let ownership = input.retained.and_then(|v| match v {
                    V::Object(o) => o.get("sourceUnitOwnership"),
                    _ => None,
                });
                if let Some(own @ V::Object(_)) = ownership {
                    let mut selected = BTreeSet::new();
                    for id in optional_rows(own, "selectedUnitIds")? {
                        p.spend()?;
                        selected.insert(string(id)?);
                    }
                    for row in optional_rows(own, "ownership")? {
                        p.spend()?;
                        let path = string(get(row, "path")?)?;
                        if selected.contains(string(get(row, "unitId")?)?) && scoped.contains(path)
                        {
                            output.push(path.into());
                        }
                    }
                } else {
                    p.refuse("ENUMERATION_ADMISSION_PRECONDITION");
                }
            }
            _ => {}
        },
    }
    Ok(EnumerationExtent {
        paths: canonical_paths(output)?,
        refusals: p.refusals,
    })
}

#[derive(Debug, PartialEq, Eq)]
pub enum EnumerationMembershipError {
    Shape,
    Limit,
}
impl From<EnumerationExtentError> for EnumerationMembershipError {
    fn from(value: EnumerationExtentError) -> Self {
        match value {
            EnumerationExtentError::Shape => Self::Shape,
            EnumerationExtentError::Limit => Self::Limit,
        }
    }
}
/// Recomputed membership diagnostics, not security-boundary or Run authority.
pub struct EnumerationMembershipChecks {
    refusals: Vec<&'static str>,
}
impl EnumerationMembershipChecks {
    pub fn refusals(&self) -> &[&'static str] {
        &self.refusals
    }
}
fn internal_root(value: &V, allow_empty: bool) -> bool {
    let V::String(s) = value else { return false };
    s.chars().count() <= 4096
        && ((allow_empty && s.is_empty())
            || (!s.contains(['\\', '\0'])
                && s.split('/')
                    .all(|segment| !matches!(segment, "" | "." | ".."))))
}
fn family(path: &str) -> &'static str {
    if path.ends_with(".rs") {
        "rust"
    } else if CODE_SUFFIXES[..8].iter().any(|s| path.ends_with(s)) {
        "tsjs"
    } else {
        "none"
    }
}
fn ordinal(v: &V) -> Result<i128, EnumerationExtentError> {
    match v {
        V::Integer(i) => Ok(i.get()),
        _ => Err(EnumerationExtentError::Shape),
    }
}
fn membership_checks(
    registry: &opensip_identity::RegisteredSchemas,
    membership: &V,
    snapshot_paths: &[String],
    steps: usize,
) -> Result<EnumerationMembershipChecks, EnumerationExtentError> {
    let mut p = Projection {
        remaining: steps,
        refusals: Vec::new(),
    };
    p.spend()?;
    let units = rows(get(membership, "units")?)?;
    // Internal representation is checked before coverage, ordering or binding.
    for unit in units {
        p.spend()?;
        let V::Object(u) = unit else {
            p.refuse("ENUMERATION_MEMBERSHIP_UNIT_ROOT");
            return Ok(EnumerationMembershipChecks {
                refusals: p.refusals,
            });
        };
        let valid_root = u.get("rootPath").is_some_and(|v| internal_root(v, true));
        let valid_members = match u.get("memberPackageRoots") {
            None => true,
            Some(V::Array(a)) => {
                let mut valid = true;
                for v in a {
                    p.spend()?;
                    valid &= internal_root(v, false);
                }
                valid
            }
            _ => false,
        };
        if !valid_root || !valid_members {
            p.refuse("ENUMERATION_MEMBERSHIP_UNIT_ROOT");
            return Ok(EnumerationMembershipChecks {
                refusals: p.refusals,
            });
        }
    }
    let source_rows = rows(get(membership, "rows")?)?;
    let mut paths = Vec::new();
    for row in source_rows {
        p.spend()?;
        paths.push(string(get(row, "path")?)?);
    }
    let unique: BTreeSet<_> = paths.iter().copied().collect();
    let snapshot: BTreeSet<_> = snapshot_paths.iter().map(String::as_str).collect();
    if unique.len() != paths.len() || unique != snapshot {
        p.refuse("ENUMERATION_ADMISSION_PRECONDITION");
    }
    let mut previous = None;
    let mut cargo_roots = BTreeSet::new();
    for (index, unit) in units.iter().enumerate() {
        p.spend()?;
        let root = string(get(unit, "rootPath")?)?;
        let family = string(get(unit, "languageFamily")?)?;
        let key = (root, family);
        if ordinal(get(unit, "unitOrdinal")?)? != index as i128
            || previous.is_some_and(|old| old >= key)
        {
            p.refuse("ENUMERATION_MEMBERSHIP_ORDER");
        }
        previous = Some(key);
        let members = rows(get(unit, "memberPackageRoots")?)?;
        let mut prev_member = None;
        if family == "rust" {
            cargo_roots.insert(root);
        }
        for m in members {
            p.spend()?;
            let m = string(m)?;
            if prev_member.is_some_and(|old| old >= m) {
                p.refuse("ENUMERATION_MEMBERSHIP_ORDER");
            }
            prev_member = Some(m);
            if family == "rust" {
                cargo_roots.insert(m);
            }
        }
        let kind = string(get(unit, "unitKind")?)?;
        if family == "tsjs" {
            let expected = match string(get(unit, "languageMode")?)? {
                "ts-tsconfig" => "ts-program",
                "js-allowjs" | "js-synthesized" => "js-program",
                _ => "",
            };
            if kind != expected {
                p.refuse("ENUMERATION_MEMBERSHIP_ORDER");
            }
        } else if matches!(kind, "ts-program" | "js-program") {
            p.refuse("ENUMERATION_MEMBERSHIP_ORDER");
        }
    }
    if paths.windows(2).any(|pair| pair[0] >= pair[1]) {
        p.refuse("ENUMERATION_MEMBERSHIP_ORDER");
    }
    for (field, kind) in [
        ("unsupportedFiles", "unsupported-file"),
        ("outsideBoundaryFiles", "outside-project-boundary"),
    ] {
        let mut projected = Vec::new();
        for row in source_rows {
            p.spend()?;
            if string(get(row, "membership")?)? == kind {
                projected.push(get(row, "path")?.clone());
            }
        }
        if get(membership, field)? != &V::Array(projected) {
            p.refuse("ENUMERATION_MEMBERSHIP_ORDER");
        }
    }
    // Re-use the source-bound bundled suffix metadata already owned by the
    // native context implementation; callers cannot supply a grammar registry.
    let law = opensip_identity::parse_json(include_bytes!("native-context-registry.json"))
        .map_err(|_| EnumerationExtentError::Shape)?;
    let V::Object(grammars) = get(&law, "bundledGrammars")? else {
        return Err(EnumerationExtentError::Shape);
    };
    let mut recomputed_rows = Vec::new();
    for row in source_rows {
        p.spend()?;
        let path = string(get(row, "path")?)?;
        let fam = family(path);
        if string(get(row, "membership")?)? == "outside-project-boundary" {
            // The security boundary inventory is not retained by the Plan.
            // Recheck only the published suffix/null facts, never fabricate it.
            if get(row, "unitOrdinal")? != &V::Null || string(get(row, "languageFamily")?)? != fam {
                p.refuse("ENUMERATION_MEMBERSHIP_ROW_DERIVATION");
            }
            continue;
        }
        let mut ignored = false;
        let mut start = 0;
        for segment in path.split('/') {
            p.spend()?;
            if matches!(segment, "node_modules" | ".git" | ".hg" | ".svn" | ".jj")
                || (segment == "target"
                    && cargo_roots.contains(if start == 0 { "" } else { &path[..start - 1] }))
            {
                ignored = true;
            }
            start += segment.len() + 1;
        }
        let mut chosen: Option<(&V, usize, i128)> = None;
        if !ignored && fam != "none" {
            for unit in units {
                p.spend()?;
                let root = string(get(unit, "rootPath")?)?;
                let order = ordinal(get(unit, "unitOrdinal")?)?;
                let length = root.chars().count();
                if string(get(unit, "languageFamily")?)? == fam
                    && under(path, root)
                    && chosen.is_none_or(|(_, depth, old)| {
                        length > depth || (length == depth && order < old)
                    })
                {
                    chosen = Some((unit, length, order));
                }
            }
        }
        let (membership_kind, reason, selected) = if ignored {
            ("syntax-only", "host-ignore-convention", V::Null)
        } else if fam == "none" {
            let name = path
                .rsplit('/')
                .next()
                .ok_or(EnumerationExtentError::Shape)?;
            let suffix = name.rfind('.').map_or("", |i| &name[i..]);
            if grammars.contains_key(suffix) {
                ("syntax-only", "grammar-only", V::Null)
            } else {
                ("unsupported-file", "no-bundled-grammar", V::Null)
            }
        } else if let Some((unit, _, _)) = chosen {
            (
                "program-member",
                "deepest-unit-in-language",
                get(unit, "unitOrdinal")?.clone(),
            )
        } else {
            ("syntax-only", "no-program-unit-for-language", V::Null)
        };
        let expected = V::Object(BTreeMap::from([
            (String::from("path"), V::String(path.into())),
            (String::from("languageFamily"), V::String(fam.into())),
            (String::from("unitOrdinal"), selected),
            (
                String::from("membership"),
                V::String(membership_kind.into()),
            ),
            (String::from("reason"), V::String(reason.into())),
        ]));
        if row != &expected {
            p.refuse("ENUMERATION_MEMBERSHIP_ROW_DERIVATION");
        }
        recomputed_rows.push(expected);
    }
    recomputed_rows.sort_by(|a, b| match (a, b) {
        (V::Object(a), V::Object(b)) => match (&a["path"], &b["path"]) {
            (V::String(a), V::String(b)) => a.cmp(b),
            _ => core::cmp::Ordering::Equal,
        },
        _ => core::cmp::Ordering::Equal,
    });
    let mut unsupported = Vec::new();
    for row in &recomputed_rows {
        p.spend()?;
        if string(get(row, "membership")?)? == "unsupported-file" {
            unsupported.push(get(row, "path")?.clone());
        }
    }
    let recomputed = V::Object(BTreeMap::from([
        (
            String::from("schemaVersion"),
            V::Integer(
                opensip_identity::JsonInteger::new(1).map_err(|_| EnumerationExtentError::Shape)?,
            ),
        ),
        (String::from("units"), V::Array(units.to_vec())),
        (String::from("rows"), V::Array(recomputed_rows)),
        (String::from("unsupportedFiles"), V::Array(unsupported)),
        (String::from("outsideBoundaryFiles"), V::Array(Vec::new())),
        (String::from("erasedFiles"), V::Array(Vec::new())),
    ]));
    let raw = canonical_bytes(&recomputed).map_err(|_| EnumerationExtentError::Shape)?;
    let schema = registry
        .schema(
            "urn:opensip:product-v1:native:evidence-schemas:v2",
            "/$defs/UnitMembershipV1",
        )
        .map_err(|_| EnumerationExtentError::Shape)?;
    match schema.admit_json(&raw, steps) {
        Ok(_) => {}
        Err(opensip_identity::SchemaAdmissionError::Mismatch) => {
            p.refuse("ENUMERATION_MEMBERSHIP_ROW_DERIVATION")
        }
        Err(opensip_identity::SchemaAdmissionError::Schema(
            opensip_identity::SchemaError::Limit,
        )) => return Err(EnumerationExtentError::Limit),
        Err(_) => return Err(EnumerationExtentError::Shape),
    }
    Ok(EnumerationMembershipChecks {
        refusals: p.refusals,
    })
}
/// Recheck internal roots, snapshot coverage, retained membership ordering and
/// per-row derivation. Inputs must otherwise have their owning native schema
/// admitted. This is not discovery, boundary custody, or full enumeration.
/// Steps separately bound local row/unit/segment visits and the recomputed
/// native record schema check; they are not an aggregate or Plan work budget.
pub fn inspect_enumeration_membership(
    registry: &opensip_identity::RegisteredSchemas,
    membership: &V,
    snapshot_paths: &[String],
    steps: usize,
) -> Result<EnumerationMembershipChecks, EnumerationMembershipError> {
    membership_checks(registry, membership, snapshot_paths, steps).map_err(Into::into)
}

/// Package projections and ordered retention refusals. No subject or Run authority.
pub struct EnumerationPackages {
    value: V,
    refusals: Vec<&'static str>,
}
impl EnumerationPackages {
    pub fn value(&self) -> &V {
        &self.value
    }
    pub fn refusals(&self) -> &[&'static str] {
        &self.refusals
    }
}
enum PackageClass {
    Named(String),
    Unnamed(&'static str),
    Failed(&'static str),
}
fn classify_manifest(raw: &[u8], json: bool) -> Result<PackageClass, EnumerationExtentError> {
    if json {
        // The selected JSON profile permits whitespace and unsorted keys.
        // Its lexical bounds are profile refusals in the selected reference.
        let data = match opensip_identity::parse_json(raw) {
            Ok(data) => data,
            Err(_) => return Ok(PackageClass::Failed("syntax")),
        };
        let V::Object(object) = data else {
            return Ok(PackageClass::Failed("classification"));
        };
        return Ok(match object.get("name") {
            None => PackageClass::Unnamed("no-name"),
            Some(V::String(name)) if !name.is_empty() => PackageClass::Named(name.clone()),
            _ => PackageClass::Failed("classification"),
        });
    }
    use opensip_identity::TomlError;
    let document = match opensip_identity::parse_toml(raw) {
        Ok(document) => document,
        Err(TomlError::InvalidUtf8 | TomlError::Syntax) => {
            return Ok(PackageClass::Failed("syntax"));
        }
        Err(TomlError::ByteLimit | TomlError::RecursionLimit | TomlError::NodeLimit) => {
            return Err(EnumerationExtentError::Limit);
        }
    };
    let table = document.table();
    let unnamed = || {
        PackageClass::Unnamed(if table.contains_key("workspace") {
            "workspace-only"
        } else {
            "no-name"
        })
    };
    let Some(package) = table.get("package") else {
        return Ok(unnamed());
    };
    let Some(package) = package.as_table() else {
        return Ok(PackageClass::Failed("classification"));
    };
    Ok(match package.get("name") {
        None => unnamed(),
        Some(value) => match value.as_str() {
            Some(name) if !name.is_empty() => PackageClass::Named(name.into()),
            _ => PackageClass::Failed("classification"),
        },
    })
}
fn package_row<const N: usize>(fields: [(&str, &str); N]) -> V {
    V::Object(
        fields
            .into_iter()
            .map(|(key, value)| (key.into(), V::String(value.into())))
            .collect(),
    )
}
/// Classify retained manifest bytes for the independently projected file extent.
/// Missing bytes and optional snapshot hash/length mismatches are precondition
/// refusals, never syntax failures. The optional index must be the full owner's
/// snapshot-derived index; this helper cannot establish its provenance.
/// `steps` separately bounds extent visits and package visits, not parser CPU.
/// TOML resource refusal aborts the projection; no partial result is returned.
pub fn project_enumeration_packages(
    input: &EnumerationExtentInputs<'_>,
    source_blobs: &BTreeMap<String, Vec<u8>>,
    snapshot_blob_index: Option<&BTreeMap<String, V>>,
    steps: usize,
) -> Result<EnumerationPackages, EnumerationExtentError> {
    let extent = project_enumeration_extent(input, EnumerationExtentKind::File, steps)?;
    let mut p = Projection {
        remaining: steps,
        refusals: extent.refusals,
    };
    p.spend()?;
    let mut named = Vec::new();
    let mut unnamed = Vec::new();
    let mut failed = Vec::new();
    let mut named_paths = Vec::new();
    let mut candidates = Vec::new();
    for path in extent.paths {
        p.spend()?;
        let name = path
            .rsplit('/')
            .next()
            .ok_or(EnumerationExtentError::Shape)?;
        if !matches!(name, "package.json" | "Cargo.toml") {
            continue;
        }
        let Some(raw) = source_blobs.get(&path) else {
            p.refuse("ENUMERATION_ADMISSION_PRECONDITION");
            continue;
        };
        if let Some(index) = snapshot_blob_index {
            let matches = index.get(&path).is_some_and(|row| {
                let V::Object(row) = row else { return false };
                let (Some(V::String(hash)), Some(V::Integer(len))) =
                    (row.get("sha256"), row.get("bytes"))
                else {
                    return false;
                };
                len.get() == raw.len() as i128
                    && *hash == opensip_identity::digest_hex(&opensip_identity::raw_sha256(raw))
            });
            if !matches {
                p.refuse("ENUMERATION_ADMISSION_PRECONDITION");
                continue;
            }
        }
        let is_json = name == "package.json";
        match classify_manifest(raw, is_json)? {
            PackageClass::Named(name) => {
                named.push(package_row([
                    ("path", &path),
                    ("packageName", &name),
                    ("format", if is_json { "json" } else { "toml" }),
                ]));
                named_paths.push(path.clone());
                candidates.push(path);
            }
            PackageClass::Unnamed(reason) => {
                unnamed.push(package_row([("path", &path), ("reason", reason)]))
            }
            PackageClass::Failed(reason) => {
                failed.push(package_row([("path", &path), ("reason", reason)]));
                candidates.push(path);
            }
        }
    }
    let strings = |paths: Vec<String>| -> Result<V, EnumerationExtentError> {
        Ok(V::Array(
            canonical_paths(paths)?.into_iter().map(V::String).collect(),
        ))
    };
    Ok(EnumerationPackages {
        value: V::Object(BTreeMap::from([
            ("named".into(), V::Array(named)),
            ("unnamed".into(), V::Array(unnamed)),
            ("parseFailed".into(), V::Array(failed)),
            ("namedPaths".into(), strings(named_paths)?),
            ("candidatePaths".into(), strings(candidates)?),
        ])),
        refusals: p.refusals,
    })
}
