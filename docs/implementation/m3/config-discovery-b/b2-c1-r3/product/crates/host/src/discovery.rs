// M3-B r7 item 14 (unit B2-c1, B2-c plan r2 section 2.1): the native unit
// instrument, NE §1.4 U-0 to U-9 as contract successors B-S1 and B2-c0 (166)
// state them. Pure: no I/O, process, socket, write or environment read
// (FW-01). The shared discovery rule is security's (`discovery_export`),
// never copied here. The admitted boundary inventory is security's opaque
// `AdmittedBoundaries`, so a caller cannot substitute an ignore list for it.
// Every record is the B2-c0 reference's, byte for byte in canonical JSON
// (`discovery_tests.rs` replays `discovery_vectors.json`). Decisions carry
// the reference's internal keys; `public_detail` normalizes one at the host
// boundary through the registry's alias rows (plan r2 section 2.3).
//
// No production caller yet: J1 composes this with the walker, C1's inventory
// and the configuration resolver.
use opensip_identity::{
    JsonInteger, JsonValue as V, canonical_bytes, digest_hex, parse_json, raw_sha256,
};
use opensip_security::discovery_export::{
    self as rule, AdmittedBoundaries, CustodyExcludedUnit, PrunedTreeRow,
};
use std::collections::{BTreeMap, BTreeSet};

/// The selected native capability matrix (`native-capability-matrix.v2.json`),
/// pinned to its architecture bytes by the vectors.
const CAPABILITY_MATRIX: &[u8] = include_bytes!("native_capability_matrix.v2.json");
const NO_BOUNDARY_DISCLOSURE: &str = "no admitted boundary inventory: standalone pure instrument over a marker inventory; nested repositories, nested projects and custody exclusions are NOT decided here and this output is not an operational host composition (native section 1.4 U-8)";
const BOUNDARY_DISCLOSURE: &str = "boundaries admitted by the security discovery instrument (S3) over the same marker inventory; units and memberships at or below a boundary are outside this project";
const VCS_MARKERS: [&str; 4] = [".git", ".hg", ".svn", ".jj"];
const TSJS_MARKERS: [&str; 3] = ["tsconfig.json", "jsconfig.json", "package.json"];
const RUST_EXT: [&str; 1] = [".rs"];
const TSJS_EXT: [&str; 8] = [".js", ".mjs", ".cjs", ".jsx", ".ts", ".tsx", ".mts", ".cts"];
const BUNDLED_GRAMMARS: [&str; 14] = [
    ".rs", ".ts", ".tsx", ".mts", ".cts", ".js", ".mjs", ".cjs", ".jsx", ".json", ".toml", ".md",
    ".yaml", ".yml",
];
/// The foundation scope-descriptor bounds (`identity-schemas.v3.json#/$defs/scope-descriptor`).
const SCOPE_LIMITS: [(&str, usize); 3] = [
    ("workspaceRoots", 1024),
    ("pathPrefixes", 65536),
    ("excludedPathPrefixes", 65536),
];
/// The requested-capability bound of the pre-Plan analysis spec.
const REQUESTED_CAPABILITY_BOUND: usize = 1024;
const RELEASE_REGISTRY_BOUND: usize = 128;

// ------------------------------------------------------------------ inputs

/// One marker observation (`{sha256, isCargoWorkspace?, allowJs?}`): trusted
/// facts of a snapshot marker file, read as data by the composition.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct MarkerFact {
    pub(crate) sha256: String,
    pub(crate) is_cargo_workspace: Option<bool>,
    pub(crate) allow_js: Option<bool>,
}

/// Language family of a unit or a path.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub(crate) enum Family {
    None,
    Rust,
    Tsjs,
}
impl Family {
    fn as_str(self) -> &'static str {
        match self {
            Self::None => "none",
            Self::Rust => "rust",
            Self::Tsjs => "tsjs",
        }
    }
}

/// `WorkspaceUnitV2` (closed).
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct WorkspaceUnit {
    pub(crate) unit_ordinal: usize,
    pub(crate) root_path: String,
    pub(crate) language_family: Family,
    pub(crate) language_mode: String,
    pub(crate) unit_kind: String,
    pub(crate) marker_path: String,
    pub(crate) marker_sha256: Option<String>,
    pub(crate) recognizer_id: String,
    pub(crate) recognizer_version: u32,
    pub(crate) provenance: String,
    pub(crate) member_package_roots: Vec<String>,
}

/// An internal decision of the instrument: the reference's key, normalized
/// to a public detail only at the host boundary (`public_detail`).
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct UnitRefusal {
    pub(crate) detail: &'static str,
    pub(crate) roots: Vec<String>,
    pub(crate) extra: Vec<(&'static str, V)>,
}

/// `UnitDiscoveryV3`, or the reference's refused shape.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct UnitDiscovery {
    pub(crate) units: Vec<WorkspaceUnit>,
    pub(crate) pruned_trees: Vec<PrunedTreeRow>,
    pub(crate) boundaries: V,
    pub(crate) refused: Option<UnitRefusal>,
}

/// A composition fault with no public detail (the reference's internal key).
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct InternalFault(pub(crate) String);

// ------------------------------------------------------------------ the alias map (plan r2 section 2.3)

/// The registry's `internalAliases` rows for this instrument's keys
/// (`public-detail-registry.v1.json`), pinned by `discovery_tests.rs`.
pub(crate) const INTERNAL_DETAIL_ALIASES: [(&str, &str); 4] = [
    (
        "native.boundary-inventory-mismatch",
        "PROJECT.DISCOVERY_INVENTORY_MISMATCH",
    ),
    (
        "native.explicit-root-crosses-boundary",
        "PROJECT.EXPLICIT_PATH_INVALID",
    ),
    (
        "native.explicit-root-grammar",
        "PROJECT.EXPLICIT_PATH_INVALID",
    ),
    ("native.too-many-units", "PROJECT.WORKSPACE_UNIT_LIMIT"),
];
/// The instrument's public records that pass unchanged.
pub(crate) const PUBLIC_DETAILS: [&str; 2] =
    ["native.explicit-root-without-marker", "PROJECT.SCOPE_LIMIT"];

