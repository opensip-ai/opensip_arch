// Law X11 r1 items 2 and 6 (unit X11a), the binary and source layer. No
// creator command is live in M2: the real built `opensip` refuses the
// default analysis, `analyze`, `fit` and `audit` in its parser, before any
// attempt, account observation, core, platform, intent, disclosure, gate,
// pack admission or file access. These tests run the binary with no override
// of any kind and pin, for every input row of item 2 in both formats, the
// exact refusal bytes (apart from the fresh request id), the envelope's
// schema validity and an empty standard error. Every run is checked for zero
// effects on the account's real installation and on its scratch working
// directory. The catalogue keeps its four rows, and the source pins keep the
// creator, the gate, the ordinary writer, pack admission and the commit path
// out of the binary and the host ingress.
use serde_json::Value;
use std::collections::{BTreeMap, BTreeSet};
use std::os::unix::fs::MetadataExt;
use std::path::{Path, PathBuf};
use std::process::{Command, Output};
use std::sync::atomic::{AtomicU64, Ordering};

const ENVELOPE: &str = "urn:opensip:product-v1:workflows:evaluator3:command-envelope:7";
const DEFAULT: &str =
    "Default analysis is not implemented in this development build. Use opensip help.";
const UNKNOWN_COMMAND: &str = "Unknown command or arguments. Use opensip help.";
const UNKNOWN_OPTION: &str = "Unknown command option. Use opensip help.";
const NOT_APPLICABLE: &str = "The selected format is not applicable to this command.";
const HELP_TOPIC: &str = "Unknown or unimplemented help topic.";
const FORMAT_TWICE: &str = "Output format was specified more than once.";
const CORRELATION: &str = "x11a-client";
// The default analysis (no command word) and the three analysis words.
const COMMANDS: [&[&str]; 4] = [&[], &["analyze"], &["fit"], &["audit"]];
// Item 2's creator flags.
const CREATOR_FLAGS: [&str; 10] = [
    "--allow-backup-custody",
    "--ephemeral",
    "--project",
    "--workspace-root",
    "--trust-group",
    "--trust-project-owner",
    "--baseline",
    "--audit-profile",
    "--closure-bundle",
    "--accept-origin",
];

static NEXT: AtomicU64 = AtomicU64::new(0);

/// The account's real installation, read by the test process only; the
/// binary reads no HOME.
fn real_installation() -> PathBuf {
    let home = std::env::var_os("HOME").expect("HOME for the test process");
    Path::new(&home).join("Library/Application Support/OpenSIP")
}
/// Existence and, when present, (device, inode, mode, modification time).
fn real_state() -> Option<(u64, u64, u32, i64, i64)> {
    std::fs::symlink_metadata(real_installation())
        .ok()
        .map(|m| (m.dev(), m.ino(), m.mode(), m.mtime(), m.mtime_nsec()))
}

/// Every entry under a directory, with each file's bytes.
fn tree(root: &Path) -> BTreeMap<PathBuf, Option<Vec<u8>>> {
    let mut out = BTreeMap::new();
    let mut pending = vec![root.to_path_buf()];
    while let Some(dir) = pending.pop() {
        for entry in std::fs::read_dir(&dir).unwrap() {
            let path = entry.unwrap().path();
            let relative = path.strip_prefix(root).unwrap().to_path_buf();
            if std::fs::symlink_metadata(&path).unwrap().is_dir() {
                pending.push(path);
                out.insert(relative, None);
            } else {
                out.insert(relative, Some(std::fs::read(&path).unwrap()));
            }
        }
    }
    out
}

