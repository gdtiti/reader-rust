import re
import glob

def refactor():
    files = glob.glob("src/api/handlers/*.rs")
    for path in files:
        if path.endswith("webdav.rs") or path.endswith("user.rs"): continue
        with open(path, "r") as f:
            content = f.read()

        changed = False
        import_stmt = 'use crate::api::handlers::webdav::AccessTokenQuery;'
        if 'AppState' in content and import_stmt not in content:
            content = content.replace('use axum::{extract::{State, Query},', f'use axum::{{extract::{{State, Query}}, Json}};\n{import_stmt}\n')
            content = content.replace('use crate::api::AppState;', f'use crate::api::AppState;\n{import_stmt}')
            changed = True
        
        book_methods = ["get_bookshelf", "get_shelf_book", "save_book", "delete_book", "delete_books", "save_book_progress", "cached_chapter_count", "is_chapter_cached", "cache_chapter", "get_cover", "load_book_sources_cache", "save_book_sources_cache", "get_content", "delete_cache"]
        source_methods = ["save", "save_many", "get", "list", "delete", "delete_all"]
        
        for m in book_methods:
            if f'state.book_service.{m}(' in content:
                content = content.replace(f'state.book_service.{m}(', f'state.book_service.{m}(&user_ns, ')
                changed = True
        
        for m in source_methods:
            if f'state.book_source_service.{m}(' in content:
                content = content.replace(f'state.book_source_service.{m}(', f'state.book_source_service.{m}(&user_ns, ')
                changed = True

        if changed:
            lines = content.split('\n')
            new_lines = []
            for i, line in enumerate(lines):
                if line.startswith('pub async fn ') and 'State(state)' in line:
                    if 'Query(access_q): Query<AccessTokenQuery>' not in line:
                        line = line.replace('State(state)', 'State(state), Query(access_q): Query<AccessTokenQuery>')
                    new_lines.append(line)
                    # Insert right after the opening brace
                    if line.rstrip().endswith('{'):
                        new_lines.append('    let user_ns = state.user_service.resolve_user_ns(access_q.access_token.as_deref(), access_q.secure_key.as_deref()).await.map_err(|_| AppError::BadRequest("NEED_LOGIN".to_string()))?;')
                elif line.strip() == '{' and new_lines and new_lines[-1].startswith('pub async fn '):
                    new_lines.append(line)
                    new_lines.append('    let user_ns = state.user_service.resolve_user_ns(access_q.access_token.as_deref(), access_q.secure_key.as_deref()).await.map_err(|_| AppError::BadRequest("NEED_LOGIN".to_string()))?;')
                else:
                    new_lines.append(line)
            
            with open(path, "w") as f:
                f.write('\n'.join(new_lines))

if __name__ == "__main__":
    refactor()
