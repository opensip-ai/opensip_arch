from pathlib import Path
import os,json,hashlib,shutil
B=Path('/tmp/opensip-implementation/native-config-merge-data-2026-10-10');BASE=Path('/tmp/opensip-implementation/native-cargo-profile-source-2026-10-09/resolver-data-producer');W=B/'producer';A=Path('/Users/sb/code/opensip-ai/opensip_arch')
assert not B.exists();B.mkdir()
for rel in ['src/cargo/util/context/mod.rs','src/cargo/util/context/resolver_projection_data.rs']:
 assert (BASE/rel).read_bytes()==(A/'docs/implementation/m3/native-profile/resolver-data-r1/producer-source'/rel).read_bytes()
assert (BASE/'src/cargo/util/context/sealed_config_data_tests.rs').read_bytes()==(A/'docs/implementation/m3/native-profile/config-data-initializer-r1/producer-source/src/cargo/util/context/sealed_config_data_tests.rs').read_bytes()
shutil.copytree(BASE,W,symlinks=True,ignore=shutil.ignore_patterns('.git','target'))
rel='src/cargo/util/context/mod.rs';p=W/rel;s=p.read_text();assert 'mod config_merge_data;'not in s;s+='\n// Supplied original config merge data; no source/provenance admission.\n#[allow(dead_code)]\nmod config_merge_data;\n';p.write_text(s)
source='''//! Pinned Cargo parsing/merge over supplied bytes and Definition data.
//! No file discovery/read, include policy, original custody, projection or grant.
use super::{ConfigValue, Definition};
use std::collections::HashMap;

pub(super) struct ConfigInputData {
    pub(super) bytes: Vec<u8>,
    pub(super) definition: Definition,
}

#[derive(Debug)]
pub(super) enum MergeDataPhase {
    Utf8,
    Toml,
    CargoValue,
    Merge,
}

#[derive(Debug)]
pub(super) struct MergeDataRefusal {
    pub(super) input_index: usize,
    pub(super) phase: MergeDataPhase,
    pub(super) cause: String,
}

pub(super) struct MergedConfigData<'a> {
    /// All original supplied bytes/definitions remain borrowed, not admitted.
    pub(super) inputs: &'a [ConfigInputData],
    /// Pinned ConfigValue preserves the definition on each scalar/list item.
    pub(super) value: ConfigValue,
}

/// Process every successful supplied input in its provided discovery order.
/// Full UTF8/TOML/Cargo conversion precedes merge, with force=false. Use the
/// whole table so pinned non-mergeable list keys retain their exact treatment.
/// No filename sort, nearest-wins list rule, filtering before parse, definition
/// replacement or normalization. Input order/completeness and every definition
/// are caller data; actual original discovery/custody remains an external duty.
/// Parsing/work/storage pricing, public failure ordering, complete key accounting,
/// deterministic projected serialization and actual initializer use are not here.
pub(super) fn merge_config_inputs_data(
    inputs: &[ConfigInputData],
) -> Result<MergedConfigData<'_>, MergeDataRefusal> {
    let mut merged = ConfigValue::Table(HashMap::new(), Definition::BuiltIn);
    for (input_index, input) in inputs.iter().enumerate() {
        let text = std::str::from_utf8(&input.bytes).map_err(|e| MergeDataRefusal {
            input_index, phase: MergeDataPhase::Utf8, cause: e.to_string(),
        })?;
        let parsed = text.parse::<toml::Value>().map_err(|e| MergeDataRefusal {
            input_index, phase: MergeDataPhase::Toml, cause: e.to_string(),
        })?;
        let value = ConfigValue::from_toml(input.definition.clone(), parsed).map_err(|e| MergeDataRefusal {
            input_index, phase: MergeDataPhase::CargoValue, cause: format!("{e:#}"),
        })?;
        merged.merge(value, false).map_err(|e| MergeDataRefusal {
            input_index, phase: MergeDataPhase::Merge, cause: format!("{e:#}"),
        })?;
    }
    Ok(MergedConfigData { inputs, value: merged })
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::path::{Path, PathBuf};
    fn file(path: &str, text: &str) -> ConfigInputData {
        ConfigInputData { bytes: text.as_bytes().to_vec(), definition: Definition::Path(PathBuf::from(path)) }
    }
    fn member<'a>(value: &'a ConfigValue, name: &str) -> &'a ConfigValue {
        &value.table().unwrap().0[name]
    }
    fn text(value: &ConfigValue) -> &str { value.string("data").unwrap().0 }
    fn root(value: &ConfigValue) -> &Path { value.definition().root(Path::new("/unadmitted/cwd")) }
    fn items(value: &ConfigValue) -> &[ConfigValue] {
        let ConfigValue::List(values, _) = value else { panic!("expected list") }; values
    }
    #[test]
    fn config_merge_data_nearest_primitive_ancestor_list_each_original_root() {
        let input = [file("/unadmitted/z/near/.cargo/config.toml", "[build]\nlabel='near'\nrustflags=['near','same']\n"), file("/unadmitted/a/ancestor/.cargo/config.toml", "[build]\nlabel='ancestor'\nrustflags=['ancestor','same']\n")];
        let merged = merge_config_inputs_data(&input).unwrap();
        let build = member(&merged.value, "build");
        assert_eq!(text(member(build,"label")),"near");
        assert_eq!(root(member(build,"label")),Path::new("/unadmitted/z/near"));
        let list=items(member(build,"rustflags"));
        assert_eq!(list.iter().map(text).collect::<Vec<_>>(),["ancestor","same","near","same"]);
        assert_eq!(root(&list[0]),Path::new("/unadmitted/a/ancestor"));
        assert_eq!(root(&list[3]),Path::new("/unadmitted/z/near"));
        assert!(std::ptr::eq(merged.inputs,&input[..]));
    }
    #[test]
    fn config_merge_data_path_definition_equality_is_not_origin_equality() {
        let a=file("/unadmitted/a/.cargo/config.toml","a='same'");
        let b=file("/unadmitted/b/.cargo/config.toml","a='same'");
        assert_eq!(a.definition,b.definition); // Upstream equality compares the kind only.
        assert_ne!(a.definition.root(Path::new("/x")),b.definition.root(Path::new("/x")));
    }
    #[test]
    fn config_merge_data_order_preserved_not_lexical_filename_order() {
        let input=[file("/unadmitted/z/.cargo/config.toml","x='first'"),file("/unadmitted/a/.cargo/config.toml","x='second'")];
        assert_eq!(text(member(&merge_config_inputs_data(&input).unwrap().value,"x")),"first");
        let reversed=[file("/unadmitted/a/.cargo/config.toml","x='second'"),file("/unadmitted/z/.cargo/config.toml","x='first'")];
        assert_eq!(text(member(&merge_config_inputs_data(&reversed).unwrap().value,"x")),"second");
    }
    #[test]
    fn config_merge_data_recursive_tables_keep_distinct_original_definitions() {
        let input=[file("/unadmitted/a/.cargo/config.toml","[target.custom]\na='one'"),file("/unadmitted/b/.cargo/config.toml","[target.custom]\nb='two'")];
        let result=merge_config_inputs_data(&input).unwrap();let table=member(member(&result.value,"target"),"custom");
        assert_eq!(root(member(table,"a")),Path::new("/unadmitted/a"));assert_eq!(root(member(table,"b")),Path::new("/unadmitted/b"));
    }
    #[test]
    fn config_merge_data_nonmergeable_program_list_uses_pinned_whole_key_rule() {
        let input=[file("/unadmitted/a/.cargo/config.toml","[target.custom]\nrunner=['first','arg']"),file("/unadmitted/b/.cargo/config.toml","[target.custom]\nrunner=['second','other']")];
        let merged=merge_config_inputs_data(&input).unwrap();let runner=member(member(member(&merged.value,"target"),"custom"),"runner");
        assert_eq!(items(runner).iter().map(text).collect::<Vec<_>>(),["first","arg"]);
    }
    #[test]
    fn config_merge_data_container_scalar_conflicts_keep_failure_input_index() {
        for second in ["x=[]","[x]\na='v'"] {
            let input=[file("/unadmitted/a/.cargo/config.toml","x='v'"),file("/unadmitted/b/.cargo/config.toml",second)];
            let e=merge_config_inputs_data(&input).err().unwrap();assert_eq!(e.input_index,1);assert!(matches!(e.phase,MergeDataPhase::Merge));assert!(!e.cause.is_empty());assert_eq!(input[1].bytes,second.as_bytes());
        }
    }
    #[test]
    fn config_merge_data_invalid_utf8_is_not_filtered_or_replaced() {
        let input=[ConfigInputData {bytes:vec![0xff],definition:Definition::BuiltIn}];
        let e=merge_config_inputs_data(&input).err().unwrap();assert!(matches!(e.phase,MergeDataPhase::Utf8));assert_eq!(input[0].bytes,[0xff]);
    }
    #[test]
    fn config_merge_data_malformed_unknown_key_toml_fails_before_any_stripping() {
        let input=[file("/unadmitted/a/.cargo/config.toml","[unselected]\nvalue=[")];
        let e=merge_config_inputs_data(&input).err().unwrap();assert!(matches!(e.phase,MergeDataPhase::Toml));
    }
    #[test]
    fn config_merge_data_cargo_unsupported_float_in_unknown_key_refuses() {
        let input=[file("/unadmitted/a/.cargo/config.toml","[unselected]\nvalue=1.5")];
        let e=merge_config_inputs_data(&input).err().unwrap();assert!(matches!(e.phase,MergeDataPhase::CargoValue));
    }
    #[test]
    fn config_merge_data_include_and_lockpath_retained_as_data_no_read_policy() {
        let input=[file("/unadmitted/a/.cargo/config.toml","include=['/unadmitted/nonexistent/include.toml']\n[resolver]\nlockfile-path='/unadmitted/nonexistent/Cargo.lock'")];
        let merged=merge_config_inputs_data(&input).unwrap();assert_eq!(text(&items(member(&merged.value,"include"))[0]),"/unadmitted/nonexistent/include.toml");
        assert_eq!(text(member(member(&merged.value,"resolver"),"lockfile-path")),"/unadmitted/nonexistent/Cargo.lock");
    }
    #[test]
    fn config_merge_data_empty_supplied_population_is_only_empty_data() {
        let input=[];let merged=merge_config_inputs_data(&input).unwrap();assert!(merged.inputs.is_empty());assert!(merged.value.table().unwrap().0.is_empty());
    }
    #[test]
    fn config_merge_data_scalar_kind_change_equal_file_priority_keeps_first() {
        let input=[file("/unadmitted/a/.cargo/config.toml","x='original'"),file("/unadmitted/b/.cargo/config.toml","x=17")];
        assert_eq!(text(member(&merge_config_inputs_data(&input).unwrap().value,"x")),"original");
    }
}
'''
(W/'src/cargo/util/context/config_merge_data.rs').write_text(source)
(B/'preparation.json').write_text(json.dumps(dict(unit='NATIVE-CONFIG-MERGE-DATA-SUPPORTING-IMPLEMENTATION-R1',sourceBase=str(BASE),producer=str(W),modifiedFiles=['src/cargo/util/context/mod.rs'],newFiles=['src/cargo/util/context/config_merge_data.rs'],expectedNewControls=12,productCodeUnchanged=True,configurationInputAdmitted=False,originalDefinitionsAdmitted=False,completeProjectionImplemented=False,includeCompatibilitySelected=False,publicFailureRoutesSelected=False,sourceProfilePublished=False,productQualification=False),indent=2)+'\n')
print('new isolated pinned producer merge-data candidate prepared; prior accepted producers unchanged')
