//! Fixed native/imported atom scanner over privately reconstructed evidence.
use alloc::{
    collections::BTreeMap,
    string::{String, ToString},
};
use opensip_identity::JsonValue as V;
#[derive(Debug, PartialEq, Eq)]
pub(super) enum Error {
    Law,
    Limit,
    Refused(&'static str),
}
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
enum Match {
    Yes,
    No,
    Unknown,
}
fn obj(v: &V) -> Result<&BTreeMap<String, V>, Error> {
    if let V::Object(v) = v {
        Ok(v)
    } else {
        Err(Error::Law)
    }
}
fn arr(v: &V) -> Result<&[V], Error> {
    if let V::Array(v) = v {
        Ok(v)
    } else {
        Err(Error::Law)
    }
}
fn text(v: &V) -> Result<&str, Error> {
    if let V::String(v) = v {
        Ok(v)
    } else {
        Err(Error::Law)
    }
}
fn field<'a>(v: &'a V, k: &str) -> Result<&'a V, Error> {
    obj(v)?.get(k).ok_or(Error::Law)
}
fn optional<'a>(v: &'a V, k: &str) -> Result<&'a V, Error> {
    Ok(obj(v)?.get(k).unwrap_or(&V::Null))
}
fn is(v: &V, s: &str) -> bool {
    matches!(v,V::String(v)if v==s)
}
fn yes(b: bool) -> Match {
    if b { Match::Yes } else { Match::No }
}
fn and(a: Match, b: Match) -> Match {
    if a == Match::No || b == Match::No {
        Match::No
    } else if a == Match::Unknown || b == Match::Unknown {
        Match::Unknown
    } else {
        Match::Yes
    }
}
fn cmp_string(cmp: &str, projected: &str, value: &V, budget: usize) -> Result<Match, Error> {
    Ok(yes(match cmp {
        "eq" => is(value, projected),
        "neq" => !is(value, projected),
        "in" => arr(value)?.iter().any(|v| is(v, projected)),
        "prefix" => projected.starts_with(text(value)?),
        "glob" => {
            crate::portable_glob_match(text(value)?, projected, budget).map_err(|_| Error::Limit)?
        }
        _ => return Err(Error::Refused("ATOM_FILTER_COMPARATOR_ILLEGAL")),
    }))
}
fn number(v: &V) -> Result<i128, Error> {
    if let V::Integer(v) = v {
        Ok(v.get())
    } else {
        Err(Error::Law)
    }
}
fn cmp_int(cmp: &str, projected: &V, value: &V) -> Result<Match, Error> {
    let p = number(projected)?;
    Ok(yes(match cmp {
        "eq" => p == number(value)?,
        "neq" => p != number(value)?,
        "in" => arr(value)?
            .iter()
            .any(|v| matches!(v,V::Integer(n)if n.get()==p)),
        "gte" => p >= number(value)?,
        "lte" => p <= number(value)?,
        _ => return Err(Error::Refused("ATOM_FILTER_COMPARATOR_ILLEGAL")),
    }))
}
fn under_prefix(path: &str, root: &str) -> bool {
    let root = if root == "." { "" } else { root };
    root.is_empty()
        || path == root
        || path
            .strip_prefix(root.trim_end_matches('/'))
            .is_some_and(|v| v.starts_with('/'))
}
fn path_in_scope(scope: &V, path: &str) -> Result<bool, Error> {
    let scope = obj(scope)?;
    let rows = |k| scope.get(k).map(arr).transpose().map(|v| v.unwrap_or(&[]));
    for e in rows("excludedPathPrefixes")? {
        if under_prefix(path, text(e)?) {
            return Ok(false);
        }
    }
    let mut root_match = false;
    for r in rows("workspaceRoots")? {
        root_match |= under_prefix(path, text(r)?);
    }
    if !root_match {
        return Ok(false);
    }
    let prefixes = rows("pathPrefixes")?;
    if prefixes.is_empty() {
        return Ok(true);
    }
    for p in prefixes {
        if under_prefix(path, text(p)?) {
            return Ok(true);
        }
    }
    Ok(false)
}
fn logical_path<'a>(subject: &'a V, row: Option<&'a V>) -> Result<Option<&'a str>, Error> {
    if let Some(row) = row
        && let Some(V::String(path)) = obj(row)?.get("path")
        && !path.is_empty()
    {
        return Ok(Some(path));
    }
    match text(field(subject, "kind")?)? {
        "file" => Ok(Some(text(field(subject, "nativeSubjectId")?)?)),
        "package" => match optional(subject, "packageManifestPath")? {
            V::Null => Ok(None),
            v => Ok(Some(text(v)?)),
        },
        _ => Ok(None),
    }
}
fn apply_import_filters(atom: &V, projected: &V, budget: usize) -> Result<Match, Error> {
    let mut acc = Match::Yes;
    let empty = [];
    let filters = match optional(atom, "filters")? {
        V::Null => &empty,
        v => arr(v)?,
    };
    for filter in filters {
        let key = text(field(filter, "field")?)?;
        let raw = obj(projected)?
            .get(key)
            .ok_or(Error::Refused("ATOM_FILTER_FIELD_FORBIDDEN"))?;
        if raw == &V::Null {
            acc = and(acc, Match::Unknown);
            continue;
        }
        let cmp = text(field(filter, "cmp")?)?;
        let value = field(filter, "value")?;
        acc = and(
            acc,
            if key == "exitStatus" {
                cmp_int(cmp, raw, value)?
            } else {
                cmp_string(cmp, text(raw)?, value, budget)?
            },
        );
    }
    Ok(acc)
}
fn complete_runtime(wrapper: &V, payload: &V) -> Result<bool, Error> {
    Ok(is(optional(wrapper, "completeness")?, "complete")
        && optional(payload, "observationWindow")? != &V::Null
        && optional(payload, "observedPopulation")? != &V::Null
        && !is(optional(payload, "observedPopulation")?, "unknown"))
}
fn complete_history(wrapper: &V, payload: &V) -> Result<bool, Error> {
    if !is(optional(wrapper, "completeness")?, "complete") {
        return Ok(false);
    }
    let range = optional(payload, "revisionRange")?;
    Ok(range == &V::Null || optional(range, "truncated")? != &V::Bool(true))
}
fn complete_test(wrapper: &V, payload: &V, consumable: &V, staleness: &V) -> Result<bool, Error> {
    if !is(optional(wrapper, "completeness")?, "complete")
        || consumable != &V::Bool(true)
        || !is(staleness, "current")
    {
        return Ok(false);
    }
    let selection = optional(payload, "selection")?;
    Ok(selection != &V::Null && optional(selection, "completenessEstablished")? == &V::Bool(true))
}
fn process_result(payload: &V) -> Result<&'static str, Error> {
    if optional(payload, "timedOut")? == &V::Bool(true)
        || optional(payload, "signal")? != &V::Null
        || optional(payload, "exitStatus")? == &V::Null
    {
        return Ok("error");
    }
    let tests = match optional(payload, "tests")? {
        V::Null => &[],
        v => arr(v)?,
    };
    for row in tests {
        if is(optional(row, "outcome")?, "error") {
            return Ok("error");
        }
    }
    if number(field(payload, "exitStatus")?)? != 0 {
        return Ok("failed");
    }
    for row in tests {
        if is(optional(row, "outcome")?, "fail") {
            return Ok("failed");
        }
    }
    Ok("passed")
}
fn ordinal(v: &V) -> Result<usize, Error> {
    usize::try_from(number(v)?).map_err(|_| Error::Law)
}
fn binding(plan: &V, cell: usize, program: usize) -> Result<Option<&V>, Error> {
    let cells = match optional(plan, "cells")? {
        V::Null => &[],
        v => arr(v)?,
    };
    let Some(cell) = cells.get(cell) else {
        return Ok(None);
    };
    let bindings = match optional(cell, "programBindings")? {
        V::Null => &[],
        v => arr(v)?,
    };
    for b in bindings {
        if let V::Integer(n) = optional(b, "ordinal")?
            && usize::try_from(n.get()).ok() == Some(program)
        {
            return Ok(Some(b));
        }
    }
    Ok(bindings.get(program))
}
fn inventory_universe<'a>(inv: &'a V, plan: Option<&'a V>) -> Result<&'a V, Error> {
    if let Some(plan) = plan
        && let Some(b) = binding(
            plan,
            ordinal(field(inv, "cellOrdinal")?)?,
            ordinal(field(inv, "programOrdinal")?)?,
        )?
    {
        return optional(b, "universe");
    }
    optional(inv, "universe")
}
fn lookup_rows<'a>(
    native: &V,
    universe: &V,
    kind: Option<&V>,
    package_path: Option<&V>,
    inventories: &'a [V],
    plan: Option<&'a V>,
) -> Result<alloc::vec::Vec<&'a V>, Error> {
    let mut rows = alloc::vec::Vec::new();
    for inv in inventories {
        if inventory_universe(inv, plan)? != universe {
            continue;
        }
        for row in arr(field(inv, "rows")?)? {
            if optional(row, "nativeSubjectId")? != native {
                continue;
            }
            if let Some(kind) = kind
                && optional(row, "kind")? != kind
            {
                continue;
            }
            if is(optional(row, "kind")?, "package")
                && let Some(path) = package_path
                && optional(row, "path")? != path
            {
                continue;
            }
            if !rows.contains(&row) {
                rows.push(row);
            }
        }
    }
    Ok(rows)
}
fn symbol_rows<'a>(
    path: &V,
    qn: &V,
    universe: &V,
    inventories: &'a [V],
    plan: Option<&'a V>,
) -> Result<alloc::vec::Vec<&'a V>, Error> {
    let mut rows = alloc::vec::Vec::new();
    let mut seen = alloc::collections::BTreeSet::new();
    for inv in inventories {
        if !is(optional(inv, "kind")?, "symbol") || inventory_universe(inv, plan)? != universe {
            continue;
        }
        for row in arr(field(inv, "rows")?)? {
            if optional(row, "path")? == path
                && optional(row, "qualifiedName")? == qn
                && seen.insert(text(field(row, "nativeSubjectId")?)?)
            {
                rows.push(row);
            }
        }
    }
    Ok(rows)
}
fn runtime_occupancy(
    row: &V,
    subject: &V,
    inventories: &[V],
    plan: Option<&V>,
) -> Result<Match, Error> {
    match text(field(subject, "kind")?)? {
        "file" => {
            if optional(row, "symbol")? != &V::Null {
                return Ok(Match::No);
            }
            Ok(yes(
                optional(row, "path")? == field(subject, "nativeSubjectId")?
            ))
        }
        "symbol" => {
            if optional(row, "symbol")? == &V::Null {
                return Ok(Match::No);
            }
            let hits = symbol_rows(
                optional(row, "path")?,
                optional(row, "symbol")?,
                field(subject, "universe")?,
                inventories,
                plan,
            )?;
            let mut found = false;
            for h in &hits {
                found |= field(h, "nativeSubjectId")? == field(subject, "nativeSubjectId")?;
            }
            Ok(if !found {
                Match::No
            } else if hits.len() > 1 {
                Match::Unknown
            } else {
                Match::Yes
            })
        }
        _ => Ok(Match::No),
    }
}
fn record<const N: usize>(pairs: [(&str, V); N]) -> V {
    V::Object(pairs.into_iter().map(|(k, v)| (k.into(), v)).collect())
}
fn string(s: &str) -> V {
    V::String(s.into())
}
fn registry() -> Result<V, Error> {
    opensip_identity::parse_json(include_bytes!("atom-registry.json")).map_err(|_| Error::Law)
}
fn cause(
    code: &str,
    evidence: Option<&str>,
    native: Option<&str>,
    extras: &[(&str, V)],
) -> Result<V, Error> {
    if let Some(native) = native {
        let r = registry()?;
        if !arr(field(field(&r, "scanner")?, "nativeCauseCodes")?)?.contains(&string(native)) {
            return Err(Error::Refused("ATOM_NATIVE_CAUSE_UNTYPED"));
        }
    }
    let mut result = obj(&record([
        ("code", string(code)),
        ("evidenceKind", evidence.map(string).unwrap_or(V::Null)),
        ("nativeCause", native.map(string).unwrap_or(V::Null)),
    ]))?
    .clone();
    for (k, v) in extras {
        if v != &V::Null {
            result.insert((*k).into(), v.clone());
        }
    }
    Ok(V::Object(result))
}
// Python's json.dumps(sort_keys=True,separators=(',',':')) orders cause
// records by ASCII-escaped JSON. General C canonical byte ordering differs
// for non-ASCII values, so retain this reference-specific sort boundary.
fn cause_sort_key(value: &V) -> Result<alloc::vec::Vec<u8>, Error> {
    let raw = opensip_identity::canonical_bytes(value).map_err(|_| Error::Law)?;
    let s = core::str::from_utf8(&raw).map_err(|_| Error::Law)?;
    let mut out = alloc::vec::Vec::new();
    for c in s.chars() {
        if c.is_ascii() {
            out.push(c as u8);
        } else {
            let mut units = [0u16; 2];
            for u in c.encode_utf16(&mut units) {
                out.extend_from_slice(alloc::format!("\\u{u:04x}").as_bytes());
            }
        }
    }
    Ok(out)
}
fn unique_causes(causes: alloc::vec::Vec<V>) -> Result<V, Error> {
    let r = registry()?;
    let scanner = field(&r, "scanner")?;
    let mut unique = BTreeMap::new();
    for c in causes {
        let row = obj(&c).map_err(|_| Error::Refused("ATOM_CAUSE_UNREGISTERED"))?;
        let valid = |key, allowed| -> Result<bool, Error> {
            Ok(row
                .get(key)
                .is_some_and(|v| v == &V::Null || arr(allowed).is_ok_and(|a| a.contains(v))))
        };
        if !row.get("code").is_some_and(|v| {
            arr(field(scanner, "atomCauseCodes").expect("embedded codes"))
                .is_ok_and(|a| a.contains(v))
        }) || !valid("evidenceKind", field(scanner, "importEvidenceKinds")?)?
            || !valid("nativeCause", field(scanner, "nativeCauseCodes")?)?
        {
            return Err(Error::Refused("ATOM_CAUSE_UNREGISTERED"));
        }
        unique.insert(cause_sort_key(&c)?, c);
    }
    Ok(V::Array(unique.into_values().collect()))
}
fn sorted_addresses(values: alloc::vec::Vec<V>) -> Result<V, Error> {
    let mut unique = BTreeMap::new();
    for v in values {
        let iid = text(field(&v, "importId")?)?.to_string();
        let selector = text(field(&v, "selector")?)?.to_string();
        let ordinal = field(&v, "ordinal")?;
        let sort = if ordinal == &V::Null {
            None
        } else {
            Some(number(ordinal)?)
        };
        let row = record([
            ("importId", string(&iid)),
            ("selector", string(&selector)),
            ("ordinal", ordinal.clone()),
        ]);
        unique.insert((iid, selector, sort), row);
    }
    Ok(V::Array(unique.into_values().collect()))
}
fn sorted_strings(values: alloc::vec::Vec<V>) -> Result<V, Error> {
    let mut unique = alloc::collections::BTreeSet::new();
    for v in values {
        unique.insert(text(&v)?.to_string());
    }
    Ok(V::Array(unique.into_iter().map(V::String).collect()))
}
fn imported_result(
    value: &str,
    known: alloc::vec::Vec<V>,
    uncertain: alloc::vec::Vec<V>,
    causes: alloc::vec::Vec<V>,
    consumed: alloc::vec::Vec<V>,
) -> Result<V, Error> {
    let empty = V::Array(alloc::vec::Vec::new());
    Ok(record([
        ("value", string(value)),
        ("kind", string("imported-atom")),
        ("knownFactIds", empty.clone()),
        ("uncertainFactIds", empty.clone()),
        ("knownObservationAddresses", sorted_addresses(known)?),
        (
            "uncertainObservationAddresses",
            sorted_addresses(uncertain)?,
        ),
        ("coverageIds", empty.clone()),
        ("scopeIds", empty.clone()),
        ("evaluationInputRefs", sorted_strings(consumed)?),
        ("causes", unique_causes(causes)?),
        ("nativeDeficiencies", empty.clone()),
        ("disclosures", empty.clone()),
        ("usedInputDigests", empty),
    ]))
}
fn rows<'a>(v: &'a V, key: &str) -> Result<&'a [V], Error> {
    match optional(v, key)? {
        V::Null => Ok(&[]),
        v => arr(v),
    }
}
fn import_scope<'a>(wrapper: &V, inputs: &'a V) -> Result<&'a V, Error> {
    let digest = text(field(wrapper, "scopeDigest")?)?;
    obj(field(inputs, "importScopes")?)?
        .get(digest)
        .ok_or(Error::Refused("ATOM_IMPORT_SCOPE_UNSTATED"))
}
fn flags<'a>(wrapper: &'a V, iid: &str, inputs: &'a V) -> Result<(&'a V, &'a V), Error> {
    let adapters = obj(field(inputs, "importFlagsAdapter")?)?;
    let adapter = adapters.get(iid);
    let get = |key, missing| -> Result<&'a V, Error> {
        if let Some(v) = obj(wrapper)?.get(key) {
            return Ok(v);
        }
        if let Some(row) = adapter {
            let row = obj(row).map_err(|_| Error::Refused("ATOM_IMPORT_FLAG_ADAPTER"))?;
            if row.keys().any(|k| k != "consumable" && k != "staleness") {
                return Err(Error::Refused("ATOM_IMPORT_FLAG_ADAPTER"));
            }
            if let Some(v) = row.get(key) {
                return Ok(v);
            }
        }
        Err(Error::Refused(missing))
    };
    Ok((
        get("consumable", "ATOM_IMPORT_CONSUMABLE_UNSTATED")?,
        get("staleness", "ATOM_IMPORT_STALENESS_UNSTATED")?,
    ))
}
fn address(iid: &str, selector: &str, ordinal: Option<usize>) -> Result<V, Error> {
    let ordinal = match ordinal {
        None => V::Null,
        Some(n) => {
            V::Integer(opensip_identity::JsonInteger::new(n as i128).map_err(|_| Error::Law)?)
        }
    };
    Ok(record([
        ("importId", string(iid)),
        ("selector", string(selector)),
        ("ordinal", ordinal),
    ]))
}
fn import_cause(code: &str, kind: &str, iid: Option<&str>) -> Result<V, Error> {
    cause(
        code,
        Some(kind),
        None,
        &iid.map(|id| alloc::vec![("importId", string(id))])
            .unwrap_or_default(),
    )
}
fn tick(work: &mut usize) -> Result<(), Error> {
    *work = work.checked_sub(1).ok_or(Error::Limit)?;
    Ok(())
}
fn eval_imported(
    atom: &V,
    subject: &V,
    inputs: &V,
    spec: &V,
    mut work: usize,
    glob_budget: usize,
) -> Result<V, Error> {
    let kind = text(field(spec, "evidenceKind")?)?;
    let selected = rows(inputs, "planSelectedImportIds")?;
    let wrappers = obj(field(inputs, "imports")?)?;
    let payloads = obj(field(inputs, "importPayloads")?)?;
    let inventories = rows(inputs, "inventories")?;
    let plan = optional(inputs, "enumerationPlan")?;
    let plan = if plan == &V::Null { None } else { Some(plan) };
    let hits = lookup_rows(
        field(subject, "nativeSubjectId")?,
        field(subject, "universe")?,
        Some(field(subject, "kind")?),
        obj(subject)?.get("packageManifestPath"),
        inventories,
        plan,
    )?;
    let inventory_row = if hits.len() == 1 { Some(hits[0]) } else { None };
    let mut flag_by_id = BTreeMap::new();
    for id in selected {
        tick(&mut work)?;
        let iid = text(id)?;
        let wrapper = wrappers
            .get(iid)
            .ok_or(Error::Refused("ATOM_IMPORT_WRAPPER_MISSING"))?;
        flag_by_id.insert(iid, flags(wrapper, iid, inputs)?);
        import_scope(wrapper, inputs)?;
    }
    let mut owed = alloc::vec::Vec::new();
    for id in selected {
        tick(&mut work)?;
        let iid = text(id)?;
        let wrapper = &wrappers[iid];
        if !is(optional(wrapper, "kind")?, kind) {
            continue;
        }
        let path = logical_path(subject, inventory_row)?;
        if path
            .map(|path| path_in_scope(import_scope(wrapper, inputs)?, path))
            .transpose()?
            .unwrap_or(true)
        {
            owed.push(iid);
        }
    }
    let consumed = owed
        .iter()
        .map(|id| string(id))
        .collect::<alloc::vec::Vec<_>>();
    if owed.is_empty() {
        return imported_result(
            "indeterminate",
            alloc::vec::Vec::new(),
            alloc::vec::Vec::new(),
            alloc::vec![
                import_cause("zero-owed-wrappers", kind, None)?,
                import_cause("evidence-kind-unavailable", kind, None)?
            ],
            consumed,
        );
    }
    let (mut known, mut uncertain, mut causes) = (
        alloc::vec::Vec::new(),
        alloc::vec::Vec::new(),
        alloc::vec::Vec::new(),
    );
    let mut covering_complete = true;
    let empty = V::Object(BTreeMap::new());
    for iid in owed {
        tick(&mut work)?;
        let wrapper = &wrappers[iid];
        let payload = payloads.get(iid).unwrap_or(&empty);
        let (consumable, staleness) = flag_by_id[iid];
        if consumable != &V::Bool(true) || !is(staleness, "current") {
            causes.push(import_cause("import-unmapped-only", kind, Some(iid))?);
            covering_complete = false;
            continue;
        }
        match kind {
            "runtime" => {
                let complete = complete_runtime(wrapper, payload)?;
                if !complete {
                    covering_complete = false;
                    let code = if is(optional(wrapper, "completeness")?, "partial") {
                        "wrapper-partial"
                    } else if optional(payload, "observationWindow")? == &V::Null
                        || optional(payload, "observedPopulation")? == &V::Null
                        || is(optional(payload, "observedPopulation")?, "unknown")
                    {
                        "observation-window-insufficient"
                    } else {
                        "incomplete-observation"
                    };
                    causes.push(import_cause(code, kind, Some(iid))?);
                }
                let (mut covering, mut matched, mut unobservable) =
                    (0usize, alloc::vec::Vec::new(), false);
                for (i, row) in rows(payload, "subjects")?.iter().enumerate() {
                    tick(&mut work)?;
                    let occupancy = runtime_occupancy(row, subject, inventories, plan)?;
                    if occupancy == Match::No {
                        continue;
                    }
                    let address = address(iid, "runtime-subject", Some(i))?;
                    if occupancy == Match::Unknown {
                        uncertain.push(address);
                        causes.push(import_cause("overload-ambiguous", kind, Some(iid))?);
                        continue;
                    }
                    let observability = optional(row, "observability")?;
                    if is(observability, "unobservable") || is(observability, "unmapped") {
                        unobservable = true;
                        uncertain.push(address);
                        causes.push(import_cause(
                            if is(observability, "unobservable") {
                                "unobservable-subject"
                            } else {
                                "unmapped-subject"
                            },
                            kind,
                            Some(iid),
                        )?);
                        continue;
                    }
                    if is(observability, "observed-hit") || is(observability, "observable-unhit") {
                        covering += 1;
                        let scalar = match text(field(subject, "kind")?)? {
                            "file" => optional(row, "path")?,
                            "symbol" => optional(row, "symbol")?,
                            _ => &V::Null,
                        };
                        let projected = record([
                            ("observability", observability.clone()),
                            ("subject", scalar.clone()),
                            ("resolution", string("observed")),
                            ("subjectKind", field(subject, "kind")?.clone()),
                        ]);
                        match apply_import_filters(atom, &projected, glob_budget)? {
                            Match::Yes => matched.push(address),
                            Match::Unknown => uncertain.push(address),
                            Match::No => {}
                        }
                    }
                }
                if matched.len() > 1 {
                    return Err(Error::Refused("ATOM_RUNTIME_ROW_AMBIGUOUS"));
                }
                known.extend(matched);
                if covering == 0 && unobservable {
                    covering_complete = false;
                } else if covering == 0 && complete {
                    covering_complete = false;
                    causes.push(import_cause("no-consumable-row", kind, Some(iid))?);
                }
            }
            "history" => {
                if !complete_history(wrapper, payload)? {
                    covering_complete = false;
                    if is(optional(wrapper, "completeness")?, "partial") {
                        causes.push(import_cause("wrapper-partial", kind, Some(iid))?);
                    }
                    let range = optional(payload, "revisionRange")?;
                    let truncated =
                        range != &V::Null && optional(range, "truncated")? == &V::Bool(true);
                    causes.push(import_cause(
                        if truncated {
                            "history-truncated"
                        } else {
                            "incomplete-observation"
                        },
                        kind,
                        Some(iid),
                    )?);
                }
                let Some(path) = logical_path(subject, inventory_row)? else {
                    causes.push(import_cause("target-metadata-unknown", kind, Some(iid))?);
                    covering_complete = false;
                    continue;
                };
                let collection = optional(payload, "collectionScope")?;
                let in_extent = if is(collection, "listed-paths") {
                    rows(payload, "subjects")?
                        .iter()
                        .any(|r| optional(r, "path").is_ok_and(|v| is(v, path)))
                } else if is(collection, "all-paths") || is(collection, "in-scope-paths") {
                    path_in_scope(import_scope(wrapper, inputs)?, path)?
                } else {
                    false
                };
                if !in_extent {
                    causes.push(import_cause(
                        "history-outside-collection-scope",
                        kind,
                        Some(iid),
                    )?);
                    covering_complete = false;
                    continue;
                }
                for (i, row) in rows(payload, "subjects")?.iter().enumerate() {
                    tick(&mut work)?;
                    if !is(optional(row, "path")?, path) {
                        continue;
                    }
                    let projected = record([
                        ("subject", optional(row, "path")?.clone()),
                        ("resolution", string("observed")),
                        ("subjectKind", field(subject, "kind")?.clone()),
                    ]);
                    match apply_import_filters(atom, &projected, glob_budget)? {
                        Match::Yes => known.push(address(iid, "history-subject", Some(i))?),
                        Match::Unknown => uncertain.push(address(iid, "history-subject", Some(i))?),
                        Match::No => {}
                    }
                }
            }
            "test" => {
                if !complete_test(wrapper, payload, consumable, staleness)? {
                    covering_complete = false;
                    if is(optional(wrapper, "completeness")?, "partial") {
                        causes.push(import_cause("wrapper-partial", kind, Some(iid))?);
                    }
                    causes.push(import_cause(
                        "test-completeness-not-established",
                        kind,
                        Some(iid),
                    )?);
                }
                if is(
                    optional(spec, "observationAddressSelector")?,
                    "test-execution",
                ) {
                    let projected = record([
                        ("testResult", string(process_result(payload)?)),
                        ("exitStatus", optional(payload, "exitStatus")?.clone()),
                        ("resolution", string("observed")),
                        ("subjectKind", field(subject, "kind")?.clone()),
                        (
                            "subject",
                            logical_path(subject, inventory_row)?
                                .filter(|s| !s.is_empty())
                                .map(string)
                                .unwrap_or(V::Null),
                        ),
                    ]);
                    let addr = address(iid, "test-execution", None)?;
                    match apply_import_filters(atom, &projected, glob_budget)? {
                        Match::Yes => known.push(addr),
                        Match::Unknown => {
                            uncertain.push(addr);
                            if optional(payload, "exitStatus")? == &V::Null {
                                causes.push(import_cause("null-exit-status", kind, Some(iid))?);
                            }
                        }
                        Match::No => {}
                    }
                } else {
                    let path = logical_path(subject, inventory_row)?;
                    for (i, row) in rows(payload, "tests")?.iter().enumerate() {
                        tick(&mut work)?;
                        if !obj(row)?.contains_key("subjectPath")
                            || !is(field(subject, "kind")?, "file")
                            || path.is_none_or(|p| {
                                !optional(row, "subjectPath").is_ok_and(|v| is(v, p))
                            })
                        {
                            continue;
                        }
                        let projected = record([
                            ("testResult", optional(row, "outcome")?.clone()),
                            ("subject", optional(row, "subjectPath")?.clone()),
                            ("resolution", string("observed")),
                            ("subjectKind", field(subject, "kind")?.clone()),
                        ]);
                        match apply_import_filters(atom, &projected, glob_budget)? {
                            Match::Yes => known.push(address(iid, "test-case", Some(i))?),
                            Match::Unknown => uncertain.push(address(iid, "test-case", Some(i))?),
                            Match::No => {}
                        }
                    }
                }
            }
            _ => {}
        }
    }
    let op = text(field(atom, "op")?)?;
    let value = if op == "exists" && !known.is_empty() {
        "true"
    } else if op == "none" && !known.is_empty()
        || op == "count-at-most" && (known.len() as i128) > number(field(atom, "n")?)?
    {
        "false"
    } else {
        let mut incomplete = !covering_complete || !uncertain.is_empty();
        for c in &causes {
            incomplete |= matches!(
                text(field(c, "code")?)?,
                "incomplete-observation"
                    | "unobservable-subject"
                    | "unmapped-subject"
                    | "no-consumable-row"
                    | "import-unmapped-only"
                    | "history-outside-collection-scope"
                    | "history-truncated"
                    | "test-completeness-not-established"
                    | "wrapper-partial"
                    | "null-exit-status"
                    | "overload-ambiguous"
                    | "target-metadata-unknown"
            );
        }
        if incomplete {
            "indeterminate"
        } else if op == "exists" {
            "false"
        } else {
            "true"
        }
    };
    imported_result(value, known, uncertain, causes, consumed)
}

