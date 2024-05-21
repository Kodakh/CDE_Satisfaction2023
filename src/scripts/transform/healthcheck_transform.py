from fastapi import FastAPI

transformation_complete = False

app = FastAPI()

@app.get('/health')
def healthcheck():
    if transformation_complete:
        return {'status': 'ok'}
    else:
        return {'status': 'error'}