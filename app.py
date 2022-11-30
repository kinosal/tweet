"""Streamlit app to generate Tweets."""

# Import from standard library
import logging

logging.basicConfig(format="\n%(asctime)s\n%(message)s", level=logging.INFO, force=True)

# Import from 3rd party libraries
import streamlit as st
import streamlit.components.v1 as components

# Import modules
import tweets as twe
import oai

# Render streamlit page
st.set_page_config(page_title="Tweet", page_icon="🤖")

st.title("Generate Tweets")
st.write("This mini-app generates Tweets using OpenAI's GPT-3 based Davinci model.")
st.markdown("You can find the code on [GitHub](https://github.com/kinosal/tweet).")

topic = st.text_input(label="Topic")
mood = st.text_input(label="Mood (e.g. inspirational, funny, serious) (optional)")
mood_prompt = f"{mood} " if mood else ""
style = st.text_input(label="Twitter account to style-copy recent Tweets (optional)")
if style:
    twitter = twe.Tweets(account=style)
    tweets = twitter.fetch_tweets()
    tweets_prompt = "\n\n".join(tweets)
    prompt = (
        f"Write a {mood_prompt}Tweet about {topic} in less than 120 characters "
        f"and in the style of the following Tweets:\n\n{tweets_prompt}\n"
    )
else:
    prompt = f"Write a {mood_prompt}Tweet about {topic} in less than 120 characters:\n"

if topic:
    openai = oai.Openai()
    flagged = openai.moderate(prompt)
    mood_output = f", Mood: {mood}" if mood else ""
    style_output = f", Style: {style}" if style else ""
    if flagged:
        logging.info(f"Topic: {topic}{mood_output}{style_output}\nflaggged")
        st.error("Inappropriate input.")
    else:
        tweet = openai.complete(prompt).strip().replace('"', "")
        logging.info(f"Topic: {topic}{mood_output}{style_output}\nTweet: {tweet}")
        st.text_area(label="Tweet", value=tweet, height=100)
        col1, col2 = st.columns([5, 1])
        with col1:
            components.html(
                f"""
                    <a href="https://twitter.com/share?ref_src=twsrc%5Etfw" class="twitter-share-button" data-size="large" data-text="{tweet}\n - Tweet generated via" data-url="https://tweets.streamlit.app" data-show-count="false">Tweet</a><script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
                """,
                height=45,
            )
        with col2:
            def regenerate():
                tweet = openai.complete(prompt).strip().replace('"', "")
            st.button("Regenerate", type="secondary", on_click=regenerate)
