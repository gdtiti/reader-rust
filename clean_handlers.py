import re
import glob

def clean():
    for path in glob.glob("src/api/handlers/*.rs"):
        with open(path, "r") as f:
            content = f.read()

        # Remove duplicate AccessTokenQuery let statements
        content = re.sub(r'(\s*let user_ns = state\.user_service.*?)+\n(\s*let user_ns =)', r'\2', content)

        # Fix the pub async fn signatures that have duplicates
        # Example broken:
        # pub async fn get_book_info(State(state), Query(access_q): Query<AccessTokenQuery>: State<AppState>, Query(q): Query<AccessTokenQuery>, Query(param): Query<BookInfoRequest>, body: Option<Json<BookInfoRequest>>)
        def fix_sig(m):
            sig = m.group(0)
            sig = re.sub(r'State\(state\),\s*Query\(access_q\):\s*Query<AccessTokenQuery>:\s*State<AppState>,\s*Query\(q\):\s*Query<AccessTokenQuery>', 
                         r'State(state): State<AppState>, Query(access_q): Query<AccessTokenQuery>', sig) 
            sig = re.sub(r'State\(state\),\s*Query\(access_q\):\s*Query<AccessTokenQuery>:\s*State<AppState>', 
                         r'State(state): State<AppState>, Query(access_q): Query<AccessTokenQuery>', sig) 
            return sig

        content = re.sub(r'pub async fn [^\(]+\([^\)]+\)', fix_sig, content)

        with open(path, "w") as f:
            f.write(content)

if __name__ == "__main__":
    clean()
