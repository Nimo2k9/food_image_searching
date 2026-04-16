import streamlit as st
from PIL import Image
from utils import detect_food, get_nutrition

st.set_page_config(page_title="🍱 Food Analyzer", layout="centered")

st.title("🍱 AI Food Nutrition Analyzer")
st.caption("⚡ Fast • Free • Production Ready")

uploaded_file = st.file_uploader("Upload Food Image", type=["jpg","jpeg","png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    image = image.resize((256, 256))  # 🔥 speed optimization
    st.image(image)

    if st.button("Analyze Food"):

        uploaded_file.seek(0)

        with st.spinner("🔍 Detecting food..."):
            food = detect_food(uploaded_file)

        # Fallback if AI fails
        if food == "error":
            st.warning("⚠️ AI failed. Enter food manually.")
            food = st.text_input("Enter food name (e.g., rice, egg, chicken)")

        if food:
            st.success(f"🍽 Food: {food}")

            with st.spinner("📊 Getting nutrition..."):
                nutrition = get_nutrition(food)

            if nutrition:
                col1, col2, col3, col4 = st.columns(4)

                col1.metric("Calories", int(nutrition["Calories"]))
                col2.metric("Protein", int(nutrition["Protein"]))
                col3.metric("Fat", int(nutrition["Fat"]))
                col4.metric("Carbs", int(nutrition["Carbs"]))

            else:
                st.error("❌ Nutrition data not found")