fn defaulted<'a>(v: &'a V, k: &str, default: &'a V) -> Result<&'a V, Error> {
    Ok(obj(v)?.get(k).unwrap_or(default))
}
fn rung_index(reg: &V, relation: &str, rung: &V) -> Result<Option<usize>, Error> {
    let Some(spec) = obj(field(reg, "relations")?)?.get(relation) else {
        return Ok(None);
    };
    Ok(arr(field(spec, "ladder")?)?.iter().position(|v| v == rung))
}
fn entry_from_cov(cov: &V) -> Result<V, Error> {
    let empty = V::Object(BTreeMap::new());
    let e = optional(cov, "entry")?;
    let e = if e == &V::Null { &empty } else { e };
    let key = optional(cov, "key")?;
    let key = if key == &V::Null { &empty } else { key };
    let rc = optional(e, "resolutionCompleteness")?;
    let rc = if matches!(rc, V::Object(_)) {
        rc.clone()
    } else {
        record([
            ("state", string("not-attempted")),
            ("attempted", V::Bool(false)),
            ("examinedExhaustive", V::Bool(false)),
            ("stageTerminal", V::Null),
            ("unresolvedEdgeCount", integer(0)?),
            ("unresolvedEdgeClasses", V::Array(alloc::vec![])),
        ])
    };
    let cw = optional(e, "closedWorld")?;
    let cw = if matches!(cw, V::Object(_)) {
        cw.clone()
    } else {
        record([
            ("exportsClosed", string("unknown")),
            ("entryPointsRecognized", string("none")),
            ("nonliteralLoading", string("none")),
            ("externalConsumers", string("unknown")),
            ("dynamicDispatch", string("not-applicable")),
            ("reasons", V::Array(alloc::vec![])),
            ("deadCodeRepairEligible", V::Bool(false)),
        ])
    };
    let native = optional(e, "nativeCause")?;
    if native != &V::Null
        && !arr(field(field(&registry()?, "scanner")?, "nativeCauseCodes")?)?.contains(native)
    {
        return Err(Error::Refused("ATOM_NATIVE_CAUSE_UNTYPED"));
    }
    let resolution = optional(key, "resolution")?;
    let resolution = if resolution == &V::Null || is(resolution, "") {
        optional(e, "resolution")?
    } else {
        resolution
    };
    let kinds = optional(e, "derivationKinds")?;
    Ok(record([
        ("resolution", resolution.clone()),
        (
            "coverage",
            defaulted(e, "coverage", &string("unknown"))?.clone(),
        ),
        (
            "confidenceMillionths",
            defaulted(e, "confidenceMillionths", &integer(1_000_000)?)?.clone(),
        ),
        ("resolutionCompleteness", rc),
        ("closedWorld", cw),
        (
            "derivationKinds",
            if kinds == &V::Null {
                V::Array(alloc::vec![])
            } else {
                kinds.clone()
            },
        ),
        ("deficiency", optional(e, "deficiency")?.clone()),
        ("nativeCause", native.clone()),
        (
            "rungUnavailableBecause",
            defaulted(e, "rungUnavailableBecause", &string(""))?.clone(),
        ),
    ]))
}
fn rank(v: &V, names: &[&str], fallback: usize) -> usize {
    names.iter().position(|s| is(v, s)).unwrap_or(fallback)
}
// Callers must supply ascending Coverage IDs. Ties intentionally keep the first carrier.
fn conservative_entry(covs: &[(String, V)]) -> Result<(V, alloc::vec::Vec<String>), Error> {
    let Some((_, first)) = covs.first() else {
        return Err(Error::Law);
    };
    let mut worst = obj(&entry_from_cov(first)?)?.clone();
    for (_, cov) in &covs[1..] {
        let e = entry_from_cov(cov)?;
        let er = field(&e, "coverage")?;
        if rank(er, &["complete", "partial", "unknown"], 2)
            > rank(&worst["coverage"], &["complete", "partial", "unknown"], 2)
        {
            worst.insert("coverage".into(), er.clone());
        }
        let rc = field(&e, "resolutionCompleteness")?;
        let rc_rank = |v: &V| -> Result<usize, Error> {
            Ok(match text(optional(v, "state")?).unwrap_or("") {
                "complete" | "not-applicable" => 0,
                "partial" => 1,
                "incomplete" => 2,
                _ => 3,
            })
        };
        if rc_rank(rc)? > rc_rank(&worst["resolutionCompleteness"])? {
            worst.insert("resolutionCompleteness".into(), rc.clone());
        }
        let confidence = field(&e, "confidenceMillionths")?;
        if number(confidence)? < number(&worst["confidenceMillionths"])? {
            worst.insert("confidenceMillionths".into(), confidence.clone());
        }
        let cw = field(&e, "closedWorld")?;
        if rank(
            optional(cw, "exportsClosed")?,
            &["closed", "open", "unknown"],
            2,
        ) > rank(
            optional(&worst["closedWorld"], "exportsClosed")?,
            &["closed", "open", "unknown"],
            2,
        ) {
            worst.insert("closedWorld".into(), cw.clone());
        }
        let deficiency = field(&e, "deficiency")?;
        if deficiency != &V::Null
            && !is(deficiency, "")
            && (worst["deficiency"] == V::Null || is(&worst["deficiency"], ""))
        {
            worst.insert("deficiency".into(), deficiency.clone());
            worst.insert("nativeCause".into(), field(&e, "nativeCause")?.clone());
        }
        let mut kinds = arr(&worst["derivationKinds"])?.to_vec();
        // Python dict.fromkeys also removes duplicates already in the first carrier.
        kinds.extend_from_slice(arr(field(&e, "derivationKinds")?)?);
        let mut unique = alloc::vec::Vec::new();
        for k in kinds {
            if !unique.contains(&k) {
                unique.push(k)
            }
        }
        worst.insert("derivationKinds".into(), V::Array(unique));
    }
    Ok((
        V::Object(worst),
        covs.iter().map(|(id, _)| id.clone()).collect(),
    ))
}
fn sufficiency_v2(
    req: &V,
    view: &V,
    target_exported: bool,
    target_affected: bool,
    depth: usize,
    reg: &V,
    work: &mut usize,
) -> Result<V, Error> {
    tick(work)?;
    let relation = text(field(req, "relation")?)?;
    let missing = || {
        record([
            ("satisfied", V::Bool(false)),
            ("deficiency", string("required-relation-missing")),
            ("disclosures", V::Array(alloc::vec![])),
            (
                "causes",
                V::Array(alloc::vec![string("required-relation-missing")]),
            ),
        ])
    };
    let Some(entry) = obj(view)?.get(relation).filter(|v| *v != &V::Null) else {
        return Ok(missing());
    };
    let (Some(have), Some(need)) = (
        rung_index(reg, relation, field(entry, "resolution")?)?,
        rung_index(reg, relation, field(req, "minResolution")?)?,
    ) else {
        return Ok(missing());
    };
    let scanner = field(reg, "scanner")?;
    let fallback = string("required-relation-missing");
    let rung_cause = obj(field(scanner, "rungCause")?)?
        .get(text(defaulted(entry, "rungUnavailableBecause", &string(""))?).unwrap_or(""))
        .unwrap_or(&fallback);
    let mut causes = alloc::vec::Vec::new();
    let mut disclosures = alloc::vec::Vec::new();
    if have < need {
        causes.push(rung_cause.clone())
    }
    if number(defaulted(
        entry,
        "confidenceMillionths",
        &integer(1_000_000)?,
    )?)? < number(defaulted(req, "minConfidenceMillionths", &integer(0)?)?)?
    {
        causes.push(string("confidence-floor-unmet"))
    }
    if relation == "types"
        && is(optional(req, "derivationPolicy")?, "declared-only")
        && arr(defaulted(
            entry,
            "derivationKinds",
            &V::Array(alloc::vec![]),
        )?)?
        .contains(&string("compiler-inferred"))
    {
        causes.push(string("derivation-policy-unmet"))
    }
    if is(field(req, "completeness")?, "complete") && !is(optional(entry, "coverage")?, "complete")
    {
        let d = optional(entry, "deficiency")?;
        causes.push(if d == &V::Null || is(d, "") {
            rung_cause.clone()
        } else {
            d.clone()
        });
    }
    let quantifier = defaulted(req, "quantifier", &string("existential"))?.clone();
    if is(&quantifier, "universal-negative") {
        let default_rc = record([
            ("state", string("not-applicable")),
            ("unresolvedEdgeCount", integer(0)?),
            ("unresolvedEdgeClasses", V::Array(alloc::vec![])),
        ]);
        let rc = defaulted(entry, "resolutionCompleteness", &default_rc)?;
        let state = field(rc, "state")?;
        if is(state, "partial") || is(state, "not-attempted") {
            causes.push(string("resolution-incomplete"))
        } else if is(state, "incomplete") || target_affected {
            if is(
                defaulted(req, "unresolvedEdgePolicy", &string("forbid"))?,
                "forbid",
            ) {
                causes.push(string("resolution-incomplete"))
            } else {
                disclosures.push(record([
                    ("kind", string("unresolved-edges")),
                    (
                        "count",
                        defaulted(rc, "unresolvedEdgeCount", &integer(0)?)?.clone(),
                    ),
                    (
                        "classes",
                        defaulted(rc, "unresolvedEdgeClasses", &V::Array(alloc::vec![]))?.clone(),
                    ),
                ]))
            }
        }
        let default_cw = record([("exportsClosed", string("unknown"))]);
        let cw = defaulted(entry, "closedWorld", &default_cw)?;
        if target_exported && !is(optional(cw, "exportsClosed")?, "closed") {
            if is(
                defaulted(req, "externalConsumerPolicy", &string("forbid"))?,
                "forbid",
            ) {
                causes.push(string("external-consumers-unknown"))
            } else {
                disclosures.push(record([
                    ("kind", string("external-consumers-assumed-closed")),
                    ("exportsClosed", optional(cw, "exportsClosed")?.clone()),
                ]))
            }
        }
    }
    if depth < 4
        && let Some(deps) = obj(field(scanner, "dependsOn")?)?.get(relation)
    {
        for dep in arr(deps)? {
            let mut sub = obj(dep)?.clone();
            sub.insert(
                "completeness".into(),
                string(if is(&quantifier, "existential") {
                    "partial-ok"
                } else {
                    "complete"
                }),
            );
            sub.insert("quantifier".into(), quantifier.clone());
            for key in ["unresolvedEdgePolicy", "externalConsumerPolicy"] {
                sub.insert(key.into(), defaulted(req, key, &string("forbid"))?.clone());
            }
            let result = sufficiency_v2(
                &V::Object(sub),
                view,
                target_exported,
                target_affected,
                depth + 1,
                reg,
                work,
            )?;
            causes.extend_from_slice(arr(field(&result, "causes")?)?);
            disclosures.extend_from_slice(arr(field(&result, "disclosures")?)?);
        }
    }
    let mut result = obj(&record([
        ("satisfied", V::Bool(causes.is_empty())),
        ("disclosures", V::Array(disclosures)),
        ("causes", V::Array(causes.clone())),
    ]))?
    .clone();
    if !causes.is_empty() {
        let order = arr(field(scanner, "sufficiencyPrecedence")?)?;
        // An unregistered deficiency is an invalid admitted carrier, never a new precedence.
        let mut best = None;
        for c in causes {
            let index = order.iter().position(|v| v == &c).ok_or(Error::Law)?;
            if best.as_ref().is_none_or(|(i, _)| index < *i) {
                best = Some((index, c));
            }
        }
        result.insert("deficiency".into(), best.ok_or(Error::Law)?.1);
    }
    Ok(V::Object(result))
}

