use chrono::{DateTime, Utc};

pub fn now_ts() -> i64 {
    Utc::now().timestamp()
}

pub fn now_rfc3339() -> String {
    let now: DateTime<Utc> = Utc::now();
    now.to_rfc3339()
}
