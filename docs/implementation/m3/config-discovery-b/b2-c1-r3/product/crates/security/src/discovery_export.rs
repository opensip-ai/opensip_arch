//! M3-B r7 item 14 (unit B2-c1, B2-c plan r2 LD-B2C-2): the narrow surface the
//! host's native unit instrument consumes. The shared discovery rule is stated
//! once, in `custody::discovery_rule` (unit B2-a), and is called from here; it
//! is never copied, and its file is unchanged (the census pins it whole). The
//! public types below mirror its crate-private ones, field for field.
//! `AdmittedBoundaries` is the admitted `AdmittedBoundaryInventoryV3` the
//! native instrument requires: only this crate constructs one from an
//! accepted discovery result, so a caller cannot hand the instrument an
//! ignore list in its place (NE U-8). Tests and scenario fixtures admit a
//! record against the closed V3 shape through `scenario::admitted_boundaries`.
use crate::custody::discovery_rule as rule;
use std::collections::BTreeSet;

/// The selected root in internal form, and the explicit-root sentinel.
pub const INTERNAL_ROOT: &str = rule::INTERNAL_ROOT;
pub const ROOT_SENTINEL: &str = rule::ROOT_SENTINEL;
/// The first-party unit cap, shared with security (U-7).
pub const MAX_WORKSPACE_UNITS: usize = rule::MAX_WORKSPACE_UNITS;

/// Why a tree is pruned (`PrunedTreeRowV3.reason`).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum PruneReason {
    DependencyTree,
    VcsTree,
    CargoBuildOutput,
    OpensipCustodyState,
}
impl PruneReason {
    pub fn as_str(self) -> &'static str {
        self.inner().as_str()
    }
    fn inner(self) -> rule::PruneReason {
        match self {
            Self::DependencyTree => rule::PruneReason::DependencyTree,
            Self::VcsTree => rule::PruneReason::VcsTree,
            Self::CargoBuildOutput => rule::PruneReason::CargoBuildOutput,
            Self::OpensipCustodyState => rule::PruneReason::OpensipCustodyState,
        }
    }
    fn of(reason: rule::PruneReason) -> Self {
        match reason {
            rule::PruneReason::DependencyTree => Self::DependencyTree,
            rule::PruneReason::VcsTree => Self::VcsTree,
            rule::PruneReason::CargoBuildOutput => Self::CargoBuildOutput,
            rule::PruneReason::OpensipCustodyState => Self::OpensipCustodyState,
        }
    }
}

/// The outermost pruned segment a path lies at or below.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct PrunedAnchor {
    pub path: String,
    pub reason: PruneReason,
}

/// Whether a pruned-tree count is over the supplied inventory.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum MarkerCountBasis {
    NotEnumerated,
    ObservedInventory,
}
impl MarkerCountBasis {
    pub fn as_str(self) -> &'static str {
        match self {
            Self::NotEnumerated => rule::MarkerCountBasis::NotEnumerated.as_str(),
            Self::ObservedInventory => rule::MarkerCountBasis::ObservedInventory.as_str(),
        }
    }
}

/// A pruned-tree row: `markerCount` is `None` exactly when not enumerated.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct PrunedTreeRow {
    pub anchor: PrunedAnchor,
    pub marker_count: Option<u64>,
    pub basis: MarkerCountBasis,
}

/// A security `excludedUnits` row the native instrument consumes.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CustodyExcludedUnit {
    pub path: String,
    pub reason: String,
}

/// An explicit root that is not the sentinel or a strict logical path.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct RootGrammar;

/// The rule's `normalize_explicit_root`: `.` is `""`; one trailing `/` of a
/// CLI value is dropped; any other malformed value refuses.
pub fn normalize_explicit_root(spec: &str) -> Result<String, RootGrammar> {
    rule::normalize_explicit_root(spec).map_err(|_| RootGrammar)
}

/// The rule's `spell_root`: `""` is spelled `.`.
pub fn spell_root(internal_root: &str) -> &str {
    rule::spell_root(internal_root)
}

/// The rule's `classify_path`: the outermost pruned anchor of `relpath`.
pub fn classify_path(
    relpath: &str,
    cargo_roots: &BTreeSet<String>,
    member_roots: &BTreeSet<String>,
) -> Option<PrunedAnchor> {
    rule::classify_path(relpath, cargo_roots, member_roots).map(|a| PrunedAnchor {
        path: a.path,
        reason: PruneReason::of(a.reason),
    })
}

/// The rule's `cargo_roots_from_markers`.
pub fn cargo_roots_from_markers<S: AsRef<str>>(
    marker_relpaths: &[S],
    member_roots: &BTreeSet<String>,
) -> BTreeSet<String> {
    rule::cargo_roots_from_markers(marker_relpaths, member_roots)
}

