//! Closed relation law coherence and local payload checks. No native admission.
use crate::{GraphError as E, JsonValue as V};
use alloc::{
    collections::{BTreeMap, BTreeSet},
    format,
    string::String,
    vec::Vec,
};
const FORMS: &[&str] = &["DigestHex", "Sha256Text", "CanonicalPath"];
fn map(v: &V) -> Result<&BTreeMap<String, V>, E> {
    if let V::Object(x) = v {
        Ok(x)
    } else {
        Err(E::Law)
    }
}
fn get<'a>(v: &'a V, k: &str) -> Result<&'a V, E> {
    map(v)?.get(k).ok_or(E::Law)
}
fn text(v: &V) -> Result<&str, E> {
    if let V::String(x) = v {
        Ok(x)
    } else {
        Err(E::Law)
    }
}
fn array(v: &V) -> Result<&[V], E> {
    if let V::Array(x) = v {
        Ok(x)
    } else {
        Err(E::Law)
    }
}
fn unique(out: &mut Vec<V>, values: impl IntoIterator<Item = V>) {
    for v in values {
        if !out.contains(&v) {
            out.push(v)
        }
    }
}
#[derive(Clone)]
struct Sighting {
    form: bool,
    field: Option<String>,
    joinable: bool,
    annotations: Vec<V>,
    missing: bool,
}
struct Sweep<'a> {
    defs: &'a V,
    seen: BTreeMap<String, Sighting>,
    steps: usize,
    depth: usize,
}
impl Sweep<'_> {
    fn spend(&mut self, depth: usize) -> Result<(), E> {
        if depth > self.depth {
            return Err(E::Limit);
        }
        self.steps = self.steps.checked_sub(1).ok_or(E::Limit)?;
        Ok(())
    }
    fn governed(
        &mut self,
        node: &V,
        chain: &mut BTreeSet<String>,
        depth: usize,
    ) -> Result<Option<Vec<V>>, E> {
        self.spend(depth)?;
        let V::Object(o) = node else { return Ok(None) };
        let mut annotations = o
            .get("x-opensip-digest")
            .cloned()
            .into_iter()
            .collect::<Vec<_>>();
        if let Some(V::String(r)) = o.get("$ref")
            && let Some(target) = r.strip_prefix("#/$defs/")
        {
            if FORMS.contains(&target) {
                return Ok(Some(annotations));
            }
            if let Some(next) = map(self.defs)?.get(target)
                && chain.insert(target.into())
            {
                let child = self.governed(next, chain, depth + 1)?;
                chain.remove(target);
                if let Some(child) = child {
                    annotations.extend(child);
                    return Ok(Some(annotations));
                }
            }
        }
        if let Some(V::String(pattern)) = o.get("pattern") {
            for name in FORMS {
                if let Some(def) = map(self.defs)?.get(*name)
                    && map(def)?.get("pattern") == Some(&V::String(pattern.clone()))
                {
                    return Ok(Some(annotations));
                }
            }
        }
        Ok(None)
    }
    fn record(&mut self, path: &str, mut sighting: Sighting) {
        if let Some(old) = self.seen.get(path) {
            sighting.form |= old.form;
            sighting.joinable &= old.joinable;
            sighting.missing |= old.missing;
            unique(&mut sighting.annotations, old.annotations.iter().cloned());
        }
        self.seen.insert(path.into(), sighting);
    }
    #[allow(clippy::too_many_arguments)]
    fn walk(
        &mut self,
        node: &V,
        path: &str,
        mut inherited: Vec<V>,
        field: Option<&str>,
        joinable: bool,
        chain: &mut BTreeSet<String>,
        depth: usize,
    ) -> Result<(), E> {
        self.spend(depth)?;
        if let V::Array(items) = node {
            for item in items {
                self.walk(
                    item,
                    path,
                    inherited.clone(),
                    field,
                    joinable,
                    chain,
                    depth + 1,
                )?
            }
            return Ok(());
        }
        let V::Object(o) = node else { return Ok(()) };
        unique(&mut inherited, o.get("x-opensip-digest").cloned());
        if let Some(on_chain) = self.governed(node, &mut BTreeSet::new(), depth + 1)? {
            unique(&mut inherited, on_chain);
            let missing = inherited.is_empty();
            self.record(
                path,
                Sighting {
                    form: true,
                    field: field.map(String::from),
                    joinable,
                    annotations: inherited,
                    missing,
                },
            );
            return Ok(());
        }
        if let Some(V::String(r)) = o.get("$ref")
            && let Some(target) = r.strip_prefix("#/$defs/")
            && let Some(next) = map(self.defs)?.get(target)
            && chain.insert(target.into())
        {
            self.walk(
                next,
                path,
                inherited.clone(),
                field,
                joinable,
                chain,
                depth + 1,
            )?;
            chain.remove(target);
        }
        for (key, child) in o {
            match key.as_str() {
                "properties" => {
                    if let V::Object(props) = child {
                        for (name, schema) in props {
                            self.walk(
                                schema,
                                &format!("{path}.{name}"),
                                inherited.clone(),
                                field.or(Some(name)),
                                joinable && field.is_none(),
                                chain,
                                depth + 1,
                            )?
                        }
                    }
                }
                "items" | "additionalProperties" => self.walk(
                    child,
                    &format!("{path}[]"),
                    inherited.clone(),
                    field,
                    false,
                    chain,
                    depth + 1,
                )?,
                "oneOf" | "anyOf" | "allOf" => {
                    if let V::Array(branches) = child {
                        for (i, branch) in branches.iter().enumerate() {
                            self.walk(
                                branch,
                                &format!("{path}|{key}[{i}]"),
                                inherited.clone(),
                                field,
                                joinable,
                                chain,
                                depth + 1,
                            )?
                        }
                    } else {
                        self.walk(
                            child,
                            path,
                            inherited.clone(),
                            field,
                            joinable,
                            chain,
                            depth + 1,
                        )?
                    }
                }
                _ => {}
            }
        }
        Ok(())
    }
}
pub(crate) fn row<'a>(document: &'a V, name: &str, steps: usize, depth: usize) -> Result<&'a V, E> {
    let rows = map(get(
        get(document, "x-opensip-relation-registry")?,
        "relations",
    )?)?;
    let row = rows.get(name).ok_or(E::PayloadRegistryRow)?;
    let defs = get(document, "$defs")?;
    let selector = text(get(row, "selector")?)?
        .strip_prefix("#/$defs/")
        .ok_or(E::Law)?;
    let selected = get(defs, selector)?;
    let properties = map(get(selected, "properties")?)?;
    let mut sweep = Sweep {
        defs,
        seen: BTreeMap::new(),
        steps,
        depth,
    };
    sweep.walk(
        selected,
        name,
        Vec::new(),
        None,
        true,
        &mut BTreeSet::new(),
        0,
    )?;
    for (field, schema) in properties {
        if let Some(annotation) = map(schema)?.get("x-opensip-digest") {
            sweep
                .seen
                .entry(format!("{name}.{field}"))
                .or_insert_with(|| Sighting {
                    form: false,
                    field: Some(field.clone()),
                    joinable: true,
                    annotations: alloc::vec![annotation.clone()],
                    missing: false,
                });
        }
    }
    let mut named = BTreeSet::new();
    for join in array(get(row, "snapshotJoins")?)? {
        for key in ["pathField", "digestField", "lengthField", "anchorPathField"] {
            if let Some(v) = map(join)?.get(key) {
                named.insert(text(v)?);
            }
        }
        if let Some(unless) = map(join)?.get("unless") {
            named.insert(text(get(unless, "field")?)?);
        }
    }
    if let Some(body) = map(row)?.get("bodyIdentityJoin") {
        for key in ["field", "levelField", "levelVersionField"] {
            named.insert(text(get(body, key)?)?);
        }
    }
    let retention = get(get(document, "x-opensip-digest-law")?, "retention")?;
    for sight in sweep.seen.values() {
        if sight.form && (sight.missing || sight.annotations.is_empty()) {
            return Err(E::RelationLaw("unannotated"));
        }
    }
    for sight in sweep.seen.values() {
        if sight.missing || sight.annotations.is_empty() {
            continue;
        }
        if sight.annotations.len() != 1 {
            return Err(E::RelationLaw("annotation conflict"));
        }
        let retained = text(get(&sight.annotations[0], "retention")?)?;
        let allowed = match retention {
            V::Object(o) => o.contains_key(retained),
            V::Array(a) => a.contains(&V::String(retained.into())),
            _ => false,
        };
        if !allowed {
            return Err(E::RelationLaw("retention"));
        }
        if retained == "not-joined" {
            continue;
        }
        if !sight.joinable {
            return Err(E::RelationLaw("unjoinable location"));
        }
        if !named.contains(sight.field.as_deref().ok_or(E::Law)?) {
            return Err(E::RelationLaw("residue"));
        }
    }
    if named.iter().any(|field| !properties.contains_key(*field)) {
        return Err(E::RelationLaw("unknown join field"));
    }
    Ok(row)
}
/// Local facts only. Caller still owes syntax capability, source/body joins,
/// admitted target universe and complete coverage/evaluator obligations.
pub(crate) fn payload_rules(
    value: &V,
    row: &V,
    fact: &V,
    steps: usize,
    depth: usize,
) -> Result<(), E> {
    let ladder = array(get(row, "ladder")?)?;
    if ladder.is_empty() {
        return Err(E::RelationLaw("missing ladder"));
    }
    let resolution = get(fact, "resolution")?;
    if !ladder.contains(resolution) {
        return Err(E::RelationRule("rung not in ladder"));
    }
    let law = get(row, "anchorLaw")?;
    let count = array(get(fact, "anchors")?)?.len() as i128;
    for key in ["cardinality", "minimum"] {
        if let Some(v) = map(law)?.get(key) {
            let V::Integer(n) = v else { return Err(E::Law) };
            if (key == "cardinality" && count != n.get()) || (key == "minimum" && count < n.get()) {
                return Err(E::RelationRule("anchor cardinality"));
            }
        }
    }
    if let Some(rung) = map(get(row, "rungs")?)?.get(text(resolution)?) {
        for v in array(get(rung, "required")?)? {
            if !map(value)?.contains_key(text(v)?) {
                return Err(E::RelationRule("required rung field"));
            }
        }
        for v in array(get(rung, "forbidden")?)? {
            if map(value)?.contains_key(text(v)?) {
                return Err(E::RelationRule("forbidden rung field"));
            }
        }
    }
    if text(get(row, "universeRule")?)? == "same-only"
        && get(fact, "sourceUniverse")? != get(fact, "targetUniverse")?
    {
        return Err(E::RelationRule("same-only universe"));
    }
    let mut remaining = steps;
    scan(value, &mut remaining, depth)
}
fn scan(value: &V, steps: &mut usize, depth: usize) -> Result<(), E> {
    *steps = steps.checked_sub(1).ok_or(E::Limit)?;
    let next = depth.checked_sub(1).ok_or(E::Limit)?;
    match value {
        V::Integer(n) if n.get() < 0 => return Err(E::RelationRule("negative integer")),
        V::String(s) if !unicode_normalization::is_nfc(s) => {
            return Err(E::RelationRule("non-NFC string"));
        }
        V::Array(a) => {
            for v in a {
                scan(v, steps, next)?
            }
        }
        V::Object(o) => {
            for (k, v) in o {
                if !unicode_normalization::is_nfc(k) {
                    return Err(E::RelationRule("non-NFC key"));
                }
                scan(v, steps, next)?
            }
        }
        _ => {}
    }
    Ok(())
}
