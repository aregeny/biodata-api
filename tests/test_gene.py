from fastapi.testclient import TestClient
from app.main import app
#Fixes due to Day Three additions
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import get_db, Base
from app import models
import pytest

SQLALCHEMY_TEST_DATABASE_URL = "postgresql://postgres:password@localhost:5432/biodata_test"

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

def test_duplicate_gene_symbol_same_organism_rejected():
    # Arrange
    gene_data = {
        "gene_symbol": "BRCA1",
        "gene_name": "Breast Cancer 1",
        "organism": "Homo sapiens",
        "chromosome": "17"
    }
    first_response = client.post("/genes/", json=gene_data)
    assert first_response.status_code == 201  # sanity check the first insert worked

    # Act
    second_response = client.post("/genes/", json=gene_data)  # exact same data

    # Assert
    assert second_response.status_code == 409


def test_same_gene_symbol_different_organism_allowed():
    # Arrange
    human_gene = {
        "gene_symbol": "BRCA1",
        "gene_name": "Breast Cancer 1",
        "organism": "Homo sapiens",
        "chromosome": "17"
    }
    client.post("/genes/", json=human_gene)

    # Act
    mouse_gene = {
        "gene_symbol": "BRCA1",  # same symbol
        "gene_name": "Breast Cancer 1",
        "organism": "Mus musculus",  # different organism
        "chromosome": "11"
    }
    response = client.post("/genes/", json=mouse_gene)

    # Assert
    assert response.status_code == 201  # should succeed, not conflict

def test_failed_duplicate_insert_does_not_corrupt_table():
    # Arrange
    gene_data = {
        "gene_symbol": "TP53",
        "gene_name": "Tumor Protein P53",
        "organism": "Homo sapiens",
        "chromosome": "17"
    }
    client.post("/genes/", json=gene_data)

    # Act — attempt the duplicate, which should fail
    client.post("/genes/", json=gene_data)

    # Assert — exactly one row exists, not zero, not two
    all_genes = client.get("/genes/").json()
    matching = [g for g in all_genes if g["gene_symbol"] == "TP53" and g["organism"] == "Homo sapiens"]
    assert len(matching) == 1

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

def test_create_gene_with_missing_required_field():
    # gene_symbol is required - omitting it should return 422
    gene_data = {
        "gene_name": "Breast Cancer 1",
        "organism": "Homo sapiens",
    } 
    response = client.post("/genes/", json=gene_data)
    assert response.status_code == 422

def test_update_gene_to_duplicate_organism_rejected():
    # Arrange — two genes, same symbol, different organism
    gene_a = {
        "gene_symbol": "BRCA1",
        "gene_name": "Breast Cancer 1",
        "organism": "Homo sapiens",
        "chromosome": "17"
    }
    gene_b = {
        "gene_symbol": "BRCA1",
        "gene_name": "Breast Cancer 1",
        "organism": "Mus musculus",
        "chromosome": "11"
    }
    client.post("/genes/", json=gene_a)
    create_b_response = client.post("/genes/", json=gene_b)
    gene_b_id = create_b_response.json()["id"]

    # Act — try to update gene_b's organism to collide with gene_a
    update_response = client.put(f"/genes/{gene_b_id}", json={"organism": "Homo sapiens"})

    # Assert — the update was rejected
    assert update_response.status_code == 409

    # Assert — gene_b's organism is still what it originally was, not corrupted
    get_response = client.get(f"/genes/{gene_b_id}")
    assert get_response.json()["organism"] == "Mus musculus"

def test_get_nonexistent_gene():
    response = client.get("/genes/9999")
    assert response.status_code == 404

def test_update_gene():
    #Create a test gene
    gene_data = {
        "gene_symbol": "TP53",
        "gene_name": "Tumour Protein P53",
        "organism": "Homo sapiens",
        "chromosome": "17"
    }
    create_response = client.post("/genes/", json=gene_data)
    gene_id = create_response.json()["id"]

    #Update the test gene
    update_data = {
        "gene_name": "Tumour Suppressor P53"
    }
    response = client.put(f"/genes/{gene_id}", json=update_data)
    assert response.status_code == 200
    #Check that the field that is changed, was changed, and other fields were not changed.
    assert response.json()["gene_name"] == "Tumour Suppressor P53"
    assert response.json()["gene_symbol"] == "TP53"

def test_update_non_existent_gene():
    response = client.put("/genes/9999", json={"gene_name": "Updated"})
    assert response.status_code == 404

def test_delete_gene():
    # Create test gene to delete
    gene_data = {
        "gene_symbol": "EGFR",
        "gene_name": "Epidermal Growth Factor Receptor",
        "organism": "Homo sapiens"
    }

    create_response = client.post("/genes/", json=gene_data)
    gene_id = create_response.json()["id"]

    #Delete test gene
    response = client.delete(f"/genes/{gene_id}")
    assert response.status_code==204

    #Confirm test gene is deleted
    response = client.delete(f"/genes/{gene_id}")
    assert response.status_code==404

def test_delete_non_existent_gene():
    response = client.delete("/genes/9999")
    assert response.status_code == 404

def test_search_genes():
    # Create two versions of test gene (one version for one organism)
    client.post("/genes/", json={
        "gene_symbol": "BRCA1",
        "gene_name": "Breast Cancer 1",
        "organism": "Homo sapiens",
        "chromosome": "17"
    })
    client.post("/genes/", json={
        "gene_symbol": "Brca1",
        "gene_name": "Breast Cancer 1",
        "organism": "Mus musculus",
        "chromosome": "11"
    })

    # Search test gene by organism
    response = client.get("/genes/search/?organism=Homo")
    assert response.status_code==200
    results = response.json()
    assert len(results) == 1
    assert results[0]["organism"] == "Homo sapiens"

def test_search_by_chromosome():
    client.post("/genes/", json={
        "gene_symbol": "TP53",
        "gene_name": "Tumour Protein P53",
        "organism": "Homo sapiens",
        "chromosome": "17"
    })
    client.post("/genes/", json={
        "gene_symbol": "Brca1",
        "gene_name": "Breast Cancer 1",
        "organism": "Mus musculus",
        "chromosome": "11"
    })
    response = client.get("/genes/search/?chromosome=17")
    assert response.status_code==200
    results = response.json()
    assert len(results) == 1
    assert all(g["chromosome"] == "17" for g in results)