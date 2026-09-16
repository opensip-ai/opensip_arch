// Review probe: raw bytes -> generated inert carrier -> serde_json bytes.
use opensip_named_contracts_trial::generated::{evidence, identity, output, protocol};
use serde::{Serialize, de::DeserializeOwned};

fn rt<T: Serialize + DeserializeOwned>(raw: &str) -> Result<String, String> {
    let dto: T = serde_json::from_str(raw).map_err(|e| e.to_string())?;
    serde_json::to_string(&dto).map_err(|e| e.to_string())
}

fn check(reference: &str, raw: &str) -> Result<String, String> {
    match reference {
        "urn:opensip:product-v1:identity:v3#/$defs/finding-parameters" => rt::<identity::Identity3FindingParameters>(raw),
        "urn:opensip:product-v1:workflows:policy-document#/$defs/Atom" => rt::<evidence::Policy1Atom>(raw),
        "opensip.product.provider-handshake.1#/$defs/TypeScriptCapabilitiesV2" => rt::<protocol::Handshake1TypeScriptCapabilitiesV2>(raw),
        "opensip.product.provider-handshake.1#/$defs/TypeScriptHelloV2" => rt::<protocol::Handshake1TypeScriptHelloV2>(raw),
        "urn:opensip:product-v1:workflows:common#/$defs/LogicalPath" => rt::<evidence::Common1LogicalPath>(raw),
        "urn:opensip:product-v1:workflows:evaluator3:command-envelope:4" => rt::<output::Envelope4Root>(raw),
        _ => panic!("unknown ref {reference}"),
    }
}

fn main() {
    let cases_path = std::env::args().nth(1).unwrap();
    let fixtures_path = std::env::args().nth(2).unwrap();
    let mut cases: Vec<serde_json::Value> = serde_json::from_slice(&std::fs::read(cases_path).unwrap()).unwrap();
    // Presence controls derived from the metadata parser-refusal fixture.
    let fixtures: serde_json::Value = serde_json::from_slice(&std::fs::read(fixtures_path).unwrap()).unwrap();
    let refusal = fixtures["cases"].as_array().unwrap().iter()
        .find(|c| c["id"] == "parser-refusal-no-invented-detail").unwrap()["value"].clone();
    let mut without_errors = refusal.clone();
    without_errors.as_object_mut().unwrap().remove("errors");
    let envelope = "urn:opensip:product-v1:workflows:evaluator3:command-envelope:4";
    cases.push(serde_json::json!({"id": "envelope-refusal-errors-empty", "ref": envelope, "raw": refusal.to_string()}));
    cases.push(serde_json::json!({"id": "envelope-refusal-errors-missing", "ref": envelope, "raw": without_errors.to_string()}));
    let mut rows = vec![];
    for case in &cases {
        let raw = case["raw"].as_str().unwrap();
        let row = match check(case["ref"].as_str().unwrap(), raw) {
            Ok(out) => {
                let input: Result<serde_json::Value, _> = serde_json::from_str(raw);
                let output: serde_json::Value = serde_json::from_str(&out).unwrap();
                serde_json::json!({"id": case["id"], "rust": "accepted", "output": out,
                    "valueEqualToSerdeParse": input.as_ref().ok() == Some(&output),
                    "serdeParseOfInput": input.map(|v| v.to_string()).unwrap_or_else(|e| e.to_string())})
            }
            Err(e) => serde_json::json!({"id": case["id"], "rust": "refused", "error": e}),
        };
        rows.push(row);
    }
    println!("{}", serde_json::to_string_pretty(&rows).unwrap());
}