/// The public `DomainDetailCode` of an internal decision key. An unknown key
/// refuses: the alias map is closed.
pub(crate) fn public_detail(internal: &str) -> Result<&'static str, InternalFault> {
    if let Some((_, public)) = INTERNAL_DETAIL_ALIASES
        .iter()
        .find(|(key, _)| *key == internal)
    {
        return Ok(public);
    }
    PUBLIC_DETAILS
        .iter()
        .find(|code| **code == internal)
        .copied()
        .ok_or_else(|| InternalFault(format!("unknown internal detail key: {internal}")))
}

// ------------------------------------------------------------------ JSON helpers

fn s(text: &str) -> V {
    V::String(text.to_owned())
}
fn int(n: usize) -> V {
    // Every count here is far below the profile's integer bound.
    match JsonInteger::new(n as i128) {
        Ok(i) => V::Integer(i),
        Err(_) => V::Null,
    }
}
fn strings<S: AsRef<str>>(items: &[S]) -> V {
    V::Array(items.iter().map(|i| s(i.as_ref())).collect())
}
fn obj(fields: Vec<(&str, V)>) -> V {
    V::Object(fields.into_iter().map(|(k, v)| (k.to_owned(), v)).collect())
}

fn d9(detail: &'static str) -> V {
    let code = match detail {
        "native.boundary-inventory-mismatch" => "REQUEST.PRECONDITION_FAILED",
        "native.too-many-units" | "PROJECT.SCOPE_LIMIT" => "REQUEST.UNSATISFIABLE",
        _ => "CONFIG.INVALID",
    };
    obj(vec![
        ("detail", s(detail)),
        ("class", s("request-rejected")),
        ("exitCode", int(2)),
        ("code", s(code)),
        ("successorCode", V::Null),
        ("interim", V::Bool(false)),
        ("typedDetailCarrier", s("request rejection detail")),
    ])
}

pub(crate) fn pruned_row_json(row: &PrunedTreeRow) -> V {
    obj(vec![
        ("path", s(&row.anchor.path)),
        ("reason", s(row.anchor.reason.as_str())),
        (
            "markerCount",
            row.marker_count
                .map_or(V::Null, |n| int(usize::try_from(n).unwrap_or(usize::MAX))),
        ),
        ("markerCountBasis", s(row.basis.as_str())),
    ])
}
fn custody_json(rows: &[CustodyExcludedUnit]) -> V {
    V::Array(
        rows.iter()
            .map(|r| obj(vec![("path", s(&r.path)), ("reason", s(&r.reason))]))
            .collect(),
    )
}

impl WorkspaceUnit {
    pub(crate) fn to_json(&self) -> V {
        obj(vec![
            ("unitOrdinal", int(self.unit_ordinal)),
            ("rootPath", s(&self.root_path)),
            ("languageFamily", s(self.language_family.as_str())),
            ("languageMode", s(&self.language_mode)),
            ("unitKind", s(&self.unit_kind)),
            ("markerPath", s(&self.marker_path)),
            (
                "markerSha256",
                self.marker_sha256.as_deref().map_or(V::Null, s),
            ),
            ("recognizerId", s(&self.recognizer_id)),
            ("recognizerVersion", int(self.recognizer_version as usize)),
            ("provenance", s(&self.provenance)),
            ("memberPackageRoots", strings(&self.member_package_roots)),
        ])
    }
}

impl UnitRefusal {
    fn to_json(&self) -> V {
        let mut fields = vec![
            ("detail", s(self.detail)),
            ("roots", strings(&self.roots)),
            ("d9", d9(self.detail)),
        ];
        fields.extend(self.extra.iter().cloned());
        obj(fields)
    }
}

impl UnitDiscovery {
    pub(crate) fn to_json(&self) -> V {
        obj(vec![
            (
                "units",
                V::Array(self.units.iter().map(WorkspaceUnit::to_json).collect()),
            ),
            (
                "prunedTrees",
                V::Array(self.pruned_trees.iter().map(pruned_row_json).collect()),
            ),
            ("boundaries", self.boundaries.clone()),
            (
                "refused",
                self.refused.as_ref().map_or(V::Null, UnitRefusal::to_json),
            ),
        ])
    }
}

// ------------------------------------------------------------------ boundaries

fn members_of(boundaries: Option<&AdmittedBoundaries>) -> BTreeSet<String> {
    boundaries.map_or_else(BTreeSet::new, |b| {
        b.member_repositories().iter().cloned().collect()
    })
}

/// The selected `_boundary_hit` (security's `AdmittedBoundaries::boundary_hit`).
fn boundary_hit(
    path: &str,
    boundaries: Option<&AdmittedBoundaries>,
    marker: Option<&str>,
) -> Option<(String, &'static str)> {
    boundaries?.boundary_hit(path, marker)
}

fn boundaries_out(boundaries: Option<&AdmittedBoundaries>, excluded_units: &[V]) -> V {
    match boundaries {
        None => obj(vec![
            ("source", s("none")),
            ("nestedRepositories", V::Array(Vec::new())),
            ("nestedProjects", V::Array(Vec::new())),
            ("custodyExcludedUnits", V::Array(Vec::new())),
            ("excludedUnits", V::Array(excluded_units.to_vec())),
            ("disclosure", s(NO_BOUNDARY_DISCLOSURE)),
            ("memberRepositories", V::Array(Vec::new())),
        ]),
        Some(b) => obj(vec![
            ("source", s("security.discovery")),
            ("nestedRepositories", strings(b.nested_repositories())),
            ("nestedProjects", strings(b.nested_projects())),
            (
                "custodyExcludedUnits",
                custody_json(b.custody_excluded_units()),
            ),
            ("excludedUnits", V::Array(excluded_units.to_vec())),
            ("disclosure", s(BOUNDARY_DISCLOSURE)),
            ("memberRepositories", strings(b.member_repositories())),
        ]),
    }
}

/// The internal root representation (U-0): `""` or a canonical relative
/// directory; a member package root is never empty.
/// The schema's `maxLength` counts characters, not UTF-8 bytes.
fn chars(text: &str) -> usize {
    text.chars().count()
}

