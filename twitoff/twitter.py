""""Connects ot Twitter API via tweepy"""
import os
import tweepy
import spacy
from .models import DB, Tweet, User

#Get API Keys
key = os.getenv('TWITTER_API_KEY')
secret = os.getenv('TWITTER_API_KEY_SECRET')

#Connect to Twitter API
twitter_auth = tweepy.OAuthHandler(key, secret)
twitter = tweepy.API(twitter_auth)

# Load pretrained SpaCy World Embeddings Model
nlp = spacy.load('my_model')
#nlp = spacy.load('my_model/') ## if failing try

def vectorize_tweet(tweet_text):
    return nlp(tweet_text).vector

def add_or_update_user(username):
    """
    Pull a user and their tweets from Twitter API.
    Save them in the DB.
    """
    try:
        twitter_user = twitter.get_user(screen_name=username)
        # Does user already exist in db?
        db_user = User.query.get(username=username)
        if not db_user:
            db_user = User(id=twitter_user.id, username=username)
            DB.session.add(db_user)

        # Get user's Tweets
        tweets = twitter_user.timeline(
            count=200, exclude_replies=True, include_rts=False, tweet_mode='extended'
        )

        #Add each tweet to db
        for tweet in tweets:
            db_tweets = Tweet(id=tweet.id, text=tweet.full_text[:300])
            db_user.tweets.append(db_tweet)
            DB.session.add(db.tweet)
    except Exception as e:
        print(f'Error processing{username}: {e}')
        raise e

    #Save our submission
    DB.session.commit()
