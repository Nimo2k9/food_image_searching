import requests
import os
import streamlit as st
import google.generativeai as genai

# -------------------------------
# SECRET HANDLER
# -------------------------------
def get_secret(key):
    return os.getenv(key) or st.secrets.get(key)


# -------------------------------
# CONFIGURE GEMINI
# -------------------------------
genai.configure(api_key=get_secret("GEMINI_API_KEY"))


# -------------------------------
# IMAGE → FOOD NAME
# -------------------------------
def detect_food(image_file):
    try:
        model = genai.GenerativeModel("gemini-3-pro")

        image_bytes = image_file.read()

        response = model.generate_content([
            "Identify the food in this image. Return only a simple food name.",
            {
                "mime_type": "image/jpeg",
                "data": image_bytes
            }
        ])

        return response.text.strip()

    except Exception as e:
        return f"Error: {str(e)}"


# -------------------------------
# CLEAN FOOD NAME
# -------------------------------
def clean_food_name(food_name):
    return food_name.lower().strip()


# -------------------------------
# USDA NUTRITION
# -------------------------------
def get_nutrition(food_name):
    try:
        api_key = get_secret("USDA_API_KEY")

        url = "https://api.nal.usda.gov/fdc/v1/foods/search"

        params = {
            "query": food_name,
            "api_key": api_key
        }

        response = requests.get(url, params=params)
        data = response.json()

        foods = data.get("foods")

        if not foods:
            return {"error": "No food found"}

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

    except Exception as e:
        return {"error": str(e)}
