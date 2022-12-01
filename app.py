"""Streamlit app to generate Tweets."""

# Import from standard library
import logging
import random
import re

logging.basicConfig(format="\n%(asctime)s\n%(message)s", level=logging.INFO, force=True)

# Import from 3rd party libraries
import streamlit as st
import streamlit.components.v1 as components

# Import modules
import tweets as twe
import oai


# Define functions
def generate_text(topic: str, mood: str = "", style: str = ""):
    """Generate Tweet text."""
    st.session_state.tweet = ""
    st.session_state.image = ""
    st.session_state.text_error = ""

    if not topic:
        st.session_state.text_error = "Please enter a topic"
        return

    with text_spinner_placeholder:
        with st.spinner("Please wait while your Tweet is being generated..."):
            mood_prompt = f"{mood} " if mood else ""
            if style:
                twitter = twe.Tweets(account=style)
                tweets = twitter.fetch_tweets()
                tweets_prompt = "\n\n".join(tweets)
                prompt = (
                    f"Write a {mood_prompt}Tweet about {topic} in less than 120 characters "
                    f"and in the style of the following Tweets:\n\n{tweets_prompt}\n\n"
                )
            else:
                prompt = f"Write a {mood_prompt}Tweet about {topic} in less than 120 characters:\n\n"

            openai = oai.Openai()
            flagged = openai.moderate(prompt)
            mood_output = f", Mood: {mood}" if mood else ""
            style_output = f", Style: {style}" if style else ""
            if flagged:
                logging.info(f"Topic: {topic}{mood_output}{style_output}\n")
                return

            else:
                st.session_state.text_error = ""
                st.session_state.tweet = (
                    openai.complete(prompt).strip().replace('"', "")
                )
                logging.info(
                    f"Topic: {topic}{mood_output}{style_output}\n"
                    f"Tweet: {st.session_state.tweet}"
                )


def generate_image(prompt: str):
    """Generate Tweet image."""
    with image_spinner_placeholder:
        with st.spinner("Please wait while your image is being generated..."):
            openai = oai.Openai()
            prompt_wo_hashtags = re.sub("#[A-Za-z0-9_]+", "", prompt)
            processing_prompt = (
                "Create a detailed but brief description of an image that captures "
                f"the essence of the following text:\n{prompt_wo_hashtags}\n\n"
            )
            processed_prompt = (
                openai.complete(
                    prompt=processing_prompt, temperature=0.5, max_tokens=40
                )
                .strip()
                .replace('"', "")
                .split(".")[0]
                + "."
            )
            logging.info(f"Tweet: {prompt}\n" f"Image prompt: {processed_prompt}")
            st.session_state.image = openai.image(processed_prompt)


# Render Streamlit page
st.set_page_config(page_title="Tweet", page_icon="🤖")
if "tweet" not in st.session_state:
    st.session_state.tweet = ""
if "image" not in st.session_state:
    st.session_state.image = ""
if "text_error" not in st.session_state:
    st.session_state.text_error = ""
if "image_error" not in st.session_state:
    st.session_state.image_error = ""
if "feeling_lucky" not in st.session_state:
    st.session_state.feeling_lucky = False

st.title("Generate Tweets")
st.markdown(
    "This mini-app generates Tweets using OpenAI's GPT-3 based [Davinci model](https://beta.openai.com/docs/models/overview) for texts and [DALL·E](https://beta.openai.com/docs/guides/images) for images. You can find the code on [GitHub](https://github.com/kinosal/tweet) and the author on [Twitter](https://twitter.com/kinosal)."
)

topic = st.text_input(label="Topic (or hashtag)", placeholder="AI")
mood = st.text_input(
    label="Mood (e.g. inspirational, funny, serious) (optional)",
    placeholder="inspirational",
)
style = st.text_input(
    label="Twitter account handle to style-copy recent Tweets (optional)",
    placeholder="elonmusk",
)
# Force responsive layout for columns also on mobile
st.write(
    '''<style>
    [data-testid="column"] {
        width: calc(50% - 1rem);
        flex: 1 1 calc(50% - 1rem);
        min-width: calc(50% - 1rem);
    }
    </style>''',
    unsafe_allow_html=True
)
col1, col2 = st.columns(2)
with col1:
    st.session_state.feeling_lucky = not st.button(
        label="Generate text",
        type="primary",
        on_click=generate_text,
        args=(topic, mood, style),
    )
with col2:
    with open("moods.txt") as f:
        sample_moods = f.read().splitlines()
    st.session_state.feeling_lucky = st.button(
        label="Feeling lucky",
        type="secondary",
        on_click=generate_text,
        args=("an interesting topic", random.choice(sample_moods), ""),
    )

text_spinner_placeholder = st.empty()
if st.session_state.text_error:
    st.error(st.session_state.text_error)

if st.session_state.tweet:
    st.markdown("""---""")
    st.text_area(label="Tweet", value=st.session_state.tweet, height=100)
    col1, col2 = st.columns(2)
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
                label="Regenerate text",
                type="secondary",
                on_click=generate_text,
                args=("an interesting topic", random.choice(sample_moods), ""),
            )
        else:
            st.button(
                label="Regenerate text",
                type="secondary",
                on_click=generate_text,
                args=(topic, mood, style),
            )

    if not st.session_state.image:
        st.button(
            label="Generate image",
            type="primary",
            on_click=generate_image,
            args=[st.session_state.tweet],
        )
    else:
        st.image(st.session_state.image)
        st.button(
            label="Regenerate image",
            type="secondary",
            on_click=generate_image,
            args=[st.session_state.tweet],
        )

    image_spinner_placeholder = st.empty()
    if st.session_state.image_error:
        st.error(st.session_state.image_error)

    st.markdown("""---""")
    st.markdown("**Other Streamlit apps by [@kinosal](https://twitter.com/kinosal)**")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("[Content Summarizer](https://web-summarizer.streamlit.app)")
    with col2:
        st.markdown(
            "[Code Translator](https://english-to-code.streamlit.app)"
        )
    with col3:
        st.markdown("[PDF Analyzer](https://pdf-keywords.streamlit.app)")
