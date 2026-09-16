use quote::ToTokens;
use std::{collections::BTreeMap, env, fs, path::PathBuf};
use syn::{visit::Visit, visit_mut::VisitMut, Item};

fn main() {
    let root = PathBuf::from(env::args().nth(1).expect("trial root"));
    let output = PathBuf::from(env::args().nth(2).expect("fresh output root"));
    let owners: serde_json::Value = serde_json::from_slice(&fs::read(root.join("owners.json")).unwrap()).unwrap();
    let owners: Vec<_> = owners.as_array().unwrap().iter().map(|row|
        (row["namespace"].as_str().unwrap().to_owned(), row["module"].as_str().unwrap().to_owned())).collect();
    let schema = serde_json::from_slice(&fs::read(root.join("rust-projection.json")).unwrap()).unwrap();
    let mut settings = typify::TypeSpaceSettings::default();
    settings.with_map_type(typify::MapType::new("::std::collections::BTreeMap"));
    settings.with_conversion(serde_json::from_value(serde_json::json!({"type":"integer"})).unwrap(), "ExactInteger", [typify::TypeSpaceImpl::Display].into_iter());
    let mut types = typify::TypeSpace::new(&settings);
    types.add_root_schema(schema).expect("schema generation");
    let mut parsed: syn::File = syn::parse2(types.to_stream()).expect("generated Rust syntax");
    PreservePresence.visit_file_mut(&mut parsed);
    let mut groups: BTreeMap<&str, Vec<Item>> = ["evidence", "identity", "invocation", "output", "protocol"].map(|name|(name, vec![])).into();
    for mut item in parsed.items {
        if let Item::Enum(value) = &item { assert!(!value.variants.is_empty(), "uninhabited generated enum {}", value.ident); }
        let name = match &item {
            Item::Struct(x) => x.ident.to_string(),
            Item::Enum(x) => x.ident.to_string(),
            Item::Type(x) => x.ident.to_string(),
            Item::Impl(x) => {
                // Normally the self type owns the implementation. For foreign
                // targets such as From<OwnedType> for String, the sole local
                // generated type in the trait arguments owns it instead.
                let mut ids = Names(vec![]);
                ids.visit_type(&x.self_ty);
                if !ids.0.iter().any(|id| owners.iter().any(|(prefix,_)|id.starts_with(prefix))) {
                    if let Some((_, path, _)) = &x.trait_ { ids.visit_path(path); }
                }
                ids.0.into_iter().find(|id| owners.iter().any(|(prefix,_)|id.starts_with(prefix))).expect("impl owner")
            }
            Item::Mod(x) => x.ident.to_string(),
            _ => panic!("unclassified generated item"),
        };
        let owner = if name == "error" || name == "defaults" {
            if let Item::Mod(module) = &mut item {
                module.vis = syn::parse_quote!(pub(crate));
                if name == "defaults" {
                    if let Some((_, items)) = &mut module.content {
                        for child in items { if let Item::Fn(f) = child { f.vis = syn::parse_quote!(pub(crate)); } }
                    }
                }
            }
            "evidence"
        } else {
            let matched: Vec<_> = owners.iter().filter(|(prefix,_)|name.starts_with(prefix)).collect();
            assert_eq!(matched.len(), 1, "unique owner of {name}");
            matched[0].1.as_str()
        };
        groups.get_mut(owner).unwrap().push(item);
    }
    let dir = output.join("crates/contracts/src/generated");
    fs::create_dir_all(&dir).unwrap();
    let header = "// Generated trial: named28 profile, typify0.8.0; inert carriers only.\n";
    for (name, items) in &groups {
        let mut text = header.to_owned();
        text.push_str("#![allow(unused_imports)]\n");
        for sibling in groups.keys().filter(|s|*s != name) {
            text.push_str(&format!("use super::{sibling}::*;\n"));
        }
        if *name != "evidence" { text.push_str("use super::evidence::error;\n"); }
        if *name == "evidence" { text.push_str(include_str!("presence.rs")); text.push_str(include_str!("integers.rs")); }
        for item in items { text.push_str(&item.to_token_stream().to_string()); text.push('\n'); }
        let syntax=syn::parse_file(&text).expect("final generated syntax");
        let formatted=header.to_owned()+&prettyplease::unparse(&syntax);
        fs::write(dir.join(format!("{name}.rs")), formatted).unwrap();
    }
    let mut index = header.to_owned();
    for name in groups.keys() { index.push_str(&format!("pub mod {name};\n")); }
    fs::write(dir.join("mod.rs"), index).unwrap();
    println!("generated six Rust files");
}

struct PreservePresence;
impl VisitMut for PreservePresence {
    fn visit_field_mut(&mut self, field: &mut syn::Field) {
        let mut optional = false;
        let mut kept = vec![];
        let mut attrs = vec![];
        for attr in &field.attrs {
            if attr.path().is_ident("serde") {
                let values = attr.parse_args_with(syn::punctuated::Punctuated::<syn::Meta, syn::Token![,]>::parse_terminated).unwrap();
                for value in values {
                    if value.path().is_ident("default") || value.path().is_ident("skip_serializing_if") {
                        optional = true;
                    } else { kept.push(value); }
                }
            } else { attrs.push(attr.clone()); }
        }
        if optional {
            let inner = &field.ty;
            field.ty = syn::parse_quote!(FieldPresence<#inner>);
            kept.push(syn::parse_quote!(default));
            kept.push(syn::parse_quote!(skip_serializing_if = "FieldPresence::is_missing"));
        }
        if !kept.is_empty() { attrs.push(syn::parse_quote!(#[serde(#(#kept),*)])); }
        field.attrs = attrs;
    }
}

struct Names(Vec<String>);
impl<'ast> Visit<'ast> for Names {
    fn visit_type_path(&mut self, node: &'ast syn::TypePath) {
        if let Some(segment) = node.path.segments.last() { self.0.push(segment.ident.to_string()); }
        syn::visit::visit_type_path(self, node);
    }
    fn visit_path(&mut self, node: &'ast syn::Path) {
        for segment in &node.segments { self.0.push(segment.ident.to_string()); }
        syn::visit::visit_path(self, node);
    }
}
