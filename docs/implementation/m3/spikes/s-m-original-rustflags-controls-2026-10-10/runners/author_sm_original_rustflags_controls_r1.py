from pathlib import Path
import hashlib,json,shutil
B=Path('/tmp/opensip-implementation');V=B/'sm-original-rustflags-2026-10-10';p=V/'producer/src/cargo/util/context/experimental_command_data.rs';old=p.read_text();s=old
before='''                    "build" => anyhow::ensure!(
                        rows.keys().all(|k| k == "target-dir"),
                        "original config build selector outside experiment"
                    ),'''
after='''                    "build" => {
                        anyhow::ensure!(rows.keys().all(|k| matches!(k.as_str(), "target-dir" | "rustflags")), "original config build selector outside experiment");
                        if let Some(value) = rows.get("rustflags") {
                            let ConfigValue::List(flags, _) = value else { anyhow::bail!("original build flags data is not a list") };
                            anyhow::ensure!(flags.iter().all(|flag| matches!(flag, ConfigValue::String(f, _) if !f.contains("codegen-backend") && !f.contains("--sysroot") && !f.contains("--extern"))), "original build flags include an operational override");
                        }
                    },'''
assert s.count(before)==1;s=s.replace(before,after)
marker='fn graph(\n';assert s.count(marker)==1
helper='''// Experimental exact query vectors from Cargo-resolved original flag DATA.
// This enumerates subsets of at most the three cfg rows observed in these
// development inputs; Cargo itself still determines which rows match.
fn original_flag_lists(context: &GlobalContext) -> CargoResult<Vec<Vec<String>>> {
    let explicit = context.target_cfg_triple("aarch64-apple-darwin")?.rustflags.map(|v| v.val.into_vec()).unwrap_or_default();
    let build = context.get::<Option<StringList>>("build.rustflags")?.map(|v| v.into_vec()).unwrap_or_default();
    let rows: Vec<_> = context.target_cfgs()?.iter().filter_map(|(_, row)| row.rustflags.as_ref().map(|v| v.val.as_slice())).collect();
    anyhow::ensure!(rows.len() <= 3, "outside observed experiment cfg-row population");
    let mut lists = Vec::new();
    for mask in 0..(1usize << rows.len()) {
        let mut flags = explicit.clone();
        for (i, row) in rows.iter().enumerate() { if mask & (1 << i) != 0 { flags.extend_from_slice(row); } }
        if flags.is_empty() { flags = build.clone(); }
        if !lists.contains(&flags) { lists.push(flags); }
    }
    Ok(lists)
}

'''
s=s.replace(marker,helper+marker)
marker='''    // Resolve actual Cargo CV environment DATA using Cargo's existing reader.
'''
new='''    // Freeze exact original-config query alternatives before any INFO query.
    // No query argument wildcard, registration after output, or compiler wrapper.
    let mut arguments: Vec<Vec<OsString>> = vec![vec!["-vV".into()]];
    arguments.push(head.iter().chain(tail.iter()).map(OsString::from).collect());
    for flags in original_flag_lists(&context)? {
        let vector = head.iter().map(OsString::from)
            .chain(flags.iter().map(OsString::from))
            .chain(["--target", "aarch64-apple-darwin"].iter().map(OsString::from))
            .chain(tail.iter().map(OsString::from)).collect();
        if !arguments.contains(&vector) { arguments.push(vector); }
    }
    context.experimental_rustc = Some(cargo_util::ProcessBuilder::experimental_information_queries(
        Path::new("/Users/sb/code/.opensip-implementation-cache/g2-rust-1.95/sysroot/bin/rustc"), project, arguments,
        "b829b733131d4e1673eeebd1f34d06ae1e9ff4977b051313cf42e2a9e79ecf1c".into(), &queries));
'''+marker
assert s.count(marker)==1;s=s.replace(marker,new)
s+='''
#[test]
fn original_rustflags_build_data_definitions_preserved() {
    let (path, hash) = large_original_fixture("[build]\\nrustflags=['-C','force-frame-pointers=yes','-A','unknown_lints']\\n");
    let got = values_with_original_data(Some((&path, &hash)), &[], true).unwrap();
    let ConfigValue::Table(expected, _) = ConfigValue::from_toml(Definition::Path(path.clone()), toml::from_str(&std::fs::read_to_string(path).unwrap()).unwrap()).unwrap() else { panic!("fixture") };
    assert_eq!(got, expected);
}
#[test]
fn original_rustflags_build_operational_override_refused() {
    let (path, hash) = large_original_fixture("[build]\\nrustflags=['--extern=forbidden=/synthetic/forbidden']\\n");
    assert!(values_with_original_data(Some((&path, &hash)), &[], true).is_err());
}
#[test]
fn original_rustflags_build_wrong_type_refused() {
    let (path, hash) = large_original_fixture("[build]\\nrustflags='-A unknown_lints'\\n");
    assert!(values_with_original_data(Some((&path, &hash)), &[], true).is_err());
}
fn original_rustflags_graph_fixture(text: &str, expected: &[&str], success: bool) {
    let root = retained_root(); let project = root.join("project");
    write(&project,"Cargo.toml","[package]\\nname='original-rustflags'\\nversion='1.0.0'\\nedition='2024'\\n");
    write(&project,"src/lib.rs","compile_error!(\\"fixture source must not execute\\");\\n");
    write(&project,".cargo/config.toml",text);
    let path = project.join(".cargo/config.toml"); let raw = std::fs::read(&path).unwrap();
    let mut h = cargo_util::Sha256::new(); h.update(&raw); let hash = h.finish_hex();
    let values = values_with_original_data(Some((&path,&hash)), &[], true).unwrap();
    let observation = root.join("observation"); std::fs::create_dir(&observation).unwrap();
    let outcome = graph(&observation,&project,values,false);
    assert_eq!(outcome.is_ok(), success, "{:?}",outcome);
    if success {
        let data: serde_json::Value = serde_json::from_slice(&std::fs::read(observation.join("unit-command-data.json")).unwrap()).unwrap();
        let units = data["units"].as_array().unwrap(); assert_eq!(units.len(),1);
        let args: Vec<_> = units[0]["arguments"].as_array().unwrap().iter().map(|v|v.as_str().unwrap()).collect();
        for value in expected { assert!(args.contains(value),"missing original flag {}",value); }
    }
    assert_eq!(std::fs::read(&path).unwrap(),raw);
    assert!(!project.join("target").exists());
    std::fs::write(root.join("control.json"),serde_json::to_vec_pretty(&serde_json::json!({"root":root,"graphSuccess":success,"error":outcome.err().map(|e|format!("{e:#}")),"originalConfigurationPin":hash,"originalConfigurationPreserved":true,"fixtureSourcesExecuted":false,"nativeAdmission":false,"SMComplete":false})).unwrap()).unwrap();
    eprintln!("ACTUAL_ORIGINAL_RUSTFLAGS_CONTROL={}",root.display());
}
#[test]
fn original_rustflags_actual_build_flags_graph() {
    original_rustflags_graph_fixture("[build]\\nrustflags=['-C','force-frame-pointers=yes','-C','force-unwind-tables=yes','-A','unknown_lints','-A','mismatched_lifetime_syntaxes']\\n", &["force-frame-pointers=yes","force-unwind-tables=yes","mismatched_lifetime_syntaxes"],true);
}
#[test]
fn original_rustflags_actual_cfg_fixed_point_graph() {
    original_rustflags_graph_fixture("[target.'cfg(all())']\\nrustflags=['--cfg','tokio_unstable','-A','clippy::all']\\n", &["tokio_unstable","clippy::all"],true);
}
#[test]
fn original_rustflags_actual_explicit_and_cfg_graph() {
    original_rustflags_graph_fixture("[target.aarch64-apple-darwin]\\nrustflags=['-C','force-frame-pointers=yes']\\n[target.'cfg(all())']\\nrustflags=['--cfg','tokio_unstable']\\n", &["force-frame-pointers=yes","tokio_unstable"],true);
}
#[test]
fn original_rustflags_actual_nightly_flags_remain_refused() {
    original_rustflags_graph_fixture("[target.'cfg(all())']\\nrustflags=['-Zshare-generics=y']\\n", &[],false);
}
'''
p.write_text(s)
(V/'authoring-r1.json').write_text(json.dumps(dict(standing='NEW ISOLATED ORIGINAL RUSTFLAGS DATA CONTROLS; UNREVIEWED; NO ACTUAL CORPUS USE',changedSourceFile=str(p),beforeSha256=hashlib.sha256(old.encode()).hexdigest(),afterSha256=hashlib.sha256(s.encode()).hexdigest(),newControls=7,actualCorpusUse=False,nativeAdmission=False,SMComplete=False),indent=2)+'\n')
C=Path('/Users/sb/code/.opensip-implementation-cache/control-2026-10-06/continuation-preserved/original-rustflags-authoring-r1');C.mkdir();shutil.copyfile(p,C/p.name);shutil.copyfile(Path(__file__),C/Path(__file__).name);shutil.copyfile(V/'authoring-r1.json',C/'authoring-r1.json');print('Authored seven new original-rustflags controls in isolated candidate only.')
