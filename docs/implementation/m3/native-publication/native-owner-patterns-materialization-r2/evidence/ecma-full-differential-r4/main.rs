#[path="original.rs"] mod original;
#[path="candidate.rs"] mod candidate;
fn main() {
 let forms: &[&str] = &[r##"^[0-9a-f]{64}(?![\s\S])"##,r##"^sha256:[0-9a-f]{64}(?![\s\S])"##,r##"^snapshot2:[0-9a-f]{64}(?![\s\S])"##,r##"^closure2:[0-9a-f]{64}(?![\s\S])"##,r##"^import2:[0-9a-f]{64}(?![\s\S])"##,r##"^(?!/)(?![\s\S]*(^|/)\.\.?(/|$))[^\u0000\\]+(?![\s\S])"##,r##"^(?!\.\.?(?:/|(?![\s\S])))[^\u0000\\/]+(/(?!\.\.?(?:/|(?![\s\S])))[^\u0000\\/]+)*(?![\s\S])"##,r##"^(?:|(?!\.\.?(?:/|(?![\s\S])))[^\u0000\\/]+(/(?!\.\.?(?:/|(?![\s\S])))[^\u0000\\/]+)*)(?![\s\S])"##,r##"^[a-z][a-z0-9._:-]*(?![\s\S])"##,r##"^(DISCLOSURE-ONLY|ENFORCED-BY-CONSTRUCTION|ENFORCED-AT-HOST-BROKER|ENFORCED-PLATFORM:[a-z0-9.-]{1,64})(?![\s\S])"##,r##"^[0-9a-f]{40}(?![\s\S])"##,r##"^prj1-[0-9a-f]{64}(?![\s\S])"##,r##"^security.repo-execution-grants.v2:[0-9a-f]{64}(?![\s\S])"##,r##"^[0-9]{4}-[0-9]{2}-[0-9]{2}(?![\s\S])"##,r##"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z(?![\s\S])"##,r##"^([0-9a-f]{40}|[0-9a-f]{64})(?![\s\S])"##,r##"^(?!/)(?![\s\S]*(^|/)\.\.?(/|$))[^\u0000\\]*(?![\s\S])"##,r##"^(DIRECTORY_CUSTODY:[A-Z_]+|MARKER_CUSTODY:(Cargo\.toml|package\.json|tsconfig\.json|jsconfig\.json):[A-Z_]+|DEPTH)(?![\s\S])"##,r##"^scope2:[0-9a-f]{64}(?![\s\S])"##,r##"^coverage2:[0-9a-f]{64}(?![\s\S])"##,r##"^[A-Za-z0-9_.-]+(?![\s\S])"##,r##"^[^\u0000-\u001f\u007f-\u009f]+(?![\s\S])"##,r##"^[a-z][a-z0-9-]*:[^\u0000-\u001f\u007f-\u009f]+(?![\s\S])"##,r##"^[^\u0000-\u001f\u007f-\u009f]*(?![\s\S])"##,r##"^[^/\\\u0000]{1,255}(/[^/\\\u0000]{1,255})*(?![\s\S])"##,r##"(^|/)\.\.?(/|$)"##];
 let bytes=std::fs::read(std::env::args().nth(1).unwrap()).unwrap();
 let mut at=0usize;let mut values=Vec::new();
 while at<bytes.len() { let n=u32::from_le_bytes(bytes[at..at+4].try_into().unwrap()) as usize;at+=4;values.push(std::str::from_utf8(&bytes[at..at+n]).unwrap());at+=n; }
 let old_forms=original::selected_patterns();
 let shared_forms=candidate::selected_patterns();
 assert_eq!(old_forms.len(),72);
 assert_eq!(shared_forms,old_forms,"shared inherited profile expanded");
 for pattern in forms {
  if !old_forms.contains(pattern) {
   for value in &values {assert!(candidate::matches(pattern,value).is_err(),"new native form leaked into shared profile: {pattern:?}");}
  }
 }
 let mut checked=0usize;
 for pattern in original::selected_patterns() {for value in &values {assert_eq!(original::matches(pattern,value),candidate::matches(pattern,value),"legacy changed {pattern:?} {value:?}");checked+=1;}}
 let mut matrix=Vec::new();for pattern in forms {for value in &values {matrix.push(match candidate::matches_native_owner(pattern,value){Ok(false)=>0,Ok(true)=>1,Err(_)=>2});}}
 std::fs::write(std::env::args().nth(2).unwrap(),matrix).unwrap();
 println!("old_forms=72 inputs={} legacy_comparisons={checked}",values.len());
}
