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


# Define functions
def generate(topic, mood="", style=""):
    """Generate Tweets."""

    if not topic:
        st.session_state.generate_error = "Please enter a topic"
        return

    mood_prompt = f"{mood} " if mood else ""
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

    openai = oai.Openai()
    flagged = openai.moderate(prompt)
    mood_output = f", Mood: {mood}" if mood else ""
    style_output = f", Style: {style}" if style else ""
    if flagged:
        logging.info(f"Topic: {topic}{mood_output}{style_output}\nflaggged")
        st.session_state.generate_error = "Inappropriate input"
        return

    else:
        st.session_state.tweet = openai.complete(prompt).strip().replace('"', "")
        logging.info(
            f"Topic: {topic}{mood_output}{style_output}\n"
            f"Tweet: {st.session_state.tweet}"
        )


# Render Streamlit page
st.set_page_config(page_title="Tweet", page_icon="🤖")
if "tweet" not in st.session_state:
    st.session_state.tweet = ""
if "generate_error" not in st.session_state:
    st.session_state.generate_error = ""

st.title("Generate Tweets")
st.write("This mini-app generates Tweets using OpenAI's GPT-3 based Davinci model.")
st.markdown("You can find the code on [GitHub](https://github.com/kinosal/tweet).")
topic = st.text_input(label="Topic", placeholder="AI")
mood = st.text_input(
    label="Mood (e.g. inspirational, funny, serious) (optional)",
    placeholder="inspirational",
)
style = st.text_input(
    label="Twitter account handle to style-copy recent Tweets (optional)",
    placeholder="elonmusk",
)
st.button(
    label="Generate",
    type="primary",
    on_click=generate,
    args=(topic, mood, style),
)
if st.session_state.tweet:
    st.markdown("""---""")
    st.text_area(label="Tweet", value=st.session_state.tweet, height=100)
    col1, col2 = st.columns([5, 1])
    with col1:
        components.html(
            f"""
                <a href="https://twitter.com/share?ref_src=twsrc%5Etfw" class="twitter-share-button" data-size="large" data-text="{st.session_state.tweet}\n - Tweet generated via" data-url="https://tweets.streamlit.app" data-show-count="false">Tweet</a><script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
            """,
            height=45,
        )
    with col2:
        st.button(
            label="Regenerate",
            type="secondary",
            on_click=generate,
            args=(topic, mood, style),
        )
elif st.session_state.generate_error:
    st.error(st.session_state.generate_error)
