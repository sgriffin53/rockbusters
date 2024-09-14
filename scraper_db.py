import json, wikipedia, requests, sys
import os

def get_band_image(band):
    url = 'https://en.wikipedia.org/wiki/' + band.replace(" ", "%20")
    r = requests.get(url)
    lines = r.text.split("\n")
    image = None
    for line in lines:
        line = line.replace('//upload.wikimedia.org/', 'https://upload.wikimedia.org/')
        if 'https://' in line and ('.jpg' in line.lower() or '.png' in line.lower() or '.jpeg' in line.lower()):
            tokens = line.split("\"")
            #print(tokens)
            for token in tokens:
                #print(token)
                if len(token) == 0: continue
                if token[-1].lower() != 'g': continue
                if ".jpg" in token.lower() and 'https://' in token:
                    band_names = band.split(" ")
                    isvalid = True
                    for band_name in band_names:
                        if band_name not in token: isvalid = False
                    isvalid = True # accept any picture - this will usually be the main article picture
                    if isvalid:
                        image = token.replace("\n","").strip()
    return image

def find_matching_bands(initials, text):
    bad_bands = ["Bee", "Good", "Radio", "That", "Moat", "Egg", "Mist", "Black", "Tea", "Musician", "Well", "Shed",
                 "Police", "Sex", "Attic", "Ink", "Walmart", "Bus", "Ember", "Bag", "Fur", "Crow", "Dodgy", "Rose",
                 "Man", "Echo", "Rolling Stone", "Boy", "Star", "Anne", "Orbit", "Hotel", "Brie", "Stephen", "Squirrel", "Allah"]
    text = text.replace("\\n"," ")
    remove_chars = ["?", ":", "-", ".", ",", "_", "!",")","(","\"","'"]
    for char in remove_chars:
        text = text.replace(char, "")
    words = text.split()  # Split the text into words
    initials = initials.upper()  # Convert initials to uppercase for consistency
    num_initials = len(initials)  # Number of initials
    matching_phrases = []  # List to store all matching phrases
    # Iterate over the text to find matching phrases
    for i in range(len(words) - num_initials + 1):
        # Extract a slice of the text of the same length as the initials
        slice_of_words = words[i:i + num_initials]
        # Extract the first letter of each word in the slice and join them
        slice_initials = ''.join(word[0] for word in slice_of_words)

        if slice_initials == initials:
            # Join the slice of words back into a phrase and add it to the list
            band = ' '.join(slice_of_words)
            if band.title() in bad_bands: continue
            matching_phrases.append(' '.join(slice_of_words))
    return matching_phrases  # Return the list of all matching phrases

def in_band_list(band):
    f = open('bands_wiki_new.txt', 'r', encoding='utf-8')
    lines = f.readlines()
    for line in lines:
        line = line.replace("\n","")
        if line == band: return True
    return False

urls = []
f = open('database.txt', 'r', encoding='utf-8')
lines = f.readlines()
for line in lines:
    if "|" not in line: continue
    if len(line.split("|")) < 5: continue
    print(line)
    url = line.split("|")[5]
    if url not in urls: urls.append(url)
last_id = -1
current_db_id = -1
for line in reversed(lines):
    if "|" not in line: continue
    last_id = line.split("|")[0]
    current_db_id = int(last_id) + 1
    break
# get all comments

comments_data = []
with open('rockbusters_comments', encoding='utf-8') as f:
    for line in f.readlines():
        line = line.replace("\\n","\\\\n")
        comments_data.append(json.loads(line))

post_comments = {}
i = 0
for comment in comments_data:
    #print(comment)
    link_id = comment['link_id'].replace("t3_","")
    if link_id not in post_comments:
        post_comments[link_id] = []
    post_comments[link_id].append(comment)
    i += 1
    print("Comment number:", i)
    #if i > 5: break

posts_data = []
with open('rockbusters_submissions', encoding='utf-8') as f:
    for line in f.readlines():
        line = line.replace("\\n","\\\\n")
        posts_data.append(json.loads(line))

print("Loaded posts and comments")
os.system("copy database.txt new_database.txt")
i = 0
bands = []
band_images = {}
f = open('bands_wiki_new.txt','r')
lines = f.readlines()
f.close()
for line in lines:
    if len(line) < 4: continue
    bands.append(line.replace("\n",""))
