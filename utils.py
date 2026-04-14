import google.generativeai as genai
import streamlit as st
import os

# -------------------------------
# SECRET HANDLER
# -------------------------------
def get_secret(key):
    return os.getenv(key) or st.secrets.get(key)

genai.configure(api_key=get_secret("GEMINI_API_KEY"))

# -------------------------------
# IMAGE → FOOD (GEMINI)
# -------------------------------
def detect_food(image_file):
    model = genai.GenerativeModel("gemini-1.5-flash")

    image_bytes = image_file.read()

    response = model.generate_content([
        "Identify the food in this image. Return only a simple food name.",
        {"mime_type": "image/jpeg", "data": image_bytes}
    ])

    return response.text.strip()
