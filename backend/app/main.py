from fastapi import FastAPI
from database import engine, Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/up")
def read_root():
    return {"status": "ok"}