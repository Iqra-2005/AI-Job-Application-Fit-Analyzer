import json
import re
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from config import GEMINI_API_KEY, MODEL_NAME
from helper.prompts import RESUME_SKILL_PROMPT, JD_SKILL_PROMPT

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
