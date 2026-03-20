import re
import glob

def clean():
    for path in glob.glob("src/api/handlers/*.rs"):
        with open(path, "r") as f:
            content = f.read()

        # Fix syntax error caused by double replacement
        content = content.replace("list(&user_ns) ).await", "list(&user_ns).await")
        content = content.replace("delete_all(&user_ns) ).await", "delete_all(&user_ns).await")

        # Fix duplicate let user_ns lines
        # if a function has two identical declarations
        lines = content.split('\n')
        new_lines = []
        user_ns_line = 'let user_ns = state.user_service.resolve_user_ns(access_q.access_token.as_deref(), access_q.secure_key.as_deref()).await.map_err(|_| AppError::BadRequest("NEED_LOGIN".to_string()))?;'
        
        in_func = False
        seen_user_ns = False
        for line in lines:
            if line.startswith('pub async fn'):
                in_func = True
                seen_user_ns = False
                new_lines.append(line)
            elif in_func and user_ns_line in line:
                if not seen_user_ns:
                    new_lines.append(line)
                    seen_user_ns = True
            else:
                new_lines.append(line)
                
        with open(path, "w") as f:
            f.write('\n'.join(new_lines))

if __name__ == "__main__":
    clean()
