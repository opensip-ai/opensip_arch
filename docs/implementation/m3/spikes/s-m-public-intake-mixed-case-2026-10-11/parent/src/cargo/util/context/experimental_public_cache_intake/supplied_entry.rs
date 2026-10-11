//! Supplied prototype packet entry; no authenticated source or production authority.
use super::*;
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
    let result = intake(root, &packet["indexReceipt"], &packet["archiveReceipt"]);
    let outcome = serde_json::json!({"success":result.is_ok(),"error":result.as_ref().err().map(|e|format!("{e:#}")),"intake":result.ok(),"packetPin":row,"sourceAuthentication":false,"corpusResolutionRun":false,"nativeAdmission":false,"SMComplete":false});
    std::fs::write(root.join("entry-packet-observation.json"), raw)?;
    std::fs::write(
        root.join("entry-outcome.json"),
        serde_json::to_vec_pretty(&outcome)?,
    )?;
    Ok(outcome)
}
fn retained_root() -> PathBuf {
    tempfile::Builder::new()
        .prefix("opensip-public-entry-control-")
        .tempdir()
        .unwrap()
        .keep()
}
fn packet(root: &Path, bad_index: bool) -> serde_json::Value {
    let mut index = receipt(
        "/tmp/opensip-implementation/sm-experimental-dependency-preparation-2026-10-10/missing-public-index-inputs-r1/receipt.json",
    );
    if bad_index {
        index["sha256"] = serde_json::Value::String("0".repeat(64));
    }
    let archive = receipt(
        "/tmp/opensip-implementation/sm-experimental-dependency-preparation-2026-10-10/missing-public-archive-inputs-r1/receipt.json",
    );
    let value =
        serde_json::json!({"outputRoot":root,"indexReceipt":index,"archiveReceipt":archive});
    let path = root.join("supplied-packet.json");
    std::fs::write(&path, serde_json::to_vec_pretty(&value).unwrap()).unwrap();
    receipt(path.to_str().unwrap())
}
#[test]
fn exact_packet_entry_calls_closed_intake_with_real_retained_public_inputs() {
    let root = retained_root();
    let pin = packet(&root, false);
    let result = run_packet(&pin).unwrap();
    assert_eq!(result["success"], true);
    assert_eq!(result["intake"]["archives"], 135);
    assert_eq!(result["intake"]["indexes"], 5);
    assert_eq!(result["intake"]["files"].as_array().unwrap().len(), 140);
    assert!(!root.join("registry/src").exists());
    eprintln!("ACTUAL_PUBLIC_INTAKE_ENTRY_CONTROL={}", root.display());
}
#[test]
fn actual_packet_pin_refusal_and_incomplete_intake_remain_distinct() {
    let root = retained_root();
    let good = packet(&root, true);
    let mut bad = good.clone();
    bad["sha256"] = serde_json::Value::String("0".repeat(64));
    assert!(run_packet(&bad).is_err());
    assert!(!root.join("entry-outcome.json").exists());
    let result = run_packet(&good).unwrap();
    assert_eq!(result["success"], false);
    assert!(result["error"].is_string());
    assert!(!root.join("registry").exists());
    eprintln!("ACTUAL_PUBLIC_INTAKE_ENTRY_CONTROL={}", root.display());
}
#[test]
#[ignore]
fn collect_explicit_experimental_public_cache_intake() {
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
