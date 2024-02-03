from llm import GPT4QAModel
import json
import PyPDF2
import numpy as np


model = GPT4QAModel()

def get_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ''
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text

def match_resumes_with_projects(resumes, project_descriptions):
    # Assuming resumes and project_descriptions are lists of strings
    allResumes = "Here is a list of resumes: \n"
    count = 1
    for resume in resumes:
        addThis = str(count) + ". " + resume + "\n"
        allResumes += addThis
        count += 1

    count = 1
    allProjects ="\nHere is a list of projects: \n"
    for project in project_descriptions:
        addThis = str(count) + ". " + project + "\n"
        allProjects += addThis
        count += 1
    prompt = allResumes + allProjects + "\nBased on these resumes and project descriptions, match each person to the best suited project."
    response = model.answer_question(prompt)
    print(prompt)
    print("ligma")
    #response = json.loads(response)
    return response

resume = get_text_from_pdf("/Users/royyuan/Desktop/resumes/oliviagreen.pdf")
print(resume)