from pathlib import Path
import shutil,json
B=Path('/tmp/opensip-implementation');K=B/'native-config-discovery-controls-2026-10-10';W=K/'producer';BASE=B/'native-config-merge-data-2026-10-10/producer'
assert not K.exists();K.mkdir();shutil.copytree(BASE,W,symlinks=True)
p=W/'src/cargo/util/context/mod.rs';p.write_bytes(p.read_bytes()+b'\n#[cfg(test)]\nmod config_discovery_controls;\n')
(W/'src/cargo/util/context/config_discovery_controls.rs').write_text(r'''//! Actual stock discovery fixture observations, not native owned discovery.
use super::*;
use std::sync::atomic::{AtomicUsize,Ordering};
static NEXT:AtomicUsize=AtomicUsize::new(0);
struct Fixture {ctx:GlobalContext,root:PathBuf,project:PathBuf,near:PathBuf,home:PathBuf}
impl Drop for Fixture {fn drop(&mut self){std::fs::remove_dir_all(&self.root).unwrap();}}
fn fixture(home_is_project_cargo:bool)->Fixture {
    let root=std::env::temp_dir().join(format!("config-discovery-control-{}-{}",std::process::id(),NEXT.fetch_add(1,Ordering::Relaxed)));let project=root.join("project");let near=project.join("a/b");std::fs::create_dir_all(&near).unwrap();let home=if home_is_project_cargo {project.join(".cargo")} else {root.join("home")};std::fs::create_dir_all(&home).unwrap();
    // Ordinary constructor captures process state. Debug map only isolates
    // config getters; it is not owned environment or native-profile evidence.
    let mut ctx=GlobalContext::new(Shell::new(),near.clone(),home.clone());ctx.set_env(HashMap::new());ctx.search_stop_path=Some(project.clone());Fixture {ctx,root,project,near,home}
}
fn write(path:PathBuf,text:&str) {std::fs::create_dir_all(path.parent().unwrap()).unwrap();std::fs::write(path,text).unwrap();}
fn value<'a>(map:&'a HashMap<String,ConfigValue>,key:&str)->&'a str {map[key].string(key).unwrap().0}
fn discovered(f:&Fixture)->Vec<PathBuf> {let mut paths=Vec::new();f.ctx.walk_tree(&f.near,&f.home,|p|{paths.push(p.to_path_buf());Ok(())}).unwrap();paths}
#[test]
fn config_discovery_controls_legacy_selected_when_both_spellings_exist() {
    let f=fixture(false);let legacy=f.near.join(".cargo/config");write(legacy.clone(),"label='legacy'");write(f.near.join(".cargo/config.toml"),"label='current'");assert_eq!(discovered(&f),[legacy]);let values=f.ctx.load_values().unwrap();assert_eq!(value(&values,"label"),"legacy");
}
#[test]
fn config_discovery_controls_malformed_legacy_never_falls_back_to_valid_current() {
    let f=fixture(false);write(f.near.join(".cargo/config"),"[malformed");write(f.near.join(".cargo/config.toml"),"label='current'");assert!(f.ctx.load_values().is_err());
}
#[test]
fn config_discovery_controls_unused_malformed_current_not_parsed_with_valid_legacy() {
    let f=fixture(false);write(f.near.join(".cargo/config"),"label='legacy'");write(f.near.join(".cargo/config.toml"),"[malformed");assert_eq!(value(&f.ctx.load_values().unwrap(),"label"),"legacy");
}
#[test]
fn config_discovery_controls_current_only_keeps_exact_file_definition() {
    let f=fixture(false);let current=f.near.join(".cargo/config.toml");write(current.clone(),"label='current'");assert_eq!(discovered(&f),[current.clone()]);let values=f.ctx.load_values().unwrap();let Definition::Path(actual)=values["label"].definition() else {panic!("file definition")};assert_eq!(actual,&current);
}
#[test]
fn config_discovery_controls_near_ancestor_order_primitive_and_list_roots() {
    let f=fixture(false);let near=f.near.join(".cargo/config.toml");let ancestor=f.project.join(".cargo/config.toml");write(near.clone(),"label='near'\nitems=['near','same']");write(ancestor.clone(),"label='ancestor'\nitems=['ancestor','same']");assert_eq!(discovered(&f),[near,ancestor]);let values=f.ctx.load_values().unwrap();assert_eq!(value(&values,"label"),"near");let ConfigValue::List(items,_)=&values["items"] else {panic!("list")};assert_eq!(items.iter().map(|v|v.string("items").unwrap().0).collect::<Vec<_>>(),["ancestor","same","near","same"]);assert_eq!(items[0].definition().root(&f.near),f.project.as_path());assert_eq!(items[3].definition().root(&f.near),f.near.as_path());
}
#[test]
fn config_discovery_controls_stop_boundary_inclusive_no_outer_malformed_read() {
    let f=fixture(false);write(f.root.join(".cargo/config.toml"),"[outer-malformed");let stop=f.project.join(".cargo/config.toml");write(stop.clone(),"label='stop'");assert_eq!(discovered(&f),[stop]);assert_eq!(value(&f.ctx.load_values().unwrap(),"label"),"stop");
}
#[test]
fn config_discovery_controls_home_follows_ancestors_even_after_search_stop() {
    let f=fixture(false);let ancestor=f.project.join(".cargo/config.toml");let home=f.home.join("config.toml");write(ancestor.clone(),"label='project'\nitems=['project']");write(home.clone(),"label='home'\nitems=['home']");assert_eq!(discovered(&f),[ancestor,home]);let values=f.ctx.load_values().unwrap();assert_eq!(value(&values,"label"),"project");let ConfigValue::List(items,_)=&values["items"] else {panic!("list")};assert_eq!(items.iter().map(|v|v.string("items").unwrap().0).collect::<Vec<_>>(),["home","project"]);
}
#[test]
fn config_discovery_controls_home_already_in_ancestor_population_only_once() {
    let f=fixture(true);let config=f.project.join(".cargo/config.toml");write(config.clone(),"items=['once']");assert_eq!(discovered(&f),[config]);let values=f.ctx.load_values().unwrap();let ConfigValue::List(items,_)=&values["items"] else {panic!("list")};assert_eq!(items.len(),1);
}
''')
(K/'preparation.json').write_text(json.dumps(dict(unit='NATIVE-CONFIG-DISCOVERY-FIXTURE-CONTROLS-R1',baseProducer=str(BASE),standing='UNREVIEWED CONDITIONAL STOCK LIBRARY OBSERVATIONS',expectedControls=8,actualFilesPrivateTMPDIROnly=True,explicitSearchStopInsideFixture=True,ordinaryConstructorCapturesAcknowledged=True,includeBehaviorSelected=False,originalHomeAdmissionSelected=False,configurationInputAdmitted=False,originalDefinitionsAdmitted=False,nativeOwnedDiscoveryImplemented=False,completeProjectionImplemented=False,sourceProfilePublished=False,productCodeUnchanged=True),indent=2)+'\n')
print(str(K))
