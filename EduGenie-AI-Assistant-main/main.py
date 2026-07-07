import os
import json
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from typing import List
from google import genai
from google.genai import types

# Load GEMINI_API_KEY from .env file if present
if os.path.exists(".env"):
    with open(".env", "r") as f:
        for line in f:
            if "=" in line and not line.strip().startswith("#"):
                key, val = line.strip().split("=", 1)
                if key.strip() == "GEMINI_API_KEY":
                    os.environ["GEMINI_API_KEY"] = val.strip().strip('"').strip("'")

app = FastAPI(
    title="EduGenie MVP",
    description="Intelligent Educational Assistant powered by Gemini 2.5 Flash"
)

# Set up templates
templates = Jinja2Templates(directory="templates")

# Helper to get GenAI Client
def get_client() -> genai.Client:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="GEMINI_API_KEY environment variable is not set. Please set it to proceed."
        )
    try:
        # genai.Client accepts api_key directly or reads GEMINI_API_KEY automatically
        return genai.Client(api_key=api_key)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to initialize Gemini Client: {str(e)}"
        )

# Request Models
class ExplainRequest(BaseModel):
    text: str
    level: str

class QuizRequest(BaseModel):
    topic: str

class SummarizeRequest(BaseModel):
    text: str
    length: str
    format: str

# Pydantic schemas for Structured Output in Quiz
class QuizQuestion(BaseModel):
    question: str = Field(description="The multiple choice question text")
    options: List[str] = Field(description="Exactly 4 multiple choice options")
    correct_answer: str = Field(description="The correct option which MUST be exactly one of the options in the options list")

class QuizResponse(BaseModel):
    questions: List[QuizQuestion] = Field(description="A list of exactly 3 multiple choice questions")

# Endpoints
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/api/explain")
async def explain_concept(request: ExplainRequest):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return {
            "explanation": (
                f"### 🧪 EduGenie Demo Mode (No API Key Configured)\n\n"
                f"Here is a demonstration explanation for **{request.text}** at the **{request.level.upper()}** level:\n\n"
                f"#### What is {request.text}?\n"
                f"Since no `GEMINI_API_KEY` was found in the environment, EduGenie is running in **Demo Mode**. "
                f"Usually, this topic would be analyzed in real-time by the `gemini-2.5-flash` model, using prompt instructions tailored for the {request.level} learning level.\n\n"
                f"#### Core Analogies & Concepts\n"
                f"- **Concept Breakdown**: For a {request.level} audience, we explain '{request.text}' using simple, relatable terms and structured key points.\n"
                f"- **Real-world connection**: We draw connections between abstract topics and everyday observations.\n\n"
                f"> [!TIP]\n"
                f"> **To enable live Gemini generation**, stop the server, set your `GEMINI_API_KEY` environment variable, and restart: \n"
                f"> `set GEMINI_API_KEY=your_api_key_here` (CMD) or `$env:GEMINI_API_KEY=\"your_api_key_here\"` (PowerShell)."
            )
        }

    client = get_client()
    
    # Prompt engineering based on explanation level
    level_guidance = {
        "child": "Explain it like I am 5 years old. Use very simple terms, analogies, stories, and emoji. Keep it extremely simple and engaging.",
        "teenager": "Explain it like I am a high school student. Keep it clear, relate it to everyday concepts, and use a friendly, conversational tone.",
        "college": "Explain it like a college professor teaching an introductory course. Use precise terms and cover core theoretical details clearly.",
        "expert": "Provide a high-level expert summary, discussing technical mechanics, nuances, and advanced research or applications. No hand-waving."
    }
    
    guidance = level_guidance.get(request.level, "Explain it clearly and concisely.")
    
    prompt = (
        f"You are an elite educational AI assistant named EduGenie.\n"
        f"Target Concept/Topic: {request.text}\n"
        f"Explanation Level/Audience: {request.level.upper()} level.\n"
        f"Instructions: {guidance}\n\n"
        f"Format your response using clean Markdown with clear headings (using ##, ###), bold text, bullet points, and code blocks if appropriate."
    )
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return {"explanation": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini API Error: {str(e)}")

@app.post("/api/quiz", response_model=QuizResponse)
async def generate_quiz(request: QuizRequest):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return {
            "questions": [
                {
                    "question": f"Which of the following is the most primary concept associated with '{request.topic}'?",
                    "options": [
                        "The fundamental governing law or principle",
                        "A secondary minor component",
                        "An unrelated historical event",
                        "A hypothetical calculation model"
                    ],
                    "correct_answer": "The fundamental governing law or principle"
                },
                {
                    "question": f"In a standard learning module for '{request.topic}', what is the main goal?",
                    "options": [
                        "To memorize terms without context",
                        "To gain intuitive understanding and core problem-solving skills",
                        "To avoid any practical application",
                        "To write long-winded descriptions"
                    ],
                    "correct_answer": "To gain intuitive understanding and core problem-solving skills"
                },
                {
                    "question": f"Why is it beneficial to learn about '{request.topic}'?",
                    "options": [
                        "It expands our knowledge of natural systems and technologies",
                        "It makes our tests harder",
                        "It is a required class with no other value",
                        "It has been fully resolved and requires no active development"
                    ],
                    "correct_answer": "It expands our knowledge of natural systems and technologies"
                }
            ]
        }

    client = get_client()
    
    prompt = (
        f"You are an educational assessment creator. Generate a 3-question multiple choice quiz on the topic: '{request.topic}'.\n"
        f"For each question, provide exactly 4 options and clearly identify the correct option (which must match one of the options verbatim)."
    )
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=QuizResponse,
                temperature=0.7,
            )
        )
        # Parse the JSON response
        quiz_data = json.loads(response.text)
        return quiz_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate quiz: {str(e)}")

