from fastapi import FastAPI
from app.config import settings
from app.routes.exams import router as exams_router

app = FastAPI()

# Register routers
app.include_router(exams_router, prefix="/exams", tags=["Exams"])

print (settings.aws_access_key_id)
print (settings.aws_secret_access_key)
print (settings.aws_session_token)
print (settings.aws_region)
print (settings.dynamodb_table)
print (settings.s3_bucket)

@app.get("/")
def root():
    return {"message": "Microservice for managing exams"}
