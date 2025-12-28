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
