//! Supplied prototype mixed-case public intake variant; the closed lowercase intake is unchanged.
//! Exact published names are kept in index rows and archive file names; only Cargo's index cache path is lowercased.
//! No authenticated source or production authority.
use super::*;
fn intake_mixed_case(
    root: &Path,
    index_receipt: &serde_json::Value,
    archive_receipt: &serde_json::Value,
) -> CargoResult<serde_json::Value> {
    anyhow::ensure!(
        root.is_absolute() && !root.join("registry").exists(),
        "fresh explicit output required"
    );
    let indexes: serde_json::Value = serde_json::from_slice(&checked(index_receipt)?)?;
    let archives: serde_json::Value = serde_json::from_slice(&checked(archive_receipt)?)?;
    anyhow::ensure!(
        archives["indexReceipt"] == *index_receipt,
        "archive receipt/index receipt association mismatch"
    );
    let mut folded = BTreeSet::new();
    let mut expected = BTreeMap::new();
    let mut output = BTreeMap::new();
    let mut records = 0;
    let mut mixed = 0;
    for input in indexes["inputs"]
        .as_array()
        .ok_or_else(|| anyhow::anyhow!("missing indexes"))?
    {
        let name = input["name"]
            .as_str()
            .ok_or_else(|| anyhow::anyhow!("missing name"))?;
        anyhow::ensure!(
            !name.is_empty()
                && name
                    .bytes()
                    .all(|b| b.is_ascii_alphanumeric() || b == b'-' || b == b'_')
                && folded.insert(name.to_ascii_lowercase()),
            "unsafe or case-folded duplicate supplied index name"
        );
        if name.bytes().any(|b| b.is_ascii_uppercase()) {
            mixed += 1;
        }
        let raw = checked(input)?;
        let mut versions = BTreeSet::new();
        let mut rows = Vec::new();
        for line in raw.split(|b| *b == b'\n').filter(|line| !line.is_empty()) {
            let json: serde_json::Value = serde_json::from_slice(line)?;
            anyhow::ensure!(json["name"] == name, "index name mismatch");
            let version = semver::Version::parse(
                json["vers"]
                    .as_str()
                    .ok_or_else(|| anyhow::anyhow!("missing version"))?,
            )?;
            anyhow::ensure!(
                versions.insert(version.clone()),
                "duplicate supplied index version"
            );
            let checksum = json["cksum"]
                .as_str()
                .ok_or_else(|| anyhow::anyhow!("missing checksum"))?;
            anyhow::ensure!(
                checksum.len() == 64
                    && checksum
                        .bytes()
                        .all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b)),
                "invalid supplied checksum"
            );
            anyhow::ensure!(
                expected
                    .insert(format!("{name}-{version}.crate"), checksum.to_string())
                    .is_none(),
                "duplicate archive slot"
            );
            rows.push((version, line.to_vec()));
            records += 1;
        }
        let borrowed = rows
            .iter()
            .map(|(v, b)| (v.clone(), b.as_slice()))
            .collect();
        let cache = crate::sources::registry::index::SpikeSummariesCache {
            versions: borrowed,
            index_version: "Unknown",
        };
        let encoded = cache.serialize("Unknown");
        let decoded = crate::sources::registry::index::SpikeSummariesCache::parse(&encoded)?;
        anyhow::ensure!(
            decoded.versions.len() == rows.len(),
            "cache roundtrip length mismatch"
        );
        for ((version, bytes), (wanted, original)) in decoded.versions.iter().zip(rows.iter()) {
            anyhow::ensure!(
                version == wanted && *bytes == original.as_slice(),
                "stock cache serialization changed version/record"
            );
        }
        // Same lowered relative path as stock `RegistryIndex` summary loading.
        let lowered = name.to_lowercase();
        anyhow::ensure!(
            output
                .insert(
                    format!(
                        "index/index.crates.io-1949cf8c6b5b557f/.cache/{}",
                        cargo_util::registry::make_dep_path(&lowered, false)
                    ),
                    encoded
                )
                .is_none(),
            "duplicate index output"
        );
    }
    let mut observed = BTreeSet::new();
    for input in archives["archives"]
        .as_array()
        .ok_or_else(|| anyhow::anyhow!("missing archives"))?
    {
        anyhow::ensure!(
            input["success"] == true,
            "failed acquisition not admitted as input"
        );
        let name = input["name"]
            .as_str()
            .ok_or_else(|| anyhow::anyhow!("missing archive name"))?;
        let version = semver::Version::parse(
            input["version"]
                .as_str()
                .ok_or_else(|| anyhow::anyhow!("missing archive version"))?,
        )?;
        let file = format!("{name}-{version}.crate");
        let checksum = expected
            .get(&file)
            .ok_or_else(|| anyhow::anyhow!("no exact supplied index record"))?;
        anyhow::ensure!(
            input["expectedSuppliedIndexChecksum"] == *checksum && observed.insert(file.clone()),
            "archive checksum association or duplicate mismatch"
        );
        let raw = archive_bytes(checked(input)?, checksum)?;
        output.insert(
            format!("cache/index.crates.io-1949cf8c6b5b557f/{file}"),
            raw,
        );
    }
    anyhow::ensure!(
        observed.len() == expected.len(),
        "incomplete acquired version set"
    );
    // Every whole input and record validated BEFORE the first registry output.
    let mut rows = Vec::new();
    for (relative, raw) in output {
        let path = root.join("registry").join(&relative);
        std::fs::create_dir_all(path.parent().unwrap())?;
        use std::io::Write;
        let mut file = std::fs::OpenOptions::new()
            .write(true)
            .create_new(true)
            .open(&path)?;
        file.write_all(&raw)?;
        rows.push(serde_json::json!({"path":relative,"bytes":raw.len(),"sha256":sha(&raw)}));
    }
    let report = serde_json::json!({"root":root,"files":rows,"indexes":folded.len(),"mixedCaseIndexes":mixed,"indexCachePathsLowercased":true,"versionRecords":records,"archives":observed.len(),"wholeSuppliedIndexChecksumsMatched":true,"stockCacheSerializationRoundtripped":true,"expandedSourcesMaterialized":false,"sourceAuthentication":false,"corpusResolutionRun":false,"nativeAdmission":false,"SMComplete":false});
    std::fs::write(
        root.join("intake.json"),
        serde_json::to_vec_pretty(&report)?,
    )?;
    Ok(report)
}
fn run_packet(row: &serde_json::Value) -> CargoResult<serde_json::Value> {
    let raw = checked(row)?;
    let packet: serde_json::Value = serde_json::from_slice(&raw)?;
    let root = Path::new(
        packet["outputRoot"]
            .as_str()
            .ok_or_else(|| anyhow::anyhow!("missing explicit output root"))?,
    );
    anyhow::ensure!(
        root.is_absolute() && root.is_dir() && !root.join("entry-outcome.json").exists(),
        "fresh existing owned experiment output root required"
    );
    let result = intake_mixed_case(root, &packet["indexReceipt"], &packet["archiveReceipt"]);
    let outcome = serde_json::json!({"success":result.is_ok(),"error":result.as_ref().err().map(|e|format!("{e:#}")),"intake":result.ok(),"packetPin":row,"mixedCaseVariant":true,"sourceAuthentication":false,"corpusResolutionRun":false,"nativeAdmission":false,"SMComplete":false});
    std::fs::write(root.join("entry-packet-observation.json"), raw)?;
    std::fs::write(
        root.join("entry-outcome.json"),
        serde_json::to_vec_pretty(&outcome)?,
    )?;
    Ok(outcome)
}
const LOWER_INDEX: &str = "/tmp/opensip-implementation/sm-experimental-dependency-preparation-2026-10-10/missing-public-index-inputs-r1/receipt.json";
const LOWER_ARCHIVE: &str = "/tmp/opensip-implementation/sm-experimental-dependency-preparation-2026-10-10/missing-public-archive-inputs-r1/receipt.json";
const MIXED_INDEX: &str =
    "/tmp/opensip-implementation/sm-public-intake-mixed-case-2026-10-11/inputs/index/receipt.json";
