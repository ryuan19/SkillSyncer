from tenacity import retry, stop_after_attempt, wait_random_exponential
from llm import GPT4QAModel
from PyPDF2 import PdfReader
import numpy as np
import os
import json
from json.decoder import JSONDecodeError
from tqdm import tqdm
from PyPDF2.errors import PdfReadError
from InstructorEmbedding import INSTRUCTOR
from models import User, Employee, Project
from openai import OpenAI
import ast
# from app import db




myModel = INSTRUCTOR('hkunlp/instructor-xl')
client = OpenAI(
            api_key = os.environ.get('OPENAI_API_KEY')
        )

def get_employee_embedding(employee):
  if employee:
    employee_embedding = np.fromstring(employee.embedding[1:-1], sep=' ')  # Convert the string back to a NumPy array
    return employee_embedding
  return None

def get_project_embedding(project):
  if project:
    proj_embedding = np.fromstring(project.embedding[1:-1], sep=' ')  # Convert the string back to a NumPy array
    return proj_embedding
  return None

def get_embedding_list(resume_text):
  response = client.chat.completions.create(
          model = "gpt-3.5-turbo",
          messages=[
                {"role": "system", "content": "You are an expert at resume parsing"},
                {"role": "user", "content": f"You are an expert at parsing resumes. I want you to take the following resume text and divide it into no more than 10 chunks.It is okay to have less than 10, but not more. I want each event in the person's life to be its own chunk, whether it is a project or a job experience. Don't include the name and contact information. Make sure different job experiences and different projects are different chunks, even if they are under the same section. Please make the output a python list, where each element of the list is a string consisting of the text corresponding to the relevant chunk. Make the output a python list that I can readily use in my code. There should not be any text in the output other than this python list. Here is an example of the output I want: ['Experience 1...', 'Experience 2...', 'Experience 3...', etc...]. Here is the resume text: {resume_text}"}
            ],
          temperature=0)
  wanted_list = response.choices[0].message.content
  wanted_list = ast.literal_eval(wanted_list)

  emb_list = []
  for experience in wanted_list:
    exp_embedding = get_embedding_from_resume(experience)
    emb_list.append(exp_embedding)
  return emb_list

def similarity_metric(resume_embeddings, project_embedding):
  similarity_values = []
  for exp_emb in resume_embeddings:
    similarity_values.append(cos_similarity(exp_emb, project_embedding))
  sorted_sums = sorted(similarity_values, reverse=True)

  largest1 = sorted_sums[0]
  largest2 = sorted_sums[1]

  return largest1 + largest2

def get_embedding_from_resume(resume_text):
  resume_instruction = [["Represent the employee resume document for retrieving suitable projects: ",resume_text]]
  embedding_resume = myModel.encode(resume_instruction)
  return embedding_resume[0]

def get_embedding_from_project(project_text):
  project_instruction = [["Represent the project description for retrieval: ", project_text]]
  embedding_project = myModel.encode(project_instruction)
  return embedding_project[0]

def cos_similarity(embedding_resume, embedding_project):
  similarity = np.dot(embedding_resume, embedding_project) / (np.linalg.norm(embedding_resume) * np.linalg.norm(embedding_project))
  return similarity

def extract_text_from_pdf(pdf_file):
    pdf_text = ""
    pdf_reader = PdfReader(pdf_file)
    for page in pdf_reader.pages:
        pdf_text += page.extract_text()
    return pdf_text

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pdf'}

def summarize_resume(resume_text):
    # Change later
    prompt = '''You are a data retriever. I will give you a resume, and I want you to summarize it.
    I want you to output a python dictionary, with the keys - name, summary, skills, hobbies, jobs.
    For name, extract the name and add it.
    For summary, give me a short 100 word summary of the whole resume and the person.
    For skills, list out skills they are good at.
    For hobbies, list of hobbies if they have, or else just write None.
    For jobs, list of 5 job titles that you think this person may be suitable for.
    Here is the resume:
    '''
    print(f"Resume Text: {resume_text}")
    prompt += resume_text
    model = GPT4QAModel()
    response = model.answer_question(prompt)
    print(f"response: {response}")
    response = json.loads(response)
    name = str(response['name'])
    summary = str(response['summary'])
    skills = str(response['skills'])
    hobbies = str(response['hobbies'])
    jobs = str(response['jobs'])
    return name, summary, skills, hobbies, jobs

def update_best_employees(employee):
    for project in Project.query.all():
        project_embedding = np.fromstring(project.embedding[1:-1], sep=' ')
        curr_best_employee = Employee.query.get(project.best_employee_id)
        curr_best_employee_embedding = np.fromstring(curr_best_employee.embedding[1:-1], sep=' ')
        employee_embedding = np.fromstring(employee.embedding[1:-1], sep=' ')
        if cos_similarity(employee_embedding, project_embedding) > cos_similarity(curr_best_employee_embedding, project_embedding):
            project.best_employee_id = employee.id
            project.best_employee_name = employee.name

