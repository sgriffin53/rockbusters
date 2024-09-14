import unicodedata

def remove_accents(input_str):
    # Normalize the string to decompose accented characters
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    # Filter out characters that are not ASCII letters
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])

f = open('band_images.txt','r',encoding='utf-8', errors='ignore')
lines = f.readlines()
f.close()
f = open('new_band_images.txt', 'w', encoding='utf-8', errors='ignore')
for line in lines:
    line = line.replace("\n","")
    band = line.split("|")[0]
    image = line.split("|")[1]
    band = remove_accents(band)
    if len(band) > 70: continue
    if "AAAAAAAAAAAAAAAAAAAAAAAA" in band: continue
    image = remove_accents(image)
    print(band, image)
    f.write(band + "|" + image + "\n")
f.close()
