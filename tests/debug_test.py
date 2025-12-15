import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("TMDB_ACCESS_TOKEN")

url = "https://api.themoviedb.org/3/movie/175223?append_to_response=credits"

print("\nSTARTING WARP CONNECTION TEST...")

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

try:
    print(f"Attempting to fetch Movie ID 175223...")
    
    response = requests.get(url, headers=headers, timeout=10)
    
    print(f"HTTP STATUS: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"SUCCESS! Found Movie: {data['title']}")
        print("WARP IS WORKING! Python can see the internet.")
    else:
        print(f"FAILED. Server said: {response.status_code}")

except Exception as e:
    print(f"CRASHED: {e}")
    print("Python is still blocked. Make sure WARP says 'Connected'.")