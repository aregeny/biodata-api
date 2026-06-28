from fastapi import FastAPI
from app.routers import genes #Day two addition

app = FastAPI(
    title="Biodata API",
    description="A backend service for biological data",
    version="0.1.0",
)

app.include_router(genes.router) # Day two addition


@app.get("/")
def root():
    return {"message": "BioData API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}