from pathlib import Path
import json,hashlib,shutil
B=Path('/tmp/opensip-implementation');V=B/'sm-original-config-hierarchy-2026-10-10';p=V/'producer/src/cargo/util/context/experimental_command_data.rs';old=p.read_text();s=old
marker='fn original_flag_lists(';i=s.index(marker)
helper='''// Experimental original ancestor configuration DATA only; no HOME discovery.
fn original_configuration_hierarchy(project: &Path, member: &Path, configurations: &[(&Path, &str)]) -> CargoResult<HashMap<String, ConfigValue>> {
    anyhow::ensure!(project.is_absolute() && member.is_absolute() && project.starts_with(member) && !configurations.is_empty(), "invalid original hierarchy roots");
    let mut merged = ConfigValue::Table(HashMap::new(), Definition::BuiltIn);
    let mut previous: Option<PathBuf> = None;
    for (path, hash) in configurations {
        anyhow::ensure!(path.is_absolute() && matches!(path.file_name().and_then(|s|s.to_str()),Some("config" | "config.toml")), "invalid original config filename");
        let cargo = path.parent().ok_or_else(|| anyhow::anyhow!("missing config parent"))?;
        anyhow::ensure!(cargo.file_name().is_some_and(|s|s==".cargo"), "not an original .cargo configuration");
        let ancestor = cargo.parent().ok_or_else(|| anyhow::anyhow!("missing original ancestor"))?;
        anyhow::ensure!(project.starts_with(ancestor) && ancestor.starts_with(member), "configuration outside original member ancestry");
        if let Some(ref closer) = previous { anyhow::ensure!(closer != ancestor && closer.starts_with(ancestor), "configuration hierarchy not strict closest-first"); }
        previous = Some(ancestor.to_path_buf());
        let values = values_with_original_data(Some((path,hash)),&[],true)?;
        merged.merge(ConfigValue::Table(values,Definition::Path(path.to_path_buf())),false)?;
    }
    let ConfigValue::Table(values, _) = merged else { unreachable!() };
    Ok(values)
}

'''
s=s[:i]+helper+s[i:]
oldline='''    let projected = values_with_original_data(config, &links, preserve_original_data).unwrap();'''
newline='''    let projected = if let Some(hierarchy) = packet.get("configurationHierarchy") {
        assert!(preserve_original_data && config.is_none() && links.is_empty());
        let configurations: Vec<_> = hierarchy.as_array().unwrap().iter().map(|v| (Path::new(v["path"].as_str().unwrap()),v["sha256"].as_str().unwrap())).collect();
        original_configuration_hierarchy(&project,&member,&configurations).unwrap()
    } else { values_with_original_data(config, &links, preserve_original_data).unwrap() };'''
