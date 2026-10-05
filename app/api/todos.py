from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.todo import Todo
from app.repositories import todo as repository
from app.schemas.todo import TodoCreate, TodoResponse, TodoUpdate

# 此處只處理 HTTP 請求與錯誤；實際資料庫操作放在 repository。
router = APIRouter(prefix="/todos", tags=["todos"])


def find_todo(todo_id: int, db: Session) -> Todo:
    """共用單筆查詢與 404 處理，避免各路由重複判斷。"""
    todo = repository.get_todo(db, todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="任務不存在")
    return todo


@router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(data: TodoCreate, db: Session = Depends(get_db)):
    # FastAPI 先以 TodoCreate 驗證輸入，再由 response_model 限定輸出欄位。
    return repository.create_todo(db, data)


@router.get("/", response_model=list[TodoResponse])
def read_todos(
    # Query 限定分頁範圍：前端逐頁載入，每頁最多 100 筆。
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
    db: Session = Depends(get_db),
):
    return repository.list_todos(db, skip, limit)


@router.get("/{todo_id}", response_model=TodoResponse)
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    return find_todo(todo_id, db)


@router.patch("/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, data: TodoUpdate, db: Session = Depends(get_db)):
    # 先檢查任務是否存在，再交由 repository 更新有提供的欄位。
    return repository.update_todo(db, find_todo(todo_id, db), data)


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    repository.delete_todo(db, find_todo(todo_id, db))
    # 刪除成功時回傳 204，依 HTTP 慣例不附加 JSON 內容。
    return Response(status_code=status.HTTP_204_NO_CONTENT)
