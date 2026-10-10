from pathlib import Path
import shutil,json
B=Path('/tmp/opensip-implementation');K=B/'native-config-pipeline-data-2026-10-10';W=K/'producer';BASE=B/'native-config-merge-data-2026-10-10/producer'
assert not K.exists();K.mkdir();shutil.copytree(BASE,W,symlinks=True)
p=W/'src/cargo/util/context/mod.rs';p.write_bytes(p.read_bytes()+b'\n#[allow(dead_code)]\nmod config_pipeline_data;\n')
(W/'src/cargo/util/context/config_pipeline_data.rs').write_text(r'''//! Merge-to-resolver-to-initializer supplied DATA only. No discovery/admission.
use super::{ConfigValue, Definition};
use std::collections::HashMap;

#[derive(Debug)]
pub(super) enum ResolverMergedRefusal<'a> {
    NonTable(&'a ConfigValue),
    InvalidLeaf(&'a ConfigValue),
}
pub(super) struct ResolverMergedData<'a> {
    pub(super) original_namespace: Option<&'a ConfigValue>,
    pub(super) honored_leaf: Option<ConfigValue>,
    /// Complete borrowed subtrees, not final public key accounting.
    pub(super) stripped_members: Vec<(&'a str, &'a ConfigValue)>,
}
pub(super) fn resolver_merged_data(
    namespace: Option<&ConfigValue>,
) -> Result<ResolverMergedData<'_>, ResolverMergedRefusal<'_>> {
    let mut out = ResolverMergedData {
        original_namespace: namespace,
        honored_leaf: None,
        stripped_members: Vec::new(),
    };
    let Some(original) = namespace else { return Ok(out); };
    let ConfigValue::Table(table, _) = original else {
        return Err(ResolverMergedRefusal::NonTable(original));
    };
    for (key, value) in table {
        if key == "incompatible-rust-versions" {
            let ConfigValue::String(text, _) = value else {
                return Err(ResolverMergedRefusal::InvalidLeaf(value));
            };
            if text != "allow" && text != "fallback" {
                return Err(ResolverMergedRefusal::InvalidLeaf(value));
            }
            // Clone exact effective value including its own supplied Definition.
            out.honored_leaf = Some(value.clone());
        } else {
            out.stripped_members.push((key.as_str(), value));
        }
    }
    Ok(out)
}
/// Only a resolver-only supplied data map for conditional constructor controls.
/// BuiltIn marks the synthetic container; the effective leaf keeps its definition.
/// This is not full projected config, original provenance admission or key account.
pub(super) fn resolver_only_initializer_data(
    data: &ResolverMergedData<'_>,
) -> HashMap<String, ConfigValue> {
    match &data.honored_leaf {
        None => HashMap::new(),
        Some(leaf) => HashMap::from([("resolver".into(), ConfigValue::Table(
            HashMap::from([("incompatible-rust-versions".into(), leaf.clone())]),
            Definition::BuiltIn,
        ))]),
    }
}
#[cfg(test)]
mod tests {
    use super::*;
    use super::super::config_merge_data::{ConfigInputData, merge_config_inputs_data};
    use crate::{core::Shell, util::GlobalContext};
    use std::{path::{Path,PathBuf}, sync::atomic::{AtomicUsize,Ordering}};
    static NEXT: AtomicUsize=AtomicUsize::new(0);
    fn input(path: &str, text: &str) -> ConfigInputData {
        ConfigInputData { bytes:text.as_bytes().to_vec(),definition:Definition::Path(PathBuf::from(path)) }
    }
    fn namespace(v:&ConfigValue)->Option<&ConfigValue> { v.table("data").unwrap().0.get("resolver") }
    #[test]
    fn config_pipeline_data_leaf_definition_survives_merge_selection_install() {
        let inputs=[input("/unadmitted/near/.cargo/config.toml","[resolver]\nincompatible-rust-versions='fallback'\n"),input("/unadmitted/far/.cargo/config.toml","[resolver]\nincompatible-rust-versions='allow'\nunknown={nested=['a','a']}\n")];
        let merged=merge_config_inputs_data(&inputs).unwrap();
        let selected=resolver_merged_data(namespace(&merged.value)).unwrap();
        assert_eq!(selected.honored_leaf.as_ref().unwrap().definition().root(Path::new("/cwd")),Path::new("/unadmitted/near"));
        let root=std::env::temp_dir().join(format!("config-pipeline-{}-{}",std::process::id(),NEXT.fetch_add(1,Ordering::Relaxed)));
        std::fs::create_dir(&root).unwrap();let home=root.join("home");std::fs::create_dir(&home).unwrap();std::fs::create_dir(root.join(".cargo")).unwrap();std::fs::write(root.join(".cargo/config.toml"),"[poisoned").unwrap();
        let mut ctx=GlobalContext::new_with_projected_values_data(Shell::new(),root.clone(),home,resolver_only_initializer_data(&selected)).unwrap();
        // Isolates getter controls only; does not undo ordinary constructor captures.
        ctx.set_env(HashMap::new());
        assert_eq!(ctx.get::<String>("resolver.incompatible-rust-versions").unwrap(),"fallback");
        let values=ctx.values().unwrap();let stored=values["resolver"].table("resolver").unwrap().0;
        assert_eq!(stored.len(),1);assert_eq!(stored["incompatible-rust-versions"].definition().root(Path::new("/cwd")),Path::new("/unadmitted/near"));
        assert!(ctx.set_values(HashMap::new()).is_err());assert!(ctx.values_mut().is_err());
        drop(ctx);std::fs::remove_dir_all(root).unwrap();
    }
    #[test]
    fn config_pipeline_data_absent_or_unknown_only_no_synthesis() {
        for text in ["", "[resolver]\nunknown={nested=[1,2]}\n"] {
            let inputs=[input("/unadmitted/.cargo/config.toml",text)];let merged=merge_config_inputs_data(&inputs).unwrap();let selected=resolver_merged_data(namespace(&merged.value)).unwrap();assert!(selected.honored_leaf.is_none());assert!(resolver_only_initializer_data(&selected).is_empty());
        }
    }
    #[test]
    fn config_pipeline_data_invalid_effective_leaf_retains_exact_failure_reference() {
        for text in ["true", "1", "'Allow'", "'fallback '", "[]", "{}"] {
            let inputs=[input("/unadmitted/.cargo/config.toml",&format!("[resolver]\nincompatible-rust-versions={text}\n"))];let merged=merge_config_inputs_data(&inputs).unwrap();let ns=namespace(&merged.value).unwrap();let original=&ns.table("resolver").unwrap().0["incompatible-rust-versions"];
            let Err(ResolverMergedRefusal::InvalidLeaf(failure))=resolver_merged_data(Some(ns)) else { panic!("must refuse") };assert!(std::ptr::eq(failure,original));
        }
    }
    #[test]
    fn config_pipeline_data_non_table_retains_original_reference() {
        let inputs=[input("/unadmitted/.cargo/config.toml","resolver='fallback'")];let merged=merge_config_inputs_data(&inputs).unwrap();let original=namespace(&merged.value).unwrap();let Err(ResolverMergedRefusal::NonTable(failure))=resolver_merged_data(Some(original)) else { panic!("must refuse") };assert!(std::ptr::eq(failure,original));
    }
    #[test]
    fn config_pipeline_data_unknown_subtrees_keep_borrowed_values_and_roots() {
        let inputs=[input("/unadmitted/near/.cargo/config.toml","[resolver]\nincompatible-rust-versions='allow'\nunknown={nested=['a','a']}\n")];let merged=merge_config_inputs_data(&inputs).unwrap();let ns=namespace(&merged.value).unwrap();let selected=resolver_merged_data(Some(ns)).unwrap();assert!(std::ptr::eq(selected.original_namespace.unwrap(),ns));assert_eq!(selected.stripped_members.len(),1);let (key,value)=selected.stripped_members[0];assert_eq!(key,"unknown");assert!(std::ptr::eq(value,&ns.table("resolver").unwrap().0[key]));assert_eq!(value.definition().root(Path::new("/cwd")),Path::new("/unadmitted/near"));
    }
    #[test]
    fn config_pipeline_data_full_merge_failure_precedes_selection() {
        let inputs=[input("/unadmitted/near/.cargo/config.toml","[resolver]\nincompatible-rust-versions='allow'\n"),input("/unadmitted/far/.cargo/config.toml","[ignored]\nfloat=1.5\n")];let Err(refusal)=merge_config_inputs_data(&inputs) else {panic!("full conversion must fail before selection")};assert_eq!(refusal.input_index,1);
    }
}
''')
(K/'preparation.json').write_text(json.dumps(dict(unit='NATIVE-CONFIG-PIPELINE-DATA-SUPPORTING-IMPLEMENTATION-R1',baseProducer=str(BASE),standing='UNREVIEWED; MERGE DATA BASE REVIEW PENDING',expectedControls=6,productCodeUnchanged=True,configurationInputAdmitted=False,originalDefinitionsAdmitted=False,completeProjectionImplemented=False,productionInitializerUsed=False,sourceProfilePublished=False),indent=2)+'\n')
print(str(K))
