//! E0 harness (throwaway probe for E1 item 3; never product code).
//!
//!   e0 inspect <module.wasm>...                     P2 and the A9/A10 shape, two witnesses
//!   e0 admit   --modules DIR                        A9-A11 chain and its cost; SymbolTableV1
//!                                                   from each module vs the native Language
//!   e0 run     --modules DIR --list TSV --root DIR --out TSV
//!              [--mode both|wasm|native] [--order sorted|reverse|shuffle:SEED]
//!              [--threads N] [--compilation eager|lazy] [--reuse-instance]
//!              [--fuel-base B --fuel-per-byte K] [--max-pages P] [--dump DIR]
//!              [--budget-from TSV --fuel-delta D --pages-delta E] [--sample N]
//!
//! --budget-from takes each file's measured w_fuel_total and w_pages_peak from an earlier
//! run and runs it with exactly that fuel + D and that ceiling + E (P6 boundary controls).
//! --sample N keeps the files whose list index is a multiple of N.
//!
//! The list is fetch_pinned.py's t2a-selected.tsv. Output rows are always written in list
//! order; `seq` records the processing position so a shuffled run is visibly shuffled.

mod native;
mod tree;
mod wasm;
mod wasmbin;

use std::collections::HashMap;
use std::fs;
use std::io::Write;
use std::path::{Path, PathBuf};
use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::Mutex;
use std::time::Instant;

const MAX_FILE_BYTES: u64 = 4 * 1024 * 1024; // E1 item 11 maxFileBytes

fn opts(args: &[String]) -> (HashMap<String, String>, Vec<String>) {
    let mut m = HashMap::new();
    let mut rest = Vec::new();
    let mut i = 0;
    while i < args.len() {
        let a = &args[i];
        if let Some(k) = a.strip_prefix("--") {
            if k == "reuse-instance" {
                m.insert(k.to_string(), "1".to_string());
            } else {
                m.insert(k.to_string(), args.get(i + 1).cloned().unwrap_or_default());
                i += 1;
            }
        } else {
            rest.push(a.clone());
        }
        i += 1;
    }
    (m, rest)
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let (o, rest) = opts(&args[2.min(args.len())..]);
    match args.get(1).map(String::as_str) {
        Some("inspect") => inspect(&rest),
        Some("admit") => admit(&o),
        Some("run") => run(&o),
        _ => {
            eprintln!("usage: see the header of src/main.rs");
            std::process::exit(2);
        }
    }
}

fn module_path(dir: &str, g: &str) -> PathBuf {
    Path::new(dir).join(format!("{g}.wasm"))
}

// ---------------------------------------------------------------------------------------
// P2: imports, exports, start, memories and target features, read by the independent
// reader and by the engine (wasmi's Module view).
fn inspect(paths: &[String]) {
    let engine = wasm::engine(false, true);
    println!("module\tsha256\tbytes\timports(reader)\timports(engine)\texports\tstart\tmemories\ttables\tglobals\tdata_segments\tdata_bytes\tfunctions\ttarget_features\tcustom_sections\tengine_shape");
    for p in paths {
        let b = fs::read(p).expect("read module");
        let s = wasmbin::read(&b).unwrap_or_else(|e| panic!("{p}: {e}"));
        let eng = wasmi::Module::new(&engine, &b);
        let (eng_imports, shape) = match &eng {
            Ok(m) => (m.imports().count().to_string(), {
                let e = wasm::check_shape(m);
                if e.is_empty() { "ok".to_string() } else { e.join(",") }
            }),
            Err(e) => ("-".into(), format!("invalid:{e}")),
        };
        let exports: Vec<String> = s
            .exports
            .iter()
            .map(|(n, k, i)| match k {
                0 => format!("{n}{}", wasmbin::export_sig(&s, *i).unwrap_or_default()),
                2 => format!("{n}:memory"),
                _ => format!("{n}:kind{k}"),
            })
            .collect();
        let mems: Vec<String> = s.memories.iter().map(|(f, mn, mx)| format!("flags{f}:min{mn}:max{mx:?}")).collect();
        println!(
            "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}",
            p,
            tree::sha256_hex(&b),
            b.len(),
            s.imports.len(),
            eng_imports,
            exports.join(" "),
            s.start.map(|x| x.to_string()).unwrap_or_else(|| "none".into()),
            mems.join(" "),
            s.tables,
            s.globals,
            s.data_segments,
            s.data_bytes,
            s.code_bodies,
            s.target_features.join(" "),
            s.custom.iter().map(|(n, z)| format!("{n}:{z}")).collect::<Vec<_>>().join(" "),
            shape
        );
    }
}

