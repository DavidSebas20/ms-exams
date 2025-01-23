from pydantic import BaseModel
from typing import Optional

class Exam(BaseModel):
    exam_id: str
    patient_id: str
    exam_type: str
    description: Optional[str]
    date: str
    image_link: Optional[str]
    uploaded_by: str
