import os
import enum
from dotenv import load_dotenv
from sqlalchemy import ForeignKey, Integer, BigInteger, String, Date, Column, create_engine
from sqlalchemy.types import Enum
from sqlalchemy.orm import DeclarativeBase, relationship, sessionmaker

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

if DATABASE_URL is None:
    raise ValueError("DATABASE_URL environment variable not set")

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
    runtime_minutes = Column(Integer)
    budget = Column(BigInteger)
    revenue = Column(BigInteger)
    cast = relationship("Actor", secondary="movie_actors", back_populates="movies")
    directors = relationship("Director", secondary="movie_directors", back_populates="movies")
    genres = relationship("Genre", secondary="movie_genres", back_populates="movies")
    countries = relationship("Country", secondary="movie_countries", back_populates="movies")



class Actor(Base):
    __tablename__ = "actors"

    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    gender = Column(Enum(Genders), nullable=False)
    movies = relationship("MovieData", secondary="movie_actors", back_populates="cast")

class MoviesAndActors(Base):
    __tablename__ = "movie_actors"
    movie_id = Column(ForeignKey("movies.id"), primary_key=True)
    actor_id = Column(ForeignKey("actors.id"), primary_key=True)



class Director(Base):
    __tablename__ = "directors"
    id = Column(Integer, primary_key=True)
    name = Column(String(200), unique=True, nullable=False)
    gender = Column(Enum(Genders), nullable=False)
    movies = relationship("MovieData", secondary="movie_directors", back_populates="directors")

class MovieDirector(Base):
    __tablename__ = 'movie_directors'
    movie_id = Column(Integer, ForeignKey('movies.id'), primary_key=True)
    director_id = Column(Integer, ForeignKey('directors.id'), primary_key=True)



class Country(Base):
    __tablename__ = "countries"
    id = Column(Integer, primary_key=True)
    country_name = Column(String(100), unique=True, nullable=False)
    movies = relationship("MovieData", secondary="movie_countries", back_populates="countries")

class MovieCountry(Base):
    __tablename__ = 'movie_countries'
    movie_id = Column(Integer, ForeignKey('movies.id'), primary_key=True)
    country_id = Column(Integer, ForeignKey('countries.id'), primary_key=True)



class Genre(Base):
    __tablename__ = "genres"
    id = Column(Integer, primary_key=True)
    genre_name = Column(String(100), unique=True, nullable=False)
    movies = relationship("MovieData", secondary="movie_genres", back_populates="genres")

class MovieGenres(Base):
    __tablename__ = 'movie_genres'
    movie_id = Column(Integer, ForeignKey('movies.id'), primary_key=True)
    genre_id = Column(Integer, ForeignKey('genres.id'), primary_key=True)


# --- CREATE ENGINE ---
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_db_tables():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    print("Creating database tables...")
    create_db_tables()
    print("Tables created successfully.")