//! T-wasm leg: wasmi 2.0.0 with fuel metering, a fixed feature set, eager compilation, a
//! store limiter as the page ceiling, and a fresh instance per file (E1 item 2).

use crate::tree::{self, SymbolTable};
use std::time::{Duration, Instant};
use wasmi::{
    CompilationMode, Config, Engine, ExternType, Instance, Module, Store, StoreLimits, StoreLimitsBuilder,
    TrapCode, TypedFunc, ValType,
};

pub const PAGE: u64 = 65_536;
pub const WASM32_MAX_PAGES: u64 = 65_536;
/// Fuel given to the admission instance (A11) and, when unbounded, to a parse.
pub const ADMISSION_FUEL: u64 = 1_000_000_000;
pub const UNBOUNDED_FUEL: u64 = 1 << 60;

/// The host's fixed engine configuration. `lazy` exists only for E0's P4 control: lazy
/// translation charges translation fuel to whichever call first reaches a function.
pub fn engine(lazy: bool, floats: bool) -> Engine {
    let mut c = Config::default();
    c.consume_fuel(true)
        .compilation_mode(if lazy { CompilationMode::LazyTranslation } else { CompilationMode::Eager })
        .allow_start_fn(false)
        .wasm_mutable_global(false)
        .wasm_multi_value(false)
        .wasm_multi_memory(false)
        .wasm_saturating_float_to_int(false)
        .wasm_sign_extension(true)
        .wasm_bulk_memory(true)
        .wasm_reference_types(false)
        .wasm_tail_call(false)
        .wasm_extended_const(false)
        .wasm_custom_page_sizes(false)
        .wasm_wide_arithmetic(false)
        .floats(floats);
    Engine::new(&c)
}

/// A10's closed export set, by name and type.
pub const EXPORTS: [(&str, &[ValType], &[ValType]); 8] = [
    ("osg_abi_version", &[], &[ValType::I32]),
    ("osg_symbols_ptr", &[], &[ValType::I32]),
    ("osg_symbols_len", &[], &[ValType::I32]),
    ("osg_result_ptr", &[], &[ValType::I32]),
    ("osg_result_len", &[], &[ValType::I32]),
    ("osg_alloc_failed", &[], &[ValType::I32]),
    ("osg_alloc", &[ValType::I32], &[ValType::I32]),
    ("osg_parse", &[ValType::I32, ValType::I32], &[ValType::I32]),
];

/// A9 (imports) and A10 (closed, typed exports) on the engine's view of the module.
pub fn check_shape(m: &Module) -> Vec<String> {
    let mut errs = Vec::new();
    for imp in m.imports() {
        errs.push(format!("import-forbidden:{}.{}", imp.module(), imp.name()));
    }
    let mut seen = Vec::new();
    for e in m.exports() {
        let name = e.name().to_string();
        match e.ty() {
            ExternType::Memory(mt) => {
                if name != "memory" {
                    errs.push(format!("exports-mismatch:{name}:memory"));
                }
                if mt.is_64() {
                    errs.push("memory-64".into());
                }
            }
            ExternType::Func(ft) => match EXPORTS.iter().find(|x| x.0 == name) {
                Some((_, p, r)) if ft.params() == *p && ft.results() == *r => {}
                Some(_) => errs.push(format!("exports-mismatch:{name}:type")),
                None => errs.push(format!("exports-mismatch:{name}:extra")),
            },
            _ => errs.push(format!("exports-mismatch:{name}:kind")),
        }
        seen.push(name);
    }
    for (n, _, _) in EXPORTS.iter() {
        if !seen.iter().any(|s| s == n) {
            errs.push(format!("exports-mismatch:{n}:missing"));
        }
    }
    if !seen.iter().any(|s| s == "memory") {
        errs.push("exports-mismatch:memory:missing".into());
    }
    errs
}

pub struct Admission {
    pub t_compile: Duration,
    pub t_shape: Duration,
    pub t_instantiate: Duration,
    pub t_symbols: Duration,
    pub admission_fuel: u64,
    pub abi: u32,
    pub table: Result<SymbolTable, String>,
    pub shape_errors: Vec<String>,
}