fn integer(n: i128) -> Result<V, Error> {
    Ok(V::Integer(
        opensip_identity::JsonInteger::new(n).map_err(|_| Error::Law)?,
    ))
}

fn map_or_empty<'a>(v: &'a V, k: &str) -> Result<Option<&'a BTreeMap<String, V>>, Error> {
    match optional(v, k)? {
        V::Null => Ok(None),
        other => Ok(Some(obj(other)?)),
    }
}
fn family_of<'a>(reg: &'a V, value: &V, language: bool) -> Result<Option<&'a str>, Error> {
    for (family, row) in obj(field(
        field(field(reg, "scanner")?, "engineFamilies")?,
        "families",
    )?)? {
        if if language {
            arr(field(row, "languageModes")?)?.contains(value)
        } else {
            field(row, "universeDomain")? == value
        } {
            return Ok(Some(family));
        }
    }
    Ok(None)
}
fn owed_source_bindings(
    relation: &str,
    inputs: &V,
    reg: &V,
) -> Result<(alloc::vec::Vec<V>, alloc::vec::Vec<V>), Error> {
    let mut available = alloc::vec::Vec::new();
    let mut unavailable = alloc::vec::Vec::new();
    let plan = optional(inputs, "enumerationPlan")?;
    if plan == &V::Null {
        return Ok((available, unavailable));
    }
    let cap = obj(field(field(reg, "scanner")?, "capabilityForRelation")?)?
        .get(relation)
        .unwrap_or(&V::Null);
    for (cell_ordinal, cell) in rows(plan, "cells")?.iter().enumerate() {
        if optional(cell, "capabilityId")? != cap {
            continue;
        }
        let family = family_of(reg, optional(cell, "languageMode")?, true)?;
        for (program_ordinal, binding) in rows(cell, "programBindings")?.iter().enumerate() {
            let mut b = obj(binding)?.clone();
            b.insert("_cellOrdinal".into(), integer(cell_ordinal as i128)?);
            b.insert("_programOrdinal".into(), integer(program_ordinal as i128)?);
            b.insert(
                "_languageMode".into(),
                optional(cell, "languageMode")?.clone(),
            );
            b.insert("_family".into(), family.map(string).unwrap_or(V::Null));
            b.insert(
                "_workspaceRoot".into(),
                optional(cell, "workspaceRoot")?.clone(),
            );
            let enumerator = map_or_empty(binding, "enumerator")?
                .and_then(|v| v.get("closureId"))
                .cloned()
                .unwrap_or(V::Null);
            b.insert("_enumerator".into(), enumerator);
            if optional(binding, "universe")? == &V::Null {
                unavailable.push(V::Object(b))
            } else {
                available.push(V::Object(b))
            }
        }
    }
    Ok((available, unavailable))
}
fn coverages_exact(
    inputs: &V,
    relation: &str,
    rung: &str,
    source: &str,
    target: Option<&str>,
) -> Result<alloc::vec::Vec<(String, V)>, Error> {
    let mut out = alloc::vec::Vec::new();
    if let Some(covs) = map_or_empty(inputs, "coverages")? {
        for (id, cov) in covs {
            let Some(key) = map_or_empty(cov, "key")? else {
                continue;
            };
            if key.get("relation") == Some(&string(relation))
                && key.get("resolution") == Some(&string(rung))
                && key.get("sourceUniverse") == Some(&string(source))
                && target.is_none_or(|t| key.get("targetUniverse") == Some(&string(t)))
            {
                out.push((id.clone(), cov.clone()))
            }
        }
    }
    Ok(out)
}
fn scopes_exact(
    inputs: &V,
    relation: &str,
    rung: &str,
    source: &str,
) -> Result<alloc::vec::Vec<(String, V)>, Error> {
    let mut out = alloc::vec::Vec::new();
    if let Some(scopes) = map_or_empty(inputs, "scopes")? {
        for (id, scope) in scopes {
            if is(optional(scope, "relation")?, relation)
                && is(optional(scope, "resolution")?, rung)
                && is(optional(scope, "sourceUniverse")?, source)
            {
                out.push((id.clone(), scope.clone()))
            }
        }
    }
    Ok(out)
}
fn unique_pairs(pairs: alloc::vec::Vec<(String, V)>) -> alloc::vec::Vec<(String, V)> {
    let mut out = BTreeMap::new();
    for (id, v) in pairs {
        out.entry(id).or_insert(v);
    }
    out.into_iter().collect()
}
fn depends_chain(relation: &str, reg: &V) -> Result<alloc::vec::Vec<V>, Error> {
    let deps = obj(field(field(reg, "scanner")?, "dependsOn")?)?;
    let mut stack = deps
        .get(relation)
        .map(arr)
        .transpose()?
        .unwrap_or(&[])
        .to_vec();
    let mut cursor = 0;
    let mut seen = alloc::collections::BTreeSet::new();
    let mut out = alloc::vec::Vec::new();
    while let Some(dep) = stack.get(cursor).cloned() {
        cursor += 1;
        let rel = text(field(&dep, "relation")?)?;
        if !seen.insert(rel.to_string()) {
            continue;
        }
        if let Some(more) = deps.get(rel) {
            stack.extend_from_slice(arr(more)?)
        }
        out.push(dep);
    }
    Ok(out)
}
fn inventory_population(
    kind: &str,
    universe: &str,
    inventories: &[V],
    plan: Option<&V>,
) -> Result<(alloc::collections::BTreeSet<String>, bool), Error> {
    let mut ids = alloc::collections::BTreeSet::new();
    let mut unknown = false;
    let mut saw = false;
    for inv in inventories {
        if !is(optional(inv, "kind")?, kind) || !is(inventory_universe(inv, plan)?, universe) {
            continue;
        }
        saw = true;
        if is(optional(inv, "state")?, "unavailable") {
            unknown = true;
            continue;
        }
        unknown |= is(optional(inv, "state")?, "partial");
        for row in rows(inv, "rows")? {
            ids.insert(text(field(row, "nativeSubjectId")?)?.to_string());
        }
        if kind == "file" {
            for path in rows(inv, "examinedPaths")? {
                ids.insert(text(path)?.to_string());
            }
        }
    }
    Ok((ids, unknown || !saw))
}
fn expected_source_ids(
    binding: &V,
    kind: &str,
    inventories: &[V],
    plan: Option<&V>,
) -> Result<(alloc::collections::BTreeSet<String>, bool), Error> {
    let (mut ids, unknown) =
        inventory_population(kind, text(field(binding, "universe")?)?, inventories, plan)?;
    if kind == "file" {
        for extent in rows(binding, "extents")? {
            if is(optional(extent, "kind")?, "file") {
                for path in rows(extent, "paths")? {
                    ids.insert(text(path)?.to_string());
                }
            }
        }
    }
    Ok((ids, unknown))
}
type IncomingGroups = BTreeMap<Option<String>, alloc::vec::Vec<(String, V)>>;
fn incoming_groups(bindings: &[V], scopes: &[(String, V)]) -> Result<IncomingGroups, Error> {
    let mut contributors = alloc::vec::Vec::new();
    for binding in bindings {
        let pc = optional(binding, "_enumerator")?;
        let pc = if pc == &V::Null {
            None
        } else {
            Some(text(pc)?.to_string())
        };
        if !contributors.contains(&pc) {
            contributors.push(pc)
        }
    }
    let mut tagged = alloc::vec::Vec::new();
    let mut untagged = alloc::vec::Vec::new();
    for (id, scope) in scopes {
        let pc = optional(scope, "enumeratorClosure")?;
        if pc == &V::Null || is(pc, "") {
            untagged.push((id.clone(), scope.clone()))
        } else {
            tagged.push((Some(text(pc)?.to_string()), (id.clone(), scope.clone())))
        }
    }
    let mut out = BTreeMap::new();
    if !contributors.is_empty() {
        for pc in &contributors {
            out.insert(pc.clone(), alloc::vec::Vec::new());
        }
        if tagged.is_empty() {
            for value in out.values_mut() {
                *value = scopes.to_vec()
            }
        } else {
            for (pc, scope) in tagged {
                out.entry(pc).or_default().push(scope)
            }
            for pc in contributors {
                out.get_mut(&pc).ok_or(Error::Law)?.extend(untagged.clone());
            }
        }
    } else if !tagged.is_empty() {
        for (pc, scope) in tagged {
            out.entry(pc)
                .or_insert_with(alloc::vec::Vec::new)
                .push(scope)
        }
    } else {
        out.insert(None, scopes.to_vec());
    }
    Ok(out)
}

struct NativeScanner<'a, 'b> {
    inputs: &'a V,
    registry: &'a V,
    retained: &'a opensip_identity::RetainedInputs<'b>,
    work: usize,
    descriptor_work: usize,
}
impl NativeScanner<'_, '_> {
    fn scope_commitment(&mut self, scope: &V) -> Result<String, Error> {
        tick(&mut self.work)?;
        let mut descriptor = BTreeMap::new();
        for k in [
            "schemaVersion",
            "snapshotId",
            "sourceUniverse",
            "targetUniverse",
            "relation",
            "resolution",
            "enumeratorClosure",
            "subjects",
        ] {
            if let Some(v) = obj(scope)?.get(k) {
                descriptor.insert(k.into(), v.clone());
            }
        }
        if let Some(V::Array(subjects)) = descriptor.get_mut("subjects") {
            let mut keyed = alloc::vec::Vec::new();
            for subject in subjects.iter() {
                keyed.push((
                    opensip_identity::canonical_bytes(subject)
                        .map_err(|_| Error::Refused("ATOM_NATIVE_CARRIER"))?,
                    subject.clone(),
                ))
            }
            keyed.sort_by(|a, b| a.0.cmp(&b.0));
            *subjects = keyed.into_iter().map(|(_, v)| v).collect();
        }
        let descriptor = V::Object(descriptor);
        self.retained
            .check_identity_value_shape(&descriptor, "subject-scope", self.descriptor_work)
            .map_err(|_| Error::Refused("ATOM_NATIVE_CARRIER"))?;
        let digest = opensip_identity::hash_canonical_value("subject-scope", &descriptor)
            .map_err(|_| Error::Refused("ATOM_NATIVE_CARRIER"))?;
        Ok(alloc::format!(
            "sha256:{}",
            opensip_identity::digest_hex(&digest)
        ))
    }
    fn pair_scope_coverages(
        &mut self,
        sid: &str,
        scope: &V,
        covs: &[(String, V)],
    ) -> Result<alloc::vec::Vec<(String, V)>, Error> {
        let derived = self.scope_commitment(scope)?;
        let mapping = map_or_empty(self.inputs, "coverageScopes")?;
        let mut seen = alloc::collections::BTreeSet::new();
        let mut found = alloc::vec::Vec::new();
        for (id, cov) in covs {
            tick(&mut self.work)?;
            let mapped = mapping.and_then(|m| m.get(id)).is_some_and(|v| is(v, sid));
            let committed = map_or_empty(cov, "key")?
                .and_then(|m| m.get("subjectScopeCommitment"))
                .is_some_and(|v| is(v, &derived));
            if (mapped || committed) && seen.insert(id.clone()) {
                found.push((id.clone(), cov.clone()))
            }
        }
        Ok(found)
    }
    fn select_dep_coverages(
        &mut self,
        dep: &V,
        source: &str,
        target: Option<&str>,
        subjects: Option<&alloc::collections::BTreeSet<String>>,
        kind: Option<&str>,
    ) -> Result<alloc::vec::Vec<(String, V)>, Error> {
        let relation = text(field(dep, "relation")?)?;
        let rung = text(field(dep, "minResolution")?)?;
        let covs = coverages_exact(self.inputs, relation, rung, source, target)?;
        if covs.is_empty() {
            return Ok(covs);
        }
        let dep_kind = optional(
            field(field(self.registry, "relations")?, relation)?,
            "sourceSubjectKind",
        )?;
        if subjects.is_none() || kind.is_some_and(|k| !is(dep_kind, k)) {
            return Ok(covs);
        }
        let subjects = subjects.ok_or(Error::Law)?;
        let mut paired = alloc::vec::Vec::new();
        for (sid, scope) in scopes_exact(self.inputs, relation, rung, source)? {
            tick(&mut self.work)?;
            if !rows(&scope, "subjects")?
                .iter()
                .any(|v| text(v).is_ok_and(|s| subjects.contains(s)))
            {
                continue;
            }
            paired.extend(self.pair_scope_coverages(&sid, &scope, &covs)?);
        }
        Ok(unique_pairs(paired))
    }
    fn dependency_gaps(
        &mut self,
        relation: &str,
        source: &str,
        target: Option<&str>,
        owed: &alloc::collections::BTreeSet<String>,
        kind: Option<&str>,
        view: &V,
    ) -> Result<alloc::vec::Vec<String>, Error> {
        if owed.is_empty() {
            return Ok(alloc::vec::Vec::new());
        }
        let mut gaps = alloc::vec::Vec::new();
        for dep in depends_chain(relation, self.registry)? {
            tick(&mut self.work)?;
            let rel = text(field(&dep, "relation")?)?;
            let rung = text(field(&dep, "minResolution")?)?;
            let dep_kind = optional(
                field(field(self.registry, "relations")?, rel)?,
                "sourceSubjectKind",
            )?;
            if !obj(view)?.contains_key(rel) || kind.is_some_and(|k| !is(dep_kind, k)) {
                continue;
            }
            let covs = coverages_exact(self.inputs, rel, rung, source, target)?;
            let mut covered = alloc::collections::BTreeSet::new();
            for (sid, scope) in scopes_exact(self.inputs, rel, rung, source)? {
                let held = rows(&scope, "subjects")?
                    .iter()
                    .map(text)
                    .collect::<Result<alloc::vec::Vec<_>, _>>()?
                    .into_iter()
                    .filter(|id| owed.contains(*id))
                    .map(ToString::to_string)
                    .collect::<alloc::collections::BTreeSet<_>>();
                if !held.is_empty() && !self.pair_scope_coverages(&sid, &scope, &covs)?.is_empty() {
                    covered.extend(held)
                }
            }
            if !owed.is_subset(&covered) {
                gaps.push(rel.into())
            }
        }
        Ok(gaps)
    }
    fn add_dependencies(
        &mut self,
        relation: &str,
        source: &str,
        target: Option<&str>,
        subjects: Option<&alloc::collections::BTreeSet<String>>,
        kind: Option<&str>,
        primary: V,
    ) -> Result<(V, alloc::vec::Vec<String>), Error> {
        let mut view = BTreeMap::from([(relation.into(), primary)]);
        let mut cited = alloc::vec::Vec::new();
        for dep in depends_chain(relation, self.registry)? {
            let covs = self.select_dep_coverages(&dep, source, target, subjects, kind)?;
            if covs.is_empty() {
                continue;
            }
            let (entry, ids) = conservative_entry(&covs)?;
            view.insert(text(field(&dep, "relation")?)?.into(), entry);
            cited.extend(ids);
        }
        Ok((V::Object(view), cited))
    }
    fn source_coverages(
        &mut self,
        relation: &str,
        rung: &str,
        source: &str,
        native_id: &str,
    ) -> Result<SourceCoverages, Error> {
        let scopes = scopes_exact(self.inputs, relation, rung, source)?;
        let covs = coverages_exact(self.inputs, relation, rung, source, None)?;
        let mut paired = alloc::vec::Vec::new();
        let mut containing = alloc::vec::Vec::new();
        let mut unmatched = alloc::vec::Vec::new();
        for (sid, scope) in scopes {
            tick(&mut self.work)?;
            if !rows(&scope, "subjects")?.contains(&string(native_id)) {
                continue;
            }
            containing.push(sid.clone());
            let found = self.pair_scope_coverages(&sid, &scope, &covs)?;
            if found.is_empty() {
                unmatched.push(sid)
            } else {
                paired.extend(found)
            }
        }
        Ok(SourceCoverages {
            paired: unique_pairs(paired),
            containing,
            unmatched,
        })
    }
}
struct SourceCoverages {
    paired: alloc::vec::Vec<(String, V)>,
    containing: alloc::vec::Vec<String>,
    unmatched: alloc::vec::Vec<String>,
}

