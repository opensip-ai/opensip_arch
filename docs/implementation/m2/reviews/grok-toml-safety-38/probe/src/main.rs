//! Independent DeTable parse/drop resource probe. Not product code.

use std::env;
use std::time::Instant;

fn nested_array(n: usize) -> String {
    let mut s = String::from("x = ");
    for _ in 0..n {
        s.push('[');
    }
    s.push('1');
    for _ in 0..n {
        s.push(']');
    }
    s.push('\n');
    s
}

fn nested_inline(n: usize) -> String {
    let mut s = String::from("x = ");
    for i in 0..n {
        s.push('{');
        s.push_str("k");
        s.push_str(&i.to_string());
        s.push_str(" = ");
    }
    s.push('1');
    for _ in 0..n {
        s.push('}');
    }
    s.push('\n');
    s
}

fn dotted_assign(n: usize) -> String {
    let mut s = String::new();
    for i in 0..n {
        if i != 0 {
            s.push('.');
        }
        s.push('k');
        s.push_str(&i.to_string());
    }
    s.push_str(" = 1\n");
    s
}

fn std_table_chain(n: usize) -> String {
    let mut s = String::new();
    let mut acc = String::new();
    for i in 0..n {
        if i != 0 {
            acc.push('.');
        }
        acc.push('k');
        acc.push_str(&i.to_string());
        s.push('[');
        s.push_str(&acc);
        s.push_str("]\n");
    }
    s.push_str("v = 1\n");
    s
}

fn array_table_chain(n: usize) -> String {
    let mut s = String::new();
    let mut acc = String::new();
    for i in 0..n {
        if i != 0 {
            acc.push('.');
        }
        acc.push('k');
        acc.push_str(&i.to_string());
        s.push_str("[[");
        s.push_str(&acc);
        s.push_str("]]\n");
    }
    s.push_str("v = 1\n");
    s
}

fn unclosed_arrays(n: usize) -> String {
    let mut s = String::from("x = ");
    for _ in 0..n {
        s.push('[');
    }
    s
}

fn sibling_std_tables(count: usize) -> String {
    let mut s = String::new();
    for i in 0..count {
        s.push('[');
        s.push('t');
        s.push_str(&i.to_string());
        s.push_str("]\nv=1\n");
    }
    s
}

fn four_mib_open_brackets() -> String {
    let budget = 4 * 1024 * 1024;
    let prefix = "x = ";
    let n = budget - prefix.len();
    let mut s = String::with_capacity(budget);
    s.push_str(prefix);
    s.extend(std::iter::repeat('[').take(n));
    s
}

fn four_mib_sibling_tables() -> String {
    let budget = 4 * 1024 * 1024;
    let mut s = String::with_capacity(budget);
    let mut i = 0usize;
    while s.len() + 32 < budget {
        s.push('[');
        s.push('t');
        s.push_str(&i.to_string());
        s.push_str("]\nv=1\n");
        i += 1;
    }
    s
}

fn mixed_table_then_arrays(table_depth: usize, array_depth: usize) -> String {
    let mut s = std_table_chain(table_depth);
    s.push_str("x = ");
    for _ in 0..array_depth {
        s.push('[');
    }
    s.push('1');
    for _ in 0..array_depth {
        s.push(']');
    }
    s.push('\n');
    s
}

fn invalid_duplicate_table() -> String {
    "[a]\nv=1\n[a]\nw=2\n".to_string()
}

fn invalid_unclosed_inline() -> String {
    "x = { a = 1".to_string()
}

fn invalid_trailing_junk() -> String {
    "x = 1\n]]]{{\n".to_string()
}

fn build(case: &str) -> Result<String, String> {
    match case {
        "nested-array-80" => Ok(nested_array(80)),
        "nested-array-81" => Ok(nested_array(81)),
        "nested-inline-80" => Ok(nested_inline(80)),
        "nested-inline-81" => Ok(nested_inline(81)),
        "dotted-80" => Ok(dotted_assign(80)),
        "dotted-81" => Ok(dotted_assign(81)),
        "std-table-chain-80" => Ok(std_table_chain(80)),
        "std-table-chain-81" => Ok(std_table_chain(81)),
        "array-table-chain-80" => Ok(array_table_chain(80)),
        "array-table-chain-81" => Ok(array_table_chain(81)),
        "unclosed-array-80" => Ok(unclosed_arrays(80)),
        "unclosed-array-200" => Ok(unclosed_arrays(200)),
        "unclosed-array-10000" => Ok(unclosed_arrays(10_000)),
        "sibling-tables-1000" => Ok(sibling_std_tables(1000)),
        "four-mib-open-brackets" => Ok(four_mib_open_brackets()),
        "four-mib-sibling-tables" => Ok(four_mib_sibling_tables()),
        "mixed-80-80" => Ok(mixed_table_then_arrays(80, 80)),
        "invalid-duplicate-table" => Ok(invalid_duplicate_table()),
        "invalid-unclosed-inline" => Ok(invalid_unclosed_inline()),
        "invalid-trailing-junk" => Ok(invalid_trailing_junk()),
        "empty" => Ok(String::new()),
        other => Err(format!("unknown case {other}")),
    }
}

fn parse_and_drop(input: &str) -> String {
    match toml::de::DeTable::parse(input) {
        Ok(parsed) => {
            let keys = parsed.get_ref().len();
            drop(parsed);
            format!("ok keys={keys}")
        }
        Err(e) => format!("err:{}", e.message()),
    }
}

fn main() {
    let mut args = env::args().skip(1);
    let case = args.next().expect("case");
    let stack: Option<usize> = args.next().map(|s| s.parse().expect("stack bytes"));
    let input = match build(&case) {
        Ok(s) => s,
        Err(e) => {
            eprintln!("{e}");
            std::process::exit(2);
        }
    };
    let input_len = input.len();
    let start = Instant::now();
    let outcome = if let Some(stack_size) = stack {
        let (tx, rx) = std::sync::mpsc::channel();
        let handle = std::thread::Builder::new()
            .name("parse".into())
            .stack_size(stack_size)
            .spawn(move || {
                let r = parse_and_drop(&input);
                let _ = tx.send(r);
            })
            .expect("spawn");
        let r = rx.recv().expect("recv");
        handle.join().expect("join");
        r
    } else {
        parse_and_drop(&input)
    };
    let ms = start.elapsed().as_millis();
    println!("case={case} input_len={input_len} stack={stack:?} ms={ms} {outcome}");
}
