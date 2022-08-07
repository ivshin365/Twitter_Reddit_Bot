import tweepy
import praw
import requests
import time
import random
import os

reddit = praw.Reddit(client_id = 'O97hL_NLQl0DTJwfjdRZkQ',
                     client_secret = '5KYC3Y4T3D3yE_GgdIil98BbY22l5Q',
                     user_agent = 'DavidIvshin',
                     username = 'David_ivshin',
                     password = 'paraivshin365')

FILE_NAME = 'lastseenmention.txt'

auth = tweepy.OAuthHandler('13v2YCY3hrKLJ1mpE9owbfZb4', 'm58152uc27NpHhgX2vl0XPMjXD5O4Um883mwQsfGbU8nJSUG3g')

auth.set_access_token('1467670128-AyTseues42wavug5zXC0bunzTTKs35b3B9QweHp', 'mCI2sfqJLEFip1kmvUKY8S45ay2OJzdHATkHUdz0NzTmY')

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

tweetNumber = 3
interval = 60 * 60 * 8

terms = ["#tech", "#finance", "#webdev"]

# Get new tweet from reddit

def get_new_tweet():
    subreddit = reddit.subreddit('memes')
    hot_python = subreddit.hot(limit=5)

    for submission in hot_python:
        if not submission.stickied:
            if submission.score > 100:
                print('fetching post from sub-reddit...')
                print(submission.title + ' - Upvotes >' + str(submission.score))
                print(submission.url)
                quote = submission.title
                url = submission.url
                break
    return url, quote

# Save image to local folder

def save_image():
    url, quote = get_new_tweet()
    response = requests.get(url)
    if response.status_code == 200:
        with open("sample.jpg", 'wb') as f:
            f.write(response.content)


def post_tweet():
    saved_url, quote = get_new_tweet()
    print('posting new tweet...')
    try:
        api.update_with_media("sample.jpg", status=quote + '\n\n#memes ' + ' #memeoftheday')
        time.sleep(5)
    except tweepy.TweepError as e:
        print(e.reason)
        time.sleep(9)

#get all mentions

def read_last_seen(FILE_NAME):
    file_read = open(FILE_NAME, 'r')
    last_seen_id = int(file_read.read().strip())
    file_read.close()
    return last_seen_id

def store_last_seen(FILE_NAME, last_seen_id):
    file_write = open(FILE_NAME, 'w')
    file_write.write(str(last_seen_id))
    file_write.close()
    return

#reply to mention with keyword hello

def reply_mention():
    print('replying to mentions...')
    tweets_mentions = api.mentions_timeline(read_last_seen(FILE_NAME), tweet_mode='extended')
    for tweet_mention in reversed(tweets_mentions):
        if 'hello' in tweet_mention.full_text.lower():
            try:
                print(str(tweet_mention.id) + ' - ' + tweet_mention.full_text)
                api.update_status("@" + tweet_mention.user.screen_name + " Thanks For tweeting at me :)", tweet_mention.id)
                api.create_favorite(tweet_mention.id)
                store_last_seen(FILE_NAME, tweet_mention.id)
                time.sleep(10)
            except tweepy.TweepError as e:
                print(e.reason)
                time.sleep(9)
                continue


# search hashtag and retweet method

def search_hashtag():
# Find 'new' tweets (under hashtags/search terms)OAuthHandler

    query = random.choice(terms)
    print("Searching under term..." + query)
    for tweet_hashtag in tweepy.Cursor(api.search, q=query, lang="en").items(tweetNumber):
        try:
            if (tweet_hashtag.user.followers_count < 100 and tweet_hashtag.user.statuses_count < 2500):
                print("Ignoring user " + tweet_hashtag.user.screen_name)
                continue
            else:
                tweet_hashtag.retweet()
                api.create_favorite(tweet_hashtag.id)
                print("Retweet Done!")
                print(tweet_hashtag.user.screen_name)
                time.sleep(10)
        except tweepy.TweepError as e:
            print(e.reason)
            time.sleep(9)
        except StopIteration:
            break


# follow user who follow you method

def follow_user():
    print('following all followers...')
    for follower in tweepy.Cursor(api.followers).items():
        if not follower.following:
            try:
                follower.follow()
                time.sleep(10)
                print('Followed - ' + follower.screen_name)
            except tweepy.TweepError as e:
                print(e.reason)
                time.sleep(9)
                continue


while True:
    search_hashtag()
    time.sleep(10)
    reply_mention()
    time.sleep(5)
    follow_user()
    time.sleep(5)
    get_new_tweet()
    time.sleep(10)
    save_image()
    time.sleep(5)
    post_tweet()
    time.sleep(interval)



