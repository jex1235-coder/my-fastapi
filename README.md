# Todo 任務清單

FastAPI + SQLAlchemy + MySQL 的 Todo 專案，附繁體中文網頁介面。支援新增、檢視、修改、完成切換、刪除與篩選任務。

## 安裝與啟動

需要 Python 3.10+ 與 MySQL。以下以 PowerShell 為例：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

先在 MySQL 執行 `fastapi_db.sql` 建立資料庫；也可以只執行 `CREATE DATABASE fastapi_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;`。啟動時 SQLAlchemy 會建立尚不存在的 `todos` 資料表，不會刪除既有資料。`create_all` 不會修改已存在的資料表結構；日後變更欄位需要資料庫遷移。

設定資料庫連線（參考 `.env.example`）：

```powershell
$env:DATABASE_URL = "mysql+pymysql://root:your_password@localhost:3306/fastapi_db"
python -m uvicorn app.main:app --reload
```

連線設定透過環境變數讀取；若未設定，預設為 `mysql+pymysql://root:@localhost:3306/fastapi_db`，供本機無密碼的 MySQL 練習環境使用。此專案不會自動載入 `.env` 檔案，請將變數設定到執行程序的環境中。

- 網頁：<http://127.0.0.1:8000/>
- 互動式 API 文件：<http://127.0.0.1:8000/docs>
- 舊的 `python main.py` 或 `uvicorn main:app --reload` 啟動方式仍可使用。

## API

| 方法 | 路徑 | 說明 |
| --- | --- | --- |
| GET | `/todos/?skip=0&limit=100` | 依最新建立順序列出任務 |
| GET | `/todos/{todo_id}` | 讀取任務 |
| POST | `/todos/` | 新增任務，例如 `{"title":"買牛奶"}` |
| PATCH | `/todos/{todo_id}` | 修改任務，例如 `{"completed":true}` 或 `{"title":"新名稱"}` |
| DELETE | `/todos/{todo_id}` | 刪除任務 |

## 專案結構

- `app/core/`：環境設定
- `app/db/`、`app/models/`：連線與資料表模型
- `app/schemas/`：API 輸入輸出驗證
- `app/repositories/`：資料庫操作
- `app/api/`：Todo API 路由
- `app/web/`、`app/templates/`、`app/static/`：頁面及靜態檔案
- `tests/`：API 測試

執行測試：`python -m pip install -r requirements-dev.txt` 後執行 `python -m pytest`。測試使用記憶體 SQLite，不會操作 MySQL 資料。

# my-fastapi
