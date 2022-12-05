"""OpenAI API connector."""

# Import from standard library
import os
import logging

# Import from 3rd party libraries
import openai
import streamlit as st

# Assign credentials from environment variable or streamlit secrets dict
openai.api_key = os.getenv("OPENAI_API_KEY") or st.secrets["OPENAI_API_KEY"]

# Suppress openai request/response logging
# Handle by manually changing the respective APIRequestor methods in the openai package
# Does not work hosted on Streamlit since all packages are re-installed by Poetry
# Alternatively (affects all messages from this logger):
logging.getLogger("openai").setLevel(logging.WARNING)


class Openai:
    """OpenAI Connector."""

    @staticmethod
    def moderate(prompt: str) -> bool:
        """Call OpenAI GPT Moderation with text prompt.
        Args:
            prompt: text prompt
        Return: boolean if flagged
        """
        try:
            response = openai.Moderation.create(prompt)
            return response["results"][0]["flagged"]

        except Exception as e:
            logging.error(f"OpenAI API error: {e}")
            st.session_state.text_error = f"OpenAI API error: {e}"

    @staticmethod
    def complete(prompt: str, temperature: float = 0.9, max_tokens: int = 50) -> str:
        """Call OpenAI GPT Completion with text prompt.
        Args:
            prompt: text prompt
        Return: predicted response text
        """
        kwargs = {
            "engine": "text-davinci-003",
            "prompt": prompt,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": 1,  # default
            "frequency_penalty": 0,  # default,
            "presence_penalty": 0,  # default
        }
        try:
            response = openai.Completion.create(**kwargs)
            return response["choices"][0]["text"]

        except Exception as e:
            logging.error(f"OpenAI API error: {e}")
            st.session_state.text_error = f"OpenAI API error: {e}"

    @staticmethod
    def image(prompt: str) -> str:
        """Call OpenAI Image Create with text prompt.
        Args:
            prompt: text prompt
        Return: image url
        """
        try:
            response = openai.Image.create(
                prompt=prompt,
                n=1,
                size="512x512",
                response_format="url",
            )
            return response["data"][0]["url"]

        except Exception as e:
            logging.error(f"OpenAI API error: {e}")
            st.session_state.image_error = f"OpenAI API error: {e}"
