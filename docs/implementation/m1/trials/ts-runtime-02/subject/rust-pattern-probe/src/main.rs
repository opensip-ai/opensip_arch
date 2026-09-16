use serde_json::Value;
use std::{env, fs, path::PathBuf};

fn main() {
    let root = PathBuf::from(env::args().nth(1).expect("trial directory"));
    let profile: Value = serde_json::from_slice(&fs::read(root.join("pattern-profile.json")).unwrap()).unwrap();
    let cases: Value = serde_json::from_slice(&fs::read(root.join("pattern-cases.json")).unwrap()).unwrap();
    let patterns = profile["patterns"].as_array().unwrap();
    let values = cases["values"].as_array().unwrap();
    let mut mismatches = vec![];
    for (p, row) in patterns.iter().enumerate() {
        let regex = regress::Regex::with_flags(row["ecma262Unicode"].as_str().unwrap(), "u").unwrap();
        for (i, value) in values.iter().enumerate() {
            let actual = regex.find(value.as_str().unwrap()).is_some();
            if actual != cases["expected"][p][i].as_bool().unwrap() {
                mismatches.push(serde_json::json!({"pattern": row["source"], "value": value, "actual": actual}));
            }
        }
    }
    let result = serde_json::json!({"patterns":patterns.len(), "values":values.len(),
        "comparisons":patterns.len()*values.len(), "mismatches":mismatches, "productQualification":false});
    fs::write(root.join("rust-pattern-differential.json"), serde_json::to_vec_pretty(&result).unwrap()).unwrap();
    println!("{result}");
    assert!(mismatches.is_empty());
}
