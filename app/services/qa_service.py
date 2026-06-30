from bson import ObjectId
from datetime import datetime
from app.database.mongodb import (documents_collection,history_collection)
from app.ai.llm_service import generate_answer

async def ask_question(document_id, question):
    document = await documents_collection.find_one({"_id":ObjectId(document_id)})
    if not document:
        raise ValueError("Document not found")

    answer = generate_answer(document["text"],question)
    await history_collection.insert_one({
        "document_id":document_id,
        "question":question,
        "answer":answer,
        "created_at":datetime.utcnow()
    })


    return {
        "question":question,
        "answer":answer
    }