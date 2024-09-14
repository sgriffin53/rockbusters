files = ['database.txt', 'bands_wiki_new.txt', 'band_images.txt']
for file in files:
    f = open(file, 'r', encoding='utf-8', errors='ignore')
    lines = f.readlines()
    f.close()
    newlines = []
    removed = 0
    for line in lines:
        if "|" not in line and file != 'bands_wiki_new.txt': continue
        tokens = line.split("|")
        band = ''
        if file == 'database.txt':
            if len(line.split("|")) < 3: continue
            band = tokens[3]
        if file == 'bands_wiki_new.txt':
            band = tokens[0].replace("\n","")
        if file == 'band_images.txt':
            band = tokens[0].replace("\n","")
        #print(file, band)
        bad_bands = ["Season", "Bee", "Good", "Radio", "That", "Moat", "Egg", "Mist", "Black", "Tea", "Musician", "Well", "Shed", "Police", "Sex", "Attic", "Ink", "Walmart", "Bus", "Ember", "Bag", "Fur", "Crow", "Dodgy", "Rose", "Man", "Echo", "Rolling Stone", "Boy", "Star", "Anne", "Orbit", "Hotel", "Brie", "Stephen"]
        if band in bad_bands:
            removed += 1
            print("removed", band)
            continue
        newlines.append(line)

    f = open(file,'w',encoding='utf-8', errors='ignore')
    for line in newlines:
        f.write(line)
    f.close()

    print("removed ", removed, file)