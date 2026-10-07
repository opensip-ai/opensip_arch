//! Complete structural manifest owner over captured bytes. External host context
//! remains a custody premise; this produces no runtime or artifact authority.
use crate::metadata_versions::{Constraint, Version};
use opensip_identity::JsonValue as V;
use std::collections::{BTreeMap, BTreeSet};
#[path = "generated/component_manifest_shape.rs"]
mod generated;
#[derive(Debug, PartialEq, Eq)]
pub(super) enum Error {
    Parse,
    Schema,
    Command,
    Path,
    Configuration,
    Capability,
    Permission,
    Dependency,
    Compatibility,
    Exception,
}
#[derive(Clone)]
pub(super) struct LiveName {
    pub(super) stable_id: String,
    pub(super) provenance: V,
    pub(super) names: BTreeSet<String>,
}
#[derive(Clone, Default)]
pub(super) struct Context {
    pub(super) approved_exceptions: BTreeSet<String>,
    pub(super) host_classifications: BTreeMap<String, String>,
    pub(super) live_names: Vec<LiveName>,
    pub(super) reserved_names: BTreeSet<String>,
}
pub(super) struct Validated {
    value: V,
}
impl Validated {
    /// CR-1 role-to-kind table only. Signature, tree capture, closure identity
    /// and field-use admission are separate owners.
    pub(super) fn closure_kind(&self) -> &'static str {
        match text(&object(&self.value)["role"]) {
            "analyzer" => "provider",
            "toolchain" => "toolchain",
            "stdlib" => "stdlib",
            "rust-dev-llvm" => "rust-dev-llvm",
            "grammar" => "grammar",
            _ => unreachable!("closed admitted role"),
        }
    }

    pub(super) fn value(&self) -> &V {
        &self.value
    }
}
// Inventory-only body validity. This is not host admission and cannot be
// converted into Validated without executing the full host checks.
pub(super) struct InventoryBody {
    value: V,
}
impl InventoryBody {
    pub(super) fn value(&self) -> &V {
        &self.value
    }
}
fn object(v: &V) -> &BTreeMap<String, V> {
    let V::Object(o) = v else {
        unreachable!("shape checked")
    };
    o
}
fn array(v: &V) -> &[V] {
    let V::Array(a) = v else {
        unreachable!("shape checked")
    };
    a
}
fn text(v: &V) -> &str {
    let V::String(s) = v else {
        unreachable!("shape checked")
    };
    s
}
fn int(v: &V) -> i128 {
    let V::Integer(n) = v else {
        unreachable!("shape checked")
    };
    n.get()
}
fn boolean(v: &V) -> bool {
    let V::Bool(b) = v else {
        unreachable!("shape checked")
    };
    *b
}
fn strings(v: &V) -> BTreeSet<&str> {
    array(v).iter().map(text).collect()
}
fn token(s: &str) -> bool {
    !s.is_empty()
        && s.bytes()
            .all(|b| b.is_ascii_lowercase() || b.is_ascii_digit() || b == b'-')
}
fn uuid(s: &str) -> bool {
    s.len() == 36
        && s.bytes().enumerate().all(|(i, b)| {
            if [8, 13, 18, 23].contains(&i) {
                b == b'-'
            } else {
                b.is_ascii_digit() || (b'a'..=b'f').contains(&b)
            }
        })
}
fn hex(s: &str) -> bool {
    s.len() == 64
        && s.bytes()
            .all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b))
}
fn version(s: &str) -> bool {
    Version::parse(s).is_some()
}
fn mode(s: &str) -> bool {
    s.len() == 4 && s.starts_with('0') && s.bytes().all(|b| (b'0'..=b'7').contains(&b))
}
fn flag(s: &str) -> bool {
    s.strip_prefix("--")
        .is_some_and(|s| !s.is_empty() && s.as_bytes()[0].is_ascii_lowercase() && token(s))
}
fn config_key(s: &str) -> bool {
    !s.is_empty()
        && s.as_bytes()[0].is_ascii_lowercase()
        && s.bytes().all(|b| b.is_ascii_alphanumeric() || b == b'_')
}
// Every uniqueItems site in this exact schema has string-only items.
fn unique(a: &[V]) -> bool {
    let mut seen = BTreeSet::new();
    a.iter().all(|v| {
        if let V::String(s) = v {
            seen.insert(s)
        } else {
            false
        }
    })
}
fn bounded(v: &V) -> bool {
    match v {
        V::Array(a) => a.len() <= 100_000 && a.iter().all(bounded),
        V::Object(o) => o.values().all(bounded),
        V::Integer(n) => i64::try_from(n.get()).is_ok(),
        _ => true,
    }
}
fn path_ok(p: &str) -> bool {
    let b = p.as_bytes();
    if p.is_empty()
        || p.len() > 1024
        || p.starts_with('/')
        || p.contains(['\\', '\0'])
        || b.len() >= 2 && b[0].is_ascii_alphabetic() && b[1] == b':'
        || !crate::metadata_unicode15::is_nfc(p)
    {
        return false;
    }
    p.split('/').all(|segment| {
        if matches!(segment, "" | "." | "..") || segment.ends_with(['.', ' ']) {
            return false;
        }
        // Reserved stems contain no ASCII I or S. Unicode15 upper mappings
        // to their alphabet introduce no extra non-ASCII aliases (fixture proof).
        let stem = segment.split('.').next().unwrap().to_ascii_uppercase();
        !["CON", "PRN", "AUX", "NUL"].contains(&stem.as_str())
            && !(stem.len() == 4
                && (stem.starts_with("COM") || stem.starts_with("LPT"))
                && (b'1'..=b'9').contains(&stem.as_bytes()[3]))
    })
}
fn parent(p: &str) -> &str {
    p.rsplit_once('/').map_or("", |(p, _)| p)
}
fn command_checks(
    m: &BTreeMap<String, V>,
    reserved_names: &BTreeSet<String>,
    context: Option<&Context>,
) -> Result<(), Error> {
    let commands = array(&m["commands"]);
    let roots: Vec<_> = commands
        .iter()
        .enumerate()
        .filter(|(_, c)| !object(c).contains_key("parent"))
        .map(|(i, _)| i)
        .collect();
    if roots.len() != 1 {
        return Err(Error::Command);
    }
    let root = roots[0];
    if object(&commands[root])["name"] != m["name"] {
        return Err(Error::Command);
    }
    let mut names: BTreeMap<&str, Vec<usize>> = BTreeMap::new();
    let mut scopes: BTreeMap<Option<&str>, BTreeSet<&str>> = BTreeMap::new();
    for (i, c) in commands.iter().enumerate() {
        let c = object(c);
        names.entry(text(&c["name"])).or_default().push(i);
        let scope = scopes.entry(c.get("parent").map(text)).or_default();
        if !scope.insert(text(&c["name"])) {
            return Err(Error::Command);
        }
        for a in c.get("aliases").map(array).unwrap_or(&[]) {
            if !scope.insert(text(a)) {
                return Err(Error::Command);
            }
        }
        let mut flags = BTreeSet::new();
        for o in c.get("options").map(array).unwrap_or(&[]) {
            let o = object(o);
            if !flags.insert(text(&o["flag"])) {
                return Err(Error::Command);
            }
            if let Some(default) = o.get("default") {
                let values = if boolean(&o["repeatable"]) {
                    let V::Array(values) = default else {
                        return Err(Error::Command);
                    };
                    values.as_slice()
                } else {
                    std::slice::from_ref(default)
                };
                if !values.iter().all(|v| {
                    matches!(
                        (text(&o["valueKind"]), v),
                        ("boolean", V::Bool(_))
                            | ("integer", V::Integer(_))
                            | ("string" | "path", V::String(_))
                    )
                }) {
                    return Err(Error::Command);
                }
            }
        }
        let args = c.get("args").map(array).unwrap_or(&[]);
        let mut argnames = BTreeSet::new();
        let mut optional = false;
        for (j, a) in args.iter().enumerate() {
            let a = object(a);
            if !argnames.insert(text(&a["name"]))
                || boolean(&a["variadic"]) && j + 1 != args.len()
                || optional && boolean(&a["required"])
            {
                return Err(Error::Command);
            }
            optional |= !boolean(&a["required"]);
        }
    }
    for i in 0..commands.len() {
        let mut seen = BTreeSet::new();
        let mut current = i;
        loop {
            if !seen.insert(current) || seen.len() > 32 {
                return Err(Error::Command);
            }
            let Some(p) = object(&commands[current]).get("parent") else {
                break;
            };
            let parents = names.get(text(p)).ok_or(Error::Command)?;
            if parents.len() != 1 {
                return Err(Error::Command);
            }
            current = parents[0];
        }
    }
    name_checks(
        m,
        reserved_names,
        context,
        object(&commands[root])
            .get("aliases")
            .map(array)
            .unwrap_or(&[]),
    )
}
// CR-1: all roles reserve their name and manifest aliases. Analyzer also
// reserves its mounted command root aliases, exactly as before.
fn name_checks(
    m: &BTreeMap<String, V>,
    reserved_names: &BTreeSet<String>,
    context: Option<&Context>,
    root_aliases: &[V],
) -> Result<(), Error> {
    let mut keys = BTreeSet::from([text(&m["name"])]);
    for a in m
        .get("aliases")
        .map(array)
        .unwrap_or(&[])
        .iter()
        .chain(root_aliases)
    {
        if !keys.insert(text(a)) {
            return Err(Error::Command);
        }
    }
    if keys.iter().any(|s| reserved_names.contains(*s)) {
        return Err(Error::Command);
    }
    for live in context.map_or(&[][..], |c| c.live_names.as_slice()) {
        if (live.stable_id.as_str(), &live.provenance) != (text(&m["stableId"]), &m["provenance"])
            && keys.iter().any(|s| live.names.contains(*s))
        {
            return Err(Error::Command);
        }
    }
    Ok(())
}
fn resolve<'a>(by: &BTreeMap<&str, &'a V>, path: &str) -> Result<&'a V, Error> {
    let mut path = path.to_owned();
    let mut seen = BTreeSet::new();
    loop {
        if !seen.insert(path.clone()) {
            return Err(Error::Path);
        }
        let e = *by.get(path.as_str()).ok_or(Error::Path)?;
        let row = object(e);
        if text(&row["type"]) != "symlink" {
            return Ok(e);
        }
        let dir = parent(&path);
        let target = text(&row["target"]);
        path = if dir.is_empty() {
            target.to_owned()
        } else {
            format!("{dir}/{target}")
        };
    }
}
fn tree_checks(p: &BTreeMap<String, V>, analyzer: bool) -> Result<(), Error> {
    let mut by = BTreeMap::new();
    let mut folded = BTreeSet::new();
    for e in array(&object(&p["tree"])["entries"]) {
        let row = object(e);
        let path = text(&row["path"]);
        if !path_ok(path)
            || by.insert(path, e).is_some()
            || !folded.insert(crate::metadata_unicode15::normalize(
                &crate::metadata_casefold15::fold(path),
            ))
        {
            return Err(Error::Path);
        }
        if text(&row["type"]) == "symlink" && !path_ok(text(&row["target"])) {
            return Err(Error::Path);
        }
    }
    for (path, e) in &by {
        let dir = parent(path);
        if !dir.is_empty()
            && by
                .get(dir)
                .is_none_or(|e| text(&object(e)["type"]) != "dir")
        {
            return Err(Error::Path);
        }
        if text(&object(e)["type"]) == "symlink" {
            resolve(&by, path)?;
        }
    }
    let entry = text(&p["entrypoint"]);
    if !path_ok(entry) {
        return Err(Error::Path);
    }
    let e = object(if analyzer {
        resolve(&by, entry)?
    } else {
        *by.get(entry).ok_or(Error::Path)?
    });
    if text(&e["type"]) != "file"
        || analyzer && u16::from_str_radix(text(&e["mode"]), 8).unwrap() & 0o111 == 0
    {
        return Err(Error::Path);
    }
    Ok(())
}
fn config_ranges(node: &V) -> bool {
    let n = object(node);
    if text(&n["type"]) == "object" {
        let p = object(&n["properties"]);
        if !strings(&n["required"]).iter().all(|k| p.contains_key(*k))
            || !p.values().all(config_ranges)
        {
            return false;
        }
    } else if text(&n["type"]) == "array" && !config_ranges(&n["items"]) {
        return false;
    }
    for (lo, hi) in [
        ("minimum", "maximum"),
        ("minItems", "maxItems"),
        ("minLength", "maxLength"),
    ] {
        if let (Some(lo), Some(hi)) = (n.get(lo), n.get(hi))
            && int(lo) > int(hi)
        {
            return false;
        }
    }
    true
}
fn config_checks(m: &BTreeMap<String, V>, context: Option<&Context>) -> Result<(), Error> {
    let Some(c) = m.get("configuration") else {
        return Ok(());
    };
    let c = object(c);
    let node = object(&c["schema"]);
    if c["namespace"] != m["name"] || text(&node["type"]) != "object" {
        return Err(Error::Configuration);
    }
    let classifications = object(&c["classifications"]);
    let properties = object(&node["properties"]);
    if classifications.keys().ne(properties.keys())
        || context.is_some_and(|context| {
            classifications.len() != context.host_classifications.len()
                || !classifications.iter().all(|(k, v)| {
                    context
                        .host_classifications
                        .get(k)
                        .is_some_and(|want| want == text(v))
                })
        })
        || !config_ranges(&c["schema"])
    {
        return Err(Error::Configuration);
    }
    Ok(())
}
pub(super) fn validate(raw: &[u8], context: &Context) -> Result<Validated, Error> {
    validate_inner(raw, &context.reserved_names, Some(context)).map(|value| Validated { value })
}
pub(super) fn validate_inventory(
    raw: &[u8],
    reserved_names: &BTreeSet<String>,
) -> Result<InventoryBody, Error> {
    validate_inner(raw, reserved_names, None).map(|value| InventoryBody { value })
}
fn validate_inner(
    raw: &[u8],
    reserved_names: &BTreeSet<String>,
    context: Option<&Context>,
) -> Result<V, Error> {
    let value = super::metadata::parse(raw).map_err(|_| Error::Parse)?;
    if !bounded(&value) || !generated::shape(&value) {
        return Err(Error::Schema);
    }
    let m = object(&value);
    let analyzer = text(&m["role"]) == "analyzer";
    if analyzer {
        command_checks(m, reserved_names, context)?;
    } else {
        name_checks(m, reserved_names, context, &[])?;
    }
    if !analyzer && !array(&m["capabilities"]).is_empty() {
        return Err(Error::Capability);
    }
    if !analyzer && !array(&m["permissions"]).is_empty() {
        return Err(Error::Permission);
    }
    let mut platforms = BTreeSet::new();
    for p in array(&m["platforms"]) {
        let p = object(p);
        if !platforms.insert((text(&p["os"]), text(&p["arch"]))) {
            return Err(Error::Path);
        }
        tree_checks(p, analyzer)?;
    }
    let mut capabilities = BTreeSet::new();
    for c in array(&m["capabilities"]) {
        if !capabilities.insert(text(&object(c)["capabilityId"])) {
            return Err(Error::Capability);
        }
    }
    if capabilities.contains("typescript.reachability")
        && !capabilities.contains("typescript.calls")
    {
        return Err(Error::Capability);
    }
    let mut permissions = BTreeSet::new();
    for p in array(&m["permissions"]) {
        if !permissions.insert(text(&object(p)["permission"])) {
            return Err(Error::Permission);
        }
    }
    let mut dependencies = BTreeSet::new();
    for d in array(&m["dependencies"]) {
        let d = object(d);
        if !dependencies.insert(text(&d["stableId"]))
            || d["stableId"] == m["stableId"]
            || !Constraint::parse(&d["versionConstraint"])
                .unwrap()
                .nonempty()
        {
            return Err(Error::Dependency);
        }
    }
    let compat = object(&m["compatibility"]);
    if !Constraint::parse(&compat["hostCore"]).unwrap().nonempty()
        || compat["manifest"] != m["manifestSchemaVersion"]
    {
        return Err(Error::Compatibility);
    }
    let mut exceptions = BTreeMap::new();
    for p in m.get("prerequisites").map(array).unwrap_or(&[]) {
        let p = object(p);
        let key = text(&p["exceptionApprovalRef"]);
        if !path_ok(text(&p["doctorContract"]))
            || context.is_some_and(|context| !context.approved_exceptions.contains(key))
            || exceptions.insert(key, p).is_some()
        {
            return Err(Error::Exception);
        }
    }
    for r in object(&m["declarations"]).values() {
        let r = object(r);
        if let Some(path) = r.get("path") {
            if !path_ok(text(path)) {
                return Err(Error::Path);
            }
        } else if exceptions
            .get(text(&r["exceptionApprovalRef"]))
            .is_none_or(|p| p["typedAbsenceBehavior"] != r["typedAbsenceBehavior"])
        {
            return Err(Error::Exception);
        }
    }
    config_checks(m, context)?;
    Ok(value)
}

