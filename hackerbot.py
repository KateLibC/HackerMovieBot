import hashlib
import tweepy
import feedparser
import json
import os
import random

sources = [
    'https://www.helpnetsecurity.com/view/news/feed/',
    'http://www.networkworld.com/category/security/index.rss',
    'http://www.infosecisland.com/rss.html',
    'https://www.scmagazine.com/home/security-news/feed/',
    'https://nakedsecurity.sophos.com/feed',
    'https://threatpost.com/feed/',
    'https://krebsonsecurity.com/feed/',
    'https://www.schneier.com/blog/atom.xml',
    'http://feeds.feedburner.com/TroyHunt?format=xml',
    'https://www.grahamcluley.com/feed/',
    'https://bhconsulting.ie/securitywatch/feed/',
    'https://www.darkreading.com/rss_simple.asp',
    'https://aws.amazon.com/blogs/security/feed/',
    'https://securelist.com/feed',
    'http://security.googleblog.com/atom.xml',
    'https://www.tripwire.com/state-of-security/feed/',
    'https://blog.trendmicro.com/feed/',
    'https://securityintelligence.com/feed/',
    'https://www.informationsecuritybuzz.com/feed/',
    'https://www.veracode.com/blog/feed',
    'https://blog.pulsesecure.net/feed/',
    'https://www.pwnieexpress.com/blog/rss.xml',
    'https://www.wombatsecurity.com/blog/rss.xml',
    'https://blog.trailofbits.com/feed/',
    'https://www.gsnmagazine.com/rss.xml',
    'https://badcyber.com/feed/',
    'https://www.securityforum.org/news/feed/',
    'http://www.cyberdefensemagazine.com/feed',
    'https://defensivesecurity.org/feed/',
    'https://www.theregister.co.uk/security/headlines.atom',
]

titleFile = 'previousTitles.json'
imageDir = './images/'
titleMaxLen = 150

twitterCredFile = './twitter.json'
twitterEnabled = True

'''
Misc functions
'''

def secureChoice(data):
    sRandom = random.SystemRandom()
    return sRandom.choice(data)

'''
Title text management and processing
'''

def retrieveRSS(url):
    out = None
    return feedparser.parse(url)

def retrieveAllRSS(sources):
    items = []
    for source in sources:
        for entry in retrieveRSS(url=source)['entries']:
            if 'tags' not in entry.keys():
                entry['tags'] = []
            tags = []
            if len(entry['tags']) is not 0:
                tags = [x['term'].lower() for x in entry['tags']]
            i = {
                    'title': entry['title'], 
                    'tags': tags, 
                    'titleHash': hashlib.md5(entry['title'].encode('utf-8')).hexdigest()
                }
            items.append(i)
    return items

def loadFilterTitles(titleFile):
    hashData = []
    if os.path.exists(titleFile):
        with open(titleFile, 'r') as f:
            hashData = json.loads(f.read())
    else:
        createFilterTitles(titleFile=titleFile)
    return hashData

def createFilterTitles(titleFile):
    items = []
    with open(titleFile, 'w') as f:
        f.write(json.dumps(items))

def appendFilterTitle(titleFile, titleHash):
    data = loadFilterTitles(titleFile=titleFile)
    data.append(titleHash)
    with open(titleFile, 'w') as f:
        f.write(json.dumps(data))

def filterTitles(data, titleFile, titleMaxLen):
    out = []
    hashData = loadFilterTitles(titleFile=titleFile)
    for item in data:
        if len(item['title']) <= titleMaxLen and item['titleHash'] not in hashData:
            out.append(item)
    return out

def chooseTitle(data, titleFile):
    out = secureChoice(data=data)
    appendFilterTitle(titleFile=titleFile, titleHash=out['titleHash'])
    return out

'''
Image processing
'''

def listImages(imageDir):
    return [os.path.join(imageDir, x) for x in os.listdir(imageDir)]

def chooseImage(imageList):
    return secureChoice(imageList)

'''
Twitter stuff
'''

def createAuthFile(twitterCredFile):
    o = {
        'consumer_key': '',
        'consumer_secret': '',
        'access_token_key': '',
        'access_token_secret': ''
    }
    with open(twitterCredFile, 'w') as f:
        f.write(json.dumps(o, indent=2))

def checkAuthFile(twitterCredFile):
    o = False
    if os.path.exists(twitterCredFile):
        i = []
        for key, value in loadAuthFile(twitterCredFile=twitterCredFile).items():
            if len(value) is 0:
                i.append(None)
        o = None not in i
    else:
        createAuthFile(twitterCredFile=twitterCredFile)
    return o

def loadAuthFile(twitterCredFile):
    with open(twitterCredFile, 'r') as f:
        return json.loads(f.read())

def authTwitter(twitterCredFile):
    authData = loadAuthFile(twitterCredFile=twitterCredFile)
    auth = tweepy.OAuthHandler(authData['consumer_key'], authData['consumer_secret'])
    auth.set_access_token(authData['access_token_key'], authData['access_token_secret'])
    twitterAPI = tweepy.API(auth)
    return twitterAPI

def postTwitter(twitterAPI, tweetMessage, tweetImage):
    twitterAPI.update_with_media(tweetImage, tweetMessage)

'''
Beyond Meat and potatoes
'''

if __name__ == '__main__':
    if not checkAuthFile(twitterCredFile) and twitterEnabled:
        print('Check the credentials file.')
        exit(1)
    if twitterEnabled:
        twitterAPI = authTwitter(twitterCredFile=twitterCredFile)
        checkTwitter = twitterAPI.me()
    print('Retrieving data...')
    data = retrieveAllRSS(sources=sources)
    print('{} items to process...'.format(len(data)))
    print('Filtering out duplicates...')
    data = filterTitles(data=data, titleFile=titleFile, titleMaxLen=titleMaxLen)
    print('{} new potential candidates for processing!'.format(len(data)))
    print('Choosing a new candidate...')
    candidate = chooseTitle(data=data, titleFile=titleFile)
    print('Title chosen: {}'.format(candidate['title']))
    images = listImages(imageDir=imageDir)
    print('{} images to pick from...'.format(len(images)))
    image = chooseImage(imageList=images)
    print('Image chosen: {}'.format(image))
    if twitterEnabled:
        print('Posting to Twitter...')
        postTwitter(twitterAPI=twitterAPI, tweetMessage=candidate['title'], tweetImage=image)
        print('Posted to Twitter!')