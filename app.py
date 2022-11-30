"""Streamlit app to generate Tweets."""

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
if mood:
    mood = f"{mood} "
style = st.text_input(
    label="Twitter account to style-copy recent Tweets (optional)"
)
if style:
    twitter = twe.Tweets(account=style)
    tweets = twitter.fetch_tweets()
    formatted_tweets = "\n\n".join(tweets)
    prompt = (
        f"Write a {mood}Tweet about {topic} in less than 120 characters "
        f"and in the style of the following Tweets:\n\n{formatted_tweets}\n"
    )
else:
    prompt = f"Write a {mood}Tweet about {topic} in less than 120 characters:\n"

if topic:
    openai = oai.Openai()
    print(f"\nTopic: {topic}")
    if mood:
        print(f"Mood: {mood}")
    if style:
        print(f"Style: {style}")
    flagged = openai.moderate(prompt)
    if flagged:
        st.error("Inappropriate input.")
    else:
        tweet = openai.complete(prompt).strip().replace('"', "")
        print(f"Tweet: {tweet}")
        st.text_area(label="Tweet", value=tweet, height=100)
        components.html(
            f"""
                <a href="https://twitter.com/share?ref_src=twsrc%5Etfw" class="twitter-share-button" data-size="large" data-text="{tweet}\n - Tweet generated via" data-url="https://tweets.streamlit.app" data-show-count="false">Tweet</a><script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
            """
        )
