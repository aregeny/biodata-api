
# Day three generated code

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database import get_db
from app import models
from app.schemas import GeneCreate, GeneResponse, GeneUpdate
from typing import List, Optional

router = APIRouter(prefix="/genes", tags=["genes"])

@router.get("/", response_model=List[GeneResponse])
def get_genes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Gene).offset(skip).limit(limit).all()

@router.post("/", response_model=GeneResponse, status_code=201)
def create_gene(gene: GeneCreate, db: Session = Depends(get_db)):
    db_gene = models.Gene(**gene.model_dump())
    db.add(db_gene)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="A gene with this symbol and organism already exists")
    db.refresh(db_gene)
    return db_gene

@router.get("/search/", response_model=List[GeneResponse])
def search_genes(organism: Optional[str] = None, chromosome: Optional[str] = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    query = db.query(models.Gene)
    if organism:
        query = query.filter(models.Gene.organism.ilike(f"%{organism}%"))
    if chromosome:
        query = query.filter(models.Gene.chromosome == chromosome)
    return query.offset(skip).limit(limit).all()

@router.get("/{gene_id}", response_model=GeneResponse)
def get_gene(gene_id: int, db: Session = Depends(get_db)):
    gene = db.query(models.Gene).filter(models.Gene.id == gene_id).first()
    if gene is None:
        raise HTTPException(status_code=404, detail="Gene not found")
    return gene

@router.put("/{gene_id}", response_model=GeneResponse)
def update_gene(gene_id: int, gene_update: GeneUpdate, db: Session = Depends(get_db)):
    gene = db.query(models.Gene).filter(models.Gene.id == gene_id).first()
    if gene is None:
        raise HTTPException(status_code=404, detail="Gene not found")
    for field, value in gene_update.model_dump(exclude_unset=True).items():
        setattr(gene, field, value)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Update would create a duplicate gene")
    db.refresh(gene)
    return gene

@router.delete("/{gene_id}", status_code=204)
def delete_gene(gene_id: int, db: Session = Depends(get_db)):
    gene = db.query(models.Gene).filter(models.Gene.id == gene_id).first()
    if gene is None:
        raise HTTPException(status_code=404, detail="Gene not found")
    db.delete(gene)
    db.commit()


