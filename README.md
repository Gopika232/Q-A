# Document Q&A API

## Overview

This project is a backend API for a Document Question & Answer system.
Users can upload documents, ask questions based on the uploaded documents, view history, and delete documents along with their associated chat history.

The API is built using **FastAPI**, **MongoDB**, and an **LLM API** for generating answers.

## Features

* Upload documents (PDF/TXT)
* Extract text from documents
* Ask questions based on document content
* Generate AI-based answers
* Store question-answer history
* Retrieve documents
* Delete documents and related history

## Tech Stack

* Python
* FastAPI
* MongoDB
* PyMongo / Motor
* Uvicorn
* LLM API (Groq)
* Pydantic

## Project Structure

```
app/
│
├── main.py                 # FastAPI application entry point
│
├── core/
│   └── config.py           # Environment configuration
│
├── routes/
│   ├── documents.py        # Document APIs
│   └── qa.py              # Question answering APIs
│
├── services/
│   ├── document_service.py # Document processing logic
│   └── llm_service.py      # LLM response generation
│
├── database.py             # MongoDB connection
│
└── models/
    └── document.py         # Data models
```

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
```

### 2. Create virtual environment

```bash
python -m venv venv
```

Activate environment:

Windows:

```bash
venv\Scripts\activate
```
### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file:

```
MONGO_URL

LLM_API_KEY
```
## Run Application

Start the server:

```bash
uvicorn app.main:app --reload
```

API will run at:

```
http://127.0.0.1:8000
```

Swagger documentation:

```
http://127.0.0.1:8000/docs
```

---

# API Endpoints

## Upload Document

### POST

```
/documents/upload
```
Uploads PDF or TXT documents.
## Ask Question

### POST

```
/qa/{document_id}
```

Example request:

```json
{
  "question": "What is this document about?"
}
```
## Get Documents

### GET

```
/documents
```
Returns all uploaded documents.

## Delete Document
### DELETE

```
/documents/{document_id}
```
Deletes:

* Document data
* Related question-answer history
Example:

```
DELETE /documents/665abc123
```
Response:
```json
{
  "message": "Document and its history deleted successfully"
}
```

## Database Collections
### documents
Stores uploaded document details.
Example:

```json
{
 "filename": "sample.pdf",
 "text": "document content",
 "uploaded_at": "date"
}
```

### history
Stores Q&A conversation history.

Example:

```json
{
 "document_id": "document_id",
 "question": "question",
 "answer": "response"
}
```

## Error Handling
The API returns proper HTTP status codes:

* 200 → Success
* 400 → Bad Request
* 404 → Not Found
* 500 → Server Error

## Future Improvements

* User authentication
* Multiple file formats
* Vector database integration
* Better document search
* Chat history management
