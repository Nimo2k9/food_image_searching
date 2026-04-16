import requests
import os
import streamlit as st
import google.generativeai as genai

# -------------------------------
# SECRET HANDLER
# -------------------------------
def get_secret(key):
    return os.getenv(key) or st.secrets.get(key)

genai.configure(api_key=get_secret("GEMINI_API_KEY"))

# -------------------------------
# FAST SINGLE FOOD DETECTION
# -------------------------------
def detect_food(image_file):
    try:
        model = genai.GenerativeModel("gemini-3.1-flash-lite-preview")

        image_file.seek(0)
        image_bytes = image_file.read()

        response = model.generate_content(
            [
                "Identify the main food in this image. Return ONLY one simple food name like 'apple', 'rice', or 'chicken curry'.",
                {
                    "mime_type": image_file.type,
                    "data": image_bytes
                }
            ],
            request_options={"timeout": 8}   # 🔥 prevents hanging
        )

        if not response.text:
            return "error"

        return response.text.strip().lower()

    except:
        return "error"


# -------------------------------
# USDA WITH TIMEOUT
# -------------------------------
@st.cache_data(show_spinner=False)
def get_nutrition(food):
    try:
        api_key = get_secret("USDA_API_KEY")

        url = "https://api.nal.usda.gov/fdc/v1/foods/search"

        params = {
            "query": food,
            "api_key": api_key
        }

        response = requests.get(url, params=params, timeout=5)
        data = response.json()

        foods = data.get("foods")
        if not foods:
            return None

        nutrients = foods[0].get("foodNutrients", [])

        result = {
            "Calories": 0,
            "Protein": 0,
            "Fat": 0,
            "Carbs": 0
        }

        for n in nutrients:
            name = n.get("nutrientName", "").lower()

            if "energy" in name:
                result["Calories"] = n.get("value", 0)
            elif "protein" in name:
                result["Protein"] = n.get("value", 0)
            elif "fat" in name:
                result["Fat"] = n.get("value", 0)
            elif "carbohydrate" in name:
                result["Carbs"] = n.get("value", 0)

        return result

    except:
        return None