/// The root grammar of `InternalUnitRootV1` / `CanonicalRelativeDirV1`:
/// `/`-joined segments, none empty, `.` or `..`, with no NUL or backslash.
fn root_grammar(path: &str) -> bool {
    path.is_empty()
        || path
            .split('/')
            .all(|seg| !matches!(seg, "" | "." | "..") && !seg.contains(['\0', '\\']))
}

/// One root scalar, as the reference's `_admit_root_scalar`: the declared
/// length bounds (characters), then the grammar.
fn admit_root(value: &str, low: usize, selector: &str, at: &str) -> Result<(), InternalFault> {
    let n = chars(value);
    if n < low || n > 4096 {
        return Err(InternalFault(format!(
            "NATIVE_UNIT_ROOT_REPRESENTATION:{at}:{selector}:length={n}:bounds={low}..4096"
        )));
    }
    if !root_grammar(value) || (low == 1 && value.is_empty()) {
        // r3 (Codex B2C1-R2-RF-1; a lead decision): an internal key names the
        // field, the selector and the class, never the value's spelling.
        // The reference's key spells it with Python's `repr`, whose
        // printability follows Python's own Unicode database (unassigned
        // code points included), which no other implementation reproduces
        // stably; the vectors normalize it to this form. No public detail.
        return Err(InternalFault(format!(
            "NATIVE_UNIT_ROOT_REPRESENTATION:{at}:{selector}:grammar"
        )));
    }
    Ok(())
}

/// `admit_unit_roots` (U-0): decided before any prefix test or slice.
pub(crate) fn admit_unit_roots(units: &[WorkspaceUnit]) -> Result<(), InternalFault> {
    for (i, u) in units.iter().enumerate() {
        admit_root(
            &u.root_path,
            0,
            "#/$defs/InternalUnitRootV1",
            &format!("units[{i}].rootPath"),
        )?;
        for (j, m) in u.member_package_roots.iter().enumerate() {
            admit_root(
                m,
                1,
                "#/$defs/CanonicalRelativeDirV1",
                &format!("units[{i}].memberPackageRoots[{j}]"),
            )?;
        }
    }
    Ok(())
}

fn under_unit(path: &str, root: &str) -> bool {
    root.is_empty() || path == root || path.starts_with(&format!("{}/", root.trim_end_matches('/')))
}

// ------------------------------------------------------------------ U-1 to U-9: discovery

