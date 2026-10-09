#![feature(rustc_private)]
extern crate rustc_driver;
extern crate rustc_interface;
extern crate rustc_middle;
use std::io::{self, Write};
struct Probe;
impl rustc_driver::Callbacks for Probe {
    fn after_analysis<'tcx>(
        &mut self,
        _: &rustc_interface::interface::Compiler,
        _: rustc_middle::ty::TyCtxt<'tcx>,
    ) -> rustc_driver::Compilation {
        println!("{}", r#"{"event":"after_analysis"}"#);
        rustc_driver::Compilation::Stop
    }
}
fn main() {
    let args: Vec<String> = std::env::args().collect();
    let mut callbacks = Probe;
    if args.get(1).map(String::as_str) == Some("--startup-probe") {
        println!("{}", r#"{"event":"ready","compiler":"1.95.0"}"#);
        io::stdout().flush().unwrap();
        let mut line = String::new();
        io::stdin().read_line(&mut line).unwrap();
    } else {
        rustc_driver::run_compiler(&args, &mut callbacks);
    }
}
