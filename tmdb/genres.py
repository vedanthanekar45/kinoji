import os
import requests
from dotenv import load_dotenv
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.movie_models import Genre, engine
from sqlalchemy import insert
from sqlalchemy.orm import sessionmaker

load_dotenv()

url = "https://api.themoviedb.org/3/genre/movie/list"
params = {
    "limit": 10,
    "offset": 0
}

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {os.getenv("TMDB_ACCESS_TOKEN")}"
}

response = requests.get(url, headers=headers, params=params)
data = response.json()
genres_list = data['genres']
print(data)

Session = sessionmaker(bind=engine)
session = Session()

# Inserting Data into the database
try:
    for genres_data in genres_list:
        new_genre = Genre(
            id=genres_data['id'],
            genre_name=genres_data['name']
        )
        session.add(new_genre)
    
    session.commit()
    print("Successfully added genres to the database!")

except Exception as e:
    print(f"An error occured: {e}")

finally:
    session.close()