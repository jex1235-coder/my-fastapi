import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.session import get_db
from app.main import app


@pytest.fixture
def client():
    # 使用記憶體 SQLite 隔離各項測試，避免測試誤動到真實 MySQL 資料。
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)

    def override_db():
        with session_factory() as db:
            yield db

    app.dependency_overrides[get_db] = override_db
    try:
        # TestClient without a context manager does not run the MySQL startup lifespan.
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()
        engine.dispose()


def test_todo_crud(client):
    # 驗證首頁、靜態資源，以及任務新增到刪除的完整流程。
    assert client.get("/").status_code == 200
    assert client.get("/static/js/app.js").status_code == 200

    created = client.post("/todos/", json={"title": "  學習 FastAPI  "})
    assert created.status_code == 201
    todo = created.json()
    assert todo == {"id": 1, "title": "學習 FastAPI", "completed": False}
    assert client.get("/todos/1").json() == todo
    assert client.get("/todos/").json() == [todo]

    updated = client.patch("/todos/1", json={"completed": True, "title": "完成練習"})
    assert updated.status_code == 200
    assert updated.json() == {"id": 1, "title": "完成練習", "completed": True}
    assert client.delete("/todos/1").status_code == 204
    assert client.get("/todos/").json() == []
    assert client.get("/todos/1").status_code == 404
    assert client.patch("/todos/1", json={"completed": False}).status_code == 404
    assert client.delete("/todos/1").status_code == 404


def test_validation_and_pagination(client):
    # 確認不合法資料會被拒絕，分頁也維持新任務在前的順序。
    for title in ("   ", "x" * 256):
        assert client.post("/todos/", json={"title": title}).status_code == 422
    assert client.post("/todos/", json={"title": "第一件"}).status_code == 201
    assert client.post("/todos/", json={"title": "第二件"}).status_code == 201
    assert [item["title"] for item in client.get("/todos/?limit=1").json()] == ["第二件"]
    assert [item["title"] for item in client.get("/todos/?skip=1&limit=1").json()] == ["第一件"]
    assert client.patch("/todos/1", json={"title": "  "}).status_code == 422
    assert client.patch("/todos/1", json={"completed": None}).status_code == 422
    assert client.get("/todos/?limit=0").status_code == 422
