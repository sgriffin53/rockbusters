import os, random
from footer import get_footer

def rockbusters_page(request):
    guessed = False
    asked_chatgpt = False
    outstring = '''
                <html>
                <head>
                                    <center>
                    <style>
</style>
</head>
                    <body>

                    '''
    # Get random picture of karl
    ff = open('/home/jimmyrustles/mysite/karl_pics.txt')
    lines = ff.readlines()
    img_url = random.choice(lines)
    outstring += '<img src="' + img_url + '" height=250>'
    game_mode = 'all'
    if request.method == "POST":
        if 'game_mode' in request.form:
            game_mode = request.form['game_mode']
    lines = ff.readlines()
    ff.close()
    ff = None
    ff = open('/home/jimmyrustles/mysite/database.txt')
    full_lines = ff.readlines()
    #outstring += str(lines)
    ff.close()
    lines = []
    if game_mode == 'all':
        try:
            ff = open('/home/jimmyrustles/mysite/database.txt')
            lines = ff.readlines()
            #outstring += str(lines)
            ff.close()
            ff = open('/home/jimmyrustles/mysite/database_OG.txt')
            second_lines = ff.readlines()
            ff.close()
            for line in second_lines:
                lines.append(line)
        except:
            outstring += "unable to open file"
    elif game_mode == 'subreddit':
        try:
            ff = open('/home/jimmyrustles/mysite/database.txt')
            lines = ff.readlines()
            #outstring += str(lines)
            ff.close()
        except:
            outstring += "Unable to open file"
    elif game_mode == 'OG':
        try:
            ff = open('/home/jimmyrustles/mysite/database_OG.txt')
            lines = ff.readlines()
            ff.close()
        except:
            outstring += "unable to open file OG"
    if len(lines) == 0:
        return outstring + " " + str(lines) + " " + game_mode
    total_clues = 0
    total_bands = 0
    all_bands = []
    db_lines = lines
    for line in lines:
        if "|" not in line: continue
        total_clues += 1
        tokens = line.split("|")
        band = tokens[3]
        if band not in all_bands:
            all_bands.append(band)
            total_bands += 1
    valid_question = False
    line = None
    while not valid_question:
        line = random.choice(lines)
        question = line.split("|")[1]
        if len(question.split(" ")[-1]) < 6:
            valid_question = True
    #line = random.choice(lines)
    tokens = line.split('|')
    id = tokens[0]
    question = tokens[1]
    initials = tokens[2]
    answer = tokens[3]
    extra_clues = []
    for item in lines:
        tokens = item.split("|")
        if len(tokens) < 3: continue
        item_question = tokens[1]
        if item_question == question: continue
        item_answer = tokens[3]
        if item_answer == answer:
            extra_clues.append(item_question)
    GPT_text = ''
        #outstring += '<br>' + line + '</br>'
  #  outstring += '<br>' + request.method + '<br>' + request.form['id'] + '<br>'
    if request.method == "POST":
        if 'guess' in request.form:
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
                    if len(tokens) < 3: continue
                    current_id = tokens[0]
                    current_answer = tokens[3]
                    if current_id == guess_id:
                        match = True
                        correct_answer = current_answer
                        correct_answer = correct_answer.strip()
                        current_question = tokens[1]
                        current_initials = tokens[2]
                        op_logic = tokens[4].replace("\\n","<br>")
                        album_image = tokens[7]
                        original_thread = tokens[5]
                        if guess_answer.lower() == current_answer.lower():
                            correct = True
                            break
                if not match:
                    outstring += '<br>Something went wrong. Can\'t find that question in the database.'
                else:
                    outstring += '<h1>' + current_question
                    last_token = None
                    if ("[" in current_question and "]" in current_question) or ("(" in current_question and ")" in current_question):
                        if "[" in current_question:
                            tokens = current_question.split("[")
                            last_token = tokens[1].split("]")[0]
                        if "(" in current_question:
                            tokens = current_question.split("(")
                            last_token = tokens[1].split(")")[0]
                    else:
                        if len(current_question.split(" ")[-1]) <= 6:
                            last_token = current_question.split(" ")[-1]
                    last_token = last_token.replace(".","").replace(",","").replace("-","").replace(" ","")
                    if current_question.split(" ")[-1].replace("(","").replace(")","").replace("[","").replace("]","").replace(".","") != current_initials:
                        outstring += ' [' + current_initials + ']'
                    outstring += '</h1>'
                    outstring += 'Your guess: ' + guess_answer
                    if correct:
                        prizes = ['Scotland Rocks', 'Best of Wild Weather', 'Best Air Guitar in the World Vol II', 'Bread Season One on DVD', 'Some tat in a jiffy bag', 'Stephen King\'s Rose Red... I\'ve never heard of it...']
                        prize = random.choice(prizes)
                        outstring += '<font color="#00BB00"><h2>Well done n that. ' + prize + ' will be winging its way to you.</h2></font>'
                    else:
                        outstring += '<font color="#BB0000"><h2>Not the right answer, but along the right lines.</h2></font>'
                    outstring += 'The correct answer was ' + correct_answer + '.'
                    album_image = album_image.replace("<br>","").replace("\n","")
                    outstring += '<br><br><img src="' + album_image + '" height=350>'
                    outstring += '<br><br>What\'s the logic?: ' + op_logic
                    if original_thread != 'None':
                        outstring += '<br><br>Original thread: <a href=https://old.reddit.com/' + original_thread + '/>' + original_thread + '</a>'
                    outstring += f'<form action="/rockbusters" method="POST"><input type="hidden" name="game_mode" value="{game_mode}">'
                    outstring += '<br><br><input type="submit" value="Try a new Rockbuster"></form>'
                    outstring += get_footer()
            except Exception as e:
                outstring += '<br>Unable to check answer. Soz. ' + str(e) + '<br>'
    if not guessed:
        outstring += '<form method="post" action="/rockbusters">'
        outstring += '<input type="hidden" name="id" value="' + id + '">'
        outstring += '<input type=\'hidden\' id=\'game_mode\' name=\'game_mode\' value=\''
        outstring += game_mode
        outstring += '\'>'
        outstring += '<h1>' + question
        last_token = None
        if ("[" in question and "]" in question) or ("(" in question and ")" in question):
            if "[" in question:
                tokens = question.split("[")
                last_token = tokens[1].split("]")[0]
            if "(" in question:
                tokens = question.split("(")
                last_token = tokens[1].split(")")[0]
        else:
            if len(question.split(" ")[-1]) <= 6:
                last_token = question.split(" ")[-1]
        last_token = last_token.replace(".","").replace(",","").replace("-","").replace(" ","")
        if last_token != initials:
            outstring += ' [' + initials + ']'
        outstring += '</h1>'
        if len(extra_clues) > 0: outstring += '<input type="button" id="extraClueButton" value="Load Extra Clues"><p id="extra_clues"><p>'
 #       outstring += 'Extra clues: ' + str(extra_clues) + '<br>'
        outstring += 'Guess: <input name="guess"> <input type="submit" value="Submit"><br>'
        outstring += '</form>'
        outstring += f'<form action="/rockbusters" method="POST"><input type="hidden" name="game_mode" value="{game_mode}">'
        outstring += '<br><br><input type="submit" value="Try a new Rockbuster"></form>'
        outstring += '''<br>Game mode:<br>
            <form id="game_mode_form" action="/rockbusters" method="POST">
                <input type="hidden" id='game_mode_option' name='game_mode' value=\''''
        outstring += game_mode
        outstring += ''''>
                <input type='button' id='game_mode_b1' style='width:300px;'''
        if game_mode == 'all': outstring += '; background-color:#77BB77'
        outstring += '''\' value='All Clues' onclick="setGameMode(this)">
                <br>
                <input type='button' id='game_mode_b2' style='width:300px'''
        if game_mode == 'subreddit': outstring += '; background-color:#77BB77'
        outstring += '''\' value='/r/rockbusters clues' onclick="setGameMode(this)">
                <br>
                <input type='button' id='game_mode_b3' style='width:300px'''
        if game_mode == 'OG': outstring += '; background-color:#77BB77'
        outstring += '''\' value="Karl's OG clues" onclick="setGameMode(this)">'''
