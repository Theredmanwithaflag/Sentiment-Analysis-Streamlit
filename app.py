import streamlit as st
import requests
import pandas as pd
import openai
import time
import re

openai.api_key = 'sk-proj-hKIXeiDyX7vcEjLqbSvvT3BlbkFJkq0AzheVfzFHKmiA2W2s'

# Function to get a response from OpenAI ChatGPT API
def get_chatgpt_response(prompt, model="gpt-3.5-turbo"):
    """
    Function to get a response from OpenAI ChatGPT API.
    Args:
    - prompt: The prompt to be sent to the API.
    - model: The model version to be used (default: "gpt-3.5-turbo").

    Returns:
    - response: The response text from the model.
    """
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]

    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        st.error(f"Error: {e}")
        return None

def get_sentiment_analysis(text):
    prompt = f"""
    Classify the sentiment of the following Persian text into one of five classes: Very Positive, Positive, Neutral, Negative, Very Negative.
    
    ---Example 1---
    Text: با وجود تمام تلاش‌هایمان، نتیجه آن چیزی نشد که انتظار داشتیم.
    Answer: منفی

    ---Example 2---
    Text: روز فوق‌العاده‌ای بود و همه چیز دقیقاً همانطور که برنامه‌ریزی کرده بودیم پیش رفت.
    Answer: بسیار مثبت

    Text: \"{text}\"
    Answer:
    """
    sentiment = get_chatgpt_response(prompt)
    if sentiment is not None:
        return sentiment.strip()
    else:
        return "Error in sentiment analysis"

# Streamlit UI
st.markdown('<h1 style="text-align: right;">تحلیل احساسات با استفاده از پردازش زبان طبیعی</h1>', unsafe_allow_html=True)
st.markdown('<div dir="rtl">تحلیل احساسات در پنج دسته‌ی بسیار مثبت، مثبت، خنثی، منفی، بسیار منفی</div>', unsafe_allow_html=True)

# Text input area with RTL direction
st.markdown('<div dir="rtl" style="text-align: right;">متن خود را در اینجا وارد کنید:</div>', unsafe_allow_html=True)
text_input = st.text_area('', '')

# Sentiment distribution initialization
if 'distribution' not in st.session_state:
    st.session_state.distribution = [0, 0, 0, 0, 0]

if st.button('انجام تحلیل'):
    if text_input:
        sentiment = get_sentiment_analysis(text_input)
        st.markdown(f'<div dir="rtl">Sentiment: **{sentiment}**</div>', unsafe_allow_html=True)
        
        # Update distribution
        if sentiment == 'Very Positive':
            st.session_state.distribution[0] += 1
        elif sentiment == 'Positive':
            st.session_state.distribution[1] += 1
        elif sentiment == 'Neutral':
            st.session_state.distribution[2] += 1
        elif sentiment == 'Negative':
            st.session_state.distribution[3] += 1
        elif sentiment == 'Very Negative':
            st.session_state.distribution[4] += 1
    else:
        st.markdown('<div dir="rtl" style="color: red;">لطفاً متنی برای تحلیل وارد کنید.</div>', unsafe_allow_html=True)

# # Display sentiment distribution
# st.write('Sentiment Distribution:')
# st.bar_chart({
#     'Sentiment': ['Very Positive', 'Positive', 'Neutral', 'Negative', 'Very Negative'],
#     'Count': st.session_state.distribution
# })

# Run the app with `streamlit run sentiment_analysis_app.py`