/// A9-A11 for one module: compile (parse + validate + translate, eager), shape, then one
/// admission instance that reports the ABI and the symbol table, which is then discarded.
pub fn admit(engine: &Engine, bytes: &[u8]) -> Result<(Module, Admission), String> {
    let t0 = Instant::now();
    let module = Module::new(engine, bytes).map_err(|e| format!("module-invalid:{e}"))?;
    let t1 = Instant::now();
    let shape_errors = check_shape(&module);
    let t2 = Instant::now();
    let mut store = Store::new(engine, StoreLimitsBuilder::new().memory_size(16 * 1024 * 1024 * 64).build());
    store.limiter(|l| l);
    store.set_fuel(ADMISSION_FUEL).map_err(|e| e.to_string())?;
    let inst = Instance::new(&mut store, &module, &[]).map_err(|e| format!("admission-call:{e}"))?;
    let t3 = Instant::now();
    let f = |name: &str| inst.get_typed_func::<(), u32>(&store, name).map_err(|e| format!("{name}:{e}"));
    let abi_fn = f("osg_abi_version")?;
    let sp = f("osg_symbols_ptr")?;
    let sl = f("osg_symbols_len")?;
    let abi = abi_fn.call(&mut store, ()).map_err(|e| format!("admission-call:{e}"))?;
    let ptr = sp.call(&mut store, ()).map_err(|e| format!("admission-call:{e}"))? as usize;
    let len = sl.call(&mut store, ()).map_err(|e| format!("admission-call:{e}"))? as usize;
    let mem = inst.get_memory(&store, "memory").ok_or("no memory")?;
    let data = mem.data(&store);
    let table = data
        .get(ptr..ptr.saturating_add(len))
        .ok_or_else(|| "symbols:out-of-bounds".to_string())
        .and_then(tree::decode_symbols);
    let t4 = Instant::now();
    let admission_fuel = ADMISSION_FUEL - store.get_fuel().unwrap_or(0);
    Ok((
        module,
        Admission {
            t_compile: t1 - t0,
            t_shape: t2 - t1,
            t_instantiate: t3 - t2,
            t_symbols: t4 - t3,
            admission_fuel,
            abi,
            table,
            shape_errors,
        },
    ))
}

#[derive(Default, Clone)]
pub struct WasmResult {
    /// ok | trunc-nodes | trunc-depth | trunc-fuel | trunc-memory | fault:<why>
    pub status: String,
    pub tree: Option<Vec<u8>>,
    pub fuel_total: u64,
    pub fuel_parse: u64,
    pub pages_initial: u64,
    pub pages_peak: u64,
    pub t_instantiate: Duration,
    pub t_parse: Duration,
    pub t_total: Duration,
}

struct Fns {
    alloc: TypedFunc<u32, u32>,
    parse: TypedFunc<(u32, u32), u32>,
    rptr: TypedFunc<(), u32>,
    rlen: TypedFunc<(), u32>,
    failed: TypedFunc<(), u32>,
}

fn fns(inst: &Instance, store: &Store<StoreLimits>) -> Result<Fns, wasmi::Error> {
    Ok(Fns {
        alloc: inst.get_typed_func(store, "osg_alloc")?,
        parse: inst.get_typed_func(store, "osg_parse")?,
        rptr: inst.get_typed_func(store, "osg_result_ptr")?,
        rlen: inst.get_typed_func(store, "osg_result_len")?,
        failed: inst.get_typed_func(store, "osg_alloc_failed")?,
    })
}

/// Classify a trap: fuel exhaustion, memory exhaustion (the shim's flag), or a fault.
fn classify(e: &wasmi::Error, store: &mut Store<StoreLimits>, f: &Fns) -> String {
    if e.as_trap_code() == Some(TrapCode::OutOfFuel) {
        return "trunc-fuel".into();
    }
    // The flag read needs a little fuel of its own; it is not counted in the file's fuel.
    let left = store.get_fuel().unwrap_or(0);
    let _ = store.set_fuel(left.saturating_add(1_000_000));
    match f.failed.call(&mut *store, ()) {
        Ok(1) => "trunc-memory".into(),
        _ => format!("fault:{}", e.as_trap_code().map(|c| format!("{c:?}")).unwrap_or_else(|| e.to_string())),
    }
}

