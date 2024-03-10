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






client = OpenAI(
            api_key = os.environ.get('OPENAI_API_KEY')
        )

def get_embedding(text, model="text-embedding-3-small"):
    text = text.replace("\n", " ")
    embedding = client.embeddings.create(input=[text], model=model).data[0].embedding
    return embedding

def get_employee_embedding(employee):
  if employee:
    #employee_embedding = np.fromstring(employee.embedding[1:-1], sep=' ')  # Convert the string back to a NumPy array
    employee_embedding = json.loads(employee.embedding_list)
    return employee_embedding
  return None

def get_project_embedding(project):
  if project:
    #proj_embedding = np.fromstring(project.embedding[1:-1], sep=' ')  # Convert the string back to a NumPy array
    proj_embedding = json.loads(project.embedding_text)
    return proj_embedding
  return None

def get_embedding_list(resume_text):
  response = client.chat.completions.create(
          model = "gpt-3.5-turbo",
          messages=[
                {"role": "system", "content": "You are an expert at resume parsing"},
                {"role": "user", "content": f"You are an expert at parsing resumes. I want you to take the following resume text and divide it into no more than 10 chunks.It is okay to have less than 10, but not more. I want each event in the person's life to be its own chunk, whether it is a project or a job experience. Don't include the name and contact information. Make sure different job experiences and different projects are different chunks, even if they are under the same section. Please make the output a python list, where each element of the list is a string consisting of the text corresponding to the relevant chunk. Make the output a python list that I can readily use in my code. There should not be any text in the output other than this python list. Don't include '''python at the beginning of your output. Do not omit any part of the resume, make sure every line of the resume is included in a chunk. Here is an example of the output I want: ['Experience 1...', 'Experience 2...', 'Experience 3...', etc...]. Here is the resume text: {resume_text}"}
            ],
          temperature=0)
  wanted_list = response.choices[0].message.content
  print(f"Output: {wanted_list}")
  wanted_list = ast.literal_eval(wanted_list)

  emb_list = []
  for experience in wanted_list:
    exp_embedding = get_embedding(experience)
    emb_list.append(exp_embedding)
  return emb_list




def get_5_best_employees_for_project(embedding, user):
  best_similarity = -1
  best_employee= None
  
  project_embedding_np = np.array(embedding)
  
  #project = Project.query.get(project_id)
  similarity_scores = []
  for employee in user.employees:
      resume_embedding_list = get_employee_embedding(employee)
      if resume_embedding_list is not None:
          similarity = similarity_metric(resume_embedding_list, project_embedding_np)
          print(similarity)
          similarity_scores.append((employee, similarity))
          similarity_scores.sort(key=lambda x: x[1], reverse=True)
          similarity_scores = similarity_scores[:5]
  best_employees = []
  for item in similarity_scores:
      best_employees.append(item[0])
  print(best_employees)
  print(similarity_scores)
  return best_employees
  

def similarity_metric(resume_embeddings, project_embedding):
  similarity_values = []
  for exp_emb in resume_embeddings:
    exp_emb_np = np.array(exp_emb)
    similarity_values.append(cos_similarity(exp_emb_np, project_embedding))
  sorted_sums = sorted(similarity_values, reverse=True)

  largest1 = sorted_sums[0]
  largest2 = sorted_sums[1]
  print(f"largest:{largest1}")
  print(f"Second Largest: {largest2}")
  return (2*largest1 + largest2)/3

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



def get_reason(best_employee, project):
  model = GPT4QAModel(model="gpt-3.5-turbo")
  prompt = f'''You are an expert hiring manager. The title of the project you are hiring for is {project.title}, and its description is {project.description}.
  Here is the resume of the person you have chosen for this project: {best_employee.resume_text}. In at most 3 sentences, tell me why this person is a good fit for the role.'''
  reason = model.answer_question(prompt)
  return reason

def llm_best_out_of_5(best_employees, new_project):
  model = GPT4QAModel()
  curr_best_employee = best_employees[0]
  print(f"Starting Best Employee: {curr_best_employee.name}")
  for i in range(1, len(best_employees)):
    curr_employee = best_employees[i]
    print(f"Considering employee: {curr_employee.name}")
    curr_best_employee_resume = curr_best_employee.resume_text
    curr_resume =curr_employee.resume_text

    prompt = f'''You are an expert hiring manager. The title of the project you are hiring for is {new_project.title}, and its description is {new_project.description}.
    We have used an automated algorithm to find the top 5 most promising candidates for the role. Here is the resume of the employee that our automated algorithm thinks is best suited for the role: {curr_best_employee_resume}. Here is the resume of a new employee that you are considering:
    {curr_resume}. Do you think this new employee is better suited for this project than the employee you currently think is best? Consider the experience, merits, and skills of the two employees. Objectively make a decision on who you think will do a better job on this project. Is the new employee better than the current best employee? Output either "Yes" or "No", nothing else.'''
    res = model.answer_question(prompt)
    if "yes" in res.lower():
       curr_best_employee = curr_employee
    print(f"New best employee: {curr_best_employee.name}")
  
  reason = get_reason(curr_best_employee, new_project)
  return curr_best_employee, reason
  
def update_projects_best_employees(new_employee, db):
  model = GPT4QAModel()
  resume_embedding_list = get_employee_embedding(new_employee) 
  for project in Project.query.all():
    project_emb = get_project_embedding(project)
    project_emb_np = np.array(project_emb)
    curr_similarity_metric = similarity_metric(resume_embedding_list, project_emb_np)

    if curr_similarity_metric > 0.25:
      curr_best_employee = Employee.query.get(project.best_employee_id)
      curr_best_resume_text = curr_best_employee.resume_text
      new_resume_text = new_employee.resume_text
      prompt = f'''You are an expert hiring manager. The title of the project you are hiring for is {project.title}, and its description is {project.description}.
      You previously made made a decision about the best employee for this project. Here is the resume of the employee that you originally thought is best suited for this role: {curr_best_resume_text}. Here is the resume of a new employee that you are considering:
      {new_resume_text}. Do you think this new employee is better suited for this project than the employee you currently think is best? Consider the experience, merits, and skills of the two employees. Objectively make a decision on who you think will do a better job on this project. Is the new employee better than the current best employee? Output either "Yes" or "No", nothing else.'''
      res = model.answer_question(prompt)

      if "yes" in res.lower():
        project.best_employee_id = new_employee.id
        project.best_employee_name = new_employee.name
        project.best_employee_reason = get_reason(new_employee, project)
        db.session.commit()


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