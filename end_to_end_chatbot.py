# -*- coding: utf-8 -*-
"""End_to_End_Chatbot.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/gaurika05/End_to_end_Chatbot/blob/main/End_to_End_Chatbot.ipynb
"""

import os
import nltk
import ssl
import streamlit as st
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

ssl._create_default_https_context = ssl._create_unverified_context
nltk.data.path.append(os.path.abspath("nltk_data"))
nltk.download('punkt')

intents = [
    {
        "tag": "greeting",
        "patterns": ["Hi", "Hello", "Hey"],
        "responses": ["Hi, I am a chatbot and my purpose is to assist you. ", "Hello, I am a chatbot and I am here to assist you. ", "Hi, How can I help you?"]
    },
    {
        "tag": "problems",
        "patterns": ["The delivered item is damaged.", "I have received a wrong item or order", "I have not received my order."],
        "responses": ["We are truly sorry for the inconvenience. Please share your order id on this WhatsApp no. +91xxxxxxxxxx."]
    },
    {
        "tag": "damage issue",
        "patterns": ["The delivered item is damaged"],
        "responses": ["Sorry for the inconvenience caused. Please share the photo of the damaged item on this WhatsApp no. +91xxxxxxxxxx"]
    },
    {
        "tag": "thanks",
        "patterns": ["Thank you", "Thanks", "Thanks a lot", "I appreciate it", "I am grateful", "Thanks for your help"],
        "responses": ["Thank you.\n I Hope all your queries are resolved.\n Have a great day.", "Thank you", "thanks"]
    },
    {
        "tag": "help",
        "patterns": ["Help", "I need help", "Can you help me?", "What should I do?"],
        "responses": ["Sure, what do you need help with?", "I'm here to help. What's the problem?", "How can I assist you?"]
    }
]

# Create the vectorizer and classifier
vectorizer = TfidfVectorizer()
clf = LogisticRegression(random_state=0, max_iter=10000)

# Preprocess the data
tags = []
patterns = []
for intent in intents:
    for pattern in intent['patterns']:
        tags.append(intent['tag'])
        patterns.append(pattern)

# training the model
x = vectorizer.fit_transform(patterns)
y = tags
clf.fit(x, y)

def chatbot(input_text):
    input_text = vectorizer.transform([input_text])
    tag = clf.predict(input_text)[0]
    for intent in intents:
        if intent['tag'] == tag:
            response = random.choice(intent['responses'])
            return response

counter = 0

def main():
    global counter
    st.title("Chatbot")
    st.write("Welcome to the chatbot. Please type a message and press Enter to start the conversation.")

    counter += 1
    user_input = st.text_input("You:", key=f"user_input_{counter}")

    if user_input:
        response = chatbot(user_input)
        st.text_area("Chatbot:", value=response, height=100, max_chars=None, key=f"chatbot_response_{counter}")

        if response.lower() in ['thank you', 'thanks']:
            st.write("Thank you for chatting with me. Have a great day!")
            st.stop()

if __name__ == '__main__':
    main()
