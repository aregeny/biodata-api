from fastapi.testclient import TestClient
from app.main import app

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