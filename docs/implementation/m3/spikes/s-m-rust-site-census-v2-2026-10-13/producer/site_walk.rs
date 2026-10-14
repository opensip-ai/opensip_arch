// Outside-product S-M site walk v2 (SM-13 decomposition, M3-L r6 item 9; S-M report plan U-3). v2 adds literal and
// control-flow sites to v1 (site_walk-v1.rs, unchanged otherwise): literal expressions and pattern literals by rustc
// LitKind, and if / match (by MatchSource) / loop (by LoopSource) / break / continue / return / short-circuit && and ||.
// Mapping these sites to NE literalKind or control-flow edgeKind is G3's; they are counted, not classified.
// Runs once in after_analysis,
// after the closed driver's timing event, and emits one `site_walk` event for the local crate.
// It counts compiler SITES per source file. Sites are not fact candidates: which sites become
// which candidates, census symbol kinds and batching are G3's, and stage grouping is C4a's.
use rustc_hir::{self as hir, def::{DefKind, Res}, intravisit::{self, Visitor}};
use rustc_middle::{hir::nested_filter, ty::{self, TyCtxt, TypeckResults}};
use rustc_span::{FileName, Span};
use std::collections::BTreeMap;
use std::time::Instant;

struct Walk<'tcx> { tcx: TyCtxt<'tcx>, typeck: Option<&'tcx TypeckResults<'tcx>>, files: BTreeMap<String, BTreeMap<String, u64>> }

impl<'tcx> Walk<'tcx> {
 // Sites from macro expansion are attributed to their outermost call site and also counted as `expanded`.
 fn add(&mut self, span: Span, kind: &str) {
  let site = span.source_callsite();
  let file = match self.tcx.sess.source_map().span_to_filename(site) {
   FileName::Real(real) => real.local_path().and_then(|p| p.to_str()).map(String::from).unwrap_or_else(|| String::from("<remapped>")),
   _ => String::from("<non-file>"),
  };
  let counts = self.files.entry(file).or_default();
  *counts.entry(kind.to_owned()).or_default() += 1;
  if span.from_expansion() { *counts.entry(format!("{kind}.expanded")).or_default() += 1; }
 }
}

impl<'tcx> Visitor<'tcx> for Walk<'tcx> {
 type NestedFilter = nested_filter::OnlyBodies;
 fn maybe_tcx(&mut self) -> TyCtxt<'tcx> { self.tcx }
 fn visit_nested_body(&mut self, id: hir::BodyId) {
  let owner = self.tcx.hir_body_owner_def_id(id);
  let saved = self.typeck.replace(self.tcx.typeck(owner));
  let body = self.tcx.hir_body(id);
  self.add(body.value.span, "body");
  self.visit_body(body);
  self.typeck = saved;
 }
 fn visit_expr(&mut self, e: &'tcx hir::Expr<'tcx>) {
  self.add(e.span, "expr");
  if let Some(t) = self.typeck && t.node_type_opt(e.hir_id).is_some() { self.add(e.span, "expr.typed"); }
  match e.kind {
   hir::ExprKind::Call(callee, _) => {
    self.add(e.span, "call");
    let resolved = match callee.kind {
     hir::ExprKind::Path(ref q) => self.typeck.is_some_and(|t| matches!(t.qpath_res(q, callee.hir_id), Res::Def(DefKind::Fn | DefKind::AssocFn | DefKind::Ctor(..), _))),
     _ => false,
    };
    self.add(e.span, if resolved { "call.pathResolved" } else { "call.other" });
   }
   hir::ExprKind::MethodCall(_, receiver, _, _) => {
    self.add(e.span, "methodCall");
    if let Some(t) = self.typeck {
     self.add(e.span, if t.type_dependent_def_id(e.hir_id).is_some() { "methodCall.resolved" } else { "methodCall.unresolved" });
     match t.expr_ty_adjusted_opt(receiver).map(|ty| ty.peel_refs().kind().clone()) {
      Some(ty::Dynamic(..)) => self.add(e.span, "methodCall.dynReceiver"),
      Some(ty::Param(_)) => self.add(e.span, "methodCall.paramReceiver"),
      _ => {}
     }
    }
   }
   hir::ExprKind::Path(ref q) => {
    self.add(e.span, "pathExpr");
    if let Some(t) = self.typeck {
     self.add(e.span, match t.qpath_res(q, e.hir_id) { Res::Def(..) => "pathExpr.def", Res::Local(_) => "pathExpr.local", Res::Err => "pathExpr.err", _ => "pathExpr.other" });
    }
   }
   hir::ExprKind::Field(..) => self.add(e.span, "field"),
   hir::ExprKind::Closure(..) => self.add(e.span, "closure"),
   hir::ExprKind::Lit(lit) => { self.add(e.span, "literal"); self.add(e.span, &format!("literal.{}", lit_kind(&lit.node))); }
   hir::ExprKind::If(..) => self.add(e.span, "controlFlow.if"),
   hir::ExprKind::Match(_, _, source) => { self.add(e.span, "controlFlow.match"); self.add(e.span, &format!("controlFlow.match.{source:?}")); }
   hir::ExprKind::Loop(_, _, source, _) => { self.add(e.span, "controlFlow.loop"); self.add(e.span, &format!("controlFlow.loop.{source:?}")); }
   hir::ExprKind::Break(..) => self.add(e.span, "controlFlow.break"),
   hir::ExprKind::Continue(..) => self.add(e.span, "controlFlow.continue"),
   hir::ExprKind::Ret(..) => self.add(e.span, "controlFlow.return"),
   hir::ExprKind::Binary(op, ..) if matches!(op.node, hir::BinOpKind::And | hir::BinOpKind::Or) => self.add(e.span, "controlFlow.shortCircuit"),
   _ => {}
  }
  intravisit::walk_expr(self, e)
 }
 fn visit_pat_expr(&mut self, p: &'tcx hir::PatExpr<'tcx>) {
  if let hir::PatExprKind::Lit { lit, .. } = p.kind { self.add(p.span, "literal.pattern"); self.add(p.span, &format!("literal.pattern.{}", lit_kind(&lit.node))); }
  intravisit::walk_pat_expr(self, p)
 }
 fn visit_path(&mut self, p: &hir::Path<'tcx>, _id: hir::HirId) {
  self.add(p.span, "path");
  match p.res { Res::Def(..) => self.add(p.span, "path.def"), Res::Err => self.add(p.span, "path.err"), _ => {} }
  intravisit::walk_path(self, p)
 }
}

