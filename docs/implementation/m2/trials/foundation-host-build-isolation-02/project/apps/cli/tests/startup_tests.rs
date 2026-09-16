use serde_json::Value;
use std::{
    path::PathBuf,
    process::{Command, Output},
    sync::atomic::{AtomicU64, Ordering},
};
static NEXT: AtomicU64 = AtomicU64::new(0);
struct Fixture(PathBuf);
impl Fixture {
    fn new() -> Self {
        let root = std::env::temp_dir().join(format!(
            "opensip-startup-{}-{}",
            std::process::id(),
            NEXT.fetch_add(1, Ordering::Relaxed)
        ));
        std::fs::create_dir(&root).unwrap();
        std::fs::create_dir(root.join(".opensip")).unwrap();
        std::fs::write(root.join(".opensip/config.json"), "not valid configuration").unwrap();
        std::fs::write(root.join("package.json"), "not valid package data").unwrap();
        Self(root)
    }
    fn run(&self, args: &[&str]) -> Output {
        Command::new(env!("CARGO_BIN_EXE_opensip"))
            .args(args)
            .current_dir(&self.0)
            .env_clear()
            .env("HOME", self.0.join("missing-home"))
            .env("OPENSIP_BUILD_CHANNEL", "release")
            .env("OPENSIP_HOST_RELEASE", "99.99.99")
            .env(
                "OPENSIP_CLOSURE_IDS",
                "closure2:ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
            )
            .env("OPENSIP_STORE", self.0.join("missing-store"))
            .env("OPENSIP_COMPONENTS", self.0.join("missing-providers"))
            .output()
            .unwrap()
    }
}
impl Drop for Fixture {
    fn drop(&mut self) {
        let _ = std::fs::remove_dir_all(&self.0);
    }
}
fn json(output: &Output) -> Value {
    serde_json::from_slice(&output.stdout).unwrap()
}
fn request_id(value: &Value) -> &str {
    let id = value["requestId"].as_str().unwrap();
    assert_eq!(id.len(), 37);
    assert!(id.starts_with("req1_"));
    assert!(
        id[5..]
            .bytes()
            .all(|x| x.is_ascii_digit() || (b'a'..=b'f').contains(&x))
    );
    id
}
#[test]
fn metadata_starts_without_project_services_and_ignores_release_environment() {
    let f = Fixture::new();
    let a = f.run(&["version", "--format=json"]);
    assert_eq!(a.status.code(), Some(0));
    assert!(a.stderr.is_empty());
    let v = json(&a);
    request_id(&v);
    assert_eq!(v["schemaMajor"], 7);
    assert_eq!(v["meta"]["hostRelease"], env!("CARGO_PKG_VERSION"));
    assert_eq!(v["meta"]["buildChannel"], "development");
    assert_eq!(v["meta"]["closureIds"], serde_json::json!([]));
    assert_eq!(v["termination"], serde_json::json!({"class":"success"}));
    for forbidden in [
        "projectId",
        "projectRoot",
        "run",
        "invocation",
        "errors",
        "diagnostics",
    ] {
        assert!(v.get(forbidden).is_none());
    }
    assert!(!f.0.join("missing-home").exists());
    assert!(!f.0.join("missing-store").exists());
    assert!(!f.0.join("missing-providers").exists());
    let human = f.run(&["--version"]);
    let text = String::from_utf8(human.stdout).unwrap();
    assert!(text.contains(env!("CARGO_PKG_VERSION")));
    assert!(text.contains("development"));
    assert!(text.contains("Component closures: none"));
}
#[test]
fn help_and_completions_share_the_implemented_catalogue() {
    let f = Fixture::new();
    let machine = f.run(&["help", "--format=json"]);
    assert!(machine.status.success());
    let value = json(&machine);
    let rows = value["meta"]["commands"].as_array().unwrap();
    let names: Vec<_> = rows.iter().map(|x| x["name"].as_str().unwrap()).collect();
    assert_eq!(names, ["completion", "help", "version"]);
    let human = String::from_utf8(f.run(&["help"]).stdout).unwrap();
    for row in rows {
        for field in ["name", "usage", "summary"] {
            assert!(human.contains(row[field].as_str().unwrap()));
        }
    }
    for shell in ["bash", "zsh", "fish"] {
        let c = f.run(&["completion", shell]);
        assert!(c.status.success());
        let text = String::from_utf8(c.stdout).unwrap();
        for name in &names {
            assert!(text.contains(name));
        }
    }
    let topic = json(&f.run(&["help", "version", "--format=json"]));
    assert_eq!(topic["meta"]["topic"], "version");
    assert_eq!(topic["meta"]["commands"].as_array().unwrap().len(), 1);
}
#[test]
fn parser_refusals_have_fresh_ids_and_preserve_present_empty_errors() {
    let f = Fixture::new();
    let mut ids = std::collections::BTreeSet::new();
    for args in [
        vec!["--format=json", "--unknown"],
        vec!["--format=json", "help", "analyze"],
        vec![
            "--format=json",
            "version",
            "--request-id",
            "req1_00000000000000000000000000000000",
        ],
        vec!["--format=json", "version", "--build-channel=release"],
    ] {
        let out = f.run(&args);
        assert_eq!(out.status.code(), Some(2));
        let value = json(&out);
        assert!(ids.insert(request_id(&value).to_owned()));
        assert_eq!(value["errors"], serde_json::json!([]));
        assert!(!value["diagnostics"].as_array().unwrap().is_empty());
        assert!(value.get("meta").is_none());
        assert_eq!(value["termination"]["errorCode"], "REQUEST.UNKNOWN_OPTION");
    }
    let out = f.run(&["completion", "bash", "--format=json"]);
    assert_eq!(out.status.code(), Some(2));
    assert_eq!(
        json(&out)["errors"][0]["code"],
        "OUTPUT.FORMAT_NOT_APPLICABLE"
    );
}
#[test]
fn correlation_has_exact_bounds_and_never_replaces_request_identity() {
    let f = Fixture::new();
    for token in ["client:42".to_owned(), "🙂".repeat(128)] {
        let out = f.run(&[
            "version",
            "--format=json",
            "--client-correlation-id",
            &token,
        ]);
        assert_eq!(out.status.code(), Some(0));
        let v = json(&out);
        assert_eq!(v["clientCorrelationId"], token);
        assert_ne!(request_id(&v), token);
    }
    for token in [String::new(), "x".repeat(129)] {
        let out = f.run(&[
            "version",
            "--format=json",
            "--client-correlation-id",
            &token,
        ]);
        assert_eq!(out.status.code(), Some(2));
        let v = json(&out);
        assert!(v.get("clientCorrelationId").is_none());
    }
}