// ---------------------------------------------------------------------------------------
// The admission chain's cost (recorded, not gated) and the A11 join against native.
fn admit(o: &HashMap<String, String>) {
    let dir = o.get("modules").expect("--modules");
    let engine = wasm::engine(false, true);
    let no_float_engine = wasm::engine(false, false);
    println!("grammar\tmodule_sha256\tbytes\tt_read_hash_us\tt_compile_us\tt_shape_us\tt_instantiate_us\tt_symbols_us\tt_total_us\tadmission_fuel\tshim_abi\tshape\tlanguage_abi\tsymbols\tfields\tsymtab_wasm_sha256\tsymtab_native_sha256\tsymtab_equal\tfloat_free");
    for g in native::GRAMMARS {
        let t0 = Instant::now();
        let bytes = fs::read(module_path(dir, g)).expect("module");
        let digest = tree::sha256_hex(&bytes);
        let t_hash = t0.elapsed();
        let float_free = wasmi::Module::validate(&no_float_engine, &bytes).is_ok();
        match wasm::admit(&engine, &bytes) {
            Err(e) => println!("{g}\t{digest}\t{}\tADMISSION-FAILED\t{e}", bytes.len()),
            Ok((_m, a)) => {
                let lang = native::language(g);
                let nt = native::symbol_table(&lang);
                let n_json = tree::symbol_table_v1(g, &nt);
                let n_sha = tree::sha256_hex(n_json.as_bytes());
                let (w_sha, lang_abi, ns, nf) = match &a.table {
                    Ok(t) => {
                        let j = tree::symbol_table_v1(g, t);
                        if let Some(d) = o.get("dump") {
                            let _ = fs::create_dir_all(d);
                            let _ = fs::write(Path::new(d).join(format!("{g}.symtab.wasm.json")), &j);
                            let _ = fs::write(Path::new(d).join(format!("{g}.symtab.native.json")), &n_json);
                        }
                        (tree::sha256_hex(j.as_bytes()), t.language_abi, t.symbols.len(), t.fields.len())
                    }
                    Err(e) => (format!("error:{e}"), 0, 0, 0),
                };
                let us = |d: std::time::Duration| d.as_micros();
                let total = t_hash + a.t_compile + a.t_shape + a.t_instantiate + a.t_symbols;
                println!(
                    "{g}\t{digest}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}",
                    bytes.len(),
                    us(t_hash),
                    us(a.t_compile),
                    us(a.t_shape),
                    us(a.t_instantiate),
                    us(a.t_symbols),
                    us(total),
                    a.admission_fuel,
                    a.abi,
                    if a.shape_errors.is_empty() { "ok".to_string() } else { a.shape_errors.join(",") },
                    lang_abi,
                    ns,
                    nf,
                    w_sha,
                    n_sha,
                    w_sha == n_sha,
                    float_free
                );
            }
        }
    }
}

// ---------------------------------------------------------------------------------------
// The sweep (P3-P6).
struct Item {
    idx: usize,
    repo: String,
    path: String,
    grammar: String,
    mode: String,
    bytes: u64,
    sha: String,
}

fn load_list(p: &str) -> Vec<Item> {
    let mut v = Vec::new();
    for line in fs::read_to_string(p).expect("list").lines() {
        if line.starts_with('#') || line.is_empty() {
            continue;
        }
        let c: Vec<&str> = line.split('\t').collect();
        v.push(Item {
            idx: v.len(),
            repo: c[0].into(),
            path: c[1].into(),
            grammar: c[3].into(),
            mode: c[4].into(),
            bytes: c[5].parse().unwrap_or(0),
            sha: c[6].into(),
        });
    }
    v
}

