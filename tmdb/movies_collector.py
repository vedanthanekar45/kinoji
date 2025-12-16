import os
import sys
import requests
import time
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from sqlalchemy.exc import IntegrityError

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db.movie_models import MovieData, Actor, Director, Country, Genre, Studio, Language, Genders, engine

load_dotenv()
ACCESS_TOKEN = os.getenv('TMDB_ACCESS_TOKEN')

session_http = requests.Session()
retries = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
session_http.mount('https://', HTTPAdapter(max_retries=retries))

Session = sessionmaker(bind=engine)
db_session = Session()

def get_or_create(session, model, id, name, gender_enum=None):
    instance = session.query(model).filter_by(id=id).first()
    if instance:
        return instance

    if model == Studio:
        instance = session.query(model).filter_by(studio_name=name).first()
        if instance:
            return instance

    params = {'id': id}
    if model == Studio:
        params['studio_name'] = name
    else:
        params['name'] = name
    
    if gender_enum: 
        params['gender'] = gender_enum

    try:
        with session.begin_nested():
            instance = model(**params)
            session.add(instance)
        return instance
    except IntegrityError:
        if model == Studio:
            return session.query(model).filter_by(studio_name=name).first()
        return session.query(model).filter_by(id=id).first()

def map_gender(tmdb_code):
    if tmdb_code == 1: return Genders.F
    if tmdb_code == 2: return Genders.M
    return Genders.N

try:
    print("Pre-loading Dimension Tables...")
    
    lang_map = {l.iso_639_1: l for l in db_session.query(Language).all()}
    genre_map = {g.id: g for g in db_session.query(Genre).all()} 
    country_map = {c.iso_3166_1: c for c in db_session.query(Country).all()}
    
    input_file = "missing_ids.txt"
    if not os.path.exists(input_file):
        input_file = "target_resume.txt"

    with open(input_file, "r") as f:
        all_ids = [line.strip() for line in f.readlines() if line.strip()]

    total_movies = len(all_ids)
    print(f"Starting Collection for {total_movies} movies...")

    for index, movie_id in enumerate(all_ids):
        if db_session.query(MovieData).filter_by(id=movie_id).first():
            continue

        url = f"https://api.themoviedb.org/3/movie/{movie_id}?append_to_response=credits"
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
        }

        try:
            response = session_http.get(url, headers=headers, timeout=10)
            
            if response.status_code == 404:
                print(f"Movie {movie_id} not found.")
                continue
            elif response.status_code == 429:
                time.sleep(5)
                continue
            elif response.status_code != 200:
                continue
                
            data = response.json()

            new_movie = MovieData(
                id=data['id'],
                name=data['title'],
                release=data.get('release_date') or None,
                runtime_minutes=data.get('runtime') or 0,
                budget=data.get('budget') or 0,
                revenue=data.get('revenue') or 0
            )

            db_session.add(new_movie)

            for g in data.get('genres', []):
                if g['id'] in genre_map: 
                    new_movie.genres.append(genre_map[g['id']])
            
            for c in data.get('production_countries', []):
                if c['iso_3166_1'] in country_map: 
                    new_movie.countries.append(country_map[c['iso_3166_1']])
                
            for l in data.get('spoken_languages', []):
                if l['iso_639_1'] in lang_map: 
                    new_movie.languages.append(lang_map[l['iso_639_1']])

            seen_studios = set()
            for company in data.get('production_companies', []):
                if company['id'] in seen_studios:
                    continue
                
                studio = get_or_create(db_session, Studio, id=company['id'], name=company['name'])
                if studio:
                    new_movie.studios.append(studio)
                    seen_studios.add(company['id'])

            credits = data.get('credits', {})
            seen_actors = set()
            for actor in credits.get('cast', [])[:15]:
                if actor['id'] in seen_actors:
                    continue
                
                gender_enum = map_gender(actor.get('gender', 0))
                actor_obj = get_or_create(db_session, Actor, id=actor['id'], name=actor['name'], gender_enum=gender_enum)
                if actor_obj:
                    new_movie.cast.append(actor_obj)
                    seen_actors.add(actor['id'])

            seen_directors = set()
            for crew in credits.get('crew', []):
                if crew['job'] == 'Director':
                    if crew['id'] in seen_directors:
                        continue

                    gender_enum = map_gender(crew.get('gender', 0))
                    director_obj = get_or_create(db_session, Director, id=crew['id'], name=crew['name'], gender_enum=gender_enum)
                    if director_obj:
                        new_movie.directors.append(director_obj)
                        seen_directors.add(crew['id'])

            if (index + 1) % 50 == 0:
                db_session.commit()
                print(f"Saved batch. Progress: {index + 1}/{total_movies}")
            
            time.sleep(0.05)

        except Exception as e:
            print(f"Error on {movie_id}: {e}")
            db_session.rollback()

    db_session.commit()
    print("RECONCILIATION COMPLETE!")

except Exception as e:
    print(f"Critical Failure: {e}")

finally:
    db_session.close()