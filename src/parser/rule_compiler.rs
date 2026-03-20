#[derive(Debug, Clone)]
pub struct CompiledRule {
    pub raw: String,
}

pub struct RuleCompiler;

impl RuleCompiler {
    pub fn compile(rule_text: &str) -> CompiledRule {
        CompiledRule { raw: rule_text.to_string() }
    }
}