fn input_plan(inputs: &V) -> Result<Option<&V>, Error> {
    Ok(match optional(inputs, "enumerationPlan")? {
        V::Null => None,
        v => Some(v),
    })
}
fn subject_rows<'a>(subject: &V, inputs: &'a V) -> Result<alloc::vec::Vec<&'a V>, Error> {
    let path = optional(subject, "packageManifestPath")?;
    lookup_rows(
        field(subject, "nativeSubjectId")?,
        field(subject, "universe")?,
        Some(field(subject, "kind")?),
        if path == &V::Null { None } else { Some(path) },
        rows(inputs, "inventories")?,
        input_plan(inputs)?,
    )
}
fn export_flag(subject: &V, inputs: &V) -> Result<(bool, alloc::vec::Vec<V>), Error> {
    let rows = subject_rows(subject, inputs)?;
    let unknown = || -> Result<(bool, alloc::vec::Vec<V>), Error> {
        Ok((
            true,
            alloc::vec![cause(
                "target-export-unknown",
                None,
                None,
                &[("universe", field(subject, "universe")?.clone())]
            )?],
        ))
    };
    if rows.is_empty() {
        return unknown();
    }
    if !is(field(subject, "kind")?, "symbol") {
        return Ok((false, alloc::vec![]));
    }
    let mut flags = alloc::vec::Vec::new();
    for row in rows {
        if is(optional(row, "kind")?, "symbol") {
            let flag = optional(row, "exported")?;
            if !flags.contains(&flag) {
                flags.push(flag)
            }
        }
    }
    if flags.len() == 1 {
        if is(flags[0], "exported") {
            return Ok((true, alloc::vec![]));
        }
        if is(flags[0], "not-exported") {
            return Ok((false, alloc::vec![]));
        }
    }
    unknown()
}
fn target_affected(
    subject: &V,
    source: &str,
    inputs: &V,
) -> Result<(bool, alloc::vec::Vec<V>), Error> {
    let rows = subject_rows(subject, inputs)?;
    let path = if rows.len() == 1 {
        optional(rows[0], "path")?
    } else {
        &V::Null
    };
    let mut affected = false;
    let mut unknown = false;
    if let Some(facts) = map_or_empty(inputs, "facts")? {
        for fact in facts.values() {
            if !is(optional(fact, "relation")?, "unresolved-edge")
                || !is(optional(fact, "sourceUniverse")?, source)
            {
                continue;
            }
            let payload = field(fact, "payload")?;
            match text(optional(payload, "targetScope")?).unwrap_or("") {
                "universe" | "unknown" | "external" => affected = true,
                "module" => {
                    let module = optional(payload, "targetModule")?;
                    if module == &V::Null {
                        unknown = true;
                        continue;
                    }
                    if let (V::String(path), V::String(module)) = (path, module) {
                        if path == module
                            || path
                                .starts_with(&alloc::format!("{}/", module.trim_end_matches('/')))
                        {
                            affected = true
                        } else {
                            unknown = true
                        }
                    } else {
                        unknown = true
                    }
                }
                _ => {}
            }
        }
    }
    let mut causes = alloc::vec::Vec::new();
    if unknown && !affected {
        causes.push(cause(
            "unresolved-edge-target-unattributed",
            None,
            None,
            &[("universe", string(source))],
        )?);
        affected = true
    }
    Ok((affected, causes))
}
struct NativeRequirement<'a> {
    relation: &'a str,
    rung: &'a str,
    subject: &'a V,
    endpoint: &'a str,
}
struct NativeCompleteness {
    complete: bool,
    unknown: bool,
    causes: alloc::vec::Vec<V>,
    coverages: alloc::vec::Vec<String>,
    scopes: alloc::vec::Vec<String>,
    deficiencies: alloc::vec::Vec<V>,
}
impl NativeCompleteness {
    fn unknown() -> Self {
        Self {
            complete: false,
            unknown: true,
            causes: alloc::vec![],
            coverages: alloc::vec![],
            scopes: alloc::vec![],
            deficiencies: alloc::vec![],
        }
    }
    fn add_cause(&mut self, code: &str, source: Option<&str>) -> Result<(), Error> {
        self.causes.push(cause(
            code,
            None,
            None,
            &[("universe", source.map(string).unwrap_or(V::Null))],
        )?);
        Ok(())
    }
}
fn family_owed(a: Option<&str>, b: Option<&str>) -> bool {
    !matches!((a,b),(Some(a),Some(b)) if !a.is_empty() && !b.is_empty() && a!=b)
}
fn attestation_proves_search(att: &V) -> Result<bool, Error> {
    Ok(optional(att, "completeSearch")? == &V::Bool(true)
        && is(optional(att, "coverage")?, "complete")
        && optional(att, "examinedExhaustive")? == &V::Bool(true)
        && map_or_empty(att, "resolutionCompleteness")?.and_then(|v| v.get("examinedExhaustive"))
            == Some(&V::Bool(true)))
}
fn entry_from_attestation(rung: &str, att: &V) -> Result<V, Error> {
    Ok(record([
        ("resolution", string(rung)),
        ("coverage", field(att, "coverage")?.clone()),
        ("confidenceMillionths", integer(1_000_000)?),
        (
            "resolutionCompleteness",
            field(att, "resolutionCompleteness")?.clone(),
        ),
        ("closedWorld", field(att, "closedWorld")?.clone()),
        ("derivationKinds", V::Array(alloc::vec![])),
        ("deficiency", V::Null),
        ("nativeCause", V::Null),
        ("rungUnavailableBecause", string("")),
    ]))
}
impl NativeScanner<'_, '_> {
    fn run_sufficiency(
        &mut self,
        req: &NativeRequirement<'_>,
        source: &str,
        view: &V,
        gaps: &[String],
        out: &mut NativeCompleteness,
    ) -> Result<bool, Error> {
        let resolved = arr(field(field(self.registry, "scanner")?, "resolvedRungs")?)?
            .contains(&string(req.rung));
        let requirement = record([
            ("relation", string(req.relation)),
            ("minResolution", string(req.rung)),
            ("completeness", string("complete")),
            (
                "quantifier",
                string(if resolved {
                    "universal-negative"
                } else {
                    "existential"
                }),
            ),
            ("minConfidenceMillionths", integer(0)?),
            ("derivationPolicy", string("any")),
            ("unresolvedEdgePolicy", string("forbid")),
            ("externalConsumerPolicy", string("forbid")),
        ]);
        let mut satisfied = true;
        for reduced in [false, true] {
            if reduced && gaps.is_empty() {
                continue;
            }
            let mut altered = obj(view)?.clone();
            if reduced {
                altered.retain(|k, _| !gaps.contains(k));
            }
            let (exported, mut extra) = if req.endpoint == "target" {
                export_flag(req.subject, self.inputs)?
            } else {
                (false, alloc::vec![])
            };
            let (affected, more) = if req.endpoint == "target" {
                target_affected(req.subject, source, self.inputs)?
            } else {
                (false, alloc::vec![])
            };
            extra.extend(more);
            let result = sufficiency_v2(
                &requirement,
                &V::Object(altered),
                exported,
                affected,
                0,
                self.registry,
                &mut self.work,
            )?;
            out.deficiencies
                .extend_from_slice(arr(field(&result, "causes")?)?);
            if let Some(deficiency) = obj(&result)?.get("deficiency") {
                out.deficiencies.push(deficiency.clone())
            }
            out.causes.extend(extra);
            satisfied &= field(&result, "satisfied")? == &V::Bool(true);
        }
        if !satisfied {
            // The selected Python view inserts the primary relation before recursive dependencies.
            // Preserve that precedence independently of the Rust map's lexical key order.
            let mut relations = alloc::vec![req.relation.to_string()];
            for dep in depends_chain(req.relation, self.registry)? {
                relations.push(text(field(&dep, "relation")?)?.into())
            }
            let mut native = None;
            for relation in relations {
                if let Some(entry) = obj(view)?.get(&relation) {
                    let nc = optional(entry, "nativeCause")?;
                    if nc != &V::Null && !is(nc, "") {
                        native = Some(text(nc)?);
                        break;
                    }
                }
            }
            out.causes.push(cause(
                "coverage-unknown",
                None,
                native,
                &[("universe", string(source))],
            )?);
        }
        Ok(satisfied)
    }
    fn native_completeness(
        &mut self,
        atom: &V,
        subject: &V,
        spec: &V,
    ) -> Result<NativeCompleteness, Error> {
        let relation = text(field(atom, "relation")?)?;
        let rung = text(field(atom, "minResolution")?)?;
        let endpoint = text(defaulted(atom, "endpoint", &string("source"))?)?.to_string();
        let u = text(field(subject, "universe")?)?;
        let native = text(field(subject, "nativeSubjectId")?)?;
        let req = NativeRequirement {
            relation,
            rung,
            subject,
            endpoint: &endpoint,
        };
        let mut out = NativeCompleteness::unknown();
        let (available, unavailable) = owed_source_bindings(relation, self.inputs, self.registry)?;
        let domain = map_or_empty(self.inputs, "universeDomains")?
            .and_then(|m| m.get(u))
            .unwrap_or(&V::Null);
        let family = family_of(self.registry, domain, false)?;
        for binding in &unavailable {
            let bfamily = optional(binding, "_family")?;
            let bfamily = if bfamily == &V::Null {
                None
            } else {
                Some(text(bfamily)?)
            };
            if !family_owed(bfamily, family) {
                out.add_cause("cross-family-edge-not-owed", None)?;
                continue;
            }
            if endpoint == "target" {
                out.add_cause("unavailable-program-binding", None)?
            }
        }
        if available.is_empty() && unavailable.is_empty() {
            out.add_cause("missing-relation-coverage", None)?;
            return Ok(out);
        }
        let mut bound = false;
        for b in &available {
            bound |= is(optional(b, "universe")?, u)
        }
        let current_kind = text(field(subject, "kind")?)?;
        if endpoint == "source" {
            if !bound {
                out.add_cause("selector-unbound", None)?;
                return Ok(out);
            }
            let selection = self.source_coverages(relation, rung, u, native)?;
            out.scopes.extend(selection.containing.clone());
            if selection.containing.is_empty() {
                out.add_cause("uncovered-expected-source-subject", Some(u))?;
                return Ok(out);
            }
            for _ in &selection.unmatched {
                out.add_cause("scope-without-coverage", Some(u))?
            }
            if !selection.unmatched.is_empty() || selection.paired.is_empty() {
                return Ok(out);
            }
            let subjects = alloc::collections::BTreeSet::from([native.to_string()]);
            let mut ok = true;
            for (cid, cov) in selection.paired {
                out.coverages.push(cid);
                let target = map_or_empty(&cov, "key")?.and_then(|m| m.get("targetUniverse"));
                let target = target.filter(|v| *v != &V::Null).map(text).transpose()?;
                let (view, extra) = self.add_dependencies(
                    relation,
                    u,
                    target,
                    Some(&subjects),
                    Some(current_kind),
                    entry_from_cov(&cov)?,
                )?;
                let gaps = self.dependency_gaps(
                    relation,
                    u,
                    target,
                    &subjects,
                    Some(current_kind),
                    &view,
                )?;
                out.coverages.extend(extra);
                ok &= self.run_sufficiency(&req, u, &view, &gaps, &mut out)?;
            }
            let mut blocking = false;
            for c in &out.causes {
                blocking |= !is(optional(c, "code")?, "cross-family-edge-not-owed")
            }
            out.unknown = blocking || !ok;
            out.complete = ok && !out.unknown;
            return Ok(out);
        }
        let source_kind =
            text(defaulted(spec, "sourceSubjectKind", &string("symbol"))?)?.to_string();
        let mut ok_all = true;
        out.unknown = false;
        if !bound {
            out.add_cause("selector-unbound", None)?;
            ok_all = false;
            out.unknown = true
        }
        for b in &unavailable {
            let bfamily = optional(b, "_family")?;
            if family_owed(
                if bfamily == &V::Null {
                    None
                } else {
                    Some(text(bfamily)?)
                },
                family,
            ) {
                out.unknown = true
            }
        }
        let mut by_u: alloc::vec::Vec<(String, alloc::vec::Vec<V>)> = alloc::vec![];
        for b in available {
            let source = text(field(&b, "universe")?)?.to_string();
            if let Some((_, bindings)) = by_u.iter_mut().find(|(s, _)| s == &source) {
                bindings.push(b)
            } else {
                by_u.push((source, alloc::vec![b]))
            }
        }
        for (source, bindings) in by_u {
            tick(&mut self.work)?;
            let explicit = optional(&bindings[0], "_family")?;
            let domain = map_or_empty(self.inputs, "universeDomains")?
                .and_then(|m| m.get(&source))
                .unwrap_or(&V::Null);
            let source_family = if explicit == &V::Null || is(explicit, "") {
                family_of(self.registry, domain, false)?
            } else {
                Some(text(explicit)?)
            };
            if !family_owed(source_family, family) {
                out.add_cause("cross-family-edge-not-owed", Some(&source))?;
                continue;
            }
            let mut expected = alloc::collections::BTreeSet::new();
            let mut exp_unknown = false;
            for b in &bindings {
                let (ids, unknown) = expected_source_ids(
                    b,
                    &source_kind,
                    rows(self.inputs, "inventories")?,
                    input_plan(self.inputs)?,
                )?;
                expected.extend(ids);
                exp_unknown |= unknown
            }
            if exp_unknown {
                out.add_cause("population-unknown", Some(&source))?;
                out.unknown = true
            }
            let scopes = scopes_exact(self.inputs, relation, rung, &source)?;
            let covs = coverages_exact(self.inputs, relation, rung, &source, None)?;
            let groups = incoming_groups(&bindings, &scopes)?;
            let mut present = alloc::collections::BTreeSet::new();
            for (sid, sc) in &scopes {
                out.scopes.push(sid.clone());
                for id in rows(sc, "subjects")? {
                    present.insert(text(id)?.to_string());
                }
            }
            if !expected.is_subset(&present) {
                out.add_cause("uncovered-expected-source-subject", Some(&source))?;
                out.unknown = true
            }
            for (provider, group) in groups {
                let mut attestation = None;
                for att in rows(self.inputs, "incomingSearchAttestations")? {
                    if is(optional(att, "sourceUniverse")?, &source)
                        && is(optional(att, "targetUniverse")?, u)
                        && is(optional(att, "relation")?, relation)
                        && is(optional(att, "minResolution")?, rung)
                        && provider.as_ref().is_none_or(|pc| {
                            optional(att, "providerClosure").is_ok_and(|v| is(v, pc))
                        })
                    {
                        attestation = Some(att);
                        break;
                    }
                }
                let att_ok = match attestation {
                    Some(att) => attestation_proves_search(att)?,
                    None => false,
                };
                if att_ok {
                    let (view, extra) = self.add_dependencies(
                        relation,
                        &source,
                        Some(u),
                        None,
                        None,
                        entry_from_attestation(rung, attestation.ok_or(Error::Law)?)?,
                    )?;
                    out.coverages.extend(extra);
                    let mut owed = alloc::collections::BTreeSet::new();
                    for (_, sc) in &group {
                        for id in rows(sc, "subjects")? {
                            owed.insert(text(id)?.to_string());
                        }
                    }
                    let gaps = self.dependency_gaps(
                        relation,
                        &source,
                        Some(u),
                        &owed,
                        Some(&source_kind),
                        &view,
                    )?;
                    if !self.run_sufficiency(&req, &source, &view, &gaps, &mut out)? {
                        ok_all = false;
                        out.unknown = true
                    }
                }
                if group.is_empty() {
                    if !att_ok {
                        out.add_cause("source-target-search-unattested", Some(&source))?;
                        out.unknown = true;
                        ok_all = false
                    }
                    continue;
                }
                for (sid, sc) in group {
                    let found = self.pair_scope_coverages(&sid, &sc, &covs)?;
                    let mut found_target = false;
                    for (cid, cov) in &found {
                        out.coverages.push(cid.clone());
                        let target = optional(field(cov, "key")?, "targetUniverse")?;
                        found_target |= is(target, u);
                        let target = if target == &V::Null {
                            None
                        } else {
                            Some(text(target)?)
                        };
                        let owed = rows(&sc, "subjects")?
                            .iter()
                            .map(|v| text(v).map(ToString::to_string))
                            .collect::<Result<alloc::collections::BTreeSet<_>, _>>()?;
                        let (view, extra) = self.add_dependencies(
                            relation,
                            &source,
                            target,
                            Some(&owed),
                            Some(&source_kind),
                            entry_from_cov(cov)?,
                        )?;
                        out.coverages.extend(extra);
                        let gaps = self.dependency_gaps(
                            relation,
                            &source,
                            target,
                            &owed,
                            Some(&source_kind),
                            &view,
                        )?;
                        if !self.run_sufficiency(&req, &source, &view, &gaps, &mut out)? {
                            ok_all = false;
                            out.unknown = true
                        }
                    }
                    if found_target || att_ok {
                        continue;
                    }
                    out.add_cause(
                        if found.is_empty() {
                            "scope-without-coverage"
                        } else {
                            "source-target-search-unattested"
                        },
                        Some(&source),
                    )?;
                    out.unknown = true;
                    ok_all = false;
                }
            }
        }
        out.complete = ok_all && !out.unknown;
        Ok(out)
    }
}

