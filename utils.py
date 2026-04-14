import base64
import requests
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
                    {"type": "text", "text": "Identify the food in this image. Give only the food name."},
                    {
                        "type": "image_url",
                        "image_url": f"data:image/jpeg;base64,{base64_image}"
                    }
                ]
            }
        ]
    )

    food_name = response.choices[0].message.content.strip()
    return food_name


# -------------------------------
# CLEAN FOOD NAME
# -------------------------------
def clean_food_name(food_name):
    return food_name.lower().replace("\n", "").strip()


# -------------------------------
# GET NUTRITION DATA
# -------------------------------
def get_nutrition(food_name):
    url = "https://api.edamam.com/api/nutrition-data"

    params = {
        "app_id": os.getenv("EDAMAM_APP_ID"),
        "app_key": os.getenv("EDAMAM_APP_KEY"),
        "ingr": food_name
    }

    response = requests.get(url, params=params)
    return response.json()
