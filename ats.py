import os
import sys
import json
import PyPDF2
import google.generativeai as genai

genai.configure(api_key="AIzaSyAH3nXug262foRug7tPKQHePBXuImgOulM") 
generation_config = {
    "temperature": 0.0,        # Lower temperature reduces randomness
    "top_p": 1.0,              # Setting top_p to 1 disables nucleus sampling
    "top_k": 0,                # Setting top_k to 0 disables top-k sampling
    "max_output_tokens": 10000,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)
chat_session = model.start_chat(history=[])

def pdf_to_text(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

# Get input arguments
resume_path = sys.argv[1]
job_descr = sys.argv[2]

resume_text = pdf_to_text(resume_path)

resume_prompt = f"""
Consider the standard that resembles the standard which is followed by the linkedin in considering th certain skills as actual skill-sets.
list only the skill sets mentioned in the following resume. Do not include any introductory sentences or additional information.

Resume:\n{resume_text}\nPlease ensure the output includes only the skill sets mentioned in the resume one below the other.

format the output as the below format.
"C Programming Language
Python Programming Language
Java Programming Language
Network Programming using Python
Discrete Mathematics (DSA)
HTML
CSS (Vanilla & Frameworks)
JavaScript
Node.js
Express.js
SQL Database Management System
MongoDB NoSQL Database Management System
React.js JavaScript Library
Microsoft Office Suite (Word, Excel, PowerPoint, Project)"
"""

resume_skill_response = chat_session.send_message(resume_prompt)
resume_skill = resume_skill_response.text
resume_skills_set = set(skill.strip() for skill in resume_skill.split("\n") if skill.strip())

job_descr_prompt = f"""
Consider the standard that resembles the standard which is followed by the linkedin in considering th certain skills as actual skill-sets.
go through the below job description and list down all the skills that are mentioned. Do not include any introductory sentences or additional information.

job description: \n{job_descr}\nPlease ensure the output includes only the skill sets mentioned in the job description one below the other.

format the output as the below format.
"C Programming Language
Python Programming Language
Java Programming Language
Network Programming using Python
Discrete Mathematics (DSA)
HTML
CSS (Vanilla & Frameworks)
JavaScript
Node.js
Express.js
SQL Database Management System
MongoDB NoSQL Database Management System
React.js JavaScript Library
Microsoft Office Suite (Word, Excel, PowerPoint, Project)"
"""

job_descr_skill_response = chat_session.send_message(job_descr_prompt)
job_descr_skill = job_descr_skill_response.text
job_descr_skill_set = set(skill.strip() for skill in job_descr_skill.split("\n") if skill.strip())

lack_prompt = f"""
Consider the standard that resembles the standard which is followed by the linkedin in considering th certain skills as actual skill-sets.
compare the skills mentioned in the resume and the job description and list down the skills which are present in the job description but not in the resume.

Resume Skills: \n{resume_skill}
Job Description Skills: \n{job_descr_skill}

Provide the response in the below format:

"C Programming Language
Python Programming Language
Java Programming Language
Network Programming using Python
Discrete Mathematics (DSA)
HTML
CSS (Vanilla & Frameworks)
JavaScript
Node.js
Express.js
SQL Database Management System
MongoDB NoSQL Database Management System
React.js JavaScript Library
Microsoft Office Suite (Word, Excel, PowerPoint, Project)"
"""
lack_skill_response = chat_session.send_message(lack_prompt)
lack_skill = lack_skill_response.text
lack_skills_set = set(skill.strip() for skill in lack_skill.split("\n") if skill.strip())

extra_prompt = f"""
Consider the standard that resembles the standard which is followed by the linkedin in considering th certain skills as actual skill-sets.
compare the skills mentioned in the resume and the job description and list down the skills which are present in the resume but not in the job description.

Resume Skills: \n{resume_skill}
Job Description Skills: \n{job_descr_skill}

Provide the response in the below format:

"C Programming Language
Python Programming Language
Java Programming Language
Network Programming using Python
Discrete Mathematics (DSA)
HTML
CSS (Vanilla & Frameworks)
JavaScript
Node.js
Express.js
SQL Database Management System
MongoDB NoSQL Database Management System
React.js JavaScript Library
Microsoft Office Suite (Word, Excel, PowerPoint, Project)"
"""
extra_skill_response = chat_session.send_message(extra_prompt)
extra_skill = extra_skill_response.text
extra_skills_set = set(skill.strip() for skill in extra_skill.split("\n") if skill.strip())

matched_prompt = f"""
Consider the standard that resembles the standard which is followed by the linkedin in considering th certain skills as actual skill-sets.
compare the skills mentioned in the resume and the job description and list down the skills which are present in both the resume and also in the job description.

Resume Skills: \n{resume_skill}
Job Description Skills: \n{job_descr_skill}

Provide the response in the below format:

"C Programming Language
Python Programming Language
Java Programming Language
Network Programming using Python
Discrete Mathematics (DSA)
HTML
CSS (Vanilla & Frameworks)
JavaScript
Node.js
Express.js
SQL Database Management System
MongoDB NoSQL Database Management System
React.js JavaScript Library
Microsoft Office Suite (Word, Excel, PowerPoint, Project)"
"""
matched_skill_response = chat_session.send_message(matched_prompt)
matched_skill = matched_skill_response.text
matched_skills_set = set(skill.strip() for skill in matched_skill.split("\n") if skill.strip())

def compare_skills(matched_skills_set, job_descr_skill_set):
    return round((len(matched_skills_set) / len(job_descr_skill_set)) * 100, 2)
    
percentage_match = compare_skills(matched_skills_set, job_descr_skill_set)

print(json.dumps(list(resume_skills_set)))
print(json.dumps(list(job_descr_skill_set)))
print(json.dumps(list(lack_skills_set)))
print(json.dumps(list(extra_skills_set)))
print(json.dumps(list(matched_skills_set)))
print(json.dumps(percentage_match))
