import streamlit as st
from PIL import Image
from utils import detect_food, get_nutrition

st.set_page_config(page_title="🍱 Food Analyzer", layout="centered")

st.title("🍱 AI Food Nutrition Analyzer + Tracker")
st.caption("⚡ Fast • Free • Track Your Daily Intake")

# -------------------------------
# SESSION STATE (STORE DATA)
# -------------------------------
if "log" not in st.session_state:
    st.session_state.log = []

# -------------------------------
# IMAGE INPUT
# -------------------------------
uploaded_file = st.file_uploader("Upload Food Image", type=["jpg","jpeg","png"])

food = None
nutrition = None

if uploaded_file:
    image = Image.open(uploaded_file)
    image = image.resize((256, 256))
    st.image(image)

    if st.button("Analyze Food"):
        uploaded_file.seek(0)

        with st.spinner("🔍 Detecting food..."):
            food = detect_food(uploaded_file)

        if food == "error":
            st.warning("⚠️ AI failed. Enter manually.")
            food = st.text_input("Enter food name")

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

                # -------------------------------
                # ADD TO LOG BUTTON
                # -------------------------------
                if st.button("➕ Add to Daily Log"):
                    st.session_state.log.append({
                        "Food": food,
                        **nutrition
                    })
                    st.success("Added to log!")

            else:
                st.error("❌ Nutrition not found")

# -------------------------------
# DASHBOARD
# -------------------------------
st.divider()
st.subheader("📊 Daily Calorie Tracker")

if st.session_state.log:

    import pandas as pd
    import matplotlib.pyplot as plt

    df = pd.DataFrame(st.session_state.log)

    st.dataframe(df)

    totals = df[["Calories","Protein","Fat","Carbs"]].sum()

    # METRICS
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
