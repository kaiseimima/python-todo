import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app
from fastapi.testclient import TestClient
from app.config import settings

# テスト専用のDBファイル
# TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
settings.DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    settings.DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db():
    # テスト開始時にテーブル作成
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # テスト終了時にテーブルを削除
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(db):
    # FastAPIの get_db 関数を、テスト用DBを使うように「上書き」する
    def override_get_db():
        try:
            yield db
        finally:
            pass
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)
