//! SyntaxTreeV1 (E0's byte layout; see shim/osg_shim.c), its host validation (E1 item 10),
//! the SymbolTableV1 canonical record (E1 item 5, A11), and small helpers.

use sha2::{Digest, Sha256};

pub const MAX_NODES: u32 = 4_194_304;
pub const MAX_DEPTH: u32 = 4_096;
pub const HDR: usize = 16;
pub const REC: usize = 20;
pub const SYM_ERROR: u16 = 0xFFFF;

pub const F_NAMED: u16 = 1;
pub const F_EXTRA: u16 = 2;
pub const F_ERROR: u16 = 4;
pub const F_MISSING: u16 = 8;

/// Status codes shared by the shim (wasm) and the native serializer.
pub const ST_OK: u32 = 0;
pub const ST_TRUNC_NODES: u32 = 1;
pub const ST_TRUNC_DEPTH: u32 = 2;
pub const ST_FAULT_PARSE_NULL: u32 = 3;
pub const ST_FAULT_LANGUAGE: u32 = 4;

pub fn sha256_hex(b: &[u8]) -> String {
    let d = Sha256::digest(b);
    let mut s = String::with_capacity(64);
    for x in d.iter() {
        s.push_str(&format!("{x:02x}"));
    }
    s
}

/// Native-side writer, the same layout the shim writes.
pub struct Writer {
    pub buf: Vec<u8>,
    pub n: u32,
}

impl Writer {
    pub fn new(hint: usize) -> Self {
        let mut buf = Vec::with_capacity(HDR + REC * hint);
        buf.extend_from_slice(b"OSGT");
        buf.extend_from_slice(&1u32.to_le_bytes());
        buf.extend_from_slice(&0u32.to_le_bytes());
        buf.extend_from_slice(&0u32.to_le_bytes());
        Writer { buf, n: 0 }
    }
    #[allow(clippy::too_many_arguments)]
    pub fn node(&mut self, symbol: u16, field: u16, flags: u16, start: u32, end: u32, children: u32) {
        self.buf.extend_from_slice(&symbol.to_le_bytes());
        self.buf.extend_from_slice(&field.to_le_bytes());
        self.buf.extend_from_slice(&flags.to_le_bytes());
        self.buf.extend_from_slice(&0u16.to_le_bytes());
        self.buf.extend_from_slice(&start.to_le_bytes());
        self.buf.extend_from_slice(&end.to_le_bytes());
        self.buf.extend_from_slice(&children.to_le_bytes());
        self.n += 1;
    }
    pub fn finish(mut self, max_depth: u32) -> Vec<u8> {
        let n = self.n;
        self.buf[8..12].copy_from_slice(&n.to_le_bytes());
        self.buf[12..16].copy_from_slice(&max_depth.to_le_bytes());
        self.buf
    }
}

#[derive(Debug, Default, Clone)]
pub struct TreeSummary {
    pub nodes: u32,
    pub max_depth: u32,
    pub error_nodes: u32,
    pub missing_nodes: u32,
}

impl TreeSummary {
    /// E1 item 10: any ERROR or MISSING node makes the whole file a syntax error.
    pub fn outcome(&self) -> &'static str {
        if self.error_nodes > 0 || self.missing_nodes > 0 {
            "syntax-error"
        } else {
            "parsed"
        }
    }
}

fn u16_at(b: &[u8], o: usize) -> u16 {
    u16::from_le_bytes([b[o], b[o + 1]])
}
fn u32_at(b: &[u8], o: usize) -> u32 {
    u32::from_le_bytes([b[o], b[o + 1], b[o + 2], b[o + 3]])
}