/// `discover_units` (NE §1.4 U-1 to U-4b, U-7, U-8 and U-9; B-S1; B2-c0):
/// `markers` is every marker file of the inventory; `explicit_roots` the raw
/// Config2 or flags-layer values; `boundaries` the admitted inventory, or
/// `None` only for the standalone instrument.
fn discover(
    markers: &BTreeMap<String, MarkerFact>,
    explicit_roots: Option<&[String]>,
    boundaries: Option<&AdmittedBoundaries>,
) -> UnitDiscovery {
    let members = members_of(boundaries);
    // LD-B2C0-1 (contract successor 166): a marker whose derived pruned anchor
    // is at or below an admitted boundary is withheld from anchor derivation.
    let markers: BTreeMap<&String, &MarkerFact> = match boundaries {
        None => markers.iter().collect(),
        Some(b) => {
            let paths: Vec<&str> = markers.keys().map(String::as_str).collect();
            let cargo = rule::cargo_roots_from_markers(&paths, &members);
            markers
                .iter()
                .filter(|(mp, _)| {
                    !rule::classify_path(mp, &cargo, &members)
                        .is_some_and(|a| b.is_boundary(&a.path))
                })
                .collect()
        }
    };
    let paths: Vec<&str> = markers.keys().map(|k| k.as_str()).collect();
    let derived = rule::marker_pruned_trees(&paths, &members);
    let mut pruned_trees = derived.clone();
    let refuse = |detail: &'static str,
                  roots: Vec<String>,
                  extra: Vec<(&'static str, V)>,
                  pruned: &[PrunedTreeRow]| UnitDiscovery {
        units: Vec::new(),
        pruned_trees: pruned.to_vec(),
        boundaries: boundaries_out(boundaries, &[]),
        refused: Some(UnitRefusal {
            detail,
            roots,
            extra,
        }),
    };
    if let Some(b) = boundaries {
        // U-8, a subset test over (path, reason): every derived anchor must be admitted.
        let admitted: BTreeSet<(&str, &str)> = b
            .pruned_trees()
            .iter()
            .map(|t| (t.anchor.path.as_str(), t.anchor.reason.as_str()))
            .collect();
        let mut missing: Vec<(&str, &str)> = derived
            .iter()
            .map(|t| (t.anchor.path.as_str(), t.anchor.reason.as_str()))
            .filter(|key| !admitted.contains(key))
            .collect();
        missing.sort();
        missing.dedup();
        if !missing.is_empty() {
            let missing_json = V::Array(
                missing
                    .iter()
                    .map(|(p, r)| obj(vec![("path", s(p)), ("reason", s(r))]))
                    .collect(),
            );
            return refuse(
                "native.boundary-inventory-mismatch",
                Vec::new(),
                vec![
                    ("missingAnchors", missing_json),
                    (
                        "expectedPrunedTrees",
                        V::Array(derived.iter().map(pruned_row_json).collect()),
                    ),
                    (
                        "inventoryPrunedTrees",
                        V::Array(b.pruned_trees().iter().map(pruned_row_json).collect()),
                    ),
                ],
                &pruned_trees,
            );
        }
        pruned_trees = b.pruned_trees().to_vec();
    }
    let cargo_roots = rule::cargo_roots_from_markers(&paths, &members);
    let mut by_dir: BTreeMap<String, BTreeMap<String, (MarkerFact, String)>> = BTreeMap::new();
    let mut excluded: Vec<(String, String, &'static str, String)> = Vec::new();
    for (mp, info) in &markers {
        if rule::classify_path(mp, &cargo_roots, &members).is_some() {
            continue;
        }
        let (dir, name) = mp.rsplit_once('/').unwrap_or(("", mp.as_str()));
        if let Some((anchor, reason)) = boundary_hit(dir, boundaries, Some(name)) {
            excluded.push((dir.to_owned(), name.to_owned(), reason, anchor));
            continue;
        }
        by_dir
            .entry(dir.to_owned())
            .or_default()
            .insert(name.to_owned(), ((*info).clone(), (*mp).clone()));
    }
    excluded.sort_by(|a, b| (a.0.as_bytes(), a.1.as_str()).cmp(&(b.0.as_bytes(), b.1.as_str())));
    let excluded_json: Vec<V> = excluded
        .iter()
        .map(|(path, marker, reason, anchor)| {
            obj(vec![
                ("path", s(path)),
                ("marker", s(marker)),
                ("reason", s(reason)),
                ("anchor", s(anchor)),
            ])
        })
        .collect();
    if let Some(specs) = explicit_roots {
        let mut roots = Vec::new();
        for spec in specs {
            match rule::normalize_explicit_root(spec) {
                Ok(root) => roots.push(root),
                Err(_) => {
                    return refuse(
                        "native.explicit-root-grammar",
                        vec![spec.clone()],
                        Vec::new(),
                        &pruned_trees,
                    );
                }
            }
        }
        for root in &roots {
            if let Some((anchor, reason)) = boundary_hit(root, boundaries, None) {
                return refuse(
                    "native.explicit-root-crosses-boundary",
                    vec![rule::spell_root(root).to_owned()],
                    vec![("anchor", s(&anchor)), ("reason", s(reason))],
                    &pruned_trees,
                );
            }
        }
        let mut missing: Vec<&String> = roots
            .iter()
            .filter(|r| by_dir.get(*r).is_none_or(BTreeMap::is_empty))
            .collect();
        missing.sort();
        if !missing.is_empty() {
            return refuse(
                "native.explicit-root-without-marker",
                missing
                    .iter()
                    .map(|r| rule::spell_root(r).to_owned())
                    .collect(),
                Vec::new(),
                &pruned_trees,
            );
        }
        let selected: BTreeSet<&String> = roots.iter().collect();
        let workspaces: Vec<&String> = selected
            .iter()
            .copied()
            .filter(|d| {
                by_dir[*d]
                    .get("Cargo.toml")
                    .is_some_and(|(f, _)| f.is_cargo_workspace == Some(true))
            })
            .collect();
        let mut kept = BTreeMap::new();
        for (dir, found) in by_dir {
            if selected.contains(&dir) {
                kept.insert(dir, found);
            } else if let Some(cargo) = found.get("Cargo.toml")
                && workspaces.iter().any(|w| **w != dir && under_unit(&dir, w))
            {
                let mut only = BTreeMap::new();
                only.insert("Cargo.toml".to_owned(), cargo.clone());
                kept.insert(dir, only);
            }
        }
        by_dir = kept;
    }
    if by_dir.len() > rule::MAX_WORKSPACE_UNITS {
        return refuse(
            "native.too-many-units",
            Vec::new(),
            vec![
                ("unitCount", int(by_dir.len())),
                ("limit", int(rule::MAX_WORKSPACE_UNITS)),
            ],
            &pruned_trees,
        );
    }
    let provenance = if explicit_roots.is_some() {
        "EXPLICIT"
    } else {
        "DISCOVERED"
    };
    let mut dirs: Vec<&String> = by_dir.keys().collect();
    dirs.sort_by_key(|d| {
        (
            if d.is_empty() {
                -1
            } else {
                i64::try_from(d.matches('/').count()).unwrap_or(i64::MAX)
            },
            d.as_str(),
        )
    });
    let mut units: Vec<WorkspaceUnit> = Vec::new();
    for dir in dirs {
        let found = &by_dir[dir];
        if let Some((fact, marker_path)) = found.get("Cargo.toml") {
            let enclosing = units
                .iter()
                .enumerate()
                .filter(|(_, u)| {
                    u.language_family == Family::Rust
                        && u.unit_kind == "cargo-workspace"
                        && u.root_path != *dir
                        && under_unit(dir, &u.root_path)
                })
                .max_by_key(|(_, u)| u.root_path.len())
                .map(|(i, _)| i);
            match enclosing {
                Some(i) => {
                    let mut set: BTreeSet<String> =
                        units[i].member_package_roots.iter().cloned().collect();
                    set.insert(dir.clone());
                    units[i].member_package_roots = set.into_iter().collect();
                }
                None => {
                    let kind = if fact.is_cargo_workspace == Some(true) {
                        "cargo-workspace"
                    } else {
                        "cargo-package"
                    };
                    units.push(WorkspaceUnit {
                        unit_ordinal: 0,
                        root_path: dir.clone(),
                        language_family: Family::Rust,
                        language_mode: "rust-cargo".to_owned(),
                        unit_kind: kind.to_owned(),
                        marker_path: marker_path.clone(),
                        marker_sha256: Some(fact.sha256.clone()),
                        recognizer_id: kind.to_owned(),
                        recognizer_version: 1,
                        provenance: provenance.to_owned(),
                        member_package_roots: Vec::new(),
                    });
                }
            }
        }
        if let Some((marker, (fact, marker_path))) = TSJS_MARKERS
            .iter()
            .find_map(|m| found.get(*m).map(|f| (*m, f)))
        {
            let mode = match marker {
                "tsconfig.json" if fact.allow_js == Some(true) => "js-allowjs",
                "tsconfig.json" => "ts-tsconfig",
                "jsconfig.json" if fact.allow_js.unwrap_or(true) => "js-allowjs",
                "jsconfig.json" => "ts-tsconfig",
                _ => "js-synthesized",
            };
            units.push(WorkspaceUnit {
                unit_ordinal: 0,
                root_path: dir.clone(),
                language_family: Family::Tsjs,
                language_mode: mode.to_owned(),
                unit_kind: if mode == "ts-tsconfig" {
                    "ts-program"
                } else {
                    "js-program"
                }
                .to_owned(),
                marker_path: marker_path.clone(),
                marker_sha256: Some(fact.sha256.clone()),
                recognizer_id: if marker == "package.json" {
                    "node-package"
                } else {
                    "typescript-config"
                }
                .to_owned(),
                recognizer_version: 1,
                provenance: provenance.to_owned(),
                member_package_roots: Vec::new(),
            });
        }
    }
    if units.is_empty() && explicit_roots.is_none() && boundary_hit("", boundaries, None).is_none()
    {
        // U-9: the one syntax-only fallback unit.
        units.push(WorkspaceUnit {
            unit_ordinal: 0,
            root_path: String::new(),
            language_family: Family::None,
            language_mode: "syntax-only".to_owned(),
            unit_kind: "syntax-only".to_owned(),
            marker_path: String::new(),
            marker_sha256: None,
            recognizer_id: "syntax-only-fallback".to_owned(),
            recognizer_version: 1,
            provenance: "DEFAULTED".to_owned(),
            member_package_roots: Vec::new(),
        });
    }
    units.sort_by(|a, b| {
        (a.root_path.as_bytes(), a.language_family.as_str())
            .cmp(&(b.root_path.as_bytes(), b.language_family.as_str()))
    });
    for (i, u) in units.iter_mut().enumerate() {
        u.unit_ordinal = i;
    }
    if units
        .iter()
        .map(|u| u.root_path.as_str())
        .collect::<BTreeSet<_>>()
        .len()
        > rule::MAX_WORKSPACE_UNITS
    {
        return refuse(
            "native.too-many-units",
            Vec::new(),
            Vec::new(),
            &pruned_trees,
        );
    }
    let out = UnitDiscovery {
        units,
        pruned_trees,
        boundaries: boundaries_out(boundaries, &excluded_json),
        refused: None,
    };
    // B-S1 U-8: a nested vcs-tree anchor names a member path (B2-c0 r2's full predicate).
    if let Some(b) = boundaries {
        let mut anchors: BTreeSet<&str> = out
            .pruned_trees
            .iter()
            .filter(|t| t.anchor.reason.as_str() == "vcs-tree")
            .map(|t| t.anchor.path.as_str())
            .collect();
        anchors.extend(
            b.pruned_trees()
                .iter()
                .filter(|t| t.anchor.reason.as_str() == "vcs-tree")
                .map(|t| t.anchor.path.as_str()),
        );
        for anchor in anchors {
            let (parent, name) = anchor.rsplit_once('/').unwrap_or(("", anchor));
            if !VCS_MARKERS.contains(&name) || parent.is_empty() || b.is_boundary(parent) {
                continue;
            }
            if !members.contains(parent) {
                return UnitDiscovery {
                    units: Vec::new(),
                    pruned_trees: out.pruned_trees.clone(),
                    boundaries: out.boundaries.clone(),
                    refused: Some(UnitRefusal {
                        detail: "native.boundary-inventory-mismatch",
                        roots: Vec::new(),
                        extra: vec![("anchor", s(anchor)), ("reason", s("member-not-admitted"))],
                    }),
                };
            }
        }
    }
    out
}

// ------------------------------------------------------------------ U-3 and U-4: membership

fn family_of(path: &str) -> Family {
    if RUST_EXT.iter().any(|e| path.ends_with(e)) {
        Family::Rust
    } else if TSJS_EXT.iter().any(|e| path.ends_with(e)) {
        Family::Tsjs
    } else {
        Family::None
    }
}
fn extension(path: &str) -> &str {
    let name = path.rsplit('/').next().unwrap_or(path);
    name.rfind('.').map_or("", |i| &name[i..])
}
fn cargo_roots_of_units(units: &[WorkspaceUnit]) -> BTreeSet<String> {
    let mut roots = BTreeSet::new();
    for u in units.iter().filter(|u| u.language_family == Family::Rust) {
        roots.insert(u.root_path.clone());
        roots.extend(u.member_package_roots.iter().cloned());
    }
    roots
}

/// `assign_membership` (U-3, U-4, U-4b item 4): exactly one row per file.
fn membership(
    units: &[WorkspaceUnit],
    files: &[String],
    boundaries: Option<&AdmittedBoundaries>,
) -> Result<V, InternalFault> {
    admit_unit_roots(units)?;
    let members = members_of(boundaries);
    let cargo_roots = cargo_roots_of_units(units);
    let mut sorted: Vec<&String> = files.iter().collect();
    sorted.sort_by(|a, b| a.as_bytes().cmp(b.as_bytes()));
    let (mut rows, mut unsupported, mut outside) = (Vec::new(), Vec::new(), Vec::new());
    let row =
        |path: &str, family: Family, ordinal: Option<usize>, membership: &str, reason: &str| {
            obj(vec![
                ("path", s(path)),
                ("languageFamily", s(family.as_str())),
                ("unitOrdinal", ordinal.map_or(V::Null, int)),
                ("membership", s(membership)),
                ("reason", s(reason)),
            ])
        };
    for f in sorted {
        if let Some((_, reason)) = boundary_hit(f, boundaries, None) {
            rows.push(row(
                f,
                family_of(f),
                None,
                "outside-project-boundary",
                reason,
            ));
            outside.push(f.clone());
            continue;
        }
        if rule::classify_path(f, &cargo_roots, &members).is_some() {
            rows.push(row(
                f,
                family_of(f),
                None,
                "syntax-only",
                "host-ignore-convention",
            ));
            continue;
        }
        let family = family_of(f);
        if family == Family::None {
            if BUNDLED_GRAMMARS.contains(&extension(f)) {
                rows.push(row(f, family, None, "syntax-only", "grammar-only"));
            } else {
                rows.push(row(
                    f,
                    family,
                    None,
                    "unsupported-file",
                    "no-bundled-grammar",
                ));
                unsupported.push(f.clone());
            }
            continue;
        }
        let deepest = units
            .iter()
            .filter(|u| u.language_family == family && under_unit(f, &u.root_path))
            .max_by(|a, b| {
                (a.root_path.len(), std::cmp::Reverse(a.unit_ordinal))
                    .cmp(&(b.root_path.len(), std::cmp::Reverse(b.unit_ordinal)))
            });
        match deepest {
            None => rows.push(row(
                f,
                family,
                None,
                "syntax-only",
                "no-program-unit-for-language",
            )),
            Some(u) => rows.push(row(
                f,
                family,
                Some(u.unit_ordinal),
                "program-member",
                "deepest-unit-in-language",
            )),
        }
    }
    Ok(obj(vec![
        ("schemaVersion", int(1)),
        (
            "units",
            V::Array(units.iter().map(WorkspaceUnit::to_json).collect()),
        ),
        ("rows", V::Array(rows)),
        ("unsupportedFiles", strings(&unsupported)),
        ("outsideBoundaryFiles", strings(&outside)),
        ("erasedFiles", V::Array(Vec::new())),
    ]))
}

// ------------------------------------------------------------------ the scope descriptor

/// `PROJECT.SCOPE_LIMIT`: an admitted population that cannot fit, never truncated.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct ScopeRefusal {
    pub(crate) field: &'static str,
    pub(crate) count: usize,
    pub(crate) limit: usize,
}
impl ScopeRefusal {
    pub(crate) fn key(&self) -> String {
        format!(
            "PROJECT.SCOPE_LIMIT:{}:{}>{}",
            self.field, self.count, self.limit
        )
    }
}

/// Why a scope descriptor cannot be built.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) enum ScopeFault {
    Limit(ScopeRefusal),
    Internal(InternalFault),
}

