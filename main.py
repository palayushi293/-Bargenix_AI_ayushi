from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
from dotenv import load_dotenv
from groq import Groq  # type: ignore # ✅ Official Groq SDK

load_dotenv("enviro.env")
GROQ_API_KEY = os.getenv("GROQ_API")

app = FastAPI()
templates = Jinja2Templates(directory="templates")

client = Groq(api_key=GROQ_API_KEY)

system_prompt = {
    "role": "system",
    "content": (
        "You are a helpful, professional career counselor. "
        "You provide detailed career advice to students and working professionals. "
        "Only answer career-related questions with accuracy and empathy."
    )
}

@app.get("/", response_class=HTMLResponse)
async def get_chat(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "response": ""})

@app.post("/", response_class=HTMLResponse)
async def post_chat(request: Request, message: str = Form(...)):
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                system_prompt,
                {"role": "user", "content": message}
            ]
        )
        reply = response.choices[0].message.content
    except Exception as e:
        reply = f" Error: {str(e)}"

    return templates.TemplateResponse("index.html", {"request": request, "response": reply})