// The rustc literal kind, by name only (never mapped to NE literalKind here).
fn lit_kind(k: &rustc_ast::LitKind) -> &'static str {
 use rustc_ast::LitKind as L;
 match k { L::Str(..) => "str", L::ByteStr(..) => "byteStr", L::CStr(..) => "cStr", L::Byte(..) => "byte", L::Char(..) => "char", L::Int(..) => "int", L::Float(..) => "float", L::Bool(..) => "bool", L::Err(..) => "err" }
}

pub fn emit(tcx: TyCtxt<'_>) {
 let started = Instant::now();
 let mut walk = Walk { tcx, typeck: None, files: BTreeMap::new() };
 for def in tcx.iter_local_def_id() {
  let kind = tcx.def_kind(def);
  walk.add(tcx.def_span(def), &format!("def.{}", kind.descr(def.to_def_id())));
 }
 for id in tcx.hir_crate_items(()).free_items() {
  let item = tcx.hir_item(id);
  match item.kind {
   hir::ItemKind::Use(path, _) => {
    walk.add(item.span, "use");
    for res in path.res.present_items() { walk.add(item.span, match res { Res::Def(..) => "use.def", Res::Err => "use.err", _ => "use.other" }); }
   }
   hir::ItemKind::ExternCrate(..) => walk.add(item.span, "externCrate"),
   _ => {}
  }
 }
 tcx.hir_visit_all_item_likes_in_crate(&mut walk);
 let elapsed = u64::try_from(started.elapsed().as_nanos()).expect("walk interval fits u64");
 let files: serde_json::Map<String, serde_json::Value> = walk.files.into_iter().map(|(f, c)| (f, serde_json::Value::from(c.into_iter().map(|(k, v)| (k, serde_json::Value::from(v))).collect::<serde_json::Map<_, _>>()))).collect();
 let mut event = serde_json::Map::new();
 event.insert("event".into(), "site_walk".into());
 event.insert("siteWalkVersion".into(), 2.into());
 event.insert("crateName".into(), tcx.crate_name(rustc_span::def_id::LOCAL_CRATE).as_str().into());
 event.insert("sitesAreNotCandidates".into(), true.into());
 event.insert("walkElapsedNanos".into(), elapsed.into());
 event.insert("files".into(), serde_json::Value::Object(files));
 println!("{}", serde_json::Value::Object(event));
}