/// `unit_scope_descriptor`: the foundation scope record, its `scopeDigest`,
/// and the boundary provenance beside it.
fn scope_descriptor(
    units: &[WorkspaceUnit],
    ignore_paths: &[String],
    explicit_path_prefixes: Option<&[String]>,
    pruned_trees: Option<&[PrunedTreeRow]>,
    boundaries: Option<&AdmittedBoundaries>,
) -> Result<V, ScopeFault> {
    admit_unit_roots(units).map_err(ScopeFault::Internal)?;
    let members = members_of(boundaries);
    let roots: Vec<String> = units
        .iter()
        .map(|u| u.root_path.clone())
        .collect::<BTreeSet<_>>()
        .into_iter()
        .collect();
    let spelled: Vec<String> = roots
        .iter()
        .map(|r| rule::spell_root(r).to_owned())
        .collect();
    let conventional =
        rule::conventional_excluded_prefixes(&roots, &cargo_roots_of_units(units), &members);
    let boundary = boundaries.map_or_else(Vec::new, AdmittedBoundaries::excluded_prefixes);
    let mut excluded: BTreeSet<String> = ignore_paths
        .iter()
        .map(|p| p.trim_end_matches('/').to_owned())
        .collect();
    excluded.extend(conventional);
    excluded.extend(
        pruned_trees
            .unwrap_or(&[])
            .iter()
            .map(|t| t.anchor.path.clone()),
    );
    excluded.extend(boundary.iter().cloned());
    let excluded: Vec<String> = excluded.into_iter().collect();
    let prefixes: Vec<String> = match explicit_path_prefixes {
        Some(p) if !p.is_empty() => p
            .iter()
            .cloned()
            .collect::<BTreeSet<_>>()
            .into_iter()
            .collect(),
        _ => spelled
            .iter()
            .cloned()
            .collect::<BTreeSet<_>>()
            .into_iter()
            .collect(),
    };
    for ((field, limit), list) in SCOPE_LIMITS.iter().zip([&spelled, &prefixes, &excluded]) {
        if list.len() > *limit {
            return Err(ScopeFault::Limit(ScopeRefusal {
                field,
                count: list.len(),
                limit: *limit,
            }));
        }
        if list.iter().any(|t| t.is_empty() || chars(t) > 4096) {
            return Err(ScopeFault::Internal(InternalFault(
                "schema-invalid".to_owned(),
            )));
        }
    }
    let desc = obj(vec![
        ("schemaVersion", int(2)),
        ("workspaceRoots", strings(&spelled)),
        ("pathPrefixes", strings(&prefixes)),
        ("excludedPathPrefixes", strings(&excluded)),
    ]);
    let bytes =
        canonical_bytes(&desc).map_err(|e| ScopeFault::Internal(InternalFault(e.to_string())))?;
    let digest = digest_hex(&raw_sha256(&bytes));
    let disclosure = match boundaries {
        None => obj(vec![
            ("source", s("none")),
            ("nestedRepositories", V::Array(Vec::new())),
            ("nestedProjects", V::Array(Vec::new())),
            ("custodyExcludedUnits", V::Array(Vec::new())),
            ("excludedPathPrefixesFromBoundaries", strings(&boundary)),
            ("disclosure", s(NO_BOUNDARY_DISCLOSURE)),
        ]),
        Some(b) => obj(vec![
            ("source", s("security.discovery")),
            ("nestedRepositories", strings(b.nested_repositories())),
            ("nestedProjects", strings(b.nested_projects())),
            (
                "custodyExcludedUnits",
                custody_json(b.custody_excluded_units()),
            ),
            ("excludedPathPrefixesFromBoundaries", strings(&boundary)),
            ("disclosure", s(BOUNDARY_DISCLOSURE)),
        ]),
    };
    Ok(obj(vec![
        ("scopeDescriptor", desc),
        ("scopeDigest", s(&digest)),
        ("boundaries", disclosure),
    ]))
}

