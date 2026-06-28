# from fastapi import APIRouter, HTTPException
# from app.schemas import GeneCreate, GeneResponse
# from typing import List, Optional

# router = APIRouter(prefix="/genes", tags=["genes"])

# genes_db: List[dict] = []
# counter = 1

# @router.get("/", response_model=List[GeneResponse])
# def get_genes():
#     return genes_db

# @router.post("/", response_model=GeneResponse, status_code=201)
# def create_gene(gene: GeneCreate):
#     global counter
#     new_gene = gene.model_dump()
#     new_gene["id"] = counter
#     counter += 1
#     genes_db.append(new_gene)
#     return new_gene

# @router.get("/{gene_id}", response_model=GeneResponse)
# def get_gene(gene_id: int):
#     for gene in genes_db:
#         if gene["id"] == gene_id:
#             return gene
#     raise HTTPException(status_code=404, detail="Gene not found")

# Above is day two, below is day three 

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.schemas import GeneCreate, GeneResponse, GeneUpdate
from typing import List, Optional

router = APIRouter(prefix="/genes", tags=["genes"])

@router.get("/", response_model=List[GeneResponse])
def get_genes(db: Session = Depends(get_db)):
    return db.query(models.Gene).all()

@router.post("/", response_model=GeneResponse, status_code=201)
def create_gene(gene: GeneCreate, db: Session = Depends(get_db)):
    db_gene = models.Gene(**gene.model_dump())
    db.add(db_gene)
    db.commit()
    db.refresh(db_gene)
    return db_gene

@router.get("/{gene_id}", response_model=GeneResponse)
def get_gene(gene_id: int, db: Session = Depends(get_db)):
    gene = db.query(models.Gene).filter(models.Gene.id == gene_id).first()
    if gene is None:
        raise HTTPException(status_code=404, detail="Gene not found")
    return gene