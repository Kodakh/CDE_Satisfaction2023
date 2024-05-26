from fastapi import FastAPI

app = FastAPI()

@app.get('/health')
def healthcheck():
    return {"status": "Le service de transformation fonctionne correctement"}