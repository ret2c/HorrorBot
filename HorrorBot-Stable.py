import requests, json, sys, random, urllib.parse, logging
from datetime import datetime
from serpapi import GoogleSearch

# Start Log
time = datetime.today().strftime('%Y-%m-%d')
logname = str(time) + "-HB.log"
logging.basicConfig(filename=str(logname),level=logging.DEBUG)
logging.info('BEGIN LOG - ' + str(time))

# Pull relevant information from api.keys
try:
    f = open('api.keys', 'r')
except FileNotFoundError:
    logging.info('Script Terminated - api.keys not found')
    sys.exit('api.keys was not found. Be sure it is in the same directory as this script.')

for key in f:
    if '#' in key:
        pass
    elif 'Apify-Key' in key:
        apifyKey = str(key[10:].strip())
    elif 'SerpApi-Key' in key:
        serpapiKey = str(key[12:].strip())
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
    sys.exit('None of the necessary information needed to run this script was found.\nBe sure to populate api.keys with the requested information.')
elif check >= 1:
    sys.exit('The following values were not present:\n' + str(error) + "This script requires every single value to run.")
else:
    f.close()

# Prevent last week's user from winning
illegal = ''
try:
    f = open('user.dream', 'r')
    for winner in f:
        illegal = str(winner)
    if illegal == '':
        print('Writing \'sampleUser\' to user.dream since no information was present.')
        f = open('user.dream', 'w')
        f.write('sampleUser')
        f.close()
        illegal = 'sampleUser'
except FileNotFoundError:
    f = open('user.dream', 'w')
    f.write('sampleUser')
    f.close()
    illegal = 'sampleUser'


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
    logging.info('Comments grabbed.')
except KeyError:
    print(request.json())
    logging.debug(request.json())
    sys.exit('There was an error in grabbing comments, did anybody comment? Please review the server\'s response in your log file or terminal output.')

print('Comments pulled via Apify, choosing winner...')

### Parse Comments ###
i = 0
f = open("word.dream", 'w')
f0 = open("user.dream", 'w')
comments = []
usernames = [] # Prevent abuse

while i != 24: # Apify API only allows up to 24 comments 
    try:
        text = request.json()[int(i)]['text']
        text = text.lower()
        if "imagine:" in text:
            uname = request.json()[int(i)]['ownerUsername']
            if uname in usernames:
                pass
            else:
                if str(illegal).lower() == str(uname):
                    pass
                else:
                    comments.append(uname + ":" + text)
                    usernames.append(uname)
        else:
            pass
        i = i + 1
    except IndexError:
        logging.info('While() loop broke at iteration #' + str(i) + '.')
        break

### Log Comments ###
if len(comments) == 0:
    logging.debug('Script aborted because no \'Imagine\' comments were found.\nIf this was an error with the script\'s function. Please contact @connorkas on GitHub.')
    sys.exit('No \'Imagine\'comments were found.\nQuitting...')
else:
    print("\nThe possible options were: ")
    print(comments)
    logging.info('Comments grabbed:')
    logging.info(comments)

### Choose Final Word to Generate With ###
finalChoice = random.choice(comments)
keyword = ':imagine:'
username, keyword, text = str(finalChoice).partition(keyword)
finalChoice = text.strip()
print("\nThe chosen comment was: " + str(finalChoice) + "\nWhich was written by: " + username + '\n')
logging.info('The chosen comment was: ' + str(finalChoice) + '\nSubmitted by: ' + username)

### Write To File ###
f.write(finalChoice)
f.close()
f0.write(username)
f0.close()
logging.info('Chosen comment and author written to *.dream files.')
print('Chosen comment has been written to: word.dream\nThe dreamer\'s handle has been written to: user.dream\n')

### Google Grab ###
print('Grabbing image from Google...')
logging.info('Attempting to grab image from Google.')

params = {
  "q": str(finalChoice),
  "tbm": "isch",
  "ijn": "0",
  "api_key": str(serpapiKey)
}

search = GoogleSearch(params)
results = search.get_dict()
images_results = results['images_results']

first_link = next(iter(images_results))

try:
    x = first_link['original']
    logging.info('Original Google image URL: ' + str(x))
except KeyError:
    logging.debug('There was an error grabbing the image from Google.')
    sys.exit('There was an error grabbing the image.\nExiting...')
print('Grabbed image from Google! Generating Deep Dream...\n')

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
input = open('word.dream', 'r')
for line in input:
    dream = str(line)
input.close()

caption = 'This week\'s AI image represents: ' + str(dream) + '\nThank you @' + str(username) + ' for this gift of imagination.\n\nIf you\'d like to imagine a new post next week, post a comment such as:\nImagine: <Insert Your Creation>\n\nThank you all. See you next week.\n4:00PM CST - Tuesday'

# URL Encode Caption
caption = urllib.parse.quote(caption, safe='')

### Request Creation ID From Meta (FB) ###
request = requests.post('https://graph.facebook.com/v13.0/' + str(profileID) + '/media?image_url=' + str(outputURL) + '&caption=' + str(caption) + '&access_token=' + str(metaKey))
try: 
    creationID = request.json()['id']
except KeyError:
    print(request.json())
    logging.debug(request.json())
    sys.exit('\nYour POST request was invalid.\nPlease review server response in logs or terminal output.')

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

print('Your post is now available at @' + str(profileName))
logging.info('Posted to @' + str(profileName) + '. Confirmation ID is: ' + str(confirmation))
logging.info('END OF LOG - ' + str(time))
