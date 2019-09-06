# Hacker Movie Bot

This is a simple Twitter bot that takes RSS feeds, selects a title at random, and then selects a random image to pair 
with it. It is currently designed to retrieve feeds from various cyber security blogs and news sites, but it can be 
easily changed to read whatever site you desire.


## Requirements

* Python 3 (2.7 should work)
* [Feedparser](https://github.com/kurtmckee/feedparser)
* [Tweepy](https://github.com/tweepy/tweepy)

Images are not included with this repository, but whatever Tweepy supports should work fine. You will also require an 
[API key](https://developer.twitter.com) from Twitter.

## Use

After installing the requisite modules, you will want to execute it for the first time using the following command:

`python3 hackerbot.py`

It will create a `twitter.json` file that you can edit to insert your API details provided by Twitter. After that, 
you can execute it once again and it should start to read RSS feeds and select them and an image at random.

Titles are stored in a JSON file that has hashes of them kept to prevent duplicates later on.

## To-do

* Support Mastodon
* Provide some sort accessibility for those with screen readers, et cetera
