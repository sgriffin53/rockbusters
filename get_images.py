import requests


celebs = []
myfile = open('bands_wiki_new.txt','r')
lines = myfile.readlines()
bands = lines
myfile.close()
#myfile = open('celeb_images.txt','w')
#celebs = ['Kate Beckinsale', 'Ben Affleck', 'Matt Damon', 'Bill Cosby']
for band in bands:
    band = band.replace("\n","")
    retries = 0
    already_written = False
    while retries < 2:
        retries += 1
        url = 'https://en.wikipedia.org/wiki/' + band.replace(" ","%20")
        if retries == 2: url += '%20(band)'
        r = requests.get(url)
        #print(r.text)
        lines = r.text.split("\n")
        image = ''
        for line in lines:
            #print(line)
            #print(line)
            if 'https://' in line and ('.jpg' in line or '.png' in line or '.jpeg' in line):
                #print(line)
                tokens = line.split("\"")
                for token in tokens:
                    if len(token) == 0: continue
                    if token[-1] != 'g': continue
                    if (".png" in token.lower() or ".jpg" in token.lower() or ".jpeg" in token.lower()) and 'https://' in token:
                        band_names = band.split(" ")
                        isvalid = True
                        for band_name in band_names:
                            if band_name in token: isvalid = True
                        if isvalid:
                            image = token.replace("\n","").strip()
            #            print(token)
            if image != '': break
        if image == '': image = 'None'
        if not already_written and (retries == 2 or image != 'None'):
            myfile = open('band_images.txt','a')
            myfile.write(band + "|" + image + "\n")
            myfile.close()
            already_written = True
        print(band, image)
        if image != 'None': break