const MIXED_ARCHIVE: &str = "/tmp/opensip-implementation/sm-public-intake-mixed-case-2026-10-11/inputs/archives/receipt.json";
fn retained_root(prefix: &str) -> PathBuf {
    tempfile::Builder::new()
        .prefix(prefix)
        .tempdir()
        .unwrap()
        .keep()
}
fn tree(root: &Path) -> BTreeMap<String, Vec<u8>> {
    let mut files = BTreeMap::new();
    let mut pending = vec![root.join("registry")];
    while let Some(dir) = pending.pop() {
        for entry in std::fs::read_dir(&dir).unwrap() {
            let path = entry.unwrap().path();
            if path.is_dir() {
                pending.push(path);
            } else {
                let relative = path
                    .strip_prefix(root)
                    .unwrap()
                    .to_str()
                    .unwrap()
                    .to_string();
                files.insert(relative, std::fs::read(&path).unwrap());
            }
        }
    }
    files
}
// Rewrites the supplied index receipt inputs and re-associates a copy of the archive receipt to it.
fn variant(root: &Path, inputs: serde_json::Value) -> (serde_json::Value, serde_json::Value) {
    let mut index: serde_json::Value =
        serde_json::from_slice(&std::fs::read(MIXED_INDEX).unwrap()).unwrap();
    index["inputs"] = inputs;
    let index_path = root.join("variant-index-receipt.json");
    std::fs::write(&index_path, serde_json::to_vec_pretty(&index).unwrap()).unwrap();
    let index_pin = receipt(index_path.to_str().unwrap());
    let mut archive: serde_json::Value =
        serde_json::from_slice(&std::fs::read(MIXED_ARCHIVE).unwrap()).unwrap();
    archive["indexReceipt"] = index_pin.clone();
    let archive_path = root.join("variant-archive-receipt.json");
    std::fs::write(&archive_path, serde_json::to_vec_pretty(&archive).unwrap()).unwrap();
    (index_pin, receipt(archive_path.to_str().unwrap()))
}
#[test]
fn lowercase_inputs_produce_closed_intake_bytes() {
    let closed_root = retained_root("opensip-mixed-case-equivalence-closed-");
    let variant_root = retained_root("opensip-mixed-case-equivalence-variant-");
    let closed = intake(&closed_root, &receipt(LOWER_INDEX), &receipt(LOWER_ARCHIVE)).unwrap();
    let result = intake_mixed_case(
        &variant_root,
        &receipt(LOWER_INDEX),
        &receipt(LOWER_ARCHIVE),
    )
    .unwrap();
    assert_eq!(closed["files"], result["files"]);
    assert_eq!(result["mixedCaseIndexes"], 0);
    assert_eq!(tree(&closed_root), tree(&variant_root));
    assert_eq!(tree(&variant_root).len(), 140);
    eprintln!(
        "ACTUAL_MIXED_CASE_EQUIVALENCE_CONTROL={} {}",
        closed_root.display(),
        variant_root.display()
    );
}
#[test]
fn actual_mixed_case_public_inputs_keep_exact_names_and_lowered_cache_path() {
    let root = retained_root("opensip-mixed-case-actual-");
    let closed_root = retained_root("opensip-mixed-case-closed-refusal-");
    assert!(intake(&closed_root, &receipt(MIXED_INDEX), &receipt(MIXED_ARCHIVE)).is_err());
    assert!(!closed_root.join("registry").exists());
    let result = intake_mixed_case(&root, &receipt(MIXED_INDEX), &receipt(MIXED_ARCHIVE)).unwrap();
    assert_eq!(result["indexes"], 1);
    assert_eq!(result["mixedCaseIndexes"], 1);
    assert_eq!(result["versionRecords"], 27);
    assert_eq!(result["archives"], 27);
    let files = tree(&root);
    assert_eq!(files.len(), 28);
    let index = files
        .get("registry/index/index.crates.io-1949cf8c6b5b557f/.cache/in/fl/inflector")
        .unwrap();
    assert_eq!(
        cargo_util::registry::make_dep_path("inflector", false),
        "in/fl/inflector"
    );
    let decoded = crate::sources::registry::index::SpikeSummariesCache::parse(index).unwrap();
    assert_eq!(decoded.versions.len(), 27);
    for (_, line) in decoded.versions.iter() {
        let json: serde_json::Value = serde_json::from_slice(line).unwrap();
        assert_eq!(json["name"], "Inflector");
    }
    assert!(
        files
            .contains_key("registry/cache/index.crates.io-1949cf8c6b5b557f/Inflector-0.11.4.crate")
    );
    assert!(
        !files
            .keys()
            .any(|k| k.contains("/cache/") && k.contains("/inflector-"))
    );
    assert!(!root.join("registry/src").exists());
    eprintln!("ACTUAL_MIXED_CASE_PUBLIC_INTAKE_CONTROL={}", root.display());
}
#[test]
fn case_variant_names_refuse_before_any_output() {
    let original: serde_json::Value =
        serde_json::from_slice(&std::fs::read(MIXED_INDEX).unwrap()).unwrap();
    let row = original["inputs"][0].clone();
    let lowered_root = retained_root("opensip-mixed-case-lowered-name-");
    let mut lowered = row.clone();
    lowered["name"] = serde_json::Value::String("inflector".into());
    let (index, archive) = variant(&lowered_root, serde_json::json!([lowered]));
    let error = intake_mixed_case(&lowered_root, &index, &archive).unwrap_err();
    assert!(format!("{error:#}").contains("index name mismatch"));
    assert!(!lowered_root.join("registry").exists());
    let duplicate_root = retained_root("opensip-mixed-case-folded-duplicate-");
    let mut folded = row.clone();
    folded["name"] = serde_json::Value::String("INFLECTOR".into());
    let (index, archive) = variant(&duplicate_root, serde_json::json!([row, folded]));
    let error = intake_mixed_case(&duplicate_root, &index, &archive).unwrap_err();
    assert!(format!("{error:#}").contains("case-folded duplicate"));
    assert!(!duplicate_root.join("registry").exists());
    let unsafe_root = retained_root("opensip-mixed-case-unsafe-name-");
    let mut unsafe_name = original["inputs"][0].clone();
    unsafe_name["name"] = serde_json::Value::String("In.flector".into());
    let (index, archive) = variant(&unsafe_root, serde_json::json!([unsafe_name]));
    let error = intake_mixed_case(&unsafe_root, &index, &archive).unwrap_err();
    assert!(format!("{error:#}").contains("unsafe"));
    assert!(!unsafe_root.join("registry").exists());
    eprintln!(
        "ACTUAL_MIXED_CASE_REFUSAL_CONTROLS={} {} {}",
        lowered_root.display(),
        duplicate_root.display(),
        unsafe_root.display()
    );
}
#[test]
#[ignore]
fn collect_explicit_experimental_public_cache_intake_mixed_case() {
    let path = std::env::var_os("OPENSIP_EXPERIMENT_PUBLIC_INTAKE_PACKET")
        .expect("explicit owned packet path");
    let expected = std::env::var("OPENSIP_EXPERIMENT_PUBLIC_INTAKE_PACKET_SHA256")
        .expect("independent supplied packet SHA");
    let bytes = std::env::var("OPENSIP_EXPERIMENT_PUBLIC_INTAKE_PACKET_BYTES")
        .expect("independent supplied packet length")
        .parse::<u64>()
        .unwrap();
    let result = run_packet(
        &serde_json::json!({"path":PathBuf::from(path),"bytes":bytes,"sha256":expected}),
    )
    .unwrap();
    eprintln!(
        "ACTUAL_EXPERIMENT_PUBLIC_INTAKE_SUCCESS={}",
        result["success"]
    );
}
