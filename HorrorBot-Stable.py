import requests, json, sys, random, urllib.parse, logging
from datetime import datetime

# Start Log
time = datetime.today().strftime('%Y-%m-%d')
logname = str(time) + "-HB.log"
logging.basicConfig(filename=str(logname),level=logging.DEBUG)

# Pull relevant information from api.keys
f = open('api.keys', 'r')
for key in f:
    if '#' in key:
        pass
    elif 'Apify-Key' in key:
        apifyKey = str(key[10:].strip())
    elif 'DeepAI-Key' in key:
        deepaiKey = str(key[11:].strip())
    elif 'Meta-Key' in key:
        metaKey = str(key[9:].strip())
    elif 'Profile-ID' in key:
        profileID = str(key[11:].strip())
    elif 'Username' in key:
        profileName = str(key[9:].strip())

# Check if values are empty
check = 0
error = ''
if apifyKey == '':
    error = 'Apify Key\n'
    check = check + 1
if deepaiKey == '':
    error = str(error) + "DeepAI Key\n"
    check = check + 1
if metaKey == '':
    error = str(error) + "Meta Key\n"
    check = check + 1
if profileID == '':
    error = str(error) + "Profile ID\n"
    check = check + 1
if profileName == '':
        error = str(error) + "Profile Name\n"
        check = check + 1

if check == 5:
    sys.exit('None of the necessary information needed to run this script was found.\nBe sure to populate api.keys with the requested information.\nIf you don\'t have the file, you can find it here: https://github.com/connorkas/HorrorBot/blob/master/api.keys')
elif check >= 1:
    sys.exit('The following values were not present:\n' + str(error) + "This script requires every single value to run.")
else:
    pass

# Prevent last week's user from winning
try:
    f = open('user.dream', 'r')
    for winner in f:
        illegal = str(winner)
    if illegal == '':
        print('No username found, but we detected user.dream\nIs this your first time running this bot?')
except FileNotFoundError:
    logging.debug('Script aborted because user.dream was not present in the same directory.')
    sys.exit('user.dream not found (is it in the same directory?)\nLast weeks\'s user is required to prevent them from winning a second time.')


### Grab Recent Instagram Post ###
print('Searching for most recent post...')
values = "{\"username\": [\"" + str(profileName) + "\"],\"resultsLimit\": 1}"
headers = {
        'Content-Type': 'application/json'
}
request = requests.get('https://api.apify.com/v2/acts/zuzka~instagram-post-scraper/run-sync-get-dataset-items?token=' + str(apifyKey) + '&build=latest&format=json&fields=url', data=values, headers=headers)

try:
    recentPostUrl = request.json()[0]['url']
except KeyError:
    print(request.json())
    logging.debug(request.json())
    sys.exit('There was an error in your request. Please review the server\'s response in your log file or terminal output.')

print('Found most recent post: ' + recentPostUrl + "\nGrabbing comments...")
logging.info('Found most recent post: ' + recentPostUrl + "\nGrabbing comments...")

### Grab Comment From Recent Post ###
values = "{\"directUrls\":[\"" + str(recentPostUrl) + "\"],\"resultsLimit\":24}"
headers = {
  'Content-Type': 'application/json'
}
request = requests.post('https://api.apify.com/v2/acts/zuzka~instagram-comment-scraper/run-sync-get-dataset-items?token=' + str(apifyKey) + '&format=json&fields=ownerUsername%2Ctext', data=values, headers=headers)

try:
    x = request.json()[0]['ownerUsername']
except KeyError:
    print(request.json())
    logging.debug(request.json())
    sys.exit('There was an error in grabbing comments, did anybody comment? Please review the server\'s response in your log file or terminal output.')

x = request.json()
print('Comments found, writing to file.')

i = 0
f = open("word.dream", 'w')
f0 = open("user.dream", 'w')
comments = []
usernames = [] # Prevent abuse