def update_best_employees_llm_actuallyupdate(currguy, newguy, proj, db):
    model = GPT4QAModel()
    best_employee_prompt = "Here is some information about the best employee so far: \n" + makeEmployeePrompt(currguy) + "\n\n"
    curr_employee_info = makeEmployeePrompt(newguy) #is actually the new guy
    curr_employee_prompt = "Now, here is some information about the new employee we are evaluating: \n"+ curr_employee_info + "\n\n"
    prompt = "Imagine you are a recruiter and you want to hire the best talent possible. You are looking at the best employee currently and a new employee applying for the postion. The new employee may or may not be better than the curent best employee.\n"
    proj_prompt = "Here is some information about the project:\nProject Title: "+proj.title + "\nProject Description: "+proj.description + "\n\n"
    end = "Looking at the current best employee and new employee applying, is the new employee better suited for this project compared to the current best employee? Output either \"Yes\" or \"No\". "

    fullprompt = prompt + proj_prompt + best_employee_prompt + curr_employee_prompt + end
    res = model.answer_question(fullprompt)
    print("starthere2")
    print(fullprompt)
    printstr = "update_best_employees_llm_actuallyupdate : " + res
    print(printstr)
    if "yes" in res.lower(): #replace
        print("update replace\n")
        replace_prompt = best_employee_prompt + "Now, here is information about " + newguy.name + " who is a better candidate: \n" + curr_employee_info
        replace_prompt += proj_prompt
        replace_prompt += "\n Why is " + newguy.name + " the best suited candidate to this project? Respond in one to two sentences why " + newguy.name + "is the best candidate for this job."
        reason = model.answer_question(replace_prompt)
        proj.best_employee_id = newguy.id
        proj.best_employee_name = newguy.name
        proj.best_employee_reason = reason
        db.session.commit() #update the reason


def update_best_employees_llm(new_employee, db):
    print("batman")
    for project in Project.query.all():
        curr_best_employee = Employee.query.get(project.best_employee_id) #guy must be in database
        if curr_best_employee is not None:
          update_best_employees_llm_actuallyupdate(curr_best_employee,new_employee, project, db)


def get_best_employee_id_name_for_project(embedding):
  best_similarity = -1
  best_employee= None

  #project = Project.query.get(project_id)
  for employee in Employee.query.all():
    employee_embedding = get_employee_embedding(employee)
    if employee_embedding is not None:
        similarity = cos_similarity(embedding, employee_embedding)
        if similarity > best_similarity:
            best_similarity = similarity
            best_employee= employee
  return best_employee.id, best_employee.name

def makeEmployeePrompt(employee):
    temp1 = "Name: " + employee.name
    temp2 = "\nID: " + str(employee.id)
    temp3 = "\nUser ID: " + str(employee.user_id)
    temp4 = "\nSummary: " + employee.summary
    temp5= "\nHobbies: " + employee.hobbies
    temp6 = "\nJobs: " +  employee.jobs
    temp7 = "\nSkills: " + employee.skills
    return temp1+temp2+temp3+temp4+temp5+temp6 +temp7

def llm_get_best_employee_id_name_for_project(new_project):
    model = GPT4QAModel()
    best_employee = None
    first = True
    reason = ""
    for employee in Employee.query.all():
        if first or best_employee is None: #set best employee to first one
            best_employee = employee
            first = False
            best_employee_prompt = "Here is some information about the employee in this role: \n" + makeEmployeePrompt(best_employee) + "\n\n"
            best_employee_prompt += "Why is this person suited for the role? Answer in one to two sentences."
            reason = model.answer_question(best_employee_prompt)
        else:
            best_employee_prompt = "Here is some information about the best employee so far: \n" + makeEmployeePrompt(best_employee) + "\n\n"
            curr_employee_info = makeEmployeePrompt(employee)
            curr_employee_prompt = "Now, here is some information about the new employee we are evaluating: \n"+ curr_employee_info + "\n\n"
            prompt = "Imagine you are a recruiter and you want to hire the best talent possible. You are looking at the best employee currently and a new employee applying for the postion. The new employee may or may not be better than the curent best employee.\n"
            proj_prompt = "Here is some information about the project:\nProject Title: "+new_project.title + "\nProject Description: "+new_project.description + "\n\n"
            end = "Looking at the current best employee and new employee applying, is the new employee better suited for this project compared to the current best employee? Output either \"Yes\" or \"No\". "

            fullprompt = prompt + proj_prompt + best_employee_prompt + curr_employee_prompt + end

            res = model.answer_question(fullprompt)
            print(employee.name, "Is this person better?:", res)
            if "yes" in res.lower(): #replace
                print("inhere\n")
                best_employee = employee
                replace_prompt = "Now, here is information about " + employee.name + " who is a better candidate: \n" + curr_employee_info
                replace_prompt += proj_prompt
                replace_prompt += "\n Why is " + employee.name + " the best suited candidate to this project? Respond in one to two sentences why " + employee.name + "is the best candidate for this job."
                reason = model.answer_question(replace_prompt)

    return best_employee, reason

def main():

    # prompt = "Hello, world!"
    # model = GPT4QAModel()
    # response = model.answer_question(prompt)
    # print(f"response: {response}")
    pass

    prompt = "Hello, world!"
    model = GPT4QAModel()
    response = model.answer_question(prompt)
    print(f"response: {response}")
    # pass



if __name__ == "__main__":
    main()