import re

with open("src/parser/rule_engine.rs", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add base_url to search_books_json
content = content.replace(
    'fn search_books_json(&self, source: &BookSource, body: &str, rule: &SearchRule)',
    'fn search_books_json(&self, source: &BookSource, body: &str, base_url: &str, rule: &SearchRule)'
)
content = content.replace(
    'return self.search_books_json(source, body, &rule);',
    'return self.search_books_json(source, body, base_url, &rule);'
)

# 2. Add base_url to parse_book_info_json
content = content.replace(
    'fn parse_book_info_json(source: &BookSource, v: &Value, rule: &BookInfoRule, book_url: &str)',
    'fn parse_book_info_json(source: &BookSource, v: &Value, base_url: &str, rule: &BookInfoRule, book_url: &str)'
)
content = content.replace(
    'return parse_book_info_json(source, &v, &rule, book_url);',
    'return parse_book_info_json(source, &v, base_url, &rule, book_url);'
)

# 3. Add base_url to parse_chapter_list_json
content = content.replace(
    'fn parse_chapter_list_json(body: &str, rule: &TocRule)',
    'fn parse_chapter_list_json(body: &str, base_url: &str, rule: &TocRule)'
)
content = content.replace(
    'return parse_chapter_list_json(body, &rule);',
    'return parse_chapter_list_json(body, base_url, &rule);'
)

# 4. Replace html method calls
content = re.sub(r'html::select_text_from_element\(&el, r\)', r'eval_field_html(r, &el, base_url)', content)
content = re.sub(r'html::select_text\(&doc, r\)', r'eval_field_html_doc(r, &doc, base_url)', content)

# 5. Replace pick_json_field with eval_field_json
content = re.sub(
    r'pick_json_field\(&item,\s*([^)]+\.as_deref\(\))\)',
    r'eval_field_json(\1.unwrap_or(""), &item, base_url)',
    content
)

content = re.sub(
    r'pick_json_field\(v,\s*([^)]+\.as_deref\(\))\)',
    r'eval_field_json(\1.unwrap_or(""), v, base_url)',
    content
)

with open("src/parser/rule_engine.rs", "w", encoding="utf-8") as f:
    f.write(content)
