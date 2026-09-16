use opensip_contracts::generated::protocol::Control3Root;
fn main() {
    let raw = std::fs::read(std::env::args().nth(1).expect("cases")).unwrap();
    let cases: Vec<serde_json::Value> = serde_json::from_slice(&raw).unwrap();
    let mut rows = Vec::new();
    for case in &cases {
        let bytes: Vec<u8> = if let Some(s) = case["raw"].as_str() { s.as_bytes().to_vec() } else {
            let h = case["rawHex"].as_str().unwrap();
            (0..h.len()).step_by(2).map(|i| u8::from_str_radix(&h[i..i + 2], 16).unwrap()).collect()
        };
        let (accepted, roundtrip, error) = match serde_json::from_slice::<Control3Root>(&bytes) {
            Ok(carrier) => {
                let original: Option<serde_json::Value> = serde_json::from_slice(&bytes).ok();
                (true, original.map(|o| serde_json::to_value(&carrier).unwrap() == o), None)
            }
            Err(e) => (false, None, Some(e.to_string())),
        };
        rows.push(serde_json::json!({"id": case["id"], "accepted": accepted, "roundtrip": roundtrip, "error": error}));
    }
    println!("{}", serde_json::to_string(&rows).unwrap());
}
