from pathlib import Path
import json,hashlib,shutil
b=Path('/tmp/opensip-implementation/component-role-materialization-authoring');p=b/'product';a=Path('/Users/sb/code/opensip-ai/opensip_arch')
raw=(a/'docs/implementation/m3/snapshot-plan-c/cr-1/completion/manifest-schema.completed.v1.json').read_bytes();assert hashlib.sha256(raw).hexdigest()=='343dc51799573bfb04b9cae5c4bfa830892b577d80a0c796c539f4f360faa008';(p/'tools/security/inputs/manifest-schema.json').write_bytes(raw)
f=p/'tools/security/inputs/sources.json';v=json.loads(f.read_text());row=next(x for x in v['files'] if x['path']=='tools/security/inputs/manifest-schema.json');row.update(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest());f.write_text(json.dumps(v,indent=2)+'\n')
f=p/'crates/security/src/component_manifest.rs';s=f.read_text();assert 'fn name_checks(' not in s
start=s.index('    let mut keys = BTreeSet::from([text(&m["name"])]);');stop=s.index('\nfn resolve',start)
old=s[start:stop];checks=old.replace('    for a in m.get("aliases").map(array).unwrap_or(&[]).iter().chain(\n        object(&commands[root])\n            .get("aliases")\n            .map(array)\n            .unwrap_or(&[]),\n    ) {','    for a in m.get("aliases").map(array).unwrap_or(&[]).iter().chain(root_aliases) {')
s=s[:start]+'''    name_checks(m, reserved_names, context,
        object(&commands[root]).get("aliases").map(array).unwrap_or(&[]))
}
// CR-1: all roles reserve their name and manifest aliases. Analyzer also
// reserves its mounted command root aliases, exactly as before.
fn name_checks(m: &BTreeMap<String,V>, reserved_names: &BTreeSet<String>, context: Option<&Context>, root_aliases: &[V]) -> Result<(),Error> {
'''+checks+s[stop:]
s=s.replace('fn tree_checks(p: &BTreeMap<String, V>)', 'fn tree_checks(p: &BTreeMap<String, V>, analyzer: bool)')
s=s.replace('    let e = object(resolve(&by, entry)?);\n    if text(&e["type"]) != "file" || u16::from_str_radix(text(&e["mode"]), 8).unwrap() & 0o111 == 0','''    let e = object(if analyzer { resolve(&by, entry)? } else { *by.get(entry).ok_or(Error::Path)? });
    if text(&e["type"]) != "file" || analyzer && u16::from_str_radix(text(&e["mode"]), 8).unwrap() & 0o111 == 0''')
s=s.replace('    command_checks(m, reserved_names, context)?;','''    let analyzer = text(&m["role"]) == "analyzer";
    if analyzer { command_checks(m, reserved_names, context)?; }
    else { name_checks(m, reserved_names, context, &[])?; }
    if !analyzer && !array(&m["capabilities"]).is_empty() { return Err(Error::Capability); }
    if !analyzer && !array(&m["permissions"]).is_empty() { return Err(Error::Permission); }''',1)
s=s.replace('        tree_checks(p)?;', '        tree_checks(p, analyzer)?;',1)
# Closed role mapping on an already validated manifest, no trust/field-use claim.
s=s.replace('impl Validated {','''impl Validated {
    /// CR-1 role-to-kind table only. Signature, tree capture, closure identity
    /// and field-use admission are separate owners.
    pub(super) fn closure_kind(&self) -> &'static str {
        match text(&object(&self.value)["role"]) {
            "analyzer" => "provider", "toolchain" => "toolchain",
            "stdlib" => "stdlib", "rust-dev-llvm" => "rust-dev-llvm",
            "grammar" => "grammar", _ => unreachable!("closed admitted role"),
        }
    }
''',1)
f.write_text(s)
print('materialization source authored; generation and controls pending')
