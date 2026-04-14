import base64
import requests
import os
import streamlit as st
from openai import OpenAI

# -------------------------------
# SAFE SECRET HANDLER
# -------------------------------
def get_secret(key):
    return os.getenv(key) or st.secrets.get(key)

client = OpenAI(api_key=get_secret("OPENAI_API_KEY"))

# -------------------------------
# IMAGE → FOOD NAME
# -------------------------------
def detect_food(image_file):
    image_bytes = image_file.read()
    base64_image = base64.b64encode(image_bytes).decode()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Identify the food in this image. Return a simple food name (e.g., 'apple', 'chicken biryani')."},
                    {
                        "type": "image_url",
                        "image_url": f"data:image/jpeg;base64,{base64_image}"
                    }
                ]
            }
        ]
    )

    return response.choices[0].message.content.strip()


# -------------------------------
# CLEAN FOOD NAME
# -------------------------------
def clean_food_name(food_name):
    return food_name.lower().replace("\n", "").strip()


# -------------------------------
# USDA NUTRITION FUNCTION
# -------------------------------
def get_nutrition(food_name):
    API_KEY = get_secret("USDA_API_KEY")

    url = "https://api.nal.usda.gov/fdc/v1/foods/search"

    params = {
        "query": food_name,
        "api_key": API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    try:
        food = data['foods'][0]

        nutrients = food['foodNutrients']

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

    except:
        return {"error": "No nutrition data found"}
