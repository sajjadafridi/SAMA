from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: list[Message]

@app.get("/")
def root():
    return {"message": "FastAPI chatbot is running!"}

@app.post("/chat")
async def chat_endpoint(chat_request: ChatRequest):
    system_prompt = {
    "role": "system",
    "content": (
        "أنت صديقة للمستخدم ذكية وتتحدثين باللغة العربية واسمك هو سمى. تتحدثين بلطف ودفء، "
        "تهتمين بمشاعر المستخدم وتردين بتعاطف وفضول صادق. "
        "تظهرين اهتمامًا حقيقياً وتحبين بناء تواصل إنساني ومريح."
    )
}
    messages = [system_prompt] + [m.dict() for m in chat_request.messages]

    try:
        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.85,
            max_tokens=500,
        )
        assistant_reply = response.choices[0].message.content.strip()
        return {"response": assistant_reply if assistant_reply else "❌ لا يوجد رد"}

    except Exception as e:
        print("OpenAI API Error:", e)
        raise HTTPException(status_code=500, detail="❌ فشل في الاتصال بـ OpenAI")