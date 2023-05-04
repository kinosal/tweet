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


def create_image_prompt(product_name: str, visual_features: str, prompt_number=2) -> str:
    """create prompts for Midjourney
    Args:
        product_name (str): name for the content breif
        visual_features (str): visual features in content brief
    Returns:
        str: Description 1... Description 2...
    """

    prompt = "I am promoting a product called {}. I need to have these visual features in my pictures: {}. \
                Can you give me {} example descriptions of images that would fit those visual features? \
                Please format the response as \"Description 1: ...; Description 2:...\"".format(product_name, visual_features, prompt_number)
    openai = oai.Openai()
    st.session_state.text_error = ""
    st.session_state.mood_board = (
        openai.complete(prompt, "gpt-3.5-turbo", temperature=0.2).strip().replace('"', "")
    )
    # logging.info(
    #     f"Descriptions: {st.session_state.mood_board}"
    # )

def generate_content_post_prompt(content_brief, network_type, guideline):
    prompt = '''
    I want to get a prompt that starts with "please write a prompt ~" to chatgpt to generate the post text.
    Please write a prompt for generating an {} post based on the given this text {} and this info {}, 
    the required hashtags from info must be included and no more than 200 words! 
    '''.format(network_type, content_brief, guideline)

    openai = oai.Openai()
    st.session_state.text_error = ""
    st.session_state.content_post = (
        openai.complete(prompt, "gpt-3.5-turbo").strip().replace('"', "")
    )
    # logging.info(
    #     f"Prompts Descriptions: {st.session_state.content_post}"
    # )


def generate_post_text(content_post, network_type):
    if network_type == "":
        st.session_state.text_error = "Please enter a network_type"
        return

    prompt = '''Please write realistic {} post text with required hashtags and emojis based on this information {}. 
        no more than 100 words!'''.format(network_type, content_post)
    openai = oai.Openai()
    st.session_state.text_error = ""
    st.session_state.post_text = (
        openai.complete(prompt, "gpt-3.5-turbo").strip().replace('"', "")
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

if "mood_board" not in st.session_state:
    st.session_state.mood_board = ""
if "content_post" not in st.session_state:
    st.session_state.content_post = ""
if "post_text" not in st.session_state:
    st.session_state.post_text = ""
if "image" not in st.session_state:
    st.session_state.image = ""
if "text_error" not in st.session_state:
    st.session_state.text_error = ""
if "image_error" not in st.session_state:
    st.session_state.image_error = ""
if "feeling_lucky" not in st.session_state:
    st.session_state.feeling_lucky = False
if "content_post_btn" not in st.session_state:
    st.session_state.content_post_btn = False
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
# Mood Board
st.title("Generate Mood Board Prompts")
product_name = st.text_input(label="Product Name")
campaign_overview = st.text_area(label="Campaign Overview", height=100)
col1, = st.columns(1)
with col1:
    st.session_state.feeling_lucky = not st.button(
        label="Generate Mood Board",
        type="primary",
        on_click=create_image_prompt,
        args=(product_name, campaign_overview),
    )

if st.session_state.mood_board:
    st.markdown("""---""")
    st.text_area(label="Mood Board", value=st.session_state.mood_board, height=150)

    image_spinner_placeholder = st.empty()
    if st.session_state.image_error:
        st.error(st.session_state.image_error)

    st.markdown("""---""")

# Content Post
st.title("Generate Content Post Prompts")
network_type = st.text_input(label="Network Type")
content_brief = st.text_area(label="Content Brief", height=100)
guideline = st.text_area(label="Guideline", height=100)
col1, = st.columns(1)
with col1:
    st.session_state.content_post_btn    = not st.button(
        label="Generate Content Post",
        type="primary",
        on_click=generate_content_post_prompt,
        args=(content_brief, network_type, guideline),
    )

if st.session_state.content_post:
    st.markdown("""---""")
    st.text_area(label="Content Post", value=st.session_state.content_post, height=150)

# Post Text
if st.session_state.content_post:
    st.title("Generate Post Text Prompts")
    col1, = st.columns(1)
    with col1:
        st.session_state.feeling_lucky = not st.button(
            label="Generate Post Text",
            type="primary",
            on_click=generate_post_text,
            args=(st.session_state.content_post, network_type),
        )

    if st.session_state.post_text:
        st.markdown("""---""")
        st.text_area(label="Post Text", value=st.session_state.post_text, height=150)

text_spinner_placeholder = st.empty()
if st.session_state.text_error:
    st.error(st.session_state.text_error)
