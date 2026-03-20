mod book;
mod book_source;
mod user;
mod rss;
mod bookmark;
mod replace_rule;
mod webdav;
mod book_group;

pub use book::*;
pub use book_source::*;
pub use user::*;
pub use rss::*;
pub use bookmark::*;
pub use replace_rule::*;
pub use webdav::*;
pub use book_group::*;

use axum::response::IntoResponse;
use axum::Json;
use crate::error::error::ApiResponse;

pub async fn health() -> impl IntoResponse {
    Json(ApiResponse::ok("ok"))
}
