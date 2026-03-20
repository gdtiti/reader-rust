use crate::error::error::AppError;
use crate::model::book_source::BookSource;
use crate::storage::db::repo::BookSourceRepo;

#[derive(Clone)]
pub struct BookSourceService {
    repo: BookSourceRepo,
}

impl BookSourceService {
    pub fn new(repo: BookSourceRepo) -> Self {
        Self { repo }
    }

    pub async fn save(&self, user_ns: &str, source: BookSource) -> Result<(), AppError> {
        let json = serde_json::to_string(&source).map_err(|e| AppError::BadRequest(e.to_string()))?;
        self.repo.upsert(user_ns, &source, &json).await
    }

    pub async fn save_many(&self, user_ns: &str, sources: Vec<BookSource>) -> Result<(), AppError> {
        for s in sources {
            self.save(user_ns, s).await?;
        }
        Ok(())
    }

    pub async fn get(&self, user_ns: &str, book_source_url: &str) -> Result<Option<BookSource>, AppError> {
        let json = self.repo.get(user_ns, book_source_url).await?;
        if let Some(j) = json {
            let source: BookSource = serde_json::from_str(&j).map_err(|e| AppError::BadRequest(e.to_string()))?;
            Ok(Some(source))
        } else {
            Ok(None)
        }
    }

    pub async fn list(&self, user_ns: &str) -> Result<Vec<BookSource>, AppError> {
        let rows = self.repo.list(user_ns).await?;
        let mut out = Vec::with_capacity(rows.len());
        for j in rows {
            if let Ok(s) = serde_json::from_str::<BookSource>(&j) {
                out.push(s);
            }
        }
        Ok(out)
    }

    pub async fn delete(&self, user_ns: &str, book_source_url: &str) -> Result<(), AppError> {
        self.repo.delete(user_ns, book_source_url).await
    }

    pub async fn delete_all(&self, user_ns: &str) -> Result<(), AppError> {
        self.repo.delete_all(user_ns).await
    }
}
