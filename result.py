import streamlit as st
import pandas as pd
import pdfplumber
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AutoG/CGPA Calc", layout="wide")

# ---------------- BACKGROUND ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 40%, #bae6fd 100%);
}
.main .block-container {
    max-width: 1100px;
    padding-top: 2rem;
}
.title {
    text-align: center;
    font-size: 40px;
    font-weight: 900;
    color: #1e293b;
    margin-bottom: 30px;
}
.kpi {
    background: linear-gradient(120deg, #667eea, #764ba2);
    color: white;
    padding: 25px;
    border-radius: 14px;
    text-align: center;
    font-size: 22px;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>🎓 AutoGPA-CGPA Calculator</div>", unsafe_allow_html=True)

# ---------------- GRADE MAP ----------------
grade_map = {
    "O": 10, "A+": 9, "A": 8,
    "B+": 7, "B": 6, "C": 5,
    "RA": 0, "U": 0, "F": 0
}

# ---------------- PREVIOUS SEM ----------------
st.subheader("📘 Previous Semester Details")

num_sem = st.number_input("How many previous semesters?", min_value=0, max_value=10)

total_prev_weighted = 0
total_prev_credits = 0

for i in range(int(num_sem)):
    col1, col2 = st.columns(2)
    gpa = col1.number_input(f"Semester {i+1} GPA", 0.0, 10.0, key=f"gpa{i}")
    credits = col2.number_input(f"Semester {i+1} Credits", 0, key=f"cred{i}")

    total_prev_weighted += gpa * credits
    total_prev_credits += credits

st.divider()

# ---------------- PDF UPLOAD ----------------
st.subheader("📂 Upload Current Semester Result")
uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file:

    subjects = []

    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                df = pd.DataFrame(table).dropna(how="all")
                for _, row in df.iterrows():
                    row_clean = [str(x).strip() for x in row if x]

                    grades = [g for g in row_clean if g in grade_map]
                    if grades:
                        grade = grades[0]

                        credit_candidates = [
                            int(x) for x in row_clean
                            if x.isdigit() and 1 <= int(x) <= 6
                        ]

                        if credit_candidates:
                            credits = credit_candidates[-1]
                            subject = row_clean[1] if len(row_clean) > 1 else "Unknown"
                            subjects.append([subject, credits, grade])

    if subjects:

        df_final = pd.DataFrame(subjects, columns=["Subject", "Credits", "Grade"])
        df_final = df_final.drop_duplicates()

        df_final["Grade Point"] = df_final["Grade"].map(grade_map)
        df_final["Weighted"] = df_final["Credits"] * df_final["Grade Point"]

        current_credits = df_final["Credits"].sum()
        current_weighted = df_final["Weighted"].sum()
        current_gpa = round(current_weighted / current_credits, 2)

        total_all_weighted = total_prev_weighted + current_weighted
        total_all_credits = total_prev_credits + current_credits
        final_cgpa = round(total_all_weighted / total_all_credits, 2) if total_all_credits else 0

        tab1, tab2, tab3 = st.tabs([
            "📊 Subjects & KPI",
            "📈 Graph",
            "🧮 Calculation"
        ])

        # -------- TAB 1 --------
        with tab1:
            st.dataframe(df_final[["Subject", "Credits", "Grade"]])

            col1, col2, col3 = st.columns(3)
            col1.markdown(f"<div class='kpi'>Current GPA<br><br>{current_gpa}</div>", unsafe_allow_html=True)
            col2.markdown(f"<div class='kpi'>Credits<br><br>{current_credits}</div>", unsafe_allow_html=True)
            col3.markdown(f"<div class='kpi'>Final CGPA<br><br>{final_cgpa}</div>", unsafe_allow_html=True)

        # -------- TAB 2 --------
        with tab2:
            st.markdown("<h3 style='text-align:center;'>Grade Distribution</h3>", unsafe_allow_html=True)

            grade_count = df_final["Grade"].value_counts().sort_index()

            fig, ax = plt.subplots(figsize=(4,3))
            bars = ax.bar(grade_count.index, grade_count.values)

            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2, height, str(height),
                        ha='center', va='bottom', fontsize=8)

            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)

            col1, col2, col3 = st.columns([1,2,1])
            with col2:
                st.pyplot(fig)

        # -------- TAB 3 --------
        with tab3:

            st.latex(r"GPA = \frac{\sum (Credits \times Grade\ Point)}{\sum Credits}")
            st.write(f"GPA = {current_weighted} / {current_credits} = **{current_gpa}**")

            st.latex(r"CGPA = \frac{Total\ Weighted\ Points}{Total\ Credits}")
            st.write(f"CGPA = {total_all_weighted} / {total_all_credits} = **{final_cgpa}**")

            if st.button("📥 Download GPA & CGPA Report"):

                file_path = "AutoGPA_Report.pdf"
                doc = SimpleDocTemplate(file_path)
                elements = []
                styles = getSampleStyleSheet()

                elements.append(Paragraph("AutoGPA Academic Report", styles["Title"]))
                elements.append(Spacer(1, 0.3 * inch))

                data = [["Subject","Credits","Grade","Grade Point","Weighted"]] + df_final.values.tolist()

                table = Table(data)

                table.setStyle(TableStyle([
                    ('BACKGROUND',(0,0),(-1,0),colors.lightgrey),
                    ('GRID',(0,0),(-1,-1),1,colors.black)
                ]))

                elements.append(table)
                elements.append(Spacer(1,0.3*inch))

                elements.append(Paragraph(f"Total Credits: {current_credits}", styles["Normal"]))
                elements.append(Paragraph(f"Total Weighted Points: {current_weighted}", styles["Normal"]))

                elements.append(Spacer(1,0.2*inch))

                elements.append(Paragraph(f"GPA = {current_weighted}/{current_credits} = {current_gpa}", styles["Normal"]))
                elements.append(Paragraph(f"CGPA = {total_all_weighted}/{total_all_credits} = {final_cgpa}", styles["Normal"]))

                doc.build(elements)

                with open(file_path,"rb") as f:
                    st.download_button(
                        "Download Report",
                        f,
                        file_name="AutoGPA_Report.pdf",
                        mime="application/pdf"
                    )

    else:
        st.error("No valid subjects detected.")

st.markdown("""
<hr>
<p style='text-align:center;font-size:16px;font-weight:600;color:#1e293b;'>
© 2026 AutoGPA-CGPA Calculator | Developed by Ganesh D
</p>
""", unsafe_allow_html=True)

