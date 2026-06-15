
from flask import Flask, render_template, request, send_from_directory
import PyPDF2
import os

app = Flask(__name__)

if not os.path.exists("uploads"):
    os.makedirs("uploads")


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['resume']

    filepath = os.path.join("uploads", file.filename)
    file.save(filepath)

    text = ""

    if file.filename.endswith(".pdf"):
        pdf = PyPDF2.PdfReader(filepath)
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text

    keywords = [
        "python", "flask", "java", "sql",
        "machine learning", "ai", "data",
        "html", "css"
    ]

    found_skills = []
    missing_skills = []

    for skill in keywords:
        if skill.lower() in text.lower():
            found_skills.append(skill)
        else:
            missing_skills.append(skill)

    # ATS SCORE
    score = len(found_skills) * 10
    if score > 100:
        score = 100

    # SUGGESTIONS + DISPLAY LOGIC
    if len(missing_skills) == 0:
        suggestions = "Great! Your resume contains all important skills."
    else:
        suggestions = "Add these skills: " + ", ".join(missing_skills)

    # JOB ROLE PREDICTION
    text_lower = text.lower()

    if "machine learning" in text_lower or "ai" in text_lower:
        job_role = "AI / Machine Learning Engineer"
    elif "data" in text_lower or "sql" in text_lower:
        job_role = "Data Analyst"
    elif "flask" in text_lower or "java" in text_lower or "html" in text_lower:
        job_role = "Software Developer"
    else:
        job_role = "General IT Role"

    return render_template(
        "result.html",
        score=score,
        suggestions=suggestions,
        job_role=job_role,
        filename=file.filename,
        found_skills=found_skills,
        missing_skills=missing_skills
    )


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)


if __name__ == "__main__":
    app.run(debug=True)