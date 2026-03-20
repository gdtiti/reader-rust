import re
import glob

def clean():
    for path in glob.glob("src/api/handlers/*.rs"):
        with open(path, "r") as f:
            content = f.read()

        content = content.replace("State(state), Query(access_q): Query<AccessTokenQuery>: State<AppState>", "State(state): State<AppState>, Query(access_q): Query<AccessTokenQuery>")

        with open(path, "w") as f:
            f.write(content)

if __name__ == "__main__":
    clean()
