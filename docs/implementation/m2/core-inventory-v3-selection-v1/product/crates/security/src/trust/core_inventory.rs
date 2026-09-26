// Exact229 core inventory projection only. Does not admit signatures, native
// tree bytes, installation TCB, original authority or an executable closure.
use crate::trust::trust_record_shapes::{self as shapes, Definition};
use opensip_identity::{JsonInteger, JsonValue as V, digest_hex, hash_canonical_value, raw_sha256};
use std::collections::{BTreeMap, BTreeSet};
#[derive(Debug, PartialEq, Eq)]
pub(super) enum Error {
    Shape(shapes::Error),
    Binding(&'static str),
    Identity,
}
pub(super) struct Projection {
    raw: Vec<u8>,
    inventory: V,
    descriptor: V,
    closure: String,
    files: BTreeMap<String, BTreeMap<String, V>>,
}
impl Projection {
    pub(super) fn raw(&self) -> &[u8] {
        &self.raw
    }
    pub(super) fn inventory(&self) -> &V {
        &self.inventory
    }
    pub(super) fn descriptor(&self) -> &V {
        &self.descriptor
    }
    pub(super) fn closure(&self) -> &str {
        &self.closure
    }
    pub(super) fn files(&self) -> &BTreeMap<String, BTreeMap<String, V>> {
        &self.files
    }
}
fn object(v: &V) -> &BTreeMap<String, V> {
    let V::Object(o) = v else {
        unreachable!("closed shape")
    };
    o
}
fn array(v: &V) -> &[V] {
    let V::Array(a) = v else {
        unreachable!("closed shape")
    };
    a
}
fn text(v: &V) -> &str {
    let V::String(s) = v else {
        unreachable!("closed shape")
    };
    s
}
fn number(v: &V) -> i128 {
    let V::Integer(n) = v else {
        unreachable!("closed shape")
    };
    n.get()
}
fn require(ok: bool, reason: &'static str) -> Result<(), Error> {
    if ok {
        Ok(())
    } else {
        Err(Error::Binding(reason))
    }
}
fn logical(path: &str) -> Result<String, Error> {
    let b = path.as_bytes();
    require(
        !path.is_empty() && path.chars().count() <= 4096,
        "logical-path",
    )?;
    require(crate::metadata_unicode15::is_nfc(path), "logical-nfc")?;
    require(
        !(path.contains(['\\', '\0'])
            || path.split('/').any(|p| ["", ".", ".."].contains(&p))
            || b.len() >= 2 && b[0].is_ascii_alphabetic() && b[1] == b':'),
        "logical-path",
    )?;
    Ok(crate::metadata_unicode15::normalize(
        &crate::metadata_casefold15::fold(path),
    ))
}
fn ordered<T: Ord>(items: &[T]) -> bool {
    items.windows(2).all(|w| w[0] < w[1])
}
fn tree(platform: &V) -> Result<BTreeMap<String, V>, Error> {
    let p = object(platform);
    let entries = array(&object(&p["tree"])["entries"]);
    let mut paths = Vec::new();
    let mut aliases = BTreeSet::new();
    let mut kinds = BTreeMap::new();
    let mut links = BTreeMap::new();
    let mut files = BTreeMap::new();
    for e in entries {
        let e = object(e);
        let path = text(&e["path"]);
        let alias = logical(path)?;
        paths.push(path);
        aliases.insert(alias);
        kinds.insert(path, text(&e["type"]));
    }
    require(ordered(&paths), "tree-order")?;
    require(aliases.len() == paths.len(), "tree-alias")?;
    require(
        !aliases.contains("inventory.json") && !aliases.contains("inventory.sig.json"),
        "inventory-self-reference",
    )?;
    for e in entries {
        let row = object(e);
        let path = text(&row["path"]);
        for (i, _) in path.match_indices('/') {
            require(kinds.get(&path[..i]) == Some(&"dir"), "tree-parent-type")?;
        }
        match text(&row["type"]) {
            "symlink" => {
                let target = text(&row["target"]);
                logical(target)?;
                links.insert(path, target);
            }
            "file" => {
                files.insert(path.to_owned(), e.clone());
            }
            _ => {}
        }
    }
    for (source, target) in &links {
        let parent = source.rsplit_once('/').map_or("", |x| x.0);
        let mut resolved = if parent.is_empty() {
            (*target).to_owned()
        } else {
            format!("{parent}/{target}")
        };
        let mut seen = BTreeSet::new();
        let mut complete = false;
        for _ in 0..=entries.len() {
            require(seen.insert(resolved.clone()), "symlink-cycle")?;
            require(resolved.chars().count() <= 4096, "symlink-resolution-bound")?;
            let mut replacement = None;
            for end in resolved
                .match_indices('/')
                .map(|(i, _)| i)
                .chain(std::iter::once(resolved.len()))
            {
                let prefix = &resolved[..end];
                if let Some(target) = links.get(prefix) {
                    let base = prefix.rsplit_once('/').map_or("", |x| x.0);
                    let suffix = &resolved[end..];
                    replacement = Some(if base.is_empty() {
                        format!("{target}{suffix}")
                    } else {
                        format!("{base}/{target}{suffix}")
                    });
                    break;
                }
            }
            if let Some(next) = replacement {
                resolved = next;
            } else {
                require(
                    kinds.contains_key(resolved.as_str()),
                    "symlink-target-missing",
                )?;
                complete = true;
                break;
            }
        }
        require(complete, "symlink-resolution-bound")?;
    }
    require(files.contains_key(text(&p["entrypoint"])), "entrypoint")?;
    let hashes: BTreeSet<_> = files.values().map(|v| text(&object(v)["sha256"])).collect();
    require(hashes.len() == files.len(), "duplicate-file-digest")?;
    let rows = array(&p["layers"]);
    let layer_paths: Vec<_> = rows.iter().map(|v| text(&object(v)["path"])).collect();
    require(
        layer_paths == files.keys().map(String::as_str).collect::<Vec<_>>(),
        "layer-coverage-order",
    )?;
    for row in rows {
        let row = object(row);
        let layers: Vec<_> = array(&row["layers"]).iter().map(text).collect();
        require(ordered(&layers), "layer-order")?;
        if layers.len() > 1 {
            require(
                layers == ["L-DIST", "L-HOST"] && row["path"] == p["entrypoint"],
                "layer-overlap",
            )?;
        }
    }
    let entry = rows
        .iter()
        .find(|v| object(v)["path"] == p["entrypoint"])
        .expect("complete layer coverage");
    require(
        array(&object(entry)["layers"])
            .iter()
            .map(text)
            .collect::<Vec<_>>()
            == ["L-DIST", "L-HOST"],
        "shared-executable-layers",
    )?;
    let edges: Vec<_> = array(&p["requires"])
        .iter()
        .map(|v| {
            let o = object(v);
            (text(&o["from"]), text(&o["to"]))
        })
        .collect();
    require(ordered(&edges), "requires-order")?;
    let mut adjacency: BTreeMap<&str, Vec<&str>> =
        files.keys().map(|s| (s.as_str(), Vec::new())).collect();
    for (from, to) in edges {
        require(
            files.contains_key(from) && files.contains_key(to),
            "requires-node",
        )?;
        adjacency.get_mut(from).expect("checked node").push(to);
    }
    let mut color: BTreeMap<&str, u8> = BTreeMap::new();
    for start in files.keys() {
        let mut stack = vec![(start.as_str(), false)];
        while let Some((name, finish)) = stack.pop() {
            if finish {
                color.insert(name, 2);
            } else if color.get(name) == Some(&1) {
                return Err(Error::Binding("requires-cycle"));
            } else if color.get(name) != Some(&2) {
                color.insert(name, 1);
                stack.push((name, true));
                stack.extend(adjacency[name].iter().rev().map(|&n| (n, false)));
            }
        }
    }
    Ok(files)
}
/// Existing callers read exactly `CoreInventoryV2`; this reader is unchanged.
pub(super) fn project(raw: &[u8], platform: &str) -> Result<Projection, Error> {
    bind(raw, platform, Definition::CoreInventoryV2)
}
/// XNU `cs_blobs.h` bits (macOS 27.0 SDK Kernel.framework, equal to the XNU
/// open-source header) for the closed `requiredCodeSigningFlags` name set.
pub(super) const CODE_SIGNING_FLAGS: [(&str, u32); 7] = [
    ("CS_VALID", 0x0000_0001),
    ("CS_HARD", 0x0000_0100),
    ("CS_KILL", 0x0000_0200),
    ("CS_RESTRICT", 0x0000_0800),
    ("CS_ENFORCEMENT", 0x0000_1000),
    ("CS_REQUIRE_LV", 0x0000_2000),
    ("CS_RUNTIME", 0x0001_0000),
];
/// The 463b release inventory, read only by a caller that opts into
/// `CoreInventoryV3`. `CoreInventoryV2` bytes refuse here, and V3 bytes refuse
/// through `project`: neither reader defaults a missing release member.
pub(super) struct ProjectionV3 {
    core: Projection,
    state_writer: u8,
    required_code_signing_flags: u32,
}
impl ProjectionV3 {
    /// The same inventory, descriptor, closure and file projection V2 makes.
    pub(super) fn core(&self) -> &Projection {
        &self.core
    }
    /// K of the selected platform row: 1 names the stage-1 writer, 2 the
    /// stage-2 writer. No other value is ever returned.
    pub(super) fn state_writer(&self) -> u8 {
        self.state_writer
    }
    /// The mask the running image's `CS_OPS_STATUS` must include, for the
    /// selected platform row. Always includes `CS_VALID`.
    pub(super) fn required_code_signing_flags(&self) -> u32 {
        self.required_code_signing_flags
    }
}
pub(super) fn project_v3(raw: &[u8], platform: &str) -> Result<ProjectionV3, Error> {
    let core = bind(raw, platform, Definition::CoreInventoryV3)?;
    let row = array(&object(core.inventory())["platforms"])
        .iter()
        .map(object)
        .find(|row| text(&row["platform"]) == platform)
        .expect("bound platform row");
    let state_writer = match number(&row["stateWriter"]) {
        1 => 1,
        2 => 2,
        _ => return Err(Error::Binding("state-writer")),
    };
    let mut required_code_signing_flags = 0;
    for name in array(&row["requiredCodeSigningFlags"]).iter().map(text) {
        let (_, bit) = CODE_SIGNING_FLAGS
            .iter()
            .find(|(known, _)| *known == name)
            .ok_or(Error::Binding("code-signing-flag"))?;
        required_code_signing_flags |= bit;
    }
    require(
        required_code_signing_flags & CODE_SIGNING_FLAGS[0].1 != 0,
        "code-signing-valid",
    )?;
    Ok(ProjectionV3 {
        core,
        state_writer,
        required_code_signing_flags,
    })
}
fn bind(raw: &[u8], platform: &str, definition: Definition) -> Result<Projection, Error> {
    let inventory = shapes::admit(definition, raw).map_err(Error::Shape)?;
    let inv = object(&inventory);
    require(
        crate::metadata_versions::Version::parse(text(&inv["semanticVersion"])).is_some(),
        "core-semver",
    )?;
    let majors: Vec<_> = array(&inv["servedProtocolMajors"])
        .iter()
        .map(number)
        .collect();
    require(
        ordered(&majors) && majors.contains(&number(&inv["protocolMajor"])),
        "protocol-membership-order",
    )?;
    let rows = array(&inv["platforms"]);
    let platforms: Vec<_> = rows.iter().map(|v| text(&object(v)["platform"])).collect();
    require(ordered(&platforms), "platform-order")?;
    require(platforms.contains(&platform), "platform-unavailable")?;
    let mut all_files = BTreeMap::new();
    for row in rows {
        all_files.insert(text(&object(row)["platform"]).to_owned(), tree(row)?);
    }
    let eb = object(&inv["embeddedBootstrap"]);
    let directory = text(&eb["directory"]);
    logical(directory)?;
    for (field, name) in [
        ("manifest", "payload.json"),
        ("envelope", "payload.sig.json"),
    ] {
        let r = object(&eb[field]);
        require(
            text(&r["path"]) == format!("{directory}/{name}"),
            "bootstrap-frame",
        )?;
    }
    for files in all_files.values() {
        for field in ["manifest", "envelope"] {
            let r = object(&eb[field]);
            let e = files
                .get(text(&r["path"]))
                .ok_or(Error::Binding("bootstrap-tree"))?;
            let e = object(e);
            require(
                e["sha256"] == r["sha256"] && e["length"] == r["bytes"],
                "bootstrap-tree",
            )?;
        }
    }
    let files = &all_files[platform];
    let tree = files
        .iter()
        .map(|(path, v)| {
            let e = object(v);
            V::Object(
                [
                    ("path".into(), V::String(path.clone())),
                    ("sha256".into(), e["sha256"].clone()),
                    ("bytes".into(), e["length"].clone()),
                ]
                .into(),
            )
        })
        .collect();
    let descriptor = V::Object(
        [
            (
                "schemaVersion".into(),
                V::Integer(JsonInteger::new(2).unwrap()),
            ),
            ("kind".into(), V::String("core".into())),
            (
                "manifestDigest".into(),
                V::String(digest_hex(&raw_sha256(raw))),
            ),
            ("tree".into(), V::Array(tree)),
            ("semanticVersion".into(), inv["semanticVersion"].clone()),
            ("protocolMajor".into(), inv["protocolMajor"].clone()),
            ("platform".into(), V::String(platform.into())),
        ]
        .into(),
    );
    let closure = format!(
        "closure2:{}",
        digest_hex(&hash_canonical_value("closure", &descriptor).map_err(|_| Error::Identity)?)
    );
    Ok(Projection {
        raw: raw.to_vec(),
        inventory,
        descriptor,
        closure,
        files: all_files,
    })
}
#[cfg(test)]
mod tests {
    use super::*;
    fn bytes(v: &V) -> Vec<u8> {
        text(v)
            .as_bytes()
            .chunks_exact(2)
            .map(|v| u8::from_str_radix(std::str::from_utf8(v).unwrap(), 16).unwrap())
            .collect()
    }
    #[test]
    fn core_inventory_projection_matches_original_distribution_owner() {
        let mut counts = (0, 0);
        let mut owned = Vec::new();
        for line in include_bytes!("../../tests/fixtures/core-inventory318.ndjson")
            .split(|b| *b == b'\n')
            .filter(|b| !b.is_empty())
        {
            let value = opensip_identity::parse_json(line).unwrap();
            let q = object(&value);
            let label = text(&q["label"]).to_owned();
            let expected = object(&q["expected"]);
            let raw = if let Some(v) = q.get("rawRepeat") {
                let r = object(v);
                vec![number(&r["byte"]) as u8; number(&r["count"]) as usize]
            } else {
                bytes(&q["raw"])
            };
            let result = project(&raw, text(&q["platform"]));
            assert_eq!(
                result.is_ok(),
                expected["ok"] == V::Bool(true),
                "{label}: {:?}",
                result.as_ref().err()
            );
            if let Ok(result) = result {
                owned.push((result, raw, expected.clone(), label));
                counts.1 += 1;
            } else if let Err(Error::Binding(reason)) = result {
                assert_eq!(reason, text(&expected["reason"]), "{label}");
            }
            counts.0 += 1;
        }
        for (projection, raw, expected, label) in owned {
            assert_eq!(projection.raw(), raw, "{label}");
            assert_eq!(projection.inventory(), &expected["inventory"], "{label}");
            assert_eq!(projection.descriptor(), &expected["descriptor"], "{label}");
            assert_eq!(projection.closure(), text(&expected["closure"]), "{label}");
            let files = V::Object(
                projection
                    .files()
                    .iter()
                    .map(|(k, v)| (k.clone(), V::Object(v.clone())))
                    .collect(),
            );
            assert_eq!(files, expected["files"], "{label}");
        }
        assert_eq!(counts, (125, 53));
    }
    use opensip_identity::{canonical_bytes, parse_json};
    fn int(n: i64) -> V {
        V::Integer(JsonInteger::new(n.into()).unwrap())
    }
    fn names(names: &[&str]) -> V {
        V::Array(names.iter().map(|s| V::String((*s).into())).collect())
    }
    /// The 318 baseline V2 inventory and its selected platform.
    fn baseline() -> (Vec<u8>, String) {
        let line = include_bytes!("../../tests/fixtures/core-inventory318.ndjson")
            .split(|b| *b == b'\n')
            .find(|b| !b.is_empty())
            .unwrap();
        let q = parse_json(line).unwrap();
        let q = object(&q);
        assert_eq!(text(&q["label"]), "baseline-macos");
        (bytes(&q["raw"]), text(&q["platform"]).to_owned())
    }
    /// Row i gets stateWriter 1 + i % 2, so the selected row is distinguishable.
    fn v3(raw: &[u8], edit: impl Fn(usize, &mut BTreeMap<String, V>)) -> Vec<u8> {
        let mut inv = parse_json(raw).unwrap();
        let V::Object(o) = &mut inv else { panic!() };
        o.insert("inventorySchema".into(), int(3));
        let Some(V::Array(rows)) = o.get_mut("platforms") else {
            panic!()
        };
        for (i, row) in rows.iter_mut().enumerate() {
            let V::Object(row) = row else { panic!() };
            row.insert("stateWriter".into(), int(1 + (i % 2) as i64));
            row.insert(
                "requiredCodeSigningFlags".into(),
                names(&["CS_HARD", "CS_KILL", "CS_RUNTIME", "CS_VALID"]),
            );
            edit(i, row);
        }
        canonical_bytes(&inv).unwrap()
    }
    #[test]
    fn v3_projects_both_release_members_of_the_selected_row() {
        let (raw2, platform) = baseline();
        let v2 = project(&raw2, &platform).unwrap();
        let raw3 = v3(&raw2, |_, _| {});
        let p = project_v3(&raw3, &platform).unwrap();
        let rows = array(&object(p.core().inventory())["platforms"]);
        let index = rows
            .iter()
            .position(|r| text(&object(r)["platform"]) == platform)
            .unwrap();
        assert_eq!(p.state_writer(), 1 + (index % 2) as u8);
        assert_eq!(p.required_code_signing_flags(), 0x0001_0301);
        // Same closure rules: only the manifest digest of the new body differs.
        let (V::Object(d2), V::Object(d3)) = (v2.descriptor(), p.core().descriptor()) else {
            panic!()
        };
        assert_eq!(d2.keys().collect::<Vec<_>>(), d3.keys().collect::<Vec<_>>());
        for (k, v) in d2 {
            if k == "manifestDigest" {
                assert_eq!(d3[k], V::String(digest_hex(&raw_sha256(&raw3))));
                assert_ne!(&d3[k], v);
            } else {
                assert_eq!(&d3[k], v, "{k}");
            }
        }
        let expected = format!(
            "closure2:{}",
            digest_hex(&hash_canonical_value("closure", p.core().descriptor()).unwrap())
        );
        assert_eq!(p.core().closure(), expected);
        assert_ne!(p.core().closure(), v2.closure());
        assert_eq!(p.core().files(), v2.files());
        // Each name maps to its own XNU bit, and every row value is read.
        for (name, bit) in CODE_SIGNING_FLAGS {
            let mut set = vec![name, "CS_VALID"];
            set.sort_unstable();
            set.dedup();
            let raw = v3(&raw2, |_, row| {
                row.insert("requiredCodeSigningFlags".into(), names(&set));
                row.insert("stateWriter".into(), int(2));
            });
            let p = project_v3(&raw, &platform).unwrap();
            assert_eq!(p.required_code_signing_flags(), bit | 1, "{name}");
            assert_eq!(p.state_writer(), 2);
        }
        let all = {
            let mut n: Vec<_> = CODE_SIGNING_FLAGS.iter().map(|x| x.0).collect();
            n.sort_unstable();
            n
        };
        let raw = v3(&raw2, |_, row| {
            row.insert("requiredCodeSigningFlags".into(), names(&all));
        });
        assert_eq!(
            project_v3(&raw, &platform).unwrap().required_code_signing_flags(),
            0x0001_3b01
        );
    }
    #[test]
    fn v2_and_v3_readers_do_not_cross() {
        let (raw2, platform) = baseline();
        let raw3 = v3(&raw2, |_, _| {});
        assert!(project(&raw2, &platform).is_ok());
        assert!(matches!(
            project(&raw3, &platform),
            Err(Error::Shape(shapes::Error::Shape))
        ));
        assert!(matches!(
            project_v3(&raw2, &platform),
            Err(Error::Shape(shapes::Error::Shape))
        ));
        // V3 keeps every V2 binding rule.
        let mut inv = parse_json(&raw3).unwrap();
        let V::Object(o) = &mut inv else { panic!() };
        o.insert("protocolMajor".into(), int(999));
        assert!(matches!(
            project_v3(&canonical_bytes(&inv).unwrap(), &platform),
            Err(Error::Binding("protocol-membership-order"))
        ));
        assert!(matches!(
            project_v3(&raw3, "macos-x86_64-none"),
            Err(Error::Binding("platform-unavailable"))
        ));
    }
    #[test]
    fn v3_release_member_shapes_refuse_missing_and_unknown_values() {
        let (raw2, platform) = baseline();
        let refuse = |edit: &dyn Fn(&mut BTreeMap<String, V>), label: &str| {
            let raw = v3(&raw2, |_, row| edit(row));
            assert!(
                shapes::admit(Definition::CoreInventoryV3, &raw).is_err(),
                "{label}"
            );
            assert!(
                matches!(
                    project_v3(&raw, &platform),
                    Err(Error::Shape(shapes::Error::Shape))
                ),
                "{label}"
            );
        };
        refuse(
            &|r| {
                r.remove("stateWriter");
            },
            "missing stateWriter",
        );
        for bad in [int(0), int(3), int(-1), V::String("2".into()), V::Null] {
            refuse(&|r| {
                r.insert("stateWriter".into(), bad.clone());
            }, "stateWriter value");
        }
        refuse(
            &|r| {
                r.remove("requiredCodeSigningFlags");
            },
            "missing flags",
        );
        // Seven names exist, so a 17-member list also breaks order or the enum.
        let long: Vec<String> = (0..17).map(|i| format!("CS_VALID{i:02}")).collect();
        let long: Vec<&str> = long.iter().map(String::as_str).collect();
        for (label, set) in [
            ("empty", names(&[])),
            ("unsorted", names(&["CS_VALID", "CS_HARD"])),
            ("duplicate", names(&["CS_HARD", "CS_HARD", "CS_VALID"])),
            ("unknown", names(&["CS_DEBUGGED", "CS_VALID"])),
            ("lower-case", names(&["CS_VALID", "cs_hard"])),
            ("no CS_VALID", names(&["CS_HARD", "CS_RUNTIME"])),
            ("more than 16", names(&long)),
            ("integer mask", int(1)),
            ("integer member", V::Array(vec![int(1)])),
        ] {
            refuse(
                &|r| {
                    r.insert("requiredCodeSigningFlags".into(), set.clone());
                },
                label,
            );
        }
        // One row without the members refuses the whole inventory.
        let raw = v3(&raw2, |i, row| {
            if i == 0 {
                row.remove("stateWriter");
            }
        });
        assert!(project_v3(&raw, &platform).is_err());
        // The row shape itself: the valid row admits; exactly one extra member refuses.
        let raw3 = v3(&raw2, |_, _| {});
        let inv = parse_json(&raw3).unwrap();
        let row = array(&object(&inv)["platforms"])[0].clone();
        let row_raw = canonical_bytes(&row).unwrap();
        assert!(shapes::admit(Definition::CorePlatformV3, &row_raw).is_ok());
        assert!(shapes::admit(Definition::CorePlatformV2, &row_raw).is_err());
        let V::Object(mut extra) = row else { panic!() };
        extra.insert("stateSchema".into(), int(2));
        let extra = canonical_bytes(&V::Object(extra)).unwrap();
        assert!(shapes::admit(Definition::CorePlatformV3, &extra).is_err());
        assert!(shapes::admit(Definition::CoreInventoryV3, &raw3).is_ok());
    }
}
