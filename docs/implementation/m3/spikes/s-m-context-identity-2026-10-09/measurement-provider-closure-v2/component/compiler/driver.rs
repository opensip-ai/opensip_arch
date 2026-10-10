#![feature(rustc_private)]
extern crate rustc_driver;
extern crate rustc_interface;
extern crate rustc_middle;
extern crate rustc_hir;
extern crate rustc_span;
extern crate rustc_ast;
extern crate rustc_ast_pretty;
extern crate rustc_lexer;
use std::{collections::BTreeMap, io, path::{Path,PathBuf,Component}, sync::{Arc,atomic::{AtomicU64,Ordering}}};
struct PreparedFiles { files: Arc<BTreeMap<PathBuf,Vec<u8>>>, cwd:PathBuf, reads:Arc<AtomicU64>, denied:Arc<AtomicU64> }
fn normalized(path:&Path,cwd:&Path)->PathBuf {
 let absolute=if path.is_absolute(){path.to_owned()}else{cwd.join(path)};let mut out=PathBuf::new();
 for p in absolute.components(){match p{Component::CurDir=>{},Component::ParentDir=>{out.pop();},p=>out.push(p.as_os_str())}}
 out
}
impl rustc_span::source_map::FileLoader for PreparedFiles {
 fn current_directory(&self)->io::Result<PathBuf>{Ok(self.cwd.clone())}
 fn file_exists(&self,path:&Path)->bool {self.files.contains_key(&normalized(path,&self.cwd))}
 fn read_file(&self,path:&Path)->io::Result<String> {
  self.reads.fetch_add(1,Ordering::Relaxed);
  match self.files.get(&normalized(path,&self.cwd)) {Some(bytes)=>String::from_utf8(bytes.clone()).map_err(|_|io::Error::new(io::ErrorKind::InvalidData,"prepared source is not UTF8")),None=>{self.denied.fetch_add(1,Ordering::Relaxed);Err(io::Error::new(io::ErrorKind::NotFound,"source read outside prepared map"))}}
 }
 fn read_binary_file(&self,path:&Path)->io::Result<Arc<[u8]>> {
  self.reads.fetch_add(1,Ordering::Relaxed);
  match self.files.get(&normalized(path,&self.cwd)){Some(bytes)=>Ok(Arc::from(bytes.clone())),None=>{self.denied.fetch_add(1,Ordering::Relaxed);Err(io::Error::new(io::ErrorKind::NotFound,"binary source read outside prepared map"))}}
 }
}
struct ExpandedFunctions<'a> { resolver: &'a rustc_middle::ty::ResolverAstLowering, rows: Vec<(rustc_hir::def_id::LocalDefId,String,bool)> }
impl<'ast> rustc_ast::visit::Visitor<'ast> for ExpandedFunctions<'_> {
 fn visit_item(&mut self,item:&'ast rustc_ast::ast::Item) {
  if let rustc_ast::ast::ItemKind::Fn(_)=&item.kind {
   let mut projection=item.clone(); projection.attrs.clear();
   if let rustc_ast::ast::ItemKind::Fn(f)=&mut projection.kind { f.body=None; }
   if let Some(def)=self.resolver.node_id_to_def_id.get(&item.id) {
    self.rows.push((*def,rustc_ast_pretty::pprust::item_to_string(&projection),item.span.from_expansion()));
   }
  }
  rustc_ast::visit::walk_item(self,item);
 }
 fn visit_assoc_item(&mut self,item:&'ast rustc_ast::ast::AssocItem,ctxt:rustc_ast::visit::AssocCtxt) {
  if let rustc_ast::ast::AssocItemKind::Fn(_)=&item.kind {
   let mut projection=item.clone(); projection.attrs.clear();
   if let rustc_ast::ast::AssocItemKind::Fn(f)=&mut projection.kind { f.body=None; }
   if let Some(def)=self.resolver.node_id_to_def_id.get(&item.id) {
    self.rows.push((*def,rustc_ast_pretty::pprust::assoc_item_to_string(&projection),item.span.from_expansion()));
   }
  }
  rustc_ast::visit::walk_assoc_item(self,item,ctxt);
 }
}
struct Probe {expanded_functions: Vec<(rustc_hir::def_id::LocalDefId,String,bool)>,loader:Option<PreparedFiles>,reads:Arc<AtomicU64>,denied:Arc<AtomicU64>,emit_metadata:bool}
impl rustc_driver::Callbacks for Probe {
 fn config(&mut self,config:&mut rustc_interface::interface::Config){config.file_loader=Some(Box::new(self.loader.take().unwrap()));}
 fn after_expansion<'tcx>(&mut self,_:&rustc_interface::interface::Compiler,tcx:rustc_middle::ty::TyCtxt<'tcx>)->rustc_driver::Compilation {
  {
   let borrowed=tcx.resolver_for_lowering().borrow(); let (resolver,krate)=&*borrowed;
   let mut observer=ExpandedFunctions{resolver,rows:Vec::new()};
   rustc_ast::visit::walk_crate(&mut observer,krate);
   self.expanded_functions=observer.rows;
  }
  println!("{{\"event\":\"after_expansion\",\"readCalls\":{},\"deniedReadCalls\":{}}}",self.reads.load(Ordering::Relaxed),self.denied.load(Ordering::Relaxed));rustc_driver::Compilation::Continue
 }
 fn after_analysis<'tcx>(&mut self,_:&rustc_interface::interface::Compiler,tcx:rustc_middle::ty::TyCtxt<'tcx>)->rustc_driver::Compilation {
  for (def,text,expanded) in &self.expanded_functions {
   println!("{{\"event\":\"expanded_function_definition_join\",\"definitionId\":{},\"defPathHash\":{},\"defPath\":{},\"headerProjection\":{}}}",json_text(&format!("{:?}",def)),json_text(&format!("{:?}",tcx.def_path_hash(def.to_def_id()))),json_text(&tcx.def_path_str(def.to_def_id())),json_text(text));
   let mut offset=0usize;let mut parts=Vec::new();
   for token in rustc_lexer::tokenize(text,rustc_lexer::FrontmatterAllowed::No) {
    let end=offset.checked_add(token.len as usize).unwrap();let spelling=&text[offset..end];
    parts.push(format!("{{\"kind\":{},\"text\":{}}}",json_text(&format!("{:?}",token.kind)),json_text(spelling)));offset=end;
   }
   assert_eq!(offset,text.len());
   println!("{{\"event\":\"compiler_function_header_lexer_observation\",\"defPath\":{},\"headerProjection\":{},\"tokens\":[{}],\"fromExpansion\":{}}}",json_text(&tcx.def_path_str(def.to_def_id())),json_text(text),parts.join(","),expanded);

   println!("{{\"event\":\"expanded_ast_function_header_observation\",\"defPath\":{},\"defKind\":{},\"headerProjection\":{},\"fromExpansion\":{},\"exported\":{}}}",json_text(&tcx.def_path_str(def.to_def_id())),json_text(&format!("{:?}",tcx.def_kind(*def))),json_text(text),expanded,tcx.effective_visibilities(()).is_exported(*def));
  }
  // Compiler observations only: not FactCandidate or complete FA2 census.
  let source_map=tcx.sess.source_map(); let mut total=0u64;let mut dummy=0u64;let mut cross_file=0u64;let mut observed=0u64;
  for def in tcx.iter_local_def_id() {
   println!("{{\"event\":\"local_definition_join\",\"definitionId\":{},\"defPathHash\":{},\"defPath\":{}}}",json_text(&format!("{:?}",def)),json_text(&format!("{:?}",tcx.def_path_hash(def.to_def_id()))),json_text(&tcx.def_path_str(def.to_def_id())));
   println!("{{\"event\":\"effective_export_observation\",\"defPath\":{},\"defKind\":{},\"exported\":{}}}",json_text(&tcx.def_path_str(def.to_def_id())),json_text(&format!("{:?}",tcx.def_kind(def))),tcx.effective_visibilities(()).is_exported(def));
   if matches!(tcx.def_kind(def),rustc_hir::def::DefKind::Fn|rustc_hir::def::DefKind::AssocFn) {
    if let Some(sig)=tcx.hir_node_by_def_id(def).fn_sig() {
     let snippet=source_map.span_to_snippet(sig.span);
     println!("{{\"event\":\"function_signature_span_observation\",\"defPath\":{},\"signatureSnippet\":{},\"snippetAvailable\":{},\"fromExpansion\":{}}}",json_text(&tcx.def_path_str(def.to_def_id())),json_text(snippet.as_deref().unwrap_or("")),snippet.is_ok(),sig.span.from_expansion());
    }
   }
   total+=1;let span=tcx.def_span(def);if span.is_dummy(){dummy+=1;continue;}
   let start=source_map.lookup_byte_offset(span.lo());
   let end=source_map.lookup_byte_offset(span.hi());
   if !std::sync::Arc::ptr_eq(&start.sf,&end.sf){cross_file+=1;continue;}observed+=1;
   println!("{{\"event\":\"local_definition_observation\",\"defPath\":{},\"defKind\":{},\"sourceName\":{},\"startByte\":{},\"endByte\":{},\"fromExpansion\":{}}}",json_text(&tcx.def_path_str(def.to_def_id())),json_text(&format!("{:?}",tcx.def_kind(def))),json_text(&start.sf.name.prefer_local_unconditionally().to_string()),start.pos.0,end.pos.0,span.from_expansion());
  }

  for sf in source_map.files().iter() {
   let length=sf.src.as_ref().map(|s|s.len().to_string()).unwrap_or_else(||"null".to_string());
   println!("{{\"event\":\"source_file_observation\",\"sourceName\":{},\"loadedSourceBytes\":{},\"hasLoadedSource\":{}}}",json_text(&sf.name.prefer_local_unconditionally().to_string()),length,sf.src.is_some());
  }
  for item_id in tcx.hir_crate_items(()).free_items() {
   let item=tcx.hir_item(item_id);
   println!("{{\"event\":\"item_visibility_observation\",\"defPath\":{},\"defKind\":{},\"declaredVisibilityDebug\":{}}}",json_text(&tcx.def_path_str(item.owner_id.to_def_id())),json_text(&format!("{:?}",tcx.def_kind(item.owner_id.def_id))),json_text(&format!("{:?}",tcx.visibility(item.owner_id.to_def_id()))));

   if let rustc_hir::ItemKind::Use(path,kind)=&item.kind {
    let snippet=source_map.span_to_snippet(path.span);
    println!("{{\"event\":\"import_observation\",\"ownerDefPath\":{},\"useKind\":{},\"resolutionDebug\":{},\"snippet\":{},\"snippetAvailable\":{},\"fromExpansion\":{}}}",json_text(&tcx.def_path_str(item.owner_id.to_def_id())),json_text(&format!("{kind:?}")),json_text(&format!("{:?}",path.res)),json_text(snippet.as_deref().unwrap_or("")),snippet.is_ok(),path.span.from_expansion());
   }
  }
  println!("{{\"event\":\"definition_observation_summary\",\"totalLocalDefinitions\":{},\"dummySpanDefinitions\":{},\"crossFileSpanDefinitions\":{},\"observedDefinitions\":{}}}",total,dummy,cross_file,observed);
  println!("{{\"event\":\"after_analysis\",\"readCalls\":{},\"deniedReadCalls\":{}}}",self.reads.load(Ordering::Relaxed),self.denied.load(Ordering::Relaxed));if self.emit_metadata {rustc_driver::Compilation::Continue} else {rustc_driver::Compilation::Stop}
 }
}
fn number(raw:&[u8],at:&mut usize)->usize {let end=at.checked_add(8).unwrap();let n=u64::from_be_bytes(raw[*at..end].try_into().unwrap());*at=end;usize::try_from(n).unwrap()}
fn bytes<'a>(raw:&'a[u8],at:&mut usize,n:usize)->&'a[u8]{let end=at.checked_add(n).unwrap();let value=&raw[*at..end];*at=end;value}
fn main(){
 let mut args:Vec<String>=std::env::args().collect();assert_eq!(args.get(1).map(String::as_str),Some("--prepared-map"));let raw=std::fs::read(&args[2]).unwrap();args.drain(1..3);let emit_metadata=if let Some(at)=args.iter().position(|a|a=="--spike-emit-metadata") {args.remove(at);true}else{false};assert!(raw.starts_with(b"OPSMRUST1\0"));let mut at=10;let count=number(&raw,&mut at);assert!(count<=raw.len()/16);let cwd=std::env::current_dir().unwrap();let mut files=BTreeMap::new();
 for _ in 0..count {let n=number(&raw,&mut at);let name=std::str::from_utf8(bytes(&raw,&mut at,n)).unwrap();let n=number(&raw,&mut at);let content=bytes(&raw,&mut at,n).to_vec();let name=PathBuf::from(name);assert!(name.is_absolute());assert_eq!(normalized(&name,&cwd),name);assert!(files.insert(name,content).is_none());}assert_eq!(at,raw.len());let reads=Arc::new(AtomicU64::new(0));let denied=Arc::new(AtomicU64::new(0));let loader=PreparedFiles{files:Arc::new(files),cwd,reads:reads.clone(),denied:denied.clone()};let mut callbacks=Probe{expanded_functions:Vec::new(),loader:Some(loader),reads,denied,emit_metadata};rustc_driver::run_compiler(&args,&mut callbacks);
}

fn json_text(text:&str)->String {let mut out=String::from("\"");for ch in text.chars(){match ch {'"'=>out.push_str("\\\""),'\\'=>out.push_str("\\\\"),'\n'=>out.push_str("\\n"),'\r'=>out.push_str("\\r"),'\t'=>out.push_str("\\t"),c if c<'\u{20}'=>out.push_str(&format!("\\u{:04x}",c as u32)),c=>out.push(c)}}out.push('"');out}
