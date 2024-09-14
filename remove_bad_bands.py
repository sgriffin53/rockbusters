import wikipedia

def get_page_match(band):
    page = ''
    title = ''
    try:
        page = wikipedia.page(band, auto_suggest=False)
        title = page.title
    except:
        return False
    if title != band: return False
    page_lines = page.content.split("\n")
    if len(page_lines) < 3: return False
    page_start = page_lines[0] + "\n" + page_lines[1] + "\n" + page_lines[2]
    match_phrases = ['band', 'musician', 'singer', 'rock', 'guitarist', 'pianist', 'group']
    matched_phrase = False
    for phrase in match_phrases:
        if phrase in page_start:
            # found new bound
            matched_phrase = True
            break
    return matched_phrase

def get_bad_bands():
    f = open('bands_wiki_new.txt')
    lines = f.readlines()
    f.close()
    to_remove = []
    i = 0
    for line in lines:
        i += 1
        if i < 1080: continue
        band = line.replace("\n","")
        match = get_page_match(band)
        if not match:
            suffixes = ["(band)", "(American band)", "(British band)", "(Canadian band)", "(Australian band)", "(musician)", "(singer)", "(guitarist)"]
            did_match = False
            for suffix in suffixes:
                current_match = get_page_match(band + " " + suffix)
                if current_match: did_match = True
            if not did_match:
                to_remove.append(band)
                print("Removing", band)
        if i % 20 == 0: print(i)
    return to_remove

def create_removal_list():
    bad_bands = get_bad_bands()
    f = open('to_remove.txt', 'w')
    for band in bad_bands:
       f.write(band + "\n")
    f.close()
    print("Created removal list")

def remove_bands():
    f = open('to_remove.txt','r')
    lines = f.readlines()
    f.close()
    bad_bands = []
    for line in lines:
        band = line.replace("\n","")
        bad_bands.append(band)
    f = open('bands_wiki_new.txt','r')
    lines = f.readlines()
    f.close()
    f = open('wiki_bands_new_new.txt','w', encoding='utf-8')
    i = 0
    for line in lines:
        band = line.replace("\n","")
        if band not in bad_bands:
            f.write(band + "\n")
        else:
            i += 1
    f.close()
    print("Removed " + str(i) + " bands")

def remove_from_db():
    f = open('to_remove.txt','r')
    lines = f.readlines()
    f.close()
    bad_bands = []
    for line in lines:
        line = line.replace("\n","")
        bad_bands.append(line)
    f = open('database.txt','r', encoding='utf-8')
    lines = f.readlines()
    f.close()
    newlines = []
    removed_count = 0
    for line in lines:
        if "|" not in line: continue
        line = line.replace("\n","")
        db_band = line.split("|")[3]
        if db_band not in bad_bands:
            newlines.append(line)
        else:
            removed_count += 1
    f = open('new_database.txt','w',encoding='utf-8')
    for line in newlines:
        f.write(line + "\n")
    f.close()
    print("Written new database")
    print(str(removed_count) + " removed")
    f = open('bands_wiki_new.txt','r',encoding='unicode_escape')
    lines = f.readlines()
    f.close()
    newbands = []
    removed_bands = 0
    for line in lines:
        line = line.replace("\n","")
        if line not in bad_bands:
            newbands.append(line)
        else:
            removed_bands += 1
    f = open('new_bands_wiki.txt','w',encoding='utf-8')
    for band in newbands:
        f.write(band + "\n")
    f.close()
    print("Written new bands wiki file")
    print(str(removed_bands) + " removed bands")
    f = open('band_images.txt','r',encoding='unicode_escape')
    lines = f.readlines()
    f.close()
    newlines = []
    removed_band_images = 0
    for line in lines:
        line = line.replace("\n","")
        band = line.split("|")[0]
        image = line.split("|")[1]
        if band not in bad_bands:
            newlines.append(band + "|" + image)
        else:
            removed_band_images += 1
    f = open('new_band_images.txt','w',encoding='utf-8')
    for line in newlines:
        f.write(line + "\n")
    f.close()
    print("Written new band images file")
    print(str(removed_band_images) + " removed band images")
#create_removal_list()
remove_from_db()
#print(get_page_match('All American Rejects'))