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
- **Gemini / OpenAI API**
- **PyPDF2**
- **Docker**
- **Hugging Face Spaces**

---

## **Project Structure**
```text
AI-Job-Application-Fit-Analyzer/
├── app.py
├── Dockerfile
├── requirements.txt
├── README.md
├── helper/
│   ├── pdf_reader.py
│   ├── skill_extractor.py
│   └── jd_processor.py
```

---

## **Run Locally**
```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## **Deployment**
- Containerized using **Docker**
- Deployed on **Hugging Face Spaces**
- Streamlit runs on **port 7860**

---

## **Learning Outcomes**sis
- Integrated Large Language Models
- Built an AI web application

---

## **Author**
**Iqra Shaikh**  
BSc Data Science & Artificial Intelligence  
