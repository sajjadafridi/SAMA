from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# Allow CORS for frontend if needed (optional)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust to your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount React static files
app.mount("/static", StaticFiles(directory="frontend/build/static"), name="static")

# Serve chatbot API
@app.post("/api/chat")
async def chat(request: Request):
    body = await request.json()
    user_input = body.get("message", "")

    # Your chatbot logic here (mock response for now)
    response = f"Hi! You said: {user_input}"
    return JSONResponse(content={"response": response})

# Serve React app for all other routes
@app.get("/{full_path:path}")
async def serve_react_app():
    file_path = "frontend/build/index.html"
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return JSONResponse(status_code=404, content={"error": "React app not found"})