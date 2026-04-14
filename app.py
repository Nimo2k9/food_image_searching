import streamlit as st
from PIL import Image
from utils import detect_food, get_nutrition, clean_food_name

st.set_page_config(page_title="Food Nutrition Analyzer", layout="centered")

st.title("🍱 AI Food Nutrition Analyzer")
st.write("Upload a food image to get nutrition details")

uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)

    st.image(image, caption="Uploaded Image", use_column_width=True)

    if st.button("Analyze Food"):
        with st.spinner("🔍 Detecting food..."):
            food_name = detect_food(uploaded_file)
            food_name = clean_food_name(food_name)

        st.success(f"🍽 Detected: {food_name}")

        with st.spinner("📊 Fetching nutrition data..."):
            nutrition = get_nutrition(food_name)

        # -------------------------------
        # DISPLAY RESULTS
        # -------------------------------
        st.subheader("📊 Nutrition Info")

        if "calories" in nutrition:
            col1, col2, col3 = st.columns(3)

            col1.metric("Calories", round(nutrition.get("calories", 0), 2))
            col2.metric("Protein", round(nutrition["totalNutrients"].get("PROCNT", {}).get("quantity", 0), 2))
            col3.metric("Fat", round(nutrition["totalNutrients"].get("FAT", {}).get("quantity", 0), 2))

            st.subheader("🍽 Detailed Nutrients")

            nutrients = nutrition.get("totalNutrients", {})

            for key, value in nutrients.items():
                st.write(f"{value['label']}: {round(value['quantity'],2)} {value['unit']}")

        else:
            st.error("❌ Could not fetch nutrition data. Try a clearer image.")