// ------------------------------------------------------------------ the entries (r2, Codex B2C1-R1-RF-1)

/// The authoritative composition's gate (NE U-8): a missing inventory refuses
/// with the internal key, which has no public detail (plan r2 section 2.3).
pub(crate) fn require_admitted_boundaries(
    boundaries: Option<&AdmittedBoundaries>,
) -> Result<&AdmittedBoundaries, InternalFault> {
    boundaries.ok_or_else(|| InternalFault("native.admitted-boundaries-required".to_owned()))
}

/// `discover_units` over the admitted inventory: the only production entry.
pub(crate) fn discover_units(
    markers: &BTreeMap<String, MarkerFact>,
    explicit_roots: Option<&[String]>,
    boundaries: &AdmittedBoundaries,
) -> UnitDiscovery {
    discover(markers, explicit_roots, Some(boundaries))
}

/// `assign_membership` over the admitted inventory.
pub(crate) fn assign_membership(
    units: &[WorkspaceUnit],
    files: &[String],
    boundaries: &AdmittedBoundaries,
) -> Result<V, InternalFault> {
    membership(units, files, Some(boundaries))
}

/// `unit_scope_descriptor` over the admitted inventory.
pub(crate) fn unit_scope_descriptor(
    units: &[WorkspaceUnit],
    ignore_paths: &[String],
    explicit_path_prefixes: Option<&[String]>,
    pruned_trees: Option<&[PrunedTreeRow]>,
    boundaries: &AdmittedBoundaries,
) -> Result<V, ScopeFault> {
    scope_descriptor(
        units,
        ignore_paths,
        explicit_path_prefixes,
        pruned_trees,
        Some(boundaries),
    )
}

