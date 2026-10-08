from pathlib import Path
p=Path('/tmp/opensip-implementation/o1b-authoring-r1/product/crates/operability/src/emit.rs');s=p.read_text()
s=s.replace('    encode_line_into(\n        stamp,\n        name,\n        level,','    encode_line_into(\n        LineHeader { stamp, name, level },',1)
s=s.replace('fn encode_line_into(\n    stamp: &[u8; 24],\n    name: &str,\n    level: Level,','''struct LineHeader<'a> {
    stamp: &'a [u8; 24],
    name: &'a str,
    level: Level,
}

fn encode_line_into(
    header: LineHeader<'_>,''',1)
s=s.replace('    out.clear();\n    out.push(b\'{\');','    let LineHeader { stamp, name, level } = header;\n    out.clear();\n    out.push(b\'{\');',1)
s=s.replace('    let bytes = encode_line_into(\n        &stamp,\n        LogLossCounted::NAME,\n        LogLossCounted::LEVEL,','    let bytes = encode_line_into(\n        LineHeader { stamp: &stamp, name: LogLossCounted::NAME, level: LogLossCounted::LEVEL },',1)
p.write_text(s)
