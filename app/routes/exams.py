from fastapi import APIRouter, HTTPException, UploadFile, Form
from app.models import Exam
from app.database import table, s3_client
import uuid
from datetime import datetime
from app.config import settings

router = APIRouter()

@router.get("/")
def list_exams():
    response = table.scan()
    return response.get("Items", [])

@router.get("/{exam_id}", response_model=Exam)
def get_exam(exam_id: str):
    response = table.get_item(Key={"exam_id": exam_id})
    if "Item" not in response:
        raise HTTPException(status_code=404, detail="Exam not found")
    return response["Item"]

@router.post("/", response_model=Exam)
def create_exam(
    patient_id: str = Form(...),
    exam_type: str = Form(...),
    description: str = Form(None),
    uploaded_by: str = Form(...),
    file: UploadFile = None,
):
    exam_id = str(uuid.uuid4())
    date = datetime.utcnow().strftime("%Y-%m-%d")
    image_link = None

    if file:
        file_key = f"exams/{exam_id}/{file.filename}"
        s3_client.upload_fileobj(file.file, settings.s3_bucket, file_key)
        image_link = f"https://{settings.s3_bucket}.s3.{settings.aws_region}.amazonaws.com/{file_key}"

    exam = {
        "exam_id": exam_id,
        "patient_id": patient_id,
        "exam_type": exam_type,
        "description": description,
        "date": date,
        "image_link": image_link,
        "uploaded_by": uploaded_by,
    }
    table.put_item(Item=exam)
    return exam

@router.delete("/{exam_id}")
def delete_exam(exam_id: str):
    response = table.delete_item(Key={"exam_id": exam_id})
    if response.get("ResponseMetadata", {}).get("HTTPStatusCode") != 200:
        raise HTTPException(status_code=500, detail="Error deleting exam")
    return {"message": "Exam deleted successfully"}
