from fastapi import FastAPI
from app.routes.exams import router as exams_router

app = FastAPI()

# Register routers
app.include_router(exams_router, prefix="/exams", tags=["Exams"])

@app.get("/")
def root():
    return {"message": "Microservice for managing exams"}
