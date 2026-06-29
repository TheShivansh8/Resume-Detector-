import re
import fitz
import streamlit as st

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# ----------------------------
# Load AI Model
# ----------------------------

@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


model = load_model()

# ----------------------------
# PDF Extraction
# ----------------------------

def extract_pdf_text(uploaded_file):

    pdf = fitz.open(
        stream=uploaded_file.read(),
        filetype="pdf"
    )

    text = ""

    for page in pdf:
        text += page.get_text()

    return text


# ----------------------------
# Text Cleaning
# ----------------------------

def clean_text(text):

    text = text.lower()

    text = re.sub(r"http\S+", " ", text)
    text = re.sub(r"[^a-z0-9+#.\s]", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ----------------------------
# Semantic Similarity
# ----------------------------

def calculate_match_score(resume_text, jd_text):

    resume_embedding = model.encode(
        resume_text,
        convert_to_numpy=True
    )

    jd_embedding = model.encode(
        jd_text,
        convert_to_numpy=True
    )

    similarity = cosine_similarity(
        resume_embedding.reshape(1, -1),
        jd_embedding.reshape(1, -1)
    )[0][0]

    score = float(similarity) * 100

    score = max(0.0, min(100.0, score))

    return round(score, 2)


# ----------------------------
# Keyword Extraction
# ----------------------------

STOPWORDS = {

    "experience",
    "experienced",
    "responsible",
    "responsibilities",
    "candidate",
    "knowledge",
    "skills",
    "ability",
    "strong",
    "excellent",
    "good",
    "work",
    "working",
    "team",
    "using",
    "years",
    "project",
    "projects",
    "resume",
    "education",
    "developer",
    "engineer",
    "software",
    "company",
    "required",
    "requirements",
    "looking",
    "must",
    "will",
    "role",
    "data"
}


def extract_keywords(text):

    words = re.findall(
        r"[a-zA-Z][a-zA-Z0-9.+#-]*",
        text.lower()
    )

    keywords = []

    for word in words:

        if (
            len(word) > 2
            and word not in STOPWORDS
            and not word.isdigit()
        ):
            keywords.append(word)

    return sorted(set(keywords))

