import streamlit as st

from util import (
    extract_pdf_text,
    clean_text,
    calculate_match_score,
    extract_keywords
)

st.set_page_config(
    page_title="Resume Screening AI",
    page_icon="📄",
    layout="wide"
)

st.markdown("""
<style>

.stApp{
    background:linear-gradient(135deg,#0f172a,#1e293b,#111827);
    color:white;
}

.block-container{
    padding-top:2rem;
}

</style>
""", unsafe_allow_html=True)

st.title("📄 Resume Screening AI")
st.write("Compare your Resume with a Job Description using NLP.")

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

    if job_description.strip() == "":
        st.error("Please enter a Job Description.")
        st.stop()

    resume_text = extract_pdf_text(uploaded_resume)

    cleaned_resume = clean_text(resume_text)
    cleaned_jd = clean_text(job_description)

    score = calculate_match_score(
        cleaned_resume,
        cleaned_jd
    )

    resume_keywords = set(extract_keywords(cleaned_resume))
    jd_keywords = set(extract_keywords(cleaned_jd))

    matched = sorted(
        resume_keywords.intersection(jd_keywords)
    )

    missing = sorted(
        jd_keywords - resume_keywords
    )

    st.success("Analysis Complete")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Resume Match",
            f"{score}%"
        )

        st.progress(score / 100)

    with col2:

        if score >= 85:
            st.success("Excellent Match")
        elif score >= 70:
            st.info("Good Match")
        elif score >= 50:
            st.warning("Average Match")
        else:
            st.error("Low Match")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("✅ Matched Keywords")

        if matched:

            for word in matched[:25]:
                st.success(word.title())

        else:
            st.info("No common keywords found.")

    with col2:

        st.subheader("❌ Missing Keywords")

        if missing:

            for word in missing[:25]:
                st.error(word.title())

        else:
            st.success("No missing keywords.")

    st.divider()

    st.subheader("📋 Recommendation")

    if score >= 85:
        st.success(
            "Your resume is strongly aligned with the job description."
        )

    elif score >= 70:
        st.info(
            "Your resume is a good match. Consider adding the missing skills."
        )

    elif score >= 50:
        st.warning(
            "Your resume requires improvements before applying."
        )

    else:
        st.error(
            "Your resume does not match the job requirements."
        )

