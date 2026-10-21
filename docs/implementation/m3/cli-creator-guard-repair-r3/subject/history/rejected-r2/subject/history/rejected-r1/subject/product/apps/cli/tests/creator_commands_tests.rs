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

/// X11 keeps the storage commit entry point out of the ingress. The
/// already selected optional logging adapter has a different responsibility.
/// Permit only its exact body in host/lib.rs; a changed body fails closed.
fn has_creator_commit_symbol(text: &str, host_lib: bool) -> bool {
    const OPTIONAL_LOGGING: &str = "pub fn finalize_invocation(cancelled: bool) {\n    opensip_operability::finalize(cancelled);\n}";
    let text = if host_lib {
        text.replace(OPTIONAL_LOGGING, "")
    } else {
        text.to_owned()
    };
    // `finalize_invocation` is one identifier, not the commit identifier
    // `finalize`. Qualified calls, imports and definitions of the latter
    // remain refused; other forbidden authority names retain their check.
    text.split(|c: char| !(c.is_alphanumeric() || c == '_'))
        .any(|identifier| identifier == "finalize")
}

#[test]
fn creator_commit_guard_keeps_storage_calls_and_limits_the_logging_exception() {
    for source in [
        "finalize(request)",
        "store.finalize(request)",
        "opensip_storage::finalize(request)",
        "use opensip_storage::finalize;",
        "fn finalize() {}",
    ] {
        assert!(
            has_creator_commit_symbol(source, true),
            "storage commit must remain forbidden: {source}"
        );
    }
    assert!(!has_creator_commit_symbol(
        "finalize_invocation(false)",
        false
    ));
    let logging = "pub fn finalize_invocation(cancelled: bool) {\n    opensip_operability::finalize(cancelled);\n}";
    assert!(!has_creator_commit_symbol(logging, true));
    assert!(
        has_creator_commit_symbol(logging, false),
        "only host/lib.rs owns the adapter exception"
    );
    let changed = logging.replace(
        "opensip_operability::finalize(cancelled);",
        "opensip_storage::finalize(cancelled);",
    );
    assert!(
        has_creator_commit_symbol(&changed, true),
        "changing the adapter body must not hide a storage commit"
    );
    assert!(has_creator_commit_symbol(
        &format!("{logging}\nopensip_storage::finalize(request);"),
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
                    !has_creator_commit_symbol(&text, *file == root.join("crates/host/src/lib.rs"))
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
