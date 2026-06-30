from fastapi import APIRouter, UploadFile, File, HTTPException
from bson import ObjectId
from bson.errors import InvalidId
from datetime import datetime
from app.utils.file_parser import extract_text
from app.ai.llm_service import generate_answer
from app.database.mongodb import history_collection,documents_collection
from app.models.document_model import QuestionRequest

router=APIRouter()

@router.post("/documents/upload")
async def upload_document(file:UploadFile=File(...)):
    if not file.filename.endswith((".pdf",".txt")):
        raise HTTPException(400,"Only PDF and TXT allowed")

    text=extract_text(file)
    if not text:
        raise HTTPException(400,"Empty document")

    doc={"filename":file.filename,"text":text,"uploaded_at":datetime.utcnow()}
    result=await documents_collection.insert_one(doc)
    return {
        "message":"Uploaded successfully",
        "document_id":str(result.inserted_id)}

@router.get("/documents")
async def get_documents():
    data=[]
    async for doc in documents_collection.find():
        data.append({
            "document_id": str(doc["_id"]),
            "filename": doc["filename"],
            "upload_timestamp": doc["uploaded_at"]
        })
    if not data:
        return {"message": "No documents found"}
    return data

@router.post("/documents/{document_id}/ask")
async def ask_question(document_id: str, request: QuestionRequest):

    try:
        document = await documents_collection.find_one({"_id": ObjectId(document_id)})

    except InvalidId:
        raise HTTPException(status_code=404,detail="Document not found")

    if not document:
        raise HTTPException(status_code=404,detail="Document not found")

    answer = generate_answer(document["text"],request.question)

    await history_collection.insert_one({
        "document_id": document_id,
        "question": request.question,
        "answer": answer,
        "time": datetime.utcnow()
        })

    return {"answer": answer}

@router.delete("/documents/{document_id}")
async def delete_document(document_id:str):
    try:
        result = await documents_collection.delete_one({"_id": ObjectId(document_id)})
    except InvalidId:
        raise HTTPException(status_code=404,detail="Document not found")
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404,detail="Document not found")

    await history_collection.delete_many({"document_id":document_id})
    return {"message":"Deleted successfully"}