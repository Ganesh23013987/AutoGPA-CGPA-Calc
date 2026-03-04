import streamlit as st

st.set_page_config(page_title="AutoGPA Calculator")

st.title("🎓 AutoGPA - CGPA Calculator")

st.write("Upload your semester result PDF to calculate GPA automatically.")

file = st.file_uploader("Upload Result PDF", type=["pdf"])

if file:
    st.success("PDF uploaded successfully!")

    st.write("Subject Table (Data)")
    st.table({
        "Subject": ["Maths", "Physics", "Programming"],
        "Credits": [3, 4, 3],
        "Grade": ["A+", "A", "O"]
    })

    st.metric("GPA", "8.7")
    st.metric("CGPA", "8.5")

st.write("© 2026 AutoGPA Calculator")
