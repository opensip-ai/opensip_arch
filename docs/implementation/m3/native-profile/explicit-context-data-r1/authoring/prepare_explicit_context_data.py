from pathlib import Path
import shutil,json,re
B=Path('/tmp/opensip-implementation');K=B/'native-explicit-context-data-2026-10-10';W=K/'producer';BASE=B/'native-config-merge-data-2026-10-10/producer'
assert not K.exists();K.mkdir();shutil.copytree(BASE,W,symlinks=True)
p=W/'src/cargo/util/context/mod.rs';source=p.read_text();p.write_bytes(p.read_bytes()+b'\n#[allow(dead_code)]\nmod explicit_context_data;\n')
start=source.index('        GlobalContext {',source.index('    pub fn new(shell:'));end=source.index('\n        }\n    }',start)+len('\n        }');body=source[start:end]
assert body.count('jobserver: unsafe {')==1
body=re.sub(r'jobserver: unsafe \{.*?\n            \},','jobserver: initial.jobserver,',body,flags=re.S)
body=body.replace('nightly_features_allowed: matches!(&*features::channel(), "nightly" | "dev"),','nightly_features_allowed: initial.nightly_features_allowed,')
assert 'features::channel()' not in body and 'GLOBAL_JOBSERVER' not in body
prefix=r'''//! Explicit constructor INITIAL STATE DATA only, no environment/Tool/profile admission.
use super::*;
pub(super) struct InitialStateData {
    /// Supplied UTF8 map; no process Env snapshot. Not an admitted environment.
    pub(super) environment: HashMap<String,String>,
    /// Supplied client data, no process/global jobserver acquisition.
    pub(super) jobserver: Option<jobserver::Client>,
    /// Supplied Cargo capability bit as data, not a native-profile permission.
    pub(super) nightly_features_allowed: bool,
}
pub(super) fn new_with_initial_state_data(
    shell: Shell,cwd:PathBuf,homedir:PathBuf,
    values:HashMap<String,ConfigValue>,initial:InitialStateData,
) -> CargoResult<GlobalContext> {
    // Reuse pinned derived Env maps without taking any process Env snapshot.
    let env=Env::from_map(initial.environment);
    let cache_rustc_info=match env.get_env_os("CARGO_CACHE_RUSTC_INFO") {
        Some(cache)=>cache!="0",_=>true,
    };
    let mut context =
'''
suffix=r''';
    context.set_values(values)?;
    context.projected_values_data=true;
    Ok(context)
}
#[cfg(test)]
mod tests {
    use super::*;
    use std::sync::atomic::{AtomicUsize,Ordering};
    static NEXT:AtomicUsize=AtomicUsize::new(0);
    struct Fixture {ctx:GlobalContext,root:PathBuf}
    impl Drop for Fixture {fn drop(&mut self){std::fs::remove_dir_all(&self.root).unwrap();}}
    fn fixture(environment:HashMap<String,String>,jobserver:Option<jobserver::Client>,nightly:bool)->Fixture {
        let root=std::env::temp_dir().join(format!("explicit-context-data-{}-{}",std::process::id(),NEXT.fetch_add(1,Ordering::Relaxed)));std::fs::create_dir(&root).unwrap();let home=root.join("home");std::fs::create_dir(&home).unwrap();std::fs::create_dir(root.join(".cargo")).unwrap();std::fs::write(root.join(".cargo/config.toml"),"[poisoned").unwrap();
        let values=HashMap::from([("resolver".into(),ConfigValue::Table(HashMap::from([("incompatible-rust-versions".into(),ConfigValue::String("fallback".into(),Definition::Path(PathBuf::from("/unadmitted/original/.cargo/config.toml"))))]),Definition::BuiltIn))]);
        let ctx=new_with_initial_state_data(Shell::new(),root.clone(),home,values,InitialStateData {environment,jobserver,nightly_features_allowed:nightly}).unwrap();Fixture {ctx,root}
    }
    #[test]
    fn explicit_context_data_empty_map_and_no_jobserver_not_process_capture() {
        let f=fixture(HashMap::new(),None,false);assert!(f.ctx.env.iter_str().next().is_none());assert!(f.ctx.get_env_os("CARGO_HOME").is_none());assert!(f.ctx.get_env_os("PATH").is_none());assert!(f.ctx.jobserver_from_env().is_none());assert!(!f.ctx.nightly_features_allowed);
    }
    #[test]
    fn explicit_context_data_supplied_environment_only_without_debug_override() {
        let f=fixture(HashMap::from([("CARGO_HOME".into(),"/unadmitted/supplied-home".into()),("CONTROL_SENTINEL".into(),"supplied".into())]),None,false);assert_eq!(f.ctx.env.iter_str().count(),2);assert_eq!(f.ctx.get_env("CONTROL_SENTINEL").unwrap(),"supplied");assert_eq!(f.ctx.get_env("CARGO_HOME").unwrap(),"/unadmitted/supplied-home");
    }
    #[test]
    fn explicit_context_data_cache_flag_derives_only_supplied_map() {
        for (value,expected) in [(None,true),(Some("0"),false),(Some("1"),true),(Some(""),true)] {let env=value.map(|v|HashMap::from([("CARGO_CACHE_RUSTC_INFO".into(),v.into())])).unwrap_or_default();let f=fixture(env,None,false);assert_eq!(f.ctx.cache_rustc_info,expected);}
    }
    #[test]
    fn explicit_context_data_channel_bit_is_supplied_not_process_query() {
        for value in [false,true] {let f=fixture(HashMap::new(),None,value);assert_eq!(f.ctx.nightly_features_allowed,value);}
    }
    #[test]
    fn explicit_context_data_supplied_jobserver_kept_without_from_env() {
        let client=jobserver::Client::new(1).unwrap();let f=fixture(HashMap::new(),Some(client),false);assert!(f.ctx.jobserver_from_env().is_some());
    }
    #[test]
    fn explicit_context_data_once_initialized_getter_preserves_leaf_definition() {
        let mut f=fixture(HashMap::new(),None,false);assert_eq!(f.ctx.get::<String>("resolver.incompatible-rust-versions").unwrap(),"fallback");assert_eq!(f.ctx.get_string("resolver.incompatible-rust-versions").unwrap().unwrap().definition.root(f.ctx.cwd()),Path::new("/unadmitted/original"));assert!(f.ctx.set_values(HashMap::new()).is_err());assert!(f.ctx.values_mut().is_err());
    }
    #[test]
    fn explicit_context_data_arbitrary_override_demonstrates_no_environment_admission() {
        let f=fixture(HashMap::from([("CARGO_RESOLVER_INCOMPATIBLE_RUST_VERSIONS".into(),"allow".into())]),None,false);assert_eq!(f.ctx.get::<String>("resolver.incompatible-rust-versions").unwrap(),"allow");
    }
    #[test]
    fn explicit_context_data_credentials_and_rediscovery_refuse_before_read() {
        let mut f=fixture(HashMap::new(),None,false);assert!(f.ctx.load_credentials().is_err());assert!(!f.ctx.credential_values.filled());let cwd=f.ctx.cwd.clone();assert!(f.ctx.reload_cwd().is_err());assert_eq!(f.ctx.cwd,cwd);assert_eq!(f.ctx.get::<String>("resolver.incompatible-rust-versions").unwrap(),"fallback");
    }
}
'''
(W/'src/cargo/util/context/explicit_context_data.rs').write_text(prefix+body+suffix)
(K/'preparation.json').write_text(json.dumps(dict(unit='NATIVE-EXPLICIT-CONTEXT-INITIAL-STATE-DATA-R1',baseProducer=str(BASE),standing='UNREVIEWED DATA CONSTRUCTOR; NO ENVIRONMENT/PROFILE ADMISSION',expectedControls=8,ordinaryConstructorUnchanged=True,ambientEnvCapturedByDataConstructor=False,ambientJobserverCapturedByDataConstructor=False,processChannelQueriedByDataConstructor=False,operationalCreationTimeUsesInstantNow=True,environmentInputIsUTF8DataOnly=True,configurationInputAdmitted=False,originalDefinitionsAdmitted=False,hostConstructedEnvironment=False,constructorCapturesGoverned=False,productionInitializerUsed=False,sourceProfilePublished=False,productCodeUnchanged=True),indent=2)+'\n')
print(str(K))
