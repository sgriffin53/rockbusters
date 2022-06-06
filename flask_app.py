
# Flask app

import os, random
from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])

def rockbusters_page():
    guessed = False
    outstring = '''
                <html>
                    <body>
                    <center>
                    '''
    # Get random picture of karl
    ff = open('/home/jimmyrustles/mysite/karl_pics.txt')
    lines = ff.readlines()
    img_url = random.choice(lines)
    outstring += '<img src="' + img_url + '" height=250>'

    try:
        ff = open('/home/jimmyrustles/mysite/database.txt')
    except:
        print("unable to open file")
    lines = ff.readlines()
    ff.close()
    line = random.choice(lines)
    tokens = line.split('|')
    id = tokens[0]
    question = tokens[1]
    initials = tokens[2]
    answer = tokens[3]
        #outstring += '<br>' + line + '</br>'
  #  outstring += '<br>' + request.method + '<br>' + request.form['id'] + '<br>'
    if request.method == "POST":
        guessed = True
        try:
            match = False
            correct = False
            #outstring += '<br>request: ' + str(request.form['id']) + ':' + str(request.form['guess']) + '<br>'
            guess_id = str(request.form['id'])
            guess_answer = str(request.form['guess'])
            guess_answer = guess_answer.strip()
            current_question = ''
            correct_answer = ''
            op_logic = ''
            current_initials = ''
            album_image = ''
            original_thread = ''
            for line in lines:
                tokens = line.split('|')
                current_id = tokens[0]
                current_answer = tokens[3]
                if current_id == guess_id:
                    match = True
                    correct_answer = current_answer
                    correct_answer = correct_answer.strip()
                    current_question = tokens[1]
                    current_initials = tokens[2]
                    op_logic = tokens[4]
                    album_image = tokens[7]
                    original_thread = tokens[5]
                    if guess_answer.lower() == current_answer.lower():
                        correct = True
                        break
            if not match:
                outstring += '<br>Something went wrong. Can\'t find that question in the database.'
            else:
                outstring += '<h1>' + current_question + ' [' + current_initials + ']</h1>'
                outstring += 'Your guess: ' + guess_answer
                if correct:
                    prizes = ['Scotland Rocks', 'Best of Wild Weather', 'Best Air Guitar in the World Vol II', 'Bread Season One on DVD', 'Some tat in a jiffy bag', 'Stephen King\'s Rose Red... I\'ve never heard of it...']
                    prize = random.choice(prizes)
                    outstring += '<font color="#00BB00"><h2>Well done n that. ' + prize + ' will be winging its way to you.</h2></font>'
                else:
                    outstring += '<font color="#BB0000"><h2>Not the right answer, but along the right lines.</h2></font>'
                outstring += 'The correct answer was ' + correct_answer + '.'
                outstring += '<br><br><img src="' + album_image + '" height=350>'
                outstring += '<br><br>What\'s the logic?: ' + op_logic
                outstring += '<br><br>Original thread: <a href=https://old.reddit.com/' + original_thread + '/>' + original_thread + '</a>'
                outstring += '<br><br><a href=/>Try a new Rockbuster</a>'
        except:
            outstring += '<br>Unable to check answer. Soz.<br>'
    if not guessed:
        outstring += '<form method="post" action=".">'
        outstring += '<input type="hidden" name="id" value="' + id + '">'
        outstring += '<h1>' + question + ' [' + initials + ']</h1><br>'
        outstring += 'Guess: <input name="guess"> <input type="submit" value="Submit"><br>'
        outstring += '</form>'
        outstring += '<a href=/>Try a new Rockbuster</a><br>'
        outstring += '<br>How to play:<br>You\'re given a clue and some initials and the answer is a music band or artist.<br>'
        outstring += 'For example if the clue is \'Exploding Pet\', and the initials are AK, the answer would be \'Atomic Kitten\'<br>'
        outstring += '<br>More links:'
        outstring += '<br>A big thanks to the mentalists at <a href=https://old.reddit.com/r/rockbusters>/r/rockbusters</a> for providing the clues.'
        outstring += '<br><a href=https://www.youtube.com/watch?v=gIclWxN-kcI>The Complete Rockbusters (Compilation with Karl Pilkington, Ricky Gervais & Steve Merchant)</a>'
        outstring += '''
                        </center>
                        </body>
                    </html>
                    '''
    return outstring
