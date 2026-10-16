// M3-B r9 item 16 (unit B2-d2, B2-d plan r3 sections 3 and 4): host-side
// framework recognition, NE section 8. Pure: it reads the bytes and member
// paths its caller supplies and evaluates nothing (FW-01). It runs the nine
// recognizers over one `rust` or `tsjs` unit and gives its
// `FrameworkRecognitionV1`, with FR-1 to FR-5, and the `UnitRecognitionV1`
// row C4 commits in `FrameworkRecognitionPlanV1`.
//
// The oracle is the bound B2-d0 reference (contract successor 171): the
// selected native model's `recognize_frameworks` with the plan's five
// changes. Manifests are read as data by the exact readers: `package.json`
// by exact JSON admission, `tsconfig.json`/`jsconfig.json` by item 14a's
// JSONC reader within its 64 KiB bound, `Cargo.toml` by the pinned `toml`
// on `parse_toml`'s profile, and `pnpm-workspace.yaml` by the closed YAML
// subset (B2-d1). A configuration that needs evaluation (`next.config.*`,
// `vite.config.*`, the jest and vitest configs) is hashed, never parsed.
// Paths are unit-root-relative (B2-d plan r3 Q2; FR-6 to FR-8 are not
// applied). Recognition binds through `FrameworkRecognitionPlanV1`, not the
// resolver: the resolver's discovery fold stays empty (law item 1).
use crate::{jsonc, typescript_config, yaml_subset};
use opensip_contracts::generated::identity::RecognitionPlan1UnitRecognitionV1;
use opensip_identity::{
    JsonInteger, JsonValue as V, canonical_bytes, digest_hex, hash_canonical_value, parse_json,
    parse_toml, raw_sha256,
};
use std::collections::{BTreeMap, BTreeSet};

pub(crate) const DOMAIN: &str = "native.framework-recognition.v1";
pub(crate) const RECOGNIZER_VERSION: i128 = 1;
/// FR-4.
pub(crate) const MAX_RECOGNIZERS: usize = 32;
pub(crate) const MAX_EVIDENCE: usize = 64;
pub(crate) const MAX_ENTRY_POINTS: usize = 65536;
pub(crate) const CONFIG_REQUIRES_EVALUATION: &str = "config-requires-evaluation";
pub(crate) const ENTRY_POINTS_OVER_BOUND: &str = "entry-points-over-bound";

/// Every file a recognizer reads or hashes when present: the caller
/// supplies the bytes of each one among the unit's member paths.
pub(crate) const EVIDENCE_FILES: [&str; 15] = [
    "Cargo.toml",
    "jest.config.js",
    "jest.config.ts",
    "jsconfig.json",
    "next.config.js",
    "next.config.mjs",
    "next.config.ts",
    "package.json",
    "pnpm-workspace.yaml",
    "tsconfig.json",
    "vite.config.js",
    "vite.config.mjs",
    "vite.config.ts",
    "vitest.config.js",
    "vitest.config.ts",
];
/// The model's FR-3 hint names (`FRAMEWORK_HINTS`).
const FRAMEWORK_HINTS: [&str; 11] = [
    "angular",
    "@angular/core",
    "svelte",
    "nuxt",
    "@remix-run/react",
    "astro",
    "solid-js",
    "vue",
    "ember-source",
    "gatsby",
    "@nestjs/core",
];
const TEST_GLOBS: [&str; 3] = ["**/*.test.*", "**/*.spec.*", "**/__tests__/**"];
const JEST_VITEST_CONFIGS: [&str; 4] = [
    "jest.config.ts",
    "jest.config.js",
    "vitest.config.ts",
    "vitest.config.js",
];
const NEXT_CONFIGS: [&str; 3] = ["next.config.js", "next.config.mjs", "next.config.ts"];
const VITE_CONFIGS: [&str; 3] = ["vite.config.ts", "vite.config.js", "vite.config.mjs"];
const APP_ROUTES: [&str; 6] = [
    "page.tsx", "page.jsx", "page.ts", "page.js", "route.ts", "route.js",
];
const PAGE_ROUTES: [&str; 4] = [".tsx", ".jsx", ".ts", ".js"];

