import os
import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from dotenv import load_dotenv

load_dotenv()

session = requests.Session()
retries = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
session.mount('https://', HTTPAdapter(max_retries=retries))

url = "https://api.themoviedb.org/3/discover/movie"
headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {os.getenv('TMDB_ACCESS_TOKEN')}"
}

output_file = "target_ids.txt"

print("Starting Robust Collection...")

for year in range(1920, 2026):
    print(f"Scanning Year: {year}...")
    year_ids = set()

    for page in range(1, 51): 
        params = {
            "include_adult": "false",
            "include_video": "false",
            "language": "en-US",
            "sort_by": "popularity.desc",
            "primary_release_year": year,  
            "vote_count.gte": "10",       
            "page": page
        }

        try:
            response = session.get(url, headers=headers, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])
                
                if not results:
                    break
                
                for movie in results:
                    year_ids.add(str(movie['id']))
            
            elif response.status_code == 429:
                print("Rate Limited. Sleeping for 10s...")
                time.sleep(10)
                continue 
            else:
                print(f"Error year {year} page {page}: {response.status_code}")
                continue

        except Exception as e:
            print(f"Failed on Year {year} Page {page}: {e}")
            continue

        time.sleep(0.2)

    if year_ids:
        with open(output_file, "a") as f:
            f.write("\n".join(year_ids) + "\n")
        print(f"   Saved {len(year_ids)} movies from {year}")

print("Done! All IDs saved to target_ids.txt")