from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from explanation_module import explain_topic
from learning_path import generate_learning_path
from qna import answer_question
from quiz_module import generate_quiz
from schemas import (
    ExplanationRequest,
    LearningPathRequest,
    QuizRequest,
    SummaryRequest,
    TextRequest,
    TextResponse,
)
from summary_module import summarize_text


BASE_DIR = Path(__file__).resolve().parent


app = FastAPI(
    title="EduGenie",
    description="AI Powered Learning Assistant",
    version="1.0.0"
)


# ==========================================
# STATIC FILES
# ==========================================

app.mount(
    "/static",
    StaticFiles(
        directory=BASE_DIR / "static"
    ),
    name="static"
)


templates = Jinja2Templates(
    directory=BASE_DIR / "templates"
)


# ==========================================
# HOME
# ==========================================

@app.get(
    "/",
    response_class=HTMLResponse
)
async def home(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


# ==========================================
# HEALTH
# ==========================================

@app.get("/health")
async def health():

    return {
        "status": "ok",
        "application": "EduGenie"
    }


# ==========================================
# QUESTION ANSWER
# ==========================================

@app.post(
    "/qa",
    response_model=TextResponse
)
async def qa(
    request: TextRequest
):

    result = answer_question(
        request.text
    )

    return TextResponse(
        result=result
    )


# ==========================================
# EXPLAIN
# ==========================================

@app.post(
    "/explain",
    response_model=TextResponse
)
async def explain(
    request: ExplanationRequest
):

    result = explain_topic(
        topic=request.topic,
        level=request.level
    )

    return TextResponse(
        result=result
    )


# ==========================================
# QUIZ
# ==========================================

@app.post("/quiz")
async def quiz(
    request: QuizRequest
):

    result = generate_quiz(

        topic=request.topic,

        number_of_questions=
            request.number_of_questions,

        level=request.level

    )

    return result


# ==========================================
# SUMMARY
# ==========================================

@app.post(
    "/summarize",
    response_model=TextResponse
)
async def summarize(
    request: SummaryRequest
):

    result = summarize_text(

        text=request.text,

        number_of_sentences=
            request.number_of_sentences

    )

    return TextResponse(
        result=result
    )


# ==========================================
# LEARNING RECOMMENDATIONS
# ==========================================

@app.post(
    "/learn/recommendations"
)
async def learning_recommendations(
    request: LearningPathRequest
):

    result = generate_learning_path(

        topic=request.topic,

        weeks=request.weeks,

        level=request.level

    )

    return result