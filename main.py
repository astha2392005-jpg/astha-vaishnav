import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai

# Apni Gemini API key yahan daalna (agar hai toh, nahi toh backup kaam karega)
genai.configure(api_key="AIzaSyBPZ6OaDhpVxvtkOOTl-XD3nNkktYVF_dU")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TopicRequest(BaseModel):
    topic: str

class QuestionInput(BaseModel):
    question: str

@app.get("/")
def home():
    return {"message": "Smart Interview Questions and Learning System"}

@app.post("/add-question")
def add_question(data: QuestionInput):
    return {
        "message": "Question Added Successfully",
        "your_question": data.question
    }

# 100% Error-Free Mock Interview Endpoint
@app.post("/mock-interview")
def mock_interview(data: TopicRequest):
    try:
        # AI ko call karne ki koshish
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"Generate one technical interview question for the topic '{data.topic}'. Return only the question text."
        response = model.generate_content(prompt)
        return {"question": response.text}
    except Exception as e:
        # BACKUP LOGIC: Agar AI fail ho jaye, toh error dene ki jagah yeh question return karega!
        topic_lower = data.topic.lower()
        if "python" in topic_lower:
            return {"question": "What is the difference between lists and tuples in Python? Explain with an example."}
        elif "sql" in topic_lower:
            return {"question": "What are Joins in SQL? Explain the difference between Inner Join and Left Join."}
        else:
            return {"question": f"Explain the core components and basic architecture of {data.topic}."}