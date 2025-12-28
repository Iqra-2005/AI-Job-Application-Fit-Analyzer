# IMPORTING NECESSARY MODULES 

import os
from dotenv import load_dotenv
import pdfplumber
import json
import re
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
import streamlit as st


# CONFIGURATION SETUP 

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")   # .env file contents gemini-api
MODEL_NAME = "gemini-2.5-flash"


# PDF READER

def extract_text_from_pdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

# SCORER TO GENERATE MATCH SCORE 

def calculate_match(resume_data, jd_data):
    resume_skills = set(map(str.lower, resume_data["skills"]))
    jd_skills = set(map(str.lower, jd_data["required_skills"]))

    matched_skills = resume_skills.intersection(jd_skills)
    missing_skills = jd_skills - resume_skills

    skill_score = (len(matched_skills) / max(len(jd_skills), 1)) * 100

    experience_gap = resume_data["experience_years"] - jd_data["min_experience"]

    if skill_score >= 75 and experience_gap >= 0:
        decision = "Apply"
    elif skill_score >= 50:
        decision = "Apply After Upskilling"
    else:
        decision = "Not Recommended"

    return {
        "skill_score": round(skill_score, 2),
        "matched_skills": list(matched_skills),
        "missing_skills": list(missing_skills),
        "experience_gap": experience_gap,
        "decision": decision
    }


# PROMPTS 

RESUME_SKILL_PROMPT = """
You are an information extraction system.

Return ONLY valid JSON.
DO NOT add explanations.
DO NOT use markdown.
DO NOT wrap in backticks.

JSON format:
{{
  "skills": [],
  "experience_years": 0,
  "domains": []
}}

Resume Text:
{resume_text}
"""


JD_SKILL_PROMPT = """
You are an information extraction system.

Return ONLY valid JSON.
DO NOT add explanations.
DO NOT use markdown.
DO NOT wrap in backticks.

JSON format:
{{
  "required_skills": [],
  "min_experience": 0,
  "role_domain": ""
}}

Job Description:
{jd_text}
"""


# SKILL EXTRACTOR


llm = ChatGoogleGenerativeAI(
    google_api_key=GEMINI_API_KEY,
    model=MODEL_NAME,
    temperature=0
)

def extract_json(text):
    if not text or not text.strip():
        raise ValueError("Empty response from LLM")

    # Try direct JSON
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Try extracting JSON block
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return json.loads(match.group())

    raise ValueError("No valid JSON found in LLM response")

def extract_resume_data(resume_text):
    prompt = PromptTemplate.from_template(RESUME_SKILL_PROMPT)
    response = llm.invoke(prompt.format(resume_text=resume_text))
    return extract_json(response.content)

def extract_jd_data(jd_text):
    prompt = PromptTemplate.from_template(JD_SKILL_PROMPT)
    response = llm.invoke(prompt.format(jd_text=jd_text))
    return extract_json(response.content)


# STREAMLIT UI


# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="AI Job Fit Analyzer",
    page_icon="🤖",
    layout="wide"
)

# ---------- HEADER ----------
st.markdown(
    """
    <h1 style='text-align:center;'>🤖 AI Job Application Fit Analyzer</h1>
    <p style='text-align:center; color:gray;'>
    Smart resume–job matching with explainable decisions
    </p>
    <hr>
    """,
    unsafe_allow_html=True
)

# ---------- SIDEBAR ----------
with st.sidebar:
    st.header("📂 Input Details")

    resume_file = st.file_uploader(
        "Upload Resume (PDF)",
        type=["pdf"]
    )

    jd_text = st.text_area(
        "Paste Job Description",
        height=250,
        placeholder="Paste the full job description including required skills, experience, and responsibilities..."
    )

    analyze_btn = st.button("🚀 Analyze Fit")

# ---------- MAIN ----------
if analyze_btn:
    if not resume_file or not jd_text:
        st.error("Please upload a resume and paste the job description.")
    else:
        with st.spinner("🔍 Analyzing resume and job description..."):
            progress = st.progress(0)

            # Step 1: Read Resume
            resume_text = extract_text_from_pdf(resume_file)
            progress.progress(30)

            # Step 2: Extract Structured Data
            try:
                resume_data = extract_resume_data(resume_text)
                progress.progress(60)

                jd_data = extract_jd_data(jd_text)
                progress.progress(90)
            except Exception as e:
                st.error("❌ Failed to extract structured data from Gemini.")
                st.code(str(e))
                st.stop()

            # Step 3: Calculate Match
            result = calculate_match(resume_data, jd_data)
            progress.progress(100)

        # ---------- DECISION REASONS ----------
        reasons = []

        if result["skill_score"] < 75:
            reasons.append("Skill match below recommended threshold")

        if result["experience_gap"] < 0:
            reasons.append("Experience requirement not met")

        if not reasons:
            reasons.append("Strong alignment with job requirements")

        # ---------- RESULTS ----------
        st.subheader("📊 Match Summary")

        st.markdown("### 🧠 Why this decision?")
        for reason in reasons:
            st.markdown(f"- {reason}")

        col1, col2, col3 = st.columns(3)

        # Skill Match
        col1.metric("Skill Match", f"{result['skill_score']}%")
        if result["skill_score"] >= 75:
            col1.caption("Confidence: High")
        elif result["skill_score"] >= 50:
            col1.caption("Confidence: Medium")
        else:
            col1.caption("Confidence: Low")

        # Experience Gap
        col2.metric("Experience Gap", f"{result['experience_gap']} yrs")

        # Decision Badge
        decision = result["decision"]
        if decision == "Apply":
            col3.success("✅ APPLY")
        elif "Upskill" in decision:
            col3.warning("🛠️ UPSKILL FIRST")
        else:
            col3.error("❌ NOT RECOMMENDED")

        st.divider()

        # ---------- SKILLS ----------
        col_left, col_right = st.columns(2)

        with col_left:
            with st.expander("✅ Matched Skills"):
                if result["matched_skills"]:
                    for skill in result["matched_skills"]:
                        st.markdown(f"- {skill}")
                else:
                    st.info("No matching skills found.")

        with col_right:
            with st.expander("❌ Missing Skills"):
                if result["missing_skills"]:
                    for skill in result["missing_skills"]:
                        st.markdown(f"- {skill}")
                else:
                    st.success("No missing skills 🎉")

        st.divider()

        # ---------- FOOTER ----------
        st.caption(
            "⚙️ Powered by Gemini AI • LangChain • Streamlit | "
            "This tool provides decision support, not hiring guarantees."
        )
