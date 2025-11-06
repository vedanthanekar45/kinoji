import os
import requests
from dotenv import load_dotenv
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.movie_models import Language, engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

url = "https://api.themoviedb.org/3/configuration/languages"
params = {
    "limit": 10,
    "offset": 0
}

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {os.getenv("TMDB_ACCESS_TOKEN")}"
}

print("Sending request to API..")
response = requests.get(url, headers=headers)
print("Got a response..")
data = response.json()

Session = sessionmaker(bind=engine)
session = Session()

try:
    for language_data in data:
        new_language = Language(
            iso_639_1 = language_data['iso_639_1'],
            name = language_data['english_name']
        )
        session.add(new_language)
    
    session.commit()
    print("Successfully added languages to the database!")

except Exception as e:
    print(f"An error occured: {e}")

finally:
    session.close()