/// Complete host validation of a SyntaxTreeV1 buffer before any use (E1 item 10):
/// header and length; every range inside the input and nested in its parent; siblings in
/// order and non-overlapping; symbols in the table (or ERROR); fields in the table; flags
/// closed; child counts consistent with the preorder; depth and count agreeing with the
/// header and within the bounds.
pub fn validate(b: &[u8], input_len: u32, symbol_count: u32, field_count: u32) -> Result<TreeSummary, String> {
    if b.len() < HDR || &b[0..4] != b"OSGT" {
        return Err("header".into());
    }
    if u32_at(b, 4) != 1 {
        return Err("version".into());
    }
    let count = u32_at(b, 8);
    let hdr_depth = u32_at(b, 12);
    if count == 0 || count > MAX_NODES {
        return Err(format!("count:{count}"));
    }
    if b.len() != HDR + REC * count as usize {
        return Err("length".into());
    }
    // frame: (remaining children, parent start, parent end, last sibling end)
    let mut stack: Vec<(u32, u32, u32, u32)> = Vec::new();
    let mut s = TreeSummary { nodes: count, ..Default::default() };
    for i in 0..count as usize {
        let o = HDR + REC * i;
        let (sym, field, flags, rsv) = (u16_at(b, o), u16_at(b, o + 2), u16_at(b, o + 4), u16_at(b, o + 6));
        let (start, end, children) = (u32_at(b, o + 8), u32_at(b, o + 12), u32_at(b, o + 16));
        if rsv != 0 || flags & !0xF != 0 {
            return Err(format!("node{i}:flags"));
        }
        if !(u32::from(sym) < symbol_count || sym == SYM_ERROR) {
            return Err(format!("node{i}:symbol:{sym}"));
        }
        if u32::from(field) > field_count {
            return Err(format!("node{i}:field:{field}"));
        }
        if start > end || end > input_len {
            return Err(format!("node{i}:range"));
        }
        if flags & F_ERROR != 0 {
            s.error_nodes += 1;
        }
        if flags & F_MISSING != 0 {
            s.missing_nodes += 1;
        }
        if i == 0 {
            if field != 0 {
                return Err("root:field".into());
            }
        } else {
            let top = stack.last_mut().ok_or(format!("node{i}:orphan"))?;
            if top.0 == 0 {
                return Err(format!("node{i}:children"));
            }
            if start < top.1 || end > top.2 {
                return Err(format!("node{i}:outside-parent"));
            }
            if start < top.3 {
                return Err(format!("node{i}:sibling-overlap"));
            }
            top.0 -= 1;
            top.3 = end;
        }
        if children > 0 {
            stack.push((children, start, end, start));
            let d = stack.len() as u32 + 1;
            if d > MAX_DEPTH {
                return Err("depth-bound".into());
            }
            s.max_depth = s.max_depth.max(d);
        } else {
            s.max_depth = s.max_depth.max(stack.len() as u32 + 1);
        }
        while let Some(t) = stack.last() {
            if t.0 == 0 {
                stack.pop();
            } else {
                break;
            }
        }
        if stack.is_empty() && i + 1 != count as usize {
            return Err(format!("node{i}:trailing"));
        }
    }
    if !stack.is_empty() {
        return Err("unterminated".into());
    }
    if s.max_depth != hdr_depth {
        return Err(format!("depth:{}!={hdr_depth}", s.max_depth));
    }
    Ok(s)
}

/// First differing node index between two SyntaxTreeV1 buffers (diagnostics for P3).
pub fn first_diff(a: &[u8], b: &[u8]) -> String {
    if a.len() < HDR || b.len() < HDR {
        return "short".into();
    }
    if a[..HDR] != b[..HDR] {
        return format!("header(n={}/{},d={}/{})", u32_at(a, 8), u32_at(b, 8), u32_at(a, 12), u32_at(b, 12));
    }
    let n = (a.len().min(b.len()) - HDR) / REC;
    for i in 0..n {
        let o = HDR + REC * i;
        if a[o..o + REC] != b[o..o + REC] {
            return format!("node{i}");
        }
    }
    "tail".into()
}

// ---------------------------------------------------------------------------------------
// SymbolTableV1 (A11): {schemaVersion: 1, grammarId, languageAbi, symbols: [{id, name,
// named, visible}], fields: [{id, name}]}, canonical JSON (sorted keys, no whitespace,
// UTF-8, the CAN:67-74 string escaping), raw SHA-256.

pub struct SymbolTable {
    pub language_abi: u32,
    pub symbols: Vec<(String, bool, bool)>,
    pub fields: Vec<String>,
}

const MAX_SYMBOLS: u32 = 65_535;
const MAX_FIELDS: u32 = 65_535;
const MAX_NAME: usize = 1_024;

fn take<'a>(b: &'a [u8], p: &mut usize, n: usize) -> Result<&'a [u8], String> {
    let e = p.checked_add(n).ok_or("symbols:len")?;
    let s = b.get(*p..e).ok_or("symbols:eof")?;
    *p = e;
    Ok(s)
}

