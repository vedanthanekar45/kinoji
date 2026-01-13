from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from typing import List, Optional
from sqlalchemy.orm import Session
from pydantic import BaseModel

# Backend imports
from server.search_and_filter import search_and_filter
from server.dashboard import top_row, format_time, avg_runtime_per_year, avg_rating_per_decade, movies_per_year, top_genres_movies, top_genres_rating, countries_by_movies
from server import db as database
from server.llm import get_insight, InsightRequest

load_dotenv()

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class InsightRequest(BaseModel):
    query: str


@app.get("/")
async def root():
    return {"message": "Welcome to Kinoji, an interesting place keep your cinema fantasies alive."}

@app.get("/search")
def search_filter_endpoint(
    title: Optional[str] = None,
    genres: Optional[List[str]] = Query(default=None),
    min_rating: Optional[float] = None,
    year: Optional[int] = None,
    db: Session = Depends(database.get_db)
):
    results = search_and_filter(db, title=title, genres=genres, min_rating=min_rating, year=year)
    return results


# -- Dashboard Endpoints --

@app.get("/dashboard/top-row")
def get_top_row_stats (db: Session = Depends(database.get_db)):
    stats, oldest = top_row(db)
    data = {
        "library_size": stats.total_movies,
        "total_watch_time": format_time(stats.total_runtime),
        "global_rating": round(stats.avg_movie_rating, 2) if stats.avg_movie_rating else 0.0,
        "oldest_movie": {
            "title": oldest.name if oldest else "Unknown",
            "year": oldest.release.year if oldest else 0,
            "date": str(oldest.release) if oldest else None
        }
    }
    return data

@app.get("/dashboard/avg-runtime-year")
def runtime_per_year(db: Session = Depends(database.get_db)):
    stats = avg_runtime_per_year(db)
    data = [
        {
            "year": row.year,
            "runtime": round(row.avg_runtime, 2),
        }
        for row in stats
    ]
    return data

@app.get("/dashboard/avg-rating-decade")
def rating_per_decade(db: Session = Depends(database.get_db)):
    stats = avg_rating_per_decade(db)
    data = [
        {
            "decade": int(row.decade),
            "runtime": round(row.avg_rating, 2),
            "movies": row.count
        }
        for row in stats
    ]
    return data

@app.get('/dashboard/movies-per-year')
def movies_per_year_count(db: Session = Depends(database.get_db)):
    stats = movies_per_year(db)
    data = [
        {
            "year": row.year,
            "count": row.count
        }
        for row in stats
    ]
    return data

@app.get('/dashboard/top_genres_by_movies')
def top_genres_by_movies(db: Session = Depends(database.get_db)):
    stats = top_genres_movies(db)
    data = [
        {
            "genre": row.genre,
            "count": row.total_movies,
        }
        for row in stats
    ]
    return data

@app.get('/dashboard/top_genres_by_rating')
def top_genres_by_rating(db: Session = Depends(database.get_db)):
    stats = top_genres_rating(db)
    data = [
        {
            "genre": row.genre,
            "average_rating": row.avg_rating,
        }
        for row in stats
    ]
    return data

@app.get("/dashboard/top_countries_by_movies")
def get_top_countries_by_movies(db: Session = Depends(database.get_db)):
    stats = countries_by_movies(db)
    data = [
        {
            "country": row.country,
            "count": row.total_movies,
        }
        for row in stats
    ]
    return data



'''
Below this, contains all the stuff I'm gonna do with AI,
So if you're looking for something else, go up.
'''

@app.post("/generate/insight")
def get_ai_insight(request: InsightRequest):
    result = get_insight(request)
    return result