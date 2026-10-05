from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Todo(Base):
    """對應 MySQL 的 todos 資料表；欄位名稱與原有資料表相容。"""

    __tablename__ = "todos"

    # 自動遞增主鍵，供查詢、更新與刪除單筆任務使用。
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    completed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
