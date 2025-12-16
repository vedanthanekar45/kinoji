import psycopg2

DB_CONFIG = {
    "dbname": "justwatch",
    "user": "postgres",
    "password": "watch",
    "host": "localhost",
    "port": "5433"
}

def export_ids():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        print("Fetching all movie IDs from the database...")
        cur.execute("SELECT id FROM movies;")
        rows = cur.fetchall()
        downloaded_ids = {row[0] for row in rows}
        
        print(f"Found {len(downloaded_ids)} unique movies in the database.")
        
        with open("downloaded_ids.txt", "w") as f:
            for mid in sorted(downloaded_ids):
                f.write(f"{mid}\n")
        
        print("Saved list to 'downloaded_ids.txt'")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'conn' in locals() and conn:
            conn.close()

if __name__ == "__main__":
    export_ids()