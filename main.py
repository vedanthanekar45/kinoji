from fastapi import FastAPI, Depends
import os
from huggingface_hub import AsyncInferenceClient
from dotenv import load_dotenv
from typing import List, Optional
from sqlalchemy.orm import Session

# Backend imports
from server.search_and_filter import search_and_filter
from server import db as database

load_dotenv()

app = FastAPI()

@app.get("/search")

def search_filter_endpoint(
    title: Optional[str] = None,
    genres: Optional[List[str]] = None,
    min_rating: Optional[float] = None,
    year: Optional[int] = None,
    db: Session = Depends(database.get_db)
):
    results = search_and_filter(db, title=title, genres=genres, min_rating=min_rating, year=year)
    return results
    

'''
Below this, contains all the stuff I'm gonna do with AI,
So if you're looking for something else, go up.
'''
client = AsyncInferenceClient(
    api_key=os.getenv("HF_TOKEN"),
)
model = "meta-llama/Llama-3.1-8B-Instruct"


@app.get("/")
async def root():
    return {"message": "Welcome to Kinoji, an interesting place keep your cinema fantasies alive."}

@app.get ("/insights")
async def getInsights():
    result = await client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": "Hello, how are you doing? I'll be using you for a data science project I'm working now, are you ready?"
            }
        ]
    )
    return result.choices[0].message.content