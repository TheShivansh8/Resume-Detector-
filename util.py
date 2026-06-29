import re
import pdfplumber

from sklearn.feature_extraction.text import (
    ENGLISH_STOP_WORDS,
    TfidfVectorizer
)
from sklearn.metrics.pairwise import cosine_similarity


# ==========================
# PDF Extraction
# ==========================

def extract_pdf_text(pdf_file):
    text = ""

    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text


# ==========================
# Text Cleaning
# ==========================

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


# ==========================
# Match Score
# ==========================

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


# ==========================
# Resume Information
# ==========================

def extract_email(text):

    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

    match = re.search(pattern, text)

    if match:
        return match.group()

    return "Not Found"


def extract_phone(text):

    pattern = r'(\+91[\s-]?)?[6-9]\d{9}'

    match = re.search(pattern, text)

    if match:
        return match.group()

    return "Not Found"


def extract_linkedin(text):

    pattern = r'(https?://)?(www\.)?linkedin\.com/in/[A-Za-z0-9_-]+'

    match = re.search(pattern, text)

    if match:
        return match.group()

    return "Not Found"


def extract_github(text):

    pattern = r'(https?://)?(www\.)?github\.com/[A-Za-z0-9_-]+'

    match = re.search(pattern, text)

    if match:
        return match.group()

    return "Not Found"


def extract_name(text):

    lines = text.split("\n")

    for line in lines:

        line = line.strip()

        if 2 <= len(line.split()) <= 4:
            return line

    return "Not Found"
