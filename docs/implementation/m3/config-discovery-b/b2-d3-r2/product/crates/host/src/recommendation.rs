// M3-B r9 item 18 (unit B2-d3, B2-d plan r3 section 5): the recommendation
// evidence for M4's `recommend` (CH13:66-75), exposed by `discovery.rs`.
// Pure: it writes nothing (item 15) and reads only the recognitions and the
// resolver input its caller supplies. M3 wires no command.
//
// It returns CH13's five parts: the detected evidence, the proposed
// settings, the default rationale, the unresolved choices, and the effect of
// each choice. Every proposed setting is checked by the actual resolver
// (`configuration::resolve`, CH13:69-71): it is placed in the project
// carrier and resolved; a proposal the resolver refuses, or resolves to
// another value, is not proposed and is recorded as an unresolved choice.
// Applying no proposal changes nothing: the base is the configuration as
// resolved. Recognition paths are unit-root-relative; a proposed project
// setting is the path joined to its unit's `rootPath` (`""` is the project
// root), keeping its unit ordinal, root and recognizer (B2-d plan r3 RF-6).
use crate::configuration::{
    CapturedCarrierV1, ConfigurationRefusal, ResolvedConfigurationV1, ResolverInputV1, resolve,
};
use crate::framework_recognition::{RECOGNIZER_VERSION, discovered_provenance};
use opensip_identity::{JsonInteger, JsonValue as V, canonical_bytes, parse_json};
use std::collections::BTreeMap;

/// The project carrier's file name, when the input has no project carrier.
pub(crate) const PROJECT_CARRIER: &str = "opensip.json";
const ENTRY_POINTS: &str = "entryPoints";
const IGNORE_PATHS: &str = "ignorePaths";

/// One unit's recognition, as `framework_recognition::recognize` gave it.
pub(crate) struct RecognizedUnit<'a> {
    pub(crate) unit_ordinal: u64,
    pub(crate) root_path: &'a str,
    pub(crate) recognition: &'a V,
}

/// Where a detected result or a proposed path came from.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct Source {
    pub(crate) unit_ordinal: u64,
    pub(crate) root_path: String,
    pub(crate) recognizer_id: String,
}

/// One unit's detected evidence, lossless (r2, B2D3-R1-RF-1): its complete
/// `FrameworkRecognitionV1` (every result with its assurance, evidence,
/// unit-relative effects and unresolved choices; the hints; the entry
/// state), and each result's FR-2 provenance, in result order. Detected
/// effects stay unit-relative; only proposals are project paths.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct DetectedUnit {
    pub(crate) unit_ordinal: u64,
    pub(crate) root_path: String,
    pub(crate) recognition: V,
    /// `(recognizerId, DISCOVERED:<id>@<version>)` per result.
    pub(crate) provenance: Vec<(String, String)>,
}

/// One project path of a proposal, and every result it came from.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct ProposedPath {
    pub(crate) path: String,
    pub(crate) sources: Vec<Source>,
}

/// One proposed setting and its effect (r2, B2D3-R1-RF-2): the resolved
/// configuration with it, as the actual resolver gave it. The configuration
/// without it is the evidence's `base`.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct ProposedSetting {
    /// `discovery.entryPoints` or `discovery.ignorePaths`.
    pub(crate) field: &'static str,
    pub(crate) paths: Vec<ProposedPath>,
    pub(crate) resolved_with: ResolvedConfigurationV1,
}

/// Why a field keeps its default (nothing is proposed for it).
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct DefaultRationale {
    pub(crate) field: &'static str,
    pub(crate) reason: &'static str,
}

/// A choice the evidence cannot settle.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct UnresolvedChoice {
    pub(crate) source: Option<Source>,
    pub(crate) choice: String,
}

/// CH13:67-73's recommendation evidence.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct RecommendationEvidenceV1 {
    pub(crate) detected: Vec<DetectedUnit>,
    pub(crate) proposed: Vec<ProposedSetting>,
    pub(crate) defaults: Vec<DefaultRationale>,
    pub(crate) unresolved: Vec<UnresolvedChoice>,
    /// FR-3's observed hints, per unit.
    pub(crate) observed_hints: Vec<(u64, String)>,
    /// The configuration as resolved, with no proposal applied: every
    /// setting's effect is its `resolved_with` against this.
    pub(crate) base: ResolvedConfigurationV1,
}

fn field<'v>(value: &'v V, key: &str) -> &'v V {
    match value {
        V::Object(fields) => fields.get(key).unwrap_or(&V::Null),
        _ => &V::Null,
    }
}
fn texts(value: &V) -> Vec<&str> {
    match value {
        V::Array(items) => items
            .iter()
            .filter_map(|v| match v {
                V::String(s) => Some(s.as_str()),
                _ => None,
            })
            .collect(),
        _ => Vec::new(),
    }
}
fn text(value: &V) -> &str {
    match value {
        V::String(s) => s,
        _ => "",
    }
}
fn items(value: &V) -> &[V] {
    match value {
        V::Array(items) => items,
        _ => &[],
    }
}

