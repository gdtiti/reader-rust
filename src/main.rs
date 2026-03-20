mod app;
mod api;
mod service;
mod parser;
mod crawler;
mod storage;
mod model;
mod error;
mod util;

use app::bootstrap::run;

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    println!("Server starting...");
    run().await
}
