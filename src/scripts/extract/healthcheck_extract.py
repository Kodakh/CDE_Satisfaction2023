from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "Le service d'extraction fonctionne correctement"}