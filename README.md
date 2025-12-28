# **AI Job Application Fit Analyzer**

An AI-powered web application that analyzes how well a resume matches a given job description using NLP and AI techniques.

---

## **Problem Statement**
Manual resume screening is time-consuming and subjective. Recruiters and job seekers need a faster and more reliable way to evaluate resume–job fit.

---

## **Solution**
The application:
- Accepts a **resume (PDF)** and a **job description**
- Extracts skills and key information
- Compares resume content with job requirements
- Generates a **match score** and **AI-based analysis**
 
---

## **Tech Stack**
- **Python**
- **Streamlit**
- **LangChain**
- **Gemini API**
- **PyPDF2**


---

## **Project Structure**
```text
AI-Job-Application-Fit-Analyzer/
|--- AI-Job-Fit-Analyzer.py
|--- Variables & Helper functions/
│   |--- pdf_reader              # to read resume pdf and extract content
|   |--- prompt                  # structured prompts for the llm
│   |--- skill_extractor         # AI agent to extract skills from the resume and job description for efficient matching
│   └--- scorer                  # to generate match scores between resume and job description
```

---

## **Run Locally**
```bash
pip install -r requirements.txt
```

Create .env file and place you GEMINI_API_KEY

```bash
streamlit run app.py
```

---

## **Learning Outcomes**sis
- Integrated Large Language Models
- Prompt Engineering 
- Built an AI web application

---

## **Author**
**Iqra Shaikh**  
BSc Data Science & Artificial Intelligence  
