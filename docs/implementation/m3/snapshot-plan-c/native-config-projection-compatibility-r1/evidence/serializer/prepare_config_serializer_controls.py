from pathlib import Path
import json,shutil
B=Path('/tmp/opensip-implementation');K=B/'native-config-serializer-controls-2026-10-10';W=K/'producer';BASE=B/'native-config-merge-data-2026-10-10/producer'
assert not K.exists();K.mkdir();shutil.copytree(BASE,W,symlinks=True)
p=W/'src/cargo/util/context/mod.rs';p.write_bytes(p.read_bytes()+b'\n#[cfg(test)]\nmod config_serializer_controls;\n')
(W/'src/cargo/util/context/config_serializer_controls.rs').write_text(r'''//! Prospective serializer artifact controls, not complete native projection.
//! Test-only algorithm. No reads, admission, initializer or production caller.
use super::{ConfigValue as CV, Definition};
use std::collections::HashMap;
use std::path::{Path, PathBuf};

fn sorted_toml(v: &CV) -> toml::Value {
    match v {
        CV::Integer(n, _) => toml::Value::Integer(*n),
        CV::String(s, _) => toml::Value::String(s.clone()),
        CV::Boolean(b, _) => toml::Value::Boolean(*b),
        CV::List(v, _) => toml::Value::Array(v.iter().map(sorted_toml).collect()),
        CV::Table(t, _) => {
            let mut keys: Vec<_> = t.keys().collect();
            keys.sort();
            let mut out = toml::map::Map::new();
            for key in keys { out.insert(key.clone(), sorted_toml(&t[key])); }
            toml::Value::Table(out)
        }
    }
}
struct SerializedData<'a> { source: &'a CV, bytes: String }
fn serialize_data(v: &CV) -> Result<SerializedData<'_>, String> {
    if !matches!(v, CV::Table(..)) { return Err("document root must be a table".into()); }
    let bytes=toml::to_string(&sorted_toml(v)).map_err(|e|e.to_string())?;
    Ok(SerializedData {source:v,bytes})
}
fn input(s: &str, path: &str) -> CV {
    let v=toml::from_str::<toml::Value>(s).unwrap();
    CV::from_toml(Definition::Path(PathBuf::from(path)),v).unwrap()
}
fn semantic_roundtrip(v: &CV) -> SerializedData<'_> {
    let out=serialize_data(v).unwrap();
    let parsed=toml::from_str::<toml::Value>(&out.bytes).unwrap();
    assert_eq!(parsed,sorted_toml(v));
    assert!(std::ptr::eq(out.source,v)); out
}
#[test]
fn config_serializer_controls_fixed_scalar_golden_and_final_newline() {
    let v=input("zzz=true\naaa=1\n", "/unadmitted/original/.cargo/config.toml");
    assert_eq!(semantic_roundtrip(&v).bytes,"aaa = 1\nzzz = true\n");
}
#[test]
fn config_serializer_controls_empty_document_exact_empty_bytes() {
    let v=input("", "/unadmitted/empty/.cargo/config.toml");
    assert_eq!(semantic_roundtrip(&v).bytes.as_bytes(),b"");
}
#[test]
fn config_serializer_controls_list_order_and_repeats_exact_golden() {
    let v=input("flags=['z','same','a','same']", "/unadmitted/list/.cargo/config.toml");
    assert_eq!(semantic_roundtrip(&v).bytes,"flags = [\"z\", \"same\", \"a\", \"same\"]\n");
}
#[test]
fn config_serializer_controls_all_six_input_orders_and_nested_order() {
    let orders=[[0,1,2],[0,2,1],[1,0,2],[1,2,0],[2,0,1],[2,1,0]];
    let names=["z","a","m"];let mut expected=None;
    for outer in orders { for inner in orders {
        let mut root=HashMap::new();
        for i in outer { let mut table=HashMap::new(); for j in inner {
            table.insert(names[j].to_string(),CV::Integer(j as i64,Definition::BuiltIn));
        } root.insert(names[i].to_string(),CV::Table(table,Definition::BuiltIn)); }
        let cv=CV::Table(root,Definition::BuiltIn);let out=semantic_roundtrip(&cv);
        if let Some(ref bytes)=expected { assert_eq!(&out.bytes,bytes); }
        else { expected=Some(out.bytes); }
    }}
    assert_eq!(expected.unwrap(),"[a]\na = 1\nm = 2\nz = 0\n\n[m]\na = 1\nm = 2\nz = 0\n\n[z]\na = 1\nm = 2\nz = 0\n");
}
#[test]
fn config_serializer_controls_unicode_quoted_keys_controls_and_escapes() {
    let mut root=HashMap::new();
    let value="nul:\0 newline:\n tab:\t quote:\" slash:\\ é🚀";
    for key in ["dot.key","","quote\"key","é🚀","tab\tkey"] {
        root.insert(key.to_string(),CV::String(value.into(),Definition::BuiltIn));
    }
    let cv=CV::Table(root,Definition::BuiltIn);let out=semantic_roundtrip(&cv);
    assert!(!out.bytes.as_bytes().contains(&0));
    assert!(!out.bytes.contains("/unadmitted"));
}
#[test]
fn config_serializer_controls_exact_integer_extremes_and_boolean_types() {
    let v=input("minimum=-9223372036854775808\nmaximum=9223372036854775807\nyes=true\nno=false", "/unadmitted/integers/.cargo/config.toml");
    assert_eq!(semantic_roundtrip(&v).bytes,"maximum = 9223372036854775807\nminimum = -9223372036854775808\nno = false\nyes = true\n");
}
#[test]
fn config_serializer_controls_nested_arrays_empty_tables_and_mixed_values() {
    let v=input("empty=[]\nmixed=['a',1,true]\nrows=[{ z=1,a='first' },{ a='second',z=2 }]\n[table.empty]\n[table.nested]\nitems=[['x','x'],['z']]", "/unadmitted/nested/.cargo/config.toml");
    semantic_roundtrip(&v);
}
#[test]
fn config_serializer_controls_definition_roots_borrowed_not_semantic_bytes() {
    let a=input("[build]\nrustflags=['near','same']", "/unadmitted/a/.cargo/config.toml");
    let b=input("[build]\nrustflags=['near','same']", "/unadmitted/b/.cargo/config.toml");
    let sa=semantic_roundtrip(&a);let sb=semantic_roundtrip(&b);assert_eq!(sa.bytes,sb.bytes);
    let get=|v:&CV|{let CV::Table(t,_)=v else {panic!()};let CV::Table(t,_)=&t["build"]else{panic!()};let CV::List(v,_)=&t["rustflags"]else{panic!()};v[0].definition().root(Path::new("/unadmitted/cwd")).to_path_buf()};
    assert_eq!(get(sa.source),Path::new("/unadmitted/a"));assert_eq!(get(sb.source),Path::new("/unadmitted/b"));
}
#[test]
fn config_serializer_controls_scalar_list_roots_refuse_no_document() {
    for v in [CV::String("x".into(),Definition::BuiltIn),CV::Integer(1,Definition::BuiltIn),CV::Boolean(false,Definition::BuiltIn),CV::List(vec![],Definition::BuiltIn)] {
        assert!(serialize_data(&v).is_err());
    }
}
''')
(K/'preparation.json').write_text(json.dumps(dict(unit='NATIVE-CONFIG-SERIALIZER-ARTIFACT-CONTROLS-R1',baseProducer=str(BASE),standing='UNREVIEWED PROSPECTIVE ARTIFACT CONTROLS; NO PRODUCTION HELPER',expectedControls=9,algorithm='Recursively sort table keys by Rust str Ord; preserve all list items/order/repeats; pinned toml::to_string once; exact returned UTF8 without postprocessing',tomlVersion='0.9.11+spec-1.1.0',tomlFeatures=['std','serde','parse','display','preserve_order'],sourceDefinitionsBorrowedNotSerialized=True,numericBoundsUnchanged=True,serializerCompatibilitySelected=False,configurationInputAdmitted=False,completeProjectionImplemented=False,sourceProfilePublished=False,productCodeUnchanged=True),indent=2)+'\n')
s=(B/'run_config_discovery_controls.py').read_text().replace('native-config-discovery-controls-2026-10-10','native-config-serializer-controls-2026-10-10').replace('config_discovery_controls','config_serializer_controls').replace('discovery-tests','serializer-tests').replace('opensip-config-discovery-','opensip-config-serializer-').replace('expectedControls=8','expectedControls=9');compile(s,'run_serializer','exec');(B/'run_config_serializer_controls.py').write_text(s)
print(str(K))