fn run(o: &HashMap<String, String>) {
    let list = load_list(o.get("list").expect("--list"));
    let root = PathBuf::from(o.get("root").expect("--root"));
    let out_path = o.get("out").expect("--out").clone();
    let mode = o.get("mode").cloned().unwrap_or_else(|| "both".into());
    let threads: usize = o.get("threads").map(|s| s.parse().unwrap()).unwrap_or(1);
    let lazy = o.get("compilation").map(|s| s == "lazy").unwrap_or(false);
    let reuse = o.contains_key("reuse-instance");
    let fuel_base: Option<u64> = o.get("fuel-base").map(|s| s.parse().unwrap());
    let fuel_per_byte: u64 = o.get("fuel-per-byte").map(|s| s.parse().unwrap()).unwrap_or(0);
    let max_pages: u64 = o.get("max-pages").map(|s| s.parse().unwrap()).unwrap_or(wasm::WASM32_MAX_PAGES);
    let dump = o.get("dump").map(PathBuf::from);
    let order = o.get("order").cloned().unwrap_or_else(|| "sorted".into());
    let sample: usize = o.get("sample").map(|s| s.parse().unwrap()).unwrap_or(1);
    let fuel_delta: i64 = o.get("fuel-delta").map(|s| s.parse().unwrap()).unwrap_or(0);
    let pages_delta: i64 = o.get("pages-delta").map(|s| s.parse().unwrap()).unwrap_or(0);
    // idx -> (fuel, pages) for --budget-from
    let budgets: HashMap<usize, (u64, u64)> = match o.get("budget-from") {
        None => HashMap::new(),
        Some(p) => {
            let mut m = HashMap::new();
            let text = fs::read_to_string(p).expect("budget-from");
            let mut cols: Vec<String> = Vec::new();
            for line in text.lines() {
                if line.starts_with('#') {
                    continue;
                }
                let c: Vec<&str> = line.split('\t').collect();
                if cols.is_empty() {
                    cols = c.iter().map(|x| x.to_string()).collect();
                    continue;
                }
                let at = |name: &str| c[cols.iter().position(|x| x == name).unwrap()];
                if let (Ok(i), Ok(fu), Ok(pg)) =
                    (at("idx").parse::<usize>(), at("w_fuel_total").parse::<u64>(), at("w_pages_peak").parse::<u64>())
                {
                    m.insert(i, (fu, pg));
                }
            }
            m
        }
    };
    let per_file = |idx: usize, bytes: u64| -> (Option<u64>, u64) {
        match budgets.get(&idx) {
            Some(&(fu, pg)) => (
                Some((fu as i64 + fuel_delta).max(0) as u64),
                ((pg as i64 + pages_delta).max(0) as u64).min(wasm::WASM32_MAX_PAGES),
            ),
            None => (fuel_base.map(|b| b + fuel_per_byte * bytes), max_pages),
        }
    };

    let mut seq: Vec<usize> = (0..list.len()).filter(|i| i % sample == 0).collect();
    match order.as_str() {
        "sorted" => {}
        "reverse" => seq.reverse(),
        s if s.starts_with("shuffle:") => tree::shuffle(&mut seq, s[8..].parse().unwrap()),
        s => panic!("order {s}"),
    }

    let engine = wasm::engine(lazy, true);
    let mut modules = HashMap::new();
    let mut tables = HashMap::new();
    if mode != "native" {
        let dir = o.get("modules").expect("--modules");
        for g in native::GRAMMARS {
            let bytes = fs::read(module_path(dir, g)).expect("module");
            let (m, a) = wasm::admit(&engine, &bytes).expect("admission");
            assert!(a.shape_errors.is_empty(), "{g}: {:?}", a.shape_errors);
            let t = a.table.expect("symbol table");
            tables.insert(g.to_string(), (t.symbols.len() as u32, t.fields.len() as u32));
            modules.insert(g.to_string(), m);
        }
    }
    let langs: HashMap<String, tree_sitter::Language> =
        native::GRAMMARS.iter().map(|g| (g.to_string(), native::language(g))).collect();
    if mode == "native" {
        for (g, l) in &langs {
            let t = native::symbol_table(l);
            tables.insert(g.clone(), (t.symbols.len() as u32, t.fields.len() as u32));
        }
    }

    let rows: Vec<Mutex<Option<String>>> = (0..list.len()).map(|_| Mutex::new(None)).collect();
    let next = AtomicUsize::new(0);
    let started = Instant::now();
    std::thread::scope(|sc| {
        for _ in 0..threads {
            sc.spawn(|| {
                let mut reused: HashMap<String, wasm::Reused> = HashMap::new();
                loop {
                    let k = next.fetch_add(1, Ordering::SeqCst);
                    if k >= seq.len() {
                        break;
                    }
                    let it = &list[seq[k]];
                    let (fuel, pages) = per_file(it.idx, it.bytes);
                    let row = one(
                        it, k, &root, &mode, &engine, &modules, &langs, &tables, reuse, &mut reused, fuel, pages,
                        dump.as_deref(),
                    );
                    *rows[it.idx].lock().unwrap() = Some(row);
                }
            });
        }
    });
    let elapsed = started.elapsed();
    let mut f = fs::File::create(&out_path).expect("out");
    writeln!(
        f,
        "# e0 run mode={mode} order={order} threads={threads} compilation={} reuse={reuse} fuel_base={fuel_base:?} fuel_per_byte={fuel_per_byte} max_pages={max_pages} budget_from={:?} fuel_delta={fuel_delta} pages_delta={pages_delta} sample={sample} files={} wall_ms={}",
        if lazy { "lazy" } else { "eager" },
        o.get("budget-from"),
        seq.len(),
        elapsed.as_millis()
    )
    .unwrap();
    writeln!(f, "idx\tseq\trepo\tpath\tgrammar\tbytes\tutf8\tw_status\tw_outcome\tw_tree_sha256\tw_nodes\tw_depth\tw_valid\tw_fuel_total\tw_fuel_parse\tw_pages_initial\tw_pages_peak\tw_t_inst_ns\tw_t_parse_ns\tw_t_total_ns\tn_status\tn_outcome\tn_tree_sha256\tn_nodes\tn_valid\tn_t_total_ns\teq\tfirst_diff").unwrap();
    for r in rows {
        if let Some(line) = r.into_inner().unwrap() {
            writeln!(f, "{line}").unwrap();
        }
    }
    eprintln!("wrote {out_path} ({} files, {:.1}s)", seq.len(), elapsed.as_secs_f64());
}