assert s.count(oldline)==1;s=s.replace(oldline,newline)
s+='''
fn original_hierarchy_fixture(outer: &str, inner: &str) -> (PathBuf, PathBuf, PathBuf, String, PathBuf, String) {
    let root=retained_root(); let project=root.join("nested"); std::fs::create_dir(&project).unwrap();
    write(&root,".cargo/config.toml",outer);write(&project,".cargo/config.toml",inner);
    let a=root.join(".cargo/config.toml");let b=project.join(".cargo/config.toml");
    let hash=|p:&Path| { let mut h=cargo_util::Sha256::new();h.update(&std::fs::read(p).unwrap());h.finish_hex() };
    let ah=hash(&a);let bh=hash(&b);(root,project,a,ah,b,bh)
}
#[test]
fn original_hierarchy_scalar_nearest_definition_preserved() {
    let (root,project,a,ah,b,bh)=original_hierarchy_fixture("[build]\\ntarget-dir='outer'\\n","[build]\\ntarget-dir='inner'\\n");
    let values=original_configuration_hierarchy(&project,&root,&[(&b,&bh),(&a,&ah)]).unwrap();
    let ConfigValue::Table(build, _)=&values["build"] else {panic!("table")};
    assert_eq!(build["target-dir"],ConfigValue::String("inner".into(),Definition::Path(b)));
}
#[test]
fn original_hierarchy_lists_use_actual_cargo_merge() {
    let (root,project,a,ah,b,bh)=original_hierarchy_fixture("[target.'cfg(all())']\\nrustflags=['--cfg','outer_flag']\\n","[target.'cfg(all())']\\nrustflags=['--cfg','inner_flag']\\n");
    let values=original_configuration_hierarchy(&project,&root,&[(&b,&bh),(&a,&ah)]).unwrap();
    let mut expected=ConfigValue::Table(HashMap::new(),Definition::BuiltIn);
    for path in [&b,&a] {expected.merge(ConfigValue::from_toml(Definition::Path(path.clone()),toml::from_str(&std::fs::read_to_string(path).unwrap()).unwrap()).unwrap(),false).unwrap();}
    let ConfigValue::Table(expected,_)=expected else {panic!("table")};assert_eq!(values,expected);
    let ConfigValue::Table(target, _)=&values["target"] else {panic!("table")};
    let ConfigValue::Table(cfg, _)=&target["cfg(all())"] else {panic!("table")};
    let ConfigValue::List(flags, _)=&cfg["rustflags"] else {panic!("list")};
    let strings:Vec<_>=flags.iter().map(|v| {let ConfigValue::String(s, _)=v else {panic!("string")};s.as_str()}).collect();
    assert_eq!(strings,vec!["--cfg","outer_flag","--cfg","inner_flag"]);
}
#[test]
fn original_hierarchy_each_hash_checked() {
    let (root,project,a,ah,b,bh)=original_hierarchy_fixture("[build]\\ntarget-dir='outer'\\n","[build]\\ntarget-dir='inner'\\n");
    assert!(original_configuration_hierarchy(&project,&root,&[(&b,&bh),(&a,&"0".repeat(64))]).is_err());
    assert!(original_configuration_hierarchy(&project,&root,&[(&b,&"0".repeat(64)),(&a,&ah)]).is_err());
}
#[test]
fn original_hierarchy_wrong_ancestry_order_and_duplicate_refused() {
    let (root,project,a,ah,b,bh)=original_hierarchy_fixture("[build]\\ntarget-dir='outer'\\n","[build]\\ntarget-dir='inner'\\n");
    assert!(original_configuration_hierarchy(&project,&root,&[(&a,&ah),(&b,&bh)]).is_err());
    assert!(original_configuration_hierarchy(&project,&root,&[(&b,&bh),(&b,&bh)]).is_err());
    assert!(original_configuration_hierarchy(&project,&project,&[(&a,&ah)]).is_err());
    assert!(original_configuration_hierarchy(&project,&root,&[]).is_err());
}
#[test]
fn original_hierarchy_unknown_operational_selector_refused_before_merge() {
    let (root,project,a,ah,b,bh)=original_hierarchy_fixture("[build]\\nrustc='never-run'\\n","[build]\\ntarget-dir='inner'\\n");
    assert!(original_configuration_hierarchy(&project,&root,&[(&b,&bh),(&a,&ah)]).is_err());
}
#[test]
fn original_hierarchy_actual_merged_static_graph() {
    let (root,project,a,ah,b,bh)=original_hierarchy_fixture("[build]\\ntarget-dir='outer-target'\\n[env]\\nCARGO_WORKSPACE_DIR={value='',relative=true}\\n[target.'cfg(all())']\\nrustflags=['--cfg','outer_flag']\\n","[build]\\ntarget-dir='inner-target'\\n[target.'cfg(all())']\\nrustflags=['--cfg','inner_flag']\\n");
    write(&project,"Cargo.toml","[package]\\nname='original-hierarchy'\\nversion='1.0.0'\\nedition='2024'\\n");write(&project,"src/lib.rs","compile_error!(\\"fixture source must not execute\\");\\n");
    let values=original_configuration_hierarchy(&project,&root,&[(&b,&bh),(&a,&ah)]).unwrap();
    let observation=root.join("observation");std::fs::create_dir(&observation).unwrap();graph(&observation,&project,values,false).unwrap();
    let data:serde_json::Value=serde_json::from_slice(&std::fs::read(observation.join("unit-command-data.json")).unwrap()).unwrap();let units=data["units"].as_array().unwrap();assert_eq!(units.len(),1);
    assert_eq!(Path::new(units[0]["constructedEnvironment"]["CARGO_WORKSPACE_DIR"].as_str().unwrap()),root);
    let args=units[0]["arguments"].as_array().unwrap();assert!(args.iter().any(|a|a=="outer_flag") && args.iter().any(|a|a=="inner_flag"));
    assert!(!project.join("inner-target").exists());assert!(!root.join("outer-target").exists());
    for (path,hash) in [(&a,&ah),(&b,&bh)] {let mut h=cargo_util::Sha256::new();h.update(&std::fs::read(path).unwrap());assert_eq!(&h.finish_hex(),hash);}
    std::fs::write(root.join("control.json"),serde_json::to_vec_pretty(&serde_json::json!({"root":root,"actualCargoConfigMerge":true,"originalConfigurationsPreserved":true,"fixtureSourceExecuted":false,"nativeAdmission":false,"SMComplete":false})).unwrap()).unwrap();eprintln!("ACTUAL_ORIGINAL_HIERARCHY_CONTROL={}",root.display());
}
'''
p.write_text(s);(V/'authoring-r1.json').write_text(json.dumps(dict(standing='NEW SEPARATE ORIGINAL CONFIGURATION HIERARCHY DATA CANDIDATE; UNREVIEWED',source=str(p),beforeSha256=hashlib.sha256(old.encode()).hexdigest(),afterSha256=hashlib.sha256(s.encode()).hexdigest(),newControls=6,actualCorpusUse=False,nativeAdmission=False,SMComplete=False),indent=2)+'\n');C=Path('/Users/sb/code/.opensip-implementation-cache/control-2026-10-06/continuation-preserved/original-config-hierarchy-authoring-r1');C.mkdir();shutil.copyfile(p,C/p.name);shutil.copyfile(Path(__file__),C/Path(__file__).name);shutil.copyfile(V/'authoring-r1.json',C/'authoring-r1.json');print('Authored six hierarchy controls in separate candidate using actual Cargo merge.')
