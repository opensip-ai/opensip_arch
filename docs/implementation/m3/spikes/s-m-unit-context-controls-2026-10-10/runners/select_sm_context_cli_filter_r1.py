from pathlib import Path
b=Path('/tmp/opensip-implementation');v=b/'sm-cargo-unit-context-2026-10-10';f=v/'producer/src/cargo/util/context/experimental_unit_context.rs';s=f.read_text();needle='    options.spec = crate::ops::Packages::Default;';assert s.count(needle)==2;s=s.replace(needle,needle+'\n    // Use the same no-selector filter constructor as the pinned Cargo CLI.\n    options.filter = crate::ops::CompileFilter::from_raw_arguments(false, vec![], false, vec![], false, vec![], false, vec![], false, false);',1)
s+='''
#[test]
fn unit_context_default_cli_target_filter_preserves_features() {
    let root=retained_root();let project=root.join("project");
    write(&project,"Cargo.toml","[package]\\nname='feature-filter'\\nversion='1.0.0'\\nedition='2024'\\n[features]\\nextra=[]\\n[[bin]]\\nname='feature-only'\\npath='src/main.rs'\\nrequired-features=['extra']\\n");
    write(&project,"src/lib.rs","compile_error!(\\\"not executed\\\");\\n");
    write(&project,"src/main.rs","compile_error!(\\\"feature-only target must not execute\\\");\\n");
    let observation=root.join("observation");std::fs::create_dir(&observation).unwrap();graph(&observation,&project,HashMap::new(),false).unwrap();
    let data:serde_json::Value=serde_json::from_slice(&std::fs::read(observation.join("unit-context-data.json")).unwrap()).unwrap();
    let graph:serde_json::Value=serde_json::from_slice(&std::fs::read(observation.join("unit-graph.json")).unwrap()).unwrap();
    assert_eq!(graph["units"].as_array().unwrap().len(),1);assert_eq!(graph["roots"].as_array().unwrap().len(),1);assert_eq!(graph["units"][0]["target"]["kind"],serde_json::json!(["lib"]));assert_eq!(graph["units"][0]["features"],serde_json::json!([]));assert_eq!(data["units"][0]["target"],graph["units"][0]["target"]);
    eprintln!("ACTUAL_UNIT_CONTEXT_CONTROL={}",root.display());
}
''';f.write_text(s)
s=(b/'run_sm_unit_context_checks_r3.py').read_text().replace('unit-context-controls-r3.log','unit-context-controls-r4.log').replace('unit-context-checks-r3.json','unit-context-checks-r4.json');(b/'run_sm_unit_context_checks_r4.py').write_text(s)
