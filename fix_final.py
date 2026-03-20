import re
import glob

def fix():
    for path in glob.glob("src/api/handlers/*.rs"):
        with open(path, "r") as f:
            content = f.read()

        # Fix q.access_token to access_q.access_token
        content = re.sub(r'q\.access_token\.as_deref\(\), q\.secure_key\.as_deref\(\)', r'access_q.access_token.as_deref(), access_q.secure_key.as_deref()', content)
        
        # In book source getters, fix `&user_ns, &user_ns`
        content = content.replace('.get(&user_ns, &user_ns,', '.get(&user_ns,') 
        content = content.replace('.list(&user_ns, &user_ns,', '.list(&user_ns)') 
        content = content.replace('.delete(&user_ns, &user_ns,', '.delete(&user_ns,') 
        content = content.replace('.delete_all(&user_ns, &user_ns,', '.delete_all(&user_ns)')
        content = content.replace('.save_many(&user_ns, &user_ns,', '.save_many(&user_ns,')
        content = content.replace('.save(&user_ns, &user_ns,', '.save(&user_ns,')
        content = content.replace('.delete_all(&user_ns, &user_ns)', '.delete_all(&user_ns)')
        content = content.replace('.list(&user_ns, &user_ns)', '.list(&user_ns)')

        # Fix ? inside SSE async blocks
        # "let user_ns = ... .await.map_err(...)?;"
        # Inside async move { }, we cannot use ?, we should return or log.
        # But actually we can resolve user_ns *outside* the async move { } and pass it in!
        # Let's find "async move {" and move the user_ns resolution above it if it's there.
        # It's easier to just match the `let user_ns` line inside SSE blocks and remove it,
        # since it's already resolved at the top of the function!
        
        lines = content.split('\n')
        new_lines = []
        for line in lines:
            if 'let user_ns = state.user_service.resolve_user_ns' in line and ('Sse::new' in '\n'.join(lines) or 'tokio::spawn' in '\n'.join(lines)):
                # If it's indented inside the block (more than 4 spaces), remove it.
                if line.startswith('        let user_ns = '):
                    continue
            new_lines.append(line)
        content = '\n'.join(new_lines)
        
        # specific fix for book.rs line 743
        content = content.replace('.get(&book_source_url)', '.get(&user_ns, &book_source_url)')

        # specific fix: unused variable `q` in user.rs etc. We don't care about warnings.
        
        with open(path, "w") as f:
            f.write(content)

if __name__ == "__main__":
    fix()
