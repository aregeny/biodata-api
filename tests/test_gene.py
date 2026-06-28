from fastapi.testclient import TestClient
from app.main import app
#Fixes due to Day Three additions
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import get_db, Base
from app import models
import pytest

SQLALCHEMY_TEST_DATABASE_URL = "postgresql://postgres:password@localhost:5432/biodata"

engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db   
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

#Beyond is previous Day 2
client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200

def test_create_gene():
    gene_data = {
        "gene_symbol": "BRCA1",
        "gene_name": "Breast Cancer 1",
        "organism": "Homo sapiens",
        "chromosome": "17",
        "description": "tumor suppressor gene"
    }
    response = client.post("/genes/", json=gene_data)
    assert response.status_code == 201
    assert response.json()["gene_symbol"] == "BRCA1"

def test_get_nonexistent_gene():
    response = client.get("/genes/9999")
    assert response.status_code == 404