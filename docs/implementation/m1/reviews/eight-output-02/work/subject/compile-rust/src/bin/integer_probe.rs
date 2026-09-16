use opensip_named_contracts_trial::generated::evidence::ExactInteger;
fn main() {
 for s in ["-9223372036854775808", "-1", "0", "1", "9223372036854775807", "9223372036854775808", "18446744073709551615"] {
  let x: ExactInteger=serde_json::from_str(s).unwrap();
  assert_eq!(serde_json::to_string(&x).unwrap(),s);
  assert_eq!(x.as_i128().to_string(),s);
 }
 for s in ["-9223372036854775809", "18446744073709551616", "1.0", "1e0", "-0", "true", "null", "[]", "{}", "\"1\""] {
  assert!(serde_json::from_str::<ExactInteger>(s).is_err(), "accepted {s}");
 }
 assert_eq!(ExactInteger::from(1_i64), ExactInteger::from(1_u64));
 assert!(ExactInteger::from(-1_i64)<ExactInteger::from(0_u64));
 println!("7 exact boundaries, 10 invalid forms, normalized equality/order passed");
}
