import glob

def clean():
    with open("src/api/handlers/book.rs", "r") as f:
        content = f.read()

    content = content.replace(".get_cover(&user_ns, &user_ns, &url)", ".get_cover(&user_ns, &url)")
    content = content.replace(".is_chapter_cached(&user_ns, &user_ns, &ch.url)", ".is_chapter_cached(&user_ns, &ch.url)")
    content = content.replace(".cache_chapter(&src, &url, refresh_flag)", ".cache_chapter(&user_ns, &src, &url, refresh_flag)")
    
    # line 505: book_source_service.get(&url)
    content = content.replace("book_source_service.get(&url)", "book_source_service.get(&user_ns, &url)")
    # line 514: book_source_service.list()
    content = content.replace("book_source_service.list()", "book_source_service.list(&user_ns)")
    # line 592: get_shelf_book(&book_url)
    content = content.replace("get_shelf_book(&book_url)", "get_shelf_book(&user_ns, &book_url)")
    # line 655: save_book_sources_cache(&book.book_url, &all_results)
    content = content.replace("save_book_sources_cache(&book.book_url, &all_results)", "save_book_sources_cache(&user_ns, &book.book_url, &all_results)")

    with open("src/api/handlers/book.rs", "w") as f:
        f.write(content)

    with open("src/api/handlers/user.rs", "r") as f:
        user_content = f.read()
    
    # Fix the user.rs error
    # It currently says:
    #     let user_ns = match state.user_service.resolve_user_ns(q.access_token.as_deref(), q.secure_key.as_deref()).await {
    # but the python script might have made it:
    #     user_ns = state.user_service.resolve...
    user_content = user_content.replace("    user_ns = ", "    let user_ns = match ")
    user_content = user_content.replace("await.map_err(|_| AppError::BadRequest(\"NEED_LOGIN\".to_string()))?;", "await {")

    with open("src/api/handlers/user.rs", "w") as f:
        f.write(user_content)

if __name__ == "__main__":
    clean()