/// A unit-root-relative path as a project path.
fn project_path(root: &str, path: &str) -> String {
    if root.is_empty() {
        path.to_owned()
    } else {
        format!("{root}/{path}")
    }
}

/// The resolver input with `discovery.<name>` set to `paths` in the project
/// carrier, every other field and layer kept: how a proposal is applied, in
/// memory only (applying one for real is a separate host operation with the
/// normal write authority, CH13:68-70). `None` when the carrier is not an
/// object with an object `discovery`.
pub(crate) fn apply_setting(
    input: &ResolverInputV1,
    name: &str,
    paths: &[String],
) -> Option<ResolverInputV1> {
    let (path, mut document) = match &input.project {
        Some(carrier) => match parse_json(&carrier.bytes).ok()? {
            V::Object(fields) => (carrier.path.clone(), fields),
            _ => return None,
        },
        None => {
            let mut fields = BTreeMap::new();
            fields.insert(
                "schemaVersion".to_owned(),
                V::Integer(JsonInteger::new(2).ok()?),
            );
            (PROJECT_CARRIER.to_owned(), fields)
        }
    };
    let mut discovery = match document.remove("discovery") {
        Some(V::Object(fields)) => fields,
        Some(_) => return None,
        None => BTreeMap::new(),
    };
    discovery.insert(
        name.to_owned(),
        V::Array(paths.iter().map(|p| V::String(p.clone())).collect()),
    );
    document.insert("discovery".to_owned(), V::Object(discovery));
    let mut next = input.clone();
    next.project = Some(CapturedCarrierV1 {
        path,
        bytes: canonical_bytes(&V::Object(document)).ok()?,
    });
    Some(next)
}

/// The resolved `discovery.<name>` leaf, if a layer won it.
fn has_leaf(resolved: &ResolvedConfigurationV1, name: &str) -> bool {
    resolved
        .provenance
        .contains_key(&format!("discovery.{name}"))
}

/// The resolved `discovery.<name>` value as strings.
fn resolved_paths(resolved: &ResolvedConfigurationV1, name: &str) -> Vec<String> {
    texts(field(field(&resolved.semantic, "discovery"), name))
        .into_iter()
        .map(str::to_owned)
        .collect()
}

/// `paths` resolved through the project carrier: the resolved configuration
/// and its order when the actual resolver admits them and gives back exactly
/// these paths (it normalizes the order; nothing added, dropped or changed).
fn round_trip(
    input: &ResolverInputV1,
    name: &str,
    paths: &[String],
) -> Option<(ResolvedConfigurationV1, Vec<String>)> {
    let resolved = resolve(&apply_setting(input, name, paths)?).ok()?;
    let back = resolved_paths(&resolved, name);
    let mut a = back.clone();
    let mut b = paths.to_vec();
    a.sort();
    b.sort();
    if a != b || back.len() != paths.len() {
        return None;
    }
    if back == paths {
        return Some((resolved, back));
    }
    // The proposal is presented in the resolver's order, so its effect is the
    // resolution of exactly that presentation (the carrier bytes differ).
    let presented = resolve(&apply_setting(input, name, &back)?).ok()?;
    (resolved_paths(&presented, name) == back).then_some((presented, back))
}

/// A proposal's paths in the resolver's order.
fn in_order(mut paths: Vec<ProposedPath>, order: &[String]) -> Vec<ProposedPath> {
    paths.sort_by_key(|p| order.iter().position(|o| *o == p.path));
    paths
}

