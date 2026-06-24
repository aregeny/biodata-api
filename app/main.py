from fastapi import FastAPI

app = FastAPI(
    title="Biodata API",
    description="A backend service for biological data",
    version="0.1.0",
)

@app.get("/")
def root():
    return {"message": "BioData API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}