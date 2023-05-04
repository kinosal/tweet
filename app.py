"""Streamlit app to generate Tweets."""

# Import from standard library
import logging
import random
import re

# Import from 3rd party libraries
import streamlit as st
import streamlit.components.v1 as components

# Import modules
import tweets as twe
import oai

# Configure logger
logging.basicConfig(format="\n%(asctime)s\n%(message)s", level=logging.INFO, force=True)


# Define functions
def generate_text(topic: str):
    """Generate Tweet text."""
    if st.session_state.n_requests >= 5:
        st.session_state.text_error = "Too many requests. Please wait a few seconds before generating another Tweet."
        logging.info(f"Session request limit reached: {st.session_state.n_requests}")
        st.session_state.n_requests = 1
        return

    st.session_state.tweet = ""
    st.session_state.image = ""
    st.session_state.text_error = ""

    if not topic:
        st.session_state.text_error = "Please enter a topic"
        return

    with text_spinner_placeholder:
        with st.spinner("Please wait while your Tweet is being generated..."):

            prompt = f"Write a post on social media about {topic} in less than 120 characters:\n\n"
            openai = oai.Openai()
            flagged = openai.moderate(prompt)
            if flagged:
                st.session_state.text_error = "Input flagged as inappropriate."
                logging.info(f"Topic: {topic}\n")
                return

            else:
                st.session_state.text_error = ""
                st.session_state.n_requests += 1
                st.session_state.tweet = (
                    openai.complete(prompt).strip().replace('"', "")
                )
                logging.info(
                    f"Topic: {topic}\n"
                    f"Tweet: {st.session_state.tweet}"
                )


def generate_image(prompt: str):
    """Generate Tweet image."""
    if st.session_state.n_requests >= 5:
        st.session_state.text_error = "Too many requests. Please wait a few seconds before generating another text or image."
        logging.info(f"Session request limit reached: {st.session_state.n_requests}")
        st.session_state.n_requests = 1
        return

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
            st.session_state.n_requests += 1
            st.session_state.image = openai.image(processed_prompt)
            logging.info(f"Tweet: {prompt}\nImage prompt: {processed_prompt}")


# Configure Streamlit page and state
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
if "n_requests" not in st.session_state:
    st.session_state.n_requests = 0

# render logo
col1, col2, col3 = st.columns(3)
with col1:
    st.write(' ')
with col2:
    st.image("./assets/hack.jpg")
with col3:
    st.write(' ')

# Render Streamlit page
st.title("Generate Tweets")

topic = st.text_input(label="Topic (or hashtag)", placeholder="AI")
col1, = st.columns(1)
with col1:
    st.session_state.feeling_lucky = not st.button(
        label="Generate text",
        type="primary",
        on_click=generate_text,
        args=(topic,),
    )

text_spinner_placeholder = st.empty()
if st.session_state.text_error:
    st.error(st.session_state.text_error)

if st.session_state.tweet:
    st.markdown("""---""")
    st.text_area(label="Post", value=st.session_state.tweet, height=100)

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