/// Item 18's recommendation evidence over the units' recognitions and the
/// resolver input. A refusal of the input as it stands is the resolver's.
pub(crate) fn recommendation_evidence(
    units: &[RecognizedUnit<'_>],
    input: &ResolverInputV1,
) -> Result<RecommendationEvidenceV1, ConfigurationRefusal> {
    let base = resolve(input)?;
    let mut detected = Vec::new();
    let mut unresolved = Vec::new();
    let mut observed_hints = Vec::new();
    // Candidate project paths, in unit then result then path order, each with
    // every result it came from.
    let mut entries: Vec<ProposedPath> = Vec::new();
    let mut ignores: Vec<ProposedPath> = Vec::new();
    let mut all_states_complete = true;
    let add = |list: &mut Vec<ProposedPath>, path: String, source: &Source| match list
        .iter_mut()
        .find(|p| p.path == path)
    {
        Some(existing) => existing.sources.push(source.clone()),
        None => list.push(ProposedPath {
            path,
            sources: vec![source.clone()],
        }),
    };
    for unit in units {
        let mut provenance = Vec::new();
        let state = text(field(field(unit.recognition, "entryPoints"), "state"));
        if state != "all" {
            all_states_complete = false;
        }
        for hint in items(field(unit.recognition, "observedHints")) {
            observed_hints.push((
                unit.unit_ordinal,
                text(field(hint, "dependencyName")).to_owned(),
            ));
        }
        for result in items(field(unit.recognition, "recognized")) {
            let source = Source {
                unit_ordinal: unit.unit_ordinal,
                root_path: unit.root_path.to_owned(),
                recognizer_id: text(field(result, "recognizerId")).to_owned(),
            };
            let version = match field(result, "recognizerVersion") {
                V::Integer(n) => n.get(),
                _ => RECOGNIZER_VERSION,
            };
            provenance.push((
                source.recognizer_id.clone(),
                discovered_provenance(&source.recognizer_id, version),
            ));
            for choice in texts(field(result, "unresolvedChoices")) {
                unresolved.push(UnresolvedChoice {
                    source: Some(source.clone()),
                    choice: choice.to_owned(),
                });
            }
            let effects = field(result, "effects");
            for path in texts(field(effects, ENTRY_POINTS)) {
                add(&mut entries, project_path(unit.root_path, path), &source);
            }
            for convention in texts(field(effects, "ignoreConventions")) {
                // A directory convention (`d/`) names the directory `d`.
                let directory = convention.strip_suffix('/').unwrap_or(convention);
                add(
                    &mut ignores,
                    project_path(unit.root_path, directory),
                    &source,
                );
            }
        }
        detected.push(DetectedUnit {
            unit_ordinal: unit.unit_ordinal,
            root_path: unit.root_path.to_owned(),
            recognition: unit.recognition.clone(),
            provenance,
        });
    }
    let mut proposed = Vec::new();
    let mut defaults = Vec::new();
    // Entry points: only when no layer set them (explicit, `[]` included,
    // wins) and every unit's recognition is complete.
    if has_leaf(&base, ENTRY_POINTS) {
        defaults.push(DefaultRationale {
            field: "discovery.entryPoints",
            reason: "explicit-configuration",
        });
    } else if !all_states_complete {
        defaults.push(DefaultRationale {
            field: "discovery.entryPoints",
            reason: "recognition-incomplete",
        });
    } else if entries.is_empty() {
        defaults.push(DefaultRationale {
            field: "discovery.entryPoints",
            reason: "nothing-recognized",
        });
    } else {
        let paths: Vec<String> = entries.iter().map(|p| p.path.clone()).collect();
        match round_trip(input, ENTRY_POINTS, &paths) {
            Some((resolved_with, order)) => proposed.push(ProposedSetting {
                field: "discovery.entryPoints",
                paths: in_order(entries, &order),
                resolved_with,
            }),
            None => unresolved.push(UnresolvedChoice {
                source: None,
                choice: "resolver-refused:discovery.entryPoints".to_owned(),
            }),
        }
    }
    // Ignore paths: only when no layer set them; each path checked alone, so
    // one the resolver refuses is recorded and the rest still proposed.
    if has_leaf(&base, IGNORE_PATHS) {
        defaults.push(DefaultRationale {
            field: "discovery.ignorePaths",
            reason: "explicit-configuration",
        });
    } else {
        let mut kept = Vec::new();
        for candidate in ignores {
            if round_trip(input, IGNORE_PATHS, std::slice::from_ref(&candidate.path)).is_some() {
                kept.push(candidate);
            } else {
                unresolved.push(UnresolvedChoice {
                    source: candidate.sources.first().cloned(),
                    choice: format!("resolver-refused:discovery.ignorePaths:{}", candidate.path),
                });
            }
        }
        let paths: Vec<String> = kept.iter().map(|p| p.path.clone()).collect();
        if kept.is_empty() {
            defaults.push(DefaultRationale {
                field: "discovery.ignorePaths",
                reason: "nothing-recognized",
            });
        } else if let Some((resolved_with, order)) = round_trip(input, IGNORE_PATHS, &paths) {
            proposed.push(ProposedSetting {
                field: "discovery.ignorePaths",
                paths: in_order(kept, &order),
                resolved_with,
            });
        } else {
            unresolved.push(UnresolvedChoice {
                source: None,
                choice: "resolver-refused:discovery.ignorePaths".to_owned(),
            });
        }
    }
    // Workspace roots are D15's configured member repositories, never
    // package-workspace membership: nothing is proposed for them.
    defaults.push(DefaultRationale {
        field: "discovery.workspaceRoots",
        reason: "not-recognition-evidence",
    });
    Ok(RecommendationEvidenceV1 {
        detected,
        proposed,
        defaults,
        unresolved,
        observed_hints,
        base,
    })
}
