import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AutoGPA Mock", layout="wide")

st.title("🎓 AutoGPA-CGPA Calculator (Demo Mode)")

st.info("⚠️ This is a demo version with mock data.")

# ---------------- PREVIOUS SEM ----------------
st.subheader("📘 Previous Semester Details")

st.number_input("Number of Previous Semesters", 0, 8)

st.divider()

# ---------------- CURRENT SEM ----------------
st.subheader("📂 Upload Current Semester Result")

st.file_uploader("Upload PDF", type=["pdf"])

if st.button("🚀 Analyze Result"):

    # -------- MOCK DATA --------
    data = {
        "Subject": ["Mathematics", "Physics", "Chemistry", "English", "Programming"],
        "Credits": [4, 3, 3, 2, 4],
        "Grade": ["O", "A+", "A", "B+", "O"]
    }

    df = pd.DataFrame(data)

    st.subheader("📋 Extracted Subject Details")
    st.dataframe(df)

    # -------- MOCK GPA VALUES --------
    current_gpa = 8.75
    current_credits = 16
    final_cgpa = 8.42

    col1, col2, col3 = st.columns(3)

    col1.metric("Current GPA", current_gpa)
    col2.metric("Total Credits", current_credits)
    col3.metric("Final CGPA", final_cgpa)

    # -------- MOCK GRAPH --------
    st.subheader("📈 Grade Distribution")

    grade_count = df["Grade"].value_counts()

    fig, ax = plt.subplots(figsize=(4,3))
    ax.bar(grade_count.index, grade_count.values)

    st.pyplot(fig)

    st.success("✅ Result Analyzed Successfully!")

st.markdown("---")
st.markdown("<p style='text-align:center;'>Website Developed by Ganesh D</p>", unsafe_allow_html=True)
