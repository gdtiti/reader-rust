import re
import glob

def clean():
    for path in glob.glob("src/api/handlers/*.rs"):
        with open(path, "r") as f:
            content = f.read()

        # Fix duplicate &user_ns, &user_ns in method calls
        content = content.replace("get_shelf_book(&user_ns, &user_ns", "get_shelf_book(&user_ns")
        content = content.replace("load_book_sources_cache(&user_ns, &user_ns", "load_book_sources_cache(&user_ns")
        content = content.replace("save_book_sources_cache(&user_ns, &user_ns", "save_book_sources_cache(&user_ns")

        # Fix SSE return types to allow `?`
        content = re.sub(r'-> Sse<impl futures::Stream<Item = Result<Event, Infallible>>> \{', r'-> Result<Sse<impl futures::Stream<Item = Result<Event, Infallible>>>, AppError> {', content)
        
        # When SSE function ends, it must return Ok(Sse::new(...))
        content = re.sub(r'Sse::new\(ReceiverStream::new\(rx\)\.map\(Ok\)\)\n\}', r'Ok(Sse::new(ReceiverStream::new(rx).map(Ok)))\n}', content)

        with open(path, "w") as f:
            f.write(content)

if __name__ == "__main__":
    clean()
