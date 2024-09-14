# Scrapes /r/rockbusters for questions

import praw, sys, json, wikipedia, requests, os
from datetime import datetime

def get_band_image(band):
    url = 'https://en.wikipedia.org/wiki/' + band.replace(" ", "%20")
    r = requests.get(url)
    lines = r.text.split("\n")
    image = None
    for line in lines:
        line = line.replace('//upload.wikimedia.org/', 'https://upload.wikimedia.org/')
        if 'https://' in line and ('.jpg' in line.lower() or '.png' in line.lower() or '.jpeg' in line.lower()) and 'archive.' not in line.lower():
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
            matching_phrases.append(' '.join(slice_of_words))
    return matching_phrases  # Return the list of all matching phrases

def acceptable_name(name):
    name = name.lower()
    for letter in name:
        match = False
        if (letter >= 'a' and letter <= 'z') or letter == ' ':
            match = True
        if not match: return False
    return True

def scrape_reddit(reddit, bands, band_images):
    homedir = '/home/jimmyrustles/mysite/'
    os.system("cp " + homedir + "database.txt " + homedir + "database_new.txt")
    myfile = open(homedir + 'database.txt', 'r', encoding='utf-8')
    lines = myfile.readlines()
    myfile.close()
    for line in reversed(lines):
        if "|" not in line: continue
        last_id = line.split("|")[0]
        current_db_id = int(last_id) + 1
        break
    already_done = []
    new_db_file = open(homedir + 'database_new.txt', 'a', encoding='utf-8')
    new_clues_count = 0
    new_bands_count = 0
    for line in lines:
        line = line.replace("\n", "")
        tokens = line.split("|")
        if len(tokens) < 6: continue
        already_done.append(tokens[5])  # url
    hot_posts = reddit.subreddit('rockbusters').new(limit=50)
    for post in hot_posts:
        if not hasattr(post.author, 'name'): continue
        title = post.title
        OP_name = post.author.name
        permalink = post.permalink
        if permalink in already_done: continue
        already_done.append(permalink)
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
        post_title = title
        if initials is None: continue
        if initials.upper() != initials: continue
        initials = initials.upper()
        initials = initials.replace(".","").replace(",","").replace("-","").replace(" ","")
        print("Initials:", initials)

        commentList = []
        OP_logic = ' '
        post.comments.replace_more(limit=None)
        for comment in post.comments.list():
            if hasattr(comment.author, 'name'): commentList.append([comment.body, comment.author.name])
        print(commentList)
        for comment in commentList:
            body = comment[0]
            author = comment[1]
            matches = find_matching_bands(initials, body)
            for match in matches:
                match = match.title()
                if match not in bands:
                    if len(match) < 4: continue
                    print("Found new potential band:", match)
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
                    if " (" in title: title = title.split(" (")[0]
                    if title.lower() != match.lower(): continue
                    match = title
                    match_phrases = ['band', 'musician', 'singer', 'rock', 'guitarist', 'pianist', 'guitar', 'hip hop', 'hip-hop']
                    matched_phrase = False
                    for phrase in match_phrases:
                        if phrase in page.content.split("\n")[0]:
                            # found new bound
                            matched_phrase = True
                            break
                    if matched_phrase:
                        image = get_band_image(match)
                        print("Found new band:", match)
                        print("Image:", image)
                        if image is None: continue
                        bands.append(match)
                        band_images[match] = image
                        new_bands_count += 1
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
        for comment in commentList:
            body = comment[0]
            author = comment[1]
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
        print(candidate_votes)
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
        print("post title:", post_title)
        db_string += "|" + post_title
        db_string += "|" + initials
        db_string += "|" + correct_answer
        db_string += "|" + OP_logic
        db_string += "|" + permalink
        db_string += "|" + OP_name
        db_string += "|" + band_images[correct_answer]
        db_string += "|" + post.score
        db_string = db_string.replace("\n","")
        db_string = db_string.replace("||","|")
        new_db_file.write(db_string + "\n")
        new_clues_count += 1
        print("!!!!!!!!!!!!!!!!!!!!!")
    new_db_file.close()
    os.system("cp " + homedir + "database_new.txt " + homedir + "database.txt")
    print("Written database")
    f = open(homedir + 'bands_wiki_new.txt','w', encoding='utf-8', errors='ignore')
    for band in bands:
        band = band.replace("\n","")
        f.write(band + "\n")
    f.close()
    print("Written bands")
    f = open(homedir + 'band_images.txt', 'w', encoding='utf-8', errors='ignore')
    for band in band_images:
        if len(band) > 70: continue # stop bands with accented letters getting corrupted
        f.write(band + "|" + band_images[band] + "\n")
    f.close()
    print("Written band images")
    f = open(homedir + 'rockbusters_updates.txt','a',encoding='utf-8', errors='ignore')
    current_date = datetime.today().date()
    f.write(str(current_date) + "|" + str(new_clues_count) + "," + str(new_bands_count) + "\n")
    f.close()
    pass
homedir = '/home/jimmyrustles/mysite/'
credentials = homedir + 'client_secrets.json'
with open(credentials) as f:
    creds = json.load(f)

reddit = praw.Reddit(client_id=creds['client_id'],
                     client_secret=creds['client_secret'],
                     user_agent=creds['user_agent'],
                     redirect_uri=creds['redirect_uri'],
                     refresh_token=creds['refresh_token'])
homedir = '/home/jimmyrustles/mysite/'

ff = open(homedir + 'bands_wiki_new.txt', 'r', encoding='unicode_escape')
read_bands = ff.readlines()
ff.close()
bands = []
for band in read_bands:
    band = band.replace("\n", "")
    acceptable = acceptable_name(band)
    if len(band) <= 3: acceptable = False
    if acceptable: bands.append(band)
band_images = {}
ff = open(homedir + 'band_images.txt', 'r', encoding='unicode_escape')
read_bands = ff.readlines()
ff.close()
for line in read_bands:
    line = line.replace("\n","")
    if "|" not in line: continue
    tokens = line.split("|")
    band = tokens[0]
    image_url = tokens[1]
    band_images[band] = image_url
scrape_reddit(reddit, bands, band_images)