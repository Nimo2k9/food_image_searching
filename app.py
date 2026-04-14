import streamlit as st
from PIL import Image
from utils import detect_food, get_nutrition, clean_food_name

st.set_page_config(page_title="🍱 Food Nutrition Analyzer", layout="centered")

st.title("🍱 AI Food Nutrition Analyzer (FREE)")
st.write("Upload a food image to get nutrition details")

uploaded_file = st.file_uploader("Upload Food Image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Open image
    image = Image.open(uploaded_file)

    # Resize image (VERY IMPORTANT FIX)
    image = image.resize((512, 512))

    st.image(image, caption="Uploaded Image", use_column_width=True)

    if st.button("Analyze Food"):

        # Reset file pointer before reading
        uploaded_file.seek(0)

        with st.spinner("🔍 Detecting food..."):
            food_name = detect_food(uploaded_file)
            food_name = clean_food_name(food_name)

        # Debug (optional - remove later)
        st.write("DEBUG:", food_name)

        # If AI fails → fallback
        if "error" in food_name.lower():
            st.warning("⚠️ AI detection failed. Please enter food manually.")
            food_name = st.text_input("Enter food name (e.g., apple, rice, chicken)")

        if food_name:
            st.success(f"🍽 Detected: {food_name}")

            with st.spinner("📊 Getting nutrition data..."):
                nutrition = get_nutrition(food_name)

            if "error" not in nutrition:
                col1, col2, col3, col4 = st.columns(4)

                col1.metric("Calories", nutrition["Calories"])
                col2.metric("Protein", nutrition["Protein"])
                col3.metric("Fat", nutrition["Fat"])
                col4.metric("Carbs", nutrition["Carbs"])

            else:
                st.error("❌ No nutrition data found")