struct EphemeralTarget {
    kind: V,
    occupancy: V,
    exported: V,
    native: V,
    package_path: V,
}
fn identity_keys(
    rows: &[&V],
) -> Result<alloc::collections::BTreeSet<(String, String, String)>, Error> {
    rows.iter()
        .map(|row| {
            let kind = text(field(row, "kind")?)?;
            Ok((
                kind.into(),
                text(field(row, "nativeSubjectId")?)?.into(),
                if kind == "package" {
                    text(field(row, "path")?)?.into()
                } else {
                    String::new()
                },
            ))
        })
        .collect()
}
fn ephemeral_target(fact: &V, spec: &V, inputs: &V) -> Result<EphemeralTarget, Error> {
    let mut out = EphemeralTarget {
        kind: string("unknown"),
        occupancy: string("unknown"),
        exported: V::Null,
        native: V::Null,
        package_path: V::Null,
    };
    let target = optional(spec, "targetNativeIdField")?;
    if target == &V::Null || is(target, "") {
        return Ok(out);
    }
    let native = optional(field(fact, "payload")?, text(target)?)?;
    if native == &V::Null {
        return Ok(out);
    }
    out.native = native.clone();
    let rows = lookup_rows(
        native,
        field(fact, "targetUniverse")?,
        None,
        None,
        rows(inputs, "inventories")?,
        input_plan(inputs)?,
    )?;
    if identity_keys(&rows)?.len() == 1 {
        let row = rows[0];
        out.kind = field(row, "kind")?.clone();
        out.occupancy = string("first-party");
        if is(&out.kind, "symbol") {
            out.exported = optional(row, "exported")?.clone()
        }
        if is(&out.kind, "package") {
            out.package_path = optional(row, "path")?.clone()
        }
    }
    Ok(out)
}
fn logical_path_grammar(path: &str) -> bool {
    !path.contains(['\\', '\0'])
        && path
            .split('/')
            .all(|p| !p.is_empty() && p.chars().count() <= 255)
}
fn symbol_grammar(id: &str) -> bool {
    let Some((prefix, body)) = id.split_once(':') else {
        return false;
    };
    !body.is_empty()
        && prefix
            .as_bytes()
            .first()
            .is_some_and(u8::is_ascii_lowercase)
        && prefix
            .bytes()
            .all(|b| b.is_ascii_lowercase() || b.is_ascii_digit() || b == b'-')
        && body
            .chars()
            .all(|c| c > '\u{1f}' && !('\u{7f}'..='\u{9f}').contains(&c))
}
fn join_sidecar(fact: &V, spec: &V, sc: &V, inputs: &V) -> Result<(), Error> {
    let pc = optional(sc, "producerClosure")?;
    if pc != optional(fact, "producerClosure")? {
        return Err(Error::Refused("TARGET_ATTRIBUTION_PRODUCER_MISMATCH"));
    }
    let closure =
        map_or_empty(inputs, "closures")?.and_then(|m| text(pc).ok().and_then(|p| m.get(p)));
    if !closure.is_some_and(|v| optional(v, "kind").is_ok_and(|k| is(k, "provider"))) {
        return Err(Error::Refused("TARGET_ATTRIBUTION_PRODUCER_NOT_PROVIDER"));
    }
    if optional(sc, "targetUniverse")? != optional(fact, "targetUniverse")? {
        return Err(Error::Refused("TARGET_ATTRIBUTION_UNIVERSE_MISMATCH"));
    }
    let target_field = optional(spec, "targetNativeIdField")?;
    let rungs = rows(spec, "endpointTargetRungs")?;
    if target_field == &V::Null
        || is(target_field, "")
        || (!rungs.is_empty() && !rungs.contains(optional(fact, "resolution")?))
    {
        return Err(Error::Refused("TARGET_ATTRIBUTION_FIELD_NOT_ON_RUNG"));
    }
    if optional(sc, "targetNativeId")? != optional(field(fact, "payload")?, text(target_field)?)? {
        return Err(Error::Refused("TARGET_ATTRIBUTION_NATIVE_ID_MISMATCH"));
    }
    let occ = optional(sc, "occupancy")?;
    let kind = optional(sc, "kind")?;
    let path = optional(sc, "packageManifestPath")?;
    let logical = optional(sc, "logicalPath")?;
    let exported = optional(sc, "exported")?;
    if is(occ, "first-party") && logical != &V::Null {
        return Err(Error::Refused(
            "TARGET_ATTRIBUTION_LOGICAL_PATH_ON_FIRST_PARTY",
        ));
    }
    if is(kind, "package") && logical != &V::Null {
        return Err(Error::Refused("TARGET_ATTRIBUTION_LOGICAL_PATH_ON_PACKAGE"));
    }
    if !is(kind, "symbol") && exported != &V::Null {
        return Err(Error::Refused("TARGET_ATTRIBUTION_EXPORTED_NOT_SYMBOL"));
    }
    if !is(kind, "package") && path != &V::Null {
        return Err(Error::Refused(
            "TARGET_ATTRIBUTION_PACKAGE_MANIFEST_NOT_PACKAGE",
        ));
    }
    if is(kind, "package")
        && (is(occ, "first-party") || is(occ, "external"))
        && (path == &V::Null || is(path, ""))
    {
        return Err(Error::Refused(
            "TARGET_ATTRIBUTION_PACKAGE_MANIFEST_REQUIRED",
        ));
    }
    if is(occ, "unknown") && path != &V::Null {
        return Err(Error::Refused("TARGET_ATTRIBUTION_PACKAGE_PATH_FORBIDDEN"));
    }
    let ev = optional(sc, "evaluationNativeId")?;
    if is(occ, "first-party") {
        if ev == &V::Null {
            return Err(Error::Refused("TARGET_ATTRIBUTION_EVALUATION_ID_REQUIRED"));
        }
        let valid = match text(kind)? {
            "file" => text(ev).is_ok_and(logical_path_grammar),
            "symbol" => text(ev).is_ok_and(symbol_grammar),
            "package" => text(ev).is_ok_and(|v| !v.is_empty()),
            _ => false,
        };
        if !valid {
            return Err(Error::Refused("TARGET_ATTRIBUTION_EVALUATION_GRAMMAR"));
        }
        if is(kind, "symbol") && ev != optional(sc, "targetNativeId")? {
            return Err(Error::Refused(
                "TARGET_ATTRIBUTION_SYMBOL_EVALUATION_ID_MISMATCH",
            ));
        }
    } else if ev != &V::Null {
        return Err(Error::Refused("TARGET_ATTRIBUTION_EVALUATION_ID_FORBIDDEN"));
    }
    let eph = ephemeral_target(fact, spec, inputs)?;
    let known = |k: &V| ["file", "symbol", "package"].iter().any(|s| is(k, s));
    if known(kind) && known(&eph.kind) && kind != &eph.kind {
        return Err(Error::Refused(
            "TARGET_ATTRIBUTION_KIND_INVENTORY_DISAGREEMENT",
        ));
    }
    let export_known = |v: &V| is(v, "exported") || is(v, "not-exported");
    if export_known(exported) && export_known(&eph.exported) && exported != &eph.exported {
        return Err(Error::Refused(
            "TARGET_ATTRIBUTION_EXPORTED_INVENTORY_DISAGREEMENT",
        ));
    }
    if is(occ, "external") && is(&eph.occupancy, "first-party") {
        return Err(Error::Refused(
            "TARGET_ATTRIBUTION_EXTERNAL_CONTRADICTS_FIRST_PARTY",
        ));
    }
    if is(occ, "first-party") {
        let rows = lookup_rows(
            ev,
            field(fact, "targetUniverse")?,
            Some(kind),
            if is(kind, "package") {
                Some(path)
            } else {
                None
            },
            rows(inputs, "inventories")?,
            input_plan(inputs)?,
        )?;
        if identity_keys(&rows)?.len() != 1 {
            return Err(Error::Refused(
                "TARGET_ATTRIBUTION_FIRST_PARTY_NOT_IN_INVENTORY",
            ));
        }
        if is(&eph.occupancy, "first-party")
            && (kind != &eph.kind
                || ev != &eph.native
                || if is(kind, "package") {
                    path != &eph.package_path
                } else {
                    false
                })
        {
            return Err(Error::Refused(
                "TARGET_ATTRIBUTION_EPHEMERAL_IDENTITY_CONFLICT",
            ));
        }
    }
    Ok(())
}
fn reconcile_attribution(fact: &V, spec: &V, inputs: &V) -> Result<V, Error> {
    let eph = ephemeral_target(fact, spec, inputs)?;
    let sidecar = map_or_empty(inputs, "targetAttributions")?
        .and_then(|m| {
            text(optional(fact, "factId").ok()?)
                .ok()
                .and_then(|id| m.get(id))
        })
        .filter(|v| !matches!(v, V::Array(_)));
    let Some(sc) = sidecar else {
        return Ok(record([
            ("kind", eph.kind),
            ("occupancy", eph.occupancy.clone()),
            ("exported", eph.exported),
            (
                "nativeId",
                if is(&eph.occupancy, "first-party") {
                    eph.native.clone()
                } else {
                    V::Null
                },
            ),
            ("payloadNativeId", eph.native),
            ("packageManifestPath", eph.package_path),
            (
                "source",
                string(if is(&eph.occupancy, "first-party") {
                    "ephemeral"
                } else {
                    "absent"
                }),
            ),
        ]));
    };
    join_sidecar(fact, spec, sc, inputs)?;
    let kind = if !is(&eph.kind, "unknown") {
        eph.kind.clone()
    } else {
        optional(sc, "kind")?.clone()
    };
    let exported = if eph.exported != V::Null && !is(&eph.exported, "unknown") {
        eph.exported.clone()
    } else {
        optional(sc, "exported")?.clone()
    };
    let sc_kind = optional(sc, "kind")?;
    let occ = optional(sc, "occupancy")?;
    let (kind, occupancy, native, path, source) = if is(&eph.occupancy, "first-party") {
        let both = is(occ, "first-party");
        (
            kind,
            string("first-party"),
            if both {
                optional(sc, "evaluationNativeId")?.clone()
            } else {
                eph.native
            },
            if both && is(sc_kind, "package") {
                optional(sc, "packageManifestPath")?.clone()
            } else {
                eph.package_path
            },
            if both {
                "sidecar+ephemeral"
            } else {
                "ephemeral"
            },
        )
    } else if is(occ, "first-party") || is(occ, "external") {
        (
            sc_kind.clone(),
            occ.clone(),
            optional(
                sc,
                if is(occ, "first-party") {
                    "evaluationNativeId"
                } else {
                    "targetNativeId"
                },
            )?
            .clone(),
            if is(sc_kind, "package") {
                optional(sc, "packageManifestPath")?.clone()
            } else {
                V::Null
            },
            "sidecar",
        )
    } else {
        (kind, string("unknown"), V::Null, V::Null, "sidecar-unknown")
    };
    Ok(record([
        ("kind", kind),
        ("occupancy", occupancy),
        ("exported", exported),
        ("nativeId", native),
        ("payloadNativeId", optional(sc, "targetNativeId")?.clone()),
        ("packageManifestPath", path),
        ("source", string(source)),
    ]))
}

fn source_value<'a>(fact: &'a V, spec: &V) -> Result<Option<&'a V>, Error> {
    let source = optional(spec, "sourceField")?;
    if is(source, "anchors[0].path") {
        return rows(fact, "anchors")?
            .first()
            .map(|v| obj(v).map(|m| m.get("path")))
            .transpose()
            .map(Option::flatten);
    }
    let payload = map_or_empty(fact, "payload")?;
    Ok(payload.and_then(|m| text(source).ok().and_then(|s| m.get(s))))
}
fn native_occupancy(fact: &V, subject: &V, spec: &V, atom: &V, inputs: &V) -> Result<Match, Error> {
    let universe = field(subject, "universe")?;
    let kind = field(subject, "kind")?;
    let native = field(subject, "nativeSubjectId")?;
    if is(defaulted(atom, "endpoint", &string("source"))?, "source") {
        if optional(fact, "sourceUniverse")? != universe
            || source_value(fact, spec)? != Some(native)
        {
            return Ok(Match::No);
        }
        if (is(kind, "package") || is(optional(spec, "sourceSubjectKind")?, "package"))
            && optional(field(fact, "payload")?, "manifestPath")?
                != optional(subject, "packageManifestPath")?
        {
            return Ok(Match::No);
        }
        return Ok(Match::Yes);
    }
    let target = optional(spec, "targetNativeIdField")?;
    if target == &V::Null || is(target, "") {
        return Ok(Match::No);
    }
    let target = optional(field(fact, "payload")?, text(target)?)?;
    if target == &V::Null || optional(fact, "targetUniverse")? != universe {
        return Ok(Match::No);
    }
    let attr = reconcile_attribution(fact, spec, inputs)?;
    let attr_kind = field(&attr, "kind")?;
    if ["file", "symbol", "package"]
        .iter()
        .any(|s| is(attr_kind, s))
        && attr_kind != kind
    {
        return Ok(Match::No);
    }
    if is(field(&attr, "occupancy")?, "external") {
        return Ok(Match::No);
    }
    if is(field(&attr, "occupancy")?, "first-party") && field(&attr, "nativeId")? != &V::Null {
        if field(&attr, "nativeId")? != native {
            return Ok(Match::No);
        }
        if is(kind, "package") {
            let path = field(&attr, "packageManifestPath")?;
            if path == &V::Null {
                return Ok(Match::Unknown);
            }
            if path != optional(subject, "packageManifestPath")? {
                return Ok(Match::No);
            }
        }
        return Ok(Match::Yes);
    }
    if is(kind, "symbol") && target != native {
        Ok(Match::No)
    } else {
        Ok(Match::Unknown)
    }
}
fn source_kind(fact: &V, spec: &V, inputs: &V) -> Result<Option<String>, Error> {
    let Some(source) = source_value(fact, spec)? else {
        return Ok(None);
    };
    let kind = optional(spec, "sourceSubjectKind")?;
    let rows = lookup_rows(
        source,
        field(fact, "sourceUniverse")?,
        if kind == &V::Null { None } else { Some(kind) },
        None,
        rows(inputs, "inventories")?,
        input_plan(inputs)?,
    )?;
    let kinds = rows
        .into_iter()
        .map(|v| text(field(v, "kind")?).map(ToString::to_string))
        .collect::<Result<alloc::collections::BTreeSet<_>, Error>>()?;
    if kinds.len() == 1 {
        Ok(kinds.into_iter().next())
    } else if kinds.is_empty() {
        Ok(if kind == &V::Null {
            None
        } else {
            Some(text(kind)?.into())
        })
    } else {
        Ok(None)
    }
}
fn apply_native_filters(
    fact: &V,
    spec: &V,
    atom: &V,
    inputs: &V,
    glob_budget: usize,
) -> Result<Match, Error> {
    let mut acc = Match::Yes;
    for filter in rows(atom, "filters")? {
        let key = text(field(filter, "field")?)?;
        let cmp = text(field(filter, "cmp")?)?;
        let value = field(filter, "value")?;
        let got = match key {
            "resolution" => cmp_string(cmp, text(field(fact, "resolution")?)?, value, glob_budget)?,
            "universe" => {
                let key = if is(defaulted(atom, "endpoint", &string("source"))?, "source") {
                    "sourceUniverse"
                } else {
                    "targetUniverse"
                };
                let coord = text(field(fact, key)?)?;
                let domain = map_or_empty(inputs, "universeDomains")?.and_then(|m| m.get(coord));
                match domain {
                    None | Some(V::Null) => Match::Unknown,
                    Some(v) => cmp_string(cmp, text(v)?, value, glob_budget)?,
                }
            }
            "confidenceMillionths" => cmp_int(
                cmp,
                defaulted(fact, "confidenceMillionths", &integer(1_000_000)?)?,
                value,
            )?,
            "subjectKind" => match source_kind(fact, spec, inputs)? {
                None => Match::Unknown,
                Some(kind) => cmp_string(cmp, &kind, value, glob_budget)?,
            },
            "targetKind" => {
                let attr = reconcile_attribution(fact, spec, inputs)?;
                let kind = field(&attr, "kind")?;
                if is(kind, "unknown") {
                    Match::Unknown
                } else {
                    cmp_string(cmp, text(kind)?, value, glob_budget)?
                }
            }
            "subject" => match source_value(fact, spec)? {
                None => Match::Unknown,
                Some(v) => cmp_string(cmp, text(v)?, value, glob_budget)?,
            },
            "target" => {
                let target_key =
                    if rows(spec, "endpointTargetRungs")?.contains(field(atom, "minResolution")?) {
                        optional(spec, "targetNativeIdField")?
                    } else {
                        optional(spec, "targetField")?
                    };
                let key = if target_key == &V::Null {
                    "targetModule"
                } else {
                    text(target_key)?
                };
                let raw = optional(field(fact, "payload")?, key)?;
                if raw == &V::Null {
                    Match::Unknown
                } else {
                    cmp_string(cmp, text(raw)?, value, glob_budget)?
                }
            }
            _ => return Err(Error::Refused("ATOM_FILTER_FIELD_FORBIDDEN")),
        };
        acc = and(acc, got);
        if acc == Match::No {
            return Ok(acc);
        }
    }
    Ok(acc)
}
impl NativeScanner<'_, '_> {
    fn eval_native(
        &mut self,
        atom: &V,
        subject: &V,
        spec: &V,
        glob_budget: usize,
    ) -> Result<V, Error> {
        let relation = text(field(atom, "relation")?)?;
        let need = rung_index(self.registry, relation, field(atom, "minResolution")?)?;
        let mut known = alloc::vec::Vec::new();
        let mut uncertain = alloc::vec::Vec::new();
        if let Some(facts) = map_or_empty(self.inputs, "facts")? {
            for (id, fact) in facts {
                tick(&mut self.work)?;
                if !is(optional(fact, "relation")?, relation) {
                    continue;
                }
                let have = rung_index(self.registry, relation, optional(fact, "resolution")?)?;
                if !matches!((have,need),(Some(h),Some(n))if h>=n) {
                    continue;
                }
                let occ = native_occupancy(fact, subject, spec, atom, self.inputs)?;
                if occ == Match::No {
                    continue;
                }
                let filter = apply_native_filters(fact, spec, atom, self.inputs, glob_budget)?;
                match and(occ, filter) {
                    Match::Yes => known.push(string(id)),
                    Match::Unknown => uncertain.push(string(id)),
                    Match::No => {}
                }
            }
        }
        let mut complete = self.native_completeness(atom, subject, spec)?;
        let op = text(field(atom, "op")?)?;
        if op == "all-covered" && !rows(atom, "filters")?.is_empty() && !uncertain.is_empty() {
            complete.unknown = true;
            complete.add_cause("target-metadata-unknown", None)?
        }
        let unknown = !uncertain.is_empty() || complete.unknown || !complete.complete;
        let value = match op {
            "exists" => {
                if !known.is_empty() {
                    "true"
                } else if unknown {
                    "indeterminate"
                } else {
                    "false"
                }
            }
            "none" => {
                if !known.is_empty() {
                    "false"
                } else if unknown {
                    "indeterminate"
                } else {
                    "true"
                }
            }
            "count-at-most" => {
                if known.len() as i128 > number(field(atom, "n")?)? {
                    "false"
                } else if unknown {
                    "indeterminate"
                } else {
                    "true"
                }
            }
            _ => {
                if !unknown {
                    "true"
                } else {
                    "indeterminate"
                }
            }
        };
        let coverage_ids = complete
            .coverages
            .into_iter()
            .map(V::String)
            .collect::<alloc::vec::Vec<_>>();
        let mut result = obj(&imported_result(
            value,
            alloc::vec![],
            alloc::vec![],
            complete.causes,
            coverage_ids.clone(),
        )?)?
        .clone();
        result.insert("kind".into(), string("native-atom"));
        result.insert("knownFactIds".into(), sorted_strings(known)?);
        result.insert("uncertainFactIds".into(), sorted_strings(uncertain)?);
        result.insert("coverageIds".into(), sorted_strings(coverage_ids)?);
        result.insert(
            "scopeIds".into(),
            sorted_strings(complete.scopes.into_iter().map(V::String).collect())?,
        );
        result.insert(
            "nativeDeficiencies".into(),
            sorted_strings(complete.deficiencies)?,
        );
        Ok(V::Object(result))
    }
}

