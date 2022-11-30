"""Streamlit app to generate Tweets."""

# Import from standard library
import logging
import random

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
    with placeholder:
        with st.spinner("Please wait while your Tweet is being generated.."):
            if not topic:
                st.session_state.spinner = ""
                st.session_state.error = "Please enter a topic"
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
                st.session_state.spinner = ""
                st.session_state.error = "Inappropriate input"
                return

            else:
                st.session_state.spinner = ""
                st.session_state.error = ""
                st.session_state.tweet = (
                    openai.complete(prompt).strip().replace('"', "")
                )
                logging.info(
                    f"Topic: {topic}{mood_output}{style_output}\n"
                    f"Tweet: {st.session_state.tweet}"
                )


# Render Streamlit page
st.set_page_config(page_title="Tweet", page_icon="🤖")
if "tweet" not in st.session_state:
    st.session_state.tweet = ""
if "error" not in st.session_state:
    st.session_state.error = ""
if "feeling_lucky" not in st.session_state:
    st.session_state.feeling_lucky = False

st.title("Generate Tweets")
st.markdown(
    "This mini-app generates Tweets using OpenAI's GPT-3 based Davinci [model](https://beta.openai.com/docs/models/overview). You can find the code on [GitHub](https://github.com/kinosal/tweet) and the author on [Twitter](https://twitter.com/kinosal)."
)

if st.session_state.error:
    st.error(st.session_state.error)
placeholder = st.empty()

topic = st.text_input(label="Topic (or hashtag)", placeholder="AI")
mood = st.text_input(
    label="Mood (e.g. inspirational, funny, serious) (optional)",
    placeholder="inspirational",
)
style = st.text_input(
    label="Twitter account handle to style-copy recent Tweets (optional)",
    placeholder="elonmusk",
)
col1, col2 = st.columns([4, 1])
with col1:
    st.session_state.feeling_lucky = not st.button(
        label="Generate",
        type="primary",
        on_click=generate,
        args=(topic, mood, style),
    )
with col2:
    with open("moods.txt") as f:
        sample_moods = f.read().splitlines()
    st.session_state.feeling_lucky = st.button(
        label="Feeling lucky",
        type="secondary",
        on_click=generate,
        args=("an interesting topic", random.choice(sample_moods), ""),
    )

if st.session_state.tweet:
    st.markdown("""---""")
    st.text_area(label="Tweet", value=st.session_state.tweet, height=100)
    col1, col2 = st.columns([4, 1])
    with col1:
        components.html(
            f"""
                <a href="https://twitter.com/share?ref_src=twsrc%5Etfw" class="twitter-share-button" data-size="large" data-text="{st.session_state.tweet}\n - Tweet generated via" data-url="https://tweets.streamlit.app" data-show-count="false">Tweet</a><script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
            """,
            height=45,
        )
    with col2:
        if st.session_state.feeling_lucky:
            st.button(
                label="Regenerate",
                type="secondary",
                on_click=generate,
                args=("an interesting topic", random.choice(sample_moods), ""),
            )
        else:
            st.button(
                label="Regenerate",
                type="secondary",
                on_click=generate,
                args=(topic, mood, style),
            )

    st.markdown("""---""")
    st.markdown("**Other Streamlit apps by [@kinosal](https://twitter.com/kinosal)**")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        st.markdown("[Summarize Web Content](https://web-summarizer.streamlit.app)")
    with col2:
        st.markdown(
            "[Translate English to Code](https://english-to-code.streamlit.app)"
        )
    with col3:
        st.markdown("[Analyze PDFs](https://pdf-keywords.streamlit.app)")
