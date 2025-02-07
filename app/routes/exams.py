from fastapi import APIRouter, HTTPException, UploadFile, Form, Query
from app.models import Exam
from app.database import table, s3_client
import uuid
from datetime import datetime
from app.config import settings
from typing import List

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

@router.get("/by-patient/", response_model=List[Exam])
def list_exams_by_patient(patient_id: str = Query(..., description="ID del paciente")):
    """
    Busca todos los exámenes asociados a un paciente específico.
    """
    # Usa un filtro en la operación scan de DynamoDB
    response = table.scan(
        FilterExpression="patient_id = :pid",
        ExpressionAttributeValues={":pid": patient_id}
    )
    
    items = response.get("Items", [])
    
    if not items:
        raise HTTPException(status_code=404, detail=f"No exams found for patient_id: {patient_id}")
    
    return items

@router.delete("/{exam_id}")
def delete_exam(exam_id: str):
    try:
        # Intenta eliminar el ítem con una condición: el ítem debe existir
        response = table.delete_item(
            Key={"exam_id": exam_id},
            ConditionExpression="attribute_exists(exam_id)"
        )
        return {"message": "Exam deleted successfully"}
    except table.meta.client.exceptions.ConditionalCheckFailedException:
        # Si el ítem no existe, DynamoDB lanza esta excepción
        raise HTTPException(status_code=404, detail="Exam not found")