fn inventory_digest(inv: &V) -> Result<String, Error> {
    let mut value = BTreeMap::new();
    for key in [
        "schemaVersion",
        "planId",
        "parameterDigest",
        "cellOrdinal",
        "programOrdinal",
        "kind",
        "state",
        "deficiency",
        "nativeCause",
        "examinedPaths",
        "rows",
    ] {
        if let Some(v) = obj(inv)?.get(key) {
            value.insert(key.into(), v.clone());
        }
    }
    let raw = opensip_identity::canonical_bytes(&V::Object(value)).map_err(|_| Error::Law)?;
    Ok(opensip_identity::digest_hex(&opensip_identity::raw_sha256(
        &raw,
    )))
}
fn string_set(v: &[V]) -> Result<alloc::collections::BTreeSet<String>, Error> {
    v.iter().map(|v| text(v).map(ToString::to_string)).collect()
}
impl NativeScanner<'_, '_> {
    fn admit_incoming(&mut self) -> Result<(), Error> {
        let mut seen = alloc::collections::BTreeSet::new();
        for att in rows(self.inputs, "incomingSearchAttestations")? {
            tick(&mut self.work)?;
            self.retained
                .check_current_value_shape(
                    att,
                    "foundation/incoming-search.schema.v1.json",
                    "#",
                    self.descriptor_work,
                )
                .map_err(|_| Error::Refused("INCOMING_SEARCH_SCHEMA"))?;
            let mut key = alloc::vec::Vec::new();
            for k in [
                "planId",
                "providerClosure",
                "sourceUniverse",
                "targetUniverse",
                "relation",
                "minResolution",
            ] {
                key.push(field(att, k)?.clone())
            }
            if !seen
                .insert(opensip_identity::canonical_bytes(&V::Array(key)).map_err(|_| Error::Law)?)
            {
                return Err(Error::Refused("INCOMING_SEARCH_DUPLICATE"));
            }
            let plan_id = optional(self.inputs, "planId")?;
            if plan_id != &V::Null && !is(plan_id, "") && field(att, "planId")? != plan_id {
                return Err(Error::Refused("INCOMING_SEARCH_JOIN"));
            }
            let relation = text(field(att, "relation")?)?;
            let rung = text(field(att, "minResolution")?)?;
            let pc = text(field(att, "providerClosure")?)?;
            let source = text(field(att, "sourceUniverse")?)?;
            let target = text(field(att, "targetUniverse")?)?;
            if rung_index(self.registry, relation, &string(rung))?.is_none() {
                return Err(Error::Refused("INCOMING_SEARCH_JOIN"));
            }
            for (key, selector) in [
                ("resolutionCompleteness", "#/$defs/ResolutionCompletenessV2"),
                ("closedWorld", "#/$defs/ClosedWorldV2"),
            ] {
                self.retained
                    .check_current_value_shape(
                        field(att, key)?,
                        "native/native-evidence.schemas.v2.json",
                        selector,
                        self.descriptor_work,
                    )
                    .map_err(|_| Error::Refused("INCOMING_SEARCH_SCHEMA"))?;
            }
            let rc = field(att, "resolutionCompleteness")?;
            let resolved = arr(field(field(self.registry, "scanner")?, "resolvedRungs")?)?
                .contains(&string(rung));
            if (!resolved
                && (!is(field(rc, "state")?, "not-applicable")
                    || number(field(rc, "unresolvedEdgeCount")?)? != 0
                    || optional(rc, "attempted")? == &V::Bool(true)
                    || !rows(rc, "unresolvedEdgeClasses")?.is_empty()))
                || (resolved && is(field(rc, "state")?, "not-applicable"))
                || (is(optional(att, "coverage")?, "complete")
                    && optional(rc, "examinedExhaustive")? != &V::Bool(true))
            {
                return Err(Error::Refused("INCOMING_SEARCH_JOIN"));
            }
            let provider = map_or_empty(self.inputs, "closures")?.and_then(|m| m.get(pc));
            if !provider.is_some_and(|v| optional(v, "kind").is_ok_and(|v| is(v, "provider"))) {
                return Err(Error::Refused("INCOMING_SEARCH_UNSELECTED_PROVIDER"));
            }
            let (available, _) = owed_source_bindings(relation, self.inputs, self.registry)?;
            let candidates = available
                .into_iter()
                .filter(|v| optional(v, "universe").is_ok_and(|v| is(v, source)))
                .collect::<alloc::vec::Vec<_>>();
            if candidates.is_empty() {
                return Err(Error::Refused("INCOMING_SEARCH_JOIN"));
            }
            let mut selected = false;
            if let Some(plan) = input_plan(self.inputs)? {
                for cell in rows(plan, "cells")? {
                    for b in rows(cell, "programBindings")? {
                        selected |= is(optional(b, "universe")?, target)
                    }
                }
            }
            let domain = map_or_empty(self.inputs, "universeDomains")?.and_then(|m| m.get(target));
            if (!selected && domain.is_none())
                || domain.is_some_and(|d| {
                    !arr(field(self.registry, "portableUniverseDomains").expect("registry domains"))
                        .is_ok_and(|v| v.contains(d))
                })
            {
                return Err(Error::Refused("INCOMING_SEARCH_JOIN"));
            }
            let mut enumerators = alloc::collections::BTreeSet::new();
            for b in &candidates {
                let en = optional(b, "_enumerator")?;
                if en != &V::Null && !is(en, "") {
                    enumerators.insert(text(en)?.to_string());
                }
            }
            if !enumerators.is_empty() && !enumerators.contains(pc) {
                return Err(Error::Refused("INCOMING_SEARCH_UNSELECTED_PROVIDER"));
            }
            let scopes = scopes_exact(self.inputs, relation, rung, source)?;
            let mut tagged = false;
            for (_, sc) in &scopes {
                let en = optional(sc, "enumeratorClosure")?;
                tagged |= en != &V::Null && !is(en, "")
            }
            let mut owed = alloc::collections::BTreeSet::new();
            for (sid, sc) in &scopes {
                if !tagged || is(optional(sc, "enumeratorClosure")?, pc) {
                    owed.insert(sid.clone());
                }
            }
            if string_set(rows(att, "scopeRefs")?)? != owed {
                return Err(Error::Refused("INCOMING_SEARCH_SCOPE_MISJOIN"));
            }
            let all_scopes = map_or_empty(self.inputs, "scopes")?;
            for sid in rows(att, "scopeRefs")? {
                let Some(sc) = all_scopes.and_then(|m| text(sid).ok().and_then(|s| m.get(s)))
                else {
                    return Err(Error::Refused("INCOMING_SEARCH_SCOPE_MISJOIN"));
                };
                if !is(optional(sc, "sourceUniverse")?, source)
                    || !is(optional(sc, "relation")?, relation)
                    || !is(optional(sc, "resolution")?, rung)
                {
                    return Err(Error::Refused("INCOMING_SEARCH_SCOPE_MISJOIN"));
                }
                let en = optional(sc, "enumeratorClosure")?;
                if en != &V::Null && !is(en, pc) {
                    return Err(Error::Refused("INCOMING_SEARCH_UNSELECTED_PROVIDER"));
                }
            }
            let spec = field(field(self.registry, "relations")?, relation)?;
            let kind = defaulted(spec, "sourceSubjectKind", &string("symbol"))?.clone();
            let mut locators = alloc::vec::Vec::new();
            let plan = input_plan(self.inputs)?;
            for inv in rows(self.inputs, "inventories")? {
                if optional(inv, "kind")? != &kind || !is(inventory_universe(inv, plan)?, source) {
                    continue;
                }
                let b = match plan {
                    Some(plan) => binding(
                        plan,
                        ordinal(field(inv, "cellOrdinal")?)?,
                        ordinal(field(inv, "programOrdinal")?)?,
                    )?,
                    None => None,
                };
                let en = b
                    .map(|b| map_or_empty(b, "enumerator"))
                    .transpose()?
                    .flatten()
                    .and_then(|m| m.get("closureId"));
                locators.push((en, inv));
            }
            let restricted = !enumerators.is_empty()
                && locators
                    .iter()
                    .any(|(en, _)| en.is_some_and(|v| v != &V::Null));
            let mut expected = alloc::collections::BTreeSet::new();
            for (en, inv) in locators {
                if !restricted || en.is_some_and(|v| is(v, pc)) {
                    expected.insert(inventory_digest(inv)?);
                }
            }
            if string_set(rows(att, "expectedInventoryRefs")?)? != expected {
                return Err(Error::Refused("INCOMING_SEARCH_INVENTORY_MISJOIN"));
            }
            let covs = coverages_exact(self.inputs, relation, rung, source, Some(target))?;
            let mut own = alloc::vec::Vec::new();
            let mut seen_covs = alloc::collections::BTreeSet::new();
            for sid in rows(att, "scopeRefs")? {
                let sid = text(sid)?;
                if let Some(sc) = all_scopes.and_then(|m| m.get(sid)) {
                    for (cid, cov) in self.pair_scope_coverages(sid, sc, &covs)? {
                        if seen_covs.insert(cid) {
                            own.push(cov)
                        }
                    }
                }
            }
            if optional(att, "completeSearch")? == &V::Bool(true) {
                for cov in own {
                    let entry = field(&cov, "entry")?;
                    let rc =
                        map_or_empty(entry, "resolutionCompleteness")?.and_then(|m| m.get("state"));
                    if !is(optional(entry, "coverage")?, "complete")
                        || rc.is_some_and(|v| {
                            ["partial", "incomplete", "not-attempted"]
                                .iter()
                                .any(|s| is(v, s))
                        })
                    {
                        return Err(Error::Refused("INCOMING_SEARCH_CANNOT_OVERRIDE_PARTIAL"));
                    }
                }
            }
        }
        Ok(())
    }
    fn admit_targets(&mut self) -> Result<(), Error> {
        let Some(items) = map_or_empty(self.inputs, "targetAttributions")? else {
            return Ok(());
        };
        let mut seen = alloc::collections::BTreeSet::new();
        let mut occupancy = BTreeMap::new();
        for (key, sc) in items {
            tick(&mut self.work)?;
            if matches!(sc, V::Array(_)) {
                return Err(Error::Refused("TARGET_ATTRIBUTION_DUPLICATE_FACT"));
            }
            if optional(sc, "schemaVersion")? != &integer(2)? {
                return Err(Error::Refused("TARGET_ATTRIBUTION_SCHEMA_VERSION"));
            }
            self.retained
                .check_current_value_shape(
                    sc,
                    "foundation/target-attribution.schema.v2.json",
                    "#",
                    self.descriptor_work,
                )
                .map_err(|_| Error::Refused("TARGET_ATTRIBUTION_SCHEMA"))?;
            let fid = text(field(sc, "sourceFactId")?)?;
            if !seen.insert(fid.to_string()) || key != fid {
                return Err(Error::Refused("TARGET_ATTRIBUTION_DUPLICATE_FACT"));
            }
            let plan = optional(self.inputs, "planId")?;
            if plan != &V::Null && !is(plan, "") && optional(sc, "planId")? != plan {
                return Err(Error::Refused("TARGET_ATTRIBUTION_FACT_NOT_IN_PLAN"));
            }
            let Some(fact) = map_or_empty(self.inputs, "facts")?.and_then(|m| m.get(fid)) else {
                return Err(Error::Refused("TARGET_ATTRIBUTION_FACT_NOT_IN_PLAN"));
            };
            let empty = record([]);
            let spec = obj(field(self.registry, "relations")?)?
                .get(text(field(fact, "relation")?)?)
                .unwrap_or(&empty);
            join_sidecar(fact, spec, sc, self.inputs)?;
        }
        // The selected owner checks all per-record joins before cross-record occupancy conflicts.
        for sc in items.values() {
            if !is(optional(sc, "occupancy")?, "first-party") {
                continue;
            }
            let key = V::Array(
                ["producerClosure", "targetUniverse", "targetNativeId"]
                    .iter()
                    .map(|k| optional(sc, k).cloned())
                    .collect::<Result<alloc::vec::Vec<_>, _>>()?,
            );
            let key = opensip_identity::canonical_bytes(&key).map_err(|_| Error::Law)?;
            let path = optional(sc, "packageManifestPath")?;
            let value = V::Array(alloc::vec![
                optional(sc, "kind")?.clone(),
                optional(sc, "evaluationNativeId")?.clone(),
                if path == &V::Null {
                    string("")
                } else {
                    path.clone()
                }
            ]);
            if let Some(old) = occupancy.insert(key, value.clone())
                && old != value
            {
                return Err(Error::Refused(
                    "TARGET_ATTRIBUTION_PROVIDER_OCCUPANCY_CONFLICT",
                ));
            }
        }
        Ok(())
    }
    fn admit_imports(&mut self) -> Result<(), Error> {
        for iid in rows(self.inputs, "planSelectedImportIds")? {
            tick(&mut self.work)?;
            let iid = text(iid)?;
            let Some(wrapper) = map_or_empty(self.inputs, "imports")?.and_then(|m| m.get(iid))
            else {
                return Err(Error::Refused("ATOM_IMPORT_WRAPPER_MISSING"));
            };
            flags(wrapper, iid, self.inputs)?;
            let scope = import_scope(wrapper, self.inputs)?;
            // Reconstructed scopes already have identity-owner admission; keep the atom's exact four-field schema too.
            let sc = obj(scope).map_err(|_| Error::Refused("ATOM_IMPORT_SCOPE_UNSTATED"))?;
            if sc.len() != 4
                || sc.get("schemaVersion") != Some(&integer(2)?)
                || ["workspaceRoots", "pathPrefixes", "excludedPathPrefixes"]
                    .iter()
                    .any(|k| {
                        !sc.get(*k).is_some_and(|v| {
                            arr(v).is_ok_and(|a| a.iter().all(|v| matches!(v, V::String(_))))
                        })
                    })
            {
                return Err(Error::Refused("ATOM_IMPORT_SCOPE_UNSTATED"));
            }
            let payload = map_or_empty(self.inputs, "importPayloads")?.and_then(|m| m.get(iid));
            let obs = map_or_empty(self.inputs, "importObservations")?.and_then(|m| m.get(iid));
            let Some(V::Object(obs)) = obs else { continue };
            let mut joins = BTreeMap::new();
            if let Some(V::Object(payload)) = payload {
                match text(optional(wrapper, "kind")?).unwrap_or("") {
                    "runtime" => {
                        for (a, b) in [
                            ("window", "observationWindow"),
                            ("population", "observedPopulation"),
                        ] {
                            if let Some(v) = payload.get(b) {
                                joins.insert(a, v.clone());
                            }
                        }
                    }
                    "test" => {
                        if let Some(v) = payload.get("selection") {
                            joins.insert("selection", v.clone());
                        }
                    }
                    "history" => {
                        if let Some(V::Object(range)) = payload.get("revisionRange")
                            && let (Some(from), Some(to)) = (range.get("from"), range.get("to"))
                        {
                            joins.insert(
                                "revisionRange",
                                record([("from", from.clone()), ("to", to.clone())]),
                            );
                        }
                    }
                    _ => {}
                }
            }
            for k in ["window", "population", "selection", "revisionRange"] {
                if let Some(v) = obs.get(k)
                    && v != &V::Null
                    && joins.get(k) != Some(v)
                {
                    return Err(Error::Refused("ATOM_IMPORT_OBSERVATION_PAYLOAD_JOIN"));
                }
            }
        }
        Ok(())
    }
    fn admit_inputs(&mut self) -> Result<(), Error> {
        let input = obj(self.inputs).map_err(|_| Error::Refused("ATOM_INPUTS_NOT_RECORD"))?;
        let allowed = [
            "facts",
            "scopes",
            "coverages",
            "enumerationPlan",
            "inventories",
            "targetAttributions",
            "closures",
            "universeDomains",
            "imports",
            "importPayloads",
            "importObservations",
            "importScopes",
            "importScopeAdapter",
            "planSelectedImportIds",
            "evaluationInputRefs",
            "incomingSearchAttestations",
            "planId",
            "blobs",
            "coverageScopes",
            "importFlagsAdapter",
        ];
        if input.keys().any(|k| !allowed.contains(&k.as_str())) {
            return Err(Error::Refused("ATOM_INPUT_KEY_UNKNOWN"));
        }
        for (k, error) in [
            ("importFlagsAdapter", "ATOM_IMPORT_FLAG_ADAPTER"),
            ("coverageScopes", "ATOM_COVERAGE_SCOPES"),
        ] {
            if input
                .get(k)
                .is_some_and(|v| v != &V::Null && !matches!(v, V::Object(_)))
            {
                return Err(Error::Refused(error));
            }
        }
        self.admit_incoming()?;
        self.admit_targets()?;
        self.admit_imports()
    }
}

fn admit_subject(subject: &V) -> Result<(), Error> {
    let s = obj(subject).map_err(|_| Error::Refused("ATOM_SUBJECT_SHAPE"))?;
    for k in ["universe", "kind", "nativeSubjectId"] {
        if !s.contains_key(k) {
            return Err(Error::Refused("ATOM_SUBJECT_SHAPE"));
        }
    }
    if !["file", "symbol", "package"]
        .iter()
        .any(|k| is(&s["kind"], k))
    {
        return Err(Error::Refused("ATOM_SUBJECT_KIND"));
    }
    if !text(&s["universe"]).is_ok_and(|u| {
        u.len() == 64
            && u.bytes()
                .all(|c| c.is_ascii_digit() || (b'a'..=b'f').contains(&c))
    }) {
        return Err(Error::Refused("ATOM_SUBJECT_UNIVERSE"));
    }
    if is(&s["kind"], "package") {
        if !s
            .get("packageManifestPath")
            .is_some_and(|v| text(v).is_ok_and(|v| !v.is_empty()))
        {
            return Err(Error::Refused("ATOM_SUBJECT_SHAPE"));
        }
    } else if s.contains_key("packageManifestPath") {
        return Err(Error::Refused("ATOM_SUBJECT_SHAPE"));
    }
    Ok(())
}
impl NativeScanner<'_, '_> {
    fn admit_atom(&mut self, atom: &V, subject: &V) -> Result<V, Error> {
        obj(atom).map_err(|_| Error::Refused("ATOM_SHAPE"))?;
        let relation = optional(atom, "relation")?;
        let spec = text(relation)
            .ok()
            .and_then(|s| obj(field(self.registry, "relations").ok()?).ok()?.get(s))
            .ok_or(Error::Refused("ATOM_RELATION_UNREGISTERED"))?;
        let op = optional(atom, "op")?;
        if !["exists", "none", "count-at-most", "all-covered"]
            .iter()
            .any(|s| is(op, s))
        {
            return Err(Error::Refused("ATOM_OP"));
        }
        if is(op, "count-at-most") && !number(optional(atom, "n")?).is_ok_and(|n| n >= 0) {
            return Err(Error::Refused("ATOM_COUNT_N"));
        }
        let source = string("source");
        let endpoint = defaulted(atom, "endpoint", &source)?;
        if !is(endpoint, "source") && !is(endpoint, "target") {
            return Err(Error::Refused("ATOM_ENDPOINT"));
        }
        let rung = optional(atom, "minResolution")?;
        if !arr(field(spec, "ladder")?)?.contains(rung) {
            return Err(Error::Refused("ATOM_MIN_RESOLUTION"));
        }
        let rungs = rows(spec, "endpointTargetRungs")?;
        if is(endpoint, "target")
            && (is(optional(spec, "endpointTarget")?, "forbidden")
                || (!rungs.is_empty() && !rungs.contains(rung)))
        {
            return Err(Error::Refused("ATOM_ENDPOINT_UNAVAILABLE"));
        }
        let evidence = optional(atom, "evidence")?;
        if if is(field(spec, "plane")?, "native") {
            evidence != &V::Null
        } else {
            evidence != optional(spec, "evidenceKind")?
        } {
            return Err(Error::Refused("ATOM_EVIDENCE_KIND_MISMATCH"));
        }
        let mut kinds = if is(endpoint, "target") {
            rows(spec, "targetKinds")?.to_vec()
        } else if !rows(spec, "sourceSubjectKinds")?.is_empty() {
            rows(spec, "sourceSubjectKinds")?.to_vec()
        } else {
            match optional(spec, "sourceSubjectKind")? {
                V::Null => alloc::vec![],
                v => alloc::vec![v.clone()],
            }
        };
        kinds.retain(|v| v != &V::Null && !is(v, ""));
        let rule_kind = optional(atom, "subjectKind")?;
        if is(rule_kind, "export") {
            if !kinds.contains(&string("symbol")) {
                return Err(Error::Refused("ATOM_KIND_INCOMPATIBLE"));
            }
            kinds = alloc::vec![string("symbol")];
        } else if ["file", "symbol", "package"]
            .iter()
            .any(|s| is(rule_kind, s))
        {
            if !kinds.contains(rule_kind) {
                return Err(Error::Refused("ATOM_KIND_INCOMPATIBLE"));
            }
            kinds = alloc::vec![rule_kind.clone()];
        }
        if !kinds.contains(field(subject, "kind")?) {
            return Err(Error::Refused("ATOM_KIND_INCOMPATIBLE"));
        }
        let filters = rows(atom, "filters").map_err(|_| Error::Refused("ATOM_FILTERS"))?;
        if filters.len() > 16 {
            return Err(Error::Refused("ATOM_FILTERS"));
        }
        for filter in filters {
            tick(&mut self.work)?;
            obj(filter).map_err(|_| Error::Refused("ATOM_FILTER_SHAPE"))?;
            self.retained
                .check_current_value_shape(
                    filter,
                    "workflows/schemas/policy-document.v2.schema.json",
                    "#/$defs/FieldFilter",
                    self.descriptor_work,
                )
                .map_err(|_| Error::Refused("ATOM_FILTER_SCHEMA"))?;
            let name = text(field(filter, "field")?)?;
            let cmp = text(field(filter, "cmp")?)?;
            let value = field(filter, "value")?;
            let projection = field(field(spec, "filters")?, name)?;
            let projection = if let V::Object(p) = projection {
                p.get(text(rung)?).unwrap_or(projection)
            } else {
                projection
            };
            if is(projection, "forbidden") {
                return Err(Error::Refused("ATOM_FILTER_FIELD_FORBIDDEN"));
            }
            let table = field(field(self.registry, "comparatorTable")?, name)?;
            if optional(table, cmp)? == &V::Null || optional(table, cmp)? == &V::Bool(false) {
                return Err(Error::Refused("ATOM_FILTER_COMPARATOR_ILLEGAL"));
            }
            let enumeration = match name {
                "resolution" => field(spec, "ladder")?,
                "universe" => field(self.registry, "portableUniverseDomains")?,
                "testResult" => map_or_empty(table, "enumByRelation")?
                    .and_then(|v| v.get(text(relation).unwrap_or("")))
                    .unwrap_or(&V::Null),
                _ => optional(table, "enum")?,
            };
            if enumeration != &V::Null {
                let allowed = arr(enumeration)?;
                if ((cmp == "eq" || cmp == "neq") && !allowed.contains(value))
                    || (cmp == "in" && arr(value)?.iter().any(|v| !allowed.contains(v)))
                {
                    return Err(Error::Refused("ATOM_FILTER_ENUM_LITERAL_UNKNOWN"));
                }
            }
            if (cmp == "prefix" || cmp == "glob")
                && !text(value).is_ok_and(|v| !v.is_empty() && !v.contains(['\\', '\0']))
            {
                return Err(Error::Refused("ATOM_GLOB_PATTERN"));
            }
        }
        Ok(spec.clone())
    }
    fn evaluate_atom(&mut self, atom: &V, subject: &V, glob_budget: usize) -> Result<V, Error> {
        self.admit_inputs()?;
        admit_subject(subject)?;
        let spec = self.admit_atom(atom, subject)?;
        if is(field(&spec, "plane")?, "native") {
            self.eval_native(atom, subject, &spec, glob_budget)
        } else {
            eval_imported(atom, subject, self.inputs, &spec, self.work, glob_budget)
        }
    }
}

