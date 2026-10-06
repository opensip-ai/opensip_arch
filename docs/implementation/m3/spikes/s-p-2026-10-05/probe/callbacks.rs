#![feature(rustc_private)]
extern crate rustc_driver;
extern crate rustc_interface;
extern crate rustc_middle;

struct Probe { expanded: bool, analyzed: bool }
impl rustc_driver::Callbacks for Probe {
    fn after_expansion<'tcx>(
        &mut self, _: &rustc_interface::interface::Compiler,
        _: rustc_middle::ty::TyCtxt<'tcx>,
    ) -> rustc_driver::Compilation {
        self.expanded = true;
        println!("{}", r#"{"callback":"after_expansion"}"#);
        rustc_driver::Compilation::Continue
    }
    fn after_analysis<'tcx>(
        &mut self, _: &rustc_interface::interface::Compiler,
        _: rustc_middle::ty::TyCtxt<'tcx>,
    ) -> rustc_driver::Compilation {
        self.analyzed = true;
        println!("{}", r#"{"callback":"after_analysis"}"#);
        rustc_driver::Compilation::Stop
    }
}
fn main() {
    let args: Vec<String> = std::env::args().collect();
    let mut callbacks = Probe { expanded: false, analyzed: false };
    rustc_driver::run_compiler(&args, &mut callbacks);
    assert!(callbacks.expanded && callbacks.analyzed);
}
