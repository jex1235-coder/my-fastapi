-- ==========================================
-- FastAPI Todo 專案資料庫
-- 資料庫名稱：fastapi_db
-- 資料表名稱：todos
-- ==========================================

CREATE DATABASE IF NOT EXISTS fastapi_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE fastapi_db;

CREATE TABLE IF NOT EXISTS todos (
    id INT NOT NULL AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    completed BOOLEAN NOT NULL DEFAULT FALSE,

    PRIMARY KEY (id),
    INDEX idx_todos_title (title)
);

-- 範例資料請依需要自行新增；重複執行此檔不會清除現有任務。
