from fastapi import FastAPI
from app.routers import genes
from app.database import engine
from app import models

models.Base.metadata.create_all(bind=engine) 

app = FastAPI(
    title="Biodata API",
    description="A backend service for biological data",
    version="0.1.0",
)

app.include_router(genes.router) 

@app.get("/")
def root():
    return {"message": "BioData API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}