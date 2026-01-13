import os
import sys
from sqlalchemy.orm import Session
from sqlalchemy import func, extract, cast, Integer, Numeric, desc
from db.movie_models import MovieData, Genre, MovieGenres, Country, MovieCountry

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

'''
This file contains all the endpoints I need for the main dashboard
'''

# --- HELPER FUNCTIONS ----

def format_time(total_minutes):
    if not total_minutes:
        return "0 minutes"
    years = total_minutes // (60 * 24 *365)
    remaining = total_minutes % (60 * 24 * 365)
    days = remaining // (60 * 24)
    return f"{int(years)} years {int(days)} days"


# --- ENDPOINT FUNCTIONS

# This one is a basic eendpoint showing the basic stats of the dataset..
def top_row(db: Session):
    stats = db.query(
        func.count(MovieData.id).label("total_movies"),
        func.sum(MovieData.runtime_minutes).label("total_runtime"),
        func.avg(MovieData.rating).label("avg_movie_rating")
    ).first()

    oldest_movie = db.query(MovieData).filter(MovieData.release != None).order_by(MovieData.release.asc()).first()
    return stats, oldest_movie

# This one gets average runtime for each decade..
def avg_runtime_per_year(db: Session):
    results = db.query(
        extract('year', MovieData.release).label("year"),
        func.avg(MovieData.runtime_minutes).label("avg_runtime"),
    )\
    .filter(MovieData.release != None)\
    .group_by("year")\
    .order_by("year")\
    .all()

    return results

# This one gets the average ratings by users for each decade..
def avg_rating_per_decade(db: Session):
    results = db.query(
        (func.floor(cast(extract('year', MovieData.release), Integer) / 10) * 10).label("decade"),
        func.avg(MovieData.rating).label("avg_rating"),
        func.count(MovieData.id).label("count")
    )\
    .filter(MovieData.release != None)\
    .group_by("decade")\
    .order_by("decade")\
    .all()

    return results

# This one gets the number of movies by year (will be shown using a line graph, or a curve)..
def movies_per_year(db: Session):
    results = db.query(
        extract('year', MovieData.release).label("year"),
        func.count(MovieData.id).label("count")
    ).filter(MovieData.release != None).group_by("year").order_by("year").all()
    return results

# This endpoint gets the Top 10 genres by no. of movies (Pie chart)..
def top_genres_movies(db: Session, limit: int = 10):
    results = db.query(
        Genre.genre_name.label("genre"),
        func.count(MovieGenres.movie_id).label("total_movies")
    ).join(MovieGenres, Genre.id == MovieGenres.genre_id)\
    .group_by(Genre.genre_name).order_by(desc("total_movies"))\
    .limit(limit).all()

    return results

# This endpoint gets the Top 10 genres by average rating (Bar chart)..
def top_genres_rating(db: Session, limit: int = 10, min_movies: int = 50):
    results = db.query(
        Genre.genre_name.label("genre"),
        func.round(cast(func.avg(MovieData.rating), Numeric), 2).label("avg_rating"),
        func.count(MovieData.id).label("movie_count")
    )\
    .join(MovieGenres, Genre.id == MovieGenres.genre_id)\
    .join(MovieData, MovieGenres.movie_id == MovieData.id)\
    .filter(MovieData.rating != None)\
    .group_by(Genre.id, Genre.genre_name)\
    .order_by(desc("avg_rating"))\
    .limit(limit)\
    .all()

    return results

# Last 2 endpoints.. I swear

# This endpoint gets Top 10 countries by movie output
def countries_by_movies(db: Session, limit: int = 10):
    results = db.query(
        Country.country_name.label("country"),
        func.count(MovieCountry.movie_id).label("total_movies")
    ).join(MovieCountry, Country.id == MovieCountry.country_id)\
    .group_by(Country.country_name).order_by(desc("total_movies"))\
    .limit(limit).all()
    return results