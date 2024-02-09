from tenacity import retry, stop_after_attempt, wait_random_exponential
from llm import GPT4QAModel
from PyPDF2 import PdfReader
import numpy as np
import os
import json
from json.decoder import JSONDecodeError
from tqdm import tqdm
from PyPDF2.errors import PdfReadError

import pandas as pd
import requests
import base64
import csv


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
    prompt += resume_text
    model = GPT4QAModel()
    response = model.answer_question(prompt)
    response = json.loads(response)

    name = str(response['name'])
    summary = str(response['summary'])
    skills = str(response['skills'])
    hobbies = str(response['hobbies'])
    jobs = str(response['jobs'])
    return name, summary, skills, hobbies, jobs

def usegpt4v(api_key0, prompt0, image_path0):
  #encode img
  def encode_image(image_path0):
    with open(image_path0, "rb") as image_file:
      return base64.b64encode(image_file.read()).decode('utf-8')

  # get base64 string
  base64_image = encode_image(image_path0)

  headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key0}"
  }

  payload = { #can change hyperparams here
    "model": "gpt-4-vision-preview",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": prompt0
          },
          {
            "type": "image_url",
            "image_url": {
              "url": f"data:image/jpeg;base64,{base64_image}"
            }
          }
        ]
      }
    ],
    "max_tokens": 300
  }

  response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
  resjson = response.json()
  return resjson['choices'][0]['message']['content']

def readcsv(path):
   df = pd.read_csv(path)

def print_kaggle_csv(path):
    file=open(path, "r")
    reader = csv.reader(file)
    for line in reader:
        t=line[0],line[1]
        print(t)



def main():
    # Load the CSV file into a DataFrame
    pass

if __name__ == "__main__":
    main()
