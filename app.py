```python
import streamlit as st
from util import (
    extract_pdf_text,
    clean_text,
    calculate_match_score,
    extract_name,
    extract_email,
    extract_phone,
    extract_linkedin,
    extract_github
)

st.set_page_config(
    page_title="Resume Screening AI",
    page_icon="📄",
    layout="wide"
)

# ---------- Custom CSS ----------

st.markdown("""
<style>

.stApp{
background: linear-gradient(135deg,#0f172a,#1e293b,#111827);
color:white;
}

.block-container{
padding-top:2rem;
padding-bottom:2rem;
}

.card{
background:#1f2937;
padding:20px;
border-radius:15px;
border:1px solid #374151;
box-shadow:0px 0px 15px rgba(0,0,0,0.25);
}

h1,h2,h3{
color:white;
}

</style>
""", unsafe_allow_html=True)

st.title("📄 Resume Screening AI")
st.write("Upload your resume and compare it with a Job Description.")

uploaded_resume = st.file_uploader(
    "Upload Resume",
    type=["pdf"]
)

job_description = st.text_area(
    "Paste Job Description",
    height=250
)

if st.button("Analyze Resume"):

    if uploaded_resume is None:
        st.error("Please upload a resume.")
        st.stop()

    if not job_description.strip():
        st.error("Please enter a Job Description.")
        st.stop()

    resume_text = extract_pdf_text(uploaded_resume)

    name = extract_name(resume_text)
    email = extract_email(resume_text)
    phone = extract_phone(resume_text)
    linkedin = extract_linkedin(resume_text)
    github = extract_github(resume_text)

    cleaned_resume = clean_text(resume_text)
    cleaned_jd = clean_text(job_description)

    score = calculate_match_score(cleaned_resume, cleaned_jd)

    st.success("Analysis Complete")

    col1, col2 = st.columns([1,1])

    with col1:

        st.markdown("### 👤 Candidate Information")

        st.info(f"""
**Name:** {name}

**Email:** {email}

**Phone:** {phone}

**LinkedIn:** {linkedin}

**GitHub:** {github}
""")

    with col2:

        st.markdown("### 🎯 Resume Match")

        st.metric(
            label="Match Score",
            value=f"{score}%"
        )

        st.progress(min(score/100,1.0))

    st.divider()

    st.markdown("### 📋 Recommendation")

    if score >= 85:
        st.success("Excellent match. Your resume strongly aligns with the job description.")
    elif score >= 70:
        st.info("Good match. A few improvements can make your profile stronger.")
    elif score >= 50:
        st.warning("Average match. Tailor your resume to the job description.")
    else:
        st.error("Low match. Consider revising your resume before applying.")
```

