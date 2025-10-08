import enum
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey, Integer, BigInteger, String, Date, Column
from sqlalchemy.types import Enum
from sqlalchemy.orm import DeclarativeBase

## --- ENUM TYPES ---


""" This class is defined to provide he options for Enum type used in the 
    Gender column of the Actors table """
class Genders(enum.Enum):
    M = "Male"
    F = "Female"
    N = "Non-binary"


# BASE CLASS
class Base(DeclarativeBase):
    pass

# --- PRIMARY TABLES ---
class MovieData(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    release = Column(Date)
    director = Column(String(100))
    budget = Column(BigInteger)
    box_office = Column(BigInteger)


class ActorData(Base):
    __tablename__ = "actors"

    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    gender = Column(Enum(Genders), nullable=False)


class MoviesAndActors(Base):
    __tablename__ = "movies_actors"

    movie_id = Column(ForeignKey("movies.id"))
    actor_id = Column(ForeignKey("actors.id"))
