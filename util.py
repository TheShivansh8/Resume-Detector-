import re
import fitz  # PyMuPDF

import streamlit as st

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# ----------------------------
# Load AI Model (Only Once)
# ----------------------------

@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


model = load_model()


# ----------------------------
# Extract Text From PDF
# ----------------------------

def extract_pdf_text(uploaded_file):

    text = ""

    pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")

    for page in pdf:
        text += page.get_text()

    return text


# ----------------------------
# Clean Text
# ----------------------------

def clean_text(text):

    text = text.lower()

    text = re.sub(r"http\S+", " ", text)

    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ----------------------------
# Semantic Similarity
# ----------------------------

def calculate_match_score(resume_text, jd_text):

    resume_embedding = model.encode(
        resume_text,
        convert_to_tensor=False
    )

    jd_embedding = model.encode(
        jd_text,
        convert_to_tensor=False
    )

    similarity = cosine_similarity(
        [resume_embedding],
        [jd_embedding]
    )[0][0]

    return round(similarity * 100, 2)


# ----------------------------
# Keyword Extraction
# ----------------------------

def extract_keywords(text):

    words = text.split()

    words = [w for w in words if len(w) > 3]

    return sorted(list(set(words)))
