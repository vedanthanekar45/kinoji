import os
import sys
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from db.movie_models import MovieData

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

'''
This file contains all the endpoints I need for the main dashboard
'''

# This one is a basic eendpoint showing the basic stats of the dataset..
def top_row(db: Session):
    stats = db.query(
        func.count(MovieData.id).label("total_movies"),
        func.sum(MovieData.runtime_minutes).label("total_runtime"),
        func.avg(MovieData.rating).label("avg_movie_rating")
    ).first()

    oldest_movie = db.query(MovieData).filter(MovieData.release != None).order_by(MovieData.release.asc()).first()
    return stats, oldest_movie