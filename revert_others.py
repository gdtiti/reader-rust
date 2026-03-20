import re
import glob

def clean():
    for path in glob.glob("src/api/handlers/*.rs"):
        if path.endswith("book.rs") or path.endswith("book_source.rs"): continue
        with open(path, "r") as f:
            content = f.read()

        # Remove the inserted let user_ns = ... line
        bad_line = r'^\s*let user_ns = state\.user_service\.resolve_user_ns\(access_q\.access_token\.as_deref\(\), access_q\.secure_key\.as_deref\(\)\)\.await\.map_err\(\|_\| AppError::BadRequest\("NEED_LOGIN"\.to_string\(\)\)\)\?;\n'
        content = re.sub(bad_line, "", content, flags=re.MULTILINE)

        bad_line2 = r'^\s*let user_ns = state\.user_service\.resolve_user_ns\(q\.access_token\.as_deref\(\), q\.secure_key\.as_deref\(\)\)\.await\.map_err\(\|_\| AppError::BadRequest\("NEED_LOGIN"\.to_string\(\)\)\)\?;\n'
        content = re.sub(bad_line2, "", content, flags=re.MULTILINE)

        # Restore access_q back to q
        content = content.replace("access_q.access_token.as_deref()", "q.access_token.as_deref()")
        content = content.replace("access_q.secure_key.as_deref()", "q.secure_key.as_deref()")
        content = content.replace("Query(access_q): Query<AccessTokenQuery>", "Query(q): Query<AccessTokenQuery>")

        with open(path, "w") as f:
            f.write(content)

if __name__ == "__main__":
    clean()
