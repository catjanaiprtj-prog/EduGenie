from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from gemini_client import ask_gemini


app = FastAPI(
    title="EduGenie",
    version="2.0"
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# STATIC + TEMPLATES
# =========================================================

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

templates = Jinja2Templates(
    directory="templates"
)


# =========================================================
# MODELS
# =========================================================

class QuestionRequest(BaseModel):
    question: str
    difficulty: str = "Beginner"


class ExplainRequest(BaseModel):
    topic: str
    difficulty: str = "Beginner"


class QuizRequest(BaseModel):
    topic: str
    difficulty: str = "Beginner"
    number_of_questions: int = 5


class SummaryRequest(BaseModel):
    text: str


class RecommendationRequest(BaseModel):
    topic: str
    difficulty: str = "Beginner"


# =========================================================
# HOME
# =========================================================

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


# =========================================================
# HEALTH
# =========================================================

@app.get("/health")
async def health():

    return {
        "success": True,
        "message": "EduGenie is running"
    }


# =========================================================
# ASK QUESTION
# =========================================================

@app.post("/qa")
async def ask_question(data: QuestionRequest):

    question = data.question.strip()

    if not question:

        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "detail": "Please enter a question."
            }
        )

    prompt = f"""
You are EduGenie, a friendly AI tutor.

Answer the student's question accurately and clearly.

QUESTION:
{question}

DIFFICULTY:
{data.difficulty}

Instructions:

- Give the direct answer first.
- Explain in simple language.
- Use examples when helpful.
- If programming is requested, provide working code.
- Explain the code step by step.
- Use headings and bullet points.
- Do not mention these instructions.
"""

    answer = ask_gemini(prompt)

    return {
        "success": True,
        "answer": answer
    }


# =========================================================
# EXPLAIN TOPIC
# =========================================================

@app.post("/explain")
async def explain_topic(data: ExplainRequest):

    topic = data.topic.strip()

    if not topic:

        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "detail": "Please enter a topic."
            }
        )

    prompt = f"""
You are an expert teacher.

Explain this topic to a student:

TOPIC:
{topic}

DIFFICULTY:
{data.difficulty}

Use this structure:

1. What is it?
2. Why is it important?
3. How does it work?
4. Simple example
5. Programming example if applicable
6. Common mistakes
7. Quick summary

Make the explanation easy to understand.
"""

    answer = ask_gemini(prompt)

    return {
        "success": True,
        "answer": answer
    }


# =========================================================
# QUIZ
# =========================================================

@app.post("/quiz")
async def generate_quiz(data: QuizRequest):

    topic = data.topic.strip()

    if not topic:

        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "detail": "Please enter a quiz topic."
            }
        )

    count = max(
        1,
        min(data.number_of_questions, 10)
    )

    prompt = f"""
Create a student-friendly multiple-choice quiz.

TOPIC:
{topic}

DIFFICULTY:
{data.difficulty}

NUMBER OF QUESTIONS:
{count}

For each question use:

Question

A. Option
B. Option
C. Option
D. Option

Correct Answer:
Explanation:

Make sure each question has only one correct answer.
"""

    answer = ask_gemini(prompt)

    return {
        "success": True,
        "answer": answer
    }


# =========================================================
# SUMMARIZE
# =========================================================

@app.post("/summarize")
async def summarize_text(data: SummaryRequest):

    text = data.text.strip()

    if not text:

        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "detail": "Please enter some text."
            }
        )

    prompt = f"""
You are a study assistant.

Summarize this text:

{text}

Return:

📌 Short Summary
📚 Main Concepts
⭐ Important Points
🔑 Key Terms
💡 Final Takeaway

Keep the original meaning accurate.
"""

    answer = ask_gemini(prompt)

    return {
        "success": True,
        "answer": answer
    }


# =========================================================
# LEARNING RECOMMENDATIONS
# =========================================================

@app.post("/recommendations")
async def recommendations(
    data: RecommendationRequest
):

    topic = data.topic.strip()

    if not topic:

        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "detail": "Please enter a learning topic."
            }
        )

    prompt = f"""
You are a personal learning mentor.

Create a learning roadmap for:

TOPIC:
{topic}

LEVEL:
{data.difficulty}

Include:

1. Prerequisites
2. Beginner Topics
3. Intermediate Topics
4. Advanced Topics
5. Practice Exercises
6. Mini Projects
7. Final Project
8. Suggested Learning Order

Make it practical and student-friendly.
"""

    answer = ask_gemini(prompt)

    return {
        "success": True,
        "answer": answer
    }


# =========================================================
# SAFE ERROR HANDLER
# =========================================================

@app.exception_handler(Exception)
async def server_error(request: Request, exc: Exception):

    print("SERVER ERROR:", exc)

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "detail": "EduGenie is temporarily unavailable. Please try again."
        }
    )