from typing import List

from pydantic import BaseModel, Field


class TextRequest(BaseModel):
    text: str = Field(..., min_length=1)


class ExplanationRequest(BaseModel):
    topic: str = Field(..., min_length=1)
    level: str = "beginner"


class QuizRequest(BaseModel):
    topic: str = Field(..., min_length=1)
    number_of_questions: int = Field(
        default=5,
        ge=1,
        le=20
    )
    level: str = "beginner"


class SummaryRequest(BaseModel):
    text: str = Field(..., min_length=1)
    number_of_sentences: int = Field(
        default=5,
        ge=1,
        le=15
    )


class LearningPathRequest(BaseModel):
    topic: str = Field(..., min_length=1)
    weeks: int = Field(
        default=4,
        ge=1,
        le=12
    )
    level: str = "beginner"


class TextResponse(BaseModel):
    result: str


class QuizQuestion(BaseModel):
    question: str
    options: List[str]
    answer: str
    explanation: str


class GeneratedQuiz(BaseModel):
    title: str
    questions: List[QuizQuestion]


class LearningWeek(BaseModel):
    week: int
    topic: str
    goals: List[str]
    activities: List[str]
    resource_types: List[str]


class LearningPath(BaseModel):
    title: str
    overview: str
    weeks: List[LearningWeek]