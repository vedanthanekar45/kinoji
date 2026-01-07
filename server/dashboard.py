import os
import sys
from sqlalchemy.orm import Session
from sqlalchemy import func, extract, cast, Integer
from db.movie_models import MovieData

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
        func.avg(MovieData.rating_out_of_five).label("avg_movie_rating")
    ).first()

    oldest_movie = db.query(MovieData).filter(MovieData.release != None).order_by(MovieData.release.asc()).first()
    return stats, oldest_movie

# This one gets average runtime for each decade..
def avg_runtime_per_decade(db: Session):
    results = db.query(
        (func.floor(cast(extract('year', MovieData.release), Integer) / 10) * 10).label("decade"),
        func.avg(MovieData.runtime_minutes).label("avg_runtime"),
        func.count(MovieData.id).label("count")
    )\
    .filter(MovieData.release != None)\
    .group_by("decade")\
    .order_by("decade")\
    .all()

    return results

# This one gets the average ratings by users for each decade..
def avg_rating_per_decade(db: Session):
    results = db.query(
        (func.floor(cast(extract('year', MovieData.release), Integer) / 10) * 10).label("decade"),
        func.avg(MovieData.rating_out_of_five).label("avg_rating"),
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