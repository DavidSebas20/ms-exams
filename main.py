from fastapi import FastAPI
from app.config import settings
from app.routes.exams import router as exams_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Register routers
app.include_router(exams_router, prefix="/exams", tags=["Exams"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Microservice for managing exams"}
