//! A small, independent reader of the WebAssembly binary format (no wasmi, no wasmparser),
//! so P2 (zero imports) and the A9/A10 shape checks have a second witness besides the engine.

#[derive(Debug, Default)]
pub struct Summary {
    pub imports: Vec<(String, String, u8)>,
    pub exports: Vec<(String, u8, u32)>,
    pub func_types: Vec<(Vec<u8>, Vec<u8>)>,
    pub defined_func_types: Vec<u32>,
    pub memories: Vec<(u8, u64, Option<u64>)>, // (limits flag, min pages, max pages)
    pub tables: u32,
    pub globals: u32,
    pub start: Option<u32>,
    pub data_segments: u32,
    pub data_bytes: u64,
    pub code_bodies: u32,
    pub custom: Vec<(String, usize)>,
    pub target_features: Vec<String>,
}

struct R<'a> {
    b: &'a [u8],
    p: usize,
}

impl<'a> R<'a> {
    fn u8(&mut self) -> Result<u8, String> {
        let v = *self.b.get(self.p).ok_or("eof")?;
        self.p += 1;
        Ok(v)
    }
    fn leb(&mut self) -> Result<u64, String> {
        let (mut v, mut s) = (0u64, 0u32);
        loop {
            let x = self.u8()?;
            v |= u64::from(x & 0x7f) << s;
            if x & 0x80 == 0 {
                return Ok(v);
            }
            s += 7;
            if s > 63 {
                return Err("leb overflow".into());
            }
        }
    }
    fn sleb(&mut self) -> Result<i64, String> {
        let (mut v, mut s) = (0i64, 0u32);
        loop {
            let x = self.u8()?;
            v |= i64::from(x & 0x7f) << s;
            s += 7;
            if x & 0x80 == 0 {
                if s < 64 && x & 0x40 != 0 {
                    v |= -1i64 << s;
                }
                return Ok(v);
            }
            if s > 63 {
                return Err("sleb overflow".into());
            }
        }
    }
    fn bytes(&mut self, n: usize) -> Result<&'a [u8], String> {
        let e = self.p.checked_add(n).ok_or("len")?;
        let s = self.b.get(self.p..e).ok_or("eof")?;
        self.p = e;
        Ok(s)
    }
    fn name(&mut self) -> Result<String, String> {
        let n = self.leb()? as usize;
        String::from_utf8(self.bytes(n)?.to_vec()).map_err(|_| "name not utf-8".into())
    }
    fn limits(&mut self) -> Result<(u8, u64, Option<u64>), String> {
        let f = self.u8()?;
        let min = self.leb()?;
        let max = if f & 1 != 0 { Some(self.leb()?) } else { None };
        Ok((f, min, max))
    }
    fn const_expr(&mut self) -> Result<(), String> {
        loop {
            match self.u8()? {
                0x0b => return Ok(()),
                0x41 | 0x42 => {
                    self.sleb()?;
                }
                0x23 => {
                    self.leb()?;
                }
                op => return Err(format!("const expr opcode {op:#x}")),
            }
        }
    }
}

pub fn read(b: &[u8]) -> Result<Summary, String> {
    if b.len() < 8 || &b[0..4] != b"\0asm" || b[4..8] != [1, 0, 0, 0] {
        return Err("not a wasm 1.0 binary".into());
    }
    let mut s = Summary::default();
    let mut r = R { b, p: 8 };
    while r.p < b.len() {
        let id = r.u8()?;
        let size = r.leb()? as usize;
        let body = r.bytes(size)?;
        let mut q = R { b: body, p: 0 };
        match id {
            0 => {
                let name = q.name()?;
                if name == "target_features" {
                    let n = q.leb()?;
                    for _ in 0..n {
                        let prefix = q.u8()? as char;
                        let f = q.name()?;
                        s.target_features.push(format!("{prefix}{f}"));
                    }
                }
                s.custom.push((name, size));
            }
            1 => {
                for _ in 0..q.leb()? {
                    if q.u8()? != 0x60 {
                        return Err("type form".into());
                    }
                    let np = q.leb()? as usize;
                    let p = q.bytes(np)?.to_vec();
                    let nr = q.leb()? as usize;
                    let rr = q.bytes(nr)?.to_vec();
                    s.func_types.push((p, rr));
                }
            }
            2 => {
                for _ in 0..q.leb()? {
                    let m = q.name()?;
                    let n = q.name()?;
                    let kind = q.u8()?;
                    match kind {
                        0 => {
                            q.leb()?;
                        }
                        1 => {
                            q.u8()?;
                            q.limits()?;
                        }
                        2 => {
                            q.limits()?;
                        }
                        3 => {
                            q.u8()?;
                            q.u8()?;
                        }
                        _ => return Err("import kind".into()),
                    }
                    s.imports.push((m, n, kind));
                }
            }
            3 => {
                for _ in 0..q.leb()? {
                    s.defined_func_types.push(q.leb()? as u32);
                }
            }
            4 => {
                let n = q.leb()?;
                s.tables = n as u32;
            }
            5 => {
                for _ in 0..q.leb()? {
                    s.memories.push(q.limits()?);
                }
            }
            6 => {
                s.globals = q.leb()? as u32;
            }
            7 => {
                for _ in 0..q.leb()? {
                    let n = q.name()?;
                    let k = q.u8()?;
                    let i = q.leb()? as u32;
                    s.exports.push((n, k, i));
                }
            }
            8 => s.start = Some(q.leb()? as u32),
            10 => {
                s.code_bodies = q.leb()? as u32; // float use is witnessed by the engine (admit)
            }
            11 => {
                let n = q.leb()?;
                s.data_segments = n as u32;
                for _ in 0..n {
                    let flags = q.leb()?;
                    match flags {
                        0 => q.const_expr()?,
                        1 => {}
                        2 => {
                            q.leb()?;
                            q.const_expr()?
                        }
                        _ => return Err("data flags".into()),
                    }
                    let len = q.leb()? as usize;
                    q.bytes(len)?;
                    s.data_bytes += len as u64;
                }
            }
            9 | 12 => {}
            _ => return Err(format!("unknown section {id}")),
        }
    }
    Ok(s)
}

/// The signature of a function export as "[params]->[results]" with i32/i64/f32/f64 names.
pub fn export_sig(s: &Summary, func_index: u32) -> Option<String> {
    let imported_funcs = s.imports.iter().filter(|i| i.2 == 0).count() as u32;
    let local = func_index.checked_sub(imported_funcs)?;
    let ty = *s.defined_func_types.get(local as usize)?;
    let (p, r) = s.func_types.get(ty as usize)?;
    let name = |v: &u8| match v {
        0x7f => "i32",
        0x7e => "i64",
        0x7d => "f32",
        0x7c => "f64",
        _ => "?",
    };
    Some(format!(
        "[{}]->[{}]",
        p.iter().map(name).collect::<Vec<_>>().join(","),
        r.iter().map(name).collect::<Vec<_>>().join(",")
    ))
}
