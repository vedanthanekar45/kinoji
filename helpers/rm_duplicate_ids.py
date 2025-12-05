input_file = "target_ids.txt"
output_file = "clean_ids.txt"

print(f"Cleaning {input_file}...")

seen_ids = set()
ordered_ids = []

with open(input_file, "r") as f:
    for line in f:
        movie_id = line.strip()
        
        if not movie_id:
            continue
            
        if movie_id not in seen_ids:
            seen_ids.add(movie_id)
            ordered_ids.append(movie_id)

print(f"Found {len(ordered_ids)} unique movies.")

with open(output_file, "w") as f:
    f.write("\n".join(ordered_ids) + "\n")

print(f"Saved clean list to {output_file}")