/// One test's runs: a scratch working directory whose configuration and
/// package data are deliberately invalid, the real installation's state when
/// the test began, and every request id seen.
struct Runs {
    cwd: PathBuf,
    scratch: BTreeMap<PathBuf, Option<Vec<u8>>>,
    real: Option<(u64, u64, u32, i64, i64)>,
    ids: BTreeSet<String>,
}
impl Runs {
    fn new() -> Self {
        let cwd = std::env::temp_dir().join(format!(
            "opensip-x11a-{}-{}",
            std::process::id(),
            NEXT.fetch_add(1, Ordering::Relaxed)
        ));
        std::fs::create_dir(&cwd).unwrap();
        std::fs::create_dir(cwd.join(".opensip")).unwrap();
        std::fs::write(cwd.join(".opensip/config.json"), "not valid configuration").unwrap();
        std::fs::write(cwd.join("package.json"), "not valid package data").unwrap();
        let scratch = tree(&cwd);
        Self {
            cwd,
            scratch,
            real: real_state(),
            ids: BTreeSet::new(),
        }
    }
    /// The real built binary with no override: the inherited environment,
    /// only the working directory chosen. Zero effects after every run.
    fn run(&mut self, args: &[String]) -> Output {
        let out = Command::new(env!("CARGO_BIN_EXE_opensip"))
            .args(args)
            .current_dir(&self.cwd)
            .output()
            .unwrap();
        assert_eq!(real_state(), self.real, "{args:?} touched the installation");
        assert_eq!(tree(&self.cwd), self.scratch, "{args:?} touched the cwd");
        out
    }
    /// A fresh, well-formed request id, never seen before in this test.
    fn fresh(&mut self, id: &str) -> String {
        assert_eq!(id.len(), 37, "{id}");
        assert!(id.starts_with("req1_"), "{id}");
        assert!(
            id[5..]
                .bytes()
                .all(|x| x.is_ascii_digit() || (b'a'..=b'f').contains(&x)),
            "{id}"
        );
        assert!(self.ids.insert(id.to_owned()), "reused {id}");
        id.to_owned()
    }
    /// Assert item 2's refusal, exactly, for one input.
    fn refused(&mut self, args: &[String], expect: Expect, diagnostic: &str, not_applicable: bool) {
        let out = self.run(args);
        assert_eq!(out.status.code(), Some(2), "{args:?}");
        assert!(out.stderr.is_empty(), "{args:?}");
        let text = String::from_utf8(out.stdout).unwrap();
        match expect {
            Expect::Json(correlation) => {
                assert!(schema_valid(text.as_bytes()), "{args:?}");
                let value: Value = serde_json::from_str(&text).unwrap();
                let id = self.fresh(value["requestId"].as_str().unwrap());
                assert_eq!(value["kind"], "failure");
                assert_eq!(
                    value["termination"],
                    serde_json::json!({"class": "request-rejected", "errorCode": "REQUEST.UNKNOWN_OPTION"})
                );
                assert_eq!(value["diagnostics"], serde_json::json!([diagnostic]));
                assert_eq!(
                    text,
                    json_bytes(&id, diagnostic, not_applicable, correlation),
                    "{args:?}"
                );
            }
            Expect::Human => {
                let line = text.lines().find(|l| l.starts_with("Request: ")).unwrap();
                let id = self.fresh(&line["Request: ".len()..]);
                assert_eq!(
                    text,
                    human_bytes(&id, diagnostic, not_applicable),
                    "{args:?}"
                );
            }
        }
    }
}
impl Drop for Runs {
    fn drop(&mut self) {
        let _ = std::fs::remove_dir_all(&self.cwd);
    }
}

