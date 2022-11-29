"""OpenAI API connector."""

# Import from standard library
import os

# Import from 3rd party libraries
import openai
import streamlit as st

# Assign credentials from environment variable or streamlit secrets dict
openai.api_key = os.getenv("OPENAI_API_KEY") or st.secrets["OPENAI_API_KEY"]


class Openai:
    """OpenAI Connector."""

    @staticmethod
    def call(prompt: str) -> str:
        """Call OpenAI GPT with text prompt.
        Args:
            prompt: text prompt
        Return: predicted response text
        """
        kwargs = {
            "engine": "text-davinci-003",
            "prompt": prompt,
            "temperature": 0.9,
            "max_tokens": 50,
            "top_p": 1,
            "frequency_penalty": 0,
            "presence_penalty": 0,
        }
        response = openai.Completion.create(**kwargs)
        return response["choices"][0]["text"]
