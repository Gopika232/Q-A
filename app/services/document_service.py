from datetime import datetime
from bson import ObjectId
from app.database.mongodb import (documents_collection,history_collection)
from app.utils.file_parser import extract_text

async def upload_document(file):
    if not file.filename.endswith((".pdf", ".txt")):
        raise ValueError("Only PDF and TXT files are allowed")
    text = extract_text(file)

    if not text.strip():
        raise ValueError("Document is empty")

    document = {
        "filename": file.filename,
        "text": text,
        "uploaded_at": datetime.utcnow()
    }

    result = await documents_collection.insert_one(document)

    return {
        "document_id": str(result.inserted_id),
        "filename": file.filename
    }

async def get_documents():
    documents=[]
    async for doc in documents_collection.find():
        documents.append({
            "document_id": str(doc["_id"]),
            "filename": doc["filename"],
            "upload_timestamp": doc["uploaded_at"]
        })

    return documents

async def delete_document(document_id):

    result = await documents_collection.delete_one({"_id":ObjectId(document_id)})
    await history_collection.delete_many({"document_id":document_id})
    if result.deleted_count == 0:
        raise ValueError("Document not found")

    return {
        "message":"Document deleted successfully"
    }