/// One file, one fresh store and instance (the product rule). `fuel` and `max_pages` are
/// the bounds under test; E0's measurement runs use UNBOUNDED_FUEL and WASM32_MAX_PAGES.
pub fn parse_fresh(engine: &Engine, module: &Module, src: &[u8], fuel: u64, max_pages: u64) -> WasmResult {
    let t0 = Instant::now();
    let mut r = WasmResult::default();
    let limits = StoreLimitsBuilder::new().memory_size((max_pages * PAGE) as usize).build();
    let mut store = Store::new(engine, limits);
    store.limiter(|l| l);
    store.set_fuel(fuel).expect("fuel enabled");
    let inst = match Instance::new(&mut store, module, &[]) {
        Ok(i) => i,
        Err(e) => {
            // An initial memory above the ceiling is a memory bound, not a fault.
            r.status = if max_pages < WASM32_MAX_PAGES { "trunc-memory".into() } else { format!("fault:instantiate:{e}") };
            r.t_total = t0.elapsed();
            return r;
        }
    };
    let mem = inst.get_memory(&store, "memory").expect("memory export");
    r.pages_initial = mem.size(&store);
    let f = fns(&inst, &store).expect("A10 checked at admission");
    let t1 = Instant::now();
    r.t_instantiate = t1 - t0;
    let len = src.len() as u32;
    let run = |store: &mut Store<StoreLimits>| -> Result<(u32, u64), wasmi::Error> {
        let ptr = f.alloc.call(&mut *store, len)?;
        mem.write(&mut *store, ptr as usize, src).map_err(wasmi::Error::from)?;
        let before = store.get_fuel().unwrap_or(0);
        let st = f.parse.call(&mut *store, (ptr, len))?;
        Ok((st, before))
    };
    let outcome = run(&mut store);
    let t2 = Instant::now();
    r.t_parse = t2 - t1;
    let after = store.get_fuel().unwrap_or(0);
    r.fuel_total = fuel - after;
    match outcome {
        Ok((st, before)) => {
            r.fuel_parse = before - after;
            r.status = match st {
                tree::ST_OK => "ok".into(),
                tree::ST_TRUNC_NODES => "trunc-nodes".into(),
                tree::ST_TRUNC_DEPTH => "trunc-depth".into(),
                tree::ST_FAULT_PARSE_NULL => "fault:parse-null".into(),
                tree::ST_FAULT_LANGUAGE => "fault:language".into(),
                x => format!("fault:status-{x}"),
            };
            if st == tree::ST_OK {
                // The two result getters are host-protocol calls, not the file's work: they
                // get a small uncounted allowance, as the trap classifier's flag read does.
                // (Phase 2 fix: without it, a budget of exactly w_fuel_total starved them.)
                let _ = store.set_fuel(after.saturating_add(1_000_000));
                let read = (|| -> Result<Vec<u8>, wasmi::Error> {
                    let p = f.rptr.call(&mut store, ())? as usize;
                    let n = f.rlen.call(&mut store, ())? as usize;
                    let d = mem.data(&store);
                    Ok(d.get(p..p.saturating_add(n)).map(|s| s.to_vec()).unwrap_or_default())
                })();
                match read {
                    Ok(b) if !b.is_empty() => r.tree = Some(b),
                    Ok(_) => r.status = "fault:result-out-of-bounds".into(),
                    Err(e) => r.status = format!("fault:result:{e}"),
                }
            }
        }
        Err(e) => {
            r.fuel_parse = 0;
            r.status = classify(&e, &mut store, &f);
        }
    }
    r.pages_peak = mem.size(&store);
    r.t_total = t0.elapsed();
    r
}

/// E0's instance-reuse control (forbidden in the product): one instance for many files.
pub struct Reused {
    store: Store<StoreLimits>,
    inst: Instance,
}

impl Reused {
    pub fn new(engine: &Engine, module: &Module) -> Self {
        let mut store = Store::new(engine, StoreLimitsBuilder::new().memory_size((WASM32_MAX_PAGES * PAGE) as usize).build());
        store.limiter(|l| l);
        store.set_fuel(UNBOUNDED_FUEL).expect("fuel");
        let inst = Instance::new(&mut store, module, &[]).expect("instantiate");
        Reused { store, inst }
    }
    pub fn parse(&mut self, src: &[u8]) -> WasmResult {
        let mut r = WasmResult::default();
        let f = fns(&self.inst, &self.store).expect("exports");
        let mem = self.inst.get_memory(&self.store, "memory").expect("memory");
        let before = self.store.get_fuel().unwrap_or(0);
        let len = src.len() as u32;
        let out = (|| -> Result<u32, wasmi::Error> {
            let ptr = f.alloc.call(&mut self.store, len)?;
            mem.write(&mut self.store, ptr as usize, src).map_err(wasmi::Error::from)?;
            f.parse.call(&mut self.store, (ptr, len))
        })();
        r.fuel_total = before - self.store.get_fuel().unwrap_or(0);
        r.status = match out {
            Ok(0) => {
                let p = f.rptr.call(&mut self.store, ()).unwrap_or(0) as usize;
                let n = f.rlen.call(&mut self.store, ()).unwrap_or(0) as usize;
                r.tree = mem.data(&self.store).get(p..p + n).map(|s| s.to_vec());
                "ok".into()
            }
            Ok(x) => format!("status-{x}"),
            Err(e) => format!("trap:{e}"),
        };
        r.pages_peak = mem.size(&self.store);
        r
    }
}
