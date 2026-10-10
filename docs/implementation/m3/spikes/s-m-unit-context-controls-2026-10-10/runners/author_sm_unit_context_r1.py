from pathlib import Path
v=Path('/tmp/opensip-implementation/sm-cargo-unit-context-2026-10-10');p=v/'producer';parent=p/'src/cargo/core/compiler/compilation.rs';parent.write_text(parent.read_text()+'\n#[cfg(test)]\npub(crate) mod experimental_unit_context;\n')
f=p/'src/cargo/core/compiler/compilation/experimental_unit_context.rs';f.parent.mkdir(parents=True,exist_ok=True)
f.write_text('''//! Unadmitted experiment DATA only; no commands are executed here.
use super::*;
use crate::core::compiler::BuildContext;

pub(crate) fn capture(bcx: &BuildContext<'_, '_>, root: &Path) -> CargoResult<()> {
    let mut compilation = Compilation::new(bcx)?;
    // Explicit prototype metadata search output, not a real Cargo layout claim.
    compilation.deps_output.insert(CompileKind::Host, root.join("prototype-host-deps"));
    let mut units: Vec<_> = bcx.unit_graph.iter().collect();
    units.sort_unstable(); // Exactly the same ordering as the pinned unit graph serializer.
    let mut rows = Vec::new();
    for (index, (unit, _)) in units.iter().enumerate() {
        // Primary-package handling and real output layout remain separate duties.
        let mut command = compilation.rustc_process(unit, false, bcx.ws.is_member(&unit.pkg))?;
        super::super::add_cap_lints(bcx, unit, &mut command);
        let arguments = command.get_args().map(|s| s.to_str().map(str::to_owned).ok_or_else(|| anyhow::anyhow!("non UTF8 argument DATA"))).collect::<CargoResult<Vec<_>>>()?;
        let mut env = std::collections::BTreeMap::new();
        let mut removed = Vec::new();
        for (name, value) in command.get_envs() {
            match value {
                Some(value) => { env.insert(name.clone(), value.to_str().ok_or_else(|| anyhow::anyhow!("non UTF8 environment DATA"))?.to_owned()); }
                None => removed.push(name.clone()),
            }
        }
        rows.push(serde_json::json!({"index":index,"packageId":unit.pkg.package_id().to_spec(),"target":unit.target,"profile":unit.profile,"platform":unit.kind,"mode":unit.mode,"features":unit.features,"cargoUnitRustflags":unit.rustflags,"cwd":command.get_cwd(),"constructedEnvironment":env,"removedEnvironmentKeys":removed,"capLintArguments":arguments,"localPackageByActualCargo":unit.is_local(),"showWarningsByActualCargo":unit.show_warnings(bcx.gctx),"primaryPackageMaterialized":false,"realCargoOutputLayoutMaterialized":false,"completeCompilerCommand":false}));
    }
    std::fs::write(root.join("unit-context-data.json"), serde_json::to_vec_pretty(&serde_json::json!({"version":1,"standing":"EXPERIMENTAL ACTUAL CARGO PACKAGE ENV/CWD/CAP-LINT DATA; NOT COMPLETE COMMAND OR NATIVE PROFILE","units":rows,"nativeAdmission":false,"BuildRunnerUsed":false,"fixtureOrCorpusCodeExecuted":false,"completeCompilerCommand":false,"fullCargoProfileEnvironment":false}))?)?;
    Ok(())
}
''')
s=(p/'src/cargo/util/context/experimental_corpus_association.rs').read_text();s=s.replace('    *context.shell() = Shell::from_write(', '    crate::core::compiler::compilation::experimental_unit_context::capture(&bcx, root)?;\n    *context.shell() = Shell::from_write(',1)
# Copied inherited controls remain source only; run only new named unit-context controls.
s+='''
#[test]
fn unit_context_actual_manifest_environment_cwd_and_local_lints() {
    let root = retained_root();
    let project = root.join("project");
    write(&project, "Cargo.toml", "[package]\\nname='unit-context'\\nversion='2.3.4-beta.1'\\nedition='2024'\\nauthors=['First','Second']\\ndescription='owned fixture'\\nlicense='MIT'\\n[lib]\\nname='selected_lib'\\n");
    write(&project, "src/lib.rs", "compile_error!(\\\"fixture must not execute\\\");\\n");
    let observation = root.join("observation"); std::fs::create_dir(&observation).unwrap();
    graph(&observation, &project, HashMap::new(), false).unwrap();
    let data: serde_json::Value = serde_json::from_slice(&std::fs::read(observation.join("unit-context-data.json")).unwrap()).unwrap();
    let units = data["units"].as_array().unwrap(); assert_eq!(units.len(),1);
    let row = &units[0]; let env = &row["constructedEnvironment"];
    assert_eq!(row["index"],0); assert_eq!(row["cwd"],project.to_str().unwrap());
    assert_eq!(env["CARGO_MANIFEST_DIR"],project.to_str().unwrap());
    assert_eq!(env["CARGO_MANIFEST_PATH"],project.join("Cargo.toml").to_str().unwrap());
    assert_eq!(env["CARGO_PKG_VERSION"],"2.3.4-beta.1"); assert_eq!(env["CARGO_PKG_VERSION_MAJOR"],"2");
    assert_eq!(env["CARGO_PKG_VERSION_MINOR"],"3"); assert_eq!(env["CARGO_PKG_VERSION_PATCH"],"4"); assert_eq!(env["CARGO_PKG_VERSION_PRE"],"beta.1");
    assert_eq!(env["CARGO_PKG_AUTHORS"],"First:Second"); assert_eq!(env["CARGO_PKG_DESCRIPTION"],"owned fixture"); assert_eq!(env["CARGO_PKG_LICENSE"],"MIT"); assert_eq!(env["CARGO_CRATE_NAME"],"selected_lib");
    assert_eq!(row["capLintArguments"],serde_json::json!([])); assert_eq!(row["localPackageByActualCargo"],true);
    assert_eq!(row["completeCompilerCommand"],false); assert_eq!(data["BuildRunnerUsed"],false);
    assert_eq!(std::fs::read(project.join("src/lib.rs")).unwrap(),b"compile_error!(\\\"fixture must not execute\\\");\\n");
    eprintln!("ACTUAL_UNIT_CONTEXT_CONTROL={}",root.display());
}
#[test]
fn unit_context_actual_two_package_index_join_and_renamed_edge() {
    let root=retained_root();let project=root.join("project");
    write(&project,"Cargo.toml","[workspace]\\nmembers=['one','two']\\nresolver='2'\\n");
    write(&project,"one/Cargo.toml","[package]\\nname='one'\\nversion='1.0.0'\\nedition='2024'\\n[dependencies]\\nrenamed={package='two',path='../two'}\\n");
    write(&project,"two/Cargo.toml","[package]\\nname='two'\\nversion='4.5.6'\\nedition='2024'\\n");
    for name in ["one","two"] {write(&project,&format!("{name}/src/lib.rs"),"compile_error!(\\\"not executed\\\");\\n");}
    let observation=root.join("observation");std::fs::create_dir(&observation).unwrap();graph(&observation,&project,HashMap::new(),false).unwrap();
    let data:serde_json::Value=serde_json::from_slice(&std::fs::read(observation.join("unit-context-data.json")).unwrap()).unwrap();
    let graph:serde_json::Value=serde_json::from_slice(&std::fs::read(observation.join("unit-graph.json")).unwrap()).unwrap()).unwrap();
    assert_eq!(data["units"].as_array().unwrap().len(),2);
    for (index,row) in data["units"].as_array().unwrap().iter().enumerate(){assert_eq!(row["index"],index);assert_eq!(row["packageId"],graph["units"][index]["pkg_id"]);assert_eq!(row["target"],graph["units"][index]["target"]);assert_eq!(row["profile"],graph["units"][index]["profile"]);assert_eq!(row["platform"],graph["units"][index]["platform"]);assert_eq!(row["features"],graph["units"][index]["features"]);assert_eq!(row["capLintArguments"],serde_json::json!([]));}
    assert!(graph["units"].as_array().unwrap().iter().any(|row|row["dependencies"].as_array().unwrap().iter().any(|dep|dep["extern_crate_name"]=="renamed")));
    eprintln!("ACTUAL_UNIT_CONTEXT_CONTROL={}",root.display());
}
'''
s=s.replace('unwrap()).unwrap()).unwrap();','unwrap()).unwrap();')
(p/'src/cargo/util/context/experimental_unit_context.rs').write_text(s)
print('New isolated Cargo context source prepared; no corpus use')