#[cfg(test)]
mod tests {
    use super::*;
    fn bytes(v: &V) -> Vec<u8> {
        let s = text(v);
        (0..s.len())
            .step_by(2)
            .map(|i| u8::from_str_radix(&s[i..i + 2], 16).unwrap())
            .collect()
    }
    fn context(v: &V) -> Context {
        let o = object(v);
        Context {
            approved_exceptions: o
                .get("approvedExceptions")
                .map(|v| array(v).iter().map(|v| text(v).to_owned()).collect())
                .unwrap_or_default(),
            reserved_names: o
                .get("reservedNames")
                .map(|v| array(v).iter().map(|v| text(v).to_owned()).collect())
                .unwrap_or_default(),
            host_classifications: o
                .get("hostClassificationMap")
                .map(|v| {
                    object(v)
                        .iter()
                        .map(|(k, v)| (k.clone(), text(v).to_owned()))
                        .collect()
                })
                .unwrap_or_default(),
            live_names: o
                .get("liveNames")
                .map(|v| {
                    array(v)
                        .iter()
                        .map(|v| {
                            let v = object(v);
                            LiveName {
                                stable_id: text(&v["stableId"]).to_owned(),
                                provenance: v["provenance"].clone(),
                                names: array(&v["names"])
                                    .iter()
                                    .map(|v| text(v).to_owned())
                                    .collect(),
                            }
                        })
                        .collect()
                })
                .unwrap_or_default(),
        }
    }
    fn cr1_object(v: &mut V) -> &mut BTreeMap<String, V> {
        let V::Object(m) = v else { panic!() };
        m
    }
    fn cr1_baseline() -> V {
        let line = include_bytes!("../tests/fixtures/manifest268-semantic.ndjson")
            .split(|b| *b == b'\n')
            .find(|b| !b.is_empty())
            .unwrap();
        let q = crate::trust::metadata::parse(line).unwrap();
        assert_eq!(text(&object(&q)["label"]), "POS/full-security");
        crate::trust::metadata::parse(&bytes(&object(&q)["raw"])).unwrap()
    }
    fn cr1_body(role: &str) -> V {
        let mut v = cr1_baseline();
        let m = cr1_object(&mut v);
        m.insert("role".into(), V::String(role.into()));
        if role != "analyzer" {
            m.remove("commands");
            m.insert("capabilities".into(), V::Array(vec![]));
            m.insert("permissions".into(), V::Array(vec![]));
        }
        v
    }
    fn cr1_validate(v: &V, c: &Context) -> Result<Validated, Error> {
        validate(&opensip_identity::canonical_bytes(v).unwrap(), c)
    }
    const CR1_ROLES: [&str; 4] = ["toolchain", "stdlib", "rust-dev-llvm", "grammar"];
    #[test]
    fn cr1_exact_role_table_and_unknown_roles() {
        let c = Context::default();
        assert_eq!(
            cr1_validate(&cr1_body("analyzer"), &c)
                .unwrap()
                .closure_kind(),
            "provider"
        );
        for role in CR1_ROLES {
            let v = cr1_body(role);
            assert!(!object(&v).contains_key("commands"));
            assert_eq!(cr1_validate(&v, &c).unwrap().closure_kind(), role);
        }
        for role in ["builder", "evaluator", "detector", "adapter", "core"] {
            assert!(matches!(
                cr1_validate(&cr1_body(role), &c),
                Err(Error::Schema)
            ));
        }
    }
    #[test]
    fn cr1_closure_commands_are_absent_and_analyzer_commands_required() {
        let c = Context::default();
        let commands = object(&cr1_baseline())["commands"].clone();
        for role in CR1_ROLES {
            for member in [commands.clone(), V::Array(vec![]), V::Null] {
                let mut v = cr1_body(role);
                cr1_object(&mut v).insert("commands".into(), member);
                assert!(matches!(cr1_validate(&v, &c), Err(Error::Schema)));
            }
        }
        for member in [None, Some(V::Array(vec![])), Some(V::Null)] {
            let mut v = cr1_body("analyzer");
            let m = cr1_object(&mut v);
            m.remove("commands");
            if let Some(member) = member {
                m.insert("commands".into(), member);
            }
            assert!(matches!(cr1_validate(&v, &c), Err(Error::Schema)));
        }
    }
    #[test]
    fn cr1_closure_capabilities_and_permissions_refuse_existing_codes() {
        let c = Context::default();
        let baseline = cr1_baseline();
        for role in CR1_ROLES {
            let mut v = cr1_body(role);
            cr1_object(&mut v).insert(
                "capabilities".into(),
                object(&baseline)["capabilities"].clone(),
            );
            assert!(matches!(cr1_validate(&v, &c), Err(Error::Capability)));
            let mut v = cr1_body(role);
            cr1_object(&mut v).insert(
                "permissions".into(),
                object(&baseline)["permissions"].clone(),
            );
            assert!(!array(&object(&v)["permissions"]).is_empty());
            assert!(matches!(cr1_validate(&v, &c), Err(Error::Permission)));
        }
    }
    fn cr1_entry(v: &mut V, entry: &str) {
        let V::Array(platforms) = cr1_object(v).get_mut("platforms").unwrap() else {
            panic!()
        };
        for p in platforms {
            cr1_object(p).insert("entrypoint".into(), V::String(entry.into()));
        }
    }
    #[test]
    fn cr1_entrypoint_regular_file_and_analyzer_execution_rule() {
        let c = Context::default();
        for role in CR1_ROLES {
            let mut v = cr1_body(role);
            cr1_entry(&mut v, "lib/provider.js");
            assert!(cr1_validate(&v, &c).is_ok());
            cr1_entry(&mut v, "lib");
            assert!(matches!(cr1_validate(&v, &c), Err(Error::Path)));
        }
        let mut v = cr1_body("analyzer");
        cr1_entry(&mut v, "lib/provider.js");
        assert!(matches!(cr1_validate(&v, &c), Err(Error::Path)));
        cr1_entry(&mut v, "lib");
        assert!(matches!(cr1_validate(&v, &c), Err(Error::Path)));
    }
    #[test]
    fn cr1_closure_symlink_entrypoint_refuses_but_analyzer_resolution_remains() {
        for role in [
            "analyzer",
            "toolchain",
            "stdlib",
            "rust-dev-llvm",
            "grammar",
        ] {
            let mut v = cr1_body(role);
            let V::Array(platforms) = cr1_object(&mut v).get_mut("platforms").unwrap() else {
                panic!()
            };
            for p in platforms {
                let m = cr1_object(p);
                m.insert("entrypoint".into(), V::String("bin/link".into()));
                let tree = cr1_object(m.get_mut("tree").unwrap());
                let V::Array(entries) = tree.get_mut("entries").unwrap() else {
                    panic!()
                };
                entries.push(V::Object(BTreeMap::from([
                    ("path".into(), V::String("bin/link".into())),
                    ("type".into(), V::String("symlink".into())),
                    ("mode".into(), V::String("0755".into())),
                    ("target".into(), V::String("entry".into())),
                ])));
            }
            let got = cr1_validate(&v, &Context::default());
            if role == "analyzer" {
                assert!(got.is_ok(), "{:?}", got.err());
            } else {
                assert!(matches!(got, Err(Error::Path)));
            }
        }
    }
    #[test]
    fn cr1_manifest_name_and_alias_custody_remains_for_every_role() {
        for role in [
            "analyzer",
            "toolchain",
            "stdlib",
            "rust-dev-llvm",
            "grammar",
        ] {
            let mut v = cr1_body(role);
            cr1_object(&mut v).insert(
                "aliases".into(),
                V::Array(vec![V::String("role-alias".into())]),
            );
            assert!(cr1_validate(&v, &Context::default()).is_ok());
            for name in ["typescript-analyzer", "role-alias"] {
                let mut c = Context::default();
                c.reserved_names.insert(name.into());
                assert!(matches!(cr1_validate(&v, &c), Err(Error::Command)));
                assert!(matches!(
                    validate_inventory(
                        &opensip_identity::canonical_bytes(&v).unwrap(),
                        &c.reserved_names
                    ),
                    Err(Error::Command)
                ));
                c.reserved_names.clear();
                c.live_names.push(LiveName {
                    stable_id: "another-component".into(),
                    provenance: object(&v)["provenance"].clone(),
                    names: BTreeSet::from([name.into()]),
                });
                assert!(matches!(cr1_validate(&v, &c), Err(Error::Command)));
                // Inventory validity has no live host namespace authority.
                assert!(
                    validate_inventory(
                        &opensip_identity::canonical_bytes(&v).unwrap(),
                        &BTreeSet::new()
                    )
                    .is_ok()
                );
                c.live_names[0].stable_id = text(&object(&v)["stableId"]).into();
                assert!(cr1_validate(&v, &c).is_ok());
            }
            cr1_object(&mut v).insert(
                "aliases".into(),
                V::Array(vec![V::String("typescript-analyzer".into())]),
            );
            assert!(matches!(
                cr1_validate(&v, &Context::default()),
                Err(Error::Command)
            ));
        }
    }
    #[test]
    fn generated_closed_schema_matches_entire_exact_schema_oracle() {
        let mut count = 0;
        for line in include_bytes!("../tests/fixtures/manifest268-shape.ndjson")
            .split(|b| *b == b'\n')
            .filter(|b| !b.is_empty())
        {
            let v = crate::trust::metadata::parse(line).unwrap();
            let q = object(&v);
            assert_eq!(
                generated::shape(&q["value"]),
                q["valid"] == V::Bool(true),
                "{}",
                text(&q["label"])
            );
            count += 1;
        }
        assert_eq!(count, 11010);
    }
    #[test]
    fn full_structural_manifest_semantics_match_original_reference() {
        let mut count = 0;
        let mut positives = 0;
        for line in include_bytes!("../tests/fixtures/manifest268-semantic.ndjson")
            .split(|b| *b == b'\n')
            .filter(|b| !b.is_empty())
        {
            let v = crate::trust::metadata::parse(line).unwrap();
            let q = object(&v);
            let raw = if let Some(r) = q.get("recipe") {
                let r = object(r);
                assert_eq!(text(&r["kind"]), "padding");
                let mut raw = bytes(&r["body"]);
                raw.resize(int(&r["bytes"]) as usize, b' ');
                raw
            } else {
                bytes(&q["raw"])
            };
            assert_eq!(raw.len() as i128, int(&q["rawBytes"]));
            assert_eq!(
                opensip_identity::digest_hex(&opensip_identity::raw_sha256(&raw)),
                text(&q["rawSha256"])
            );
            let c = context(&q["context"]);
            let got = validate(&raw, &c);
            assert_eq!(
                got.is_ok(),
                q["valid"] == V::Bool(true),
                "{}: {:?}",
                text(&q["label"]),
                got.as_ref().err()
            );
            if let Ok(m) = got {
                let before = m.value().clone();
                drop(raw);
                assert_eq!(m.value(), &before);
                positives += 1;
            }
            count += 1;
        }
        assert_eq!(count, 186);
        assert_eq!(positives, 26);
    }
    #[test]
    fn inventory_body_validity_is_distinct_from_host_admission() {
        let mut counts = (0, 0, 0, 0);
        for line in include_bytes!("../tests/fixtures/inventory293.ndjson")
            .split(|b| *b == b'\n')
            .filter(|b| !b.is_empty())
        {
            let v = crate::trust::metadata::parse(line).unwrap();
            let q = object(&v);
            let label = text(&q["label"]).to_owned();
            let raw = if let Some(r) = q.get("recipe") {
                let r = object(r);
                let mut raw = bytes(&r["body"]);
                raw.resize(int(&r["bytes"]) as usize, b' ');
                raw
            } else {
                bytes(&q["raw"])
            };
            assert_eq!(raw.len() as i128, int(&q["rawBytes"]));
            assert_eq!(
                opensip_identity::digest_hex(&opensip_identity::raw_sha256(&raw)),
                text(&q["rawSha256"])
            );
            let context = context(&q["context"]);
            let inventory = validate_inventory(&raw, &context.reserved_names);
            let full = validate(&raw, &context);
            assert_eq!(
                inventory.is_ok(),
                q["inventoryValid"] == V::Bool(true),
                "{label} inventory {:?}",
                inventory.as_ref().err()
            );
            assert_eq!(
                full.is_ok(),
                q["hostValid"] == V::Bool(true),
                "{label} host {:?}",
                full.as_ref().err()
            );
            counts.0 += 1;
            counts.1 += usize::from(inventory.is_ok());
            counts.2 += usize::from(full.is_ok());
            counts.3 += usize::from(inventory.is_ok() && full.is_err());
            let original = inventory
                .as_ref()
                .ok()
                .map(|_| crate::trust::metadata::parse(&raw).unwrap());
            drop(raw);
            drop(context);
            drop(v);
            if let Ok(body) = inventory {
                assert_eq!(body.value(), original.as_ref().unwrap(), "{label}");
                if let Ok(full) = full {
                    assert_eq!(full.value(), body.value());
                }
            }
        }
        assert_eq!(counts, (301, 98, 57, 41));
    }
}
