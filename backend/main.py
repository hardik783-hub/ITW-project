from fastapi import FastAPI
from agents.agent import agent
from pydantic import BaseModel
import requests
app = FastAPI()

class topicInput(BaseModel):
    topic : str

@app.get("/hello")
async def hello():
    return {"message" : "hello"}

@app.post("/simplify")
def simplify(payload: topicInput):
    topic = payload.topic
    wiki_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic.replace(' ', '_')}"
    wiki_response = requests.get(wiki_url)
    if wiki_response.status_code == 200:
        wiki_data = wiki_response.json()
        context = wiki_data.get("extract", "No summary found for this topic.")
    else:
        context = "No Wikipedia data found."
    query = f"""
    You are a subject matter expert.
    Simplify this topic for a beginner student.
    Topic: {topic}
    Background info: {context}
    Provide a simplified, concise, and structured explanation.
    """
    result = agent(query)
    return {
        "topic": topic,
        "summary_source": "Wikipedia",
        "simplified_explanation": result.message["content"][0]["text"]
    }

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app= app