fn canonical_set(values: alloc::vec::Vec<V>) -> Result<V, Error> {
    let mut ordered = BTreeMap::new();
    for value in values {
        ordered.insert(
            opensip_identity::canonical_bytes(&value).map_err(|_| Error::Law)?,
            value,
        );
    }
    Ok(V::Array(ordered.into_values().collect()))
}
// I1-L §4a: a whole-rule graph, never the per-subject atom API.
type CycleVertex = (String, String); // universe, path
struct CycleGraph {
    vertices: alloc::vec::Vec<CycleVertex>,
    edges: BTreeMap<(usize, usize), alloc::vec::Vec<String>>,
    uncertain: alloc::vec::Vec<(Option<usize>, String)>,
    unresolved: BTreeMap<usize, alloc::vec::Vec<String>>,
    causes: alloc::vec::Vec<V>,
}
impl CycleGraph {
    fn build(selected: &[V], inputs: &V, registry: &V, work: &mut usize) -> Result<Self, Error> {
        use alloc::collections::BTreeSet;
        let mut vertices: BTreeSet<CycleVertex> = BTreeSet::new();
        for subject in selected {
            tick(work)?;
            if !is(field(subject, "kind")?, "file") {
                return Err(Error::Refused("ATOM_KIND_INCOMPATIBLE"));
            }
            vertices.insert((
                text(field(subject, "universe")?)?.into(),
                text(field(field(subject, "row")?, "path")?)?.into(),
            ));
        }
        let vertices: alloc::vec::Vec<_> = vertices.into_iter().collect();
        let by_vertex: BTreeMap<_, _> = vertices
            .iter()
            .cloned()
            .enumerate()
            .map(|(i, v)| (v, i))
            .collect();
        let universes: BTreeSet<_> = vertices.iter().map(|v| v.0.clone()).collect();
        // P3: equal (id,path) observations count once, regardless of the rest of a row.
        let mut index: BTreeMap<(String, String), BTreeSet<String>> = BTreeMap::new();
        for inventory in rows(inputs, "inventories")? {
            tick(work)?;
            if !is(optional(inventory, "kind")?, "symbol") {
                continue;
            }
            let universe = text(inventory_universe(inventory, input_plan(inputs)?)?)?;
            for row in rows(inventory, "rows")? {
                tick(work)?;
                index
                    .entry((
                        universe.into(),
                        text(field(row, "nativeSubjectId")?)?.into(),
                    ))
                    .or_default()
                    .insert(text(field(row, "path")?)?.into());
            }
        }
        let place = |universe: &str, native: &str| -> Option<CycleVertex> {
            let paths = index.get(&(universe.into(), native.into()))?;
            if paths.len() != 1 {
                return None;
            }
            Some((universe.into(), paths.first()?.clone()))
        };
        let spec = field(field(registry, "relations")?, "imports")?;
        let need =
            rung_index(registry, "imports", &string("resolved-target"))?.ok_or(Error::Law)?;
        let mut graph = Self {
            vertices,
            edges: BTreeMap::new(),
            uncertain: alloc::vec![],
            unresolved: BTreeMap::new(),
            causes: alloc::vec![],
        };
        for (fid, fact) in map_or_empty(inputs, "facts")?
            .into_iter()
            .flat_map(|m| m.iter())
        {
            tick(work)?;
            let source_u = text(field(fact, "sourceUniverse")?)?;
            if !universes.contains(source_u) {
                continue;
            }
            let payload = field(fact, "payload")?;
            if is(field(fact, "relation")?, "unresolved-edge")
                && is(optional(payload, "relation")?, "imports")
            {
                let source = place(source_u, text(field(payload, "referrer")?)?);
                if let Some(i) = source.as_ref().and_then(|v| by_vertex.get(v)) {
                    graph.unresolved.entry(*i).or_default().push(fid.clone());
                }
                continue;
            }
            if !is(field(fact, "relation")?, "imports") {
                continue;
            }
            let have =
                rung_index(registry, "imports", field(fact, "resolution")?)?.ok_or(Error::Law)?;
            if have < need {
                continue;
            }
            let source = place(source_u, text(field(payload, "importer")?)?);
            if source.as_ref().is_some_and(|v| !by_vertex.contains_key(v)) {
                continue;
            }
            let attr = reconcile_attribution(fact, spec, inputs)?;
            if is(field(&attr, "occupancy")?, "external") {
                continue;
            }
            let source_i = source.as_ref().and_then(|v| by_vertex.get(v)).copied();
            let mut causes = alloc::vec![];
            if source_i.is_none() {
                causes.push(cause(
                    "population-unknown",
                    None,
                    None,
                    &[("universe", string(source_u))],
                )?);
            }
            let target_u = text(field(fact, "targetUniverse")?)?;
            let target = if !is(field(&attr, "occupancy")?, "first-party") {
                causes.push(cause(
                    "target-kind-unknown",
                    None,
                    None,
                    &[("universe", string(target_u))],
                )?);
                None
            } else {
                match text(field(&attr, "kind")?)? {
                    "file" => Some((target_u.into(), text(field(&attr, "nativeId")?)?.into())),
                    "symbol" => {
                        let target = place(target_u, text(field(&attr, "nativeId")?)?);
                        if target.is_none() {
                            causes.push(cause(
                                "target-kind-unknown",
                                None,
                                None,
                                &[("universe", string(target_u))],
                            )?);
                        }
                        target
                    }
                    "package" => {
                        causes.push(cause(
                            "population-unknown",
                            None,
                            None,
                            &[("universe", string(target_u))],
                        )?);
                        None
                    }
                    _ => return Err(Error::Law),
                }
            };
            let target_i = target.as_ref().and_then(|v| by_vertex.get(v)).copied();
            if target.is_some() && target_i.is_none() {
                causes.push(cause(
                    "population-unknown",
                    None,
                    None,
                    &[("universe", string(target_u))],
                )?);
            }
            if causes.is_empty() {
                graph
                    .edges
                    .entry((source_i.ok_or(Error::Law)?, target_i.ok_or(Error::Law)?))
                    .or_default()
                    .push(fid.clone());
            } else {
                graph.causes.extend(causes);
                graph.uncertain.push((source_i, fid.clone()));
            }
        }
        Ok(graph)
    }
    // Iterative Kosaraju: a long import chain cannot exhaust the Rust stack.
    fn components(
        &self,
        work: &mut usize,
    ) -> Result<alloc::vec::Vec<Option<(usize, usize)>>, Error> {
        let n = self.vertices.len();
        let mut successors = alloc::vec![alloc::vec::Vec::new(); n];
        let mut predecessors = alloc::vec![alloc::vec::Vec::new(); n];
        for &(a, b) in self.edges.keys() {
            tick(work)?;
            successors[a].push(b);
            predecessors[b].push(a);
        }
        let mut seen = alloc::vec![false; n];
        let mut finish = alloc::vec![];
        for root in 0..n {
            if seen[root] {
                continue;
            }
            seen[root] = true;
            let mut stack = alloc::vec![(root, 0)];
            while let Some((v, next)) = stack.last_mut() {
                tick(work)?;
                if let Some(&w) = successors[*v].get(*next) {
                    *next += 1;
                    if !seen[w] {
                        seen[w] = true;
                        stack.push((w, 0));
                    }
                } else {
                    finish.push(*v);
                    stack.pop();
                }
            }
        }
        let mut assigned = alloc::vec![false; n];
        let mut out = alloc::vec![None; n];
        for root in finish.into_iter().rev() {
            if assigned[root] {
                continue;
            }
            assigned[root] = true;
            let mut members = alloc::vec![];
            let mut stack = alloc::vec![root];
            while let Some(v) = stack.pop() {
                tick(work)?;
                members.push(v);
                for &w in &predecessors[v] {
                    if !assigned[w] {
                        assigned[w] = true;
                        stack.push(w);
                    }
                }
            }
            if members.len() == 1 && !self.edges.contains_key(&(root, root)) {
                continue;
            }
            let rep = *members
                .iter()
                .min_by(|&&a, &&b| {
                    self.vertices[a]
                        .1
                        .cmp(&self.vertices[b].1)
                        .then_with(|| self.vertices[a].0.cmp(&self.vertices[b].0))
                })
                .ok_or(Error::Law)?;
            for v in members {
                out[v] = Some((root, rep));
            }
        }
        Ok(out)
    }
    fn results(
        self,
        mut complete: NativeCompleteness,
        work: &mut usize,
    ) -> Result<BTreeMap<CycleVertex, V>, Error> {
        let components = self.components(work)?;
        complete.causes.extend(self.causes);
        let causes = unique_causes(complete.causes)?;
        let blocking = arr(&causes)?.iter().any(|c| {
            !is(
                optional(c, "code").unwrap_or(&V::Null),
                "cross-family-edge-not-owed",
            )
        });
        let mut matching = alloc::vec![alloc::vec::Vec::new(); self.vertices.len()];
        // An internal known fact is in at most the representative and its source witness.
        for ((a, b), facts) in &self.edges {
            tick(work)?;
            if let (Some((c, rep)), Some((d, _))) = (components[*a], components[*b])
                && c == d
            {
                matching[rep].extend(facts.iter().cloned().map(V::String));
                if *a != rep {
                    matching[*a].extend(facts.iter().cloned().map(V::String));
                }
            }
        }
        let mut uncertain = alloc::vec![alloc::vec::Vec::new(); self.vertices.len()];
        let mut unplaced = alloc::vec![];
        for (source, fid) in self.uncertain {
            if let Some(source) = source {
                uncertain[source].push(string(&fid));
            } else {
                unplaced.push(string(&fid));
            }
        }
        for (source, facts) in self.unresolved {
            uncertain[source].extend(facts.into_iter().map(V::String));
        }
        let coverage_ids = sorted_strings(complete.coverages.into_iter().map(V::String).collect())?;
        let scope_ids = sorted_strings(complete.scopes.into_iter().map(V::String).collect())?;
        let deficiencies = sorted_strings(complete.deficiencies)?;
        let mut out = BTreeMap::new();
        for (i, vertex) in self.vertices.into_iter().enumerate() {
            tick(work)?;
            let value = match components[i] {
                Some((_, rep)) if i == rep => "true",
                Some(_) => "false",
                None if complete.complete && !blocking => "false",
                None => "indeterminate",
            };
            if value == "indeterminate" && !blocking {
                return Err(Error::Law);
            }
            if value == "indeterminate" {
                uncertain[i].extend_from_slice(&unplaced);
            }
            let mut result = obj(&imported_result(
                value,
                alloc::vec![],
                alloc::vec![],
                arr(&causes)?.to_vec(),
                arr(&coverage_ids)?.to_vec(),
            )?)?
            .clone();
            result.insert("kind".into(), string("native-atom"));
            result.insert("coverageIds".into(), coverage_ids.clone());
            result.insert(
                "knownFactIds".into(),
                sorted_strings(core::mem::take(&mut matching[i]))?,
            );
            result.insert(
                "uncertainFactIds".into(),
                sorted_strings(core::mem::take(&mut uncertain[i]))?,
            );
            result.insert("scopeIds".into(), scope_ids.clone());
            result.insert("nativeDeficiencies".into(), deficiencies.clone());
            out.insert(vertex, V::Object(result));
        }
        Ok(out)
    }
}

impl NativeScanner<'_, '_> {
    fn cycle_completeness(
        &mut self,
        universes: &alloc::collections::BTreeSet<String>,
    ) -> Result<NativeCompleteness, Error> {
        use alloc::collections::BTreeSet;
        let mut out = NativeCompleteness::unknown();
        let (available, unavailable) = owed_source_bindings("imports", self.inputs, self.registry)?;
        if available.is_empty() && unavailable.is_empty() {
            out.add_cause("missing-relation-coverage", None)?;
            return Ok(out);
        }
        for b in &unavailable {
            if let V::String(family) = optional(b, "_family")?
                && family != "tsjs"
            {
                out.add_cause("cross-family-edge-not-owed", None)?;
            }
        }
        let mut bindings_by_universe: BTreeMap<&str, BTreeSet<(i128, i128)>> = BTreeMap::new();
        for b in &available {
            tick(&mut self.work)?;
            bindings_by_universe
                .entry(text(field(b, "universe")?)?)
                .or_default()
                .insert((
                    number(field(b, "_cellOrdinal")?)?,
                    number(field(b, "_programOrdinal")?)?,
                ));
        }
        let mut inventories_by_universe: BTreeMap<&str, alloc::vec::Vec<&V>> = BTreeMap::new();
        for inventory in rows(self.inputs, "inventories")? {
            tick(&mut self.work)?;
            if is(optional(inventory, "kind")?, "symbol") {
                inventories_by_universe
                    .entry(text(inventory_universe(
                        inventory,
                        input_plan(self.inputs)?,
                    )?)?)
                    .or_default()
                    .push(inventory);
            }
        }
        let mut paired = alloc::vec![];
        for universe in universes {
            tick(&mut self.work)?;
            let Some(bound) = bindings_by_universe.get(universe.as_str()) else {
                out.add_cause("selector-unbound", None)?;
                continue;
            };
            let mut expected = BTreeSet::new();
            let mut saw = false;
            let mut unknown = false;
            for inventory in inventories_by_universe
                .get(universe.as_str())
                .into_iter()
                .flat_map(|v| v.iter())
            {
                tick(&mut self.work)?;
                if !bound.contains(&(
                    number(field(inventory, "cellOrdinal")?)?,
                    number(field(inventory, "programOrdinal")?)?,
                )) {
                    continue;
                }
                saw = true;
                unknown |= !is(field(inventory, "state")?, "complete");
                for row in rows(inventory, "rows")? {
                    tick(&mut self.work)?;
                    expected.insert(text(field(row, "nativeSubjectId")?)?.to_string());
                }
            }
            if unknown || !saw {
                out.add_cause("population-unknown", Some(universe))?;
            }
            let scopes = scopes_exact(self.inputs, "imports", "resolved-target", universe)?;
            let covs = coverages_exact(self.inputs, "imports", "resolved-target", universe, None)?;
            let mut present = BTreeSet::new();
            for (sid, scope) in &scopes {
                tick(&mut self.work)?;
                out.scopes.push(sid.clone());
                for id in rows(scope, "subjects")? {
                    tick(&mut self.work)?;
                    present.insert(text(id)?.to_string());
                }
                let found = self.pair_scope_coverages(sid, scope, &covs)?;
                if found.is_empty() {
                    out.add_cause("scope-without-coverage", Some(universe))?;
                }
                paired.extend(found);
            }
            if scopes.is_empty() || !expected.is_subset(&present) {
                out.add_cause("uncovered-expected-source-subject", Some(universe))?;
            }
        }
        for (cid, cov) in unique_pairs(paired) {
            tick(&mut self.work)?;
            let universe = text(field(field(&cov, "key")?, "sourceUniverse")?)?;
            out.coverages.push(cid);
            let subject = record([
                ("universe", string(universe)),
                ("kind", string("symbol")),
                ("nativeSubjectId", string("")),
            ]);
            let req = NativeRequirement {
                relation: "imports",
                rung: "resolved-target",
                endpoint: "source",
                subject: &subject,
            };
            let view = record([("imports", entry_from_cov(&cov)?)]);
            self.run_sufficiency(&req, universe, &view, &[], &mut out)?;
        }
        out.unknown = out.causes.iter().any(|c| {
            !is(
                optional(c, "code").unwrap_or(&V::Null),
                "cross-family-edge-not-owed",
            )
        });
        out.complete = !out.unknown;
        Ok(out)
    }
}

