// Law X10 items 5 and 7, the binary layer. The real built `opensip doctor`
// runs with no override of any kind: a development build ends at F0 with
// `CORE.NO_EMBEDDED_RELEASE`, exit 2, before any installation path is
// opened. These tests assert exactly that shipped behaviour, the envelope's
// schema validity, and that the account's real installation is untouched.
// The source pins keep every home, profile and release selector out of the
// binary and the doctor ingress.
use serde_json::Value;
use std::path::{Path, PathBuf};
use std::process::Command;

const ENVELOPE: &str = "urn:opensip:product-v1:workflows:evaluator3:command-envelope:7";

fn real_installation() -> PathBuf {
    let home = std::env::var_os("HOME").expect("HOME for the test process");
    Path::new(&home).join("Library/Application Support/OpenSIP")
}
fn doctor(args: &[&str]) -> std::process::Output {
    // A scratch working directory: the command reads no project or
    // configuration, and HOME plays no part in finding the installation.
    let cwd = std::env::temp_dir();
    Command::new(env!("CARGO_BIN_EXE_opensip"))
        .args(args)
        .current_dir(cwd)
        .output()
        .unwrap()
}
fn schema_valid(raw: &[u8]) -> bool {
    opensip_host::embedded_schema_registry()
        .unwrap()
        .schema(ENVELOPE, "")
        .unwrap()
        .admit_json(raw, 64 * 1024 * 1024)
        .is_ok()
}

#[test]
fn a_development_build_doctor_ends_at_no_embedded_release_in_both_formats() {
    let existed = real_installation().exists();
    let out = doctor(&["doctor", "--format", "json"]);
    assert_eq!(out.status.code(), Some(2));
    assert!(out.stderr.is_empty());
    assert!(schema_valid(&out.stdout));
    let value: Value = serde_json::from_slice(&out.stdout).unwrap();
    assert_eq!(value["kind"], "failure");
    assert!(value.get("doctor").is_none());
    assert_eq!(value["exitCode"], 2);
    assert_eq!(value["termination"]["class"], "request-rejected");
    assert_eq!(
        value["termination"]["errorCode"],
        "REQUEST.PRECONDITION_FAILED"
    );
    assert_eq!(
        value["termination"]["domainDetail"]["code"],
        "CORE.NO_EMBEDDED_RELEASE"
    );
    assert_eq!(value["errors"][0], value["termination"]["domainDetail"]);
    let id = value["requestId"].as_str().unwrap();
    assert!(id.starts_with("req1_") && id.len() == 37);

    let human = doctor(&["doctor"]);
    assert_eq!(human.status.code(), Some(2));
    let text = String::from_utf8(human.stdout).unwrap();
    let remedy = value["errors"][0]["remedy"].as_str().unwrap();
    assert!(text.starts_with(&format!(
        "Termination: request-rejected\nError: REQUEST.PRECONDITION_FAILED\n\
         Detail: CORE.NO_EMBEDDED_RELEASE\nRemedy: {remedy}\nRequest: req1_"
    )));
    // Nothing was created: a development build cannot reach any path.
    assert_eq!(real_installation().exists(), existed);
}

#[test]
fn doctor_takes_no_flags_and_agent_format_is_not_applicable() {
    let out = doctor(&["doctor", "--checks", "platform", "--format=json"]);
    assert_eq!(out.status.code(), Some(2));
    let value: Value = serde_json::from_slice(&out.stdout).unwrap();
    assert_eq!(value["termination"]["errorCode"], "REQUEST.UNKNOWN_OPTION");
    let out = doctor(&["doctor", "extra", "--format=json"]);
    assert_eq!(out.status.code(), Some(2));
    let out = doctor(&["doctor", "--format=agent"]);
    assert_eq!(out.status.code(), Some(2));
    assert!(
        String::from_utf8(out.stdout)
            .unwrap()
            .contains("OUTPUT.FORMAT_NOT_APPLICABLE")
    );
}

#[test]
fn help_and_completion_list_doctor() {
    let out = doctor(&["help", "doctor", "--format=json"]);
    assert_eq!(out.status.code(), Some(0));
    let value: Value = serde_json::from_slice(&out.stdout).unwrap();
    assert_eq!(
        value["meta"]["commands"],
        serde_json::json!([{
            "name": "doctor",
            "usage": "opensip doctor [--format human|json]",
            "summary": "Report the health of this account's OpenSIP installation."
        }])
    );
    let text = String::from_utf8(doctor(&["completion", "bash"]).stdout).unwrap();
    assert!(text.contains("doctor"));
}

/// Production code: everything before a `#[cfg(test)]` test module, with
/// comment lines removed.
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

#[test]
fn no_home_profile_or_release_selector_reaches_the_binary_or_the_ingress() {
    let root = Path::new(env!("CARGO_MANIFEST_DIR")).join("../..");
    let mut files: Vec<PathBuf> = std::fs::read_dir(root.join("apps/cli/src"))
        .unwrap()
        .map(|entry| entry.unwrap().path())
        .collect();
    files.push(root.join("crates/host/src/doctor_ingress.rs"));
    files.push(root.join("crates/host/src/outcomes.rs"));
    files.push(root.join("crates/host/src/request.rs"));
    files.sort();
    for file in &files {
        let text = production(file);
        for forbidden in [
            "std::env::var",
            "env::var",
            "var_os",
            "home_dir",
            "cfg(feature",
            "cfg(test)",
            "cfg(debug_assertions)",
        ] {
            // `main.rs` passes the process arguments, nothing else.
            assert!(
                !text.contains(forbidden),
                "{forbidden} in {}",
                file.display()
            );
        }
    }
    // The ingress's one producer call; no other producer or session entry.
    let ingress = production(&root.join("crates/host/src/doctor_ingress.rs"));
    assert_eq!(
        ingress.matches("observe_installation_for_doctor()").count(),
        1
    );
    for forbidden in [
        "produce_read_platform",
        "produce_on",
        "observe_with",
        "ObservationSession",
        "HomeSource",
        "read_producers",
    ] {
        assert!(!ingress.contains(forbidden), "{forbidden} in the ingress");
    }
    // No cross-crate test bridge reaches the binary, the ingress or a
    // default or release build (law X10 r4 item 5): `apps/cli` and
    // `reporting` declare no features; host, security and storage declare
    // only X9's `crash-matrix` and X8's `scenario-fixtures`, never as a
    // default. Their own release guards are pinned by their laws' units.
    for manifest in ["apps/cli", "crates/reporting"] {
        let text = std::fs::read_to_string(root.join(manifest).join("Cargo.toml")).unwrap();
        assert!(!text.contains("[features]"), "{manifest} declares features");
    }
    for manifest in ["crates/host", "crates/security", "crates/storage"] {
        let text = std::fs::read_to_string(root.join(manifest).join("Cargo.toml")).unwrap();
        let mut in_features = false;
        for raw in text.lines() {
            let line = raw.split('#').next().unwrap_or("").trim();
            if line.starts_with('[') {
                in_features = line == "[features]";
                continue;
            }
            if !in_features || line.is_empty() {
                continue;
            }
            let name = line.split('=').next().unwrap_or("").trim();
            assert!(
                matches!(name, "crash-matrix" | "scenario-fixtures"),
                "{manifest} declares feature {name:?}"
            );
        }
    }
}
