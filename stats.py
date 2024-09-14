f = open('database.txt','r', encoding='utf-8')
lines = f.readlines()
f.close()
total_clues = len(lines)
poster_counts = {}
band_counts = {}
for line in lines:
    if len(line.split("|")) < 6: continue
    band = line.split("|")[3]
    OP = line.split("|")[6]
    if OP == "[deleted]": continue
    if band not in band_counts:
        band_counts[band] = 0
    band_counts[band] += 1
    if OP not in poster_counts:
        poster_counts[OP] = 0
    poster_counts[OP] += 1
# Function to get top N items from a dictionary
def get_top_n_items(d, n=20):
    # Sort the dictionary by value in descending order and get the top N items
    return dict(sorted(d.items(), key=lambda item: item[1], reverse=True)[:n])

# Get top 20 for each dictionary
top_20_bands = get_top_n_items(band_counts, 20)
top_20_posters = get_top_n_items(poster_counts, 20)

# Print the top 20 bands
print("Top 20 Bands:")
for band, count in top_20_bands.items():
    print(f"{band}: {count}")

# Print the top 20 posters
print("\nTop 20 Posters:")
for poster, count in top_20_posters.items():
    print(f"/u/{poster}: {count}")
print("")
print(f"Total clues: {total_clues}")
print(f"Total bands: {len(band_counts)}")
print(f"Total posters: {len(poster_counts)}")