#                <br>
#                <input type='button' id='game_mode_b4' style='width:300px'''
#        if game_mode == 'best_rated': outstring += '; background-color:#77BB77'
#        outstring += '''\' value="Best-rated clues" onclick="setGameMode(this)">
#                <br>
#                <input type='button' id='game_mode_b5' style='width:300px'''
#        if game_mode == 'this_month': outstring += '; background-color:#77BB77'
#        outstring += '''\' value="This month's clues" onclick="setGameMode(this)">
        outstring += '''
                <br>
                <input type='submit' id='game_mode_submit' style='display:none'>
            </form>

            <script>
            function setGameMode(button) {
                // Set the hidden input's value to the clicked button's value
                var game_mode = 'None'
                if (button.id == 'game_mode_b1') {
                    game_mode = 'all'
                }
                if (button.id == 'game_mode_b2') {
                    game_mode = 'subreddit'
                }
                if (button.id == 'game_mode_b3') {
                    game_mode = 'OG'
                }
                if (button.id == 'game_mode_b4') {
                    game_mode = 'best_rated'
                }
                if (button.id == 'game_mode_b5') {
                    game_mode = 'this_month'
                }
                document.getElementById('game_mode_option').value = game_mode;

                // Submit the form
                document.getElementById('game_mode_form').submit();
            }
            </script>
        '''

        outstring += '<br>Disclaimer:<br>Due to the user-generated nature of the clues, some clues may be inappropriate or offensive.<br>'
        outstring += '<br>How to play:<br>You\'re given a clue and some initials and the answer is a music band or artist.<br>'
        outstring += 'For example if the clue is \'Exploding Pet\', and the initials are AK, the answer would be \'Atomic Kitten\'<br>'
        outstring += f'<br>Total clues: {total_clues}<br>'
        outstring += f'Total bands: {total_bands}<br>'
        f = open('/home/jimmyrustles/mysite/database.txt','r')
        lines = f.readlines()
        f.close()
        i = 0
        for line in reversed(lines):
            i += 1
           # outstring += line + "<br><br>"
            if i > 10: break
        if os.path.exists('/home/jimmyrustles/mysite/rockbusters_updates.txt'):
            f = open('/home/jimmyrustles/mysite/rockbusters_updates.txt','r')
            lines = f.readlines()
            f.close()
            i = 0
            tot_bands = 0
            tot_clues = 0
            today_bands = 0
            today_clues = 0
            updated_date = ''
            for line in reversed(lines):
                if "|" not in line or "," not in line: continue
                line = line.replace("\n","")
                i += 1
                if i > 7: break
                num_clues = line.split("|")[1].split(",")[0]
                num_bands = line.split("|")[1].split(",")[1]
                tot_bands += int(num_bands)
                tot_clues += int(num_clues)
                if i == 1:
                    today_bands = int(num_bands)
                    today_clues = int(num_clues)
                    updated_date = line.split("|")[0]
            today_bands = 0
            tot_bands = 0
            week_bands_list = []
            today_bands_list = []
            full_bands = []
            i = 0
            for line in full_lines:
                i += 1
                if len(line.split("|")) < 3: continue
                if i > len(full_lines) - tot_clues - 1: break
                line = line.replace("\n","")
                band = line.split("|")[3]
                if band not in full_bands:
                    full_bands.append(band)
            i = 0
            for line in reversed(full_lines):
                if "|" not in line: continue
                line = line.replace("\n","")
                band = line.split("|")[3]
                i += 1
                if i > tot_clues: break
                if i <= today_clues:
                    if band not in today_bands_list and band not in full_bands:
                        today_bands_list.append(band)
                        today_bands += 1
                if band not in week_bands_list and band not in full_bands:
                    week_bands_list.append(band)
                    tot_bands += 1
            today_bands = len(today_bands_list)
            week_bands = len(week_bands_list)
            outstring += f'<br>New clues added: {updated_date}<br>'
            outstring += f'Clues added today: {today_clues}<br>'
            outstring += f'Bands added today: {today_bands}<br>'
            outstring += f'Clues added this week: {tot_clues}<br>'
            outstring += f'Bands added this week: {tot_bands}<br>'
            outstring += 'This week\'s new bands: '
            i = 0
            for band in week_bands_list:
                i += 1
                if i != len(band) and i != 1: outstring += ", "
                outstring += band
            outstring += '<br>'
        outstring += '<br>More links:'
        outstring += '<br>A big thanks to the mentalists at <a href=https://old.reddit.com/r/rockbusters>/r/rockbusters</a> for providing the clues.'
        outstring += '<br><a href=https://www.youtube.com/watch?v=gIclWxN-kcI>The Complete Rockbusters (Compilation with Karl Pilkington, Ricky Gervais & Steve Merchant)</a>'

        outstring += get_footer()
        outstring += '''
        <script>
        // Initialize the array with three strings
        '''
        outstring += 'let strings = ' + str(extra_clues) + ";"
        outstring += '''
        // Get references to the HTML elements
        const outputElement = document.getElementById('extra_clues');
        const button = document.getElementById('extraClueButton');

        // Function to handle button click
        function handleButtonClick() {
            // Check if the array has strings left
            if (strings.length > 0) {
                // Get the last string from the array
                const lastString = strings.pop();
                // Append the last string to the <p> element
                outputElement.innerHTML += '<h1> ' + lastString + ' </h1>';
                if (strings.length == 0) {
                    outputElement.innerHTML += 'No more clues for this band.';
                    document.getElementById("extraClueButton").style.display="none"
                }
            } else {
                // Optionally handle the case where the array is empty
                outputElement.innerHTML += 'No more clues for this band.';
                document.getElementById("extraClueButton").style.display="none"
            }
        }

        // Add event listener to the button
        button.addEventListener('click', handleButtonClick);
        </script>'''
        outstring += '''
                        </center>
                        </body>
                    </html>
                    '''
    return outstring