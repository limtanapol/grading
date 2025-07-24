import streamlit as st
from pdf_utils import convert_pdf_to_images
from scorer import score_answers
import pandas as pd

st.title("📄 Answer Sheet Scoring System (Force Dummy Data)")

# Step 1: Input answer key
st.subheader("Step 1: Input Answer Key")
num_questions = 120
answer_key = {}
with st.form("answer_key_form"):
    cols = st.columns(6)
    for i in range(1, num_questions + 1):
        col = cols[(i - 1) % 6]
        answer = col.multiselect(f"Q{i}", ["A", "B", "C", "D", "E"], key=f"q{i}")
        if answer:
            answer_key[i] = answer
    submitted = st.form_submit_button("Submit Answer Key")

# Step 2: Upload PDF
st.subheader("Step 2: Upload Answer Sheet PDF")
uploaded_pdf = st.file_uploader("Upload PDF file", type=["pdf"])

# Step 3: Process and Score
if uploaded_pdf:
    st.write("📥 PDF uploaded.")

if uploaded_pdf and submitted:
    st.write("✅ Answer key submitted.")
    if st.button("Process & Score"):
        try:
            images = convert_pdf_to_images(uploaded_pdf)
            st.success(f"✅ Detected {len(images)} page(s) in PDF.")
            results = []

            for i, img in enumerate(images):
                st.write(f"🔍 Processing page {i+1}...")
                student_id = f"ID_{i+1:03d}"
                answers = {q: ["A"] for q in answer_key.keys()}
                st.write(f"👤 Student ID: {student_id}")
                st.write(f"✅ Answers: {answers}")
                score, per_question = score_answers(answers, answer_key)
                results.append({
                    "Student ID": student_id,
                    **per_question,
                    "Total Score": score
                })

            if results:
                df = pd.DataFrame(results)
                st.subheader("📊 Results")
                st.dataframe(df)

                csv = df.to_csv(index=False).encode()
                st.download_button("Download CSV", csv, "scores.csv", "text/csv")
            else:
                st.warning("⚠️ No results generated. Check answer key and PDF.")

        except Exception as e:
            st.error(f"❌ An error occurred: {e}")