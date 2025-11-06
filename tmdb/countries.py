import os
import requests
from dotenv import load_dotenv
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.movie_models import Country, engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

url = "https://api.themoviedb.org/3/configuration/countries"
params = {
    "limit": 10,
    "offset": 0
}

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {os.getenv("TMDB_ACCESS_TOKEN")}"
}

response = requests.get(url, headers=headers)
data = response.json()

Session = sessionmaker(bind=engine)
session = Session()

try:
    existing_codes_query = session.query(Country.iso_3166_1).all()
    existing_codes = {code[0] for code in existing_codes_query}
    iso_code = data['iso_3166_1']

    for country_data in data:
        if iso_code not in existing_codes:
            new_country = Country(
                iso_3166_1 = country_data['iso_3166_1'],
                country_name = country_data['english_name']
            )
            session.add(new_country)
    
    session.commit()
    print("Successfully added countries to the database!")

except Exception as e:
    print(f"An error occured: {e}")

finally:
    session.close()