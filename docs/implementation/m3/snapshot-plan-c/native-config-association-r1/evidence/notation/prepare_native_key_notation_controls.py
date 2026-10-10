from pathlib import Path
import hashlib,json
root=Path('/tmp/opensip-implementation/native-config-key-notation-controls-2026-10-10'); assert not root.exists();root.mkdir()
p=Path('/Users/sb/code/opensip-ai/opensip/crates/identity/src/canonical.rs'); b=p.read_bytes();(root/'canonical.rs').write_bytes(b)
(root/'source-pin.json').write_text(json.dumps(dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),purpose='Exact existing canonical string primitive copied read-only for authoring controls; no product or law change'),indent=2)+'\n')
(root/'key_notation.rs').write_text(r'''extern crate alloc;
mod canonical;
use canonical::Value;
use std::io::{self, Read};
fn render(path: &Value) -> Result<String, &'static str> {
    let Value::Array(parts) = path else { return Err("path must be an array") };
    if !matches!(parts.first(), Some(Value::String(_))) { return Err("first segment must be named") }
    let mut out = String::new();
    for part in parts {
        match part {
            Value::String(s) => {
                if !out.is_empty() { out.push('.'); }
                if !s.is_empty() && s.bytes().all(|b| b.is_ascii_alphanumeric() || b == b'_' || b == b'-') {
                    out.push_str(s);
                } else {
                    let encoded = canonical::encode(&Value::String(s.clone())).map_err(|_| "canonical bound")?;
                    out.push_str(std::str::from_utf8(&encoded).map_err(|_| "encoding")?);
                }
            }
            Value::Integer(n) if n.get() >= 0 => { out.push('['); out.push_str(&n.get().to_string()); out.push(']'); }
            _ => return Err("segment must be a name or nonnegative actual list index"),
        }
    }
    Ok(out)
}
fn main() {
    let mut raw = Vec::new(); io::stdin().read_to_end(&mut raw).unwrap();
    let paths = canonical::parse(&raw).expect("authoring input JSON");
    let Value::Array(paths) = paths else { panic!("authoring path population must be an array") };
    let output: Vec<_> = paths.iter().map(|p| Value::String(render(p).expect("authoring typed path"))).collect();
    let bytes = canonical::encode(&Value::Array(output)).expect("authoring output bounds");
    use std::io::Write; io::stdout().write_all(&bytes).unwrap();
}
''')
print(root)
