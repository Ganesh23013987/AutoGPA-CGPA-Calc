# 🎓 AutoGPA – Smart Academic Performance Dashboard

AutoGPA is a Streamlit-based web application that automatically extracts subject details from semester result PDFs and calculates GPA and CGPA with full transparency.

The system provides real-time grade visualization, detailed calculation breakdowns, and downloadable PDF reports.

---

## 📌 Project Overview

Managing semester results manually can be time-consuming and error-prone.  
AutoGPA simplifies this process by:

- Automatically extracting subject data from uploaded PDFs
- Mapping grades to grade points
- Calculating GPA and CGPA instantly
- Displaying results in a clean dashboard
- Generating professional PDF reports

This project demonstrates practical implementation of data processing, automation, visualization, and report generation.

---

## 🚀 Features

- 📂 Upload Semester Result PDF
- 📊 Automatic Subject, Credit & Grade Detection
- 🎯 Current Semester GPA Calculation
- 🏆 Final CGPA Calculation (including previous semesters)
- 📈 Grade Distribution Visualization (Bar Chart)
- 🧮 Step-by-Step GPA & CGPA Calculation Display
- 📥 Downloadable PDF Report with Full Calculation Breakdown
- 🎨 Modern, Clean UI Design

---

## 🛠 Technologies Used

- Python
- Streamlit
- Pandas
- Matplotlib
- pdfplumber
- ReportLab

---

## 📐 GPA Calculation Logic

### 🎯 Grade to Grade Point Mapping

| Grade  | Grade Point |
|--------|-------------|
| O      | 10          |
| A+     | 9           |
| A      | 8           |
| B+     | 7           |
| B      | 6           |
| C      | 5           |
| RA     | 0           |
| U      | 0           |
| F      | 0           |

---

### 🎓 GPA Formula

<img width="580" height="580" alt="image" src="https://github.com/user-attachments/assets/d031f317-2486-4517-8b6e-52ac7dfcc914" />


Where:
- Weighted Points = Credits × Grade Point
- Total Credits = Sum of all subject credits

---

### 🏆 CGPA Formula

<img width="580" height="580" alt="image" src="https://github.com/user-attachments/assets/9eac31ba-fc62-4fc5-b3a9-40f658fe3303" />


Where:
- Previous semester weighted totals are included
- Current semester weighted totals are added

---

## 📊 Dashboard Structure

### 1️⃣ Subjects & KPI Tab
- Displays subject list
- Current GPA
- Total Credits
- Final CGPA

### 2️⃣ Graph Tab
- Centered grade distribution bar chart
- Clean and compact visualization

### 3️⃣ Calculation Tab
- Formula explanation
- Numerical substitution
- GPA breakdown
- CGPA breakdown
- PDF report download option

---

## 📥 PDF Report Includes

The generated report contains:

- Subject-wise details
- Credits
- Grades
- Grade Points
- Weighted Calculations
- Total Credits
- Total Weighted Points
- GPA Formula with numerical substitution
- CGPA Formula with numerical substitution

This ensures full transparency of academic calculations.

---

## Our Project features

✔ Automatically extracts data from PDF

✔ Calculates GPA & CGPA

✔ Displays grade analytics graph

✔ Generates downloadable report

✔ Works as a web application

## ▶️ How to Run the Project

streamlit run result.py

Now our website is on live:

https://autogpa-cgpa-calc.onrender.com/

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/AutoGPA.git
cd AutoGPA
