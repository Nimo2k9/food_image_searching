import streamlit as st
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt

from utils import detect_food, get_nutrition

st.set_page_config(page_title="🍱 Food Analyzer", layout="centered")

st.title("🍱 AI Food Nutrition Analyzer + Tracker")
st.caption("⚡ Fast • Free • Production Ready")

# -------------------------------
# SESSION STATE INIT
# -------------------------------
if "log" not in st.session_state:
    st.session_state.log = []

if "current_food" not in st.session_state:
    st.session_state.current_food = None

if "current_nutrition" not in st.session_state:
    st.session_state.current_nutrition = None


# -------------------------------
# IMAGE INPUT
# -------------------------------
uploaded_file = st.file_uploader("Upload Food Image", type=["jpg","jpeg","png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    image = image.resize((256, 256))
    st.image(image)

    # -------------------------------
    # ANALYZE BUTTON
    # -------------------------------
    if st.button("Analyze Food"):
        uploaded_file.seek(0)

        with st.spinner("🔍 Detecting food..."):
            food = detect_food(uploaded_file)

        # fallback
        if food == "error":
            st.warning("⚠️ AI failed. Enter manually.")
            food = st.text_input("Enter food name")

        if food:
            with st.spinner("📊 Getting nutrition..."):
                nutrition = get_nutrition(food)

            if nutrition:
                # ✅ store in session
                st.session_state.current_food = food
                st.session_state.current_nutrition = nutrition
            else:
                st.error("❌ Nutrition not found")


# -------------------------------
# DISPLAY CURRENT FOOD
# -------------------------------
if st.session_state.current_food and st.session_state.current_nutrition:

    food = st.session_state.current_food
    nutrition = st.session_state.current_nutrition

    st.success(f"🍽 Food: {food}")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Calories", int(nutrition["Calories"]))
    col2.metric("Protein", int(nutrition["Protein"]))
    col3.metric("Fat", int(nutrition["Fat"]))
    col4.metric("Carbs", int(nutrition["Carbs"]))

    # -------------------------------
    # ADD TO LOG BUTTON (FIXED)
    # -------------------------------
    if st.button("➕ Add to Daily Log"):
        st.session_state.log.append({
            "Food": food,
            **nutrition
        })
        st.success("✅ Added to log!")


# -------------------------------
# DASHBOARD
# -------------------------------
st.divider()
st.subheader("📊 Daily Calorie Tracker")

if st.session_state.log:

    df = pd.DataFrame(st.session_state.log)
    st.dataframe(df)

    totals = df[["Calories","Protein","Fat","Carbs"]].sum()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Calories", int(totals["Calories"]))
    col2.metric("Protein", int(totals["Protein"]))
    col3.metric("Fat", int(totals["Fat"]))
    col4.metric("Carbs", int(totals["Carbs"]))

    # -------------------------------
    # BAR CHART
    # -------------------------------
    st.subheader("📊 Macronutrient Breakdown")

    fig, ax = plt.subplots()
    ax.bar(totals.index, totals.values)
    st.pyplot(fig)

    # -------------------------------
    # PIE CHART
    # -------------------------------
    st.subheader("🥧 Distribution")

    fig2, ax2 = plt.subplots()
    ax2.pie(totals.values, labels=totals.index, autopct='%1.1f%%')
    st.pyplot(fig2)

    # -------------------------------
    # RESET BUTTON
    # -------------------------------
    if st.button("🗑 Reset Daily Log"):
        st.session_state.log = []
        st.success("Log cleared!")

else:
    st.info("No foods added yet.")
