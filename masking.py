import re
import spacy
import random
import string
from util import extract_text_from_pdf

# Load the English NLP model
nlp = spacy.load('en_core_web_sm')
pdf = './resume.pdf'
resume = extract_text_from_pdf(pdf)
print(resume)

def mask_sensitive_data(text):
    # Mask email addresses
    masked_text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', text)
    # Mask phone numbers
    masked_text = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '[PHONE]', masked_text)        
    return masked_text


# Function to generate a random name
def generate_random_name():
    return ''.join(random.choices(string.ascii_letters, k=10))

# Function to extract the first name from a resume
def extract_name(resume):
    doc = nlp(resume)
    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            return ent.text
    return None

# Function to anonymize a name in a resume
def anonymize_name(resume, original_name, random_name):
    return resume.replace(original_name, random_name)

# Function to de-anonymize a name in a response
def deanonymize_name(response, original_name, random_name):
    return response.replace(random_name, original_name)


# Extract the name from the resume
# original_name = extract_name(resume)

# # Generate a random name
# random_name = generate_random_name()

# # Anonymize the name in the resume
# anonymized_resume = anonymize_name(resume, original_name, random_name)

# # Send the anonymized resume to OpenAI and get a response
# # This is a placeholder. Replace it with the actual method of getting the response.
# response = "..."  # replace with the actual response

# # De-anonymize the name in the response
# deanonymized_response = deanonymize_name(response, original_name, random_name)

# # Print the deanonymized response
# print(deanonymized_response)

# Example usage
# resume_text = "Contact me at jane.doe@example.com or 555-123-4567."
# masked_resume = mask_sensitive_data(resume_text)
# print(masked_resume)