#[derive(Clone, Copy)]
enum Expect {
    Human,
    Json(Option<&'static str>),
}

fn schema_valid(raw: &[u8]) -> bool {
    opensip_host::embedded_schema_registry()
        .unwrap()
        .schema(ENVELOPE, "")
        .unwrap()
        .admit_json(raw, 64 * 1024 * 1024)
        .is_ok()
}
/// Command-envelope v7's empty-errors diagnostic branch, byte for byte; the
/// format-not-applicable row carries its one registered error.
fn json_bytes(
    id: &str,
    diagnostic: &str,
    not_applicable: bool,
    correlation: Option<&str>,
) -> String {
    let correlation = correlation
        .map(|c| format!("\"clientCorrelationId\":\"{c}\","))
        .unwrap_or_default();
    let errors = if not_applicable {
        r#"[{"code":"OUTPUT.FORMAT_NOT_APPLICABLE","remedy":"Choose an applicable output format."}]"#
    } else {
        "[]"
    };
    format!(
        "{{{correlation}\"diagnostics\":[\"{diagnostic}\"],\"errors\":{errors},\"exitCode\":2,\
         \"kind\":\"failure\",\"requestId\":\"{id}\",\"schemaFamily\":\"opensip.product.envelope\",\
         \"schemaMajor\":7,\"termination\":{{\"class\":\"request-rejected\",\
         \"errorCode\":\"REQUEST.UNKNOWN_OPTION\"}}}}\n"
    )
}
/// The failure renderer's lines; the correlation id is never rendered.
fn human_bytes(id: &str, diagnostic: &str, not_applicable: bool) -> String {
    let detail = if not_applicable {
        "Detail: OUTPUT.FORMAT_NOT_APPLICABLE\nRemedy: Choose an applicable output format.\n"
    } else {
        ""
    };
    format!(
        "Termination: request-rejected\nError: REQUEST.UNKNOWN_OPTION\n{detail}Request: {id}\n{diagnostic}\n"
    )
}

fn strings(parts: &[&[&str]]) -> Vec<String> {
    parts
        .iter()
        .flat_map(|p| p.iter().map(|s| (*s).to_owned()))
        .collect()
}
/// One input in several orders of `--format human|json` and
/// `--client-correlation-id`, with the format placed before, between and
/// after the words.
fn placements(words: &[&str]) -> Vec<(Vec<String>, Expect)> {
    let c = CORRELATION;
    let eq = format!("--client-correlation-id={c}");
    let (head, tail) = words.split_at(words.len().min(1));
    vec![
        (strings(&[words]), Expect::Human),
        (strings(&[&["--format", "human"], words]), Expect::Human),
        (
            strings(&[&["--client-correlation-id", c], words, &["--format=human"]]),
            Expect::Human,
        ),
        (strings(&[words, &["--format=json"]]), Expect::Json(None)),
        (strings(&[&["--format", "json"], words]), Expect::Json(None)),
        (
            strings(&[head, &["--format=json"], tail]),
            Expect::Json(None),
        ),
        (
            strings(&[words, &[eq.as_str(), "--format", "json"]]),
            Expect::Json(Some(c)),
        ),
        (
            strings(&[&["--format=json"], words, &["--client-correlation-id", c]]),
            Expect::Json(Some(c)),
        ),
    ]
}

#[test]
fn the_default_analysis_keeps_its_refusal_in_both_formats() {
    let mut runs = Runs::new();
    for (args, expect) in placements(&[]) {
        runs.refused(&args, expect, DEFAULT, false);
    }
    assert_eq!(runs.ids.len(), 8);
}

#[test]
fn analyze_fit_and_audit_keep_their_refusal_with_or_without_further_words() {
    let mut runs = Runs::new();
    for word in ["analyze", "fit", "audit"] {
        for words in [
            vec![word],
            vec![word, "src"],
            vec![word, "src", "default"],
            vec!["src", word],
        ] {
            for (args, expect) in placements(&words) {
                runs.refused(&args, expect, UNKNOWN_COMMAND, false);
            }
        }
    }
    assert_eq!(runs.ids.len(), 3 * 4 * 8);
}

#[test]
fn every_creator_flag_is_an_unknown_option_on_every_creator_command() {
    let mut runs = Runs::new();
    for command in COMMANDS {
        for flag in CREATOR_FLAGS {
            for (args, expect) in placements(
                &strings(&[command, &[flag]])
                    .iter()
                    .map(String::as_str)
                    .collect::<Vec<_>>(),
            ) {
                runs.refused(&args, expect, UNKNOWN_OPTION, false);
            }
            // The flag before the command word, and with a value.
            let valued = format!("{flag}=x11a");
            for words in [
                strings(&[&[flag], command]),
                strings(&[command, &[valued.as_str()]]),
                strings(&[command, &[flag, "x11a"]]),
            ] {
                let mut json = words.clone();
                json.push("--format=json".to_owned());
                runs.refused(&words, Expect::Human, UNKNOWN_OPTION, false);
                runs.refused(&json, Expect::Json(None), UNKNOWN_OPTION, false);
            }
        }
    }
    assert_eq!(runs.ids.len(), 4 * 10 * (8 + 6));
}

#[test]
fn agent_html_and_sarif_are_not_applicable_to_every_creator_command() {
    let mut runs = Runs::new();
    for command in COMMANDS {
        for format in ["agent", "html", "sarif"] {
            let eq = format!("--format={format}");
            // A single inapplicable format leaves the output human.
            for args in [
                strings(&[command, &["--format", format]]),
                strings(&[&[eq.as_str()], command]),
                strings(&[
                    &["--client-correlation-id", CORRELATION],
                    command,
                    &[eq.as_str()],
                ]),
            ] {
                runs.refused(&args, Expect::Human, NOT_APPLICABLE, true);
            }
            // The JSON branch is reached only with JSON selected first; the
            // inapplicable format then ends the parse.
            runs.refused(
                &strings(&[&["--format=json"], command, &[eq.as_str()]]),
                Expect::Json(None),
                NOT_APPLICABLE,
                true,
            );
            runs.refused(
                &strings(&[
                    &["--format", "json", "--client-correlation-id", CORRELATION],
                    command,
                    &["--format", format],
                ]),
                Expect::Json(Some(CORRELATION)),
                NOT_APPLICABLE,
                true,
            );
            // Competing parser failures: the bytes the existing parser emits.
            runs.refused(
                &strings(&[command, &[eq.as_str(), "--format=json"]]),
                Expect::Json(None),
                FORMAT_TWICE,
                false,
            );
            runs.refused(
                &strings(&[command, &["--ephemeral", eq.as_str()]]),
                Expect::Human,
                NOT_APPLICABLE,
                true,
            );
            runs.refused(
                &strings(&[command, &[eq.as_str(), "--ephemeral"]]),
                Expect::Human,
                UNKNOWN_OPTION,
                false,
            );
            runs.refused(
                &strings(&[&["--format=json"], command, &["--baseline", eq.as_str()]]),
                Expect::Json(None),
                NOT_APPLICABLE,
                true,
            );
            runs.refused(
                &strings(&[&["--format=json"], command, &[eq.as_str(), "--baseline"]]),
                Expect::Json(None),
                UNKNOWN_OPTION,
                false,
            );
        }
    }
    assert_eq!(runs.ids.len(), 4 * 3 * 10);
}

#[test]
fn help_for_the_analysis_commands_is_an_unknown_topic() {
    let mut runs = Runs::new();
    for topic in ["analyze", "fit", "audit", "default"] {
        for (args, expect) in placements(&["help", topic]) {
            runs.refused(&args, expect, HELP_TOPIC, false);
        }
    }
    assert_eq!(runs.ids.len(), 4 * 8);
}

const HELP: &str = "OpenSIP\n\n\
completion\n  opensip completion <bash|zsh|fish>\n  Print shell completion for implemented commands.\n\n\
doctor\n  opensip doctor [--format human|json]\n  Report the health of this account's OpenSIP installation.\n\n\
help\n  opensip help [command] [--format human|json]\n  Show help for implemented commands.\n\n\
version\n  opensip version [--format human|json]\n  Show the compiled host version and component selection.\n\n\
Termination: success\n";

#[test]
fn help_and_completion_keep_the_four_row_catalogue() {
    let mut runs = Runs::new();
    let out = runs.run(&strings(&[&["help"]]));
    assert_eq!(out.status.code(), Some(0));
    assert!(out.stderr.is_empty());
    assert_eq!(String::from_utf8(out.stdout).unwrap(), HELP);

    let out = runs.run(&strings(&[&["help", "--format=json"]]));
    assert_eq!(out.status.code(), Some(0));
    assert!(out.stderr.is_empty());
    assert!(schema_valid(&out.stdout));
    let value: Value = serde_json::from_slice(&out.stdout).unwrap();
    runs.fresh(value["requestId"].as_str().unwrap());
    assert_eq!(value["kind"], "meta");
    assert_eq!(value["meta"]["topic"], Value::Null);
    assert_eq!(
        value["meta"]["commands"],
        serde_json::json!([
            {"name": "completion", "usage": "opensip completion <bash|zsh|fish>",
             "summary": "Print shell completion for implemented commands."},
            {"name": "doctor", "usage": "opensip doctor [--format human|json]",
             "summary": "Report the health of this account's OpenSIP installation."},
            {"name": "help", "usage": "opensip help [command] [--format human|json]",
             "summary": "Show help for implemented commands."},
            {"name": "version", "usage": "opensip version [--format human|json]",
             "summary": "Show the compiled host version and component selection."},
        ])
    );

    for (shell, script) in [
        (
            "bash",
            "complete -W 'completion doctor help version' opensip\n",
        ),
        (
            "zsh",
            "#compdef opensip\n_arguments '1:command:(completion doctor help version)'\n",
        ),
        (
            "fish",
            "complete -c opensip -f -a 'completion doctor help version'\n",
        ),
    ] {
        let out = runs.run(&strings(&[&["completion", shell]]));
        assert_eq!(out.status.code(), Some(0));
        assert!(out.stderr.is_empty());
        assert_eq!(
            String::from_utf8(out.stdout).unwrap(),
            format!("{script}# Termination: success\n")
        );
    }
}

/// Production code: everything before a `#[cfg(test)]` test module, with
/// comment lines removed (`doctor_tests.rs`'s reader).
fn production(path: &Path) -> String {
    let text = std::fs::read_to_string(path).unwrap();
    let text = match text.find("#[cfg(test)]\nmod tests") {
        Some(at) => &text[..at],
        None => &text[..],
    };
    text.lines()
        .filter(|line| !line.trim_start().starts_with("//"))
        .collect::<Vec<_>>()
        .join("\n")
}
fn rust_files(dir: &Path, out: &mut Vec<PathBuf>) {
    for entry in std::fs::read_dir(dir).unwrap() {
        let path = entry.unwrap().path();
        if path.is_dir() {
            rust_files(&path, out);
        } else if path.extension().is_some_and(|x| x == "rs") {
            out.push(path);
        }
    }
}

/// The exception is pinned to the accepted top-level source boundary.
/// Additional name bindings, glob imports or macro expansion cannot silently
/// turn the logging crate reference into an unscanned bridge.
const OPTIONAL_LOGGING: &str = "pub fn finalize_invocation(cancelled: bool) {\n    opensip_operability::finalize(cancelled);\n}";
const HOST_PREFIX: &str = "#![forbid(unsafe_code)]\n\n#[cfg(all(feature = \"crash-matrix\", not(debug_assertions)))]\ncompile_error!(\n    \"the crash-matrix feature is test-only (law X9 r1 item 2) and refuses every build without debug assertions\"\n);\n#[cfg(all(feature = \"crash-matrix\", target_os = \"macos\"))]\n#[doc(hidden)]\npub mod crash_matrix_support;\nmod delivery;\n#[allow(dead_code)]\nmod invocation;\n#[allow(dead_code)]\nmod outcomes;\nmod request;\npub use delivery::deliver_required;\n\n";
const NEXT_EXPORT: &str =
    "\npub use outcomes::{Format, MetadataError, MetadataHost, MetadataRequest, RenderedResponse};";
fn identifier_present(text: &str, name: &str) -> bool {
    text.split(|c: char| !(c.is_alphanumeric() || c == '_'))
        .any(|identifier| identifier == name)
}
fn logging_adapter_is_single_top_level(text: &str) -> bool {
    if text.matches(OPTIONAL_LOGGING).count() != 1 {
        return false;
    }
    let Some(rest) = text
        .strip_prefix(HOST_PREFIX)
        .and_then(|s| s.strip_prefix(OPTIONAL_LOGGING))
    else {
        return false;
    };
    if !rest.starts_with(NEXT_EXPORT)
        || identifier_present(rest, "opensip_operability")
        || rest.contains(['!', '*'])
    {
        return false;
    }
    // The pinned prefix contains the one existing compile_error! and its
    // built-in attributes. Below the adapter only the existing built-in
    // attributes are permitted: no macro_use/cfg_attr/procedural injection.
    let unaccounted = rest
        .lines()
        .map(str::trim)
        .filter(|line| {
            ![
                r#"#[cfg(target_os = "macos")]"#,
                "#[allow(dead_code)]",
                r#"#[cfg(all(test, target_os = "macos"))]"#,
                "#[cfg(test)]",
            ]
            .contains(line)
        })
        .collect::<Vec<_>>()
        .join("\n");
    // Rust permits whitespace/comments between attribute tokens. Removing
    // only exact known lines and rejecting every remaining '#' fails closed
    // for separated, multiline and injected attribute spellings too.
    !unaccounted.contains('#')
        && !["cfg", "allow", "forbid", "doc", "compile_error"]
            .iter()
            .any(|name| identifier_present(&unaccounted, name))
}
fn operability_is_the_resolved_logging_crate(root: &Path) -> bool {
    // Cargo's actual offline locked resolution handles renames and patches;
    // matching a dependency spelling in TOML would not establish resolution.
    let Ok(output) = Command::new(env!("CARGO"))
        .args(["metadata", "--locked", "--offline", "--format-version", "1"])
        .current_dir(root)
        .output()
    else {
        return false;
    };
    if !output.status.success() {
        return false;
    }
    let Ok(doc) = serde_json::from_slice::<Value>(&output.stdout) else {
        return false;
    };
    operability_metadata_binds_logging_crate(root, &doc)
}
fn operability_metadata_binds_logging_crate(root: &Path, doc: &Value) -> bool {
    let Some(packages) = doc["packages"].as_array() else {
        return false;
    };
    let same = |value: &Value, relative: &str| -> bool {
        let Some(actual) = value
            .as_str()
            .and_then(|p| Path::new(p).canonicalize().ok())
        else {
            return false;
        };
        let Ok(expected) = root.join(relative).canonicalize() else {
            return false;
        };
        actual == expected
    };
    let Some(host) = packages.iter().find(|p| {
        p["name"] == "opensip-host" && same(&p["manifest_path"], "crates/host/Cargo.toml")
    }) else {
        return false;
    };
    let Some(host_targets) = host["targets"].as_array() else {
        return false;
    };
    let host_libraries: Vec<_> = host_targets
        .iter()
        .filter(|t| {
            t["kind"]
                .as_array()
                .is_some_and(|k| k.iter().any(|v| v == "lib"))
        })
        .collect();
    if host_libraries.len() != 1 || !same(&host_libraries[0]["src_path"], "crates/host/src/lib.rs")
    {
        return false;
    }
    let Some(nodes) = doc["resolve"]["nodes"].as_array() else {
        return false;
    };
    let Some(node) = nodes.iter().find(|n| n["id"] == host["id"]) else {
        return false;
    };
    let Some(deps) = node["deps"].as_array() else {
        return false;
    };
    let matching: Vec<_> = deps
        .iter()
        .filter(|d| d["name"] == "opensip_operability")
        .collect();
    if matching.len() != 1 {
        return false;
    }
    let Some(package) = packages.iter().find(|p| p["id"] == matching[0]["pkg"]) else {
        return false;
    };
    if package["name"] != "opensip-operability"
        || !same(&package["manifest_path"], "crates/operability/Cargo.toml")
    {
        return false;
    }
    let Some(targets) = package["targets"].as_array() else {
        return false;
    };
    let libraries: Vec<_> = targets
        .iter()
        .filter(|t| {
            t["kind"]
                .as_array()
                .is_some_and(|k| k.iter().any(|v| v == "lib"))
        })
        .collect();
    libraries.len() == 1 && same(&libraries[0]["src_path"], "crates/operability/src/lib.rs")
}
fn has_creator_commit_symbol(text: &str, host_lib: bool, logging_binding: bool) -> bool {
    let text = if host_lib && logging_binding && logging_adapter_is_single_top_level(text) {
        text.replacen(OPTIONAL_LOGGING, "", 1)
    } else {
        text.to_owned()
    };
    identifier_present(&text, "finalize")
}

#[test]
fn creator_commit_guard_keeps_storage_calls_and_limits_the_logging_exception() {
    for source in [
        "finalize(request)",
        "store.finalize(request)",
        "opensip_storage::finalize(request)",
        "use opensip_storage::finalize;",
        "fn finalize() {}",
        "r#finalize(request)",
    ] {
        assert!(
            has_creator_commit_symbol(source, true, true),
            "storage commit must remain forbidden: {source}"
        );
    }
    assert!(!has_creator_commit_symbol(
        "finalize_invocation(false)",
        false,
        true
    ));
    // Dependency names alone are insufficient: bind the resolved package,
    // manifest and both actual library source roots, including rename/bridge
    // and alternate-lib-path negatives without editing any Cargo manifest.
    let root = Path::new(env!("CARGO_MANIFEST_DIR")).join("../..");
    let manifest = |relative: &str| root.join(relative).to_string_lossy().into_owned();
    let graph = serde_json::json!({
        "packages": [
            {"id":"host", "name":"opensip-host", "manifest_path":manifest("crates/host/Cargo.toml"), "targets":[{"kind":["lib"], "src_path":manifest("crates/host/src/lib.rs")}]},
            {"id":"logging", "name":"opensip-operability", "manifest_path":manifest("crates/operability/Cargo.toml"), "targets":[{"kind":["lib"], "src_path":manifest("crates/operability/src/lib.rs")}]},
            {"id":"bridge", "name":"opensip-operability", "manifest_path":manifest("crates/security/Cargo.toml"), "targets":[{"kind":["lib"], "src_path":manifest("crates/security/src/lib.rs")}]}
        ],
        "resolve":{"nodes":[{"id":"host", "deps":[{"name":"opensip_operability", "pkg":"logging"}]}]}
    });
    assert!(operability_metadata_binds_logging_crate(&root, &graph));
    let mut alias = graph.clone();
    alias["resolve"]["nodes"][0]["deps"][0]["pkg"] = serde_json::json!("bridge");
    assert!(
        !operability_metadata_binds_logging_crate(&root, &alias),
        "a same-named bridge is not the logging crate"
    );
    let mut rename = graph.clone();
    rename["resolve"]["nodes"][0]["deps"][0]["name"] = serde_json::json!("other_binding");
    assert!(!operability_metadata_binds_logging_crate(&root, &rename));
    let mut alternate = graph.clone();
    alternate["packages"][1]["targets"][0]["src_path"] =
        serde_json::json!(manifest("crates/security/src/lib.rs"));
    assert!(!operability_metadata_binds_logging_crate(&root, &alternate));
    let mut alternate_host = graph.clone();
    alternate_host["packages"][0]["targets"][0]["src_path"] =
        serde_json::json!(manifest("crates/security/src/lib.rs"));
    assert!(!operability_metadata_binds_logging_crate(
        &root,
        &alternate_host
    ));
    let accepted = format!("{HOST_PREFIX}{OPTIONAL_LOGGING}{NEXT_EXPORT}");
    assert!(!has_creator_commit_symbol(&accepted, true, true));
    assert!(
        has_creator_commit_symbol(&accepted, false, true),
        "only host/lib.rs owns the adapter exception"
    );
    assert!(
        has_creator_commit_symbol(&accepted, true, false),
        "logging must resolve to the actual operability crate"
    );
    let nested = format!("{HOST_PREFIX}mod nested {{\n{OPTIONAL_LOGGING}\n}}{NEXT_EXPORT}");
    assert!(
        has_creator_commit_symbol(&nested, true, true),
        "nested adapter must not be admitted"
    );
    assert!(
        has_creator_commit_symbol(&format!("{accepted}\n{OPTIONAL_LOGGING}"), true, true),
        "duplicate adapter must not be admitted"
    );
    assert!(
        has_creator_commit_symbol(
            &format!("{accepted}\nuse bridge as opensip_operability;"),
            true,
            true
        ),
        "shadowed operability must not be admitted"
    );
    assert!(has_creator_commit_symbol(
        &format!("{accepted}\nmod opensip_operability;"),
        true,
        true
    ));
    assert!(has_creator_commit_symbol(
        &format!("{accepted}\nuse bridge::*;"),
        true,
        true
    ));
    assert!(has_creator_commit_symbol(
        &format!("{accepted}\nbridge::declare_alias!();"),
        true,
        true
    ));
    assert!(has_creator_commit_symbol(
        &format!("{accepted}\n#[macro_use]\nmod bridge;"),
        true,
        true
    ));
    for attribute in [
        "# [path = \"bridge.rs\"]",
        "#\n[path = \"bridge.rs\"]",
        "#//separator\n[some_attribute]",
        "#/**/[some_attribute]",
    ] {
        assert!(
            has_creator_commit_symbol(&format!("{accepted}\n{attribute}\nmod bridge;"), true, true),
            "token-separated attribute must not be admitted: {attribute}"
        );
    }
    assert!(
        has_creator_commit_symbol(
            &format!("{accepted}\nuse bridge::compile_error;"),
            true,
            true
        ),
        "the pinned prefix macro must not be rebound"
    );
    let changed = accepted.replace(
        "opensip_operability::finalize(cancelled);",
        "opensip_storage::finalize(cancelled);",
    );
    assert!(
        has_creator_commit_symbol(&changed, true, true),
        "changing the adapter body must not hide a storage commit"
    );
    assert!(has_creator_commit_symbol(
        &format!("{accepted}\nopensip_storage::finalize(request);"),
        true,
        true
    ));
}

#[test]
fn no_creator_gate_writer_pack_or_commit_symbol_reaches_the_binary_or_the_ingress() {
    let root = Path::new(env!("CARGO_MANIFEST_DIR")).join("../..");
    let mut cli = Vec::new();
    rust_files(&root.join("apps/cli/src"), &mut cli);
    cli.sort();
    assert!(cli.len() >= 4);
    let mut files = cli.clone();
    for host in ["outcomes.rs", "doctor_ingress.rs", "request.rs", "lib.rs"] {
        files.push(root.join("crates/host/src").join(host));
    }
    let logging_binding = operability_is_the_resolved_logging_crate(&root);
    assert!(
        logging_binding,
        "the operability binding must resolve to the accepted logging crate"
    );
    for file in &files {
        let text = production(file);
        for forbidden in [
            // The creator.
            "run_initial_creator",
            "create_initial_installation",
            "mint_intent",
            "CreationIntent",
            // The ordinary writer and the gate.
            "admit_ordinary_writer",
            "produce_write_platform",
            "DurableWriteGate",
            // Pack admission.
            "admit_policy_selection",
            // The commit path.
            "finalize",
            "route_recovery",
        ] {
            assert!(
                if forbidden == "finalize" {
                    !has_creator_commit_symbol(
                        &text,
                        *file == root.join("crates/host/src/lib.rs"),
                        logging_binding,
                    )
                } else {
                    !text.contains(forbidden)
                },
                "{forbidden} in {}",
                file.display()
            );
        }
    }
    for file in &cli {
        assert!(
            !production(file).contains("installation_entry"),
            "installation_entry in {}",
            file.display()
        );
    }
    // In opensip-security the creator and the ordinary writer stay
    // crate-private, each defined once, and lib.rs re-exports neither.
    let mut security = Vec::new();
    rust_files(&root.join("crates/security/src"), &mut security);
    for (name, owner) in [
        ("run_initial_creator", "custody/installation_routing.rs"),
        ("admit_ordinary_writer", "custody/ordinary_writer.rs"),
    ] {
        let definition = format!("fn {name}(");
        let defined: Vec<_> = security
            .iter()
            .filter(|file| production(file).contains(&definition))
            .collect();
        assert_eq!(
            defined,
            [&root.join("crates/security/src").join(owner)],
            "{name}"
        );
        let text = production(defined[0]);
        assert_eq!(text.matches(&definition).count(), 1, "{name}");
        assert!(
            text.contains(&format!("pub(crate) {definition}")),
            "{name} is not pub(crate)"
        );
        let lib = production(&root.join("crates/security/src/lib.rs"));
        assert!(!lib.contains(name), "lib.rs names {name}");
    }
}
