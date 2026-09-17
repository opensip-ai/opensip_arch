//! Private atom-scanner draft. Pure helpers do not establish input admission.
use alloc::{
    collections::BTreeMap,
    string::{String, ToString},
};
use opensip_identity::JsonValue as V;
#[derive(Debug, PartialEq, Eq)]
enum Error {
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
    root.is_empty() || path == root || path.strip_prefix(root).is_some_and(|v| v.starts_with('/'))
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
