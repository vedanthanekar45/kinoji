# --- CONFIGURATION ---
TARGET_FILE = "target_ids.txt"
DB_FILE = "downloaded_ids.txt"
OUTPUT_FILE = "missing_ids.txt"

def find_gaps():
    try:
        print(f"Loading TARGET IDs from {TARGET_FILE}...")
        with open(TARGET_FILE, 'r') as f:
            target_ids = {line.strip() for line in f if line.strip()}
        print(f"   Target Count: {len(target_ids)}")

        print(f"Loading DATABASE IDs from {DB_FILE}...")
        with open(DB_FILE, 'r') as f:
            db_ids = {line.strip() for line in f if line.strip()}
        print(f"   Database Count: {len(db_ids)}")

        # The Magic Line: Set Subtraction
        missing_ids = target_ids - db_ids
        
        print(f"\n  Found {len(missing_ids)} missing movies.")

        if missing_ids:
            with open(OUTPUT_FILE, "w") as f:
                for mid in sorted(missing_ids):
                    f.write(f"{mid}\n")
            print(f"Saved missing IDs to: {OUTPUT_FILE}")
        else:
            print("No gaps found! Your database is complete.")

    except FileNotFoundError as e:
        print(f"Error: Could not find file. {e}")

if __name__ == "__main__":
    find_gaps() 