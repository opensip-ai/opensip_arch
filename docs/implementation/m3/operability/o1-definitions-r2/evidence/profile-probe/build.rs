fn main() {
    let profile = std::env::var("PROFILE").expect("Cargo PROFILE");
    let opt = std::env::var("OPT_LEVEL").expect("Cargo OPT_LEVEL");
    let debug = std::env::var("DEBUG").expect("Cargo DEBUG");
    println!("cargo::warning=PROFILE_CAPTURE={profile};OPT_LEVEL={opt};DEBUG={debug}");
}
