import os
import re
import sys
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func, extract, and_
from db.movie_models import MovieData, Genre, MovieGenres

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def search_and_filter (db: Session, title: str=None, genres: List = None, min_rating: float=None, year: int=None, limit: int=20):
    '''
    Searches the dataset or the dataset, and returns the results, no rocket science.
    Oh, and also applies some filters.
    '''

    query = db.query(MovieData)

    if title:
        clean_input = re.sub(r'[^a-zA-Z0-9]', '', title)
        query = query.filter(
            func.regexp_replace(MovieData.name, '[^a-zA-Z0-9]', '', 'g')
            .ilike(f"%{clean_input}%")
        )
    if genres:
        # Subquery to find movies that have ALL the requested genres
        for genre in genres:
            genre_subquery = (
                db.query(MovieGenres.movie_id)
                .join(Genre, MovieGenres.genre_id == Genre.id)
                .filter(func.lower(Genre.genre_name) == genre.lower())
            )
            query = query.filter(MovieData.id.in_(genre_subquery))
    if min_rating:
        query = query.filter(MovieData.rating >= min_rating)
    if year:
        query = query.filter(extract('year', MovieData.release) == year)
    
    query = query.order_by(MovieData.rating.desc())

    return query.limit(limit).all()