/// The standalone pure instrument (`boundaries=None`: fixtures only; its
/// output discloses `source: none`). Never compiled outside tests.
#[cfg(test)]
pub(crate) mod standalone {
    use super::InternalFault;
    use super::{BTreeMap, MarkerFact, PrunedTreeRow, ScopeFault, UnitDiscovery, V, WorkspaceUnit};
    pub(crate) fn discover_units(
        markers: &BTreeMap<String, MarkerFact>,
        explicit_roots: Option<&[String]>,
    ) -> UnitDiscovery {
        super::discover(markers, explicit_roots, None)
    }
    pub(crate) fn assign_membership(
        units: &[WorkspaceUnit],
        files: &[String],
    ) -> Result<V, InternalFault> {
        super::membership(units, files, None)
    }
    pub(crate) fn unit_scope_descriptor(
        units: &[WorkspaceUnit],
        ignore_paths: &[String],
        explicit_path_prefixes: Option<&[String]>,
        pruned_trees: Option<&[PrunedTreeRow]>,
    ) -> Result<V, ScopeFault> {
        super::scope_descriptor(
            units,
            ignore_paths,
            explicit_path_prefixes,
            pruned_trees,
            None,
        )
    }
}

// ------------------------------------------------------------------ default selection (AQ:76-99)

/// A release declaration row (`ReleaseCapabilityDeclarationV1`).
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct ReleaseDeclaration {
    pub(crate) capability_id: String,
    pub(crate) language_modes: Vec<String>,
}

/// Why a default selection cannot be made: a reference internal key, the
/// analysis-spec cardinality bound, or a malformed registry.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) enum SelectionFault {
    Key(String),
    Limit(ScopeRefusal),
    SchemaInvalid,
}

struct Matrix {
    /// Capability id and its relation@rung pairs, in matrix order.
    capabilities: Vec<(String, Vec<String>)>,
    modes: Vec<String>,
    not_selected: BTreeSet<(String, String)>,
}

fn matrix() -> Result<Matrix, SelectionFault> {
    let bad = || SelectionFault::Key("NATIVE_CAPABILITY_MATRIX".to_owned());
    let V::Object(m) = parse_json(CAPABILITY_MATRIX).map_err(|_| bad())? else {
        return Err(bad());
    };
    let text = |v: &V| match v {
        V::String(t) => Some(t.clone()),
        _ => None,
    };
    let array = |v: Option<&V>| match v {
        Some(V::Array(a)) => Some(a.clone()),
        _ => None,
    };
    let mut capabilities = Vec::new();
    for c in array(m.get("capabilities")).ok_or_else(bad)? {
        let V::Object(c) = c else { return Err(bad()) };
        let id = c.get("id").and_then(text).ok_or_else(bad)?;
        let mut relations = Vec::new();
        for r in array(c.get("relations")).ok_or_else(bad)? {
            let V::Array(pair) = r else { return Err(bad()) };
            let (Some(rel), Some(rung)) = (pair.first().and_then(text), pair.get(1).and_then(text))
            else {
                return Err(bad());
            };
            relations.push(format!("{rel}@{rung}"));
        }
        capabilities.push((id, relations));
    }
    let modes = array(m.get("languageModes"))
        .ok_or_else(bad)?
        .iter()
        .map(text)
        .collect::<Option<Vec<_>>>()
        .ok_or_else(bad)?;
    let mut not_selected = BTreeSet::new();
    for cell in array(m.get("cells")).ok_or_else(bad)? {
        let V::Object(cell) = cell else {
            return Err(bad());
        };
        let (Some(cap), Some(mode), Some(state)) = (
            cell.get("capability").and_then(text),
            cell.get("mode").and_then(text),
            cell.get("state").and_then(text),
        ) else {
            return Err(bad());
        };
        if state == "NOT-SELECTED" {
            not_selected.insert((cap, mode));
        }
    }
    Ok(Matrix {
        capabilities,
        modes,
        not_selected,
    })
}

fn capability_id_shape(id: &str) -> bool {
    let mut bytes = id.bytes();
    !id.is_empty()
        && id.len() <= 128
        && bytes.next().is_some_and(|b| b.is_ascii_lowercase())
        && bytes.all(|b| b.is_ascii_lowercase() || b.is_ascii_digit() || b"._:-".contains(&b))
}

/// `admit_release_capability_registry`: the closed shape, then membership.
fn admit_registry(registry: &[ReleaseDeclaration], m: &Matrix) -> Result<(), SelectionFault> {
    if registry.len() > RELEASE_REGISTRY_BOUND {
        return Err(SelectionFault::SchemaInvalid);
    }
    for row in registry {
        let modes_ok = !row.language_modes.is_empty()
            && row.language_modes.len() <= 6
            && row
                .language_modes
                .iter()
                .all(|mode| !mode.is_empty() && mode.len() <= 128)
            && row
                .language_modes
                .windows(2)
                .all(|w| w[0].as_bytes() < w[1].as_bytes());
        if !capability_id_shape(&row.capability_id) || !modes_ok {
            return Err(SelectionFault::SchemaInvalid);
        }
    }
    let mut seen = BTreeSet::new();
    for row in registry {
        let cap = &row.capability_id;
        if cap.starts_with("preview-") {
            return Err(SelectionFault::Key(format!(
                "native.release-capability-preview-constant:{cap}"
            )));
        }
        if !m.capabilities.iter().any(|(id, _)| id == cap) {
            return Err(SelectionFault::Key(format!(
                "native.release-capability-unregistered:{cap}"
            )));
        }
        if !seen.insert(cap.as_str()) {
            return Err(SelectionFault::Key(format!(
                "native.release-capability-duplicate:{cap}"
            )));
        }
        for mode in &row.language_modes {
            if !m.modes.contains(mode) {
                return Err(SelectionFault::Key(format!(
                    "native.release-capability-mode-unregistered:{cap}:{mode}"
                )));
            }
            if m.not_selected.contains(&(cap.clone(), mode.clone())) {
                return Err(SelectionFault::Key(format!(
                    "native.release-capability-mode-not-selected:{cap}:{mode}"
                )));
            }
        }
    }
    Ok(())
}

