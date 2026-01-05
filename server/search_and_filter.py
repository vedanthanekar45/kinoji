import os
import re
import sys
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from db.movie_models import MovieData, Genre

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
        query = query.join(MovieData.genres)
        query = query.filter(func.lower(Genre.genre_name).in_([g.lower() for g in genres]))
        query = query.group_by(MovieData.id)
        query = query.having(func.count(MovieData.id) == len(genres))
    if min_rating:
        query = query.filter(MovieData.rating_out_of_five >= min_rating)
    if year:
        query = query.filter(extract('year', MovieData.release) == year)
    
    query = query.order_by(MovieData.rating_out_of_five.desc())

    return query.limit(limit).all()