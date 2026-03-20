use regex::Regex;

pub fn strip_whitespace(s: &str) -> String {
    s.split_whitespace().collect::<Vec<_>>().join(" ")
}

pub fn apply_regex_replace(input: &str, pattern: &str, replace: &str) -> String {
    if let Ok(re) = Regex::new(pattern) {
        re.replace_all(input, replace).to_string()
    } else {
        input.to_string()
    }
}
