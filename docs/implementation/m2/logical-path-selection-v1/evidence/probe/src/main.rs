use std::io::{self, BufRead};
use opensip_identity::{parse_json, JsonValue, LogicalPath};
fn main() -> Result<(), Box<dyn std::error::Error>> {
    for line in io::stdin().lock().lines() {
        let line = line?;
        let JsonValue::String(value) = parse_json(line.as_bytes())? else { return Err("expected string".into()); };
        let result = LogicalPath::parse(&value);
        if let Ok(ref admitted) = result { assert_eq!(admitted.as_str(), value); }
        println!("{}", u8::from(result.is_ok()));
    }
    Ok(())
}
