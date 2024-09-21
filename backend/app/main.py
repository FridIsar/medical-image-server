from fastapi import FastAPI

app = FastAPI()

@app.get("/up")
def read_root():
    return {"status": "ok"}