fn outcome_of(status: &str, summary: &Result<tree::TreeSummary, String>) -> String {
    match status {
        "ok" => match summary {
            Ok(s) => s.outcome().to_string(),
            Err(_) => "backend-fault".into(),
        },
        "trunc-nodes" => "truncated:nodes".into(),
        "trunc-depth" => "truncated:depth".into(),
        "trunc-fuel" => "truncated:fuel".into(),
        "trunc-memory" => "truncated:memory".into(),
        "trunc-size" => "truncated:size".into(),
        _ => "backend-fault".into(),
    }
}

#[allow(clippy::too_many_arguments)]
fn one(
    it: &Item,
    k: usize,
    root: &Path,
    mode: &str,
    engine: &wasmi::Engine,
    modules: &HashMap<String, wasmi::Module>,
    langs: &HashMap<String, tree_sitter::Language>,
    tables: &HashMap<String, (u32, u32)>,
    reuse: bool,
    reused: &mut HashMap<String, wasm::Reused>,
    fuel: Option<u64>,
    max_pages: u64,
    dump: Option<&Path>,
) -> String {
    let head = format!("{}\t{}\t{}\t{}\t{}\t{}", it.idx, k, it.repo, it.path, it.grammar, it.bytes);
    if it.mode == "symlink" {
        // 28 columns like every row: utf8, w_status, w_outcome, then 19 placeholders.
        return format!("{head}\t-\tnot-regular\tnot-regular{}", "\t-".repeat(19));
    }
    let src = fs::read(root.join(&it.repo).join(&it.path)).expect("source");
    assert_eq!(tree::sha256_hex(&src), it.sha, "pinned digest of {}/{}", it.repo, it.path);
    let utf8 = std::str::from_utf8(&src).is_ok();
    let (sc, fc) = tables[&it.grammar];
    let too_big = src.len() as u64 > MAX_FILE_BYTES;

    // wasm leg
    let mut w_cols = "\t-".repeat(13);
    let mut w_tree: Option<Vec<u8>> = None;
    if mode != "native" {
        let r = if too_big {
            wasm::WasmResult { status: "trunc-size".into(), ..Default::default() }
        } else if reuse {
            reused
                .entry(it.grammar.clone())
                .or_insert_with(|| wasm::Reused::new(engine, &modules[&it.grammar]))
                .parse(&src)
        } else {
            wasm::parse_fresh(engine, &modules[&it.grammar], &src, fuel.unwrap_or(wasm::UNBOUNDED_FUEL), max_pages)
        };
        let t_valid = Instant::now();
        let summary = match &r.tree {
            Some(b) => tree::validate(b, src.len() as u32, sc, fc),
            None => Err("no-tree".into()),
        };
        let t_total = r.t_total + t_valid.elapsed(); // host validation is part of the per-file cost
        let outcome = outcome_of(&r.status, &summary);
        let (sha, nodes, depth) = match &r.tree {
            Some(b) => {
                let (n, d) = summary.as_ref().map(|s| (s.nodes, s.max_depth)).unwrap_or((0, 0));
                (tree::sha256_hex(b), n.to_string(), d.to_string())
            }
            None => ("-".into(), "-".into(), "-".into()),
        };
        w_cols = format!(
            "\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}",
            r.status,
            outcome,
            sha,
            nodes,
            depth,
            summary.as_ref().map(|_| "ok".to_string()).unwrap_or_else(|e| e.clone()),
            r.fuel_total,
            r.fuel_parse,
            r.pages_initial,
            r.pages_peak,
            r.t_instantiate.as_nanos(),
            r.t_parse.as_nanos(),
            t_total.as_nanos()
        );
        w_tree = r.tree;
    }

    // native leg
    let mut n_cols = "\t-".repeat(6);
    let mut n_tree: Option<Vec<u8>> = None;
    if mode != "wasm" {
        let t0 = Instant::now();
        let r = if too_big {
            native::NativeResult { status: u32::MAX, tree: None }
        } else {
            native::parse(&langs[&it.grammar], &src)
        };
        let summary = match &r.tree {
            Some(b) => tree::validate(b, src.len() as u32, sc, fc),
            None => Err("no-tree".into()),
        };
        let t = t0.elapsed();
        let status = match r.status {
            tree::ST_OK => "ok".to_string(),
            tree::ST_TRUNC_NODES => "trunc-nodes".into(),
            tree::ST_TRUNC_DEPTH => "trunc-depth".into(),
            u32::MAX => "trunc-size".into(),
            x => format!("fault:status-{x}"),
        };
        let outcome = outcome_of(&status, &summary);
        let (sha, nodes) = match &r.tree {
            Some(b) => (tree::sha256_hex(b), summary.as_ref().map(|s| s.nodes.to_string()).unwrap_or("-".into())),
            None => ("-".into(), "-".into()),
        };
        n_cols = format!(
            "\t{}\t{}\t{}\t{}\t{}\t{}",
            status,
            outcome,
            sha,
            nodes,
            summary.as_ref().map(|_| "ok".to_string()).unwrap_or_else(|e| e.clone()),
            t.as_nanos()
        );
        n_tree = r.tree;
    }

    let (eq, diff) = match (&w_tree, &n_tree) {
        (Some(a), Some(b)) if a == b => ("1".to_string(), "-".to_string()),
        (Some(a), Some(b)) => {
            if let Some(d) = dump {
                let _ = fs::create_dir_all(d);
                let _ = fs::write(d.join(format!("{}.wasm.bin", it.idx)), a);
                let _ = fs::write(d.join(format!("{}.native.bin", it.idx)), b);
            }
            ("0".to_string(), tree::first_diff(a, b))
        }
        _ => ("-".to_string(), "-".to_string()),
    };
    format!("{head}\t{}{w_cols}{n_cols}\t{eq}\t{diff}", if utf8 { 1 } else { 0 })
}
