use std::{env, fs};
fn main() {
    let path = env::args().nth(1).expect("schema argument");
    let raw = fs::read_to_string(path).unwrap();
    let schema = serde_json::from_str(&raw).unwrap();
    let mut types = typify::TypeSpace::default();
    match types.add_root_schema(schema) {
        Ok(_) => println!("{}", types.to_stream()),
        Err(error) => { eprintln!("generation refused: {error:?}"); std::process::exit(2); }
    }
}
