from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.todos import router as todos_router
from app.db.base import Base
from app.db.session import engine
from app.models import Todo  # noqa: F401 - 匯入模型，讓資料表登記到 Base.metadata
from app.web.routes import router as web_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 啟動時僅建立不存在的資料表，不會清除既有任務或變更舊表欄位。
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Todo 任務清單", lifespan=lifespan)
# API 與首頁路由分開管理；CSS/JS 由 FastAPI 提供靜態檔案。
app.include_router(todos_router)
app.include_router(web_router)
app.mount(
    "/static",
    StaticFiles(directory=str(Path(__file__).resolve().parent / "static")),
    name="static",
)
