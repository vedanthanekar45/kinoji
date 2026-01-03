import os
import time
import requests
import psycopg2
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from dotenv import load_dotenv

load_dotenv()

session_http = requests.Session()
retries = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
session_http.mount('https://', HTTPAdapter(max_retries=retries))

conn = psycopg2.connect(os.getenv("DATABASE_URL"))
cursor = conn.cursor()

ACCESS_TOKEN = os.getenv('TMDB_ACCESS_TOKEN')
input_file = "retry_ids.txt"

try:
    with open(input_file, "r") as f:
        all_ids = [line.strip() for line in f.readlines() if line.strip()]

    total_movies = len(all_ids)
    print(f"Starting Collection for {total_movies} movies...")

    for index, movie_id in enumerate(all_ids):
        url = f"https://api.themoviedb.org/3/movie/{movie_id}"
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
            rating = data['vote_average'] / 2

            cursor.execute(
                "UPDATE movies SET rating = %s WHERE id = %s",
                (rating, movie_id)
            )
            conn.commit()
            print(f"Successfully updated rating {rating} on movie ID {movie_id}")

        except Exception as e:
            print(f"Error on {movie_id}: {e}")
            conn.rollback()

except Exception as e:
    print(f"Critical Failure: {e}")

finally:
    cursor.close()
    conn.close()