while i != 24: # API only allows up to 24 comments 
    try:
        text = request.json()[int(i)]['text']
        text = text.lower()
        if "imagine:" in text:
            uname = request.json()[int(i)]['ownerUsername']
            if uname in usernames:
                pass
            else:
                if str(illegal) in str(uname):
                    pass
                else:
                    comments.append(uname + ":" + text)
                    usernames.append(uname)
        else:
            pass
        i = i + 1
    except IndexError:
        logging.info('While() loop broke at the _' + str(i) + '_ iteration.')
        break

### Choose Final Word to Generate With ###
print("\nThe possible options were: ")
print(comments)
logging.info(comments)
finalChoice = random.choice(comments)
keyword = ':imagine:'
username, keyword, text = str(finalChoice).partition(keyword)
finalChoice = text.strip()
print("\nThe chosen comment was: " + str(finalChoice) + "\nWhich was written by: " + username + '\n')
logging.info('The chosen comment was: ' + str(finalChoice) + '\nSubmitted by: ' + username)

### Write To File ###
f.write(finalChoice)
f0.write(username)
logging.info('Chosen comment and author written to *.dream files.')
print('Chosen comment has been written to: word.dream\nThe dreamer\'s handle has been written to: user.dream\n')

### Grab Chosen Word ###
filename = "word.dream"

### Text2Img API ###
t2iRes = requests.post(
    "https://api.deepai.org/api/text2img",
    data={
        'text': open(filename, 'rb'),
    },
    headers={'api-key': str(deepaiKey)}
)

### Original Image URL ###
try:
    x = t2iRes.json()['output_url']
except KeyError:
    print(t2iRes.json())
    logging.debug(t2iRes.json())
    print('Error generation output URL. Please review terminal output or log file.')

print('Success! Your image has been generated. Loading Deep Dream...')

### Deep Dream API ###
i = 0
while (i != 5):
    print('Working on iteration #' + str((i + 1)) + '...')
    ddRes = requests.post(
        "https://api.deepai.org/api/deepdream",
        data={
            'image': str(x),
        },
        headers={'api-key': str(deepaiKey)}
    )
    x = ddRes.json()['output_url']
    i = i + 1

### Final Output ###
try:
    outputURL = ddRes.json()['output_url']
except KeyError:
    print(ddRes.json())
    logging.debug(ddRes.json())
    print('There was an error in generating the final output. Please review logs or terminal output.')

print('\nYour deep dream image can be found here: ' + outputURL + '\n')
logging.info('Deep Dream URL: ' + outputURL)

f = open('outputURL', 'w')
f.write(outputURL)
logging.info('Wrote to filename: outputURL')

### Grab Relevent Information ###
# Grab Input 
input = open('word.dream', 'r')
for line in input:
    input = str(line)

caption = 'This week\'s AI image represents: ' + str(input) + '\nThank you @' + str(username) + ' for this gift of imagination.\n\nIf you\'d like to imagine a new post next week, post a comment such as:\nImagine: <Insert Your Creation>\n\nThank you all. See you next week.\n4:00PM CST - Tuesday'

# URL Encode Caption
caption = urllib.parse.quote(caption, safe='')

### Request Creation ID From Meta (FB) ###
request = requests.post('https://graph.facebook.com/v13.0/' + str(profileID) + '/media?image_url=' + str(outputURL) + '&caption=' + str(caption) + '&access_token=' + str(metaKey))
try: 
    creationID = request.json()['id']
except KeyError:
    print(request.json())
    logging.debug(request.json())
    sys.exit('\nYour POST request was invalid\nPlease review server response in logs or terminal output.')

print('Creation ID generation was successful.')
logging.info('Creation ID: ' + str(creationID))

### Use Creation ID to POST to Instagram ###
request = requests.post('https://graph.facebook.com/v13.0/' + str(profileID) + '/media_publish?creation_id=' + str(creationID) + '&access_token=' + str(metaKey))

try:
    confirmation = request.json()['id']
except KeyError:
    print(request.json())
    logging.debug(request.json())
    sys.exit('\nThere was a problem posting your image.\nPlease review server response.')

print('Your post is now available at @connorkas')
logging.info('Posted to @connorkas. Confirmation ID is: ' + str(confirmation))
logging.info('END OF LOG - ' + str(time))
