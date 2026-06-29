import streamlit as st

from util import (
    extract_pdf_text,
    clean_text,
    calculate_match_score,
    extract_keywords
)

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🤖",
    layout="wide"
)

# -----------------------
# Custom CSS
# -----------------------

st.markdown("""
<style>

.stApp{
    background: linear-gradient(135deg,#0f172a,#111827,#1f2937);
    color:white;
}

h1,h2,h3{
    color:white;
}

</style>
""", unsafe_allow_html=True)

st.title("🤖 AI Resume Analyzer")
st.write("Compare your Resume with a Job Description using Semantic AI.")

uploaded_resume = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

job_description = st.text_area(
    "Paste Job Description",
    height=250
)

if st.button("Analyze Resume"):

    if uploaded_resume is None:
        st.error("Please upload a Resume.")
        st.stop()

    if not job_description.strip():
        st.error("Please enter a Job Description.")
        st.stop()

    # -----------------------
    # Extract Resume
    # -----------------------

    resume_text = extract_pdf_text(uploaded_resume)

    cleaned_resume = clean_text(resume_text)
    cleaned_jd = clean_text(job_description)

    score = calculate_match_score(
        cleaned_resume,
        cleaned_jd
    )

    score = float(score)

    # -----------------------
    # Keyword Comparison
    # -----------------------

    resume_keywords = set(
        extract_keywords(cleaned_resume)
    )

    jd_keywords = set(
        extract_keywords(cleaned_jd)
    )

    matched = sorted(
        resume_keywords.intersection(jd_keywords)
    )

    missing = sorted(
        jd_keywords - resume_keywords
    )

    # -----------------------
    # Results
    # -----------------------

    st.success("Analysis Completed Successfully!")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            label="Resume Match",
            value=f"{score:.2f}%"
        )

        progress_value = max(
            0.0,
            min(1.0, score / 100.0)
        )

        st.progress(progress_value)

    with col2:

        if score >= 85:
            st.success("Excellent Match ⭐")

        elif score >= 70:
            st.info("Good Match 👍")

        elif score >= 50:
            st.warning("Average Match ⚠")

        else:
            st.error("Low Match ❌")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("✅ Matched Keywords")

        if matched:

            for word in matched[:25]:
                st.write(f"✅ {word.title()}")

        else:

            st.info("No matching keywords found.")

    with col2:

        st.subheader("❌ Missing Keywords")

        if missing:

            for word in missing[:25]:
                st.write(f"❌ {word.title()}")

        else:

            st.success("No missing keywords.")

    st.divider()

    st.subheader("📋 AI Recommendation")

    if score >= 85:

        st.success("""
Your resume is highly aligned with this Job Description.

You are a strong candidate based on semantic similarity.
        """)

    elif score >= 70:

        st.info("""
Good overall match.

Improve the missing skills and tailor your resume before applying.
        """)

    elif score >= 50:

        st.warning("""
Average match.

Consider adding more relevant projects, technical skills,
and keywords from the Job Description.
        """)

    else:

        st.error("""
Low match.

Your resume does not align well with the Job Description.
Consider rewriting your resume for this specific role.
        """)

