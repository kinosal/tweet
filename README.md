# Tweet Generation with OpenAI GPT-3

Live version of this app at [tweets.streamlit.app](https://tweets.streamlit.app)

## Description

This [Streamlit](https://streamlit.io) mini-app generates Tweet texts using OpenAI's GPT-3 based [Davinci model](https://beta.openai.com/docs/models/overview) for texts and [DALL·E](https://beta.openai.com/docs/guides/images) for images.

The text prompt creation form accepts a topic as well as an optional mood parameter and a Twitter account for "style-transfer". The app then generates a prompt with an instruction to write a respective Tweet and sends this to the OpenAI API which - using the GPT-3 Davinci engine that has been trained on a lot of publicly available text content - predicts the next likely to be used (word) tokens and thus generates the Tweet content. Furthermore, the app can request and display an image from OpenAI's DALL·E model using the previously generated Tweet text as a prompt.

## Quick Start
### Dependencies Installation
```buildoutcfg
# execute below commands under root dir
# create a virtual env
$ python3.10 -m venv venv

# activate virtual env
$ source venv/bin/activate

# upgrade pip
$ pip install --upgrade pip

# install poetry
$ pip install poetry 

# install dependencies
$ poetry install 
```
### Local Dev
```
# please pass in env variables before run below command
$ streamlit run app.py
```

