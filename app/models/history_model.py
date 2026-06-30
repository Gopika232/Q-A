from pydantic import BaseModel
from datetime import datetime

class HistoryResponse(BaseModel):
    document_id: str
    question: str
    answer: str
    created_at: datetime