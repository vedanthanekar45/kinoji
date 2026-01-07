import os
import sys
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from db.movie_models import MovieData

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))