f = open('band_images.txt','r')
lines = f.readlines()
f.close()
for line in lines:
    line = line.replace("\n","")
    band = line.split("|")[0]
    image = line.split("|")[1]
    band_images[band] = image
current_db_id = int(last_id) + 1
for post in posts_data:
    i += 1
    print("Post number:", i)
    print("Title:", post["title"])
    if post['permalink'] in urls: continue
    urls.append(post['permalink'])
    title = post["title"]
    OP_name = post["author"]
    initials = None
    if ("[" in title and "]" in title) or ("(" in title and ")" in title):
        if "[" in title:
            tokens = title.split("[")
            initials = tokens[1].split("]")[0]
            title = tokens[0]
        if "(" in title:
            tokens = title.split("(")
            initials = tokens[1].split(")")[0]
            title = tokens[0]
    else:
        if len(title.split(" ")[-1]) <= 6:
            initials = title.split(" ")[-1]
    if initials is None: continue
    if initials.upper() != initials: continue
    initials = initials.upper()
    initials = initials.replace(".","").replace(",","").replace("-","").replace(" ","")
    print("Initials:", initials)
    id = post["id"]
    comments = []
    if id in post_comments: comments = post_comments[id]
    # first pass - get new band names
    for comment in comments:
        body = comment["body"]
        matches = find_matching_bands(initials, body)
        for match in matches:
            if match not in bands:
                match = match.title()
                print("Found new potential band:", match)
                if len(match) < 3: continue
                page = ''
                title = ''
                suffixes = ["", " (band)", " (American band)", " (British band)", " (Canadian band)", " (Australian band)", " (musician)", " (singer)", " (guitarist)"]
                page_match = False
                for suffix in suffixes:
                    try:
                        page = wikipedia.page(match + suffix, auto_suggest=False)
                        title = page.title
                        page_match = True
                        break
                    except:
                        page_match = False
                if not page_match: continue
                orig_match = match
                match = title
                if " (" in match: match = match.split(" (")[0]
                if orig_match != match: continue
                else:
                    image = get_band_image(match)
                    print("Found new band:", match)
                    print("Image:", image)
                    if image is None: continue
                    bands.append(match)
                    band_images[match] = image
                    # found new band
    candidates = []
    for band in bands:
        tokens = band.split(" ")
        band_initials = ''
        for token in tokens:
            band_initials += token[0].upper()
        if band_initials == initials:
            candidates.append(band)
    print("Candidates:", candidates)
    candidate_votes = {}
    OP_logic = ' '
    for comment in comments:
        body = comment['body']
        author = comment['author']
        print(body)
        for band in candidates:
            banned_bands = ["Meat", "Album", "Metal", "Train", "Lincoln Park"]
            if band in banned_bands: continue
            tokens = band.split(" ")
            band_initials = ''
            for token in tokens:
                band_initials += token[0].upper()
            if band.lower() in body.lower() and band_initials == initials:
                val = 1
                if author == OP_name:
                    val = 3
                    OP_logic = body  # override non-OP comments
                if OP_logic == ' ':  # hasn't already been set
                    OP_logic = body
                if band in candidate_votes:
                    candidate_votes[band] += val
                else:
                    candidate_votes[band] = val
    best = 0
    best_band = None
    for cand_band in candidate_votes:
        if candidate_votes[cand_band] > best:
            best_band = cand_band
            best = candidate_votes[cand_band]
    correct_answer = best_band
    print("Correct Answer:", correct_answer)
    if correct_answer is None: continue
    if correct_answer not in band_images:
        image = get_band_image(correct_answer)
        if image is None: continue
        band_images[correct_answer] = image
    current_db_id += 1
    db_string = ""
    db_string += str(current_db_id)
    db_string += "|" + post['title']
    db_string += "|" + initials
    db_string += "|" + correct_answer
    db_string += "|" + OP_logic
    db_string += "|" + post['permalink']
    db_string += "|" + OP_name
    db_string += "|" + band_images[correct_answer]
    db_string += "|" + post['score']
    db_string = db_string.replace("\n","<br>")
    print("!!!!!!!!!!!!!!!!!!!!!")
    ff = open("new_database.txt", "a", encoding='utf-8')
    ff.write(db_string + "\n")
    ff.close()
print("Updating bands and images")
f = open('bands_wiki_new.txt','w')
for band in bands:
    f.write(band + "\n")
f.close()
f = open('band_images.txt','w')
for band in band_images:
    f.write(band + "|" + band_images[band] + "\n")
f.close()