/// One unit's recognition inputs.
pub(crate) struct RecognitionInputs<'a> {
    /// Every member path of the unit, unit-root-relative.
    pub(crate) paths: &'a BTreeSet<String>,
    /// The bytes of each `EVIDENCE_FILES` entry among `paths`.
    pub(crate) bytes: &'a BTreeMap<String, Vec<u8>>,
    /// The resolved `discovery.entryPoints`: `None` when the resolved
    /// configuration has no such field (no winning leaf), else the list a
    /// carrier won, possibly empty (explicit).
    pub(crate) explicit_entry_points: Option<&'a [String]>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) enum RecognitionError {
    /// A present evidence file whose bytes the caller did not supply.
    MissingEvidenceBytes(String),
    /// FR-4's structural bounds (unreachable with the nine recognizers).
    Bound(&'static str),
    /// The row does not admit as `UnitRecognitionV1`.
    Shape,
}

/// One recognized result before rendering.
pub(crate) struct Recognized {
    pub(crate) id: &'static str,
    pub(crate) evidence: Vec<(String, String, &'static str)>,
    pub(crate) assurance: &'static str,
    pub(crate) entry: Vec<String>,
    pub(crate) tests: Vec<&'static str>,
    pub(crate) ignore: Vec<&'static str>,
    pub(crate) unresolved: Vec<&'static str>,
}

/// FR-4's structural bounds over any list of results: at most 32 results,
/// each citing 1 to 64 evidence files.
pub(crate) fn structural_bounds(out: &[Recognized]) -> Result<(), RecognitionError> {
    if out.len() > MAX_RECOGNIZERS {
        return Err(RecognitionError::Bound("maxRecognizersPerUnit"));
    }
    if out
        .iter()
        .any(|r| r.evidence.is_empty() || r.evidence.len() > MAX_EVIDENCE)
    {
        return Err(RecognitionError::Bound("maxEvidenceFilesPerRecognizer"));
    }
    Ok(())
}

/// FR-4's per-unit entry bound, all or nothing over the distinct union of
/// every result's entry points: one past it, no result keeps its entries and
/// each entry-bearing result discloses `entry-points-over-bound`.
pub(crate) fn entry_bound(out: &mut [Recognized]) {
    let union: BTreeSet<&String> = out.iter().flat_map(|r| r.entry.iter()).collect();
    if union.len() > MAX_ENTRY_POINTS {
        for r in out.iter_mut().filter(|r| !r.entry.is_empty()) {
            r.entry.clear();
            r.unresolved.push(ENTRY_POINTS_OVER_BOUND);
        }
    }
}

/// FR-2's provenance for a recognized result's effects.
pub(crate) fn discovered_provenance(recognizer_id: &str, version: i128) -> String {
    format!("DISCOVERED:{recognizer_id}@{version}")
}

/// `MarkerFact.is_cargo_workspace`: true or false on a parsed `Cargo.toml`,
/// `None` (unknown, read by B2-c's instrument as not a workspace) on any
/// parse error. The same parse decides `cargo-workspace`.
pub(crate) fn cargo_workspace_fact(raw: &[u8]) -> Option<bool> {
    let doc = parse_toml(raw).ok()?;
    Some(
        doc.table()
            .get("workspace")
            .and_then(|v| v.as_table())
            .is_some(),
    )
}

/// One unit's `FrameworkRecognitionV1`, as a canonical JSON value.
pub(crate) fn recognize(inputs: &RecognitionInputs<'_>) -> Result<V, RecognitionError> {
    let has = |p: &str| inputs.paths.contains(p);
    let bytes_of = |p: &str| -> Result<&[u8], RecognitionError> {
        inputs
            .bytes
            .get(p)
            .map(Vec::as_slice)
            .ok_or_else(|| RecognitionError::MissingEvidenceBytes(p.to_owned()))
    };
    let ev = |p: &str,
              field: &'static str|
     -> Result<(String, String, &'static str), RecognitionError> {
        Ok((p.to_owned(), digest_hex(&raw_sha256(bytes_of(p)?)), field))
    };
    let result = |id, evidence, assurance| Recognized {
        id,
        evidence,
        assurance,
        entry: Vec::new(),
        tests: Vec::new(),
        ignore: Vec::new(),
        unresolved: Vec::new(),
    };
    let mut out: Vec<Recognized> = Vec::new();
    let mut hints: BTreeSet<String> = BTreeSet::new();
    if has("package.json") {
        match parse_json(bytes_of("package.json")?) {
            Ok(V::Object(pkg)) => {
                let mut node = result(
                    "node-package",
                    vec![ev("package.json", "type/private/exports/main")?],
                    "declared",
                );
                node.ignore.push("node_modules/");
                out.push(node);
                if matches!(pkg.get("workspaces"), Some(V::Array(_) | V::Object(_))) {
                    out.push(result(
                        "npm-workspaces",
                        vec![ev("package.json", "workspaces")?],
                        "declared",
                    ));
                }
                let config = JEST_VITEST_CONFIGS.iter().copied().find(|p| has(p));
                if pkg.contains_key("jest") || config.is_some() {
                    let path = config.unwrap_or("package.json");
                    let mut tests =
                        result("vitest-jest", vec![ev(path, "jest|vitest")?], "declared");
                    tests.tests.extend(TEST_GLOBS);
                    if config.is_some() {
                        tests.unresolved.push(CONFIG_REQUIRES_EVALUATION);
                    }
                    out.push(tests);
                }
                for key in ["dependencies", "devDependencies", "peerDependencies"] {
                    if let Some(V::Object(deps)) = pkg.get(key) {
                        hints.extend(
                            deps.keys()
                                .filter(|n| FRAMEWORK_HINTS.contains(&n.as_str()))
                                .cloned(),
                        );
                    }
                }
            }
            // Admitted JSON that is not an object: the model recognizes
            // nothing from it.
            Ok(_) => {}
            Err(_) => {
                let mut node = result(
                    "node-package",
                    vec![ev("package.json", "<unparseable>")?],
                    "inferred",
                );
                node.ignore.push("node_modules/");
                node.unresolved.push("package.json-not-strict-json");
                out.push(node);
            }
        }
    }
    if let Some(config) = ["tsconfig.json", "jsconfig.json"]
        .into_iter()
        .find(|p| has(p))
    {
        let raw = bytes_of(config)?;
        let mut ts = result(
            "typescript-config",
            vec![ev(config, "compilerOptions/extends/references")?],
            "declared",
        );
        if raw.len() > typescript_config::MAX_CONFIG_FILE_BYTES || jsonc::parse(raw).is_err() {
            ts.assurance = "inferred";
            ts.unresolved.push("tsconfig-not-jsonc");
        }
        out.push(ts);
    }
    if has("pnpm-workspace.yaml") {
        let mut pnpm = result(
            "pnpm-workspace",
            vec![ev("pnpm-workspace.yaml", "packages")?],
            "declared",
        );
        if yaml_subset::parse_pnpm_packages(bytes_of("pnpm-workspace.yaml")?).is_err() {
            pnpm.unresolved.push(CONFIG_REQUIRES_EVALUATION);
        }
        out.push(pnpm);
    }
    if has("Cargo.toml") {
        match parse_toml(bytes_of("Cargo.toml")?) {
            Err(_) => {
                let mut cargo = result(
                    "cargo-package",
                    vec![ev("Cargo.toml", "<unparseable>")?],
                    "inferred",
                );
                cargo.ignore.push("target/");
                cargo.unresolved.push("Cargo.toml-not-toml");
                out.push(cargo);
            }
            Ok(doc) => {
                let table = doc.table();
                if table.get("workspace").and_then(|v| v.as_table()).is_some() {
                    let mut ws = result(
                        "cargo-workspace",
                        vec![ev("Cargo.toml", "workspace.members")?],
                        "declared",
                    );
                    ws.ignore.push("target/");
                    out.push(ws);
                }
                if table.get("package").and_then(|v| v.as_table()).is_some() {
                    let mut pkg = result(
                        "cargo-package",
                        vec![ev("Cargo.toml", "package/lib/bin")?],
                        "declared",
                    );
                    pkg.entry.extend(
                        ["src/main.rs", "src/lib.rs"]
                            .into_iter()
                            .filter(|p| has(p))
                            .map(str::to_owned),
                    );
                    pkg.ignore.push("target/");
                    out.push(pkg);
                }
            }
        }
    }
    if let Some(config) = NEXT_CONFIGS.into_iter().find(|p| has(p)) {
        let mut next = result("nextjs", vec![ev(config, "presence")?], "inferred");
        next.entry.extend(
            inputs
                .paths
                .iter()
                .filter(|p| {
                    (p.starts_with("app/") && APP_ROUTES.iter().any(|s| p.ends_with(s)))
                        || (p.starts_with("pages/") && PAGE_ROUTES.iter().any(|s| p.ends_with(s)))
                })
                .cloned(),
        );
        next.ignore.push(".next/");
        next.unresolved.push(CONFIG_REQUIRES_EVALUATION);
        out.push(next);
    }
    if let Some(config) = VITE_CONFIGS.into_iter().find(|p| has(p)) {
        let mut vite = result("vite", vec![ev(config, "presence")?], "inferred");
        if has("index.html") {
            vite.entry.push("index.html".to_owned());
        }
        vite.ignore.push("dist/");
        vite.unresolved.push(CONFIG_REQUIRES_EVALUATION);
        out.push(vite);
    }
    out.sort_by(|a, b| a.id.cmp(b.id));
    // FR-4: the structural bounds, then the per-unit entry bound, an
    // explicit override included (the retained results stay schema-valid).
    structural_bounds(&out)?;
    entry_bound(&mut out);
    // FR-2 and FR-1: the explicit override, then the state rule.
    let (state, source) = if inputs.explicit_entry_points.is_some() {
        ("all", "explicit")
    } else if out.iter().any(|r| !r.unresolved.is_empty()) {
        ("partial", "recognized")
    } else if out.iter().any(|r| !r.entry.is_empty()) {
        ("all", "recognized")
    } else {
        ("none", "none")
    };
    Ok(render(&out, &hints, state, source))
}

fn text(s: &str) -> V {
    V::String(s.to_owned())
}
fn texts<S: AsRef<str>>(items: &[S]) -> V {
    V::Array(items.iter().map(|s| text(s.as_ref())).collect())
}
fn object<const N: usize>(fields: [(&str, V); N]) -> V {
    V::Object(fields.into_iter().map(|(k, v)| (k.to_owned(), v)).collect())
}
fn integer(n: i128) -> V {
    V::Integer(JsonInteger::new(n).expect("a small integer"))
}

fn render(out: &[Recognized], hints: &BTreeSet<String>, state: &str, source: &str) -> V {
    let recognized = out
        .iter()
        .map(|r| {
            object([
                ("recognizerId", text(r.id)),
                ("recognizerVersion", integer(RECOGNIZER_VERSION)),
                (
                    "evidence",
                    V::Array(
                        r.evidence
                            .iter()
                            .map(|(path, sha, field)| {
                                object([
                                    ("path", text(path)),
                                    ("contentSha256", text(sha)),
                                    ("field", text(field)),
                                ])
                            })
                            .collect(),
                    ),
                ),
                ("assurance", text(r.assurance)),
                (
                    "effects",
                    object([
                        ("entryPoints", texts(&r.entry)),
                        ("testGlobs", texts(&r.tests)),
                        ("ignoreConventions", texts(&r.ignore)),
                    ]),
                ),
                ("unresolvedChoices", texts(&r.unresolved)),
            ])
        })
        .collect();
    object([
        ("schemaVersion", integer(1)),
        ("recognized", V::Array(recognized)),
        (
            "observedHints",
            V::Array(
                hints
                    .iter()
                    .map(|n| object([("dependencyName", text(n))]))
                    .collect(),
            ),
        ),
        (
            "entryPoints",
            object([("state", text(state)), ("source", text(source))]),
        ),
    ])
}

/// The `UnitRecognitionV1` row: its `recognitionId` the derived identity
/// `closure.rs` checks, the whole row admitted by the generated type.
pub(crate) fn unit_recognition(
    unit_ordinal: u64,
    root_path: &str,
    marker_path: &str,
    recognition: V,
) -> Result<RecognitionPlan1UnitRecognitionV1, RecognitionError> {
    let id = hash_canonical_value(DOMAIN, &recognition).map_err(|_| RecognitionError::Shape)?;
    let row = object([
        ("unitOrdinal", integer(unit_ordinal as i128)),
        ("rootPath", text(root_path)),
        ("markerPath", text(marker_path)),
        (
            "recognitionId",
            text(&format!("sha256:{}", digest_hex(&id))),
        ),
        ("recognition", recognition),
    ]);
    let raw = canonical_bytes(&row).map_err(|_| RecognitionError::Shape)?;
    serde_json::from_slice(&raw).map_err(|_| RecognitionError::Shape)
}
