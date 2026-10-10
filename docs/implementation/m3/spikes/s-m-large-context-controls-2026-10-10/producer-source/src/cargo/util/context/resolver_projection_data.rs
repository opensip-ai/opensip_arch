// Exact NRC-1 conditional resolver namespace data, not owned config/profile admission.
use super::{ConfigValue, Definition};

#[derive(Debug)]
pub(crate) enum Refusal<'a> {
    NonTableResolver(&'a toml::Value),
    MalformedHonoredValue(&'a toml::Value),
}

pub(crate) struct ResolverData<'a> {
    pub(crate) original_namespace: Option<&'a toml::Value>,
    pub(crate) honored_leaf: Option<ConfigValue>,
    // Every other member retains its entire original value, including all descendants.
    // These are NOT the final public honoredKeys/strippedKeys accounting lists.
    pub(crate) stripped_members: Vec<(&'a str, &'a toml::Value)>,
}

/// Caller still owes actual original definition/root/effective-merge/input association.
/// No original file read, include, lock-path resolution or alternative failure route.
pub(crate) fn resolver_data<'a>(
    original_namespace: Option<&'a toml::Value>,
    definition: Definition,
) -> Result<ResolverData<'a>, Refusal<'a>> {
    let mut result = ResolverData {
        original_namespace,
        honored_leaf: None,
        stripped_members: Vec::new(),
    };
    let Some(value) = original_namespace else {
        return Ok(result);
    };
    let toml::Value::Table(table) = value else {
        return Err(Refusal::NonTableResolver(value));
    };
    for (name, value) in table {
        if name == "incompatible-rust-versions" {
            let toml::Value::String(text) = value else {
                return Err(Refusal::MalformedHonoredValue(value));
            };
            if text != "allow" && text != "fallback" {
                return Err(Refusal::MalformedHonoredValue(value));
            }
            result.honored_leaf = Some(ConfigValue::String(text.clone(), definition.clone()));
        } else {
            result.stripped_members.push((name.as_str(), value));
        }
    }
    Ok(result)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::core::Shell;
    use crate::util::GlobalContext;
    use std::collections::HashMap;
    fn namespace(source: &str) -> toml::Value {
        toml::from_str(source).unwrap()
    }
    #[test]
    fn resolver_projection_data_absence_no_synthesized_leaf() {
        let data = resolver_data(None, Definition::BuiltIn).unwrap();
        assert!(
            data.original_namespace.is_none()
                && data.honored_leaf.is_none()
                && data.stripped_members.is_empty()
        );
    }
    #[test]
    fn resolver_projection_data_allow_and_fallback_exact() {
        for text in ["allow", "fallback"] {
            let input = namespace(&format!("incompatible-rust-versions = \"{text}\""));
            let data = resolver_data(Some(&input), Definition::BuiltIn).unwrap();
            assert!(std::ptr::eq(data.original_namespace.unwrap(), &input));
            let Some(ConfigValue::String(value, _)) = data.honored_leaf else {
                panic!("expected string")
            };
            assert_eq!(value, text);
            assert!(data.stripped_members.is_empty());
        }
    }
    #[test]
    fn resolver_projection_data_non_table_retains_failure_input() {
        for input in [
            toml::Value::String("allow".into()),
            toml::Value::Boolean(false),
            toml::Value::Integer(1),
            toml::Value::Array(vec![]),
        ] {
            let Err(Refusal::NonTableResolver(original)) =
                resolver_data(Some(&input), Definition::BuiltIn)
            else {
                panic!("non-table must refuse")
            };
            assert!(std::ptr::eq(original, &input));
        }
    }
    #[test]
    fn resolver_projection_data_malformed_honored_no_coercion_or_drop() {
        for text in [
            "'Allow'",
            "'fallback '",
            "' allow'",
            "''",
            "true",
            "1",
            "1.5",
            "[]",
            "{}",
            "1979-05-27",
        ] {
            let input = namespace(&format!("incompatible-rust-versions = {text}"));
            let Err(Refusal::MalformedHonoredValue(original)) =
                resolver_data(Some(&input), Definition::BuiltIn)
            else {
                panic!("malformed must refuse: {text}")
            };
            assert!(std::ptr::eq(original, &input["incompatible-rust-versions"]));
        }
    }
    #[test]
    fn resolver_projection_data_other_members_whole_values_retained() {
        let input = namespace(
            "feature-unification = { nested = [{ alpha = 1.5 }, { beta = 1979-05-27 }] }\nlockfile-path = ['not/a/real/path', true]\nother = { deeper = { unchanged = false } }",
        );
        let data = resolver_data(Some(&input), Definition::BuiltIn).unwrap();
        assert!(data.honored_leaf.is_none());
        assert_eq!(data.stripped_members.len(), 3);
        for (key, value) in data.stripped_members {
            assert!(std::ptr::eq(value, &input[key]));
        }
    }
    #[test]
    fn resolver_projection_data_unknown_only_no_default() {
        let input =
            namespace("feature-unification = 'package'\nlockfile-path = 'elsewhere/Cargo.lock'");
        let data = resolver_data(Some(&input), Definition::BuiltIn).unwrap();
        assert!(data.honored_leaf.is_none());
        assert_eq!(data.stripped_members.len(), 2);
    }
    #[test]
    fn resolver_projection_data_supplied_definition_preserved_as_data() {
        let input = namespace("incompatible-rust-versions = 'fallback'");
        let definition = Definition::Path("/unadmitted/logical/.cargo/config.toml".into());
        let data = resolver_data(Some(&input), definition.clone()).unwrap();
        let Some(ConfigValue::String(_, actual)) = data.honored_leaf else {
            panic!("string expected")
        };
        assert_eq!(format!("{actual:?}"), format!("{definition:?}"));
    }
    #[test]
    fn resolver_projection_data_actual_context_consumes_selected_leaf() {
        let root = std::env::temp_dir().join(format!("resolver-data-{}", std::process::id()));
        std::fs::create_dir(&root).unwrap();
        let input = namespace(
            "incompatible-rust-versions = 'fallback'\nlockfile-path = { unexpected = true }",
        );
        let data = resolver_data(Some(&input), Definition::BuiltIn).unwrap();
        assert_eq!(data.stripped_members.len(), 1);
        let table = HashMap::from([(
            "incompatible-rust-versions".into(),
            data.honored_leaf.unwrap(),
        )]);
        let map = HashMap::from([(
            "resolver".into(),
            ConfigValue::Table(table, Definition::BuiltIn),
        )]);
        let mut gctx = GlobalContext::new_with_projected_values_data(
            Shell::new(),
            root.clone(),
            root.join("home"),
            map,
        )
        .unwrap();
        gctx.set_env(HashMap::new());
        assert_eq!(
            gctx.get::<String>("resolver.incompatible-rust-versions")
                .unwrap(),
            "fallback"
        );
        assert!(
            gctx.values().unwrap()["resolver"]
                .table("resolver")
                .unwrap()
                .0
                .contains_key("incompatible-rust-versions")
        );
    }
}
