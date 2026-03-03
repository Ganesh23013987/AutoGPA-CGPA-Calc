import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AutoGPA Dummy", layout="wide")

# ---------------- STYLING ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 40%, #bae6fd 100%);
}
.title {
    text-align: center;
    font-size: 38px;
    font-weight: 800;
    margin-bottom: 25px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>🎓 AutoGPA-CGPA Calculator (Demo Version)</div>", unsafe_allow_html=True)

# ---------------- GRADE MAP ----------------
grade_map = {
    "O": 10,
    "A+": 9,
    "A": 8,
    "B+": 7,
    "B": 6,
    "C": 5,
    "RA": 0,
    "U": 0,
    "F": 0
}

# ---------------- PREVIOUS SEMESTERS ----------------
st.subheader("📘 Previous Semester Details")

num_sem = st.number_input("Number of Previous Semesters", 0, 8)

total_prev_weighted = 0
total_prev_credits = 0

for i in range(int(num_sem)):
    col1, col2 = st.columns(2)
    gpa = col1.number_input(f"Semester {i+1} GPA", 0.0, 10.0, key=f"gpa{i}")
    credits = col2.number_input(f"Semester {i+1} Credits", 0, key=f"cred{i}")

    total_prev_weighted += gpa * credits
    total_prev_credits += credits

st.divider()

# ---------------- CURRENT SEMESTER ----------------
st.subheader("📊 Enter Current Semester Subjects")

num_subjects = st.number_input("Number of Subjects", 1, 10)

subjects = []

for i in range(int(num_subjects)):
    col1, col2, col3 = st.columns(3)

    subject = col1.text_input(f"Subject {i+1} Name", key=f"sub{i}")
    credits = col2.number_input("Credits", 1, 6, key=f"credit{i}")
    grade = col3.selectbox("Grade", list(grade_map.keys()), key=f"grade{i}")

    subjects.append([subject, credits, grade])

st.divider()

# ---------------- CALCULATE BUTTON ----------------
if st.button("🚀 Calculate GPA & CGPA"):

    df = pd.DataFrame(subjects, columns=["Subject", "Credits", "Grade"])

    df["Grade Point"] = df["Grade"].map(grade_map)
    df["Weighted"] = df["Credits"] * df["Grade Point"]

    current_credits = df["Credits"].sum()
    current_weighted = df["Weighted"].sum()

    current_gpa = round(current_weighted / current_credits, 2)

    total_all_weighted = total_prev_weighted + current_weighted
    total_all_credits = total_prev_credits + current_credits

    final_cgpa = round(total_all_weighted / total_all_credits, 2) if total_all_credits else 0

    # ---------------- RESULTS ----------------
    st.subheader("📋 Subject Details")
    st.dataframe(df)

    col1, col2, col3 = st.columns(3)
    col1.metric("Current GPA", current_gpa)
    col2.metric("Total Credits", current_credits)
    col3.metric("Final CGPA", final_cgpa)

    # ---------------- GRAPH ----------------
    st.subheader("📈 Grade Distribution")

    grade_count = df["Grade"].value_counts().sort_index()

    fig, ax = plt.subplots(figsize=(4,3))
    bars = ax.bar(grade_count.index, grade_count.values)

    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width()/2,
            height,
            str(height),
            ha='center',
            va='bottom',
            fontsize=8
        )

    ax.set_xlabel("Grade")
    ax.set_ylabel("Count")
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    st.pyplot(fig)