fn name_of(raw: &[u8]) -> Result<String, String> {
    if raw.len() > MAX_NAME {
        return Err("symbols:name-bound".into());
    }
    String::from_utf8(raw.to_vec()).map_err(|_| "symbols:name-utf8".to_string())
}

/// Decode the shim's symbol blob within A11's bounds.
pub fn decode_symbols(b: &[u8]) -> Result<SymbolTable, String> {
    if b.len() < 20 || &b[0..4] != b"OSGS" || u32_at(b, 4) != 1 {
        return Err("symbols:header".into());
    }
    let abi = u32_at(b, 8);
    let sc = u32_at(b, 12);
    let fc = u32_at(b, 16);
    if sc > MAX_SYMBOLS || fc > MAX_FIELDS {
        return Err("symbols:bounds".into());
    }
    let mut p = 20usize;
    let mut symbols = Vec::with_capacity(sc as usize);
    for _ in 0..sc {
        let h = take(b, &mut p, 4)?;
        let (named, visible, n) = (h[0], h[1], u16::from_le_bytes([h[2], h[3]]) as usize);
        if named > 1 || visible > 1 {
            return Err("symbols:flag".into());
        }
        symbols.push((name_of(take(b, &mut p, n)?)?, named == 1, visible == 1));
    }
    let mut fields = Vec::with_capacity(fc as usize);
    for _ in 0..fc {
        let h = take(b, &mut p, 2)?;
        let n = u16::from_le_bytes([h[0], h[1]]) as usize;
        fields.push(name_of(take(b, &mut p, n)?)?);
    }
    if p != b.len() {
        return Err("symbols:trailing".into());
    }
    Ok(SymbolTable { language_abi: abi, symbols, fields })
}

fn json_str(out: &mut String, s: &str) {
    out.push('"');
    for c in s.chars() {
        match c {
            '"' => out.push_str("\\\""),
            '\\' => out.push_str("\\\\"),
            '\n' => out.push_str("\\n"),
            '\r' => out.push_str("\\r"),
            '\t' => out.push_str("\\t"),
            '\u{8}' => out.push_str("\\b"),
            '\u{c}' => out.push_str("\\f"),
            c if (c as u32) < 0x20 => out.push_str(&format!("\\u{:04x}", c as u32)),
            c => out.push(c),
        }
    }
    out.push('"');
}

/// Canonical SymbolTableV1 bytes. Keys sort as: fields, grammarId, languageAbi,
/// schemaVersion, symbols; and id, name, named, visible.
pub fn symbol_table_v1(grammar_id: &str, t: &SymbolTable) -> String {
    let mut o = String::new();
    o.push_str("{\"fields\":[");
    for (i, f) in t.fields.iter().enumerate() {
        if i > 0 {
            o.push(',');
        }
        o.push_str(&format!("{{\"id\":{},\"name\":", i + 1));
        json_str(&mut o, f);
        o.push('}');
    }
    o.push_str("],\"grammarId\":");
    json_str(&mut o, grammar_id);
    o.push_str(&format!(",\"languageAbi\":{},\"schemaVersion\":1,\"symbols\":[", t.language_abi));
    for (i, (name, named, visible)) in t.symbols.iter().enumerate() {
        if i > 0 {
            o.push(',');
        }
        o.push_str(&format!("{{\"id\":{i},\"name\":"));
        json_str(&mut o, name);
        o.push_str(&format!(",\"named\":{named},\"visible\":{visible}}}"));
    }
    o.push_str("]}");
    o
}

/// Deterministic shuffle (splitmix64 + Fisher-Yates), so P4's orders are reproducible.
pub fn shuffle<T>(v: &mut [T], seed: u64) {
    let mut x = seed;
    let mut next = || {
        x = x.wrapping_add(0x9E37_79B9_7F4A_7C15);
        let mut z = x;
        z = (z ^ (z >> 30)).wrapping_mul(0xBF58_476D_1CE4_E5B9);
        z = (z ^ (z >> 27)).wrapping_mul(0x94D0_49BB_1331_11EB);
        z ^ (z >> 31)
    };
    for i in (1..v.len()).rev() {
        let j = (next() % (i as u64 + 1)) as usize;
        v.swap(i, j);
    }
}
