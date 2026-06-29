import re
import pdfplumber

from sklearn.feature_extraction.text import (
    ENGLISH_STOP_WORDS,
    TfidfVectorizer
)
from sklearn.metrics.pairwise import cosine_similarity


# -------------------------------
# Extract text from PDF
# -------------------------------

def extract_pdf_text(pdf_file):

    text = ""

    with pdfplumber.open(pdf_file) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text


# -------------------------------
# Clean Text
# -------------------------------

def clean_text(text):

    text = text.lower()

    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)

    words = text.split()

    words = [
        word
        for word in words
        if word not in ENGLISH_STOP_WORDS
    ]

    return " ".join(words)


# -------------------------------
# TF-IDF Similarity
# -------------------------------

def calculate_match_score(resume_text, jd_text):

    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform(
        [resume_text, jd_text]
    )

    similarity = cosine_similarity(
        vectors[0],
        vectors[1]
    )[0][0]

    return round(similarity * 100, 2)


# -------------------------------
# Extract Keywords
# -------------------------------

def extract_keywords(text):

    words = text.split()

    keywords = []

    for word in words:

        if len(word) > 3:
            keywords.append(word)

    return sorted(list(set(keywords)))

