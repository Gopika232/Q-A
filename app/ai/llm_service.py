from groq import Groq
from app.core.config import settings

client=Groq(api_key=settings.LLM_API_KEY)

def generate_answer(context,question):
    prompt=f"""
    Answer the question using the document content.
    Document:
    {context}

    Question:
    {question}
    """

    response=client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
            "role":"user",
            "content":prompt
            }
        ]
    )
    return response.choices[0].message.content