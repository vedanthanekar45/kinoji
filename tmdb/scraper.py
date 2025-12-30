import httpx
import time
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, text

load_dotenv()

engine = create_engine(os.getenv('DATABASE_URL'))

def get_letterboxd_rating(tmdb_id: int) -> float | None:
    url = f"https://letterboxd.com/tmdb/{tmdb_id}"
    
    try:
        with httpx.Client(follow_redirects=True, timeout=10.0) as client:
            response = client.get(url)
            
            if response.status_code != 200:
                print(f"Failed to fetch {tmdb_id}: HTTP {response.status_code}")
                return None
            
            soup = BeautifulSoup(response.text, "html.parser")
            rating_meta = soup.find("meta", {"name": "twitter:data2"})
            if rating_meta and rating_meta.get("content"):
                content = rating_meta["content"]
                try:
                    rating = float(content.split()[0])
                    return rating
                except (ValueError, IndexError):
                    pass
            
            rating_elem = soup.select_one('a.tooltip.display-rating')
            if rating_elem:
                try:
                    return float(rating_elem.text.strip())
                except ValueError:
                    pass
                    
            return None
            
    except httpx.RequestError as e:
        print(f"Request error for {tmdb_id}: {e}")
        return None
    

def update_to_db(rating_dict):
    update_data = [{"b_id": k, "b_rating": v} for k, v in rating_dict.items()]
    with engine.connect() as conn:
        with conn.begin():
            stmt = text("UPDATE movies SET rating = :b_rating WHERE id = :b_id")
            conn.execute(stmt, update_data)


def scrape_letterboxd_ratings(tmdb_ids: list[int], delay: float = 0.5, batch_size: int = 50):
    ratings = {}
    total_updated = 0
    batch_num = 1
    
    for i, tmdb_id in enumerate(tmdb_ids):
        print(f"[{i+1}/{len(tmdb_ids)}] Fetching rating for TMDB ID: {tmdb_id}")
        rating = get_letterboxd_rating(tmdb_id)
        
        if rating is not None:
            ratings[tmdb_id] = rating
            print(f"  -> Rating: {rating}")
        else:
            print(f"  -> No rating found")
        
        if len(ratings) >= batch_size:
            print(f"\n{'='*50}")
            print(f"BATCH {batch_num}: Updating {len(ratings)} ratings to database...")
            print(f"{'='*50}")
            update_to_db(ratings)
            total_updated += len(ratings)
            print(f"Batch {batch_num} complete. Total updated so far: {total_updated}")
            print(f"{'='*50}\n")
            ratings.clear()
            batch_num += 1
        
        if i < len(tmdb_ids) - 1:
            time.sleep(delay)
    
    if ratings:
        print(f"\n{'='*50}")
        print(f"FINAL BATCH: Updating remaining {len(ratings)} ratings to database...")
        print(f"{'='*50}")
        update_to_db(ratings)
        total_updated += len(ratings)
    
    print(f"\n{'='*50}")
    print(f"COMPLETE: Total ratings updated to database: {total_updated}")
    print(f"{'='*50}")
    
    return total_updated


if __name__ == "__main__":
    with open("downloaded_ids.txt", "r") as f:
        tmdb_ids = [int(line.strip()) for line in f if line.strip()]
    
    print(f"Scraping ratings for {len(tmdb_ids)} movies in batches of 50...\n")
    total = scrape_letterboxd_ratings(tmdb_ids, delay=0.5, batch_size=50) 
    print(f"\nDone! Updated {total} movie ratings.")