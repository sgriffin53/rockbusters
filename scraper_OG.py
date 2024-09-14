import json, wikipedia, requests, sys
import os

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

f = open('band_images.txt', 'r', encoding='utf-8', errors='ignore')
lines = f.readlines()
f.close()
band_images = {}
for line in lines:
    if "|" not in line: continue
    band = line.split("|")[0]
    image = line.split("|")[1]
    band_images[band] = image

f = open('bands_wiki_new.txt', 'r', encoding='utf-8', errors='ignore')
lines = f.readlines()
f.close()
bands = []
for line in lines:
    line = line.replace("\n","")
    bands.append(line)

f = open('OG_clues.txt', 'r', encoding='utf-8', errors='ignore')
lines = f.readlines()
f.close()
f = open('database_OG.txt','w',encoding='utf-8')
current_db_id = 0
for line in lines:
    if '=' in line:
        line = line.replace("\n","").strip()
        #print(line)
        clue = line.split("=")[0].strip()
        initials = clue.split("(")[1].split(")")[0]
        logic = 'None'
        answer = line.split("=")[1]
        if line.count("(") > 1:
            answer = answer.split("(")[0]
            logic = line.split("(")[2].split(")")[0]
        answer = answer.strip()
        print("clue:", clue)
        print("initials:", initials)
        print("answer:", answer)
        print("logic:", logic)
        band_image = None
        band = answer
        if band in band_images:
            band_image = band_images[band]
        else:
            band_image = get_band_image(answer)
            if band_image is not None: band_images[band] = band_image
        if band not in bands:
            bands.append(band)
        print("image:", band_image)
        if band_image is None: continue
        current_db_id += 1
        db_string = ""
        db_string += "OG" + str(current_db_id)
        db_string += "|" + clue
        db_string += "|" + initials
        db_string += "|" + answer
        db_string += "|" + logic
        db_string += "|" + 'None'
        db_string += "|" + 'Karl Pilkington'
        db_string += "|" + band_image
        db_string = db_string.replace("\n","<br>")
        f.write(db_string + "\n")
f.close()
f = open('band_images.txt','w',encoding='utf-8', errors='ignore')
for band in band_images.keys():
    f.write(band + "|" + band_images[band] + "\n")
f.close()
f = open('bands_wiki_new.txt','w',encoding='utf-8', errors='ignore')
for band in band_images.keys():
    f.write(band + "\n")
f.close()
