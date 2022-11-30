# Tweet Generation with OpenAI GPT-3

Live version of this app at [tweets.streamlit.app](https://tweets.streamlit.app)

## Description

This [Streamlit](https://streamlit.io) mini-app generates Tweet texts using [OpenAI's GPT-3 based Davinci model](https://beta.openai.com/docs/models/overview).

The prompt creation form accepts a topic as well as an optional mood parameter and a Twitter account for "style-transfer". The app then generates a text prompt with an instruction to write a respective Tweet and sends this to the OpenAI API which - using the GPT-3 Davinci engine that has been trained on a lot of publicly available text content - predicts the next likely to be used (word) tokens and thus generates the Tweet content.

## Contribution

I hope this will be of value to people seeking to understand GPT-3's current capabilities and the overall progress of natural language processing (NLP) and generative AI. Plus maybe you can even use the app to generate some interesting Tweets for your Twitter account.

Please reach out to me at nikolas@schriefer.me with any feedback - especially suggestions to improve this - or questions you might have.