fn canonical_key(v: &V) -> Vec<u8> {
    canonical_bytes(v).unwrap_or_default()
}

/// `default_capability_selection`: every non-`NOT-SELECTED` capability per
/// unit, requested; a release absence disclosed, never dropped. The full
/// analysis-spec admission of an externally supplied spec is the Plan
/// stage's (J1); this applies its cardinality bound and the ownership-tuple
/// law to the defaulted rows, which the matrix vocabulary already closes.
pub(crate) fn default_capability_selection(
    units: &[WorkspaceUnit],
    registry: &[ReleaseDeclaration],
) -> Result<V, SelectionFault> {
    let m = matrix()?;
    admit_registry(registry, &m)?;
    if units.is_empty() {
        return Err(SelectionFault::Key(
            "NATIVE_DEFAULT_SELECTION_WITHOUT_UNIT".to_owned(),
        ));
    }
    let available: BTreeSet<(&str, &str)> = registry
        .iter()
        .flat_map(|r| {
            r.language_modes
                .iter()
                .map(move |mode| (r.capability_id.as_str(), mode.as_str()))
        })
        .collect();
    let (mut requested, mut undeclared) = (Vec::new(), Vec::new());
    for u in units {
        let mode = u.language_mode.as_str();
        let root = if u.root_path.is_empty() {
            "."
        } else {
            u.root_path.as_str()
        };
        let mut required: Vec<&(String, Vec<String>)> = m
            .capabilities
            .iter()
            .filter(|(id, _)| !m.not_selected.contains(&(id.clone(), mode.to_owned())))
            .collect();
        required.sort_by(|a, b| a.0.cmp(&b.0));
        for (capability, relations) in required {
            requested.push(obj(vec![
                ("capabilityId", s(capability)),
                ("languageMode", s(mode)),
                ("workspaceRoot", s(root)),
                ("required", V::Bool(true)),
            ]));
            if !available.contains(&(capability.as_str(), mode)) {
                undeclared.push(obj(vec![
                    ("capabilityId", s(capability)),
                    ("languageMode", s(mode)),
                    ("workspaceRoot", s(root)),
                    (
                        "projection",
                        s(if relations.is_empty() {
                            "selection-account-only"
                        } else {
                            "coverage-entry"
                        }),
                    ),
                    ("relations", strings(relations)),
                    ("declared", V::Bool(false)),
                    ("candidateDeficiency", s("provider-unavailable")),
                    ("candidateNativeCause", s("capability-missing")),
                    ("subjectToPrecedence", V::Bool(true)),
                ]));
            }
        }
    }
    requested.sort_by_key(canonical_key);
    let mut owners: BTreeMap<(String, String, String), usize> = BTreeMap::new();
    for row in &requested {
        let V::Object(r) = row else { continue };
        let get = |k: &str| match r.get(k) {
            Some(V::String(t)) => t.clone(),
            _ => String::new(),
        };
        *owners
            .entry((
                get("capabilityId"),
                get("languageMode"),
                get("workspaceRoot"),
            ))
            .or_default() += 1;
    }
    if let Some(((c, mode, root), _)) = owners.iter().find(|(_, n)| **n > 1) {
        return Err(SelectionFault::Key(format!(
            "native.requested-capability-duplicate-ownership-tuple:{c}:{mode}:{root}"
        )));
    }
    if requested.len() > REQUESTED_CAPABILITY_BOUND {
        return Err(SelectionFault::Limit(ScopeRefusal {
            field: "requestedCapabilities",
            count: requested.len(),
            limit: REQUESTED_CAPABILITY_BOUND,
        }));
    }
    // r2 (Codex B2C1-R1-RF-3): the closed vocabulary over the defaulted rows,
    // in their canonical order, as the reference's `admit_requested_capabilities`.
    for row in &requested {
        let V::Object(r) = row else { continue };
        let (Some(V::String(capability)), Some(V::String(mode))) =
            (r.get("capabilityId"), r.get("languageMode"))
        else {
            continue;
        };
        if !m.capabilities.iter().any(|(id, _)| id == capability) {
            return Err(SelectionFault::Key(format!(
                "native.requested-capability-unregistered:{capability}"
            )));
        }
        if !m.modes.contains(mode) {
            return Err(SelectionFault::Key(format!(
                "native.requested-capability-mode-unregistered:{capability}:{mode}"
            )));
        }
        if m.not_selected.contains(&(capability.clone(), mode.clone())) {
            return Err(SelectionFault::Key(format!(
                "native.requested-capability-mode-not-selected:{capability}:{mode}"
            )));
        }
    }
    undeclared.sort_by_key(canonical_key);
    let families: BTreeSet<&str> = units.iter().map(|u| u.language_family.as_str()).collect();
    let families: Vec<&str> = families.into_iter().collect();
    Ok(obj(vec![
        (
            "analysisSpec",
            obj(vec![
                ("schemaVersion", int(2)),
                ("requestedCapabilities", V::Array(requested)),
                ("policyPackIds", V::Array(Vec::new())),
                ("parameters", V::Array(Vec::new())),
            ]),
        ),
        ("familiesSelected", strings(&families)),
        ("previewDefaultsUsed", V::Bool(false)),
        ("provenance", s("DEFAULTED")),
        ("undeclaredCapabilities", V::Array(undeclared)),
        ("defaultIsCompleteCapabilitySelection", V::Bool(true)),
    ]))
}
