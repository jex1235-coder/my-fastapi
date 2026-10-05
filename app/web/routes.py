from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

# 使用檔案所在位置尋找模板，避免從其他工作目錄啟動時找不到頁面。
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parents[1] / "templates"))
router = APIRouter()


@router.get("/", include_in_schema=False)
def home(request: Request):
    # 首頁由模板提供 HTML；任務資料在瀏覽器端透過 /todos/ API 取得。
    return templates.TemplateResponse(request, "index.html")
