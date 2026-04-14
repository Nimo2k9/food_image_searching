import streamlit as st
from PIL import Image
from utils import detect_food, get_nutrition, clean_food_name

st.title("🍱 AI Food Nutrition Analyzer (FREE VERSION)")

uploaded_file = st.file_uploader("Upload Food Image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image")

    if st.button("Analyze"):
        with st.spinner("🔍 Detecting food..."):
            food_name = detect_food(uploaded_file)
            food_name = clean_food_name(food_name)

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
