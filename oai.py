"""OpenAI API connector."""

# Import from standard library
import os
import logging

# Import from 3rd party libraries
import openai
import streamlit as st

# Instantiate OpenAI with credentials from environment or streamlit secrets
openai_key = os.getenv("OPENAI_API_KEY") or st.secrets["OPENAI_API_KEY"]
client = openai.OpenAI(api_key=openai_key)

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
            response = client.moderations.create(input=prompt)
            return response.results[0].flagged

        except Exception as e:
            logging.error(f"OpenAI API error: {e}")
            st.session_state.text_error = f"OpenAI API error: {e}"

    @staticmethod
    def complete(
        prompt: str,
        model: str = "gpt-3.5-turbo",
        temperature: float = 0.9,
        max_tokens: int = 50,
    ) -> str:
        """Call OpenAI GPT Completion with text prompt.
        Args:
            prompt: text prompt
            model: OpenAI model name, e.g. "gpt-3.5-turbo"
            temperature: float between 0 and 1
            max_tokens: int between 1 and 2048
        Return: predicted response text
        """
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content

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
            response = client.images.generate(
                prompt=prompt,
                model="dall-e-3",
                quality="standard",
                n=1,
                size="1024x1024",
            )
            return response.data[0].url

        except Exception as e:
            logging.error(f"OpenAI API error: {e}")
            st.session_state.image_error = f"OpenAI API error: {e}"
