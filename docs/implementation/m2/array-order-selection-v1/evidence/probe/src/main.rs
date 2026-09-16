use std::io::{self, BufRead};
use opensip_identity::{parse_json, canonical_bytes, JsonValue, ArrayOrder};
fn main() -> Result<(), Box<dyn std::error::Error>> {
 for line in io::stdin().lock().lines() {
  let line = line?;
  let value = parse_json(line.as_bytes())?;
  let JsonValue::Object(object) = &value else {return Err("expected object".into());};
  let JsonValue::Array(values) = &object["values"] else {return Err("expected array".into());};
  let before = canonical_bytes(&value)?;
  let good = ArrayOrder::parse(&object["order"]).and_then(|order| order.verify(values)).is_ok();
  assert_eq!(canonical_bytes(&value)?, before);
  println!("{}", u8::from(good));
 }
 Ok(())
}
