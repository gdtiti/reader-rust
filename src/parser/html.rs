use scraper::{Html, Selector, ElementRef};

pub fn parse_document(html: &str) -> Html {
    Html::parse_document(html)
}

pub fn select_list<'a>(doc: &'a Html, selector: &str) -> Vec<ElementRef<'a>> {
    let sel_text = selector.split('@').next().unwrap_or(selector).trim();
    if let Ok(sel) = Selector::parse(sel_text) {
        doc.select(&sel).collect()
    } else {
        vec![]
    }
}

pub fn select_text_from_element(el: &ElementRef, rule: &str) -> Option<String> {
    let parts: Vec<&str> = rule.split('@').collect();
    let mut current_el = el.clone();
    
    for i in 0..parts.len() {
        let part = parts[i].trim();
        if part.is_empty() { continue; }
        
        // Final part could be an attribute or special extractor (text, html)
        if i == parts.len() - 1 {
            return match part {
                "text" => Some(current_el.text().collect::<Vec<_>>().join(" ").trim().to_string()),
                "html" => Some(current_el.html()),
                attr => {
                    if attr.is_empty() {
                         Some(current_el.text().collect::<Vec<_>>().join(" ").trim().to_string())
                    } else {
                        current_el.value().attr(attr).map(|v| v.to_string())
                    }
                },
            };
        }
        
        // Intermediate part is a selector
        // Support index shortcut like .class.0 or .class.-1
        let (selector_str, index) = parse_selector_with_index(part);
        let sel = match Selector::parse(&selector_str) {
            Ok(s) => s,
            Err(_) => return None,
        };
        
        let matches: Vec<_> = current_el.select(&sel).collect();
        if matches.is_empty() { return None; }
        
        let idx = if index < 0 {
            let n = matches.len() as i32 + index;
            if n < 0 { return None; }
            n as usize
        } else {
            index as usize
        };
        
        if idx < matches.len() {
            current_el = matches[idx];
        } else {
            return None;
        }
    }
    
    // Default if no parts or only one part that is not an attribute
    Some(current_el.text().collect::<Vec<_>>().join(" ").trim().to_string())
}

pub fn select_text(doc: &Html, rule: &str) -> Option<String> {
    let parts: Vec<&str> = rule.split('@').collect();
    if parts.is_empty() { return None; }

    // For root selection, first part MUST be a selector
    let first_part = parts[0].trim();
    let (selector_str, index) = parse_selector_with_index(first_part);
    
    let sel = match Selector::parse(&selector_str) {
        Ok(s) => s,
        Err(_) => return None,
    };
    
    let matches: Vec<_> = doc.select(&sel).collect();
    if matches.is_empty() { return None; }
    
    let idx = if index < 0 {
        let n = matches.len() as i32 + index;
        if n < 0 { return None; }
        n as usize
    } else {
        index as usize
    };
    
    if idx < matches.len() {
        let el = matches[idx];
        if parts.len() > 1 {
            // Pass the rest of the chain to select_text_from_element
            let rest = parts[1..].join("@");
            return select_text_from_element(&el, &rest);
        } else {
            return Some(el.text().collect::<Vec<_>>().join(" ").trim().to_string());
        }
    }
    None
}

/// Parses a selector string and extracts index shortcut like .class.0
fn parse_selector_with_index(s: &str) -> (String, i32) {
    if let Some(pos) = s.rfind('.') {
        let last_part = &s[pos + 1..];
        if let Ok(idx) = last_part.parse::<i32>() {
            return (s[..pos].to_string(), idx);
        }
    }
    (s.to_string(), 0)
}
