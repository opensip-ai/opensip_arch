from pathlib import Path
V=Path('/tmp/opensip-implementation/sm-command-data-2026-10-10');p=V/'producer'
f=p/'src/cargo/core/compiler/mod.rs';f.write_text(f.read_text()+'''\n#[cfg(test)]\nmod experimental_command_data;\n#[cfg(test)]\npub(crate) fn capture_experimental_command_data(bcx: &BuildContext<'_, '_>, root: &Path) -> CargoResult<()> { experimental_command_data::capture(bcx, root) }\n''')
f=p/'src/cargo/core/compiler/experimental_command_data.rs';assert not f.exists();f.write_text(r'''//! Static Cargo command DATA only. No unit is compiled or executed.
use super::*;
pub(crate) fn capture(bcx: &BuildContext<'_, '_>, root: &Path) -> CargoResult<()> {
    let mut runner = BuildRunner::new(bcx)?;
    runner.lto = lto::generate(bcx)?;
    runner.prepare_units()?;
    runner.prepare()?;
    let mut units: Vec<_> = bcx.unit_graph.iter().collect();
    units.sort_unstable();
    let mut unavailable: HashSet<&Unit> = HashSet::new();
    for (unit, _) in &units {
        let t = serde_json::to_value(&unit.target)?;
        let supported = (t["kind"] == serde_json::json!(["lib"]) && (t["crate_types"] == serde_json::json!(["lib"]) || t["crate_types"] == serde_json::json!(["rlib"]))) || (t["kind"] == serde_json::json!(["bin"]) && t["crate_types"] == serde_json::json!(["bin"]));
        if !supported || !unit.mode.is_check() { unavailable.insert(*unit); }
    }
    loop {
        let mut changed = false;
        for (unit, deps) in &units {
            if deps.iter().any(|dep| unavailable.contains(&dep.unit)) { changed |= unavailable.insert(*unit); }
        }
        if !changed { break; }
    }
    let mut rows = Vec::new();
    for (index, (unit, _)) in units.iter().enumerate() {
        let mut row = serde_json::json!({"index":index,"packageId":unit.pkg.package_id().to_spec(),"target":unit.target,"profile":unit.profile,"platform":unit.kind,"mode":unit.mode,"features":unit.features,"staticCargoCommandConstructed":false,"compilerLaunched":false,"completeRuntimeCommand":false});
        if unavailable.contains(unit) {
            row["standing"] = serde_json::json!("expansion-or-target-context-unavailable");
        } else {
            let command = super::prepare_rustc(&runner, unit)?;
            let args = command.get_args().map(|s| s.to_str().map(str::to_owned).ok_or_else(|| anyhow::anyhow!("non UTF8 static command DATA"))).collect::<CargoResult<Vec<_>>>()?;
            let mut env = std::collections::BTreeMap::new(); let mut removed = Vec::new();
            for (name, value) in command.get_envs() {
                match value { Some(v) => { env.insert(name.clone(), v.to_str().ok_or_else(|| anyhow::anyhow!("non UTF8 static environment DATA"))?.to_owned()); }, None => removed.push(name.clone()) }
            }
            row["standing"] = serde_json::json!("actual-static-cargo-command-data");
            row["staticCargoCommandConstructed"] = serde_json::json!(true);
            row["arguments"] = serde_json::json!(args);
            row["constructedEnvironment"] = serde_json::json!(env);
            row["removedEnvironmentKeys"] = serde_json::json!(removed);
            row["cwd"] = serde_json::json!(command.get_cwd());
            row["primaryPackageByActualCargo"] = serde_json::json!(runner.is_primary_package(unit));
        }
        rows.push(row);
    }
    std::fs::write(root.join("unit-command-data.json"), serde_json::to_vec_pretty(&serde_json::json!({"version":1,"standing":"EXPERIMENTAL ACTUAL STATIC CARGO COMMAND DATA; NO UNIT EXECUTION OR NATIVE ADMISSION","units":rows,"BuildRunnerConstructedForStaticData":true,"BuildRunnerCompileOrDryRunCalled":false,"fixtureOrCorpusCodeExecuted":false,"completeRuntimeCommand":false,"fullCargoProfileEnvironment":false,"nativeAdmission":false}))?)?;
    Ok(())
}
''')
f=p/'src/cargo/util/context/mod.rs';f.write_text(f.read_text()+'\n#[cfg(test)]\nmod experimental_command_data;\n')
s=(p/'src/cargo/util/context/experimental_unit_context.rs').read_text().replace('capture_experimental_unit_context','capture_experimental_command_data')
s+=r'''
#[test]
fn command_data_actual_primary_profile_and_feature_arguments() {
    let root = retained_root(); let project = root.join("project");
    write(&project,"Cargo.toml","[package]\nname='command-profile'\nversion='2.3.4'\nedition='2024'\n[features]\ndefault=['chosen']\nchosen=[]\n[profile.dev]\nopt-level=1\ndebug=0\ndebug-assertions=true\noverflow-checks=false\n");
    let original=b"compile_error!(\"fixture must not compile\");\n";write(&project,"src/lib.rs",std::str::from_utf8(original).unwrap());
    let observation=root.join("observation");std::fs::create_dir(&observation).unwrap();graph(&observation,&project,HashMap::new(),false).unwrap();
    let data:serde_json::Value=serde_json::from_slice(&std::fs::read(observation.join("unit-command-data.json")).unwrap()).unwrap();let row=&data["units"][0];let args=row["arguments"].as_array().unwrap();
    assert_eq!(row["staticCargoCommandConstructed"],true);assert_eq!(row["primaryPackageByActualCargo"],true);assert_eq!(row["constructedEnvironment"]["CARGO_PRIMARY_PACKAGE"],"1");
    assert!(args.windows(2).any(|p|p[0]=="-C"&&p[1]=="opt-level=1"));assert!(args.windows(2).any(|p|p[0]=="-C"&&p[1]=="overflow-checks=off"));
    assert!(args.iter().any(|a|a=="--check-cfg"));assert!(args.iter().any(|a|a=="feature=\"chosen\""));
    let out=args.windows(2).find(|p|p[0]=="--out-dir").unwrap()[1].as_str().unwrap();assert!(Path::new(out).starts_with(&observation));
    assert_eq!(std::fs::read(project.join("src/lib.rs")).unwrap(),original);assert_eq!(data["BuildRunnerCompileOrDryRunCalled"],false);
    eprintln!("ACTUAL_COMMAND_DATA_CONTROL={}",root.display());
}
#[test]
fn command_data_actual_renamed_dependency_arguments() {
    let root=retained_root();let project=root.join("project");write(&project,"Cargo.toml","[package]\nname='command-app'\nversion='1.0.0'\nedition='2024'\n[dependencies]\nrenamed={package='command-dependency',path='dep'}\n");write(&project,"dep/Cargo.toml","[package]\nname='command-dependency'\nversion='4.5.6'\nedition='2024'\n");for name in ["src/lib.rs","dep/src/lib.rs"]{write(&project,name,"compile_error!(\"not compiled\");\n");}
    let observation=root.join("observation");std::fs::create_dir(&observation).unwrap();graph(&observation,&project,HashMap::new(),false).unwrap();let data:serde_json::Value=serde_json::from_slice(&std::fs::read(observation.join("unit-command-data.json")).unwrap()).unwrap();let rows=data["units"].as_array().unwrap();assert_eq!(rows.len(),2);
    let app=rows.iter().find(|r|r["constructedEnvironment"]["CARGO_PKG_NAME"]=="command-app").unwrap();let dep=rows.iter().find(|r|r["constructedEnvironment"]["CARGO_PKG_NAME"]=="command-dependency").unwrap();assert_eq!(app["primaryPackageByActualCargo"],true);assert_eq!(dep["primaryPackageByActualCargo"],false);assert!(dep["constructedEnvironment"].get("CARGO_PRIMARY_PACKAGE").is_none());
    assert!(app["arguments"].as_array().unwrap().windows(2).any(|p|p[0]=="--extern"&&p[1].as_str().unwrap().starts_with("renamed=")));eprintln!("ACTUAL_COMMAND_DATA_CONTROL={}",root.display());
}
#[test]
fn command_data_script_macro_consumers_unavailable_without_execution() {
    let root=retained_root();let project=root.join("project");write(&project,"Cargo.toml","[package]\nname='command-blocked'\nversion='1.0.0'\nedition='2024'\n[dependencies]\nmacrodep={path='macrodep'}\n");write(&project,"macrodep/Cargo.toml","[package]\nname='macrodep'\nversion='1.0.0'\nedition='2024'\n[lib]\nproc-macro=true\n");for name in ["src/lib.rs","macrodep/src/lib.rs","build.rs"]{write(&project,name,"compile_error!(\"not compiled or executed\");\n");}
    let observation=root.join("observation");std::fs::create_dir(&observation).unwrap();graph(&observation,&project,HashMap::new(),false).unwrap();let data:serde_json::Value=serde_json::from_slice(&std::fs::read(observation.join("unit-command-data.json")).unwrap()).unwrap();assert!(data["units"].as_array().unwrap().len()>2);assert!(data["units"].as_array().unwrap().iter().all(|r|r["staticCargoCommandConstructed"]==false));assert_eq!(data["fixtureOrCorpusCodeExecuted"],false);eprintln!("ACTUAL_COMMAND_DATA_CONTROL={}",root.display());
}
'''
f=p/'src/cargo/util/context/experimental_command_data.rs';assert not f.exists();f.write_text(s)
print('New isolated actual static-command DATA authoring complete; no tests or corpus execution yet.')
