//! Anonymous public experiment receipts are supplied data, not source admission.
use super::*;
use std::collections::{BTreeMap, BTreeSet};
fn sha(raw: &[u8]) -> String {
    let mut h = cargo_util::Sha256::new();
    h.update(raw);
    h.finish_hex()
}
fn checked(row: &serde_json::Value) -> CargoResult<Vec<u8>> {
    let path = Path::new(
        row["path"]
            .as_str()
            .ok_or_else(|| anyhow::anyhow!("missing supplied path"))?,
    );
    anyhow::ensure!(
        std::fs::symlink_metadata(path)?.file_type().is_file(),
        "not a regular supplied input"
    );
    let raw = std::fs::read(path)?;
    anyhow::ensure!(
        Some(raw.len() as u64) == row["bytes"].as_u64()
            && Some(sha(&raw).as_str()) == row["sha256"].as_str(),
        "supplied byte pin mismatch"
    );
    Ok(raw)
}
fn archive_bytes(raw: Vec<u8>, expected: &str) -> CargoResult<Vec<u8>> {
    anyhow::ensure!(
        sha(&raw) == expected,
        "supplied index checksum mismatch before archive intake"
    );
    Ok(raw)
}
fn intake(
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
    let mut names = BTreeSet::new();
    let mut expected = BTreeMap::new();
    let mut output = BTreeMap::new();
    let mut records = 0;
    for input in indexes["inputs"]
        .as_array()
        .ok_or_else(|| anyhow::anyhow!("missing indexes"))?
    {
        let name = input["name"]
            .as_str()
            .ok_or_else(|| anyhow::anyhow!("missing name"))?;
        anyhow::ensure!(
            !name.is_empty()
                && name.bytes().all(|b| b.is_ascii_lowercase()
                    || b.is_ascii_digit()
                    || b == b'-'
                    || b == b'_')
                && names.insert(name.to_string()),
            "unsafe or duplicate supplied index name"
        );
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
        let prefix = match name.len() {
            1 => "1".to_string(),
            2 => "2".to_string(),
            3 => format!("3/{}", &name[..1]),
            _ => format!("{}/{}", &name[..2], &name[2..4]),
        };
        anyhow::ensure!(
            output
                .insert(
                    format!("index/index.crates.io-1949cf8c6b5b557f/.cache/{prefix}/{name}"),
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
    let report = serde_json::json!({"root":root,"files":rows,"indexes":names.len(),"versionRecords":records,"archives":observed.len(),"wholeSuppliedIndexChecksumsMatched":true,"stockCacheSerializationRoundtripped":true,"expandedSourcesMaterialized":false,"sourceAuthentication":false,"corpusResolutionRun":false,"nativeAdmission":false,"SMComplete":false});
    std::fs::write(
        root.join("intake.json"),
        serde_json::to_vec_pretty(&report)?,
    )?;
    Ok(report)
}
fn receipt(path: &str) -> serde_json::Value {
    let raw = std::fs::read(path).unwrap();
    serde_json::json!({"path":path,"bytes":raw.len(),"sha256":sha(&raw)})
}
#[test]
fn actual_anonymous_public_inputs_roundtrip_stock_cache_before_whole_archive_intake() {
    let root = tempfile::Builder::new()
        .prefix("opensip-public-intake-control-")
        .tempdir()
        .unwrap()
        .keep();
    let index = receipt(
        "/tmp/opensip-implementation/sm-experimental-dependency-preparation-2026-10-10/missing-public-index-inputs-r1/receipt.json",
    );
    let archive = receipt(
        "/tmp/opensip-implementation/sm-experimental-dependency-preparation-2026-10-10/missing-public-archive-inputs-r1/receipt.json",
    );
    let r = intake(&root, &index, &archive).unwrap();
    assert_eq!(r["indexes"], 5);
    assert_eq!(r["versionRecords"], 135);
    assert_eq!(r["archives"], 135);
    assert_eq!(r["files"].as_array().unwrap().len(), 140);
    assert!(!root.join("registry/src").exists());
    eprintln!("ACTUAL_PUBLIC_CACHE_INTAKE_CONTROL={}", root.display());
}
#[test]
fn wrong_whole_checksum_and_wrong_receipt_pin_refuse_before_intake() {
    let root = tempfile::Builder::new()
        .prefix("opensip-public-intake-negative-")
        .tempdir()
        .unwrap()
        .keep();
    let index_receipt = receipt(
        "/tmp/opensip-implementation/sm-experimental-dependency-preparation-2026-10-10/missing-public-index-inputs-r1/receipt.json",
    );
    let mut bad_receipt:serde_json::Value=serde_json::from_slice(&std::fs::read("/tmp/opensip-implementation/sm-experimental-dependency-preparation-2026-10-10/missing-public-archive-inputs-r1/receipt.json").unwrap()).unwrap();
    let bad = root.join("corrupt-archive-input");
    std::fs::write(&bad, b"self-consistently pinned corrupt input").unwrap();
    let bad_pin = receipt(bad.to_str().unwrap());
    for key in ["path", "bytes", "sha256"] {
        bad_receipt["archives"][0][key] = bad_pin[key].clone();
    }
    // Declared local pin is internally consistent, but retained index checksum differs.
    let bad_receipt_path = root.join("corrupt-acquisition-receipt.json");
    std::fs::write(
        &bad_receipt_path,
        serde_json::to_vec_pretty(&bad_receipt).unwrap(),
    )
    .unwrap();
    assert!(
        intake(
            &root,
            &index_receipt,
            &receipt(bad_receipt_path.to_str().unwrap())
        )
        .is_err()
    );
    assert!(!root.join("registry").exists());
    let mut index = receipt(
        "/tmp/opensip-implementation/sm-experimental-dependency-preparation-2026-10-10/missing-public-index-inputs-r1/receipt.json",
    );
    index["sha256"] = serde_json::Value::String("0".repeat(64));
    let archive = receipt(
        "/tmp/opensip-implementation/sm-experimental-dependency-preparation-2026-10-10/missing-public-archive-inputs-r1/receipt.json",
    );
    assert!(intake(&root, &index, &archive).is_err());
    assert!(!root.join("registry").exists());
    std::fs::write(
        root.join("negative.json"),
        "{\"preIntakeRefusals\":2,\"registryOutputAbsent\":true,\"sourceAuthentication\":false}",
    )
    .unwrap();
    eprintln!("ACTUAL_PUBLIC_CACHE_INTAKE_CONTROL={}", root.display());
}

mod supplied_entry;

mod mixed_case_entry;
