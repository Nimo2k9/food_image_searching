import base64
import requests
import os
import streamlit as st
import google.generativeai as genai

# -------------------------------
# SECRET HANDLER (WORKS LOCAL + CLOUD)
# -------------------------------
def get_secret(key):
    return os.getenv(key) or st.secrets.get(key)


# -------------------------------
# CONFIGURE GEMINI
# -------------------------------
genai.configure(api_key=get_secret("GEMINI_API_KEY"))


# -------------------------------
# IMAGE → FOOD NAME (GEMINI)
# -------------------------------
def detect_food(image_file):
    try:
       model = genai.GenerativeModel("gemini-1.5-flash-latest")
        # Read image
        image_bytes = image_file.read()

        # Send to Gemini
        response = model.generate_content([
            "Identify the food in this image. "
            "Return only a simple, common food name suitable for nutrition lookup "
            "(e.g., 'apple', 'boiled rice', 'chicken curry').",
            {
                "mime_type": "image/jpeg",
                "data": image_bytes
            }
        ])

        # Extract response
        food_name = response.text.strip()

        return food_name

    except Exception as e:
        return f"Error: {str(e)}"


# -------------------------------
# CLEAN FOOD NAME
# -------------------------------
def clean_food_name(food_name):
    return food_name.lower().replace("\n", "").strip()


# -------------------------------
# USDA NUTRITION FUNCTION (FREE)
# -------------------------------
def get_nutrition(food_name):
    try:
        API_KEY = get_secret("USDA_API_KEY")

        url = "https://api.nal.usda.gov/fdc/v1/foods/search"

        params = {
            "query": food_name,
            "api_key": API_KEY
        }

        response = requests.get(url, params=params)
        data = response.json()

        foods = data.get("foods")

        if not foods:
            return {"error": "No food found"}

        food = foods[0]
        nutrients = food.get("foodNutrients", [])

        # Default values
        nutrition_data = {
            "Calories": 0,
            "Protein": 0,
            "Fat": 0,
            "Carbs": 0
        }

        for n in nutrients:
            name = n.get("nutrientName", "").lower()

            if "energy" in name:
                nutrition_data["Calories"] = n.get("value", 0)
            elif "protein" in name:
                nutrition_data["Protein"] = n.get("value", 0)
            elif "fat" in name:
                nutrition_data["Fat"] = n.get("value", 0)
            elif "carbohydrate" in name:
                nutrition_data["Carbs"] = n.get("value", 0)

        return nutrition_data

    except Exception as e:
        return {"error": str(e)}
