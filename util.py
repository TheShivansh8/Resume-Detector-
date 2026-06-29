import pandas as pd
import pdfplumber
import re
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

def extract_pdf_text(pdf_file):
    text = ""

    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    return text


def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)

    words = text.split()
    words = [word for word in words if word not in ENGLISH_STOP_WORDS]

    return " ".join(words)


def load_skills(path="data/skills.csv"):
    df = pd.read_csv(path)
    return df["skill"].str.lower().tolist()


def extract_skills(text, skills):
    found = []

    text = text.lower()

    for skill in skills:
        if skill in text:
            found.append(skill)

    return sorted(list(set(found)))
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_match_score(resume_text, jd_text):

    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform([resume_text, jd_text])

    similarity = cosine_similarity(vectors[0], vectors[1])

    return round(similarity[0][0] * 100, 2)
import re


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

        if len(line.split()) <= 4 and len(line) > 2:
            return line

    return "Not Found"