@app.post("/api/summarize")
async def summarize_text(request: SummarizeRequest):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        bullets_content = (
            f"### 📝 EduGenie Demo Summary (No API Key Configured)\n\n"
            f"Here is a demonstration summary of your text in a **{request.format}** format (Detail level: **{request.length}**):\n\n"
            f"- **Main Theme**: The provided text centers on key themes, definitions, and applications related to your study material.\n"
            f"- **Primary Takeaway**: Processing educational text into structured notes helps maximize memory retention.\n"
            f"- **Important Detail**: This is a template summary designed to verify frontend markdown parsing.\n\n"
            f"*Configure your `GEMINI_API_KEY` to run live summarizations with Gemini 2.5 Flash.*"
        )
        
        para_content = (
            f"### 📝 EduGenie Demo Summary (No API Key Configured)\n\n"
            f"This summary demonstrates the **paragraph** output format with a **{request.length}** level of detail. "
            f"In a production environment, the `gemini-2.5-flash` model will read the full context of the source text "
            f"({len(request.text)} characters long) and compress the narrative according to the requested length and format. "
            f"The parsed output is rendered instantly with markdown formatting and styling. "
            f"Please configure the `GEMINI_API_KEY` environment variable to enable live summaries."
        )
        
        return {"summary": bullets_content if request.format == "bullets" else para_content}

    client = get_client()
    
    format_instruction = "bulleted key takeaways (using Markdown bullets)" if request.format == "bullets" else "a cohesive narrative paragraph"
    length_instruction = "a brief, high-level overview (under 150 words)" if request.length == "short" else "a detailed, comprehensive summary covering key sub-concepts"
    
    prompt = (
        f"You are EduGenie, an expert summarizer. Summarize the following educational text.\n"
        f"Length: {length_instruction}.\n"
        f"Format: {format_instruction}.\n\n"
        f"Text to summarize:\n{request.text}"
    )
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return {"summary": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini API Error: {str(e)}")
