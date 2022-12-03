"""Twitter API connector."""

# Import from standard library
import os

# Import from 3rd party libraries
import streamlit as st
import tweepy

# Assign credentials from environment variable or streamlit secrets dict
consumer_key = os.getenv("TWITTER_CONSUMER_KEY") or st.secrets["TWITTER_CONSUMER_KEY"]
consumer_secret = (
    os.getenv("TWITTER_CONSUMER_SECRET") or st.secrets["TWITTER_CONSUMER_SECRET"]
)
access_key = os.getenv("TWITTER_ACCESS_KEY") or st.secrets["TWITTER_ACCESS_KEY"]
access_secret = (
    os.getenv("TWITTER_ACCESS_SECRET") or st.secrets["TWITTER_ACCESS_SECRET"]
)


class Tweets:
    """Twitter connector."""

    def __init__(self, account):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_key, access_secret)
        self.api = tweepy.API(auth)
        self.account = account

    def fetch_tweets(self) -> list:
        """Fetch most recent tweets."""
        try:
            tweets = self.api.user_timeline(
                screen_name=self.account,
                tweet_mode="extended",  # returns full text
                count=50,
                exclude_replies=True,
                include_rts=False,
            )
            return [tweet.full_text for tweet in tweets][:10]
        except tweepy.errors.NotFound:
            st.error("Twitter account not found.")
        except tweepy.errors.Unauthorized:
            st.error("Twitter account is private.")
        return []
