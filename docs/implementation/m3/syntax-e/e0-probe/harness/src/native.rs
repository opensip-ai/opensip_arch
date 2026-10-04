//! T-native leg: the `tree-sitter` crate (=0.27.0, its bundled runtime checked against the
//! pinned tag) with the four grammars compiled natively by build.rs from the same pinned
//! sources. Its serializer is written here, independently of the shim, so P3 compares two
//! implementations of SyntaxTreeV1 as well as two executions of the parser.

use crate::tree::{self, SymbolTable, Writer};
use tree_sitter::{Language, Parser, Tree};
use tree_sitter_language::LanguageFn;

extern "C" {
    fn tree_sitter_javascript() -> *const ();
    fn tree_sitter_rust() -> *const ();
    fn tree_sitter_tsx() -> *const ();
    fn tree_sitter_typescript() -> *const ();
}

pub const GRAMMARS: [&str; 4] = ["javascript", "rust", "tsx", "typescript"];

pub fn language(grammar: &str) -> Language {
    let f: unsafe extern "C" fn() -> *const () = match grammar {
        "javascript" => tree_sitter_javascript,
        "rust" => tree_sitter_rust,
        "tsx" => tree_sitter_tsx,
        "typescript" => tree_sitter_typescript,
        g => panic!("unknown grammar {g}"),
    };
    Language::new(unsafe { LanguageFn::from_raw(f) })
}

/// SymbolTableV1 recomputed from the linked Language (the T-native A11 join, E1 item 5).
pub fn symbol_table(lang: &Language) -> SymbolTable {
    let sc = lang.node_kind_count();
    let symbols = (0..sc)
        .map(|id| {
            let id = id as u16;
            (
                lang.node_kind_for_id(id).unwrap_or("").to_string(),
                lang.node_kind_is_named(id),
                lang.node_kind_is_visible(id),
            )
        })
        .collect();
    let fields = (1..=lang.field_count())
        .map(|id| lang.field_name_for_id(id as u16).unwrap_or("").to_string())
        .collect();
    SymbolTable { language_abi: lang.abi_version() as u32, symbols, fields }
}

pub struct NativeResult {
    pub status: u32,
    pub tree: Option<Vec<u8>>,
}

/// Parse with a fresh Parser (mirroring the fresh-instance rule) and serialize.
pub fn parse(lang: &Language, src: &[u8]) -> NativeResult {
    let mut parser = Parser::new();
    if parser.set_language(lang).is_err() {
        return NativeResult { status: tree::ST_FAULT_LANGUAGE, tree: None };
    }
    match parser.parse(src, None) {
        None => NativeResult { status: tree::ST_FAULT_PARSE_NULL, tree: None },
        Some(t) => serialize(&t),
    }
}

fn serialize(t: &Tree) -> NativeResult {
    let mut w = Writer::new(1024);
    let mut cur = t.walk();
    let (mut depth, mut max_depth) = (1u32, 1u32);
    let mut status = tree::ST_OK;
    'outer: loop {
        if depth > tree::MAX_DEPTH {
            status = tree::ST_TRUNC_DEPTH;
            break;
        }
        if w.n == tree::MAX_NODES {
            status = tree::ST_TRUNC_NODES;
            break;
        }
        let node = cur.node();
        let mut flags = 0u16;
        if node.is_named() {
            flags |= tree::F_NAMED;
        }
        if node.is_extra() {
            flags |= tree::F_EXTRA;
        }
        if node.is_error() {
            flags |= tree::F_ERROR;
        }
        if node.is_missing() {
            flags |= tree::F_MISSING;
        }
        let field = cur.field_id().map(|f| f.get()).unwrap_or(0);
        w.node(
            node.kind_id(),
            field,
            flags,
            node.start_byte() as u32,
            node.end_byte() as u32,
            node.child_count(),
        );
        if cur.goto_first_child() {
            depth += 1;
            max_depth = max_depth.max(depth);
            continue;
        }
        loop {
            if cur.goto_next_sibling() {
                continue 'outer;
            }
            if !cur.goto_parent() {
                break 'outer;
            }
            depth -= 1;
        }
    }
    // Like the shim: a truncated walk yields a status and no tree.
    let tree = if status == tree::ST_OK { Some(w.finish(max_depth)) } else { None };
    NativeResult { status, tree }
}
