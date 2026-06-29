import streamlit as st
from utils import (
    extract_pdf_text,
    clean_text,
    load_skills,
    extract_skills,
    calculate_match_score,
    extract_name,
    extract_email,
    extract_phone,
    extract_linkedin,
    extract_github
)

st.set_page_config(page_title="Resume Screening AI", page_icon="📄")

st.title("📄 Resume Screening AI")
st.write("Upload your resume and paste the Job Description.")

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
        st.error("Please upload a resume.")
        st.stop()

    if not job_description.strip():
        st.error("Please enter a Job Description.")
        st.stop()

    # ==========================
    # Extract Resume Text
    # ==========================

    resume_text = extract_pdf_text(uploaded_resume)

    # ==========================
    # Candidate Information
    # ==========================

    name = extract_name(resume_text)
    email = extract_email(resume_text)
    phone = extract_phone(resume_text)
    linkedin = extract_linkedin(resume_text)
    github = extract_github(resume_text)

    # ==========================
    # Clean Text
    # ==========================

    cleaned_resume = clean_text(resume_text)
    cleaned_jd = clean_text(job_description)

    # ==========================
    # Match Score
    # ==========================

    score = calculate_match_score(cleaned_resume, cleaned_jd)

    # ==========================
    # Skills
    # ==========================

    skills = load_skills()

    resume_skills = extract_skills(cleaned_resume, skills)
    jd_skills = extract_skills(cleaned_jd, skills)

    matched_skills = sorted(
        list(set(resume_skills).intersection(jd_skills))
    )

    missing_skills = sorted(
        list(set(jd_skills) - set(resume_skills))
    )

    # ==========================
    # Display
    # ==========================

    st.success("Resume Analysis Complete")

    st.subheader("👤 Candidate Information")

    st.write(f"**Name:** {name}")
    st.write(f"**Email:** {email}")
    st.write(f"**Phone:** {phone}")
    st.write(f"**LinkedIn:** {linkedin}")
    st.write(f"**GitHub:** {github}")

    st.divider()

    st.metric("🎯 Match Score", f"{score}%")

    st.divider()

    st.subheader("✅ Matched Skills")

    if matched_skills:
        for skill in matched_skills:
            st.write(f"✔ {skill.title()}")
    else:
        st.info("No matching skills found.")

    st.subheader("❌ Missing Skills")

    if missing_skills:
        for skill in missing_skills:
            st.write(f"✖ {skill.title()}")
    else:
        st.success("No missing skills detected.")

    st.divider()

    st.subheader("📋 Recommendation")

    if score >= 85:
        st.success("Excellent match. Highly suitable for this role.")
    elif score >= 70:
        st.info("Good match. Strengthen the missing skills to improve.")
    elif score >= 50:
        st.warning("Average match. Resume should be tailored to this job.")
    else:
        st.error("Low match. Significant improvements are recommended.")