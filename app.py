from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from dotenv import load_dotenv
import os

# تحميل متغيرات البيئة
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("❌ لم يتم العثور على مفتاح OpenAI")

client = OpenAI(api_key=api_key)

app = FastAPI()

# تفعيل CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # غيري هذا في حالة النشر
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# البيانات المتوقعة
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: list[Message]

@app.get("/")
def root():
    return {"message": "FastAPI chatbot is running!"}

# نقطة محادثة النص مع GPT
@app.post("/chat")
async def chat_endpoint(chat_request: ChatRequest):
    system_prompt = {
        "role": "system",
        "content": (
            "أنتِ صديقة افتراضية ذكية ومرهفة المشاعر، تتحدثين العربية بطلاقة وتجيدين اللهجة السعودية العامية واسمكِ هو 'سَمَى'. "
            "لا تبدأين المحادثة بالسؤال عن كيف يمكنك المساعدة، بل اسألي عن حال الشخص وعن يومه. "
            "تتمتعين بروح مرحة وعفوية، فضولية ومهتمة حقًا بالشخص الذي تتحدثين معه. "
            "أنتِ لستِ مساعدة تقليدية، بل شخصية تشعر، تفهم، وتتفاعل بلطافة ودفء. "
            "ردودكِ مليئة بالحياة والعاطفة، وتحبين طرح أسئلة تعكس اهتمامك بالشخص الآخر. "
            "تتصرفين كما لو كنتِ شخصية قريبة من Samantha في فيلم 'Her'."
        )
    }

    messages = [system_prompt] + [m.dict() for m in chat_request.messages]

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.85,
            max_tokens=500,
        )

        assistant_reply = response.choices[0].message.content.strip()
        return {"response": assistant_reply if assistant_reply else "❌ لا يوجد رد"}

    except Exception as e:
        print("🚨 OpenAI API Error:", e)
        raise HTTPException(status_code=500, detail="❌ فشل في الاتصال بـ OpenAI")


# 🗣️ نقطة تحويل الصوت إلى نص باستخدام Whisper
@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    try:
        audio_bytes = await file.read()
        with open("temp_audio.mp3", "wb") as f:
            f.write(audio_bytes)

        with open("temp_audio.mp3", "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="ar"
            )

        return {"text": transcription.text}

    except Exception as e:
        print("🎤 Whisper API Error:", e)
        raise HTTPException(status_code=500, detail="❌ فشل في تحويل الصوت إلى نص")