// Only the sibling composition owner can construct this adapter. Public callers
// cannot supply atom results, scanner callbacks, flags, or normalized evidence.
pub(super) struct CompositionScanner<'a, 'b> {
    native: NativeScanner<'a, 'b>,
    normalized: &'a V,
    glob_budget: usize,
    cycles: BTreeMap<String, BTreeMap<CycleVertex, V>>,
}
impl<'a, 'b> CompositionScanner<'a, 'b> {
    pub(super) fn new(
        retained: &'a opensip_identity::RetainedInputs<'b>,
        normalized: &'a V,
        evidence: &'a V,
        registry: &'a V,
        limits: opensip_identity::TraversalBudget,
    ) -> Result<Self, Error> {
        let mut native = NativeScanner {
            inputs: evidence,
            registry,
            retained,
            work: limits.steps,
            descriptor_work: limits.descriptor_work,
        };
        // This is unconditional, including empty or disabled policies.
        native.admit_inputs()?;
        Ok(Self {
            native,
            normalized,
            glob_budget: limits.steps,
            cycles: BTreeMap::new(),
        })
    }
    pub(super) fn scan(
        &mut self,
        rule: &V,
        subject: &V,
        node: &V,
        predicate_id: &str,
    ) -> Result<V, Error> {
        let mut desc = obj(&record([
            ("universe", field(subject, "universe")?.clone()),
            ("kind", field(subject, "kind")?.clone()),
            (
                "nativeSubjectId",
                field(field(subject, "row")?, "nativeSubjectId")?.clone(),
            ),
        ]))?
        .clone();
        if is(field(subject, "kind")?, "package") {
            desc.insert(
                "packageManifestPath".into(),
                field(field(subject, "row")?, "path")?.clone(),
            );
        }
        let result = if is(field(node, "op")?, "cycle-representative") {
            if predicate_id != "p"
                || field(rule, "emitWhen")? != node
                || !is(field(node, "relation")?, "imports")
                || !is(field(node, "minResolution")?, "resolved-target")
                || !rows(node, "filters")?.is_empty()
                || ["endpoint", "evidence", "n"]
                    .iter()
                    .any(|k| obj(node).is_ok_and(|m| m.contains_key(*k)))
                || !is(
                    field(field(rule, "subjectEnumeration")?, "subjectKind")?,
                    "file",
                )
            {
                return Err(Error::Refused("ATOM_CYCLE_RULE_LAW"));
            }
            let rid = text(field(rule, "ruleId")?)?;
            if !self.cycles.contains_key(rid) {
                let enumeration = field(field(self.normalized, "enumerations")?, rid)?;
                let selected = rows(enumeration, "selectedSubjectIds")?
                    .iter()
                    .map(|id| field(field(self.normalized, "population")?, text(id)?).cloned())
                    .collect::<Result<alloc::vec::Vec<_>, Error>>()?;
                let graph = CycleGraph::build(
                    &selected,
                    self.native.inputs,
                    self.native.registry,
                    &mut self.native.work,
                )?;
                let universes = graph.vertices.iter().map(|v| v.0.clone()).collect();
                let completeness = self.native.cycle_completeness(&universes)?;
                self.cycles.insert(
                    rid.into(),
                    graph.results(completeness, &mut self.native.work)?,
                );
            }
            let key = (
                text(field(subject, "universe")?)?.into(),
                text(field(field(subject, "row")?, "path")?)?.into(),
            );
            self.cycles
                .get(rid)
                .and_then(|m| m.get(&key))
                .cloned()
                .ok_or(Error::Law)?
        } else {
            self.native
                .evaluate_atom(node, &V::Object(desc), self.glob_budget)?
        };
        let refs = canonical_set(arr(field(self.normalized, "evaluationInputRefs")?)?.to_vec())?;
        let plane = if is(field(&result, "kind")?, "imported-atom") {
            "import"
        } else {
            "native"
        };
        let evidence_kind = if plane == "import" {
            optional(node, "evidence")?.clone()
        } else {
            V::Null
        };
        let deficiency = |code: V, native: V, universe: V| -> Result<V, Error> {
            Ok(record([
                ("source", string(plane)),
                ("cause", code),
                ("subjectId", field(subject, "subjectId")?.clone()),
                ("predicateId", string(predicate_id)),
                ("inputRefs", refs.clone()),
                ("evidenceKind", evidence_kind.clone()),
                ("nativeCause", native),
                ("universe", universe),
            ]))
        };
        let mut defs = alloc::vec::Vec::new();
        let allowed = field(
            field(
                field(
                    field(self.native.registry, "scanner")?,
                    "evaluatorDeficiencyRegistry",
                )?,
                "sources",
            )?,
            plane,
        )?;
        for cause in arr(field(&result, "causes")?)? {
            if optional(cause, "evidenceKind")? != &evidence_kind {
                return Err(Error::Refused("EVALUATOR_ATOM_CAUSE_PLANE_JOIN"));
            }
            if !arr(allowed)?.contains(field(cause, "code")?) {
                return Err(Error::Refused("EVALUATOR_ATOM_CAUSE_UNREGISTERED"));
            }
            defs.push(deficiency(
                field(cause, "code")?.clone(),
                optional(cause, "nativeCause")?.clone(),
                optional(cause, "universe")?.clone(),
            )?);
        }
        for cause in arr(field(&result, "nativeDeficiencies")?)? {
            defs.push(deficiency(cause.clone(), V::Null, V::Null)?)
        }
        for cid in arr(field(&result, "coverageIds")?)? {
            let cov = field(field(self.native.inputs, "coverages")?, text(cid)?)?;
            let entry = field(cov, "entry")?;
            let code = field(entry, "deficiency")?;
            if code != &V::Null {
                let mut d = obj(&deficiency(
                    code.clone(),
                    field(entry, "nativeCause")?.clone(),
                    field(field(cov, "key")?, "sourceUniverse")?.clone(),
                )?)?
                .clone();
                let (_, digest) = text(cid)?.split_once(':').ok_or(Error::Law)?;
                d.insert(
                    "inputRefs".into(),
                    V::Array(alloc::vec![record([
                        ("domain", string("coverage")),
                        ("digest", string(digest))
                    ])]),
                );
                defs.push(V::Object(d));
            }
        }
        Ok(record([
            ("kind", field(&result, "kind")?.clone()),
            ("value", field(&result, "value")?.clone()),
            ("matchingFactIds", field(&result, "knownFactIds")?.clone()),
            (
                "uncertainFactIds",
                field(&result, "uncertainFactIds")?.clone(),
            ),
            (
                "matchingImportRows",
                field(&result, "knownObservationAddresses")?.clone(),
            ),
            (
                "uncertainImportRows",
                field(&result, "uncertainObservationAddresses")?.clone(),
            ),
            ("coverageIds", field(&result, "coverageIds")?.clone()),
            ("scopeIds", field(&result, "scopeIds")?.clone()),
            ("inputRefs", refs),
            ("deficiencies", canonical_set(defs)?),
        ]))
    }
}
pub(super) fn scanner_registry() -> Result<V, Error> {
    registry()
}

#[cfg(test)]
mod scope_tests {
    use super::*;
    #[test]
    fn import_scope_trailing_slashes_preserve_descendants_and_exclusions() {
        let scope = |roots: &[&str], prefixes: &[&str], excluded: &[&str]| {
            record([
                ("schemaVersion", integer(2).unwrap()),
                (
                    "workspaceRoots",
                    V::Array(roots.iter().map(|s| string(s)).collect()),
                ),
                (
                    "pathPrefixes",
                    V::Array(prefixes.iter().map(|s| string(s)).collect()),
                ),
                (
                    "excludedPathPrefixes",
                    V::Array(excluded.iter().map(|s| string(s)).collect()),
                ),
            ])
        };
        for root in ["src/", "src//"] {
            assert!(path_in_scope(&scope(&[root], &[], &[]), "src/child.ts").unwrap());
            assert!(path_in_scope(&scope(&["."], &[root], &[]), "src/child.ts").unwrap());
            assert!(!path_in_scope(&scope(&["."], &[], &[root]), "src/child.ts").unwrap());
            assert!(!path_in_scope(&scope(&[root], &[], &[]), "srcx/child.ts").unwrap());
        }
        assert!(!under_prefix("src", "src/"));
        assert!(under_prefix("src/", "src/"));
        assert!(under_prefix("/child", "/"));
    }
}

#[cfg(test)]
mod cycle_tests {
    extern crate std;
    use super::*;
    use alloc::{collections::BTreeSet, format, vec, vec::Vec};
    use opensip_identity::{RegisteredSchemas, RetainedInputs};

    fn schemas() -> RegisteredSchemas {
        let root = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("../..");
        let owned: alloc::vec::Vec<_> = RegisteredSchemas::source_requirements()
            .iter()
            .map(|p| std::fs::read(root.join(p.source_path())).expect("pinned repository schema"))
            .collect();
        RegisteredSchemas::from_sources(
            &owned
                .iter()
                .map(|v| v.as_slice())
                .collect::<alloc::vec::Vec<_>>(),
        )
        .expect("exact current schemas")
    }
    #[test]
    fn cycle_graph_and_census_match_all_accepted_oracle_cases() {
        let fixture = opensip_identity::parse_json(include_bytes!(
            "../tests/fixtures/cycle-representative.native-owner-r1.v1.json"
        ))
        .unwrap();
        let cases = rows(&fixture, "cases").unwrap();
        assert_eq!(cases.len(), 45);
        let schemas = schemas();
        let objects = BTreeMap::new();
        let blobs = BTreeMap::new();
        let retained = RetainedInputs::new(&schemas, &objects, &blobs);
        let registry = scanner_registry().unwrap();
        for case in cases {
            let label = text(field(case, "label").unwrap()).unwrap();
            let evidence = field(case, "evidence").unwrap();
            let mut scanner = NativeScanner {
                inputs: evidence,
                registry: &registry,
                retained: &retained,
                work: 20_000_000,
                descriptor_work: 20_000_000,
            };
            let graph = CycleGraph::build(
                rows(case, "selected").unwrap(),
                evidence,
                &registry,
                &mut scanner.work,
            )
            .unwrap_or_else(|e| panic!("{label}: graph {e:?}"));
            let universes = graph.vertices.iter().map(|v| v.0.clone()).collect();
            let completeness = scanner
                .cycle_completeness(&universes)
                .unwrap_or_else(|e| panic!("{label}: census {e:?}"));
            let results = graph
                .results(completeness, &mut scanner.work)
                .unwrap_or_else(|e| panic!("{label}: results {e:?}"));
            assert_eq!(
                results.len(),
                rows(case, "expected").unwrap().len(),
                "{label}"
            );
            for expected in rows(case, "expected").unwrap() {
                let key = (
                    text(field(expected, "universe").unwrap()).unwrap().into(),
                    text(field(expected, "path").unwrap()).unwrap().into(),
                );
                let result = &results[&key];
                for (actual, want) in [
                    ("value", "value"),
                    ("knownFactIds", "matchingFactIds"),
                    ("uncertainFactIds", "uncertainFactIds"),
                    ("scopeIds", "scopeIds"),
                    ("coverageIds", "coverageIds"),
                    ("nativeDeficiencies", "nativeDeficiencies"),
                ] {
                    assert_eq!(
                        canonical_set(
                            arr(field(result, actual).unwrap())
                                .map(|v| v.to_vec())
                                .unwrap_or_else(|_| alloc::vec![
                                    field(result, actual).unwrap().clone()
                                ])
                        )
                        .unwrap(),
                        canonical_set(
                            arr(field(expected, want).unwrap())
                                .map(|v| v.to_vec())
                                .unwrap_or_else(|_| alloc::vec![
                                    field(expected, want).unwrap().clone()
                                ])
                        )
                        .unwrap(),
                        "{label}: {key:?}: {actual}"
                    );
                }
                let project = |rows: &[V]| {
                    rows.iter()
                        .map(|c| {
                            record([
                                ("code", field(c, "code").unwrap().clone()),
                                ("nativeCause", optional(c, "nativeCause").unwrap().clone()),
                                ("universe", optional(c, "universe").unwrap().clone()),
                            ])
                        })
                        .collect()
                };
                assert_eq!(
                    canonical_set(project(rows(result, "causes").unwrap())).unwrap(),
                    canonical_set(project(rows(expected, "causes").unwrap())).unwrap(),
                    "{label}: {key:?}: causes"
                );
            }
        }
    }
    fn hex(raw: &str) -> alloc::vec::Vec<u8> {
        raw.as_bytes()
            .chunks_exact(2)
            .map(|v| u8::from_str_radix(core::str::from_utf8(v).unwrap(), 16).unwrap())
            .collect()
    }
    #[test]
    fn cycle_retained_evaluation_and_replay_match_known_and_partial_results() {
        use opensip_identity::{IdentityDomain, ObjectInput};
        let fixture = opensip_identity::parse_json(include_bytes!(
            "../tests/fixtures/cycle-representative.native-owner-r1.v1.json"
        ))
        .unwrap();
        let schemas = schemas();
        for case in rows(&fixture, "retainedCases").unwrap() {
            let label = text(field(case, "label").unwrap()).unwrap();
            let objects = rows(case, "objects")
                .unwrap()
                .iter()
                .map(|v| {
                    (
                        text(field(v, "id").unwrap()).unwrap().into(),
                        ObjectInput {
                            domain: IdentityDomain::parse(
                                text(field(v, "domain").unwrap()).unwrap(),
                            )
                            .unwrap(),
                            descriptor: field(v, "descriptor").unwrap().clone(),
                        },
                    )
                })
                .collect();
            let blobs = rows(case, "blobs")
                .unwrap()
                .iter()
                .map(|digest| {
                    let key = text(digest).unwrap();
                    (
                        hex(key).try_into().unwrap(),
                        hex(text(
                            field(field(&fixture, "retainedBlobPool").unwrap(), key).unwrap(),
                        )
                        .unwrap()),
                    )
                })
                .collect();
            let retained = RetainedInputs::new(&schemas, &objects, &blobs);
            let query = field(case, "query").unwrap();
            let budget = opensip_identity::TraversalBudget {
                steps: 20_000_000,
                depth: 96,
                descriptor_work: 20_000_000,
            };
            let candidate = crate::derive_evaluation(
                &retained,
                text(field(query, "planId").unwrap()).unwrap(),
                text(field(query, "executionId").unwrap()).unwrap(),
                text(field(query, "evaluatorClosure").unwrap()).unwrap(),
                rows(query, "inputRefs").unwrap(),
                crate::RetainedWalkLimits {
                    walk: budget,
                    owner: budget,
                    owner_invocations: 100_000,
                },
            )
            .unwrap_or_else(|e| panic!("{label}: {e:?}"));
            let expected = field(case, "expectedVerdict").unwrap();
            assert_eq!(
                field(candidate.proof(), "verdict").unwrap(),
                expected,
                "{label}"
            );
            let findings = rows(candidate.proof(), "findingIds").unwrap();
            assert_eq!(findings.len(), usize::from(is(expected, "fail")), "{label}");
            if is(expected, "fail") {
                let finding = &arr(candidate
                    .objects()
                    .get(text(&findings[0]).unwrap())
                    .unwrap())
                .unwrap()[1];
                assert_eq!(
                    field(field(finding, "subject").unwrap(), "logicalPath").unwrap(),
                    &string("a.ts")
                );
            }
            assert!(
                rows(candidate.proof(), "predicateProofs")
                    .unwrap()
                    .iter()
                    .all(|p| is(field(p, "operation").unwrap(), "cycle-representative"))
            );
            if label.ends_with("file-partial") {
                assert!(
                    rows(candidate.proof(), "predicateProofs")
                        .unwrap()
                        .iter()
                        .all(|p| is(field(p, "value").unwrap(), "false")),
                    "{label}"
                );
                assert!(
                    rows(candidate.proof(), "ruleResults")
                        .unwrap()
                        .iter()
                        .flat_map(|r| rows(r, "deficiencies").unwrap())
                        .any(|d| is(field(d, "cause").unwrap(), "incomplete-inventory")),
                    "{label}"
                );
            }
            if label.ends_with("symbol-partial-optional") {
                assert!(
                    rows(candidate.proof(), "predicateProofs")
                        .unwrap()
                        .iter()
                        .all(|p| is(field(p, "value").unwrap(), "indeterminate")),
                    "{label}"
                );
                assert!(
                    rows(candidate.proof(), "ruleResults")
                        .unwrap()
                        .iter()
                        .flat_map(|r| rows(r, "deficiencies").unwrap())
                        .any(|d| is(field(d, "cause").unwrap(), "population-unknown")),
                    "{label}"
                );
            }
            // Seal the independently derived output, then replay from retained
            // bytes and again from replay's owned evidence arena.
            let mut output_objects: BTreeMap<String, ObjectInput> = objects
                .iter()
                .map(|(k, v)| {
                    (
                        k.clone(),
                        ObjectInput {
                            domain: v.domain,
                            descriptor: v.descriptor.clone(),
                        },
                    )
                })
                .collect();
            let mut output_blobs = blobs.clone();
            for (key, pair) in candidate.objects() {
                let pair = arr(pair).unwrap();
                output_objects.insert(
                    key.clone(),
                    ObjectInput {
                        domain: IdentityDomain::parse(text(&pair[0]).unwrap()).unwrap(),
                        descriptor: pair[1].clone(),
                    },
                );
            }
            for (key, bytes) in candidate.blobs() {
                output_blobs.insert(hex(key).try_into().unwrap(), bytes.clone());
            }
            let plan_id = text(field(query, "planId").unwrap()).unwrap();
            let plan = &objects.get(plan_id).unwrap().descriptor;
            let snapshot = &objects
                .get(text(field(plan, "snapshotId").unwrap()).unwrap())
                .unwrap()
                .descriptor;
            let refs = rows(query, "inputRefs").unwrap();
            let views: BTreeSet<String> = refs
                .iter()
                .filter(|r| is(field(r, "domain").unwrap(), "view"))
                .map(|r| format!("view2:{}", text(field(r, "digest").unwrap()).unwrap()))
                .collect();
            let mut coverages: BTreeSet<String> = refs
                .iter()
                .filter(|r| is(field(r, "domain").unwrap(), "coverage"))
                .map(|r| format!("coverage2:{}", text(field(r, "digest").unwrap()).unwrap()))
                .collect();
            for view in &views {
                coverages.extend(
                    rows(&objects.get(view).unwrap().descriptor, "coverageIds")
                        .unwrap()
                        .iter()
                        .map(|c| text(c).unwrap().into()),
                );
            }
            let obj = |fields: Vec<(&str, V)>| {
                V::Object(fields.into_iter().map(|(k, v)| (k.into(), v)).collect())
            };
            let version = || V::Integer(opensip_identity::JsonInteger::new(3).unwrap());
            let mut add = |domain: IdentityDomain, descriptor: V| {
                let id = format!(
                    "{}:{}",
                    domain.prefix(),
                    opensip_identity::digest_hex(
                        &opensip_identity::hash_canonical_value(domain.name(), &descriptor)
                            .unwrap()
                    )
                );
                output_objects.insert(id.clone(), ObjectInput { domain, descriptor });
                id
            };
            let evidence = add(
                IdentityDomain::SemanticEvidence,
                obj(vec![
                    ("schemaVersion", version()),
                    ("planId", string(plan_id)),
                    (
                        "viewIds",
                        V::Array(views.into_iter().map(|v| string(&v)).collect()),
                    ),
                    (
                        "coverageIds",
                        V::Array(coverages.into_iter().map(|v| string(&v)).collect()),
                    ),
                    ("importIds", field(plan, "importIds").unwrap().clone()),
                    (
                        "findingIds",
                        field(candidate.proof(), "findingIds").unwrap().clone(),
                    ),
                    ("proofBundleId", string(candidate.proof_bundle_id())),
                ]),
            );
            let seal = add(
                IdentityDomain::EvaluationSeal,
                obj(vec![
                    ("schemaVersion", version()),
                    ("planId", string(plan_id)),
                    (
                        "executionPlanId",
                        field(query, "executionId").unwrap().clone(),
                    ),
                    ("evidenceId", string(&evidence)),
                    (
                        "evaluatorClosure",
                        field(query, "evaluatorClosure").unwrap().clone(),
                    ),
                    ("policyDigest", field(plan, "policyDigest").unwrap().clone()),
                    ("proofBundleId", string(candidate.proof_bundle_id())),
                    (
                        "verdict",
                        field(candidate.proof(), "verdict").unwrap().clone(),
                    ),
                ]),
            );
            let run = add(
                IdentityDomain::Run,
                obj(vec![
                    ("schemaVersion", version()),
                    ("projectId", field(snapshot, "projectId").unwrap().clone()),
                    ("snapshotId", field(plan, "snapshotId").unwrap().clone()),
                    ("planId", string(plan_id)),
                    ("evidenceId", string(&evidence)),
                    ("evaluationSealId", string(&seal)),
                    (
                        "capabilityManifestId",
                        field(plan, "capabilityManifestId").unwrap().clone(),
                    ),
                ]),
            );
            let limits = crate::ReplayLimits {
                retained: crate::RetainedWalkLimits {
                    walk: budget,
                    owner: budget,
                    owner_invocations: 100_000,
                },
                capture_entries: 100_000,
                retained_bytes: 32 * 1024 * 1024,
            };
            let inputs = RetainedInputs::new(&schemas, &output_objects, &output_blobs);
            let replayed = crate::replay_run(&inputs, &run, limits)
                .unwrap_or_else(|e| panic!("replay {label}: {e:?}"));
            assert_eq!(replayed.proof(), candidate.proof());
            let owned = replayed.retained_evidence();
            let owned_inputs = RetainedInputs::new(&schemas, owned.objects(), owned.blobs());
            let again = crate::replay_run(&owned_inputs, &run, limits).unwrap();
            assert_eq!(
                again.retained_evidence().object_frames(),
                owned.object_frames()
            );
            assert_eq!(again.retained_evidence().blobs(), owned.blobs());
        }
    }
}
