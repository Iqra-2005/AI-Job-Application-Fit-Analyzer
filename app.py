import streamlit as st
from helper.pdf_reader import extract_text_from_pdf
from helper.skill_extractor import extract_resume_data, extract_jd_data
from helper.scorer import calculate_match

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
