import requests, json, sys, random, urllib.parse, logging
from datetime import datetime

# Start Log
time = datetime.today().strftime('%Y-%m-%d')
logname = str(time) + "-HB.log"
logging.basicConfig(filename=str(logname),level=logging.DEBUG)
logging.info('BEGIN LOG - ' + str(time))
logging.info('BEGIN DEEPAI POST - ' + str(time))

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

username = open('user.dream', 'r')
for line in username:
    username = str(line)

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

print('Your post is now available at @' + str(profileName))
logging.info('Posted to @' + str(profileName) + '. Confirmation ID is: ' + str(confirmation))
logging.info('END OF LOG - ' + str(time))
