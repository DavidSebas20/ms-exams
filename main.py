from fastapi import FastAPI
from app.config import settings

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Microservice for managing exams"}
