--- /dev/null
+++ candidate/src/cargo/util/context/experimental_resolver_controls.rs
@@ -0,0 +1,206 @@
+//! First-party fixtures only: never build or execute their source files.
+use super::*;
+use crate::core::Workspace;
+use crate::core::compiler::{CompileKind, CompileTarget, UnitInterner, UserIntent};
+use crate::core::resolver::CliFeatures;
+use std::collections::BTreeSet;
+use std::ffi::OsString;
+
+fn write(root: &Path, relative: &str, text: &str) {
+    let path = root.join(relative);
+    std::fs::create_dir_all(path.parent().unwrap()).unwrap();
+    std::fs::write(path, text).unwrap();
+}
+
+fn run_fixture(with_macro: bool, defaults: bool) -> serde_json::Value {
+    let root = tempfile::Builder::new()
+        .prefix("opensip-experiment-resolver-control-")
+        .tempdir()
+        .unwrap()
+        .keep();
+    let project = root.join("project");
+    write(
+        &project,
+        "Cargo.toml",
+        "[workspace]\nmembers=['app','dep','macro_pkg','build_helper','linux_only']\ndefault-members=['app']\nresolver='2'\n",
+    );
+    write(
+        &project,
+        "app/Cargo.toml",
+        "[package]\nname='app'\nversion='1.0.0'\nedition='2024'\n[dependencies]\nrenamed={package='dep',path='../dep',default-features=false}\nmacro_pkg={path='../macro_pkg',optional=true}\n[build-dependencies]\nbuild_helper={path='../build_helper'}\n[target.'cfg(target_os = \"linux\")'.dependencies]\nlinux_only={path='../linux_only'}\n[features]\ndefault=['picked']\npicked=['renamed/chosen']\nwith-macro=['dep:macro_pkg']\n",
+    );
+    write(
+        &project,
+        "app/src/lib.rs",
+        "compile_error!(\"fixture source must not be compiled\");\n",
+    );
+    write(
+        &project,
+        "app/build.rs",
+        "fn main(){panic!(\"fixture build script must not execute\");}\n",
+    );
+    for name in ["dep", "macro_pkg", "build_helper", "linux_only"] {
+        let mut manifest = format!("[package]\nname='{name}'\nversion='1.0.0'\nedition='2024'\n");
+        if name == "macro_pkg" {
+            manifest.push_str("[lib]\nproc-macro=true\n");
+        }
+        if name == "dep" {
+            manifest.push_str("[features]\ndefault=['ambient']\nambient=[]\nchosen=[]\n");
+        }
+        write(&project, &format!("{name}/Cargo.toml"), &manifest);
+        write(
+            &project,
+            &format!("{name}/src/lib.rs"),
+            "compile_error!(\"fixture dependency must not be compiled\");\n",
+        );
+    }
+    let home = root.join("home");
+    let queries = root.join("queries");
+    std::fs::create_dir(&home).unwrap();
+    std::fs::create_dir(&queries).unwrap();
+    let head = ["-", "--crate-name", "___", "--print=file-names"];
+    let tail = [
+        "--crate-type",
+        "bin",
+        "--crate-type",
+        "rlib",
+        "--crate-type",
+        "dylib",
+        "--crate-type",
+        "cdylib",
+        "--crate-type",
+        "staticlib",
+        "--crate-type",
+        "proc-macro",
+        "--print=sysroot",
+        "--print=split-debuginfo",
+        "--print=crate-name",
+        "--print=cfg",
+        "-Wwarnings",
+    ];
+    let host_args = head.iter().chain(tail.iter()).map(OsString::from).collect();
+    let target_args = head
+        .iter()
+        .chain(["--target", "aarch64-apple-darwin"].iter())
+        .chain(tail.iter())
+        .map(OsString::from)
+        .collect();
+    let base = cargo_util::ProcessBuilder::experimental_information_queries(
+        Path::new("/Users/sb/code/.opensip-implementation-cache/g2-rust-1.95/sysroot/bin/rustc"),
+        &project,
+        vec![vec!["-vV".into()], host_args, target_args],
+        "b829b733131d4e1673eeebd1f34d06ae1e9ff4977b051313cf42e2a9e79ecf1c".into(),
+        &queries,
+    );
+    let mut context = GlobalContext::new_experimental_query_context(
+        Shell::new(),
+        project.clone(),
+        home,
+        HashMap::new(),
+        base,
+    );
+    // An absent lock is an explicitly generated first-party experiment input.
+    context
+        .configure(0, false, Some("never"), false, false, true, &None, &[], &[])
+        .unwrap();
+    let mut workspace = Workspace::new(&project.join("Cargo.toml"), &context).unwrap();
+    workspace.set_target_dir(Filesystem::new(root.join("target")));
+    let mut options =
+        crate::ops::CompileOptions::new(&context, UserIntent::Check { test: false }).unwrap();
+    options.spec = crate::ops::Packages::Default;
+    options.cli_features = CliFeatures::from_command_line(
+        &if with_macro {
+            vec!["with-macro".to_string()]
+        } else {
+            vec![]
+        },
+        false,
+        defaults,
+    )
+    .unwrap();
+    options.build_config.requested_kinds = vec![CompileKind::Target(
+        CompileTarget::new("aarch64-apple-darwin", false).unwrap(),
+    )];
+    options.build_config.unit_graph = true;
+    let interner = UnitInterner::new();
+    let bcx = crate::ops::create_bcx(&workspace, &options, &interner, None).unwrap();
+    // Retain Cargo's full indexed graph, not only the assertion summary.
+    let graph_path = root.join("unit-graph.json");
+    *context.shell() = Shell::from_write(Box::new(std::fs::File::create(&graph_path).unwrap()));
+    crate::core::compiler::unit_graph::emit_serialized_unit_graph(
+        &bcx.roots,
+        &bcx.unit_graph,
+        &context,
+    )
+    .unwrap();
+    *context.shell() = Shell::new();
+    let complete_graph: serde_json::Value =
+        serde_json::from_slice(&std::fs::read(&graph_path).unwrap()).unwrap();
+    assert_eq!(complete_graph["version"], 1);
+    assert_eq!(
+        complete_graph["units"].as_array().unwrap().len(),
+        bcx.unit_graph.len()
+    );
+    let mut rows: Vec<_> = bcx.unit_graph.iter().map(|(unit, deps)| serde_json::json!({
+        "package": unit.pkg.name().to_string(), "target": unit.target.name(),
+        "customBuild": unit.target.is_custom_build(), "procMacro": unit.target.proc_macro(),
+        "mode": format!("{:?}",unit.mode), "platform": format!("{:?}",unit.kind),
+        "features": unit.features.iter().map(ToString::to_string).collect::<Vec<_>>(),
+        "dependencies": deps.iter().map(|d| serde_json::json!({"package":d.unit.pkg.name().to_string(),"extern":d.extern_crate_name.to_string()})).collect::<Vec<_>>()
+    })).collect();
+    rows.sort_by_key(ToString::to_string);
+    let roots: BTreeSet<_> = bcx.roots.iter().map(|u| u.pkg.name().to_string()).collect();
+    assert_eq!(roots, BTreeSet::from(["app".to_string()]));
+    assert!(!rows.iter().any(|r| r["package"] == "linux_only"));
+    assert_eq!(rows.iter().any(|r| r["procMacro"] == true), with_macro);
+    assert!(rows.iter().any(|r| r["customBuild"] == true));
+    let dep = rows.iter().find(|r| r["package"] == "dep").unwrap();
+    assert_eq!(
+        dep["features"]
+            .as_array()
+            .unwrap()
+            .iter()
+            .any(|v| v == "chosen"),
+        defaults
+    );
+    assert!(
+        !dep["features"]
+            .as_array()
+            .unwrap()
+            .iter()
+            .any(|v| v == "ambient")
+    );
+    assert!(
+        rows.iter()
+            .filter(|r| r["package"] == "app" && r["customBuild"] == false)
+            .any(|r| r["dependencies"]
+                .as_array()
+                .unwrap()
+                .iter()
+                .any(|d| d["package"] == "dep" && d["extern"] == "renamed"))
+    );
+    assert!(project.join("Cargo.lock").is_file());
+    let report = serde_json::json!({"root":root,"units":rows,"roots":roots,"withMacro":with_macro,
+        "defaultFeatures":defaults,"generatedExperimentalLock":true,"unitGraphOnly":true,
+        "fixtureSourcesExecuted":false,"nativeAdmission":false,"fullSM":false});
+    std::fs::write(
+        root.join("control.json"),
+        serde_json::to_vec_pretty(&report).unwrap(),
+    )
+    .unwrap();
+    eprintln!("ACTUAL_EXPERIMENT_RESOLVER_CONTROL={}", root.display());
+    report
+}
+
+#[test]
+fn default_member_features_target_and_renamed_path_dependency() {
+    run_fixture(false, true);
+}
+#[test]
+fn no_default_features_keeps_real_dependency_without_feature() {
+    run_fixture(false, false);
+}
+#[test]
+fn selected_macro_and_custom_build_remain_graph_units_without_execution() {
+    run_fixture(true, true);
+}