#[test]
fn required_output_failure_never_emits_a_second_envelope() {
    let fixture = Fixture::new();
    let readonly = std::fs::File::open(fixture.0.join("package.json")).unwrap();
    let out = Command::new(env!("CARGO_BIN_EXE_opensip"))
        .args(["version", "--format=json"])
        .stdout(std::process::Stdio::from(readonly))
        .stderr(std::process::Stdio::piped())
        .output()
        .unwrap();
    assert_eq!(out.status.code(), Some(4));
    assert_eq!(
        out.stderr,
        b"OUTPUT.SERIALIZATION_FAILED: required output emission failed.\n"
    );
    assert!(out.stdout.is_empty());
}

#[test]
fn human_failure_and_success_display_termination_and_registered_details() {
    let fixture = Fixture::new();
    for (args, code, detail) in [
        (vec!["--nope"], "REQUEST.UNKNOWN_OPTION", None),
        (
            vec!["version", "--format=sarif"],
            "REQUEST.UNKNOWN_OPTION",
            Some("OUTPUT.FORMAT_NOT_APPLICABLE"),
        ),
    ] {
        let out = fixture.run(&args);
        assert_eq!(out.status.code(), Some(2));
        let text = String::from_utf8(out.stdout).unwrap();
        assert!(text.contains("Termination: request-rejected"));
        assert!(text.contains(&format!("Error: {code}\n")));
        assert!(text.contains("Request: req1_"));
        if let Some(detail) = detail {
            assert!(text.contains(&format!(
                "Detail: {detail}\nRemedy: Choose an applicable output format.\nRequest: req1_"
            )));
        }
    }
    for args in [
        vec!["help"],
        vec!["version"],
        vec!["completion", "bash"],
        vec!["completion", "zsh"],
        vec!["completion", "fish"],
    ] {
        let out = fixture.run(&args);
        assert!(out.status.success());
        assert!(
            String::from_utf8(out.stdout)
                .unwrap()
                .contains("Termination: success")
        );
    }
    let readonly = std::fs::File::open(fixture.0.join("package.json")).unwrap();
    let out = Command::new(env!("CARGO_BIN_EXE_opensip"))
        .arg("version")
        .stdout(std::process::Stdio::from(readonly))
        .stderr(std::process::Stdio::piped())
        .output()
        .unwrap();
    assert_eq!(out.status.code(), Some(4));
    let text = String::from_utf8(out.stderr).unwrap();
    assert_eq!(
        text,
        "OUTPUT.SERIALIZATION_FAILED: required output emission failed.\n"
    );
}
