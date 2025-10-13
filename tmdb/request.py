import requests
from dotenv import load_dotenv
import os

load_dotenv()

url = "https://api.themoviedb.org/3/authentication"
headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {os.getenv("TMDB_ACCESS_TOKEN")}"
}

response = requests.get(url, headers=headers)
print(response.text)