/// The pruned trees the rule's `enumerate_units` derives from a marker
/// inventory alone (no directory observation, no limit): the native
/// instrument's derived anchors, counted over the supplied inventory.
pub fn marker_pruned_trees<S: AsRef<str>>(
    marker_relpaths: &[S],
    member_roots: &BTreeSet<String>,
) -> Vec<PrunedTreeRow> {
    let none: [S; 0] = [];
    let out = rule::enumerate_units(
        marker_relpaths,
        &rule::EnumerationInput {
            enforce_limit: false,
            observed_directories: None,
            basis: rule::MarkerCountBasis::ObservedInventory,
            unreadable_anchors: &none,
            member_roots,
        },
    );
    out.pruned_trees.into_iter().map(public_row).collect()
}

fn public_row(row: rule::PrunedTreeRow) -> PrunedTreeRow {
    PrunedTreeRow {
        anchor: PrunedAnchor {
            path: row.anchor.path,
            reason: PruneReason::of(row.anchor.reason),
        },
        marker_count: row.marker_count,
        basis: match row.basis {
            rule::MarkerCountBasis::NotEnumerated => MarkerCountBasis::NotEnumerated,
            rule::MarkerCountBasis::ObservedInventory => MarkerCountBasis::ObservedInventory,
        },
    }
}

/// The rule's `conventional_excluded_prefixes`.
pub fn conventional_excluded_prefixes<S: AsRef<str>>(
    unit_roots: &[S],
    cargo_roots: &BTreeSet<String>,
    member_roots: &BTreeSet<String>,
) -> Vec<String> {
    rule::conventional_excluded_prefixes(unit_roots, cargo_roots, member_roots)
}

/// An admitted `AdmittedBoundaryInventoryV3`: relative scope paths under the
/// selected root, in the record's own orders. Read-only.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct AdmittedBoundaries {
    selected_root: String,
    nested_repositories: Vec<String>,
    nested_projects: Vec<String>,
    custody_excluded_units: Vec<CustodyExcludedUnit>,
    pruned_trees: Vec<PrunedTreeRow>,
    member_repositories: Vec<String>,
}

impl AdmittedBoundaries {
    /// From an accepted discovery result's inventory (the composition J1 owns).
    #[allow(dead_code)]
    pub(crate) fn new(
        selected_root: String,
        nested_repositories: Vec<String>,
        nested_projects: Vec<String>,
        custody_excluded_units: Vec<CustodyExcludedUnit>,
        pruned_trees: Vec<PrunedTreeRow>,
        member_repositories: Vec<String>,
    ) -> Self {
        Self {
            selected_root,
            nested_repositories,
            nested_projects,
            custody_excluded_units,
            pruned_trees,
            member_repositories,
        }
    }
    pub fn selected_root(&self) -> &str {
        &self.selected_root
    }
    pub fn nested_repositories(&self) -> &[String] {
        &self.nested_repositories
    }
    pub fn nested_projects(&self) -> &[String] {
        &self.nested_projects
    }
    pub fn custody_excluded_units(&self) -> &[CustodyExcludedUnit] {
        &self.custody_excluded_units
    }
    pub fn pruned_trees(&self) -> &[PrunedTreeRow] {
        &self.pruned_trees
    }
    pub fn member_repositories(&self) -> &[String] {
        &self.member_repositories
    }

    fn custody(&self) -> Vec<rule::CustodyExcludedUnit> {
        self.custody_excluded_units
            .iter()
            .map(|r| rule::CustodyExcludedUnit {
                path: r.path.clone(),
                reason: r.reason.clone(),
            })
            .collect()
    }

    /// The native instrument's boundary hit (the selected `_boundary_hit`): the
    /// nested repository or project `path` is at or below, else a custody
    /// exclusion; with a marker name, a marker-custody row for exactly that
    /// marker in that directory also counts. `(anchor, reason)`.
    pub fn boundary_hit(&self, path: &str, marker: Option<&str>) -> Option<(String, &'static str)> {
        if let Some((anchor, reason)) =
            rule::classify_boundary(path, &self.nested_repositories, &self.nested_projects)
        {
            return Some((anchor.to_owned(), reason.as_str()));
        }
        let custody = self.custody();
        rule::classify_custody_exclusion(path, marker, &custody)
            .map(|anchor| (anchor.to_owned(), "custody-excluded"))
    }

    /// Whether `path` is at or below an admitted boundary: a nested repository
    /// or project, or a directory-custody or `DEPTH` exclusion (contract
    /// successor 166, B2-c0 r2). A marker-custody row is never a boundary here.
    pub fn is_boundary(&self, path: &str) -> bool {
        self.boundary_hit(path, None).is_some()
    }

    /// The rule's `boundary_excluded_prefixes` for this inventory.
    pub fn excluded_prefixes(&self) -> Vec<String> {
        rule::boundary_excluded_prefixes(
            &self.nested_repositories,
            &self.nested_projects,
            &self.custody(),
        )
    }
}

/// Why a record is not an admitted V3 inventory (`scenario::admitted_boundaries`).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum InventoryRecordRefusal {
    /// A record of another version: `native.boundary-inventory-version-unsupported:<n>`.
    VersionUnsupported(i128),
    /// Not the closed V3 shape.
    SchemaInvalid,
}
