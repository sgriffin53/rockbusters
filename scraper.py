# Scrapes /r/rockbusters for questions

import praw, sys
bands = []

def acceptable_name(name):
    name = name.lower()
    for letter in name:
        match = False
        if (letter >= 'a' and letter <= 'z') or letter == ' ':
            match = True
        if not match: return False
    return True

reddit = praw.Reddit(client_id='XXX',  # enter reddit api credentials
                     client_secret='XXX',
                     user_agent='XXX',
                     username='XXX',
                     password='XXX')

# get band list and remove unacceptable band names

ff = open('bands_wiki_new.txt', 'r')
read_bands = ff.readlines()
ff.close()
for band in read_bands:
    band = band.replace("\n", "")
    acceptable = acceptable_name(band)
    if len(band) <= 3: acceptable = False
    if acceptable: bands.append(band)
band_images = {}
ff = open('band_images.txt', 'r')
read_bands = ff.readlines()
ff.close()
for line in read_bands:
    tokens = line.split("|")
    band = tokens[0]
    image_url = tokens[1]
    band_images[band] = image_url
hot_posts = reddit.subreddit('rockbusters').top(limit=10000)
i = 0
j = 0
db_id = 0
unique_answers = []
ff = open("new_database.txt", "a", encoding='utf-8')
fg = open("unique.txt", "a", encoding='utf-8')
for post in hot_posts:
    j+=1
    print(j,"of 1000")
    title = post.title
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
    if initials == None: continue
    if not hasattr(post.author, 'name'): continue
    candidates = []
    for band in bands:
        tokens = band.split(" ")
        band_initials = ''
        for token in tokens:
            band_initials += token[0].upper()
        if band_initials == initials:
            candidates.append(band)
    if candidates == []: continue
    print("title:",post.title)
    print("initials:", initials)
    print("candidates:", candidates)
    OP_name = post.author.name
    #print(post.comments)
    candidate_votes = {}
    commentList = []
    OP_logic = ' '
    post.comments.replace_more(limit=None)
    for comment in post.comments.list():
        if hasattr(comment.author, 'name'): commentList.append([comment.body, comment.author.name])
    print(commentList)
    for comment in commentList:
        body = comment[0]
        author = comment[1]
        for band in bands:
            tokens = band.split(" ")
            band_initials = ''
            for token in tokens:
                band_initials += token[0].upper()
            if band.lower() in body.lower() and band_initials == initials:
                val = 1
                if author == OP_name:
                    val = 3
                    OP_logic = body # override non-OP comments
                if OP_logic == ' ': # hasn't already been set
                    OP_logic = body
                if band in candidate_votes: candidate_votes[band] += val
                else: candidate_votes[band] = val
    best = 0
    best_band = None
    for cand_band in candidate_votes:
        if candidate_votes[cand_band] > best:
            best_band = cand_band
            best = candidate_votes[cand_band]
    correct_answer = best_band
    img_link = "None"
    if correct_answer in band_images:
        img_link = band_images[correct_answer]
    else:
        continue
    if correct_answer == None: continue
    print("votes:",candidate_votes)
    print("correct answer:", correct_answer)
    db_id += 1
    db_string = ""
    db_string += str(db_id)
    db_string += "|" + title
    db_string += "|" + initials
    db_string += "|" + correct_answer
    db_string += "|" + OP_logic
    db_string += "|" + post.permalink
    db_string += "|" + OP_name
    db_string += "|" + img_link
    if correct_answer not in unique_answers:
        unique_answers.append(correct_answer)
        fg.write(correct_answer + "\n")
    db_string = db_string.replace("\n","")
    ff.write(db_string + "\n")
    print(" ")
    i += 1
ff.close()
fg.close()
print(i)
print("unique:", len(unique_answers))
#    print(post.title)